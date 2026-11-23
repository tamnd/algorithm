---
tag: 6G5Z3M
kind: algorithm
slug: binary-tree-mechanism
name: Binary tree mechanism
aliases:
- tree aggregation for continual counting
- continual observation counter
area: security-and-privacy/differential-privacy
level: advanced
summary: Releases a running count of a bit stream at every step. It adds noise to the dyadic partial sums and adds at most log T of them, so the error grows only as a polylog of T.
model: real-ram
complexity:
  vars: {T: the length of the stream}
  time: {worst: O(T log T)}
  space: {extra: O(log T)}
history:
  year: 2010
  people: [T.-H. Hubert Chan, Elaine Shi, Dawn Song, Cynthia Dwork, Moni Naor, Toniann Pitassi, Guy N. Rothblum]
  note: Chan, Shi and Song (ICALP 2010) and Dwork, Naor, Pitassi and Rothblum (STOC 2010) found the mechanism at the same time.
prereqs: [differential-privacy-definition, global-sensitivity, laplace-mechanism, post-processing-theorem]
see_also: [fenwick-tree, prefix-sums, segment-tree, matrix-mechanism, private-query-release, sparse-vector-technique, sequential-composition-theorem, parallel-composition-theorem]
sources:
  - paper: "T.-H. Hubert Chan, Elaine Shi and Dawn Song, Private and continual release of statistics, ICALP 2010; full version in ACM Transactions on Information and System Security 14(3), 2011"
    locator: the binary mechanism, its error bound, and the hybrid mechanism for streams of unknown length
  - paper: "Cynthia Dwork, Moni Naor, Toniann Pitassi and Guy N. Rothblum, Differential privacy under continual observation, STOC 2010, pages 715 to 724"
    locator: the tree counter for event-level privacy and the lower bound of order log T on the error
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012"
    locator: the attack on floating-point Laplace noise and the snapping defense
---

The binary tree mechanism releases, at each time $t$ of a stream of bits, a private count of the ones seen so far. To add fresh Laplace noise to each count would cost privacy at every step. To add noise to each bit and sum gives error of order $\sqrt{t}$. The tree mechanism keeps noisy sums over dyadic blocks of time, the same blocks as a [Fenwick tree](/fenwick-tree/). Each count is a sum of at most $\log_2 T + 1$ of them, and each bit is in at most $\log_2 T + 1$ of them. So the error is polylogarithmic in $T$ and the whole output stream is $\varepsilon$-differentially private. It is the base of continual release, and of the private optimizers that add noise to running sums of gradients.

## In plain words

A counter at a door must post the number of visitors each minute, but no single visit may show. If it posts the true count plus new noise each minute, an observer can average the posts and remove the noise. If it adds noise to each visit and posts the sum, the noise piles up.

The tree mechanism groups the minutes into blocks: blocks of 1 minute, of 2, of 4, of 8, and so on. It adds noise one time to the total of each block when the block ends. To post the count at a minute, it adds the few block totals that cover the time so far. A visit is in only a few blocks, and each count uses only a few blocks. So the noise stays small and the privacy cost is small.

## The problem

The input is a stream $\sigma(1), \ldots, \sigma(T)$ with $\sigma(t) \in \{0, 1\}$ and a known length $T$. At each time $t$ the mechanism must output an estimate $s_t$ of the count $c_t = \sum_{s \le t} \sigma(s)$, using only $\sigma(1), \ldots, \sigma(t)$. Two streams are neighbors if they have the same length and differ at one time step (event-level privacy, replace one item). The goal is that the whole output sequence $(s_1, \ldots, s_T)$ is $\varepsilon$-DP, with a small error $\max_t |s_t - c_t|$.

$\mathrm{Lap}(b)$ is the Laplace distribution with density $\frac{1}{2b} e^{-|z|/b}$. It has variance $2b^2$, and $P(|Z| > t) = e^{-t/b}$.

## The algorithm

Let $L = \lfloor \log_2 T \rfloor + 1$ be the number of bits of $T$. The node closed at time $u$ is the interval $(u - 2^i, u]$, where $2^i$ is the lowest one bit of $u$. The mechanism keeps one exact partial sum $a_j$ and one noisy partial sum $\hat a_j$ for each level $j < L$.

```pseudo id=main
BINARY-TREE-COUNTER(σ(1..T), ε)
L1  L ← ⌊log₂ T⌋ + 1                        ▷ the number of levels
L2  for t ← 1 to T do
L3      i ← the index of the lowest 1 bit of t
L4      aᵢ ← σ(t) + Σ_{j<i} aⱼ               ▷ the node (t − 2ⁱ, t] closes now
L5      for j ← 0 to i − 1 do aⱼ ← 0, âⱼ ← 0
L6      âᵢ ← aᵢ + Lap(L/ε)                   ▷ noise one time for each node
L7      output sₜ ← Σ_{j : bit j of t is 1} âⱼ
```

Line L3 finds the level of the node that closes at time $t$. Line L4 merges the $i$ smaller nodes below it, which together cover $(t - 2^i, t - 1]$, and adds the new item. Line L5 clears the merged levels. Line L6 adds the noise, one time for each node. Line L7 writes $t$ in binary and adds one noisy node for each one bit. For $t = 6 = 110_2$ these are the nodes $(0, 4]$ and $(4, 6]$.

## Example

Take $T = 8$, $\varepsilon = 1$ and the stream $1, 0, 1, 1, 0, 1, 1, 1$. Then $L = 4$ and each node gets $\mathrm{Lap}(4)$ noise. The run of the code with `random.Random(1)` gives the values below, rounded to two places.

| $t$ | $\sigma(t)$ | $i$ | node | exact node | noisy node | nodes used in L7 | $s_t$ | $c_t$ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 0 | $(0, 1]$ | 1 | $-4.26$ | $(0,1]$ | $-4.26$ | 1 |
| 2 | 0 | 1 | $(0, 2]$ | 1 | 5.75 | $(0,2]$ | 5.75 | 1 |
| 3 | 1 | 0 | $(2, 3]$ | 1 | 4.00 | $(0,2], (2,3]$ | 9.75 | 2 |
| 4 | 1 | 2 | $(0, 4]$ | 3 | 0.31 | $(0,4]$ | 0.31 | 3 |
| 5 | 0 | 0 | $(4, 5]$ | 0 | $-0.04$ | $(0,4], (4,5]$ | 0.27 | 3 |
| 6 | 1 | 1 | $(4, 6]$ | 1 | 0.57 | $(0,4], (4,6]$ | 0.88 | 4 |
| 7 | 1 | 0 | $(6, 7]$ | 1 | 2.45 | $(0,4], (4,6], (6,7]$ | 3.33 | 5 |
| 8 | 1 | 3 | $(0, 8]$ | 6 | 9.45 | $(0,8]$ | 9.45 | 6 |

The time step 1 is in the four nodes $(0,1]$, $(0,2]$, $(0,4]$ and $(0,8]$, which is why the scale is $L/\varepsilon = 4$. The release at $t = 7$ uses three nodes, so its variance is $3 \cdot 2 \cdot 4^2 = 96$. The other releases use one or two nodes, with variance 32 or 64. At this small $T$ the noise is larger than the counts. The method pays off for long streams: for $T = 2^{20}$ the variance is at most $2 \cdot 21^3 = 18522$, a standard error of about 136, while Laplace noise on each bit gives a variance of $2t$, about $2.1 \cdot 10^6$ at $t = T$.

## Correctness

**Exact sums (a theorem).** With the noise set to 0, the output at time $t$ is $c_t$. The invariant: after step $t$, for each one bit $j$ of $t$, $a_j$ is the exact sum over the node of level $j$ in the binary form of $t$, and $a_j = 0$ for each zero bit. Line L4 keeps it because the nodes of the low bits of $t - 1$ partition $(t - 2^i, t - 1]$.

**Privacy (a theorem).** Each time step lies in at most one node of each level, so in at most $L$ nodes. A change at one time step changes the vector of node values by at most $L$ in $\ell_1$ norm. So the vector of noisy nodes, with $\mathrm{Lap}(L/\varepsilon)$ on each, is $\varepsilon$-DP by the [Laplace mechanism](/laplace-mechanism/). The outputs are sums of noisy nodes, so they are $\varepsilon$-DP by [post-processing](/post-processing-theorem/).

**Error (a theorem).** The error at time $t$ is a sum of $\mathrm{popcount}(t) \le L$ independent $\mathrm{Lap}(L/\varepsilon)$ draws. It has mean 0 and variance $2\,\mathrm{popcount}(t)\,L^2/\varepsilon^2$. By the union bound, all $T$ errors are at most $L^2 \ln(T/\beta)/\varepsilon$ with probability at least $1 - \beta$. The full proofs are in proofs/correctness.md.

## Complexity

In the [real-RAM model](/real-ram/) with one Laplace draw at unit cost:

- Each step adds at most $L$ values in line L4 and at most $L$ values in line L7. So a step costs $O(\log T)$, and the whole stream $O(T \log T)$.
- The state is the $2L$ values $a_j$ and $\hat a_j$, so the extra space is $O(\log T)$.
- Each step draws one Laplace value.

Line L4 adds $i$ values at time $t$, and the sum of $i$ over all $t \le T$ is less than $T$. So line L4 costs $O(1)$ amortized, and line L7 sets the $O(\log T)$ cost of one step.

## Properties

- **Online.** The release at time $t$ uses only nodes that are closed by time $t$, so it uses only $\sigma(1), \ldots, \sigma(t)$.
- **Unbiased.** Each $s_t$ has mean $c_t$.
- **Event-level privacy.** The guarantee is for neighbors that differ at one time step. If one person adds many items to the stream, group privacy over that number of steps applies, and the cost grows with it.
- **Consistent noise.** A node's noise is drawn one time and reused. So the releases are correlated: for example $s_5 - s_4$ is the noisy node $(4, 5]$.
- **Pure DP.** With Laplace noise the mechanism is $(\varepsilon, 0)$-DP. With Gaussian noise of scale set by the $\ell_2$ sensitivity $\sqrt{L}$, it is $(\varepsilon, \delta)$-DP, as in the [Gaussian mechanism](/gaussian-mechanism/).

## Variants and improvements

- **Unknown $T$.** The hybrid mechanism of Chan, Shi and Song runs a new tree for each block of length $2^k$, and a separate counter over the block totals. It needs no bound on $T$ and keeps polylog error.
- **Sharper error.** Chan, Shi and Song prove the bound $O(\varepsilon^{-1} (\log T)^{1.5} \log(1/\beta))$ for one time step, with a concentration bound for sums of Laplace variables.
- **Lower bound.** Dwork, Naor, Pitassi and Rothblum show that any $\varepsilon$-DP continual counter has error of order $\log T$ at some step. So the polylog error is close to the best possible.
- **Matrix view.** The release is $W A^{+}(A\sigma + z)$ with $W$ the prefix-sum matrix and $A$ the 0-1 matrix of the tree nodes. The [matrix mechanism](/matrix-mechanism/) searches over all strategies $A$, and later work on factorization mechanisms finds strategies with smaller constants for prefix sums.
- **Sums of vectors.** The same tree releases running sums of vectors of bounded norm. Private online learning and the DP-FTRL optimizer of Kairouz and others (ICML 2021) use it to add noise to running sums of gradients.

## When to use it

Use the binary tree mechanism when you must release a running count or a running sum at many time steps, and each item belongs to one event. Examples are counts of events posted each hour, and running gradient sums in private training. If you need only the final count, one draw of the [Laplace mechanism](/laplace-mechanism/) is better. If you need all prefix sums of a fixed dataset at once, and not online, the [matrix mechanism](/matrix-mechanism/) can choose a better strategy. If each person contributes many items, use a user-level bound and scale the noise to it.

## Pitfalls

- **Too few levels.** Line L1 must use $L = \lfloor \log_2 T \rfloor + 1$, the number of bits of $T$. The common shorthand $\lceil \log_2 T \rceil$ is one too small when $T$ is a power of two: for $T = 8$ it gives 3, but the time step 1 lies in 4 nodes. Then line L6 adds $\mathrm{Lap}(3/\varepsilon)$ and the mechanism is only $\frac{4}{3}\varepsilon$-DP. The test file checks that the bound $L$ is reached for $T = 1, 2, 4, 8$.
- **Fresh noise at each release.** Line L6 draws the noise of a node one time, and line L7 reuses it. Drawing new noise for each node each time it is used in line L7 gives many independent noisy copies of the same node. An observer averages them, and the privacy loss grows with the number of uses.
- **Noise scaled to one node.** The scale in line L6 is $L/\varepsilon$, not $1/\varepsilon$. With $\mathrm{Lap}(1/\varepsilon)$ on each node, the noisy node vector is only $L\varepsilon$-DP, because one change moves $L$ nodes.
- **Items outside the range.** The sensitivity bound needs $|\sigma(t) - \sigma'(t)| \le 1$. For real items, clip each item to $[0, 1]$ (or scale the noise to the range) before line L4.
- **Float noise.** The code uses float Laplace noise from `random.Random`, for tests only. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020); see the [discrete Gaussian mechanism](/discrete-gaussian-mechanism/).

## Implementations

## History

Chan, Shi and Song (ICALP 2010) and Dwork, Naor, Pitassi and Rothblum (STOC 2010) found the mechanism at the same time. Chan, Shi and Song called it the binary mechanism, and also gave the hybrid mechanism for streams of unknown length. Dwork, Naor, Pitassi and Rothblum framed the problem as differential privacy under continual observation, and proved a lower bound of order $\log T$ on the error. The tree later became a standard tool for private online learning and, from 2021, for private training with noisy running sums of gradients.

## References
