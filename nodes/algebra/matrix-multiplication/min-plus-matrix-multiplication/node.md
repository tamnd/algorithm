---
tag: 52F2YQ
kind: problem
slug: min-plus-matrix-multiplication
name: Min-plus matrix multiplication
aliases:
- tropical matrix product
- distance product
- min-plus product
- (min,+) matrix product
area: algebra/matrix-multiplication
level: advanced
summary: The matrix product over the (min,+) semiring, C[i][j] = min over k of (A[i][k] + B[k][j]); it is equivalent to all pairs shortest paths, and no algorithm in time n^(3−ε) is known.
model: word-ram
complexity:
  vars: {n: the order of the matrices}
  time: {worst: O(n^3)}
prereqs: [naive-matrix-multiplication, all-pairs-shortest-paths]
see_also: [apsp-repeated-squaring, floyd-warshall, apsp-conjecture, apsp-negative-triangle-equivalence, boolean-matrix-multiplication, min-plus-convolution, matrix-power, negative-triangle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.1, Shortest paths and matrix multiplication (the extended product with min and +, and repeated squaring)
  - paper: "Michael L. Fredman, New bounds on the complexity of the shortest path problem, SIAM Journal on Computing 5(1) (1976)"
    locator: the main theorems (an O(n^2.5) decision tree for the min-plus product, and an o(n^3) algorithm)
  - paper: "Ryan Williams, Faster all-pairs shortest paths via circuit complexity, 46th ACM Symposium on Theory of Computing (STOC 2014)"
    locator: the main theorem (APSP and min-plus products in n^3 / 2^(Ω(sqrt(log n))) randomized time)
  - paper: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5) (2018), doi:10.1145/3186893"
    locator: the equivalences between the min-plus product, APSP and negative triangle under subcubic reductions
  - paper: "Uri Zwick, All pairs shortest paths using bridging sets and rectangular matrix multiplication, Journal of the ACM 49(3) (2002)"
    locator: the section on distance products of matrices with small integer entries (O(M n^ω) by an integer embedding)
  - paper: "Leslie R. Kerr, The effect of algebraic structure on the computational complexity of matrix multiplication, PhD thesis, Cornell University (1970)"
    locator: the lower bound of Ω(n^3) for programs that use only min and + on the min-plus product
---

Min-plus matrix multiplication, also called the distance product, replaces the sum in a matrix product by a minimum and the product by a sum: $C[i][j] = \min_k (A[i][k] + B[k][j])$. If $A$ and $B$ hold edge weights, $C$ gives the lightest paths of two edges, and $\lceil \lg (n - 1) \rceil$ min-plus squarings give [all pairs shortest paths](/all-pairs-shortest-paths/). The min-plus semiring has no subtraction, so [Strassen's algorithm](/strassen-algorithm/) and its successors do not apply. The best known algorithm saves only a factor $2^{\Omega(\sqrt{\log n})}$ over $n^3$, and the [APSP conjecture](/apsp-conjecture/) states that no algorithm runs in $O(n^{3 - \varepsilon})$ time for real or polynomially bounded integer weights.

## In plain words

The first table gives the length of the road from each city to each crossing. The second table gives the length from each crossing to each town. For each city and town, you want the shortest trip through one crossing: try each crossing, add the two lengths, and keep the smallest sum. Where there is no road, the length is infinite.

This looks like a normal table product, with adding in place of multiplying and taking the smallest in place of adding. But the clever tricks for normal products need subtraction, and there is no way to undo taking the smallest. So nobody knows a method that is much faster than trying every crossing for every pair.

## Definition

The min-plus (tropical) semiring is $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$: its addition is $\min$ with neutral element $+\infty$, and its multiplication is $+$ with neutral element $0$. For $A$ of size $n \times m$ and $B$ of size $m \times p$ with entries in it, the min-plus product is

$$(A \star B)[i][j] = \min_{0 \le k < m} \big( A[i][k] + B[k][j] \big),$$

with $\min \emptyset = +\infty$ and $x + \infty = +\infty$. The identity matrix has $0$ on the diagonal and $+\infty$ elsewhere. The product is associative, so powers are defined. The cost model is a [word RAM](/word-ram/) with comparisons and additions of weights at unit cost; for integer weights, the weights are in $\{-W, \ldots, W\}$ with $W$ polynomial in $n$.

## Variants

- **Max-plus product.** $\max_k (A[i][k] + B[k][j])$, the same problem after negating the entries. It appears in longest path, scheduling and dynamic programming.
- **Bounded integer entries.** Entries in $\{-M, \ldots, M\} \cup \{+\infty\}$ for a small $M$.
- **Bounded differences.** Entries that change by at most a constant between neighbours in a row or column, as in some problems on strings and in language edit distance.
- **(max, min) product.** $\max_k \min(A[i][k], B[k][j])$, for bottleneck paths. It has algorithms in $O(n^{(3 + \omega)/2})$ time (Duan and Pettie 2009), so it is easier than the min-plus product.
- **Witnesses.** Also return a $k$ that attains each minimum, to recover the paths.
- **Min-plus convolution.** The one-dimensional analogue on sequences; see [min-plus convolution](/min-plus-convolution/).

## Examples

1. Let $A = \begin{pmatrix} 0 & 3 & \infty \\ \infty & \infty & \infty \\ 2 & \infty & 0 \end{pmatrix}$ and $B = \begin{pmatrix} 0 & 1 & 4 \\ \infty & 0 & 1 \\ \infty & \infty & 0 \end{pmatrix}$. Row $0$ of $A \star B$ is the minimum of $0 + (0, 1, 4)$ and $3 + (\infty, 0, 1) = (\infty, 3, 4)$, so $(0, 1, 4)$. Row $1$ of $A$ is all $\infty$, so row $1$ of the product is all $\infty$: no path leaves vertex $1$. Row $2$ is the minimum of $2 + (0, 1, 4)$ and $0 + (\infty, \infty, 0)$, so $(2, 3, 0)$. Hence $A \star B = \begin{pmatrix} 0 & 1 & 4 \\ \infty & \infty & \infty \\ 2 & 3 & 0 \end{pmatrix}$.
2. Shortest paths. If $D$ is the weight matrix of a graph with $D[i][i] = 0$ and no negative cycle, then $D^{\star k}[i][j]$ is the weight of a lightest path from $i$ to $j$ with at most $k$ edges, and $D^{\star (n-1)}$ is the distance matrix. See [APSP by repeated squaring](/apsp-repeated-squaring/).
3. The identity. With $I_\star$ the min-plus identity, $0$ on the diagonal and $+\infty$ elsewhere, $A \star I_\star = A$. The ordinary identity matrix is not the identity here: its $0$ entries off the diagonal give $(A \star I)[i][j] = \min(A[i][j] + 1, \min_{k \ne j} A[i][k])$.

## Known algorithms

- **Naive product.** $n^3$ additions and $n^3$ comparisons, $\Theta(n^3)$ time.
- **Fredman (1976).** A decision tree of depth $O(n^{2.5})$, and an algorithm in $O(n^3 (\log \log n / \log n)^{1/3})$ time that uses table lookup on small blocks.
- **Polylogarithmic savings.** A series of papers by Takaoka, Zwick, Chan and others improved the savings; Chan (2010) reached $O(n^3 (\log \log n)^3 / \log^2 n)$.
- **Williams (2014).** $n^3 / 2^{\Omega(\sqrt{\log n})}$ randomized time, by reducing many small min-plus products to the evaluation of low-depth circuits, which are in turn evaluated with fast rectangular matrix products. Chan and Williams (2016) made it deterministic. It is faster than any polylogarithmic saving but still not $O(n^{3 - \varepsilon})$.
- **Small integer entries.** For entries in $\{0, \ldots, M\} \cup \{+\infty\}$, encode $A'[i][k] = x^{M - A[i][k]}$ (and $0$ for $+\infty$), similarly for $B$, and multiply the polynomial matrices; the minimum is read from the highest power of $x$ in each entry. With $x = n + 1$ this is an integer product of numbers with $O(M \log n)$ digits, so the cost is $\tilde{O}(M n^{\omega})$ (Yuval 1976; Alon, Galil and Margalit 1997; Zwick 2002). This is subcubic only when $M = O(n^{3 - \omega - \varepsilon})$.
- **Structured inputs.** Bringmann, Grandoni, Saha and Vassilevska Williams (2016) gave a truly subcubic algorithm for matrices with bounded differences, and later work improved the exponent for monotone and bounded difference inputs.

## Bounds

- **Upper bound.** $O(n^3)$, improved by the subpolynomial factor $2^{\Omega(\sqrt{\log n})}$ (Williams 2014).
- **Restricted lower bound.** Any program that uses only $\min$ and $+$ on the entries needs $\Omega(n^3)$ operations (Kerr 1970). So a faster algorithm must use other operations, such as comparisons of sums with branching, table lookup or bit tricks.
- **Decision trees.** The $O(n^{2.5})$ decision tree of Fredman shows that the number of comparisons is not the obstacle: the cost is in choosing which comparisons to make.
- **APSP conjecture.** No algorithm computes the min-plus product of $n \times n$ matrices with integer entries in $\{-n^c, \ldots, n^c\}$ in $O(n^{3 - \varepsilon})$ time, for any $\varepsilon > 0$ and some constant $c$. It is a conjecture, not a theorem, and it is a base of [fine-grained reductions](/fine-grained-reduction/).

## Reductions

- **APSP.** The min-plus product and all pairs shortest paths have the same running time up to constant factors. One direction squares the weight matrix $\lceil \lg(n-1) \rceil$ times, and a recursive method removes the $\log n$ factor. The other direction takes the distances of the three-layer graph with edges from layer $1$ to layer $2$ weighted by $A$ and from layer $2$ to layer $3$ weighted by $B$: the distance from $i$ in layer $1$ to $j$ in layer $3$ is $(A \star B)[i][j]$. See [all pairs shortest paths](/all-pairs-shortest-paths/).
- **Negative triangle.** Vassilevska Williams and Williams (2010, 2018) showed that a truly subcubic algorithm for the min-plus product exists exactly when one exists for detecting a triangle of negative total weight; see [APSP and negative triangle equivalence](/apsp-negative-triangle-equivalence/) and [negative triangle](/negative-triangle/).
- **Boolean products.** A Boolean product is a min-plus product with entries $0$ and $+\infty$, so min-plus is at least as hard as [Boolean matrix multiplication](/boolean-matrix-multiplication/), which takes $O(n^{\omega})$.

## Applications

- All pairs shortest paths, and shortest paths with at most $k$ edges.
- Dynamic programming over sequences and trees, such as some versions of language edit distance, RNA folding and optimal parenthesization, where the speed-up methods reduce to min-plus products.
- Max-plus algebra for scheduling and discrete event systems, where the powers of a matrix describe the timing of a periodic system.
- Tropical geometry, where the min-plus semiring is the basic arithmetic.

## References
