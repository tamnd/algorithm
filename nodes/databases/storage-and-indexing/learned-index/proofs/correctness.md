---
title: An RMI with stored error bounds finds every present key and reports every absent key as absent
proves: [correctness]
status: full
---

Notation as on the page. $K[0..n-1]$ is sorted with distinct keys, $\rho$ is the routing function of line L2, and for each nonempty $D_j$ the bounds $e_{lo}(j)$ and $e_{hi}(j)$ are computed in line L4.

**Lemma 1 (invariant).** For every $i$ and $j = \rho(K[i])$, with $p = \lfloor f_j'(K[i]) \rfloor$: $e_{lo}(j) \le i - p \le e_{hi}(j)$.

*Proof.* Line L2 puts $i$ into $D_j$ for $j = \rho(K[i])$. Line L4 sets $e_{lo}(j)$ to the minimum and $e_{hi}(j)$ to the maximum of $i' - \lfloor f_j'(K[i']) \rfloor$ over all $i' \in D_j$, and $i$ is one of them. $\square$

This lemma does not depend on the quality of the models: any $f_1$ and $f_j'$ satisfy it, since the bounds are measured, not assumed.

**Theorem 1 (present keys).** If $k = K[i]$, LOOKUP$(k)$ returns $i$.

*Proof.* Line L5 computes $j = \rho(k)$, the same value as line L2 computed for $i$, because $\rho$ is a fixed function of the key and exact arithmetic gives the same result each time. So $i \in D_j$, $D_j$ is not empty, and line L6 does not return. Line L7 computes the same $p$ as line L4 used for $i$. By Lemma 1, $p + e_{lo}(j) \le i \le p + e_{hi}(j)$, and $0 \le i \le n - 1$, so $lo \le i \le hi$ after line L8. The subarray $K[lo..hi]$ is sorted and contains $k$ at position $i$, and since the keys are distinct, no other position holds $k$. Binary search on a sorted array keeps the invariant that if $k$ is in $K[lo..hi]$, it is in the current range: when $K[mid] < k$, all of $K[lo..mid]$ is below $k$, and when $K[mid] > k$, all of $K[mid..hi]$ is above it. The range shrinks at each step, so the search reaches $mid = i$ and returns it. $\square$

**Theorem 2 (absent keys).** If $k$ is not in $K$, LOOKUP$(k)$ returns *absent*.

*Proof.* LOOKUP returns a position only at line L10, and only a position $mid$ with $K[mid] = k$. No such position exists. Every other exit (line L6, or an empty range at line L9) returns *absent*. $\square$

**Lemma 2 (window size).** LOOKUP compares $k$ with at most $\lceil \log_2 (w + 1) \rceil$ keys, where $w = e_{hi}(j) - e_{lo}(j) + 1$.

*Proof.* After line L8, $hi - lo + 1 \le w$. Each step of binary search leaves at most $\lfloor (r - 1)/2 \rfloor$ positions out of $r$, so after $t$ steps at most $\lfloor w / 2^t \rfloor$ remain, which is 0 for $2^t > w$. $\square$

**Lemma 3 (PGM segment count).** For an integer $\varepsilon \ge 0$, there is a piecewise linear function with at most $\lceil n / (2\varepsilon + 1) \rceil$ pieces that predicts the position of every key within $\varepsilon$. So the optimal $\varepsilon$-approximation used by the PGM-index has at most this many segments.

*Proof.* Cut the positions into runs $R_t = \{t(2\varepsilon + 1), \ldots, \min(n, (t + 1)(2\varepsilon + 1)) - 1\}$. On the key interval from the first key of $R_t$ up to the first key of $R_{t+1}$, use the constant $c_t = t(2\varepsilon + 1) + \varepsilon$. For $i \in R_t$, $|i - c_t| \le \varepsilon$, since $i - t(2\varepsilon + 1)$ lies in $[0, 2\varepsilon]$. There are $\lceil n / (2\varepsilon + 1) \rceil$ runs. $\square$
