from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return equality of <self> and <other>

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool

        >>> f = open('words.txt', 'r')
        >>> word_set = set(f.read().split())
        >>> s = WordLadderPuzzle("mule", "zoom", word_set)
        >>> t = WordLadderPuzzle("mule", "zoom", word_set)
        >>> s == t
        True
        >>> r = WordLadderPuzzle("bam", "zoom", word_set)
        >>> s == r
        False
        """
        return (type(self) == type(other) and self._from_word == 
                other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __str__(self):
        """
        Return str representation of <self>
        
        @type self: WordLadderPuzzle
        @rtype: str
        
        >>> f = open('words.txt', 'r')
        >>> word_set = set(f.read().split())
        >>> s = WordLadderPuzzle("mule", "zoom", word_set)
        >>> print(s)
        mule -> zoom
        >>> s = WordLadderPuzzle("moose", "tower", word_set)
        >>> print(s)
        moose -> tower
        """
        return "{} -> {}".format(self._from_word, self._to_word)
        
    def __repr__(self):
        """
        Return a user-friendly representation of WordLadder <self>

        @type self: WordLadderPuzzle
        @rtype: str

        >>> ws = set(['ruby', 'java'])
        >>> w = WordLadderPuzzle('turtle', 'python', ws)
        >>> w
        turtle -> python
        >>> w = WordLadderPuzzle('lambda', 'house', ws)
        >>> w
        lambda -> house
        """
        return "{} -> {}".format(self._from_word, self._to_word)

    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[Puzzle]

        >>> word_set = set(['lab', 'tab', 'cat', 'cap', 'pow'])
        >>> w = WordLadderPuzzle('cab', 'mow', word_set)
        >>> new = WordLadderPuzzle('lab', 'mow', word_set)
        >>> new in w.extensions()
        True
        >>> new = WordLadderPuzzle('mow', 'mow', word_set)
        >>> new in w.extensions()
        False
        """
        # override extensions
        # legal extensions are WordPadderPuzzles that have a from_word that can
        # be reached from this one by changing a single letter to one of those
        # in self._chars
        ext = []
        for char in self._chars:
            for index in range(len(self._from_word)):
                word = self._from_word[:index] + char + self._from_word[
                                                        index + 1:]
                # Check if generated word is in _word_set
                if word in self._word_set:
                    ext.append(WordLadderPuzzle(word, self._to_word, 
                                                self._word_set))
        return ext

    def is_solved(self):
        """
        Return whether Puzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> f = open('words.txt', 'r')
        >>> word_set = set(f.read().split())
        >>> s = WordLadderPuzzle("zoom", "zoom", word_set)
        >>> s.is_solved()
        True
        >>> s = WordLadderPuzzle("boom", "zoom", word_set)
        >>> s.is_solved()
        False
        """
        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words.txt", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
