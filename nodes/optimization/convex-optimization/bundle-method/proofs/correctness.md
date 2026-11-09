---
title: The two-cut proximal bundle method stops with a certified point after O(1/eps^2) oracle calls
proves: [correctness, termination, iteration-bound]
status: full
---

The problem is $\min f(x)$ over $\mathbb{R}^n$. A cut is a pair $(h, g)$ that stands for the affine function $\ell(y) = h + g^\top(y - c)$, where $c$ is the current center, so $h = \ell(c)$. Let $\phi(h, g) = h - \tfrac t2\|g\|^2$. One iteration, with center $c$ and a bundle of one cut $a$ or two cuts $a, b$:

1. pick $\lambda \in [0, 1]$ that maximizes $\phi(\lambda a + (1 - \lambda)b)$ (take $\lambda = 1$ for one cut), and let $(h_a, g_a) = \lambda a + (1 - \lambda)b$, the aggregate cut;
2. let $y = c - tg_a$ and $v = f(c) - h_a + t\|g_a\|^2$; stop if $v \le \varepsilon$;
3. call the oracle at $y$. If $f(c) - f(y) \ge \kappa v$ (serious step), set $c \leftarrow y$ and the bundle to the single cut $(f(y), g_y)$. Otherwise (null step), keep $c$ and set the bundle to the aggregate $(h_a, g_a)$ and the new cut $(f(y) + g_y^\top(c - y), g_y)$.

We assume:

- (A1) $f: \mathbb{R}^n \to \mathbb{R}$ is convex and has a minimizer $x^*$, with $f^* = f(x^*)$;
- (A2) every subgradient returned by the oracle has $\|g\| \le G$, with $G > 0$ (for example, $f$ is $G$-Lipschitz);
- (A3) $t > 0$ and $0 < \kappa < 1$.

Write $e = f(c) - h_a$ for the error of the aggregate cut at the center, and $W = f(c) - \phi(h_a, g_a) = e + \tfrac t2\|g_a\|^2$.

**Lemma 1 (every cut is a minorant).** Every cut in the bundle and every aggregate cut satisfies $\ell(z) \le f(z)$ for all $z$. So $e \ge 0$, $v = e + t\|g_a\|^2$, and $\tfrac12 v \le W \le v$.

*Proof.* A new cut is $f(y) + g_y^\top(z - y)$, written with its value at $c$, so it is a minorant by the subgradient inequality. A cut kept after a null step is an aggregate, which is a convex combination of two minorants, so it is a minorant. The center does not change at a null step, so the stored values stay correct. At $z = c$ we get $h_a \le f(c)$, that is, $e \ge 0$. The formula for $v$ is its definition, and $\tfrac12 v \le W \le v$ follows from $e \ge 0$. $\square$

**Lemma 2 (the certificate).** At each iteration, for every $z$, $f(c) - f(z) \le e + \|g_a\|\,\|z - c\|$. If the method stops, $f(c) - f(z) \le \varepsilon + \sqrt{\varepsilon/t}\,\|z - c\|$ for every $z$.

*Proof.* By Lemma 1, $f(z) \ge h_a + g_a^\top(z - c) = f(c) - e + g_a^\top(z - c) \ge f(c) - e - \|g_a\|\,\|z - c\|$. At a stop, $e \le v \le \varepsilon$ and $t\|g_a\|^2 \le v \le \varepsilon$. $\square$

**Lemma 3 (null steps).** Suppose iteration $k$ is a null step with values $v_k$, $W_k$, and let $W_{k+1}$ belong to the next iteration, which has the same center. Then

$$W_{k+1} \le W_k - \min\Big(\frac{(1 - \kappa)v_k}{2},\ \frac{(1 - \kappa)^2v_k^2}{8tG^2}\Big).$$

*Proof.* Let $a = (h_a, g_a)$ be the aggregate of iteration $k$, and $b = (h_b, g_b)$ the new cut at $y = c - tg_a$. Iteration $k + 1$ maximizes $\phi$ over the segment from $a$ to $b$, so for each $s \in [0, 1]$, $f(c) - W_{k+1} \ge \phi(a + s(b - a))$. Expand:

$$\phi(a + s(b - a)) = \phi(a) + s\big(h_b - h_a - tg_a^\top(g_b - g_a)\big) - \tfrac t2 s^2\|g_b - g_a\|^2.$$

The new cut at $y$ has the value $h_b + g_b^\top(y - c) = h_b - tg_b^\top g_a = f(y)$. The aggregate at $y$ has the value $h_a - t\|g_a\|^2 = f(c) - v_k$. So the bracket equals $f(y) - (f(c) - v_k)$, and the null step condition $f(c) - f(y) < \kappa v_k$ makes it larger than $(1 - \kappa)v_k$. With $q = \|g_b - g_a\|^2 \le (2G)^2$, since $g_a$ is a convex combination of subgradients of norm at most $G$:

$$W_k - W_{k+1} \ge \max_{s \in [0, 1]}\Big(s(1 - \kappa)v_k - \tfrac t2 s^2 q\Big).$$

If $tq \le (1 - \kappa)v_k$, take $s = 1$, which gives at least $(1 - \kappa)v_k/2$. Otherwise take $s = (1 - \kappa)v_k/(tq)$, which gives $(1 - \kappa)^2v_k^2/(2tq) \ge (1 - \kappa)^2v_k^2/(8tG^2)$. $\square$

**Lemma 4 (a run of null steps is short).** Let $\alpha = (1 - \kappa)^2/(8tG^2)$. Consider the iterations with one fixed center, starting just after a serious step or at the start. While these iterations are null steps, $1/W$ grows by at least $\alpha$ per step. So at most $\lceil 2/(\alpha\varepsilon)\rceil = \lceil 16tG^2/((1 - \kappa)^2\varepsilon)\rceil$ null steps occur in a row before a serious step or a stop.

*Proof.* The first iteration with this center has one cut with $e = 0$, so $W = \tfrac t2\|g\|^2 \le \tfrac t2 G^2$. By Lemma 3 the values $W$ do not increase along the null steps, so $W_k \le \tfrac t2 G^2 \le 4tG^2/(1 - \kappa)$ for each of them. For such $W_k$, using $v_k \ge W_k$ from Lemma 1:

$$\frac{(1 - \kappa)v_k}{2} \ge \frac{(1 - \kappa)W_k}{2} \ge \alpha W_k^2 \quad\text{and}\quad \frac{(1 - \kappa)^2v_k^2}{8tG^2} \ge \alpha W_k^2.$$

So $W_{k+1} \le W_k - \alpha W_k^2$, and if $W_{k+1} > 0$, then $\frac{1}{W_{k+1}} - \frac{1}{W_k} = \frac{W_k - W_{k+1}}{W_kW_{k+1}} \ge \frac{\alpha W_k^2}{W_k^2} = \alpha$. After $j$ null steps in a row, the next iteration has $W < 1/(\alpha j)$ or $W = 0$, so $v \le 2W < 2/(\alpha j)$. When $j \ge 2/(\alpha\varepsilon)$, this gives $v < \varepsilon$, and the method stops. $\square$

**Theorem (termination and iteration bound).** Let $\varepsilon > 0$. Each serious step lowers $f(c)$ by more than $\kappa\varepsilon$, so there are at most $S = \lfloor (f(x_0) - f^*)/(\kappa\varepsilon)\rfloor$ serious steps. With $J = \lceil 16tG^2/((1 - \kappa)^2\varepsilon)\rceil$, the method stops after at most $(S + 1)(J + 1)$ iterations, each with at most one oracle call besides the first. At the stop, Lemma 2 gives $f(c) - f^* \le \varepsilon + \sqrt{\varepsilon/t}\,\|x^* - c\|$, and $f(c) \le f(x_0)$.

*Proof.* A serious step happens only when $v > \varepsilon$ (otherwise the method stopped) and $f(c) - f(y) \ge \kappa v > \kappa\varepsilon$. The center values stay at least $f^*$, which bounds the number of serious steps by $S$. Between two serious steps, and after the last one, Lemma 4 allows at most $J$ null steps, followed by one iteration that is a serious step or a stop. $\blacksquare$
