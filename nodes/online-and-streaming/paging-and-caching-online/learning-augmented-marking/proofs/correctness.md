---
title: Predictive Marker is a marking rule, is 2-competitive with perfect predictions, and is O(log k)-competitive for every predictor
proves: [correctness]
status: sketch
---

**Setting.** The cache has $k$ slots and starts empty. Phases, marks, clean and stale pages, and chains are as on the main page. Let $P$ be the number of phases, and let $c_r$ be the number of clean pages of phase $r$, with $c_1 = $ the number of distinct pages of phase $1$.

**Lemma 1 (a marking rule).** After each request, the marked pages are exactly the distinct pages requested so far in the current phase, all of them are in the cache, and the rule never evicts a marked page. Each eviction finds an unmarked page.

*Proof.* Line L6 unmarks all pages exactly when a phase starts, and lines L4, L7 and L12 mark the requested page. Lines L10 and L11 choose only unmarked pages, so a marked page stays in the cache until the phase ends. If the cache is full and $x$ is not in it, then not all $k$ cached pages are marked, unless line L6 has just unmarked them. So line L10 or L11 has a page to choose. $\square$

**Lemma 2 (the deterministic bound).** $\mathrm{ALG} \le k P \le k \cdot \mathrm{OPT}$.

*Proof.* Each miss marks a new distinct page of the phase, so a phase has at most $k$ misses. For the bound on $\mathrm{OPT}$: the first request is a miss for every rule. For $r < P$, let $p$ be the first page of phase $r$. From the second request of phase $r$ to the first request of phase $r + 1$, there are $k$ distinct pages other than $p$. Each rule holds $p$ just after its request, so it has at most $k - 1$ of them, and it misses at least once in this window. The windows for $r = 1, \ldots, P - 1$ are disjoint and do not contain the first request. So $\mathrm{OPT} \ge P$. $\square$

**Lemma 3 (chains).** In a phase $r \ge 2$, each miss either is clean and starts a chain of length $1$, or is stale and adds $1$ to the length of one chain. So the cost of the phase is the sum of the chain lengths, and there are $c_r$ chains. Each stale miss has a chain.

*Proof.* By Lemma 1, the pages in the cache at the start of phase $r$ are the $k$ pages of phase $r - 1$. A stale page is one of them. If a request to it is a miss, it was evicted earlier in phase $r$, and line L12 put it in a chain then. The rest is lines L8 and L9. $\square$

**Lemma 4 (the clean pages).** $\sum_{r=1}^{P} c_r \le 2 \cdot \mathrm{OPT}$.

*Proof.* In phase $1$, every rule loads $c_1$ distinct pages into an empty cache. For $r \ge 2$, consider the requests from the second request of phase $r - 1$ to the end of phase $r$. Let $p$ be the first page of phase $r - 1$. These requests contain the $k - 1$ other pages of phase $r - 1$ and the $c_r$ clean pages of phase $r$, which are not pages of phase $r - 1$, so $k - 1 + c_r$ distinct pages other than $p$. Each rule holds $p$ at the start of this window, so it misses at least $c_r$ times in the window. Each request lies in at most two of these windows, one for phase $r$ and one for phase $r + 1$, so the windows of even $r$ are disjoint and those of odd $r$ are disjoint. With $\mathrm{OPT}_{even}$ and $\mathrm{OPT}_{odd}$ the misses of the optimum in each family, $\sum_r c_r \le \mathrm{OPT}_{even} + \mathrm{OPT}_{odd} \le 2 \cdot \mathrm{OPT}$, where phase $1$ counts with the odd family and its window is all of phase $1$. $\square$

**Theorem 5 (consistency).** If $h_i = y_i$ for all $i$, then no stale miss happens, no random choice is made, and $\mathrm{ALG} = \sum_r c_r \le 2 \cdot \mathrm{OPT}$.

*Proof.* Take an eviction in phase $r$, at a miss on $x$, and let $m$ be the number of marked pages before $x$ is marked. The cache holds $k$ pages, so there are $k - m$ unmarked pages in it. The phase has $k$ distinct pages in total, and $m + 1$ of them, the marked pages and $x$, are already known. So at most $k - m - 1$ of the $k - m$ unmarked pages are requested later in phase $r$, and at least one of them, say $q$, is not. The next request of $q$ is after the end of phase $r$, so it is later than the next request of each unmarked page that is requested in phase $r$. With perfect predictions, $\mathrm{pred}[q]$ is this true time, so line L10 evicts a page that is not requested again in phase $r$ (a page with the same prediction is also not requested in the phase). So no evicted page comes back in its phase, and there is no stale miss. By Lemma 3, each chain has length $1 \le H_k$, line L11 never runs, and the cost of phase $r$ is $c_r$. Lemma 4 completes the proof. $\square$

**Theorem 6 (robustness, sketch).** For every predictor, $\mathbb{E}[\mathrm{ALG}] \le 2 H_k \sum_r c_r \le 4 H_k \cdot \mathrm{OPT}$.

*Sketch.* By Lemma 3 it is enough to show that each chain has expected length at most $2 H_k$. The first $\lfloor H_k \rfloor$ steps of a chain cost at most $H_k$. After that, each step evicts a uniformly random unmarked page. The chain grows again only if the evicted page is requested later in the same phase. This is the situation of [randomized marking](/randomized-marking/): order the unmarked pages by their next request; if $u$ pages are unmarked, the evicted page is the $j$-th in this order with probability $1/u$, and the chain can continue only through the $j - 1$ pages before it. The usual argument of Fiat, Karp, Luby, McGeoch, Sleator and Young then bounds the expected number of further steps by $H_k$. Lemma 4 gives the second inequality. Lykouris and Vassilvitskii (2021) give the full proof. $\square$

**Theorem 7 (smoothness, cited).** For the absolute loss and an $\epsilon$-accurate predictor, $\mathbb{E}[\mathrm{ALG}] \le \min(2 + 2\sqrt{5 \epsilon}, 4 H_k) \cdot \mathrm{OPT}$ (Lykouris and Vassilvitskii 2021, Theorem 3.3 and its corollary). The proof charges each step of a chain beyond the first to the prediction errors of the pages in the chain: an evicted page with the largest prediction that comes back in the same phase must have an error at least the gap to a page that does not come back. This part is not repeated here. $\blacksquare$

The tests check Lemma 1 against an independent computation of the phases, Lemma 2, the chain structure of Lemma 3 and the rule that random choices happen only after length $H_k$, Theorem 5 on random sequences, and the bound of Theorem 6 as an average over random runs with reversed predictions.
