import pygame as pg
from classes import *
from classes import Game_State as Gs

dimension = 8
width = height = 512



pg.init()

screen = pg.display.set_mode((width, height))

CIRCLE_RADIUS = 8
circle_group = pg.sprite.Group()

clock = pg.time.Clock()

flag = True

square_group = pg.sprite.Group()


for row in range(8):
    for column in range(8):
        if (row + column) % 2 == 0:
            square = Squares(column * 64, row * 64, '#F4A460')
        else:
            square = Squares(column * 64, row * 64, '#9D5A30')
        square_group.add(square)

global black_location
black_location = set()

global white_location
white_location = set()

Selected= ()
Player_click = []

global gs
gs = Gs()

for i, row in enumerate(gs.board):
    for x,col in enumerate(row):
         if col != "--":
            if gs.board[i][x].color == "black":
                if isinstance(gs.board[i][x], King):
                    gs.blackKing = (i, x)
                gs.black_pieces.append(gs.board[i][x])
            else:
                if isinstance(gs.board[i][x], King):
                    gs.whiteKing = (i, x)
                gs.white_pieces.append(gs.board[i][x])
turn = "white"

move_sound = pg.mixer.Sound("move-self.mp3")


def draw_pieces(screen,gs):
    for row in range(8):
        for column in range(8):
            if gs.board[row][column] != "--":
                if gs.board[row][column].color == "black":
                    pos = (column * 64, row * 64)
                    screen.blit(gs.board[row][column].image, pos)
                    black_location.add((pos[1] // 64 , pos[0] // 64))

                elif gs.board[row][column].color == "white":
                    pos = (column * 64, row * 64)
                    screen.blit(gs.board[row][column].image, pos)
                    white_location.add((pos[1] // 64, pos[0] // 64))


def move_piece(Player_click, gs):
    piece_selected, desired_move = Player_click
    if desired_move in white_location:
        white_location.remove(desired_move)
    elif desired_move in black_location:
        black_location.remove(desired_move)

    if desired_move in gs.board[piece_selected[0]][piece_selected[1]].get_valid_moves(piece_selected, gs, turn):
        tmp = gs.board[piece_selected[0]][piece_selected[1]]
        gs.board[piece_selected[0]][piece_selected[1]] = "--"
        captured = gs.board[desired_move[0]][desired_move[1]]
        gs.board[desired_move[0]][desired_move[1]] = tmp
        move_sound.play()
        circle_group.empty()

        if captured != "--":
            if captured.color == "white":
                gs.white_pieces.remove((captured))
            elif captured.color == "black":
                gs.black_pieces.remove((captured))
        return True
    return False


while flag:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag = False
        if event.type == pg.MOUSEBUTTONDOWN:
            y_pos, x_pos = pg.mouse.get_pos()

            if Selected == (x_pos//64, y_pos//64):
                    Selected = ()
                    Player_click = []
                    circle_group.empty()
            else:
                    if len(Player_click) == 0:
                        if turn == 'white' and (x_pos//64, y_pos//64) in white_location:
                            Selected = (x_pos//64, y_pos//64)
                            Player_click.append(Selected)
                        elif turn == 'black' and (x_pos//64, y_pos//64) in black_location:
                            Selected = (x_pos//64, y_pos//64)
                            Player_click.append(Selected)
                    else:
                        if turn == 'white' and (x_pos//64, y_pos//64) in white_location:
                                circle_group.empty()
                                Player_click.clear()
                                Selected = (x_pos//64, y_pos//64)
                                Player_click.append(Selected)

                        elif turn == 'black' and (x_pos//64, y_pos//64) in black_location:
                                circle_group.empty()
                                Player_click.clear()
                                Selected = (x_pos//64, y_pos//64)
                                Player_click.append(Selected)
                        else:
                                Selected = (x_pos//64, y_pos//64)
                                Player_click.append(Selected)

            if len(Player_click) == 1:
                    for n in gs.board[x_pos//64][y_pos//64].get_valid_moves((x_pos//64, y_pos//64), gs, turn):
                        circle_sprite = Circle((n[1] * 64) + 32, (n[0] * 64) + 32, CIRCLE_RADIUS)
                        circle_group.add(circle_sprite)  

            if len(Player_click) == 2:
                if turn == "white" and Player_click[0] in white_location:
                        if move_piece(Player_click, gs):
                            white_location.remove(Player_click[0])
                            white_location.add(Player_click[1])
                            turn = "black"

                elif turn == "black" and Player_click[0] in black_location:
                    if move_piece(Player_click, gs):
                            black_location.remove(Player_click[0])
                            black_location.add(Player_click[1])
                            turn = "white"
                
                if gs.if_Check(turn):
                    if turn == "white":
                         for square in square_group.sprites():
                            if square.rect.y // 64 == gs.whiteKing[0] and square.rect.x // 64 == gs.whiteKing[1]:
                                square.image.fill('red')
                    elif turn == "black":
                          for square in square_group.sprites():
                            if square.rect.y // 64 == gs.whiteKing[0] and square.rect.x // 64 == gs.whiteKing[1]:
                                square.image.fill('red')
                else:
                    for square in square_group.sprites():
                        square.image.fill(square.original)

                draw_pieces(screen,gs)
                Selected = ()
                Player_click = []

        
    square_group.draw(screen)
    draw_pieces(screen,gs)

    circle_group.update()
    circle_group.draw(screen)

    pg.display.update()
    clock.tick(60)