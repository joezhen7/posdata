from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

df = pd.read_excel('data.xlsx', dtype=str)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    machine_id = request.form.get('machine_id')
    try:
        result = df[df['收銀機編號'] == machine_id]
        if not result.empty:
            row = result.iloc[0]
            fields = [
                '機台屬性', '裝設中信卡機', '裝設聯信卡機', '裝設悠遊卡機',
                'SC後台IP', 'POS機台IP', '子網路遮罩', '預設閘道'
            ]
            data = {field: row[field] for field in fields}
            return jsonify(data)
        else:
            return jsonify({'error': '查無資料'})
    except Exception as e:
        print("錯誤:", e)
        return jsonify({'error': '伺服器錯誤'})

if __name__ == '__main__':
    app.run(debug=True)
