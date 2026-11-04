---
tag: FHW6KS
kind: concept
slug: parenthesization
name: Parenthesization
area: techniques/dynamic-programming
level: intro
summary: A full placement of parentheses in a product of matrices that fixes the order of multiplication and determines the total cost.
prereqs: [binary-tree, catalan-numbers]
see_also: [matrix-chain-multiplication, catalan-numbers, catalan-triangulation-theorem, optimal-polygon-triangulation, interval-dp, expression-tree, pairwise-summation, join-ordering]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.2 (fully parenthesized products, the cost of a matrix product, and the count P(n) of parenthesizations)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 7.5 (convolutions and the Catalan numbers)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.4 (enumeration of trees and binary trees)
---

A parenthesization of a product $A_1 A_2 \cdots A_n$ is a full placement of parentheses that says, for each multiplication, which two adjacent factors it joins. For an associative operation every parenthesization gives the same value, but the work to compute it can differ by a large factor. The parenthesizations of $n$ factors correspond one to one to the full [binary trees](/binary-tree/) with $n$ leaves, and their number is the [Catalan number](/catalan-numbers/) $C_{n-1}$. This page is about the objects and their count; the search for the cheapest one for matrices is the [matrix-chain multiplication](/matrix-chain-multiplication/) problem.

## In plain words

You must multiply a row of things together, and you can multiply only two at a time. You also may not change the left-to-right order. So you must decide which neighbours to join first, then which results to join next, and so on until one thing is left. Writing this plan with brackets gives a parenthesization.

When the operation is associative, every plan gives the same answer. But the plans do not cost the same. With matrices, one plan can do ten times the arithmetic of another. A computer cannot just try every plan, because the number of plans grows almost four times with each extra factor. This is why the choice of plan is a classic job for dynamic programming.

## The idea

### Full parenthesization

A product is *fully parenthesized* when it is a single factor $A_i$, or the product $(X\,Y)$ of two fully parenthesized products $X$ and $Y$, where $X$ covers $A_i \cdots A_k$ and $Y$ covers $A_{k+1} \cdots A_j$ for some $i \le k < j$. This is the definition of CLRS Section 14.2. Each pair of parentheses marks one multiplication, so a full parenthesization of $n$ factors has exactly $n - 1$ pairs. The index $k$ of the outermost pair is the *split point*.

### Parenthesizations are binary trees

Map a parenthesization $\pi$ to a tree $T(\pi)$: a single factor $A_i$ becomes a leaf labelled $A_i$, and $(X\,Y)$ becomes a node with left subtree $T(X)$ and right subtree $T(Y)$. Every internal node of $T(\pi)$ has exactly two children, so $T(\pi)$ is a full binary tree. Its leaves, read from left to right, are $A_1, \ldots, A_n$. The map has an inverse: read a full binary tree with $n$ leaves bottom up and write $(X\,Y)$ at each internal node. So the map is a bijection between the full parenthesizations of $n$ factors and the full binary trees with $n$ leaves, or, after removing the leaves, all binary trees with $n - 1$ nodes. The tree is the [expression tree](/expression-tree/) of the product, and the internal nodes are the $n - 1$ multiplications.

### The count

Let $P(n)$ be the number of full parenthesizations of $n$ factors.

**Claim.** $P(1) = 1$ and, for $n \ge 2$,
$$P(n) = \sum_{k=1}^{n-1} P(k)\, P(n - k).$$

**Proof.** A single factor has one parenthesization. For $n \ge 2$ the outermost pair splits the product at a unique $k$ with $1 \le k \le n - 1$. Given $k$, the parenthesization is fixed by a full parenthesization of the left part $A_1 \cdots A_k$ and an independent one of the right part $A_{k+1} \cdots A_n$. The left part can be chosen in $P(k)$ ways and the right part in $P(n-k)$ ways, and different choices give different strings. Different $k$ give different outermost pairs, so no parenthesization is counted twice. Summing over $k$ gives the formula. ∎

The Catalan numbers satisfy $C_0 = 1$ and $C_m = \sum_{i=0}^{m-1} C_i C_{m-1-i}$ for $m \ge 1$. Put $P(n) = C_{n-1}$: the recurrence for $P$ becomes $C_{n-1} = \sum_{k=1}^{n-1} C_{k-1} C_{n-k-1}$, which is the Catalan recurrence with $m = n - 1$ and $i = k - 1$. Both sequences start at 1, so by induction on $n$,
$$P(n) = C_{n-1} = \frac{1}{n}\binom{2n-2}{n-1}.$$
The closed form of $C_m$ is derived with generating functions in Concrete Mathematics, Section 7.5.

### Exponential growth

Two lower bounds show that trying all parenthesizations is hopeless.

- **A simple bound.** For $n \ge 3$ the terms $k = 1$ and $k = n - 1$ of the sum are different terms, and each equals $P(n-1)$. So $P(n) \ge 2P(n-1)$, and with $P(2) = 1$ this gives $P(n) \ge 2^{n-2}$ for $n \ge 2$.
- **A sharper bound.** $\binom{2m}{m}$ is the largest of the $2m + 1$ binomial coefficients $\binom{2m}{i}$, whose sum is $4^m$. So $\binom{2m}{m} \ge 4^m/(2m+1)$ and $C_m \ge 4^m / \bigl((m+1)(2m+1)\bigr)$. With $m = n - 1$, $P(n) \ge 4^{n-1}/\bigl(n(2n-1)\bigr)$, so $P(n) = \Omega(4^n / n^2)$.

An upper bound is $C_m \le \binom{2m}{m} \le 4^m$. So $P(n)$ grows like $4^n$ up to a polynomial factor.

### The cost of a parenthesization of matrices

Let $A_i$ be a $p_{i-1} \times p_i$ matrix. The product $A_i \cdots A_j$ is a $p_{i-1} \times p_j$ matrix, whatever the parenthesization inside it. The [standard algorithm](/naive-matrix-multiplication/) multiplies a $p \times q$ matrix by a $q \times r$ matrix with $pqr$ scalar multiplications. So the internal node of $T(\pi)$ that joins $A_i \cdots A_k$ and $A_{k+1} \cdots A_j$ costs $p_{i-1} p_k p_j$, and the cost of $\pi$ is
$$\mathrm{cost}(\pi) = \sum_{\text{internal nodes } (i, k, j)} p_{i-1}\, p_k\, p_j .$$
Every parenthesization does $n - 1$ matrix multiplications. Only the sizes of the matrices that each multiplication sees change, and the cost formula depends only on the triples $(i, k, j)$ of the tree. This additive form, with each term fixed by one split, is what makes the minimization a dynamic program over intervals.

## Examples

**All parenthesizations of four factors.** $P(4) = C_3 = 5$. Take the dimensions $p = (30, 35, 15, 5, 10)$, so $A_1$ is $30 \times 35$, $A_2$ is $35 \times 15$, $A_3$ is $15 \times 5$ and $A_4$ is $5 \times 10$.

| parenthesization | split points, outer first | scalar multiplications |
|---|---|---|
| $(A_1(A_2(A_3A_4)))$ | 1, 2, 3 | 16500 |
| $(A_1((A_2A_3)A_4))$ | 1, 3, 2 | 14875 |
| $((A_1A_2)(A_3A_4))$ | 2, 1, 3 | 21000 |
| $((A_1(A_2A_3))A_4)$ | 3, 1, 2 | 9375 |
| $(((A_1A_2)A_3)A_4)$ | 3, 2, 1 | 19500 |

The best is 9375 and the worst is 21000. For example, $((A_1(A_2A_3))A_4)$ costs $35 \cdot 15 \cdot 5 + 30 \cdot 35 \cdot 5 + 30 \cdot 5 \cdot 10 = 2625 + 5250 + 1500 = 9375$.

**Three factors, a factor of ten.** For $A_1$ of size $10 \times 100$, $A_2$ of size $100 \times 5$ and $A_3$ of size $5 \times 50$, the order $((A_1 A_2) A_3)$ costs $5000 + 2500 = 7500$ and the order $(A_1 (A_2 A_3))$ costs $25000 + 50000 = 75000$. This is the example of CLRS Section 14.2.

**Growth of the count.**

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| $P(n)$ | 1 | 1 | 2 | 5 | 14 | 42 | 4862 | 2674440 | 1767263190 | 1002242216651368 |

For six matrices with $p = (30, 35, 15, 5, 10, 20, 25)$, the 42 parenthesizations cost from 15125 to 58000 scalar multiplications. The plain left-to-right order costs 40500.

**Non-example: a partial placement.** $(A_1 A_2) A_3 A_4$ is not a full parenthesization. It leaves open whether $A_3$ joins first with $(A_1 A_2)$ or with $A_4$, so it does not fix the order of the work.

**Non-example: a reordering.** $((A_1 A_3) A_2)$ is not a parenthesization of $A_1 A_2 A_3$. Parentheses may change the grouping but not the order of the factors, because matrix multiplication is not commutative.

## Where it is used

- **[Matrix-chain multiplication](/matrix-chain-multiplication/).** The problem of finding a parenthesization of least cost. The recurrence over split points solves it in $O(n^3)$ time, against about $4^n$ parenthesizations.
- **Triangulations.** The parenthesizations of $n$ factors correspond one to one to the triangulations of a convex polygon with $n + 1$ sides ([Catalan triangulation theorem](/catalan-triangulation-theorem/)). With this bijection, matrix-chain multiplication becomes a case of [optimal polygon triangulation](/optimal-polygon-triangulation/).
- **[Interval DP](/interval-dp/).** Every problem whose solution is a binary tree over a sequence in fixed order uses the same split-point recurrence: the [optimal binary search tree](/optimal-binary-search-tree/), parsing with the [CYK algorithm](/cyk-algorithm/), and optimal triangulation.
- **Floating-point sums.** Addition of [floating-point](/floating-point-arithmetic/) numbers is not associative, so the parenthesization changes the result. In IEEE double precision, $(10^{16} + (-10^{16})) + 1 = 1$ but $10^{16} + ((-10^{16}) + 1) = 0$. [Pairwise summation](/pairwise-summation/) uses a balanced parenthesization to bound the rounding error.
- **Parallel evaluation.** The depth of the tree is the span of the computation. A balanced tree has depth $\lceil \lg n \rceil$, which is the basis of a [parallel reduction](/parallel-reduction/), while the left-to-right order has depth $n - 1$.
- **Join order in databases.** A join of several tables in a query is a product whose cost depends on the sizes of the intermediate results. Choosing a [join order](/join-ordering/) restricted to a fixed sequence of tables is a parenthesization problem.

## References
