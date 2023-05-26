import random
import math
import os

# X is max = 1
# O in min = -1
turno_humano = 0

class TicTacToe:
    def __init__(self):
        self.board = ['-' for _ in range(9)]  # Inicializa el tablero vacío con 9 posiciones
        if random.randint(0, 1) == 1:
            self.humanPLayer = 'X'  # Si el número aleatorio es 1, el jugador humano será 'X'
            self.botPlayer = "O"  # Si el número aleatorio es 1, el jugador de la computadora será 'O'
        else:
            self.humanPLayer = "O"  # Si el número aleatorio es 0, el jugador humano será 'O'
            self.botPlayer = "X"  # Si el número aleatorio es 0, el jugador de la computadora será 'X'

    def show_board(self): # Realiza el tablero
        print("")
        for i in range(3):
            print("  ", self.board[0 + (i * 3)], " | ", self.board[1 + (i * 3)], " | ", self.board[2 + (i * 3)])
            print("")

    def is_board_filled(self, state):
        return not "-" in state  # Verifica si el tablero está lleno, es decir, no hay '-' en ninguna posición

    def is_player_win(self, state, player):
        # Verifica si el jugador ha ganado el juego en el estado 'state'
        if state[0] == state[1] == state[2] == player: return True
        if state[3] == state[4] == state[5] == player: return True
        if state[6] == state[7] == state[8] == player: return True
        if state[0] == state[3] == state[6] == player: return True
        if state[1] == state[4] == state[7] == player: return True
        if state[2] == state[5] == state[8] == player: return True
        if state[0] == state[4] == state[8] == player: return True
        if state[2] == state[4] == state[6] == player: return True

        return False

    def checkWinner(self):
        if self.is_player_win(self.board, self.humanPLayer):
            os.system("cls")
            print(f"   Player {self.humanPLayer} wins the game!")  # El jugador humano ha ganado
            return True

        if self.is_player_win(self.board, self.botPlayer):
            os.system("cls")
            print(f"   Player {self.botPlayer} wins the game!")  # El jugador de la computadora ha ganado
            return True

        # Verifica si el juego ha terminado en empate
        if self.is_board_filled(self.board):
            os.system("cls")
            print("   Match Draw!")  # Empate
            return True
        return False

    def start(self):
        bot = ComputerPlayer(self.botPlayer)  # Crea una instancia de la clase ComputerPlayer para la computadora
        human = HumanPlayer(self.humanPLayer)  # Crea una instancia de la clase HumanPlayer para el jugador humano
        
        while True:
            os.system("cls")
            print(f"   Player {self.humanPLayer} turn")
            self.show_board()
            
            bandera=False
            if(turno_humano==1):
                bandera=True #Si empieza el humano
            if(bandera):
                #juega el humano
                square = human.human_move(self.board)  # El jugador humano realiza su movimiento y se obtiene la posición del cuadrado
                self.board[square] = self.humanPLayer  # Actualiza el estado (cuadrado) del tablero con el movimiento del jugador humano
                if self.checkWinner():  # Verifica si el jugador humano ha ganado o el juego ha terminado en empate
                    break
                #juega la maquina
                square = bot.machine_move(self.board)  # La computadora realiza su movimiento
                self.board[square] = self.botPlayer  # Actualiza el estado del tablero con el movimiento de la computadora
                if self.checkWinner():  # Verifica si la computadora ha ganado o el juego ha terminado en empate
                    break
            else:
                #juega la maquina
                square = bot.machine_move(self.board)  # La computadora realiza su movimiento
                self.board[square] = self.botPlayer  # Actualiza el estado del tablero con el movimiento de la computadora
                if self.checkWinner():  # Verifica si la computadora ha ganado o el juego ha terminado en empate
                    break
                os.system("cls")
                self.show_board()
                #juega el humano
                square = human.human_move(self.board)  # El jugador humano realiza su movimiento y se obtiene la posición del cuadrado
                self.board[square] = self.humanPLayer  # Actualiza el estado (cuadrado) del tablero con el movimiento del jugador humano
                if self.checkWinner():  # Verifica si el jugador humano ha ganado o el juego ha terminado en empate
                    break
        # Muestra el estado final del tablero
        print()
        self.show_board()

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter # Aqui se guarda su ficha "O" o "X"

    def human_move(self, state):
        # Toma la entrada del usuario para realizar un movimiento
        while True:
            square = int(input("Enter the square to fix spot(1-9): "))
            print()
            if state[square - 1] == "-":
                break
        return square - 1

class ComputerPlayer(TicTacToe):
    # Constructor de la clase que recibe como parámetro la letra asignada al jugador automático
    def __init__(self, letter):
        self.botPlayer = letter
        self.humanPlayer = "X" if letter == "O" else "O"
        self.turno_jugada=1

    # Método que determina qué jugador es el próximo en jugar
    def players(self, state):
        n = len(state)
        x = 0
        o = 0
        for i in range(9):
            if state[i] == "X":
                x = x + 1
            if state[i] == "O":
                o = o + 1

        if self.humanPlayer == "X":
            return "X" if x == o else "O"
        if self.humanPlayer == "O":
            return "O" if x == o else "X"
    
    def actions(self, state):
        # Retorna una lista de las posiciones vacías en el estado actual del tablero
        return [i for i, x in enumerate(state) if x == "-"]
    
    def result(self, state, action):
        # Retorna un nuevo estado después de realizar una acción en una posición dada
        newState = state.copy()
        player = self.players(state)
        newState[action] = player
        return newState
    
    def terminal(self, state):
        # Verifica si el juego ha terminado en un estado terminal (victoria o empate)
        if self.is_player_win(state, "X"):
            return True
        if self.is_player_win(state, "O"):
            return True
        return False

    def minimax(self, state, player):
        max_player = self.humanPlayer  # el humano buscará maximizar
        other_player = 'O' if player == 'X' else 'X'

        # Primero, verificamos si el movimiento anterior resultó en una victoria
        if self.terminal(state):
            return {'position': None, 'score': 1 * (len(self.actions(state)) + 1) if other_player == max_player else -1 * (len(self.actions(state)) + 1)}
        elif self.is_board_filled(state):
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # cada puntaje debe maximizarse
        else:
            best = {'position': None, 'score': math.inf}  # cada puntaje debe minimizarse
        for possible_move in self.actions(state):
            newState = self.result(state, possible_move)
            sim_score = self.minimax(newState, other_player)  # simular un juego después de realizar ese movimiento

            sim_score['position'] = possible_move  # esto representa el movimiento óptimo siguiente

            if player == max_player:  # X es el jugador máximo
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

    def machine_move(self, state):
        # Retorna el movimiento óptimo para la computadora utilizando el algoritmo Minimax
        if(turno_humano==2 and self.turno_jugada==1):
            square = 4
            self.turno_jugada=self.turno_jugada+1
            return square
        if(turno_humano==2 and self.turno_jugada==2):
            for i,estado in enumerate(state):
                if(i==8 and estado==self.humanPlayer):
                    square=2
                    self.turno_jugada=self.turno_jugada+1
                    return square
        
        square = self.minimax(state, self.botPlayer)['position']
        self.turno_jugada=self.turno_jugada+1
        return square

if __name__ =="__main__":
    # starting the game
    turno_humano = int(input("¿Turno 1 o 2?:" ))
    tic_tac_toe = TicTacToe()
    tic_tac_toe.start()
