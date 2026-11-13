---
title: The semi-implicit snake step decreases the energy when the step is small enough
proves: [correctness]
status: full
---

Write the curve as the vector $z = (x, y) \in \mathbb{R}^{2n}$. Let $L$ be the circulant matrix of the cycle with the row $(-1, 2, -1)$, and $A = \alpha L + \beta L^2$ with $\alpha, \beta \ge 0$. Let $F(z) = \sum_i P(x_i, y_i)$, the image energy.

**Lemma 1 (the internal energy is a quadratic form).** $\sum_i \tfrac{\alpha}{2} |v_{i+1} - v_i|^2 + \tfrac{\beta}{2} |v_{i+1} - 2 v_i + v_{i-1}|^2 = Q(z)$ with $Q(z) = \tfrac{1}{2} x^T A x + \tfrac{1}{2} y^T A y$, and $A$ is symmetric and positive semidefinite.

*Proof.* Let $D$ be the circulant difference matrix with $(D x)_i = x_{i+1} - x_i$. Then $D^T D = L$, so $\sum_i (x_{i+1} - x_i)^2 = |D x|^2 = x^T L x$. The second difference is $(L x)_i = -(x_{i+1} - 2 x_i + x_{i-1})$, so $\sum_i (x_{i+1} - 2x_i + x_{i-1})^2 = |L x|^2 = x^T L^2 x$, because $L$ is symmetric. The same holds for $y$, and the two coordinates add. $L = D^T D$ and $L^2 = L^T L$ are positive semidefinite, and so is a combination with weights that are not negative. $\square$

So $E(z) = Q(z) + F(z)$, and $\nabla Q(z) = (A x, A y)$, which we write $\mathbf{A} z$, with $\mathbf{A}$ the block diagonal matrix with two copies of $A$.

**Lemma 2 (the step is a minimization).** Lines L5 and L6 compute $z' = (x', y')$, the unique minimizer of

$$\Phi(u) = Q(u) + \langle \nabla F(z), u - z \rangle + \frac{\gamma}{2} |u - z|^2.$$

*Proof.* $\Phi$ is a quadratic function with the Hessian $\mathbf{A} + \gamma I$, which is positive definite because $\mathbf{A}$ is positive semidefinite and $\gamma > 0$. So $\Phi$ has exactly one minimizer, the zero of the gradient: $\mathbf{A} u + \nabla F(z) + \gamma (u - z) = 0$, that is $(A + \gamma I)\, x' = \gamma x - P_x$ and $(A + \gamma I)\, y' = \gamma y - P_y$, where $P_x$ and $P_y$ are the vectors of the partial derivatives of $P$ at the points of $z$. Line L2 factors $A + \gamma I = C C^T$, which exists because the matrix is positive definite, and lines L5 and L6 solve these two systems. $\square$

**Theorem (decrease of the energy).** Let $\nabla P$ be Lipschitz with the constant $\Lambda$, that is $|\nabla P(p) - \nabla P(q)| \le \Lambda |p - q|$ for all points $p$ and $q$ of the plane. Then each step from $z$ to $z'$ satisfies

$$E(z') \le E(z) - \left(\gamma - \frac{\Lambda}{2}\right) |z' - z|^2.$$

*Proof.* The gradient of $F$ is the list of the gradients of $P$ at the $n$ points, so $|\nabla F(z) - \nabla F(u)|^2 = \sum_i |\nabla P(v_i) - \nabla P(u_i)|^2 \le \Lambda^2 |z - u|^2$, and $\nabla F$ is Lipschitz with the constant $\Lambda$. The descent lemma for such a function gives

$$F(z') \le F(z) + \langle \nabla F(z), z' - z \rangle + \frac{\Lambda}{2} |z' - z|^2.$$

$\Phi$ is strongly convex with modulus at least $\gamma$, because its Hessian is at least $\gamma I$, and $z'$ is its minimizer, so $\Phi(z) \ge \Phi(z') + \tfrac{\gamma}{2} |z - z'|^2$. With $\Phi(z) = Q(z)$, this is

$$Q(z') + \langle \nabla F(z), z' - z \rangle + \frac{\gamma}{2} |z' - z|^2 + \frac{\gamma}{2} |z' - z|^2 \le Q(z).$$

Add the two inequalities and cancel the inner product: $Q(z') + F(z') \le Q(z) + F(z) - \gamma |z' - z|^2 + \tfrac{\Lambda}{2} |z' - z|^2$. $\blacksquare$

**Corollary (convergence to stationary points).** Let $\gamma > \Lambda / 2$, and let $P$ be bounded below. Then $E(z^{(t)})$ decreases and converges, $\sum_t |z^{(t+1)} - z^{(t)}|^2$ is finite, so $|z^{(t+1)} - z^{(t)}| \to 0$, and every limit point $z^*$ of the iterates has $\nabla E(z^*) = 0$.

*Proof.* $Q \ge 0$ and $F \ge n \inf P$, so $E$ is bounded below, and a decreasing sequence that is bounded below converges. Summing the theorem over the steps bounds $(\gamma - \Lambda/2) \sum_t |z^{(t+1)} - z^{(t)}|^2$ by $E(z^{(0)}) - \inf E$. The map $T$ from $z$ to $z'$ is continuous, because $\nabla F$ is continuous and the solve is linear. If $z^{(t)} \to z^*$ along a subsequence, then $T(z^{(t)}) \to T(z^*)$ along it, and $|T(z^{(t)}) - z^{(t)}| \to 0$, so $T(z^*) = z^*$. By Lemma 2, a fixed point satisfies $\mathbf{A} z^* + \nabla F(z^*) = 0$, which is $\nabla E(z^*) = 0$. $\square$

The corollary does not say that $z^*$ is a minimum, and not that it is the boundary of an object. $E$ is not convex, and different starts can converge to different stationary points, as the test with two disks shows.

**Lemma 3 (the constant for the spline potential).** Let $P(x, y) = -w \sum_{i, j} S_{ij}\, b(x - i)\, b(y - j)$, with $b$ the cubic B-spline, $w > 0$ and $|S_{ij}| \le M$. Then $\nabla P$ is Lipschitz with the constant $6.25\, w M$.

*Proof.* On $|u| < 1$, $b(u) = \tfrac{2}{3} - u^2 + \tfrac{1}{2}|u|^3$, on $1 \le |u| < 2$, $b(u) = \tfrac{1}{6}(2 - |u|)^3$, and $b = 0$ elsewhere. So $b \ge 0$, $b$ has two continuous derivatives, $\sum_i b(t - i) = 1$, and for $t \in [0, 1)$ only the four terms with $t - i \in \{t + 1, t, t - 1, t - 2\}$ are not zero. From the formulas, $b''(u) = -2 + 3|u|$ on $|u| < 1$ and $b''(u) = 2 - |u|$ on $1 \le |u| < 2$, so

$$\sum_i |b''(t - i)| = (1 - t) + |3t - 2| + |1 - 3t| + t = 1 + |3t - 2| + |3t - 1|,$$

a convex function of $t$ whose maximum on $[0, 1]$ is 4, at $t = 0$ and $t = 1$. In the same way, with $b'(u) = \operatorname{sign}(u)(-2|u| + \tfrac{3}{2} u^2)$ on $|u| < 1$ and $b'(u) = -\operatorname{sign}(u)\tfrac{1}{2}(2 - |u|)^2$ on $1 \le |u| < 2$,

$$\sum_i |b'(t - i)| = \tfrac{1}{2}(1 - t)^2 + (2t - \tfrac{3}{2}t^2) + (2(1 - t) - \tfrac{3}{2}(1 - t)^2) + \tfrac{1}{2}t^2 = 2 - t^2 - (1 - t)^2,$$

whose maximum on $[0, 1]$ is $\tfrac{3}{2}$, at $t = \tfrac{1}{2}$. Both sums are periodic in $t$ with period 1, so the bounds hold for every real $t$.

The Hessian of $P$ exists and is continuous everywhere. Its entries are bounded by

$$|P_{xx}| \le w M \sum_i |b''(x - i)| \sum_j b(y - j) \le 4 w M, \qquad |P_{yy}| \le 4 w M, \qquad |P_{xy}| \le w M \sum_i |b'(x - i)| \sum_j |b'(y - j)| \le 2.25\, w M.$$

By the theorem of Gershgorin, the eigenvalues of the symmetric Hessian are at most $4 w M + 2.25\, w M = 6.25\, w M$ in absolute value, so its operator norm is at most $6.25\, w M$. A function whose Hessian has norm at most $\Lambda$ everywhere has a gradient that is Lipschitz with the constant $\Lambda$, by the mean value theorem along the segment from $p$ to $q$. $\square$

The edge strength of the implementation has $M = 1$, so with $w = 1$ the step needs $\gamma > 3.125$, and the test of the disk uses $\gamma = 3.5$. The clamped reads of $S$ outside the grid are values of $S$, so the bound $M$ still holds.

**Remark (the circle without an image).** With $P = 0$, a circle $v_k = c + \rho (\cos(2\pi k/n), \sin(2\pi k/n))$ gives vectors $x - c_x$ and $y - c_y$ in the eigenspace of $L$ for $\mu = 2 - 2\cos(2\pi/n)$, and the constant vectors are in the kernel of $A$. So the step maps the circle to the circle with the same center and the radius $\rho\, \gamma / (\gamma + \alpha\mu + \beta\mu^2)$, which the test checks to 12 decimal places.
