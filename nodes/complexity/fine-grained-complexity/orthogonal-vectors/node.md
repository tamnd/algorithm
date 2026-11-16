---
tag: 691VYT
kind: problem
slug: orthogonal-vectors
name: Orthogonal Vectors
aliases:
- OV
area: complexity/fine-grained-complexity
level: core
summary: Given two lists of n vectors in {0,1}^d, decide whether some vector of the first list and some vector of the second have inner product 0. The source problem of most quadratic lower bounds.
prereqs: [word-ram, time-complexity]
see_also: [orthogonal-vectors-hypothesis, seth-implies-ov-lower-bound, strong-exponential-time-hypothesis, quadratic-time-hardness, sum-over-subsets, maximum-inner-product-search, edit-distance-seth-lower-bound, 3sum]
sources:
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365 (conference version in ICALP 2004)"
    locator: the section on cooperative subset queries and orthogonal vectors (the problem, and the reduction from CNF-SAT)
  - paper: "Amir Abboud, Ryan Williams and Huacheng Yu, More applications of the polynomial method to algorithm design, Proceedings of the 26th ACM-SIAM Symposium on Discrete Algorithms (SODA 2015), 218-230"
    locator: the randomized algorithm for orthogonal vectors with d = c log n in time n^(2 - 1/O(log c))
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the section on the orthogonal vectors problem, its variants and the problems that OV reduces to
  - paper: doi:10.1145/2488608.2488673
    title: "Liam Roditty and Virginia Vassilevska Williams, Fast approximation algorithms for the diameter and radius of sparse graphs, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 515-524"
    locator: the lower bound for approximating the diameter of sparse graphs, from CNF-SAT through orthogonal vectors
  - paper: doi:10.1137/15M1053128
    title: "Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing 47(3), 2018 (conference version in STOC 2015)"
    locator: the reduction from orthogonal vectors to edit distance
  - paper: arxiv:1501.07053
    title: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 59-78"
    locator: the reductions from orthogonal vectors and from k-OV to LCS
---

Orthogonal Vectors (OV) is the problem of deciding whether two lists of $n$ Boolean vectors of dimension $d$ contain a pair, one from each list, with inner product 0. The obvious algorithm checks all $n^2$ pairs in time $O(n^2 d)$, and no algorithm is known that is faster by a polynomial factor when $d$ is a large multiple of $\log n$. The [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/) says that none exists, and it follows from [SETH](/strong-exponential-time-hypothesis/). Because many problems with quadratic algorithms can encode OV, it is the usual starting point for [quadratic-time hardness](/quadratic-time-hardness/).

This page is about the problem: its forms, its algorithms and what reduces to it and from it. The hypothesis about its running time is on [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/), and the proof that SETH implies it is on [SETH implies OV lower bound](/seth-implies-ov-lower-bound/).

## In plain words

There are two groups of people. For each person there is a list of yes-or-no answers to the same set of questions. Is there a pair, one person from each group, who never both said yes to the same question?

The direct way compares every person in the first group with every person in the second group, question by question. The work grows with the product of the group sizes. When the number of questions is small, a table of all possible answer patterns helps. When the number of questions is a little larger than that, no method is known that does much better than comparing all pairs, and experts believe that none exists.

## Definition

Write $u \cdot v = \sum_{i=1}^{d} u_i v_i$ for $u, v \in \{0,1\}^d$. The vectors $u$ and $v$ are *orthogonal* if $u \cdot v = 0$, that is, if no coordinate is 1 in both.

**ORTHOGONAL VECTORS (OV)**

- Instance: integers $n, d \ge 1$, and two lists $A = (a_1, \ldots, a_n)$ and $B = (b_1, \ldots, b_n)$ of vectors in $\{0,1\}^d$.
- Question: are there $i$ and $j$ with $a_i \cdot b_j = 0$?

The input has $2nd$ bits. The running time is measured on the [word RAM](/word-ram/) with words of $O(\log n)$ bits, as a function of $n$ and $d$. The interesting range is $\omega(\log n) \le d \le n^{o(1)}$: for $d \le c \log n$ with a small constant $c$ the problem is easy (see below), and for $d \ge n$ the input itself has $n^2$ bits or more.

**Equivalent forms.**

- *Sets.* Each vector is the set $\{i : u_i = 1\} \subseteq \{1, \ldots, d\}$. OV asks for a disjoint pair. Equivalently, it asks whether some set of $A$ is a subset of the complement of some set of $B$; this is the subset query form that Williams used.
- *One list.* Given one list $S$ of $n$ vectors, are two distinct entries orthogonal? Two lists become one list by appending two coordinates: $a \mapsto (a, 1, 0)$ and $b \mapsto (b, 0, 1)$. Two vectors from the same list then share a coordinate, so only pairs from different lists can be orthogonal. One list becomes two lists by setting $A = B = S$ and handling the zero vector apart, since only the zero vector is orthogonal to itself. Both maps take $O(nd)$ time.
- *Search and count.* The search version outputs a pair. The counting version (#OV) outputs the number of orthogonal pairs.

## Variants

- **Unbalanced OV.** $|A| = n$ and $|B| = n^{\alpha}$ for a constant $\alpha > 0$; the naive bound is $n^{1+\alpha} d$.
- **$k$-OV.** Given $k$ lists of $n$ vectors, are there $a^{(1)}, \ldots, a^{(k)}$, one from each list, with $\sum_i \prod_{t} a^{(t)}_i = 0$? The naive time is $O(n^k d)$. Conditional on SETH, it has no $O(n^{k-\varepsilon})$ algorithm for $d = \omega(\log n)$, by the same split of the variables into $k$ parts.
- **Maximum and minimum inner product.** Find the pair with the largest or smallest $a \cdot b$. OV is the special case "is the minimum 0". See [maximum inner product search](/maximum-inner-product-search/).
- **Low dimension.** $d = c \log n$ for a constant $c$. This is the form in the [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/).
- **Vectors over larger domains.** Inner product 0 over integer or real vectors. These are not covered here, and the algorithms below do not apply to them.

## Examples

**A no-instance.** Let $d = 5$, $A = \{10110, 01101, 11010\}$ and $B = \{01011, 10101, 00111\}$. The inner products, with rows for $A$ and columns for $B$, are

| | 01011 | 10101 | 00111 |
|---|---|---|---|
| 10110 | 1 | 2 | 2 |
| 01101 | 2 | 2 | 2 |
| 11010 | 2 | 1 | 1 |

No entry is 0, so the answer is no.

**A yes-instance.** Replace $01011$ by $01001$ in $B$. The first row becomes $0, 2, 2$, the second $2, 2, 2$ and the third $1, 1, 1$. The pair $(10110, 01001)$ is orthogonal: as sets, $\{1, 3, 4\}$ and $\{2, 5\}$ are disjoint.

**The subset table.** For small $d$, mark every vector of $A$ in a table $f$ of size $2^d$, indexed by bit masks. Then, for each coordinate $i$ and each mask $M$ with bit $i$ set, set $f[M] \leftarrow f[M] \lor f[M \setminus \{i\}]$. After all $d$ rounds, $f[M]$ is true if and only if some $a \in A$ is a subset of $M$. A vector $b$ has an orthogonal partner in $A$ if and only if $f[\overline{b}]$ is true, where $\overline{b}$ is the complement. On the no-instance above, the table with 32 entries gives false for all three complements $10100$, $01010$ and $11000$. This is the [sum over subsets](/sum-over-subsets/) transform over the OR operation.

## Known algorithms

All bounds are on the word RAM with words of $\Theta(\log n)$ bits.

- Checking all pairs takes $O(n^2 d)$ time, deterministic; with $w$-bit words and bit-parallel AND, it takes $O(n^2 \lceil d / w \rceil)$.
- The subset table above takes $O(2^d d + n d)$ time, deterministic, which is $O(n^{c} \log n)$ for $d = c \log_2 n$ with $c \ge 1$; it beats $n^2$ when $c < 2$.
- Multiplying the $n \times d$ matrix of $A$ by the transpose of the matrix of $B$ gives all $n^2$ inner products in $O(n^2 d^{\omega - 2})$ arithmetic operations for $d \le n$, deterministic, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/); it also counts the orthogonal pairs.
- The polynomial method of Abboud, Williams and Yu (2015) decides OV with $d = c \log n$ in time $n^{2 - 1/O(\log c)}$, randomized. The saving tends to 0 as $c$ grows, so this does not contradict the hypothesis.

## Bounds

- **Unconditional.** Any algorithm must read the input, so $\Omega(nd)$. No better unconditional lower bound is known on the word RAM.
- **Conditional on SETH.** For every $\varepsilon > 0$ there is a $c$ such that OV with $d = c \log n$ has no $O(n^{2-\varepsilon})$ algorithm, randomized algorithms included if SETH excludes them. In particular, there is no $O(n^{2-\varepsilon} \mathrm{poly}(d))$ algorithm. The proof is on [SETH implies OV lower bound](/seth-implies-ov-lower-bound/).
- **Gaps that do not contradict it.** Gains by factors such as $\log n$ or $2^{\Theta(\sqrt{\log n})}$ do not refute the bound. The Abboud, Williams and Yu algorithm shows that, for each fixed $c$, the exponent is below 2, so the constant $c$ in the hypothesis must depend on $\varepsilon$.

## Reductions

- **From CNF-SAT to OV** (Williams 2005). Deterministic, split and list. A CNF formula on $N$ variables and $m$ clauses becomes an OV instance with $n = 2^{N/2}$ vectors per list and $d = m$, in time $O(2^{N/2} m N)$. An $O(n^{2-\varepsilon}\mathrm{poly}(d))$ algorithm for OV would then decide CNF-SAT in time $2^{(1 - \varepsilon/2) N} \mathrm{poly}(m)$. Full proof on [SETH implies OV lower bound](/seth-implies-ov-lower-bound/).
- **From OV to edit distance** (Backurs and Indyk 2015). Deterministic, time $O(nd)$, two strings of length $O(nd)$ over an alphabet of size $O(d)$. See [edit distance SETH lower bound](/edit-distance-seth-lower-bound/).
- **From OV to LCS** (Abboud, Backurs and Vassilevska Williams 2015; Bringmann and Künnemann 2015). Deterministic, strings of length $n \cdot \mathrm{poly}(d)$ over a constant alphabet. See [LCS SETH lower bound](/lcs-seth-lower-bound/).
- **From OV to graph diameter, 2 against 3.** Deterministic, time $O(nd)$. Make a vertex for each vector of $A$ and of $B$, a vertex for each coordinate, and two extra vertices $x$ and $y$. Join $a$ to coordinate $i$ when $a_i = 1$, and the same for $b$. Join $x$ to every $a$ and every coordinate, $y$ to every $b$ and every coordinate, and $x$ to $y$. A vector $a$ and a vector $b$ are at distance 2 if they share a coordinate, and at distance 3 otherwise; all other pairs are at distance at most 2. So the diameter is 3 if an orthogonal pair exists, and 2 if not. The graph has $2n + d + 2$ vertices and $O(nd)$ edges. On the yes-instance above it has 13 vertices and 34 edges, and breadth-first search finds diameter 3; on the no-instance it has 13 vertices and 35 edges and diameter 2. So an algorithm that approximates the diameter of a sparse graph within a factor below $3/2$ in time $O(m^{2-\varepsilon})$ would refute SETH (Roditty and Vassilevska Williams 2013).
- **From OV to the other lists.** Fréchet distance, regular expression matching, dynamic time warping and many others; see [quadratic-time hardness](/quadratic-time-hardness/).

No reduction is known from OV to [3SUM](/3sum/) or from 3SUM to OV.

## Applications

- **Conditional lower bounds.** OV is the middle step between SETH and most problems in the class of quadratic SETH-hard problems. Nearly every such proof builds a gadget for a vector and a way to combine all pairs; see [fine-grained reduction](/fine-grained-reduction/).
- **Set containment and partial match.** A database query that asks whether a stored set is contained in a given set, for many given sets, is OV in the subset form. [All-pairs similarity search](/all-pairs-similarity-search/) and [maximum inner product search](/maximum-inner-product-search/) contain it as a special case, which explains why exact methods for them do not scale well in high dimension.
- **Algorithm design.** Fast algorithms for OV with $d = c \log n$ give faster algorithms for CNF-SAT with few clauses and for other problems that reduce to it.

## References
