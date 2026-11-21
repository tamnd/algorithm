---
title: RTO-MH stops after the given number of steps, its proposal has the stated density, and the chain leaves the posterior invariant
proves: [correctness, termination]
status: full
---

**Setting.** $F: \mathbb{R}^n \to \mathbb{R}^M$ with $M \ge n$ is continuously differentiable with Jacobian $J(x)$, $\bar y \in \mathbb{R}^M$, and the target density is

$$\pi(x) = \frac1Z\exp\big(-\tfrac12\lVert F(x) - \bar y\rVert^2\big).$$

For a Gaussian prior $N(m_0, C)$ with $L^TL = C^{-1}$ and noise $N(0, \Gamma)$, $F(x) = [\Gamma^{-1/2}G(x); L(x - m_0)]$ and $\bar y = [\Gamma^{-1/2}y; 0]$ give the posterior. $Q$ is an $M \times n$ matrix with orthonormal columns (line L2). Write $T(x) = Q^TF(x)$, so $T'(x) = Q^TJ(x)$.

**Assumption (A).** $T$ is one-to-one on $\mathbb{R}^n$, $\det T'(x) \ne 0$ for all $x$, and whenever $Q^T(\bar y + \varepsilon)$ lies in the image $T(\mathbb{R}^n)$ the solver of line L6 returns the solution $x' = T^{-1}(Q^T(\bar y + \varepsilon))$. When the target is not in the image, line L6 returns no point.

**Claim 1 (termination).** For $N \ge 1$ the procedure stops and returns a chain of $N$ states and an acceptance rate in $[0, 1]$.

*Proof.* The Gauss-Newton loop of line L1 has at most a fixed number of outer steps (100 in the code), and each step halves its step length at most 34 times before it stops. The Gram-Schmidt step of line L2 has $n$ columns. The Newton solver of line L6 has at most a fixed number of steps (50). The loop of line L4 has $N$ passes, and each appends one state in line L9. $\square$

**Claim 2 (the proposal density).** Under (A), the points returned by line L6 have the sub-probability density

$$q(x) = (2\pi)^{-n/2}\,\lvert\det(Q^TJ(x))\rvert\,\exp\big(-\tfrac12\lVert Q^T(F(x) - \bar y)\rVert^2\big), \qquad x \in \mathbb{R}^n,$$

and the remaining mass $1 - \int q$ is the probability that line L6 returns no point.

*Proof.* Let $\varepsilon \sim N(0, I_M)$. Then $z = Q^T(\bar y + \varepsilon)$ is Gaussian with mean $Q^T\bar y$ and covariance $Q^TQ = I_n$, so it has density $(2\pi)^{-n/2}\exp(-\frac12\lVert z - Q^T\bar y\rVert^2)$. By (A), line L6 returns $x' = T^{-1}(z)$ exactly when $z \in T(\mathbb{R}^n)$. $T$ is a $C^1$ bijection from $\mathbb{R}^n$ onto the open set $T(\mathbb{R}^n)$ with nonsingular derivative, so by the change of variables formula $x'$ has density $(2\pi)^{-n/2}\exp(-\frac12\lVert T(x) - Q^T\bar y\rVert^2)\lvert\det T'(x)\rvert$ on $\mathbb{R}^n$. Since $T(x) - Q^T\bar y = Q^T(F(x) - \bar y)$, this is $q$. $\square$

**Claim 3 (the weight).** The ratio $\pi/q$ is, up to a constant factor,

$$w(x) = \lvert\det(Q^TJ(x))\rvert^{-1}\exp\big(-\tfrac12\lVert F(x) - \bar y\rVert^2 + \tfrac12\lVert Q^T(F(x) - \bar y)\rVert^2\big),$$

and line L7 computes $\log w(x')$.

*Proof.* Divide $\pi$ by $q$ from Claim 2 and drop the constant $(2\pi)^{n/2}/Z$. The function `log_weight` computes the three terms of $\log w$ directly. $\square$

**Claim 4 (detailed balance).** Under (A), one pass of lines L5 to L9 has the kernel

$$P(x, dx') = q(x')\,a(x, x')\,dx' + r(x)\,\delta_x(dx'), \qquad a(x, x') = \min\{1, w(x')/w(x)\},$$

where $r(x)$ collects the rejections and the failed solves, and $\pi(x)P(x, dx') = \pi(x')P(x', dx)$. So $\pi$ is invariant.

*Proof.* Line L8 accepts with probability $\min\{1, w(x')/w(x)\}$: as in Metropolis-Hastings, with $U$ uniform on $(0, 1]$, the event $\log U < \log w(x') - \log w(x)$ has this probability. If line L6 returns no point, the state stays. For the moving part, using $\pi = cwq$ for a constant $c > 0$,

$$\pi(x)q(x')a(x, x') = c\,w(x)q(x)q(x')\min\{1, w(x')/w(x)\} = c\,q(x)q(x')\min\{w(x), w(x')\},$$

which is symmetric in $(x, x')$. The staying part is concentrated on $x = x'$ and is symmetric too. Integrate over $x$ to get invariance. $\square$

This is the independence Metropolis-Hastings sampler with proposal $q$. Under (A), $q(x) > 0$ for every $x$, also when its total mass is below one, and $w$ is finite and positive. So every set of positive $\pi$-measure is reached in one step with positive probability, the chain is $\pi$-irreducible, and averages along the chain converge to posterior expectations for $\pi$-almost every start (the standard law of large numbers for Markov chains).

**Claim 5 (the linear case is exact without correction).** Let $F(x) = Hx - h_0$ be affine with $H$ of full column rank $n$, and let the columns of $Q$ span the range of $H$. Then (A) holds, $w$ is constant, every proposal is accepted, and the proposals are independent draws from $\pi$, which is $N((H^TH)^{-1}H^T(\bar y + h_0), (H^TH)^{-1})$.

*Proof.* Write $H = QR$ with $R = Q^TH$ invertible. Then $T(x) = Rx - Q^Th_0$ is an affine bijection, so (A) holds, and Newton's method solves it in one step. The determinant $\det(Q^TJ) = \det R$ is constant. With $d(x) = Hx - h_0 - \bar y$,

$$\lVert d(x)\rVert^2 - \lVert Q^Td(x)\rVert^2 = \lVert(I - QQ^T)d(x)\rVert^2 = \lVert(I - QQ^T)(h_0 + \bar y)\rVert^2,$$

since $(I - QQ^T)H = 0$. So $w$ is constant and the ratio in line L8 is $1$. The equation $Rx = Q^T(\bar y + h_0 + \varepsilon)$ is equivalent to the normal equations $H^THx = H^T(\bar y + h_0 + \varepsilon)$, because $H^T = R^TQ^T$ and $R^T$ is invertible. So $x$ is the least squares solution of the perturbed problem, a Gaussian vector with mean $(H^TH)^{-1}H^T(\bar y + h_0)$ and covariance $(H^TH)^{-1}H^TH(H^TH)^{-1} = (H^TH)^{-1}$, which are the mean and covariance of $\pi \propto \exp(-\frac12\lVert Hx - h_0 - \bar y\rVert^2)$. $\square$

The choice of $Q$ at the MAP point in line L1 is not needed for correctness: any $Q$ with orthonormal columns for which (A) holds gives an exact chain. It matters for efficiency, since it makes $q$ close to $\pi$ near the mode. Assumption (A) is a real restriction. If $T$ is not one-to-one or the solver misses solutions, the weight of Claim 3 is wrong and the chain is biased; the page lists this as a pitfall.
