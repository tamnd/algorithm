---
title: The false positive rate of a Bloom filter
proves: [false-positive-rate]
status: full
---

**Model.** Ideal hashing: the values $h_i(y)$, over all keys $y \in U$ and all $i \in \{1, \ldots, k\}$, are independent and uniform on $\{0, \ldots, m - 1\}$. Insert $n$ distinct keys $S$, and let $x \notin S$. Let $X$ be the number of positions $j$ with $B[j] = 1$, and let $\varepsilon = \Pr[\text{QUERY}(x) = \text{true}]$.

**Claim 1 (the exact rate).** $\varepsilon = \mathbb{E}[(X/m)^k]$.

*Proof.* By the correctness proof, $B$ is a function of the $kn$ values $h_i(y)$ for $y \in S$, and QUERY$(x)$ returns true exactly when $B[h_i(x)] = 1$ for each $i$. The $k$ values $h_i(x)$ are independent of the values for $S$, because $x \notin S$, and independent of each other. Given $B$, each $h_i(x)$ hits a 1 bit with probability $X/m$, so the conditional probability that all $k$ hit a 1 bit is $(X/m)^k$. Taking the expectation over $B$ gives the claim. $\square$

**Claim 2 (the mean of $X$).** $\mathbb{E}[X] = m\left(1 - (1 - 1/m)^{kn}\right)$.

*Proof.* Position $j$ stays 0 exactly when none of the $kn$ independent values $h_i(y)$, $y \in S$, equals $j$. Each misses $j$ with probability $1 - 1/m$, so position $j$ is 0 with probability $(1 - 1/m)^{kn}$. By [linearity of expectation](/linearity-of-expectation/) over the $m$ positions, $\mathbb{E}[m - X] = m(1 - 1/m)^{kn}$. $\square$

**Claim 3 (the classical formula is a lower bound).**
$$ \varepsilon \ge \left(1 - \left(1 - \tfrac1m\right)^{kn}\right)^k \ge \left(1 - e^{-kn/m}\right)^k. $$

*Proof.* The function $t \mapsto t^k$ is convex on $[0, 1]$ for $k \ge 1$, so by [Jensen's inequality](/jensens-inequality/) $\mathbb{E}[(X/m)^k] \ge (\mathbb{E}[X]/m)^k$. Claim 2 gives the first inequality. The second follows from $1 - 1/m \le e^{-1/m}$, which makes $1 - (1 - 1/m)^{kn} \ge 1 - e^{-kn/m}$, and from the fact that $t \mapsto t^k$ is increasing on $[0, 1]$. $\square$

**Claim 4 (concentration).** For each $\lambda > 0$, $\Pr[X \ge \mathbb{E}[X] + \lambda] \le e^{-2\lambda^2/(kn)}$. Hence, with $p = \mathbb{E}[X]/m$,
$$ \varepsilon \le \left(p + \tfrac{\lambda}{m}\right)^k + e^{-2\lambda^2/(kn)}. $$

*Proof.* $X$ is a function of the $kn$ independent values $h_i(y)$. Changing one of them moves at most one 1 bit, so it changes $X$ by at most 1. The bounded differences inequality (McDiarmid's form of the [Azuma inequality](/azuma-inequality/)) then gives the tail bound. For the second part, split on the event $E = \{X < \mathbb{E}[X] + \lambda\}$. On $E$, $(X/m)^k \le (p + \lambda/m)^k$. Off $E$, $(X/m)^k \le 1$, and $\Pr[\bar E]$ is at most the tail bound. Claim 1 adds the two parts. $\square$

**Consequence.** Take $\lambda = \sqrt{kn \ln m}$. Then the second term is $m^{-2}$, and $\lambda/m = O(\sqrt{(\log m)/m})$ when $kn = O(m)$. So $\varepsilon = (1 - (1 - 1/m)^{kn})^k + O(k\sqrt{(\log m)/m}) + O(m^{-2})$, and for fixed $k$ and a fixed ratio $m/n$ the rate tends to $(1 - e^{-kn/m})^k$ as $m \to \infty$, since $(1 - 1/m)^{kn} \to e^{-kn/m}$.

**Probes of a query.** For $x \notin S$, given $B$, the rounds of line L6 look at independent uniform positions, and each one is 0 with probability $1 - X/m$. The loop stops at the first 0 or after $k$ rounds, so the number of rounds is at most a geometric random variable with mean $1/(1 - X/m)$ when $X < m$. $\blacksquare$
