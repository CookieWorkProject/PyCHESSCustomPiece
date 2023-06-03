from main import move_piece, checkMate, staleMate, update_atrs
from classes import *


def test_checkMate():
    gs = Game_State()
    gs.board = [
    [Castle("bR.png", "black"), '--', Bishop("bB.png", "black"), '--', King("bK.png", "black"), '--', Knight("bN.png", "black"), Castle("bR.png", "black")],
    [Pawn("bp.png", "black"), Pawn("bp.png", "black"), Pawn("bp.png", "black"), Pawn("bp.png", "black"), Pawn("bp.png", "black"), '--', '--', Pawn("bp.png", "black")],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', Pawn("wp.png", "white"), '--',  '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', Queen("wQ.png", "white"), '--', '--', '--', Knight("wN.png", "white"), '--', '--'],
    [Pawn("wp.png", "white"), '--', Pawn("wp.png", "white"), '--', Pawn("wp.png", "white"), Pawn("wp.png", "white"), Pawn("wp.png", "white"), Pawn("wp.png", "white")],
    [Castle("wR.png", "white"), Knight("wN.png", "white"),Queen("bQ.png", "black"), '--', King("wK.png", "white"), Bishop("wB.png", "white"), '--', Castle("wR.png", "white")]
    ]

    update_atrs(gs)

    assert checkMate(gs, turn="white") == True


def test_move_piece():
    gs = Game_State()
    update_atrs(gs)
    assert move_piece([(6,0), (5,0)], gs, turn="white") == True


    gs = Game_State()
    gs.board = [
    [Castle("bR.png", "black"), '--', Bishop("bB.png", "black"), '--', King("bK.png", "black"), '--', Knight("bN.png", "black"), Castle("bR.png", "black")],
    [Pawn("bp.png", "black"), Pawn("bp.png", "black"), Pawn("bp.png", "black"), Pawn("bp.png", "black"), Pawn("bp.png", "black"), '--', '--', Pawn("bp.png", "black")],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', Pawn("wp.png", "white"), '--',  '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', Queen("wQ.png", "white"), '--', '--', '--', Knight("wN.png", "white"), '--', '--'],
    [Pawn("wp.png", "white"), '--', Pawn("wp.png", "white"), '--', Pawn("wp.png", "white"), Pawn("wp.png", "white"), Pawn("wp.png", "white"), Pawn("wp.png", "white")],
    [Castle("wR.png", "white"), Knight("wN.png", "white"),Queen("bQ.png", "black"), '--', King("wK.png", "white"), Bishop("wB.png", "white"), '--', Castle("wR.png", "white")]
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
    ['--', '--', '--', Queen("bQ.png", "black"), '--', '--', '--',  King("bK.png", "black")],
    ['--', '--','--', '--', '--', King("wK.png", "white"), '--', '--']
    ]
    update_atrs(gs)
    staleMate(gs, turn="white")