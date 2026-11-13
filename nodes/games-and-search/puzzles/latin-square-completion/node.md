---
tag: 5D4CRB
kind: problem
slug: latin-square-completion
name: Latin square completion
aliases:
- Latin square completion problem
area: games-and-search/puzzles
level: advanced
summary: Decide whether a partial Latin square can be filled to a full one. NP-complete in general (Colbourn 1984); always possible for full rows (Hall) and for at most n - 1 filled cells (Evans).
prereqs: [hall-theorem, bipartite-matching, np-complete]
see_also: [sudoku, counting-latin-squares, edge-coloring, all-different-constraint, perfect-matching, kuhn-algorithm, three-dimensional-matching, exact-cover]
sources:
  - paper: doi:10.1016/0166-218X(84)90075-1
    title: Charles J. Colbourn, The complexity of completing partial Latin squares, Discrete Applied Mathematics 8(1), 1984, 25 to 30
    locator: the main theorem, NP-completeness by a reduction from partitioning a tripartite graph into triangles
  - paper: doi:10.1090/S0002-9904-1945-08361-X
    title: Marshall Hall, An existence theorem for Latin squares, Bulletin of the American Mathematical Society 51(6), 1945, 387 to 388
    locator: the theorem that every k by n Latin rectangle extends to a Latin square
  - paper: "Herbert J. Ryser, A combinatorial theorem with an application to Latin rectangles, Proceedings of the American Mathematical Society 2, 1951"
    locator: the condition for completing an r by s Latin rectangle
  - paper: "Trevor Evans, Embedding incomplete Latin squares, American Mathematical Monthly 67, 1960"
    locator: the conjecture on partial Latin squares with at most n - 1 filled cells
  - paper: "Bohdan Smetaniuk, A new construction for Latin squares I. Proof of the Evans conjecture, Ars Combinatoria 11, 1981, 155 to 172"
    locator: the proof of the Evans conjecture
  - paper: doi:10.1112/plms/s3-47.3.507
    title: Lars Døvling Andersen and Anthony J. W. Hilton, Thank Evans!, Proceedings of the London Mathematical Society (3) 47(3), 1983, 507 to 522
    locator: an independent proof of the Evans conjecture, and the partial squares with n filled cells that cannot be completed
  - paper: "Carla P. Gomes and Bart Selman, Problem structure in the presence of perturbations, Proceedings of the Fourteenth National Conference on Artificial Intelligence (AAAI-97), 1997, 221 to 226"
    locator: the quasigroup completion problem as a benchmark for constraint solvers
  - paper: "Takayuki Yato and Takahiro Seta, Complexity and completeness of finding another solution and its application to puzzles, IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences E86-A(5), 2003, 1052 to 1060"
    locator: the ASP-completeness of Latin square completion, used for Number Place
---

Latin square completion asks whether a partial Latin square of order $n$, an $n \times n$ array with some cells filled so that no symbol repeats in a row or a column, can be filled to a full Latin square. Colbourn (1984) proved the problem [NP-complete](/np-complete/). Two special cases are always solvable: when the filled cells are complete rows (Marshall Hall 1945, by [bipartite matching](/bipartite-matching/)), and when at most $n - 1$ cells are filled (the Evans conjecture, proved by Smetaniuk in 1981 and by Andersen and Hilton in 1983). In the constraint programming literature the same problem is the quasigroup completion problem, a standard benchmark.

## In plain words

A Latin square is a square table of symbols in which each row and each column holds each symbol once, like a Sudoku without the boxes. Some cells of the table are filled in, and no symbol repeats so far. Can you fill the rest?

If the filled cells are whole rows at the top, the answer is always yes, and a matching method fills one more row at a time. If only a few cells are filled, fewer than the number of rows, the answer is again always yes, but the proof is much harder. In general the answer depends on the pattern, and the problem is as hard as any puzzle whose answers are easy to check. No fast method is known for all inputs.

## Definition

Let $[n] = \{0, \ldots, n-1\}$. A *partial Latin square* of order $n$ is a map $P$ from a set $F \subseteq [n] \times [n]$ of *filled cells* to $[n]$ such that $P(r, c) \ne P(r, c')$ for $c \ne c'$ and $P(r, c) \ne P(r', c)$ for $r \ne r'$, whenever both cells are filled. A *completion* of $P$ is a Latin square $L$ of order $n$ (each row and each column a permutation of $[n]$) with $L = P$ on $F$.

- **Decision (PLSC).** Input: $n$ and $P$. Question: does $P$ have a completion?
- **Search.** Output a completion or report that none exists.
- **Counting.** Output the number of completions; see [counting Latin squares](/counting-latin-squares/).

The input is $n$ and the list of $|F| \le n^2$ filled cells, each in $O(\log n)$ bits. A completion has $n^2$ entries and is checked in $O(n^2)$ time, so the problem is in [NP](/np/).

**The triangle view.** Let $K_{n,n,n}$ be the complete tripartite graph on row vertices, column vertices and symbol vertices. An entry $L(r, c) = s$ is the triangle $\{r, c, s\}$. Two entries of a Latin square never share two coordinates, so their triangles share no edge, and a Latin square is exactly a partition of the $3n^2$ edges of $K_{n,n,n}$ into $n^2$ triangles. A partial square is a set of edge-disjoint triangles, and completing it means partitioning the remaining edges into triangles. This view shows that rows, columns and symbols play the same role: permuting the three coordinates of every entry (taking a *conjugate*) maps partial squares to partial squares and completions to completions.

**Rectangles.** A $k \times n$ *Latin rectangle* is a partial square whose filled cells are the first $k$ rows. An $r \times s$ Latin rectangle on $n$ symbols fills the top left $r \times s$ block.

## Variants

- **Quasigroup completion.** The same problem in the language of algebra: a Latin square is the multiplication table of a finite quasigroup. Gomes and Selman (1997) proposed random instances of it as a benchmark with a controllable structure.
- **Quasigroup with holes.** Start from a full Latin square and erase cells. Every instance then has a solution, which makes the benchmark useful for incomplete solvers.
- **Sudoku.** Adding the box rule gives [Sudoku](/sudoku/), and Latin square completion reduces to it.
- **Precoloring extension.** A Latin square of order $n$ is a proper [edge coloring](/edge-coloring/) of $K_{n,n}$ with $n$ colors (color the edge from row $r$ to column $c$ with $L(r, c)$). Completion is the extension of a partial edge coloring.
- **Unique completion.** A partial square whose completion is unique and that loses this property when any filled cell is removed is a *critical set*. The smallest critical sets are studied in design theory.

## Examples

**Hall extension, $n = 4$.** Take the $2 \times 4$ rectangle with rows $0\,1\,2\,3$ and $1\,0\,3\,2$. Column 0 misses the symbols $\{2, 3\}$, column 1 misses $\{2, 3\}$, column 2 misses $\{0, 1\}$ and column 3 misses $\{0, 1\}$. The graph of columns and missing symbols is 2-regular, a union of two 4-cycles, so it has $2 \cdot 2 = 4$ perfect matchings, and each one gives a valid third row, for example $2\,3\,0\,1$. The fourth row is then forced. So this rectangle has exactly 4 completions. The rectangle with rows $0\,1\,2\,3$ and $1\,2\,3\,0$ has a graph that is one 8-cycle, with 2 perfect matchings, and so 2 completions.

**$n$ filled cells can block completion.** For $n = 4$, fill row 0 with $0, 1, 2$ in columns 0 to 2, and put symbol 3 in cell $(1, 3)$:

```
0 1 2 .
. . . 3
. . . .
. . . .
```

Cell $(0, 3)$ must hold the only symbol missing from row 0, which is 3, but column 3 already has a 3. The same pattern works for every $n \ge 2$: symbols $0, \ldots, n-2$ in row 0 and symbol $n-1$ at $(1, n-1)$. So the Evans bound $n - 1$ is tight.

**Counts of squares.** The numbers of Latin squares of orders 1 to 4 are 1, 2, 12 and 576. Completing the empty square is always possible (the cyclic square $L(r, c) = (r + c) \bmod n$ is one completion), so the hard instances are partly filled.

## Known algorithms

**Hall's row by row extension.** This algorithm is polynomial for the case where the filled cells are $k$ complete rows.

```pseudo id=main
HALL-EXTEND(P)                       ▷ P is a k × n Latin rectangle
L1  while P has fewer than n rows do
L2      H ← bipartite graph with an edge (j, s) when symbol s is not in column j of P
L3      m ← a perfect matching of H
L4      append the row (m(0), m(1), ..., m(n-1)) to P
L5  return P
```

*Proof that line L3 always succeeds (Hall 1945).* Suppose $P$ has $k < n$ rows. Column $j$ holds $k$ different symbols, so it has $n - k$ edges in $H$. Symbol $s$ appears once in each row, in $k$ different columns, so it is missing from $n - k$ columns and also has degree $n - k$. Thus $H$ is $(n - k)$-regular with $n - k \ge 1$. For any set $X$ of columns, the $(n-k)|X|$ edges leaving $X$ end in $N(X)$, and each vertex of $N(X)$ takes at most $n - k$ of them, so $|N(X)| \ge |X|$. By [Hall's theorem](/hall-theorem/), $H$ has a perfect matching $m$. The new row $m(0), \ldots, m(n-1)$ is a permutation because $m$ is a matching, and no column repeats a symbol because $m(j)$ is missing from column $j$. So the result is a $(k+1) \times n$ Latin rectangle, and induction on $k$ completes the proof. $\square$

With augmenting paths ([Kuhn's algorithm](/kuhn-algorithm/)), each matching costs $O(n \cdot n^2) = O(n^3)$ time on a graph with $n(n-k)$ edges, so the extension costs $O(n^4)$ in all. [Hopcroft-Karp](/hopcroft-karp/) lowers each matching to $O(n^{2.5})$.

**Backtracking for the general case.** Model each empty cell as a variable with domain $[n]$, and each row and column as an [all-different constraint](/all-different-constraint/), $2n$ constraints in all. Fill the cell with the fewest candidates first ([minimum remaining values](/minimum-remaining-values/)) and keep bit masks of the used symbols. Filtering each all-different constraint by matching makes the search much smaller on hard instances. The same problem is an [exact cover](/exact-cover/) instance with $3n^2$ items ("cell $(r, c)$ filled", "row $r$ has $s$", "column $c$ has $s$") and $n^3$ options of three items each; in the triangle view the options are the triangles of $K_{n,n,n}$ and the items are its edges. A SAT encoding uses the $n^3$ variables $x_{r,c,s}$ with the cell, row and column constraints.

## Bounds

| Case | Result | Who |
|---|---|---|
| General partial square | NP-complete | Colbourn 1984 |
| Another solution, given one | NP-complete (ASP-complete) | Yato and Seta 2003 |
| $k$ full rows | always completable, $O(n^4)$ | Hall 1945 |
| $r \times s$ block on $n$ symbols | completable iff each symbol occurs at least $r + s - n$ times | Ryser 1951 |
| at most $n - 1$ filled cells | always completable | Smetaniuk 1981; Andersen and Hilton 1983 |
| $n$ filled cells | can fail (example above) | |

**Ryser's condition.** The necessity part is short. In a completion, a symbol $x$ occurs once in each of the first $r$ rows. The cells of these rows outside the block lie in the $n - s$ columns outside the block, and each such column holds $x$ at most once. So at most $n - s$ of the $r$ occurrences lie outside the block, and at least $r - (n - s) = r + s - n$ lie inside it. Ryser proved that this condition is also sufficient, so an $r \times s$ block is tested in $O(rs + n)$ time.

**NP-hardness.** Colbourn's reduction starts from the problem of partitioning the edges of a tripartite graph into triangles. By the triangle view, a completion of a partial square is a triangle partition of the edges of $K_{n,n,n}$ that its filled cells leave uncovered. Colbourn embeds a given tripartite graph into such a leftover graph, filling the rest with Latin rectangles in the manner of the Hall and Ryser theorems, so that the graph has a triangle partition exactly when the partial square has a completion. The general problem is therefore hard even though the row-only and block-only cases are easy.

## Reductions

- **From triangle partition (Colbourn).** As above, partitioning the edges of a tripartite graph into triangles reduces to completion. The triangles of a tripartite graph are triples with one row, one column and one symbol, as in [three-dimensional matching](/three-dimensional-matching/), but here every edge, not every vertex, must be covered once.
- **To Sudoku.** Yato and Seta map a partial Latin square of order $n$ to a Sudoku of side $n^2$ with the same completions; the construction and its proof are on the [Sudoku page](/sudoku/).
- **To exact cover and SAT.** By the encodings in Known algorithms.
- **To edge coloring extension.** By the edge coloring view of $K_{n,n}$.

## Applications

- **Benchmarks.** Quasigroup completion and quasigroups with holes are standard test sets for CSP and SAT solvers, because their structure is regular and they are easy to generate in any size and density. Random instances with very few or very many filled cells are easy, and the hard ones lie at an intermediate density.
- **Scheduling.** A timetable in which each class meets each teacher once and each teacher has one class in each period is a Latin square (rows are classes, columns are periods, symbols are teachers), and fixed meetings are filled cells.
- **Design of experiments.** Latin squares arrange treatments in rows and columns so that each treatment meets each row and each column once; completion extends a partial design.

## References
