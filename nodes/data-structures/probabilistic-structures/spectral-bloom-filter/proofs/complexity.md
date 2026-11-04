---
title: The error probability of a spectral Bloom filter
proves: [complexity]
status: full
---

**Model.** Assume ideal hashing: the values $h_i(y)$ for all $i \le k$ and all keys $y$ are independent and uniform on $\{0, \ldots, m - 1\}$. Fix the sequence of operations, so that the multiset $f$ does not depend on the hash values; neither rule reads a hash value to decide which key to update. Fix a key $x$, let $Y$ be the set of keys $y \ne x$ with $f_y > 0$, $n = |Y|$, and $B = \bigcup_{y \in Y} H(y)$.

**Theorem 1.** Under either rule, $\Pr[\hat f_x \ne f_x] \le \mathbb{E}[(|B|/m)^k]$. In particular it is at most $\big(1 - (1 - 1/m)^{kn}\big)^k$ up to the gap between the exact and the classical Bloom filter formulas, and it does not depend on the counts.

*Proof.* By Theorems 1 and 2 of the correctness proof, $f_x \le \hat f_x^{\mathrm{MI}} \le \hat f_x^{\mathrm{MS}}$, and $\hat f_x^{\mathrm{MS}} \ne f_x$ only if every $p \in H(x)$ lies in $B$. So for both rules the error implies $H(x) \subseteq B$. The set $B$ is a function of the hash values of the keys in $Y$, which are independent of $h_1(x), \ldots, h_k(x)$. Given $B$, each $h_i(x)$ lies in $B$ with probability $|B|/m$, independently, so
$$ \Pr[H(x) \subseteq B] = \mathbb{E}\big[\Pr[h_1(x), \ldots, h_k(x) \in B \mid B]\big] = \mathbb{E}\big[(|B|/m)^k\big]. $$
This is exactly the probability that a [Bloom filter](/bloom-filter/) with the same $m$ and $k$, built from the $n$ keys of $Y$, accepts $x$, its [false positive rate](/false-positive-rate/). Its classical estimate is $(1 - (1 - 1/m)^{kn})^k \approx (1 - e^{-kn/m})^k$. $\square$

**Theorem 2 (time and space).** Each operation evaluates $k$ hash functions and reads or writes at most $k$ counters, so it takes $\Theta(k)$ time on the word RAM when a counter fits in a word. The array takes $m$ counters. $\blacksquare$
