---
title: What can be proved about ASD-POCS
proves: [correctness]
status: partial
---

ASD-POCS as a whole has no convergence proof, and we give none. We prove the two parts that the page states as theorems: the data steps alone converge on consistent data, and line L6 uses the exact gradient of a convex function, so short steps along it lower the total variation. We also prove two small facts about lines L6 and L7. We work in exact arithmetic in $\mathbb{R}^N$ with the Euclidean norm.

## Part 1: the data steps

Let $H_i = \{x : \langle a_i, x\rangle = y_i\}$ for each ray $i$ with $a_i \ne 0$, and $Q = \{x : x \ge 0\}$. The projection onto $H_i$ is $P_i x = x + \frac{y_i - \langle a_i, x\rangle}{\|a_i\|^2} a_i$, and the projection onto $Q$ clips at 0. So with $g = 0$ and a fixed $\beta$ ($\beta_{\text{red}} = 1$), line L3 applies $x \leftarrow x + \beta(P_i x - x)$ for each ray in turn, and line L4 applies $P_Q$.

**Lemma 1 (Fejer steps).** Let $p \in S = Q \cap \bigcap_i H_i$ and $0 < \beta < 2$. Then
$$\|x + \beta(P_i x - x) - p\|^2 = \|x - p\|^2 - \beta(2 - \beta)\|P_i x - x\|^2, \qquad \|P_Q x - p\|^2 \le \|x - p\|^2 - \|P_Q x - x\|^2.$$

*Proof.* The vector $P_i x - x$ is a multiple of $a_i$, and $x - P_i x$ is orthogonal to $P_i x - p$ because both $P_i x$ and $p$ lie in $H_i$. Write $u = x - p$ and $s = P_i x - x$, so $\langle u, s\rangle = \langle P_i x - p, s\rangle - \|s\|^2 = -\|s\|^2$. Then $\|u + \beta s\|^2 = \|u\|^2 + 2\beta\langle u, s\rangle + \beta^2\|s\|^2 = \|u\|^2 - (2\beta - \beta^2)\|s\|^2$. For the closed convex set $Q$, the projection satisfies $\langle x - P_Q x, p - P_Q x\rangle \le 0$, so $\|x - p\|^2 = \|x - P_Q x\|^2 + \|P_Q x - p\|^2 + 2\langle x - P_Q x, P_Q x - p\rangle \ge \|x - P_Q x\|^2 + \|P_Q x - p\|^2$. $\square$

**Theorem 1.** Let $S$ be nonempty (consistent data with a nonnegative solution), $0 < \beta < 2$ fixed and $g = 0$. Then the iterates of ASD-POCS converge to a point of $S$.

*Proof.* List all sub-steps (one per ray, then the clipping) as one sequence $u_0, u_1, u_2, \dots$. By Lemma 1, $\|u_t - p\|$ does not increase for each $p \in S$, so the sequence is bounded, and summing the decreases gives $\sum_t \|u_{t+1} - u_t\|^2 < \infty$, so the step lengths tend to 0. Let $x^*$ be a cluster point of the sweep starts $x_k$, along a subsequence $k_l$. The sweep has a fixed finite number of sub-steps, each of length tending to 0, so all sub-iterates of sweep $k_l$ tend to $x^*$ too. The sub-step for ray $i$ moves $u$ by $\beta\,\mathrm{dist}(u, H_i)$, and the clipping moves $u$ by $\mathrm{dist}(u, Q)$. These tend to 0, and the distance functions are continuous, so $\mathrm{dist}(x^*, H_i) = 0$ for every $i$ and $\mathrm{dist}(x^*, Q) = 0$. The sets are closed, so $x^* \in S$. Now apply the monotonicity with $p = x^*$: $\|u_t - x^*\|$ does not increase and has a subsequence tending to 0, so the whole sequence tends to $x^*$. The code returns $x_{\text{res}}$, a member of this sequence, so it converges to $x^*$ as well. $\square$

With $\beta_{\text{red}} < 1$ the relaxation $\beta_k = \beta\,\beta_{\text{red}}^k$ tends to 0 and is summable, so Theorem 1 does not apply. The example of the page shows the misfit leveling off above $\varepsilon$ in that case.

## Part 2: the TV steps

For $x \in \mathbb{R}^{n \times n}$, index $k = i n + j$, put $\delta^x_k = x_{k+n} - x_k$ if $i + 1 < n$ and 0 otherwise, $\delta^y_k = x_{k+1} - x_k$ if $j + 1 < n$ and 0 otherwise, and $s_k = \sqrt{(\delta^x_k)^2 + (\delta^y_k)^2 + \eta^2}$. Then $\operatorname{TV}_\eta(x) = \sum_k s_k$.

**Lemma 2 (convexity).** For $\eta \ge 0$, $\operatorname{TV}_\eta$ is convex. For $\eta > 0$ it is differentiable everywhere.

*Proof.* The map $x \mapsto (\delta^x_k, \delta^y_k, \eta)$ is affine, and $s_k$ is the Euclidean norm of its value. A norm composed with an affine map is convex, and a sum of convex functions is convex. For $\eta > 0$, the norm is evaluated away from the origin, where it is differentiable. $\square$

**Lemma 3 (the gradient).** For $\eta > 0$, `tv_grad` returns $\nabla \operatorname{TV}_\eta(x)$.

*Proof.* The term $s_k$ depends on $x_k$, on $x_{k+n}$ when $i + 1 < n$, and on $x_{k+1}$ when $j + 1 < n$. By the chain rule, $\partial s_k / \partial x_{k+n} = \delta^x_k / s_k$, $\partial s_k / \partial x_{k+1} = \delta^y_k / s_k$ and $\partial s_k / \partial x_k = -(\delta^x_k + \delta^y_k)/s_k$, where a difference that is fixed at 0 contributes nothing. The code adds exactly these terms for each $k$, and the gradient of a sum is the sum of the gradients. $\square$

**Proposition 4 (descent for short steps).** If $v = \nabla \operatorname{TV}_\eta(x) \ne 0$, then $\operatorname{TV}_\eta(x - t v/\|v\|) < \operatorname{TV}_\eta(x)$ for all small enough $t > 0$.

*Proof.* The directional derivative of $\operatorname{TV}_\eta$ at $x$ along $-v/\|v\|$ is $-\langle v, v\rangle / \|v\| = -\|v\| < 0$. $\square$

Line L6 uses the fixed length $dtvg$, not a line search, so this proposition does not imply that each step of line L6 lowers TV.

## Part 3: two facts about lines L6 and L7

**Proposition 5.** Each step of line L6 moves the image by exactly $dtvg$, and $dg \le g \cdot dtvg$.

*Proof.* The step is $-dtvg \cdot v/\|v\|$, a vector of length $dtvg$. The total change $x - x_1$ is the sum of $g$ such vectors, and the triangle inequality bounds its length. (The code stops early if $v = 0$, which only shortens the sum.) $\square$

**Proposition 6.** The TV step length $dtvg$ never increases, and it decreases by the factor $\alpha_{\text{red}}$ in each iteration in which $dg > r_{\max}\, dp$ and $dd > \varepsilon$.

*Proof.* Line L7 is the only line that changes $dtvg$ after the first iteration, and it multiplies it by $\alpha_{\text{red}} < 1$ under exactly this condition. $\square$

These facts bound the TV steps; they do not show that the iterates converge or that the limit, if any, solves the constrained TV problem.
