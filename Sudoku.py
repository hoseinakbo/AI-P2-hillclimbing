import random
import PSA, PSA_2

dont_touches = [1, 2, 7, 8, 13, 14]


class SudokuState(PSA.State):
    def __init__(self, board_array):
        self.board_array = list(board_array)

    def __eq__(self, other):
        if len(self.board_array) != len(other.board_array):
            return False
        for i in range(0, len(self.board_array)):
            if self.board_array[i] != other.board_array[i]:
                return False
        return True


class SudokuAction(PSA.Action):
    def __init__(self, first_num, second_num):
        self.first_num = first_num
        self.second_num = second_num


class SudokuProblem(PSA.Problem):
    def get_initial_state(self):
        return SudokuState([2, 4, 1, 3, 2, 3, 1, 4, 1, 4, 2, 3, 3, 2, 1, 4])

    def get_random_initial_state(self):
        array = [0, 4, 2, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 3, 1, 0]
        for i in range(0, 4):
            temp_array = [0, 0, 0, 0]
            for j in range(0, 4):
                if array[(i * 4) + j] != 0:
                    temp_array[array[(i * 4) + j] - 1] = 1
            for j in range(0, 4):
                if array[(i * 4) + j] != 0:
                    continue
                rand = 0
                while True:
                    rand = random.randint(0, 3)
                    if temp_array[rand] != 1:
                        temp_array[rand] = 1
                        break
                array[(i * 4) + j] = rand + 1
        return SudokuState(array)

    def get_actions(self, state):
        actions = []
        for k in range(0, 4):
            for i in range(0, 4 - 1):
                for j in range(i + 1, 4):
                    if (k * 4) + i not in dont_touches and (k * 4) + j not in dont_touches:
                        actions.append(SudokuAction((k * 4) + i, (k * 4) + j))
        return actions

    def get_result_of_action(self, action, state):
        new_state = SudokuState(state.board_array)
        temp = new_state.board_array[action.first_num]
        new_state.board_array[action.first_num] = new_state.board_array[action.second_num]
        new_state.board_array[action.second_num] = temp
        return new_state

    def is_goal(self, state):
        counter = 0
        for i in range(0, 4):
            counter += count_conflicts(get_row(i), state)
            counter += count_conflicts(get_col(i), state)
        if counter == 0:
            return True
        return False

    def get_cost(self, state1, state2, action):
        return 1

    def get_state_fitness(self, state):
        counter = 0
        for i in range(0, 4):
            counter += count_conflicts(get_row(i), state)
            counter += count_conflicts(get_col(i), state)
        return counter*-1

        # def get_random_action(self, state):
        #     random_i = random.randint(0, len(state.board_array)-1)
        #     random_j = random.randint(0, len(state.board_array)-1)
        #     return SudokuAction(random_i, random_j)


def count_conflicts(array, state):
    result_array = []
    for i in range(0, 4):
        result_array.append(state.board_array[array[i]])
    counter = 0
    for i in range(0, len(result_array)-1):
        for j in range(i+1, len(result_array)):
            if result_array[i] == result_array[j]:
                counter += 1
    return counter

def get_row(i):
    if i == 0:
        return [0, 1, 4, 5]
    if i == 1:
        return [2, 3, 6, 7]
    if i == 2:
        return [8, 9, 12, 13]
    if i == 3:
        return [10, 11, 14, 15]

def get_col(i):
    if i == 0:
        return [0, 2, 8, 10]
    if i == 1:
        return [1, 3, 9, 11]
    if i == 2:
        return [4, 6, 12, 14]
    if i == 3:
        return [5, 7, 13, 15]
