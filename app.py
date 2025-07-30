from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# 讀取 Excel
df = pd.read_excel('data.xlsx', dtype=str)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        machine_id = data.get('machine_number', '').strip().upper()

        # 模糊查詢（以輸入值開頭）
        result = df[df['收銀機編號'].str.startswith(machine_id)]

        if result.empty:
            return jsonify({'result': '查無資料'})

        row = result.iloc[0]
        fields = [
            '收銀機編號', '機台屬性', '裝設中信卡機', '裝設聯信卡機', '裝設悠遊卡機',
            'SC後台IP', 'POS機台IP', '子網路遮罩', '預設閘道'
        ]

        output = '\n'.join(f"{field}: {row.get(field, '')}" for field in fields)
        return jsonify({'result': output})

    except Exception as e:
        print(f'錯誤: {e}')
        return jsonify({'result': '查詢失敗，請稍後再試。'})

if __name__ == '__main__':
    app.run(debug=True)
