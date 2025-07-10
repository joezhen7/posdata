from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# 讀取 Excel，請確保 data.xlsx 在同目錄
df = pd.read_excel('data.xlsx', dtype=str)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    machine_id = request.form.get('machine_id', '').strip()
    if not machine_id:
        return jsonify({'error': '請輸入收銀機編號'})
    try:
        result = df[df['收銀機編號'] == machine_id]
        if not result.empty:
            row = result.iloc[0]
            fields = [
                '機台屬性', '裝設中信卡機', '裝設聯信卡機', '裝設悠遊卡機',
                'SC後台IP', 'POS機台IP', '子網路遮罩', '預設閘道'
            ]
            data = {field: row.get(field, '') for field in fields}
            return jsonify(data)
        else:
            return jsonify({'error': '查無資料'})
    except Exception as e:
        print("錯誤:", e)
        return jsonify({'error': '伺服器錯誤'})

if __name__ == '__main__':
    # 指定只監聽本機 IP，埠號 5000，並開啟除錯模式
    app.run(host='127.0.0.1', port=5000, debug=True)
