"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# import resource
import sys
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.
    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    # # This is an iterative depth first search. It works but we decided that
    # # the recursive implementation was faster
    # def search_stack(s, seen):
    #     # Stack to search for extension that solves puzzle state
    #     while len(s) > 0:
    #         # Pop the next extension to be checked but do not keep it removed
    #         curr_ext = s.pop()
    #         s.append(curr_ext)
    #         # Check if curr_ext has already been processed
    #         if str(curr_ext.puzzle) not in seen and \
    #                 not curr_ext.puzzle.fail_fast():
    #             if curr_ext.puzzle.is_solved():
    #                 curr_ext.children = []
    #                 # If the puzzle is solved we construct a solution
    #                 # array by going up the path that we took
    #                 while curr_ext.parent is not None:
    #                     tmp = curr_ext.parent
    #                     tmp.children = [curr_ext]
    #                     curr_ext = tmp
    #                 return curr_ext
    #             else:
    #                 seen.add(str(curr_ext.puzzle))
    #                 for child in curr_ext.children:
    #                     children = [i for i in child.extensions()]
    #                     s.append(PuzzleNode(child, children, curr_ext))
    #         # If the curr_ext has already been processed, pop it from stack
    #         else:
    #             s.pop()
    #     return None
    #
    # configs_seen = set()
    # stack = deque()
    # ext = [i for i in puzzle.extensions()]
    # p_node = PuzzleNode(puzzle, ext)
    # stack.append(p_node)
    # return search_stack(stack, configs_seen)

    # Recursive depth first search. It was faster than the iterative version
    # when we tested
    def dfs(node, visited, solution=[None]):
        # Add node to the set of visited nodes
        visited.add(str(node.puzzle))
        if node.puzzle.is_solved():
            node.children = []
            # If the puzzle is solved we construct a solution
            # array by going up the path that we took
            while node.parent is not None:
                tmp = node.parent
                tmp.children = [node]
                node = tmp
            # solution is a list of 1 element because it needed to be immutable
            solution[0] = node
        # If a solution is not found, run dfs on all children that have not been
        # visited
        if solution == [None]:
            for next_ in [e for e in node.puzzle.extensions()
                          if str(e) not in visited and not e.fail_fast()]:
                dfs(PuzzleNode(next_, [i for i in next_.extensions()], node),
                    visited, solution)
        return solution

    visited_ = set()
    ext = [i for i in puzzle.extensions()]
    p_node = PuzzleNode(puzzle, ext)
    return dfs(p_node, visited_)[0]


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.
    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    def search_queue(q, seen):
        # Queue to search for extension that solves puzzle state
        while len(q) > 0:
            # Pop the next extension to be checked
            curr_ext = q.popleft()
            # Check if curr_ext has already been processed
            # If it has the next iteration of the while loop begins
            if str(curr_ext.puzzle) not in seen and \
                    not curr_ext.puzzle.fail_fast():
                # Add curr_ext to the set <seen> because it has now
                # been seen
                seen.add(str(curr_ext.puzzle))
                # Check if we have found the solution
                if curr_ext.puzzle.is_solved():
                    curr_ext.children = []
                    # If the puzzle is solved we construct a solution
                    # array by going up the path that we took
                    while curr_ext.parent is not None:
                        tmp = curr_ext.parent
                        tmp.children = [curr_ext]
                        curr_ext = tmp
                    return curr_ext
                else:
                    # Otherwise another set of steps is added to the queue
                    # to be processed
                    for child in curr_ext.children:
                        # If a possible move has already been seen it is
                        # ignored
                        if str(child) not in seen:
                            children = [i for i in child.extensions()]
                            q.append(PuzzleNode(child, children, curr_ext))
        # Return None if all steps are exhausted without finding a solution
        return None

    configs_seen = set()
    queue = deque()
    ext = [i for i in puzzle.extensions()]
    p_node = PuzzleNode(puzzle, ext)
    queue.append(p_node)
    return search_queue(queue, configs_seen)

# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
