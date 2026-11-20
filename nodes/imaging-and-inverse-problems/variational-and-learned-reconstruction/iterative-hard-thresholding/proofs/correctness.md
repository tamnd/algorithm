---
title: IHT with unit step converges linearly to an s-sparse x when delta_3s < 1/2, and its residual does not increase when ||A|| <= 1
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix, $x \in \mathbb{R}^n$ has at most $s$ nonzero entries, and $y = Ax + e$. The hard thresholding operator $H_s(v)$ keeps the $s$ entries of $v$ of largest magnitude and sets the others to zero. The iteration with unit step is $u^k = x^k + A^T(y - Ax^k)$ and $x^{k+1} = H_s(u^k)$. For a set $T \subseteq \{1, \dots, n\}$, $A_T$ is the submatrix of the columns in $T$ and $v_T$ is the restriction of a vector $v$ to $T$. The restricted isometry constant $\delta_k$ is the smallest $\delta \ge 0$ with $(1 - \delta)\|z\|^2 \le \|Az\|^2 \le (1 + \delta)\|z\|^2$ for every $z$ with at most $k$ nonzero entries.

## Part 1: a contraction under the restricted isometry property

**Lemma 1 (best $s$-term approximation).** For every $v$, the vector $H_s(v)$ minimizes $\|v - z\|$ over all $z$ with at most $s$ nonzero entries.

*Proof.* For $z$ with support $S$, $|S| \le s$, we have $\|v - z\|^2 = \|v_S - z_S\|^2 + \sum_{i \notin S} v_i^2 \ge \sum_{i \notin S} v_i^2$, with equality for $z = v_S$. The sum $\sum_{i \notin S} v_i^2 = \|v\|^2 - \sum_{i \in S} v_i^2$ is smallest when $S$ holds the $s$ largest values of $|v_i|$, and then $z = v_S = H_s(v)$. $\square$

**Lemma 2 (restricted operators).** If $|T| \le k$, then every eigenvalue of $A_T^TA_T$ lies in $[1 - \delta_k, 1 + \delta_k]$. Hence $\|I - A_T^TA_T\| \le \delta_k$ and $\|A_T^Te\| \le \sqrt{1 + \delta_k}\,\|e\|$.

*Proof.* For $z \in \mathbb{R}^T$, the Rayleigh quotient $z^TA_T^TA_Tz/\|z\|^2 = \|A_Tz\|^2/\|z\|^2$ lies in $[1 - \delta_k, 1 + \delta_k]$ by the definition of $\delta_k$. The symmetric matrix $I - A_T^TA_T$ has eigenvalues in $[-\delta_k, \delta_k]$, so its norm is at most $\delta_k$. Finally $\|A_T^T\| = \|A_T\| \le \sqrt{1 + \delta_k}$. $\square$

**Theorem 1.** Let $\delta = \delta_{3s}$. For every $k \ge 0$ with $x^k$ at most $s$-sparse,

$$\|x^{k+1} - x\| \le 2\delta\,\|x^k - x\| + 2\sqrt{1 + \delta}\,\|e\|.$$

If $\delta < 1/2$ and $x^0 = 0$, then for all $k$

$$\|x^k - x\| \le (2\delta)^k\|x\| + \frac{2\sqrt{1 + \delta}}{1 - 2\delta}\|e\|.$$

*Proof.* Let $T = \operatorname{supp}(x) \cup \operatorname{supp}(x^k) \cup \operatorname{supp}(x^{k+1})$, so $|T| \le 3s$. The vectors $x$, $x^k$ and $x^{k+1}$ all vanish off $T$, so $A(x - x^k) = A_T(x - x^k)_T$. Restrict $u^k$ to $T$:

$$u^k_T = x^k_T + A_T^T\big(A_T(x - x^k)_T + e\big),\qquad u^k_T - x_T = (I - A_T^TA_T)(x^k - x)_T + A_T^Te.$$

By Lemma 2, $\|u^k_T - x_T\| \le \delta\|x^k - x\| + \sqrt{1 + \delta}\,\|e\|$.

Next compare $x^{k+1}$ with $x$. Both are $s$-sparse, so Lemma 1 gives $\|u^k - x^{k+1}\| \le \|u^k - x\|$. For any $z$ that vanishes off $T$, $\|u^k - z\|^2 = \|u^k_T - z_T\|^2 + \|u^k_{T^c}\|^2$. Both $x^{k+1}$ and $x$ vanish off $T$, so the common term cancels and $\|u^k_T - x^{k+1}_T\| \le \|u^k_T - x_T\|$. The triangle inequality gives

$$\|x^{k+1} - x\| = \|x^{k+1}_T - x_T\| \le \|x^{k+1}_T - u^k_T\| + \|u^k_T - x_T\| \le 2\|u^k_T - x_T\|,$$

which is the one-step bound. Every iterate $x^k$ with $k \ge 1$ is $s$-sparse because it is an output of $H_s$, and $x^0 = 0$ is $s$-sparse. With $\rho = 2\delta < 1$ and $c = 2\sqrt{1 + \delta}\|e\|$, induction on the one-step bound gives $\|x^k - x\| \le \rho^k\|x^0 - x\| + c(1 + \rho + \dots + \rho^{k-1}) \le \rho^k\|x\| + c/(1 - \rho)$. $\square$

In particular, without noise the iterates converge to $x$ with rate $(2\delta_{3s})^k$, and $x$ is the only $s$-sparse fixed point. The proof uses only $\|I - A_T^TA_T\|$ and $\|A_T^Te\|$ for the sets $T$ that occur, so the one-step bound holds with these quantities for every matrix. The test file checks this local form on a Gaussian matrix where $\delta_{3s}$ is not small.

## Part 2: the residual does not increase when $\|A\| \le 1$

**Theorem 2.** If $\|A\| \le 1$, then for every $y$, every start and every $k \ge 1$, $\|y - Ax^{k+1}\| \le \|y - Ax^k\|$.

*Proof.* Define the surrogate, for $x, z \in \mathbb{R}^n$,

$$C(x, z) = \|y - Ax\|^2 + \|x - z\|^2 - \|A(x - z)\|^2.$$

Since $\|A(x - z)\| \le \|A\|\,\|x - z\| \le \|x - z\|$, we have $C(x, z) \ge \|y - Ax\|^2$, with equality at $x = z$. Expand the squares:

$$\|y - Ax\|^2 - \|Ax - Az\|^2 = \|y\|^2 - 2\langle Ax, y - Az\rangle - \|Az\|^2,$$

$$\|x - z\|^2 = \|x\|^2 - 2\langle x, z\rangle + \|z\|^2.$$

Adding these, $C(x, z) = \|x - u\|^2 + c(z)$ with $u = z + A^T(y - Az)$ and a number $c(z)$ that does not depend on $x$. By Lemma 1, $x^{k+1} = H_s(u^k)$ minimizes $C(\cdot, x^k)$ over the $s$-sparse vectors. For $k \ge 1$, $x^k$ is itself $s$-sparse, so

$$\|y - Ax^{k+1}\|^2 \le C(x^{k+1}, x^k) \le C(x^k, x^k) = \|y - Ax^k\|^2. \qquad \square$$

This is a majorization-minimization argument, as in Blumensath and Davies (2008). It needs no sparsity of the true signal and no restricted isometry property, but it gives no statement about the distance to $x$. It is the reason for the condition $\|A\| < 1$ in that paper. Without it the residual can grow: the example on the main page with $\|A\|^2 = 2$ cycles between two points with different residuals.
