---
tag: HAD331
kind: problem
slug: boolean-matrix-multiplication
name: Boolean matrix multiplication
aliases:
- Boolean matrix product
- BMM
- OR-AND matrix product
area: algebra/matrix-multiplication
level: core
summary: Compute the product of two 0/1 matrices over the Boolean semiring, C[i][j] = OR over k of (A[i][k] AND B[k][j]); it is used for reachability, transitive closure, triangle detection and parsing.
model: algebraic-computation-tree
complexity:
  vars: {n: the order of the matrices, ω: the matrix multiplication exponent (read n^ω as n^(ω+ε) for each ε > 0)}
  time: {worst: O(n^ω)}
prereqs: [naive-matrix-multiplication, adjacency-matrix]
see_also: [transitive-closure, four-russians-method, combinatorial-bmm-conjecture, triangle-detection-hypothesis, valiant-algorithm, min-plus-matrix-multiplication, triangle-counting, reachability]
sources:
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 6, Matrix multiplication and related operations (Boolean matrix multiplication through the integer product, and the four Russians algorithm)
  - paper: "V. L. Arlazarov, E. A. Dinic, M. A. Kronrod and I. A. Faradzev, On economical construction of the transitive closure of an oriented graph, Soviet Mathematics Doklady 11 (1970)"
    locator: the main algorithm (Boolean products in O(n^3 / log n) operations)
  - paper: "Michael J. Fischer and Albert R. Meyer, Boolean matrix multiplication and transitive closure, 12th Annual Symposium on Switching and Automata Theory (1971)"
    locator: the main theorem (transitive closure and Boolean matrix multiplication have the same cost up to constant factors)
  - paper: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5) (2018), doi:10.1145/3186893"
    locator: the theorem on combinatorial Boolean matrix multiplication and triangle detection (conference version FOCS 2010)
  - paper: "Noga Alon, Zvi Galil, Oded Margalit and Moni Naor, Witnesses for Boolean matrix multiplication and for shortest paths, 33rd IEEE Symposium on Foundations of Computer Science (FOCS 1992)"
    locator: the randomized algorithm for witnesses in O(n^ω polylog n) expected time
  - paper: "Vaughan R. Pratt, The power of negative thinking in multiplying Boolean matrices, SIAM Journal on Computing 4(3) (1975)"
    locator: the lower bound of n^3 AND gates for monotone circuits
  - paper: "Timothy M. Chan, Speeding up the four Russians algorithm by about one more logarithmic factor, 26th ACM-SIAM Symposium on Discrete Algorithms (SODA 2015)"
    locator: the main theorem (combinatorial Boolean products in O(n^3 (log log n)^3 / log^3 n) time)
---

Boolean matrix multiplication (BMM) is the matrix product over the Boolean semiring, where addition is OR and multiplication is AND. If $A$ and $B$ are the [adjacency matrices](/adjacency-matrix/) of two relations, the product $C$ has $C[i][j] = 1$ exactly when some $k$ has $A[i][k] = 1$ and $B[k][j] = 1$, so it composes relations and finds paths of length two. The Boolean semiring has no subtraction, so [Strassen's algorithm](/strassen-algorithm/) does not run on it directly, but the integer product gives $C$ from the test $(AB)[i][j] > 0$, which brings the cost down to $O(n^{\omega})$ operations on numbers of $O(\log n)$ binary digits. Without algebra, the best known methods save only polylogarithmic factors or slightly more over $n^3$, and the conjecture that no combinatorial method saves a polynomial factor underlies part of [fine-grained complexity](/fine-grained-complexity/).

## In plain words

You have two tables of yes and no answers. Row $i$ of the first table says which middle points you can reach from point $i$. Column $j$ of the second table says from which middle points you can reach point $j$. The product says, for each pair $i$ and $j$, whether there is at least one middle point that links them.

The usual way checks every middle point for every pair. A faster way counts the linking middle points with ordinary arithmetic, using a fast method for number tables, and then answers yes when the count is not zero.

## Definition

The Boolean semiring is $\mathbb{B} = (\{0, 1\}, \vee, \wedge, 0, 1)$. The input is $A \in \mathbb{B}^{n \times m}$ and $B \in \mathbb{B}^{m \times p}$. The output is $C = A \cdot B \in \mathbb{B}^{n \times p}$ with

$$C[i][j] = \bigvee_{k=0}^{m-1} \left( A[i][k] \wedge B[k][j] \right).$$

When $m = 0$, each OR is empty and $C$ is the zero matrix. The product is associative, and the identity matrix has $1$ on the diagonal and $0$ elsewhere. $\mathbb{B}$ is not a ring: $1 \vee 1 = 1$, so $1$ has no additive inverse, and algorithms that subtract partial products, such as Strassen's, give wrong answers when they are run with OR and AND. The square case $n = m = p$ is the main one.

Costs are counted in two models. In the algebraic model, the cost is the number of ring operations of an algorithm on the integer embedding. On a [word RAM](/word-ram/) with words of $w \ge \lg n$ binary digits, combinatorial algorithms pack rows into words and count word operations.

## Variants

- **Witnesses.** For each $(i, j)$ with $C[i][j] = 1$, also return one $k$ with $A[i][k] = B[k][j] = 1$. This is needed to recover paths, not only their existence.
- **Counting.** Return the number of such $k$, which is the integer product $AB$ itself.
- **Matrix-vector form.** Compute $A x$ for a Boolean vector $x$: the set of vertices with an edge into the set $x$. This is one step of breadth-first search. See [matrix-vector multiplication](/matrix-vector-multiplication/).
- **Sparse inputs.** When $A$ and $B$ have few ones, the cost can depend on the number of ones instead of $n$. See [sparse matrix multiplication](/sparse-matrix-multiplication/).
- **Transitive closure.** Compute $A^* = I \vee A \vee A^2 \vee \cdots$, the reachability relation. It is equivalent to BMM up to constant factors.
- **Rectangular products.** $n \times n^{a}$ times $n^{a} \times n$, with its own exponent, used in some reductions.

## Examples

1. Let $A = \begin{pmatrix} 1 & 0 & 1 \\ 0 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$ and $B = \begin{pmatrix} 0 & 1 \\ 1 & 0 \\ 1 & 1 \end{pmatrix}$. Row $0$ of $C$ is the OR of rows $0$ and $2$ of $B$, which is $(1, 1)$. Row $1$ of $A$ is empty, so row $1$ of $C$ is $(0, 0)$. Row $2$ of $C$ is row $1$ of $B$, which is $(1, 0)$. So $C = \begin{pmatrix} 1 & 1 \\ 0 & 0 \\ 1 & 0 \end{pmatrix}$. The integer product is $\begin{pmatrix} 1 & 2 \\ 0 & 0 \\ 1 & 0 \end{pmatrix}$; its positive entries are the ones of $C$.
2. Paths of length two. For the directed path $0 \to 1 \to 2$ with adjacency matrix $A$, the Boolean square $A^2$ has a single $1$, in position $(0, 2)$.
3. Why subtraction matters. Let $A$ and $B$ be the all-ones $2 \times 2$ matrices, with $1 \times 1$ blocks. Over $\mathbb{Z}$, Strassen's products are $M_1 = 4$, $M_4 = 0$, $M_5 = 2$ and $M_7 = 0$, so $C_{11} = M_1 + M_4 - M_5 + M_7 = 2$, which is positive, so the Boolean entry is $1$. Over $\mathbb{B}$, no $x$ satisfies $1 \vee x = 0$, so the term $-M_5$ has no meaning, and the formula cannot be run with OR and AND.

## Known algorithms

- **Naive product.** $\Theta(n^3)$ AND and OR operations. With rows of $B$ packed into words, row $i$ of $C$ is the OR of the rows $k$ of $B$ with $A[i][k] = 1$, which costs $O(n^3 / w)$ word operations. See [bit parallelism](/bit-parallelism/).
- **Through the integer product.** Compute $D = AB$ over $\mathbb{Z}$, or over $\mathbb{Z}/q\mathbb{Z}$ for a prime $q > m$, and set $C[i][j] = [D[i][j] \ne 0]$. Each entry of $D$ is at most $m$, so the entries stay small. With any fast algorithm this takes $O(n^{\omega})$ ring operations on numbers of $O(\log n)$ binary digits. This is the best known bound. It uses subtraction. With the classical or Strassen product it is practical; the algorithms behind the smallest known bounds on $\omega$ are not.
- **Four Russians.** Arlazarov, Dinic, Kronrod and Faradzev (1970). Split $A$ into column groups of $t \approx \lg n$ columns, precompute the ORs of all $2^t$ subsets of the matching rows of $B$, and look up each row piece. This takes $O(n^3 / \log n)$ operations, or $O(n^3 / (w \log n))$ word operations with packed rows. See the [four Russians method](/four-russians-method/).
- **Better combinatorial methods.** Bansal and Williams (2009) reached $O(n^3 / \log^{2.25} n)$ with regularity lemmas, Chan (2015) $O(n^3 (\log \log n)^3 / \log^3 n)$, and Yu (2015) $O(n^3 \operatorname{poly}(\log \log n) / \log^4 n)$. Abboud, Fischer, Kelley, Lovett and Meka (2024) gave the first combinatorial method that saves more than any polylogarithmic factor, $n^3 / 2^{\Omega((\log n)^{1/7})}$.
- **Witnesses.** Alon, Galil, Margalit and Naor (1992), and Seidel (1995), find witnesses for all entries in $O(n^{\omega} \log^{c} n)$ expected time for a constant $c$, by random sampling of the middle index and integer products that encode indices.

## Bounds

- **Upper bound.** $O(n^{\omega})$ operations through the integer embedding, which is $O(n^{2.371552})$ by the bound of Vassilevska Williams, Xu, Xu and Zhou (2024). See the [matrix multiplication exponent](/matrix-multiplication-exponent/). The algorithms behind such bounds are galactic; in practice the integer route is used with the classical or Strassen product.
- **Lower bound.** $\Omega(n^2)$, since the output has $n^2$ entries and every input entry can matter, see the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/).
- **Monotone circuits.** A circuit with only AND and OR gates needs $n^3$ AND gates to compute the Boolean product (Pratt 1975, and also Paterson 1975 and Mehlhorn and Galil 1976). So any subcubic method must use negation or, equivalently, the subtraction of the integer route.
- **[Combinatorial BMM hypothesis](/combinatorial-bmm-conjecture/).** It is conjectured that no combinatorial algorithm (one that avoids the algebraic tricks behind fast products) runs in $O(n^{3 - \varepsilon})$ time for any $\varepsilon > 0$. The notion of a combinatorial algorithm has no formal definition. This hypothesis is the base of many conditional lower bounds in [fine-grained complexity](/fine-grained-complexity/).

## Reductions

- **Transitive closure.** BMM and transitive closure have the same cost up to constant factors (Furman 1970, Fischer and Meyer 1971, Munro 1971). One direction squares $I \vee A$ about $\lg n$ times; the constant factor bound uses the strongly connected components and a block recursion. The other direction reads $AB$ from the closure of a three-layer graph with adjacency matrix $\begin{pmatrix} 0 & A & 0 \\ 0 & 0 & B \\ 0 & 0 & 0 \end{pmatrix}$. See [transitive closure](/transitive-closure/).
- **Triangle detection.** A graph with adjacency matrix $A$ has a triangle exactly when some $(A^2)[i][j] = 1$ with $A[i][j] = 1$, so triangles are found with one Boolean product. Vassilevska Williams and Williams (2010, 2018) showed the converse for combinatorial algorithms: a combinatorial $O(n^{3-\varepsilon})$ triangle detection gives a combinatorial $O(n^{3 - \varepsilon/3})$ BMM. See [triangle counting](/triangle-counting/).
- **Context-free parsing.** Valiant (1975) recognized context-free languages in the time of BMM, and Lee (2002) showed a converse: fast parsing gives fast BMM. See [Valiant's algorithm](/valiant-algorithm/) and the [CYK algorithm](/cyk-algorithm/).
- **Unweighted shortest paths.** Seidel's method computes all distances in an undirected unweighted graph with $O(\log n)$ Boolean and integer products. By contrast, [min-plus products](/min-plus-matrix-multiplication/) of general weights have no known truly subcubic algorithm.

## Applications

- [Reachability](/reachability/) and transitive closure of relations and graphs.
- Triangle detection and the counting of short cycles.
- Context-free recognition and some problems on regular expressions and databases (joins of binary relations).
- Graph algorithms over $\mathbb{F}_2$ and linear algebra of 0/1 matrices, where the [four Russians method](/four-russians-method/) is used in practice.

## References
