---
title: The O(M) form of delay-multiply-and-sum equals the pair sum, is bounded by the channel energy, and rectifies the signal
proves: [correctness]
status: full
---

We prove five facts about the combiner on the main page (lines L1 to L4). The input is a real vector $s = (s_1, \ldots, s_M)$ of delayed RF samples at one pixel. Let $r_i = \operatorname{sign}(s_i) \sqrt{|s_i|}$ (line L1), $R = \sum_i r_i$ (line L2) and $E = \sum_i |s_i|$ (line L3). The definition of DMAS is

$$y(s) = \sum_{1 \le i < j \le M} \operatorname{sign}(s_i s_j) \sqrt{|s_i s_j|}.$$

**Theorem 1 (the O(M) form).** $y(s) = (R^2 - E)/2$, which is line L4.

*Proof.* For every pair, $\operatorname{sign}(s_i s_j) = \operatorname{sign}(s_i) \operatorname{sign}(s_j)$ and $\sqrt{|s_i s_j|} = \sqrt{|s_i|} \sqrt{|s_j|}$, so each term is $r_i r_j$. This also holds when $s_i = 0$ or $s_j = 0$, because both sides are then $0$. Expand the square: $R^2 = \sum_i r_i^2 + 2 \sum_{i < j} r_i r_j$, and $r_i^2 = |s_i|$, so $\sum_i r_i^2 = E$. Solve for the pair sum. $\square$

The test compares the two forms on 300 random vectors with some zero entries.

**Theorem 2 (bounds).** $-E/2 \le y(s) \le \frac{M - 1}{2} E$. The lower bound holds with equality if and only if $R = 0$. The upper bound holds with equality if and only if all $r_i$ are equal, that is, all $s_i$ are equal.

*Proof.* $R^2 \ge 0$ gives the lower bound, with equality exactly when $R = 0$. By the Cauchy-Schwarz inequality, $R^2 = (\sum_i 1 \cdot r_i)^2 \le M \sum_i r_i^2 = M E$, with equality if and only if $r$ is a multiple of $(1, \ldots, 1)$. Then $y \le (M E - E)/2$. The map $v \mapsto \operatorname{sign}(v)\sqrt{|v|}$ is one-to-one, so equal $r_i$ means equal $s_i$. $\square$

So, for a fixed channel energy $E$, DMAS is largest when all delayed channels agree exactly in value and sign, and for $M$ equal samples $v$ it returns $\frac{M(M-1)}{2} |v|$. The test checks this value for $v = \pm 2.25$ and $v = 0$. For the same equal samples, delay-and-sum gives $M v$, which grows like $M$ and keeps the sign. DMAS grows like $M^2/2$ for agreeing channels, and it can be negative (down to $-E/2$) when the signed roots cancel, which happens at a pixel where the channels disagree in sign.

**Theorem 3 (homogeneity).** For every real $a$, $y(a s) = |a|\, y(s)$.

*Proof.* $\operatorname{sign}(a s_i) \sqrt{|a s_i|} = \operatorname{sign}(a) \sqrt{|a|}\, r_i$. Each product $r_i r_j$ is multiplied by $\operatorname{sign}(a)^2 |a| = |a|$. $\square$

So the output keeps the dimension of the input (the square root undoes the product), which is the purpose of the signed square root, but it does not keep the sign: $y(-s) = y(s)$.

**Theorem 4 (rectification).** Let all channels carry the same delayed signal, $s_i(t) = A(t) \cos(2\pi f_0 t + \varphi)$ for all $i$. Then $y(s(t)) = \frac{M(M-1)}{2} |A(t)|\, |\cos(2\pi f_0 t + \varphi)|$. For a constant $A$ this is periodic with period $1/(2 f_0)$, so its spectrum lies at $0$ and at the multiples of $2 f_0$, and has nothing at $f_0$.

*Proof.* Theorem 2 with equal entries gives the first formula. The function $|\cos|$ has period $\pi$, so $t \mapsto |\cos(2\pi f_0 t + \varphi)|$ has period $1/(2 f_0)$, and a periodic function has a Fourier series on the multiples of its base frequency. $\square$

This is why the filtered DMAS of Matrone et al. (2015) applies a band-pass filter around $2 f_0$ to the output before envelope detection: the DC part is removed and the second harmonic band is kept. For channels that differ, the output is no longer a pure rectified signal; the statement about the band at $2 f_0$ is then a heuristic for narrow-band data, not a theorem.

**Theorem 5 (cost).** Lines L1 to L4 cost $O(M)$ per pixel, against $O(M^2)$ for the pair sum. An $n \times n$ image costs $O(M n^2)$, the same order as delay-and-sum.

*Proof.* Lines L1 and L3 touch each entry once, line L2 is one sum and line L4 is $O(1)$. $\square$
