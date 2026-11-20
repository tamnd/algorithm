---
title: The lifted linear map, the projection onto the semidefinite cone, and the rate of projected gradient
proves: [correctness]
status: full
---

Matrices are $n \times n$ Hermitian, with the real inner product $\langle P, Q \rangle = \operatorname{Re} \operatorname{tr}(P^* Q)$ and the Frobenius norm. $X \succeq 0$ means positive semidefinite, and $S_+$ is the set of these matrices. The data are $y_r = |a_r^* x|^2$ for $r = 1, \dots, m$. Put

$$\mathcal{A}(X)_r = a_r^* X a_r, \qquad F(X) = \tfrac12 \|\mathcal{A}(X) - y\|^2 + \lambda \operatorname{tr} X, \qquad \lambda \ge 0 .$$

The implementation runs $X_{k+1} = P_{S_+}\bigl(X_k - \nabla F(X_k) / L\bigr)$ from $X_0 = 0$ with $L \ge \|\mathcal{A}\|^2$ (lines L1 to L6), and then takes $\sqrt{w_1}\, u_1$ from the top eigenpair of the result. The claim of correctness has four parts: the data are linear in $X = x x^*$ (Lemma 1), the projection step is the exact projection onto $S_+$ (Lemmas 2 and 3), the iteration converges to the minimum of $F$ at the rate $O(1/k)$ (Lemma 4), and when the feasible set is the single point $x x^*$ the iterates and the extracted vector converge to the signal (Lemma 5). When the feasible set is a single point is the result of Candès and Li (2014), which is cited and not proved here.

**Lemma 1 (lifting).** $\mathcal{A}$ is real linear, $\mathcal{A}(x x^*) = y$, and its adjoint is $\mathcal{A}^*(v) = \sum_r v_r a_r a_r^*$. If $X = x x^*$ with $x \neq 0$, its top eigenvalue is $\|x\|^2$ with the eigenvector $x / \|x\|$, and $\sqrt{w_1}\, u_1 = e^{i\varphi} x$ for some real $\varphi$.

*Proof.* $a_r^* X a_r = \operatorname{tr}(a_r a_r^* X) = \langle a_r a_r^*, X \rangle$, which is real for Hermitian $X$ and linear in $X$. For $X = x x^*$ it is $(a_r^* x)(x^* a_r) = |a_r^* x|^2$. Then $\sum_r v_r \mathcal{A}(X)_r = \sum_r v_r \langle a_r a_r^*, X \rangle = \langle \sum_r v_r a_r a_r^*, X \rangle$ for real $v$. Finally $x x^* x = \|x\|^2 x$ and $x x^* w = 0$ for $w \perp x$, so the top eigenvalue is $\|x\|^2$ with a one dimensional eigenspace; a unit eigenvector is $e^{i\varphi} x / \|x\|$. $\square$

So the quadratic equations in $x$ become linear equations in $X$, with the two extra conditions $X \succeq 0$ and $\operatorname{rank} X = 1$. PhaseLift keeps the first condition and drops the second.

**Lemma 2 (projection onto $S_+$).** Let $X = U \operatorname{diag}(w) U^*$ with $U$ unitary. Then $X_+ = U \operatorname{diag}(\max(w, 0)) U^*$ is the unique nearest point of $S_+$ to $X$. It satisfies $\langle X - X_+, Z - X_+ \rangle \le 0$ for all $Z \in S_+$, and $X_+ (X_+ - X) = 0$.

*Proof.* For $Z \in S_+$ put $M = U^* Z U$, which is also positive semidefinite, so $M_{kk} \ge 0$. The norm does not change under unitary maps, so

$$\|X - Z\|^2 = \|\operatorname{diag}(w) - M\|^2 \ge \sum_k (w_k - M_{kk})^2 \ge \sum_{k : w_k < 0} w_k^2 = \|X - X_+\|^2 .$$

The second inequality uses $M_{kk} \ge 0$ for each $k$ with $w_k < 0$. So $X_+ \in S_+$ is a nearest point. $S_+$ is closed and convex, so the nearest point is unique and is characterized by the variational inequality. Also $X_+ - X = U \operatorname{diag}(\max(-w, 0)) U^*$, and $\max(w_k, 0) \max(-w_k, 0) = 0$ for each $k$. $\square$

**Lemma 3 (the real form).** For $X = B + iC$ with real $B$ and $C$, put $\phi(X) = \begin{pmatrix} B & -C \\ C & B \end{pmatrix}$. Then $\phi(X + Y) = \phi(X) + \phi(Y)$, $\phi(XY) = \phi(X)\phi(Y)$, $\phi(X^*) = \phi(X)^T$, and $\|\phi(X)\|^2 = 2\|X\|^2$. If $X$ is Hermitian, $\phi(X)$ is real symmetric with the same eigenvalues, each twice, and $\phi(X_+) = \phi(X)_+$, the clipping of $\phi(X)$.

*Proof.* The first three are direct computations with $(B + iC)(D + iE) = (BD - CE) + i(BE + CD)$. Each of $B$ and $C$ appears twice in $\phi(X)$, which gives the norm. If $X u = w u$ with $u = p + iq$, then $\phi(X)$ maps $(p, q)$ to $w (p, q)$ and $(-q, p)$ to $w(-q, p)$, which is the eigenvector for $i u$. These two real vectors are orthogonal, and an orthonormal basis $u_1, \dots, u_n$ of $\mathbb{C}^n$ gives an orthonormal basis of $\mathbb{R}^{2n}$ in this way. So the eigenvalues of $\phi(X)$ are those of $X$, each twice. Let $p$ be a real polynomial with $p(w_k) = \max(w_k, 0)$ for every eigenvalue $w_k$ of $X$. Then $X_+ = p(X)$ and $\phi(X)_+ = p(\phi(X))$, because both matrices have the same eigenvalues. By the rules above, $p(\phi(X)) = \phi(p(X)) = \phi(X_+)$. $\square$

The implementation computes $\phi(X)_+ = \sum_{w_k > 0} w_k q_k q_k^T$ from the eigenvectors $q_k$ of the Jacobi method, and reads $X_+ = B_+ + i C_+$ off its blocks. Each block appears twice, so it takes the mean of the two copies.

**Lemma 4 (projected gradient).** $F$ is convex on $S_+$, $\nabla F(X) = \mathcal{A}^*(\mathcal{A}(X) - y) + \lambda I$, and for all $X$ and $Y$

$$F(Y) = F(X) + \langle \nabla F(X), Y - X \rangle + \tfrac12 \|\mathcal{A}(Y - X)\|^2 \le F(X) + \langle \nabla F(X), Y - X \rangle + \tfrac{L}{2} \|Y - X\|^2 .$$

Let $F^*$ be the minimum of $F$ over $S_+$ and $X^*$ a minimizer. A minimizer exists when $\lambda > 0$, because then $F(X) \ge \lambda \operatorname{tr} X \ge \lambda \|X\|$ on $S_+$, and when $\lambda = 0$ and the data are exact, because then $F(x x^*) = 0$. Then the iterates satisfy $F(X_{k+1}) \le F(X_k) - \frac{L}{2}\|X_{k+1} - X_k\|^2$, $\|X_{k+1} - X^*\| \le \|X_k - X^*\|$, and

$$F(X_k) - F^* \le \frac{L \|X_0 - X^*\|^2}{2k} \qquad (k \ge 1).$$

*Proof.* $F$ is a convex quadratic plus a linear term, so the expansion is exact: the linear terms give $\nabla F$ by Lemma 1, and the quadratic term is $\frac12 \|\mathcal{A}(Y - X)\|^2 \le \frac{L}{2}\|Y - X\|^2$. Fix $X$, put $G = \nabla F(X)$ and $X^+ = P_{S_+}(X - G/L)$. By Lemma 2 with the point $X - G/L$, every $Z \in S_+$ has $\langle X - G/L - X^+, Z - X^+ \rangle \le 0$, that is $\langle G, X^+ - Z \rangle \le L \langle X - X^+, X^+ - Z \rangle$. Convexity gives $F(X) \le F(Z) - \langle G, Z - X \rangle$. With the expansion for $Y = X^+$,

$$F(X^+) \le F(Z) + \langle G, X^+ - Z \rangle + \tfrac{L}{2}\|X^+ - X\|^2 \le F(Z) + L \langle X - X^+, X^+ - Z \rangle + \tfrac{L}{2}\|X^+ - X\|^2 .$$

The right side equals $F(Z) + \frac{L}{2}\bigl(\|X - Z\|^2 - \|X^+ - Z\|^2\bigr)$, by the expansion of $\|(X - X^+) + (X^+ - Z)\|^2$. With $Z = X$ this is the decrease of $F$. With $Z = X^*$ and $F(X^+) \ge F^*$ it gives $\|X^+ - X^*\| \le \|X - X^*\|$. Add the inequalities for $Z = X^*$ over the steps $0, \dots, k - 1$: the right sides telescope, so $\sum_{j=1}^{k} (F(X_j) - F^*) \le \frac{L}{2}\|X_0 - X^*\|^2$. $F(X_j)$ does not increase, so the left side is at least $k (F(X_k) - F^*)$. $\square$

The implementation takes $L = \|\mathcal{A}\|^2 (1 + 10^{-9})$, where $\|\mathcal{A}\|$ is the largest singular value of the $m \times n^2$ real matrix of $\mathcal{A}$ in the orthonormal basis $E_{jj}$, $(E_{jk} + E_{kj})/\sqrt2$, $i(E_{jk} - E_{kj})/\sqrt2$ of the Hermitian matrices. The cheaper bound $L = \sum_r \|a_r\|^4$ is also valid, because $\langle a_r a_r^*, X \rangle^2 \le \|a_r a_r^*\|^2 \|X\|^2 = \|a_r\|^4 \|X\|^2$ by the Cauchy-Schwarz inequality.

**Lemma 5 (recovery when the feasible point is unique).** Let $\lambda = 0$ and suppose that $\{X \in S_+ : \mathcal{A}(X) = y\} = \{x x^*\}$. Then $X_k \to x x^*$, and $\operatorname{dist}(\sqrt{w_1(X_k)}\, u_1(X_k), x) \to 0$, where $\operatorname{dist}(z, x) = \min_\varphi \|z - e^{i\varphi} x\|$.

*Proof.* $F \ge 0$ and $F(x x^*) = 0$, so $F^* = 0$, and the minimizers are exactly the feasible points, so $X^* = x x^*$ is the only one. By Lemma 4, $F(X_k) \to 0$ and $\|X_k - X^*\|$ does not increase, so the sequence is bounded. Every limit point $\bar X$ of the sequence lies in the closed set $S_+$ and has $F(\bar X) = 0$ by continuity, so $\bar X = X^*$. A bounded sequence with a single limit point converges to it. For the vector, $w_1$ is a continuous function of $X$, so $w_1(X_k) \to \|x\|^2$. The top eigenvalue of $x x^*$ is simple, so the projection $u_1 u_1^*$ onto its eigenspace is continuous at $x x^*$, and $w_1 u_1 u_1^* \to x x^*$. For $z = \sqrt{w_1}\, u_1$ this says $z z^* \to x x^*$. Then $|x^* z|^2 = x^* z z^* x \to \|x\|^4$ and $\|z\|^2 \to \|x\|^2$, so $\operatorname{dist}^2(z, x) = \|z\|^2 + \|x\|^2 - 2|x^* z| \to 0$. $\square$

**The cited results.** Candès, Strohmer and Voroninski (2013) take the problem "minimize $\operatorname{tr} X$ subject to $\mathcal{A}(X) = y$ and $X \succeq 0$" and show that, for $m \ge c_0\, n \log n$ Gaussian vectors and a fixed $x$, its unique solution is $x x^*$ with high probability (Theorem 1.1 in the statement of Candès and Li). Candès and Li (2014, Theorem 1.2) show the same for $m \ge c_0\, n$, with probability at least $1 - O(e^{-\gamma m})$, and for all $x$ at once. Their proof shows that $x x^*$ is the only feasible point (their Lemma 2.2), so the condition of Lemma 5 holds and the trace does not matter. In that case the projected gradient with $\lambda = 0$ finds $x$.

**What is not claimed.** The probabilistic results above are cited, not proved. With $\lambda > 0$ the minimizer of $F$ is not in general $x x^*$; the penalty pulls the trace down, which helps with noise but adds a bias. The rate $O(1/k)$ is the worst case; the faster, linear decrease in the example on the main page is a measurement. The tests check Lemmas 1 to 4 on random data, and they measure the recovery on fixed seeds without a theorem for those sizes.
