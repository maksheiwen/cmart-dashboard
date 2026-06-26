Here's a **complete, professional `README.md`** for your GitHub repository. It explains the project, how to run it, and highlights all the features you've built.

Copy this text and save it as `README.md` in your project root folder before uploading to GitHub.

---

```markdown
# 🏬 Cmart Changlun Analytics Dashboard

## Social Network-Based Loyalty Influencer Program for Shopping Malls

This interactive dashboard was developed as part of a **SULAM project** to analyze vendor and customer feedback, as well as social media engagement, for **Cmart Changlun**. The goal is to design a data-driven loyalty program leveraging insights from text analytics and social network analysis (SNA).

---

## 🎯 Project Overview

This project integrates three key data sources to provide actionable insights for mall management:

1.  **Vendor Interviews** – Understanding the operational challenges and strategies of vendors at the car boot sales.
2.  **Customer Interviews** – Capturing shopper experiences, pain points, and satisfaction levels.
3.  **Social Media Analysis (SNA)** – Mapping the online community and identifying key influencers discussing Cmart Changlun on TikTok.

---

## ✨ Dashboard Features

- **📊 Executive Overview** – High-level KPIs, word clouds, and sentiment comparison.
- **👨‍💼 Vendor Analysis** – Sentiment distribution and topic modeling for vendor interviews.
- **👤 Customer Analysis** – Sentiment distribution and topic modeling for customer interviews.
- **🌐 SNA Network** – Interactive network visualization of TikTok hashtags, top influencers, and network metrics.
- **📈 Comparison & Recommendations** – Side-by-side comparison of vendor vs. customer perspectives and actionable recommendations for management.
- **🌙 Dark Mode** – Toggle between light and dark themes for comfortable viewing.
- **📥 Downloadable Data** – Export sentiment results as CSV files.

---

## 🧠 Methodology

| Component | Method | Tools |
|-----------|--------|-------|
| **Text Preprocessing** | Tokenization, Stopword Removal, Stemming | NLTK, Malaya Sastrawi |
| **Sentiment Analysis** | HuggingFace (T5) vs. Multinomial | Malaya, scikit-learn |
| **Topic Modeling** | LDA vs. NMF | scikit-learn |
| **Social Network Analysis** | Network visualization and influencer identification | Gephi, Sigma.js |

---

## 🗂️ Project Structure

```
project_cmart/
├── dashboard/
│   └── app_streamlit.py          # Main Streamlit dashboard application
├── data/
│   ├── vendor_transcript.txt     # Raw vendor interview data
│   └── customers_transcripts.txt # Raw customer interview data
├── outputs/                      # Generated outputs (CSVs, images, network files)
│   ├── vendor/
│   ├── customer/
│   └── sna/
├── full_analysis.py              # Script to run sentiment and topic modeling
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/cmart-dashboard.git
cd cmart-dashboard
```

### 2. Install Dependencies
It's recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 3. Run the Analysis (Optional)
If you want to regenerate the outputs from raw transcripts:
```bash
python full_analysis.py
```

### 4. Launch the Dashboard
```bash
streamlit run dashboard/app_streamlit.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Frontend & Dashboard:** [Streamlit](https://streamlit.io/)
- **Visualization:** Plotly, Matplotlib, WordCloud
- **NLP & Machine Learning:** Malaya, NLTK, scikit-learn, Transformers
- **Network Visualization:** Gephi, Sigma.js

---

## 📊 Data Sources

- **Interviews:** 1 vendor and 3 customers were interviewed at Cmart Changlun.
- **Social Media:** TikTok hashtags related to Cmart Changlun were scraped for network analysis.

---

## 👥 Team & Acknowledgments

This project was developed by a collaborative team as part of the SULAM program. Special thanks to Cmart Changlun management, vendors, and customers who participated in the interviews.

---

## 📅 Last Updated

v2.0 | June 2026

---

## 📄 License

This project is for academic and research purposes only.
```

---

## ✅ How to Add It

1.  Create a new file named `README.md` in your `project_cmart/` folder.
2.  Copy and paste the entire text above.
3.  Save the file.
4.  When uploading to GitHub, include this file – it will appear as the repository description on the main page.

---
