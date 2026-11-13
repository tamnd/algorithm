---
tag: EHAYPB
kind: data-structure
slug: bitboard
name: Bitboard
aliases:
- bit board
area: games-and-search/game-tree-search
level: core
summary: Machine word whose bits mark the squares of a board that hold a given kind of piece. Move generation and tests such as four in a row become a few shifts, ANDs and ORs.
model: word-ram
complexity:
  vars: {n: the number of squares (at most the word size), s: the number of set bits}
  time: {worst: O(1)}
  space: {extra: O(1)}
prereqs: [bitwise-operations, bitmask]
see_also: [bit-set, population-count, lowest-set-bit, de-bruijn-bit-scan, trailing-zero-count, bit-parallelism, zobrist-hashing, alpha-beta-pruning]
sources:
  - paper: doi:10.1147/rd.33.0210
    title: Arthur L. Samuel, Some studies in machine learning using the game of checkers, IBM Journal of Research and Development 3(3) (1959)
    locator: pp. 210 to 229; the section on the representation of the board (the board as bits of machine words, with moves as shifts)
  - paper: doi:10.1070/RM1970v025n02ABEH003792
    title: G. M. Adelson-Velsky, V. L. Arlazarov, A. R. Bitman, A. A. Zhivotovsky and A. V. Uskov, Programming a computer to play chess, Russian Mathematical Surveys 25(2) (1970)
    locator: pp. 221 to 262; the description of the representation of positions by sets of squares in machine words
  - book: isbn:9780387908151
    title: David J. Slate and Lawrence R. Atkin, CHESS 4.5, the Northwestern University chess program, in Peter W. Frey (ed.), Chess Skill in Man and Machine, Springer
    locator: pp. 82 to 118 (the bit board representation of CHESS 4.5 and its attack maps)
  - paper: doi:10.3233/ICG-1999-22403
    title: Robert M. Hyatt, Rotated bitmaps, a new twist on an old idea, ICCA Journal 22(4) (1999)
    locator: pp. 213 to 222 (bitboards for the attacks of sliding pieces, kept in four rotations)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (bitwise tricks and techniques, including x AND -x and the counting of bits)
---

A bitboard is a machine word that stands for a set of squares of a game board: bit $i$ is 1 when square $i$ is in the set. A chess program keeps one 64-bit bitboard for each kind of piece and each color, such as "the white knights", and one for all pieces. Then a question about the whole board becomes one or a few word operations. The squares that a white pawn can push to are the white pawns shifted one rank up, ANDed with the empty squares. A line of four in Connect Four is found by two shifts and two ANDs per direction. The idea is the same as a [bit set](/bit-set/), applied to a board, with care at the edges so that a shift does not carry a piece from one side of the board to the other.

## In plain words

Draw the board and give each square a number. Now take a row of switches, one switch for each square. To store "where are my pieces", turn on the switches of the squares that hold your pieces. One such row of switches fits in a single number of the computer.

The computer can work on all the switches of a number at once. It can combine two rows of switches, keep only the switches that are on in both, or slide all switches by a few places, which moves every piece one step in the same direction. So one step of work answers a question about all squares together, where a plain board needs a loop over the squares.

The hard part is the edge of the board. When pieces slide off one side, they must not come back on the other side.

## The abstract type

A bitboard holds a subset of a fixed set of $n$ squares, where $n$ is at most the word size $w$. The operations are those of a set, plus a shift:
- `union(a, b)`, `intersection(a, b)`, `difference(a, b)` and `complement(a)` within the board.
- `contains(a, i)`, `add(a, i)` and `remove(a, i)` for one square $i$.
- `count(a)`: the number of squares in $a$.
- `lowest(a)`: the square with the smallest number in $a$, and the iteration over all squares of $a$.
- `shift(a, s)`: move every square of $a$ by the same step $s$ on the board, and drop the squares that leave the board.

A position of a game is a small tuple of bitboards. Tic-tac-toe needs two: the squares of X and the squares of O. Chess needs one per piece type and color, 12 in all.

## Representation

Number the squares $0$ to $n - 1$ and let bit $i$ of a word stand for square $i$. In tic-tac-toe square $i$ is in row $\lfloor i/3 \rfloor$ and column $i \bmod 3$, and the 8 winning lines are 8 constant masks of three bits each, for example $2^0 + 2^1 + 2^2 = 7$ for the top row.

For Connect Four on $w$ columns and $h$ rows, cell $(c, r)$, with the row $r$ counted from the bottom, is bit $c(h+1) + r$. So each column gets $h + 1$ bits, and the top bit of each column is a *guard bit* that is always 0. A move in direction "up" adds 1 to the bit number, "right" adds $h + 1$, and the two diagonals add $h$ and $h + 2$. The guard bits stop a run of stones that would wrap from the top of one column to the bottom of the next. A position is a pair (cur, mask): mask holds all stones, and cur holds the stones of the side to move. The 7 by 6 board needs 49 bits, which fit in one 64-bit word. This layout is the one of John Tromp's Fhourstones program.

The invariants are:
- **(B1) Range.** No bit outside the board is set, and in Connect Four no guard bit is set.
- **(B2) Disjoint sides.** In tic-tac-toe the boards of X and O share no bit. In Connect Four cur is a subset of mask.
- **(B3) Gravity.** In Connect Four, each column of mask is a block of ones that starts at the bottom row.

## Operations

```pseudo id=main
HAS-LINE(b)                                ▷ tic-tac-toe: does b hold a full line?
L1  return true if b AND w = w for one of the 8 line masks w, else false

EMPTY(x, o)
L2  return NOT (x OR o) AND (2^9 − 1)

PLAY-SQUARE(x, i)
L3  return x OR 2^i

BITS(b)                                    ▷ the squares of b, lowest first
L4  while b ≠ 0 do low ← b AND (−b)        ▷ the lowest set bit
L5      output the index of low
L6      b ← b XOR low

CAN-PLAY(mask, c)                          ▷ Connect Four
L7  return (mask AND TOP(c)) = 0           ▷ TOP(c) is the bit of cell (c, h − 1)

PLAY(cur, mask, c)
L8  cur ← cur XOR mask                     ▷ the stones of the opponent, who moves next
L9  mask ← mask OR (mask + BOTTOM(c)); return (cur, mask)   ▷ BOTTOM(c) is the bit of cell (c, 0)

WON(b)                                     ▷ four in a row in b?
L10 for s in 1, h + 1, h, h + 2 do         ▷ up, right and the two diagonals
L11     m ← b AND (b >> s)                 ▷ bit i: stones at i and i + s
L12     if m AND (m >> 2s) ≠ 0 then return true
L13 return false
```

Line L9 is the main trick. The stones of column $c$ are a block of ones from the bottom, so adding the bottom bit of the column makes a carry run through the block and stop at the first empty cell. The OR puts the old stones back. Lines L11 and L12 find four in a row in two steps. The first step marks every stone whose neighbor in direction $s$ is also a stone, and the second step marks the pairs whose pair at distance $2s$ is also marked. The side that just moved is cur XOR mask after the move, so a search tests WON(cur XOR mask) after each move.

## Example

Take Connect Four on 4 columns and 4 rows, so each column has 5 bits and column $c$ starts at bit $5c$. Suppose column 1 holds two stones. Its bits in mask are 5 and 6, so this part of mask is $2^5 + 2^6 = 96$. To play in column 1, add BOTTOM(1) $= 2^5 = 32$. The sum is $128 = 2^7$: the carry cleared bits 5 and 6 and set bit 7. The OR with the old mask gives bits 5, 6 and 7, so the new stone is at row 2, the lowest empty cell.

Now let the side that just moved hold the bottom row: cells $(0, 0)$, $(1, 0)$, $(2, 0)$ and $(3, 0)$, which are bits 0, 5, 10 and 15. For the shift $s = 5$, $b >> 5$ has bits 0, 5 and 10, so $m$ has bits 0, 5 and 10. Then $m >> 10$ has bit 0, and $m$ AND $(m >> 10)$ is bit 0, which is not zero. So WON reports four in a row, starting at cell $(0, 0)$.

The test file checks all 5478 positions that can come up in tic-tac-toe and all 161029 positions that can come up in Connect Four on 4 columns and 4 rows. In each position it compares the legal moves, the win tests and the board with a plain array version.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). Lines L4 to L6 work because, in two's complement, $-b$ is NOT $b$ plus 1, and the carry of the plus 1 stops at the lowest set bit of $b$, so $b$ AND $(-b)$ keeps only that bit. Line L9 is correct by (B3): the carry runs through the block of stones of the column and stops at the lowest empty cell, and the guard bit and CAN-PLAY make sure that this cell is on the board. Line L8 is correct by (B2). For WON, bit $i$ of $m$ AND $(m >> 2s)$ is set exactly when the bits $i$, $i + s$, $i + 2s$ and $i + 3s$ are stones. By (B1) a run of four that leaves a column passes through a guard bit, so every such run is a real line of the board.

## Complexity

| operation | time | space |
|---|---|---|
| union, intersection, complement, shift | $O(1)$ | one word |
| contains, add, remove | $O(1)$ | |
| count | $O(1)$ with a popcount instruction, else $O(\log w)$ | |
| lowest | $O(1)$ with a bit-scan instruction, else $O(\log w)$ | |
| iterate over the squares | $O(s)$ for $s$ set bits | |
| PLAY and WON in Connect Four | $O(1)$ | |

The bounds are on the [word RAM](/word-ram/), where a word op costs $O(1)$ and the board has at most $w$ squares. The count and the lowest bit come from [population count](/population-count/) and from [lowest set bit](/lowest-set-bit/) with a [trailing zero count](/trailing-zero-count/) or a [de Bruijn bit scan](/de-bruijn-bit-scan/). A board with more squares than the word size uses several words, and each operation costs $O(n/w)$.

## Variants

- **Chess bitboards.** Twelve 64-bit boards, one per piece and color, plus their unions. Knight and king attacks come from a table of 64 masks. Pawn pushes and captures are shifts with masks for the a-file and the h-file.
- **Sliding pieces.** The attacks of a rook, bishop or queen depend on the pieces in the way. *Rotated bitboards* keep the occupancy also in board copies rotated by 90 and 45 degrees, so a whole line becomes a run of adjacent bits that indexes a table. *Magic bitboards* multiply the masked occupancy by a constant and use the top bits as an index. A fill with parallel prefix shifts, the Kogge-Stone fill, needs no table.
- **Checkers.** Samuel used a word with padding squares so that each diagonal step is a shift by 4 or 5.
- **Othello.** A shift in a direction, ANDed with a mask that removes the wrapped files, gives the flips of all discs at once.
- **Guard bits or masks.** Connect Four uses guard bits to stop wraps. Chess uses masks after each shift, because 64 squares leave no spare bits in a 64-bit word.

## When to use it

Use bitboards when the board has at most a few words of squares and the rules are local, such as steps, lines and neighbors. They suit search programs that make millions of moves per second, because a position is a few words, so it is cheap to copy, to compare, and to hash. A plain array is simpler for boards much larger than a word, for rules that are not local, and for code where speed does not matter.

## Pitfalls

- **Wrap-around at the edges.** In chess, $b << 1$ moves a piece on the h-file to the a-file of the next rank. Mask the result, or keep guard bits as in Connect Four.
- **Shifts by the word size or more.** In C, a shift by 64 or more of a 64-bit value is undefined. Python ints grow without limit, so mask the result with $2^{64} - 1$ after a left shift where a C program would lose the high bits.
- **Signed right shift.** In Java a right shift `>>` of a signed value copies the sign bit, and in C the result for a negative value is implementation-defined (most compilers copy the sign bit). Use unsigned types, or `>>>` in Java.
- **Square numbering.** Programs differ in where square 0 is and whether the bits go by rank or by file. The masks, the shifts and the tables must all use the same order.
- **Counting by loop.** A loop over all $n$ bits to count them throws away the gain. Use the popcount instruction or a [bit-parallel](/bit-parallelism/) count.

## Implementations

The Python version has tic-tac-toe with two 9-bit boards and Connect Four for any size of board, with the guard bits of the layout above. The tests compare both with plain array versions on every reachable position of tic-tac-toe and of Connect Four on 4 by 4, on several other board shapes, and on random games on the 7 by 6 board.

## History

Samuel's checkers program of the 1950s, described in 1959, kept the board in machine words and made moves by shifts. In chess, the Soviet program of the Institute for Theoretical and Experimental Physics, described by Adelson-Velsky and others in 1970, kept positions as sets of squares in machine words, and the same group later wrote Kaissa. In the United States, Slate and Atkin used bitboards in the Northwestern program CHESS 4.5 and described them in 1977. Hyatt described rotated bitboards in 1999, after he had used them in his program Crafty, and magic bitboards became common in the 2000s.

## References
