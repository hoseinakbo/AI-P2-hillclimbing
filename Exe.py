import PSA_2
import Sudoku

print('Random Restart Hill Climbing: ')
b = PSA_2.PSA_2(Sudoku.SudokuProblem())
a = b.random_restart_hill_climbing()
print('Final Result: ', a.board_array)