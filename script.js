document.addEventListener('DOMContentLoaded', () => {
    let allWords = [];
    let currentQueue = [];
    let currentWord = null;
    let isRepeatMode = false;
    let currentIndex = 0;

    const unitSelect = document.getElementById('unit-select');
    const repeatToggle = document.getElementById('repeat-toggle');
    const resetBtn = document.getElementById('reset-btn');
    const wordText = document.getElementById('word-text');
    const wordMeaning = document.getElementById('word-meaning');
    const showAnswerBtn = document.getElementById('show-answer-btn');
    const nextBtn = document.getElementById('next-btn');
    const progressText = document.getElementById('progress-text');
    const statusMsg = document.getElementById('status-msg');

    // Load Data
    if (window.wordData) {
        allWords = window.wordData;
        populateUnits();
        initSession();
    } else {
        wordText.textContent = '数据加载失败';
        wordMeaning.textContent = '请确保 words.js 存在';
        wordMeaning.classList.remove('hidden');
    }

    // Event Listeners
    unitSelect.addEventListener('change', initSession);
    
    repeatToggle.addEventListener('change', (e) => {
        isRepeatMode = e.target.checked;
        // If switching to repeat mode, we don't necessarily need to reset, 
        // but if switching OFF repeat mode, we might want to restart or continue?
        // Let's just update the mode flag. 
        // If we are in "Finished" state and toggle repeat on, we should probably auto-start.
        if (isRepeatMode && currentQueue.length === 0 && allWords.length > 0) {
            initSession();
        }
        updateProgress();
    });

    resetBtn.addEventListener('click', initSession);

    showAnswerBtn.addEventListener('click', () => {
        wordMeaning.classList.remove('hidden');
    });

    nextBtn.addEventListener('click', () => nextWord(false));
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            // Prevent scrolling
            e.preventDefault();
            if (wordMeaning.classList.contains('hidden')) {
                wordMeaning.classList.remove('hidden');
            } else {
                nextWord();
            }
        }
    });

    function populateUnits() {
        const units = new Set(allWords.map(w => w.unit));
        // Sort units naturally (list 1, list 2, list 10 instead of list 1, list 10, list 2)
        const sortedUnits = Array.from(units).sort((a, b) => {
            const numA = parseInt(a.replace(/\D/g, '')) || 0;
            const numB = parseInt(b.replace(/\D/g, '')) || 0;
            return numA - numB;
        });

        sortedUnits.forEach(unit => {
            const option = document.createElement('option');
            option.value = unit;
            option.textContent = unit;
            unitSelect.appendChild(option);
        });
    }

    function initSession() {
        const selectedUnit = unitSelect.value;
        isRepeatMode = repeatToggle.checked;

        // Filter words
        if (selectedUnit === 'all') {
            currentQueue = [...allWords];
        } else {
            currentQueue = allWords.filter(w => w.unit === selectedUnit);
        }

        if (currentQueue.length === 0) {
            wordText.textContent = "无单词";
            return;
        }

        // Shuffle for initial order
        shuffleArray(currentQueue);
        currentIndex = 0;
        
        statusMsg.textContent = "";
        nextWord(true); // true = isFirst
    }

    function nextWord(isFirst = false) {
        if (!isFirst) {
            // If not first load, check logic
            if (!isRepeatMode) {
                currentIndex++;
            } else {
                // In repeat mode, pick a random index
                currentIndex = Math.floor(Math.random() * currentQueue.length);
            }
        }

        // Check if finished (only for non-repeat mode)
        if (!isRepeatMode && currentIndex >= currentQueue.length) {
            showFinished();
            return;
        }

        // Get word
        currentWord = currentQueue[currentIndex];
        
        // Update UI
        wordText.textContent = currentWord.word;
        wordMeaning.textContent = currentWord.meaning;
        wordMeaning.classList.add('hidden');
        
        updateProgress();
    }

    function showFinished() {
        wordText.textContent = "本组背诵完成!";
        wordMeaning.textContent = "点击重置或切换单元";
        wordMeaning.classList.remove('hidden');
        statusMsg.textContent = "🎉 完成!";
    }

    function updateProgress() {
        if (isRepeatMode) {
            progressText.textContent = `当前: ${currentWord ? currentWord.unit : '-'} (无限模式)`;
        } else {
            progressText.textContent = `进度: ${Math.min(currentIndex + 1, currentQueue.length)} / ${currentQueue.length}`;
        }
    }

    // Fisher-Yates Shuffle
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
});
