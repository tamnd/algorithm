---
tag: W8GV6X
kind: definition
slug: canonical-coin-system
name: Canonical coin system
aliases:
- canonical coin denominations
- greedy coin system
area: techniques/greedy
level: intro
summary: A coin system for which the greedy largest-coin-first rule gives an optimal change for every amount.
prereqs: [coin-change-problem, greedy-algorithm]
see_also: [coin-change-problem, unbounded-knapsack, greedy-choice-property, knapsack-problem, coin-change-counting, pseudo-polynomial-time]
sources:
  - paper: doi:10.1016/0304-3975(94)90134-1
    title: Dexter Kozen and Shmuel Zaks, Optimal bounds for the change-making problem, Theoretical Computer Science 123(2), 1994
    locator: pages 377 to 388
  - paper: doi:10.1016/j.orl.2004.06.001
    title: David Pearson, A polynomial-time algorithm for the change-making problem, Operations Research Letters 33(3), 2005
    locator: pages 231 to 234
  - paper: doi:10.1287/opre.23.2.207
    title: M. J. Magazine, G. L. Nemhauser and L. E. Trotter, When the greedy solution solves a class of knapsack problems, Operations Research 23(2), 1975
    locator: pages 207 to 217
  - paper: doi:10.1145/321556.321567
    title: S. K. Chang and A. Gill, Algorithmic solution of the change-making problem, Journal of the ACM 17(1), 1970
    locator: pages 113 to 122
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Problem 16-1, Coin changing
---

A coin system is canonical if, for every amount, the greedy rule that repeatedly takes the largest coin that fits uses the fewest coins. The coins of the euro and of the United States are canonical, so a cashier who gives change greedily gives the fewest coins. Many systems are not canonical: with coins 1, 3 and 4, greedy pays 6 as $4 + 1 + 1$, while $3 + 3$ uses two coins. Whether a system is canonical can be decided in $O(n^3)$ time for $n$ coins.

## Definition

**Coin systems.** A coin system is a finite set of positive integers $c_1 < c_2 < \cdots < c_n$ with $c_1 = 1$. The coin $1$ makes every amount payable. A *representation* of an amount $x \ge 0$ is a vector $(a_1, \ldots, a_n)$ of nonnegative integers with $\sum_i a_i c_i = x$, and its size is $\sum_i a_i$, the number of coins.

**Greedy and optimal.** The *greedy representation* $G(x)$ takes $a_n = \lfloor x / c_n \rfloor$ coins of the largest value, then pays the rest $x - a_n c_n$ greedily with the smaller coins. Let $|G(x)|$ be its size, and let $M(x)$ be the least size of any representation of $x$, the answer of the [change-making problem](/coin-change-problem/).

**Canonical.** The system is *canonical* if $|G(x)| = M(x)$ for every amount $x \ge 0$. A *counterexample* is an amount $x$ with $|G(x)| > M(x)$.

**Small systems.** Every system with $n \le 2$ coins is canonical, because $\{1, c_2\}$ forces $\lfloor x / c_2 \rfloor$ coins of $c_2$ in any optimal representation. For three coins $\{1, a, b\}$ with $b = q a + r$ and $0 \le r < a$, the system is not canonical exactly when $0 < r < a - q$.

**Divisible systems are canonical.** *If each coin divides the next one, the system is canonical.* Proof: take an optimal representation $(a_1, \ldots, a_n)$ of $x$. For $i < n$, $a_i < c_{i+1} / c_i$, because $c_{i+1} / c_i$ coins of value $c_i$ can be replaced by one coin $c_{i+1}$. Then the coins below $c_{i+1}$ add up to at most $\sum_{l \le i} (c_{l+1} / c_l - 1)\, c_l = \sum_{l \le i} (c_{l+1} - c_l) = c_{i+1} - 1$. So $a_n$ is $\lfloor x / c_n \rfloor$, and by the same bound at each level, each $a_i$ is the greedy choice. The optimal representation is the greedy one. $\square$

**Where counterexamples lie (Kozen and Zaks, 1994).** If a system with $n \ge 3$ coins is not canonical, its smallest counterexample $x$ satisfies
$$ c_3 + 1 < x < c_n + c_{n-1}. $$
Kozen and Zaks show that both ends of this range are tight. With this bound, canonicity can be tested by computing $M(x)$ for all $x < c_n + c_{n-1}$ by dynamic programming, in $O(n\, c_n)$ time. This is polynomial in the values but exponential in their number of bits. Chang and Gill (1970) gave the first such test, with a larger range.

**Pearson's test (2005).** Write the coins in decreasing order, $d_1 > d_2 > \cdots > d_n = 1$. Pearson proved that the smallest counterexample, if there is one, has an optimal representation of a special form: for some $1 < i \le j \le n$, take the greedy representation of $d_{i-1} - 1$, keep its entries for $d_1, \ldots, d_{j-1}$, add 1 to its entry for $d_j$, and set the entries after $d_j$ to 0. There are $O(n^2)$ pairs $(i, j)$. For each one, compute the amount $w$ of the candidate and compare the size of the candidate with $|G(w)|$ in $O(n)$ time. The system is canonical if and only if no candidate is smaller than the greedy representation of its amount. The total is $O(n^3)$ time, polynomial in the size of the input.

**Adding one coin (Magazine, Nemhauser and Trotter, 1975).** Let $c_1 < \cdots < c_n$ be canonical, let $c_{n+1} > c_n$ be a new coin, and let $m = \lceil c_{n+1} / c_n \rceil$. Then the system with $c_{n+1}$ is canonical if and only if $1 + |G(m c_n - c_{n+1})| \le m$, where $G$ is the greedy representation in the old system. The test compares two ways to pay $m c_n$: $m$ coins of value $c_n$, and the new coin plus change for the rest.

## Examples and non-examples

**Euro coins.** In cents, $\{1, 2, 5, 10, 20, 50, 100, 200\}$ is canonical. No amount below $200 + 100$ is a counterexample, which by the bound of Kozen and Zaks covers all amounts.

**United States coins.** $\{1, 5, 10, 25\}$ is canonical. Here $25 = 2 \cdot 10 + 5$, so it is not a divisible system, and the bound of Kozen and Zaks reduces the check to amounts below 35.

**Powers of two.** $\{1, 2, 4, \ldots, 2^k\}$ is canonical, because each coin divides the next. The greedy representation is the binary expansion of $x$.

**Coins 1, 3, 4.** Not canonical. The smallest counterexample is 6: greedy gives $4 + 1 + 1$, three coins, and $3 + 3$ uses two. Here $4 = 1 \cdot 3 + 1$, so $q = 1$, $r = 1$, and $0 < 1 < 3 - 1$ as the three-coin rule says.

**Coins 1, 10, 25.** Not canonical. For 30, greedy gives $25 + 5 \cdot 1$, six coins, and $10 + 10 + 10$ uses three. With the coin 5 added, $\{1, 5, 10, 25\}$ is canonical again.

**Old British coins.** In pence, $\{1, 3, 6, 12, 24, 30\}$, the penny, threepence, sixpence, shilling, florin and half crown. Not canonical: greedy pays 48 as $30 + 12 + 6$, three coins, and two florins $24 + 24$ use two. The smallest counterexample is 48, inside the range $7 < x < 54$ of Kozen and Zaks.

**Coins 1, 5, 10, 20, 25.** Not canonical. The smallest counterexample is 40: greedy gives $25 + 10 + 5$, and $20 + 20$ uses two coins.

**Canonical is not inherited.** $\{1, 2, 10, 11, 20\}$ is canonical, but its subset $\{1, 2, 10, 11\}$ is not: it pays 20 greedily as $11 + 2 + 2 + 2 + 2 + 1$, six coins, while $10 + 10$ uses two. Adding a coin can repair a system, and removing one can break it.

## Related definitions

- **Change-making problem.** Given a system and an amount $x$, find $M(x)$ and an optimal representation. This is the [coin change problem](/coin-change-problem/), solved by dynamic programming in $O(n x)$ time for any system, and by the greedy rule in $O(n)$ time for canonical systems.
- **Counting representations.** The number of representations of $x$, regardless of size, is a different problem; see [coin change counting](/coin-change-counting/).
- **Unbounded knapsack.** Change-making is a special case of the [unbounded knapsack](/unbounded-knapsack/) problem with an exact capacity, where each coin has weight $c_i$ and cost 1.
- **Greedy choice property.** A canonical system is one where the change-making problem has the [greedy choice property](/greedy-choice-property/) for every amount: some optimal representation uses the largest coin that fits.

## References
