---
title: Correctness of Fermat's factorization method
proves: [correctness, termination]
status: full
---

Let $N \ge 1$ be odd, and let $s = \lceil \sqrt N \rceil$.

**Lemma 1 (pairs and factorizations).** The map $(u, v) \mapsto (x, y) = \left(\frac{u + v}{2}, \frac{v - u}{2}\right)$ is a bijection from the pairs of positive integers $u \le v$ with $uv = N$ onto the pairs of integers $x > 0$, $y \ge 0$ with $x^2 - y^2 = N$. Its inverse is $(x, y) \mapsto (x - y, x + y)$.

*Proof.* Since $N$ is odd, $u$ and $v$ are odd, so $u + v$ and $v - u$ are even and $x$, $y$ are integers, with $x > 0$ and $y \ge 0$ because $v \ge u \ge 1$. Then $x^2 - y^2 = (x - y)(x + y) = uv = N$. Conversely, let $x > 0$, $y \ge 0$ and $x^2 - y^2 = N$. Put $u = x - y$ and $v = x + y$. Then $v > 0$, $uv = N > 0$, so $u > 0$, and $u \le v$ because $y \ge 0$. The two maps are inverse to each other by direct substitution. $\square$

**Lemma 2 (order).** If $uv = N$ with $1 \le u \le v$, then $x = (u + v)/2 \ge s$. If $u < u'$ are two divisors of $N$ that are at most $\sqrt N$, with cofactors $v = N/u$ and $v' = N/u'$, then $(u' + v')/2 < (u + v)/2$.

*Proof.* By the inequality of the arithmetic and geometric means, $(u + v)/2 \ge \sqrt{uv} = \sqrt N$, and since $(u + v)/2$ is an integer, it is at least $s$. For the second claim, $(u + v) - (u' + v') = (u - u') + N\left(\frac1u - \frac1{u'}\right) = (u' - u)\left(\frac{N}{uu'} - 1\right)$. Here $u' - u > 0$, and $uu' < u'^2 \le N$, so $N/(uu') > 1$. The difference is positive. $\square$

**Invariant.** Each time line L3 is reached, $r = x^2 - N$, $x \ge s$, and no integer $x'$ with $s \le x' < x$ has $x'^2 - N$ equal to a square.

*Initialization.* Lines L1 and L2 set $x = s$ and $r = s^2 - N$. There is no $x'$ with $s \le x' < s$.

*Maintenance.* Line L4 runs only when $r = x^2 - N$ is not a square. It sets $r$ to $x^2 - N + 2x + 1 = (x + 1)^2 - N$ and $x$ to $x + 1$. The old $x$ is now one of the values below the new $x$, and it failed, so the third part holds again.

**Termination.** By Lemma 1 with $u = 1$, $v = N$, the value $x^* = (N + 1)/2$ gives $x^{*2} - N = ((N - 1)/2)^2$, a square, and $x^* \ge s$ by Lemma 2. The value $x$ grows by $1$ in each pass of the loop, so the loop reaches a square at some $x \le x^*$ and stops after at most $x^* - s + 1$ tests.

**Correctness.** When the loop stops, $r = x^2 - N$ is a square, and line L5 sets $y = \sqrt r \ge 0$, so $x^2 - y^2 = N$ with $x \ge s > 0$. By Lemma 1, line L6 returns a pair $(a, b) = (x - y, x + y)$ of positive integers with $a \le b$ and $ab = N$. So $a \le \sqrt N$.

It remains to show that $a$ is the largest divisor of $N$ at most $\sqrt N$. Suppose a divisor $u'$ of $N$ has $a < u' \le \sqrt N$, and let $x' = (u' + N/u')/2$. By Lemma 2, $s \le x' < (a + b)/2 = x$, and by Lemma 1, $x'^2 - N$ is a square. This contradicts the invariant. So $a$ is the largest such divisor; in particular $a = 1$ if and only if $N$ has no divisor in $[2, \sqrt N]$, that is, if and only if $N = 1$ or $N$ is prime.

**The number of steps.** The loop stops at $x = (a + b)/2$, so line L4 runs exactly $(a + b)/2 - s$ times. $\blacksquare$
