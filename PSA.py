import queue
from random import randint


class Problem:
    def get_initial_state(self):
        pass

    def get_random_initial_state(self):
        pass

    def get_actions(self, state):
        pass

    def get_result_of_action(self, action, state):
        pass

    def is_goal(self, state):
        pass

    def get_cost(self, state1, state2, action):
        pass

    def get_state_fitness(self, state):
        pass

    def get_random_action(self, state):
        pass

    def crossover(self, parent1, parent2):
        pass

    def mutate(self, child):
        pass


class State:
    pass


class Action:
    pass


class Node:
    def __init__(self, current_state, parent_node, cost=0):
        self.current_state = current_state
        self.parent_node = parent_node
        self.cost = cost

    def __eq__(self, other):
        return self.current_state == other.current_state

    def __lt__(self, other):
        return 0


class PSA:
    def __init__(self, problem):
        self.problem = problem

    # def final_result(self, node):
    #     return node.current_state.board_array

    def add_to_f_queue(self, node):
        num = 0
        for i in range(len(self.f_queue)):
            if self.f_queue[i].cost > node.cost:
                num = i
                break
        self.f_queue.insert(num, node)


    def bfs_tree_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop(0)
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node)
                print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if self.problem.is_goal(result_state):
                    return result_state.board_array
                else:
                    self.f_queue.append(result_node)

    def bfs_graph_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        self.e_queue = []
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop(0)
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node)
                print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if self.problem.is_goal(result_state):
                    return result_state.board_array
                else:
                    if result_node not in self.f_queue and result_node not in self.e_queue:
                        self.f_queue.append(result_node)
            self.e_queue.append(self.current_node)

    def dfs_tree_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop()
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node)
                print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if self.problem.is_goal(result_state):
                    # print("f_queue size: " + str(len(self.f_queue)))
                    return result_state.board_array
                else:
                    self.f_queue.append(result_node)

    def dfs_graph_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        self.e_queue = []
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop()
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node)
                print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if self.problem.is_goal(result_state):
                    return result_state.board_array
                else:
                    if result_node not in self.f_queue and result_node not in self.e_queue:
                        self.f_queue.append(result_node)
            self.e_queue.append(self.current_node)

    def uniform_cost_search(self):
        self.f_pqueue = queue.PriorityQueue()
        self.f_pqueue.put((0, Node(self.problem.get_initial_state(), None, 0)))
        self.e_queue = []

        while self.f_pqueue.qsize() != 0:
            self.current_node = self.f_pqueue.get()[1]
            if self.current_node in self.e_queue:
                continue
            if self.problem.is_goal(self.current_node.current_state):
                return self.current_node.current_state.board_array
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_cost = self.current_node.cost + \
                              self.problem.get_cost(result_state, self.current_node.current_state, actions[i])
                print("cost: " + str(result_cost))
                result_node = Node(result_state, self.current_node, result_cost)
                print(str(result_state.board_array) + "   f_queue size: " + str(self.f_pqueue.qsize()))
                if result_node not in self.e_queue:
                    self.f_pqueue.put((result_cost, result_node))
            self.e_queue.append(self.current_node)

    def uniform_cost_search_without_priority_queue(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        self.e_queue = []

        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop(0)
            if self.problem.is_goal(self.current_node.current_state):
                return self.current_node.current_state.board_array
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_cost = self.current_node.cost + \
                              self.problem.get_cost(result_state, self.current_node.current_state, actions[i])
                print("cost: " + str(result_cost))
                result_node = Node(result_state, self.current_node, result_cost)
                print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if result_node not in self.f_queue and result_node not in self.e_queue:
                    # self.f_queue.put((result_cost, result_node))
                    self.add_to_f_queue(result_node)
            self.e_queue.append(self.current_node)

    # def bidirectional_search(self):
