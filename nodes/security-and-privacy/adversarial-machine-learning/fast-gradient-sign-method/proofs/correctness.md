---
title: FGSM stays in the allowed set and is the exact maximizer of a linearized loss
proves: [correctness]
status: full
---

We write $S = B_\infty(x, \epsilon) \cap [0,1]^d$ for the allowed set, with $x \in [0,1]^d$ and $\epsilon \ge 0$, and $g = \nabla_x L(\theta, x, y)$ for the gradient that line L1 computes. FGSM returns $x'$ with $x'_i = \operatorname{clip}_{[0,1]}(x_i + \epsilon \operatorname{sign}(g_i))$ (lines L2 to L4), where $\operatorname{sign}(0) = 0$.

**Lemma 1 (the set is a box).** $S = \prod_i [\ell_i, u_i]$ with $\ell_i = \max(x_i - \epsilon, 0)$ and $u_i = \min(x_i + \epsilon, 1)$, and $\ell_i \le x_i \le u_i$.

*Proof.* A point $v$ is in $S$ when $|v_i - x_i| \le \epsilon$ and $0 \le v_i \le 1$ for every $i$. These are two interval conditions on each coordinate, and their intersection is $[\ell_i, u_i]$. Because $0 \le x_i \le 1$ and $\epsilon \ge 0$, $x_i$ is in both intervals. $\square$

**Lemma 2 (feasibility).** $x' \in S$.

*Proof.* Take a coordinate $i$. If $g_i > 0$, line L3 gives $v = x_i + \epsilon \ge 0$, so line L4 gives $x'_i = \min(x_i + \epsilon, 1) = u_i$. If $g_i < 0$, then $v = x_i - \epsilon \le 1$ and $x'_i = \max(x_i - \epsilon, 0) = \ell_i$. If $g_i = 0$, then $x'_i = x_i$. In each case $x'_i \in [\ell_i, u_i]$, so $x' \in S$ by Lemma 1. $\square$

**Theorem 1 (exact for the linearized loss).** Let $\hat L(v) = L(\theta, x, y) + g^\top (v - x)$ be the first-order model of the loss at $x$. Then $x'$ maximizes $\hat L$ over $S$. If no coordinate is clipped (that is, $\epsilon \le x_i \le 1 - \epsilon$ wherever $g_i \ne 0$), the maximum gain is $\hat L(x') - \hat L(x) = \epsilon \lVert g \rVert_1$.

*Proof.* The gain $g^\top(v - x) = \sum_i g_i (v_i - x_i)$ is a sum of terms that each depend on one coordinate, and by Lemma 1 the coordinates of $v$ range over independent intervals. So the sum is largest when each term is largest. The term $g_i(v_i - x_i)$ is increasing in $v_i$ when $g_i > 0$, so its maximum is at $v_i = u_i$; it is decreasing when $g_i < 0$, so its maximum is at $v_i = \ell_i$; it is $0$ for every $v_i$ when $g_i = 0$. The proof of Lemma 2 shows that $x'_i$ takes exactly these values. Without clipping, $u_i - x_i = \epsilon$ and $\ell_i - x_i = -\epsilon$, so the gain is $\sum_i |g_i| \epsilon = \epsilon \lVert g \rVert_1$. $\square$

**Theorem 2 (exact for logistic regression).** Let the model be logistic regression with logit $z(v) = w^\top v + b$, label $y \in \{0, 1\}$, $s = 2y - 1$ and loss $L(v) = \ln(1 + e^{-s z(v)})$. Then $x'$ maximizes the true loss $L$ over $S$, not only its linearization.

*Proof.* The gradient is $g = (\sigma(z(x)) - y)\, w$. For $y = 1$ the factor $\sigma(z) - 1$ is negative, and for $y = 0$ the factor $\sigma(z)$ is positive, so $\operatorname{sign}(g_i) = -s \operatorname{sign}(w_i)$ for every $i$ (both are $0$ when $w_i = 0$). The function $t \mapsto \ln(1 + e^{t})$ is increasing, so $L(v)$ is an increasing function of $-s\, z(v) = -s\, b + \sum_i (-s\, w_i) v_i$. By the argument of Theorem 1 with the coefficients $-s\, w_i$ in place of $g_i$, the linear function $-s\, z(v)$ is largest over $S$ at the point with $v_i = u_i$ when $-s\, w_i > 0$ and $v_i = \ell_i$ when $-s\, w_i < 0$. Since the coefficients have the signs of the $g_i$, this point is $x'$. A maximizer of $-s\, z$ is a maximizer of $L$. $\blacksquare$

**Targeted variant.** The function `targeted_fgsm` steps against the gradient of the loss of the target label. The same argument with $-g$ in place of $g$ shows that it minimizes the linearized target loss over $S$.
