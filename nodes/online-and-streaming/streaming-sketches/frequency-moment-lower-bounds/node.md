---
tag: 7C0H0K
kind: theorem
slug: frequency-moment-lower-bounds
name: Frequency moment lower bounds
aliases:
- Alon-Matias-Szegedy lower bounds
- Bar-Yossef-Jayram-Kumar-Sivakumar bounds
- F_k space lower bounds
area: online-and-streaming/streaming-sketches
level: research
summary: Space lower bounds for F_k estimation, showing F_k needs polynomial space for k > 2.
prereqs: [frequency-moment-problem, disjointness-problem, randomized-communication-complexity, number-in-hand-model, streaming-model]
see_also: [index-problem-lower-bound, ams-sketch, indyk-p-stable-sketch, information-complexity, gap-hamming-distance, communication-complexity, join-size-estimation-problem, frequent-items-problem]
sources:
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999 (STOC 1996)
    locator: Section 3, the lower bounds, with Ω(n^(1 − 5/k)) for F_k, Ω(n) for F_∞, and Ω(n) for deterministic algorithms (section number to check)
  - paper: doi:10.1016/j.jcss.2003.11.006
    title: Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar and D. Sivakumar, An information statistics approach to data stream and communication complexity, Journal of Computer and System Sciences 68(4), 2004 (FOCS 2002)
    locator: the lower bounds for multi-party promise disjointness and the resulting bounds for F_k (to check)
  - paper: doi:10.1109/CCC.2003.1214414
    title: Amit Chakrabarti, Subhash Khot and Xiaodong Sun, Near-optimal lower bounds on the multi-party communication complexity of set disjointness, Proceedings of the 18th IEEE Conference on Computational Complexity, 2003
    locator: the bounds Ω(n/(t log t)) for general protocols and Ω(n/t) for one-way protocols, and the corollaries for F_k (to check)
  - paper: doi:10.1145/1060590.1060621
    title: Piotr Indyk and David Woodruff, Optimal approximations of the frequency moments of data streams, Proceedings of the 37th ACM Symposium on Theory of Computing (STOC), 2005
    locator: the matching upper bound n^(1 − 2/k) times polylogarithmic factors (to check)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 10, Lower bounds for summaries (disjointness and the frequency moments)
---

The frequency moment lower bounds show that estimating $F_k = \sum_i f_i^k$ in one pass needs space polynomial in the universe size $n$ when $k > 2$, and space linear in $n$ for $F_\infty = \max_i f_i$. Alon, Matias and Szegedy (1996) proved $\Omega(n)$ for $F_\infty$ and $\Omega(n^{1 - 5/k})$ for $F_k$ by reductions from set disjointness. Better bounds for multi-party disjointness, by Bar-Yossef, Jayram, Kumar and Sivakumar (2002, journal 2004) and by Chakrabarti, Khot and Sun (2003), raised the exponent to $1 - 2/k$, which matches the upper bound of Indyk and Woodruff (2005) up to polylogarithmic factors. So $k = 2$ is the exact threshold between polylogarithmic and polynomial space for the [frequency moment problem](/frequency-moment-problem/). This page proves the reductions in full and cites the communication bounds.

## Statement

The model is the insertion-only stream over $[n]$ with $m \le n \cdot t$ items, and the algorithms are randomized with failure probability at most $1/3$, using any number of random bits. Space is counted in bits. $t$-party promise disjointness, $\mathrm{DISJ}_{n,t}$, is the problem where each of $t$ players holds a set $S_j \subseteq [n]$, with the promise that either the sets are pairwise disjoint (NO), or they share exactly one element and are otherwise pairwise disjoint (YES). In the number-in-hand model, the players communicate by messages; write $C_{n,t}$ for its randomized communication complexity, and $C^{\to}_{n,t}$ for one-way protocols where player $j$ sends one message to player $j + 1$.

**Theorem 1 ($F_\infty$).** Any $q$-pass streaming algorithm that, with probability at least $2/3$, tells $F_\infty \le 1$ from $F_\infty \ge 2$ uses $\Omega(n/q)$ bits. In particular, an estimate of $F_\infty$ within a factor below 2 needs $\Omega(n)$ bits in one pass.

**Theorem 2 (the reduction for $F_k$).** Let $k > 1$, $0 < \varepsilon \le 1/3$, and let $t \ge 2$ satisfy $t^k > 2n$. Any $q$-pass streaming algorithm that outputs a $(1 \pm \varepsilon)$ estimate of $F_k$ with probability at least $2/3$ uses
$$ s \ge \frac{C_{n,t}}{qt} \text{ bits, and } s \ge \frac{C^{\to}_{n,t}}{t - 1} \text{ bits for } q = 1 . $$

**Corollary (the bounds for $F_k$, $k > 2$).** With $t = \Theta(n^{1/k})$, Theorem 2 and the cited communication bounds give:

| communication bound | source | space for a $(1 \pm \frac13)$ estimate of $F_k$ |
|---|---|---|
| $C_{n,t} = \Omega(n/t^4)$ | Alon, Matias, Szegedy 1996 | $\Omega(n^{1 - 5/k})$ bits, constant passes |
| $C_{n,t} = \Omega(n/t^2)$ | Bar-Yossef, Jayram, Kumar, Sivakumar 2004 | $\Omega(n^{1 - 3/k})$ bits, constant passes |
| $C^{\to}_{n,t} = \Omega(n/t^{1+\gamma})$ for any $\gamma > 0$ | Bar-Yossef, Jayram, Kumar, Sivakumar 2004 | $\Omega(n^{1 - (2+\gamma)/k})$ bits, one pass |
| $C^{\to}_{n,t} = \Omega(n/t)$ | Chakrabarti, Khot, Sun 2003 | $\Omega(n^{1 - 2/k})$ bits, one pass |
| $C_{n,t} = \Omega(n/(t \log t))$ | Chakrabarti, Khot, Sun 2003 | $\Omega(n^{1 - 2/k} / \log n)$ bits, constant passes |
| $C_{n,t} = \Omega(n/t)$ | Gronemeier 2009, Jayram 2009 | $\Omega(n^{1 - 2/k})$ bits, constant passes |

The exponents follow from $s \ge C/(qt)$ and $t^k = \Theta(n)$: for example $n/t^2 = n \cdot n^{-2/k}$. The exact forms and hypotheses of the cited communication bounds are in the sources; only the reductions are proved here.

## In plain words

Give each of several people a set of numbers, and promise that either all sets are apart, or all of them share one number and are otherwise apart. Put all sets into one stream, one after the other. If they share a number, that number occurs once for each person, and a high power of its count is large. If they do not, every count is one, and the sum of powers is at most the number of possible items.

So a good estimate of a high moment tells the two cases apart. A streaming algorithm can be run by the people in turn, each handing over its memory to the next. If finding a shared number needs much talk in total, then the memory must be large. With two people and the largest count, the memory must be close to the size of the universe.

## Proof

**Lemma (simulation).** Let $A$ be a $q$-pass streaming algorithm with $s$ bits of memory, and let the stream be $\sigma_1 \sigma_2 \cdots \sigma_t$, where player $j$ knows only $\sigma_j$. Then the players can compute the output of $A$ with $q(t - 1) + (q - 1)$ messages of $s$ bits, using public random bits for the coins of $A$. For $q = 1$ this is a one-way protocol from player 1 to player $t$.

*Proof.* In each pass, player 1 runs $A$ on $\sigma_1$ from the current memory state and sends the state to player 2, who continues on $\sigma_2$, and so on up to player $t$. Between passes, player $t$ sends the state back to player 1. Each player processes the items of its own part with the same random bits as $A$ would use, so the final state, and the output, are those of $A$ on the whole stream. There are $t - 1$ messages in each pass and $q - 1$ messages between passes. $\square$

**Proof of Theorem 1.** Let Alice and Bob hold $A, B \subseteq [n]$, an instance of two-party set disjointness. Let $\sigma_1$ list the elements of $A$ and $\sigma_2$ the elements of $B$, each once. In the stream $\sigma_1 \sigma_2$, item $i$ occurs $1[i \in A] + 1[i \in B]$ times. So $F_\infty = 2$ if $A \cap B \ne \emptyset$, and $F_\infty \le 1$ otherwise. An algorithm that tells $F_\infty \le 1$ from $F_\infty \ge 2$ with probability $2/3$ therefore decides disjointness with probability $2/3$. By the lemma with $t = 2$, this is a protocol with at most $2q \cdot s$ bits. The randomized communication complexity of two-party disjointness is $\Omega(n)$ (Kalyanasundaram and Schnitger 1992, Razborov 1992), and this holds even under the promise $|A \cap B| \le 1$. So $2qs = \Omega(n)$ and $s = \Omega(n/q)$. An estimate $\hat F$ with $F_\infty \le \hat F < 2F_\infty$, or any estimate within a factor $c < 2$ after rescaling, tells the two cases apart, which gives the second claim. $\square$

**Proof of Theorem 2.** Take an instance $S_1, \ldots, S_t$ of $\mathrm{DISJ}_{n,t}$ and let $\sigma_j$ list the elements of $S_j$, each once. In the stream $\sigma_1 \cdots \sigma_t$, the count of item $i$ is the number of sets that contain it.

- NO instance: the sets are pairwise disjoint, every count is 0 or 1, and $F_k = \sum_j |S_j| \le n$.
- YES instance: the common element has count $t$, so $F_k \ge t^k > 2n$.

A $(1 \pm \varepsilon)$ estimate $\hat F$ with $\varepsilon \le 1/3$ is at most $(1 + \varepsilon) n \le \frac{4}{3} n$ on a NO instance and at least $(1 - \varepsilon) t^k > \frac{2}{3} \cdot 2n = \frac{4}{3} n$ on a YES instance. So the rule "YES if $\hat F > (1 + \varepsilon) n$" decides $\mathrm{DISJ}_{n,t}$ whenever the estimate is good, with probability at least $2/3$. By the lemma, this is a protocol with $(q(t-1) + q - 1) s < qts$ bits, so $qts \ge C_{n,t}$. For $q = 1$, it is a one-way protocol with $(t-1) s$ bits, so $(t-1)s \ge C^{\to}_{n,t}$. $\square$

**Proof of the corollary.** Take $t = \lceil (2n + 1)^{1/k} \rceil$, so $t^k > 2n$ and $t = \Theta(n^{1/k})$; for $k > 2$ this is at most $n$ for large $n$. Substituting a bound $C = \Omega(n / t^a)$ in $s \ge C/(qt)$ gives $s = \Omega(n / t^{a+1}) = \Omega(n^{1 - (a+1)/k})$ for constant $q$. With $a = 4$ this is $n^{1 - 5/k}$; with $a = 2$, $n^{1-3/k}$; with $a = 1$, $n^{1 - 2/k}$. For one-way bounds, $s \ge C^{\to}/(t - 1)$ gives the same exponents. A factor $1/\log t$ in $C$ becomes a factor $1/\log n$ in $s$, up to the constant $k$. $\blacksquare$

The tests check the two reductions on small instances: $F_\infty$ against disjointness on all pairs of subsets of a 5-element set, and the gap $F_k \le n$ against $F_k \ge t^k$ on random promise instances.

## Consequences

- **The threshold at $k = 2$.** For $k \le 2$, $F_k$ has $(1 \pm \varepsilon)$ estimates in $O(\varepsilon^{-2} \log n)$ bits, by the [AMS sketch](/ams-sketch/) and the [Indyk p-stable sketch](/indyk-p-stable-sketch/). For every $k > 2$, the space is $n^{1 - 2/k}$ up to lower-order factors. The exponent $1 - 2/k$ tends to 1 as $k$ grows, in line with the $\Omega(n)$ bound for $F_\infty$.
- **Approximating the largest count.** With $t$ players, a YES instance has $F_\infty = t$ and a NO instance has $F_\infty \le 1$. So an estimate of $F_\infty$ within a factor below $t$ decides $\mathrm{DISJ}_{n,t}$, and the lemma with the $\Omega(n/t)$ bound gives $\Omega(n/t^2)$ bits for constant passes. A constant factor costs $\Omega(n)$ bits.
- **Exact and deterministic computation.** Exact $F_k$ for $k \ne 1$ needs $\Omega(n)$ bits by the same reduction with $t = 2$: exact $F_k$ for $k \ne 1$ tells $|A \cap B| = 0$ from $|A \cap B| = 1$ when $|A|$ and $|B|$ are known. Alon, Matias and Szegedy also showed that deterministic algorithms need $\Omega(n)$ bits for a $(1 \pm 0.1)$ estimate of $F_k$, $k \ne 1$.
- **Dependence on $\varepsilon$.** For every $k \ne 1$, $\Omega(\varepsilon^{-2})$ bits are needed, by a reduction from the [gap Hamming problem](/gap-hamming-distance/) (Indyk and Woodruff 2003, Woodruff 2004), which in turn reduces from [INDEX](/index-problem-lower-bound/).

## Tightness

- **$F_\infty$.** Keeping an exact count for each item uses $O(n \log m)$ bits, and $q$ passes over $n/q$ items each use $O((n/q) \log m)$ bits. So Theorem 1 is tight up to the $\log m$ factor.
- **$F_k$ for $k > 2$.** Indyk and Woodruff (2005) gave a one-pass algorithm with $n^{1 - 2/k} \cdot \mathrm{poly}(\varepsilon^{-1} \log n)$ bits. Later algorithms removed most of the polylogarithmic factors. So the exponent $1 - 2/k$ is exact.
- **The reduction itself.** The promise disjointness approach cannot give more than about $n^{1 - 2/k}$. In a NO instance some set has at most $n/t$ elements, so the players can announce their set sizes, let the player with the smallest set send it in $O((n/t) \log n)$ bits, and let each other player say in one bit whether it holds one of those elements. With $C_{n,t} = O((n/t) \log n + t \log n)$, the bound $s \ge C_{n,t}/(qt)$ is at most $O(n^{1 - 2/k} \log n)$.
- **Earlier exponents.** The bound $n^{1 - 5/k}$ of Alon, Matias and Szegedy is non-trivial only for $k > 5$, and $n^{1 - 3/k}$ only for $k > 3$. The progress came from information complexity, which gave the tight $\Omega(n/t)$ bounds for $\mathrm{DISJ}_{n,t}$.

## History

Alon, Matias and Szegedy (STOC 1996) proved the first space lower bounds for streams: $\Omega(n)$ for $F_\infty$ and for deterministic approximation of $F_k$, $k \ne 1$, and $\Omega(n^{1 - 5/k})$ for $F_k$ through a multi-party disjointness bound of $\Omega(n/t^4)$. Bar-Yossef, Jayram, Kumar and Sivakumar (FOCS 2002, JCSS 2004) introduced the information statistics method and proved $\Omega(n/t^2)$ for general protocols, which gave the first bounds close to $n^{1 - 2/k}$. Chakrabarti, Khot and Sun (CCC 2003) proved $\Omega(n/t)$ for one-way protocols, giving $\Omega(n^{1 - 2/k})$ for one pass. Gronemeier (2009) and Jayram (2009) proved $\Omega(n/t)$ for general protocols. Indyk and Woodruff (STOC 2005) gave the matching upper bound, which closed the question of the exponent.

## References
