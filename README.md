# PyCHESS

## PyCHESS is a Player versus Player (PVP) chess game implemented in Python using the Pygame library.

## Project Files
The PyCHESS project consists of the following files:

### project.py
project.py is the main file of the PyCHESS game. It contains important functions and features, including:

#### update_attrs()
The update_attrs() function updates the attributes of the Game_State object, such as the location of the white king, black king, black pieces, and white pieces.

#### draw_pieces()
The draw_pieces() function recreates the game state on the GUI board, displaying the chess pieces.

#### move_piece()
The move_piece() function handles the movement of selected pieces. It takes a list of two tuple coordinates, indicating the start position and the end position of the piece, as well as the game turn and the Game_State object. Within this function, several important blocks are present:
* En passant move block: Checks for en passant moves.
* Castling move block: Checks for castling moves.
* awn promotion block: Checks for pawn promotion.

#### checkMate()
The checkMate() function checks if the current board configuration leads to checkmate for the current turn.

#### StaleMate()
The StaleMate() function checks if the current board configuration results in a stalemate.

#### main()
The main() function initializes important game variables and contains the main game loop. Within this loop, user input, such as mouse clicks or keyboard presses, is processed, and the screen is updated at a rate of 60 frames per second.

### Classes.py
Classes.py contains essential classes used in the PyCHESS game:

#### Piece
The Piece class is a parent class inherited by all chess pieces. It defines attributes such as the piece's image and color. Specific piece classes override instance methods like get_moves() and get_valid_moves(). The get_moves() method generates all possible moves for a given piece, while get_valid_moves() checks if each move would result in the king being in check and removes invalid moves.

#### Game_State
The Game_State class is the core class of the program. It includes attributes such as the game board, positions of both black and white kings, and lists of black and white pieces. Instance methods like get_pos(), if_Check(), squareUnderAttack(), Pseudo_move(), and undo_move() handle various aspects of the game logic. These methods facilitate tasks such as obtaining a piece's position, checking if a king is in check, generating possible moves, making the moves and undoing moves.

#### Squares, Circle, Rectangle
* The Squares class represents each square on the chessboard. It has parameters for color and position on the screen.

* The Circle class is responsible for highlighting valid moves on the GUI board.

* The Rectangle class is crucial for implementing pawn promotion. It provides a dropdown menu-like feature on the GUI board and includes attributes such as promotion pieces, which assigns a dictionary of promotion pieces based on the pawn's color. The display_images() instance method recreates the dropdown menu, displaying each promotion piece. The assign_pieces() method handles user clicks and assigns the clicked piece.

### Image and Sound Files
The PyCHESS project includes image files representing chess piece images and sound files for move, capture, and castle effects. These files are used to enhance the visual and auditory experience of the game.

### test_project.py
This program tests the move_piece, checkMate and staleMate functions of project.py. It makes use of hardcorded board configuration

## Known Issues
* The UI is not user-friendly, I will like to improve on it.
* There are lots of redundancies in the program, I didn't really map out the structure of the program at the start and I had to make so many changes as I went on, forgetting to eliminate some redundancies
* There are some special chess rules like fifty move and threefold repitition rules which I have not yet implemented
* I will like to implement an AI, so users can able to play vs COM.
* There is no win by resigning as well.


## Contributors
If you have identified an issue or have suggestions for improvements to the program, you are welcome to contribute to the project. To contribute, please follow the steps below:

* Fork the repository on GitHub.
* Make the necessary changes and improvements in your local fork.
* Test your changes to ensure they are functioning correctly.
* Commit your changes and push them to your forked repository.
* Create a pull request from your forked repository to the main repository.
* Please provide a clear and concise description of the changes or improvements you have made in the pull request.

Thank you for helping to enhance the program! Your contribution means a lot to me.


## Dependencies
The PyCHESS game requires the following dependencies:

* Python (version 3.2)
* Pygame (version 2.3.0)

Please make sure you have Python and Pygame installed before running the game.

## Installation
* Clone or download the PyCHESS repository.
* Install Python (version 3.2) from the official Python website (https://www.python.org).
* Install Pygame (version 2.3.0) by running the following command: pip install Pygame

## Running the Game
To run the PyCHESS game, follow these steps:

* Open your terminal or command prompt.
* Navigate to the directory where you cloned or downloaded the PyCHESS repository.
* Run the following command to start the game: python project.py

## License
PyChess is released under the MIT License. You are free to use, modify, and distribute this software. See the LICENSE file for more details.
    