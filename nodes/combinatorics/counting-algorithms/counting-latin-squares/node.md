---
tag: B65PF7
kind: problem
slug: counting-latin-squares
name: Counting Latin squares
aliases:
- number of Latin squares
- counting reduced Latin squares
area: combinatorics/counting-algorithms
level: research
summary: Counts n×n arrays in which each symbol appears once per row and column.
prereqs: [permutation-cycles, derangement, perfect-matching, rule-of-product]
see_also: [latin-square-completion, permanent-computation, counting-perfect-matchings, edge-coloring, sudoku, dancing-links, exact-cover, birkhoff-von-neumann-decomposition]
sources:
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: Chapter 17, Latin squares (the bounds on the number of Latin squares); Chapter 11, Permanents (Bregman's bound); Chapter 12, The Van der Waerden conjecture
  - paper: doi:10.1007/s00026-005-0261-7
    title: Brendan D. McKay and Ian M. Wanless, On the number of Latin squares, Annals of Combinatorics 9(3), 335 to 344, 2005
    locator: the count of Latin squares of order 11 and the method of counting by classes of partial squares
  - paper: doi:10.1090/S0025-5718-2010-02420-2
    title: Alexander Hulpke, Petteri Kaski and Patric R. J. Östergård, The number of Latin squares of order 11, Mathematics of Computation 80(274), 1197 to 1219, 2011
    locator: the counts of the equivalence classes of Latin squares of order 11
  - url: https://oeis.org/A002860
    title: OEIS A002860, Number of Latin squares of order n; or labeled quasigroups
    locator: the data and the formula with A000315
---

Counting Latin squares asks for the number $L_n$ of $n \times n$ arrays with entries in $\{1, \ldots, n\}$ in which each symbol appears exactly once in each row and once in each column. No formula and no polynomial-time algorithm in $n$ is known. The exact values are known only up to $n = 11$, from large computer searches that use the symmetry of the problem. Building a square one row at a time, each new row is a [perfect matching](/perfect-matching/) between columns and unused symbols, so the number of choices is a [permanent](/permanent-computation/). The bounds on permanents of Van der Waerden and Bregman then pin down the growth: $L_n^{1/n^2} = (1 + o(1))\, n / e^2$.

## In plain words

Fill a square grid with numbers so that each row and each column holds each number exactly once. How many ways are there to do this?

For small grids you can try every way. For larger grids the count explodes, and no one knows a short formula. A useful trick is to fill the grid one row at a time. Each new row must avoid, in each column, the numbers already used there. The number of ways to choose the next row is a well-studied quantity, and good upper and lower limits for it are known. Multiplying these limits row by row gives limits for the whole count that agree closely as the grid grows. The exact counts for grids of up to eleven rows came from long computer runs that group similar partial grids and count each group once.

## Definition

Notation: $[n] = \{1, \ldots, n\}$, $D_n$ is the number of [derangements](/derangement/) of $[n]$.

A *Latin square* of order $n$ is a map $A : [n] \times [n] \to [n]$ such that each row $A(i, \cdot)$ and each column $A(\cdot, j)$ is a permutation of $[n]$. A *$k \times n$ Latin rectangle* is the same with $k \le n$ rows. A Latin square is *reduced* (or normalized) if its first row and its first column are $1, 2, \ldots, n$ in order.

**Problem.** Input: $n$. Output: $L_n$, the number of Latin squares of order $n$. A common variant asks for $R_n$, the number of reduced squares, or for the number of completions of a given partial square.

**Lemma 1.** $L_n = n! \, (n-1)! \, R_n$.

*Proof.* Permuting the columns of a Latin square gives a Latin square, and permuting the rows $2, \ldots, n$ does too. Given any Latin square, there is exactly one column permutation that puts its first row in the order $1, \ldots, n$, and then exactly one permutation of rows $2, \ldots, n$ that puts its first column in order (the first column of a square with first row $1, \ldots, n$ starts with 1 and has distinct entries). So the group of these $n! \, (n-1)!$ operations acts freely on Latin squares, and each orbit contains exactly one reduced square. $\square$

**Lemma 2 (row by row).** Let $P$ be a $k \times n$ Latin rectangle with $k < n$. Let $M$ be the $n \times n$ 0-1 matrix with $M_{js} = 1$ when symbol $s$ does not appear in column $j$ of $P$. Then the number of ways to add a row $k + 1$ is $\operatorname{per}(M)$, and every row and column of $M$ has exactly $n - k$ ones.

*Proof.* A new row is a permutation $\pi$ of $[n]$ (column $j$ gets symbol $\pi(j)$) with $M_{j \pi(j)} = 1$ for all $j$, and the [permanent](/permanent-computation/) of a 0-1 matrix counts exactly these permutations. Column $j$ of $P$ uses $k$ distinct symbols, so row $j$ of $M$ has $n - k$ ones; each symbol appears once in each of the $k$ rows of $P$, in $k$ distinct columns, so column $s$ of $M$ has $n - k$ ones. $\square$

## Variants

- **Reduced squares.** $R_n$, which is $L_n / (n! \, (n-1)!)$ by Lemma 1.
- **Latin rectangles.** The number of $k \times n$ Latin rectangles. For $k = 2$ it is $n! \, D_n$, since the second row is a derangement relative to the first.
- **Completions.** Given a partial Latin square, count its completions. Deciding whether one completion exists is already NP-complete, by Colbourn's theorem; see [Latin square completion](/latin-square-completion/). So this counting problem is NP-hard. [Sudoku](/sudoku/) puzzles add box constraints to the same problem.
- **Equivalence classes.** Count the squares up to isotopy (permuting rows, columns and symbols), or up to main class (also permuting the three roles), or the isomorphism classes of quasigroups. These counts use [Burnside's lemma](/burnside-lemma/) over the symmetry group.
- **Edge colorings.** A Latin square of order $n$ is the same as a proper [edge coloring](/edge-coloring/) of the complete bipartite graph $K_{n,n}$ with $n$ colors: color the edge from row $i$ to column $j$ with $A(i, j)$.

## Examples

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $R_n$ (A000315) | 1 | 1 | 1 | 4 | 56 | 9408 | 16942080 | 535281401856 |
| $L_n$ (A002860) | 1 | 2 | 12 | 576 | 161280 | 812851200 | 61479419904000 | 108776032459082956800 |

The known values continue with $R_9 = 377597570964258816$, $R_{10} = 7580721483160132811489280$ and $R_{11} = 5363937773277371298119673540771840$. The value for $n = 12$ is not known.

**The case $n = 3$.** The first row has $3! = 6$ choices. The second row must be a derangement relative to the first, $D_3 = 2$ choices, and then the third row is forced. So $L_3 = 6 \cdot 2 \cdot 1 = 12$, and $R_3 = 12 / (3! \, 2!) = 1$.

**The case $n = 4$.** Fix the first row as $1, 2, 3, 4$ (24 choices in all). The second row is one of the $D_4 = 9$ derangements. By Lemma 2, the third row is a perfect matching in a 2-regular bipartite graph, which is a union of even cycles, so it has $2^{c}$ choices where $c$ is the number of cycles. If the second row differs from the first by a 4-cycle (6 cases), there is one cycle and 2 choices. If it differs by two transpositions (3 cases), there are two cycles and 4 choices. The last row is forced. So $L_4 = 24 \cdot (6 \cdot 2 + 3 \cdot 4) = 24 \cdot 24 = 576$.

## Known algorithms

- **Backtracking.** Fill the cells in order, keeping a bit mask of the symbols used in each row and column, and count the leaves. Fixing the first row and column (Lemma 1) divides the work by $n! \, (n-1)!$. The run time is proportional to the number of partial reduced squares, so this is practical up to about $n = 7$. Formulating the square as an [exact cover](/exact-cover/) problem and using [dancing links](/dancing-links/) is the same method with a better choice of the next cell.
- **Row by row with permanents.** By Lemma 2, the count of completions of a $k$-row rectangle by one row is a permanent of a 0-1 matrix, which can be computed by [Ryser's formula](/ryser-formula/). This alone does not reduce the work, because the number of rectangles is large.
- **Counting by classes.** The record computations split the square into a top part and a bottom part. They group the partial rectangles into classes under the symmetries that act on them (rows, columns and symbols), compute the number of completions for one representative of each class, and add these numbers weighted by the class sizes. McKay and Rogoyski computed $L_{10}$ this way in 1995, and McKay and Wanless computed $L_{11}$ in 2005.
- **Approximation.** Monte Carlo estimates by sequential importance sampling, choosing one row or one cell at a time and weighting by the number of choices, give estimates of $L_n$ for $n$ beyond the exact range, without proven error bounds.

## Bounds

For every $n \ge 1$,

$$\frac{(n!)^{2n}}{n^{n^2}} \;\le\; L_n \;\le\; \prod_{k=1}^{n} (k!)^{n/k}.$$

*Proof.* Build the square row by row. When $n - k$ rows are left to place, Lemma 2 says the next row has $\operatorname{per}(M)$ choices, where $M$ is a 0-1 matrix with all row and column sums equal to $k$. The matrix $M / k$ is doubly stochastic, so by the Van der Waerden bound (proved by Egorychev and by Falikman), $\operatorname{per}(M) = k^n \operatorname{per}(M / k) \ge k^n \, n! / n^n$. By Bregman's theorem, $\operatorname{per}(M) \le \prod_{\text{rows}} (k!)^{1/k} = (k!)^{n/k}$. Multiply over $k = n, n - 1, \ldots, 1$: the lower bounds give $(n!)^n \cdot (n!)^n / n^{n^2}$, and the upper bounds give the product on the right. $\square$

Taking logarithms with Stirling's formula, both sides are $n^2 (\ln n - 2) + O(n \ln^2 n)$, so

$$L_n = \left( (1 + o(1)) \frac{n}{e^2} \right)^{n^2}.$$

For $n = 10$ the bounds are about $1.6 \cdot 10^{31} \le L_{10} \le 1.8 \cdot 10^{40}$, while $L_{10} \approx 1.0 \cdot 10^{37}$.

## Reductions

- **To permanents.** By Lemma 2, counting one-row extensions is the permanent of a regular 0-1 matrix, which is the count of perfect matchings of a regular bipartite graph; see [counting perfect matchings](/counting-perfect-matchings/).
- **To exact cover.** A Latin square is an exact cover of the $3n^2$ constraints (row and column, row and symbol, column and symbol) by $n^3$ candidate triples, so exact cover counters apply.
- **From completion.** Counting completions of partial squares is at least as hard as deciding completability, which is NP-complete.

## Applications

- Design of experiments: Latin squares are the classic designs that balance two nuisance factors, and their counts give the size of the space from which a design is drawn at random.
- Error-correcting codes and cryptography, where Latin squares and quasigroups give codes and simple ciphers.
- Benchmarks for exact counting and for approximate counting by sampling, because the true values are known up to $n = 11$.

## References
