import os ## to clear
import platform

board = [[1,2,3],[4,5,6],[7,8,9]]
count = 0 ## used to check if it's X's or O's turn


def clear():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

clear() ## making terminal clear on start

gameMechanicChoice = input("Play using (c)oordinates or (n)umbers?\n\n> ")


def main():
	global board, count

	clear() ## another clear to wipe gameMechanicChoice

	symbol = "X" if count % 2 == 0 else "O" ## count is going up every round, count is odd = X's turn, count is even = O's turn

	print(f"{symbol}'s Turn.")

	def showBoard():
		print(f'''
	 {board[0][0]} | {board[0][1]} | {board[0][2]}
	-----------
	 {board[1][0]} | {board[1][1]} | {board[1][2]}
	-----------
	 {board[2][0]} | {board[2][1]} | {board[2][2]}''')



	showBoard() ## shows board every round

	if gameMechanicChoice == "n":
		placeOnBoard = int(input("Number: "))

	else: ## if game input wasnt numbers, use co-ordinates 
		x = int(input("X: "))
		y = int(input("Y: "))
		x -= 1 ## 0 is first item in python, therefore if someone picks 3, 1 needs to be taken away to make it easier to use
		y -= 1

		if y == 2: ## y co-ordinate goes top to bottom, switching it around here
			y = 0
		elif y == 0:
			y = 2

		placeOnBoard = board[y][x] ## specifying which item the user wants

	isTakenN = 0 ## checks to see if the place on board is taken, for numbers
	isTakenCo = 0 ## checks to see if the place on board is taken, for co-ordinates

	for rows in board: 
		for i in rows:
			if i == placeOnBoard:
				isTakenN += 1 ## cant check co-ordinates on number mechanic, so we go through entire board checking is exists


	## if the spot user wants is not there (already taken), or is already X or O, make them try again

	if isTakenN == 0 or placeOnBoard == "X" or placeOnBoard == "O":
		input("\nTry again, Place is taken, press ENTER") 
		main()

	else:
		## overwrite board with everything that was there before, except from thing we chose, we make that our symbol instead
		board = [[i if i != placeOnBoard else symbol for i in rows]for rows in board]
		count += 1


	if count == 9: ## if we played 9 rounds, make it a draw
		clear()
		showBoard()
		print("\nDRAW")
	else:
		main() ## if not draw (9 plays), keep going
		
main() ## initiate game 
