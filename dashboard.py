def version1():

    import pandas as pd
    import streamlit as st
    import plotly.express as px

    # Load DataFrame
    df = pd.read_csv('jobs_requirements_analysis.csv')

    # Convert string representation of lists to actual lists
    df = df.applymap(lambda x: eval(x) if isinstance(x, str) and x.startswith("[") else x)
    import pandas as pd
    import streamlit as st
    import plotly.express as px

    # Load DataFrame
    df = pd.read_csv('jobs_requirements_analysis.csv')

    # Convert string representation of lists to actual lists
    df = df.applymap(lambda x: eval(x) if isinstance(x, str) and x.startswith("[") else x)

    # Synonym Mapping
    SYNONYM_MAPPING = {
        "gcp": "google cloud",
        "aws s3": "amazon s3",
        "azure cloud": "microsoft azure",
        "sagemaker": "amazon sagemaker",
    }

    # Function to replace synonyms in lists
    def standardize_synonyms(column_data):
        if isinstance(column_data, list):
            return [SYNONYM_MAPPING.get(item.lower(), item.lower()) for item in column_data]
        return column_data

    # Apply synonym replacement for relevant columns
    for column in ["Cloud_Services", "Big_Data_Tools", "Frameworks", "ETL_TOOLS", "Experience"]:
        df[column] = df[column].apply(standardize_synonyms)



    # Function to clean and count occurrences in a column
    def process_column(df, column_name):
        all_values= [item.lower() for sublist in df[column_name] for item in (sublist if isinstance(sublist, list) else [])]
        processed_df = pd.DataFrame(pd.Series(all_values).value_counts()).reset_index()
        processed_df.columns = [column_name, "Count"]  # Ensure correct column names
        return processed_df

    # Process each category
    cloud_df = process_column(df, "Cloud_Services")
    big_data_df = process_column(df, "Big_Data_Tools")
    frameworks_df = process_column(df, "Frameworks")
    etl_df = process_column(df, "ETL_TOOLS")
    experience_df = process_column(df, "Experience")

    # Streamlit Dashboard
    st.title("Job Description Analytics Dashboard 📊")

    # Cloud Services
    st.subheader("Cloud Services Usage")
    if not cloud_df.empty:
        fig1 = px.bar(cloud_df, x="Cloud_Services", y="Count", color="Cloud_Services", title="Cloud Services in Job Descriptions")
        st.plotly_chart(fig1)
    else:
        st.write("No data available for Cloud Services.")

    # Big Data Tools
    st.subheader("Big Data Tools Popularity")
    if not big_data_df.empty:
        fig2 = px.bar(big_data_df, x="Big_Data_Tools", y="Count", color="Big_Data_Tools", title="Big Data Tools in Job Descriptions")
        st.plotly_chart(fig2)
    else:
        st.write("No data available for Big Data Tools.")

    # Frameworks
    st.subheader("Frameworks Used")
    if not frameworks_df.empty:
        fig3 = px.bar(frameworks_df, x="Frameworks", y="Count", color="Frameworks", title="Frameworks in Job Descriptions")
        st.plotly_chart(fig3)
    else:
        st.write("No data available for Frameworks.")

    # ETL Tools
    st.subheader("ETL Tools Popularity")
    if not etl_df.empty:
        fig4 = px.bar(etl_df, x="ETL_TOOLS", y="Count", color="ETL_TOOLS", title="ETL Tools in Job Descriptions")
        st.plotly_chart(fig4)
    else:
        st.write("No data available for ETL Tools.")

    # Experience
    st.subheader("Experience Requirements")
    if not experience_df.empty:
        fig5 = px.pie(experience_df, names="Experience", values="Count", title="Experience Distribution")
        st.plotly_chart(fig5)
    else:
        st.write("No data available for Experience Requirements.")


import pandas as pd
import streamlit as st
import plotly.express as px
import ast  # Use safe literal evaluation
import matplotlib.pyplot as plt


# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("jobs_requirements_analysis.csv")

    # Safely convert string representations of lists
    def safe_eval(val):
        try:
            return ast.literal_eval(val) if isinstance(val, str) and val.startswith("[") else val
        except (ValueError, SyntaxError):
            return []

    df = df.applymap(safe_eval)

    return df

df = load_data()

# Synonym Mapping
SYNONYM_MAPPING = {
    "gcp": "google cloud",
    "aws s3": "amazon s3",
    "azure cloud": "microsoft azure",
    "sagemaker": "amazon sagemaker",
}

def standardize_synonyms(column_data):
    if isinstance(column_data, list):
        return [SYNONYM_MAPPING.get(str(item).lower(), str(item).lower()) for item in column_data]
    return column_data  

# Apply synonym replacement
for column in ["Cloud_Services", "Big_Data_Tools", "Frameworks", "ETL_TOOLS", "Experience"]:
    df[column] = df[column].apply(standardize_synonyms)

# Function to count occurrences in a column
def process_column(df, column_name):
    all_values = [item.lower() for sublist in df[column_name] if isinstance(sublist, list) for item in sublist]
    processed_df = pd.DataFrame(pd.Series(all_values).value_counts()).reset_index()
    processed_df.columns = [column_name, "Count"]
    return processed_df

# Process each category
cloud_df = process_column(df, "Cloud_Services")
big_data_df = process_column(df, "Big_Data_Tools")
frameworks_df = process_column(df, "Frameworks")
etl_df = process_column(df, "ETL_TOOLS")
experience_df = process_column(df, "Experience")

# Streamlit Dashboard
st.title("📊 Data Engineering Job Description Analytics Dashboard")

# Experience Filter (Include "All" option)
experience_options = ["All"] + sorted(experience_df["Experience"].astype(str).unique())
experience_filter = st.selectbox("Filter by Experience Level", experience_options)

if experience_filter != "All":
    filtered_df = df[df["Experience"].apply(lambda x: experience_filter in map(str, x))]
else:
    filtered_df = df

# Function to plot bar charts
def plot_bar_chart(data, x_col, y_col, title):
    if not data.empty:
        data = data.sort_values(by=y_col, ascending=False)  # Sort bars by count
        fig = px.bar(data, x=x_col, y=y_col, color=x_col, title=title, text_auto=True)
        st.plotly_chart(fig)
    else:
        st.write("No data available.")

st.subheader("📌 Cloud Services Usage")
plot_bar_chart(cloud_df, "Cloud_Services", "Count", "Cloud Services in Job Descriptions")

st.subheader("🔍 Big Data Tools Popularity")
plot_bar_chart(big_data_df, "Big_Data_Tools", "Count", "Big Data Tools in Job Descriptions")

st.subheader("🛠️ Frameworks Usage")
plot_bar_chart(frameworks_df, "Frameworks", "Count", "Frameworks in Job Descriptions")

st.subheader("📦 ETL Tools Popularity")
plot_bar_chart(etl_df, "ETL_TOOLS", "Count", "ETL Tools in Job Descriptions")

# Experience Distribution Pie Chart
st.subheader("🎯 Experience Distribution")
if not experience_df.empty:
    fig5 = px.pie(experience_df, names="Experience", values="Count", title="Experience Requirements")
    st.plotly_chart(fig5)

# Word Cloud for Responsibilities (Optional)
# if st.checkbox("Show Word Cloud of Responsibilities"):
#     st.subheader("📝 Word Cloud of Responsibilities")
#     responsibility_text = " ".join([" ".join(r) for r in df["Other_Responsibilities"] if isinstance(r, list)])
#     if responsibility_text:
#         wordcloud = WordCloud(width=800, height=400, background_color="white").generate(responsibility_text)
#         fig, ax = plt.subplots(figsize=(10, 5))
#         ax.imshow(wordcloud, interpolation="bilinear")
#         ax.axis("off")
#         st.pyplot(fig)
#     else:
#         st.write("No data available.")
