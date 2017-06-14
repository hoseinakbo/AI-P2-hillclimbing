from random import randint, uniform

import math


class PSA_2:
    def __init__(self, problem):
        self.problem = problem

    def normal_hill_climbing(self):
        self.current_state = self.problem.get_initial_state()
        self.current_state_fitness = self.problem.get_state_fitness(self.current_state)
        bastCounter = 0
        ijadCounter = 0
        while True:
            bastCounter += 1
            print(str(self.current_state.board_array))
            actions = self.problem.get_actions(self.current_state)
            best_next_state = self.current_state
            best_next_state_fitness = self.problem.get_state_fitness(best_next_state)
            for i in range(0, len(actions)):
                ijadCounter += 1
                res = self.problem.get_result_of_action(actions[i], self.current_state)
                if self.problem.get_state_fitness(res) > best_next_state_fitness:
                    best_next_state = res
                    best_next_state_fitness = self.problem.get_state_fitness(best_next_state)
            if self.current_state == best_next_state:
                print("Expanded: ", bastCounter)
                print("Visited: ", ijadCounter)
                return self.current_state
            self.current_state = best_next_state
            self.current_state_fitness = best_next_state_fitness

    def stochastic_hill_climbing(self):
        self.current_state = self.problem.get_initial_state()
        self.current_state_fitness = self.problem.get_state_fitness(self.current_state)
        bastCounter = 0
        ijadCounter = 0
        while True:
            bastCounter += 1
            print(str(self.current_state.board_array))
            actions = self.problem.get_actions(self.current_state)
            best_next_state = self.current_state
            best_next_state_fitness = self.problem.get_state_fitness(best_next_state)
            self.better_next_states = []
            for i in range(0, len(actions)):
                ijadCounter += 1
                res = self.problem.get_result_of_action(actions[i], self.current_state)
                if self.problem.get_state_fitness(res) > best_next_state_fitness:
                    self.better_next_states.append(res)
            if len(self.better_next_states) == 0:
                print("Expanded: ", bastCounter)
                print("Visited: ", ijadCounter)
                return self.current_state
            self.current_state = self.better_next_states[randint(0, len(self.better_next_states)-1)]
            self.current_state_fitness = self.problem.get_state_fitness(self.current_state)

    def first_choice_hill_climbing(self):
        self.current_state = self.problem.get_initial_state()
        self.current_state_fitness = self.problem.get_state_fitness(self.current_state)
        bastCounter = 0
        ijadCounter = 0
        while True:
            bastCounter += 1
            print(str(self.current_state.board_array))
            best_next_state = self.current_state
            best_next_state_fitness = self.problem.get_state_fitness(best_next_state)
            # while True:
            for i in range(0, 100):
                ijadCounter += 1
                random_action = self.problem.get_random_action(self.current_state)
                res = self.problem.get_result_of_action(random_action, self.current_state)
                if self.problem.get_state_fitness(res) > best_next_state_fitness:
                    self.current_state = res
                    self.current_state_fitness = self.problem.get_state_fitness(self.current_state)
                    break
            if self.problem.is_goal(self.current_state):
                print("Expanded: ", bastCounter)
                print("Visited: ", ijadCounter)
                return self.current_state

    def random_restart_hill_climbing(self):
        self.current_state = self.problem.get_random_initial_state()
        self.current_state_fitness = self.problem.get_state_fitness(self.current_state)
        self.best_result = self.current_state
        bastCounter = 0
        ijadCounter = 0
        # for i in range(0, 100):
        while not self.problem.is_goal(self.best_result):
            counter = 0
            while True:
                counter += 1
                bastCounter += 1
                # print(str(self.current_state.board_array))
                actions = self.problem.get_actions(self.current_state)
                best_next_state = self.current_state
                best_next_state_fitness = self.problem.get_state_fitness(best_next_state)
                for i in range(0, len(actions)):
                    ijadCounter += 1
                    res = self.problem.get_result_of_action(actions[i], self.current_state)
                    if self.problem.get_state_fitness(res) > best_next_state_fitness:
                        best_next_state = res
                        best_next_state_fitness = self.problem.get_state_fitness(best_next_state)
                if self.current_state == best_next_state:
                    # print("Fitness: ", self.problem.get_state_fitness(self.current_state))
                    if self.problem.get_state_fitness(self.current_state) > self.problem.get_state_fitness(self.best_result):
                        self.best_result = self.current_state
                    break
                self.current_state = best_next_state
                self.current_state_fitness = best_next_state_fitness
            self.current_state = self.problem.get_random_initial_state()
            self.current_state_fitness = self.problem.get_state_fitness(self.current_state)
        print("Best Fitness Found: ", self.problem.get_state_fitness(self.best_result))
        print("Expanded: ", bastCounter)
        print("Visited: ", ijadCounter)
        return self.best_result

    def simulated_annealing(self, method):
        self.current_state = self.problem.get_initial_state()
        t = 0
        T = 1000
        bastCounter = 0
        ijadCounter = 0
        while True:
            ijadCounter += 1
            t += 1
            T = self.schedule(method, t, T)
            if T == 0:
                print("Expanded: ", bastCounter)
                print("Visited: ", ijadCounter)
                return self.current_state
            next_state = self.problem.get_result_of_action(self.problem.get_random_action(self.current_state), self.current_state)
            delta_e = self.problem.get_state_fitness(next_state) - self.problem.get_state_fitness(self.current_state)
            if delta_e > 0:
                bastCounter += 1
                self.current_state = next_state
            elif self.check_probability(delta_e, T):
                bastCounter += 1
                self.current_state = next_state

    def check_probability(self, delta_e, t):
        rand = uniform(0, 1)
        if rand < math.pow(math.e, (delta_e/t)):
            return True
        else:
            return False

    def schedule(self, method, t, T):
        if method == 1:
            if T-0.5 < 0:
                return 0
            return T - 0.5
        elif method == 2:
            if 0.95*T < 0.000000000005:
                return 0
            return 0.95*T
        elif method == 3:
            return pow(1000 - t, 1./10.)

    def genetic_algorithm(self, pop_num):
        population = []
        for i in range(0, pop_num):
            population.append(self.problem.get_random_initial_state())
        for j in range(0, 100):
            # population.sort(key=lambda x: self.problem.get_state_fitness(x))
            new_population = []
            for i in range(0, len(population)):
                parent1 = self.parent_selection(population, int(pop_num/4))
                parent2 = self.parent_selection(population, int(pop_num/4))
                child = self.problem.crossover(parent1, parent2)
                if self.get_random_probability():
                    child = self.problem.mutate(child)
                new_population.append(child)
            new_population.sort(key=lambda x: self.problem.get_state_fitness(x))
            pop_sum = 0
            for i in range(0, len(new_population)):
                pop_sum += new_population[i]
            average = pop_sum / len(new_population)
            # print(j, self.problem.get_state_fitness(new_population[0]), self.problem.get_state_fitness(new_population[len(new_population)-1]),
            #       self.problem.get_state_fitness(average))
            print("\nWorst Result: ", new_population[0], "    |    Fitness: ", self.problem.get_state_fitness(new_population[0]))
            print("Best Result: ", new_population[len(new_population)-1], "    |    Fitness: ",
                  self.problem.get_state_fitness(new_population[len(new_population)-1]))
            print("Average Result: ", average, "    |    Fitness: ", self.problem.get_state_fitness(average))
            population = new_population
        return (population[len(population)-1], self.problem.get_state_fitness(population[len(population)-1]))

    def parent_selection(self, population, k):
        best = None
        for i in range(0, k):
            ind = population[randint(1, len(population)-1)]
            if (best is None) or (self.problem.get_state_fitness(ind) > self.problem.get_state_fitness(best)):
                best = ind
        return best

    def get_random_probability(self):
        rand = uniform(0, 1)
        return rand < 0.5

