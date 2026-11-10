---
title: The corrected sample and hold estimate is unbiased with variance at most (1 - p)/p^2
proves: [correctness]
status: full
---

Fix the sampling probability $p \in (0, 1]$ and write $q = 1 - p$. Fix an item $x$ with $f \ge 0$ units in the stream. Each unit of $x$ that arrives while $x$ is not held is sampled with probability $p$, independently (line L2). Once $x$ is held, every unit is counted (line L1).

**The law of the held count.** Let $J$ be the number of units of $x$ before the first sampled one. Then $\Pr[J = j] = q^j p$ for $0 \le j < f$, and $x$ is never held with probability $q^f$. If $x$ is held, its count is $H[x] = f - J$.

**Coupling.** Let $Y$ be a geometric variable with $\Pr[Y = j] = q^j p$ for all $j \ge 0$, and let the coins of the units of $x$ be the first $f$ trials of the sequence that defines $Y$. Then $x$ is held if and only if $Y < f$, and then $J = Y$. Define
$$ g = f - Y + \frac{q}{p}, \qquad \hat f_x = g \cdot 1_{Y < f} . $$
This $\hat f_x$ is the output of lines L3 and L4. The geometric law has $\mathbb{E}[Y] = q/p$ and $\mathrm{Var}[Y] = q/p^2$, so $\mathbb{E}[g] = f$ and $\mathrm{Var}[g] = q/p^2$.

**Lemma (memorylessness).** For each integer $f \ge 0$ with $q^f > 0$, the law of $Y - f$ given $Y \ge f$ is the law of $Y$.

*Proof.* $\Pr[Y - f = j \mid Y \ge f] = q^{f + j} p / q^f = q^j p$. $\square$

**Theorem.**

1. $\mathbb{E}[\hat f_x] = f$.
2. $\mathrm{Var}[\hat f_x] \le q/p^2 = (1 - p)/p^2$.
3. $\mathbb{E}[H[x] \cdot 1_{Y < f}] = f - \frac{q}{p}(1 - q^f)$, so the held count is low by less than $1/p$ on average.
4. $\Pr[x \text{ is not held}] = q^f \le e^{-pf}$.
5. The expected number of held items is at most $pm$, where $m$ is the total number of units.

*Proof.* If $q^f = 0$, then $p = 1$ and $f \ge 1$, every unit is sampled, $\hat f_x = f$, and all claims hold. Also if $f = 0$, then $\hat f_x = 0 = f$ always. So let $f \ge 1$ and $q^f > 0$.

(1) By the lemma, given $Y \ge f$, $g = q/p - (Y - f)$ has mean $q/p - q/p = 0$. So $\mathbb{E}[g \cdot 1_{Y \ge f}] = \Pr[Y \ge f] \cdot 0 = 0$, and
$$ \mathbb{E}[\hat f_x] = \mathbb{E}[g] - \mathbb{E}[g \cdot 1_{Y \ge f}] = f . $$

(2) $\mathbb{E}[\hat f_x^2] = \mathbb{E}[g^2 \cdot 1_{Y < f}] \le \mathbb{E}[g^2]$. The means of $\hat f_x$ and $g$ are both $f$, so
$$ \mathrm{Var}[\hat f_x] = \mathbb{E}[\hat f_x^2] - f^2 \le \mathbb{E}[g^2] - f^2 = \mathrm{Var}[g] = \frac{q}{p^2} . $$

(3) On $Y < f$, $H[x] = \hat f_x - q/p$. So $\mathbb{E}[H[x] \cdot 1_{Y < f}] = \mathbb{E}[\hat f_x] - \frac{q}{p} \Pr[Y < f] = f - \frac{q}{p}(1 - q^f)$, and $\frac{q}{p}(1 - q^f) < \frac{1}{p}$.

(4) $x$ is not held if and only if its $f$ coins all fail, with probability $q^f = (1 - p)^f \le e^{-pf}$.

(5) By (4) and Bernoulli's inequality, item $x$ is held with probability $1 - q^{f_x} \le p f_x$. By linearity of expectation, the expected number of held items is at most $\sum_x p f_x = pm$. $\blacksquare$

**Corollary (large flows).** Let $p = O/T$ for a threshold $T$ and an oversampling factor $O \le T$. A flow with $f_x \ge T$ is missed with probability at most $e^{-O}$, and its estimate has standard deviation below $1/p = T/O$, so relative to $T$ it is below $1/O$.
