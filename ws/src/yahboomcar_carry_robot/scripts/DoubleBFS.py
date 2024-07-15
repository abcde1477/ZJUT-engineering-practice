from collections import deque

def is_valid_move(grid, visited, x, y):
    rows, cols = len(grid), len(grid[0])
    return 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0 and (x, y) not in visited

def get_neighbors(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def get_path_using_DBFS(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    if start == goal:
        return [start]

    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return None

    start_queue = deque([start])
    goal_queue = deque([goal])

    start_visited = {start: None}
    goal_visited = {goal: None}

    while start_queue and goal_queue:
        # Expand from start side
        current = start_queue.popleft()
        for neighbor in get_neighbors(*current):
            if is_valid_move(grid, start_visited, *neighbor):
                start_visited[neighbor] = current
                start_queue.append(neighbor)
                if neighbor in goal_visited:
                    return reconstruct_path(start_visited, goal_visited, neighbor)

        # Expand from goal side
        current = goal_queue.popleft()
        for neighbor in get_neighbors(*current):
            if is_valid_move(grid, goal_visited, *neighbor):
                goal_visited[neighbor] = current
                goal_queue.append(neighbor)
                if neighbor in start_visited:
                    return reconstruct_path(start_visited, goal_visited, neighbor)

    return None


def reconstruct_path(start_visited, goal_visited, meeting_point):
    path = []
    current = meeting_point

    # Path from start to meeting_point
    while current is not None:
        path.append(current)
        current = start_visited[current]
    path.reverse()

    # Path from meeting_point to goal
    current = goal_visited[meeting_point]
    while current is not None:
        path.append(current)
        current = goal_visited[current]

    return path
