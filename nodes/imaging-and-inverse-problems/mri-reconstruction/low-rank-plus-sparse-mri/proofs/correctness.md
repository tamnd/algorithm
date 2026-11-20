---
title: L+S is proximal gradient on a convex objective, with sufficient decrease for small steps
proves: [correctness]
status: full
---

The setting is that of the algorithm. A series is an $n \times n_t$ complex Casorati matrix with one column per frame, where $n$ is the number of pixels. The inner product of two series is $\langle X, Y \rangle = \operatorname{Re} \operatorname{tr}(X^H Y)$, and $\|\cdot\|$ is the Frobenius norm. The encoding operator $E$ maps frame $t$ and coil $j$ to $M_t F_u (c_j x_t)$, with a 0/1 mask $M_t$, the unitary 2D DFT $F_u$ and coil maps $c_j$. The transform $T$ is the unitary DFT along time at each pixel. The objective is

$$F(L, S) = f(L, S) + \lambda_L \|L\|_* + \lambda_S \|T S\|_1, \qquad f(L, S) = \tfrac12 \|E(L + S) - d\|^2,$$

with $\lambda_L, \lambda_S \ge 0$. Each term is convex, so $F$ is convex.

## 1. The norm of the encoding operator

**Lemma 1.** If $\sum_j |c_j(p)|^2 \le 1$ at every pixel $p$, then $\|E\| \le 1$. With one coil, $c = 1$ and full masks, $E^H E = I$.

*Proof.* $M_t$ is an orthogonal projection and $F_u$ is unitary, so $\|M_t F_u (c_j x_t)\| \le \|c_j x_t\|$. Summing over $j$ and $t$ gives $\|E X\|^2 \le \sum_t \sum_p \sum_j |c_j(p)|^2 |x_t(p)|^2 \le \|X\|^2$. With one coil $c = 1$ and $M_t = I$, $E^H E = F_u^H F_u = I$ frame by frame. $\square$

## 2. The two proximal maps

The proximal map of a convex function $h$ is $\operatorname{prox}_h(Z) = \arg\min_X \tfrac12 \|X - Z\|^2 + h(X)$. It exists and is unique because the objective is strongly convex.

**Lemma 2 (singular value thresholding).** Let $Z = U \Sigma V^H$ be an SVD with singular values $\sigma_i$, and $\tau \ge 0$. Then

$$\operatorname{prox}_{\tau \|\cdot\|_*}(Z) = U \operatorname{diag}(\max(\sigma_i - \tau, 0)) V^H = Z\, V \operatorname{diag}(\max(1 - \tau/\sigma_i, 0)) V^H,$$

where a term with $\sigma_i = 0$ is 0.

*Proof.* Let $X$ have the singular values $s_1 \ge s_2 \ge \cdots$. Von Neumann's trace inequality gives $\operatorname{Re} \operatorname{tr}(X^H Z) \le \sum_i s_i \sigma_i$, so

$$\tfrac12 \|X - Z\|^2 + \tau \|X\|_* \ge \sum_i \Big( \tfrac12 (s_i - \sigma_i)^2 + \tau s_i \Big).$$

Each term on the right is a scalar function of $s_i \ge 0$ with its minimum at $s_i = \max(\sigma_i - \tau, 0)$. The matrix $X = U \operatorname{diag}(\max(\sigma_i - \tau, 0)) V^H$ has these singular values and gives equality in the trace inequality, because it shares the singular vectors of $Z$. So it attains the lower bound, and by uniqueness it is the proximal point. For the second form, $Z V = U \Sigma$, so $Z V \operatorname{diag}(g_i) V^H = U \operatorname{diag}(\sigma_i g_i) V^H$, and $\sigma_i \max(1 - \tau/\sigma_i, 0) = \max(\sigma_i - \tau, 0)$ for $\sigma_i > 0$. $\square$

The code forms $V \operatorname{diag}(g(\sigma_i^2)) V^H$ from the $n_t \times n_t$ Gram matrix $G = Z^H Z = V \Sigma^2 V^H$. It uses the real symmetric matrix $\Phi(G) = \begin{pmatrix} \operatorname{Re} G & -\operatorname{Im} G \\ \operatorname{Im} G & \operatorname{Re} G \end{pmatrix}$. If $G v = \mu v$, then $(\operatorname{Re} v, \operatorname{Im} v)$ and $(-\operatorname{Im} v, \operatorname{Re} v)$ are orthogonal eigenvectors of $\Phi(G)$ for $\mu$. So every eigenvalue of $G$ appears twice, and $\sum_q g(\mu_q)\, q q^T = \Phi\big(V \operatorname{diag}(g(\sigma_i^2)) V^H\big)$, summed over an orthonormal eigenbasis of $\Phi(G)$. The complex matrix is the top left block plus $i$ times the bottom left block. This holds for any orthonormal eigenbasis, also when eigenvalues repeat, because the sum depends only on the eigenspaces.

**Lemma 3 (soft thresholding in a unitary transform).** For a unitary $T$ and $\tau \ge 0$,

$$\operatorname{prox}_{\tau \|T \cdot\|_1}(Z) = T^H \Lambda_\tau(T Z), \qquad \Lambda_\tau(w) = \frac{w}{|w|} \max(|w| - \tau, 0) \text{ entry by entry}.$$

*Proof.* Put $W = T X$. Then $\|X - Z\| = \|W - T Z\|$, so the problem becomes $\min_W \tfrac12 \|W - TZ\|^2 + \tau \|W\|_1$, which splits into one problem per complex entry: $\min_w \tfrac12 |w - a|^2 + \tau |w|$. For a fixed modulus $|w| = \rho$, the first term is smallest when $w$ has the phase of $a$, and then the problem is $\min_{\rho \ge 0} \tfrac12 (\rho - |a|)^2 + \tau \rho$, with the minimizer $\rho = \max(|a| - \tau, 0)$. So $w = \Lambda_\tau(a)$, and $X = T^H W$. $\square$

## 3. The iteration is proximal gradient

**Theorem 4.** Lines L3 to L6 are one proximal gradient step with step $t$ on $F$ in the variable $z = (L, S)$:

$$z_{k+1} = \operatorname{prox}_{t g}\big(z_k - t \nabla f(z_k)\big), \qquad g(L, S) = \lambda_L \|L\|_* + \lambda_S \|T S\|_1.$$

*Proof.* The gradient of $f$ with respect to $L$ and to $S$ is the same matrix $\gamma = E^H(E(L + S) - d)$. The function $g$ is a sum of a function of $L$ and a function of $S$, so its proximal map acts on each part alone. Line L6 stores $M = (L + S) - t \gamma$. Then $M - S = L - t \gamma$, and line L3 applies Lemma 2 with $\tau = t \lambda_L$. Also $M - L = S - t \gamma$, and line L4 applies Lemma 3 with $\tau = t \lambda_S$. Line L1 sets $L = S = 0$ and $M = t E^H d$, which is $0 - t \gamma$ at $z = 0$. $\square$

## 4. Sufficient decrease

**Theorem 5.** For every step $t > 0$,

$$F(z_{k+1}) \le F(z_k) - \Big(\frac1t - \|E\|^2\Big) \|z_{k+1} - z_k\|^2.$$

So $F$ does not increase for $t \le 1 / \|E\|^2$, and it decreases strictly at each step that moves for $t < 1 / \|E\|^2$.

*Proof.* Write $\Delta = z_{k+1} - z_k = (\Delta_L, \Delta_S)$ and $\gamma = \nabla_L f(z_k) = \nabla_S f(z_k)$. Since $f$ is quadratic,

$$f(z_{k+1}) = f(z_k) + \langle \gamma, \Delta_L + \Delta_S \rangle + \tfrac12 \|E(\Delta_L + \Delta_S)\|^2 \le f(z_k) + \langle \nabla f(z_k), \Delta \rangle + \|E\|^2 \|\Delta\|^2,$$

using $\|\Delta_L + \Delta_S\|^2 \le 2 \|\Delta_L\|^2 + 2 \|\Delta_S\|^2$. So the gradient of $f$ is Lipschitz with the constant $2 \|E\|^2$. The optimality condition of the proximal map says that $u = (z_k - t \nabla f(z_k) - z_{k+1})/t$ is a subgradient of $g$ at $z_{k+1}$. So

$$g(z_k) \ge g(z_{k+1}) + \langle u, z_k - z_{k+1} \rangle = g(z_{k+1}) + \tfrac1t \|\Delta\|^2 - \langle \nabla f(z_k), \Delta \rangle.$$

Add the two inequalities. $\square$

**Consequences.** Let $t < 1/\|E\|^2$ and $c = 1/t - \|E\|^2 > 0$. Summing Theorem 5 gives $\sum_k \|z_{k+1} - z_k\|^2 \le (F(z_0) - \inf F) / c$, which is finite because $F \ge 0$. So the steps tend to zero. The step $t < 1/\|E\|^2$ is $t < 2/\mathrm{Lip}$ for $\mathrm{Lip} = 2\|E\|^2$. In this range the general theory of forward-backward splitting gives convergence of $z_k$ to a minimizer of $F$ when one exists (Combettes and Wajs 2005). For $t \le 1/\mathrm{Lip} = 1/(2\|E\|^2)$, Beck and Teboulle (2009) also give $F(z_k) - \min F \le \|z_0 - z^\star\|^2 / (2 t k)$. With $\|E\| = 1$, the step $t = 1$ of Otazo et al. is the boundary case: Theorem 5 still gives a non-increasing $F$, but none of these convergence results applies.

These results are about $F$. They do not say that the minimizer splits the true series into its true $L$ and $S$, or that it is close to the true series. Both depend on the sampling, the weights and the series, and are measured.

## 5. Known answers with full sampling

With one coil, $c = 1$, full masks and $t = 1$, Lemma 1 gives $E^H E = I$, so $\gamma = L + S - X$ for the true series $X$, and $M = X$ after every step. Then line L3 gives $L = \operatorname{prox}_{\lambda_L \|\cdot\|_*}(X - S)$ and line L4 gives $S = T^H \Lambda_{\lambda_S}(T(X - L))$, each from the previous pair. If $\lambda_S$ exceeds every entry of $|T X|$ and of $|T(X - L)|$ along the iteration, then $S = 0$ and $L = \operatorname{prox}_{\lambda_L \|\cdot\|_*}(X)$ after one step. If $\lambda_L$ exceeds every singular value of $X$ and of $X - S$, then $L = 0$ and $S = T^H \Lambda_{\lambda_S}(T X)$. The test file checks both cases.
