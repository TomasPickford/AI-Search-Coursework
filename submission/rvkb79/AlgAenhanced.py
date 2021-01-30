############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import os
import sys
import time
import random

############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r') 
    current_char = the_file.read(1) 
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}   
    tariff_dictionary = {}  
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"  
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)  
    location = 0
    EOF = False
    list_of_items = []  
    while EOF == False: 
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT 
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############

input_file = "AISearchfile058.txt"

############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

the_particular_city_file_folder = "city-files"
    
if os.path.isfile("../" + the_particular_city_file_folder + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string("../" + the_particular_city_file_folder + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY 
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############

############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME, E.G., 'abcd12'.
############

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs("../alg_codes_and_tariffs.txt")

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR USER-NAME, E.G., "abcd12"
############

my_user_name = "rvkb79"

############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT 
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############

my_first_name = "Tomas"
my_last_name = "Pickford"

############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############

algorithm_code = "AC"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the agorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first 
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = ""

############
############ NOW YOUR CODE SHOULD BEGIN.
############

start_time = time.time()
time_limit = 57 # seconds

# dist_matrix
# num_cities

# DEFINE PARAMETERS
num_ants = num_cities # = num_cities recommended, but might be too many for large city sets
num_iterations = 50 # more iterations only improve the tours

phero_decay = 0.2 # rho (0.5 or 0.1 for ASrank)
phero_weight = 1 # alpha (1)
heuristic_weight = 4 # beta (2-5)
w = min(10,num_ants) # number of top ants that may deposit pheromone (can't be more than the number of ants)
# the parameter init_phero_level is defined within the function initPheroMatrix() and is dependent on w, phero_decay and the length of a tour from the Nearest Neighbour heuristic

# IMPLEMENTATION SPECIFIC PARAMETERS
min_dist_for_heuristic = 0.1 # if the distance to the city is less than this (especially 0), use this minimum distance for division 

# GLOBAL VARIABLES

iteration = 0 # time t
zero_distance = False

def tourCost(tour):
    cost = 0
    for i in range(len(tour)-1):
        cost += dist_matrix[tour[i]][tour[i+1]]
    cost += dist_matrix[tour[i+1]][tour[0]]
    dist_matrix[current_city][next_city]
    return cost

# a 3-opt algorithm for post-processing the best of the ants' tours:
def localSearch(tour,cost):
    best_3opt_tour = tour
    best_3opt_tour_cost = cost
    for cut1 in range(len(tour)):
        for cut2 in range(cut1+1,len(tour)):
            for cut3 in range(cut2+1,len(tour)):
                if time.time() > start_time + time_limit:
                    return [], float("inf") # infinite length ensures it won't be used
                segA = tour[cut1:cut2]
                segB = tour[cut2:cut3]
                segC = tour[cut3:]+tour[:cut1]
                moves = []
                costs = []

                ''' # this is the original tour
                move = segA+segB+segC
                moves.append(move)
                costs.append(tourCost(move))
                '''

                move = segA[::-1]+segB+segC
                moves.append(move)
                costs.append(tourCost(move))

                move = segA+segB+segC[::-1]
                moves.append(move)
                costs.append(tourCost(move))

                move = segA[::-1]+segB+segC[::-1]
                moves.append(move)
                costs.append(tourCost(move))
                
                move = segA[::-1]+segB[::-1]+segC
                moves.append(move)
                costs.append(tourCost(move))
                
                move = segA+segB[::-1]+segC
                moves.append(move)
                costs.append(tourCost(move))
                
                move = segA+segB[::-1]+segC[::-1]
                moves.append(move)
                costs.append(tourCost(move))
                
                move = segA[::-1]+segB[::-1]+segC[::-1]
                moves.append(move)
                costs.append(tourCost(move))

                cheapest = min(costs)
                if cheapest < best_3opt_tour_cost:
                    index = costs.index(cheapest)
                    best_3opt_tour = moves[index]
                    best_3opt_tour_cost = costs[index]
    return best_3opt_tour, best_3opt_tour_cost

def nearestNeighbour():
    unvisited_cities = list(range(num_cities))
    first_city = random.randrange(0, num_cities)
    current_city = first_city
    partial_tour = [first_city]
    partial_tour_length = 0
    unvisited_cities.pop(current_city)
    # build the tour up, one city at a time
    for path in range(num_cities - 1): # there is one less city, and one less edge needed to connect the number of cities, but range() excludes the upper limit
        nearest_city = unvisited_cities[0] # choose any unvisited city's distance to compare the others' distances to
        nearest_distance = dist_matrix[current_city][unvisited_cities[0]]
        # determine which city is the nearest
        for next_city in unvisited_cities: # it doesn't matter that city [0] will be compared against itself
            next_distance = dist_matrix[current_city][next_city]
            if next_distance < nearest_distance:
                nearest_city = next_city
                nearest_distance = next_distance
                break
        # after finding the nearest next city, add it to the path
        partial_tour.append(nearest_city)
        partial_tour_length += nearest_distance
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city

    # once we have visited all cities (unvisited_cities is empty), add the path back to the start
    partial_tour_length += dist_matrix[nearest_city][first_city]
    # don't add the first city to the tour again
    # we only need to return the length of the tour, not the tour itself
    return partial_tour_length

# initialise the pheromone matrix
def initPheroMatrix():
    repeats = 3 # Nearest Neighbour algorithm gives widly varied lengths depending on its starting city
    NN_lengths = []
    for repeat in range(repeats):
        NN_lengths.append(nearestNeighbour())
    average_length = sum(NN_lengths) / repeats
    if average_length > 0:
        # init_phero_level = num_ants / average_length
        init_phero_level = (0.5 * w * (w - 1)) / (phero_decay * average_length)
    else:
        init_phero_level = 0.5 # if the city set has all edges of distance 0
        global zero_distance
        zero_distance = True # used later to avoid division by 0
    phero_matrix = []
    phero_matrix_column = []
    for i in range(num_cities):
        phero_matrix_column.append(init_phero_level)
    for j in range(num_cities):
        phero_matrix.append(phero_matrix_column.copy())
    # return a matrix that corresponds to the edges represented in dist_matrix, but holds (initially equal) pheromone levels instead of distances
    return phero_matrix



# MAIN SCRIPT

phero_matrix = initPheroMatrix()
best_tour = []
best_tour_length = 0
first_iteration = True

for iteration in range(num_iterations):
    print(time.time() - start_time)
    new_tours = []
    new_tours_lengths = []
    for ant in range(num_ants):
        #print(time.time() - start_time)
        if time.time() > start_time + time_limit:
            break
        # pick starting location randomly
        unvisited_cities = list(range(num_cities))
        first_city = random.randrange(0, num_cities)
        current_city = first_city
        partial_tour = [first_city]
        partial_tour_length = 0
        unvisited_cities.pop(current_city)
        # build the tour up, one city at a time
        while len(unvisited_cities) > 0:
            # calculate heuristic desirability of moving to each unvisited city
            city_indices = []
            city_scores = []
            for city in unvisited_cities:
                city_indices.append(city)
                if dist_matrix[current_city][city] < min_dist_for_heuristic:
                    city_dist = min_dist_for_heuristic # make this number non-zero
                else:
                    city_dist = dist_matrix[current_city][city]
                city_score = (phero_matrix[current_city][city]**phero_weight) * ((1 / city_dist)**heuristic_weight)
                city_scores.append(city_score)
            # randomly choose the next city to visit, based on the weighted probabilities (scores) of each
            next_city = random.choices(city_indices, weights=city_scores)[0] # random.choices returns a list 
            # after finding the nearest next city, add it to the path
            partial_tour.append(next_city)
            partial_tour_length += dist_matrix[current_city][next_city] # not city_dist, as this may have been modified
            unvisited_cities.remove(next_city)
            current_city = next_city

        # once we have visited all cities (unvisited_cities is empty), add the path back to the start
        partial_tour_length += dist_matrix[current_city][first_city]
        # don't add the first city to the tour again
        # save this ant's tour for later
        new_tours.append(partial_tour)
        new_tours_lengths.append(partial_tour_length)
    # this time limit is almost only ever triggered when the one in the loop above has been
    if time.time() > start_time + time_limit:
        break # totally discard the last iteration, as there may be no new_tours yet, which would cause errors

        # decay pheromone levels
    for i in range(num_cities):
        for j in range(num_cities):
            phero_matrix[i][j] = phero_matrix[i][j] - phero_decay * phero_matrix[i][j]

    ''' # the best tour doesn't need to be extracted this way anymore
    best_new_tour_index = new_tours_lengths.index(min(new_tours_lengths)) # if there is a tie, it doesn't matter which is chosen as the best
    # compare the best tour of the last iteration to the best from all previous iterations
    if first_iteration == True or new_tours_lengths[best_new_tour_index] < best_tour_length: # for the first iteration, we will always want to replace the empty 'best_tour'
        first_iteration = False
        best_tour = new_tours[best_new_tour_index]
        best_tour_length = new_tours_lengths[best_new_tour_index]
    '''

    # find the best w tours between this iteration and also the best-so-far tour from any previous iteration
    if first_iteration == False: # on the first iteration, there is no best_tour
        new_tours.append(best_tour)
        new_tours_lengths.append(best_tour_length)
    else:
        first_iteration = False
    best_tours = []
    best_tours_lengths = []
    for i in range(w):
        index = new_tours_lengths.index(min(new_tours_lengths))
        best_tours.append(new_tours[index])
        best_tours_lengths.append(new_tours_lengths[index])
        new_tours.pop(index)
        new_tours_lengths.pop(index)
    # the best w tours are now stored in best_tours in worsening quality order

    # apply 3-opt local search on just only the best tour
    if num_cities < 60: # 3-opt local search takes too long for large city sets. It is more beneficial to have more iterations without the local search.
        alternative_tour, alternative_cost = localSearch(best_tours[0],best_tours_lengths[0])
        if alternative_cost < best_tours_lengths[0]:
            best_tours[0] = alternative_tour
            best_tours_lengths[0] = alternative_cost

    best_tour = best_tours[0]
    best_tour_length = best_tours_lengths[0]

    # for each of the best w ants, deposit some pheromone on the edges of its tour
    if zero_distance == False: # if all the distances between cities are 0, avoid dividing by the tour length (0) here
        for ant in range(w):
            phero_deposit = 1 / best_tours_lengths[ant]
            for step in range(num_cities - 1):
                phero_matrix[best_tours[ant][step]][best_tours[ant][step+1]] += (w - ant) * phero_deposit
            phero_matrix[best_tours[ant][step+1]][best_tours[ant][0]] += (w - ant) * phero_deposit # manually update the edge from the last city back to the first
        
    

tour = best_tour
tour_length = best_tour_length








############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour', 
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1}, AND YOU SHOULD ALSO
############ HOLD THE LENGTH OF THIS TOUR IN THE RESERVED INTEGER VARIABLE 'tour_length'.
############

############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE,
############ WHOSE NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATA AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name,'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1,num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")

    











    


