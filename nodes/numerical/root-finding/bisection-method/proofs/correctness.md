---
title: Bisection returns a point within the tolerance of a root, after a known number of steps
proves: [correctness, termination, evaluations.worst]
status: full
---

We work in exact real arithmetic. Let $f$ be continuous on $[a_0, b_0]$ with $a_0 < b_0$ and $f(a_0) f(b_0) < 0$, and let $\delta > 0$. Write $a_k, b_k$ for the values of $a, b$ after $k$ passes of the loop of lines L4 to L11, and $w = b_0 - a_0$. In exact arithmetic the midpoint $c = a + (b - a)/2$ lies strictly between $a$ and $b$, so line L6 never returns.

**Invariant (B).** After $k$ passes that did not return: $a_k < b_k$; $fa = f(a_k)$ and $fb = f(b_k)$; both are nonzero and have opposite signs; and $b_k - a_k = w / 2^k$.

*Initialization.* For $k = 0$, line L1 sets $fa = f(a_0)$ and $fb = f(b_0)$. Line L2 returns if one is zero, and line L3 returns if they have the same sign. Otherwise (B) holds with $b_0 - a_0 = w$.

*Maintenance.* Assume (B) after $k$ passes and that pass $k+1$ does not return. Line L5 sets $c = (a_k + b_k)/2$, so $a_k < c < b_k$ and $c - a_k = b_k - c = (b_k - a_k)/2 = w/2^{k+1}$. Line L8 did not return, so $f(c) \ne 0$. The signs of $fa$ and $fb$ differ, and $f(c)$ has one of the two signs. If $f(c)$ has the sign of $fa$, line L9 sets $a_{k+1} = c$, $fa = f(c)$, and $b_{k+1} = b_k$. Then $f(a_{k+1})$ has the sign of $f(a_k)$, which is opposite to the sign of $f(b_{k+1})$. Otherwise $f(c)$ has the sign of $fb$, and line L10 sets $b_{k+1} = c$, with the symmetric argument. In both cases the new width is $w/2^{k+1}$, so (B) holds after $k + 1$ passes.

**Lemma (a root in the bracket).** If (B) holds, then $[a_k, b_k]$ holds a root of $f$.

*Proof.* $f$ is continuous on $[a_k, b_k] \subseteq [a_0, b_0]$, and $f(a_k)$ and $f(b_k)$ have opposite signs. By the intermediate value theorem there is $x^* \in (a_k, b_k)$ with $f(x^*) = 0$. $\square$

**Theorem.** Let $N = \max(0, \lceil \log_2(w/(2\delta)) \rceil)$. If $k_{\max} \ge N$, then BISECT returns a point $\hat x$ such that some root $x^*$ of $f$ in $[a_0, b_0]$ has $|\hat x - x^*| \le \delta$. It makes at most $N$ passes and at most $N + 2$ evaluations of $f$. If no end and no midpoint is a root and $w > 2\delta$, it makes exactly $N$ passes and $N + 2$ evaluations.

*Proof.* There are four ways to return.

1. Line L2 returns $a_0$ or $b_0$, which is a root, so the error is 0.
2. Line L8 returns a midpoint $c$ with $f(c) = 0$, a root in $[a_0, b_0]$.
3. Line L11 returns the midpoint $m$ of $[a_k, b_k]$ when $b_k - a_k \le 2\delta$. By the lemma there is a root $x^* \in [a_k, b_k]$, and each point of this interval is within $(b_k - a_k)/2 \le \delta$ of $m$.
4. Line L12 is reached only if $k_{\max}$ passes end without a return.

We show that case 4 does not happen when $k_{\max} \ge N$. If $w \le 2\delta$ we have $N = 0$. Then the first pass either returns at line L8, or reaches line L11 with width $w/2 \le 2\delta$ and returns. If $w > 2\delta$, then $N \ge 1$ is the least integer with $w/2^N \le 2\delta$. By (B) the width after $k$ passes is $w/2^k$, which is greater than $2\delta$ for $k < N$ and at most $2\delta$ for $k = N$. So the test of line L11 fails in passes 1 to $N - 1$ and holds in pass $N$, unless line L8 returned earlier. This proves the bound of $N$ passes. Each pass evaluates $f$ once (line L7), and line L1 evaluates it twice, which gives $N + 2$. When no end and no midpoint is a root, no early return happens, so the counts are exact. $\blacksquare$

**The error of each midpoint.** After $k$ passes the midpoint $m_k$ of $[a_k, b_k]$ satisfies $|m_k - x^*| \le w/2^{k+1}$ for a root $x^*$ in the bracket, by (B) and the lemma. This bound halves at each pass. The error $|m_k - x^*|$ itself need not decrease: it can grow from one step to the next when $x^*$ is close to $m_k$ and far from $m_{k+1}$.

**Floating point.** In floating point, the computed midpoint $c$ satisfies $a \le c \le b$ when $a + (b - a)/2$ is computed with $b - a$ finite and rounding to nearest, because rounding is monotone. Line L6 returns when $c$ equals an end, which happens when $a$ and $b$ are adjacent numbers. A pass that does not return at line L6 replaces one end by a number strictly between $a$ and $b$, so the number of floating-point numbers in $[a, b]$ falls by at least one. That number is finite, so the loop ends after finitely many passes for every $\delta \ge 0$, even when the test of line L11 never holds. The invariant (B) then holds for the computed values $\hat f$ in place of $f$, except for the exact width. If $|\hat f - f| \le \varepsilon_f$ on the bracket and both $|f(a_k)|$ and $|f(b_k)|$ exceed $\varepsilon_f$, the computed signs are the true signs, and the lemma gives a true root in $[a_k, b_k]$. Otherwise an end of the final bracket lies in the set $\{x : |f(x)| \le \varepsilon_f\}$.
