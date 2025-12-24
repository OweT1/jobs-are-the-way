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
  You are an expert at categorising a job into one of the job categories based on the provided job details.
  You should refer to the job descriptions (in <job_descriptions> XML tags) when categorising the job based on the provided job details.
  You are to STRICTLY follow the output instructions found in <output_instructions> tags.

  The list of job categories can be found in <job_categories> XML tags.
  You will be provided with the job details in the <job_details> XML tags.
  </instructions>

  <output_instructions>
  You are to STRICTLY output only one of the categories from <job_categories> as your output.
  You must not include any reasoning in your output.
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
