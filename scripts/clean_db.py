# Local Project
from src.db.job_results import delete_old_transactions
from src.db.pg import PostgresDB

if __name__ == "__main__":
    db = PostgresDB()
    delete_old_transactions(db)
