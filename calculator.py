from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .calculator {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
        }
        
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 20px;
            font-size: 2em;
        }
        
        .display {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            min-height: 80px;
        }
        
        .previous-operand {
            color: rgba(255, 255, 255, 0.6);
            font-size: 1.2em;
            text-align: right;
            margin-bottom: 5px;
            min-height: 1.5em;
        }
        
        .current-operand {
            color: white;
            font-size: 2.5em;
            text-align: right;
            word-wrap: break-word;
            min-height: 1.2em;
        }
        
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        
        button {
            padding: 20px;
            font-size: 1.5em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 600;
        }
        
        button:hover {
            transform: scale(1.05);
        }
        
        button:active {
            transform: scale(0.95);
        }
        
        .number, .decimal {
            background: rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .number:hover, .decimal:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .operator {
            background: #3b82f6;
            color: white;
        }
        
        .operator:hover {
            background: #2563eb;
        }
        
        .clear {
            background: #ef4444;
            color: white;
            grid-column: span 2;
        }
        
        .clear:hover {
            background: #dc2626;
        }
        
        .delete {
            background: #f59e0b;
            color: white;
        }
        
        .delete:hover {
            background: #d97706;
        }
        
        .equals {
            background: #10b981;
            color: white;
        }
        
        .equals:hover {
            background: #059669;
        }
        
        .zero {
            grid-column: span 2;
        }
        
        .footer {
            color: rgba(255, 255, 255, 0.7);
            text-align: center;
            margin-top: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>Calculator</h1>
        <div class="display">
            <div class="previous-operand" id="previous"></div>
            <div class="current-operand" id="current">0</div>
        </div>
        <div class="buttons">
            <button class="clear" id="clearBtn">AC</button>
            <button class="delete" id="deleteBtn">DEL</button>
            <button class="operator" data-operator="÷">÷</button>
            
            <button class="number" data-number="7">7</button>
            <button class="number" data-number="8">8</button>
            <button class="number" data-number="9">9</button>
            <button class="operator" data-operator="×">×</button>
            
            <button class="number" data-number="4">4</button>
            <button class="number" data-number="5">5</button>
            <button class="number" data-number="6">6</button>
            <button class="operator" data-operator="-">-</button>
            
            <button class="number" data-number="1">1</button>
            <button class="number" data-number="2">2</button>
            <button class="number" data-number="3">3</button>
            <button class="operator" data-operator="+">+</button>
            
            <button class="number zero" data-number="0">0</button>
            <button class="decimal" data-number=".">.</button>
            <button class="equals" id="equalsBtn">=</button>
        </div>
        <div class="footer">
            Powered by Python Flask
        </div>
    </div>

    <script>
        class Calculator {
            constructor() {
                this.currentOperand = '0';
                this.previousOperand = '';
                this.operation = null;
                this.init();
            }

            init() {
                // Number buttons
                document.querySelectorAll('[data-number]').forEach(button => {
                    button.addEventListener('click', () => {
                        this.appendNumber(button.dataset.number);
                    });
                });

                // Operator buttons
                document.querySelectorAll('[data-operator]').forEach(button => {
                    button.addEventListener('click', () => {
                        this.chooseOperation(button.dataset.operator);
                    });
                });

                // Clear button
                document.getElementById('clearBtn').addEventListener('click', () => {
                    this.clearAll();
                });

                // Delete button
                document.getElementById('deleteBtn').addEventListener('click', () => {
                    this.deleteDigit();
                });

                // Equals button
                document.getElementById('equalsBtn').addEventListener('click', () => {
                    this.compute();
                });

                this.updateDisplay();
            }

            updateDisplay() {
                document.getElementById('current').textContent = this.currentOperand;
                if (this.operation) {
                    document.getElementById('previous').textContent = this.previousOperand + ' ' + this.operation;
                } else {
                    document.getElementById('previous').textContent = this.previousOperand;
                }
            }

            clearAll() {
                this.currentOperand = '0';
                this.previousOperand = '';
                this.operation = null;
                this.updateDisplay();
            }

            deleteDigit() {
                if (this.currentOperand.length > 1) {
                    this.currentOperand = this.currentOperand.slice(0, -1);
                } else {
                    this.currentOperand = '0';
                }
                this.updateDisplay();
            }

            appendNumber(number) {
                if (number === '.' && this.currentOperand.includes('.')) return;
                if (this.currentOperand === '0' && number !== '.') {
                    this.currentOperand = number;
                } else {
                    this.currentOperand += number;
                }
                this.updateDisplay();
            }

            chooseOperation(op) {
                if (this.currentOperand === '') return;
                if (this.previousOperand !== '' && this.operation !== null) {
                    this.compute();
                }
                this.operation = op;
                this.previousOperand = this.currentOperand;
                this.currentOperand = '';
                this.updateDisplay();
            }

            compute() {
                let result;
                const prev = parseFloat(this.previousOperand);
                const current = parseFloat(this.currentOperand);
                
                if (isNaN(prev) || isNaN(current)) return;
                
                switch (this.operation) {
                    case '+':
                        result = prev + current;
                        break;
                    case '-':
                        result = prev - current;
                        break;
                    case '×':
                        result = prev * current;
                        break;
                    case '÷':
                        if (current === 0) {
                            alert('Cannot divide by zero!');
                            this.clearAll();
                            return;
                        }
                        result = prev / current;
                        break;
                    default:
                        return;
                }
                
                this.currentOperand = result.toString();
                this.operation = null;
                this.previousOperand = '';
                this.updateDisplay();
            }
        }

        // Initialize calculator when page loads
        const calc = new Calculator();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🚀 Calculator is running!")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🌐 Share with others on your network using your IP address")
    print("⏹️  Press CTRL+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)