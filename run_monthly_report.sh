#!/bin/bash
echo "🌟 啟動 Yuki 的跨部門月報工具 🌟"

# 自動啟動虛擬環境並執行
source venv/bin/activate
python monthly_report.py

echo "✅ 執行完成！請查看產生的 Excel 和 PNG 檔案～"