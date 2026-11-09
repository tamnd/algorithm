---
tag: TH2QRV
kind: problem
slug: n-queens-problem
name: N-queens problem
aliases:
- Eight queens puzzle
- eight queens
- eight queens puzzle
- n queens
area: combinatorics/exhaustive-search
level: intro
summary: Place n queens on an n-by-n board so that no two attack each other; a classic backtracking example.
prereqs: [generic-backtracking-algorithm, permutation]
see_also: [generic-backtracking-algorithm, exact-cover, algorithm-x, dancing-links, search-space, constraint-satisfaction-problem, symmetry-breaking, bit-set]
sources:
  - paper: doi:10.1016/j.disc.2007.12.043
    title: Jordan Bell and Brett Stevens, A survey of known results and research areas for n-queens, Discrete Mathematics 309(1), 2009, 1 to 31
    locator: the history (Bezzel, Nauck, Gauss), the explicit constructions for all n of at least 4, the modular (toroidal) board, and the table of counts
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2, Backtrack programming (the n queens problem as the main example, with bitwise methods and the counts)
  - paper: doi:10.1613/jair.5512
    title: Ian P. Gent, Christopher Jefferson and Peter Nightingale, Complexity of n-Queens Completion, Journal of Artificial Intelligence Research 59, 2017, 815 to 848
    locator: the NP-completeness and the #P-completeness of n-queens completion
  - paper: "Michael Simkin, The number of n-queens configurations, Advances in Mathematics 427 (2023) 109127, arXiv:2107.13460"
    locator: the main theorem, Q(n) = ((1 ± o(1)) n e^(-α))^n with α = 1.942 ± 0.003
  - url: https://oeis.org/A000170
    title: OEIS A000170, number of ways of placing n nonattacking queens on an n X n board
    locator: the table of values
---

The $n$-queens problem asks for a placement of $n$ queens on an $n \times n$ chessboard so that no two queens share a row, a column or a diagonal. It has a solution for $n = 1$ and for every $n \ge 4$, and none for $n = 2$ and $n = 3$. Finding one solution is easy, by an explicit formula, but counting all solutions $Q(n)$ is hard, and no closed form is known. The problem is the standard first example of [backtracking](/generic-backtracking-algorithm/) and an instance of [exact cover](/exact-cover/) with secondary items.

## In plain words

A queen in chess attacks every square in her row, in her column and on her two diagonals. The puzzle is to put as many queens as there are rows on the board so that no queen attacks another one.

Since no two queens can share a row, there is exactly one queen in each row, and in the same way one in each column. So a solution is a list that gives the column of the queen in each row. The task is to find such a list in which no two queens are on a common diagonal.

On the usual board with eight rows there are 92 solutions. People often want to find all of them, or to count them for larger boards. The count grows very fast, and computers find exact counts only for boards of modest size.

## Definition

A *placement* of $n$ queens is a set of $n$ cells $(r, c)$ with $r, c \in \{0, \ldots, n-1\}$. Two queens at $(r_1, c_1)$ and $(r_2, c_2)$ *attack* each other if $r_1 = r_2$, or $c_1 = c_2$, or $r_1 + c_1 = r_2 + c_2$, or $r_1 - c_1 = r_2 - c_2$. A *solution* is a placement in which no two queens attack each other.

Each solution has one queen in each row and one in each column, so it is a [permutation](/permutation/) $p$ of $\{0, \ldots, n-1\}$, with the queen of row $r$ in column $p(r)$. The permutation is a solution exactly when the $n$ values $r + p(r)$ are distinct and the $n$ values $r - p(r)$ are distinct.

Three tasks are studied.

- **Find.** Input $n$; output one solution, or report that there is none.
- **List or count.** Input $n$; output all solutions, or their number $Q(n)$.
- **Completion.** Input $n$ and a placement of some queens that do not attack each other; decide whether it extends to a solution.

## Variants

- **Distinct solutions.** The 8 symmetries of the square (rotations and reflections) map solutions to solutions. The number of classes of solutions under these symmetries is OEIS A002562.
- **Modular or toroidal queens.** The diagonals wrap around: $r + c$ and $r - c$ are taken modulo $n$. Solutions exist if and only if $\gcd(n, 6) = 1$; this result goes back to Pólya (see the survey of Bell and Stevens).
- **Queens completion.** Some queens are given in advance. This version is NP-complete (Gent, Jefferson and Nightingale, 2017).
- **Other pieces and boards.** Non-attacking kings, rooks or bishops; queens on boards with holes; queens in three dimensions; the domination problem, which asks for the fewest queens that attack every cell.

## Examples

**The 4-queens problem.** There are two solutions, $p = (1, 3, 0, 2)$ and $p = (2, 0, 3, 1)$, each the mirror image of the other:

```
. Q . .      . . Q .
. . . Q      Q . . .
Q . . .      . . . Q
. . Q .      . Q . .
```

**The counts.** Here $Q(n)$ is the number of solutions, "distinct" counts them up to the 8 symmetries, and "nodes" is the number of placements of queens in the first rows that a backtracking search visits when it tests each new queen at once (the root included).

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $Q(n)$ | 1 | 0 | 0 | 2 | 10 | 4 | 40 | 92 | 352 | 724 | 2,680 | 14,200 |
| distinct | 1 | 0 | 0 | 1 | 2 | 1 | 6 | 12 | 46 | 92 | | |
| nodes | 2 | 3 | 6 | 17 | 54 | 153 | 552 | 2,057 | 8,394 | 35,539 | 166,926 | 856,189 |

The count is not monotone: $Q(6) = 4 < Q(5) = 10$. OEIS A000170 lists $Q(n)$ for larger $n$, for example $Q(16) = 14{,}772{,}512$.

**An explicit solution.** For $n = 8$, the queens of rows 1 to 8 in the columns $2, 4, 6, 8, 3, 1, 7, 5$ form a solution. It comes from the rule below.

## Known algorithms

**Backtracking.** Place queens row by row. Keep three sets: the used columns, the used values of $r + c$, and the used values of $r - c$. A new queen in row $r$ may go to column $c$ only if $c$, $r + c$ and $r - c$ are all unused. This is the [generic backtracking algorithm](/generic-backtracking-algorithm/) with $O(1)$ tests. With [bit sets](/bit-set/), the three sets are machine words. If $cols$, $ld$ and $rd$ mark the cells of the next row that are attacked along columns and along the two diagonals, the free cells are $\lnot(cols \lor ld \lor rd)$ restricted to $n$ bits, and after a queen at bit $b$ the next row gets $cols \lor b$, $(ld \lor b) \ll 1$ and $(rd \lor b) \gg 1$. Each node then costs $O(1)$ word operations per child. Knuth develops these programs in Section 7.2.2 of *The Art of Computer Programming*. The search visits each node of the backtrack tree once; the "nodes" row of the table above shows that the tree grows much more slowly than $n!$ but still exponentially.

**Exact cover.** Make one primary item for each row and each column, and one secondary item for each diagonal, which may be covered at most once. Each cell is an option that covers its row, its column and its two diagonals. The exact covers are the solutions. [Algorithm X](/algorithm-x/) with [dancing links](/dancing-links/) solves it this way.

**Explicit construction.** A solution for each $n \ge 4$ can be written down in $O(n)$ time. With columns numbered 1 to $n$:

1. Write the even numbers $2, 4, \ldots$ up to $n$, then the odd numbers $1, 3, \ldots$ up to $n$.
2. If $n \bmod 6 = 2$, swap 1 and 3 in the odd list and move 5 to its end.
3. If $n \bmod 6 = 3$, move 2 to the end of the even list, and move 1 and 3, in this order, to the end of the odd list.

The list gives the column of the queen in rows 1 to $n$. Constructions of this kind go back to Pauls (1874); Bell and Stevens survey them. For $n$ with $\gcd(n, 6) = 1$ there is a shorter rule with a short proof: put the queen of row $r$ in column $2r \bmod n$, for $r = 0, \ldots, n-1$. The columns are distinct because 2 is invertible modulo $n$. The values $r + c \equiv 3r$ are distinct modulo $n$ because 3 is invertible, so they are distinct as integers too. The values $r - c \equiv -r$ are distinct modulo $n$. So no two queens attack, even on the toroidal board.

**Local search.** Start with a permutation and repeatedly move a queen that is attacked to the column in its row with the fewest conflicts (the *min-conflicts* heuristic). In practice this finds one solution for very large $n$ quickly, but it gives no guarantee and cannot count.

## Bounds

- **Existence.** $Q(n) \ge 1$ for $n = 1$ and $n \ge 4$, by the construction; $Q(2) = Q(3) = 0$ by inspection of all placements.
- **Trivial upper bound.** $Q(n) \le n!$, since each solution is a permutation.
- **Asymptotics.** Simkin (2023) proved that there is a constant $\alpha = 1.942 \pm 0.003$ with

$$Q(n) = \left((1 \pm o(1))\, n e^{-\alpha}\right)^n.$$

So $Q(n)$ is about $(0.143\, n)^n$, which is exponentially smaller than $n! \approx (n/e)^n$ but still grows faster than any $c^n$.

- **Complexity.** Finding one solution takes $O(n)$ time. Completion is NP-complete, and counting the completions is #P-complete (Gent, Jefferson and Nightingale, 2017). No polynomial-time method to compute $Q(n)$ is known; the best exact counts come from very large backtracking searches.

## Reductions

- **To exact cover.** As above, with $2n$ primary items, $4n - 2$ secondary items for the diagonals, and $n^2$ options. Each solution of the queens problem is one exact cover, and conversely.
- **To SAT.** One Boolean variable per cell, with clauses "at least one queen in each row" and "at most one queen in each row, column and diagonal". The satisfying assignments are the solutions.
- **To completion from other problems.** The hardness of completion comes from a polynomial reduction of a known NP-complete problem to it, given by Gent, Jefferson and Nightingale. They also show that counting the completions is #P-complete.

## Applications

The problem is a standard test case. It is the first example of backtracking in many textbooks, a benchmark for [constraint satisfaction](/constraint-satisfaction-problem/) solvers and SAT solvers, and a test of parallel search because the subtrees below the first rows are independent.

## References
