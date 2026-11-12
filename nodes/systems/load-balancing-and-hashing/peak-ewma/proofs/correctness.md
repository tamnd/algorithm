---
title: The peak EWMA cost stays between the time-decayed largest sample and the largest sample, and its decay does not depend on how often it is read
proves: [correctness, termination]
status: full
---

We use the pseudocode OBSERVE, LOAD, PICK and DONE of the page, with a time constant $\tau > 0$. Fix one backend $j$ and write $c$ for $c[j]$ and $s$ for $s[j]$. At the start $c = 0$. We assume that the calls on this backend come with non-decreasing times $t$, as with a monotonic clock; then line L1 sets $\Delta = t - s$ and $s = t$. A call of LOAD runs OBSERVE with $x = 0$; we call it a *read*. A call of OBSERVE with a measured time $x \ge 0$, from line L13, is a *sample*, taken at time $t_i$ with value $x_i$.

**Claim 1 (pending counts).** Between calls, $p[j]$ is the number of requests sent to $j$ by PICK that have not ended. Line L11 adds 1 for each pick of $j$, line L12 subtracts 1 for each end, and nothing else changes $p[j]$.

**Claim 2 (one step).** Let a call at time $t$ with value $x \ge 0$ change $c$ to $c'$, and let $w = e^{-\Delta/\tau}$, so $0 < w \le 1$. Then $c' \ge x$, $c' \ge c\,w$ and $c' \le \max(c, x)$.

*Proof.* If $x > c$, line L3 sets $c' = x$. Then $c' \ge x$, $c' = x \le \max(c, x)$, and $c' = x > c \ge c\,w$ because $c \ge 0$ and $w \le 1$. Otherwise $x \le c$ and line L5 sets $c' = c\,w + x(1 - w)$, a weighted average of $c$ and $x$ with weights $w$ and $1 - w$ in $[0, 1]$. So $c' \le c = \max(c, x)$. Since $x \ge 0$, $c' \ge c\,w$. Since $c \ge x$, $c' \ge x\,w + x(1-w) = x$. $\square$

**Claim 3 (the bounds).** After any sequence of samples and reads, with $t$ the time of the last call,

$$\max_{i \,:\, t_i \le t} x_i\, e^{-(t - t_i)/\tau} \;\le\; c \;\le\; \max_{i \,:\, t_i \le t} x_i ,$$

where an empty maximum is 0.

*Proof.* Write $B(t)$ for the left side and $M$ for the right side. By induction on the number of calls. At the start no sample exists, and $c = B = M = 0$. Take a call at time $t \ge s$, with $\Delta = t - s$ and $w = e^{-\Delta/\tau}$. Each term $x_i e^{-(t - t_i)/\tau}$ of an earlier sample equals $x_i e^{-(s - t_i)/\tau} \cdot w$, so the earlier terms give $B(s)\,w$. A read adds no sample. A sample adds the term $x\, e^{0} = x$. So the new left side is $B(s)\,w$ for a read, and $\max(B(s)\,w, x)$ for a sample. A read is a call with $x = 0$, so in both cases the new left side is at most $\max(B(s)\,w, x)$. By Claim 2 and the induction hypothesis $c \ge B(s)$, the new value has $c' \ge c\,w \ge B(s)\,w$ and $c' \ge x$, so $c'$ is at least the new left side. For the right side, Claim 2 gives $c' \le \max(c, x)$, and $c \le M$ by the induction hypothesis. For a read $x = 0 \le M$, and for a sample $x$ joins the maximum, so $c'$ is at most the new right side. $\square$

**Claim 4 (decay does not depend on reads).** Suppose that between the times $t_a$ and $t_b$ only reads happen on the backend, and let $c_a$ be the cost after the call at $t_a$. Then after the read at $t_b$, $c = c_a\, e^{-(t_b - t_a)/\tau}$, whatever the number and the times of the reads in between.

*Proof.* A read has $x = 0 \le c$, so line L5 runs with $x = 0$ and gives $c' = c\,e^{-\Delta/\tau}$. For reads at times $t_a < r_1 < \cdots < r_m = t_b$, the factors multiply to $e^{-((r_1 - t_a) + (r_2 - r_1) + \cdots + (r_m - r_{m-1}))/\tau} = e^{-(t_b - t_a)/\tau}$, because the sum telescopes. With $m = 0$ reads the claim is empty. $\square$

So a peak $x$ at time $t_0$ that is followed only by reads falls to half at $t_0 + \tau \ln 2$. A sample that is smaller than the current cost does depend on the reads before it, because its weight $1 - w$ uses only the time since the last call.

**Claim 5 (the choice).** For $n \ge 2$, PICK draws an ordered pair $(i, k)$ of different backends, each pair with probability $1/(n(n-1))$, and returns $k$ if LOAD$(k) <$ LOAD$(i)$, else $i$. So it returns the one of the two with the smaller load, and $i$ on a tie.

*Proof.* Line L9 draws $i$ uniformly from $n$ backends and then $k$ uniformly from the $n - 1$ others. The comparison of line L10 replaces $i$ only on a strictly smaller load. $\square$

**Termination.** Each call runs a constant number of steps: OBSERVE has no loop, LOAD calls OBSERVE once, PICK calls LOAD twice and DONE calls OBSERVE once. $\blacksquare$

Claim 3 is the precise sense of "sensitive to peaks": one response of $x$ seconds keeps the cost at least $x\,e^{-\Delta/\tau}$ for every $\Delta$ after it, whatever smaller samples follow. The cost never exceeds the slowest response seen. Neither claim says anything about response times; peak EWMA is a heuristic.
