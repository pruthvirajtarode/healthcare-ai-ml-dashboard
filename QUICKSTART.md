# Quick Start Guide - Healthcare AI/ML Project

## 🚀 30-Second Quick Start

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Run the Complete Pipeline (5-10 minutes)
```bash
python run_pipeline.py
```

### Step 3: Open the Dashboard
Open `frontend/index.html` in your browser or use:
```bash
python -m http.server 8000 --directory frontend
# Then visit http://localhost:8000
```

Done! ✅

---

## 📊 What Gets Generated

After running the pipeline, you'll have:

1. **Cleaned Data**
   - `data/healthcare_data_cleaned.csv` - Patient data with all issues fixed

2. **Analysis Reports**
   - `data/eda_report.json` - Comprehensive analysis results
   - `data/kpi_report.json` - All calculated metrics
   - `data/high_risk_patients.csv` - List of at-risk patients

3. **ML Training Data**
   - `data/ml_preparation_report.json` - Model performance metrics
   - `data/ml_training_data/` - Training and test datasets

---

## 📋 Main Features to Try

### 1. **View Dashboard**
- Open `frontend/index.html` in browser
- Click through different tabs:
  - **Overview** - Key statistics
  - **Analytics** - Charts and visualizations
  - **High-Risk** - At-risk patient analysis
  - **KPIs** - Performance indicators
  - **Predictions** - ML-based risk calculator

### 2. **Run Individual Analysis Steps**
```bash
# Just clean data
python scripts/data_cleaning.py

# Just do EDA
python scripts/eda_analysis.py

# Just engineer features
python scripts/feature_engineering.py

# Just prepare ML models
python scripts/ml_preparation.py
```

### 3. **Use the Risk Prediction Tool**
- Go to "Predictions" tab in dashboard
- Enter patient health info:
  - Age, BMI, Blood Pressure, Glucose
  - Disease type, City
- Get instant risk assessment with recommendations

---

## 🔍 Key Statistics to Expect

After running pipeline:
- **Total Patients Analyzed:** 85
- **High-Risk Identified:** ~42 patients
- **Data Cleaning:** Removed/fixed ~50 invalid records
- **Features Created:** 40+ engineered features
- **ML Model Accuracy:** 85%+

---

## ⚠️ Troubleshooting

### Problem: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Problem: Empty results or "Dataset not found"
**Solution:**
1. Ensure `data/healthcare_data.csv` exists
2. Run `python run_pipeline.py` first
3. Check console for error messages

### Problem: Dashboard loads but no data shows
**Solution:**
1. Check browser console (F12) for JavaScript errors
2. Ensure all frontend files (html, css, js) are in `frontend/` folder
3. Try opening directly: `frontend/index.html` (not through HTTP)

### Problem: Plots not showing in charts
**Solution:**
- Open browser console (F12)
- Look for errors mentioning Chart.js
- Ensure Chart.js CDN is accessible (check internet connection)

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `run_pipeline.py` | Master script - run this first! |
| `frontend/index.html` | Main dashboard interface |
| `scripts/data_cleaning.py` | Data quality fixes |
| `scripts/eda_analysis.py` | Statistical analysis |
| `scripts/feature_engineering.py` | ML feature creation |
| `scripts/ml_preparation.py` | Model training |
| `data/healthcare_data.csv` | Raw dataset (input) |
| `README.md` | Full documentation |

---

## 💻 Command Quick Reference

```bash
# Install all dependencies
pip install -r requirements.txt

# Run entire pipeline
python run_pipeline.py

# Run one script
python scripts/data_cleaning.py
python scripts/eda_analysis.py
python scripts/feature_engineering.py
python scripts/ml_preparation.py

# Start local web server for dashboard
python -m http.server 8000 --directory frontend

# Start Flask API server (if enabled)
python app.py
```

---

## 🎯 Next Steps After First Run

1. ✅ **Explore the Dashboard**
   - Review all tabs
   - Try the risk prediction tool
   - Check different charts

2. ✅ **Review Generated Reports**
   - Open `data/eda_report.json` - analyze results
   - Check `data/kpi_report.json` - key metrics
   - Review high-risk patients in CSV

3. ✅ **Understand the Data**
   - Dataset has 85 patients
   - 42 classified as high-risk
   - Multiple disease types present

4. ✅ **Try Predictions**
   - Use the Prediction tab
   - Input different patient profiles
   - See how risk changes with metrics

---

## 📞 Need Help?

Check these resources:
1. **README.md** - Complete documentation
2. **Script headers** - Each Python file has comments
3. **Scripts** - Print statements show progress
4. **Browser console** (F12) - Shows JavaScript errors

---

## ⚡ Performance Tips

- **First run takes:** 2-5 minutes (includes feature engineering)
- **Subsequent runs:** Check if data files exist, they won't regenerate
- **Dashboard:** Loads instantly once files are generated
- **ML Prediction:** Instantaneous (no server needed for basic version)

---

## 🎓 What You'll Learn

✓ Data cleaning best practices
✓ Healthcare data challenges
✓ EDA methodologies
✓ Feature engineering
✓ ML model training
✓ Dashboard creation
✓ Data visualization
✓ Risk analysis

---

**You're all set! Start with `python run_pipeline.py` 🚀**
