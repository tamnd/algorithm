---
tag: YB6SSK
kind: problem
slug: greater-than-problem
name: Greater-than problem
aliases:
- GT
- comparison problem
area: complexity/communication-and-query-complexity
level: advanced
summary: Alice and Bob decide whether Alice's n-bit number is larger than Bob's. Deterministic cost is n + 1 bits, and randomized cost is Θ(log n), even with public coins.
prereqs: [deterministic-communication-complexity, equality-problem]
see_also: [equality-problem, equality-testing-protocol, randomized-communication-complexity, fooling-set-method, log-rank-lower-bound, binary-search, index-problem, one-way-communication-complexity]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1, Basics (fooling sets and rank), and Chapter 3, Randomization
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 3, Randomized Protocols (section Some Protocols)
  - paper: doi:10.1137/S0097539791195877
    title: "Uriel Feige, Prabhakar Raghavan, David Peleg and Eli Upfal, Computing with noisy information, SIAM Journal on Computing 23(5) (1994), pages 1001-1018"
    locator: binary search when each comparison is wrong with a constant probability, which gives the O(log n) protocol
  - paper: doi:10.1007/s00493-014-3078-3
    title: "Emanuele Viola, The communication complexity of addition, Combinatorica 35(6) (2015), pages 703-747 (SODA 2013)"
    locator: the lower bound Omega(log n) for greater-than with public coins
---

The greater-than problem asks Alice, who holds an $n$-bit number $x$, and Bob, who holds an $n$-bit number $y$, to decide whether $x > y$. Deterministic protocols need $n + 1$ bits, as for the [equality problem](/equality-problem/), but the randomized cost is $\Theta(\log n)$ even with public coins, where equality costs only $O(1)$. The upper bound is a binary search for the first bit where $x$ and $y$ differ, with randomized equality tests on prefixes; the matching public-coin lower bound is due to Viola (2015).

## In plain words

Two people each hold a whole number written with the same number of binary digits. They want to know if the first number is the larger one, by sending as few bits as they can.

To compare two numbers, you look for the first digit where they differ. The number with a one there is larger. So the task is to find that first difference.

If the answer must be certain, one person must send the whole number. With a small chance of error, the two people can search for the first difference by halves. At each step they check whether the first halves of what is left are equal, with a short random test. A search by halves takes few steps, so the talk is short.

## Definition

Fix $n \ge 1$. Read $x = x_1 x_2 \ldots x_n$ and $y = y_1 y_2 \ldots y_n$ as numbers in binary, with $x_1$ the most significant bit, so $x, y \in \{0, 1, \ldots, 2^n - 1\}$.

**Instance:** a number $x$ with $n$ bits, known only to Alice, and a number $y$ with $n$ bits, known only to Bob. Both know $n$.

**Question:** is $x > y$?

The function is $\mathrm{GT}_n(x, y) = 1$ if $x > y$ and $0$ otherwise. The model is the two-party [communication model](/communication-model/), and the measure is the number of bits sent on the worst input, with both players informed of the answer. Randomized protocols must be correct with probability at least $2/3$ on every input. The [communication matrix](/communication-matrix/) is strictly lower triangular, with rank $2^n - 1$ over the reals.

## Variants

- **Greater or equal.** $x \ge y$ has the same costs, since $x \ge y$ exactly when not $y > x$, with the roles swapped.
- **Three-way comparison.** Output one of $x < y$, $x = y$, $x > y$. It costs at most two calls of $\mathrm{GT}$ and has the same asymptotic costs.
- **Numbers in a range.** For $x, y \in \{0, \ldots, N - 1\}$, replace $n$ by $\lceil \log_2 N \rceil$. The randomized cost is then $\Theta(\log \log N)$.
- **Few rounds.** Restricting the number of rounds raises the cost. A one-way protocol from Alice to Bob needs $\Omega(n)$ bits even with randomness (see "Reductions"), so $\mathrm{GT}$ separates one-way and two-way randomized protocols. See [one-way communication complexity](/one-way-communication-complexity/).
- **Addition.** Decide whether $x + y \ge t$ for a fixed $t$, or compare $x + y$ with a third number. Viola's paper studies these forms, also with more than two players.

## Examples

For $n = 2$, the numbers are $0, 1, 2, 3$, and

$$M_{\mathrm{GT}} = \begin{pmatrix} 0&0&0&0 \\ 1&0&0&0 \\ 1&1&0&0 \\ 1&1&1&0 \end{pmatrix},$$

with rows for $x$ and columns for $y$. The instance $x = 10$, $y = 01$ is a yes-instance: the first bit where they differ is bit 1, and $x_1 = 1$. The instance $x = 01$, $y = 01$ is a no-instance.

For $n = 8$, take $x = 10110100$ and $y = 10101111$. The longest common prefix is $101$, of length 3, and $x_4 = 1 > 0 = y_4$, so $x > y$. A search by halves finds this position by equality tests on the prefixes of lengths 4, 2 and 3, in that order.

An exhaustive search over all protocol trees confirms $D^{cc}(\mathrm{GT}_n) = n + 1$ for $n = 1, 2, 3$.

## Known algorithms

- **Trivial protocol.** Alice sends $x$, and Bob sends the answer: $n + 1$ bits, deterministic, the best possible.
- **Binary search with equality tests.** The players binary search for the length of the longest common prefix of $x$ and $y$, testing each candidate prefix with a public-coin equality test. With each test repeated until its error is $1/(3 \lceil \log_2 n \rceil)$, the cost is $O(\log n \log \log n)$; see [binary search](/binary-search/) and the [randomized equality testing protocol](/equality-testing-protocol/).
- **Noisy binary search.** Binary search that tolerates a constant error in each comparison, by the method of Feige, Raghavan, Peleg and Upfal (1994), needs only $O(\log n)$ equality tests of constant cost, for $O(\log n)$ bits in all.

## Bounds

| Model | Cost of $\mathrm{GT}_n$ | Source of the lower bound |
|---|---|---|
| Deterministic, $D^{cc}$ | $n + 1$ | [fooling sets](/fooling-set-method/) of sizes $2^n - 1$ and $2^n$, or the [log-rank bound](/log-rank-lower-bound/) |
| Nondeterministic, $N^1$ and $N^0$ | $n$ each, for $n \ge 2$ | the same fooling sets |
| Randomized, private coins | $\Theta(\log n)$ | $R(f) = \Omega(\log D^{cc}(f))$ for private coins |
| Randomized, public coins | $\Theta(\log n)$ | Viola (2015) |
| One-way randomized | $\Theta(n)$ | reduction from augmented index |

The deterministic lower bound uses two fooling sets. The pairs $(x, x - 1)$ for $1 \le x \le 2^n - 1$ form a 1-fooling set, and the pairs $(x, x)$ form a 0-fooling set. Together they force $2^{n+1} - 1$ leaves, so $D^{cc}(\mathrm{GT}_n) \ge \lceil \log_2(2^{n+1} - 1) \rceil = n + 1$.

Unlike equality, $\mathrm{GT}$ is hard for nondeterminism on both sides: the 1-entries and the 0-entries each need about $2^n$ rectangles in any cover.

The public-coin lower bound is harder than the private-coin one, because public coins make equality cost $O(1)$, so a lower bound must use the order. Viola proved the tight bound $\Omega(\log n)$, improving earlier bounds of order $\sqrt{\log n}$.

## Reductions

- **From equality.** $x = y$ exactly when $\mathrm{GT}(x, y) = 0$ and $\mathrm{GT}(y, x) = 0$. So a protocol for $\mathrm{GT}$, run twice with the roles of the players swapped, solves the [equality problem](/equality-problem/). With private coins this gives $R(\mathrm{GT}_n) = \Omega(\log n)$.
- **From augmented index.** In augmented index, Alice holds $x \in \{0,1\}^n$, and Bob holds an index $i$ and the bits $x_1, \ldots, x_{i-1}$; Bob must output $x_i$. Bob forms $y = x_1 \ldots x_{i-1} 1 0 \ldots 0$. Then $x \ge y$ exactly when $x_i = 1$. So a one-way protocol for $x \ge y$ solves augmented index, which needs $\Omega(n)$ bits one-way. See the [index problem](/index-problem/).
- **To equality on prefixes.** $\mathrm{GT}$ reduces to $O(\log n)$ adaptive equality tests on prefixes, which is the base of the randomized upper bound.

## Applications

- **Comparisons in distributed systems.** Deciding which of two remote counters, timestamps or version numbers is larger.
- **Secure comparison.** The millionaires' problem of secure computation asks for $\mathrm{GT}$ while hiding the inputs; communication bounds for $\mathrm{GT}$ bound such protocols from below.
- **Lower bounds by reduction.** Data structure problems that contain a comparison, such as predecessor search in the [cell-probe model](/cell-probe-model/), get lower bounds from communication problems built on comparisons and from their round lower bounds.
- **A separation.** $\mathrm{GT}$ shows that public coins cannot always give constant cost where private coins give $\Theta(\log n)$, unlike equality.

## References
