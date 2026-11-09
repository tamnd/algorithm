---
title: Rprop uses only gradient signs, keeps its steps in range, and converges linearly on separable functions whose derivatives change sign once
proves: [correctness, convergence-rate]
status: full
---

**Setting.** This file analyses Rprop in the iRprop⁻ form of Igel and Hüsken (2000), which is the form in the code. Each coordinate $i$ has a step size $\Delta_i$, starting at $\Delta_0 > 0$, and a stored gradient $p_i$, starting at $0$. With factors $0 < \eta^- < 1 < \eta^+$ and bounds $0 \le \Delta_{\min} \le \Delta_0 \le \Delta_{\max}$, iteration $t$ computes $g = \nabla f(x_t)$ and, for each $i$:

1. if $g_ip_i > 0$, set $\Delta_i \leftarrow \min(\eta^+\Delta_i, \Delta_{\max})$;
2. if $g_ip_i < 0$, set $\Delta_i \leftarrow \max(\eta^-\Delta_i, \Delta_{\min})$ and $g_i \leftarrow 0$;
3. set $x_{t+1,i} = x_{t,i} - \operatorname{sign}(g_i)\Delta_i$ and $p_i \leftarrow g_i$.

So in an iteration where the sign flips, coordinate $i$ does not move, and in the next iteration the product $g_ip_i$ is $0$, so the step size is kept.

**Proposition 1 (only signs matter).** Let $\phi_{t,i} > 0$ be arbitrary. If the gradient oracle returns $\phi_{t,i}g_{t,i}$ instead of $g_{t,i}$, the iterates do not change.

*Proof.* Each rule uses $g_i$ only through the sign of $g_ip_i$ and the sign of $g_i$, and $p_i$ is either $0$ or a past gradient with a positive factor. By induction the two runs have the same signs, the same $\Delta$ and the same $x$. $\square$

Hence Rprop is invariant to any rescaling of the loss and to any monotone change of each partial derivative, but not to a rotation or a rescaling of the coordinates.

**Proposition 2 (step sizes in range).** At every iteration, $\Delta_{\min} \le \Delta_i \le \Delta_{\max}$, and every move $|x_{t+1,i} - x_{t,i}|$ is either $0$ or equal to the current $\Delta_i$.

*Proof.* The bounds hold at the start and each rule clips to them. A move is $\operatorname{sign}(g_i)\Delta_i$ with $\operatorname{sign}(g_i) \in \{-1, 0, 1\}$. $\square$

**Theorem 3 (separable functions).** Let $f(x) = \sum_ih_i(x_i)$, where each $h_i$ is differentiable and has a point $z_i$ with $h_i'(u) < 0$ for $u < z_i$ and $h_i'(u) > 0$ for $u > z_i$. So $z$ is the unique stationary point and the unique minimizer; $h_i$ need not be convex. Let $\Delta_{\min} = 0$ and

$$\eta^-\eta^+ < 1, \qquad \eta^-(1 + \eta^+) \ge 1,$$

which hold for the usual $\eta^+ = 1.2$, $\eta^- = 0.5$. Fix a coordinate $i$. Then either $x_{t,i} = z_i$ from some iteration on, or the following hold. Let $t_1 < t_2 < \dots$ be the iterations in which a sign flip is detected in coordinate $i$, and let $s_k$ be the length of the last move before $t_k$. Then

1. $t_1$ is finite;
2. $|x_{t,i} - z_i| \le s_k$ for all $t \ge t_k$;
3. $s_{k+1} \le \eta^-\eta^+s_k$ and $t_{k+1} - t_k \le 3$.

Consequently, for all $t \ge t_1$,

$$|x_{t,i} - z_i| \le s_1(\eta^-\eta^+)^{\lfloor(t - t_1)/3\rfloor}.$$

*Proof.* The function is separable, so $g_i = h_i'(x_i)$ depends only on $x_i$ and each coordinate runs Rprop in one dimension on its own. Drop the index $i$ and write $e_t = |x_t - z|$. If some iterate equals $z$, then $g = 0$ from then on, nothing moves and the first case holds. Otherwise the sign of $g$ at $x$ is the sign of $x - z$, so each move goes toward $z$, and a sign flip is detected exactly when the previous move crossed $z$.

*Part 1.* Before the first flip all moves go in the same direction. The first move has length $\Delta_0$, and every later one has length $\min(\Delta_0(\eta^+)^j, \Delta_{\max}) \ge \Delta_0$. So the total distance moved grows without bound, and $z$ is crossed after finitely many moves.

*Part 2.* At $t_k$ the last move, of length $s_k$, crossed $z$, so $e_{t_k} \le s_k$. Until the next crossing the moves go toward $z$ without passing it, so $e$ does not increase. At the next crossing $e \le s_{k+1}$, and part 3 gives $s_{k+1} \le s_k$. By induction $e_t \le s_k$ for all $t \ge t_k$.

*Part 3.* At $t_k$, coordinate $i$ does not move and $\Delta$ becomes $\eta^-s_k$ (the clip at $\Delta_{\min} = 0$ is inactive). At $t_k + 1$ the gradient is the same as at $t_k$, the product with the stored $0$ is $0$, and the method moves by $\eta^-s_k$ toward $z$. If this crosses $z$, then $t_{k+1} = t_k + 2$ and $s_{k+1} = \eta^-s_k \le \eta^-\eta^+s_k$. Otherwise, at $t_k + 2$ the sign is unchanged, $\Delta$ becomes $\min(\eta^+\eta^-s_k, \Delta_{\max}) = \eta^+\eta^-s_k$, because $\eta^+\eta^-s_k < s_k \le \Delta_{\max}$, and the method moves by this amount. The two moves together cover $\eta^-(1 + \eta^+)s_k \ge s_k \ge e_{t_k}$, so this move reaches or crosses $z$. If it reaches $z$ exactly, the first case holds. Otherwise $t_{k+1} = t_k + 3$ and $s_{k+1} = \eta^-\eta^+s_k$.

*The bound.* For $t_k \le t < t_{k+1}$, part 2 and part 3 give $e_t \le s_k \le s_1(\eta^-\eta^+)^{k-1}$, and $t - t_1 < t_{k+1} - t_1 \le 3k$, so $\lfloor(t - t_1)/3\rfloor \le k - 1$. $\square$

For the defaults the error falls by at least the factor $0.6$ every three iterations, about $0.843$ per iteration, independent of the curvature of $h_i$: a flat or a steep $h_i$ gives the same rate, because only signs are used. This is the property that made Rprop fast on the badly scaled error surfaces of neural networks.

**What the theorem does not cover.**

- **$\Delta_{\min} > 0$.** Then the step cannot shrink below $\Delta_{\min}$, and the iterates end up moving around $z$ at distances of order $\Delta_{\min}$, not converging to it.
- **Nonseparable functions.** Then $g_i$ depends on the other coordinates, a sign flip no longer means that $z_i$ was crossed, and the argument fails. The sources here give no convergence theorem for the original rules on general smooth functions. Anastasiadis, Magoulas and Vrahatis (2005) add a step-size condition to obtain a globally convergent variant.
- **Stochastic gradients.** With minibatches, the sign of a noisy gradient flips at random, the step sizes shrink, and the method stalls; signs of small and large gradients get the same weight, so the sign of a sum is not recovered from the signs of its parts. This is why RMSProp was proposed as a minibatch version.
- **The original 1993 rule.** Riedmiller and Braun also undo the previous move after a sign flip (weight backtracking); the theorem above is for the form without backtracking.
