---
title: The sliding window counter passes at most n requests in each aligned window and at most 2n - 1 in any window of length w, and both bounds are reached
proves: [correctness]
status: full
---

**Setup.** The counter has a limit $n \ge 1$ and a window length $w > 0$. The aligned window $k$ is $W_k = [kw, (k+1)w)$. Requests arrive at times $t_1 \le t_2 \le \cdots \le t_M$, and the counter runs lines L1 to L8 for each of them in order. For a request at time $t \in W_k$ let $f = (t - kw)/w \in [0, 1)$, let $p$ be the number of passed requests in $W_{k-1}$, and let $c$ be the number of passed requests before it in $W_k$. Its estimate is $E = p(1 - f) + c$.

**Lemma 1 (invariant).** At line L5 for a request at time $t \in W_k$, the fields hold $C.k = k$, $C.prev = p$ and $C.cur = c$.

*Proof.* By induction over the requests. After the previous request, at time $t' \in W_{k'}$ with $k' \le k$, the claim for it and the update at line L6 give $C.k = k'$, $C.prev$ equal to the passed requests in $W_{k'-1}$ and $C.cur$ equal to the passed requests in $W_{k'}$ so far. (Before the first request, $C.k$ is none.) Line L1 computes $k$.

1. If $k = k'$, lines L2 and L3 change nothing, and the fields are right for $W_k$.
2. If $k = k' + 1$, line L2 moves $C.cur$, the count of $W_{k'} = W_{k-1}$, into $C.prev$ and sets $C.cur = 0$. No request before this one is in $W_k$, so this is right.
3. If $k > k' + 1$ or there is no previous request, line L3 sets both to 0. No request before this one is in $W_{k-1}$ or $W_k$, because the previous request was in $W_{k'}$ with $k' < k - 1$ and the times do not go back. $\square$

**Theorem 1 (the rule).** A request passes if and only if $p(1 - f) + c + 1 \le n$.

*Proof.* Line L4 computes $f$, and by Lemma 1 the estimate is $p(1-f) + c$. Line L5 tests it. $\square$

**Theorem 2 (aligned windows).** Each aligned window holds at most $n$ passed requests. So the output conforms to a token bucket with rate $n/w$ and depth $2n$, as for the fixed window counter.

*Proof.* Since $p \ge 0$ and $1 - f > 0$, a request passes only if $c + 1 \le n$, so the count of a window never goes above $n$. The second claim then follows as for the fixed window counter: an interval of length $\tau$ meets at most $\lceil \tau/w \rceil + 1$ aligned windows. $\square$

**Theorem 3 (sliding windows).** Each window $J = (s - w, s]$ holds at most $2n - 1$ passed requests.

*Proof.* Let $s \in W_k$. Then $s - w \ge (k - 1)w$, so $J \subseteq W_{k-1} \cup W_k$. Let $a$ be the number of passed requests in $J \cap W_{k-1}$ and $c'$ the number in $J \cap W_k$; let $p$ be the number of passed requests in all of $W_{k-1}$, so $a \le p \le n$ by Theorem 2. If $c' = 0$, the window holds $a \le n \le 2n - 1$. Else let $t \le s$ be the time of the last passed request in $J \cap W_k$, with fraction $f < 1$. Before it, $c' - 1$ requests had passed in $W_k$, so by Theorem 1, $p(1 - f) + c' \le n$. Then

$$a + c' \le p + n - p(1 - f) = n + pf < n + n = 2n,$$

because $p \le n$ and $f < 1$. The count is an integer, so it is at most $2n - 1$. $\square$

**Theorem 4 (both bounds are reached).** For each $n \ge 1$, let $n$ requests come at time $w - w/(2n)$ and then $n$ requests at time $2w - w/n$. Then $2n - 1$ of them pass, and all passed requests lie in one window of length $w$.

*Proof.* The first $n$ requests are in $W_0$, with $p = 0$, so they pass while $c + 1 \le n$: all $n$ pass. The next requests are in $W_1$ with $p = n$ and $f = 1 - 1/n$, so $p(1 - f) = 1$, and a request passes while $1 + c + 1 \le n$, that is for $c = 0, \ldots, n - 2$: $n - 1$ requests pass. The window $(w - w/n, 2w - w/n]$ has length $w$ and holds both groups, since $w - w/(2n) > w - w/n$. $\square$

The first $n$ requests also show that an aligned window can hold $n$, so Theorem 2 is reached too.

**Proposition 5 (it can reject what the exact rule allows).** With $n = 10$ and $w = 60$, let 10 requests come at time 0 and one request at time 61. The counter rejects the last request, although no passed request lies in $(1, 61]$.

*Proof.* At time 61, $k = 1$, $p = 10$, $c = 0$ and $f = 1/60$, so the estimate plus one is $10 \cdot 59/60 + 1 = 10 + 5/6 > 10$. The requests at time 0 are not in $(1, 61]$. $\square$

So the counter is neither sound nor tight for the sliding window rule: it can pass up to $2n - 1$ in a window, and it can reject a request when the window is empty. Both errors come from the assumption that the requests of the previous window were spread evenly over it.
