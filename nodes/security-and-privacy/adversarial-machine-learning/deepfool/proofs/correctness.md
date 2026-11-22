---
title: DeepFool finds the minimum l2 perturbation of an affine classifier in one iteration
proves: [correctness]
status: full
---

Let the model have logits $z(v) \in \mathbb{R}^K$ and label $\hat k(v) = \arg\max_k z_k(v)$, and let $k_0 = \hat k(x)$ (line L1). For $k \ne k_0$ write $f_k(v) = z_k(v) - z_{k_0}(v)$ and $w_k(v) = \nabla f_k(v)$. At the current point $p$ the function `nearest_boundary_step` picks the class $l$ with the smallest $|f_l(p)| / \lVert w_l(p) \rVert_2$ among the classes with $w_k \ne 0$, and returns $r_p = \frac{|f_l(p)| + \delta}{\lVert w_l \rVert_2^2}\, w_l$, where $\delta = 10^{-12}$.

**Lemma 1 (the step of one iteration).** Let the model be affine, $z(v) = Wv + b$, so that each $w_k$ is a constant vector and each $f_k$ is affine. Let $p$ have label $k_0$, so $f_k(p) \le 0$ for all $k$. Then:

1. The $\ell_2$ distance from $p$ to the closed half space $\{v : f_k(v) \ge 0\}$ is $|f_k(p)| / \lVert w_k \rVert_2$.
2. The $\ell_2$ distance from $p$ to the set $A = \{v \in \mathbb{R}^d : \hat k(v) \ne k_0\}$ is at least $\rho = \min_{k: w_k \ne 0} |f_k(p)| / \lVert w_k \rVert_2$.
3. $f_l(p + t\, r_p) = (t - 1)|f_l(p)| + t\delta$ for $t \ge 0$. So $f_l(p + t r_p) > 0$ for every $t \ge 1$.

*Proof.* (1) The half space is $\{v : w_k^\top (v - p) \ge -f_k(p)\}$. The distance from a point to the half space $\{v : a^\top (v - p) \ge \beta\}$ with $\beta \ge 0$ and $a \ne 0$ is $\beta / \lVert a \rVert_2$, attained at $p + \beta a / \lVert a \rVert_2^2$. (2) A point $v$ has $\hat k(v) \ne k_0$ only if $z_k(v) \ge z_{k_0}(v)$ for some $k$, that is $f_k(v) \ge 0$. So $A$ is inside the union of the half spaces of part (1). A class with $w_k = 0$ has $f_k$ constant and $f_k(p) \le 0$. If $f_k(p) < 0$, its half space is empty. If $f_k(p) = 0$, then $z_k = z_{k_0}$ everywhere; a tie goes to the smaller index, and the label at $p$ is $k_0$, so $k_0 < k$ and the class $k$ never takes the label. So only the classes with $w_k \ne 0$ count. The distance to a union is the minimum of the distances. (3) Since $f_l$ is affine, $f_l(p + t r_p) = f_l(p) + t\, w_l^\top r_p = f_l(p) + t(|f_l(p)| + \delta)$, and $f_l(p) = -|f_l(p)|$. $\square$

**Theorem 1 (affine models).** Let the model be affine and let the point $q = x + (1 + \gamma) r_x$, where $\gamma \ge 0$ is the overshoot, lie in $[0,1]^d$. Then DeepFool returns $(q, 1)$. The label of $q$ is not $k_0$, and $\lVert q - x \rVert_2 = (1 + \gamma)(\rho + \delta / \lVert w_l \rVert_2)$, where $\rho$ is the lower bound of Lemma 1 at $p = x$. So the distance is the true minimum times $1 + \gamma$, up to the term in $\delta$.

*Proof.* At $it = 0$, line L3 gives $p = x$ because $r = 0$, and line L4 does not return because the label of $x$ is $k_0$ (assume $\text{max\_iter} \ge 1$). Lines L5 to L7 set $r = r_x$. At $it = 1$, line L3 gives $p = \operatorname{clip}(x + (1+\gamma) r_x) = q$, since $q$ is in the box. By Lemma 1(3) with $t = 1 + \gamma \ge 1$, $f_l(q) > 0$, so $z_l(q) > z_{k_0}(q)$ and the label of $q$ is not $k_0$. Line L4 returns $(q, 1)$. The length of $r_x$ is $(|f_l(x)| + \delta) / \lVert w_l \rVert_2 = \rho + \delta / \lVert w_l \rVert_2$. By Lemma 1(2) no point closer than $\rho$ to $x$ has another label, and the point $x + r_x - \delta w_l / \lVert w_l\rVert_2^2$, at distance $\rho$, is on the boundary, so $\rho$ is the minimum distance to the closure of $A$. $\square$

**Theorem 2 (any model).** For every model, DeepFool returns $(p, it)$ with $p \in [0,1]^d$ and $0 \le it \le \text{max\_iter}$. If $it < \text{max\_iter}$, the label of $p$ is not $k_0$. It calls the logits $it + 2$ times and the Jacobian $it$ times.

*Proof.* Line L3 clips every point to $[0,1]^d$. The loop of line L2 runs for $it = 0, 1, \dots, \text{max\_iter}$, and line L4 returns at the latest when $it = \text{max\_iter}$; so line L8 is never reached and $it \le \text{max\_iter}$. Line L4 returns with $it < \text{max\_iter}$ only when the label of $p$ is not $k_0$. Each pass calls the logits once in line L3 and, if it does not return, the Jacobian once in line L5; line L1 adds one call of the logits. $\blacksquare$

**What is not claimed.** For a nonlinear model, the linearization of line L6 is only a local model. DeepFool can need many iterations, can stop at $\text{max\_iter}$ without a label change, and its distance is an upper bound on the true minimum, not the minimum. If every $w_k(p)$ is $0$, the step is $0$ and the loop runs to $\text{max\_iter}$.
