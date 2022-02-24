import os
import socket
import requests
import platform
from threading import Thread

def clear():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

clear()

hostOrConnect = input("Select (A/B):\n\na) Host game\nb) Join game\n\n> ").lower()

if hostOrConnect == "a":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    NAME = input("Pick a name: ")
    PORT = input("Pick a port: ")
    INT_PORT = int(PORT)
    server.bind(("0.0.0.0", INT_PORT))
    server.listen()

    def send_game_details():
        r = requests.post(f"http://ssh.lejeff.com:5000/game/{NAME}/{PORT}")

    Thread(target = send_game_details).start()
    print("Waiting for someone to join...")
    client, addr = server.accept()
    count = 1 ## used to check if it's X's or O's turn

elif hostOrConnect == "b":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    r = requests.get("http://ssh.lejeff.com:5000/game/null/0")
    j = r.json()
    
    print("Games available:\n")
    for key, value in j.items():
        print(key)
    

    game_pick = input("\nEnter game name:")

    HOST = j[game_pick]["ip"]
    strPORT = j[game_pick]["port"]
    PORT = int(strPORT)

    #HOST = input("Enter host server: ")
    #PORT = int(input("Enter port: "))
    client.connect((HOST, PORT))
    count = 0 ## used to check if it's X's or O's turn

board = [[7,8,9],[4,5,6],[1,2,3]]
solutions = [[[0,0],[0,1],[0,2]],[[1,0],[1,1],[1,2]],[[2,0],[2,1],[2,2]],[[0,0],[1,0],[2,0]],[[0,1],[1,1],[2,1]],[[0,2],[1,2],[2,2]],[[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]]] 

def checkWin():
    global solutions, board

    for i in solutions:
        if board[i[0][0]][i[0][1]] == "X" and board[i[1][0]][i[1][1]] == "X" and board[i[2][0]][i[2][1]] == "X":
            return "X Wins"
            break
        elif board[i[0][0]][i[0][1]] == "O" and board[i[1][0]][i[1][1]] == "O" and board[i[2][0]][i[2][1]] == "O":
            return "O Wins"
            break


#gameMechanicChoice = input("Play using (c)oordinates or (n)umbers?\n\n> ")
gameMechanicChoice = "n"

## i have not implemented online yet for coordinates, either way, coords arent completed yet.

#numTutorial()

def main():
    global board, count

    clear() ## another clear to wipe gameMechanicChoice

    if checkWin() == "X Wins":
        print("You win!")
        return
    elif checkWin() == "O Wins":
        print("Opponent wins!")
        return

    symbol = "X" if count % 2 == 0 else "O" ## count is going up every round, count is odd = X's turn, count is even = O's turn

    if symbol == "X":
        whosTurn = "Your"
    else:
        whosTurn = "Opponents"
    print(f"{whosTurn} Turn: ({symbol})")

    def numCheck(y, x):
        if board[y][x] == "X" or board[y][x] == "O":
            return board[y][x]
        else:
            return ' '


    def showBoard():
        print(f'''
 {numCheck(0, 0)} | {numCheck(0, 1)} | {numCheck(0, 2)}
-----------
 {numCheck(1, 0)} | {numCheck(1, 1)} | {numCheck(1, 2)}
-----------
 {numCheck(2, 0)} | {numCheck(2, 1)} | {numCheck(2, 2)}
 ''')

    showBoard() ## shows board every round


    if gameMechanicChoice == "n":
        try:
            if symbol == "X":
                done = False
                while not done:
                    STRplaceOnBoard = input("Your Turn: ")
                    try:
                        placeOnBoard = int(STRplaceOnBoard)
                        client.send(STRplaceOnBoard.encode("utf-8"))
                    except:
                        clear()
                        input("You didn't enter a number, press ENTER to try again")
                        main()
                    placeOnBoard = int(placeOnBoard)
                    done = True
            else:
                done = False
                while not done:
                    msg = client.recv(1024).decode("utf-8")

                    placeOnBoard = int(msg) ## turning socket response into int
                    done = True

			#client.send(input("Message: ").encode("utf-8"))
        except:
            clear()
            input("Something went wrong, could not send data.")
            main()

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
        input("\nPlace on board is occupied, press ENTER to try again.") 
        main()

    else:
		## overwrite board with everything that was there before, except from thing we chose, we make that our symbol instead
        board = [[i if i != placeOnBoard else symbol for i in rows]for rows in board]
        count += 1

    if count == 10: ## if we played 9 rounds, make it a draw
        clear()
        showBoard()
        print("\nDRAW")
    else:
        main() ## if not draw (9 plays), keep going
		
main() ## initiate game 
