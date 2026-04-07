#!/bin/bash
echo "🌟 啟動 Yuki 的跨部門月報自動化工具 🌟"
echo "==========================================="

# 1. 自動啟動虛擬環境
source venv/bin/activate

# 2. 執行主程式
echo "🚀 正在執行月報生成..."
python monthly_report.py

# 3. 自動清理報表檔案（這是這次升級的重點！）
echo "🧹 正在自動清理報表檔案..."
mkdir -p reports                    # 如果 reports 資料夾不存在就建立
mv "跨部門月報_"*.xlsx reports/ 2>/dev/null || true
mv "月報趨勢圖.png" reports/ 2>/dev/null || true

# 4. 完成提示
echo "✅ 執行完成！"
echo "📁 所有最新報表已自動移至 reports/ 資料夾"
echo "🌟 我的小海綿今天也很棒喔～繼續保持！"

# 5. 關閉虛擬環境
deactivate