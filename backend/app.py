from flask import Flask, request, jsonify, render_template, redirect,url_for
from data import get_connection
from datetime import date

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template("login.html")

# LOGIN PAGE
@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")

# LOGIN SUBMIT
@app.route('/login', methods=['POST'])
def login():
    return redirect(url_for('dashboard_page'))


# ---------------- DASHBOARD PAGE (HTML) ----------------

@app.route('/dashboard-page')
def dashboard_page():
    return render_template("dashboard.html")

@app.route('/customers-page')
def customers_page():
    return render_template("customers.html")


# ---------------- DASHBOARD API (JSON) ----------------

@app.route('/dashboard', methods=['GET'])
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    # Total Customers
    cur.execute("SELECT COUNT(*) FROM customer_info")
    total_customers = cur.fetchone()[0]

    # Total Invoices
    cur.execute("SELECT COUNT(invoice_id) FROM customer_info")
    total_invoices = cur.fetchone()[0]

    # Outstanding Amount
    cur.execute("""
        SELECT COALESCE(SUM(outstanding_balance),0)
        FROM customer_info
    """)
    outstanding_amount = float(cur.fetchone()[0])

    # Overdue Invoices
    cur.execute("""
        SELECT COUNT(*)
        FROM customer_info
        WHERE days_overdue > 0
    """)
    overdue_invoices = cur.fetchone()[0]

    # High Risk Customers
    cur.execute("""
        SELECT COUNT(*)
        FROM customer_info
        WHERE credit_score < 600
    """)
    high_risk_customers = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({
        "total_customers": total_customers,
        "total_invoices": total_invoices,
        "outstanding_amount": outstanding_amount,
        "overdue_invoices": overdue_invoices,
        "high_risk_customers": high_risk_customers
    })

# ---------------- ADD CUSTOMER ----------------

@app.route('/customers', methods=['POST'])
def add_customer():

    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO customer_info
        (
            customer_name,
            invoice_amount,
            due_date,
            payment_status
        )
        VALUES (%s, %s, %s, %s)
    """, (
        data['customer_name'],
        data['invoice_amount'],
        data['due_date'],
        'Unpaid'
    ))

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Customer added successfully"
    })


# ---------------- GET CUSTOMERS ----------------

@app.route('/customers', methods=['GET'])
def get_customers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM customer_info")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)


# ---------------- MARK PAYMENT AS PAID ----------------

@app.route('/customers/<int:id>/pay', methods=['PUT'])
def mark_paid(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE customer_info
        SET payment_status='Paid',
            actual_payment_date=%s
        WHERE customer_id=%s
    """, (date.today(), id))

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Payment updated successfully"
    })


# ---------------- RUN APP ----------------

if __name__ == '__main__':
    app.run(debug=True)