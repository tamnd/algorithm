---
tag: 5N96QY
kind: problem
slug: sudoku
name: Sudoku problem
aliases:
- Generalized Sudoku
- Number Place
- Sudoku
- number place
- sudoku solving
area: games-and-search/puzzles
level: intro
summary: Fill an n^2 by n^2 grid so that each row, column and box holds each symbol once. The 9 by 9 case is finite; the generalized family is NP-complete and ASP-complete.
prereqs: [constraint-satisfaction-problem, exact-cover, np-complete]
see_also: [latin-square-completion, algorithm-x, dancing-links, all-different-constraint, minimum-remaining-values, sat, list-coloring, counting-latin-squares]
sources:
  - paper: "Takayuki Yato and Takahiro Seta, Complexity and completeness of finding another solution and its application to puzzles, IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences E86-A(5), 2003, 1052 to 1060"
    locator: the definition of ASP-completeness and the reduction from partial Latin square completion to Number Place (Sudoku)
  - paper: doi:10.1016/0166-218X(84)90075-1
    title: Charles J. Colbourn, The complexity of completing partial Latin squares, Discrete Applied Mathematics 8(1), 1984, 25 to 30
    locator: the NP-completeness of partial Latin square completion
  - paper: "Bertram Felgenhauer and Frazer Jarvis, Mathematics of Sudoku I, Mathematical Spectrum 39(1), 2006, 15 to 22"
    locator: the count of 6,670,903,752,021,072,936,960 completed 9 by 9 grids
  - paper: "Ed Russell and Frazer Jarvis, Mathematics of Sudoku II, Mathematical Spectrum 39(2), 2006, 54 to 58"
    locator: the count of 5,472,730,538 essentially different grids, by Burnside's lemma
  - paper: "Gary McGuire, Bastian Tugemann and Gilles Civario, There is no 16-clue Sudoku: solving the Sudoku minimum number of clues problem via hitting set enumeration, Experimental Mathematics 23(2), 2014, 190 to 217"
    locator: the main result, that a 9 by 9 puzzle with a unique solution has at least 17 clues
  - paper: "Inês Lynce and Joël Ouaknine, Sudoku as a SAT problem, Ninth International Symposium on Artificial Intelligence and Mathematics (ISAIM), Fort Lauderdale, 2006"
    locator: the minimal and the extended CNF encodings, and the propagation rules that solve puzzles without search
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2.1, Dancing links (Sudoku as an exact cover problem)
  - url: https://oeis.org/A107739
    title: OEIS A107739, number of completed Sudokus of size n^2 X n^2
    locator: the values 1, 1, 288 and 6670903752021072936960
---

The Sudoku problem gives a square grid of side $n^2$, split into $n^2$ boxes of size $n \times n$, with some cells filled with symbols from $1$ to $n^2$, and asks for a filling of the empty cells so that each row, each column and each box holds each symbol exactly once. The usual puzzle is the case $n = 3$, a $9 \times 9$ grid. One fixed size is a finite problem, so the hardness results are for the family over all $n$: Yato and Seta (2003) proved that the generalized problem is [NP-complete](/np-complete/), and that it stays NP-complete to decide whether a second solution exists when one solution is given. In practice, Sudoku is a small [constraint satisfaction problem](/constraint-satisfaction-problem/), and a search with propagation, an [exact cover](/exact-cover/) solver or a [SAT](/sat/) solver finds the answer in milliseconds for $n = 3$.

## In plain words

The board is a square of cells, cut into equal square boxes. The usual board has nine rows, nine columns and nine boxes of three by three cells. Some cells already show a digit. You must write a digit in each empty cell so that no digit repeats in any row, any column or any box. Then each row, column and box holds each digit exactly once.

A good puzzle has exactly one answer, and you can reach it by logic alone: a cell where only one digit still fits, or a digit that fits in only one cell of a row.

A computer can solve the usual board at once. The hard question is about bigger boards of the same shape. Nobody knows a method that stays fast as the board grows, and such a method would also solve thousands of other hard problems.

## Definition

Fix an integer $n \ge 1$ and put $N = n^2$. The grid has the cells $(r, c)$ with $r, c \in \{0, \ldots, N-1\}$. Cell $(r, c)$ lies in row $r$, column $c$ and box $b(r, c) = n \lfloor r/n \rfloor + \lfloor c/n \rfloor$. Rows, columns and boxes are the $3N$ *units*, and each unit has $N$ cells.

A *partial grid* is a map $G$ from the cells to $\{0, 1, \ldots, N\}$, where $0$ marks an empty cell and the nonzero values are the *clues* (givens). A *completion* of $G$ is a map $S$ from the cells to $\{1, \ldots, N\}$ with $S(r, c) = G(r, c)$ at every clue, such that the $N$ cells of each unit get $N$ different symbols. A completed grid is a Latin square of order $N$ with the extra box condition.

- **Decision.** Input: $n$ and a partial grid $G$. Question: does $G$ have a completion?
- **Search.** Output a completion, or report that none exists.
- **Counting.** Output the number of completions.
- **Uniqueness.** Decide whether $G$ has exactly one completion. A *proper puzzle* is a partial grid with exactly one completion.
- **Another solution (ASP).** Input: $G$ and one completion $S$. Question: does $G$ have a completion other than $S$?

The input has $N^2 = n^4$ cells of $O(\log n)$ bits each, so its size is $\Theta(n^4 \log n)$. A completion is a certificate of size $O(n^4 \log n)$ that can be verified in $O(n^4)$ unit operations, one pass per unit, so the decision problem is in [NP](/np/). For a fixed $n$ there are at most $N^{N^2}$ fillings, which is $9^{81}$ for the usual grid: a constant, so the $9 \times 9$ problem has no asymptotic complexity.

## Variants

- **Rectangular boxes.** Boxes of $p \times q$ cells in a grid of side $N = pq$, for example the $6 \times 6$ grid with $2 \times 3$ boxes.
- **Irregular boxes.** Any partition of the $N \times N$ grid into $N$ regions of $N$ cells ("jigsaw Sudoku"). A completed grid is then a gerechte design.
- **Extra units.** Sudoku X adds the two main diagonals as units. Each extra unit is one more all-different constraint.
- **Arithmetic clues.** Killer Sudoku replaces the givens by cages with a given sum, which brings in the sum constraints of [Kakuro](/kakuro-problem/).
- **Latin squares.** Without the box rule, only rows and columns remain, and the problem becomes [Latin square completion](/latin-square-completion/).
- **Puzzle design.** Find a proper puzzle with few clues, or decide whether removing a clue keeps the solution unique. These tasks ask the uniqueness question many times.

## Examples

**A $4 \times 4$ puzzle ($n = 2$).** Dots are empty cells, and the bars mark the $2 \times 2$ boxes.

```
1 . | . .        1 2 | 4 3
. . | 2 .        3 4 | 2 1
----+----        ----+----
. 3 | . .        4 3 | 1 2
. . | . 4        2 1 | 3 4
```

Cell $(1, 1)$ sees 2 in its row, 3 in its column and 1 in its box, so only 4 fits there. Then cell $(0, 1)$ must be 2, the last cells of row 0 get 4 and 3 (column 3 already has a 4), row 1 gets 3 and 1, column 0 gets 4 and 2, row 2 gets 1 and 2, and row 3 gets 1 and 3. Each step fills a cell that has one candidate, so the solution on the right is the only one. This puzzle has 4 clues. No $4 \times 4$ puzzle with 3 clues has a unique solution, and among the $288 \cdot \binom{16}{4}$ pairs of a grid and a set of 4 cells, 25,728 give a proper puzzle.

**Counts of completed grids.**

| $n$ | grid | completed grids | source |
|---|---|---|---|
| 1 | $1 \times 1$ | 1 | |
| 2 | $4 \times 4$ | 288 | OEIS A107739 |
| 3 | $9 \times 9$ | 6,670,903,752,021,072,936,960 | Felgenhauer and Jarvis |

The $9 \times 9$ count factors as $2^{20} \cdot 3^8 \cdot 5 \cdot 7 \cdot 27{,}704{,}267{,}971$. Felgenhauer and Jarvis found it by listing the fillings of the top band of three boxes, sorting them into classes with the same number of completions, and counting the completions of one band per class by computer. The grid symmetries are the permutations of the three bands, of the rows inside each band, of the three stacks and of the columns inside each stack, and the transposition: $2 \cdot 6^8 = 3{,}359{,}232$ maps, together with the $9!$ relabelings of the symbols. Russell and Jarvis counted the orbits of this group with [Burnside's lemma](/burnside-lemma/) and found 5,472,730,538 essentially different grids. This is a little more than the total count divided by the group order, $6.67 \cdot 10^{21} / (3{,}359{,}232 \cdot 9!) \approx 5{,}472{,}447{,}994$, because a few grids have nontrivial symmetries.

**Clues.** A proper $9 \times 9$ puzzle has at least 17 clues (McGuire, Tugemann and Civario 2014, by an exhaustive computer search over all essentially different grids). Here is one with 17 clues, row by row, where 0 is an empty cell:

```
000000010 400000000 020000000 000050407 008000300 001090000 300400200 050100000 000806000
```

At the other end, a puzzle with at least 78 clues that has a completion has only one. Proof: let $S \ne S'$ be two completions and let $D$ be the set of cells where they differ. In a row that meets $D$, the cells outside $D$ hold the same symbols in $S$ and $S'$, so the cells of $D$ in that row hold the same set of symbols in both; with one cell this set has one symbol, and the two completions agree there, a contradiction. So each row and each column that meets $D$ has at least two cells of $D$, and $|D| \ge 4$. Hence a puzzle with at most 3 empty cells has at most one completion. The bound is tight. Take the completed grid with the rows 534678912, 672195348, 198342567, 859761423, 426853791, 713924856, 961537284, 287419635 and 345286179. In rows 0 and 3, columns 3 and 4 hold 6, 7 and 7, 6, and both pairs lie in the middle stack of boxes. Swapping the symbols in these four cells keeps every row, column and box valid, so the 77 other cells form a puzzle with two solutions.

## Known algorithms

**Backtracking with propagation.** Treat each empty cell as a variable with the domain $\{1, \ldots, N\}$ and each unit as an [all-different constraint](/all-different-constraint/). The search fills one cell at a time and keeps, for each unit, the set of symbols already used. At each node it picks the empty cell with the fewest candidates, the [minimum remaining values](/minimum-remaining-values/) rule. A cell with one candidate ("naked single") is filled without a real branch, and a cell with no candidate ends the branch.

```pseudo id=main
SUDOKU-SOLVE(G)
L1  E ← the empty cells of G
L2  if E is empty then output G and return
L3  for each c ∈ E: cand(c) ← the symbols not used in the row, column or box of c
L4  pick c ∈ E with the fewest candidates
L5  if cand(c) is empty then return
L6  for each v ∈ cand(c) do
L7      G(c) ← v
L8      SUDOKU-SOLVE(G)
L9      G(c) ← 0
```

The recursion depth is at most the number of empty cells, and each node costs $O(N^3)$ time to recompute the candidates of $O(N^2)$ cells, or less with incremental bit masks. The search is complete, because each branch tries every symbol that the clues allow. Stronger propagation cuts more branches: [forward checking](/forward-checking/), [arc consistency](/arc-consistency/) on the binary form of the constraints, and the matching-based filtering of all-different by [Régin's algorithm](/regin-all-different-filtering/), which finds "hidden singles" (a symbol with one possible cell in a unit) and the pair and triple rules of human solvers.

**Exact cover.** The [exact cover page](/exact-cover/) gives the model: $4N^2$ items ("cell $(r, c)$ is filled", "row $r$ has $v$", "column $c$ has $v$", "box $b$ has $v$") and $N^3$ options, one for each symbol in each cell, each covering four items. For $n = 3$ that is 324 items and 729 options. [Algorithm X](/algorithm-x/) with [dancing links](/dancing-links/) branches on the item with the fewest live options. A cell item with one option is a naked single and a row, column or box item with one option is a hidden single, so this one rule covers both kinds of forced move. Knuth uses Sudoku as a main example of exact cover in TAOCP Section 7.2.2.1.

**SAT encoding.** Use one Boolean variable $x_{r,c,v}$ for "cell $(r, c)$ holds $v$", $N^3$ variables in all, and set the clue variables true by unit clauses. The *minimal* encoding of Lynce and Ouaknine has, for each cell, the clause "the cell has some symbol" ($N^2$ clauses of length $N$), and, for each unit and symbol, the binary clauses "no two cells of the unit both hold $v$" ($3 N^2 \binom{N}{2}$ clauses). The *extended* encoding adds "the cell has at most one symbol" ($N^2 \binom{N}{2}$ clauses) and "each unit has $v$ somewhere" ($3N^2$ clauses). For $N = 9$ this gives 8,829 and 11,988 clauses before the clues. The formula is small, and a [CDCL](/cdcl/) solver needs very little search on it. Lynce and Ouaknine study which propagation rules, from [unit propagation](/unit-propagation/) to [failed literal probing](/failed-literal-probing/), solve puzzles without branching, and the extended encoding lets the weaker rules do more.

**Counting.** The exact cover search and a [model counter](/model-counting/) both count completions. Large counts, such as the number of all $9 \times 9$ grids, need symmetry and band decomposition as in the example above.

## Bounds

- **NP-completeness.** The decision problem for the family is NP-complete: it is in NP by the certificate above, and it is NP-hard by the reduction below from [Latin square completion](/latin-square-completion/), which Colbourn (1984) proved NP-complete. Yato and Seta (2003) proved the stronger statement that Sudoku is *ASP-complete*: their reductions map solutions to solutions by a polynomial time bijection, so deciding whether a puzzle has a second solution, given one, is also NP-complete.
- **Uniqueness.** Because the another solution problem is NP-complete, testing whether a puzzle is proper is co-NP-hard under polynomial time reductions, so a puzzle setter has no known polynomial time test for the family.
- **Brute force.** The search tree of the backtracking solver has at most $N^e$ leaves for $e$ empty cells, so the worst case time is $O(N^{e} \cdot N^3)$. No polynomial time algorithm for the family is known, and one would give $\mathrm{P} = \mathrm{NP}$.
- **Fixed size.** For $n = 3$ the problem is finite. The facts of interest are the counts and the clue bounds: 17 clues are needed and suffice for a proper puzzle, and every solvable puzzle with 78 or more clues is proper (both in Examples).

## Reductions

**Latin square completion to Sudoku (Yato and Seta).** Let $L$ be a partial Latin square of order $n$ with symbols $0, \ldots, n-1$. Build a Sudoku instance of order $n$, with side $N = n^2$ and 0-based symbols $0, \ldots, N-1$. Let $B = \{(i, kn) : 0 \le i < n, 0 \le k < n\}$, the first column of each box in the top band. Every cell outside $B$ gets the clue

$$S(i, j) = \big((i \bmod n)\, n + \lfloor i/n \rfloor + j\big) \bmod N,$$

and a cell $(i, kn) \in B$ gets the clue $n \cdot L(i, k)$ when $L(i, k)$ is given, and stays empty otherwise.

*Claim.* The completions of the Sudoku instance correspond one to one to the completions of $L$, by $L(i, k) = S'(i, kn)/n$.

*Proof.* Write $c_i = (i \bmod n)\, n + \lfloor i/n \rfloor$. The map $i \mapsto c_i$ swaps the two base-$n$ digits of $i$, so it is a bijection of $\{0, \ldots, N-1\}$, with $c_i \equiv 0 \pmod n$ exactly when $i < n$. Rows: row $i$ holds $(c_i + j) \bmod N$ for all $j$, which is all $N$ symbols. For $i < n$, $c_i = in$, so the cells outside $B$ in row $i$ (those with $j \not\equiv 0$) hold exactly the $N - n$ symbols that are not multiples of $n$. Columns: column $j$ holds $(c_i + j) \bmod N$ for all $i$, all $N$ symbols. For $j = kn$ the cells with $i \ge n$ hold the symbols $\equiv \lfloor i/n \rfloor \not\equiv 0 \pmod n$, again exactly the non-multiples. Boxes: box $(p, q)$ holds $(an + d + p + qn) \bmod N$ for $0 \le a, d < n$, and $an + d$ runs over all symbols, so the box holds all $N$ symbols. In box $(0, q)$ the cells outside $B$ ($d \ne 0$) hold exactly the non-multiples of $n$. So in every completion $S'$, the cells of $B$ in row $i < n$, in column $kn$ and in box $(0, k)$ hold the multiples of $n$, each once. Hence $M(i, k) = S'(i, kn)/n$ has each symbol once in each row and each column: $M$ is a Latin square, and it agrees with $L$ at the given cells. Conversely, for each completion $M$ of $L$, put $n M(i, k)$ in the cells of $B$. Each row, column and box then holds all non-multiples outside $B$ and all multiples inside $B$, so the grid is a completion. The two maps are inverse to each other. $\square$

The instance has $n^4$ cells and is built in polynomial time, and the map between solutions is a bijection, so the reduction is [parsimonious](/parsimonious-reduction/) and carries over the ASP and counting questions. The reduction is a [polynomial time reduction](/polynomial-time-reduction/) of an NP-complete problem to Sudoku, which proves NP-hardness.

**Sudoku to other problems.** Sudoku maps to exact cover and to SAT by the encodings above, and to a CSP with $3N$ all-different constraints. It is also a [list coloring](/list-coloring/) problem: the *Sudoku graph* has the $N^2$ cells as vertices and an edge between two cells of a common unit. Each vertex has $3(N-1) - 2(n-1) = 3N - 2n - 1$ neighbors (20 for the usual grid, because the box shares $n - 1$ cells with the row and $n - 1$ with the column). A completion is a proper [coloring](/graph-coloring/) with $N$ colors that extends the clue colors.

## Applications

- **Benchmarks.** Sudoku of order 3 to 5 and its variants are standard test cases for CSP solvers, SAT encodings, exact cover programs and propagation rules, because the instances are small, the structure is regular and the answers are easy to check.
- **Teaching.** The puzzle shows on one example the CSP model, the effect of the variable order, the power of propagation and the exact cover view.
- **Puzzle generation.** Generators fill a random grid, then remove clues while a solver confirms that the solution stays unique. The difficulty grade is usually the set of human rules (singles, pairs, chains) that a propagation solver needs before it must guess.
- **Design of experiments.** Completed grids with general regions are gerechte designs, which arrange treatments in a field so that each row, column and region gets each treatment once.

## References
