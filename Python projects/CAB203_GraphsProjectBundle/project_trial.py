# import graphs  # for undirected graphs
# import digraphs  # for directed graphs
from digraphs import N_out, topOrdering
from digraphs import maxMatching
import csv
import digraphs
import graphs


def gamesOK(games):
    # Create the set of vertices (players) and edges (games)
    V = {player for game in games for player in game}
    E = {game for game in games} | {(v, u) for (u, v) in games}

    def check_pairs(pairs):
        # Base case: if no more pairs to check, return True
        if not pairs:
            return True

        # Check the first pair in the list
        u, v = pairs[0]
        if (u, v) not in E and (v, u) not in E:
            common_players = list(digraphs.N_out(
                V, E, u) & digraphs.N_out(V, E, v))
            if len(common_players) < 2:
                return False

        # Recursively check the rest of the pairs
        return check_pairs(pairs[1:])

    # Create a list of all pairs of distinct players
    pairs = [(u, v) for u in V for v in V if u != v]

    # Check if all players have the same number of games
    degrees = [len(digraphs.N_out(V, E, player)) for player in V]
    if len(set(degrees)) > 1:
        return False

    return check_pairs(pairs)


def referees(games, csvfilename):
    # Read the CSV file to get the conflicts of interest for each referee
    with open(csvfilename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        conflicts = {row[0]: set(row[1:]) for row in reader}

    # Create a list of referees
    referees = list(conflicts.keys())

    # Create a list of games
    games = list(games)

    def assign_referee(i, j):
        # Base case: if all games have been assigned a referee, return the assignments
        if i == len(games):
            return {game: referee for game, referee in zip(games, referees)}

        # If no more referees to try, return None
        if j == len(referees):
            return None

        game = games[i]
        referee = referees[j]

        # Check if the referee has a conflict of interest with the current game
        if referee not in game and not (set(game) & conflicts[referee]):
            # Swap the current referee with the referee at position i
            referees[i], referees[j] = referees[j], referees[i]

            # Recursively assign referees to the rest of the games
            result = assign_referee(i + 1, i + 1)

            # If we found a valid assignment, return it
            if result is not None:
                return result

            # Swap the referees back
            referees[i], referees[j] = referees[j], referees[i]

        # Recursively try the next referee
        return assign_referee(i, j + 1)

    # Start the recursive function
    return assign_referee(0, 0)


def gameGroups(assignedReferees):
    # Extract the set of all games
    games = set(assignedReferees.keys())

    # Create vertices (V) for each game
    V = games

    # Create edges (E) between games that cannot be played at the same time
    E = {
        frozenset({game1, game2}) for game1 in games for game2 in games
        if game1 != game2 and (
            set(game1) & set(game2) or
            assignedReferees[game1] in game2 or
            assignedReferees[game2] in game1 or
            assignedReferees[game1] == assignedReferees[game2]
        )
    }

    # Make the edge set symmetric by converting frozensets to tuples
    E_symmetric = {(u, v) for edge in E for u, v in [tuple(edge)]}
    E_symmetric.update({(v, u) for (u, v) in E_symmetric})

    # Use the minColouring function from graphs.py to find the chromatic number and a coloring for the graph
    k, C = graphs.minColouring(V, E_symmetric)

    # Use the coloring to create timeslots
    timeslots = graphs.colourClassesFromColouring(C)

    # Convert the sets of games into a list of sets for timeslots
    timeslots_list = [timeslot for timeslot in timeslots]

    return timeslots_list


def gameSchedule(assignedReferees, gameGroups):
    # Create vertices (V) for each game group
    V = set(range(len(gameGroups)))

    # Recursive function to build edges based on refereeing relationships
    def build_edges(gameGroups, assignedReferees, i=0, j=0, E=set()):
        if i >= len(gameGroups):
            return E
        if j >= len(gameGroups):
            return build_edges(gameGroups, assignedReferees, i + 1, 0, E)
        if i != j:
            referees_in_group1 = {assignedReferees.get(
                game) for game in gameGroups[i]}
            players_in_group2 = {
                player for game in gameGroups[j] for player in game}
            if referees_in_group1.intersection(players_in_group2):
                E.add((j, i))  # Reverse the direction of the edge
        return build_edges(gameGroups, assignedReferees, i, j + 1, E)

    # Build edges (E) using the recursive function
    E = build_edges(gameGroups, assignedReferees)

    # Use the topOrdering function from digraphs.py to attempt to find a topological ordering
    ordering = digraphs.topOrdering(V, E)

    # If topOrdering returns None, it means there is no valid ordering (i.e., there is a cycle)
    if ordering is None:
        return None

    # Use a comprehension to order the game groups based on the topological ordering
    ordered_game_groups = [gameGroups[i] for i in ordering]

    return ordered_game_groups


def scores(p, s, c, games):
    # Define vertices and edges for the directed graph
    V = {player for game in games for player in game}
    E = {(winner, loser) for winner, loser in games}

    # Calculate primary wins using N_out
    primary_wins = {player: N_out(V, E, player) for player in V}

    # Calculate primary scores
    primary_scores = {player: p * len(wins)
                      for player, wins in primary_wins.items()}

    # Calculate secondary wins using NS_out and N_in
    secondary_wins = {
        player: {sec_player for opponent in primary_wins[player]
                 for sec_player in N_out(V, E, opponent) if sec_player != player}
        for player in V
    }

    # Remove primary wins from secondary wins to avoid double counting
    secondary_wins = {
        player: secondary_wins[player] - primary_wins[player] for player in V}

    # Calculate secondary scores with a cap
    secondary_scores = {
        player: min(s * len(secondary_wins[player]), c)
        for player in V
    }

    # Combine primary and secondary scores
    total_scores = {
        player: primary_scores[player] + secondary_scores[player] for player in V}

    return total_scores
