import math
import random
from algGenTesting import drawing_boards

boardWidth,boardHeight=15,15
def calculate_position(pos: int):
    x = pos % boardWidth
    y = pos // boardWidth
    return (x, y)
def generateBoard():
    board_string=""
    for i in range(0,boardHeight):
        for j in range(0, boardWidth):
            #board_string=board_string+random.choices(characters,weights=[5,2,2,2,2,2,2,2,1,1,1,1])[0]
            board_string = board_string + random.choices(characters)[0]
    return board_string
def decorateBoard(board_string):
    board_string = board_string[:boardWidth] + "\n" + board_string[boardWidth:]
    bias=1
    for i in range(1,boardHeight):
        board_string = board_string[:((i+1)*(boardWidth))+bias] + "\n" + board_string[((i+1)*boardWidth)+bias:]
        bias+=1
    return board_string
def letterOn(direction: str,boardstring,position):
    letter =""
    match direction:
        case "left":
            if(position%(boardWidth)==0):
                letter="W"
            else:
                letter=boardstring[position-1]

        case "right":
            if (position % boardWidth  == boardWidth-1):
                    letter = "W"
            else:
                letter = boardstring[position+1]
        case "up":
            if (position // boardWidth == 0):
                letter = "W"

            else:
                letter = boardstring[position - (boardWidth)]
        case "down":
            if (position// boardHeight == boardWidth-1):
                letter = "W"
            else:
                letter = boardstring[position + boardWidth]
        case _:
            return SyntaxError
    return letter
def countObjects(board_string,letters=["G","R","C","B"]):

    answer=[]
    for letter in letters:
        answer.append(board_string.count(letter))
    return answer
def decoratePositionAnalysis(board_string,position):
    center=board_string[position]
    print("",letterOn("up",board_string,position))
    print(letterOn("left", board_string, position),end="")
    print(center,end="")
    print(letterOn("right", board_string, position))
    print("",letterOn("down", board_string, position),end="")

def mutate(board_string):
    positions_to_mutate=random.sample(range(len(board_string)),math.floor((boardWidth*boardHeight)*MUTATION_PERCENTAGE))
    for letter_position in positions_to_mutate:
        mutation=random.choices(characters,weights=[20,2,2,2,2,2,2,2,1,1,1,1])[0]
        #mutation = random.choices(characters)[0]
        board_string = board_string[:letter_position] + mutation + board_string[letter_position + 1:]

    return board_string

#TODO: CHANGE NEGATIVE FINTESS VALUES
def evaluate(board_string):
    # TODO: CHANGE NEGATIVE FINTESS VALUES
    def check_shelves_count(importance):
        sum=0
        list=[0,0,0,0,0,0,0]
        for i, letter in enumerate(board_string):
            if letter in SHELVES:
                list[int(letter)-1]+=1
        for i in list:
            sum+=i
            if i==0:
                #return -20*importance
                return 0
        if sum/(boardWidth*boardHeight)<=SHELVES_PERCENTAGE_MAX:
            return 300
        else :
            return 100




    def check_shelve_clusters(importance):
        sum=0
        for i,letter in enumerate(board_string):
            for direction in DIRECTIONS:
                if letterOn(direction,board_string,i) ==letter:
                    sum+=1
        return sum * importance
    def check_spacing(importance):
        sum=0
        for i,letter in enumerate(board_string):
            if letter in SHELVES:
                count=0
                for direction in DIRECTIONS:
                    if letterOn(direction,board_string,i) in CHARACTERS:
                        count+=1
                if count<=2:
                    sum=1
        return sum*importance

    # TODO: CHANGE NEGATIVE FINTESS VALUES
    def check_count(importance):
        start = [1, 1, 1, 1]
        counters = countObjects(board_string)
        tolerance= 50
        sum = 0
        for i in range(0, len(start)):
            counters[i] = counters[i] - start[i]
            sum += abs(counters[i])
        if sum>tolerance:
            return 0
        else:
            return (tolerance-sum) * importance
    def check_charger_middle(importance):
        charger_index = 0
        previous_index = 0
        sum = 0
        while (charger_index >= 0):
            charger_index = board_string[previous_index:].find("B")
            if charger_index == -1:
                break
            position=charger_index+previous_index
            #print(f"check:{board_string[position]}")

            x=position
            y=x
            x_relative_position=((x % boardWidth) + 1) / boardWidth
            y_relative_position=((y//boardHeight)+1)/boardHeight
            if(0.3<x_relative_position and x_relative_position <0.6 and 0.4<y_relative_position and y_relative_position<0.6):
                sum+=1
            previous_index = position
            previous_index += 1

        return sum * importance
    def check_client_wall(importance):
        client_index=0
        previous_index=0
        sum=0
        while(client_index>=0):
            client_index=board_string[previous_index:].find("C")
            if client_index==-1:
                break
            for direction in DIRECTIONS:
                if (letterOn(direction, board_string, client_index+previous_index) == "W"):
                    sum += 1
                    break
            previous_index+=client_index
            previous_index+=1


        return sum*importance

    return check_count(400)+check_client_wall(400) + check_charger_middle(400) + check_shelve_clusters(40) + check_shelves_count(100) +check_spacing(50)# check_shelve_clusters(10) +check_spacing(40)+#+check_charger_middle(20)


def breed(parents_list):
    # def make_pairs(parents_list):
    #     pairs=[]
    #     for i in range(0, int(((NUMBER_OF_SPECIMEN-(NUMBER_OF_SPECIMEN * PERCENT_OF_TOP_PARENTS * PERCENT_OF_BEST_PARENTS)) // 2) + 1)):
    #         pair=random.sample(parents_list,2)
    #         pairs.append(pair)
    #     return pairs
    def make_pairs(parents_list):
        weights=[]
        pairs=[]
        for i in parents_list:
            weights.append(i[0])
        for i in range(0, int(((NUMBER_OF_SPECIMEN-(NUMBER_OF_SPECIMEN * PERCENT_OF_TOP_PARENTS * PERCENT_OF_BEST_PARENTS)) // 2) + 1)):
            parent1=0
            parent2=0
            while(parent1==parent2):
                parent1,parent2=random.choices(parents_list,weights=weights,k=2)
            pairs.append((parent1,parent2))
        return pairs
    def make_babies(pairs_list):
        babies=[]
        for pair in pairs_list:
            p1,p2=pair
            p1=p1[2]
            p2=p2[2] #extracting genome
            splitpoint=random.randint(0,len(p1)-1)
            baby=p1[:splitpoint]+p2[splitpoint:]
            babies.append(baby)
            baby = p2[:splitpoint] + p1[splitpoint:]
            babies.append(baby)
        return babies

    top_parents= parents_list[:math.floor(NUMBER_OF_SPECIMEN * PERCENT_OF_TOP_PARENTS)]
    best_parents= parents_list[:math.floor(NUMBER_OF_SPECIMEN * PERCENT_OF_TOP_PARENTS * PERCENT_OF_BEST_PARENTS)]
    pairs=make_pairs(parents_list)
    specimen_list=make_babies(pairs)[:NUMBER_OF_SPECIMEN-len(best_parents)]
    for i in range(0,len(best_parents)):
        specimen_list.append(best_parents[i][2])
    return specimen_list
def new_generation(specimen_list:list):
    fitness=[]
    for i,specimen in enumerate(specimen_list):
        fitness.append((evaluate(specimen),i,specimen))
    fitness.sort(reverse=True)
    specimen_list=breed(fitness)
    for i in range(0,len(specimen_list)):
        if(random.random()<=MUTATION_PROBABILITY):
            specimen_list[i]=mutate(specimen_list[i])
    return specimen_list

NUMBER_OF_GENERATIONS=2000
NUMBER_OF_SPECIMEN=200

PERCENT_OF_TOP_PARENTS=0.5
PERCENT_OF_BEST_PARENTS=0.15
MUTATION_PROBABILITY=0.8
MUTATION_PERCENTAGE=0.06
SHELVES_PERCENTAGE_MAX=0.1
SHELVES = ["1", "2", "3", "4", "5", "6", "7"]
DIRECTIONS = ["up", "down", "left", "right"]
CHARACTERS=['0','1','2','3','4','5','6','7','R','C','G','B']

characters=['0','1','2','3','4','5','6','7','R','C','G','B']
if __name__ == "__main__":
    bw=10
    bh=10

    # gen=int(input("how many generations?"))
    # spc=int(input("how many specimen?"))
    specimen_list=[]
    results=[]
    for m in range(0,NUMBER_OF_SPECIMEN):
        board = generateBoard()
        #print(decorateBoard(board))
        specimen_list.append(board)
    for g in range(0,NUMBER_OF_GENERATIONS):
        specimen_list=new_generation(specimen_list)
        if g%100==0:
            print(f"GENERATION COMPLETE: {g}")
    for i, specimen in enumerate(specimen_list):
        results.append((evaluate(specimen), i, specimen))


    results.sort(reverse=True)
    for i, m in enumerate(results):
        print(f"#{i}#\n points:{m[0]}\n", decorateBoard(m[2]),sep="")
        f=open(f"algGenTesting/boards/"+ f"{(i)}.txt".rjust(10, '0') ,'w')
        f.write(decorateBoard(m[2]))
        f.close()