import sqlite3

class JobDatabase:
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seen_jobs (
                    job_id TEXT PRIMARY KEY
                )
            ''')
            conn.commit()

    def is_seen(self, job_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM seen_jobs WHERE job_id = ?', (job_id,))
            return cursor.fetchone() is not None

    def mark_seen(self, job_id: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)', (job_id,))
            conn.commit()
