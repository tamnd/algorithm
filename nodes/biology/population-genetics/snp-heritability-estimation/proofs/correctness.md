---
title: The average information step goes uphill on the REML likelihood and stops at a stationary point
proves: [correctness]
status: full
---

Let $y \in \mathbb R^n$, let $X$ be $n \times p$ with full column rank and $p < n$, and let $A_1, \dots, A_r$ be symmetric. For $\theta = (\theta_1, \dots, \theta_{r+1})$ put $V(\theta) = \sum_{k \le r} \theta_k A_k + \theta_{r+1} I$, and let $\Omega$ be the open set of $\theta$ with $V(\theta)$ positive definite. On $\Omega$ put $C = X^\top V^{-1} X$, $P = V^{-1} - V^{-1} X C^{-1} X^\top V^{-1}$, and

$$\ell_R(\theta) = -\tfrac12 \bigl[\log\det V + \log\det C + y^\top P y\bigr].$$

$V_k = \partial V / \partial \theta_k$ is $A_k$ for $k \le r$ and $I$ for $k = r + 1$, and does not depend on $\theta$.

**Lemma 1 (properties of $P$).** $P$ is symmetric, $P X = 0$, $P V P = P$, and $P$ is positive semidefinite.

*Proof.* Symmetry is clear. $P X = V^{-1} X - V^{-1} X C^{-1} C = 0$. Let $V^{1/2}$ be the symmetric square root and $Z = V^{-1/2} X$. Then $P = V^{-1/2} (I - H) V^{-1/2}$ with $H = Z (Z^\top Z)^{-1} Z^\top$, the orthogonal projection on the columns of $Z$. $I - H$ is a symmetric idempotent matrix, so it is positive semidefinite, and $P V P = V^{-1/2} (I - H)^2 V^{-1/2} = P$. $\square$

**Lemma 2 (derivative of $P$).** $\partial P / \partial \theta_k = -P V_k P$.

*Proof.* With $\partial V^{-1} = -V^{-1} V_k V^{-1}$ and $\partial C^{-1} = C^{-1} (X^\top V^{-1} V_k V^{-1} X) C^{-1}$, the product rule gives

$$\partial P = -V^{-1} V_k V^{-1} + V^{-1} V_k V^{-1} X C^{-1} X^\top V^{-1} + V^{-1} X C^{-1} X^\top V^{-1} V_k V^{-1} - V^{-1} X C^{-1} X^\top V^{-1} V_k V^{-1} X C^{-1} X^\top V^{-1}.$$

Write $Q = V^{-1} X C^{-1} X^\top V^{-1}$, so $P = V^{-1} - Q$. The four terms are $-(V^{-1} V_k V^{-1} - V^{-1} V_k Q - Q V_k V^{-1} + Q V_k Q) = -(V^{-1} - Q) V_k (V^{-1} - Q)$. $\square$

**Lemma 3 (score, line L3).** $\partial \ell_R / \partial \theta_k = -\tfrac12 \bigl[\operatorname{tr}(P V_k) - y^\top P V_k P y\bigr]$.

*Proof.* $\partial \log\det V = \operatorname{tr}(V^{-1} V_k)$ and $\partial \log\det C = \operatorname{tr}(C^{-1} \partial C) = -\operatorname{tr}(C^{-1} X^\top V^{-1} V_k V^{-1} X) = -\operatorname{tr}(Q V_k)$ by the cyclic property of the trace. Their sum is $\operatorname{tr}((V^{-1} - Q) V_k) = \operatorname{tr}(P V_k)$. By Lemma 2, $\partial (y^\top P y) = -y^\top P V_k P y$. $\square$

**Lemma 4 (the average information, line L4).** Let $H_{kl} = -\partial^2 \ell_R / \partial \theta_k \partial \theta_l$ be the observed information and $F_{kl} = \mathrm E[H_{kl}]$ under $y \sim N(X \beta, V)$ the expected information. Then $\tfrac12 (H_{kl} + F_{kl}) = \tfrac12 y^\top P V_k P V_l P y = \mathrm{AI}_{kl}$, and $\mathrm{AI}$ is positive semidefinite.

*Proof.* Differentiate Lemma 3 in $\theta_l$ with Lemma 2: $\partial \operatorname{tr}(P V_k) = -\operatorname{tr}(P V_l P V_k)$ and $\partial (y^\top P V_k P y) = -2 y^\top P V_l P V_k P y$ (two terms, equal because the matrices are symmetric). So $H_{kl} = -\tfrac12 \operatorname{tr}(P V_k P V_l) + y^\top P V_k P V_l P y$. For a symmetric $B$, $\mathrm E[y^\top B y] = \operatorname{tr}(B V) + \beta^\top X^\top B X \beta$. With $B = P V_k P V_l P$, $B X = 0$ by Lemma 1, and $\operatorname{tr}(B V) = \operatorname{tr}(V_k P V_l P V P) = \operatorname{tr}(V_k P V_l P)$ since $P V P = P$. So $F_{kl} = \tfrac12 \operatorname{tr}(P V_k P V_l)$, and the mean of $H$ and $F$ is $\tfrac12 y^\top P V_k P V_l P y$. With $u_k = V_k P y$, $\mathrm{AI}_{kl} = \tfrac12 u_k^\top P u_l$, so for any $c$, $c^\top \mathrm{AI}\, c = \tfrac12 (\sum_k c_k u_k)^\top P (\sum_k c_k u_k) \ge 0$ by Lemma 1. $\square$

**Lemma 5 (the halving of line L6 ends).** Let $\theta \in \Omega$ have every component above the floor, let $d = \nabla \ell_R(\theta) \ne 0$, let $\mathrm{AI}$ be positive definite, and let $\Delta = \mathrm{AI}^{-1} d$. Then for all small enough $t > 0$, $\theta + t \Delta \in \Omega$, every component stays above the floor, and $\ell_R(\theta + t \Delta) > \ell_R(\theta)$.

*Proof.* $\Omega$ is open and the floor constraints are strict at $\theta$, so both hold for small $t$. $\mathrm{AI}^{-1}$ is positive definite, so $d^\top \Delta = d^\top \mathrm{AI}^{-1} d > 0$. $\ell_R$ is smooth on $\Omega$, so $\ell_R(\theta + t \Delta) = \ell_R(\theta) + t\, d^\top \Delta + o(t)$, which is above $\ell_R(\theta)$ for small $t$. Halving $\Delta$ reaches such a $t = 2^{-j}$ after finitely many steps. $\square$

The first round uses the EM-REML step $\Delta_k = \theta_k^2 (y^\top P V_k P y - \operatorname{tr}(P V_k)) / n = 2 \theta_k^2 d_k / n$. This is $D d$ with the positive diagonal matrix $D = \operatorname{diag}(2 \theta_k^2 / n)$, so $d^\top \Delta > 0$ when $d \ne 0$, and the proof of Lemma 5 applies to it too.

**Theorem.** (a) The values $\ell_R(\theta^{(t)})$ of the accepted iterates never decrease. (b) Let the iterates converge to $\theta^\ast \in \Omega$ with every component above the floor and $\mathrm{AI}(\theta^\ast)$ positive definite, with steps of length $t_j \ge \tau > 0$ for some $\tau$. Then $\nabla \ell_R(\theta^\ast) = 0$, so $\theta^\ast$ is a stationary point of the REML likelihood.

*Proof.* (a) Line L6 accepts a point only when $\ell_R$ does not go down. (b) The iterates converge, so the accepted steps $t_j \mathrm{AI}(\theta^{(j)})^{-1} d(\theta^{(j)})$ go to $0$. Since $t_j \ge \tau$, $\mathrm{AI}(\theta^{(j)})^{-1} d(\theta^{(j)}) \to 0$. The functions $d$ and $\mathrm{AI}$ are continuous on $\Omega$ and $\mathrm{AI}(\theta^\ast)$ is invertible, so $\mathrm{AI}(\theta^\ast)^{-1} d(\theta^\ast) = 0$ and $d(\theta^\ast) = 0$. $\square$

Line L7 computes $h^2$ from the returned $\theta$. Line L8 uses $\mathrm{AI}^{-1}$ at the end point as the covariance matrix of $\hat\theta$, and the gradient $g$ of $h^2(\theta) = \sum_{k \le r} \theta_k / \sum_k \theta_k$, with $g_k = \theta_{r+1} / \sigma_P^4$ for $k \le r$ and $g_{r+1} = -\sum_{k \le r} \theta_k / \sigma_P^4$, where $\sigma_P^2 = \sum_k \theta_k$. The standard error is $\sqrt{g^\top \mathrm{AI}^{-1} g}$, the delta method.

**What the theorem does not say.** It does not say that the stationary point is the global maximum, and it does not cover a maximum on the boundary, where a component sits at the floor. At a stationary point the AI matrix differs from the expected information by a term with mean zero, so the standard error is an approximation that is good in large samples and away from the boundary. The tests check the stationary point against an independent maximization of the profile likelihood, against the closed form of the balanced one-way layout, and against finite differences of $\ell_R$.
