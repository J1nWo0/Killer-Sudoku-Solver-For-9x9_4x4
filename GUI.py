import pygame
import sys
from LinearProgramming import KillerSudokuSolver

# Initialize pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Killer Sudoku Solver')

# Define colors
BLACK = pygame.Color("#222222")
WHITE_ROCK = pygame.Color("#EFE7D6")
GREEN = pygame.Color("#A7FF04")
BUTTON_COLOR = pygame.Color("#FF4D00")
HOVER_COLOR = pygame.Color("#FF7133")
BUTTON_COLOR_WHITE = pygame.Color("#EFE7D6")
HOVER_COLOR_WHITE = pygame.Color("#F5F8FB")
LIGHT_YELLOW = pygame.Color("#FBD502")

# Define fonts
FONT = "assets\\Press-Start-2P\\PressStart2P-Regular.ttf"

font = pygame.font.Font(None, 36)


# Initialize a set to keep track of selected cells
selected_cells_set = set()

# Position of the killer sudoku solver
grid_origin_4x4 = (350, 190)
grid_origin_9x9 = (320, 145)

# Define button class
class Button:
    def __init__(self, text, x, y, font, font_size, color, hover_color, action=None):
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(font, font_size)
        self.text_surface = self.font.render(self.text, True, color)
        self.text_rect = self.text_surface.get_rect(topleft=(x, y))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(mouse_pos):
            self.text_surface = self.font.render(self.text, True, self.hover_color)
        else:
            self.text_surface = self.font.render(self.text, True, self.color)
        
        screen.blit(self.text_surface, self.text_rect)
    
    def is_clicked(self, mouse_pos):
        return self.text_rect.collidepoint(mouse_pos)

# Function to display the main menu
def main_menu():
    buttons = [
        Button("9X9 KILLER SUDOKU", 830, 360, FONT, 17, BUTTON_COLOR, HOVER_COLOR, action="9x9"),
        Button("4X4 KILLER SUDOKU", 830, 442, FONT, 17, BUTTON_COLOR, HOVER_COLOR, action="4x4"),
        Button("CONTROLS", 830, 520, FONT, 20, BUTTON_COLOR, HOVER_COLOR, action="controls"),
        Button("QUIT", 830, 600, FONT, 20, BUTTON_COLOR, HOVER_COLOR, action="quit"),
    ]

    background_image = pygame.image.load("assets\\MENU.jpg")

    while True:
        screen.blit(background_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        if button.action == "quit":
                            pygame.quit()
                            sys.exit()
                        elif button.action == "9x9":
                            killer_sudoku_9x9()
                        elif button.action == "4x4":
                            killer_sudoku_4x4()
                        elif button.action == "controls":
                            controls_screen()

        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()

# Function to display the 9x9 Killer Sudoku screen
def killer_sudoku_9x9():
    solve_button = Button("SOLVE", 930, 300, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="solve")
    reset_button = Button("RESET", 930, 390, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="reset")
    back_button = Button("BACK", 930, 482, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="back")
    cage_constraints = []
    selected_cells = []
    temp_cells = []
    solution = []
    str = ""

    background_image = pygame.image.load("assets/9X9.jpg")

    while True:
        screen.blit(background_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button.is_clicked(mouse_pos):
                    main_menu()
                elif reset_button.is_clicked(mouse_pos):
                    cage_constraints.clear()
                    selected_cells.clear()
                    temp_cells.clear()
                    solution.clear()
                    str = ""
                    print("Cages reset")
                elif solve_button.is_clicked(mouse_pos):
                    missing_coordinates_exist = check_missing_coordinates(9, temp_cells)

                    if missing_coordinates_exist[0]:
                        str = missing_coordinates_exist[1]
                        cage_constraints.clear()
                        selected_cells.clear()
                        temp_cells.clear()
                    else:
                        try:
                            killer_sudoku = KillerSudokuSolver(9, temp_cells)
                            solution = killer_sudoku.solve()
                            if solution:
                                print(solution)
                                print("9x9 Killer Sudoku Solution:")
                                for row in solution:
                                    print(row)
                        except:
                            str = "No Solution Exists!!"
                else:
                    cell = get_grid_cell_9x9(mouse_pos)
                    if cell:
                        if cell in selected_cells:
                            selected_cells.remove(cell)
                        else:
                            selected_cells.append(cell)
                        print(f"Selected cells: {selected_cells}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_cells:
                    cage_sum = get_cage_sum(9, cage_constraints)
                    if cage_sum is not None:
                        cage_constraints.append((cage_sum, selected_cells.copy()))
                        temp_cells.append({"sum": cage_sum, "cells": selected_cells.copy()})
                        print(f"Added cage: Sum={cage_sum}, Cells={selected_cells}")
                        selected_cells = []

        # Draw grid and other components here
        draw_9x9_grid()
        highlight_cages_9x9(cage_constraints)
        highlight_cells_9x9(selected_cells)
        back_button.draw(screen)
        reset_button.draw(screen)
        solve_button.draw(screen)
        if solution:
            cage_constraints.clear()
            selected_cells.clear()
            temp_cells.clear()
            text_surface = font.render("Solution Found!!", True, WHITE_ROCK)
            text_rect = text_surface.get_rect(center=(550, 620))

            # Automatically adjust the background rectangle based on the text_rect
            background_color = BLACK  # Change to your desired background color
            padding_x, padding_y = 10, 5  # Adjust padding as needed
            background_rect = pygame.Rect(
                text_rect.left - padding_x, text_rect.top - padding_y,
                text_rect.width + 2 * padding_x, text_rect.height + 2 * padding_y
            )

            # Draw the background rectangle
            pygame.draw.rect(screen, background_color, background_rect)

            # Draw the text on top of the background rectangle
            screen.blit(text_surface, text_rect)


            draw_solution_9x9(solution)
        else:
            text_surface = font.render(str, True, WHITE_ROCK)
            text_rect = text_surface.get_rect(center=(550, 620))

            # Automatically adjust the background rectangle based on the text_rect
            background_color = BLACK  # Change to your desired background color
            padding_x, padding_y = 10, 5  # Adjust padding as needed
            background_rect = pygame.Rect(
                text_rect.left - padding_x, text_rect.top - padding_y,
                text_rect.width + 2 * padding_x, text_rect.height + 2 * padding_y
            )

            # Draw the background rectangle
            pygame.draw.rect(screen, background_color, background_rect)

            # Draw the text on top of the background rectangle
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()

def killer_sudoku_4x4():
    solve_button = Button("SOLVE", 930, 300, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="solve")
    reset_button = Button("RESET", 930, 390, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="reset")
    back_button = Button("BACK", 930, 482, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="back")
    cage_constraints = []
    selected_cells = []
    temp_cells = []
    solution = []
    str = ""

    background_image = pygame.image.load("assets/4X4.jpg")

    while True:
        screen.blit(background_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button.is_clicked(mouse_pos):
                    main_menu()
                elif reset_button.is_clicked(mouse_pos):
                    cage_constraints.clear()
                    selected_cells.clear()
                    temp_cells.clear()
                    solution.clear()
                    str = ""
                    print("Cages reset")
                elif solve_button.is_clicked(mouse_pos):
                    missing_coordinates_exist = check_missing_coordinates(4, temp_cells)

                    if missing_coordinates_exist[0]:
                        str = missing_coordinates_exist[1]
                        cage_constraints.clear()
                        selected_cells.clear()
                        temp_cells.clear()
                    else:
                        killer_sudoku = KillerSudokuSolver(4, temp_cells)
                        solution = killer_sudoku.solve()
                        print(temp_cells)
                        if solution:
                            print(solution)
                            print("4x4 Killer Sudoku Solution:")
                            for row in solution:
                                print(row)
                        else:
                            str = "No Solution Exists!!"
                else:
                    cell = get_grid_cell_4x4(mouse_pos)
                    if cell:
                        if cell in selected_cells:
                            selected_cells.remove(cell)
                        else:
                            selected_cells.append(cell)
                        print(f"Selected cells: {selected_cells}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_cells:
                    cage_sum = get_cage_sum(4, cage_constraints)
                    if cage_sum is not None:
                        cage_constraints.append((cage_sum, selected_cells.copy()))
                        temp_cells.append({"sum": cage_sum, "cells": selected_cells.copy()})
                        print(f"Added cage: Sum={cage_sum}, Cells={selected_cells}")
                        selected_cells = []

        # Draw grid and other components here
        draw_4x4_grid()
        highlight_cages_4x4(cage_constraints)
        highlight_cells_4x4(selected_cells)
        back_button.draw(screen)
        reset_button.draw(screen)
        solve_button.draw(screen)
        if solution:
            cage_constraints.clear()
            selected_cells.clear()
            temp_cells.clear()
            text_surface = font.render("Solution Found!!", True, WHITE_ROCK)
            text_rect = text_surface.get_rect(center=(550, 620))

            # Automatically adjust the background rectangle based on the text_rect
            background_color = BLACK  # Change to your desired background color
            padding_x, padding_y = 10, 5  # Adjust padding as needed
            background_rect = pygame.Rect(
                text_rect.left - padding_x, text_rect.top - padding_y,
                text_rect.width + 2 * padding_x, text_rect.height + 2 * padding_y
            )

            # Draw the background rectangle
            pygame.draw.rect(screen, background_color, background_rect)

            # Draw the text on top of the background rectangle
            screen.blit(text_surface, text_rect)
            
            draw_solution_4x4(solution)
        else:
            text_surface = font.render(str, True, WHITE_ROCK)
            text_rect = text_surface.get_rect(center=(550, 620))

            # Automatically adjust the background rectangle based on the text_rect
            background_color = BLACK  # Change to your desired background color
            padding_x, padding_y = 10, 5  # Adjust padding as needed
            background_rect = pygame.Rect(
                text_rect.left - padding_x, text_rect.top - padding_y,
                text_rect.width + 2 * padding_x, text_rect.height + 2 * padding_y
            )

            # Draw the background rectangle
            pygame.draw.rect(screen, background_color, background_rect)

            # Draw the text on top of the background rectangle
            screen.blit(text_surface, text_rect)

        
        pygame.display.flip()

# Function to draw the 9x9 grid
def draw_9x9_grid():
    # grid_origin_9x9 = (100, 50)
    cell_size = 50
    grid_size = cell_size * 9

    pygame.draw.rect(screen, WHITE_ROCK, (*grid_origin_9x9, grid_size, grid_size))

    for i in range(10):
        line_thickness = 1 if i % 3 else 3
        pygame.draw.line(screen, BLACK, 
                         (grid_origin_9x9[0], grid_origin_9x9[1] + i * cell_size), 
                         (grid_origin_9x9[0] + grid_size, grid_origin_9x9[1] + i * cell_size), line_thickness)
        pygame.draw.line(screen, BLACK, 
                         (grid_origin_9x9[0] + i * cell_size, grid_origin_9x9[1]), 
                         (grid_origin_9x9[0] + i * cell_size, grid_origin_9x9[1] + grid_size), line_thickness)

# Function to draw the 4x4 grid
def draw_4x4_grid():
    # grid_origin_4x4 = (100, 50)
    cell_size = 100
    grid_size = cell_size * 4

    pygame.draw.rect(screen, WHITE_ROCK, (*grid_origin_4x4, grid_size, grid_size))

    for i in range(5):
        line_thickness = 1 if i % 2 else 3
        pygame.draw.line(screen, BLACK, 
                         (grid_origin_4x4[0], grid_origin_4x4[1] + i * cell_size), 
                         (grid_origin_4x4[0] + grid_size, grid_origin_4x4[1] + i * cell_size), line_thickness)
        pygame.draw.line(screen, BLACK, 
                         (grid_origin_4x4[0] + i * cell_size, grid_origin_4x4[1]), 
                         (grid_origin_4x4[0] + i * cell_size, grid_origin_4x4[1] + grid_size), line_thickness)

# Function to display the controls screen
def controls_screen():
    back_button = Button("Back to Menu", 90, 53, FONT, 15, BUTTON_COLOR_WHITE, HOVER_COLOR_WHITE, action="back")

    background_image = pygame.image.load("assets\\CONTROLS.jpg")

    while True:
        screen.blit(background_image, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button.is_clicked(mouse_pos):
                    main_menu()


        back_button.draw(screen)
        pygame.display.flip()


def get_grid_cell_9x9(mouse_pos):
    # grid_origin_9x9 = (100, 50)
    cell_size = 50
    grid_x, grid_y = grid_origin_9x9
    x, y = mouse_pos

    if grid_x <= x < grid_x + 9 * cell_size and grid_y <= y < grid_y + 9 * cell_size:
        col = (x - grid_x) // cell_size
        row = (y - grid_y) // cell_size
        return row, col
    return None

def highlight_cells_9x9(cells):
    # grid_origin_9x9 = (100, 50)
    grid_x, grid_y = grid_origin_9x9
    for row, col in cells:
        pygame.draw.rect(screen, GREEN, (grid_x + col * 50, grid_y + row * 50, 50, 50), 3)

def highlight_cages_9x9(cage_constraints):
    grid_x, grid_y = grid_origin_9x9
    for cage_sum, cells in cage_constraints:
        for row, col in cells:
            pygame.draw.rect(screen, LIGHT_YELLOW, (grid_x + col * 50, grid_y + row * 50, 50, 50), 3)
        
            # Render and display the cage sum text
            font = pygame.font.Font(None, 24)
            sum_text = font.render(str(cage_sum), True, BLACK)
            # text_rect = sum_text.get_rect(center=(grid_x + (cells[0][1] + cells[-1][1] + 1) * 25, grid_y + (cells[0][0] + cells[-1][0] + 1) * 25))
            text_rect = sum_text.get_rect(center=(grid_x + col * 50 + 50/2, grid_y + row * 50 + 50/2))
            pygame.draw.rect(screen, WHITE_ROCK, text_rect)  # Background rectangle for better visibility
            screen.blit(sum_text, text_rect)

def get_grid_cell_4x4(mouse_pos):
    # grid_origin_4x4 = (100, 50)
    cell_size = 100
    grid_x, grid_y = grid_origin_4x4
    x, y = mouse_pos

    if grid_x <= x < grid_x + 4 * cell_size and grid_y <= y < grid_y + 4 * cell_size:
        col = (x - grid_x) // cell_size
        row = (y - grid_y) // cell_size
        return row, col
    return None

def highlight_cells_4x4(cells):
    # grid_origin_4x4 = (100, 50)
    grid_x, grid_y = grid_origin_4x4
    for row, col in cells:
        pygame.draw.rect(screen, GREEN, (grid_x + col * 100, grid_y + row * 100, 100, 100), 3)

def highlight_cages_4x4(cage_constraints):
    # grid_origin_4x4 = (100, 50)
    grid_x, grid_y = grid_origin_4x4
    for cage_sum, cells in cage_constraints:
        for row, col in cells:
            pygame.draw.rect(screen, LIGHT_YELLOW, (grid_x + col * 100, grid_y + row * 100, 100, 100), 3)

            # Render and display the cage sum text
            font = pygame.font.Font(None, 24)
            sum_text = font.render(str(cage_sum), True, BLACK)
            # text_rect = sum_text.get_rect(center=(grid_x + (cells[0][1] + cells[-1][1] + 1) * 50, grid_y + (cells[0][0] + cells[-1][0] + 1) * 50))
            text_rect = sum_text.get_rect(center=(grid_x + col * 100 + 100/2, grid_y + row * 100 + 100/2))
            pygame.draw.rect(screen, WHITE_ROCK, text_rect)  # Background rectangle for better visibility
            screen.blit(sum_text, text_rect)

def get_cage_sum(size, cage_constraints):
    sum_str = ""
    solve_button = Button("SOLVE", 930, 300, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="solve")
    reset_button = Button("RESET", 930, 390, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="reset")
    back_button = Button("BACK", 930, 482, FONT, 30, BUTTON_COLOR, HOVER_COLOR, action="back")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return int(sum_str) if sum_str.isdigit() else None
                elif event.key == pygame.K_BACKSPACE:
                    sum_str = sum_str[:-1]
                elif event.unicode.isdigit():
                    sum_str += event.unicode

        if size == 9:
            background_image = pygame.image.load("assets/9X9.jpg")
            screen.blit(background_image, (0,0))
            draw_9x9_grid()
            highlight_cages_9x9(cage_constraints)
        else:
            background_image = pygame.image.load("assets/4X4.jpg")
            screen.blit(background_image, (0,0))
            draw_4x4_grid()
            highlight_cages_4x4(cage_constraints)

        back_button.draw(screen)
        reset_button.draw(screen)
        solve_button.draw(screen)

        # Render the text
        text_surface = font.render("Enter Cage Sum: " + sum_str, True, WHITE_ROCK)

        # Set the position for the text_rect
        text_rect = text_surface.get_rect(center=(470, 620))

        # Automatically adjust the background rectangle based on the text_rect
        background_color = BLACK  # Change to your desired background color
        padding_x, padding_y = 10, 5  # Adjust padding as needed
        background_rect = pygame.Rect(
            text_rect.left - padding_x, text_rect.top - padding_y,
            text_rect.width + 2 * padding_x, text_rect.height + 2 * padding_y
        )

        # Draw the background rectangle
        pygame.draw.rect(screen, background_color, background_rect)

        # Draw the text on top of the background rectangle
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

def draw_solution_9x9(solution):
    # grid_origin_9x9 = (100, 50)
    cell_size = 50
    for row in range(9):
        for col in range(9):
            if solution[row][col] != 0:  # Ensure you have a non-zero value to display
                value = str(solution[row][col])
                font = pygame.font.Font(None, 36)
                text = font.render(value, True, BLACK)
                text_rect = text.get_rect(center=(grid_origin_9x9[0] + col * cell_size + cell_size / 2,
                                                  grid_origin_9x9[1] + row * cell_size + cell_size / 2))
                screen.blit(text, text_rect)


def draw_solution_4x4(solution):
    # grid_origin_4x4 = (100, 50)
    cell_size = 100
    for row in range(4):
        for col in range(4):
            if solution[row][col] != 0:  # Ensure you have a non-zero value to display
                value = str(solution[row][col])
                font = pygame.font.Font(None, 36)
                text = font.render(value, True, BLACK)
                text_rect = text.get_rect(center=(grid_origin_4x4[0] + col * cell_size + cell_size / 2,
                                                  grid_origin_4x4[1] + row * cell_size + cell_size / 2))
                screen.blit(text, text_rect)


def check_missing_coordinates(size, cage_constraints):
    # Create a set of all coordinates in the grid
    all_coordinates = {(i, j) for i in range(size) for j in range(size)}
    used_coordinates = set()  # Track coordinates used in cages
    cage_coordinates = []
    warning = ""
    
    for cage in cage_constraints:
        cage_set = set()
        for cell in cage["cells"]:
            # Check for duplicate coordinates across cages
            if cell in used_coordinates:
                print(f"Warning: Coordinate {cell} is duplicated across multiple cages")
                warning = f"Warning: Coordinate {cell} is duplicated across multiple cages"
                return [True, warning]
            # Check if cell coordinates are out of bounds
            if not (0 <= cell[0] < size and 0 <= cell[1] < size):
                print(f"Warning: Coordinate {cell} is out of bounds for {size}x{size} Sudoku")
                warning = f"Warning: Coordinate {cell} is out of bounds for {size}x{size} Sudoku"
                return [True, warning]
            cage_set.add(cell)
            used_coordinates.add(cell)  # Mark the coordinate as used
        cage_coordinates.append(cage_set)
    
    # Check for any missing coordinates (not covered by cages)
    all_cage_coordinates = set().union(*cage_coordinates)
    missing_coordinates = all_coordinates - all_cage_coordinates
    if missing_coordinates:
        print(f"Warning: Missing coordinates for {size}x{size} Killer Sudoku:", missing_coordinates)
        warning = f"Warning: Missing coordinates"
    return [bool(missing_coordinates), warning]


# Start the main menu
main_menu()
