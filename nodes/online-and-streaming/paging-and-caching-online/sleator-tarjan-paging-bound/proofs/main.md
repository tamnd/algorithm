---
title: LRU and FIFO with cache k against an optimum with cache h, and the matching lower bound
proves: [statement]
status: full
---

The cost of an algorithm is the number of pages it loads. When it serves request $t$, an algorithm may load and evict pages, and after that its cache must hold $\sigma_t$. A cache of size $h$ holds at most $h$ pages. Fix $1 \le h \le k$ and a sequence $\sigma = \sigma_1 \cdots \sigma_n$ with $n \ge 1$.

## Part 1: the upper bound

**Phases.** Cut $\sigma$ into [phases](/marking-phases/) greedily: phase 1 starts at request 1, and a new phase starts at each request that would make the current phase contain $k + 1$ distinct pages. Let $N$ be the number of phases, let phase $i$ start at time $s_i$, and let $D_i$ be its set of distinct pages. Each phase has at most $k$ distinct pages. For $i < N$, $|D_i| = k$ and $\sigma_{s_{i+1}} \notin D_i$, by the rule that starts phase $i + 1$.

**Claim 1.** $A$ has at most $k$ faults in each phase, so $A(\sigma) \le kN$.

*Proof.* If $A$ is conservative, this is its definition, since a phase is a contiguous part with at most $k$ distinct pages. If $A$ is a [marking algorithm](/marking-algorithm/), it never evicts a page that was requested earlier in the current phase. So after the first request for a page in a phase, the page stays in the cache until the phase ends, and each of the at most $k$ pages of $D_i$ faults at most once in phase $i$. $\square$

**Claim 2.** $\mathrm{OPT}_h(\sigma) \ge (N - 1)(k - h + 1)$.

*Proof.* For $i = 1, \ldots, N - 1$, let $W_i$ be the requests at times $s_i + 1, \ldots, s_{i+1}$, from the second request of phase $i$ to the first request of phase $i + 1$. The parts $W_1, \ldots, W_{N-1}$ do not overlap. Let $p_i = \sigma_{s_i}$.

The pages of $D_i$ other than $p_i$ are $k - 1$ pages, and each is requested in phase $i$ after time $s_i$, so in $W_i$. The page $\sigma_{s_{i+1}}$ is not in $D_i$, so it is a $k$-th page, also requested in $W_i$. So $W_i$ requests a set $Q_i$ of $k$ distinct pages, none equal to $p_i$.

Take any offline algorithm with cache $h$. After it serves request $s_i$, its cache holds $p_i$, so it holds at most $h - 1$ pages of $Q_i$. Each of the at least $k - (h - 1)$ other pages of $Q_i$ must be in the cache at its first request in $W_i$, so it is loaded at some time in $W_i$. Loads of distinct pages are distinct loads, so the algorithm loads at least $k - h + 1$ pages during $W_i$. Adding over $i$ gives the claim. $\square$

**Conclusion.** By Claims 1 and 2,

$$A(\sigma) \le kN = k(N - 1) + k \le \frac{k}{k - h + 1}\,\mathrm{OPT}_h(\sigma) + k.$$

LRU is a marking algorithm, see [marking algorithm](/marking-algorithm/), and FIFO is conservative, see [cache replacement policy](/cache-replacement-policy/). With $h = k$, both are $k$-competitive. $\square$

## Part 2: the lower bound

**The adversary.** Let $P = \{1, \ldots, k + 1\}$. For $t = 1, \ldots, n$, let $\sigma_t$ be the smallest page of $P$ that is not in the cache of $A$ after request $t - 1$. It exists, because that cache holds at most $k$ pages. Since $A$ is deterministic and online, this defines $\sigma$. Each request is a fault of $A$, so $A(\sigma) \ge n$. After request $t$ the cache of $A$ holds $\sigma_t$, so $\sigma_{t+1} \ne \sigma_t$.

**A family of offline algorithms.** For each $t$, let $\mathcal{S}_t$ be the set of $h$-subsets of $P$ that contain $\sigma_t$. Then $|\mathcal{S}_t| = \binom{k}{h-1}$, since the other $h - 1$ pages come from the $k$ pages of $P \setminus \{\sigma_t\}$. For $t \ge 2$ define $\varphi_t : \mathcal{S}_{t-1} \to \mathcal{S}_t$ by

$$\varphi_t(S) = \begin{cases} S & \text{if } \sigma_t \in S, \\ (S \setminus \{\sigma_{t-1}\}) \cup \{\sigma_t\} & \text{if } \sigma_t \notin S. \end{cases}$$

In the second case $\sigma_{t-1} \in S$ and $\sigma_t \ne \sigma_{t-1}$, so the result has $h$ pages and contains $\sigma_t$. The map is one to one. Two sets of the first case have equal images only if they are equal. Two sets $S, S'$ of the second case both contain $\sigma_{t-1}$, so equal images give $S \setminus \{\sigma_{t-1}\} = S' \setminus \{\sigma_{t-1}\}$ and $S = S'$. An image of the first case contains $\sigma_{t-1}$ and an image of the second case does not. Since both sets have $\binom{k}{h-1}$ elements, $\varphi_t$ is a bijection.

For each $S \in \mathcal{S}_1$, let $B_S$ be the offline algorithm with cache $h$ that changes its initial cache to $S$ at request 1, with at most $h$ loads, and at each request $t \ge 2$ changes its cache from $S'$ to $\varphi_t(S')$. In the second case of $\varphi_t$, this is one fault: evict $\sigma_{t-1}$ and load $\sigma_t$. In the first case it is a hit. Each $B_S$ holds $\sigma_t$ after request $t$, so it is a valid algorithm. Since each $\varphi_t$ is a bijection, by induction on $t$ the caches of the $\binom{k}{h-1}$ algorithms after request $t$ are exactly the sets of $\mathcal{S}_t$, each once.

**Counting.** At request $t \ge 2$, the algorithms that fault are those whose cache is a set of $\mathcal{S}_{t-1}$ without $\sigma_t$. Such a set holds $\sigma_{t-1}$ and $h - 1$ pages of the $k - 1$ pages of $P \setminus \{\sigma_{t-1}, \sigma_t\}$, so there are $\binom{k-1}{h-1}$ of them. The total cost of the family is at most

$$h \binom{k}{h-1} + (n - 1)\binom{k-1}{h-1}.$$

Since $\binom{k-1}{h-1} / \binom{k}{h-1} = (k - h + 1)/k$, the average cost of an algorithm of the family is at most $h + (n - 1)(k - h + 1)/k$. Some $B_S$ costs at most the average, so

$$\mathrm{OPT}_h(\sigma) \le \frac{k - h + 1}{k}(n - 1) + h.$$

**The ratio.** If $A(\sigma) \le c \cdot \mathrm{OPT}_h(\sigma) + b$ for all $\sigma$, then for every $n$,

$$n \le c\left(\frac{k - h + 1}{k}(n - 1) + h\right) + b.$$

Divide by $n$ and let $n \to \infty$: $1 \le c\,(k - h + 1)/k$, so $c \ge k/(k - h + 1)$. With $h = k$ this gives $c \ge k$. $\blacksquare$

With $h = k$, the family has $k$ algorithms, and the one that faults at request $t$ is the one that does not hold $\sigma_t$. Each fault of $B_S$ evicts the page of the previous request. This is a different proof of the bound in the [deterministic lower bound](/online-caching-lower-bound/), where the offline algorithm is Belady's rule.
