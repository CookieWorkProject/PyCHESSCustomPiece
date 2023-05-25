import pygame as pg


class Player:
    pass


class Circle(pg.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.color = "#D3D3D3"
        self.image = pg.Surface((self.radius*2, self.radius*2), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)


class Game_State:
    def __init__(self, background=None):
        self.image = background
        self.board = [
            [Castle('bR.png', 'black'), Knight('bN.png', 'black'), Bishop('bB.png', 'black') ,Queen('bQ.png', 'black'), King('bK.png', 'black'), Bishop('bB.png', 'black'), Knight('bN.png', 'black'),Castle('bR.png', 'black')],
            [Pawn('bp.png', 'black'), Pawn('bp.png', 'black'), Pawn('bp.png', 'black'), Pawn('bp.png', 'black'), Pawn('bp.png', 'black'), Pawn('bp.png', 'black'), Pawn('bp.png', 'black'), Pawn('bp.png', 'black')],
            ["--" for _ in range(8)],
            ["--" for _ in range(8)],
            ["--" for _ in range(8)],
            ["--" for _ in range(8)],
            [Pawn('wp.png', 'white'), Pawn('wp.png', 'white'), Pawn('wp.png', 'white'), Pawn('wp.png', 'white'), Pawn('wp.png', 'white'), Pawn('wp.png', 'white'), Pawn('wp.png', 'white'), Pawn('wp.png', 'white')],
            [Castle('wR.png', 'white'),Knight('wN.png', 'white'),Bishop('wB.png', 'white'), Queen('wQ.png', 'white'), King('wK.png', 'white'), Bishop('wB.png', 'white'), Knight('wN.png', 'white'), Castle('wR.png', 'white')]
        ]

        self.white_pieces = []
        self.black_pieces = []

        self.whiteKing = None
        self.blackKing = None

    def get_pos(self,chesspiece):
        """
        Input type: Piece Object
        Return type: A tuple of the x and y coords on the board
        """
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == chesspiece:
                    return (i,j)


    def if_Check(self, turn):
        if turn == "white":
            for pieces in self.black_pieces:
                if self.whiteKing in pieces.get_moves(self.get_pos(pieces), self.board):
                    return True
        elif turn == "black":
            for pieces in self.white_pieces:
                if self.blackKing in pieces.get_moves(self.get_pos(pieces), self.board):
                    return True

    def squareUnderAttack(self, start, turn):
        valid_moves = []
        piece = self.board[start[0]][start[1]]
        if turn == "white":
            if piece in self.white_pieces:
                pseudo_moves = piece.get_moves(start, self.board)
                for moves in pseudo_moves:
                    captured = self.pseudo_move([start, moves])
                    is_valid = True
                    for pieces in self.black_pieces:
                        if self.whiteKing in pieces.get_moves(self.get_pos(pieces), self.board):
                            is_valid = False
                    self.undo_move([start, moves], captured)
                    if is_valid:
                        valid_moves.append(moves)

        elif turn == "black":
            if piece in self.black_pieces:
                pseudo_moves = piece.get_moves(start, self.board)
                for moves in pseudo_moves:
                    captured = self.pseudo_move([start, moves])
                    is_valid = True
                    for pieces in self.white_pieces:
                        if self.blackKing in pieces.get_moves(self.get_pos(pieces), self.board):
                            is_valid = False
                    self.undo_move([start, moves], captured)
                    if is_valid:
                        valid_moves.append(moves)                        
        return valid_moves


    def pseudo_move(self, coords):
        start, end = coords
        tmp = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = "--"
        captured = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = tmp

        if tmp.color == "white" and isinstance(tmp, King):
            self.whiteKing = end
        elif tmp.color == "black" and isinstance(tmp, King):
            self.blackKing = end
        if captured in self.white_pieces:
            self.white_pieces.remove(captured)
        elif captured in self.black_pieces:
            self.black_pieces.remove(captured)

        return captured
    

    def undo_move(self, coords, captured_piece):
        start, end = coords
        piece = self.board[end[0]][end[1]]
        self.board[start[0]][start[1]] = piece
        self.board[end[0]][end[1]] = captured_piece

        if piece.color == "white" and isinstance(piece,King):
            self.whiteKing = start
        elif piece.color == "black" and isinstance(piece, King):
            self.blackKing = start
        if captured_piece != "--":
            if captured_piece.color == "white":
                self.white_pieces.append(captured_piece)
            elif captured_piece.color == "black":
                self.black_pieces.append(captured_piece)

class Piece:
    def __init__(self, image, color):
        self.image = pg.image.load(image) 
        self.color = color


    def get_moves(self, pos, board):
        return []

    def get_valid_moves(self, pos, gs, turn):
        if self.color == "white":
            return gs.squareUnderAttack(pos, turn)
        elif self.color == "black":
            return gs.squareUnderAttack(pos, turn)
    
class King(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

    def get_moves(self, pos, board):
            x, y = pos
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            moves = []

            for dx, dy in directions:
                x_temp, y_temp = x + dx, y + dy
                if 0 <= x_temp < len(board) and 0 <= y_temp < len(board[x_temp]):
                    if board[x_temp][y_temp] == "--":
                        moves.append((x_temp, y_temp))
                    elif board[x_temp][y_temp].color != self.color:
                        moves.append((x_temp, y_temp))
                    
            return moves
        

class Queen(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

    def get_moves(self, pos, board):
        x, y = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        moves = []

        for dx, dy in directions:
            x_temp, y_temp = x + dx, y + dy
            while 0 <= x_temp < len(board) and 0 <= y_temp < len(board[x_temp]):
                if board[x_temp][y_temp] != "--":
                    if board[x_temp][y_temp].color == self.color:
                        break
                    else:
                        moves.append((x_temp, y_temp))
                        break
                moves.append((x_temp, y_temp))
                x_temp += dx
                y_temp += dy

        return moves
    

class Castle(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

    def get_moves(self, pos, board):
        x, y = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        moves = []

        for dx, dy in directions:
            x_temp, y_temp = x + dx, y + dy
            while 0 <= x_temp < len(board) and 0 <= y_temp < len(board[x_temp]):
                if board[x_temp][y_temp] != "--":
                    if board[x_temp][y_temp].color == self.color:
                        break
                    else:
                        moves.append((x_temp, y_temp))
                        break
                moves.append((x_temp, y_temp))
                x_temp += dx
                y_temp += dy

        return moves


class Bishop(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)

    def get_moves(self,pos,board):
        x,y = pos
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        moves = []

        for dx, dy in directions:
            x_temp, y_temp = x + dx, y + dy
            while 0 <= x_temp < len(board) and 0 <= y_temp < len(board[x_temp]):
                if board[x_temp][y_temp] != "--":
                    if board[x_temp][y_temp].color == self.color:
                        break
                    else:
                        moves.append((x_temp, y_temp))
                        break
                moves.append((x_temp, y_temp))
                x_temp += dx
                y_temp += dy

        return moves


class Knight(Piece):
    def __init__(self, image, color):
        Piece.__init__(self, image, color)
    
    def get_moves(self, pos, board):
        moves = []
        x, y = pos

        # determine direction based on color
        direction = 1 if self.color == "white" else -1

        # check all 8 possible moves for a knight
        potential_moves = [(x+2*direction, y+1), (x+2*direction, y-1), 
                           (x+1*direction, y+2), (x+1*direction, y-2), 
                           (x-1*direction, y+2), (x-1*direction, y-2), 
                           (x-2*direction, y+1), (x-2*direction, y-1)]

        for move in potential_moves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:  # make sure move is on the board
                if board[move[0]][move[1]] == "--":  # empty square
                    moves.append(move)
                elif board[move[0]][move[1]].color != self.color:  # capture opponent's piece
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
        if y > 0 and board[x+direction][y-1] != '--' and board[x+direction][y-1].color != self.color:
            moves.append((x+direction, y-1))
        if y < 7 and board[x+direction][y+1] != '--' and board[x+direction][y+1].color != self.color:
            moves.append((x+direction, y+1))

        return moves

class Squares(pg.sprite.Sprite):
    def __init__(self, x, y, fill):
        super().__init__()
        self.image = pg.Surface((64, 64))
        self.image.fill(fill)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.original = fill