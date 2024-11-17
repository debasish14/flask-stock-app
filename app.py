from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Class to represent a buy/sell transaction interval
class Interval:
    def __init__(self, buy, sell):
        self.buy = buy
        self.sell = sell

def stock_buy_sell(price):
    if len(price) < 2:
        return []

    i = 0
    sol = []

    while i < len(price) - 1:
        while i < len(price) - 1 and price[i + 1] <= price[i]:
            i += 1
        if i == len(price) - 1:
            break
        buy = i
        i += 1
        while i < len(price) and price[i] >= price[i - 1]:
            i += 1
        sell = i - 1
        sol.append(Interval(buy, sell))

    return sol

def calculate_brokerage(stock_quantity, stock_price, choice):
    brokerage = 45
    total = stock_quantity * stock_price
    if choice == 'B':
        return total + brokerage
    elif choice == 'S':
        return total - brokerage
    return total

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    # Sample price data
    price = [
        100, 98, 105, 110, 120, 115, 125, 130, 140, 135, 145, 150, 155, 160,
        150, 145, 155, 165, 170, 175, 180, 190, 185, 195, 200, 210, 220, 230,
        225, 235, 240, 245, 250, 240, 230, 225, 235, 245, 250, 260, 265, 270
    ]
    
    transactions = stock_buy_sell(price)
    
    result = []
    for t in transactions:
        result.append({
            'buy_day': t.buy,
            'sell_day': t.sell,
            'buy_price': price[t.buy],
            'sell_price': price[t.sell],
            'profit': price[t.sell] - price[t.buy]
        })
    
    return render_template('analysis.html', transactions=result, prices=price)

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    data = request.form
    
    client_id = data.get('client_id')
    client_name = data.get('client_name')
    stock_name = data.get('stock_name')
    stock_quantity = int(data.get('stock_quantity'))
    stock_price = float(data.get('stock_price'))
    choice = data.get('choice')
    
    brokerage = 45
    total_stock_value = stock_quantity * stock_price
    total_with_brokerage = calculate_brokerage(stock_quantity, stock_price, choice)
    
    bill_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'client_id': client_id,
        'client_name': client_name,
        'stock_name': stock_name,
        'stock_quantity': stock_quantity,
        'stock_price': stock_price,
        'total_stock_value': total_stock_value,
        'brokerage': brokerage,
        'total_with_brokerage': total_with_brokerage,
        'transaction_type': 'Purchase' if choice == 'B' else 'Sale'
    }
    
    return render_template('bill.html', bill=bill_data)

if __name__ == '__main__':
    app.run(debug=True)