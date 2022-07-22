from re import T
from connect4.Board import Board

def test_board_move():
	#takes in: col:int, turn:bool
	
	#arrange:
	board = Board()

	#act
	board.move(0, False)
	board.move(0, True)
	board.move(2, False)
	
	#assert
	assert board.state[0][0] == False
	assert board.state[1][0] == True
	assert board.state[0][2] == False

	#cleanup
	#noop

def test_board_checkWin_vert():
	#this test goes for checkWinAux as well
	#takes in turn:bool
	
	#arrange
	board = Board()
	board.move(0, True)
	board.move(0, True)
	board.move(0, True)
	board.move(0, True)

	#act

	#assert
	assert board.checkWin(True) == True
	assert board.checkWin(False) == False

def test_board_checkWin_horiz():
	#this test goes for checkWinAux as well
	#takes in turn:bool
	
	#arrange
	board = Board()
	board.move(0, False)
	board.move(1, False)
	board.move(2, False)
	board.move(3, False)

	#act

	#assert
	assert board.checkWin(False) == True
	assert board.checkWin(True) == False

def test_board_checkWin_diag():
	#this test goes for checkWinAux as well
	#takes in turn:bool
	
	#arrange
	board = Board()
	board.move(0, False)
	board.move(1, True)
	board.move(2, True)
	board.move(3, True)
	board.move(1, False)
	board.move(2, True)
	board.move(3, True)
	board.move(2, False)
	board.move(3, True)
	board.move(3, False)

	#act

	#assert
	assert board.checkWin(False) == True
	assert board.checkWin(True) == False

def test_board_colFull():
	#takes in col:int

	#arrange
	board = Board()

	for _ in range(6):
		board.move(0, True)
	
	#act
	board.move(0, False)

	#assert
	assert board.colFull(0) == True
	assert board.colFull(1) == False

def test_board_top():
	#takes in: col:int
	#arrange
	board = Board()

	for _ in range(6):
		board.move(0, True)
	
	for _ in range(5):
		board.move(1, True)
	
	for _ in range(4):
		board.move(2, True)
	
	for _ in range(3):
		board.move(3, True)
	
	for _ in range(2):
		board.move(4, True)
	
	board.move(5, True)

	#leave the last col empty
	
	assert board.top(0) == 6
	assert board.top(1) == 5
	assert board.top(2) == 4
	assert board.top(3) == 3
	assert board.top(4) == 2
	assert board.top(5) == 1
	assert board.top(6) == 0


if __name__ == "__main__":
	test_board_move()
	test_board_checkWin_vert()
	test_board_checkWin_horiz()
	test_board_checkWin_diag()
	test_board_colFull()
	test_board_top()

