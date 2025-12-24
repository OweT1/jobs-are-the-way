# Local Project
from src.constants import JOB_CATEGORIES, JOB_CATEGORIES_DESCRIPTIONS


# --- Helper --- #
def get_job_descriptions() -> str:
    job_descriptions = [
        f"{job}: {description}"
        for job, description in JOB_CATEGORIES_DESCRIPTIONS.items()
    ]
    output = "\n\n".join(job_descriptions)
    return output


# --- Prompts --- #
def get_category_prompt(job_details: str) -> str:
    return f"""
  <instructions>
  You are an expert system for categorising a job into exactly ONE job category based on the provided job details.

  You MUST categorise the job using ONLY the definitions and technology stacks provided in <job_descriptions>.
  If multiple categories appear relevant, choose the MOST SPECIFIC and BEST-MATCHING category.
  If the job does not clearly match any technical data-related role or if the role is of a senior/managerial/lead position, categorise it as NOT_RELEVANT.

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
