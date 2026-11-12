---
title: The sliding window log passes exactly the requests that keep at most n passed requests in every window of length w, and an exact limiter needs log2 C(W, n) bits for W ticks per window
proves: [correctness]
status: full
---

**Setup.** The log has a limit $n \ge 1$ and a window length $w > 0$. Requests arrive at times $t_1 \le t_2 \le \cdots \le t_M$, and the log runs lines L1 to L6 for each of them in order. $A$ is the set of indices of the requests that pass. A set $K$ of request indices *fits* the rule $(n, w)$ when any $n + 1$ requests of $K$ span at least $w$: for $i_0 < i_1 < \cdots < i_n$ in $K$, $t_{i_n} - t_{i_0} \ge w$. An interval of length $w$ that is open at one end, such as $(s - w, s]$ or $[s, s + w)$, has a span below $w$ between any two of its points, so a set that fits has at most $n$ requests in each such interval. Conversely, if $n + 1$ requests span less than $w$, the interval $(t_{i_n} - w, t_{i_n}]$ holds all of them. So "fits" is the same as "at most $n$ in each window $(s - w, s]$".

**Lemma 1 (invariant).** After request $j$ is handled, the log holds, oldest first, the times of the passed requests $i \le j$ with $t_i > t_j - w$.

*Proof.* By induction on $j$. Before request $j$ the log holds the passed times greater than $t_{j-1} - w$, in order (for $j = 1$ it is empty). A passed time $t_i \le t_{j-1} - w$ that left the log earlier also has $t_i \le t_j - w$, since $t_{j-1} \le t_j$. Lines L1 and L2 remove the times $\le t_j - w$ from the front. The log is sorted, so they are all at the front, and the loop stops at the first time $> t_j - w$. So after line L2 the log holds the passed times before $j$ in $(t_j - w, t_j]$. If $j$ passes, line L4 appends $t_j$, which is the largest time so far, so the log stays sorted and the claim holds for $j$. $\square$

**Theorem 1 (the rule).** Request $j$ passes if and only if fewer than $n$ passed requests before it lie in $(t_j - w, t_j]$.

*Proof.* At line L3 the log length is that number, by Lemma 1 and lines L1 and L2. $\square$

**Theorem 2 (soundness).** The passed requests fit $(n, w)$.

*Proof.* Let $i_0 < \cdots < i_n$ be in $A$. When $i_n$ passed, by Theorem 1 fewer than $n$ passed requests before it lay in $(t_{i_n} - w, t_{i_n}]$. The $n$ requests $i_0, \ldots, i_{n-1}$ passed before $i_n$ and have times at most $t_{i_n}$, so at least one of them has a time $\le t_{i_n} - w$. Since $t_{i_0}$ is the smallest of them, $t_{i_0} \le t_{i_n} - w$. $\square$

**Theorem 3 (greedy).** Request $j$ passes if and only if the passed requests before $j$, together with $j$, fit $(n, w)$.

*Proof.* If $j$ passes, the set $A \cap \{1, \ldots, j\}$ fits by Theorem 2 applied to the first $j$ requests. If $j$ is rejected, then by Theorem 1 there are $n$ passed requests before $j$ in $(t_j - w, t_j]$; with $j$ they are $n + 1$ requests in an interval that is open at one end and of length $w$, so they span less than $w$, and the set does not fit. $\square$

**Corollary 1 (tight).** If the whole input fits $(n, w)$, every request passes. So the log rejects a request only when the rule forces it.

*Proof.* By induction on $j$: if requests $1$ to $j - 1$ passed, the set of them with $j$ is a subset of the input, so it fits, and $j$ passes by Theorem 3. $\square$

**Corollary 2 (token bucket bound).** Each interval of length $\tau \ge 0$ holds at most $n(\lfloor \tau / w \rfloor + 1) \le (n/w)\tau + n$ passed requests. So the output conforms to a token bucket with rate $n/w$ and depth $n$.

*Proof.* Let the interval be inside $[a, a + \tau]$ and let $q = \lfloor \tau / w \rfloor$. The $q + 1$ intervals $[a + iw, a + (i + 1)w)$ for $i = 0, \ldots, q$ cover $[a, a + (q+1)w)$, which contains $[a, a + \tau]$ because $(q + 1)w > \tau$. Each of them holds at most $n$ passed requests by Theorem 2. $\square$

**Lemma 2 (the ring).** Let the ring hold the times of the last $n$ passed requests. Then fewer than $n$ passed requests lie in $(t - w, t]$ if and only if fewer than $n$ requests passed so far, or the oldest time in the ring is $\le t - w$.

*Proof.* The passed times are in order. Fewer than $n$ of them lie in $(t - w, t]$ if and only if the $n$-th most recent passed time, when it exists, is $\le t - w$. That time is the oldest in the ring. $\square$

So the ring version makes the same decisions as the log, with $\Theta(1)$ work per request.

**Theorem 4 (memory lower bound).** Let the times be integers (ticks) and $w = W$ ticks, with $1 \le n \le W$. Each deterministic limiter that makes the same decisions as the rule of Theorem 1 has at least $\binom{W}{n}$ different states, so in the worst case it needs at least $\log_2 \binom{W}{n}$ bits per key.

*Proof.* For each set $S$ of $n$ distinct times in $\{0, 1, \ldots, W - 1\}$, send one request at each time of $S$ in order. These $n$ requests span at most $W - 1 < w$ and there are only $n$ of them, so all pass. Let $\sigma(S)$ be the state of the limiter after them. For a tick $u$ with $W \le u < 2W$, a burst of $n$ requests at time $u$ from state $\sigma(S)$ passes exactly $c_S(u) = |\{s \in S : s \le u - W\}|$ requests: the passed requests in $(u - W, u]$ are the $n - c_S(u)$ times of $S$ above $u - W$, so by Theorem 1 the requests of the burst pass one by one until the window holds $n$. The function $c_S$ on $u = W, \ldots, 2W - 1$ determines $S$, because $s \in S$ if and only if $c_S(s + W) - c_S(s + W - 1) = 1$ (with $c_S(W - 1) = 0$). So two different sets lead to two states that answer some burst differently, and the states differ. There are $\binom{W}{n}$ sets. $\square$

Since $\binom{W}{n} \ge (W/n)^n$, the bound is at least $n \log_2 (W/n)$ bits. The log stores $n$ times; if each is kept relative to the window, it takes about $\log_2 W$ bits. For $n \le \sqrt{W}$ we have $\log_2 (W/n) \ge \tfrac12 \log_2 W$, so the log is within a factor of 2 of the least memory an exact limiter can use.
