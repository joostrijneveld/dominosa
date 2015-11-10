#!/usr/bin/env python3

from itertools import combinations_with_replacement as cwr
from collections import Counter

board = [[2, 3, 2, 2, 1],
         [1, 1, 0, 2, 3],
         [0, 3, 3, 1, 0],
         [0, 3, 1, 0, 2]]

board = [[5, 5, 0, 4, 5, 5, 1],
         [5, 0, 3, 4, 1, 1, 4],
         [1, 0, 3, 1, 2, 5, 1],
         [2, 4, 4, 3, 2, 2, 1],
         [0, 2, 4, 2, 4, 0, 0],
         [3, 2, 3, 5, 0, 3, 3]]

# board = [[2, 1, 5, 0, 5, 2, 1, 5, 6],
#          [5, 1, 7, 2, 0, 0, 5, 3, 6],
#          [1, 5, 6, 0, 4, 3, 1, 4, 7],
#          [1, 5, 4, 2, 2, 3, 0, 0, 6],
#          [2, 4, 3, 7, 3, 2, 4, 5, 2],
#          [1, 7, 1, 4, 4, 7, 3, 7, 7],
#          [1, 6, 3, 5, 0, 7, 6, 0, 0],
#          [4, 6, 2, 4, 6, 3, 5, 3, 7]]

board = list(zip(*board))  # makes coordinates more intuitive
N = max([x for row in board for x in row]) + 1


class Pair(object):

    def __init__(self, v, x, y, horizontal=False):
        self.v = v
        self.x = x
        self.y = y
        self.horizontal = horizontal

    def __eq__(self, other):
        if isinstance(other, type(self.v)):
            return self.v == other
        else:
            return self.v == other.v

    def __hash__(self):
        return self.v.__hash__()

    def __repr__(self):
        return "({},{})-{}-{}".format(self.x, self.y, self.horizontal, self.v)


def possible_pairs(board):
    for x in range(N+1):
        for y in range(N):
            if x > 0:
                yield Pair(frozenset([board[x][y], board[x-1][y]]), x, y, True)
            if y > 0:
                yield Pair(frozenset([board[x][y], board[x][y-1]]), x, y)


def find_all_xy(pairs, x, y):
    for p in list(pairs):  # copy the list to prevent modification errors
        if p.x == x and p.y == y:
            yield p
        elif p.horizontal and p.x-1 == x and p.y == y:
            yield p
        elif not p.horizontal and p.x == x and p.y-1 == y:
            yield p


def remove_all_overlapping(pairs, pair):
    def remove_all_xy(pairs, x, y):
        for p in find_all_xy(pairs, x, y):
            # because of __eq__ trickery, we cannot use the regular list.remove
            for i, el in enumerate(pairs):
                if el is p:
                    del pairs[i]

    remove_all_xy(pairs, pair.x, pair.y)
    if pair.horizontal:
        remove_all_xy(pairs, pair.x-1, pair.y)
    else:
        remove_all_xy(pairs, pair.x, pair.y-1)


def remove_eq_except(all_pairs, pair, except_pairs):
    for i, p in enumerate(all_pairs):
        if not any(p is x for x in except_pairs) and p == pair:
            del all_pairs[i]


def solve(board):
    boardpairs = list(possible_pairs(board))
    found_pairs = set([])
    while boardpairs:
        # check for unique pairs
        for p, c in Counter(boardpairs).items():
            if c == 1:
                found_pairs.add(p)
                remove_all_overlapping(boardpairs, p)
        boardpairs = [x for x in boardpairs if x not in found_pairs]
        for x in range(N+1):
            for y in range(N):
                # for all unused fields
                if len(list(find_all_xy(found_pairs, x, y))) == 0:
                    # test if there is only one alternative
                    pairs = list(find_all_xy(boardpairs, x, y))
                    if len(pairs) == 1:
                        found_pairs.add(pairs[0])
                        remove_all_overlapping(boardpairs, pairs[0])
                    # or if all of these alternatives are identical
                    elif len(set(pairs)) == 1:
                        # remove other occurrences of this pair
                        remove_eq_except(boardpairs, pairs[0], pairs)
        boardpairs = [x for x in boardpairs if x not in found_pairs]

    return found_pairs

print(solve(board))
