---
title: Correctness and termination of Dekker's method
proves: [correctness, termination]
status: full
---

We work in exact arithmetic for the decisions, with $t = 4u|b| + \delta/2 > 0$ as in line L4; in exact arithmetic take $u = 0$ and $\delta > 0$. Let $f$ be continuous on $[a_0, b_0]$ with $f(a_0) f(b_0) < 0$, and write $W = |a - b|$ for the width of the current bracket.

**Theorem 1 (invariant).** At each test of line L4: $a$ and $b$ lie in $[a_0, b_0]$, $f(a)$ and $f(b)$ are nonzero with opposite signs, and $|f(b)| \le |f(a)|$. So a root $x^*$ lies strictly between $a$ and $b$, and a return at L4 gives $|b - x^*| < W \le 2t = \delta + 8u|b|$.

*Proof.* At the first pass the first two claims are the hypothesis, and line L3 gives the third by a swap, which keeps the first two. Suppose the claims hold at the test of L4 and the method does not return. Lines L5 to L7 produce $s$ strictly between $b$ and $m$: L6 replaces any $s$ outside the open interval between $b$ and $m$ by $m$, which is also strictly inside $(a, b)$; if $|s - b| < t$, L7 sets $s = b + t\,\operatorname{sign}(m - b)$, which lies strictly between $b$ and $m$ because $|m - b| > t$. So $s$ lies strictly between $a$ and $b$, hence in $[a_0, b_0]$. If $f(s) = 0$ the method returns a root. Otherwise, at L9, if $f(s)$ has the sign of $f(a)$, then the old $b$ (now $p$) has the opposite sign, and the new contrapoint is $p$; if not, $a$ stays. In both cases $f(a)$ and $f(b)$ have opposite signs, and line L3 of the next pass restores $|f(b)| \le |f(a)|$. The intermediate value theorem gives the root. Since $m$ is the midpoint, $W = 2|m - b|$, so the test $|m - b| \le t$ means $W \le 2t$. $\square$

**Lemma 2 (progress).** If a pass does not return, the width after it satisfies $W' \le W - t$.

*Proof.* The new point $s$ lies between $b$ and $m$ with $|s - b| \ge t$ (by L7, or because $s = m$ and $|m - b| > t$). If the contrapoint stays, the new bracket is between $a$ and $s$, and since $s$ lies between $b$ and $a$, $W' = W - |s - b| \le W - t$. If the contrapoint becomes the old $b$, the new bracket is between the old $b$ and $s$, so $W' = |s - b| \le |m - b| = W/2$. Since the pass did not return, $W > 2t$, so $W/2 < W - t$. In both cases $W' \le W - t$. A swap at L3 does not change $W$. $\square$

**Theorem 3 (termination).** Let $\delta > 0$ and $w = |b_0 - a_0|$. DEKKER returns within $\lceil 2w/\delta \rceil$ passes, so with at most $\lceil 2w/\delta \rceil + 2$ evaluations of $f$. For any $\delta \ge 0$ it ends within $k_{\max}$ passes.

*Proof.* $t \ge \delta/2$ at every pass. By Lemma 2, after $j$ passes that do not return, $0 < W \le w - j\delta/2$, so $j < 2w/\delta$. Each pass costs one evaluation, the start two. The loop has $k_{\max}$ passes. $\square$

In binary64 with $\delta = 0$, $t = 4u|b|$ is at least one unit in the last place of $b$ when $b \ne 0$, so each pass moves $b$ to a different floating point number and the width shrinks; the bound of Theorem 3 does not apply, and $k_{\max}$ is the guarantee. Near $b = 0$ with $\delta = 0$ the floor $t$ can underflow; a positive $\delta$ avoids this.

**Local behavior.** Theorem 3 is the only bound for general continuous $f$, and it is linear in $w/\delta$. The page shows functions ($x^9$ and $(x - 0.3)^{19}$) that need hundreds of steps. Near a simple root of a $C^2$ function the accepted steps are secant steps, which converge with order $(1 + \sqrt5)/2$; this is the classical local theory of the [secant method](/secant-method/), and the observed log ratios in the example are 1.61 to 1.66. $\blacksquare$
