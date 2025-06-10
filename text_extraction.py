def version1():

    import pandas as pd
    import spacy
    from collections import defaultdict
    from spacy.matcher import PhraseMatcher
    from textblob import TextBlob
    import re
    # Load spaCy NLP model
    nlp = spacy.load("en_core_web_sm")

    # Define keyword lists
    CLOUD_SERVICES = ["AWS", "Azure", "GCP", "Google Cloud",  "S3", "Lambda"]
    BIG_DATA_TOOLS = ["Databricks", "Hadoop", "Spark", "Kafka", "Redshift", "Snowflake"]
    FRAMEWORKS = ["TensorFlow", "PyTorch", "FastAPI", "Django", "Flask", "Sklearn", "KubeFlow", "MLFlow", "SageMaker"]
    EXPERIENCE_KEYWORDS = ["years of experience", "experience with", "+ years"]
    ETL_TOOLS=  ["Airflow", "dbt", "Informatica", "Talend", "SSIS"]

    EXPERIENCE_REGEX = r"(\d+)\s*\+?\s*years? of experience|(\d+)\s*\+?\s*years? of data engineering experience|\bminimum (\d+) years|\b(\d+)\+ years"

    # Setup PhraseMatcher once (Global)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    matcher.add("CLOUD_SERVICES", [nlp.make_doc(kw) for kw in CLOUD_SERVICES])
    matcher.add("BIG_DATA_TOOLS", [nlp.make_doc(kw) for kw in BIG_DATA_TOOLS])
    matcher.add("FRAMEWORKS", [nlp.make_doc(kw) for kw in FRAMEWORKS])
    matcher.add("ETL_TOOLS", [nlp.make_doc(kw) for kw in ETL_TOOLS])

    def extract_requirements(text):
        """Extracts Cloud Services, Big Data Tools, Frameworks, ETL Tools, Responsibilities, and Experience from job descriptions."""
        doc = nlp(text)
        extracted = defaultdict(list)

        # Match technologies using PhraseMatcher
        matches = matcher(doc)
        for match_id, start, end in matches:
            category = nlp.vocab.strings[match_id]
            extracted[category].append(doc[start:end].text)

        # Extract responsibilities using NLP parsing
        responsibilities = []
        for sent in doc.sents:
            if any(kw in sent.text.lower() for kw in ["responsible", "develop", "maintain", "design", "implement"]):
                responsibilities.append(sent.text.strip())

        # Extract experience using regex
        experience_matches = re.findall(EXPERIENCE_REGEX, text, re.IGNORECASE)
        experience_years = [match[0] or match[1] or match[2] for match in experience_matches if any(match)]

        return {
            "Cloud_Services": list(set(extracted.get("CLOUD_SERVICES", []))),
            "Big_Data_Tools": list(set(extracted.get("BIG_DATA_TOOLS", []))),
            "Frameworks": list(set(extracted.get("FRAMEWORKS", []))),
            "ETL_TOOLS": list(set(extracted.get("ETL_TOOLS", []))),
            "Other_Responsibilities": responsibilities,
            "Experience": list(set(experience_years))  # Remove duplicates
        }

    # Load CSV file
    df = pd.read_csv("cleaned_jobs.csv")

    # Apply extraction function to job descriptions
    df["Extracted_Info"] = df["descprition"].apply(lambda x: extract_requirements(str(x)))

    # Expand extracted dictionary into separate columns
    df = df.join(pd.json_normalize(df["Extracted_Info"]))

    # Drop unnecessary column
    df.drop(columns=["Extracted_Info"], inplace=True)

    # Save to CSV
    df.to_csv("jobs_requirements_analysis.csv", index=False)

    print("Job requirements extracted and saved successfully! ✅")


import pandas as pd
import spacy
from collections import defaultdict
from spacy.matcher import PhraseMatcher
import re

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Define keyword lists
CLOUD_SERVICES = ["AWS", "Azure", "GCP", "Google Cloud", "S3", "Lambda"]
BIG_DATA_TOOLS = ["Databricks", "Hadoop", "Spark", "Kafka", "Redshift", "Snowflake"]
FRAMEWORKS = ["TensorFlow", "PyTorch", "FastAPI", "Django", "Flask", "Sklearn", "KubeFlow", "MLFlow", "SageMaker"]
ETL_TOOLS = ["Airflow", "dbt", "Informatica", "Talend", "SSIS"]

# Precompile regex for better performance
EXPERIENCE_REGEX = re.compile(
    r"(\d+)\s*\+?\s*years? of experience|(\d+)\s*\+?\s*years? of data engineering experience|\bminimum (\d+) years|\b(\d+)\+ years",
    re.IGNORECASE
)

# Setup PhraseMatcher once (Global)
matcher = PhraseMatcher(nlp.vocab, attr="ORTH")  # Using ORTH for better efficiency

matcher.add("CLOUD_SERVICES", [nlp.make_doc(kw) for kw in CLOUD_SERVICES])
matcher.add("BIG_DATA_TOOLS", [nlp.make_doc(kw) for kw in BIG_DATA_TOOLS])
matcher.add("FRAMEWORKS", [nlp.make_doc(kw) for kw in FRAMEWORKS])
matcher.add("ETL_TOOLS", [nlp.make_doc(kw) for kw in ETL_TOOLS])

def extract_requirements(text):
    """Extracts technologies, responsibilities, and experience from job descriptions."""
    if not isinstance(text, str) or not text.strip():
        return {
            "Cloud_Services": [],
            "Big_Data_Tools": [],
            "Frameworks": [],
            "ETL_TOOLS": [],
            "Other_Responsibilities": [],
            "Experience": []
        }

    doc = nlp(text)
    extracted = defaultdict(set)  # Use set to remove duplicates

    # Match technologies using PhraseMatcher
    for match_id, start, end in matcher(doc):
        category = nlp.vocab.strings[match_id]
        extracted[category].add(doc[start:end].text)

    # Extract responsibilities with dependency parsing
    responsibilities = [
        sent.text.strip()
        for sent in doc.sents
        if any(token.lemma_ in ["responsible", "develop", "maintain", "design", "implement"] for token in sent)
    ]

    # Extract experience using regex and filter values
    experience_matches = EXPERIENCE_REGEX.findall(text)
    experience_years = {
        int(match[0] or match[1] or match[2] or match[3])
        for match in experience_matches if any(match)
    }
    
    # Remove unrealistic experience values
    experience_years = [year for year in experience_years if 0 < year <= 30]

    return {
        "Cloud_Services": list(extracted["CLOUD_SERVICES"]),
        "Big_Data_Tools": list(extracted["BIG_DATA_TOOLS"]),
        "Frameworks": list(extracted["FRAMEWORKS"]),
        "ETL_TOOLS": list(extracted["ETL_TOOLS"]),
        "Other_Responsibilities": responsibilities,
        "Experience": experience_years
    }

# Load CSV file
df = pd.read_csv("cleaned_jobs.csv")

# Ensure column name is correct and no NaN values
if "descprition" in df.columns:
    df["descprition"] = df["descprition"].fillna("")
    df["Extracted_Info"] = df["descprition"].apply(extract_requirements)
else:
    raise KeyError("Column 'description' not found in the dataset.")

# Expand extracted dictionary into separate columns
df = df.join(pd.json_normalize(df["Extracted_Info"]))

# Drop unnecessary column
df.drop(columns=["Extracted_Info"], inplace=True)

# Save to CSV
df.to_csv("jobs_requirements_analysis.csv", index=False)

print("✅ Job requirements extracted and saved successfully!")
