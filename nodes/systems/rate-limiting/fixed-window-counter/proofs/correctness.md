---
title: The fixed window counter passes at most n requests in each aligned window, at most n (ceil(tau / w) + 1) in any interval of length tau, and 2n in a window of length w is reached
proves: [correctness]
status: full
---

**Setup.** The counter has a limit $n \ge 1$ and a window length $w > 0$. The aligned window $k$ is $W_k = [kw, (k+1)w)$, for each integer $k$. Requests arrive at times $t_1 \le t_2 \le \cdots \le t_m$, and the counter runs lines L1 to L6 for each of them in order. We write $k_j = \lfloor t_j / w \rfloor$, so that $t_j \in W_{k_j}$, and $A$ for the set of indices of the requests that pass. Since the times do not decrease, $k_1 \le k_2 \le \cdots \le k_m$.

**Lemma 1 (invariant).** After request $j$ is handled, $C.k = k_j$ and $C.count = |\{i \in A : i \le j,\ k_i = k_j\}|$, the number of passed requests up to $j$ in the window of $t_j$.

*Proof.* By induction on $j$. Before request $j$, by the claim for $j - 1$ (or by the start state when $j = 1$), $C.count$ is the number of passed requests before $j$ in $W_{C.k}$. Line L1 sets $k = k_j$. If $k_j \ne C.k$, then $k_j > k_{j-1}$, so no request before $j$ is in $W_{k_j}$, and line L2 sets $C.count = 0$, the right number. If $k_j = C.k$, the count is already the number of passed requests before $j$ in $W_{k_j}$. Lines L3 and L4 add 1 if and only if $j$ passes. So after request $j$ the claim holds. $\square$

**Theorem 1 (exact per aligned window).** Request $j$ passes if and only if fewer than $n$ requests before $j$ passed in the window $W_{k_j}$. So each aligned window holds at most $n$ passed requests, and the counter rejects a request only when its window already has $n$.

*Proof.* At line L3, by Lemma 1 and the reset at line L2, $C.count$ is the number of passed requests before $j$ in $W_{k_j}$. The request passes if and only if this number is below $n$. The count of a window starts at 0 and grows by 1 at each pass, so it never passes $n$. $\square$

**Lemma 2 (integers in a short interval).** An interval of real numbers of length $\ell > 0$ that is open at one end or at both ends holds at most $\lceil \ell \rceil$ integers.

*Proof.* Let the integers in it be $c, c + 1, \ldots, c + q - 1$. The interval holds $c$ and $c + q - 1$ and is open at one end, so the distance $q - 1$ between them is less than $\ell$. Thus $q < \ell + 1$, and since $q$ is an integer, $q \le \lceil \ell \rceil$. $\square$

**Theorem 2 (any interval).** Each interval $I$ of the time line of length $\tau > 0$ (open, closed or half-open) holds at most $n\left(\lceil \tau / w \rceil + 1\right)$ passed requests. In particular it holds at most $(n / w)\tau + 2n$, so the passed requests conform to a token bucket with rate $n/w$ and depth $2n$.

*Proof.* Let $I$ have ends $s \le s + \tau$. The window $W_k$ meets $I$ only if $kw \le s + \tau$ and $(k+1)w > s$, that is $s/w - 1 < k \le (s + \tau)/w$. This interval of $k$ has length $\tau/w + 1$ and is open at its left end, so by Lemma 2 at most $\lceil \tau/w + 1 \rceil = \lceil \tau / w \rceil + 1$ windows meet $I$. By Theorem 1 each of them holds at most $n$ passed requests. For the second bound, $\lceil \tau/w \rceil < \tau / w + 1$. A single point lies in one window and so holds at most $n$ passed requests, which covers the case $\tau = 0$ of the token bucket bound. $\square$

**Theorem 3 (the bound is reached).** For each $\varepsilon$ with $0 < \varepsilon \le w$, the input of $n$ requests at time $w - \varepsilon$ followed by $n$ requests at time $w$ makes all $2n$ requests pass. They lie in the interval $[w - \varepsilon, w]$ of length $\varepsilon$, so a window of length $w$ can hold $2n$ passed requests, twice the limit.

*Proof.* The first $n$ requests are in $W_0$ and the next $n$ are in $W_1$. By Theorem 1 the first $n$ requests of each window pass. $\square$

**Corollary 1 (long-run rate).** For each integer $K \ge 1$, the interval $[k w, (k + K) w)$ holds at most $Kn$ passed requests. So over many windows the rate is at most $n / w$, and only the burst at a window edge goes over the limit.

*Proof.* The interval is the union of the $K$ windows $W_k, \ldots, W_{k+K-1}$, and each holds at most $n$ by Theorem 1. $\square$
