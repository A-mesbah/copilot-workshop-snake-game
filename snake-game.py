import curses
import random

# Initialize the game screen
def init_screen():
    screen = curses.initscr()
    curses.curs_set(0)
    screen.keypad(1)
    screen.timeout(100)
    return screen

# Initialize the snake and food positions
def init_game(screen):
    sh, sw = screen.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    snake = [[sh//2, sw//4], [sh//2, sw//4 - 1], [sh//2, sw//4 - 2]]
    food = [sh//2, sw//2]
    w.addch(food[0], food[1], curses.ACS_PI)
    return w, snake, food

# Capture user input for direction changes
def get_direction(key, direction):
    if key == curses.KEY_UP and direction != curses.KEY_DOWN:
        direction = curses.KEY_UP
    elif key == curses.KEY_DOWN and direction != curses.KEY_UP:
        direction = curses.KEY_DOWN
    elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
        direction = curses.KEY_LEFT
    elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
        direction = curses.KEY_RIGHT
    return direction

# Update the snake's position
def update_snake(snake, direction):
    head = [snake[0][0], snake[0][1]]
    if direction == curses.KEY_UP:
        head[0] -= 1
    elif direction == curses.KEY_DOWN:
        head[0] += 1
    elif direction == curses.KEY_LEFT:
        head[1] -= 1
    elif direction == curses.KEY_RIGHT:
        head[1] += 1
    snake.insert(0, head)
    return snake

# Check for collisions
def check_collisions(snake, sh, sw):
    if (snake[0][0] in [0, sh] or
        snake[0][1] in [0, sw] or
        snake[0] in snake[1:]):
        return True
    return False

# Check if the snake has eaten the food
def check_food(snake, food):
    if snake[0] == food:
        return True
    return False

# Render the updated game state on the screen
def render(screen, snake, food):
    screen.clear()
    for segment in snake:
        screen.addch(segment[0], segment[1], curses.ACS_CKBOARD)
    screen.addch(food[0], food[1], curses.ACS_PI)
    screen.refresh()

# Main game loop
def main(screen):
    w, snake, food = init_game(screen)
    direction = curses.KEY_RIGHT
    score = 0

    while True:
        key = w.getch()
        if key != -1:
            direction = get_direction(key, direction)
        snake = update_snake(snake, direction)

        if check_collisions(snake, *screen.getmaxyx()):
            break

        if check_food(snake, food):
            score += 1
            food = None
            while food is None:
                nf = [random.randint(1, screen.getmaxyx()[0] - 1),
                      random.randint(1, screen.getmaxyx()[1] - 1)]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        render(w, snake, food)

    screen.addstr(0, 0, f"Game Over! Your score is {score}")
    screen.refresh()
    screen.getch()

# Run the game
curses.wrapper(main)