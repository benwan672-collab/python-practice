# daily_mood.py
# Yuki 的小海綿每日心情日記 - 優化版

from datetime import datetime

print("🌟 Yuki 的小海綿每日心情日記 🌟")
print("=" * 50)

# 自動取得今天日期
today = datetime.now().strftime("%Y 年 %m 月 %d 日")
print(f"今天日期：{today}")

# 讓你輸入今天的心情
mood = input("\n今天的心情如何？（例如：開心、疲憊、有點焦慮...）：")
energy = int(input("今天能量值（0-100）："))

print(f"\n今天的心情：{mood}")
print(f"今天能量值：{energy}/100")

# 把記錄存到檔案（累積記錄）
with open("mood_history.txt", "a", encoding="utf-8") as f:
    f.write(f"{today} | 心情：{mood} | 能量：{energy}/100\n")

print("\n✅ 已把今天的心情記錄儲存到 mood_history.txt")

# 顯示今天學到的東西
print("\n今天我學會了：")
print("1. 正確設定 Python 環境")
print("2. 在新資料夾建立 Git 專案")
print("3. 寫 Python 程式並用 Git 管理版本")
print("4. 使用 input() 與檔案寫入功能")

# 給自己的鼓勵
print("\n給自己的小鼓勵：")
print("我的小海綿今天很棒！繼續跟 Yuki 一起慢慢吸收知識～❤️")
print("=" * 50)