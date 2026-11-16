---
tag: 5NNCDT
kind: definition
slug: communication-matrix
name: Communication matrix
aliases:
- function matrix
area: complexity/communication-and-query-complexity
level: intro
summary: "The matrix M_f of a two-party function f: rows are Alice's inputs, columns are Bob's inputs, and the entry in row x and column y is f(x, y)."
prereqs: [communication-model, rank]
see_also: [deterministic-communication-complexity, fooling-set-method, log-rank-lower-bound, nondeterministic-communication-complexity, sign-rank, discrepancy-method, equality-problem, greater-than-problem]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1, Basics (Section 1.2, Rectangles, and Section 1.4, Rank Lower Bound)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 1, Deterministic Protocols (section Rectangles), and Chapter 2, Rank
---

The communication matrix of a function $f : X \times Y \to Z$ is the $|X| \times |Y|$ matrix $M_f$ whose row $x$ and column $y$ hold $f(x, y)$. It turns a question about protocols in the [communication model](/communication-model/) into a question about a matrix: a protocol of cost $c$ cuts $M_f$ into at most $2^c$ submatrices, each a set of rows times a set of columns, on which the entry is constant. Lower bounds such as the [fooling set method](/fooling-set-method/) and the [log-rank lower bound](/log-rank-lower-bound/) are statements about $M_f$.

## Definition

Let $X$, $Y$ and $Z$ be finite sets and $f : X \times Y \to Z$. Fix an order of $X$ and an order of $Y$. The **communication matrix** of $f$ is the matrix

$$M_f = \big( f(x, y) \big)_{x \in X,\ y \in Y},$$

with one row for each input of Alice and one column for each input of Bob. The orders do not matter: a change of order permutes rows and columns, and every notion below is the same for all orders.

For Boolean $f$, $M_f$ is a 0-1 matrix, and its **rank** $\operatorname{rank}(M_f)$ is the rank over the real numbers unless a text says otherwise. Some texts use the sign matrix $(-1)^{f(x,y)}$ instead; its rank differs from the rank of $M_f$ by at most 1.

The definitions that come with $M_f$:

- A **combinatorial rectangle** is a set $R = A \times B$ with $A \subseteq X$ and $B \subseteq Y$. In the matrix it is the submatrix on the rows in $A$ and the columns in $B$. The rows and columns need not be next to each other. A set $S \subseteq X \times Y$ is a rectangle exactly when $(x, y) \in S$ and $(x', y') \in S$ imply $(x, y') \in S$.
- A rectangle is **monochromatic** if $f$ is constant on it, and it is a **$z$-rectangle** if that constant is $z$.
- The inputs that reach one leaf of a protocol form a monochromatic rectangle, and the leaves cut $X \times Y$ into disjoint rectangles. This is proved on the [communication model](/communication-model/) page.

## Examples and non-examples

Take $n = 2$, with rows and columns in the order $00, 01, 10, 11$.

**Equality.** $\mathrm{EQ}(x, y) = 1$ exactly when $x = y$, so $M_{\mathrm{EQ}}$ is the identity matrix $I_4$. In general $M_{\mathrm{EQ}} = I_{2^n}$, of rank $2^n$. Two 1-entries $(x, x)$ and $(x', x')$ cannot share a 1-rectangle, because the rectangle would also hold $(x, x')$, which is 0. So the 1-entries alone need $2^n$ rectangles. See the [equality problem](/equality-problem/).

**Greater-than.** $\mathrm{GT}(x, y) = 1$ exactly when $x > y$ as binary numbers. Its matrix is strictly lower triangular. For $n = 2$ the two matrices are:

$$M_{\mathrm{EQ}} = \begin{pmatrix} 1&0&0&0 \\ 0&1&0&0 \\ 0&0&1&0 \\ 0&0&0&1 \end{pmatrix}, \qquad M_{\mathrm{GT}} = \begin{pmatrix} 0&0&0&0 \\ 1&0&0&0 \\ 1&1&0&0 \\ 1&1&1&0 \end{pmatrix}.$$

The first row of $M_{\mathrm{GT}}$ is zero and the other rows are independent, so the rank is $2^n - 1$. See the [greater-than problem](/greater-than-problem/).

**Inner product.** $\mathrm{IP}(x, y) = x_1 y_1 + \cdots + x_n y_n \bmod 2$. For $n = 2$:

$$M_{\mathrm{IP}} = \begin{pmatrix} 0&0&0&0 \\ 0&1&0&1 \\ 0&0&1&1 \\ 0&1&1&0 \end{pmatrix}.$$

Over the reals its rank is 3, and in general it is $2^n - 1$. Over the field $\mathrm{GF}(2)$ the rank is only 2, and in general it is $n$, because the entry is a bilinear form over $\mathrm{GF}(2)$. Its sign matrix $(-1)^{\mathrm{IP}(x,y)}$ is a Hadamard matrix of rank $2^n$. This example is why the field must be stated. See the [inner product problem](/inner-product-problem/).

**Disjointness.** $\mathrm{DISJ}(x, y) = 1$ exactly when no $i$ has $x_i = y_i = 1$. The matrix is the $n$-fold [Kronecker product](/kronecker-product/) of $\begin{pmatrix} 1&1 \\ 1&0 \end{pmatrix}$, so its rank is $2^n$. See the [disjointness problem](/disjointness-problem/).

The ranks above, for $n = 1$ to $5$, agree with an exact computation over the rationals and over $\mathrm{GF}(2)$.

**Non-examples.**

- The truth table of a function of $2n$ bits is a vector of $2^{2n}$ entries. It becomes a communication matrix only after the bits are split between Alice and Bob, and a different split gives a different matrix. Take $F(u, v) = 1$ exactly when $u = v$, for $u, v \in \{0,1\}^n$ with $n$ even. If Alice holds $u$ and Bob holds $v$, the matrix is $I_{2^n}$, of rank $2^n$. If Alice holds the first halves of $u$ and $v$ and Bob holds the second halves, then $F(x, y) = g(x) h(y)$, where $g$ tests Alice's halves and $h$ tests Bob's. That matrix has rank 1, and 2 bits are enough.
- A submatrix on a set of rows and a set of columns is a rectangle, but a set of entries that is not of the form $A \times B$ is not, even if $f$ is constant on it. The diagonal of $M_{\mathrm{EQ}}$ is not a rectangle.
- For a relation, such as the [Karchmer-Wigderson relation](/karchmer-wigderson-relation/), each pair $(x, y)$ may have many correct outputs, so the entry is a set and there is no single matrix of values.

## Related definitions

- **Partition number** $\chi(f)$: the least number of disjoint monochromatic rectangles that cover $X \times Y$. A protocol of cost $c$ gives such a partition with $2^c$ parts, so $D^{cc}(f) \ge \log_2 \chi(f)$, where $D^{cc}(f)$ is the [deterministic communication complexity](/deterministic-communication-complexity/). Not every partition comes from a protocol.
- **Cover number** $C^1(f)$: the least number of 1-rectangles, not necessarily disjoint, that cover the 1-entries; $C^0(f)$ is the same for the 0-entries. The [nondeterministic communication complexity](/nondeterministic-communication-complexity/) is $\lceil \log_2 C^1(f) \rceil$.
- **Fooling set**: a set of entries with the same value, no two of which fit in one monochromatic rectangle. See the [fooling set method](/fooling-set-method/).
- **Rank**: the [rank](/rank/) of $M_f$ over the reals. The [log-rank lower bound](/log-rank-lower-bound/) gives $D^{cc}(f) \ge \log_2 \operatorname{rank}(M_f)$, and the [log-rank conjecture](/log-rank-conjecture/) asks for an upper bound of the form $(\log_2 \operatorname{rank}(M_f))^{O(1)}$.
- **Sign rank**: the least rank of a real matrix whose entries have the signs of $(-1)^{f(x,y)}$. It characterizes unbounded-error protocols. See [sign rank](/sign-rank/).
- **Discrepancy**: how far from balanced $f$ can be on a large rectangle. It bounds randomized protocols. See the [discrepancy method](/discrepancy-method/).

## References
