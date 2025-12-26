AIML_ENGINEER_ROLES = [
    "AI Engineer",
    "Artificial Intelligence Engineer",
    "ML Engineer",
    "Machine Learning Engineer",
    "MLE",
]
DATA_ENGINEER_ROLES = ["Data Engineer"]
DATA_SCIENTIST_ROLES = ["Data Scientist", "Data Science"]
DATA_ANALYST_ROLES = ["Data Analyst", "Business Analyst"]

ALL_ROLES = [
    *AIML_ENGINEER_ROLES,
    *DATA_ENGINEER_ROLES,
    *DATA_SCIENTIST_ROLES,
    *DATA_ANALYST_ROLES,
]

JOB_CATEGORIES = [
    "AIML_ENGINEER",
    "DATA_ENGINEER",
    "DATA_SCIENTIST",
    "DATA_ANALYST",
    "OTHERS",
    "SENIOR_TECH",
    "NOT_RELEVANT",
]

JOB_CATEGORIES_DESCRIPTIONS = {
    "AIML_ENGINEER": (
        "Artificial Intelligence Engineer / Machine Learning Engineer - "
        "Works on building, training, evaluating, and deploying machine learning or AI models, "
        "including model pipelines, inference services, and MLOps workflows."
        "Common Technology Stack/Terms: Python, Go, C++, Rust, Tensorflow/PyTorch, CUDA, "
        "Traditional Machine Learning, Deep Learning, LLMs, Model Serving, MLOps"
    ),
    "DATA_ENGINEER": (
        "Data Engineer - Works on designing, building, and maintaining data ETL/ELT pipelines, "
        "data warehouses, and data infrastructure using technologies such as SQL, Spark, "
        "Snowflake, Microsoft Azure, or similar platforms"
        "Common Technology Stack/Terms: SQL, NoSQL, Spark, Hadoop, MapReduce, Data Streaming, Flink, Kafka,"
        "ETL/ELT pipelines, Airflow, Cloud Computing, Databases, APIs,"
        "Snowflake, Microsoft Azure, Google Cloud Platform, AWS"
    ),
    "DATA_SCIENTIST": (
        "Data Scientist - Works on analyzing data to extract insights, build predictive or "
        "statistical models, perform experimentation, and communicate findings to support "
        "business or product decisions"
        "Common Technology Stack/Terms: Python, R, SQL, Pandas, NumPy, Scikit-learn, "
        "Statistical Modeling, Experimentation, A/B Testing, Data Visualization"
    ),
    "DATA_ANALYST": (
        "Data Analyst - Works on querying, cleaning, and analyzing data to produce dashboards, "
        "reports, and ad-hoc analyses using tools such as SQL, Excel, BI tools, or Python, "
        "primarily focused on descriptive and diagnostic analytics"
        "Common Technology Stack/Terms: SQL, Excel, BI Tools (Tableau, Power BI, Looker), "
        "Python, Data Visualization, Reporting, Dashboards"
    ),
    "OTHERS": (
        "Other Tech Roles - Jobs within the technology sector that do not fall under AI/ML Engineer, "
        "Data Engineer, Data Scientist, or Data Analyst categories; such as Software Engineer, "
        "Frontend/Backend Engineer, Mobile Developer, QA Engineer, or any other similar Tech roles."
        "Tech Graduate Programmes should fall under this category as well."
        "Common Technology Stack/Terms: Programming Languages, Web Frameworks, Databases, "
        "APIs, Cloud Services, DevOps Tools"
    ),
    "SENIOR_TECH": (
        "Senior Technology Role - Jobs that are related to technology, but are of senior level (not junior level), "
        "where senior level roles are defined to require minimally 2 years of full-time working experience. "
        "Common Terms in Non-Junior Job Titles: Senior, Lead, Principal, Expert, Manager, President, Vice-President, VP etc.."
    ),
    "NOT_RELEVANT": (
        "Not Relevant - Jobs that are not relevant to the target scope, primarily non-tech roles "
        "such as marketing, sales, business, finance, traditional engineering etc."
    ),
}
