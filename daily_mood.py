# daily_mood.py
# Yuki 的小海綿每日心情日記 - 統計加強版

from datetime import datetime
import os

print("🌟 Yuki 的小海綿每日心情日記 🌟")
print("=" * 55)

# 自動取得今天日期
today = datetime.now().strftime("%Y 年 %m 月 %d 日")
print(f"今天日期：{today}")

# 讓你輸入今天的心情與能量值
mood = input("\n今天的心情如何？（例如：開心、平穩、有點累、很有動力...）： ")
energy = int(input("今天能量值（0-100）： "))

print(f"\n今天的心情：{mood}")
print(f"今天能量值：{energy}/100")

# 把記錄存到檔案（累積記錄）
with open("mood_history.txt", "a", encoding="utf-8") as f:
    f.write(f"{today} | 心情：{mood} | 能量：{energy}\n")

print("✅ 已把今天的心情記錄儲存到 mood_history.txt")

# === 新增：簡單統計功能 ===
if os.path.exists("mood_history.txt"):
    with open("mood_history.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if len(lines) > 0:
        energies = []
        for line in lines:
            if "|" in line and "能量：" in line:
                try:
                    energy_value = int(line.split("能量：")[-1].strip())
                    energies.append(energy_value)
                except:
                    pass
        
        if energies:
            avg_energy = sum(energies) / len(energies)
            print(f"\n📊 統計摘要（共 {len(energies)} 天記錄）")
            print(f"平均能量值：{avg_energy:.1f}/100")
            print(f"最高能量：{max(energies)} | 最低能量：{min(energies)}")

# 給自己的鼓勵
print("\n💪 給自己的小鼓勵：")
print("我的小海綿今天很棒！繼續跟 Yuki 一起慢慢吸收知識～❤️")
print("=" * 55)