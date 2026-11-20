---
title: Projective forward Euler is stable for stiff linear systems with enough inner steps and first order accurate in the outer step
proves: [correctness]
status: full
---

We prove the properties of projective forward Euler, the case of the page where the lift and the restriction are the identity and the micro step is forward Euler, for the linear system $y' = A y$, in exact arithmetic. Let $h$ be the micro step, $k$ the number of healing steps, $M \ge 0$ the projection factor, $m = M + k + 1$ and $H = m h$ the length of an outer step. Assume $A = V \Lambda V^{-1}$ with $\Lambda$ diagonal, and write $Z = I + h A$ for the Euler matrix.

**Lemma 1 (one outer step).** One outer step maps $y$ to $\sigma(Z) y$, with the polynomial

$$\sigma(\zeta) = \big((M + 1)\zeta - M\big)\zeta^k.$$

So the eigenvector components evolve independently: the component on the eigenvalue $\lambda$ is multiplied by $\sigma(1 + h\lambda)$.

*Proof.* Line L3 applies $Z$ to $y$ a total of $k + 1$ times, so $X_k = Z^k y$ and $X_{k+1} = Z^{k+1} y$. Lines L4 and L5 give $X_{k+1} + M h \cdot (X_{k+1} - X_k)/h = (M + 1) Z^{k+1} y - M Z^k y$. Since $Z = V (I + h\Lambda) V^{-1}$, $\sigma(Z) = V \sigma(I + h\Lambda) V^{-1}$. $\square$

With $M = 0$, $\sigma(\zeta) = \zeta^{k+1}$, so the method is plain forward Euler, as the tests check.

**Lemma 2 (damping of the fast modes).** If $|\zeta| \le \rho < 1$ and $\rho^k \le 1/(2M + 1)$, then $|\sigma(\zeta)| \le 1$.

*Proof.* $|\sigma(\zeta)| \le ((M + 1)\rho + M)\rho^k \le (2M + 1)\rho^k \le 1$. $\square$

So a fast mode with $|1 + h\lambda| \le \rho$ is not amplified if $k \ge \log(2M + 1) / \log(1/\rho)$. The modes are damped by the inner steps, which forward Euler can take stably, and the projection over $M h$ cannot amplify them by more than the factor $2M + 1$, which the $k$ damping steps cancel. For $\rho = 1/2$ and $M = 100$ the condition is $k \ge 7.65$; the example of the page shows $k = 8$ stable and $k = 4$ unstable.

**Lemma 3 (consistency for the slow modes).** Let $z = h\lambda$ be real with $-2/(M + 1) \le z \le 0$ and $z \ge -1$. Then

$$|\sigma(1 + z) - e^{m z}| \le \tfrac12 m^2 z^2 \quad\text{and}\quad |\sigma(1 + z)| \le 1.$$

*Proof.* For $w \le 0$, $0 \le e^w - 1 - w \le w^2 / 2$, by Taylor's theorem with remainder $e^\xi w^2/2$ and $\xi \le 0$. Also $|a^k - b^k| \le k |a - b|$ for $|a|, |b| \le 1$. Since $0 \le 1 + z \le 1$ and $0 < e^z \le 1$, these give $|(1 + z)^k - e^{k z}| \le k z^2 / 2$. With $w = (M + 1) z$, $|1 + w - e^w| \le w^2 / 2$, and $|1 + w| \le 1$ because $-2 \le w \le 0$. Then

$$\sigma(1 + z) - e^{m z} = (1 + w)\big[(1 + z)^k - e^{k z}\big] + \big[1 + w - e^{w}\big] e^{k z},$$

whose modulus is at most $k z^2 / 2 + (M + 1)^2 z^2 / 2 \le m^2 z^2 / 2$. Finally $|\sigma(1 + z)| = |1 + w| (1 + z)^k \le 1$. $\square$

**Theorem.** Let all eigenvalues of $A$ be real and negative, split into slow ones with $|\lambda| \le 2/((M + 1) h)$ and $|\lambda| \le 1/h$, and fast ones with $|1 + h\lambda| \le \rho$ and $\rho^k \le 1/(2M + 1)$. Let $y_n$ be the result of $n$ outer steps and $T = n H$. Then

$$\|y_n - e^{T A} y_0\| \le \|V\| \|V^{-1}\| \|y_0\| \max\Big( \tfrac12 T H \lambda_s^2,\ \max_{\text{fast}} |\sigma(1 + h\lambda)|^n + e^{-T |\lambda_f|} \Big),$$

where $\lambda_s$ is the slow eigenvalue of largest modulus and $\lambda_f$ the fast one of smallest modulus. So the error in the slow modes is of first order in $H$, and the fast modes stay bounded and decay.

*Proof.* In the eigenvector coordinates $c = V^{-1} y$, Lemma 1 gives $c_n = \sigma(I + h\Lambda)^n c_0$, and the exact solution has $e^{T\Lambda} c_0 = (e^{H\Lambda})^n c_0$. For a slow mode let $a = \sigma(1 + h\lambda)$ and $b = e^{m h \lambda}$; both have modulus at most 1 by Lemma 3, so

$$|a^n - b^n| \le n |a - b| \le n \tfrac12 m^2 h^2 \lambda^2 = \tfrac12 T H \lambda^2.$$

For a fast mode, $|a^n - b^n| \le |a|^n + |b|^n$, and $|a| \le 1$ by Lemma 2. The bound on each coordinate holds for the maximum norm of $c_n - e^{T\Lambda} c_0$ relative to that of $c_0$; multiply by the condition number of $V$ to return to $y$. $\square$

For a normal $A$, as in the example of the page, $V$ is orthogonal and the condition number is 1.

**The coarse case.** With a fine simulator and a coarse restriction, the same argument applies when the fine dynamics has a slow manifold that is parametrized by the coarse variables: after the healing steps, the fine state is close to the slow manifold, and the outer step is a projective Euler step for the coarse dynamics on it. The lift adds an error at every outer step that the healing steps reduce only to the size of the deviation of the slow dynamics during the healing, so it adds a term proportional to the number of outer steps. We do not prove a bound for this case.
