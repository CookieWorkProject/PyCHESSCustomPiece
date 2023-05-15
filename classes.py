import pygame as pg


class Player:
    pass

class Game_State:
    def __init__(self,background = None):
        self.image = background
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp' for n in range(8)],
            ["--" for n in range(8)],
            ["--" for n in range(8)],
            ["--" for n in range(8)],
            ["--" for n in range(8)],
            ['wp' for n in range(8)],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]


    def print_board(self):
        for n in self.board:
            print(n)

class Piece:
    def __init__(self, image, color):
        self.image = pg.image.load(image) 
        self.color = color

class King(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)
        

class Queen(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

class Castle(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

class Bishop(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

class Knight(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)
    
    def get_moves(self, pos, board):
        moves = []
        x, y = pos

        # determine direction based on color
        if self.color == "white":
            direction = -1
        else:
            direction = 1

        # check all 8 possible moves for a knight
        potential_moves = [(x+2*direction, y+1), (x+2*direction, y-1), 
                           (x+1*direction, y+2), (x+1*direction, y-2), 
                           (x-1*direction, y+2), (x-1*direction, y-2), 
                           (x-2*direction, y+1), (x-2*direction, y-1)]

        for move in potential_moves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:  # make sure move is on the board
                if board[move[0]][move[1]] == "--":  # empty square
                    moves.append(move)
                elif board[move[0]][move[1]][0] != self.color:  # capture opponent's piece
                    moves.append(move)

        return moves

class Pawn(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

    def get_moves(self, pos, board):
        moves = []
        x, y = pos

        # determine direction based on color
        if self.color == "white":
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        # check one square forward
        if board[x+direction][y] == "--":
            moves.append((x+direction, y))
            # check two squares forward if pawn is on starting row
            if x == start_row and board[x+2*direction][y] == "--":
                moves.append((x+2*direction, y))

        # check diagonal capture moves
        if y > 0 and board[x+direction][y-1][0] == self.color:
            moves.append((x+direction, y-1))
        if y < 7 and board[x+direction][y+1][0] == self.color:
            moves.append((x+direction, y+1))

        return moves

class Squares(pg.sprite.Sprite):
    def __init__(self, x, y, fill):
        super().__init__()
        self.image = pg.Surface((64, 64))
        self.image.fill(fill)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]


