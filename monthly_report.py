import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

print("🌟 Yuki 的小海綿 - 跨部門月報自動化工具 🌟")
print("=" * 70)
# ==================== Step 2: 讀取資料 ====================
print("正在讀取三個部門的資料...")

sales_df = pd.read_csv('業務部_sales.csv')
marketing_df = pd.read_csv('行銷部_campaign.csv')
expense_df = pd.read_csv('財務部_expense.csv')     # ← 統一用 expense_df

print(f"✅ 業務部資料：{len(sales_df)} 筆")
print(f"✅ 行銷部資料：{len(marketing_df)} 筆")
print(f"✅ 財務部資料：{len(expense_df)} 筆")

# ==================== 資料清洗區塊 ====================
print("\n🧼 開始進行資料清洗...")

# 業務部清洗
sales_df = sales_df.drop_duplicates()
sales_df['營收'] = pd.to_numeric(sales_df['營收'], errors='coerce').fillna(0)
sales_df['地區'] = sales_df['地區'].fillna('未知')

# 行銷部清洗
marketing_df = marketing_df.drop_duplicates()
marketing_df['成本'] = pd.to_numeric(marketing_df['成本'], errors='coerce').fillna(0)
marketing_df['轉換客戶數'] = pd.to_numeric(marketing_df['轉換客戶數'], errors='coerce').fillna(0)   # ← 這裡改成這樣

# 財務部清洗 + 產生「月份」欄位
expense_df['日期'] = pd.to_datetime(expense_df['日期'], errors='coerce')
expense_df['月份'] = expense_df['日期'].dt.strftime('%Y-%m')
expense_df = expense_df.drop(columns=['日期'])

print("✅ 資料清洗完成！現在所有表格都有「月份」欄位了")
# ==================== Step 4: 合併三張表 ====================
print("\n🔗 正在合併三個部門資料...")

merged_df = pd.merge(sales_df, marketing_df, on='月份', how='left')
merged_df = pd.merge(merged_df, expense_df, on='月份', how='left')

print(f"✅ 合併完成！最終資料筆數：{len(merged_df)} 筆")
print(f"✅ 合併完成！最終資料筆數：{len(merged_df)} 筆")

print("\n✅ 三個部門資料已成功合併！預覽：")
print(merged_df)

# ==================== Step 5: KPI 計算區塊（優化版） ====================
print("\n📊 開始計算 KPI...")

# 先強制把所有可能用到的數值欄位轉成數字（這是關鍵防護）
numeric_cols = ['營收', '成本', '固定成本', '其他費用', '轉換客戶戶數']

for col in numeric_cols:
    if col in merged_df.columns:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(0)

# 現在安全地計算 KPI
merged_df['總營收'] = merged_df['營收']
merged_df['總成本'] = merged_df['成本'] + merged_df['固定成本'] + merged_df['其他費用']
merged_df['淨利'] = merged_df['總營收'] - merged_df['總成本']

# 成長率計算（需要先排序）
merged_df = merged_df.sort_values('月份')
merged_df['營收成長率(%)'] = merged_df['總營收'].pct_change() * 100

# 可選：加上簡單異常提示（公司很實用）
if (merged_df['淨利'] < 0).any():
    print("⚠️  注意：本期出現淨利為負的月份，請主管特別關注！")

print("✅ KPI 計算完成！（已確保所有數值欄位安全轉型）")
print("✅ KPI 計算完成！")

# ==================== Step 6: 使用 groupby + pivot_table 做出交叉報表 ====================
print("\n📋 正在產生每月各產品 KPI 交叉分析表...")

# 先確保月份是正確排序
merged_df = merged_df.sort_values('月份')

# 使用 groupby + pivot_table 做出漂亮的交叉表
pivot_table = pd.pivot_table(
    merged_df,
    values=['總營收', '總成本', '淨利', '營收成長率(%)'],
    index='月份',           # 列 = 月份
    columns='產品',         # 欄 = 產品
    aggfunc='sum',          # 數值加總
    fill_value=0
)

# 加上總計欄
pivot_table['總計'] = pivot_table.sum(axis=1)

print("✅ 交叉分析表產生完成！")

# 輸出到 Excel 的新工作表
with pd.ExcelWriter(f"跨部門月報_{datetime.now().strftime('%Y%m%d')}.xlsx", engine='openpyxl', mode='a') as writer:
    pivot_table.to_excel(writer, sheet_name='產品交叉分析')

print("📊 已將「每月各產品 KPI 交叉表」新增到 Excel 的新工作表中")

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

# ==================== 步驟6：自動寄送月報 Email (進階功能) ====================
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_monthly_report_email():
    print("📧 準備自動寄送跨部門月報給主管...")

    # 這裡先用模擬方式（真實寄信需要你的 email 帳號密碼，之後再教你安全做法）
    excel_file = f"跨部門月報_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    print(f"✅ 月報已準備完成：{excel_file}")
    print("📨 模擬寄送給：")
    print("   - 業務主管 (sales@company.com)")
    print("   - 行銷主管 (marketing@company.com)")
    print("   - 財務主管 (expense@company.com)")
    print("🎉 月報自動寄送功能已執行！")

# 在程式結束前呼叫這個功能
send_monthly_report_email()


print("✅ 趨勢圖已儲存為 月報趨勢圖.png")

print("\n🎊 恭喜我的小海綿！第一個跨部門月報工具完成啦～")

