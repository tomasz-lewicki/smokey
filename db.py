

import sqlite3
from dataclasses import dataclass
import datetime
from typing import List

@dataclass
class Measurement:
    pm2_5: int
    pm10: int
    t: datetime.datetime


from collections import namedtuple

@dataclass
class _TIME_FORMAT:
    """Aparently these are inconsistent..."""
    python = "%Y-%m-%d %H:%M:%S.%f"
    sqlite ="%Y-%m-%d %H:%M:%f"

class DB:
    def __init__(self, filename: str):
        # Connect
        self._connection = sqlite3.connect(filename)
        
        # Initialize
        init_query = """CREATE TABLE IF NOT EXISTS measurements (t TIMESTAMP, pm10 INTEGER, pm2_5 INTEGER);"""
        cursor =  self._connection.cursor()
        cursor.execute(init_query)
        self._connection.commit()
        
    def insert(self, pm2_5: int, pm10: int):
        cursor =  self._connection.cursor()
        cursor.execute(f"INSERT INTO measurements (pm10, pm2_5, t) VALUES ({pm2_5}, {pm10},strftime('{_TIME_FORMAT.sqlite}','now','localtime'));")
        self._connection.commit()
        
    def read_all(self) -> List[Measurement]:
        cursor =  self._connection.cursor()
        cursor.execute(f"SELECT * FROM measurements;")
        rows = cursor.fetchall()
        print(rows[0])
        measurements = [self._row2measurement(row) for row in rows]
        return measurements
    
    def read_latest(self) -> Measurement:
        cursor =  self._connection.cursor()
        cursor.execute(f"SELECT * FROM measurements ORDER BY t DESC LIMIT 1")
        row = cursor.fetchall()[0]
        mesurement = self._row2measurement(row)
        return mesurement
    
    @staticmethod
    def _row2measurement(row: tuple) -> Measurement:
        """Conversion from DB row as `tuple` to a `Mesurement` object"""
        m = Measurement(
            t=datetime.datetime.strptime(row[0], _TIME_FORMAT.python),
            pm10 = row[1],
            pm2_5 = row[2]
        )
        
        return m