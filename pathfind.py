import pygame
from collections import deque

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PANEL_HEIGHT = 100
CELL_SIZE = 25
GRID_HEIGHT = WINDOW_HEIGHT - PANEL_HEIGHT
GRID_WIDTH = WINDOW_WIDTH
COLUMNS = GRID_WIDTH//CELL_SIZE
ROWS = GRID_HEIGHT//CELL_SIZE
start = None
end = None
walls = set()
path = []

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinding AI Project")
clock = pygame.time.Clock()
FPS_LIMIT = 60
font = pygame.font.Font(None, 30)
BFS_BUTTON = pygame.Rect(20, GRID_HEIGHT + 25, 120, 50)

def get_grid_position(mouse_position):
    x, y = mouse_position

    if y >= GRID_HEIGHT:
        return None

    column = x // CELL_SIZE
    row = y // CELL_SIZE

    return row, column

def get_neighbours(cell):
    row, column = cell
    neighbours = []
    if row > 0 and (row - 1, column) not in walls:
        neighbours.append((row - 1, column))
    if row < (ROWS - 1) and (row + 1, column) not in walls:
        neighbours.append((row+1, column))
    if column > 0 and (row, column - 1) not in walls:
        neighbours.append((row, column - 1))
    if column < (COLUMNS - 1) and (row, column + 1) not in walls:
        neighbours.append((row, column + 1))
    return neighbours

def change_fps(current_fps):
    if current_fps == 60:
        return 120
    else:
        return 60

def bfs(start, end):
    queue = deque([start])
    visited_cells = set()
    visited_cells.add(start)
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbour in get_neighbours(current):
            if neighbour not in visited_cells:
                visited_cells.add(neighbour)
                queue.append(neighbour)
                came_from[neighbour] = current
    if end not in came_from:
        return None
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path



running = True


while running: ##Makes sure the event check in the for loop happens continuously and not once at the beginning of the program launch.
    for event in pygame.event.get(): ##This for loop collects all recent user events and checks each event individually. Pygame receives recognised user and window interactions from the operating system, converts them into event objects, and stores them in an event queue until the program checks them.
        if event.type == pygame.QUIT: ##Checks whether the user is trying to close the window, which creates a pygame.QUIT evenT. Event types are stored within events. Each event variable refers to one event object rather than a list of event types. That event object will contain info such as its event type (ie MOUSEBUTTONDOWN)
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cell = get_grid_position(event.pos)

            if cell is not None:
                keys = pygame.key.get_pressed()

                if event.button == 1:
                    if keys[pygame.K_s]:
                        if cell != end:
                            start = cell
                            walls.discard(cell)

                    elif keys[pygame.K_e]:
                        if cell != start:
                            end = cell
                            walls.discard(cell)

                    elif cell != start and cell != end:
                        walls.add(cell)

                elif event.button == 3:
                    walls.discard(cell)

                    if start == cell:
                        start = None

                    if end == cell:
                        end = None
            ##This while loop ensures that the window created does not automatically closes itself. while running is used rather than while True as the value of running can be changed to False when the user presses the red X, allowing the loop to end cleanly.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                FPS_LIMIT = change_fps(FPS_LIMIT)
                print("FPS limit:", FPS_LIMIT)
  
    screen.fill((100, 100, 100))
    pygame.draw.rect(screen, (180, 180, 180), BFS_BUTTON)
    for row, column in walls:
        wall_rectangle = pygame.Rect(
            column * CELL_SIZE,
            row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (30, 30, 30), wall_rectangle)

    for row, column in path:
        path_rectangle = pygame.Rect(
            column * CELL_SIZE,
            row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (0, 120, 255), path_rectangle)

    if start is not None:
        row, column = start
        start_rectangle = pygame.Rect(
            column * CELL_SIZE,
             row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (0, 200, 0), start_rectangle)

    if end is not None:
        row, column = end
        end_rectangle = pygame.Rect(
            column * CELL_SIZE,
            row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (220, 40, 40), end_rectangle)
    for i in range(0, GRID_WIDTH + 1, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (i, 0), (i, GRID_HEIGHT), 1)
    for i in range(0, GRID_HEIGHT + 1, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, i), (GRID_WIDTH, i), 1)
    
    pygame.display.flip()
    clock.tick(FPS_LIMIT)



pygame.quit()