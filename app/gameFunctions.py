# ChewyChupucabras - Tanzeem Hasan, Ethan Sie, Brian Liu
# SoftDev
# P02:
# 2024-01-XX
# Time Spent: not enough hours

import db
import random


#recieves username of players (could be changed to challengeID); gives them 6 random pokemon with 4 random moves
def startgame(player1, player2):
    id = 1 if db.getLatestGameHistory() == -1 else db.getLatestGameHistory()[0] + 1

    for player in [player1, player2]:
        # Retrieve user's existing team from gamePokeSets
        user_team = db.getTableData("gamePokeSets", "user", player)
        counter = 0  # Counter for total Pokémon added to the team
        
        # If no team exists, initialize a new random team
        if user_team == -1:
            user_team = [None] * 7  # Placeholder for 6 Pokémon slots + user column
        
        for i in range(1, 7):  # Check all six slots in the team
            if user_team[i] is not None:  # Slot is filled
                poke_name = user_team[i]
                try:
                    # Get 4 random moves for this Pokémon
                    move1_ID = db.getAllTableData("pokemon_moves", "poke_name", poke_name)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", poke_name)) - 1)][1]
                    move2_ID = db.getAllTableData("pokemon_moves", "poke_name", poke_name)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", poke_name)) - 1)][1]
                    move3_ID = db.getAllTableData("pokemon_moves", "poke_name", poke_name)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", poke_name)) - 1)][1]
                    move4_ID = db.getAllTableData("pokemon_moves", "poke_name", poke_name)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", poke_name)) - 1)][1]
                except:
                    print(f"Failed to initialize moves for existing Pokémon: {poke_name}")
                    continue
                # Add Pokémon to gamePokeStats
                db.updateGamePokeList(
                    id, player, poke_name,
                    0.01 * (db.getTableData("pokeDex", "poke_name", poke_name)[4] * 2) * 100 + 110,
                    "True" if counter == 0 else "False",  # Mark first Pokémon as active
                    move1_ID, move2_ID, move3_ID, move4_ID
                )
                counter += 1
            else:  # Slot is empty; add a random Pokémon
                while True:
                    randomPoke = db.getTable("pokeDex")[random.randint(0, len(db.getTable("pokeDex")) - 1)][1]
                    try:
                        # Get 4 random moves for this Pokémon
                        move1_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
                        move2_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
                        move3_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
                        move4_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
                    except:
                        print(f"Failed to initialize random Pokémon: {randomPoke}")
                        continue
                    # Add Pokémon to gamePokeStats
                    db.updateGamePokeList(
                        id, player, randomPoke,
                        0.01 * (db.getTableData("pokeDex", "poke_name", randomPoke)[4] * 2) * 100 + 110,
                        "True" if counter == 0 else "False",  # Mark first Pokémon as active
                        move1_ID, move2_ID, move3_ID, move4_ID
                    )
                    break  # Exit the random Pokémon loop once successful
                counter += 1
            # Stop once we have 6 Pokémon
            if counter >= 6:
                break



                

#recieves game_id, username of player that's swapping, and name of the pokemon to swap into; updates gamePokeStats so new Pokemon is switched to active
def swapPokemon(game_id, username, swapPokeName):
    print(db.getAllTableData("gamePokeStats", "game_ID", game_id))
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "True":
            db.setTableData("gamePokeStats", "active_status", "False", "poke_name", pokemon[2]) #POSSIBLE ISSUE if there are multiple pokemon of the same name in the db
        elif pokemon[1] == username and pokemon[4] == "False" and pokemon[2] == swapPokeName:
            db.setTableData("gamePokeStats", "active_status", "True", "poke_name", pokemon[2])

#helper function to get the name of the current active pokemon based on username and gameID -- may delete later cuz idk if this is really necessary
def getCurrActivePokemon(game_id, username):
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "True":
            return pokemon[2]

def endGame():
    return

#my idea of how this could work:
#recieves gameId and action of first player (idk how this will be implemented) and action of second player (maybe by move name? or "swap" if swapping)
#uses function to get active pokemon speed to determine who moves first
#calls swapPokemon if user needs to swap
#calls calcDamage(move used, pokemon1, pokemon2)
#checks if the reciveing pokemon is dead, if yes force swap
#if no, calls calcDamage(move used, pokemon2, pokemon1)
#checks if the reciveing pokemon is dead, if yes force swap
#calls a function to check if all pokemon are alive; if no, end game and update gameHistory
#repeat
def turn():
    return

#recieves name of move used, name of attacking pokemon, name of recieving pokemon; returns dmg
def damageCalc(move, attacker, reciever):
    #Base Stats + RNG
    pokeLevel = 100 #probably standardized?
    crtical = 2 if (random.randint(0, 255) > random.randint(0, 255)) else 1
    movePower = db.getTableData("moves", "name", move)[3]
    rng = (random.randint(217, 255)) / 255
    #ATK + DEF Stats
    if (db.getTableData("moves", "name", move)[6] == 'physical'):
        attackerATK = db.getTableData("pokeDex", "poke_name", attacker)[5]
        recieverDEF = db.getTableData("pokeDex", "poke_name", reciever)[6]
    else:
        attackerATK = db.getTableData("pokeDex", "poke_name", attacker)[7]
        recieverDEF = db.getTableData("pokeDex", "poke_name", reciever)[8]
    #Same Attack Type Bonus
    stab = 1.5 if db.getTableData("moves", "name", move)[2] == db.getTableData("pokeDex", "poke_name", attacker)[2] or db.getTableData("moves", "name", move)[2] == db.getTableData("pokeDex", "poke_name", attacker)[3] else 1
    #Type Matchup Multipliers
    movetype = db.getTableData("moves", "name", move)[2]
    typeMultipler = 1
    for recievertype in [db.getTableData("pokeDex", "poke_name", reciever)[2], db.getTableData("pokeDex", "poke_name", reciever)[3]]:
        if recievertype:
            if (recievertype in db.getTableData("types", "type", movetype)[3]):
                typeMultipler *= 2
            if (recievertype in db.getTableData("types", "type", movetype)[5]):
                typeMultipler *= 0.5
            if (recievertype in db.getTableData("types", "type", movetype)[7]):
                typeMultipler *= 0
    #print(f"level: {pokeLevel}, crit: {crtical}, power: {movePower}")
    #print(f"atk: {attackerATK}, def: {recieverDEF}, stab: {stab}, rng: {rng}")
    #print(f"typeMulti: {typeMultipler}")

    return (((((((2.0 * pokeLevel * crtical) / 5) + 2) * movePower * attackerATK / recieverDEF) / 50) + 2) * stab * typeMultipler * rng)

#recieves id of the game; updates players' elo based on winner/loser
def updateElo(gameID):
    winner_user = db.getTableData("gameHistory", "game_ID", gameID)[1]
    loser_user = db.getTableData("gameHistory", "game_ID", gameID)[2]

    pokemonAlive = 0
    match_pokemon = (db.getAllTableData("gamePokeStats", "game_ID", gameID)) # gets data of all the pokemon in the match from gamePokeStats
    for pokemon_data in match_pokemon:
        print(pokemon_data)
        if pokemon_data[1] == winner_user and pokemon_data[3] > 0:
            pokemonAlive += 1

    winner_elo = db.getTableData("users", "username", winner_user)[3] + 10 + (pokemonAlive * 5)
    loser_elo = db.getTableData("users", "username", loser_user)[3] - 20

    db.setTableData("users", "rank", winner_elo, "username", winner_user)
    db.setTableData("users", "rank", loser_elo, "username", loser_user)

#too many helper functions
def getCurrActivePokemon(game_id, username):
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "True":
            return pokemon[2]

def getInActivePokemonTypes(game_id, username):
    pokeList = []
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        types = []
        if pokemon[1] == username and pokemon[4] == "False":
            types = [db.getTableData("pokeDex", "poke_name", pokemon[2])[2]]
            if db.getTableData("pokeDex", "poke_name", pokemon[2])[3]:
                types.append(db.getTableData("pokeDex", "poke_name", pokemon[2])[3])
            pokeList.append(types)
    return pokeList
def getInActivePokemon(game_id, username):
    pokeList = []
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "False":
            pokeList.append(pokemon[2])
    return pokeList
def getAlivePokemon(game_id, username):
    pokeList = []
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "False" and pokemon[3] > 0:
            pokeList.append(pokemon[2])
    return pokeList

def getActivePokemonMoves(game_id, username):
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "True":
            return [db.getTableData("moves", "id", pokemon[5])[1], db.getTableData("moves", "id", pokemon[6])[1], db.getTableData("moves", "id", pokemon[7])[1], db.getTableData("moves", "id", pokemon[8])[1]]
def getActivePokemonMovesTypes(game_id, username):
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "True":
            return [db.getTableData("moves", "id", pokemon[5])[2], db.getTableData("moves", "id", pokemon[6])[2], db.getTableData("moves", "id", pokemon[7])[2], db.getTableData("moves", "id", pokemon[8])[2]]
def getPokeSprite(pokeName):
    pokeData = db.getTableData("pokeDex", "poke_name", pokeName)
    if not isinstance(pokeData, (list, tuple)) or len(pokeData) <= 10:
        raise ValueError(f"Invalid data for pokeName '{pokeName}': {pokeData}")
    return pokeData[10]

def getActivePokemonHP(game_id, username):
    for pokemon in db.getAllTableData("gamePokeStats", "game_ID", game_id):
        if pokemon[1] == username and pokemon[4] == "True":
            return pokemon[3]

def updateActiveHP(game_id, username, pokeName, damage):
    newHP = 0 if getActivePokemonHP(game_id, username) - damage < 0 else getActivePokemonHP(game_id, username) - damage
    db.setActiveHP(newHP, game_id, username, pokeName)
