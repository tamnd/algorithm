---
tag: VTJXE5
kind: algorithm
slug: matrix-exponentiation
name: Matrix exponentiation
aliases:
- fast matrix power
- exponentiation by squaring of matrices
- binary matrix powering
- repeated squaring of a matrix
area: algebra/matrix-multiplication
level: core
summary: Compute A^k with floor(lg k) squarings and one extra product for each further one in the binary form of k, so O(log k) matrix products; it works over any ring or semiring.
solves: [matrix-power]
model: algebraic-computation-tree
complexity:
  vars: {n: the order of the matrix A, k: the exponent}
  time: {worst: Θ(n^3 log k), best: Θ(n^3 log k)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [matrix-power, binary-exponentiation, naive-matrix-multiplication]
see_also: [matrix-fibonacci, addition-chain, linear-recurrence-nth-term, apsp-repeated-squaring, strassen-algorithm, integer-exponentiation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (the left-to-right and right-to-left binary methods, the count λ(n) + ν(n) − 1, and addition chains)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.1, Shortest paths and matrix multiplication (repeated squaring over the min-plus semiring)
  - paper: "Charles M. Fiduccia, An efficient formula for linear recurrences, SIAM Journal on Computing 14(1), 1985"
    locator: pp. 106 to 112 (the k-th term by powers of x modulo the characteristic polynomial instead of powers of the companion matrix)
---

Matrix exponentiation computes the [matrix power](/matrix-power/) $A^k$ of a square matrix with $O(\log k)$ matrix products instead of $k - 1$, by repeated squaring. The left-to-right binary method does $\lfloor \lg k \rfloor$ squarings and $\nu(k) - 1$ further products, where $\nu(k)$ is the number of ones in the binary form of $k$. With the [triple loop](/naive-matrix-multiplication/) as the product, this is $\Theta(n^3 \log k)$ ring operations; with any product of cost $MM(n)$ it is $O(MM(n) \log k)$. It needs only associativity, so it works over any ring and over semirings such as min-plus, where it gives [shortest paths by repeated squaring](/apsp-repeated-squaring/).

## In plain words

To raise a square table to a large power, do not multiply by the table again and again. Read the exponent in binary, from the left. Start with the table itself. For each further binary digit, square what you have, and if the digit is a one, also multiply once by the original table. At the end you hold the wanted power.

Each step doubles the exponent reached so far, or doubles it and adds one. So the number of steps is about the number of binary digits of the exponent, not the exponent itself. A power of a million needs about forty table products instead of a million.

## The problem

The input is a matrix $A \in R^{n \times n}$ over a ring, or a semiring with a unit, and an integer $k \ge 0$. The output is $A^k$, with $A^0 = I_n$. This is the [matrix power](/matrix-power/) problem. The cost counts matrix products; each product costs $MM(n)$ ring operations, which is $2n^3 - n^2$ with the triple loop.

## The algorithm

Write $k = (b_t b_{t-1} \ldots b_0)_2$ with $b_t = 1$, so $t = \lfloor \lg k \rfloor$.

```pseudo id=main
MATRIX-EXPONENTIATION(A, k)              ▷ A is n × n, k ≥ 0
L1  if k = 0 then return I_n
L2  let b_t b_(t−1) … b_0 be the binary digits of k, with b_t = 1
L3  R ← A
L4  for i ← t − 1 downto 0 do
L5      R ← R · R
L6      if b_i = 1 then R ← R · A
L7  return R
```

Line L1 handles the empty product. Line L3 starts with the leading digit, which is always $1$. In the loop, line L5 doubles the exponent of $R$, and line L6 adds one to it when the next digit is $1$. The products of lines L5 and L6 must go into a new matrix: a product cannot overwrite one of its own factors while it still reads it.

The right-to-left method reads the digits from $b_0$ upward. It keeps $S = A^{2^i}$ and multiplies $S$ into the result for each digit $1$. It does the same number of products. The left-to-right method has the advantage that line L6 always multiplies by the fixed matrix $A$, which is cheaper when $A$ is sparse or has a special form.

## Example

Let $A$ be the [adjacency matrix](/adjacency-matrix/) of the triangle (the complete graph on three vertices), $A = \begin{pmatrix} 0 & 1 & 1 \\ 1 & 0 & 1 \\ 1 & 1 & 0 \end{pmatrix}$, and $k = 13 = (1101)_2$, so $t = 3$. By symmetry each power of $A$ has one value $d$ on the diagonal and one value $e$ off the diagonal.

| step | digit $b_i$ | operation | exponent of $R$ | $d$ | $e$ |
|---|---|---|---|---|---|
| L3 | $b_3 = 1$ | $R \leftarrow A$ | 1 | 0 | 1 |
| L5 | $b_2 = 1$ | $R \leftarrow R \cdot R$ | 2 | 2 | 1 |
| L6 |  | $R \leftarrow R \cdot A$ | 3 | 2 | 3 |
| L5 | $b_1 = 0$ | $R \leftarrow R \cdot R$ | 6 | 22 | 21 |
| L5 | $b_0 = 1$ | $R \leftarrow R \cdot R$ | 12 | 1366 | 1365 |
| L6 |  | $R \leftarrow R \cdot A$ | 13 | 2730 | 2731 |

The run makes 5 products, which is $t + \nu(13) - 1 = 3 + 3 - 1$. Repeated multiplication would make 12. The entries count walks: there are 2731 walks with 13 edges between two distinct vertices of the triangle. They agree with the closed form $d = (2^k + 2(-1)^k)/3$ and $e = (2^k - (-1)^k)/3$, which follows from the eigenvalues $2, -1, -1$ of $A$.

## Correctness

The loop of line L4 keeps the invariant: at the start of the iteration for $i$, $R = A^{q_i}$ with $q_i = \lfloor k / 2^{i+1} \rfloor$, the number formed by the digits $b_t \ldots b_{i+1}$. At the start, $i = t - 1$ and $q_{t-1} = b_t = 1$, and $R = A$. Lines L5 and L6 turn $A^{q}$ into $A^{2q + b_i}$, and $2 q_i + b_i = q_{i-1}$. After the last iteration ($i = 0$), $R = A^{\lfloor k / 2^0 \rfloor} = A^k$. Only associativity of the product is used, through $A^{q} A^{q} = A^{2q}$ and $A^{2q} A = A^{2q+1}$. The full proof is in the proofs section.

## Complexity

- **Products.** Line L5 runs $t = \lfloor \lg k \rfloor$ times and line L6 runs once for each digit $1$ below the leading one, $\nu(k) - 1$ times. So the method makes $\lfloor \lg k \rfloor + \nu(k) - 1$ products for $k \ge 1$. This is between $\lfloor \lg k \rfloor$ (for $k$ a power of two) and $2\lfloor \lg k \rfloor$ (for $k = 2^{t+1} - 1$).
- **Ring operations.** With the triple loop, each product costs $2n^3 - n^2$ operations, so the total is $\Theta(n^3 \log k)$ for $k \ge 2$, in each case, since the count of products is between $\lfloor \lg k \rfloor$ and $2 \lfloor \lg k \rfloor$. With [Strassen's algorithm](/strassen-algorithm/) as the product, it is $O(n^{\log_2 7} \log k)$, and in general $O(MM(n) \log k)$.
- **Space.** Two $n \times n$ matrices besides the input: $R$ and the target of the current product.
- **Lower bound.** Any method that only multiplies matrices it has already computed (powers of $A$) needs at least $\lceil \lg k \rceil$ products, since each product at most doubles the largest exponent. So the binary method is within a factor $2$ of optimal among such methods. The exact optimum is the length of a shortest [addition chain](/addition-chain/) for $k$, which is hard to compute in general.
- **Size of numbers.** Over $\mathbb{Z}$, the entries of $A^k$ can grow to $\Theta(k)$ digits, so on a [word RAM](/word-ram/) the time is dominated by the last products of long integers. Work modulo $q$ to keep each operation on one word.

## Properties

- **Any associative product.** Rings, semirings (Boolean, min-plus, max-plus), and matrices of polynomials all work.
- **Deterministic and data-oblivious.** The sequence of products depends only on $k$.
- **Few products, not optimal.** For $k = 15$ the method makes 6 products, while the addition chain $1, 2, 3, 6, 12, 15$ needs 5.

## Variants and improvements

- **Right-to-left binary method.** The same count, with a running square $S = A^{2^i}$.
- **Window methods.** Precompute $A^1, A^3, \ldots, A^{2^w - 1}$ and process $w$ digits at a time. This lowers the number of non-squaring products to about $\lg k / (w + 1)$, at the cost of $2^{w-1}$ stored matrices, see [sliding window exponentiation](/sliding-window-exponentiation/).
- **Addition chains.** Use a short addition chain for a fixed exponent that is used many times.
- **Power times a vector.** For $A^k x$ with small $k$, use $k$ [matrix-vector products](/matrix-vector-multiplication/), at $\Theta(k n^2)$ cost.
- **Linear recurrences.** For the companion matrix of a recurrence of order $d$, compute $x^k \bmod \chi(x)$ instead, with polynomial products of degree $d$. This needs $O(d^2 \log k)$ operations with the classical product of polynomials, against $O(d^3 \log k)$ with matrices (Fiduccia, 1985). See [linear recurrence nth term](/linear-recurrence-nth-term/).
- **Fibonacci numbers.** The $2 \times 2$ case gives the [matrix Fibonacci](/matrix-fibonacci/) method and the fast doubling formulas.

## When to use it

Use it to compute one large power of a small or medium matrix, especially modulo a prime, and over semirings, where no faster general method exists. For a power applied to one vector with $k$ not much larger than $n$, use repeated matrix-vector products. For the terms of a linear recurrence of large order, prefer the polynomial method.

## Pitfalls

- **Forgetting $k = 0$.** Without line L1, the method returns $A$ for $k = 0$, but $A^0 = I_n$, also for the zero matrix.
- **Overwriting a factor.** Computing $R \leftarrow R \cdot R$ in place, with $R$ as both input and output of the triple loop, reads entries that it has already overwritten. Write each product to a new matrix (lines L5 and L6).
- **Overflow.** Entries grow fast: the triangle example reaches 2731 at $k = 13$ and has about $0.3 k$ decimal digits in general. Reduce modulo $q$ after each product with fixed-width integers.
- **The identity of a semiring.** Over min-plus, the identity has $0$ on the diagonal and $+\infty$ elsewhere, not the usual $1$ and $0$.

## Implementations

## History

The binary method for powers of numbers is very old; Knuth traces it to an Indian text from before 200 BC. Its use for matrix powers, for example for the Fibonacci numbers and for linear recurrences, is standard in the literature on algorithms. Its use over the min-plus semiring for shortest paths appears in textbook treatments of all pairs shortest paths, such as CLRS.

## References
