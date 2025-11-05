# 🏢 Company Pulse – Real-Time Business Intelligence Dashboard

### 💡 Overview
Company Pulse is a real-time BI dashboard that streams and visualizes company KPIs—sales, transactions, and customer sentiment—in live time.  
It integrates predictive analytics via Prophet to forecast future sales performance.

---

### ⚙️ Tech Stack
- **Python 3.13**
- **Streamlit** for interactive dashboard
- **Plotly Express** for visualization
- **Pandas / DuckDB** for data processing
- **Prophet** for forecasting
- **TextBlob** for sentiment generation

---

### 🧠 Features
✅ Real-time simulated data feed (5-second interval)  
✅ Live KPI cards and sentiment tracking  
✅ Automatic refresh every 5 seconds  
✅ Prophet forecasting for next-hour sales  
✅ Modular architecture (stream → ETL → dashboard)

---

### 🚀 How to Run
```bash
# 1. Clone repository
git clone https://github.com/CalebM2000/company_pulse.git
cd company_pulse

# 2. Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start data stream
python3 src/stream_producer.py

# 5. Launch dashboard
streamlit run src/dashboard_app.py
