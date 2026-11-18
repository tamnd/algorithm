---
title: XPBD is Gauss-Seidel on a simplified Newton system of backward Euler, and it is exact for linear constraints
proves: [correctness]
status: full
---

We use the notation of the page. There are $n$ particles with positions $\mathbf x \in \mathbb R^{2n}$, a diagonal mass matrix $M$ and inverse masses $w_i = 1/m_i$; a pinned particle has $w_i = 0$ and is left out of all sums over masses. There are $c$ constraints $C_j$ with compliances $\alpha_j \ge 0$, and $\tilde\alpha_j = \alpha_j / \Delta t^2$. The matrix $G(\mathbf x)$ has the rows $\nabla C_j(\mathbf x)^T$, and $\tilde A = \operatorname{diag}(\tilde\alpha_j)$. The prediction of line L1 is $\tilde{\mathbf x} = \mathbf x^n + \Delta t \mathbf v^n + \Delta t^2 \mathbf g$ on the free particles. Lines L6 and L7 apply to the constraint $j$

$$\Delta\lambda_j = \frac{-C_j(\mathbf p) - \tilde\alpha_j \lambda_j}{\sum_i w_i |\nabla_i C_j(\mathbf p)|^2 + \tilde\alpha_j}, \qquad \Delta \mathbf p_i = w_i \nabla_i C_j(\mathbf p)\, \Delta\lambda_j ,$$

which is equation (18) of Macklin et al. (2016). For a distance constraint $|\nabla_i C_j| = 1$, so the denominator is $w_i + w_j + \tilde\alpha_j$.

## The backward Euler step and its Newton system

**Lemma 1.** Let $\alpha_j > 0$ for all $j$. The backward Euler step for the potential $U(\mathbf x) = \sum_j \frac{1}{2\alpha_j} C_j(\mathbf x)^2$ is a stationary point of

$$E(\mathbf x) = \tfrac12 (\mathbf x - \tilde{\mathbf x})^T M (\mathbf x - \tilde{\mathbf x}) + \Delta t^2 U(\mathbf x).$$

With $\lambda_j = -C_j(\mathbf x)/\tilde\alpha_j$, the condition $\nabla E = 0$ is equivalent to the two equations

$$\mathbf h(\mathbf x, \boldsymbol\lambda) := M(\mathbf x - \tilde{\mathbf x}) - G(\mathbf x)^T \boldsymbol\lambda = 0, \qquad \mathbf C(\mathbf x) + \tilde A \boldsymbol\lambda = 0 .$$

*Proof.* Backward Euler is $M(\mathbf x - 2\mathbf x^n + \mathbf x^{n-1})/\Delta t^2 = -\nabla U(\mathbf x) + M\mathbf g$ with $\mathbf x^n - \mathbf x^{n-1} = \Delta t \mathbf v^n$, that is $M(\mathbf x - \tilde{\mathbf x}) + \Delta t^2 \nabla U(\mathbf x) = 0$, and this is $\nabla E(\mathbf x) = 0$. Now $\Delta t^2 \nabla U = \sum_j (\Delta t^2/\alpha_j) C_j \nabla C_j = -\sum_j \lambda_j \nabla C_j = -G^T \boldsymbol\lambda$ by the definition of $\lambda_j$, and that definition is the second equation. $\square$

The function $\mathbf h$ is the residual $\mathbf g$ of the paper; we write $\mathbf h$ to keep $\mathbf g$ for gravity. One Newton step on the two equations at $(\mathbf x, \boldsymbol\lambda)$ solves

$$\begin{pmatrix} K & -G^T \\ G & \tilde A \end{pmatrix} \begin{pmatrix} \Delta\mathbf x \\ \Delta\boldsymbol\lambda \end{pmatrix} = -\begin{pmatrix} \mathbf h \\ \mathbf C + \tilde A \boldsymbol\lambda \end{pmatrix}, \qquad K = M - \sum_j \lambda_j \nabla^2 C_j ,$$

which is equation (12) of the paper.

**Lemma 2.** Replace $K$ by $M$ and $\mathbf h$ by $0$. Then the system becomes $(G M^{-1} G^T + \tilde A)\Delta\boldsymbol\lambda = -\mathbf C - \tilde A\boldsymbol\lambda$ with $\Delta \mathbf x = M^{-1} G^T \Delta\boldsymbol\lambda$. One Gauss-Seidel update of the row $j$ of this system, with $G$ evaluated at the current $\mathbf p$, is lines L6 to L8.

*Proof.* The first block row gives $M\Delta\mathbf x = G^T \Delta\boldsymbol\lambda$. Put this into the second row: $G M^{-1} G^T \Delta\boldsymbol\lambda + \tilde A \Delta\boldsymbol\lambda = -\mathbf C - \tilde A\boldsymbol\lambda$. The diagonal entry of row $j$ is $\nabla C_j^T M^{-1} \nabla C_j + \tilde\alpha_j = \sum_i w_i |\nabla_i C_j|^2 + \tilde\alpha_j$. A Gauss-Seidel update solves row $j$ for $\Delta\lambda_j$ with the other unknowns at their current values. Since each earlier update has already been applied to $\mathbf p$ and $\boldsymbol\lambda$, the right side of row $j$ is $-C_j(\mathbf p) - \tilde\alpha_j\lambda_j$ and the off-diagonal terms are already used up, so the update is the $\Delta\lambda_j$ of line L6. The matching change of $\mathbf p$ is $M^{-1}\nabla C_j \Delta\lambda_j$, which is line L7. $\square$

Dropping the term $\sum_j \lambda_j \nabla^2 C_j$ (the geometric stiffness) makes this a quasi-Newton method. It changes the path to the solution but not the equations that a fixed point must satisfy. Setting $\mathbf h = 0$ is a different matter, as the next lemma shows.

## Fixed points

**Lemma 3.** Suppose the sweeps converge, so that $\Delta\lambda_j \to 0$ for every $j$ and $\mathbf p \to \mathbf x^*$, $\boldsymbol\lambda \to \boldsymbol\lambda^*$. Then $\mathbf C(\mathbf x^*) + \tilde A\boldsymbol\lambda^* = 0$. Also

$$\mathbf h(\mathbf x^*, \boldsymbol\lambda^*) = \sum_{\text{updates } u} \big(\nabla C_{j(u)}(\mathbf p_u) - \nabla C_{j(u)}(\mathbf x^*)\big)\, \Delta\lambda_u ,$$

where the sum runs over all updates of lines L6 and L7, $\mathbf p_u$ is the state at which update $u$ was computed, and the gradients are stacked into $\mathbb R^{2n}$.

*Proof.* The first claim is line L6 with $\Delta\lambda_j = 0$ and a finite denominator. For the second, line L3 sets $\mathbf p = \tilde{\mathbf x}$ and line L2 sets $\boldsymbol\lambda = 0$. Each update adds $M^{-1}\nabla C_j(\mathbf p_u)\Delta\lambda_u$ to $\mathbf p$ and $\Delta\lambda_u$ to $\lambda_j$. Summing, $M(\mathbf x^* - \tilde{\mathbf x}) = \sum_u \nabla C_{j(u)}(\mathbf p_u)\Delta\lambda_u$ and $G(\mathbf x^*)^T\boldsymbol\lambda^* = \sum_u \nabla C_{j(u)}(\mathbf x^*)\Delta\lambda_u$. Subtract. $\square$

So a converged XPBD step is a backward Euler step exactly when the residual $\mathbf h$ of Lemma 3 is zero, and the size of $\mathbf h$ depends on how much the constraint gradients turn during the step. This is a property of the method, not of the number of sweeps.

**Theorem 4 (linear constraints).** Let every $C_j$ be affine on a region that holds all iterates, $C_j(\mathbf x) = C_j(\tilde{\mathbf x}) + \mathbf a_j^T(\mathbf x - \tilde{\mathbf x})$, let $\alpha_j > 0$ for all $j$ and let every constraint touch at least one free particle. Then the XPBD sweeps converge for any number of constraints and any order, and the limit is the backward Euler step of Lemma 1.

*Proof.* The gradients $\mathbf a_j$ are constant, so the invariant of Lemma 3 reads $\mathbf p - \tilde{\mathbf x} = M^{-1} G^T \boldsymbol\lambda$ at all times, where now $G$ is constant. Hence $C_j(\mathbf p) + \tilde\alpha_j\lambda_j = (\mathbf b + A\boldsymbol\lambda)_j$ with $\mathbf b = \mathbf C(\tilde{\mathbf x})$ and $A = G M^{-1} G^T + \tilde A$, and line L6 is $\Delta\lambda_j = -(\mathbf b + A\boldsymbol\lambda)_j / A_{jj}$. This is the Gauss-Seidel method for $A\boldsymbol\lambda = -\mathbf b$. The matrix $A$ is symmetric, and it is positive definite because $\mathbf z^T A \mathbf z = |M^{-1/2} G^T \mathbf z|^2 + \sum_j \tilde\alpha_j z_j^2 > 0$ for $\mathbf z \ne 0$ (here $M^{-1/2}$ acts on the free particles only). Gauss-Seidel converges for every symmetric positive definite matrix and every start, so $\boldsymbol\lambda \to \boldsymbol\lambda^*$ with $A\boldsymbol\lambda^* = -\mathbf b$, and $\mathbf p \to \mathbf x^*$. Then $\mathbf h(\mathbf x^*, \boldsymbol\lambda^*) = 0$ by the invariant, and $\mathbf C(\mathbf x^*) + \tilde A\boldsymbol\lambda^* = 0$ by Lemma 3. By Lemma 1, $\mathbf x^*$ is the backward Euler step. $\square$

A distance constraint $|\mathbf x_i - \mathbf x_j| - d$ is affine on every region where the direction of $\mathbf x_i - \mathbf x_j$ does not change, for example a vertical chain that only moves vertically.

**Corollary 5 (one spring).** Take a pinned particle at the origin and a free particle of mass $m$ on the $x$ axis, joined by one distance constraint of rest length $r$ and compliance $\alpha$, with $k = 1/\alpha$ and no gravity. Let $y = x^n + \Delta t v^n > 0$ be the prediction. One sweep gives

$$x^{n+1} = \frac{m y + \Delta t^2 k r}{m + \Delta t^2 k},$$

the backward Euler step of the linear spring of stiffness $k$, for every $\Delta t > 0$.

*Proof.* With one constraint, Gauss-Seidel solves the $1 \times 1$ system in one update. Directly: $\lambda = -(y - r)/(w + \tilde\alpha)$ with $w = 1/m$, and $x^{n+1} = y + w\lambda = y - \frac{y - r}{1 + m\alpha/\Delta t^2} = y - \frac{\Delta t^2 k (y - r)}{\Delta t^2 k + m}$, which is the formula. The backward Euler equation $m(x - y)/\Delta t^2 = -k(x - r)$ has the same solution. $\square$

In particular the stiffness of a spring in XPBD is $k = 1/\alpha$ for every $\Delta t$ and every number of sweeps once the sweeps have converged. With few sweeps the result is softer, since the sweeps stop early.

## Zero compliance and momentum

**Lemma 6.** If $\alpha_j = 0$, line L6 is the PBD projection with the sweep stiffness $1$.

*Proof.* With $\tilde\alpha_j = 0$ the term $\tilde\alpha_j\lambda_j$ vanishes and $\Delta\lambda_j = -C_j(\mathbf p)/\sum_i w_i|\nabla_i C_j|^2$, which is $-s$ in the notation of the PBD page. Then $\Delta\mathbf p_i = -s\, w_i\nabla_i C_j$. $\square$

**Theorem 7 (linear momentum).** Let every $C_j$ be invariant under a common translation of its particles, let no particle be pinned and let $\mathbf g = 0$. Then $\sum_i m_i \mathbf v_i^{n+1} = \sum_i m_i \mathbf v_i^n$.

*Proof.* Translation invariance gives $\sum_i \nabla_i C_j = 0$, so each update changes $\sum_i m_i \mathbf p_i$ by $\Delta\lambda_j\sum_i \nabla_i C_j = 0$. Hence $\sum m_i \mathbf p_i = \sum m_i(\mathbf x_i^n + \Delta t \mathbf v_i^n)$ at the end of the sweeps, and line L9 gives the claim. $\square$

Angular momentum is not kept in general. Each update is torque-free about the current $\mathbf p$, as in Lemma 4 of the PBD proof, but the velocity of line L9 is measured from $\mathbf x^n$. The two-particle counterexample of Theorem 7 there applies without change when $\alpha = 0$.

**Lemma 8.** With no constraints, one step is the symplectic Euler step $\mathbf v^{n+1} = \mathbf v^n + \Delta t\mathbf g$, $\mathbf x^{n+1} = \mathbf x^n + \Delta t\mathbf v^{n+1}$.

*Proof.* Line L1 computes $\mathbf x^n + \Delta t(\mathbf v^n + \Delta t\mathbf g)$, nothing changes it, and line L9 returns $\mathbf v^n + \Delta t\mathbf g$. $\square$

## Cost

**Lemma 9.** A step with $k$ sweeps over $c$ distance constraints on $n$ particles costs $\Theta(n + kc)$ time and $\Theta(n + c)$ memory.

*Proof.* Lines L1, L3 and L9 touch each particle once. Each constraint update in lines L6 to L8 does a constant amount of work for a constraint on two particles. The state is $\mathbf p$, the velocities and one multiplier per constraint. $\square$
