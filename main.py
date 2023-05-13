import copy
import time
import heapdict


# Define the Fruit class to represent each fruit
class Fruit:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return self.name


# Define the State class to represent the current state of the data
class State:
    def __init__(self, array, moves=0, parent=None):
        self.array = array
        self.moves = moves
        self.parent = parent

    # Get the neighboring states that can be reached by swapping two fruits
    def get_neighbors(self):
        neighbors = []
        # Swap any two fruits horizontally
        for i in range(3):
            for j1 in range(len(self.array[0])):
                for j2 in range(j1 + 1, len(self.array[0])):
                    new_array = copy.deepcopy(self.array)
                    new_array[i][j1], new_array[i][j2] = new_array[i][j2], new_array[i][j1]
                    neighbors.append(State(new_array, self.moves + 1, self))
        # Swap any two fruits vertically
        for i1 in range(3):
            for j1 in range(len(self.array[0])):
                for i2 in range(i1 + 1, 3):
                    new_array = copy.deepcopy(self.array)
                    new_array[i1][j1], new_array[i2][j1] = new_array[i2][j1], new_array[i1][j1]
                    neighbors.append(State(new_array, self.moves + 1, self))
        return neighbors

    # Check if the current state is the goal state
    def is_goal(self):
        for i in range(3):
            fruit_type = self.array[i][0].name.split("_")[0]
            for j in range(len(self.array[0])):
                if (j < 9 and int(self.array[i][j].size) > int(self.array[i][j + 1].size)) or \
                        self.array[i][j].name.split("_")[0] != fruit_type:
                    return False
        return True


# Define the heuristic function to estimate the remaining moves required
def heu(current_cost, neighbor, finalColumn, sizeGoal):
    score = 0
    # Calculate the score for each fruit in the board
    for i in range(3):
        for j in range(len(neighbor.array[0])):
            fruit, size = neighbor.array[i][j].name.split("_")
            if finalColumn[i] != fruit:
                score += 1
            if fruit == "apple":
                if int(size) != sizeGoal[0][j]:
                    score += 1
            elif fruit == "banana":
                if int(size) != sizeGoal[2][j]:
                    score += 1
            else:
                if int(size) != sizeGoal[1][j]:
                    score += 1
    return (score + current_cost) / 4


# get column positions according to heuristic of initial state with possible columns
def startSearch(initialState):
    finalColumnList = [["apple", "orange", "banana"], ["orange", "apple", "banana"], ["banana", "orange", "apple"],
                       ["apple", "banana", "orange"], ["orange", "banana", "apple"], ["banana", "apple", "orange"]]
    minPath, minCost = [], float('inf')
    for columns in finalColumnList:
        path, cost = astar(initialState, columns)
        if minCost > cost:
            shortestOrdering = columns
            minPath = path
            minCost = cost
    return minPath, minCost


# Define the A* algorithm to solve the problem
def astar(initial_state, columns):
    apple = []
    banana = []
    orange = []
    # Find the goal state
    for i in range(3):
        for j in range(len(initial_state.array[0])):
            fruit, size = initial_state.array[i][j].name.split("_")
            if fruit == "apple":
                apple.append(int(size))
            elif fruit == "banana":
                banana.append(int(size))
            else:
                orange.append(int(size))
    sizeGoal = [sorted(apple), sorted(orange), sorted(banana)]
    # Define the final column
    finalColumn = columns
    closed_states = []
    open_states = heapdict.heapdict()
    open_states[(0, initial_state)] = 0
    # Iterate until the open states list is empty or the goal state is found
    while open_states:
        # Pop the state with the lowest score from the open_state set
        current_cost, current_state = open_states.popitem()[0]
        # Check if the goal state has been reached
        if current_state.is_goal():
            # Reconstruct the path from the initial state to the goal state
            path = []
            while current_state:
                path.append(current_state.array)
                current_state = current_state.parent
            path.reverse()
            return path, current_cost
        # Add the current state to the closed_states set
        visitedArray = current_state.array
        closed_states.append(visitedArray)
        # Generate the neighboring states and add them to the open state set
        for neighbor in current_state.get_neighbors():
            # Check if the neighbor is already in the closed_states set
            if neighbor.array not in closed_states:
                # update its score
                heuristic = heu(current_cost, neighbor, finalColumn, sizeGoal)
                open_states[(current_cost + 1, neighbor)] = heuristic

    # Return None if the goal state is not reachable
    return None, None


def main():
    start_time = time.time()
    initial_array = [
        [Fruit("orange_1", 1), Fruit("apple_5", 5), Fruit("banana_3", 3), Fruit("orange_4", 4), Fruit("apple_1", 1),
         Fruit("banana_7", 7), Fruit("apple_6", 6), Fruit("banana_9", 9), Fruit("orange_8", 8), Fruit("banana_2", 2)],

        [Fruit("apple_2", 2), Fruit("banana_1", 1), Fruit("apple_3", 3), Fruit("orange_2", 2), Fruit("banana_4", 4),
         Fruit("apple_8", 8), Fruit("orange_7", 7), Fruit("banana_5", 5), Fruit("orange_6", 6), Fruit("apple_9", 9)],

        [Fruit("apple_10", 10), Fruit("orange_3", 3), Fruit("orange_5", 5), Fruit("banana_10", 10), Fruit("apple_4", 4),
         Fruit("orange_10", 10), Fruit("banana_6", 6), Fruit("apple_7", 7), Fruit("banana_8", 8), Fruit("orange_9", 9)]
    ]
    initial_state = State(initial_array)
    path, currentCost = startSearch(initial_state)
    if path is not None:
        print("Cost ", currentCost)
        for p in path:
            print(p)
    else:
        print(path)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
