---
title: The PGD attack stays in the allowed set and reaches the optimum on a linear model
proves: [correctness]
status: full
---

We write $S_p = B_p(x, \epsilon) \cap [0,1]^d$ for $p \in \{2, \infty\}$, with $x \in [0,1]^d$, $\epsilon \ge 0$ and $\alpha > 0$. The map $P$ of line L5 is the function `project`: for $p = \infty$ it clips coordinate $i$ to $[\ell_i, u_i] = [\max(x_i - \epsilon, 0), \min(x_i + \epsilon, 1)]$; for $p = 2$ it rescales $v - x$ onto the ball, $v \mapsto x + \min(1, \epsilon / \lVert v - x \rVert_2)(v - x)$, and then clips to $[0,1]^d$.

**Lemma 1.** $P(v) \in S_p$ for every $v \in \mathbb{R}^d$. For $p = \infty$, $P$ is the Euclidean projection onto $S_\infty$.

*Proof.* For $p = \infty$, $S_\infty = \prod_i [\ell_i, u_i]$, since each coordinate must satisfy $|v_i - x_i| \le \epsilon$ and $0 \le v_i \le 1$. Clipping each coordinate to its interval gives a point of the product, and it is the nearest point because the squared distance is a sum of one term for each coordinate. For $p = 2$, the rescaled point $r$ satisfies $\lVert r - x \rVert_2 \le \epsilon$. Clipping to $[0,1]$ moves each coordinate $r_i$ toward the interval $[0,1]$, which contains $x_i$, so $|\operatorname{clip}(r_i) - x_i| \le |r_i - x_i|$ for each $i$. Hence the clipped point is in $[0,1]^d$ and still within distance $\epsilon$ of $x$. $\square$

**Theorem 1 (feasibility and monotone record).** Every iterate $x^t$ lies in $S_p$, and the returned point $x^\star$ is an iterate with $L(x^\star) = \max_{0 \le t \le T} L(x^t)$, where $T$ is the number of steps.

*Proof.* The start of line L1 is $x \in S_p$ or the image under $P$ of a random point, so it lies in $S_p$ by Lemma 1. Each later iterate is an image under $P$ (line L5), so it lies in $S_p$ too. Lines L2 and L6 keep the iterate with the largest loss seen so far, and line L7 returns it. $\square$

So the returned point is always a valid perturbation of $x$, and its loss is at least the loss of the start. This is what an attack needs to give an upper bound on robust accuracy: if $x^\star$ is misclassified, then $x$ is not robust at radius $\epsilon$.

**Theorem 2 (the linear model, $p = \infty$).** Let the model be logistic regression with logit $z(v) = w^\top v + b$ and label $y \in \{0,1\}$, and let $s = 2y - 1$. Assume $\alpha T \ge 2\epsilon$. Then, from any start in $S_\infty$, the last iterate $x^T$ is the point $x^{\mathrm{F}}$ returned by FGSM, and $x^\star$ maximizes the loss over $S_\infty$.

*Proof.* The input gradient is $g(v) = (\sigma(z(v)) - y)\, w$. The scalar factor is negative for $y = 1$ and positive for $y = 0$, at every $v$, so $\operatorname{sign}(g_i(v)) = -s \operatorname{sign}(w_i)$ does not depend on $v$. Fix a coordinate $i$ with $w_i \ne 0$, and say $-s\, w_i > 0$ (the other sign is symmetric). Each step adds $\alpha$ to coordinate $i$ and clips it to $[\ell_i, u_i]$. So the coordinate is $\min(x^0_i + t\alpha, u_i)$ after $t$ steps. Since $u_i - x^0_i \le u_i - \ell_i \le 2\epsilon \le \alpha T$, it equals $u_i$ after $T$ steps. A coordinate with $w_i = 0$ has a step of $0$ and keeps its start value; it does not change the loss. FGSM sets coordinate $i$ to $u_i$ when $-s\, w_i > 0$ and to $\ell_i$ when $-s\, w_i < 0$ (see the proof page of fast-gradient-sign-method), so $x^T$ and $x^{\mathrm{F}}$ agree on all coordinates that affect the loss, and $L(x^T) = L(x^{\mathrm{F}})$. That proof also shows that $x^{\mathrm{F}}$ maximizes the loss over $S_\infty$. By Theorem 1, $L(x^\star) \ge L(x^T)$, and $L(x^\star)$ cannot be larger than the maximum, so $x^\star$ is a maximizer too. $\square$

**Theorem 3 (the linear model, $p = 2$).** Under the same model, assume that the point $x^{\mathrm{L2}} = x - s\, \epsilon\, w / \lVert w \rVert_2$ lies in $[0,1]^d$, that $w \ne 0$, and that the start is $x$. If $\alpha T \ge \epsilon$, the last iterate is $x^{\mathrm{L2}}$, and $x^{\mathrm{L2}}$ maximizes the loss over $S_2$.

*Proof.* The normalized ascent direction is $g / \lVert g \rVert_2 = -s\, w / \lVert w \rVert_2 =: e$ at every point, a fixed unit vector. Starting from $x$, the iterates stay on the ray $x + \tau e$ with $\tau \ge 0$: a step adds $\alpha$ to $\tau$, the rescaling caps $\tau$ at $\epsilon$, and the clip does nothing because the whole segment from $x$ to $x^{\mathrm{L2}}$ lies in the convex set $[0,1]^d$. After $T$ steps $\tau = \min(T\alpha, \epsilon) = \epsilon$. For optimality, the loss is increasing in $-s\, z(v) = -s\,b - s\, w^\top v$, and by the Cauchy-Schwarz inequality $-s\, w^\top (v - x) \le \lVert w \rVert_2 \lVert v - x \rVert_2 \le \epsilon \lVert w \rVert_2$ on $S_2$, with equality at $v = x^{\mathrm{L2}}$. $\blacksquare$

**What is not claimed.** For a nonlinear model the loss is not concave in $v$, and PGD can stop at a local maximum. Theorem 1 still holds, so the output is a valid perturbation, but a failure of PGD is no proof of robustness. Only a verifier or a certificate gives a lower bound on robust accuracy.
