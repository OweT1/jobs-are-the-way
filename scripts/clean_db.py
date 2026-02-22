# Local Project
from src.db.pg import PostgresDB
from src.db.repositories import JobResultsRepository, WorkflowRunsRepository

if __name__ == "__main__":
    db = PostgresDB()
    repos = [JobResultsRepository(), WorkflowRunsRepository()]
    for repo in repos:
        repo.delete_old_transactions(db)
