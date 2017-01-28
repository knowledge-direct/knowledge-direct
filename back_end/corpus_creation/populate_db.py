import sqlite3


import config


conn = sqlite3.connect(config.DB_ADDR)

c = conn.cursor()

c.execute("""
          """)


