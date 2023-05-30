from project import move_piece, checkMate, staleMate
from classes import *
import pytest

gs = Game_State()

def test_1():
    assert checkMate(gs, turn="white") == False


def test_2():
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

    assert checkMate(gs, turn="white") == True


def test_3():
    assert move_piece([(6,0), (3,0)], gs) == False

def test_4():
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

    print(len(gs.white_pieces))

    assert move_piece([(7,4),(7,3)], gs) == False


def test_5():
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
    gs.black_pieces = {Queen("bQ.png", "black"),King("bK.png", "black")}
    gs.white_pieces = {King("wK.png", "white")}
    gs.blackKing = (6,7)
    staleMate(gs, turn="white")