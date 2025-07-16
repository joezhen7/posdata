from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# 讀取 Excel
df = pd.read_excel('data.xlsx', dtype=str)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    machine_id = request.form.get('machine_id', '').strip().upper()

    # 模糊查詢（以輸入值開頭）
    result = df[df['收銀機編號'].str.startswith(machine_id)]

    if result.empty:
        return jsonify({'error': '查無資料'})

    data = result.iloc[0]

    # 查詢結果欄位（含收銀機編號在最前）
    fields = [
        '收銀機編號', '機台屬性', '裝設中信卡機', '裝設聯信卡機', '裝設悠遊卡機',
        'SC後台IP', 'POS機台IP', '子網路遮罩', '預設閘道'
    ]

    return jsonify({field: data.get(field, '') for field in fields})

if __name__ == '__main__':
    app.run(debug=True)
