---
title: Hyperbolic caching stays within its size and evicts a sampled minimum of n/t
proves: [correctness]
status: full
---

We use the pseudocode of the page with a cache of $c \ge 1$ items and $S \ge 1$ samples. Let $t$ be the clock after line L1 of the current request, and for a cached item $i$ let $n_i$ be its count and $\tau_i$ its insertion time.

**Lemma 1 (priorities are well defined).** Before line L6 runs, every cached item has $\tau_i < t$ and $1 \le n_i \le t - \tau_i$. So $p_i = n_i/(t - \tau_i)$ is defined and $0 < p_i \le 1$.

*Proof.* An item $i$ is inserted on line L8 during the request at time $\tau_i$, with $n_i = 1$. Every later request raises $t$ by one on line L1 before anything else, so at any later request $t \ge \tau_i + 1$. The count $n_i$ rises by one only on a hit to $i$, at most once per request. Between the request at $\tau_i$ and the start of the request at $t$ there are $t - \tau_i - 1$ requests, so $n_i \le 1 + (t - \tau_i - 1) = t - \tau_i$. $\square$

**Theorem.** After every request:

1. (I1) at most $c$ items are cached, and every cached item has exactly one entry in the key array;
2. (I2) a request is a hit if and only if its item was cached before the request;
3. (I3) if $S \ge c$, every eviction removes an item of least priority in the cache, ties broken by the earliest insertion time.

*Proof.* By induction. A hit (lines L2 and L3) changes only $n_x$. On a miss, if $c$ items are cached, lines L5 to L7 remove one of them, so after line L8 again at most $c$ are cached. Removal swaps the last key of the array into the place of $v$, so the array still holds each cached key once. This gives (I1), and (I2) holds since line L2 tests membership. If $S \ge c$, line L5 draws all $c$ cached items, and line L6 takes the least priority among them, which gives (I3). $\blacksquare$

**Lemma 2 (rank of the sampled minimum).** Let $N$ cached items have distinct priorities, ranked $1$ (least) to $N$. Draw $S \le N$ distinct items uniformly. The least rank $R$ in the sample has $\mathbb{E}[R] = (N+1)/(S+1)$.

*Proof.* For $1 \le k \le N$, $R \ge k$ exactly when all $S$ samples come from the $N - k + 1$ items of rank at least $k$. So $\Pr[R \ge k] = \binom{N-k+1}{S} / \binom{N}{S}$. Then
$$
\mathbb{E}[R] = \sum_{k=1}^{N} \Pr[R \ge k] = \frac{1}{\binom{N}{S}} \sum_{j=S}^{N} \binom{j}{S} = \frac{\binom{N+1}{S+1}}{\binom{N}{S}} = \frac{N+1}{S+1},
$$
by the hockey stick identity $\sum_{j=S}^{N} \binom{j}{S} = \binom{N+1}{S+1}$. $\square$

**Consequences.**

1. *The newest item survives the next miss.* An item inserted at $t - 1$ has $p = 1$, the largest value allowed by Lemma 1. With $S \ge c$ and the tie rule, it is evicted at time $t$ only if every cached item has priority 1 and it entered last of all, which needs $c = 1$.
2. *Idle items decay.* While $i$ gets no hits, $n_i$ is fixed and $t - \tau_i$ grows, so $p_i$ falls like $1/t$.
3. *Cost.* A hit costs $O(1)$ and a miss costs $O(S)$, as the page states.

**The test file.** It compares the code with $S = c$ against a separate exact version on 40 seeded random traces, with unit costs and with random costs, checks the array, the positions and the clock after every request with $S = 2$, checks that a sample has $\min(S, N)$ distinct items, checks Lemma 2 by enumerating all samples for $N \le 8$, checks the evictions of the worked example, and checks that an old popular item loses to items that are requested now.
