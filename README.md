# 📊 Data Engineering Job Description Analytics Dashboard

This interactive dashboard helps visualize and analyze technology trends in Data Engineering job descriptions. It extracts insights from job listings by identifying the most common cloud services, big data tools, frameworks, ETL platforms, and experience requirements.
Built using **Streamlit**, **Plotly**, and **Pandas**, this tool is great for students, career switchers, or professionals aiming to understand the current hiring landscape in data engineering roles.
I've scraped the data from Linkedin using **BeautifulSoup**. And for extracting the text from job descriptions i have used the Spacy NLP model

---

## 🚀 Features

* 📌 **Cloud Services Analysis**: Discover top cloud platforms mentioned in job descriptions (AWS, GCP, Azure, etc.).
* 🔍 **Big Data Tools Popularity**: See which big data tools (Spark, Hadoop, etc.) are most in-demand.
* 🛠️ **Frameworks & ETL Tools Usage**: Identify preferred frameworks and ETL tools used in industry.
* 🎯 **Experience Filter**: Filter data based on required experience levels.
* 📊 **Dynamic Visualizations**: Clean and interactive bar charts and pie charts using Plotly.
* 🔁 **Synonym Standardization**: Handles variations (e.g., "GCP" → "Google Cloud") to normalize insights.

---

## 🛠️ Tech Stack

* **Frontend & App Framework**: [Streamlit](https://streamlit.io)
* **Visualization**: Plotly, Matplotlib
* **Data Manipulation**: Pandas, Ast
* **Language**: Python

---

## 📁 Dataset

The app uses a CSV file named `jobs_requirements_analysis.csv`, which includes extracted and structured job description data with fields such as:

* `Cloud_Services`
* `Big_Data_Tools`
* `Frameworks`
* `ETL_TOOLS`
* `Experience`
* `Other_Responsibilities` (optional, for word cloud generation)

---

## 📦 Installation & Run

```bash
# Clone the repo
git clone https://github.com/your-username/data-engineering-jobs-dashboard.git
cd data-engineering-jobs-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

---

## 📌 Notes

* The app includes synonym mapping to unify tools with different names (e.g., "aws s3" → "amazon s3").
* Optional word cloud for responsibilities can be enabled by uncommenting the respective block in the code.
* Use your own `jobs_requirements_analysis.csv` file or scrape job boards to create one.

---

## 📜 License

MIT License

---

## 👩‍💻 Author

**[Subiksha Devi]**
