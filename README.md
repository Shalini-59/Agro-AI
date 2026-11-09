# 🌱 Agro AI – Agricultural Market Price Intelligence Platform

Agro AI is a web-based agricultural market price platform designed to help farmers and purchasers access, compare, and understand agricultural commodity prices across different market locations.

The platform combines market price management, location-based price comparison, and experimental machine learning-based price estimation in one application.

## 🚀 Key Features

### 👨‍🌾 Farmer Dashboard
- View available agricultural market prices.
- Filter prices by product, location, and date.
- Sort prices from low to high or high to low.
- Access experimental AI price estimation.

### 🛒 Purchaser Dashboard
- View market prices across locations.
- Compare prices for different agricultural products.
- Filter and sort market price records.

### 🔐 Admin Dashboard
- Add and manage agricultural products.
- Add market locations.
- Enter and update market prices.
- Prevent duplicate price records for the same product, location, and date.

### 🤖 AI Price Estimation
- Uses historical mandi market data.
- Includes data preprocessing and model comparison.
- Explores machine learning approaches for price estimation.

**Important:** The current experimental prediction uses historical Tomato price data from Dahod APMC, Gujarat. It is not a live market price or a validated Chennai market forecast.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS |
| Database | MySQL |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Matplotlib |
| Model Storage | Joblib |
| Version Control | Git, GitHub |

## 📁 Project Structure

```text
Agro-AI/
├── dataset/
├── models/
├── static/
├── templates/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shalini-59/Agro-AI.git
cd Agro-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=agro_ai
SECRET_KEY=your_secret_key
```

### 5. Configure MySQL

Create a MySQL database named `agro_ai` and configure the required tables.

### 6. Run the application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

## 📊 Dataset Information

The machine learning experiments use historical agricultural market data from Gujarat.

- Original dataset: Bharat Mandi historical data.
- Selected commodity: Tomato.
- Selected market: Dahod APMC.
- Price unit: Indian Rupees per quintal.

The large original and cleaned CSV datasets are not included in this GitHub repository because of their file size. The selected smaller dataset and supporting analysis files are included.

## 🔒 Security

- Database credentials are stored in environment variables.
- Flask secret key is loaded from `.env`.
- `.env` and the virtual environment are excluded using `.gitignore`.

## 🔮 Future Enhancements

- Integration with verified live agricultural market price APIs.
- Expansion to multiple commodities and market locations.
- Improved time-series forecasting.
- More accurate location-specific price predictions.
- Deployment to a cloud platform.

## 👩‍💻 Author

**Shalini**  
B.Tech – Artificial Intelligence and Data Science

GitHub: [Shalini-59](https://github.com/Shalini-59)

---

*Agro AI – Empowering agricultural decisions through data and technology.*
