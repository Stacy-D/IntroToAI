# search.py
# ---------
import util


def depth_first_search(problem):
    frontier = util.Stack()
    return search_graph(problem, frontier)


def breadth_first_search(problem):
    frontier = util.PriorityQueueWithFunction(len)
    return search_graph(problem, frontier)


def uniform_cost_search(problem):
    frontier = util.PriorityQueueWithFunction(lambda aPath: problem.get_cost_of_actions([x[1] for x in aPath]))
    return search_graph(problem, frontier)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def search_graph(problem, frontier):

    print("Start:", problem.get_initial_state())
    print("Is the start a goal?", problem.is_goal_state(problem.get_initial_state()))
    print("Start's successors:", problem.get_successors(problem.get_initial_state()))
    explored_paths = []
    frontier.push([(problem.get_initial_state(), "Stop", 0)])
    while not frontier.is_empty():
        path = frontier.pop()
        state = path[len(path) - 1]
        state = state[0]
        if problem.is_goal_state(state):
            return [x[1] for x in path][1:]
        if state not in explored_paths:
            explored_paths.append(state)
            for successor in problem.get_successors(state):
                if successor[0] not in explored_paths:
                    successor_path = path[:]
                    successor_path.append(successor)
                    frontier.push(successor_path)
    return None


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
ucs = uniform_cost_search
