---
tag: XVHXZM
kind: problem
slug: bounded-integer-solutions-counting
name: Counting integer solutions with upper bounds
aliases:
- Number of integer solutions with upper bounds
- bounded stars and bars
- bounded compositions counting
area: combinatorics/counting-algorithms
level: core
summary: Counting the nonnegative integer solutions of a linear equation with upper bounds on each variable, using inclusion-exclusion.
model: word-ram
complexity:
  vars: {n: the required sum, k: the number of variables}
  time: {worst: "O(min(2^k*k, k*n))"}
prereqs: [stars-and-bars, inclusion-exclusion-principle]
see_also: [stars-and-bars, inclusion-exclusion-principle, counting-integer-compositions, counting-subset-sum, generating-functions, prefix-sums, barvinok-algorithm, binomial-coefficient-computation]
sources:
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Chapter 6, The Inclusion-Exclusion Principle and Applications (Section 6.2, Combinations with repetition, which counts multisets and solutions with upper bounds)
  - book: isbn:9780073383095
    title: Kenneth H. Rosen, Discrete Mathematics and Its Applications, seventh edition
    locator: Section 8.6, Applications of Inclusion-Exclusion (solutions of linear equations with upper bounds)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 2, Sieve Methods (Section 2.1, Inclusion-exclusion)
---

Counting integer solutions with upper bounds asks for the number of tuples $(x_1, \ldots, x_k)$ of integers with $x_1 + \cdots + x_k = n$ and $0 \le x_i \le u_i$ for each $i$. Without the upper bounds the answer is the [stars and bars](/stars-and-bars/) count $\binom{n+k-1}{k-1}$; with them, [inclusion-exclusion](/inclusion-exclusion-principle/) over the set of broken bounds gives a sum of $2^k$ such counts, which collapses to $k + 1$ terms when all bounds are equal. A dynamic program with [prefix sums](/prefix-sums/) solves it in $O(kn)$ additions, which is better when $n$ is small and $k$ is large.

## In plain words

You share some identical candies among a few children, but each child can take at most a given number. Without the limits, the count has a simple formula. The limits make it harder, because some of the shares counted by the simple formula give a child too many.

So you count all shares, then take away the shares where one particular child gets too many, then add back the shares where two children get too many, because they were taken away twice, and so on. A second method builds the answer one child at a time: for each possible total so far, it counts the ways to reach that total, and adds the next child with each allowed amount.

## Definition

Notation: $n \ge 0$ is the required sum, $k \ge 1$ is the number of variables, $u_1, \ldots, u_k \ge 0$ are the upper bounds, $[k] = \{1, \ldots, k\}$, and $\binom{a}{b}$ or $C(a, b)$ is the [binomial coefficient](/binomial-coefficient/), $0$ when $b < 0$ or $b > a$, and also taken as $0$ here when $a < 0$.

**Input.** Integers $n$, $k$ and $u_1, \ldots, u_k$.

**Output.** $N(n; u_1, \ldots, u_k) = \bigl|\{x \in \mathbb{Z}^k : x_1 + \cdots + x_k = n,\ 0 \le x_i \le u_i \text{ for all } i\}\bigr|$.

**Cost model.** The answer is at most $\binom{n+k-1}{k-1}$, so it can have many digits. Programs compute it exactly with big integers, or modulo a prime $p$, where each operation on residues costs $O(1)$ on the [word RAM](/word-ram/).

**Theorem.** With $s(J) = \sum_{i \in J} (u_i + 1)$,
$$N(n; u_1, \ldots, u_k) = \sum_{J \subseteq [k]} (-1)^{|J|} \binom{n - s(J) + k - 1}{k - 1},$$
where terms with $n - s(J) < 0$ are $0$. If all $u_i = u$, then $N = \sum_{j \ge 0} (-1)^j \binom{k}{j}\binom{n - j(u+1) + k - 1}{k - 1}$.

*Proof.* Let $U$ be the set of nonnegative solutions of $\sum x_i = n$, and $A_i \subseteq U$ the solutions with $x_i \ge u_i + 1$. The wanted solutions are $U \setminus \bigcup A_i$. For $J \subseteq [k]$, the map $x \mapsto y$ with $y_i = x_i - (u_i + 1)$ for $i \in J$ and $y_i = x_i$ otherwise is a bijection from $A_J$ onto the nonnegative solutions of $\sum y_i = n - s(J)$. By stars and bars, $|A_J| = \binom{n - s(J) + k - 1}{k - 1}$ when $n - s(J) \ge 0$, and $A_J = \emptyset$ otherwise. The inclusion-exclusion principle gives the formula. When all $u_i = u$, $s(J) = |J|(u + 1)$ depends only on $|J|$, and there are $\binom{k}{j}$ sets $J$ of size $j$. $\square$

## Variants

- **Lower bounds too.** With $l_i \le x_i \le u_i$, substitute $x_i' = x_i - l_i$, which gives the sum $n - \sum l_i$ and bounds $u_i - l_i$.
- **Equal bounds.** All $u_i = u$: the $k + 1$ term formula. This counts the strings of length $k$ over the digits $\{0, \ldots, u\}$ with digit sum $n$, and the sums of $k$ dice.
- **At most $n$.** $\sum x_i \le n$: add a slack variable with bound $n$, or sum the answers for $0, \ldots, n$.
- **Coefficients.** With $a_1 x_1 + \cdots + a_k x_k = n$ and positive integer $a_i$, the inclusion-exclusion formula no longer has binomial terms. With $x_i \in \{0, 1\}$ the problem becomes [counting subset sums](/counting-subset-sum/), which is #P-complete when the numbers are written in binary.
- **All sums at once.** The whole distribution $N(n)$ for $n = 0, \ldots, \sum u_i$ is the coefficient list of $\prod_i (1 + z + \cdots + z^{u_i})$.

## Examples

**1. Three dice.** The number of ways three distinguishable dice show the sum 10: with $x_i = d_i - 1 \in [0, 5]$, the sum is $7$, and the formula gives $\binom{9}{2} - 3\binom{3}{2} = 36 - 9 = 27$ of the $216$ outcomes.

**2. Different bounds.** $x_1 + x_2 + x_3 = 15$ with $x_1 \le 5$, $x_2 \le 6$, $x_3 \le 7$. Here $u_i + 1 = 6, 7, 8$:

| $J$ | $n - s(J)$ | term |
|---|---|---|
| $\emptyset$ | 15 | $+\binom{17}{2} = 136$ |
| $\{1\}$, $\{2\}$, $\{3\}$ | 9, 8, 7 | $-(55 + 45 + 36) = -136$ |
| $\{1,2\}$, $\{1,3\}$, $\{2,3\}$ | 2, 1, 0 | $+(6 + 3 + 1) = 10$ |
| $\{1,2,3\}$ | $-6$ | $0$ |

The answer is $136 - 136 + 10 = 10$, which a listing of all solutions confirms.

**3. Digit sums.** The strings of 4 decimal digits with digit sum 18: $k = 4$, $u = 9$, so $\binom{21}{3} - 4\binom{11}{3} + 6\binom{1}{3} = 1330 - 660 + 0 = 670$.

**4. One bound.** 12 identical balls into 5 distinct boxes with box 1 holding at most 3: $\binom{16}{4} - \binom{12}{4} = 1820 - 495 = 1325$.

**5. The DP on example 1.** Let $f_i(s)$ be the number of ways for the first $i$ dice (shifted to $[0, 5]$) to sum to $s$. Then $f_i(s) = \sum_{t=0}^{\min(5, s)} f_{i-1}(s - t)$:

| $s$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f_0$ | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $f_1$ | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| $f_2$ | 1 | 2 | 3 | 4 | 5 | 6 | 5 | 4 |
| $f_3$ | 1 | 3 | 6 | 10 | 15 | 21 | 25 | 27 |

and $f_3(7) = 27$, as in example 1.

## Known algorithms

| method | time | space | best when |
|---|---|---|---|
| listing all tuples | $\prod_i (u_i + 1)$ | $O(k)$ | tiny inputs and tests |
| inclusion-exclusion, general bounds | $2^k$ binomials | $O(k)$ | $k$ small, $n$ and $u_i$ huge |
| inclusion-exclusion, equal bounds | $k + 1$ binomials | $O(k)$ | all bounds equal |
| DP with prefix sums | $O(kn)$ additions | $O(n)$ | $n$ moderate, $k$ large |
| polynomial product | $\prod_i (1 + \cdots + z^{u_i})$ by FFT | $O(n)$ | all values of $n$ at once |

**Inclusion-exclusion.** Each term is one binomial coefficient with lower index $k - 1$, which costs $O(k)$ operations by the product formula, or $O(1)$ after a table of factorials and inverse factorials modulo a prime; see [computing binomial coefficients](/binomial-coefficient-computation/). With a [Gray code](/gray-code/) order of the subsets $J$, $s(J)$ changes by one bound per step. With direct binomials the time is $O(2^k k)$ arithmetic operations, which does not depend on the size of $n$ except through the bit length of the numbers. With tables of factorials up to $n + k$ modulo a prime $p > n + k$, it is $O(n + k + 2^k)$.

**DP with prefix sums.** Keep the row $f_{i-1}(0), \ldots, f_{i-1}(n)$ and its prefix sums $P(s) = \sum_{r \le s} f_{i-1}(r)$. Then $f_i(s) = P(s) - P(s - u_i - 1)$, with $P$ of a negative index equal to $0$. Each row costs $O(n)$, so the total is $O(kn)$ additions and $O(n)$ space, and it needs no division, so it works modulo any number. It is a pseudo-polynomial algorithm: polynomial in the value $n$, not in its bit length.

**Fixed dimension.** The solutions are the lattice points of a polytope of dimension $k - 1$. For a fixed $k$, [Barvinok's algorithm](/barvinok-algorithm/) counts the lattice points of any rational polytope in time polynomial in the bit length of the input, which also covers general coefficients.

## Bounds

- **Output size.** $0 \le N \le \min\bigl(\binom{n+k-1}{k-1}, \prod_i (u_i + 1)\bigr)$, so an exact answer has $O(k \log(n + k))$ bits.
- **Symmetry.** With $U = \sum u_i$, $N(n) = N(U - n)$, by $x_i \mapsto u_i - x_i$. So one may assume $n \le U/2$, which removes the terms with large $s(J)$.
- **Number of nonzero terms.** Only the sets $J$ with $s(J) \le n$ contribute. With all $u_i = u$ this is $\lfloor n/(u+1) \rfloor + 1$ values of $j$.
- **Cancellation.** The terms of the alternating sum can be far larger than the answer: in example 2, the answer $10$ comes from terms of size $136$. Exact big integers or a prime modulus avoid any rounding issue; floating point does not.

## Reductions

- **To stars and bars.** Every term of the inclusion-exclusion sum is an unbounded stars and bars count after a shift.
- **From dice and digit sums.** The distribution of the sum of $k$ dice with $f$ faces, and the number of $k$-digit strings in base $b$ with a given digit sum, are the equal-bounds case with $u = f - 1$ or $u = b - 1$. The digit DP of [digit dynamic programming](/digit-dynamic-programming/) handles the version with an upper limit on the number itself.
- **From compositions with bounded parts.** Compositions of $n$ into $k$ parts in $[1, u]$ are solutions with $x_i - 1 \in [0, u - 1]$; see [counting integer compositions](/counting-integer-compositions/).
- **To polynomial multiplication.** The generating function $\prod_i \frac{1 - z^{u_i+1}}{1 - z}$ has coefficient $N(n)$ at $z^n$; expanding the numerator is exactly the inclusion-exclusion sum. See [generating functions](/generating-functions/).

## Applications

- **Probability.** Sums of dice, and the number of ways to reach a score with bounded points per round.
- **Resource allocation.** Distributing $n$ identical units among $k$ machines of limited capacity.
- **Coding theory and strings.** Strings over an alphabet of size $u + 1$ with a given weight, such as words of length $k$ with digit sum $n$.
- **Combinatorial generation.** The counts give the ranks needed to [rank and unrank](/combinatorial-ranking-and-unranking/) bounded compositions in lexicographic order.

## References
