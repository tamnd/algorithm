---
tag: A6NC0T
kind: technique
slug: broken-profile-dp
name: Broken-profile dynamic programming
aliases:
- plug DP
- profile DP
area: techniques/dynamic-programming
level: advanced
summary: Process a grid cell by cell, keeping as state the profile of the frontier already decided.
prereqs: [bitmask-dp, bit-manipulation]
see_also: [domino-tiling-problem, transfer-matrix-method, counting-perfect-matchings, bitmask-dp, dp-on-tree-decompositions, rolling-array-space-reduction]
sources:
  - book: isbn:9783030393564
    title: Antti Laaksonen, Guide to Competitive Programming, second edition, Springer, 2020
    locator: Chapter 6, Dynamic Programming, the section on counting tilings
  - paper: doi:10.1016/0031-8914(61)90063-5
    title: P. W. Kasteleyn, The statistics of dimers on a lattice, I. The number of dimer arrangements on a quadratic lattice, Physica 27(12), 1209-1225, 1961
    locator: the closed formula for the number of domino tilings of a rectangle, used here to check the counts
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 4.7, The transfer-matrix method
---

Broken-profile dynamic programming fills a grid of $n$ rows and $m$ columns one cell at a time, in row order, and keeps as its state the profile: for each of the $m$ columns, a few bits about the boundary between the decided and the undecided cells. Because the cells are processed one by one, the boundary is a broken line: it is one row lower for the columns already passed in the current row. The state has $2^m$ values for one bit per column, and each cell has $O(1)$ transitions, so the time is $O(n m 2^m)$, against $O(n 4^m)$ or more for a DP that moves one whole row at a time. Counting the [domino tilings](/domino-tiling-problem/) of a rectangle is the standard example.

## In plain words

You must fill a grid, for example with dominoes, and count the ways. Going row by row, you need to remember which cells of the next row are already covered by pieces that stick out from the row above. That is one yes or no per column.

Instead of placing a whole row at once, place pieces one cell at a time, left to right, top to bottom. At each step, the memory is still one yes or no per column. For the columns you have passed, it is about the next row; for the others, it is about the current row. At each cell there are only a few choices: the cell is already covered, or you put a domino down from it, or you put one to the right. The counts move from one set of memories to the next.

## When it applies

- The input is a grid with one small side $m$ (up to about 10 to 20) and one long side $n$.
- The pieces or constraints are local: each piece touches only neighboring cells, so the effect of the decided part on the undecided part passes only through the cells next to the boundary.
- The question is to count, or to optimize over, all fillings: tilings with dominoes or small polyominoes, covers of a board with forbidden cells, or colorings with local rules.
- When the constraints are about connectivity, such as one closed path through all cells (plug DP), the profile must also store which boundary cells are connected, and the state space grows; see the variations.

## The template

Let bit $j$ of the profile $p$ mean "the cell in column $j$ just below the boundary is already covered". Before cell $(i, j)$ is processed, the bits $0, \ldots, j-1$ refer to row $i + 1$ and the bits $j, \ldots, m-1$ refer to row $i$. The holes are the moves allowed at a cell and the start and end profiles. The version below counts domino tilings.

```pseudo id=main
BROKEN-PROFILE(n, m)
L1  dp ← {0 ↦ 1}                                     ▷ hole: the start profile
L2  for i ← 0 to n − 1 do
L3      for j ← 0 to m − 1 do
L4          nd ← empty map
L5          for each (p, c) in dp do
L6              if bit j of p is 1 then               ▷ (i, j) is already covered
L7                  nd[p without bit j] += c
L8              else                                  ▷ hole: the pieces that can cover (i, j)
L9                  if i + 1 < n then nd[p with bit j] += c                    ▷ vertical domino down
L10                 if j + 1 < m and bit j+1 of p is 0 then nd[p with bit j+1] += c   ▷ horizontal domino right
L11         dp ← nd
L12 return dp[0]                                      ▷ hole: the end profile
```

**Why the profile is enough.** Before cell $(i, j)$, the cells above the boundary are all decided and covered. A piece placed earlier can reach below the boundary only by one cell, at the bit of its column, because a domino covers two adjacent cells. So which cells below the boundary are already covered is the only thing the future needs, and the bits record exactly that. After cell $(i, j)$, bit $j$ means row $i + 1$: line L7 clears it (nothing from $(i, j)$ reaches $(i + 1, j)$), line L9 sets it (the vertical domino covers $(i + 1, j)$), and line L10 leaves it 0 and sets bit $j + 1$, which still refers to row $i$.

**Why the count is right.** Every tiling makes one choice at each cell, in the fixed order, and each choice moves to one profile. So the tilings are in bijection with the paths from the start profile to the end profile, and the map $dp$ counts the paths.

**Cost.** There are $nm$ cells, at most $2^m$ profiles before each, and at most 2 moves per profile. The time is $O(n m 2^m)$ and the space is $O(2^m)$, since only the current map is kept, as in [rolling arrays](/rolling-array-space-reduction/).

## Classic examples

### Domino tilings of a 2 by 3 board

Write a profile as the bits of the columns 0, 1, 2 from left to right. The maps after each cell are:

| after cell | profiles and counts |
|---|---|
| $(0, 0)$ | $100 \mapsto 1$, $010 \mapsto 1$ |
| $(0, 1)$ | $000 \mapsto 1$, $110 \mapsto 1$, $101 \mapsto 1$ |
| $(0, 2)$ | $100 \mapsto 1$, $001 \mapsto 1$, $111 \mapsto 1$ |
| $(1, 0)$ | $000 \mapsto 1$, $011 \mapsto 2$ |
| $(1, 1)$ | $001 \mapsto 3$ |
| $(1, 2)$ | $000 \mapsto 3$ |

The answer is 3: three vertical dominoes, or one vertical domino at either end with two horizontal ones beside it. In the first row, profile $100$ after $(0, 0)$ means a vertical domino from $(0, 0)$ covers $(1, 0)$, and $010$ means a horizontal domino covers $(0, 0)$ and $(0, 1)$.

### Larger boards

The same program gives these counts, which agree with Kasteleyn's formula:

| board | $2 \times 7$ | $3 \times 4$ | $3 \times 8$ | $4 \times 4$ | $8 \times 8$ |
|---|---|---|---|---|---|
| tilings | 21 | 11 | 153 | 36 | 12,988,816 |

The $2 \times n$ counts are the Fibonacci numbers, and a $3 \times n$ board with $n$ odd has no tiling, since it has an odd number of cells.

### Other uses

- **Boards with holes.** Mark the forbidden cells as covered from the start, by treating them as in line L7.
- **Other pieces.** Trominoes and other small shapes reach more than one row down; the profile then needs one bit per column for each row that a piece can reach.
- **Optimization.** Replace the counts by a minimum or a maximum, for example the most dominoes that fit on a board with holes.
- **Independent sets and colorings of a grid.** A cell in a chosen set needs its upper and left neighbors to be free; the profile stores the last $m$ cells.

## Variations

- **Row by row.** A DP from one row profile to the next, over all pairs that fit, is the [transfer matrix method](/transfer-matrix-method/). For dominoes it has up to $4^m$ pairs per row; the broken profile splits each row step into $m$ cheap steps. For a very long board with small $m$, the transfer matrix can be raised to the $n$-th power in $O(8^m \log n)$ time.
- **Plug DP.** For problems on paths and cycles, such as counting Hamiltonian cycles of a grid graph, each boundary edge has a plug, and the profile also stores a matching of the plugs that tells which ones are joined by a path below the boundary. The states are coded as bracket sequences or with small labels.
- **Closed formulas.** For domino tilings of a full rectangle, the count has the product formula of Kasteleyn and of Temperley and Fisher, and for planar graphs, [counting perfect matchings](/counting-perfect-matchings/) is polynomial by the Pfaffian method. Broken profile is still useful for boards with holes and for other pieces.

## Pitfalls

- **The orientation.** Make $m$ the smaller side. $2^m$ for $m = 20$ is already about a million profiles.
- **Mixed meaning of the bits.** Bit $j$ changes from row $i$ to row $i + 1$ when cell $(i, j)$ is processed. Code that tests bit $j + 1$ as if it were in the next row gives wrong counts.
- **Pieces that leave the board.** Line L9 must check $i + 1 < n$ and line L10 must check $j + 1 < m$. Without these checks, the program counts pieces that hang off the board, and the end profile $0$ may hide the error only on some sizes.
- **Overflow.** The counts grow exponentially in $nm$; use big integers or a modulus.

## Exercises

1. Run the template by hand on a $2 \times 2$ board, and check that it gives 2.
2. Change the template to count the tilings of a board in which some cells are blocked.
3. Prove that the number of domino tilings of a $2 \times n$ board is the Fibonacci number $F_{n+1}$.
   <details><summary>Hint</summary>Look at the left end: one vertical domino leaves a $2 \times (n-1)$ board, two horizontal ones leave a $2 \times (n-2)$ board.</details>
4. Write a broken-profile DP that counts the sets of cells of an $n \times m$ grid with no two cells side by side, and give its running time.

## References
