import os
import time

# 7-segments
#   -- A --
#  |       |
#  F       B
#  |       |
#   -- G --
#  |       |
#  E       C
#  |       |
#   -- D --
#translate numbers into letters on 7-segments
number_to_segments_map = {
    0: ['A', 'B', 'C', 'D', 'E', 'F'],
    1: ['B', 'C'],
    2: ['A', 'B', 'G', 'E', 'D'],
    3: ['A', 'B', 'G', 'C', 'D'],
    4: ['F', 'G', 'B', 'C'],
    5: ['A', 'F', 'G', 'C', 'D'],
    6: ['A', 'F', 'G', 'E', 'C', 'D'],
    7: ['A', 'B', 'C'],
    8: ['A', 'B', 'C', 'D', 'E', 'F', 'G']
}

# Maps segments to positions in the 5x4 grid
# for each letter to be activated these positions should be '#'
segments_to_list_map = {
    'A': [(0, 0), (0, 1), (0, 2), (0, 3)],
    'B': [(1, 3), (2, 3)],
    'C': [(3, 3), (4, 3)],
    'D': [(4, 0), (4, 1), (4, 2), (4, 3)],
    'E': [(3, 0), (4, 0)],
    'F': [(1, 0), (2, 0)],
    'G': [(2, 0), (2, 1), (2, 2), (2, 3)]
}

def display_gear(gear_number):
    # Create 5x4 grid filled with spaces
    grid = []

    for row in range(5):
        line = [' ', ' ', ' ', ' ']
        grid.append(line)

    if gear_number not in number_to_segments_map :
        print("Error: Unsupported gear number.")
        return

    # Get segments to activate
    active_segments = number_to_segments_map[gear_number] #returning letters

    # Fill grid based on active segments
    for segment in active_segments: #for each letter
        for row, col in segments_to_list_map[segment]:
            grid[row][col] = '#'

    # Print the grid
    for row in grid:
        print(''.join(row))

def animate_shift(from_gear, to_gear):
    display_gear(from_gear)
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    display_gear(to_gear)

def get_valid_gear_input(prompt):
    while True:
        gear_input = input(prompt).strip()
        if gear_input.isdigit():
            gear_number = int(gear_input)
            if 0 <= gear_number <= 8:
                return gear_number
            else:
                print("Please enter a number between 0 and 8")
        else:
            print("Invalid input. Please enter a number between 0 and 8")

def main():
    print("Gear Display System (0 = Neutral, 1-8 = Gears)")
    
    # Get initial gear
    current_gear = get_valid_gear_input("Enter starting gear (0–8): ")
    display_gear(current_gear)

    # Ask if user wants to shift gear
    while True:
        user_input = input("Shift gear? (y/n): ").lower()
        if user_input == 'y':
            new_gear = get_valid_gear_input("Enter new gear (0–8): ")
            animate_shift(current_gear, new_gear)
            current_gear = new_gear
        elif user_input == 'n':
            print("Exiting gear display.")
            break
        else:
            print("Please type 'y' or 'n'.")

if __name__ == "__main__":
    main()
