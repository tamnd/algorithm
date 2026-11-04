---
tag: HVHZZP
kind: problem
slug: coin-change-problem
name: Coin change problem
aliases:
- change-making problem
- minimum coin change
area: techniques/dynamic-programming
level: intro
summary: Make an amount with the fewest coins, or count the ways to make it.
prereqs: [optimal-substructure, tabulation, pseudo-polynomial-time]
see_also: [coin-change-counting, canonical-coin-system, greedy-algorithm, unbounded-knapsack, knapsack-problem, subset-sum-problem, min-plus-convolution, rod-cutting-problem]
sources:
  - book: isbn:9780471924203
    title: Silvano Martello and Paolo Toth, Knapsack Problems, Algorithms and Computer Implementations, Wiley, 1990
    locator: Chapter 5 (the change-making problem)
  - paper: doi:10.1016/0304-3975(94)90134-1
    title: Dexter Kozen and Shmuel Zaks, Optimal bounds for the change-making problem, Theoretical Computer Science 123(2), 1994
    locator: pp. 377 to 388, Theorem 4 (the range of the smallest counterexample) and Section 5 (NP-hardness, after Lueker 1975)
  - paper: doi:10.1016/j.orl.2004.06.001
    title: David Pearson, A polynomial-time algorithm for the change-making problem, Operations Research Letters 33(3), 2005
    locator: pp. 231 to 234
  - paper: doi:10.1137/1.9781611976014.7
    title: Timothy M. Chan and Qizheng He, On the change-making problem, Symposium on Simplicity in Algorithms (SOSA), 2020
    locator: pp. 38 to 42
---

The coin change problem gives a set of coin values and an amount, and asks for the fewest coins whose values sum to the amount, with each value usable any number of times. Its counting form asks for the number of ways to make the amount. Both forms are solved by [dynamic programming](/tabulation/) over the amounts $0, 1, \ldots, n$ in $O(nk)$ time for $k$ coin values, which is [pseudo-polynomial](/pseudo-polynomial-time/): the minimization form is [NP-hard](/np-hard/) when the numbers are written in binary. For the coin systems of most countries the [greedy algorithm](/greedy-algorithm/) is also optimal, but not for every system.

## In plain words

A shop has coins of a few fixed values and an unlimited supply of each. It must give a customer a given amount of change and wants to hand over as few coins as possible.

The usual habit is to take the largest coin that fits, then repeat. This works for real money, but with coins of 1, 3 and 4 it fails: for 6 it gives 4, 1 and 1, while 3 and 3 is better.

The safe method fills a table. For each amount from zero upward, it tries each coin as the last coin. The rest of the amount is smaller, so its best answer is already in the table. The best of these choices, plus one coin, is the answer for the current amount.

## Definition

**Input.** A set $D = \{d_1, \ldots, d_k\}$ of distinct positive integers, the coin values, and an integer amount $n \ge 0$.

**Representation.** A vector $x = (x_1, \ldots, x_k)$ of nonnegative integers with $\sum_{i=1}^{k} x_i d_i = n$. Its size is $|x| = \sum_i x_i$, the number of coins.

**Minimization form (change making).** Output a representation of least size, or report that none exists. Write $f(n)$ for the least size, with $f(n) = \infty$ when $n$ has no representation. Then $f(0) = 0$ and, for $n \ge 1$,

$$ f(n) = 1 + \min_{d \in D,\ d \le n} f(n - d), $$

where the minimum of an empty set is $\infty$.

**Counting form.** Output the number $W(n)$ of representations, that is, of multisets of coins with sum $n$. The order of the coins does not matter. That form has its own page, [counting ways to make change](/coin-change-counting/).

## Variants

- **With a penny.** If $1 \in D$, every amount has a representation and $f(n) \le n$. Kozen and Zaks study this case.
- **Greedy test.** Decide whether the greedy rule (take the largest coin $\le$ the rest, repeat) is optimal for every amount. A system with this property is a [canonical coin system](/canonical-coin-system/).
- **Ordered sequences.** Count the sequences of coins with sum $n$, where $1, 2$ and $2, 1$ differ. The recurrence is $S(0) = 1$ and $S(n) = \sum_{d \le n} S(n - d)$.
- **Limited supply.** Coin $d_i$ may be used at most $c_i$ times. This is a [bounded knapsack](/bounded-knapsack/) with value $-1$ per coin and an exact fill.
- **All targets.** Compute $f(t)$ for every $t \le n$ at once. The table of the dynamic program gives this at no extra cost.
- **Decision form.** Given $n$ and a bound $m$, decide whether $f(n) \le m$. With $m = \infty$ it asks only whether $n$ is a sum of coins.

## Examples

**Greedy fails.** Take $D = \{1, 3, 4\}$. The table of $f$ and of the greedy count $G$:

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $f(t)$ | 0 | 1 | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 |
| $G(t)$ | 0 | 1 | 2 | 1 | 1 | 2 | 3 | 2 | 2 | 3 | 4 | 3 | 3 |

At $t = 6$ greedy takes $4 + 1 + 1$, and the optimum is $3 + 3$. At $t = 10$ greedy takes $4 + 4 + 1 + 1$, and the optimum is $4 + 3 + 3$. If the program stores for each $t$ the coin that reached the minimum, a [traceback](/traceback/) from $t = 6$ reads the coin 3, then the coin 3 for $t = 3$, then stops at $t = 0$.

**Greedy is right.** For $D = \{1, 5, 10, 25\}$ and $n = 63$, both greedy and the table give 6 coins: $25 + 25 + 10 + 1 + 1 + 1$.

**No solution.** For $D = \{2, 5\}$ the table is $f = 0, \infty, 1, \infty, 2, 1, 3, 2, 4, 3, 2, 4$ for $t = 0$ to $11$. The amounts 1 and 3 have no representation, and each amount from 4 on has one.

**Counting.** For $D = \{1, 2, 5\}$ and $n = 5$ there are $W(5) = 4$ multisets: $5$, $2 + 2 + 1$, $2 + 1 + 1 + 1$ and $1 + 1 + 1 + 1 + 1$. The number of ordered sequences is $S(5) = 9$. For $n = 100$ cents with the coins $\{1, 5, 10, 25\}$ there are $W(100) = 242$ ways, and with $\{1, 5, 10, 25, 50, 100\}$ there are 293 ways.

**The smallest counterexample.** For $D = \{1, 5, 10, 20, 25\}$, greedy first fails at 40: it gives $25 + 10 + 5$, and $20 + 20$ is better. This lies in the range $c_3 + 1 < x < c_m + c_{m-1}$ of Kozen and Zaks, here $11 < 40 < 45$.

## Known algorithms

- **Dynamic programming over amounts.** Fill $f(0), f(1), \ldots, f(n)$ in increasing order with the recurrence of the definition. Each entry looks at $k$ coins, so the time is $O(nk)$ and the space is $O(n)$. To output the coins, store the minimizing $d$ for each $t$ and follow it back. This is [tabulation](/tabulation/) of an [unbounded knapsack](/unbounded-knapsack/) with weight $d$ and value $-1$ for each coin, and an exact fill.
- **Counting by coins in the outer loop.** Set $W[0] = 1$ and $W[t] = 0$ for $t > 0$. For each coin $d$, for $t = d$ to $n$, add $W[t - d]$ to $W[t]$. After the coins $d_1, \ldots, d_j$ are done, $W[t]$ counts the multisets of these coins with sum $t$, because each multiset is counted once, with its coins in the order $d_1, \ldots, d_j$. Time $O(nk)$.
- **Greedy.** Take $x_i = \lfloor r / d_i \rfloor$ for the coins from largest to smallest, with $r$ the rest. Time $O(k)$ after sorting, and optimal exactly for canonical systems.
- **Greedy test.** Kozen and Zaks show that if greedy fails for some amount, the smallest such amount lies strictly between $c_3 + 1$ and $c_m + c_{m-1}$, where $1 = c_1 < \cdots < c_m$ are the coins, and that these bounds are tight. Testing that range gives an $O(m c_m)$ test. Pearson gives a test with $O(m^3)$ arithmetic operations, which is polynomial in the number of coins alone. It bounds the candidates for the smallest counterexample by $O(m^2)$ and tests each one in $O(m)$ operations.
- **Faster minimization.** Chan and He give a deterministic $O(n \log n \log \log n)$ algorithm and a randomized $O(n \log n)$ algorithm, both based on convolution.

## Bounds

**Correctness of the recurrence.** Let $n \ge 1$ have a representation, and let $M$ be a multiset of $f(n)$ coins with sum $n$. Pick any coin $d \in M$. Then $M$ minus one copy of $d$ has sum $n - d$, so $f(n - d) \le f(n) - 1$. Conversely, for any $d \le n$ with $f(n - d) < \infty$, a best multiset for $n - d$ plus one coin $d$ has sum $n$, so $f(n) \le 1 + f(n - d)$. Together, $f(n) = 1 + \min_d f(n - d)$. If $n$ has no representation, then no $n - d$ has one either, since adding $d$ would give one for $n$, and both sides are $\infty$. This is the [optimal substructure](/optimal-substructure/) of the problem.

**Time of the table.** $\Theta(nk)$ word operations, which is exponential in the length $O(k \log n)$ of the input. This is not known to be avoidable: the minimization form is NP-hard when the coin values and the amount are written in binary (Lueker 1975, as cited by Kozen and Zaks). The problem is [weakly NP-hard](/weak-np-hardness/), since the table is polynomial in the value of $n$.

**Near-linear time in the amount.** The bound of Chan and He, $O(n \log n \log \log n)$ deterministic, does not depend on $k$ at all, beyond reading the input.

**The greedy test.** The decision whether a given system is canonical is polynomial in $m$ by Pearson. Kozen and Zaks show that a related question, whether the greedy representation of one given amount is optimal, is coNP-complete when the numbers are in binary.

## Reductions

- **To the unbounded knapsack.** A coin of value $d$ becomes an item of weight $d$ and value $-1$, and the capacity must be filled exactly. The general [unbounded knapsack](/unbounded-knapsack/) table solves it in the same $O(nk)$ time.
- **Relation to subset sum.** The decision "is $n$ a sum of coins" is the form of [subset sum](/subset-sum-problem/) in which each number may be used any number of times.
- **To a shortest path.** Make a vertex for each amount $0, \ldots, n$ and an edge $t \to t + d$ for each coin. Then $f(n)$ is the length of a shortest path from 0 to $n$ in this [directed acyclic graph](/directed-acyclic-graph/), found by [breadth-first search](/breadth-first-search/) in $O(nk)$ time.
- **To convolution.** Let $S_j$ be the set of amounts in $[0, n]$ that are sums of at most $j$ coins. Then $S_{2j}$ is the sumset $S_j + S_j$ cut at $n$, and a sumset is a Boolean convolution, computable with the fast Fourier transform. The fast algorithms of Chan and He build on this view; see also [min-plus convolution](/min-plus-convolution/).

## Applications

- **Cash registers and vending machines.** They pay out change with the fewest coins. For a canonical system they can use greedy; for others they need the table.
- **Design of coin systems.** A mint checks that a new set of values is canonical with the tests of Kozen and Zaks or of Pearson.
- **Teaching.** The problem is the standard first example where a greedy rule fails and dynamic programming succeeds.
- **Resource units.** The same table answers questions such as the fewest standard packages, cable lengths or time slots of fixed sizes that make an exact total.

## References
