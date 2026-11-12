---
tag: JZN82D
kind: theorem
slug: lru-competitiveness
name: k-competitiveness of LRU
aliases:
- competitive ratio of LRU
area: systems/caching-policies
level: advanced
summary: "From an empty cache, LRU with k items never has more than k times the misses of Belady's MIN, and no deterministic online policy does better. Cyclic scans reach the bound."
prereqs: [competitive-ratio, marking-phases, belady-optimal]
see_also: [sleator-tarjan-paging-bound, online-caching-lower-bound, lru, fifo-replacement, flush-when-full, harmonic-paging-bound, locality-of-reference, paging-problem]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the paging theorems, LRU and FIFO with k frames against MIN with h frames, the bound k/(k-h+1), and the lower bound for every on-line rule
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, the competitive analysis of LRU, FIFO and flush when full, and the deterministic lower bound
---

The theorem of Sleator and Tarjan (1985) bounds the misses of LRU on every request sequence, not on average. With a cache of $k$ items and an empty start, LRU has at most $k$ times as many misses as Belady's [MIN](/belady-optimal/), the best possible with full knowledge of the future. If MIN gets only $h \le k$ items, the factor becomes $k/(k - h + 1)$, up to an additive $k$. FIFO meets the same bounds. No deterministic online policy does better, and a loop over $k + 1$ items forces LRU to the bound. This page gives the systems reading of the result and a direct proof for LRU and FIFO; the page [Sleator and Tarjan paging bound](/sleator-tarjan-paging-bound/) states it for all marking and conservative algorithms in the language of online algorithms.

## Statement

Requests are for items of size 1, each miss costs 1, and each cache starts empty. For $1 \le h \le k$, let $\mathrm{OPT}_h(\sigma)$ be the least number of misses on $\sigma$ with a cache of $h$ items; MIN with $h$ items attains it. Let $\mathrm{LRU}_k(\sigma)$ and $\mathrm{FIFO}_k(\sigma)$ be the misses of LRU and FIFO with $k$ items.

**Theorem.**

1. **Upper bound.** For $A \in \{\mathrm{LRU}, \mathrm{FIFO}\}$ and every $\sigma$,
$$A_k(\sigma) \le \frac{k}{k - h + 1}\, \mathrm{OPT}_h(\sigma) + k, \qquad \text{and} \qquad A_k(\sigma) \le k \cdot \mathrm{OPT}_k(\sigma).$$
2. **Lower bound.** For every deterministic online policy $A$ with $k$ items and every $n \ge 1$, there is a sequence $\sigma$ of $n$ requests over $k + 1$ items with
$$A_k(\sigma) = n \qquad \text{and} \qquad \mathrm{OPT}_h(\sigma) \le \frac{k - h + 1}{k}(n - 1) + h.$$
So no bound $A_k(\sigma) \le c \cdot \mathrm{OPT}_h(\sigma) + b$ with a constant $b$ holds for all $\sigma$ if $c < k/(k - h + 1)$.

## In plain words

No policy that cannot see the future can beat the best policy that can. The question is how much worse it is. This theorem answers it for the least recently used rule, on the worst possible trace.

Cut the trace into rounds, so that each round asks for exactly as many different items as the cache holds. In one round the rule loses each item at most once, so it misses at most once per slot. The rule that sees the future must also miss in each round, at least once, and more often if its cache is smaller. Compare the two counts, and the gap is at most the number of slots.

The bad case is real: a loop over one item more than the cache holds. Then the least recently used rule misses on every request, while the best rule misses about once in each round.

## Proof

**Phases.** Cut $\sigma$ into *phases* for $k$: the first phase starts at request 1, and a new phase starts at the request that would make the current phase contain $k + 1$ distinct items. So each phase contains at most $k$ distinct items, and every phase except the last contains exactly $k$. Let $N$ be the number of phases. The page on [marking phases](/marking-phases/) studies this partition in general.

**Lemma 1 (LRU misses at most $k$ times per phase).** Let $p$ be requested in a phase at time $s$. Suppose that LRU evicts $p$ at a later time $r$ in the same phase. Then the cache is full at time $r$, and $p$ is its least recently used item, so the other $k - 1$ cached items were all requested in $(s, r)$. The item $\sigma_r$ is not cached, so it differs from all of them and from $p$. That makes $k + 1$ distinct items in the phase, which is impossible. So after its first request in a phase, an item stays in the LRU cache until the phase ends, and each of the at most $k$ distinct items of the phase causes at most one miss. $\square$

**Lemma 2 (FIFO misses at most $k$ times per phase).** Suppose that $p$ misses twice in one phase, at times $s_1 < s_2$. Then FIFO evicted $p$ at some time $r$ with $s_1 < r < s_2$. At that time $p$ was the oldest item in the queue, so the other $k - 1$ items were loaded, and so requested, in $(s_1, r)$. The item $\sigma_r$ is not in the queue, so it differs from all of them. Again the phase contains $k + 1$ distinct items. So each item misses at most once per phase. $\square$

**Lemma 3 (MIN misses often).** $\mathrm{OPT}_h(\sigma) \ge (N - 1)(k - h + 1) + 1$ if $\sigma$ is not empty.

*Proof.* For a phase $i < N$, let $q$ be its first item, and let $W_i$ be the window from the second request of phase $i$ to the first request of phase $i + 1$, both included. Phase $i$ has $k$ distinct items and the next phase starts with a new one, so $W_i$ contains at least $k$ distinct items other than $q$. Just before $W_i$, an optimal cache of $h$ items holds $q$, which was just requested, and at most $h - 1$ other items. So at least $k - (h - 1)$ distinct items of $W_i$ are not cached at its start, and each of them must be loaded inside $W_i$. The windows $W_1, \ldots, W_{N-1}$ do not overlap, and none of them contains the first request of $\sigma$, which is a miss from an empty cache. $\square$

**The upper bound.** By Lemma 1 or Lemma 2, $A_k(\sigma) \le kN$. By Lemma 3, $N - 1 \le \mathrm{OPT}_h(\sigma)/(k - h + 1)$. So
$$A_k(\sigma) \le k(N - 1) + k \le \frac{k}{k - h + 1}\, \mathrm{OPT}_h(\sigma) + k.$$
For $h = k$, Lemma 3 gives $N \le \mathrm{OPT}_k(\sigma)$, so $A_k(\sigma) \le kN \le k \cdot \mathrm{OPT}_k(\sigma)$ with no additive term. For the empty sequence all counts are 0.

**The lower bound.** Fix a set $P$ of $k + 1$ items. The adversary always requests an item of $P$ that $A$ does not hold. One exists, because $A$ holds at most $k$ items. So $A$ misses on every request, and $A_k(\sigma) = n$. Two consecutive requests always differ, because after request $t$ the cache of $A$ holds $\sigma_t$.

To bound $\mathrm{OPT}_h$, run a family of offline policies with $h$ items side by side and average. For each set $R$ of $h - 1$ items of $P \setminus \{\sigma_1\}$, the policy $B_R$ starts by loading $\{\sigma_1\} \cup R$, at a cost of $h$. Keep the invariant: just after request $t$, each $B_R$ holds $\sigma_t$ plus a set of $h - 1$ other items, and these sets are exactly all the $(h - 1)$-subsets of the $k$ items $P \setminus \{\sigma_t\}$, each once. It holds for $t = 1$. At request $t + 1$, let $x = \sigma_{t+1} \ne \sigma_t$.

- A policy whose other items include $x$ hits. Its new other items are the old ones with $x$ replaced by $\sigma_t$. These are exactly the $(h - 1)$-subsets of $P \setminus \{x\}$ that contain $\sigma_t$.
- A policy whose other items do not include $x$ misses, loads $x$ and evicts $\sigma_t$. Its other items do not change. These are exactly the $(h - 1)$-subsets of $P \setminus \{x\}$ that do not contain $\sigma_t$.

So the invariant holds after request $t + 1$. The policies that miss at that request correspond to the $(h - 1)$-subsets of the $k$ items $P \setminus \{\sigma_t\}$ that avoid $x$. There are $\binom{k - 1}{h - 1}$ of them, out of $\binom{k}{h - 1}$, a fraction of $(k - h + 1)/k$. Summed over requests 2 to $n$, the mean cost of the policies is $h + \frac{k - h + 1}{k}(n - 1)$, and the cheapest policy costs at most the mean. The policies load items before they are requested, but a policy that loads early can be changed into a demand policy with no more loads, so $\mathrm{OPT}_h(\sigma)$ is at most this mean too. Dividing, $A_k(\sigma)/\mathrm{OPT}_h(\sigma)$ tends to $k/(k - h + 1)$ as $n$ grows, so no smaller factor $c$ is possible. $\square$

The tests of the implementation check the upper bounds and the three lemmas on hundreds of random sequences of up to 15 requests, against a brute-force optimum that tries every eviction choice. They do not use MIN, so they do not assume its optimality.

## Consequences

- **The bound is about loops.** On a trace with locality, LRU is close to MIN; the factor $k$ appears only on sequences that cycle through just more items than the cache holds. A program that scans an array of 13 cache lines ten times with a 12-line LRU cache misses on all 130 accesses, see [locality of reference](/locality-of-reference/). Scan-resistant policies such as [ARC](/arc/) and [LIRS](/lirs/) target exactly this case.
- **Resource augmentation.** Compare LRU with $k = 2h$ items to MIN with $h$. The factor is $2h/(h + 1) < 2$. So doubling the memory of LRU brings it within a factor 2 of the best possible use of the smaller memory, on every trace. This is a better guide for sizing than the factor $k$.
- **The bound does not separate good from bad policies.** [Flush when full](/flush-when-full/), which empties the cache when it is full, is also $k$-competitive, but it is much worse than LRU on real traces. Later models of locality, such as access graphs and bijective analysis, were made to separate LRU from such policies.
- **Policies outside the theorem.** LFU and MRU have no bounded ratio: on a suitable sequence their misses grow without bound while MIN's stay fixed.
- **Randomness helps.** Against an adversary that does not see the random choices, randomized marking has ratio $O(\log k)$, see the [harmonic paging bound](/harmonic-paging-bound/). The lower bound $k$ is for deterministic policies only.

## Tightness

Take $k = 3$ and the cycle $0\,1\,2\,3\,0\,1\,2\,3 \cdots$ of $n = 60$ requests over 4 items, which is also what the adversary produces against LRU. It has $N = 20$ phases. The values of $\mathrm{OPT}_h$ come from the brute-force search.

| $h$ | 1 | 2 | 3 |
|---|---|---|---|
| $\mathrm{LRU}_3 = \mathrm{FIFO}_3$ | 60 | 60 | 60 |
| $\mathrm{OPT}_h$ | 60 | 41 | 22 |
| Lemma 3: $(N - 1)(k - h + 1) + 1$ | 58 | 39 | 20 |
| lower bound part: $\frac{k - h + 1}{k}(n - 1) + h$ | 60 | 41.3 | 22.7 |
| ratio $\mathrm{LRU}_3 / \mathrm{OPT}_h$ | 1 | 1.46 | 2.73 |
| $k/(k - h + 1)$ | 1 | 1.5 | 3 |

On a cycle of $k + 1$ items, MIN with $k$ items misses $k + \lfloor (n - 1)/k \rfloor$ times, so the ratio tends to $k$. With augmentation, on the cycle of 5 items with $n = 40$, LRU with 4 items has 40 misses and MIN with 2 items has 31, a ratio of $1.29$, below the bound $4/3$.

## History

Sleator and Tarjan proved the bound in 1985 for LRU and FIFO with $k$ frames against MIN with $h$ frames, together with the lower bound for every on-line rule, in the same paper that analyzed move to front for list update. The word *competitive* came later, from Karlin, Manasse, Rudolph and Sleator (1988). The analysis turned a fact known from simulations since Belady (1966), that LRU is good but not optimal, into a guarantee per trace. Because the guarantee is weak for the policies that matter in practice, later work added models of locality to the analysis.

## References
