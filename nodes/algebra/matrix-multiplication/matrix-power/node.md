---
tag: A98XEA
kind: problem
slug: matrix-power
name: Matrix power
aliases:
- computing A^k
- power of a matrix
- matrix powering
area: algebra/matrix-multiplication
level: intro
summary: Compute A^k for a square matrix A and a nonnegative integer k; repeated squaring does it with O(log k) matrix products.
model: algebraic-computation-tree
complexity:
  vars: {n: the order of the matrix A, k: the exponent, ω: the matrix multiplication exponent (read n^ω as n^(ω+ε) for each ε > 0)}
  time: {worst: O(n^ω log k)}
prereqs: [naive-matrix-multiplication, binary-exponentiation]
see_also: [matrix-exponentiation, matrix-fibonacci, addition-chain, linear-recurrence-nth-term, apsp-repeated-squaring, transfer-matrix-method, cayley-hamilton-theorem]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (the binary method, addition chains and the bound l(n) ≥ lg n)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.1, Shortest paths and matrix multiplication (powers of a matrix over the min-plus semiring by repeated squaring)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition
    locator: Chapter 9, Functions of matrices (powers and polynomials of a matrix, including the Paterson and Stockmeyer evaluation)
---

The matrix power problem asks for $A^k$, the product of $k$ copies of a square matrix $A$, with $A^0 = I$. Multiplying $k - 1$ times is slow; [repeated squaring](/matrix-exponentiation/) needs fewer than $2 \lg k$ matrix products, so the cost is $O(MM(n) \log k)$ ring operations. It needs only an associative product, so it works over any ring and over semirings such as min-plus. Powers of a matrix count walks in graphs, step Markov chains, and give the terms of [linear recurrences](/linear-recurrence-nth-term/) such as the [Fibonacci numbers](/matrix-fibonacci/).

## In plain words

You have a square table of numbers. You want to multiply the table by itself many times, for example a thousand times. Doing the multiplications one after the other takes a thousand steps. There is a much faster way: multiply the table by itself to get the second power, multiply that by itself to get the fourth power, then the eighth, and so on. With these squares you can build any power by combining a few of them, in about as many steps as the number of binary digits of the exponent.

This works for each kind of number for which the table product follows the usual grouping rule. It also works for tables of distances, where adding takes the role of multiplying.

## Definition

Let $R$ be a ring, or a semiring with a multiplicative unit. The input is a matrix $A \in R^{n \times n}$ and an integer $k \ge 0$. The output is

$$A^0 = I_n, \qquad A^k = A^{k-1} A \quad (k \ge 1),$$

where $I_n$ is the identity matrix of the semiring (its unit on the diagonal and its zero elsewhere). Because the matrix product is associative, $A^{i} A^{j} = A^{i+j}$ for all $i, j \ge 0$, so any grouping of the $k$ factors gives the same matrix. The cost is counted in ring operations, and $MM(n)$ is the cost of one $n \times n$ product.

## Variants

- **Fixed vector.** Compute $A^k x$ for a vector $x$. This takes $k$ [matrix-vector products](/matrix-vector-multiplication/), $O(kn^2)$ operations, which beats $O(MM(n) \log k)$ when $k$ is small compared with $n$.
- **Modular powers.** Compute $A^k \bmod q$, for example to get large terms of a recurrence modulo a prime. The entries stay small, so each ring operation is one word operation.
- **Semiring powers.** Over the min-plus semiring, $A^{k}[i][j]$ is the weight of a lightest walk with exactly $k$ edges from $i$ to $j$ (with $A[i][i] = 0$, at most $k$ edges). This gives [all pairs shortest paths by repeated squaring](/apsp-repeated-squaring/). Over the Boolean semiring with $I$ added, $(I + A)^{n-1}$ is the reflexive [transitive closure](/transitive-closure/).
- **All powers up to $k$.** Compute $A, A^2, \ldots, A^k$, for example for a Krylov sequence. This needs $k - 1$ products.
- **Matrix exponential.** $e^A = \sum_k A^k / k!$ over the reals. Its standard method, scaling and squaring, also uses repeated squaring.

## Examples

1. The Fibonacci matrix: $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^5 = \begin{pmatrix} 8 & 5 \\ 5 & 3 \end{pmatrix}$ and $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^{10} = \begin{pmatrix} 89 & 55 \\ 55 & 34 \end{pmatrix}$. The entries are the Fibonacci numbers $F_{k+1}$, $F_k$ and $F_{k-1}$.
2. Walks in a triangle. Let $A$ be the [adjacency matrix](/adjacency-matrix/) of the complete graph on 3 vertices. Then $A^2 = \begin{pmatrix} 2 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 1 & 2 \end{pmatrix}$ and $A^3 = \begin{pmatrix} 2 & 3 & 3 \\ 3 & 2 & 3 \\ 3 & 3 & 2 \end{pmatrix}$. The entry $A^k[i][j]$ is the number of walks with $k$ edges from $i$ to $j$. The trace of $A^3$ is $6$, which is $6$ times the number of triangles: each triangle gives two closed walks from each of its three vertices.
3. A nilpotent matrix: $\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}^2 = 0$, so all higher powers are zero.
4. A Jordan block: $\begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}^5 = \begin{pmatrix} 32 & 80 \\ 0 & 32 \end{pmatrix}$, in line with the formula $\begin{pmatrix} \lambda & 1 \\ 0 & \lambda \end{pmatrix}^k = \begin{pmatrix} \lambda^k & k \lambda^{k-1} \\ 0 & \lambda^k \end{pmatrix}$.
5. Edge cases: $A^0 = I_n$ for every $A$, including the zero matrix, and $A^1 = A$.

## Known algorithms

- **Repeated multiplication.** $k - 1$ products for $k \ge 1$, so $O(k \cdot MM(n))$.
- **[Matrix exponentiation by squaring](/matrix-exponentiation/).** The binary method uses $\lfloor \lg k \rfloor + \nu(k) - 1$ products, where $\nu(k)$ is the number of ones in the binary form of $k$. This is at most $2 \lfloor \lg k \rfloor$, so the cost is $O(MM(n) \log k)$.
- **[Addition chains](/addition-chain/).** A chain $1 = e_0 < e_1 < \cdots < e_r = k$, where each $e_t$ is the sum of two earlier terms, gives $A^k$ in $r$ products. The shortest chain can save products for some $k$, for example $k = 15$ needs 5 products instead of the 6 of the binary method.
- **Cayley and Hamilton.** Over a field, the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) gives $\chi_A(A) = 0$ for the [characteristic polynomial](/characteristic-polynomial-computation/) $\chi_A$. So $A^k = r(A)$ where $r(x) = x^k \bmod \chi_A(x)$ has degree less than $n$. Computing $r$ takes $O(\log k)$ polynomial products of degree $n$, and evaluating $r(A)$ takes $O(\sqrt{n})$ matrix products with the Paterson and Stockmeyer method. This is better when $k$ is very large.
- **Diagonalization.** If $A = P D P^{-1}$ with $D$ diagonal, then $A^k = P D^k P^{-1}$. This is used over the reals and complex numbers, with the rounding errors of an eigenvalue method.

## Bounds

- **Upper bound.** $O(MM(n) \log k)$ ring operations, which is $O(n^{\omega + \varepsilon} \log k)$ for each $\varepsilon > 0$, and $O(n^3 \log k)$ with the [naive product](/naive-matrix-multiplication/).
- **Lower bound for chains of products.** A method that only multiplies two matrices that it has already computed (each a power of $A$) needs at least $\lceil \lg k \rceil$ products: after $t$ products the largest power is at most $A^{2^t}$. This is the bound $l(k) \ge \lceil \lg k \rceil$ for addition chains.
- **Lower bound by output size.** $\Omega(n^2)$ operations, since the output has $n^2$ entries.
- **Size of the numbers.** Over $\mathbb{Z}$, the entries of $A^k$ can have length $\Theta(k)$ digits (for example the Fibonacci matrix), so the time on a [word RAM](/word-ram/) grows with the cost of [integer multiplication](/integer-multiplication/) of long numbers, not only with the number of ring operations.

## Reductions

- **Linear recurrences.** The $k$-th term of a linear recurrence of order $d$ is an entry of $M^k v$ for the $d \times d$ companion matrix $M$. See [linear recurrence nth term](/linear-recurrence-nth-term/) and the [matrix Fibonacci](/matrix-fibonacci/) method.
- **Shortest paths.** All pairs shortest paths reduce to $\lceil \lg (n-1) \rceil$ min-plus squarings. See [APSP by repeated squaring](/apsp-repeated-squaring/).
- **Counting.** The number of strings of length $k$ accepted by a finite automaton, and many counting problems on paths and tilings, are entries of $A^k$ for a transfer matrix. See the [transfer matrix method](/transfer-matrix-method/).

## Applications

- Counting walks of a given length in a graph, and the $k$-step transitions of a [Markov chain](/markov-chain/).
- Fast terms of recurrences modulo a prime in programming contests and in number theory.
- Transitive closure and shortest paths over Boolean and min-plus semirings.
- Graph invariants: the trace of $A^3$ counts triangles, see [triangle counting](/triangle-counting/).

## References
