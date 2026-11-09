---
tag: X4CC5C
kind: algorithm
slug: glynn-formula
name: Glynn's formula
aliases:
- Glynn's permanent formula
- Balasubramanian-Bax-Franklin-Glynn formula
area: combinatorics/counting-algorithms
level: advanced
summary: Computes the permanent via a Gray-code sum over sign vectors.
solves: [permanent-computation]
model: word-ram
complexity:
  vars: {n: the order of the matrix}
  time: {worst: Θ(2^n n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2010
  people: [David G. Glynn]
  note: Glynn published the formula with a proof by polarization in 2010. The same sum over sign vectors had appeared earlier, in work of Balasubramanian (1980) and of Bax and Franklin (1996).
prereqs: [permanent-computation, ryser-formula, binary-reflected-gray-code]
see_also: [counting-perfect-matchings, determinant-computation, inclusion-exclusion-principle, gray-code, derangement, exact-exponential-algorithms, kasteleyn-method, fpras]
sources:
  - paper: doi:10.1016/j.ejc.2010.01.010
    title: David G. Glynn, The permanent of a square matrix, European Journal of Combinatorics 31(7), 1887 to 1891, 2010
    locator: the main theorem (the formula as a sum over sign vectors with the first sign fixed) and the remark on Gray code evaluation
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: the chapter on the permanent of a matrix (the Gray code evaluation of Ryser's formula, which Glynn's formula follows)
---

Glynn's formula computes the [permanent](/permanent-computation/) of an $n \times n$ matrix $A$, $n \ge 1$, as an average over sign vectors:

$$\operatorname{per}(A) = \frac{1}{2^{n-1}} \sum_{\substack{\delta \in \{\pm 1\}^n \\ \delta_1 = 1}} \left( \prod_{k=1}^{n} \delta_k \right) \prod_{j=1}^{n} \sum_{i=1}^{n} \delta_i a_{ij}.$$

The sum has $2^{n-1}$ terms, half as many as [Ryser's formula](/ryser-formula/). In [Gray code](/binary-reflected-gray-code/) order each step flips one sign $\delta_i$, which changes each column sum by $\pm 2 a_{ij}$, so the whole sum takes $\Theta(2^n n)$ arithmetic operations and $O(n)$ extra space. The proof is a parity argument: a term survives the averaging only when every row is used an odd number of times, and with $n$ rows and $n$ columns that forces each row to be used once. The formula needs division by $2^{n-1}$, so it fails in characteristic 2.

## In plain words

The permanent picks one entry from each row, with all picks in different columns, multiplies them, and adds up over all ways of picking.

Glynn's formula gives each row a sign, plus or minus, with the first row always plus. For each column it adds up the signed entries, multiplies these column totals, and multiplies again by the product of all the signs. Then it averages over all sign choices. When you expand the column totals, a way of picking that uses some row twice, or an even number of times, appears with both signs equally often and cancels out. Only the ways that use each row exactly once survive, and those are the terms of the permanent. Walking through the sign choices so that one sign flips at a time makes each step cheap.

## The problem

Input: an $n \times n$ matrix $A$ with entries in a commutative ring in which division by $2^{n-1}$ is possible: the integers (where the division is exact), the rationals, the reals or the complex numbers. Output: $\operatorname{per}(A) = \sum_{\pi \in S_n} \prod_{i=1}^{n} a_{i \pi(i)}$, with $\operatorname{per}$ of the $0 \times 0$ matrix equal to 1.

## The algorithm

The signs $\delta_2, \ldots, \delta_n$ run through all $2^{n-1}$ sign vectors in binary reflected Gray code order: at step $k = 1, \ldots, 2^{n-1} - 1$, the sign of row $\rho(k) + 2$ flips, where $\rho(k)$ is the number of trailing zeros of $k$. The array $c$ holds the column sums $c_j = \sum_i \delta_i a_{ij}$, and $\sigma = \prod_k \delta_k$.

```pseudo id=main
GLYNN(A)                                          ▷ A is n × n; returns per(A)
L1  if n = 0 then return 1
L2  δ[1..n] ← +1;  σ ← +1;  c[j] ← Σ_i a[i][j] for j = 1..n
L3  total ← c[1] · c[2] ⋯ c[n]                    ▷ the term of δ = (+1, …, +1)
L4  for k ← 1 to 2^(n−1) − 1 do
L5      i ← ρ(k) + 2                              ▷ the row whose sign flips
L6      δ[i] ← −δ[i];  σ ← −σ
L7      for j ← 1 to n do c[j] ← c[j] + 2 · δ[i] · a[i][j]
L8      total ← total + σ · c[1] · c[2] ⋯ c[n]
L9  return total / 2^(n−1)
```

## Example

Let $A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$, so $n = 3$ and there are 4 sign vectors.

| step | row flipped (L5) | $\delta$ | $c$ | $\prod c_j$ | $\sigma$ | total |
|---|---|---|---|---|---|---|
| L3 | | $+, +, +$ | 12, 15, 18 | 3240 | $+1$ | 3240 |
| $k = 1$ | 2 | $+, -, +$ | 4, 5, 6 | 120 | $-1$ | 3120 |
| $k = 2$ | 3 | $+, -, -$ | $-10, -11, -12$ | $-1320$ | $+1$ | 1800 |
| $k = 3$ | 2 | $+, +, -$ | $-2, -1, 0$ | 0 | $-1$ | 1800 |

Line L9 returns $1800 / 2^2 = 450$, the permanent. In step $k = 1$, line L7 changes $c$ by $2 \cdot (-1) \cdot (4, 5, 6)$, from $(12, 15, 18)$ to $(4, 5, 6)$.

## Correctness

The full proof is in `proofs/correctness.md`. Expand the product of the column sums:

$$\prod_{j=1}^{n} \sum_{i=1}^{n} \delta_i a_{ij} = \sum_{f : [n] \to [n]} \prod_{j=1}^{n} \delta_{f(j)} a_{f(j) j},$$

where $f$ picks a row $f(j)$ for each column $j$. Let $m_k = |f^{-1}(k)|$, the number of columns that pick row $k$. The coefficient of $\prod_j a_{f(j) j}$ in the full sum is $\sum_{\delta} \prod_k \delta_k^{1 + m_k}$ over $\delta_1 = 1$ and free $\delta_2, \ldots, \delta_n$. The sum over $\delta_k = \pm 1$ of $\delta_k^{1 + m_k}$ is 2 if $m_k$ is odd and 0 if it is even. So the coefficient is $2^{n-1}$ if $m_2, \ldots, m_n$ are all odd, and 0 otherwise. If they are all odd, each is at least 1, so $m_1 \le 1$; and $m_1 = n - \sum_{k \ge 2} m_k \equiv n - (n - 1) = 1 \pmod 2$, so $m_1 = 1$, and then all $m_k = 1$. So the surviving $f$ are exactly the bijections, each with coefficient $2^{n-1}$, and the sum is $2^{n-1} \operatorname{per}(A)$. The loop visits each sign vector once by the Gray code property, and lines L6 and L7 keep $\sigma = \prod_k \delta_k$ and $c_j = \sum_i \delta_i a_{ij}$.

## Complexity

- **Time.** Line L3 and each of the $2^{n-1} - 1$ passes of the loop do $\Theta(n)$ additions and multiplications. The total is $\Theta(2^{n-1} n) = \Theta(2^n n)$ arithmetic operations, about half the work of Ryser's formula with a Gray code.
- **Space.** The arrays $\delta$ and $c$ take $\Theta(n)$ words beyond the input.
- **Bit cost.** For integer entries of absolute value at most $M$, each $|c_j| \le nM$, each product is at most $(nM)^n$, and the total is at most $2^{n-1} (nM)^n$, so all numbers have $O(n \log(nM))$ bits.

## Properties

- **Exact over the integers.** The total is divisible by $2^{n-1}$, so line L9 is an exact division, and the algorithm returns the exact integer permanent.
- **Characteristic 2.** Over a field of characteristic 2, the division in line L9 is impossible, and for $n \ge 2$ the sum itself is 0. There, the permanent equals the determinant and takes polynomial time.
- **Fewer terms than Ryser.** Ryser's sum has $2^n - 1$ nonzero candidate terms, Glynn's has $2^{n-1}$. For the same Gray code cost per term, Glynn's formula is about twice as fast.
- **Numerically better.** In floating point the column sums of Glynn's formula are often smaller in magnitude than Ryser's row sums, which reduces cancellation, but large cancellation is still possible.

## Variants and improvements

- **Ryser's formula.** The inclusion-exclusion version over column subsets; see [Ryser's formula](/ryser-formula/).
- **Rows or columns.** By symmetry, the formula can sign the columns and sum over the rows, since $\operatorname{per}(A) = \operatorname{per}(A^T)$.
- **Parallel.** The $2^{n-1}$ sign vectors split into blocks of consecutive Gray code ranks, each started from its first vector with direct column sums.
- **Bounded entries.** For matrices with few distinct entries or low rank, sums over the values of the column sums instead of over sign vectors can be faster.

## When to use it

Use Glynn's formula as the default exact method for the permanent of a dense matrix over the integers, rationals, reals or complex numbers, for orders up to about 30 to 40. It is commonly used for the exact permanents that arise in the simulation of boson sampling. Over a ring of characteristic 2, or modulo a power of 2, use other methods. For planar bipartite 0-1 matrices, [Kasteleyn's method](/kasteleyn-method/) is polynomial, and for large nonnegative matrices an [FPRAS](/fpras/) gives an estimate.

## Pitfalls

- **The first sign.** Line L5 must flip only rows $2, \ldots, n$ (hence the $+2$). Letting row 1 flip too doubles the number of terms and makes line L9 return $2 \operatorname{per}(A)$, unless the divisor is changed to $2^n$.
- **The step of the update.** Line L7 adds $2 \delta_i a_{ij}$ with the new sign, because the old contribution $-\delta_i a_{ij}$ must be removed and the new one added. Adding $\delta_i a_{ij}$ gives wrong column sums.
- **The sign $\sigma$.** Line L6 must flip $\sigma$ at every step. Forgetting it adds all products with the same sign, which gives a wrong total (for the example, $3240 + 120 - 1320 + 0 = 2040$, and $2040 / 4 = 510$).
- **Integer division.** In line L9, use exact division. Floating-point division of a large integer total loses digits.

## Implementations

## History

David Glynn published the formula in 2010, with a proof based on polarization of the product of linear forms, and noted that a Gray code makes each term cost $O(n)$. The same formula had appeared before: in the thesis of Balasubramanian (1980) and in the finite-difference method of Bax and Franklin (1996). It improves Ryser's formula of 1963 by a factor of about 2, and it is the usual exact method in the literature on boson sampling.

## References
