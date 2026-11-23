---
title: Report noisy max is epsilon-DP and picks a nearly best index
proves: [correctness]
status: full
---

We work in the real RAM. Fix a neighbor relation $\sim$, scores $c_1, \ldots, c_m$ with $m \ge 1$, a number $\Delta > 0$ with $|c_i(x) - c_i(x')| \le \Delta$ for all $i$ and all $x \sim x'$, and $\varepsilon > 0$. Let $b$ be the scale of line L1. Line L4 draws $r_i \sim \mathrm{Lap}(b)$, independent for each $i$; the sampler is the one of the Laplace mechanism, and the correctness proof of that page shows that it draws $\mathrm{Lap}(b)$. Let $p_b(z) = \frac{1}{2b}e^{-|z|/b}$.

**Lemma 1 (the loop computes the noisy argmax).** Line L6 returns an index $i$ with $c_i + r_i = \max_j (c_j + r_j)$, the lowest such index if there are ties. Ties have probability 0.

*Proof.* After pass $i$ of the loop, $best = \max_{j \le i}(c_j + r_j)$ and $best\_i$ is the lowest index that attains it: line L5 replaces the pair only when the new value is strictly larger. The first pass replaces $-\infty$, so $best\_i$ is an index. For $i \ne j$ the event $c_i + r_i = c_j + r_j$ fixes $r_i$ given $r_j$, and $r_i$ has a density, so it has probability 0. $\square$

So the output is $M(x) = \arg\max_j (c_j(x) + r_j)$, well defined with probability 1.

**Lemma 2 (shift).** For every $t \in \mathbb R$ and $s \ge 0$, $\Pr[r_i \ge t + s] \ge e^{-s/b}\Pr[r_i \ge t]$.

*Proof.* For every $z$, $|z + s| \le |z| + s$, so $p_b(z + s) \ge e^{-s/b} p_b(z)$. Then $\Pr[r_i \ge t + s] = \int_t^\infty p_b(z + s)\,dz \ge e^{-s/b}\int_t^\infty p_b(z)\,dz$. $\square$

**Lemma 3 (one direction).** Let $x$ and $x'$ be datasets, $i$ an index and $s \ge 0$ a number such that

$$c_i(x) + s \ge c_i(x') + (c_j(x) - c_j(x')) \quad \text{for every } j \ne i. \tag{$*$}$$

Then $\Pr[M(x) = i] \ge e^{-s/b}\Pr[M(x') = i]$.

*Proof.* Fix the noise $r_{-i} = (r_j)_{j \ne i}$. The index $i$ wins on $x'$ when $r_i > t' = \max_{j \ne i}(c_j(x') + r_j) - c_i(x')$, up to a tie of probability 0, and the event is a half-line in $r_i$ because the left side $c_i(x') + r_i$ grows with $r_i$. If $r_i > t' + s$, then for every $j \ne i$,

$$c_i(x) + r_i > c_i(x) + t' + s \ge c_i(x) + c_j(x') + r_j - c_i(x') + s \ge c_j(x) + r_j,$$

where the last step is $(*)$. So $i$ wins on $x$. By Lemma 2 and the independence of $r_i$ from $r_{-i}$, $\Pr[M(x) = i \mid r_{-i}] \ge \Pr[r_i > t' + s] \ge e^{-s/b}\Pr[r_i > t'] = e^{-s/b}\Pr[M(x') = i \mid r_{-i}]$. The expectation over $r_{-i}$ gives the claim. $\square$

**Theorem 1 (privacy).** (a) If the scores are monotone and $b = \Delta/\varepsilon$, then $M$ is $\varepsilon$-DP. (b) In general, if $b = 2\Delta/\varepsilon$, then $M$ is $\varepsilon$-DP.

*Proof.* Fix $x \sim x'$ and an index $i$. A set $S$ of indices has $\Pr[M(x) \in S] = \sum_{i \in S}\Pr[M(x) = i]$, so it is enough to prove $\Pr[M(x) = i] \ge e^{-\varepsilon}\Pr[M(x') = i]$ for every ordered pair of neighbors, because the relation is symmetric.

(a) Assume first $c_j(x') \le c_j(x)$ for all $j$, so $0 \le c_j(x) - c_j(x') \le \Delta$. Then $(*)$ holds with $s = \Delta$: its left side is at least $c_i(x') + \Delta$ and its right side is at most $c_i(x') + \Delta$. If instead $c_j(x') \ge c_j(x)$ for all $j$, then $c_j(x) - c_j(x') \le 0$ and $c_i(x) \ge c_i(x') - \Delta$, so $(*)$ holds again with $s = \Delta$. By monotonicity one of the two cases holds. Lemma 3 with $s/b = \Delta/(\Delta/\varepsilon) = \varepsilon$ gives the bound.

(b) Without monotonicity, $c_i(x) \ge c_i(x') - \Delta$ and $c_j(x) - c_j(x') \le \Delta$, so $(*)$ holds with $s = 2\Delta$. Lemma 3 with $s/b = 2\Delta/(2\Delta/\varepsilon) = \varepsilon$ gives the bound. $\square$

This is the argument of Dwork-Roth Claim 3.9, which treats counts under add/remove neighbors, where case (a) applies with $\Delta = 1$.

**Theorem 2 (accuracy).** For $0 < \beta < 1$, let $i = M(x)$. Then $\Pr[c_i(x) < \max_j c_j(x) - 2b\ln(m/\beta)] \le \beta$.

*Proof.* Let $t = b\ln(m/\beta)$. For each $j$, $\Pr[|r_j| > t] = 2\int_t^\infty p_b = e^{-t/b} = \beta/m$. By the union bound, with probability at least $1 - \beta$ every $|r_j| \le t$. In that event, let $k$ be an index with the largest score. Since $i$ wins, $c_i + r_i \ge c_k + r_k$, so $c_i \ge c_k + r_k - r_i \ge c_k - 2t$. $\square$
