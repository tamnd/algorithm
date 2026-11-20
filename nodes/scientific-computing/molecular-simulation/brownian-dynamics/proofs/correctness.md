---
title: The Ermak-McCammon step is the Euler-Maruyama step of an equation whose stationary law is the Boltzmann density
proves: [correctness]
status: full
---

Let $x \in \mathbb{R}^{n}$ hold all coordinates ($n = N d$), $f = -\nabla U$, and let $D(x)$ be a symmetric positive definite $n \times n$ diffusion matrix. The overdamped Langevin equation in the Ito form is
$$dx = \frac{1}{k_B T} D(x) f(x)\,dt + (\nabla \cdot D)(x)\,dt + \sqrt{2}\,L(x)\,dW, \qquad L L^{\mathsf T} = D, \qquad (1)$$
with $(\nabla \cdot D)_a = \sum_b \partial_b D_{ab}$.

**Claim 1 (the Boltzmann density is stationary).** $\rho(x) \propto e^{-\beta U(x)}$ is a stationary solution of the Fokker-Planck equation of (1), and its probability flux is 0.

*Proof.* For $dx = b\,dt + \sigma\,dW$ the Fokker-Planck equation is $\partial_t \rho = -\nabla \cdot J$ with $J_a = b_a \rho - \sum_b \partial_b \bigl( \frac12 (\sigma\sigma^{\mathsf T})_{ab} \rho \bigr)$. Here $\frac12 \sigma\sigma^{\mathsf T} = D$, so
$$J_a = \frac{(Df)_a}{k_B T}\rho + (\nabla \cdot D)_a \rho - (\nabla \cdot D)_a \rho - \sum_b D_{ab} \partial_b \rho = \sum_b D_{ab} \Bigl( \frac{f_b}{k_B T}\rho - \partial_b \rho \Bigr).$$
For $\rho \propto e^{-\beta U}$, $\partial_b \rho = \beta f_b \rho$, so $J = 0$. $\square$

The term $\nabla \cdot D$ is needed for this: without it the flux has the extra part $-(\nabla \cdot D)\rho$, and the stationary law is wrong.

**Claim 2 (the step).** If $\nabla \cdot D = 0$, then lines L3 to L6 are the Euler-Maruyama step of (1):
$$x' = x + \frac{h}{k_B T} D(x) f(x) + \sqrt{2h}\,L(x) R, \qquad R \sim N(0, I).$$
The noise term has the covariance $2hD(x)$. For a scalar diffusion coefficient $D_i$ per particle, $L$ is diagonal with entries $\sqrt{D_i}$, and line L6 adds $\sqrt{2 D_i h}$ times a standard normal to each coordinate.

*Proof.* Line L4 computes the Cholesky factor $L$ of $D$, line L5 draws $R$, and line L6 adds the drift and $\sqrt{2h} L R$. The covariance is $2h\,\mathbb{E}[L R R^{\mathsf T} L^{\mathsf T}] = 2h L L^{\mathsf T} = 2h D$. $\square$

$D$ constant gives $\nabla \cdot D = 0$. The [Euler-Maruyama method](/euler-maruyama-method/) has weak order 1, so averages over the sampled law differ from Boltzmann averages by $O(h)$. Claim 5 gives this error in a case we can solve.

**Claim 3 (the Rotne-Prager-Yamakawa tensor has zero divergence).** For spheres of radius $a$ in three dimensions, with the blocks used by the implementation, $\nabla \cdot D = 0$ in both regions $r \ge 2a$ and $r < 2a$.

*Proof.* The diagonal blocks are the constant $D_0 I$ with $D_0 = k_B T / (6\pi\eta a)$. An off-diagonal block $T(r)$ depends on $r = x_i - x_j$, so its contribution to $(\nabla \cdot D)_i$ is $\pm \sum_b \partial_b T_{ab}(r)$, and it is enough to show $\sum_b \partial_b T_{ab} = 0$. Write $r = |r|$.

For $r \ge 2a$,
$$T = \frac{k_B T}{8\pi\eta} \Bigl( \frac{\delta_{ab}}{r} + \frac{r_a r_b}{r^3} \Bigr) + \frac{k_B T\,a^2}{12\pi\eta} \Bigl( \frac{\delta_{ab}}{r^3} - \frac{3 r_a r_b}{r^5} \Bigr).$$
For the first bracket, $\partial_b(\delta_{ab}/r) = -r_a/r^3$ and $\partial_b(r_a r_b / r^3) = r_a/r^3 + 3r_a/r^3 - 3r_a/r^3 = r_a/r^3$, with sum 0. The second bracket is $-\partial_a\partial_b (1/r)$, and its divergence is $-\partial_a \nabla^2(1/r) = 0$ for $r \ne 0$.

For $r < 2a$, $T = D_0 \bigl( (1 - \frac{9r}{32a})\delta_{ab} + \frac{3}{32a} \frac{r_a r_b}{r} \bigr)$. Here $\partial_b\bigl((1 - \frac{9r}{32a})\delta_{ab}\bigr) = -\frac{9 r_a}{32 a r}$ and $\partial_b (r_a r_b / r) = r_a/r + 3r_a/r - r_a/r = 3r_a/r$, so the sum is $-\frac{9r_a}{32ar} + \frac{9 r_a}{32ar} = 0$. $\square$

So the step of Claim 2 is the Euler-Maruyama step of (1) also for the Rotne-Prager-Yamakawa tensor, with no divergence term to add. The tensor is positive definite for all configurations, which is the reason it is used in place of the Oseen tensor (the first bracket alone), so the Cholesky factor in line L4 exists. The two forms agree at $r = 2a$, where both give $D_0 \bigl(\frac{7}{16}\delta_{ab} + \frac{3}{16} e_a e_b\bigr)$ with $e = r/|r|$, and the diagonal blocks give the Stokes-Einstein value $D_0$.

**Claim 4 (free particles and a constant force).** With a constant scalar $D$ and a constant force $g$ on each particle, the displacement after $n$ steps is normal with mean $n h D g / (k_B T)$ and covariance $2 n h D\,I$, for every $h$. So for $g = 0$ the mean squared displacement in $d$ dimensions is exactly $2 d D t$ at $t = nh$.

*Proof.* Each step adds $h D g/(k_B T)$ and an independent normal with covariance $2hD\,I$. $\square$

**Claim 5 (the harmonic well).** For $U = \frac12 k x^2$ with a scalar $D$, let $c = hDk/(k_B T)$ with $0 < c < 2$. The stationary variance of the chain is
$$\langle x^2 \rangle = \frac{k_B T}{k} \, \frac{1}{1 - c/2}.$$

*Proof.* The step is $x' = (1 - c)x + \sqrt{2Dh}\,R$. A stationary variance $s$ satisfies $s = (1 - c)^2 s + 2Dh$, so $s = 2Dh / (c(2 - c)) = \frac{k_B T}{k} \cdot \frac{2}{2 - c}$. For $0 < c < 2$, $|1 - c| < 1$, so the chain converges to this law from any start. $\square$

The right value is $k_B T/k$; the relative error is $c/2 + O(c^2)$, of order $h$ as Claim 2 says. The step is unstable for $c \ge 2$, so $h$ must be small compared with $k_B T / (D k)$ for the stiffest force.
