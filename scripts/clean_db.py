# Local Project
from src.db import JobResultsRepository, PostgresDB, WorkflowRunsRepository

if __name__ == "__main__":
    db = PostgresDB()
    repos = [JobResultsRepository(db), WorkflowRunsRepository(db)]
    for repo in repos:
        repo.delete_old_transactions()
