---
title: Least connections keeps exact connection counts and sends each new connection to a backend with the fewest
proves: [correctness, termination]
status: full
---

We use the pseudocode LC-PICK and LC-DONE of the page. There are $n \ge 0$ backends with counters $a[0..n-1]$, all 0 at the start, and flags $up[0..n-1]$. A *connection* to $j$ is opened when LC-PICK returns $j$ and closed when the caller runs LC-DONE$(j)$ for it. The caller closes only connections that it opened, each one once.

**Claim 1 (the counters).** At every moment between calls, $a[j]$ equals the number of connections to $j$ that are open, that is, opened and not yet closed.

*Proof.* By induction on the number of calls. At the start no connection exists and $a[j] = 0$. A call of LC-PICK that returns $j$ opens one connection to $j$ and line L4 adds 1 to $a[j]$ and to no other counter. A call that returns none opens nothing and changes nothing. A call of LC-DONE$(j)$ closes one open connection to $j$, and line L6 subtracts 1 from $a[j]$ only. So each call changes each side of the equation by the same amount. Because the caller closes only open connections, $a[j] \ge 1$ before line L6, and the counters never become negative. $\square$

**Claim 2 (the choice).** LC-PICK returns none if no backend is up. Otherwise it returns the smallest index $j^*$ among the up backends with the smallest counter: $up[j^*]$ holds, $a[j^*] \le a[j]$ for every up $j$, and $a[j^*] < a[j]$ for every up $j < j^*$.

*Proof.* We show the invariant at the test of line L2 for index $j$: if no backend among $0, \ldots, j-1$ is up, $best$ is none; otherwise $best$ is the smallest index among the up backends in $0, \ldots, j-1$ with the smallest counter among them. *Initialization:* for $j = 0$ the range is empty and line L1 set $best$ to none. *Maintenance:* if backend $j$ is down, line L3 does nothing and the range grows by a backend that does not count. If it is up and $best$ is none, $j$ is the only up backend so far, and line L3 sets $best = j$. If it is up and $a[j] < a[best]$, then $j$ has a strictly smaller counter than all earlier up backends, and line L3 sets $best = j$. If $a[j] \ge a[best]$, $best$ keeps the smallest counter, and on a tie the smaller index $best < j$ stays, as the invariant requires. *Termination:* the loop ends after $n$ passes with the range $0, \ldots, n-1$, and the invariant gives the claim. Line L4 then counts the new connection. $\square$

**Claim 3 (balance with no departures).** Suppose all backends stay up and no connection closes during a run of $k$ calls of LC-PICK, starting from counters $a_0[j]$. Let $M = \max_j a_0[j]$. If $k \ge \sum_j (M - a_0[j])$, then at the end $\max_j a[j] - \min_j a[j] \le 1$.

*Proof.* Let $D = \sum_j (M - a[j])$, which is $\ge 0$ while every counter is at most $M$. *Phase 1.* While $D > 0$, some counter is below $M$, so the minimum counter is below $M$. By Claim 2 the pick raises a counter with the minimum value, so that counter rises by 1 to a value $\le M$. Thus all counters stay $\le M$ and $D$ falls by exactly 1. After $D_0 = \sum_j (M - a_0[j])$ picks, $D = 0$ and all counters equal $M$. *Phase 2.* Suppose all counters lie in $\{c, c+1\}$ for some $c$, with at least one equal to $c$. The pick raises a counter equal to $c$ to $c + 1$, so afterwards all counters lie in $\{c, c+1\}$, or all equal $c + 1$, which is the same form with $c + 1$. By induction this holds after every later pick. Since $k \ge D_0$, the run ends in Phase 2, so the counters differ by at most 1. $\blacksquare$

Claim 1 is the property that the balancer needs from the caller: the counts are exact only if every closed connection is reported once. Claims 2 and 3 are deterministic and hold for any arrival order. The response-time results of the page (Winston, Weber) are about a queueing model and are cited, not proved here.
