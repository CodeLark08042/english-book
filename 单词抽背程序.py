import pandas as pd
import random
import time
from collections import defaultdict

class VocabularyQuizzer:
    def __init__(self, excel_path):
        """
        单词抽背程序初始化
        
        Args:
            excel_path (str): Excel文件路径
        """
        self.excel_path = excel_path
        self.vocab_data = {}  # 存储所有词汇数据
        self.selected_lists = []  # 已选择的List
        self.quiz_words = []  # 待抽背的单词列表
        self.mastered_words = []  # 已掌握的单词
        self.need_review_words = []  # 需要复习的单词
        self.quiz_history = []  # 抽背历史
        
        # 初始化：读取并解析数据
        print("=" * 60)
        print("          绿皮书单词抽背程序          ")
        print("=" * 60)
        self.load_and_parse_data()
    
    def load_and_parse_data(self):
        """读取并解析Excel文件中的词汇数据"""
        try:
            # 读取Excel文件
            df = pd.read_excel(self.excel_path)
            df.columns = ['序号', '单词', '释义']
            
            # 解析数据，按List分组
            current_list = None
            current_words = []
            
            for idx, row in df.iterrows():
                序号 = str(row['序号']).strip() if pd.notna(row['序号']) else ''
                单词 = str(row['单词']).strip() if pd.notna(row['单词']) else ''
                释义 = str(row['释义']).strip() if pd.notna(row['释义']) else ''
                
                # 检测新的List开始
                if 'list' in 序号.lower() and 序号.lower() != 'nan':
                    # 保存之前的List
                    if current_list and current_words:
                        self.vocab_data[current_list] = current_words
                    
                    # 统一List格式
                    list_num = ''.join(filter(str.isdigit, 序号))
                    current_list = f"List {list_num}" if list_num else 序号.title()
                    current_words = []
                # 处理单词数据
                elif 序号.isdigit() and 单词 and 单词.lower() != 'nan' and 释义 and 释义.lower() != 'nan':
                    current_words.append({
                        '序号': int(序号),
                        '单词': 单词,
                        '释义': 释义,
                        '来源List': current_list,
                        '背诵次数': 0,
                        '正确次数': 0
                    })
            
            # 保存最后一个List
            if current_list and current_words:
                self.vocab_data[current_list] = current_words
            
            print(f"✅ 数据加载完成！共解析出 {len(self.vocab_data)} 个List，{sum(len(words) for words in self.vocab_data.values())} 个单词")
            print()
            
        except Exception as e:
            print(f"❌ 数据加载失败：{str(e)}")
            raise
    
    def show_list_selection(self):
        """显示List选择菜单"""
        print("📋 可用的单词List：")
        print("-" * 50)
        
        # 按List编号排序
        sorted_lists = sorted(self.vocab_data.items(), key=lambda x: int(x[0].split()[1]))
        
        # 分页显示List（每页10个）
        page_size = 10
        total_pages = (len(sorted_lists) + page_size - 1) // page_size
        current_page = 1
        
        while True:
            # 计算当前页显示的List范围
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, len(sorted_lists))
            current_page_lists = sorted_lists[start_idx:end_idx]
            
            # 显示当前页的List
            print(f"📄 第 {current_page}/{total_pages} 页")
            for i, (list_name, words) in enumerate(current_page_lists, start_idx + 1):
                print(f"  {i:2d}. {list_name:8s} - {len(words)} 个单词")
            
            # 分页控制
            print()
            print("🔧 分页操作：")
            print("   N/n - 下一页   P/p - 上一页   Q/q - 返回主菜单")
            print("   输入数字直接选择List，多个List用逗号分隔（如：1,3,5）")
            
            user_input = input("请输入操作：").strip()
            
            # 退出分页
            if user_input.lower() == 'q':
                break
            
            # 分页导航
            elif user_input.lower() == 'n' and current_page < total_pages:
                current_page += 1
                print("\n" * 20)  # 清屏效果
            
            elif user_input.lower() == 'p' and current_page > 1:
                current_page -= 1
                print("\n" * 20)  # 清屏效果
            
            # 处理List选择
            elif user_input.replace(',', '').isdigit():
                selected_nums = list(map(int, user_input.split(',')))
                valid_selected = []
                
                for num in selected_nums:
                    if 1 <= num <= len(sorted_lists):
                        list_name = sorted_lists[num - 1][0]
                        valid_selected.append(list_name)
                    else:
                        print(f"⚠️  无效的List编号：{num}（已忽略）")
                
                if valid_selected:
                    self.selected_lists = valid_selected
                    print(f"✅ 已选择List：{', '.join(valid_selected)}")
                    print(f"📊 共包含 {sum(len(self.vocab_data[list_name]) for list_name in valid_selected)} 个单词")
                    self.prepare_quiz_words()
                    break
                else:
                    print("❌ 未选择任何有效的List，请重新输入")
            
            else:
                print("❌ 无效的输入，请重新尝试")
            
            print("\n" + "-" * 50)
    
    def prepare_quiz_words(self):
        """准备抽背的单词列表"""
        self.quiz_words = []
        for list_name in self.selected_lists:
            self.quiz_words.extend(self.vocab_data[list_name])
        
        print(f"✅ 抽背单词准备完成，共 {len(self.quiz_words)} 个单词")
    
    def start_quiz(self):
        """开始单词抽背"""
        if not self.selected_lists:
            print("❌ 请先选择要抽背的List！")
            return
        
        if not self.quiz_words:
            print("❌ 没有可抽背的单词，请重新准备！")
            return
        
        print("\n" + "=" * 60)
        print("          开始单词抽背          ")
        print("=" * 60)
        print(f"🎯 抽背范围：{', '.join(self.selected_lists)}")
        print(f"📝 总单词数：{len(self.quiz_words)}")
        print()
        
        # 设置抽背参数
        while True:
            repeat_input = input("是否允许重复抽背同一单词？(Y/N，默认N)：").strip().lower()
            if not repeat_input:
                repeat_allowed = False
                break
            elif repeat_input in ['y', 'n']:
                repeat_allowed = (repeat_input == 'y')
                break
            else:
                print("❌ 无效输入，请输入 Y 或 N")
        
        quiz_count = 0
        correct_count = 0
        remaining_words = self.quiz_words.copy()
        
        print(f"\n🎮 抽背规则：允许重复={['否', '是'][repeat_allowed]}")
        print("💡 操作提示：")
        print("   按 Enter 查看释义   Q/q 退出抽背   R/r 重新开始")
        
        while True:
            if not remaining_words:
                if repeat_allowed:
                    # 允许重复时重新填充单词列表
                    remaining_words = self.quiz_words.copy()
                    print("\n🔄 所有单词已抽背一遍，重新开始...")
                else:
                    print("\n🎉 恭喜！所有单词已抽背完成！")
                    break
            
            # 随机选择一个单词
            random_word = random.choice(remaining_words)
            
            # 显示单词，等待用户查看释义
            print("\n" + "-" * 50)
            print(f"📌 第 {quiz_count + 1} 个单词")
            print(f"   单词：{random_word['单词']}")
            print(f"   来源：{random_word['来源List']}")
            
            user_action = input("   按Enter查看释义，Q退出，R重新开始：").strip().lower()
            
            if user_action == 'q':
                print("\n🛑 抽背已退出")
                break
            elif user_action == 'r':
                print("\n🔄 重新开始抽背...")
                quiz_count = 0
                correct_count = 0
                remaining_words = self.quiz_words.copy()
                continue
            
            # 显示释义
            print(f"   释义：{random_word['释义']}")
            
            # 记录背诵结果
            while True:
                result_input = input("   掌握了吗？(Y=掌握/N=未掌握，Q退出)：").strip().lower()
                if result_input in ['y', 'n', 'q']:
                    break
                print("❌ 无效输入，请输入 Y、N 或 Q")
            
            if result_input == 'q':
                print("\n🛑 抽背已退出")
                break
            
            quiz_count += 1
            random_word['背诵次数'] += 1
            
            if result_input == 'y':
                correct_count += 1
                random_word['正确次数'] += 1
                print("✅ 太棒了！继续加油！")
                # 不允许重复时，从剩余列表中移除
                if not repeat_allowed:
                    remaining_words.remove(random_word)
            else:
                print("🔄 没关系，继续努力！这个单词会继续出现")
                random_word['正确次数'] = max(0, random_word['正确次数'] - 0.5)  # 降低正确次数权重
            
            # 记录抽背历史
            self.quiz_history.append({
                '时间': time.strftime("%Y-%m-%d %H:%M:%S"),
                '单词': random_word['单词'],
                '来源List': random_word['来源List'],
                '掌握情况': '掌握' if result_input == 'y' else '未掌握'
            })
        
        # 显示抽背统计
        if quiz_count > 0:
            accuracy = (correct_count / quiz_count) * 100
            print("\n" + "=" * 60)
            print("          抽背统计报告          ")
            print("=" * 60)
            print(f"📊 总抽背次数：{quiz_count}")
            print(f"✅ 掌握单词数：{correct_count}")
            print(f"📈 掌握率：{accuracy:.1f}%")
            
            # 找出需要重点复习的单词
            review_words = [word for word in self.quiz_words if word['背诵次数'] > 0 and 
                          (word['正确次数'] / word['背诵次数']) < 0.5]
            
            if review_words:
                print(f"\n🔴 需要重点复习的单词（共 {len(review_words)} 个）：")
                for i, word in enumerate(review_words[:10], 1):  # 显示前10个
                    mastery_rate = (word['正确次数'] / word['背诵次数']) * 100
                    print(f"   {i}. {word['单词']:<15} (掌握率：{mastery_rate:.0f}%，来源：{word['来源List']})")
                if len(review_words) > 10:
                    print(f"   ... 还有 {len(review_words) - 10} 个单词需要复习")
        
        print("\n" + "=" * 60)
    
    def show_menu(self):
        """显示主菜单"""
        while True:
            print("\n" + "=" * 60)
            print("          单词抽背程序 - 主菜单          ")
            print("=" * 60)
            print(f"📋 当前选择的List：{', '.join(self.selected_lists) if self.selected_lists else '未选择'}")
            if self.selected_lists:
                total_words = sum(len(self.vocab_data[list_name]) for list_name in self.selected_lists)
                print(f"📝 可选单词数：{total_words}")
            print()
            print("1. 选择抽背的List")
            print("2. 开始单词抽背")
            print("3. 查看抽背历史")
            print("4. 重置选择的List")
            print("5. 退出程序")
            print("=" * 60)
            
            choice = input("请输入选项（1-5）：").strip()
            
            if choice == '1':
                self.show_list_selection()
            elif choice == '2':
                self.start_quiz()
            elif choice == '3':
                self.show_quiz_history()
            elif choice == '4':
                self.reset_selection()
            elif choice == '5':
                print("\n👋 感谢使用单词抽背程序，再见！")
                break
            else:
                print("❌ 无效的选项，请输入 1-5 之间的数字")
    
    def show_quiz_history(self):
        """查看抽背历史"""
        if not self.quiz_history:
            print("\n📜 暂无抽背历史记录")
            return
        
        print("\n" + "=" * 80)
        print("          抽背历史记录          ")
        print("=" * 80)
        print(f"📅 总记录数：{len(self.quiz_history)}")
        print("-" * 80)
        print(f"{'序号':<4} {'时间':<20} {'单词':<15} {'来源List':<10} {'掌握情况':<6}")
        print("-" * 80)
        
        # 显示最近的20条记录
        recent_history = self.quiz_history[-20:]
        for i, record in enumerate(recent_history, len(self.quiz_history) - len(recent_history) + 1):
            print(f"{i:<4} {record['时间']:<20} {record['单词']:<15} {record['来源List']:<10} {record['掌握情况']:<6}")
        
        if len(self.quiz_history) > 20:
            print(f"... 共 {len(self.quiz_history)} 条记录，仅显示最近20条")
        
        print("=" * 80)
    
    def reset_selection(self):
        """重置选择的List"""
        self.selected_lists = []
        self.quiz_words = []
        print("\n🔄 已重置选择的List，现在可以重新选择")

# 程序入口
if __name__ == "__main__":
    # 设置Excel文件路径（请根据实际情况修改）
    excel_file_path = "绿皮书1-50.xlsx"
    
    try:
        # 创建并运行单词抽背程序
        quizzer = VocabularyQuizzer(excel_file_path)
        quizzer.show_menu()
    except Exception as e:
        print(f"\n❌ 程序运行出错：{str(e)}")
        print("请确保Excel文件路径正确，并且文件格式符合要求")
