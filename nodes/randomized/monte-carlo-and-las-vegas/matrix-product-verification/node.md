---
tag: 32V2XY
kind: problem
slug: matrix-product-verification
name: Matrix product verification
aliases:
- verifying AB = C
- verifying matrix multiplication
- matrix multiplication checking
area: randomized/monte-carlo-and-las-vegas
level: advanced
summary: Decide whether AB = C for given n by n matrices, in less time than it takes to compute the product AB.
prereqs: [naive-matrix-multiplication, one-sided-error, schwartz-zippel-lemma]
see_also: [freivalds-algorithm, polynomial-identity-testing, schwartz-zippel-lemma, naive-matrix-multiplication, strassen-algorithm, matrix-multiplication-exponent, fingerprinting, error-amplification]
sources:
  - paper: "Rusins Freivalds, Probabilistic machines can use less running time, Information Processing 77, Proceedings of the IFIP Congress 1977, North-Holland, 1977"
    title: Rusins Freivalds, Probabilistic machines can use less running time
    locator: pages 839 to 842 (checking a matrix product with random vectors)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1, Section 1.3 (verifying matrix multiplication, with the principle of deferred decisions)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Section 7.1 (fingerprinting and Freivalds' technique)
  - paper: "Tracy Kimbrel and Rakesh Kumar Sinha, A probabilistic algorithm for verifying matrix products using O(n^2) time and log2 n + O(1) random bits, Information Processing Letters 45(2), 1993"
    title: Tracy Kimbrel and Rakesh Kumar Sinha, A probabilistic algorithm for verifying matrix products using O(n^2) time and log2 n + O(1) random bits, Information Processing Letters 45(2), 1993
    locator: pages 107 to 110 (the vector (1, x, x^2, ..., x^(n-1)) for a random x)
  - paper: doi:10.1007/978-3-319-04298-5_33
    title: Ivan Korec and Jiri Wiedermann, Deterministic verification of integer matrix multiplication in quadratic time, SOFSEM 2014, Lecture Notes in Computer Science 8327
    locator: the main theorem (a deterministic O(n^2) check for integer matrices in a model with arithmetic on large integers)
---

Matrix product verification asks whether a claimed product is correct: given $n \times n$ matrices $A$, $B$ and $C$, decide whether $AB = C$. Computing $AB$ and comparing takes the time of matrix multiplication, $\Theta(n^3)$ with the [naive method](/naive-matrix-multiplication/) and $O(n^{\omega})$ with $\omega < 2.372$ in theory. A randomized check is much faster: [Freivalds' algorithm](/freivalds-algorithm/) multiplies by a random vector in $O(n^2)$ time and is wrong with probability at most $1/2$, and only when $AB \ne C$. This page is about the problem; the algorithm, its proof and its code are on the page of Freivalds' algorithm.

## In plain words

Someone gives you two tables of numbers and a third table that they say is the product of the first two. Checking the claim by doing the full product yourself is as slow as the product itself.

There is a faster way. Make up a random column of numbers and push it through both sides: through the two factor tables one after the other, and through the claimed product. Each push costs only about the size of a table. If the claim is true, the two results always match. If it is false, they fail to match at least half of the time. A few repetitions make a wrong claim almost certain to show.

## Definition

Notation on this page: $n$ is the dimension, $R$ is the ring of the entries, $D = AB - C$, and $\Pr$ is over the random choices of the checker. Time is counted in ring operations, unless the page says otherwise.

**Matrix product verification.**

- *Input:* matrices $A, B, C \in R^{n \times n}$, where $R$ is a ring, usually $\mathbb{Z}$, $\mathbb{Z}/q\mathbb{Z}$ or a finite field.
- *Question:* is $AB = C$?

The input has $3n^2$ entries. The problem is interesting because it seems easier than computing $AB$, while a checker for it tests any matrix multiplication program, whatever its method.

The answer "no" has a short proof: a vector $r$ with $A(Br) \ne Cr$. Such an $r$ exists exactly when $D \ne 0$: if $D \ne 0$, some unit vector $e_j$ with column $j$ of $D$ nonzero gives $De_j \ne 0$.

## Variants

- **Rectangular matrices.** $A$ is $n \times m$, $B$ is $m \times p$ and $C$ is $n \times p$. The random check costs $O(nm + mp + np)$, the input size.
- **A product of many matrices.** Check $A_1 A_2 \cdots A_k = C$ by computing $A_1(A_2(\cdots(A_k r)))$, in $O(k n^2)$ time.
- **An inverse.** Check that $B = A^{-1}$ by testing $AB = I$.
- **Other rings.** The random check needs subtraction and works over any ring for vectors in $\{0, 1\}^n$. Its error bound $1/|S|$ for larger sets $S$ needs an integral domain. Over a semiring with no subtraction, such as the Boolean semiring of [Boolean matrix multiplication](/boolean-matrix-multiplication/), the method does not apply as it is.
- **Fewer random bits.** Kimbrel and Sinha (1993) use the vector $(1, x, x^2, \dots, x^{n-1})$ for one random $x$ from a field with at least $2n$ elements, so they need about $\log_2 n + 1$ random bits instead of $n$.
- **Finding the errors.** When $AB \ne C$, find the wrong entries, not only decide that some exist.

## Examples

Let

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}, \quad B = \begin{pmatrix} 9 & 8 & 7 \\ 6 & 5 & 4 \\ 3 & 2 & 1 \end{pmatrix}, \quad AB = \begin{pmatrix} 30 & 24 & 18 \\ 84 & 69 & 54 \\ 138 & 114 & 90 \end{pmatrix}.$$

- **A correct claim.** With $C = AB$, every vector $r$ gives $A(Br) = Cr$. A checker with one-sided error accepts it every time.
- **One wrong entry.** Let $C$ be $AB$ with the entry in row 2, column 3 changed from 54 to 55. Then $D = AB - C$ has a single nonzero entry, $-1$, in column 3, and $Dr = 0$ exactly when $r_3 = 0$. Of the 8 vectors in $\{0, 1\}^3$, exactly 4 detect the error, so the error of one round is exactly $1/2$, and the bound $1/2$ is reached. With $r = (1, 0, 1)$: $Br = (16, 10, 4)$, $A(Br) = (48, 138, 228)$ and $Cr = (48, 139, 228)$. With $r = (1, 1, 0)$ both sides are $(54, 153, 252)$, a false "equal".
- **Two wrong entries.** More errors do not always make a miss less likely. If row 1 of $D$ is $(1, -1, 0)$, then $(Dr)_1 = r_1 - r_2$ is zero for the 4 vectors with $r_1 = r_2$, and the error of one round is again $1/2$. If row 1 of $D$ is $(1, 1, 0)$, then $(Dr)_1 = r_1 + r_2$ is zero only for $r_1 = r_2 = 0$, and the error is $1/4$.

## Known algorithms

| Method | Time | Error | Notes |
| --- | --- | --- | --- |
| Compute $AB$ with the [naive method](/naive-matrix-multiplication/) | $\Theta(n^3)$ | 0 | deterministic |
| Compute $AB$ with fast multiplication ([Strassen](/strassen-algorithm/) and later) | $O(n^{2.81})$, $O(n^{\omega})$ | 0 | deterministic, large constants for small $\omega$ |
| [Freivalds](/freivalds-algorithm/), $k$ vectors from $\{0, 1\}^n$ | $O(k n^2)$ | $\le 2^{-k}$ | one-sided: "not equal" is always right |
| Freivalds, $k$ vectors from $S^n$, over an integral domain | $O(k n^2)$ | $\le |S|^{-k}$ | by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) with degree 1 |
| Kimbrel and Sinha, $r = (1, x, \dots, x^{n-1})$ | $O(n^2)$ | $\le (n-1)/|S|$ | about $\log_2 n$ random bits per round |
| Korec and Wiedermann (2014), integer matrices | $O(n^2)$ arithmetic operations | 0 | deterministic, with operations on integers much longer than the entries |

The Korec and Wiedermann check uses one vector of powers of a large integer, so that the products cannot cancel; it counts each operation on a large integer as one step, so it is not faster than Freivalds in the bit model.

**The two error bounds.** For $r$ uniform on $\{0, 1\}^n$, if $D \ne 0$ then $\Pr[Dr = 0] \le 1/2$. Pick $D_{ij} \ne 0$ and pair each $r$ with $r'$, which is $r$ with bit $j$ flipped. Then $(Dr)_i - (Dr')_i = \pm D_{ij} \ne 0$, so at most one vector of each pair has $(Dr)_i = 0$. This uses only subtraction, so it holds over every ring, even $\mathbb{Z}/2^{64}\mathbb{Z}$. For $r$ uniform on $S^n$, row $i$ of $D$ gives the nonzero linear polynomial $\sum_j D_{ij} x_j$, and the Schwartz-Zippel lemma with degree 1 gives $\Pr[Dr = 0] \le 1/|S|$; this needs an integral domain. The full proofs are on the page of [Freivalds' algorithm](/freivalds-algorithm/).

## Bounds

- **Lower bound $\Omega(n^2)$.** Any algorithm, deterministic or randomized with error below $1/2$, must read a constant fraction of the $n^2$ entries of $C$ on some inputs: a single wrong entry can be anywhere, and an entry that the algorithm does not read cannot change its answer. So the random check is optimal up to the number of rounds.
- **The deterministic question.** No deterministic $O(n^2)$ algorithm is known for verification over a finite field, or over the integers when each operation acts on numbers of about the size of the entries. The known deterministic methods in this model compute $AB$ in some form, so they are not faster than matrix multiplication.

## Reductions

- **To polynomial identity testing.** $AB = C$ if and only if the vector of linear polynomials $(AB - C)x$ is zero. It is a PIT instance of degree 1 that can be evaluated in $O(n^2)$ time without forming $AB - C$.
- **From the problem of checking a multiplication program.** A program that claims to multiply matrices can be checked on each call by this problem, which is the idea of result checking.
- **To the problem of computing $AB$.** Trivially, by computing and comparing.

## Applications

- **Testing fast multiplication code.** Implementations of Strassen-type methods are hard to test because the rounding and the many cases hide errors. A random check after each call finds wrong results at a cost of $O(n^2)$.
- **Algorithm-based fault tolerance.** Huang and Abraham (1984) added checksum rows and columns to matrices, so that a hardware fault in a product shows in the checksums. A checksum with the all-ones vector is Freivalds' check with the fixed vector $(1, \dots, 1)$, which a bad error pattern can pass; a random vector closes this gap.
- **Outsourced computation.** A weak client can check the product returned by a strong server in $O(n^2)$ time.
- **Teaching.** It is the first example of a randomized algorithm that is faster than any known deterministic one, in many textbooks.

## References
