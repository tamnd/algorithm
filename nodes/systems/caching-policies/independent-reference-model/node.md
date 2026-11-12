---
tag: A6MTB2
kind: model
slug: independent-reference-model
name: Independent reference model
aliases:
- IRM
- independent reference model of paging
area: systems/caching-policies
level: advanced
summary: "Requests are independent draws from a fixed popularity distribution. The model gives exact long-run hit ratios: A0 keeps the k-1 most popular items plus one changing slot and is optimal."
prereqs: [cache-hit-ratio, markov-chain]
see_also: [lru, lfu, fifo-replacement, random-replacement, stationary-distribution, locality-of-reference, belady-optimal, working-set-model]
sources:
  - paper: "W. F. King III, Analysis of demand paging algorithms, Proceedings of IFIP Congress 1971, Volume 1, 485-490"
    title: "W. F. King III, Analysis of demand paging algorithms, IFIP Congress 1971"
    locator: the independent reference assumption, and the stationary analysis of the LRU and FIFO page fault rates as Markov chains
  - book: isbn:9780136378686
    title: Edward G. Coffman Jr. and Peter J. Denning, Operating Systems Theory, Prentice-Hall, 1973
    locator: the chapter on paging algorithms, which treats the independent reference model, the optimal policy A0 and the LRU fault rate
  - paper: doi:10.1145/321623.321632
    title: "Alfred V. Aho, Peter J. Denning and Jeffrey D. Ullman, Principles of optimal page replacement, Journal of the ACM 18(1) (1971), 80-93"
    locator: optimal replacement when references are independent with known probabilities, where keeping the most probable pages is optimal
---

The independent reference model, or IRM, is a probabilistic model of the requests to a cache. There are $N$ items with fixed probabilities $p_1, \ldots, p_N$, and each request is an independent draw from this distribution. The model has popularity but no other form of locality: what was requested a moment ago says nothing about what comes next, except through the $p_i$. In return, the long-run hit ratio of many policies becomes an exact formula. In particular, the policy A0 that keeps the $k - 1$ most probable items, with one more slot for the last other item requested, is optimal, the hit ratio of LRU has a closed form, and FIFO and RANDOM have the same hit ratio.

## The machine

- **Items and probabilities.** A finite set of items $1, \ldots, N$ with $p_i > 0$ and $\sum_i p_i = 1$. Often the $p_i$ follow a Zipf law, $p_i \propto i^{-\alpha}$, which fits the popularity of web objects and of many keys.
- **Requests.** $\sigma_1, \sigma_2, \ldots$ are independent, and $\Pr[\sigma_t = i] = p_i$ for each $t$.
- **The cache.** A cache of $k < N$ items, all of size 1, run by a replacement policy that may know the $p_i$ but not the future requests. A request for an item in the cache is a hit.
- **The state.** For many policies, the content of the cache, sometimes with an order, is a [Markov chain](/markov-chain/) driven by the requests. LRU keeps the order of last use, FIFO the order of loading, and RANDOM only the set.

## What it counts

The quantity is the long-run hit ratio

$$h = \lim_{n \to \infty} \frac{1}{n} \#\{ t \le n : \sigma_t \text{ hits} \}.$$

Because $\sigma_{t+1}$ is independent of the past, a request that arrives when the cache holds the set $S$ hits with probability $p(S) = \sum_{i \in S} p_i$. If the chain of states has the [stationary distribution](/stationary-distribution/) $\pi$, then

$$h = \sum_{\text{states } s} \pi(s)\, p(S(s)),$$

where $S(s)$ is the set of items in state $s$. The miss ratio is $1 - h$. The start state matters only for the first requests, unless the chain has several closed classes, as FIFO can.

## Relation to other models

- **Worst-case paging.** The [paging problem](/paging-problem/) of competitive analysis lets an adversary choose each request. There, no deterministic policy beats a factor of $k$ against the optimum. The IRM is the average-case opposite: a random source with fixed statistics.
- **Locality.** Real traces have [locality of reference](/locality-of-reference/) in time: the chance of a request for $i$ is much higher shortly after a use of $i$. The IRM leaves this out. The LRU stack model of Shedler and Tung (1972), later studied by Spirn, draws [reuse distances](/reuse-distance/) instead of items, and the working set model follows phases. Both capture recency, which the IRM does not.
- **Offline optimum.** [Belady's MIN](/belady-optimal/) sees the future and is optimal on each sequence. Under the IRM, it usually has more hits than A0, but no policy that does not see the future can beat A0.
- **Time-varying popularity.** Models with popularity that changes over time, such as the shot noise model, extend the IRM to content whose popularity rises and falls.

## Known results in the model

**A0 is optimal.** Let A0 be the policy that, on a miss, loads the requested item and evicts the resident item with the smallest $p_i$. Write $p_{(1)} \ge p_{(2)} \ge \cdots$ for the sorted probabilities and $P_{k-1} = p_{(1)} + \cdots + p_{(k-1)}$. The long-run hit ratio of A0 is

$$h_{A0} = P_{k-1} + \sum_{j \ge k} \frac{p_{(j)}^2}{1 - P_{k-1}},$$

and Aho, Denning and Ullman (1971) proved that no demand policy that does not see the future has a larger one. A simpler bound holds for each policy: the hit ratio is at most the sum of the $k$ largest $p_i$. A cache that must load each requested item does not reach it in general.

*Proof.* Let $S_t$ be the cache just before request $t$. It depends only on $\sigma_1, \ldots, \sigma_{t-1}$, so $\Pr[\sigma_t \in S_t] = \mathbb{E}[p(S_t)] \le p_{(1)} + \cdots + p_{(k)}$, which is the simple bound. For the formula, take distinct probabilities and let $T$ be the set of the $k - 1$ most probable items. An item $a$ of $T$ is evicted only when the other $k - 1$ residents are all more probable than $a$, and fewer than $k - 1$ items are, so an item of $T$ once loaded stays for good. With probability 1 every item of $T$ is requested, and so loaded, after a finite time. From then on, the last slot holds an item outside $T$, and a miss evicts it, so the slot holds the most recent request among the items outside $T$. By independence that item is $j$ with probability $p_j / (1 - P_{k-1})$, and the next request hits it with probability $p_j$. Adding the hits on $T$ gives $h_{A0}$. With ties, break them by a fixed order of the items, and the same argument applies. $\square$

When the $p_i$ are not known, perfect LFU, which counts all past requests of each item, estimates them and tends to the same hit ratio. Aho, Denning and Ullman (1971) named the policy A0 and proved its optimality; Coffman and Denning (1973) treat it in their book.

**LRU.** Let the LRU state be the ordered tuple $(i_1, \ldots, i_k)$, most recent first. Its stationary probability is

$$\pi(i_1, \ldots, i_k) = \prod_{j=1}^{k} \frac{p_{i_j}}{1 - p_{i_1} - \cdots - p_{i_{j-1}}},$$

and the LRU hit ratio is $\sum \pi(i_1, \ldots, i_k)\,(p_{i_1} + \cdots + p_{i_k})$ over all ordered $k$-tuples of distinct items.

*Derivation.* At a large time $t$, the LRU state is the list of the first $k$ distinct items in the backward sequence $\sigma_t, \sigma_{t-1}, \sigma_{t-2}, \ldots$. This sequence is again independent with the same law. Its first item is $i_1$ with probability $p_{i_1}$. Given that the distinct items seen so far are $i_1, \ldots, i_{j-1}$, the requests for these items are skipped, and the next new item is $i_j$ with probability $p_{i_j} / (1 - p_{i_1} - \cdots - p_{i_{j-1}})$. Multiplying gives $\pi$. The hit ratio follows from the formula for $h$ above. King derived the LRU fault rate under this model in 1971. The tests of the implementation check the formula against the exact stationary distribution of the LRU chain, found by solving the balance equations in rational numbers.

For $k = 1$ the formula gives $h = \sum_i p_i^2$, the chance that two independent requests are equal. For the uniform distribution $p_i = 1/N$ it gives $h = k/N$, the same as each other policy, because then all items look alike.

**FIFO and RANDOM.** Under the IRM, FIFO and RANDOM have the same long-run hit ratio: the set $S$ is resident with probability proportional to $\prod_{i \in S} p_i$. For RANDOM this follows from detailed balance: a miss on $i$ that evicts $j$ moves $S$ to $S' = S - \{j\} + \{i\}$ with probability $p_i / k$, the reverse move has probability $p_j / k$, and $\pi(S)\, p_i = \pi(S')\, p_j$ holds for this $\pi$. The result for FIFO is usually credited to Gelenbe (1973). The tests check both against the exact stationary distributions of the two chains.

**A worked example.** Take $N = 3$, $p = (1/2, 1/3, 1/6)$ and $k = 2$.

| LRU state | $(1,2)$ | $(2,1)$ | $(1,3)$ | $(3,1)$ | $(2,3)$ | $(3,2)$ |
|---|---|---|---|---|---|---|
| $\pi$ | $1/3$ | $1/4$ | $1/6$ | $1/10$ | $1/12$ | $1/15$ |
| $p(S)$ | $5/6$ | $5/6$ | $2/3$ | $2/3$ | $1/2$ | $1/2$ |

For example $\pi(3,1) = \frac{1/6}{1} \cdot \frac{1/2}{1 - 1/6} = \frac{1}{10}$. The hit ratios are:

| policy | long-run hit ratio |
|---|---|
| A0 | $7/9 \approx 0.778$ |
| LRU | $133/180 \approx 0.739$ |
| FIFO, RANDOM | $8/11 \approx 0.727$ |

Here A0 keeps item 1 and holds the last of items 2 and 3 in its second slot: $h_{A0} = 1/2 + (1/9 + 1/36)/(1/2) = 7/9$. So under the IRM, LRU loses about 5 percent of the hits of A0, because it keeps the rare item 3 for a while after each request for it. On real traces with locality, the order can be the opposite: LRU often beats LFU, which aims at A0, because recent use predicts the next use better than long-run popularity does.

**Approximations.** For large $N$ the exact LRU sum has too many terms. The approximation of Che, Tung and Wang (2002) replaces the cache by a characteristic time $T$, the time an item stays after its last use, and is very accurate under the IRM for large caches.

## References
