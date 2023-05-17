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

bK = King('bK.png', 'black')
bQ = Queen('bQ.png', 'black')
bB = Bishop('bB.png', 'black')
bN = Knight('bN.png', 'black')
bR = Castle('bR.png', 'black')
bp = Pawn('bp.png', 'black')

wK = King('wK.png', 'white')
wQ = Queen('wQ.png', 'white')
wB = Bishop('wB.png', 'white')
wN = Knight('wN.png', 'white')
wR = Castle('wR.png', 'white')
wp = Pawn('wp.png', 'white')


piece_list = [bK, bQ, bB, bN, bR, bp, wK, wQ, wB, wN, wR, wp]


global black_location
black_location = set()

global white_location
white_location = set()

Selected= ()
Player_click = []

global gs
gs = Gs()

turn = "white"

move_sound = pg.mixer.Sound("move-self.mp3")


def draw_pieces(screen,gs):
    for row in range(8):
        for column in range(8):
            if gs.board[row][column] != "--":
                if gs.board[row][column] == "bp":
                    pos = (column * 64, row * 64)
                    screen.blit(bp.image, pos)
                    black_location.add((pos[1] // 64 , pos[0] // 64))

                elif gs.board[row][column] == "wp":
                    pos = (column * 64, row * 64)
                    screen.blit(wp.image, pos)
                    white_location.add((pos[1] // 64, pos[0] // 64))

                elif gs.board[row][column][0] == "b":
                    pos = (column * 64, row * 64)
                    screen.blit(pg.image.load(gs.board[row][column] + '.png'), pos)
                    black_location.add((pos[1] // 64 , pos[0] // 64))

                else:
                    pos = (column * 64, row * 64)
                    screen.blit(pg.image.load(gs.board[row][column] + '.png'), pos)
                    white_location.add((pos[1] // 64, pos[0] // 64))

def move_piece(Player_click, gs):
    piece_selected, desired_move = Player_click
    if eval(gs.board[piece_selected[0]][piece_selected[1]]) in piece_list:
        if desired_move in eval(gs.board[piece_selected[0]][piece_selected[1]]).get_moves(piece_selected, gs.board):
            tmp = gs.board[piece_selected[0]][piece_selected[1]]
            gs.board[piece_selected[0]][piece_selected[1]] = "--"
            gs.board[desired_move[0]][desired_move[1]] = tmp
            move_sound.play()
            circle_group.empty()

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
                        print(Selected)
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
                for n in (eval(gs.board[x_pos//64][y_pos//64]).get_moves((x_pos//64, y_pos//64), gs.board)):
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
               draw_pieces(screen,gs)
    
               Selected = ()
               Player_click = []

          
    square_group.draw(screen)
    draw_pieces(screen,gs)

    circle_group.update()
    circle_group.draw(screen)

    pg.display.update()
    clock.tick(60)