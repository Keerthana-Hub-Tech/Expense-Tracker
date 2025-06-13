from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
CSV_FILE = 'expenses.csv'

# Ensure the CSV file exists with a header
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Description', 'Amount'])

# Home page: show all expenses
@app.route('/')
def index():
    expenses = []
    total = 0

    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            expenses.append(row)
            total += float(row[2])

    return render_template('index.html', expenses=expenses, total=total)

# Add expense
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date = request.form['date']
        desc = request.form['description']
        amount = request.form['amount']

        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, desc, amount])

        return redirect(url_for('index'))

    return render_template('add.html')

# Edit expense
@app.route('/edit/<int:id>', methods=['GET', 'POST'])

def edit(id):
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if request.method == 'POST':
        rows[id + 1] = [request.form['date'], request.form['description'], request.form['amount']]  # +1 to skip header
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        return redirect(url_for('index'))

    expense = rows[id + 1]
    return render_template('edit.html', expense=expense)

# Delete expense
@app.route('/delete/<int:id>')
def delete(id):
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if 0 <= id + 1 < len(rows):
        rows.pop(id + 1)

    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
