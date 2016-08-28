from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return True iff GridPegSolitairePuzzle equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool
        
        >>> grid1 =  [["*", "*", "*", "*", "*"]]
        >>> grid1 += [["*", "*", "*", "*", "*"]]
        >>> grid1 += [["*", "*", "*", "*", "*"]]
        >>> grid1 += [["*", "*", ".", "*", "*"]]
        >>> grid1 += [["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 =  [["*", "*", "*", "*", "*"]]
        >>> grid2 += [["*", "*", "*", "*", "*"]]
        >>> grid2 += [["*", "*", "*", "*", "*"]]
        >>> grid2 += [["*", "*", ".", "*", "*"]]
        >>> grid2 += [["*", "*", "*", "*", "*"]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp1 == gpsp2
        True
        >>> gpsp1 == 1234
        False
        """
        return (type(other) == type(self) and self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitairePuzzle
        self.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid =  [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", ".", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(gpsp1.__str__())
        *****
        *****
        *****
        **.**
        *****
        """
        puzzle_str = ""
        for row in self._marker:
            for column in row:
                puzzle_str += column
            puzzle_str += "\n"
        return puzzle_str.rstrip("\n")

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]
        >>> g =  [["*", "*", "*", "*", "*"]]
        >>> g += [["*", "*", "*", "*", "*"]]
        >>> g += [["*", "*", "*", "*", "*"]]
        >>> g += [["*", "*", ".", "*", "*"]]
        >>> g += [["*", "*", "*", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(g, {"*", ".", "#"})
        >>> for i in gpsp.extensions(): print(str(i)+"\\n")
        *****
        **.**
        **.**
        *****
        *****
        <BLANKLINE>
        *****
        *****
        *****
        ..***
        *****
        <BLANKLINE>
        *****
        *****
        *****
        ***..
        *****
        <BLANKLINE>
        >>> g =  [["*", "*", "*", "*", "*"]]
        >>> g += [["*", "*", "*", ".", "*"]]
        >>> g += [["*", "*", "*", "*", "*"]]
        >>> g += [["*", "*", ".", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(g, {"*", ".", "#"})
        >>> for i in gpsp.extensions(): print(str(i)+"\\n")
        *****
        *..**
        *****
        **.**
        <BLANKLINE>
        *****
        **..*
        **.**
        *****
        <BLANKLINE>
        *****
        ***.*
        *****
        ..***
        <BLANKLINE>
        *****
        *****
        ***.*
        **..*
        <BLANKLINE>
        *****
        ***.*
        *****
        ***..
        <BLANKLINE>
        """
        # helper
        def create_grid(grid_, x_, y_, new_value):
            """
            Return a new grid with a new_value in position x, y without
            modifying grid

            @type grid_: list[list[str]]
            @type x_: int
            @type y_: int
            @type new_value: str
            @rtype: list[list[str]]
            """
            new_grid = grid_[:y_] + [grid_[y_][:x_]]
            new_grid[y_].extend([new_value])
            new_grid[y_].extend(grid_[y_][x_ + 1:])
            new_grid += grid_[y_ + 1:]
            return new_grid

        ext = []
        for y in range(len(self._marker)):
            if "*" in self._marker[y]:
                for x in range(len(self._marker[y])):
                    if self._marker[y][x] == "*":
                        # Check if a jump from the left is possible
                        # If it is add it to <list> ext
                        if x >= 2 and self._marker[y][x - 1] == "*" and \
                                self._marker[y][x - 2] == ".":
                            new_grid = create_grid(self._marker, x, y, ".")
                            new_grid = create_grid(new_grid, x - 1, y, ".")
                            new_grid = create_grid(new_grid, x - 2, y, "*")
                            ext.append(GridPegSolitairePuzzle(new_grid,
                                                              self._marker_set))
                        # Check if a jump from the right is possible
                        # If it is add it to <list> ext
                        if x <= len(self._marker[y]) - 3 and \
                            self._marker[y][x + 1]\
                                == "*" and self._marker[y][x + 2] == ".":
                            new_grid = create_grid(self._marker, x, y, ".")
                            new_grid = create_grid(new_grid, x + 1, y, ".")
                            new_grid = create_grid(new_grid, x + 2, y, "*")
                            ext.append(GridPegSolitairePuzzle(new_grid,
                                                              self._marker_set))
                        # Check if a jump from the top is possible
                        # If it is add it to <list> ext
                        if y >= 2 and self._marker[y - 1][x] == "*" and \
                                self._marker[y - 2][x] == ".":
                            new_grid = create_grid(self._marker, x, y, ".")
                            new_grid = create_grid(new_grid, x, y - 1, ".")
                            new_grid = create_grid(new_grid, x, y - 2, "*")
                            ext.append(GridPegSolitairePuzzle(new_grid,
                                                              self._marker_set))
                        # Check if a jump from the bottom is possible
                        # If it is add it to <list> ext
                        if y <= len(self._marker) - 3 and \
                            self._marker[y + 1][x] ==\
                                "*" and self._marker[y + 2][x] == ".":
                            new_grid = create_grid(self._marker, x, y, ".")
                            new_grid = create_grid(new_grid, x, y + 1, ".")
                            new_grid = create_grid(new_grid, x, y + 2, "*")
                            ext.append(GridPegSolitairePuzzle(new_grid,
                                                              self._marker_set))
        return ext

    def is_solved(self):
        """
        Return  GridPegSolitairePuzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool
        >>> grid =  [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", ".", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        False
        >>> grid =  [[".", ".", ".", ".", "."]]
        >>> grid += [[".", ".", ".", ".", "."]]
        >>> grid += [[".", ".", ".", ".", "."]]
        >>> grid += [[".", ".", ".", ".", "."]]
        >>> grid += [["*", ".", ".", ".", "."]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        True

        """
        counter = 0
        for y in range(len(self._marker)):
            for x in range(len(self._marker[y])):
                if self._marker[y][x] == "*":
                    counter += 1
        return counter == 1

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    from puzzle_tools import depth_first_solve
    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time
    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
