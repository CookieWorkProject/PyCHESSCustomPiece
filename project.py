import pygame as pg
from classes import *
from classes import Game_State as Gs

dimension = 8

width = height = 512

CIRCLE_RADIUS = 8

global black_location
black_location = set()

global white_location
white_location = set()

global gs
gs = Gs()

turn = "white"

pawn_promotion = False

former_piece = None

former_index = None

rectangle = Rectangle(0, 0)

en_passant_piece = None


pg.init()

screen = pg.display.set_mode((width, height))

circle_group = pg.sprite.Group()

clock = pg.time.Clock()

move_sound = pg.mixer.Sound("move-self.mp3")

capture_sound = pg.mixer.Sound("capture.mp3")

castle_sound = pg.mixer.Sound("castle.mp3")

square_group = pg.sprite.Group()

for row in range(8):
    for column in range(8):
        if (row + column) % 2 == 0:
            square = Squares(column * 64, row * 64, "#F4A460")
        else:
            square = Squares(column * 64, row * 64, "#9D5A30")
        square_group.add(square)

for i, row in enumerate(gs.board):
    for x, col in enumerate(row):
        if col != "--":
            if gs.board[i][x].color == "black":
                if isinstance(gs.board[i][x], King):
                    gs.blackKing = (i, x)
                gs.black_pieces.append(gs.board[i][x])
            else:
                if isinstance(gs.board[i][x], King):
                    gs.whiteKing = (i, x)
                gs.white_pieces.append(gs.board[i][x])


def draw_pieces(screen, gs):
    for row in range(8):
        for column in range(8):
            if gs.board[row][column] != "--":
                if gs.board[row][column].color == "black":
                    pos = (column * 64, row * 64)
                    screen.blit(gs.board[row][column].image, pos)
                    black_location.add((pos[1] // 64, pos[0] // 64))

                elif gs.board[row][column].color == "white":
                    pos = (column * 64, row * 64)
                    screen.blit(gs.board[row][column].image, pos)
                    white_location.add((pos[1] // 64, pos[0] // 64))


def move_piece(Player_click, gs):
    global pawn_promotion
    global rectangle
    global former_piece
    global former_index
    global en_passant_piece

    capture_a_piece = False
    castle = False
    piece_selected, desired_move = Player_click

    if en_passant_piece:
        if gs.board_state != gs.board:
            gs.board[en_passant_piece[0]][en_passant_piece[1]].en_passant = False
            en_passant_piece = None

    if desired_move in white_location:
        white_location.remove(desired_move)
    elif desired_move in black_location:
        black_location.remove(desired_move)

    if desired_move in gs.board[piece_selected[0]][piece_selected[1]].get_valid_moves(
        piece_selected, gs, turn
    ):
        if isinstance(gs.board[piece_selected[0]][piece_selected[1]], Castle):
            gs.board[piece_selected[0]][piece_selected[1]].castling = False

        if isinstance(gs.board[piece_selected[0]][piece_selected[1]], King):
            if gs.board[piece_selected[0]][piece_selected[1]].color == "white":
                gs.whiteKing = desired_move
            else:
                gs.blackKing = desired_move
            gs.board[piece_selected[0]][piece_selected[1]].castling = False

            if abs(desired_move[1] - piece_selected[1]) == 2:
                if isinstance(gs.board[desired_move[0]][desired_move[1] + 1], Castle):
                    tmp = gs.board[desired_move[0]][desired_move[1] + 1]
                    gs.board[desired_move[0]][desired_move[1] + 1] = "--"
                    gs.board[desired_move[0]][desired_move[1] - 1] = tmp
                    prev_pos = (desired_move[0], desired_move[1] + 1)
                    new_pos = (desired_move[0], desired_move[1] - 1)

                elif isinstance(gs.board[desired_move[0]][desired_move[1] - 2], Castle):
                    tmp = gs.board[desired_move[0]][desired_move[1] - 2]
                    gs.board[desired_move[0]][desired_move[1] - 2] = "--"
                    gs.board[desired_move[0]][desired_move[1] + 1] = tmp
                    prev_pos = (desired_move[0], desired_move[1] + 1)
                    new_pos = (desired_move[0], desired_move[1] - 1)

                castle = True

                if prev_pos in white_location:
                    white_location.remove(prev_pos)
                    white_location.add(new_pos)
                elif prev_pos in black_location:
                    black_location.remove(prev_pos)
                    white_location.add(new_pos)

        if isinstance(gs.board[piece_selected[0]][piece_selected[1]], Pawn):
            gs.board[piece_selected[0]][piece_selected[1]].current_row = desired_move[0]
            gs.board[piece_selected[0]][piece_selected[1]].move_count += 1

            if gs.board[piece_selected[0]][piece_selected[1]].move_count == 1:
                if (
                    abs(
                        gs.board[piece_selected[0]][piece_selected[1]].current_row
                        - gs.board[piece_selected[0]][piece_selected[1]].start_row
                    )
                    == 2
                ):
                    gs.board[piece_selected[0]][piece_selected[1]].en_passant = True
                    if en_passant_piece:
                        gs.board[en_passant_piece[0]][en_passant_piece[1]].en_passant = False
                    en_passant_piece = desired_move
                    gs.board_state = [n[::] for n in gs.board]
                    cpy = gs.board_state[piece_selected[0]][piece_selected[1]]
                    gs.board_state[piece_selected[0]][piece_selected[1]] = "--"
                    gs.board_state[desired_move[0]][desired_move[1]] = cpy
            else:
                gs.board[piece_selected[0]][piece_selected[1]].en_passant = False

            if desired_move[0] == 7 or desired_move[0] == 0:
                pawn_promotion = True
                former_piece = gs.board[piece_selected[0]][piece_selected[1]]
                former_index = desired_move
                rectangle = Rectangle(desired_move[1], desired_move[0])

            dir = -gs.board[piece_selected[0]][piece_selected[1]].direction
            col = gs.board[piece_selected[0]][piece_selected[1]].color

            if isinstance(gs.board[desired_move[0] + dir][desired_move[1]], Pawn):
                if (
                    gs.board[desired_move[0] + dir][desired_move[1]].en_passant
                    and gs.board[desired_move[0] + dir][desired_move[1]].color != col
                ):
                    if (
                        gs.board[desired_move[0] + dir][desired_move[1]].color
                        == "white"
                    ):
                        gs.white_pieces.remove(
                            gs.board[desired_move[0] + dir][desired_move[1]]
                        )
                        white_location.remove((desired_move[0] + dir, desired_move[1]))
                    else:
                        gs.black_pieces.remove(
                            gs.board[desired_move[0] + dir][desired_move[1]]
                        )
                        black_location.remove((desired_move[0] + dir, desired_move[1]))
                    gs.board[desired_move[0] + dir][desired_move[1]] = "--"
                    capture_a_piece = True
                    en_passant_piece = None

        tmp = gs.board[piece_selected[0]][piece_selected[1]]
        gs.board[piece_selected[0]][piece_selected[1]] = "--"
        captured = gs.board[desired_move[0]][desired_move[1]]
        gs.board[desired_move[0]][desired_move[1]] = tmp

        if captured != "--":
            capture_a_piece = True
            if captured.color == "white":
                gs.white_pieces.remove(captured)
            elif captured.color == "black":
                gs.black_pieces.remove(captured)

        if capture_a_piece:
            capture_sound.play()
        elif castle:
            castle_sound.play()
        else:
            move_sound.play()
        circle_group.empty()
        return True
    return False


def checkMate(gamestate, turn):
        if gamestate.if_Check(turn):
            if turn == "white":
                for pieces in gamestate.white_pieces:
                    if pieces.get_valid_moves(gamestate.get_pos(pieces), gamestate, turn):
                        return False
            elif turn == "black":
                for pieces in gamestate.black_pieces:
                    if pieces.get_valid_moves(gamestate.get_pos(pieces), gamestate, turn):
                        return False
            return True
        return False


def staleMate(gamestate,turn):
        if turn == "white":
            for pieces in gamestate.white_pieces:
                if pieces.get_valid_moves(gamestate.get_pos(pieces), gamestate, turn):
                    return False
        elif turn == "black":
            for pieces in gamestate.black_pieces:
                if pieces.get_valid_moves(gamestate.get_pos(pieces), gamestate, turn):
                    return False
        return True


def main():
    global turn
    global pawn_promotion
    global former_piece

    flag = True
    active = False
    check_mate = False
    stale_mate = False
    Selected = ()
    Player_click = []


    while flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not active:
                        active = True
                    stale_mate = False
                    check_mate = False

            if event.type == pg.MOUSEBUTTONDOWN:
                y_pos, x_pos = pg.mouse.get_pos()

                if Selected == (x_pos // 64, y_pos // 64):
                    Selected = ()
                    Player_click = []
                    circle_group.empty()
                else:
                    if len(Player_click) == 0:
                        if turn == "white" and (x_pos // 64, y_pos // 64) in white_location:
                            Selected = (x_pos // 64, y_pos // 64)
                            Player_click.append(Selected)
                        elif (
                            turn == "black" and (x_pos // 64, y_pos // 64) in black_location
                        ):
                            Selected = (x_pos // 64, y_pos // 64)
                            Player_click.append(Selected)
                    else:
                        if turn == "white" and (x_pos // 64, y_pos // 64) in white_location:
                            circle_group.empty()
                            Player_click.clear()
                            Selected = (x_pos // 64, y_pos // 64)
                            Player_click.append(Selected)

                        elif (
                            turn == "black" and (x_pos // 64, y_pos // 64) in black_location
                        ):
                            circle_group.empty()
                            Player_click.clear()
                            Selected = (x_pos // 64, y_pos // 64)
                            Player_click.append(Selected)
                        else:
                            Selected = (x_pos // 64, y_pos // 64)
                            Player_click.append(Selected)

                if len(Player_click) == 1:
                    for n in gs.board[x_pos // 64][y_pos // 64].get_valid_moves(
                        (x_pos // 64, y_pos // 64), gs, turn
                    ):
                        circle_sprite = Circle(
                            (n[1] * 64) + 32, (n[0] * 64) + 32, CIRCLE_RADIUS
                        )
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

                    Selected = ()
                    Player_click = []
        if active:
            square_group.draw(screen)
            draw_pieces(screen, gs)

            if pawn_promotion:
                pg.draw.rect(screen, "#ffffff", rectangle)
                rectangle.display_images(screen)
                initial = former_piece
                turn = former_piece.color
                former_piece = rectangle.assign_piece(former_piece)

                if initial != former_piece:
                    if former_piece.color == "white":
                        gs.white_pieces.remove(gs.board[former_index[0]][former_index[1]])
                        gs.white_pieces.append(former_piece)
                        turn = "black"
                    elif former_piece.color == "black":
                        gs.black_pieces.remove(gs.board[former_index[0]][former_index[1]])
                        gs.black_pieces.append(former_piece)
                        turn = "white"
                    gs.board[former_index[0]][former_index[1]] = former_piece
                    pawn_promotion = False

            if gs.if_Check(turn):
                if turn == "white":
                    gs.board[gs.whiteKing[0]][gs.whiteKing[1]].check = True
                    for square in square_group.sprites():
                        if (
                            square.rect.y // 64 == gs.whiteKing[0]
                            and square.rect.x // 64 == gs.whiteKing[1]
                        ):
                            square.image.fill("red")
                elif turn == "black":
                    gs.board[gs.whiteKing[0]][gs.whiteKing[1]].check = True
                    for square in square_group.sprites():
                        if (
                            square.rect.y // 64 == gs.blackKing[0]
                            and square.rect.x // 64 == gs.blackKing[1]
                        ):
                            square.image.fill("red")
            else:
                for square in square_group.sprites():
                    square.image.fill(square.original)

            if checkMate(gs, turn):
                check_mate = True
                active = False

            elif staleMate(gs, turn):
                stale_mate = True
                active =  False


            circle_group.update()
            circle_group.draw(screen)

        else:
            font = pg.font.SysFont("Helvetica", 25)
            if check_mate:
                text1 = font.render(f"{turn} lose", True, "red")
                text1_rect = text1.get_rect(center=(256, 256))

            elif stale_mate:
                text1 = font.render(f"Stalemate", True, "red")
                text1_rect = text1.get_rect(center=(256, 256))

            else:
                text1 = font.render(f"Hit Space to Start", True, "red")
                text1_rect = text1.get_rect(center=(256, 256))

            screen.fill("white")
            screen.blit(text1, text1_rect)

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
    