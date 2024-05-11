# import graphs  # for undirected graphs
# import digraphs  # for directed graphs
import csv
import graphs
import digraphs


def gamesOK(games):
    players = {player for game in games for player in game}
    player_games = {player: {
        opponent for game in games if player in game for opponent in game if opponent != player} for player in players}
    return all(
        len(player_games[player]) == len(player_games[next(iter(players))]) and
        all(
            opponent in player_games[player] or len(
                player_games[player] & player_games[opponent]) >= 2
            for opponent in players if opponent != player
        )
        for player in players
    )


def gameReferees(games, csvfilename):
    with open(csvfilename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        referees = {row['Referee']: {
            conflict for conflict in row.values() if conflict} for row in reader}

    possible_referees = {game: {
        referee for referee in referees if not referees[referee] & set(game)} for game in games}
    assigned_referees = {}

    for game in games:
        for referee in possible_referees[game]:
            if referee not in assigned_referees.values():
                assigned_referees[game] = referee
                break
        else:
            return None

    return assigned_referees if len(assigned_referees) == len(games) else None


def gameGroups(assignedReferees):
    # Extract the set of all games
    games = set(assignedReferees.keys())

    # Create vertices (V) for each game
    V = games

    # Create edges (E) between games that cannot be played at the same time
    E = {
        (game1, game2) for game1 in games for game2 in games
        if game1 != game2 and (
            set(game1) & set(game2) or
            assignedReferees[game1] in game2 or
            assignedReferees[game2] in game1 or
            assignedReferees[game1] == assignedReferees[game2]
        )
    }

    # Make the edge set symmetric
    E = E.union({(v, u) for (u, v) in E})

    # Use the minColouring function from graphs.py to find the chromatic number and a coloring for the graph
    k, C = graphs.minColouring(V, E)

    # Use the coloring to create timeslots
    timeslots = graphs.colourClassesFromColouring(C)

    # Convert the sets of games into a list of timeslots
    timeslots_list = [list(timeslot) for timeslot in timeslots]

    return timeslots_list


def gameSchedule(assignedReferees, gameGroups):
    players = {player for game in assignedReferees for player in game}
    ref_games = {player: [
        game for game in assignedReferees if assignedReferees[game] == player] for player in players}
    player_games = {player: [
        game for game in assignedReferees if player in game] for player in players}

    schedule = []
    while gameGroups:
        for timeslot in gameGroups:
            if all(
                all(game not in ref_games[player] for game in timeslot) or
                all(game in schedule for game in player_games[player])
                for player in players
            ):
                schedule.extend(timeslot)
                gameGroups.remove(timeslot)
                break
        else:
            return None
    return schedule
