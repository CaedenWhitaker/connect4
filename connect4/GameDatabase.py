from connect4.Constants import Constants
from connect4.Match import Match
import sqlite3
import os


class GameDatabase:
	def __init__(self, path=Constants.DATABASE_PATH) -> None:
		self.path = path

	def update(self, match: Match) -> bool:
		with sqlite3.connect(Constants.DATABASE_PATH) as connection:
			cursor = connection.cursor()
			try:
				cursor.execute("""
				INSERT INTO Players(?,0,0,0) 
				SELECT 5, 'text to insert' 
				WHERE NOT EXISTS(SELECT 1 FROM memos WHERE id = 5 AND text = 'text to insert');
				""")
				return True
			except sqlite3.OperationalError:
				return False

	def create(self) -> bool:
		connection = None
		try:
			connection = sqlite3.connect(Constants.DATABASE_PATH)
			cursor = connection.cursor()
			cursor.execute("""
				CREATE TABLE Player(
					player CHAR(3) NOT NULL,
					wins INTEGER NOT NULL,
					draws INTEGER NOT NULL,
					losses INTEGER NOT NULL,
					PRIMARY KEY(player)
				)
			""")
			cursor.execute("""
			CREATE TABLE Matches(
					start DATETIME NOT NULL,
					end DATETIME NOT NULL,
					player1 CHAR(3) NOT NULL,
					player2 CHAR(3) NOT NULL,
					win INTEGER NOT NULL,
					PRIMARY KEY(start, end)
					FOREIGN KEY(player1) REFERENCES Player(player)
					FOREIGN KEY(player2) REFERENCES Player(player)
				)
			""")
			cursor.execute("""
			CREATE TABLE Moves(
					turn INTEGER NOT NULL,
					start DATETIME NOT NULL,
					end DATETIME NOT NULL,
					column INTEGER NOT NULL,
					PRIMARY KEY(turn, start, end)
					FOREIGN KEY(start) REFERENCES Matches(start)
					FOREIGN KEY(end) REFERENCES Matches(end)
				)
			""")
			return True
		except sqlite3.OperationalError:
			return False
		except (sqlite3.DatabaseError, sqlite3.DatabaseError):
			return None
		finally:
			if connection is not None:
				connection.close()
		


