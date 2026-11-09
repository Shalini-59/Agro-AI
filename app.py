from flask import Flask, render_template, request, redirect, session
import mysql.connector
import joblib
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
price_model = joblib.load("models/gradient_boosting.pkl")
# Load historical tomato market data
tomato_history = pd.read_csv(
    "dataset/tomato_dahod.csv",
    parse_dates=["date"]
)
tomato_history = tomato_history.sort_values("date").reset_index(drop=True)
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# Load trained price prediction model
price_model = joblib.load("models/gradient_boosting.pkl")

# Connect to MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:
            session["user_id"] = user["user_id"]
            session["role"] = user["role"]
            session["name"] = user["name"]

            if user["role"] == "farmer":
                return redirect("/farmer")
            elif user["role"] == "purchaser":
                return redirect("/purchaser")
            elif user["role"] == "admin":
                return redirect("/admin")

        return "Invalid email or password"

    return render_template("login.html")
@app.route("/")
def landing():
    return render_template("home.html")


@app.route("/marketplace")
def home():
    if "user_id" not in session:
        return redirect("/login")

    selected_product = request.args.get("product")
    selected_location = request.args.get("location")
    selected_date = request.args.get("date")
    sort_order = request.args.get("sort")

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()

    query = """
        SELECT
            p.product_name,
            l.location_name,
            pr.price,
            pr.price_date
        FROM prices pr
        JOIN products p ON pr.product_id = p.product_id
        JOIN locations l ON pr.location_id = l.location_id
    """

    conditions = []
    values = []

    if selected_date:
        conditions.append("pr.price_date = %s")
        values.append(selected_date)
    else:
        conditions.append("pr.price_date = CURDATE()")

    if selected_product:
        conditions.append("p.product_name = %s")
        values.append(selected_product)

    if selected_location:
        conditions.append("l.location_name = %s")
        values.append(selected_location)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if sort_order == "low":
        query += " ORDER BY pr.price ASC"
    elif sort_order == "high":
        query += " ORDER BY pr.price DESC"
    else:
        query += " ORDER BY pr.price_date DESC, pr.price_id DESC"

    cursor.execute(query, tuple(values))

    prices = cursor.fetchall()
    cursor.close()
    
    return render_template(
        "index.html",
        prices=prices,
        products=products,
        locations=locations,
        today=pd.Timestamp.today().strftime("%Y-%m-%d")
)
@app.route("/farmer")
def farmer_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "farmer":
        return "Access Denied"

    return render_template("farmer.html")
@app.route("/purchaser")
def purchaser_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "purchaser":
        return "Access Denied"

    return render_template("purchaser.html")
@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access Denied"

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()

    cursor.close()

    return render_template(
    "admin.html",
    products=products,
    locations=locations,
    today=pd.Timestamp.today().strftime("%Y-%m-%d")
)
@app.route("/admin/add-product", methods=["POST"])
def add_product():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access Denied"
    product_name = request.form["product_name"].strip()
    category = request.form["category"].strip()
    cursor = db.cursor()
   
    cursor.execute(
        """
        INSERT INTO products (product_name, category)
        VALUES (%s, %s)
        """,
        (product_name, category)
    )

    db.commit()
    cursor.close()

    return redirect("/admin")
@app.route("/admin/add-location", methods=["POST"])
def add_location():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access Denied"

    location_name = request.form["location_name"]
    district = request.form["district"]
    state = request.form["state"]

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO locations (location_name, district, state)
        VALUES (%s, %s, %s)
        """,
        (location_name, district, state)
    )

    db.commit()
    cursor.close()

    return redirect("/admin")

@app.route("/admin/add-price", methods=["POST"])
def add_price():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access Denied"

    product_id = request.form["product_id"]
    location_id = request.form["location_id"]
    price = float(request.form["price"])
    if price <= 0:
        return "Price must be greater than 0."
    price_date = request.form["price_date"]
    today = pd.Timestamp.today().strftime("%Y-%m-%d")
    if price_date > today:
        return "Future dates are not allowed."

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO prices
        (product_id, location_id, price, price_date)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        price = VALUES(price)
        """,
        (product_id, location_id, price, price_date)
    )

    db.commit()
    cursor.close()

    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
@app.route("/predict")
def predict_price():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "farmer":
        return "Access Denied"

    if len(tomato_history) < 31:
        return "Not enough historical data for prediction."

    # Get historical prices
    prices = tomato_history["modal_price_rs_quintal"]

    # Get the last available date
    last_date = tomato_history["date"].iloc[-1]

    # Next calendar date
    next_date = last_date + pd.Timedelta(days=1)

    # Baseline estimate using the previous observation
    prediction = float(prices.iloc[-1])

    return render_template(
        "predict.html",
        prediction=round(prediction, 2),
        prediction_date=next_date.strftime("%d %B %Y"),
        latest_data_date=last_date.strftime("%d %B %Y")
    )

if __name__ == "__main__":
    app.run(debug=True)