import sqlite3
import sys
import string

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me less than six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"

    connection = sqlite3.connect("pokemon.sqlite")
    try:
        cursor = connection.cursor()
        
        # Check if input is numeric. If it is, search for pokemon by pokedex number.
        if arg.isdigit():
            cursor.execute("SELECT pokemon.pokedex_number, pokemon.name, pokemon_types_view.type1, pokemon_types_view.type2 " +
                           ", against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water" +
                           " FROM pokemon " +
                           " JOIN pokemon_types_view ON pokemon.name = pokemon_types_view.name " +
                           " LEFT JOIN battle ON pokemon_types_view.type1 = battle.type1name " +
                           " AND pokemon_types_view.type2 = battle.type2name " +
                           " WHERE pokemon.pokedex_number = ? " +
                           " GROUP BY pokemon.pokedex_number ", (arg,))
            results = cursor.fetchall()
       
        # If user input is not numeric (i.e. string), search for pokemon by pokemon name (case-insensitive).
        else:
            arg = string.capwords(arg)
            cursor.execute("SELECT pokemon.pokedex_number, pokemon.name, pokemon_types_view.type1, pokemon_types_view.type2 " +
                           ", against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water" +
                           " FROM pokemon " +
                           " JOIN pokemon_types_view ON pokemon.name = pokemon_types_view.name " +
                           " LEFT JOIN battle ON pokemon_types_view.type1 = battle.type1name " +
                           " AND pokemon_types_view.type2 = battle.type2name " +
                           " WHERE pokemon.name = ? " +
                           " GROUP BY pokemon.pokedex_number ", (arg,))
            results = cursor.fetchall()

        if len(results) == 0:
                print("No Pokemon found with pokemon name", arg)
        else:
            (pokedex_number, name, poke_type1, poke_type2, *against) = results[0]
            strong_against = [t for t, a in zip(types, against) if a is not None and float(a) < 1]
            weak_against = [t for t, a in zip(types, against) if a is not None and float(a) > 1]
                # This does not work:
                # strong_against = [poke_types[i] for i in range(len(types)) if float(against[i]) > 1]
                # weak_against = [poke_types[i] for i in range(len(types)) if float(against[i]) < 1]
            print(f"Analyzing {arg}\n{name} ({poke_type1} {poke_type2}) is strong against {strong_against} but weak against {weak_against}")
    
    finally:
        connection.close()

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")