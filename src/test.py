from main import move_piece, checkMate, staleMate, update_atrs
from classes import *


def test_checkMate():
    gs = Game_State()
    gs.board = [
    [Castle("../assets/images/bR.png", "black"), '--', Bishop("../assets/images/bB.png", "black"), '--', King("../assets/images/bK.png", "black"), '--', Knight("../assets/images/bN.png", "black"), Castle("../assets/images/bR.png", "black")],
    [Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), '--', '--', Pawn("../assets/images/bp.png", "black")],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', Pawn("../assets/images/wp.png", "white"), '--',  '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', Queen("../assets/images/wQ.png", "white"), '--', '--', '--', Knight("../assets/images/wN.png", "white"), '--', '--'],
    [Pawn("../assets/images/wp.png", "white"), '--', Pawn("../assets/images/wp.png", "white"), '--', Pawn("../assets/images/wp.png", "white"), Pawn("../assets/images/wp.png", "white"), Pawn("../assets/images/wp.png", "white"), Pawn("../assets/images/wp.png", "white")],
    [Castle("../assets/images/wR.png", "white"), Knight("../assets/images/wN.png", "white"),Queen("../assets/images/bQ.png", "black"), '--', King("../assets/images/wK.png", "white"), Bishop("../assets/images/wB.png", "white"), '--', Castle("../assets/images/wR.png", "white")]
    ]

    update_atrs(gs)

    assert checkMate(gs, turn="white") == True


def test_move_piece():
    gs = Game_State()
    update_atrs(gs)
    assert move_piece([(6,0), (5,0)], gs, turn="white") == True


    gs = Game_State()
    gs.board = [
    [Castle("../assets/images/bR.png", "black"), '--', Bishop("../assets/images/bB.png", "black"), '--', King("../assets/images/bK.png", "black"), '--', Knight("../assets/images/bN.png", "black"), Castle("../assets/images/bR.png", "black")],
    [Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), Pawn("../assets/images/bp.png", "black"), '--', '--', Pawn("../assets/images/bp.png", "black")],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', Pawn("../assets/images/wp.png", "white"), '--',  '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', Queen("../assets/images/wQ.png", "white"), '--', '--', '--', Knight("../assets/images/wN.png", "white"), '--', '--'],
    [Pawn("../assets/images/wp.png", "white"), '--', Pawn("../assets/images/wp.png", "white"), '--', Pawn("../assets/images/wp.png", "white"), Pawn("../assets/images/wp.png", "white"), Pawn("../assets/images/wp.png", "white"), Pawn("../assets/images/wp.png", "white")],
    [Castle("../assets/images/wR.png", "white"), Knight("../assets/images/wN.png", "white"),Queen("../assets/images/bQ.png", "black"), '--', King("../assets/images/wK.png", "white"), Bishop("../assets/images/wB.png", "white"), '--', Castle("../assets/images/wR.png", "white")]
    ]

    update_atrs(gs)

    assert move_piece([(7,4),(7,3)], gs, turn="white") == False


def test_staleMate():
    gs = Game_State()
    gs.board = [
    ['--' for n in range(8)],
    ['--' for n in range(8)],
    ['--' for n in range(8)],
    ['--' for n in range(8)],
    ['--' for n in range(8)],
    ['--' for n in range(8)],
    ['--', '--', '--', Queen("../assets/images/bQ.png", "black"), '--', '--', '--',  King("../assets/images/bK.png", "black")],
    ['--', '--','--', '--', '--', King("../assets/images/wK.png", "white"), '--', '--']
    ]
    update_atrs(gs)
    staleMate(gs, turn="white")