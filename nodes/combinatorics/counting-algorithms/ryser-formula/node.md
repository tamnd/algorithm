---
tag: 11ZBTR
kind: algorithm
slug: ryser-formula
name: Ryser's formula
aliases:
- Ryser's algorithm
- Ryser's method for the permanent
area: combinatorics/counting-algorithms
level: advanced
summary: Computes the permanent of an n×n matrix in O(2^n n) arithmetic operations by inclusion-exclusion over column subsets, visited in Gray code order.
solves: [permanent-computation]
model: word-ram
complexity:
  vars: {n: the order of the matrix}
  time: {worst: Θ(2^n n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1963
  people: [Herbert J. Ryser]
  note: Ryser gave the inclusion-exclusion formula in his book Combinatorial Mathematics in 1963. Nijenhuis and Wilf evaluated it in Gray code order, which saves a factor of n.
prereqs: [permanent-computation, inclusion-exclusion-principle, binary-reflected-gray-code]
see_also: [glynn-formula, counting-perfect-matchings, determinant-computation, derangement, exact-exponential-algorithms, sum-over-subsets, gray-code, kasteleyn-method]
sources:
  - book: "Herbert J. Ryser, Combinatorial Mathematics, Carus Mathematical Monographs 14, Mathematical Association of America, 1963"
    title: Herbert J. Ryser, Combinatorial Mathematics
    locator: Chapter 2, The principle of inclusion and exclusion (the formula for the permanent)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: the chapter on the permanent of a matrix (Ryser's formula in Gray code order)
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 189 to 201, 1979
    locator: the introduction (Ryser's method as the fastest known exact algorithm, and the #P-completeness of the permanent)
---

Ryser's formula computes the [permanent](/permanent-computation/) of an $n \times n$ matrix $A$ as

$$\operatorname{per}(A) = (-1)^n \sum_{S \subseteq [n]} (-1)^{|S|} \prod_{i=1}^{n} \sum_{j \in S} a_{ij}.$$

It is [inclusion-exclusion](/inclusion-exclusion-principle/) over the set $S$ of columns that a row may use: the product counts all maps from rows to columns in $S$, and the signs cancel every map that is not a bijection. Evaluated naively, the sum takes $O(2^n n^2)$ operations. If the subsets $S$ are visited in [Gray code](/binary-reflected-gray-code/) order, each step adds or removes one column, the row sums change in $O(n)$ time, and the total is $O(2^n n)$ operations with $O(n)$ extra space. This is far below the $n! \, n$ of the definition, and no algorithm is known that is faster by more than a factor $2^{o(n)}$.

## In plain words

The permanent picks one entry from each row, with all picks in different columns, multiplies the picks, and adds up over all ways of picking. Doing this directly takes a huge number of steps.

Ryser's idea is to drop the rule "all in different columns" and fix it afterwards. Choose a group of columns. Let each row pick any entry in those columns, even if two rows pick the same column. The total over all such picks is easy: multiply, over the rows, the sum of the row's entries in the chosen columns. Now add these totals over all groups of columns with plus and minus signs. The signs are arranged so that every bad pick, where some column is never used, cancels out, and only the good picks remain. Visiting the groups so that each one differs from the last by a single column makes each step cheap.

## The problem

Input: an $n \times n$ matrix $A$ with entries in a commutative ring (integers, rationals, reals or complex numbers). Output: $\operatorname{per}(A) = \sum_{\pi \in S_n} \prod_{i=1}^{n} a_{i \pi(i)}$, with $\operatorname{per}$ of the $0 \times 0$ matrix equal to 1. For a 0-1 matrix this is the number of [perfect matchings](/counting-perfect-matchings/) of the bipartite graph with biadjacency matrix $A$.

## The algorithm

The subsets $S \subseteq [n]$ are visited in the order of the binary reflected Gray code: at step $k = 1, \ldots, 2^n - 1$, the column that changes is $\rho(k) + 1$, where $\rho(k)$ is the number of trailing zeros of $k$. The array $r$ holds the row sums $r_i = \sum_{j \in S} a_{ij}$ of the current $S$. The empty set adds $\prod_i 0 = 0$ for $n \ge 1$, so it is skipped.

```pseudo id=main
RYSER(A)                                          ▷ A is n × n; returns per(A)
L1  if n = 0 then return 1
L2  r[1..n] ← 0;  S ← ∅;  total ← 0               ▷ r[i] = Σ_{j∈S} a[i][j]
L3  for k ← 1 to 2^n − 1 do
L4      j ← ρ(k) + 1                              ▷ the column that enters or leaves S
L5      if j ∈ S then remove j from S; s ← −1 else add j to S; s ← +1
L6      for i ← 1 to n do r[i] ← r[i] + s · a[i][j]
L7      total ← total + (−1)^|S| · r[1] · r[2] ⋯ r[n]
L8  return (−1)^n · total
```

## Example

Let $A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$, so $n = 3$. Each row of the table is one pass of the loop of line L3.

| $k$ | column $j$ (L4) | $S$ after L5 | $r$ after L6 | $\prod r_i$ | sign $(-1)^{\lvert S \rvert}$ | total after L7 |
|---|---|---|---|---|---|---|
| 1 | 1 | $\{1\}$ | 1, 4, 7 | 28 | $-1$ | $-28$ |
| 2 | 2 | $\{1, 2\}$ | 3, 9, 15 | 405 | $+1$ | 377 |
| 3 | 1 | $\{2\}$ | 2, 5, 8 | 80 | $-1$ | 297 |
| 4 | 3 | $\{2, 3\}$ | 5, 11, 17 | 935 | $+1$ | 1232 |
| 5 | 1 | $\{1, 2, 3\}$ | 6, 15, 24 | 2160 | $-1$ | $-928$ |
| 6 | 2 | $\{1, 3\}$ | 4, 10, 16 | 640 | $+1$ | $-288$ |
| 7 | 1 | $\{3\}$ | 3, 6, 9 | 162 | $-1$ | $-450$ |

Line L8 returns $(-1)^3 \cdot (-450) = 450$. The definition gives the same value: $1 \cdot (45 + 48) + 2 \cdot (36 + 42) + 3 \cdot (32 + 35) = 93 + 156 + 201 = 450$.

## Correctness

The full proof is in `proofs/correctness.md`. It has two parts.

- **The formula.** For a fixed $S$, expanding $\prod_i \sum_{j \in S} a_{ij}$ gives one term $\prod_i a_{i f(i)}$ for each map $f : [n] \to S$. So the signed sum is $\sum_f c_f \prod_i a_{i f(i)}$ over all maps $f : [n] \to [n]$, with $c_f = \sum_{S \supseteq f([n])} (-1)^{n - |S|}$. If the image $f([n])$ has $m$ elements, the sets $S$ that contain it are the image plus any subset of the other $n - m$ columns, so $c_f = \sum_{t=0}^{n-m} \binom{n-m}{t} (-1)^{n-m-t} = (1 - 1)^{n-m}$, which is 1 if $m = n$ and 0 otherwise. A map $f : [n] \to [n]$ with image of size $n$ is a permutation, so the sum is $\operatorname{per}(A)$.
- **The loop.** By the properties of the binary reflected Gray code, the set $S$ after step $k$ is the set of one bits of $k \oplus \lfloor k/2 \rfloor$ (bit $j - 1$ for column $j$), and these sets for $k = 1, \ldots, 2^n - 1$ are the nonempty subsets of $[n]$, each once. Line L6 keeps the invariant $r_i = \sum_{j \in S} a_{ij}$. So line L7 adds the term of each nonempty $S$, and the empty set adds 0.

## Complexity

- **Time.** The loop of line L3 runs $2^n - 1$ times. Each pass does $O(n)$ additions in line L6 and $n - 1$ multiplications in line L7. The total is $\Theta(2^n n)$ arithmetic operations. Computing $\rho(k)$ is one word operation with a count-trailing-zeros instruction, or $O(1)$ amortized by a loop.
- **Space.** The array $r$ and the set $S$ (a bit mask) take $\Theta(n)$ words beyond the input.
- **Bit cost.** For an integer matrix with entries of absolute value at most $M$, every row sum has absolute value at most $nM$, every product at most $(nM)^n$, and the total at most $2^n (nM)^n$. So all numbers have $O(n \log(nM))$ bits.
- **Naive order.** Recomputing the row sums for each $S$ from scratch costs $\Theta(2^n n^2)$ operations, which is the bound often quoted for Ryser's formula.

## Properties

- **Exact.** Over the integers, the algorithm uses only additions, subtractions and multiplications, so it returns the exact permanent with no division.
- **Any ring.** The proof uses only the commutative ring axioms, so the algorithm works modulo any integer, over polynomials, and over the complex numbers.
- **Cancellation.** The terms can be much larger than the result. For a 0-1 matrix, the final value can be 0 while intermediate totals are near $2^n n^n$. In floating point this loses precision.
- **Parallel.** The subsets split into blocks of consecutive Gray code ranks, and each block can start from the row sums of its first set, computed directly. The blocks run independently.

## Variants and improvements

- **Glynn's formula.** A sum over sign vectors $\delta \in \{\pm 1\}^n$ with $\delta_1 = 1$ has $2^{n-1}$ terms, half as many, with the same $O(n)$ update per term; see [Glynn's formula](/glynn-formula/).
- **Nijenhuis and Wilf.** Shifting each row sum by half the row total before the products halves the number of subsets, with a similar effect to Glynn's formula.
- **Sparse matrices.** If $A$ has few nonzero entries, the products are zero for many $S$, and branching methods that skip them are faster. For bipartite graphs of bounded treewidth, a tree decomposition gives a polynomial algorithm.
- **General graphs.** Björklund's algorithm counts perfect matchings of a general graph on $n$ vertices in $O^*(2^{n/2})$ time, which matches Ryser on bipartite graphs.

## When to use it

Use Ryser's formula, or Glynn's, to compute the exact permanent of a dense matrix of order up to about 30 to 40, or as the exact oracle for tests of approximation algorithms. For 0-1 matrices of planar bipartite graphs, [Kasteleyn's method](/kasteleyn-method/) is polynomial. For large nonnegative matrices where an estimate is enough, use the FPRAS of Jerrum, Sinclair and Vigoda. Do not use the formula for the determinant: [Gaussian elimination](/gaussian-elimination/) is polynomial.

## Pitfalls

- **The final sign.** Line L8 multiplies by $(-1)^n$. Returning `total` alone gives $-\operatorname{per}(A)$ for odd $n$; in the example it gives $-450$.
- **The sign of each term.** Line L7 uses $(-1)^{|S|}$ for the current $S$, after the change of line L5. Using the sign of $k$ or the size before the change gives a wrong sum.
- **The changing column.** Line L4 must take $j$ from the trailing zeros of $k$. Taking it from another bit of $k$, for example the highest one bit, toggles the wrong column: $S$ no longer follows the Gray code, some subsets are visited twice and others never.
- **The empty matrix.** For $n = 0$ the loop does nothing, and line L8 would return 0; line L1 returns 1, the permanent of the empty matrix.
- **Floating point.** The alternating sum cancels heavily. Use exact integers or rationals when the exact value matters.

## Implementations

## History

Herbert Ryser published the formula in 1963 in his book Combinatorial Mathematics, as an application of inclusion-exclusion. Nijenhuis and Wilf, in their book on combinatorial algorithms (1975, second edition 1978), visited the subsets in Gray code order and used a shift to halve the work. Valiant's 1979 proof that the permanent is #P-complete explained why no polynomial method has been found. Glynn gave a formula with half as many terms in 2010.

## References
