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


## 📸 Application Screenshots


<img width="938" height="496" alt="Screenshot 2026-11-10 102052" src="https://github.com/user-attachments/assets/bf7ab150-ba90-4c63-a565-5c77b3307140" />

### Farmer Marketplace Dashboard


<img width="1870" height="1599" alt="agro-ai-farmer-marketplace" src="https://github.com/user-attachments/assets/6007477c-1569-436a-85e7-584434bcfdde" />

### AI Price Prediction

<img width="1873" height="1405" alt="agro-ai-price-prediction" src="https://github.com/user-attachments/assets/af522939-6940-477c-bf13-91a0649d96d2" />

### Admin Dashboard
<img width="930" height="448" alt="Screenshot 2026-11-10 110530" src="https://github.com/user-attachments/assets/e27bed9d-b43e-46c0-8013-54ea1fe909b1" />
<img width="936" height="470" alt="Screenshot 2026-11-10 110633" src="https://github.com/user-attachments/assets/d91ba066-99ee-4ee9-a353-bc8aa5170c5d" />






## 👩‍💻 Author

**Shalini**  
B.Tech – Artificial Intelligence and Data Science

GitHub: [Shalini-59](https://github.com/Shalini-59)

---

*Agro AI – Empowering agricultural decisions through data and technology.*
