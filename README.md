# Buyer Retention &amp; Experimentation Analytics Lab

An end-to-end analytics platfrom that simulates how an e-commerce company (Etsy-style) measures buyer retention, purchase frequency, and product impact using A/B experimentation and causal inference.

This project demonstrates how data scientists turn behavioral + transactional data into product decisions that improve user engagement and growth.

## 🎯 Project Goal

Modern marketplaces live or die by retention and repeat purchase behavior.

This project answers:
- Do product changes increase buyer rentention?
- Does a new experience increase purchase frequency?
- If we can't run an A/B test, can we estimate impact causally?

We buld a system that:
✅ Computer retention & frequency metrics
✅ Analyzed controlled A/B experiments
✅ Runs causal inference when experiments aren't possible
✅ Generates insights like a real product analytics team

## 📊 Core Analytics Questions
- D1/D7/D30 retention by cohort
- Repeat purchase rate
- Time to next purchase
- Buyer lifetime value (LTV proxy)
- Experiment uplift & statistical significance
- Causal impact of product interventions

## 🧠 Skills Demonstrated
- Advanced SQL analytics
- A/B testing & experiment design
- CUPED variance reduction
- Causal inference (Difference-in-Differences, PSM)
- Product metrics & retention modeling
- Data governance & metric definitions
- Insight storytelling
- Dashboard analytics

## 🧱 Tech Stack
- **Python**: pandas, numpy, statsmodels, scipy
- **SQL**: Postgres / BigQuery style analytics
- **Experimentation**: statsmodels
- **Causal inference**: causalml / econml
- **Visualization**: Plotly + Streamlit
- **Data modeling**: dbt-style transformations
- **Environment**: Docker (optional)

## 📂 Repository Structure
<img width="424" height="683" alt="image" src="https://github.com/user-attachments/assets/3edefba2-4837-44dc-a2d7-f428fca99bbe" />

## ⚙️ Setup Instructions
1. Clone repo
git clone https://github.com/yourname/buyer-retention-lab.git
cd buyer-retention-lab

2. Create environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Load dataset
Place dataset inside:
data/raw/

Supported datasets:
Olist e-commerce dataset
Instacart repeat orders
Online Retail II dataset

## ▶️ Run Analytics Pipeline
Retention analysis
python notebooks/01_retention_analysis.ipynb

A/B experiment engine
python experiments/ab_test_engine.py

Causal inference module
python causal/diff_in_diff.py

Launch dashboard
streamlit run app/streamlit_dashboard.py

## 🧪 Experiment Framework
The project simulates product experiments:
- Control vs Treatment groups
- SRM checks
- Uplift estimation
- Statistical significance testing
- CUPED variance reduction
- Confidence intervals

Outputs:
- Conversion lift
- Retention lift
- Frequency impact
- Experiment decision recommendation

## 🔬 Causal Inference Engine
When experiments are unavailable:
- Difference-in-Differences
- Propensity Score Matching
- Treatment effect estimation
- Counterfactual modeling

This mirrors real-world product analytics constraints.

## 📈 Dashboard Features
- Retentition cohort explorer
- Purchase frquency charts
- Experiment impact viewer
- Causal effect summary
- Buyer segmentation analytics

## 📘 Documentation
The docs/ folder includes:
- Metric definitions
- Experiment best practices
- Governance standards
- Insight narratives
- Product recommendations

## 💡 Example Insights
- Checkout redesign increased D30 retention by 6%
- Repeat buyers show 2.4x higher lifetime value
- Fatser shipping reduces churn probability
- Treatment group purchase frequency +9%

## 🚀 Why This Project Matters
This project mirrors how real product analytics teams operate at:
- Etsy
- Airbnb
- Amazon
- Meta
- Uber
- Shopify

It demonstrates the full lifecycle:

**raw data -> experiments -> causal reasoning -> product decisions**
