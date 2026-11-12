---
title: GTD2 and TDC follow the gradient of the MSPBE and their mean dynamics converge to the TD fixed point
proves: [correctness]
status: partial
---

We use the notation of the page. Samples $(x, \rho, r, x')$ are drawn with $x = \phi(s)$, $s \sim d$, the action from $\mu$, $\rho = \pi(a \mid s)/\mu(a \mid s)$ and $x' = \phi(s')$. Let

$$A = \mathbb{E}[\rho\,x(x - \gamma x')^\top], \qquad b = \mathbb{E}[\rho\,r\,x], \qquad C = \mathbb{E}[x x^\top], \qquad E = \mathbb{E}[\rho\,x' x^\top].$$

Assume that $A$ and $C$ are invertible. The status is partial: we prove the facts about the mean dynamics, and we cite Sutton et al. (2009) and Borkar (2008) for the step from the mean dynamics to convergence with probability one.

**Lemma 1 (the objective).** Let $\Phi$ have rows $\phi(s)$, $D = \operatorname{diag}(d)$, $\Pi = \Phi(\Phi^\top D\Phi)^{-1}\Phi^\top D$, and let $T$ be the Bellman operator of $\pi$. Then

$$\mathrm{MSPBE}(\theta) = \lVert\Pi(T\Phi\theta - \Phi\theta)\rVert_D^2 = (b - A\theta)^\top C^{-1}(b - A\theta).$$

*Proof.* For a fixed state and action, $\mathbb{E}_\mu[\rho f(a)] = \sum_a \mu(a \mid s)\frac{\pi(a \mid s)}{\mu(a \mid s)}f(a) = \mathbb{E}_\pi[f(a)]$. So $\mathbb{E}[\rho\delta x] = \sum_s d(s)\phi(s)\bigl((T\Phi\theta)(s) - (\Phi\theta)(s)\bigr) = \Phi^\top D(T\Phi\theta - \Phi\theta)$, and $\mathbb{E}[\rho\delta x] = b - A\theta$ by the definition of $\delta$. Also $C = \Phi^\top D\Phi$. For any vector $u$, $\lVert\Pi u\rVert_D^2 = u^\top\Pi^\top D\Pi u$, and $\Pi^\top D\Pi = D\Phi C^{-1}\Phi^\top D\Phi C^{-1}\Phi^\top D = D\Phi C^{-1}\Phi^\top D$. With $u = T\Phi\theta - \Phi\theta$ this gives $(\Phi^\top Du)^\top C^{-1}(\Phi^\top Du) = (b - A\theta)^\top C^{-1}(b - A\theta)$. $\square$

Because $C$ is positive definite, $\mathrm{MSPBE}(\theta) = 0$ exactly when $A\theta = b$. So the minimum of the MSPBE is the TD fixed point $\theta^* = A^{-1}b$.

**Lemma 2 (the gradient).** $-\tfrac{1}{2}\nabla\mathrm{MSPBE}(\theta) = A^\top C^{-1}(b - A\theta) = (b - A\theta) - \gamma E\,C^{-1}(b - A\theta)$.

*Proof.* The first equation is the gradient of a quadratic form with the symmetric matrix $C^{-1}$. For the second, $A^\top = \mathbb{E}[\rho(x - \gamma x')x^\top] = \mathbb{E}[\rho x x^\top] - \gamma E$, and $\mathbb{E}[\rho x x^\top] = \mathbb{E}[x x^\top] = C$ because $\mathbb{E}_\mu[\rho \mid s] = 1$. So $A^\top C^{-1} = I - \gamma E C^{-1}$. $\square$

Let $w^*(\theta) = C^{-1}(b - A\theta)$, the least-squares solution of $x^\top w \approx \mathbb{E}[\rho\delta \mid x]$. The mean of line L7 is $\beta\bigl((b - A\theta) - Cw\bigr)$, which is zero at $w = w^*(\theta)$. With $w = w^*(\theta)$, the mean of line L6 (GTD2) is $\alpha\,\mathbb{E}[\rho(x - \gamma x')x^\top]w = \alpha A^\top w^*(\theta)$, and the mean of line L5 (TDC) is $\alpha\bigl((b - A\theta) - \gamma E w^*(\theta)\bigr)$. By Lemma 2 both equal $-\tfrac{\alpha}{2}\nabla\mathrm{MSPBE}(\theta)$.

**Theorem 1 (the only rest point).** For both methods, the mean update of $(\theta, w)$ is zero exactly at $(\theta^*, 0)$.

*Proof.* The $w$ update is zero when $Cw = b - A\theta$. For GTD2 the $\theta$ update is zero when $A^\top w = 0$, so $w = 0$ since $A$ is invertible, and then $A\theta = b$. For TDC it is zero when $(b - A\theta) - \gamma Ew = 0$; with $b - A\theta = Cw$ this is $(C - \gamma E)w = A^\top w = 0$, so again $w = 0$ and $A\theta = b$. Conversely, at $(\theta^*, 0)$ every term vanishes. $\square$

**Theorem 2 (GTD2 on one time scale).** Let $\beta = \eta\alpha$ with $\eta > 0$. The mean ODE $\dot{\theta} = A^\top w$, $\dot{w} = \eta(b - A\theta - Cw)$ has $(\theta^*, 0)$ as a globally asymptotically stable equilibrium.

*Proof.* Shift to $u = \theta - \theta^*$. The ODE is linear, $\dot{z} = Gz$ with $z = (u, w)$ and $G = \begin{pmatrix} 0 & A^\top \\ -\eta A & -\eta C\end{pmatrix}$. Let $\lambda$ be an eigenvalue with eigenvector $(u, v) \ne 0$, so $A^\top v = \lambda u$ and $-\eta Au - \eta Cv = \lambda v$. If $v = 0$, then $Au = 0$, so $u = 0$, which is impossible. So $v \ne 0$; scale it so that $v^* v = 1$. If $\lambda = 0$, then $A^\top v = 0$ gives $v = 0$, a contradiction. So $\lambda \ne 0$ and $u = A^\top v/\lambda$. Multiply the second equation on the left by $v^*$:

$$-\frac{\eta}{\lambda}\lVert A^\top v\rVert^2 - \eta\,v^* C v = \lambda, \quad\text{so}\quad \lambda^2 + \eta c\lambda + \eta a = 0,$$

with $a = \lVert A^\top v\rVert^2 > 0$ and $c = v^* Cv > 0$, both real. A quadratic $\lambda^2 + p\lambda + q$ with $p, q > 0$ has both roots in the open left half plane: if the roots are real, they are both negative because their sum is $-p < 0$ and their product is $q > 0$; if they are complex, their real part is $-p/2 < 0$. So every eigenvalue of $G$ has a negative real part, and $z(t) \to 0$ from every start. $\blacksquare$

**Theorem 3 (TDC on two time scales).** Let $\alpha_k/\beta_k \to 0$. On the fast time scale $\theta$ is frozen and $\dot{w} = b - A\theta - Cw$ has the globally stable rest point $w^*(\theta)$, because $C$ is positive definite. On the slow time scale the mean dynamics are $\dot{\theta} = (b - A\theta) - \gamma E w^*(\theta) = A^\top C^{-1}(b - A\theta)$. The matrix $A^\top C^{-1}A$ is symmetric and positive definite because $A$ is invertible, so $\theta^*$ is the globally asymptotically stable rest point.

*Proof.* The two statements about the ODEs are the computations above, together with the facts that $\dot{w} = -C(w - w^*)$ and $\dot{u} = -A^\top C^{-1}Au$ for $u = \theta - \theta^*$ are stable linear systems. The two time scale theorem of stochastic approximation (Borkar 2008, Chapter 6) then gives $\theta_k \to \theta^*$ with probability one, under the step conditions of the page, i.i.d. samples with bounded second moments, and bounded iterates. This is Theorem 2 of Sutton et al. (2009). $\blacksquare$

**Remark (why semi-gradient TD can fail).** Semi-gradient TD has the mean ODE $\dot{\theta} = b - A\theta$. On-policy, $d$ is the stationary distribution and $A$ is positive definite, so it is stable. Off-policy, $A$ can have an eigenvalue with negative real part, and then $\theta$ diverges from almost every start, as in Baird's counterexample. The matrix of GTD2 and the matrix $-A^\top C^{-1}A$ of TDC are stable for every invertible $A$, which is why these methods converge off-policy.
