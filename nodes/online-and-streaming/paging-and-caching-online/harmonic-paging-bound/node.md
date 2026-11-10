---
tag: KV5B78
kind: theorem
slug: harmonic-paging-bound
name: Harmonic number paging bound
aliases:
- randomized paging bound
- H_k bound
- randomized paging lower bound
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Randomized paging has competitive ratio Theta(H_k), the k-th harmonic number, against an oblivious adversary.
prereqs: [yao-minimax-principle, oblivious-adversary, coupon-collector-problem, marking-phases, online-caching-lower-bound]
see_also: [randomized-marking, harmonic-series, randomized-online-algorithm, adaptive-offline-adversary, sleator-tarjan-paging-bound, k-server-problem, learning-augmented-marking, linearity-of-expectation]
sources:
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the lower bound H_k for every randomized paging algorithm against an oblivious adversary
  - paper: doi:10.1007/BF01759073
    title: "Lyle A. McGeoch and Daniel D. Sleator, A strongly competitive randomized paging algorithm, Algorithmica 6(6) (1991), 816-825"
    locator: the algorithm Partition and the proof that it is H_k-competitive
  - paper: doi:10.1016/S0304-3975(98)00116-9
    title: "Dimitris Achlioptas, Marek Chrobak and John Noga, Competitive analysis of randomized paging algorithms, Theoretical Computer Science 234(1-2) (2000), 203-218"
    locator: the algorithm Equitable, which is H_k-competitive, and the ratio 2H_k - 1 of MARK
  - paper: doi:10.1109/SFCS.1977.24
    title: "Andrew Chi-Chih Yao, Probabilistic computations: toward a unified measure of complexity, 18th Annual Symposium on Foundations of Computer Science (1977), 222-227"
    locator: the principle that a lower bound for deterministic algorithms on a random input is a lower bound for randomized algorithms
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 4, the lower bound H_k for randomized paging
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 13, Online algorithms, the lower bound for randomized paging with Yao's principle
---

The harmonic number paging bound says that the best competitive ratio of a randomized online paging algorithm with cache size $k$, against an [oblivious adversary](/oblivious-adversary/), is exactly $H_k = 1 + \frac{1}{2} + \cdots + \frac{1}{k}$, which is about $\ln k$. Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) proved the lower bound $H_k$ with [Yao's principle](/yao-minimax-principle/), on uniform random requests over $k + 1$ pages. McGeoch and Sleator (1991) gave an algorithm that reaches $H_k$, and Achlioptas, Chrobak and Noga (2000) a simpler one. Compared with the [deterministic bound](/online-caching-lower-bound/) $k$, randomization gives an exponential gain.

## Statement

Use the [paging problem](/paging-problem/) model with a cache of $k$ pages and cost 1 per page loaded. A [randomized online algorithm](/randomized-online-algorithm/) $R$ is *$c$-competitive against an oblivious adversary* if there is a constant $b$ with $\mathbb{E}[R(\sigma)] \le c \cdot \mathrm{OPT}(\sigma) + b$ for every request sequence $\sigma$, where the expectation is over the random choices of $R$.

**Theorem.** Let $k \ge 1$.

1. **Lower bound** (Fiat et al. 1991). If $R$ is a randomized online paging algorithm with cache size $k$ that is $c$-competitive against an oblivious adversary, then $c \ge H_k$. This holds already for sequences over $k + 1$ pages.
2. **Upper bound** (McGeoch and Sleator 1991; Achlioptas, Chrobak and Noga 2000). There are randomized online paging algorithms, Partition and Equitable, that are $H_k$-competitive against an oblivious adversary.

So the optimal randomized ratio is $H_k$. Since $\ln(k + 1) < H_k \le 1 + \ln k$, it is $\Theta(\log k)$.

## In plain words

Use one page more than the cache holds, and ask for a page picked at random each time. Whatever an online rule does, the page asked for is missing with a chance of one in that number of pages. So the online rule misses at a steady rate.

A rule that sees the future does much better. Cut the requests into rounds, each with as many different pages as the cache holds. The future rule needs to miss at most once per round. How long is a round? It is like collecting coupons: it takes a long time to see all the different pages, about the number of pages times the harmonic number. So the ratio of the two miss counts is the harmonic number.

## Proof

Part 2 is cited. We prove part 1. Let $P = \{1, \ldots, k + 1\}$, and let both $R$ and the offline algorithm start with the cache $C_0 = \{1, \ldots, k\}$. Assume that $R$ is $c$-competitive with constant $b$.

**The random input.** Let $\sigma_1, \sigma_2, \ldots$ be independent, each uniform on $P$. Cut this sequence into [phases](/marking-phases/) greedily: phase 1 starts at request 1, and a new phase starts at each request that would make the current phase contain $k + 1$ distinct pages. Fix $m \ge 1$ and let $\tau$ be the time of the first request of phase $m + 1$. For $T \ge 1$, let $\sigma^{(T)} = \sigma_1 \cdots \sigma_{\min(\tau, T)}$. This is a random sequence with finitely many possible values.

**Step 1: the length of a phase.** A phase starts with one distinct page. While it has $i$ distinct pages, with $1 \le i \le k$, each request is a page not yet in the phase with probability $(k + 1 - i)/(k + 1)$, whatever came before. So the number of requests until that happens has expected value $(k + 1)/(k + 1 - i)$, as in the [coupon collector problem](/coupon-collector-problem/). For $i \le k - 1$ that request adds a page to the phase. For $i = k$ it is the first request of the next phase. So the expected number of requests from the first request of a phase to the first request of the next one is

$$\sum_{i=1}^{k} \frac{k + 1}{k + 1 - i} = (k + 1) H_k.$$

By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\tau] = 1 + m(k + 1)H_k$. In particular $\tau$ is finite with probability 1.

**Step 2: every deterministic online algorithm.** Let $D$ be a deterministic online algorithm, and let $C_{t-1}$ be its cache before request $t$. Both $C_{t-1}$ and the event $\{t \le \tau\}$ depend only on $\sigma_1, \ldots, \sigma_{t-1}$, and $\sigma_t$ is independent of them. Since $|C_{t-1}| \le k$, $\Pr[\sigma_t \notin C_{t-1} \mid \sigma_1, \ldots, \sigma_{t-1}] \ge 1/(k + 1)$. So

$$\mathbb{E}\big[D(\sigma^{(T)})\big] \ge \sum_{t=1}^{T} \Pr[t \le \tau] \cdot \frac{1}{k + 1} = \frac{\mathbb{E}[\min(\tau, T)]}{k + 1}.$$

**Step 3: the offline algorithm.** For $i \le m$, phase $i$ is complete, so its set $D_i$ of distinct pages has $k$ elements, and the only page of $P$ not in $D_i$ is the first page $q_{i+1}$ of phase $i + 1$. Consider this offline rule: on a fault in phase $i \le m$, evict $q_{i+1}$. The cache always has $k$ pages. At a fault at time $t$ in phase $i$, the cache is $P \setminus \{\sigma_t\}$, and $\sigma_t \in D_i$, so $q_{i+1}$ is in the cache. After the fault the cache is $P \setminus \{q_{i+1}\} = D_i$, so the rest of phase $i$ has no fault. So the rule has at most one fault in each of phases $1, \ldots, m$, and at most one at time $\tau$. Its schedule restricted to $\sigma^{(T)}$ is a valid schedule, so $\mathrm{OPT}(\sigma^{(T)}) \le m + 1$.

**Step 4: Yao's principle.** For a fixed string $r$ of random bits, $R$ is a deterministic online algorithm $R_r$. By step 2, for every $r$, $\mathbb{E}_\sigma[R_r(\sigma^{(T)})] \ge \mathbb{E}[\min(\tau, T)]/(k + 1)$. The costs are nonnegative, so the two expectations can be swapped, and with the competitive bound for each fixed value of $\sigma^{(T)}$ and step 3,

$$\frac{\mathbb{E}[\min(\tau, T)]}{k + 1} \le \mathbb{E}_r\,\mathbb{E}_\sigma\big[R_r(\sigma^{(T)})\big] = \mathbb{E}_\sigma\,\mathbb{E}_r\big[R_r(\sigma^{(T)})\big] \le c\,\mathbb{E}\big[\mathrm{OPT}(\sigma^{(T)})\big] + b \le c(m + 1) + b.$$

Let $T \to \infty$. By monotone convergence, $\mathbb{E}[\min(\tau, T)] \to \mathbb{E}[\tau]$, so by step 1

$$\frac{1}{k + 1} + m H_k \le c(m + 1) + b.$$

Divide by $m$ and let $m \to \infty$: $H_k \le c$.

**Other initial caches.** Step 2 holds for every initial cache of $R$. If the offline algorithm starts empty, it first loads $C_0$, which adds $k$ to step 3, and the limit is the same. $\blacksquare$

## Consequences

- **Randomization helps exponentially.** Every deterministic algorithm has ratio at least $k$ ([deterministic lower bound](/online-caching-lower-bound/)), and the best randomized ratio is $H_k$. For $k = 100$, this is 100 against about 5.19.
- **MARK is within a factor of 2.** [Randomized marking](/randomized-marking/) is $2H_k$-competitive, and its exact ratio is $2H_k - 1$. So it is within a factor 2 of the bound. Partition and Equitable reach $H_k$ but are more complex.
- **The adversary model matters.** The proof uses a fixed distribution over sequences, so it is a bound against an oblivious adversary. Against an [adaptive offline adversary](/adaptive-offline-adversary/), randomization gives no gain, and the bound is $k$ (Ben-David et al. 1994).
- **One page more is enough.** The input uses only $k + 1$ pages, the smallest universe on which paging is not trivial.
- **Generalizations.** The bound $H_k$ is a lower bound for the randomized [$k$-server problem](/k-server-problem/) on every metric with more than $k$ points, since a uniform metric is a special case. The conjecture that $O(\log k)$ holds on every metric was disproved by Bubeck, Coester and Rabani (2023).
- **Predictions.** [Learning-augmented marking](/learning-augmented-marking/) keeps a ratio of $O(\log k)$ when predictions are bad, so the bound $H_k$ limits how robust such algorithms can be.

## Tightness

The bound is exact, by part 2. The table gives $H_k$, the expected phase length $(k + 1)H_k$ of the random input, and the deterministic ratio $k$.

| $k$ | 1 | 2 | 3 | 4 | 8 | 16 | 100 |
|---|---|---|---|---|---|---|---|
| $H_k$ | 1 | 3/2 | 11/6 | 25/12 | 2.7179 | 3.3807 | 5.1874 |
| $(k + 1)H_k$ | 2 | 9/2 | 22/3 | 125/12 | 24.46 | 57.47 | 523.9 |
| deterministic ratio | 1 | 2 | 3 | 4 | 8 | 16 | 100 |
| MARK ratio $2H_k - 1$ | 1 | 2 | 8/3 | 19/6 | 4.436 | 5.761 | 9.375 |

For $k = 1$ the bound is 1: with one slot, every algorithm, online or offline, faults at each change of page. For $k = 2$ the random input has phases of $4.5$ requests on average, an online rule faults on a third of them, so $1.5$ per phase, while the offline rule faults once per phase.

## History

Yao (1977) stated the principle that a lower bound for deterministic algorithms on a random input is a lower bound for randomized algorithms. Fiat, Karp, Luby, McGeoch, Sleator and Young (1991) used it to prove the lower bound $H_k$, and gave MARK with ratio $2H_k$. McGeoch and Sleator (1991) found Partition, the first $H_k$-competitive algorithm, which shows that the bound is tight. Achlioptas, Chrobak and Noga (2000) gave Equitable, a simpler $H_k$-competitive algorithm, and proved that the ratio of MARK is exactly $2H_k - 1$.

## References
