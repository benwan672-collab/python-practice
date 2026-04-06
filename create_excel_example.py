import pandas as pd
from datetime import datetime

print("🌟 Yuki 的小海綿 - 建立新Excel範例 🌟")
print("=" * 60)

# 步驟1：先準備資料（可以用字典或列表）
data = {
    '月份': ['2026-03', '2026-04', '2026-05'],
    '業務部營收': [150000, 180000, 210000],
    '行銷成本': [30000, 35000, 40000],
    '轉換客戶數': [45, 60, 78]
}

# 步驟2：把資料變成 DataFrame（pandas 的表格）
df = pd.DataFrame(data)

print("✅ 資料準備完成，預覽：")
print(df)

# 步驟3：建立新的 Excel 檔案（這就是「建立Excel」的關鍵一行）
excel檔名 = f"跨部門月報_{datetime.now().strftime('%Y%m%d')}.xlsx"

df.to_excel(excel檔名, index=False, sheet_name='月報總表')

print(f"\n🎉 新Excel已成功建立！檔案名稱：{excel檔名}")
print("你可以在資料夾裡找到它，直接用Excel打開看看～")