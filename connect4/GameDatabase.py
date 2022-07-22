from connect4.Match import Match
import sqlite3


class GameDatabase:
	def __init__(self, path="connect4.db") -> None:
		self.path = path
		self.safe = self.create() is not None
		self.errors = False
		self.players = []
		self.matches = []
		self.moves = []

	def getPlayers(self):
		self.errors = self.errors or not self.loadPlayers()
		self.players = [
			dict(zip(("player","wins","losses","draws"), row))
			for row in self.players
		]
		return self.players

	def loadPlayers(self) -> bool:
		try:
			connection = sqlite3.connect(self.path)
			self.players = connection.execute(
				"""
					SELECT player, wins, losses, draws FROM Players;
				"""
			).fetchall()
			return True
		except (sqlite3.OperationalError, sqlite3.DatabaseError, sqlite3.DatabaseError):
			return False
		finally:
			if connection is not None:
				connection.close()
	
	def getMatches(self):
		self.errors = self.errors or not self.loadMatches()
		self.matches = [
			dict(zip(("start","end","plname","p2name","p1type","p2type","winner","moves"), row))
			for row in self.matches
		]
		for match in self.matches:
			match["winner"] = int(match["winner"])
			match["moves"] = list(map(int, match["moves"]))
		return self.matches

	def loadMatches(self) -> bool:
		try:
			connection = sqlite3.connect(self.path)
			self.matches = connection.execute(
				"""
					SELECT start, end, p1name, p2name, p1type, p2type, winner, moves FROM Matches;
				"""
			).fetchall()
			return True
		except (sqlite3.OperationalError, sqlite3.DatabaseError, sqlite3.DatabaseError):
			return False
		finally:
			if connection is not None:
				connection.close()

	def save(self, match: Match) -> bool:
		player1WinsDelta = int(match.winner == 1)
		player1LossesDelta = int(match.winner == 2)
		player1DrawsDelta = int(match.winner == 3)

		player2WinsDelta = int(match.winner == 2)
		player2LossesDelta = int(match.winner == 1)
		player2DrawsDelta = int(match.winner == 3)

		connection = None
		try:
			connection = sqlite3.connect(self.path)
			player1 = connection.execute(
				"""
					SELECT player, wins, losses, draws FROM Players
					WHERE player = :player;
				""",
				{
					"player": match.player1.name
				}
			).fetchall()

			player2 = connection.execute(
				"""
					SELECT player, wins, losses, draws FROM Players
					WHERE player = :player;
				""",
				{
					"player": match.player2.name
				}
			).fetchall()

			if len(player1) > 0:
				player1 = player1[0]
				connection.execute(
					"""
						UPDATE Players
						SET wins = :wins,
							losses = :losses,
							draws = :draws
						WHERE player = :player;
					""",
					{
						"player": match.player1.name,
						"wins": player1[1] + player1WinsDelta,
						"losses": player1[2] + player1LossesDelta,
						"draws": player1[3] + player1DrawsDelta
					}
				)
			else:
				connection.execute(
					"""
						INSERT INTO Players(
							player,
							wins,
							losses,
							draws
						)
						VALUES(
							:player,
							:wins,
							:losses,
							:draws
						);
					""",
					{
						"player": match.player1.name,
						"wins": player1WinsDelta,
						"losses": player1LossesDelta,
						"draws": player1DrawsDelta
					}
				)
			if len(player2) > 0:
				player2 = player2[0]
				connection.execute(
					"""
						UPDATE Players
						SET wins = :wins,
							losses = :losses,
							draws = :draws
						WHERE player = :player;
					""",
					{
						"player": match.player2.name,
						"wins": player2[1] + player2WinsDelta,
						"losses": player2[2] + player2LossesDelta,
						"draws": player2[3] + player2DrawsDelta
					}
				)
			else:
				connection.execute(
					"""
						INSERT INTO Players(
							player,
							wins,
							losses,
							draws
						)
						VALUES(
							:player,
							:wins,
							:losses,
							:draws
						);
					""",
					{
						"player": match.player2.name,
						"wins": player2WinsDelta,
						"losses": player2LossesDelta,
						"draws": player2DrawsDelta
					}
				)
			connection.execute(
				"""
					INSERT INTO Matches(
						start,
						end,
						p1name,
						p2name,
						p1type,
						p2type,
						winner,
						moves
					)
					VALUES(
						:start,
						:end,
						:p1name,
						:p2name,
						:p1type,
						:p2type,
						:winner,
						:moves
					);
				""",
				{
					"start": match.start,
					"end": match.end,
					"p1name": match.player1.name,
					"p2name": match.player2.name,
					"p1type": match.player1.type,
					"p2type": match.player2.type,
					"winner": str(match.winner),
					"moves": "".join(map(str,match.moves))
				}
			)
			connection.commit()
			return True
		except (sqlite3.OperationalError, sqlite3.DatabaseError, sqlite3.DatabaseError):
			return False
		finally:
			if connection is not None:
				connection.close()

	def create(self) -> bool:
		connection = None
		try:
			connection = sqlite3.connect(self.path)
			connection.execute("""
				CREATE TABLE Players(
					player CHAR(3) NOT NULL,
					wins INTEGER NOT NULL,
					losses INTEGER NOT NULL,
					draws INTEGER NOT NULL,
					PRIMARY KEY(player)
				);
			""")
			connection.execute("""
				CREATE TABLE Matches(
					start DATETIME NOT NULL,
					end DATETIME NOT NULL,
					p1name CHAR(3) NOT NULL,
					p2name CHAR(3) NOT NULL,
					p1type CHAR(1) NOT NULL,
					p2type CHAR(1) NOT NULL,
					winner CHAR(1) NOT NULL,
					moves VARCHAR(42) NOT NULL,
					PRIMARY KEY(start, end)
					FOREIGN KEY(p1name) REFERENCES Player(player)
					FOREIGN KEY(p2name) REFERENCES Player(player)
				);
			""")
			return True
		except sqlite3.OperationalError:
			return False
		except (sqlite3.DatabaseError, sqlite3.DatabaseError):
			return None
		finally:
			if connection is not None:
				connection.close()
