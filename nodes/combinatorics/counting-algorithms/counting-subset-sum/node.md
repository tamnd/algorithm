---
tag: QSKRPB
kind: problem
slug: counting-subset-sum
name: Counting subsets with a given sum
aliases:
- number of subset sum solutions
- '#Subset Sum'
- counting subset sum
area: combinatorics/counting-algorithms
level: intro
summary: Counts subsets of a multiset whose elements add up to a target.
prereqs: [subset-sum-problem, knapsack-dynamic-programming, generating-functions, pseudo-polynomial-time]
see_also: [horowitz-sahni-algorithm, partition-problem, knapsack-problem, subset-sum-fptas, exact-cover, convolution-via-fft, approximate-counting, fpras]
sources:
  - paper: doi:10.1145/321812.321823
    title: Ellis Horowitz and Sartaj Sahni, Computing partitions with applications to the knapsack problem, Journal of the ACM 21(2), 277 to 292, 1974
    locator: the two-list method that splits the items into two halves and sorts the sums of each half
  - paper: doi:10.1145/780542.780643
    title: Martin Dyer, Approximate counting by dynamic programming, Proceedings of the 35th ACM Symposium on Theory of Computing (STOC), 693 to 699, 2003
    locator: the randomized approximation scheme for counting knapsack solutions by rounding the weights and running the counting dynamic program
  - paper: doi:10.1137/11083976X
    title: Daniel Štefankovič, Santosh Vempala and Eric Vigoda, A deterministic polynomial-time approximation scheme for counting knapsack solutions, SIAM Journal on Computing 41(2), 356 to 366, 2012
    locator: the deterministic FPTAS for the number of subsets with weight at most C
  - url: https://oeis.org/A063865
    title: OEIS A063865, Number of solutions to +- 1 +- 2 +- 3 +- ... +- n = 0
    locator: the data, and the comment that a(n) counts the subsets of [n] with sum n(n+1)/4
---

Counting subsets with a given sum asks, for positive integers $a_1, \ldots, a_n$ and a target $T$, how many index sets $S \subseteq [n]$ satisfy $\sum_{i \in S} a_i = T$. It is the counting version of the [subset sum problem](/subset-sum-problem/). The standard method is a [dynamic program](/knapsack-dynamic-programming/) that counts the subsets of the first $i$ items with each sum $t \le T$, in $O(nT)$ additions. This is [pseudo-polynomial](/pseudo-polynomial-time/): fast when $T$ is small, but exponential in the number of bits of $T$. The answer is also the coefficient of $x^T$ in the [generating function](/generating-functions/) $\prod_i (1 + x^{a_i})$. With large numbers, the problem is #P-complete, and even deciding whether the count is positive is NP-complete.

## In plain words

You have a pile of coins with numbers written on them, and a target number. How many different handfuls of coins add up to exactly the target?

Go through the coins one at a time and keep a table. The table says, for each total from zero up to the target, how many handfuls of the coins seen so far give that total. When a new coin comes, each total can be reached in two ways: without the new coin, as before, or with it, from a total that was smaller by the coin's value. Add the two numbers. After the last coin, the entry for the target is the answer. The table is as long as the target, so this is fast for small targets and slow for very large ones.

## Definition

Notation: $[n] = \{1, \ldots, n\}$. For $S \subseteq [n]$, $a(S) = \sum_{i \in S} a_i$, with $a(\emptyset) = 0$.

**Problem.** Input: positive integers $a_1, \ldots, a_n$ (a multiset: equal values are allowed and count as different items) and an integer $T \ge 0$. Output: $N(T) = |\{S \subseteq [n] : a(S) = T\}|$.

**Recurrence.** Let $N_i(t)$ be the number of $S \subseteq [i]$ with $a(S) = t$. Then $N_0(0) = 1$, $N_0(t) = 0$ for $t \ne 0$, and for $i \ge 1$

$$N_i(t) = N_{i-1}(t) + N_{i-1}(t - a_i),$$

with $N_{i-1}(t) = 0$ for $t < 0$.

*Proof.* Split the subsets of $[i]$ with sum $t$ by whether they contain $i$. Those without $i$ are the subsets of $[i-1]$ with sum $t$. Those with $i$ are $S' \cup \{i\}$ for a subset $S'$ of $[i-1]$ with sum $t - a_i$, and this is a bijection. $\square$

**Generating function.** $\sum_t N(t) x^t = \prod_{i=1}^{n} (1 + x^{a_i})$, because expanding the product picks, for each $i$, either $1$ or $x^{a_i}$, and each choice is one subset. The recurrence is the multiplication by one factor at a time.

## Variants

- **At most $T$.** Count the subsets with $a(S) \le T$. This is #Knapsack, the number of feasible solutions of a knapsack constraint. The same table gives it as $\sum_{t \le T} N(t)$.
- **Distinct values.** If the input is a multiset and two subsets with the same multiset of values count as one, then a value $v$ with multiplicity $m$ contributes a factor $1 + x^v + \cdots + x^{mv}$ instead of $(1 + x^v)^m$.
- **Signed sums.** The number of sign choices with $\pm a_1 \pm \cdots \pm a_n = 0$ equals $N(\sigma / 2)$ where $\sigma = \sum_i a_i$: the plus signs form a subset with sum $\sigma / 2$.
- **Modular targets.** Count the subsets with $a(S) \equiv T \pmod m$. The table then has $m$ entries, indexed by residues, and the recurrence is the same with indices modulo $m$.
- **Equal halves.** The number of ways to split the items into two parts with equal sums, as in the [partition problem](/partition-problem/), is $N(\sigma / 2) / 2$ when $\sigma > 0$, since each split is counted once for each part.

## Examples

**A small table.** Let $a = (2, 3, 5, 7)$ and $T = 10$. The row after each item is $N_i(0), \ldots, N_i(10)$:

| after item | $t = 0$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| none | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $a_1 = 2$ | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $a_2 = 3$ | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| $a_3 = 5$ | 1 | 0 | 1 | 1 | 0 | 2 | 0 | 1 | 1 | 0 | 1 |
| $a_4 = 7$ | 1 | 0 | 1 | 1 | 0 | 2 | 0 | 2 | 1 | 1 | 2 |

So $N(10) = 2$: the subsets $\{2, 3, 5\}$ and $\{3, 7\}$.

**The first $n$ integers.** For $a = (1, 2, \ldots, n)$ and $T = n(n+1)/4$, the counts for $n = 0, 1, \ldots, 20$ are 1, 0, 0, 2, 2, 0, 0, 8, 14, 0, 0, 70, 124, 0, 0, 722, 1314, 0, 0, 8220, 15272 (OEIS A063865). The count is 0 unless $n(n+1)/2$ is even, that is, unless $n \equiv 0$ or $3 \pmod 4$. For $n = 3$ the two subsets are $\{3\}$ and $\{1, 2\}$.

## Known algorithms

- **Dynamic programming.** Keep one array $N[0..T]$ and, for each item, update $N[t] \mathrel{+}= N[t - a_i]$ for $t$ from $T$ down to $a_i$. Going down makes each item used at most once. This takes $O(nT)$ additions and $O(T)$ space. The counts can be as large as $2^n$, so each addition is on numbers of up to $n$ bits; modulo a prime they are word operations.
- **Meet in the middle.** Split the items into two halves of sizes $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$. List the $2^{n/2}$ subset sums of each half, sort them, and for each sum $s$ of the first half count the sums $T - s$ in the second half with two pointers, multiplying the multiplicities. This is the method of [Horowitz and Sahni](/horowitz-sahni-algorithm/), in $O(2^{n/2} n)$ time and $O(2^{n/2})$ space, and it does not depend on the size of $T$.
- **Polynomial products.** Compute $\prod_i (1 + x^{a_i}) \bmod x^{T+1}$ by multiplying the factors in a balanced tree with [FFT convolution](/convolution-via-fft/). With exact or modular counts this gives all $N(0), \ldots, N(T)$ in about $O(T \log T \log n)$ operations, which beats the plain table when $n$ is large. Modulo a prime, taking the logarithm of the product (a sum of $\log(1 + x^{a_i})$ series) and then the exponential gives about $O(T \log T)$ operations.
- **Approximate counting of #Knapsack.** Dyer (2003) gave a randomized approximation scheme that rounds the weights to a coarse scale, counts the rounded instance exactly by the dynamic program, and corrects the error by rejection sampling. Gopalan, Klivans, Meka and coauthors, and Štefankovič, Vempala and Vigoda, gave deterministic approximation schemes (FPTAS) in 2011 and 2012.

## Bounds

$0 \le N(T) \le 2^n$, and $\sum_t N(t) = 2^n$. The table method is polynomial in $n$ and in the value $T$, not in the number of bits of the input.

**Hardness of exact counting.** Counting subsets with a given sum is #P-complete. *Reduction.* Take an instance of exact cover: a ground set $U = [m]$ and nonempty sets $F_1, \ldots, F_n \subseteq U$. Let $b = n + 1$ and write each set as the number $a_j = \sum_{u \in F_j} b^{u-1}$, and set $T = \sum_{u=1}^{m} b^{u-1}$. In base $b$, a sum of at most $n$ of the $a_j$ has all digits at most $n < b$, so there are no carries, and the digit at position $u$ counts the chosen sets that contain $u$. So $a(S) = T$ exactly when each element is covered once, and the number of subsets with sum $T$ equals the number of exact covers. Counting [exact covers](/exact-cover/) is #P-complete, and this reduction is parsimonious. $\square$

**Hardness of approximation.** Whether $N(T) > 0$ is the subset sum problem, which is NP-complete. A multiplicative approximation of $N(T)$ within any factor tells whether $N(T) = 0$, so no such approximation runs in polynomial time unless P = NP (or, for randomized algorithms, NP = RP). The variant "at most $T$" is different: its count is always at least 1 (the empty set), and it has an FPRAS and an FPTAS.

## Reductions

- **To polynomial multiplication.** The count is a coefficient of a product of sparse polynomials.
- **From exact cover.** By the base-$b$ encoding above, which preserves the number of solutions.
- **To the decision problem.** $N(T) > 0$ decides [subset sum](/subset-sum-problem/), and the table method for the count is the table method for the decision with sums in place of Boolean or.

## Applications

- Combinatorial identities and partitions, for example the number of ways to sign $\pm 1 \pm 2 \cdots \pm n$ to get 0.
- Probability: the distribution of the sum of a random subset, for example the null distribution of the Wilcoxon signed-rank statistic, which is $N(t) / 2^n$ for $a = (1, \ldots, n)$.
- Counting the feasible solutions of a knapsack constraint, a building block for approximate counting and for sampling a uniform feasible solution.

## References
