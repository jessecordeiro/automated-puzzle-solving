from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Returns whether this MNPuzzle is equal to other.

        @param MNPuzzle self: this MNPuzzle
        @param MNPuzzle | Puzzle other: the Puzzle to compare
        @rtype bool
        
        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid1 = (("*", "2", "3"), ("1", "4", "5"))
        >>> a = MNPuzzle(start_grid1, target_grid1)
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid2 = (("*", "2", "3"), ("1", "4", "5"))
        >>> b = MNPuzzle(start_grid2, target_grid2)
        >>> a == b
        True
        """
        assert type(other) is MNPuzzle,\
            "You're not comparing to an MNPuzzle!"
        if self.to_grid == other.to_grid \
                and self.from_grid == other.from_grid:
            return True
        return False

    def __str__(self):
        """
        Returns a string representation of the puzzle's current
        state.

        @param MNPuzzle self: this MNPuzzle
        @rtype: str
        
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> a = MNPuzzle(start_grid, target_grid)
        >>> print(a)
        *23
        145
        """
        ret = ""
        # Return the current state of the grid
        for x in self.from_grid:
            for y in x:
                ret += y
            ret += "\n"
        return ret.rstrip()

    def __repr__(self):
        """
        Returns a detailed string representation of the puzzle's
        current state and desired solution state.

        @param MNPuzzle self: this MNPuzzle
        @rtype: str
        
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> a = MNPuzzle(start_grid, target_grid)
        >>> print(repr(a))
        Our puzzle currently looks like:
        *23
        145
        <BLANKLINE>
        The solution is:
        123
        45*
        """
        ret = ""
        # Introduce the current state
        ret += "Our puzzle currently looks like:\n"
        # Print out the current state
        ret += str(self)
        # Return twice for presentation and
        # introduce the solution state
        ret += "\n\nThe solution is:\n"
        for x in self.to_grid:
            for y in x:
                ret += y
            ret += "\n"
        return ret.rstrip()

    def extensions(self):
        """
        Return list of legal extensions of MNPuzzle self.

        Legal extensions are configurations that can be
        reached by swapping one symbol to the left, right,
        above, or below "*" with "*"

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> a = MNPuzzle(start_grid, target_grid)
        >>> for i in a.extensions(): print(str(i)+"\\n")
        123
        *45
        <BLANKLINE>
        2*3
        145
        <BLANKLINE>
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("2", "*", "3"), ("1", "4", "5"))
        >>> a = MNPuzzle(start_grid, target_grid)
        >>> for i in a.extensions(): print(str(i)+"\\n")
        *23
        145
        <BLANKLINE>
        243
        1*5
        <BLANKLINE>
        23*
        145
        <BLANKLINE>
        """
        # Initiate a storage array
        ext = []
        # Find the location of the "*" symbol
        x = -1
        y = -1
        for r in range(len(self.from_grid)):
            for c in range(len(self.from_grid[r])):
                if self.from_grid[r][c] == "*":
                    x, y = r, c
                    break
        # Add each possibility sequentially
        if x - 1 > -1:
            top_shift = [list(i) for i in self.from_grid]
            top_shift[x][y] = self.from_grid[x - 1][y]
            top_shift[x - 1][y] = "*"
            ext.append(MNPuzzle(tuple(top_shift), self.to_grid))
        if y - 1 > -1:
            left_shift = [list(i) for i in self.from_grid]
            left_shift[x][y] = self.from_grid[x][y - 1]
            left_shift[x][y - 1] = "*"
            ext.append(MNPuzzle(tuple(left_shift), self.to_grid))
        if x + 1 < len(self.from_grid):
            bottom_shift = [list(i) for i in self.from_grid]
            bottom_shift[x][y] = self.from_grid[x + 1][y]
            bottom_shift[x + 1][y] = "*"
            ext.append(MNPuzzle(tuple(bottom_shift), self.to_grid))
        if y + 1 < len(self.from_grid[0]):
            right_shift = [list(i) for i in self.from_grid]
            right_shift[x][y] = self.from_grid[x][y + 1]
            right_shift[x][y + 1] = "*"
            ext.append(MNPuzzle(tuple(right_shift), self.to_grid))
        # Return the list of possible states
        return ext

    def is_solved(self):
        """
        Return True iff MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool
        
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> a1 = MNPuzzle(start_grid, target_grid)
        >>> a1.is_solved()
        False
        >>> start_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> a2 = MNPuzzle(start_grid, target_grid)
        >>> a2.is_solved()
        True
        """
        # Return true if every part of both grids are identical
        for a in range(len(self.from_grid)):
            for b in range(len(self.from_grid[a])):
                if self.from_grid[a][b] != self.to_grid[a][b]:
                    return False
        return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
