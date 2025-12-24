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
    "NOT_RELEVANT",
]

JOB_CATEGORIES_DESCRIPTIONS = {
    "AIML_ENGINEER": (
        "Artificial Intelligence Engineer / Machine Learning Engineer - "
        "Works on building, training, evaluating, and deploying machine learning or AI models, "
        "including model pipelines, inference services, and MLOps workflows"
    ),
    "DATA_ENGINEER": (
        "Data Engineer - Works on designing, building, and maintaining data ETL/ELT pipelines, "
        "data warehouses, and data infrastructure using technologies such as SQL, Spark, "
        "Snowflake, Microsoft Azure, or similar platforms"
    ),
    "DATA_SCIENTIST": (
        "Data Scientist - Works on analyzing data to extract insights, build predictive or "
        "statistical models, perform experimentation, and communicate findings to support "
        "business or product decisions"
    ),
    "DATA_ANALYST": (
        "Data Analyst - Works on querying, cleaning, and analyzing data to produce dashboards, "
        "reports, and ad-hoc analyses using tools such as SQL, Excel, BI tools, or Python, "
        "primarily focused on descriptive and diagnostic analytics"
    ),
    "OTHERS": (
        "Other Tech Roles - Jobs within the technology sector that do not fall under AI/ML Engineer, "
        "Data Engineer, Data Scientist, or Data Analyst categories, such as Software Engineer, "
        "Frontend/Backend Engineer, Mobile Developer, QA Engineer, or similar roles"
    ),
    "NOT_RELEVANT": (
        "Not Relevant - Jobs that are not relevant to the target scope, including non-tech roles "
        "(e.g. marketing, sales, business, finance, traditional engineering), or roles that are "
        "not junior-level and require two or more years of full-time working experience"
    ),
}
