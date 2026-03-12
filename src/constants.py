AIML_ENGINEER_ROLES = [
    "AI Engineer",
    "Artificial Intelligence Engineer",
    "ML Engineer",
    "Machine Learning Engineer",
]
DATA_ENGINEER_ROLES = ["Data Engineer"]
DATA_SCIENTIST_ROLES = ["Data Scientist", "Data Science"]
DATA_ANALYST_ROLES = ["Data Analyst", "Business Analyst"]
SOFTWARE_ENGINEER_ROLES = [
    "Software Engineer",
    "Backend Engineer",
    "Frontend Engineer",
    "Fullstack Engineer",
]

ALL_ROLES_FT = [
    *AIML_ENGINEER_ROLES,
    *DATA_ENGINEER_ROLES,
    *DATA_SCIENTIST_ROLES,
    *DATA_ANALYST_ROLES,
    *SOFTWARE_ENGINEER_ROLES,
]

ALL_ROLES_INTERN = [f"{role} Intern" for role in ALL_ROLES_FT]

ALL_ROLES = [
    *ALL_ROLES_FT,
    *ALL_ROLES_INTERN,
]

JOB_CATEGORIES = [
    "AIML_ENGINEER",
    "DATA_ENGINEER",
    "DATA_SCIENTIST",
    "DATA_ANALYST",
    "SOFTWARE_ENGINEER",
    "OTHERS",
    "SENIOR_TECH",
    "NOT_RELEVANT",
]

JOB_CATEGORIES_DESCRIPTIONS = {
    "AIML_ENGINEER": """
        Artificial Intelligence Engineer / Machine Learning Engineer - Works on building, training, evaluating, and deploying machine learning or AI models, including model pipelines, inference services, and MLOps workflows.

        Common Job Title(s): AI Engineer / Artificial Intelligence Engineer / ML Engineer / Machine Learning Engineer
        Common Technology Stack/Terms: Python, Go, C++, Rust, Tensorflow/PyTorch, CUDA, Traditional Machine Learning, Deep Learning, LLMs, Model Serving, MLOps
    """,
    "DATA_ENGINEER": """
        Data Engineer - Works on designing, building, and maintaining data ETL/ELT pipelines, data warehouses, and data infrastructure using technologies such as SQL, Spark, Snowflake, Microsoft Azure, or similar platforms.

        Common Job Title(s): Data Engineer
        Common Technology Stack/Terms: SQL, NoSQL, Spark, Hadoop, MapReduce, Data Streaming, Flink, Kafka, ETL/ELT pipelines, Airflow, Cloud Computing, Databases, APIs, Snowflake, Microsoft Azure, Google Cloud Platform, AWS
    """,
    "DATA_SCIENTIST": """
        Data Scientist - Works on analyzing data to extract insights, build predictive or statistical models, perform experimentation, and communicate findings to support business or product decisions.

        Common Job Title(s): Data Scientist / Data Science Analyst / Data Science Engineer
        Common Technology Stack/Terms: Python, R, SQL, Pandas, NumPy, Scikit-learn, Statistical Modeling, Experimentation, A/B Testing, Data Visualization
    """,
    "DATA_ANALYST": """
        Data Analyst - Works on querying, cleaning, and analyzing data to produce dashboards, reports, and ad-hoc analyses using tools such as SQL, Excel, BI tools, or Python, primarily focused on descriptive and diagnostic analytics.

        Common Job Title(s): Data Analyst / Business Analyst
        Common Technology Stack/Terms: SQL, Excel, BI Tools (Tableau, Power BI, Looker), Python, Data Visualization, Reporting, Dashboards
    """,
    "SOFTWARE_ENGINEER": """
        Software Engineer - Design, build, test, and maintain software applications and systems. This includes developing backend services, frontend interfaces, or full-stack features, while writing clean, efficient, and maintainable code. Some work that typical Software Engineers do include designing and consuming APIs, working with various databases to store, retrieve and process data, as well as debugging and optimisation of code performance.

        Common Job Title(s): Software Engineer / Software Development Engineer / Software Developer / Backend Engineer / Backend Developer / Frontend Engineer / Frontend Developer / Fullstack Engineer / Fullstack Developer
        Common Technology Stack/Terms: Java, Python, C++, Go, JavaScript, TypeScript, RESTful APIs, Microservices, Distributed Systems, React, Angular, Vue, HTML, CSS, SQL (MySQL / PostgreSQL), NoSQL, Redis, AWS, GCP, Azure, Docker, Kubernetes, Git, CI/CD, Linux, Monitoring, Unit Testing, Integration Testing, System Design
    """,
    "OTHERS": """
        Other Tech Roles - Jobs within the technology sector that do not fall under AI/ML Engineer, Data Engineer, Data Scientist, Data Analyst or Software Engineer categories; such as Mobile Developer, QA Engineer, or any other similar Technology roles.
        Additionally, Tech Graduate Programmes / General Technology Internship Programmes should fall under this category as well.

        Common Job Title(s): Mobile Developer / QA Engineer / DevOps Engineer / Site Reliability Engineer / IT Engineer
        Common Technology Stack/Terms: Programming Languages, Web Frameworks, Databases, APIs, Cloud Services, DevOps Tools
    """,
    "SENIOR_TECH": """
        Senior Technology Roles - Jobs that are related to technology, but are of mid/senior level (not junior level), where mid/senior level roles are defined to require minimally 2 years of full-time working experience.

        Common Terms in Non-Junior Job Titles: Senior, Lead, Principal, Expert, Manager, President, Vice-President, VP etc..
    """,
    "NOT_RELEVANT": """
        Not Relevant - Jobs that are not relevant to the target scope, primarily non-tech roles such as marketing, sales, business, finance, traditional engineering etc.
    """,
}

REQUIRED_FIELDS = frozenset(["company", "title", "job_url"])
NON_RELEVANT_CHANNEL_CATEGORIES = frozenset(["NOT_RELEVANT", "SENIOR_TECH"])

HOURS_OLD_FALLBACK: int = 3
HOURS_OLD_MAX: int = 12

DB_CLEAN_UP_DAYS_THRESHOLD: int = 7

BLACKLIST_COMPANIES = frozenset(
    [
        "PT Minyak Urapan Anggur",
        "The Quantum Index",
        "ECO-IMPACT Senegal",
        "MINDSET INFORMATION TECHNOLOGY",
        "Data Analyst Job",
        "📊 Data 📑 & Analytics 📈 Leadership 👑 Jobs 👔",
        "Jobs Wanted",
        "XR-LEAN",
        "Wise Solutions.Eco",
        "Perspectiva surveys",
        "NOUVELLETALENT.AI",
        "Grupo Aw Oriental, C.A",
        "MCO Consulting Brasil",
        "BRAHMA AI",
        "Global Business analyst",
        "Catalyst Funds Management",
        "Viral Set Go",
        "Viral Internet Brands",
        "Level Zero OT Cyber Security Conference",
        "Khdma Dz",
        "AR TECH DIARIES",
        "Nova Rota RH",
        "Tips, Tricks and Hacks for Doing Everything Better",
        "Black Swan Holdings",
        "Ningbo Deli Imp & Exp Co., Ltd.",
        "Data Analyst",
        "CXO Chapter",
        "MSL EXPERT & MENTORING",
        "Nova Hospitality Club",
        "UJ Faculty of Engineering and the Built Environment",
        "The CMO Circle",
        "Tax Savyy",
        "Black Nurse Collaborative, Inc",
        "Last Mile",
        "THE GLOBAL CEO NETWORK",
        "ILM Accounting & Tax Services",
        "Delta Black Aerospace",
        "Tax & Women",
        "THE GLOBAL CEO NETWORK",
        "Head Hunter l Ceyda Kaptan",
        "Société Juris Tax Tchad SAS",
        "MK INFRABUILD VENTURES INDIA PRIVATE LIMITED",
        "Fin-Erth",
        "Data Science Hiring",
        "Trouve Ton Talent 🎤🎓",
        "Sony Acceleration Platform Europe",
        "Min-Tai Machinery Co., Ltd",
        "TON Society",
        "Blue Azores",
        "TEHDAS2 joint action",
        "UNFPA-UNICEF Joint Programme on the Elimination of Female Genital Mutilation",
        "NesmaKent Joint Venture",
        "Zero To Cloud",
        "Neurasmus - Erasmus Mundus Joint Master Degree in Neurosciences",
        "Zero Gravity",
        "Net Zero Frontiers",
        "QAS CONSULTORIA, LDA - Moçambique",
        "Zero Vendor",
        "Zero One Zero Seven",
        "Open Ledger",
        "ART NETWORK",
        "&Done",
        "Zero Grad",
        "Get Offers",
        "Global Opportunity Desk",
        "BUSINESS & MORE 🎩",
        "The VET Recruiter Relief",
        "Fine Art",
        "The Contemporary Art Club",
        "ArtBlast | Art Jobs",
        "Ministerio para la Transformación Digital y de la Función Pública",
        "HL Mando Corporation do Brasil",
        "TM Automotive Seating Systems Pvt. Ltd.",
        "Consortium for Clinical Research and Innovation Singapore",
        "Social Like SLU",
        "Prestige African Art",
        "Health tips and advices",
        "TM Group",
        "The Logical Recruiter - An i-Qode Company",
        "Federal Tax Ombudsman of Pakistan",
        "Branding Türkiye",
        "Sine Bahia - Sistema Nacional de Emprego",
        "European Court of Human Rights / Cour européenne des droits de l'homme",
        "Recruiter",
        "Healthcare Recruiter UAE",
        "Health & Wellness Tips",
        "Black Panda Enterprises",
        "Mental Health",
        "Volunteer at UN and global institutes",
        "Objective Zero",
        "Nine Yards Real Estate Development",
        "Hustlers Organization",
        "Nextbot",
        "High-paid Jobs for Vietnamese Talents",
    ]
)
