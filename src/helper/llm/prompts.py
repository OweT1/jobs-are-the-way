# Local Project
from src.constants import JOB_CATEGORIES, JOB_CATEGORIES_DESCRIPTIONS


# --- Helper --- #
def get_job_descriptions() -> str:
    job_descriptions = [
        f"{job}: {description}" for job, description in JOB_CATEGORIES_DESCRIPTIONS.items()
    ]
    output = "\n\n".join(job_descriptions)
    return output


# --- Prompts --- #
def get_category_prompt(job_details: str) -> str:
    return f"""
    <instructions>
    You are an expert system for categorising a job into exactly ONE job category based on the provided job details.
    The job details will usually contain the 'Job Title', and may or may not contain the 'Job Description'.
    You MUST use the information provided in <job_details> and categorise the job using the definitions provided in <job_descriptions>.
    If multiple categories appear relevant, choose the MOST SPECIFIC and BEST-MATCHING category.

    You MUST categorise the job as 'SENIOR_TECH' if all of the conditions are met:
    - The role matches any of the technology roles.
    - The role is of a senior/lead/principal/expert/managerial/president or similar position, or requires minimally 2 years of working experience.

    You MUST categorise the job as 'NOT_RELEVANT' if any of the conditions are met:
    - The role matches any of the technology roles, BUT it requires candidates to have working proficiency in languages that are not English or Chinese/Mandarin. For example, if a job requires working proficiency in Malay/Korean/Japanese or any other language that is not English or Chinese/Mandarin, you should categorise the job as 'NOT_RELEVANT'.
    - The role does not clearly match any technology role in the Job Categories.

    You MUST NOT infer skills or responsibilities that are not explicitly mentioned in the job details.

    You MUST follow the output instructions found in <output_instructions> strictly.
    </instructions>

    <output_instructions>
    You must output ONLY ONE value from <job_categories>.
    Do NOT include explanations, reasoning, punctuation, or additional text.
    </output_instructions>

    <job_descriptions>
    {get_job_descriptions()}
    </job_descriptions>

    <job_categories>
    {JOB_CATEGORIES}
    </job_categories>

    <job_details>
    {job_details}
    </job_details>

    YOUR RESPONSE:
  """
