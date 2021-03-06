"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def calculate_distance(game, player, opp_player):
    """Helper function to calculate the total distance between the player current
    location and its opponent's location
    """

    player_location = game.get_player_location(player)
    opponnent_location = game.get_player_location(opp_player)
    x_distance = math.pow(player_location[0] - opponnent_location[0], 2)
    y_distance = math.pow(player_location[1] - opponnent_location[1], 2)
    return math.sqrt(x_distance + y_distance)


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Look ahead heuristic
    Calculate the difference in the number of legal moves in the current state
    of the game plus the number of legal moves of the next phase

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float('-inf')

    if game.is_winner(player):
        return float('inf')

    player_legal_moves = game.get_legal_moves(player)
    player_moves_length = len(player_legal_moves)
    for legal_move in player_legal_moves:
        next_phase = game.forecast_move(legal_move)
        # On next phase the player is the opponent
        next_phase_player = next_phase.get_opponent(next_phase.active_player)
        next_phase_moves = next_phase.get_legal_moves(next_phase_player)
        player_moves_length += len(next_phase_moves)

    opponent_legal_moves = game.get_legal_moves(game.get_opponent(player))
    opponent_moves_length = len(opponent_legal_moves)
    for legal_move in opponent_legal_moves:
        next_phase = game.forecast_move(legal_move)
        # On the next phase the opponent is the active player
        # So by default get_legal_moves use the active player
        opponent_next_legal_moves = next_phase.get_legal_moves()
        opponent_moves_length += len(opponent_next_legal_moves)

    return float(player_moves_length - opponent_moves_length)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Run boy run
    Get the max distance between the player and the opponent,
    run away from the opponent. Returns the absolute difference
    between the sum of the locations, higher distance means higher score.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_player = game.get_opponent(player)
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(opp_player))

    distance = calculate_distance(game, player, opp_player)
    return float((own_moves + distance) - opp_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Dangerous chase
    Get the min distance between the player and the opponent, chase
    down the opponent. Returns the negative of the absolute difference
    between the sum of the locations, smaller distance means higher scores

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent_location = game.get_player_location(game.get_opponent(player))
    if opponent_location is None:
        return 0

    player_location = game.get_player_location(player)
    if player_location is None:
        return 0

    return float(-abs(sum(opponent_location) - sum(player_location)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        results = self.min_max_common(game, depth, True)
        best_move = results[1]
        return best_move

    def min_max_common(self, game, depth, get_max_value):
        """Common code base for min_value and max_value
            Checks for depth in order to return the score
            or continue the recursive search also have
            the terminal test that consist to check if there
            are legal moves available

        Parameters
        ----------
        get_max_value: int
            Indicates if it will try to get the max value or the min value

        Returns the highest(get_max_value=True) or lowest(get_max_value=False)
        score/move tuple found in game
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Finally we are were we wanted! The max_depth
        if depth == 0:
            # So lets get the score
            return self.score(game, self), None

        # Terminal test
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (game.utility(self), (-1, -1))

        # Are we going for the max value or the min value?
        if get_max_value is True:
            return self.max_value(game, depth, legal_moves)
        else:
            return self.min_value(game, depth, legal_moves)

    def max_value(self, game, depth, legal_moves):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        highest_score = float('-inf')
        selected_move = (-1, -1)
        for move in legal_moves:
            results = self.min_max_common(
                game.forecast_move(move), depth - 1, False)
            score = results[0]
            highest_score, selected_move = max(
                (highest_score, selected_move), (score, move))
        return (highest_score, selected_move)

    def min_value(self, game, depth, legal_moves):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        lowest_score = float('inf')
        selected_move = (-1, -1)
        for move in legal_moves:
            results = self.min_max_common(
                game.forecast_move(move), depth - 1, True)
            score = results[0]
            lowest_score, selected_move = min(
                (lowest_score, selected_move), (score, move))
        return (lowest_score, selected_move)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return -1, -1

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = legal_moves[0]
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            # Depth used for iterative deepening
            depth = 0
            # while True:
            inf = float('inf')
            while depth < inf:
                depth += 1
                best_move = self.alphabeta(game, depth)

        except SearchTimeout:
            pass

        # Safety check
        if best_move == (-1, -1) and legal_moves:
            # Not giving up, we fight till the end!
            return legal_moves[0]

        # Best move from the last recursive search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        results = self.alpha_beta_common(game, depth, alpha, beta, True)
        best_move = results[1]
        return best_move

    def alpha_beta_common(self, game, depth, alpha, beta, get_max_value):
        """Common code base for min_value and max_value
            Checks for depth in order to return the score
            or continue the recursive search also have
            the terminal test that consist to check if there
            are legal moves available

        Parameters
        ----------
        get_max_value: int
            Indicates if it will try to get the max value or the min value

        Returns the highest(get_max_value=True) or lowest(get_max_value=False)
        score/move tuple found in game
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Finally we are were we wanted! The max_depth
        if depth == 0:
            # So lets get the score
            return self.score(game, self), None

        # Terminal test
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (game.utility(self), (-1, -1))
        # return 10, legal_moves[0]

        # Are we going for the max value or the min value?
        if get_max_value:
            return self.alphabeta_max_value(game, legal_moves, depth,
                                            alpha, beta)
        else:
            return self.alphabeta_min_value(game, legal_moves, depth,
                                            alpha, beta)

    def alphabeta_max_value(self, game, legal_moves, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        highest_score = float('-inf')
        selected_move = (-1, -1)
        for move in legal_moves:
            results = self.alpha_beta_common(game.forecast_move(
                move), depth - 1, alpha, beta, False)
            score = results[0]
            if score > alpha:
                alpha = score
                highest_score, selected_move = score, move
            if alpha >= beta:
                # Let the prune happen
                break
        return (highest_score, selected_move)

    def alphabeta_min_value(self, game, legal_moves, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        lowest_score = float('inf')
        selected_move = (-1, -1)
        for move in legal_moves:
            results = self.alpha_beta_common(game.forecast_move(
                move), depth - 1, alpha, beta, True)
            score = results[0]
            if score < beta:
                beta = score
                lowest_score, selected_move = score, move
            if beta <= alpha:
                # Let the prune happen
                break
        return (lowest_score, selected_move)
