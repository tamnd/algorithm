---
tag: 3F89AQ
kind: problem
slug: exact-cover
name: Exact cover problem
aliases:
- X3C
- exact cover
- exact cover by 3-sets
area: combinatorics/exhaustive-search
level: core
summary: Given a family of subsets of a universe, select subsets that cover every element exactly once.
prereqs: [set-cover, np-complete]
see_also: [algorithm-x, dancing-links, exact-cover-by-3-sets, three-dimensional-matching, set-cover, set-packing, polyomino-tiling-problem, sudoku]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, 85 to 103
    locator: the list of 21 NP-complete problems, with EXACT COVER and its reductions to 3-dimensional matching, hitting set and knapsack
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A3.1, Sets and partitions, problem SP2, exact cover by 3-sets (X3C), NP-complete by a transformation from 3-dimensional matching
  - paper: "Donald E. Knuth, Dancing links, in Millennial Perspectives in Computer Science, Palgrave, 2000, 187 to 214, arXiv:cs/0011047"
    locator: exact cover as a 0/1 matrix, the small example with seven columns, and the pentomino and other tiling examples
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2.1, Dancing links (exact covering with primary and secondary items, Sudoku, Langford pairs and n queens as exact cover problems)
  - paper: "Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 2009, 546 to 563"
    locator: counting the partitions of an n-element set into k members of a given family in time 2^n times a polynomial, by inclusion-exclusion
---

The exact cover problem gives a finite set $U$ and a family $\mathcal{S}$ of subsets of $U$, and asks for a subfamily in which every element of $U$ lies in exactly one chosen set; that is, a partition of $U$ into members of $\mathcal{S}$. Karp listed it among his 21 [NP-complete](/np-complete/) problems in 1972, and it stays NP-complete when every set has three elements ([X3C](/exact-cover-by-3-sets/)). Many puzzles are exact cover problems in disguise, among them [polyomino tilings](/polyomino-tiling-problem/), [Sudoku](/sudoku/) and the [n-queens problem](/n-queens-problem/), so a single solver such as [Algorithm X](/algorithm-x/) handles all of them.

## In plain words

You have a set of things and a collection of groups, where each group holds some of the things. You must pick some groups so that every thing is in exactly one picked group. No thing may be left out, and no thing may be picked twice.

A jigsaw puzzle is a good picture. The things are the squares of the board and the pieces themselves. A group is one way to put one piece on the board: it holds that piece and the squares it covers. A set of groups that covers each square once and uses each piece once is a solution of the puzzle.

The problem is easy to state but can be very hard to solve, because the number of ways to pick groups grows very fast.

## Definition

**Instance.** A finite set $U$ of $n$ elements, the *items*, and a list $\mathcal{S} = (S_1, \ldots, S_m)$ of subsets of $U$, the *options*.

**Solution.** A set $I \subseteq \{1, \ldots, m\}$ of indices such that every $u \in U$ lies in exactly one set $S_j$ with $j \in I$. Equivalently, the sets $S_j$ for $j \in I$ are pairwise disjoint and their union is $U$.

**Matrix form.** Let $A$ be the $m \times n$ matrix with $A_{ju} = 1$ when $u \in S_j$ and $0$ otherwise. A solution is a set of rows whose sum is the all-ones row: a vector $x \in \{0, 1\}^m$ with $x^{\mathsf{T}} A = \mathbf{1}$.

The *decision problem* asks if a solution exists, the *search problem* asks for one, and the *enumeration problem* asks for all of them (see [enumeration problem](/enumeration-problem/)). The counting problem asks for their number. With $s = \sum_j |S_j|$, the size of the input is $\Theta(n + m + s)$.

If $\emptyset \in \mathcal{S}$, it can be added to any solution, so options are usually required to be nonempty. A solution of an instance with $U = \emptyset$ is the empty set of options.

## Variants

- **Exact cover by 3-sets (X3C).** Every option has exactly three elements, and $|U| = 3q$. A solution then has exactly $q$ sets. See [exact cover by 3-sets](/exact-cover-by-3-sets/).
- **Exact cover by 2-sets.** Every option has exactly two elements. The options are the edges of a graph on $U$, and a solution is a perfect matching, which Edmonds' matching algorithm finds in polynomial time.
- **Primary and secondary items.** Primary items must be covered exactly once, and secondary items at most once. This is the form of Knuth's [Algorithm X](/algorithm-x/), and it expresses the diagonals of the [n-queens problem](/n-queens-problem/). It reduces to the basic form by adding, for each secondary item $v$, the option $\{v\}$.
- **Colors and multiplicities.** In *The Art of Computer Programming*, Section 7.2.2.1, a secondary item may be shared by options that give it the same color, and a primary item may have to be covered between $u$ and $v$ times.
- **Exact hitting set.** Choose a set $H$ of elements such that every given set contains exactly one element of $H$. It is exact cover for the transposed matrix: swap the roles of rows and columns.
- **Weighted set partitioning.** Give each option a cost and ask for a solution of least total cost. This is the *set partitioning problem* of integer programming, the form $\min c^{\mathsf{T}} x$ with $x^{\mathsf{T}} A = \mathbf{1}$ and $x \in \{0,1\}^m$.

## Examples

**Knuth's small example.** Let $U = \{A, \ldots, G\}$ and the options be $\{C, E, F\}$, $\{A, D, G\}$, $\{B, C, F\}$, $\{A, D\}$, $\{B, G\}$, $\{D, E, G\}$. The only solution is $\{A, D\}$, $\{B, G\}$, $\{C, E, F\}$. The trace of Algorithm X on this instance is on the [Algorithm X](/algorithm-x/) page.

**A non-example.** For $U = \{1, 2, 3\}$ and options $\{1, 2\}$, $\{2, 3\}$, $\{1, 3\}$ there is no solution: any two options share an element, and one option leaves an element out. The family has a [set cover](/set-cover/) of size two, so the word *exact* matters.

**Pentominoes.** To tile the $6 \times 10$ rectangle with the 12 pentominoes, take 72 items: the 60 cells and the 12 piece names. Each option is one placement of one piece in one of its orientations, and holds the piece name and the 5 cells. There are 2,056 options. The instance has 9,356 solutions, which are 2,339 tilings counted up to the 4 symmetries of the rectangle. The $3 \times 20$ rectangle has 1,236 options and only 8 solutions, that is, 2 tilings up to symmetry.

**Sudoku.** A $9 \times 9$ Sudoku has 324 items: "cell $(r, c)$ is filled", "row $r$ has digit $d$", "column $c$ has digit $d$" and "box $b$ has digit $d$", 81 of each kind. There are $9 \cdot 81 = 729$ options, one for each digit in each cell, and each option holds 4 items. A given clue keeps only one option for its cell. A solution of the exact cover problem is a filled grid.

**Langford pairs.** Arrange two copies of each of $1, \ldots, n$ in a row so that the two copies of $k$ have exactly $k$ numbers between them. The items are the $n$ numbers and the $2n$ positions, and each option places both copies of $k$ at positions $j$ and $j + k + 1$. For $n = 3$ there are 2 solutions, $2\,3\,1\,2\,1\,3$ and its reverse.

**Steiner triple systems.** A Steiner triple system on $v$ points is a set of triples in which each pair of points lies in exactly one triple. Take the pairs as items and every triple as an option that holds its 3 pairs.

## Known algorithms

- **Brute force.** Try all $2^m$ subfamilies, each in $O(s)$ time. This is [brute-force search](/brute-force-search/).
- **Backtracking on an element.** Choose an uncovered element, branch on the options that contain it, remove the conflicting options, and recurse. With the element of fewest options at each step, this is Knuth's [Algorithm X](/algorithm-x/), and with the [dancing links](/dancing-links/) structure each step costs only the options that it removes. It lists all solutions and uses $O(n + s)$ space. It is the method of choice for puzzles in practice.
- **Dynamic programming over subsets of $U$.** Let $f(T)$ be the number of exact covers of $T \subseteq U$ by options inside $T$. With $u = \min T$ for a fixed order of $U$,
  $$f(\emptyset) = 1, \qquad f(T) = \sum_{S \in \mathcal{S},\ u \in S \subseteq T} f(T \setminus S).$$
  The rule counts each solution once, because it fixes the set that covers the least element. With [bit masks](/bitmask-dp/) this takes $O(2^n m)$ time and $O(2^n)$ space, and $f(U)$ is the number of solutions.
- **Inclusion-exclusion.** Björklund, Husfeldt and Koivisto count the partitions with $k$ parts in time $2^n$ times a polynomial and in polynomial space when the family is listed. For $X \subseteq U$, let $a_k(X)$ be the number of ordered $k$-tuples of options inside $X$ whose sizes add up to $n$. Then the number of ordered $k$-tuples that partition $U$ is $\sum_{X \subseteq U} (-1)^{|U \setminus X|} a_k(X)$, and $a_k(X)$ is a coefficient of a power of a polynomial in one variable. Divide by $k!$ and add over $k$ to count the solutions. This is an application of the [inclusion-exclusion principle](/inclusion-exclusion-principle/).
- **Integer programming and SAT.** Solvers for 0/1 integer programs and for [SAT](/sat/) handle large instances with structure, especially in the weighted form.

## Bounds

The decision problem is in [NP](/np/), since a solution is checked in $O(s)$ time, and it is NP-complete. It remains NP-complete for X3C, but with options of size two it is the perfect matching problem and is in P. So the line between easy and hard is at options of size three.

The number of solutions can be very large. If $\mathcal{S}$ is the family of all nonempty subsets of $U$, every partition of $U$ is a solution, and their number is the Bell number $B_n$, which grows faster than any exponential $c^n$. So any algorithm that lists all solutions needs time at least the number of solutions, and an output-sensitive bound is the right goal for listing. No algorithm lists all solutions in time polynomial in the size of the input and the output unless $\mathrm{P} = \mathrm{NP}$, because such an algorithm would decide whether a solution exists, by the argument on the [enumeration problem](/enumeration-problem/) page.

The best general upper bounds are of the form $2^n$ times a polynomial, from the two methods above, and $2^m$ times a polynomial, from brute force. Which is better depends on whether there are more elements or more options.

## Reductions

- **3-dimensional matching to X3C.** A [3-dimensional matching](/three-dimensional-matching/) instance with disjoint sets $X$, $Y$, $Z$ of $q$ elements each and a set of triples is an X3C instance on $U = X \cup Y \cup Z$, with each triple as a 3-set. A perfect matching is then an exact cover. Garey and Johnson list X3C as NP-complete by this transformation.
- **Exact cover in Karp's tree.** Karp reduced the chromatic number problem to exact cover, and exact cover to 3-dimensional matching, to [hitting set](/hitting-set/) and to [knapsack](/knapsack-problem/).
- **Exact cover to SAT.** Take one Boolean variable $x_j$ for each option. For each element $u$, let $J_u$ be the indices of the options that contain $u$, add the clause $\bigvee_{j \in J_u} x_j$, and for each pair $j < k$ in $J_u$ add $\neg x_j \vee \neg x_k$. The satisfying assignments are exactly the solutions, so the reduction keeps the number of solutions.
- **Puzzles to exact cover.** Tiling, Sudoku, Langford pairs and n queens reduce to exact cover by the constructions in the examples. This is why a fast exact cover solver is a general puzzle solver.

## Applications

- **Puzzles and recreational mathematics.** Polyomino and polycube tilings, Sudoku and its variants, and word puzzles, by Algorithm X and its extensions.
- **Combinatorial designs.** Steiner systems, Latin squares and similar designs are exact covers of pairs or of cells.
- **Scheduling.** In the weighted set partitioning form, each option is a feasible schedule for one worker or one vehicle, and each element is a task that must be done exactly once, as in airline crew scheduling.
- **Proofs of NP-hardness.** X3C is a common starting point for reductions, because its structure is simple and rigid.

## References
