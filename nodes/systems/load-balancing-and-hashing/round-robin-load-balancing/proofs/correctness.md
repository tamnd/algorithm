---
title: Round-robin load balancing returns the next backend that is up, and balances request counts exactly
proves: [correctness, termination]
status: full
---

We use the pseudocode RR-PICK of the page. The pool has $n \ge 0$ backends $B[0], \ldots, B[n-1]$, the flags $up[0..n-1]$, and the index $i$ with $0 \le i < n$ when $n \ge 1$. One call reads the flags as they are at the time of the call.

**Claim 1 (one pick).** Let $i_0$ be the index at the start of a call. If some backend is up, the call returns $B[j^*]$, where $j^* = (i_0 + d^*) \bmod n$ and $d^* = \min\{d \in \{0, \ldots, n-1\} : up[(i_0 + d) \bmod n]\}$, and it leaves $i = (j^* + 1) \bmod n$. If no backend is up (or $n = 0$), it returns none and leaves $i = i_0$. The call ends after at most $n$ passes of the loop.

*Proof.* We show the invariant: at the start of pass $t$ of line L1 ($t = 1, 2, \ldots$), $i = (i_0 + t - 1) \bmod n$, and $up[(i_0 + d) \bmod n]$ is false for each $d < t - 1$.

*Initialization.* At $t = 1$, $i = i_0$ and there is no $d < 0$.

*Maintenance.* In pass $t$, line L2 sets $j = (i_0 + t - 1) \bmod n$ and line L3 sets $i = (i_0 + t) \bmod n$. If $up[j]$ holds, line L4 returns $B[j]$. Otherwise pass $t + 1$ starts with $i = (i_0 + t) \bmod n$, and now $up[(i_0 + d) \bmod n]$ is false for each $d < t$.

*Termination.* The loop of line L1 runs at most $n$ times, so the call ends. If it returns in pass $t$, the invariant says that the indices $i_0, \ldots, i_0 + t - 2$ (mod $n$) are down and $(i_0 + t - 1) \bmod n$ is up, so $t - 1 = d^*$ and $j = j^*$, and $i = (j^* + 1) \bmod n$. If it does not return, the invariant at $t = n + 1$ says that all $n$ indices are down, and $i = (i_0 + n) \bmod n = i_0$. Line L5 returns none. For $n = 0$ the loop does not run. $\square$

**Claim 2 (all up).** If all backends stay up, the $k$-th call ($k = 0, 1, 2, \ldots$) after a call that left the index at $i_0$ returns $B[(i_0 + k) \bmod n]$. In each window of $m$ consecutive calls, each backend is returned $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ times.

*Proof.* With all backends up, $d^* = 0$ in Claim 1, so each call returns $B[i]$ and adds one to $i$ modulo $n$. By induction on $k$, call $k$ starts with $i = (i_0 + k) \bmod n$. A window of $m$ consecutive calls returns the indices $(s + k) \bmod n$ for $k = 0, \ldots, m-1$ and some start $s$. Write $m = qn + r$ with $0 \le r < n$. The first $qn$ calls visit each residue exactly $q$ times, and the last $r$ calls visit $r$ distinct residues once each. So each backend gets $q = \lfloor m/n \rfloor$ or $q + 1$ requests, and $q + 1 = \lceil m/n \rceil$ when $r > 0$. $\blacksquare$

**Claim 3 (changes of the up set).** Suppose the set of up backends is fixed during a window of calls and holds $u \ge 1$ backends. Then the calls of the window return the up backends in cyclic order, and each one is returned $\lfloor m/u \rfloor$ or $\lceil m/u \rceil$ times in each sub-window of $m$ calls.

*Proof.* By Claim 1, each call returns the first up backend at or after $i$ in cyclic order and moves $i$ to just after it. So the next call returns the next up backend in cyclic order. The returned sequence is the cyclic sequence of the $u$ up indices, and the counting argument of Claim 2 with $u$ in place of $n$ applies. $\blacksquare$
