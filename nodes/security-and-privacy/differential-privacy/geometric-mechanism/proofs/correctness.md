---
title: The geometric mechanism samples two-sided geometric noise and is ln(1/alpha)-DP
proves: [correctness, termination]
status: full
---

Fix $\alpha = a/q \in (0, 1)$, a neighbor relation $\sim$, and an integer query $f$ with $|f(x) - f(x')| \le 1$ for all $x \sim x'$. Write $c = (1 - \alpha)/(1 + \alpha)$.

**Lemma 1 (one loop).** The value $g_1$ after line L3 has $\Pr[g_1 = j] = (1 - \alpha)\alpha^j$ for $j \ge 0$, and the loop ends with probability 1. The same holds for $g_2$ after line L5, and $g_1$ and $g_2$ are independent.

*Proof.* Each coin is heads with probability exactly $a/q = \alpha$, because it compares a uniform integer of $\{0, \ldots, q-1\}$ with $a$, and the coins are independent. The loop of line L3 ends with $g_1 = j$ exactly when the first $j$ coins are heads and coin $j + 1$ is a tail. This has probability $\alpha^j(1 - \alpha)$. These probabilities sum to $(1-\alpha) \sum_{j \ge 0} \alpha^j = 1$, so the loop ends with probability 1. Line L5 uses fresh coins, so $g_2$ has the same law and is independent of $g_1$. $\square$

**Lemma 2 (the noise).** $Z = g_1 - g_2$ has $\Pr[Z = d] = c\,\alpha^{|d|}$ for every integer $d$.

*Proof.* Let $d \ge 0$. By Lemma 1 and independence,

$$\Pr[Z = d] = \sum_{j \ge 0} \Pr[g_2 = j] \Pr[g_1 = j + d] = (1-\alpha)^2 \alpha^d \sum_{j \ge 0} \alpha^{2j} = \frac{(1-\alpha)^2 \alpha^d}{1 - \alpha^2} = c\,\alpha^d.$$

For $d < 0$, swap the roles of $g_1$ and $g_2$; the two have the same law, so $\Pr[Z = d] = \Pr[Z = -d] = c\,\alpha^{|d|}$. $\square$

**Theorem 1 (privacy without the clamp).** Let $M(x) = f(x) + Z$ be the output of line L6. For all $x \sim x'$ and every set $S \subseteq \mathbb Z$, $\Pr[M(x) \in S] \le \alpha^{-1} \Pr[M(x') \in S]$.

*Proof.* By Lemma 2, $\Pr[M(x) = y] = c\,\alpha^{|y - f(x)|}$ for every integer $y$. Let $u = f(x)$ and $u' = f(x')$, with $|u - u'| \le 1$. By the triangle inequality, $|y - u'| \le |y - u| + |u - u'| \le |y - u| + 1$. So

$$\frac{\Pr[M(x) = y]}{\Pr[M(x') = y]} = \alpha^{|y - u| - |y - u'|} \le \alpha^{-1},$$

where the inequality uses $\alpha < 1$ and $|y - u| - |y - u'| \ge -1$. Both probabilities are positive. Sum $\Pr[M(x) = y] \le \alpha^{-1} \Pr[M(x') = y]$ over $y \in S$. The relation is symmetric, so the same bound holds with $x$ and $x'$ swapped. $\square$

**Theorem 2 (privacy with the clamp).** The output of line L9 is $\ln(1/\alpha)$-DP for fixed bounds $lo \le hi$ that do not depend on the data.

*Proof.* Lines L7 and L8 compute $h(z) = \min(\max(z, lo), hi)$, a fixed function of $z$ alone (with $lo = -\infty$ or $hi = +\infty$ when a bound is not given). For a set $T$ of outputs, $\Pr[h(M(x)) \in T] = \Pr[M(x) \in h^{-1}(T)]$. Theorem 1 with $S = h^{-1}(T)$ gives $\Pr[h(M(x)) \in T] \le \alpha^{-1} \Pr[M(x') \in h^{-1}(T)] = \alpha^{-1} \Pr[h(M(x')) \in T]$. $\square$

**Lemma 3 (the truncated pmf).** If $lo < hi$ and $lo \le v = f(x) \le hi$, the output of line L9 has $\Pr[lo] = \alpha^{v - lo}/(1 + \alpha)$, $\Pr[hi] = \alpha^{hi - v}/(1 + \alpha)$, and $\Pr[y] = c\,\alpha^{|y - v|}$ for $lo < y < hi$.

*Proof.* For $lo < y < hi$, $h(z) = y$ only for $z = y$, so Lemma 2 gives the value. The end point $lo$ collects all $z \le lo$, that is $Z \le -(v - lo)$. For $t \ge 0$, $\Pr[Z \le -t] = c \sum_{d \ge t} \alpha^d = c\,\alpha^t/(1-\alpha) = \alpha^t/(1+\alpha)$. The same sum gives $\Pr[hi]$. $\square$

**Accuracy.** For an integer $t \ge 1$, $\Pr[|Z| \ge t] = 2 c\,\alpha^t/(1 - \alpha) = 2\alpha^t/(1+\alpha)$ by the sum in the proof of Lemma 3. If $lo \le v \le hi$, then $|h(z) - v| \le |z - v|$, so the clamp keeps the bound.

Lemma 1 shows termination with probability 1, Lemma 2 the law of the noise, and Theorems 1 and 2 the privacy, with and without the clamp. $\blacksquare$
