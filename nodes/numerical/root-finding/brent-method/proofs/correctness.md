---
title: Correctness, termination and the k^2 bound of Brent's method
proves: [correctness, termination, complexity]
status: full
---

Let $f$ be continuous on $[a_0, b_0]$ with $f(a_0) f(b_0) < 0$, let $w = |b_0 - a_0|$, and let $t = 4u|b| + \delta/2$ be the floor of line L5 (in exact arithmetic take $u = 0$). Write $W = |c - b|$ for the width of the bracket, and $m = (c - b)/2$.

**Theorem 1 (invariant).** At each test of line L5: $b$ and $c$ lie in $[a_0, b_0]$, $f(b)$ and $f(c)$ are nonzero with opposite signs, and $|f(b)| \le |f(c)|$. So a root $x^*$ lies strictly between $b$ and $c$, and a return at L5 with $f(b) \ne 0$ gives $|b - x^*| < W \le 2t = \delta + 8u|b|$.

*Proof.* At the first pass, $c = a_0$ and $b = b_0$ have values of opposite signs, and L4 swaps if needed. Suppose the claims hold at L5 and the pass does not return, so $|m| > t$. We show that the new $b$ lies strictly between the old $b$ and $c$. If L9 accepts $d = p/q$, then $0 \le 2p < 3mq - |tq|$, so $mq > 0$: $q$ has the sign of $m$, $d$ has the sign of $m$ or is 0, and $|d| < \frac32|m| - \frac t2 < \frac32 |m|$, that is less than $\frac34 W$. If $|d| > t$, the new point $b + d$ is strictly between $b$ and $c$. If $|d| \le t$, or after a bisection, the new point is $b + t\operatorname{sign}(m)$ or $b + m$, also strictly between $b$ and $c$ since $t < |m|$. So the new $b$ is in $[a_0, b_0]$. If $f$ is zero there, L5 of the next pass returns a root. Otherwise L11 makes the old $b$ the point $a$, and L3 of the next pass sets $c \leftarrow a$ when the new $b$ has the sign of $c$; the old $b$ had the other sign. Either way $f(b)$ and $f(c)$ have opposite signs, and L4 restores $|f(b)| \le |f(c)|$ by a swap that keeps the pair. The intermediate value theorem gives the root, and $W = 2|m| \le 2t$ at the return. $\square$

**Lemma 2 (the width falls).** If a pass does not return, the new width satisfies $W' \le W - t$. After a bisection, $W' = W/2$.

*Proof.* Let $b'$ be the new point, strictly between $b$ and $c$, with $|b' - b| \ge t$ (L11). If the contrapoint stays, $W' = |c - b'| = W - |b' - b| \le W - t$. If L3 sets the contrapoint to the old $b$, then $W' = |b' - b|$, which is less than $\frac34 W - \frac t2$ for an accepted step, equals $t$ for a minimum step, and equals $W/2$ for a bisection; since $W > 2t$, each of these is at most $W - t$. After a bisection $b' = b + m$ is the midpoint, so $W' = W/2$ in both cases. The swap at L4 does not change $W$. $\square$

**Theorem 3 (termination).** For $\delta > 0$, BRENT returns within $\lceil 2w/\delta \rceil$ passes. For any $\delta \ge 0$ it ends within $k_{\max}$ passes.

*Proof.* As for [Dekker's method](/dekker-method/): $t \ge \delta/2$, so by Lemma 2 after $j$ passes $0 < W \le w - j\delta/2$. $\square$

**Theorem 4 (the $k^2$ bound).** Let $\delta > 0$ and $k = \lceil \log_2(w/\delta) \rceil$. BRENT returns within $2(k + 2)^2$ passes, that is with at most $2(k + 2)^2 + 2$ evaluations.

*Proof.* Call a pass a bisection if it ends in L9's else branch or L10, and an interpolation pass if L9 accepts. Line L1 sets $d = e = b - a$, of size $w$, and a bisection sets $d = e = m$, of size at most $w$.

*Bisections.* By Lemma 2 the width never grows, and a bisection halves it. After $j$ bisections, $W \le w 2^{-j}$. A pass that does not return has $W > 2t \ge \delta$, so $j < \log_2(w/\delta) \le k$: there are at most $k$ bisections.

*Runs of interpolation passes.* A run is a maximal sequence of interpolation passes; it starts at the beginning or after a bisection, when $|d|, |e| \le w$. We claim that after $i$ passes of a run, at the next test of L6, $|d| \le w 2^{-\lceil i/2 \rceil}$ and $|e| \le w 2^{-\lfloor i/2 \rfloor}$. This holds for $i = 0$. An accepted step has $2|p| < |eq|$, so the new $|d|$ is less than $|e|/2 \le w 2^{-\lfloor i/2 \rfloor - 1} = w 2^{-\lceil (i+1)/2 \rceil}$, and the new $|e|$ is the old $|d|$, at most $w 2^{-\lceil i/2 \rceil} = w 2^{-\lfloor (i+1)/2 \rfloor}$. A reset at L3 sets $d = e = b - a$, the move just made. If that move was a step $d$ with $|d| > t$, the reset sets both to the stored $|d|$ and the claim still holds. If it was a minimum step of size $t$, the reset makes the old $b$ the contrapoint, so $W = t \le 2t$, and L5 returns at once. This proves the claim. An interpolation pass needs $|e| \ge t \ge \delta/2$ at L6, so $w 2^{-\lfloor i/2 \rfloor} \ge \delta/2$, which gives $\lfloor i/2 \rfloor \le k + 1$ and $i \le 2k + 3$. So a run has at most $2k + 4$ passes; after it, L6 fails or L9 rejects, and both are bisections.

*Count.* There are at most $k + 1$ runs (one before each bisection and one after the last), each with at most $2k + 4$ passes, and at most $k$ bisections: in all at most $(k + 1)(2k + 4) + k \le 2(k + 2)^2$ passes. Each pass costs one evaluation, and the start costs two. $\square$

The constant in Theorem 4 is not sharp; Brent (1973, Chapter 4) counts more carefully and obtains a bound of the same order $k^2$. The bound is far above what happens on smooth functions, where the method needs about $\log\log(1/\delta)$ passes once it is close to a simple root; that local behavior is the order of the [secant method](/secant-method/) and of [inverse quadratic interpolation](/inverse-quadratic-interpolation/), proved on their pages, and it is observed in the example. $\blacksquare$
