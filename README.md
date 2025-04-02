# 📉 BLS Layoff Forecasting (T3 & T7)

This project uses data from the **Bureau of Labor Statistics (BLS)** to forecast layoffs using time series modeling with Facebook Prophet. It includes two components:

- **T3**: Forecasting by demographic groups (e.g. age, gender, race/ethnicity)
- **T7**: Forecasting by industry and occupational categories

---

## 📊 Data Sources

### 🔹 BLS Table 3 (T3) – Demographic Forecasting
Forecasts layoffs by:
- Gender
- Race and Ethnicity
- Age Group

**File**: `bls-T3.xlsx`

---

### 🔸 BLS Table 7 (T7) – Industry & Occupation Forecasting
Forecasts layoffs by:
- Occupational Categories (e.g. Healthcare, Manufacturing)
- Industry Sectors (e.g. Government, Durable Goods)

**File**: `bls-T7.xlsx`

---

## ⚙️ How to Run

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Run the forecast:

```bash
python scripts/forecast_layoffs.py
```

3. **Check the outputs/prediction_plots/ directory for the generated plots.
