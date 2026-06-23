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
    "TECH_PROG",
    "OTHERS",
    "SENIOR_TECH",
    "NOT_RELEVANT",
]

JOB_CATEGORIES_DESCRIPTIONS = {
    "AIML_ENGINEER": """
        Artificial Intelligence Engineer / Machine Learning Engineer

        WHAT THEY DO: Builds, trains, evaluates, and deploys machine learning or AI models. Core work involves
        designing model architectures, managing training pipelines (data ingestion → training → evaluation →
        serving), developing inference services, and maintaining MLOps infrastructure. Distinct from a Data
        Scientist in that the focus is engineering production-grade ML systems, not exploratory analysis or
        statistical modelling.

        BOUNDARY CASES:
        - If the role primarily trains and deploys models (not just analyses data) → AIML_ENGINEER
        - If the role applies ML as a tool within a product feature but the primary identity is software
          development → SOFTWARE_ENGINEER
        - If the role is LLM prompt engineering or AI product management with no model training → NOT_RELEVANT

        Common Job Titles: AI Engineer, Artificial Intelligence Engineer, ML Engineer, Machine Learning
        Engineer, Applied Scientist (engineering-heavy), Research Engineer, MLOps Engineer, AI Infrastructure
        Engineer

        Common Technologies: Python, Go, C++, Rust, PyTorch, TensorFlow, JAX, CUDA, ONNX, Triton,
        HuggingFace, LLMs / Foundation Models, Model Serving (vLLM, TorchServe, Ray Serve), Feature Stores,
        Experiment Tracking (MLflow, W&B), Kubeflow, Airflow, Docker, Kubernetes
    """,
    "DATA_ENGINEER": """
        Data Engineer

        WHAT THEY DO: Designs, builds, and maintains the infrastructure that moves and transforms data at
        scale — ETL/ELT pipelines, data warehouses, data lakes, and streaming systems. Primary output is
        reliable, well-modelled data that downstream consumers (analysts, scientists) can trust. Distinct
        from a Software Engineer in that the domain is data infrastructure, not general application
        development; distinct from a Data Scientist in that the work is engineering pipelines, not
        extracting insights.

        BOUNDARY CASES:
        - If the role builds data pipelines and warehouses as the primary focus → DATA_ENGINEER
        - If the role involves some pipeline work but the core output is software products → SOFTWARE_ENGINEER
        - If the role is primarily consuming clean data for analysis or modelling → DATA_SCIENTIST or DATA_ANALYST

        Common Job Titles: Data Engineer, Analytics Engineer, Data Platform Engineer, ETL Developer,
        Data Infrastructure Engineer, Big Data Engineer

        Common Technologies: SQL, Python, Spark, Hadoop, Kafka, Flink, dbt, Airflow, Prefect, Dagster,
        Snowflake, BigQuery, Redshift, Delta Lake, Iceberg, AWS (S3, Glue, EMR), GCP (Dataflow, Pub/Sub),
        Azure (Data Factory, Synapse), REST APIs, Docker, Kubernetes
    """,
    "DATA_SCIENTIST": """
        Data Scientist

        WHAT THEY DO: Uses statistical methods, machine learning, and experimentation to extract actionable
        insights from data and build predictive models that inform product or business decisions. Primary
        output is insight, predictions, or experiment results — not production pipelines or deployed services.
        Distinct from a Data Analyst in that the work involves building models and running experiments, not
        just descriptive reporting; distinct from an AIML Engineer in that the focus is on analysis and
        modelling for decisions, not engineering production ML systems at scale.

        BOUNDARY CASES:
        - If the role designs A/B tests, builds predictive models, and communicates findings → DATA_SCIENTIST
        - If the role is purely dashboard creation and SQL reporting → DATA_ANALYST
        - If the role deploys and maintains ML models in production systems at engineering scale → AIML_ENGINEER

        Common Job Titles: Data Scientist, Applied Scientist (research-heavy), Data Science Analyst,
        Data Science Engineer, Quantitative Analyst, Research Scientist (non-ML infra)

        Common Technologies: Python, R, SQL, Pandas, NumPy, Scikit-learn, SciPy, Statsmodels, XGBoost,
        LightGBM, Jupyter, A/B Testing frameworks, Causal Inference, Bayesian methods, Data Visualization
        (Matplotlib, Seaborn, Plotly), Databricks, Spark (for data access)
    """,
    "DATA_ANALYST": """
        Data Analyst

        WHAT THEY DO: Queries, cleans, and interprets data to produce dashboards, reports, and ad-hoc
        analyses that answer specific business questions. Work is primarily descriptive and diagnostic —
        understanding what happened and why — rather than predictive or prescriptive. Distinct from a
        Data Scientist in that the work rarely involves building statistical or ML models; distinct from a
        Data Engineer in that they consume data infrastructure rather than build it.

        BOUNDARY CASES:
        - If the role is primarily reporting, dashboarding, and SQL querying for business stakeholders → DATA_ANALYST
        - If the role involves building predictive models or running controlled experiments → DATA_SCIENTIST
        - "Business Analyst" titles that focus on data and BI tools → DATA_ANALYST; those focused on
          process/requirements with no data tooling → NOT_RELEVANT

        Common Job Titles: Data Analyst, Business Analyst (data-focused), BI Analyst, Reporting Analyst,
        Analytics Analyst, Insights Analyst, Operations Analyst (data-focused)

        Common Technologies: SQL, Excel, Google Sheets, Tableau, Power BI, Looker, Metabase, Mode,
        Python (basic Pandas), R (basic), Data Visualization, Reporting automation
    """,
    "TECH_PROG": """
        Graduate / Internship Technology Programmes

        WHAT THEY DO: Structured entry-level programmes for undergraduate or fresh-graduate candidates
        that rotate across or assign candidates into a variety of technology functions (e.g., Software
        Engineering, Data, AI/ML, Product, Infrastructure). The defining feature is the programme
        structure itself — cohort-based hiring, rotation tracks, or formal graduate schemes — rather than
        a single specialist function. These roles may sit across any tech sub-discipline and should be
        classified here rather than into a specific technical category.

        BOUNDARY CASES:
        - If the job posting is a named graduate programme or internship programme with broad tech scope → TECH_PROG
        - If the posting is a direct individual-contributor internship with a specific, well-defined
          technical role (e.g., "Software Engineering Intern") → classify by the underlying function
          (SOFTWARE_ENGINEER, DATA_ENGINEER, etc.)
        - If the programme is for non-tech functions (e.g., finance, HR graduate programmes) → NOT_RELEVANT

        Common Job Titles: Graduate Technology Programme, Technology Graduate, Technology Internship
        Programme, Technology Associate Programme, Rotational Technology Analyst, Digital Graduate Scheme

        Common Signals: Words like "programme", "cohort", "graduate scheme", "rotational", "track",
        paired with broad technology or digital scope; no requirement for prior full-time experience
    """,
    "SOFTWARE_ENGINEER": """
        Software Engineer

        WHAT THEY DO: Designs, builds, tests, and maintains software applications and systems — covering
        backend services, frontend interfaces, APIs, and full-stack features. Core work includes writing
        clean, maintainable code; designing system architecture; integrating with databases and third-party
        services; and optimising for performance, reliability, and scalability. This is the broadest
        engineering category and is the default for general programming roles not better captured by a
        more specific category.

        BOUNDARY CASES:
        - Backend, frontend, fullstack, API, and platform engineering roles → SOFTWARE_ENGINEER
        - If the role's primary domain is data pipelines and warehousing → DATA_ENGINEER
        - If the role's primary domain is training and deploying ML models → AIML_ENGINEER
        - Mobile development, QA, DevOps, or SRE → OTHERS
        - If the role requires 2+ years of full-time experience and carries a senior signal in the title
          (Senior, Lead, Principal, etc.) → SENIOR_TECH

        Common Job Titles: Software Engineer, Software Development Engineer (SDE), Software Developer,
        Backend Engineer, Backend Developer, Frontend Engineer, Frontend Developer, Fullstack Engineer,
        Fullstack Developer, Platform Engineer, API Engineer, Systems Engineer (software-focused)

        Common Technologies: Java, Python, C++, C#, Go, Rust, JavaScript, TypeScript, Ruby, PHP;
        React, Angular, Vue, Next.js, HTML, CSS; RESTful APIs, GraphQL, gRPC, Microservices, Event-driven
        Architecture; MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch; AWS, GCP, Azure; Docker,
        Kubernetes, CI/CD (GitHub Actions, Jenkins); Git, Linux, System Design, Unit & Integration Testing
    """,
    "OTHERS": """
        Other Technology Roles

        WHAT THEY DO: Technology roles that do not fit into any of the defined specialist categories
        (AIML_ENGINEER, DATA_ENGINEER, DATA_SCIENTIST, DATA_ANALYST, SOFTWARE_ENGINEER). This includes
        mobile development, quality assurance, DevOps, site reliability, IT operations, security
        engineering, and other technology-adjacent disciplines. Use this category when the role is clearly
        within the technology sector but does not map to a more specific category above.

        BOUNDARY CASES:
        - Mobile development (iOS, Android) → OTHERS
        - QA / Test Automation Engineer → OTHERS
        - DevOps / Platform / Infrastructure Engineer (infra-focused, not software product) → OTHERS
        - Site Reliability Engineer (SRE) → OTHERS
        - Cybersecurity / Information Security Engineer → OTHERS
        - IT support, IT operations, systems administration → OTHERS
        - If the role is non-junior and carries senior signals in the title → SENIOR_TECH (takes priority)

        Common Job Titles: Mobile Developer, iOS Engineer, Android Engineer, QA Engineer, Test Engineer,
        SDET, DevOps Engineer, Site Reliability Engineer (SRE), Infrastructure Engineer, Cloud Engineer,
        Security Engineer, IT Engineer, Systems Administrator, Network Engineer, Technical Support Engineer

        Common Technologies: Swift, Kotlin, React Native, Flutter; Selenium, Cypress, Playwright, Appium;
        Terraform, Ansible, Helm, Prometheus, Grafana; Cloud platforms (AWS, GCP, Azure) from an
        infrastructure/operations perspective; Networking, Linux administration
    """,
    "SENIOR_TECH": """
        Senior / Mid-Level Technology Roles

        WHAT THEY DO: Technology roles across any discipline (software engineering, data, AI/ML, DevOps,
        etc.) that explicitly require prior full-time working experience — defined as a minimum of 2 years
        — at the time of application. The seniority signal in the job title or requirements is the primary
        classifier criterion, not the technical domain. This category takes priority over all domain-specific
        categories (SOFTWARE_ENGINEER, DATA_ENGINEER, etc.) when the seniority threshold is clearly met.

        BOUNDARY CASES:
        - "Senior Software Engineer", "Lead Data Engineer", "Principal ML Engineer" → SENIOR_TECH
          (regardless of domain)
        - Roles with managerial or people-leadership scope in tech (e.g. Engineering Manager,
          VP Engineering) → SENIOR_TECH
        - A role titled "Software Engineer" that incidentally lists 3+ years experience as preferred
          but not required may still be entry/junior level — assess the spirit of the posting, not just
          the keyword
        - Graduate programmes or internships (even if competitive) → TECH_PROG, not SENIOR_TECH

        Strong Title Signals (any of these in the title strongly indicate SENIOR_TECH):
        Senior, Sr., Lead, Principal, Staff, Distinguished Fellow, Architect, Manager, Director,
        Head of, Vice President (VP), President, C-suite (CTO, CDO, CIO)

        Strong Requirement Signals: "X+ years of experience", "proven track record", "prior industry
        experience required", mentioning leadership or mentoring responsibilities
    """,
    "NOT_RELEVANT": """
        Not Relevant

        WHAT THEY ARE: Roles that fall outside the defined technology job scope. This covers any position
        whose primary function is not in software engineering, data, AI/ML, or related technical disciplines.
        Use this when the role is clearly non-technical or is a business/operational function that happens
        to sit within a technology company.

        BOUNDARY CASES:
        - Pure business functions regardless of industry (finance, accounting, HR, legal, compliance,
          sales, marketing, operations, strategy) → NOT_RELEVANT
        - Traditional/physical engineering (civil, mechanical, electrical) → NOT_RELEVANT
        - Product Manager, Project Manager, Scrum Master, Agile Coach (non-coding) → NOT_RELEVANT
        - UX/UI Designer, Graphic Designer → NOT_RELEVANT
        - Technical Recruiter, IT Recruiter → NOT_RELEVANT
        - LLM / AI "prompt engineer" roles with no coding or model-training component → NOT_RELEVANT
        - Business Analyst focused on process/requirements (no data tooling) → NOT_RELEVANT
        - Customer Success, Technical Account Manager (relationship-focused) → NOT_RELEVANT

        Note: A non-tech role at a tech company is still NOT_RELEVANT. Classification is based on the
        nature of the work, not the employer's industry.
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
        "Veteran Reach Back Group",
        "Care Setu",
        "Alexa Developers Community-CU",
        "Black On Board Ltd",
        "GRUPO VALTE Reformas + Arquitectura",
        "BABY TEETH",
        "Mi Chanc-e",
        "Let's Begin",
        "Black in Health Policy",
        "THE TRAVEL AGENT",
        "Road 2 Intern",
        "PNG IT Network",
        "APPLE RETAIL ITALIA SRL",
        "GTMOffice",
        "MCC-Tanzania Limited",
        "Cellcraft",
        "InsourceAI",
        "CFP Learning - GM",
        "Gaming Company",
        "Thrivento",
        "InsourceAI",
        "Pencilish Animation Studios",
        "User Experience Researchers Pte Ltd (Singapore)",
        "Seattle Department of Neighborhoods",
        "GEN AI",
        "NuPoint",
        "AI Daily",
        "BBI - Intrakat RT Joint Venture",
        "Workaholic360",
        "Quantum Gestão de Pessoas",
        "Construction Innovation",
        "Orbit Institute",
        "Join Media Agency",
        "Defense Innovation Highway | DIH",
        "AI Revolution",
        "Tips Hindawi",
        "Precision Metal Experts",
        "Fitelo",
        "BBI - Intrakat RT Joint Venture",
        "AIN'T",
        "Scavenger Zero",
        "Finance apex",
        "Economic Reform Activity",
        "XY Booster By Unicorn Series",
        "Graphic Design",
        "MarketMuse",
        "Art Dubai Group",
        "Future Skills Education Varsity",
        "Future Of Sales",
        "Pv Solutions - Prime Volt Solutions",
        "Future is AI",
        "EMP GoWIN Global",
        "Quantum University",
        "Cardano Africa Tech Summit",
        "AI Mindset",
        "Ascend Organisation",
        "Analyst Skill",
        "The Makeup Choice",
        "Antas",
        "Dimension Six Technologies Private Limited",
        "Six Sigma Org.",
        "PALECYTO MECANIQUE DE PRECISION",
        "The Innovation Spark",
        "Joint Special Operations Command",
        "Apex Technologies",
        "Reliance Automated Verified Leads, LLC",
        "Tap Growth ai",
        "Rhino Partners",
        "Team_Work (TM_W)",
        "Future Translation Co.",
    ]
)
