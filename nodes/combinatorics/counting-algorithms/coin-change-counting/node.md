---
tag: RVP2W2
kind: problem
slug: coin-change-counting
name: Counting ways to make change
aliases:
- coin change ways
- unbounded coin change count
- denumerants
- coin change II
area: combinatorics/counting-algorithms
level: intro
summary: Counts multisets of coins that sum to a target amount.
prereqs: [rule-of-sum, tabulation]
see_also: [coin-change-problem, integer-partition-counting, counting-integer-compositions, unbounded-knapsack, counting-subset-sum, generating-functions, pseudo-polynomial-time, linear-recurrence-nth-term]
sources:
  - book: isbn:9781568812793
    title: Herbert S. Wilf, generatingfunctionology, third edition, A K Peters, 2006
    locator: Chapter 1 and Chapter 3 (the generating function of the change-making problem and the counting of solutions of linear equations)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter IV, Section IV.3 (denumerants and the asymptotic number of ways to make change)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.1, Domino Theory and Change (the number of ways to change a dollar)
---

Counting ways to make change asks how many multisets of coins, from given denominations with unlimited supply, add up to a target amount $n$. Two ways that use the same coins in a different order count once. The standard solution is a one-dimensional [tabulation](/tabulation/) with $O(nm)$ additions for $m$ denominations, and the [generating function](/generating-functions/) $\prod_i 1/(1 - z^{d_i})$ explains it, gives the order-$\sum d_i$ linear recurrence for huge $n$, and gives the growth $n^{m-1}$. With all denominations $1, \ldots, n$ it is the partition function $p(n)$.

## In plain words

A shop has an unlimited supply of coins of a few kinds, for example 1, 5, 10 and 25 cents. You ask in how many ways it can pay out a given amount, say one dollar. Only how many coins of each kind are used matters, not the order in which they are handed over. The method works through the coin kinds one at a time and keeps, for every amount up to the target, the number of ways to pay it with the kinds seen so far.

## Definition

**Notation.** $n \ge 0$ is the target amount. $d_1, \ldots, d_m$ are distinct positive integers, the denominations, and $D = \{d_1, \ldots, d_m\}$. $C(n, k)$ is a binomial coefficient.

**Input:** $n$ and $d_1, \ldots, d_m$, and in some variants a modulus.

**Output:** the number $W_D(n)$ of tuples $(x_1, \ldots, x_m)$ of non-negative integers with $d_1 x_1 + \cdots + d_m x_m = n$. Here $x_i$ is the number of coins of value $d_i$.

**Generating function.**

$$\sum_{n \ge 0} W_D(n)\, z^n = \prod_{i=1}^{m} \frac{1}{1 - z^{d_i}}.$$

*Proof.* The factor $1/(1 - z^{d_i}) = \sum_{x \ge 0} z^{d_i x}$ records the choice of $x_i$, and the product of the factors adds the exponents. So the coefficient of $z^n$ counts the tuples with $\sum d_i x_i = n$. $\square$

**The recurrence.** Let $W_j(a)$ count the ways to pay $a$ with the first $j$ denominations. Then $W_0(a) = [a = 0]$, and for $j \ge 1$,

$$W_j(a) = W_{j-1}(a) + W_j(a - d_j),$$

with $W_j(a) = 0$ for $a < 0$. *Proof.* By the [rule of sum](/rule-of-sum/), split the ways by whether they use a coin of value $d_j$. Those with no such coin are counted by $W_{j-1}(a)$. Removing one coin $d_j$ from the others is a bijection onto the ways to pay $a - d_j$ with the first $j$ denominations. $\square$

## Variants

- **Ordered payments.** If the order of the coins matters, the count is the number of compositions of $n$ with parts in $D$, which satisfies $c(a) = \sum_i c(a - d_i)$. See [counting integer compositions](/counting-integer-compositions/). In code, the two differ only in the order of the two loops, which is a common bug.
- **Limited supply.** If coin $i$ may be used at most $b_i$ times, the factor becomes $(1 - z^{d_i (b_i + 1)})/(1 - z^{d_i})$. The table update becomes $W_j(a) = W_{j-1}(a) + W_j(a - d_j) - W_{j-1}(a - d_j(b_j + 1))$, still $O(nm)$. With $b_i = 1$ this is [counting subset sums](/counting-subset-sum/).
- **Fewest coins.** The optimization version, the minimum number of coins, is the [coin change problem](/coin-change-problem/).
- **All denominations.** With $D = \{1, \ldots, n\}$, $W_D(n) = p(n)$, the [partition function](/integer-partition-counting/).
- **Huge amounts.** For a fixed small set $D$ and $n$ up to $10^{18}$, compute $W_D(n)$ modulo a prime or exactly with the methods below.
- **Fixed number of coins.** Count the ways that use exactly $k$ coins: add a second variable $u$ for the coin count, with the product $\prod_i 1/(1 - u z^{d_i})$, and a two-dimensional table.

## Examples

**Example 1.** With coins $1, 2, 5$ there are 4 ways to pay $5$: $5$, $2 + 2 + 1$, $2 + 1 + 1 + 1$ and $1 + 1 + 1 + 1 + 1$. The counts for $n = 0$ to $20$ are $1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14, 16, 18, 20, 22, 24, 26, 29$ (OEIS A000115).

**Example 2: a dollar.** With the US coins of 1, 5, 10 and 25 cents there are 242 ways to change a dollar (OEIS A001299). Adding the half dollar gives 292 ways (OEIS A001300), and adding the dollar coin itself gives 293.

**Example 3: the table.** For coins $1, 2, 5$ and $n = 7$, the rows of the table after each coin are:

| coins used | $a = 0$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| none | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $\{1\}$ | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| $\{1, 2\}$ | 1 | 1 | 2 | 2 | 3 | 3 | 4 | 4 |
| $\{1, 2, 5\}$ | 1 | 1 | 2 | 2 | 3 | 4 | 5 | 6 |

**Example 4: amounts with no way.** With coins $3$ and $5$, the amounts $1, 2, 4, 7$ have no way to be paid, and every amount from $8$ on has at least one. The largest amount with no way is the Frobenius number, here $3 \cdot 5 - 3 - 5 = 7$.

## Known algorithms

**One-dimensional table.** Keep one array $w[0 \ldots n]$ with $w[0] = 1$. For each denomination $d$, run $a$ from $d$ up to $n$ and set $w[a] \leftarrow w[a] + w[a - d]$. Because $a$ increases, $w[a - d]$ already counts the ways that use coin $d$, which is the recurrence for $W_j$. This uses $mn$ additions and $O(n)$ memory. It is pseudo-polynomial: with $n$ written in binary, the time is exponential in the input length (see [pseudo-polynomial time](/pseudo-polynomial-time/)).

- *Exact cost.* $W_D(n) \le C(n + m, m)$, which has $O(m \log n)$ bits for $m \le n$, so the exact bit cost is $O(n m^2 \log n)$.
- *Modulo a prime.* $O(nm)$ word operations.

**Linear recurrence for huge $n$.** The denominator $Q(z) = \prod_i (1 - z^{d_i})$ has degree $L = \sum_i d_i$, so $W_D$ satisfies a linear recurrence of order $L$ with the coefficients of $Q$. Compute the first $L$ values with the table, then get $W_D(n)$ with the [n-th term of a linear recurrence](/linear-recurrence-nth-term/) in $O(L^2 \log n)$ operations, or $O(L \log L \log n)$ with fast polynomial multiplication. For the coins $1, 5, 10, 25, 50$, $L = 91$.

**Quasi-polynomial.** For fixed $D$, $W_D(n)$ is a quasi-polynomial in $n$ of degree $m - 1$: a polynomial whose coefficients depend on $n$ modulo $\operatorname{lcm}(D)$. Computing it once, by interpolation on $m$ values in each residue class, gives every later value in $O(m)$ operations on numbers of $O(m \log n)$ bits.

**Power series.** For a long prefix modulo a suitable prime, multiply the sparse numerator out and invert $Q(z)$ by [power series inversion](/power-series-inversion/), in $O(n \log n)$ operations. This beats the table when $m$ is large.

## Bounds

- **Growth for fixed coins.** If $\gcd(d_1, \ldots, d_m) = 1$, then $W_D(n) \sim \frac{n^{m-1}}{(m-1)!\, d_1 d_2 \cdots d_m}$ as $n \to \infty$ (Schur's theorem; Flajolet and Sedgewick, Section IV.3). For the coins $1, 5, 10, 25, 50$ and $n = 10^5$, the ratio of the true count to this formula is $1.0019$. If the gcd $g$ is larger than 1, $W_D(n) = 0$ unless $g$ divides $n$.
- **Upper bound.** Every $d_i \ge 1$, so each counted tuple has $\sum_i x_i \le n$. There are $C(n + m, m)$ tuples of non-negative integers with this property, so $W_D(n) \le C(n + m, m)$, and the count has $O(m \log(n + m))$ bits.

## Reductions

- Counting integer partitions of $n$ is this problem with $D = \{1, \ldots, n\}$, so the pentagonal recurrence beats the table there.
- Counting solutions of $d_1 x_1 + \cdots + d_m x_m = n$ in non-negative integers is exactly this problem, so it is a special case of [lattice point counting](/lattice-point-counting/) in a simplex.
- The ordered version is counting paths from $0$ to $n$ in the DAG with edges $a \to a + d_i$. The unordered version counts such paths with non-decreasing edge labels.
- The table is the counting form of the [unbounded knapsack](/unbounded-knapsack/) recurrence, with addition in place of maximum.

## Applications

- **Teaching dynamic programming.** It is a standard first example of a counting DP, and of the difference between counting multisets and counting sequences.
- **Integer programming.** It counts the feasible points of a single equality constraint, which is a check for enumeration code.
- **Number theory.** The amounts with $W_D(n) = 0$ are the gaps of the numerical semigroup generated by $D$, and the largest one is the Frobenius number.
- **Combinatorial identities.** Changing the denominations turns the problem into counts of partitions with restricted parts, such as parts in $\{1, 2\}$, whose count is $\lfloor n/2 \rfloor + 1$.

## References
