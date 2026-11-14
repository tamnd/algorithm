---
tag: 09FYV2
kind: data-structure
slug: determinant-decision-diagram
name: Determinant decision diagram
aliases:
- DDD
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Shi and Tan's BDD-like canonical graph of the symbolic determinant of a circuit matrix, which shares subexpressions so exact symbolic analysis scales to large circuits.
model: word-ram
complexity:
  vars: {n: the order of the matrix, M: the number of distinct minors that BUILD reaches, V: the number of DDD vertices, T: the number of nonzero terms of the determinant}
  time: {build: O(n M) expected, evaluate: O(V), count_terms: O(V), list_terms: "O(n T + V)"}
  space: {vertices: O(n M)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1997
  people: [C.-J. Richard Shi, Xiang-Dong Tan]
  note: Shi and Tan gave determinant decision diagrams at ICCAD 1997, with the journal version in IEEE TCAD in 2000. In 2001 they extended them to network functions expanded in powers of the frequency variable.
prereqs: [determinant, laplace-expansion, zero-suppressed-bdd, symbolic-circuit-analysis]
see_also: [binary-decision-diagram, reduced-ordered-bdd, hash-consing, memoization, cramers-rule, modified-nodal-analysis, approximate-symbolic-analysis, variable-ordering]
sources:
  - paper: "C.-J. Richard Shi and Xiang-Dong Tan, Canonical symbolic analysis of large analog circuits with determinant decision diagrams, IEEE Transactions on Computer-Aided Design 19(1), 1 to 18, 2000"
    title: C.-J. R. Shi and X.-D. Tan, Canonical symbolic analysis of large analog circuits with determinant decision diagrams, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 19(1), 1 to 18, January 2000
    locator: the definition of the DDD (a signed vertex per matrix entry with a 1-edge and a 0-edge), its relation to zero-suppressed BDDs, its canonical form under a fixed order, its construction by Laplace expansion, and the vertex ordering
  - paper: "C.-J. Richard Shi and Xiang-Dong Tan, Symbolic analysis of large analog circuits with determinant decision diagrams, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 366 to 373, 1997"
    title: C.-J. R. Shi and X.-D. Tan, Symbolic analysis of large analog circuits with determinant decision diagrams, ICCAD 1997, pages 366 to 373
    locator: the conference version
  - paper: doi:10.1109/43.930996
    title: C.-J. R. Shi and X.-D. Tan, Compact representation and efficient generation of s-expanded symbolic network functions for computer-aided analog circuit design, IEEE Transactions on Computer-Aided Design 20(7), 813 to 827, 2001
    locator: multiroot DDDs for the coefficients of each power of s of a network function
  - paper: "Shin-ichi Minato, Zero-suppressed BDDs for set manipulation in combinatorial problems, Proceedings of the 30th Design Automation Conference, 272 to 277, 1993"
    title: S. Minato, Zero-suppressed BDDs for set manipulation in combinatorial problems, DAC 1993, pages 272 to 277
    locator: the zero-suppression rule and the canonical form of a family of sets
  - paper: "Xiang-Dong Tan and C.-J. Richard Shi, Hierarchical symbolic analysis of analog integrated circuits via determinant decision diagrams, IEEE Transactions on Computer-Aided Design 19(4), 401 to 412, 2000"
    title: X.-D. Tan and C.-J. R. Shi, Hierarchical symbolic analysis of analog integrated circuits via determinant decision diagrams, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 19(4), 401 to 412, April 2000
    locator: the analysis of a circuit split into blocks, with one DDD for each block
---

A determinant decision diagram, or DDD, is a [directed acyclic graph](/directed-acyclic-graph/) that holds the [determinant](/determinant/) of a sparse matrix with symbolic entries, one vertex for each entry in each minor that it appears in, and one path for each term. It is a [zero-suppressed BDD](/zero-suppressed-bdd/) of the set of terms, with a sign on each vertex. Its topic is symbolic circuit analysis: the matrix comes from [modified nodal analysis](/modified-nodal-analysis/) of a small-signal circuit, and the determinant and its cofactors give the network functions of [symbolic circuit analysis](/symbolic-circuit-analysis/). A DDD can have far fewer vertices than the determinant has terms, so a computer can store, evaluate and count an exact expression whose expanded form does not fit in memory.

## In plain words

The determinant of a matrix, written out in full, is a long sum of products. Each product takes one entry from each row, and no two entries from the same column. For a circuit, these sums grow so fast that a printed formula becomes useless after a few dozen nodes.

Many products share their tails. After you choose the entries of the first rows, the rest of the product only depends on which columns are still free. A DDD stores each such tail one time, and every product that ends with it points to it. Each node of the graph asks one question: do we use this entry or not? Follow the yes and no arrows from the top to the end marked one, and you read one product. The graph can be small when the list of products is huge.

## The abstract type

The input is an $n \times n$ matrix $A$ whose nonzero entries are distinct symbols. The DDD represents the polynomial $\det A$ in these symbols, and the set of its nonzero terms. It has these operations:

- BUILD$(A)$: make the DDD of $\det A$.
- EVALUATE$(x)$: the value of $\det A$ when each symbol has a number.
- COUNT-TERMS: the number of nonzero terms of $\det A$.
- TERMS: list the terms, each with its sign.
- SIZE: the number of vertices.

A network function of a linear circuit is a ratio of a cofactor and the determinant, by [Cramer's rule](/cramers-rule/). A cofactor is the determinant of a submatrix, so the same structure holds it. The DDDs of the determinant and of its cofactors can share one table of vertices, with one root for each.

## Representation

There are two terminal vertices, $0$ and $1$. Each inner vertex $v$ has five fields:

- an entry $(r, c)$ of $A$ and its symbol $a_v = A[r, c]$,
- a sign $s_v \in \{+1, -1\}$,
- a hi child (the 1-edge): the DDD of the minor without row $r$ and column $c$,
- a lo child (the 0-edge): the DDD of the rest of the expansion of row $r$.

The value of a vertex is

$$D(0) = 0, \qquad D(1) = 1, \qquad D(v) = s_v \, a_v \, D(\mathrm{hi}(v)) + D(\mathrm{lo}(v)).$$

A 1-path goes from the root to the terminal $1$. Its term is the product of the symbols and signs of the vertices that it leaves by a hi edge. The value of the root is the sum of the terms of all 1-paths.

Two rules keep the graph small and canonical, as in a [reduced ordered BDD](/reduced-ordered-bdd/):

- **Zero suppression.** A vertex whose hi child is $0$ adds nothing. It is never made, and its lo child takes its place.
- **Unique table.** A hash table on (row, column, sign, hi, lo) returns the old vertex when the same vertex is asked for again. This is [hash consing](/hash-consing/).

The entries are ordered row by row, and in each row by column. Each vertex comes before all vertices below it in this order. Shi and Tan allow other orders of the entries and choose one with a heuristic, because the size depends on the order, as for a BDD and its [variable ordering](/variable-ordering/).

## Operations

BUILD makes the DDD by [Laplace expansion](/laplace-expansion/) along the first row of each minor, with [memoization](/memoization/) on the minor. A minor is fixed by its set $C$ of columns: its rows are the last $|C|$ rows. Laplace expansion along its first row $r$ is

$$\det A_C = \sum_{c \in C,\ A[r,c] \neq 0} (-1)^{|\{c' \in C \,:\, c' < c\}|} \, A[r, c] \, \det A_{C \setminus \{c\}}.$$

CHAIN$(C, k)$ is the part of this sum with the $k$-th to the last nonzero column of row $r$.

```pseudo id=main
BUILD(A)                                   ▷ A is n × n
L1  return MINOR({0, …, n − 1})

MINOR(C)                                   ▷ rows n − |C| .. n − 1, columns C; memoized on C
L2  if C = ∅ then return the terminal 1
L3  r ← n − |C|
L4  c_1 < … < c_m ← the columns c ∈ C with A[r, c] ≠ 0
L5  return CHAIN(C, 1)

CHAIN(C, k)                                ▷ memoized on (C, k)
L6  if k > m then return the terminal 0
L7  c ← c_k, s ← (−1)^|{c' ∈ C : c' < c}|
L8  h ← MINOR(C \ {c})
L9  l ← CHAIN(C, k + 1)
L10 if h = 0 then return l                 ▷ zero suppression
L11 return UNIQUE(r, c, s, h, l)           ▷ an old vertex with these fields, or a new one
```

EVALUATE computes $D$ for every vertex in one pass from the terminals up, with the numbers in place of the symbols. COUNT-TERMS computes the number of 1-paths with $P(0) = 0$, $P(1) = 1$ and $P(v) = P(\mathrm{hi}(v)) + P(\mathrm{lo}(v))$, in one pass. TERMS walks all 1-paths. In the implementation, a vertex is made after its two children, so the index order is a valid bottom-up order.

## Example

Take the $4 \times 4$ tridiagonal matrix

$$A = \begin{pmatrix} a & b & 0 & 0 \\ c & d & e & 0 \\ 0 & f & g & h \\ 0 & 0 & i & j \end{pmatrix}.$$

BUILD makes 10 inner vertices, one for each nonzero entry:

| vertex | entry | sign | hi | lo |
|---|---|---|---|---|
| $a$ | (0, 0) | + | $d$ | $b$ |
| $b$ | (0, 1) | − | $c$ | 0 |
| $c$ | (1, 0) | + | $g$ | 0 |
| $d$ | (1, 1) | + | $g$ | $e$ |
| $e$ | (1, 2) | − | $f$ | 0 |
| $f$ | (2, 1) | + | $j$ | 0 |
| $g$ | (2, 2) | + | $j$ | $h$ |
| $h$ | (2, 3) | − | $i$ | 0 |
| $i$ | (3, 2) | + | 1 | 0 |
| $j$ | (3, 3) | + | 1 | 0 |

The vertices $c$ and $d$ share the hi child $g$, which is the DDD of the minor with rows 2, 3 and columns 2, 3. After $b$ takes column 1, the minor has rows 1 to 3 and columns 0, 2 and 3. In its row 1, the entry $e$ leads to a minor with no terms, because then no row is left that has an entry in column 0. Zero suppression drops this vertex, so the lo child of $c$ is 0. The five 1-paths give

$$\det A = adgj - adhi - aefj - bcgj + bchi.$$

The path counts are $P(i) = P(j) = P(h) = P(f) = P(e) = 1$, $P(g) = 2$, $P(c) = P(b) = 2$, $P(d) = 3$ and $P(a) = 5$. With $a, b, \ldots, j = 1, 2, \ldots, 10$, EVALUATE gives $D(h) = -72$, $D(g) = 70 - 72 = -2$, $D(f) = 60$, $D(e) = -300$, $D(d) = -8 - 300 = -308$, $D(c) = -6$, $D(b) = 12$ and $D(a) = -308 + 12 = -296$. The five terms give $280 - 288 - 300 - 420 + 432 = -296$, the same value.

Larger cases show the gap between terms and vertices:

| matrix | order $n$ | terms | DDD vertices |
|---|---|---|---|
| tridiagonal | 10 | 89 | 28 |
| tridiagonal | 30 | 1,346,269 | 88 |
| dense | 6 | 720 | 192 |
| dense | 8 | 40,320 | 1,024 |

A tridiagonal matrix of order $n$ has $F_{n+1}$ terms, a [Fibonacci number](/fibonacci-numbers/), and its DDD in this order has $3n - 2$ vertices. The reason: the minors that BUILD reaches at row $r$ have the columns $\{r, \ldots, n-1\}$, which gives the vertices of the entries $(r, r)$ and $(r, r+1)$, or the columns $\{r-1, r+1, \ldots, n-1\}$, where only the entry $(r, r-1)$ leads to a nonzero minor. So each nonzero entry has exactly one vertex. A dense matrix has $n!$ terms and $n \, 2^{n-1}$ vertices: each nonempty column set $C$ is reached, and it gives one vertex for each of its $|C|$ columns, so the count is $\sum_k k \binom{n}{k} = n \, 2^{n-1}$.

## Correctness

BUILD is correct by induction on the number of columns of the minor. For the empty minor it returns the terminal 1, the determinant of a $0 \times 0$ matrix. For a larger minor, CHAIN follows the Laplace expansion along the first row term by term: the sign $(-1)^{|\{c' < c\}|}$ of line L7 is the sign of the column's position in the minor, and the hi child is the DDD of the smaller minor. Zero suppression drops only a term whose minor has no terms. The symbols are distinct, so no two terms cancel, and the 1-paths are in bijection with the nonzero terms. The unique table merges only vertices with the same five fields, so it changes neither the value nor the paths. Two vertices with the same set of signed terms are the same vertex, which makes the DDD canonical for a fixed order of the entries. The full proof is below.

## Complexity

The costs are in the word-RAM model, with a column set stored as a bit mask of $n \le w$ bits, and with expected $O(1)$ hash operations.

- **BUILD.** Let $M$ be the number of distinct column sets that MINOR reaches. Each needs $O(n)$ time to list its nonzero columns (line L4), and it has at most $n + 1$ CHAIN calls of $O(1)$ time each. So BUILD takes $O(n M)$ expected time and makes $V \le n M$ vertices. For a dense matrix $M = 2^n$, so BUILD takes $O(n \, 2^n)$ time, against the $n!$ terms of a full expansion. For a tridiagonal matrix, $M$ is 11, 56 and 466 for $n = 4$, 10 and 30, because BUILD also enters minors with no terms before zero suppression drops them. A check of the structural rank of each minor (a bipartite matching) would stop these calls early.
- **EVALUATE and COUNT-TERMS.** One pass over the vertices: $O(V)$ arithmetic operations. The term count can be exponential in $n$, so its numbers can have $O(n \log n)$ bits.
- **TERMS.** Each term has $n$ entries, so listing $T$ terms takes $O(n T + V)$ time. This cost is the reason to keep the expression as a DDD.

The size of the DDD depends on the order of the entries. A good order for a circuit matrix follows the structure of the circuit. No order makes every matrix small: the dense matrix of order $n$ has $n \, 2^{n-1}$ vertices in the row order above.

## Variants

- **Multiroot DDDs.** The determinant and the cofactors of one matrix share one unique table. Shi and Tan also expand each entry $g + s C$ by powers of the frequency variable $s$, and build one root for each coefficient of each power, so the numerator and the denominator of a network function come out as polynomials in $s$.
- **Other entry orders.** The row order of this page is the simplest. Shi and Tan order the entries with a heuristic that follows the circuit graph.
- **Approximate generation.** The dominant terms of a DDD can be found by a shortest-path search on the graph, with the logarithm of each term's size as the path length. This is one of the methods of [approximate symbolic analysis](/approximate-symbolic-analysis/).
- **Hierarchical analysis.** Tan and Shi split a large circuit into blocks, build one DDD for each block, and combine their results.

## When to use it

Use a DDD when you need the exact symbolic determinant or network function of a circuit with tens to hundreds of nodes, and need to evaluate it many times with new numbers, count its terms, or take the largest terms from it. To get a number for one set of values, [Gaussian elimination](/gaussian-elimination/) is faster. To give a designer a short formula, the exact expression is too long, and an approximate method is the right tool.

## Pitfalls

- **Expanding the terms.** The terms can be many more than the vertices. Count and evaluate on the graph. Do not list the terms unless you need a few of them.
- **A bad order of the entries.** The size depends on the order. A random order of the rows and columns of a band matrix can make the graph much larger.
- **Equal symbols.** The term count and the bijection with the paths assume distinct symbols. If two entries carry the same symbol, for example the conductance $g$ in four entries of a nodal matrix, then terms can cancel or merge, and the 1-paths overcount the terms of the polynomial in the element values.
- **The wrong sign.** The sign depends on the position of the column in the current minor, not in the full matrix.
- **No zero suppression.** Without line L10, the graph keeps vertices for entries that lead to no term. The value is still right, but the canonical form and the size are lost.

## Implementations

## History

Shi and Tan presented determinant decision diagrams at ICCAD in 1997 and in IEEE Transactions on Computer-Aided Design in 2000. They built them on the zero-suppressed BDDs of Minato from 1993. In 2001 they gave multiroot DDDs for the coefficients of the powers of the frequency variable.

## References
