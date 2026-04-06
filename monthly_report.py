import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

print("🌟 Yuki 的小海綿 - 跨部門月報自動化工具 🌟")
print("=" * 70)

# ==================== 步驟2：讀取三個部門的 CSV ====================
print("正在讀取三個部門的資料...")

sales_df = pd.read_csv('業務部_sales.csv')
marketing_df = pd.read_csv('行銷部_campaign.csv')
finance_df = pd.read_csv('財務部_expense.csv')

print(f"✅ 業務部資料：{len(sales_df)} 筆")
print(f"✅ 行銷部資料：{len(marketing_df)} 筆")
print(f"✅ 財務部資料：{len(finance_df)} 筆")

# ==================== 步驟3：用 merge 把資料合併 ====================
# 先把業務部和行銷部合併（用「月份」當關鍵字）
merged_df = pd.merge(sales_df, marketing_df, on='月份', how='outer')

# 再把財務部合併進來
merged_df = pd.merge(merged_df, finance_df, on='月份', how='outer')

print("\n✅ 三個部門資料已成功合併！預覽：")
print(merged_df)

# ==================== 步驟4：計算 KPI ====================
merged_df = merged_df.sort_values('月份')  # 按月份排序

merged_df['總營收'] = merged_df['營收']
merged_df['總成本'] = merged_df['成本'] + merged_df['固定成本'] + merged_df['其他費用']
merged_df['淨利'] = merged_df['總營收'] - merged_df['總成本']

# 成長率（本月比上月）
merged_df['營收成長率(%)'] = merged_df['總營收'].pct_change() * 100

# 行銷成本佔比
merged_df['行銷成本佔比(%)'] = (merged_df['成本'] / merged_df['總營收']) * 100

print("\n✅ KPI 計算完成！完整表格：")
print(merged_df)

# ==================== 步驟5：輸出 Excel + 畫折線圖 ====================
today = datetime.now().strftime('%Y%m%d')
output_file = f"跨部門月報_{today}.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    merged_df.to_excel(writer, sheet_name='月報總表', index=False)

print(f"\n🎉 Excel 已成功輸出！檔案名稱：{output_file}")

# 畫簡單折線圖
plt.figure(figsize=(10, 6))
plt.plot(merged_df['月份'], merged_df['總營收'], marker='o', label='總營收', linewidth=2)
plt.plot(merged_df['月份'], merged_df['總成本'], marker='s', label='總成本', linewidth=2)
plt.plot(merged_df['月份'], merged_df['淨利'], marker='^', label='淨利', linewidth=2)
plt.title('2026 年跨部門營收與成本趨勢')
plt.xlabel('月份')
plt.ylabel('金額 (元)')
plt.legend()
plt.grid(True)
plt.savefig('月報趨勢圖.png')
plt.show()

print("✅ 趨勢圖已儲存為 月報趨勢圖.png")

print("\n🎊 恭喜我的小海綿！第一個跨部門月報工具完成啦～")