---
title: Inverse iteration converges to the eigenvector of the eigenvalue nearest the shift
proves: [correctness, termination]
status: full
---

Notation of the page: $A \in \mathbb{C}^{n \times n}$, a shift $\sigma$ that is not an eigenvalue, $B = (A - \sigma I)^{-1}$, and $x_k$ the unit vector after step $k$. In exact arithmetic line L4 computes $y = B x_{k-1}$, so by induction $x_k = B^k x_0 / \|B^k x_0\|_2$: each step multiplies by $B$ and rescales, and rescaling does not change the direction.

**Spectrum of $B$.** If $A v = \lambda v$, then $(A - \sigma I) v = (\lambda - \sigma) v$, so $B v = \mu v$ with $\mu = 1/(\lambda - \sigma)$. So $B$ has the eigenvalues $\mu_i = 1/(\lambda_i - \sigma)$ with the same eigenvectors. The eigenvalue of $A$ nearest $\sigma$ is the eigenvalue of $B$ of largest modulus.

**Theorem 1 (convergence, diagonalizable case).** Let $A = V \Lambda V^{-1}$ be diagonalizable, with eigenvectors $v_1, \dots, v_n$ of unit norm. Let $J$ be an index with
$$|\lambda_J - \sigma| < |\lambda_i - \sigma| \quad \text{for every } i \text{ with } \lambda_i \neq \lambda_J,$$
and let $P$ be the eigenprojector onto $\operatorname{null}(A - \lambda_J I)$ along the other eigenvectors. Let $r = \max_{\lambda_i \neq \lambda_J} |\lambda_J - \sigma| / |\lambda_i - \sigma| < 1$. If $P x_0 \neq 0$, then for every $k \ge 1$
$$\sin \angle(x_k, \operatorname{null}(A - \lambda_J I)) \le \frac{C r^k}{1 - C r^k} \quad \text{whenever } C r^k < 1, \qquad C = \frac{\sum_{\lambda_i \neq \lambda_J} |c_i|}{\|P x_0\|_2},$$
where $x_0 = \sum_i c_i v_i$.

*Proof.* Write $x_0 = P x_0 + \sum_{\lambda_i \neq \lambda_J} c_i v_i$, where $P x_0 = \sum_{\lambda_i = \lambda_J} c_i v_i$ is an eigenvector of $\lambda_J$. Then
$$\frac{B^k x_0}{\mu_J^k} = P x_0 + \sum_{\lambda_i \neq \lambda_J} c_i \left(\frac{\mu_i}{\mu_J}\right)^k v_i = P x_0 + e_k, \qquad \|e_k\|_2 \le \sum_{\lambda_i \neq \lambda_J} |c_i| \, r^k,$$
because $|\mu_i / \mu_J| = |\lambda_J - \sigma| / |\lambda_i - \sigma| \le r$ and $\|v_i\|_2 = 1$. Let $w = P x_0 + e_k$, which is parallel to $x_k$. The distance from $w$ to the eigenspace is at most $\|e_k\|_2$, and $\|w\|_2 \ge \|P x_0\|_2 - \|e_k\|_2$. So
$$\sin \angle(x_k, \operatorname{null}(A - \lambda_J I)) = \frac{\operatorname{dist}(w, \operatorname{null}(A - \lambda_J I))}{\|w\|_2} \le \frac{\|e_k\|_2}{\|P x_0\|_2 - \|e_k\|_2} \le \frac{C r^k}{1 - C r^k}. \qquad \square$$

So the angle goes to zero at least linearly with the ratio $r$. The ratio is sharp when $c_K \neq 0$ for an index $K$ with $|\lambda_J - \sigma| / |\lambda_K - \sigma| = r$, since then the $K$ term of $e_k$ has exactly that rate.

**Theorem 2 (the eigenvalue estimate, Hermitian case).** If $A$ is Hermitian, $\lambda_J$ is simple, and $s_k = \sin \angle(x_k, v_J)$, then the Rayleigh quotient $\theta_k = x_k^* A x_k$ of line L6 satisfies $|\theta_k - \lambda_J| \le (\lambda_{\max} - \lambda_{\min}) \, s_k^2$.

*Proof.* Write $x_k = \cos\phi \, v_J + \sin\phi \, z$ with $z$ a unit vector orthogonal to $v_J$, after a unimodular scaling of $v_J$; here $|\sin \phi| = s_k$. As $A v_J = \lambda_J v_J$ and $z \perp v_J$, the cross terms vanish and $\theta_k = \cos^2\phi \, \lambda_J + \sin^2\phi \, z^* A z$. So $\theta_k - \lambda_J = \sin^2\phi \, (z^* A z - \lambda_J)$, and both $z^* A z$ and $\lambda_J$ lie in $[\lambda_{\min}, \lambda_{\max}]$. $\square$

So for a Hermitian matrix the eigenvalue estimate converges with the rate $r^2$.

**Theorem 3 (what the stopping test certifies).** When the loop returns at line L8 with CONVERGED, the pair $(\theta, x)$ is an exact eigenpair of $A + E$ with $E = -r_k x_k^*$ and $\|E\|_2 = \|r_k\|_2 \le \mathrm{tol} \cdot \|A\|_F$.

*Proof.* $(A + E) x_k = A x_k - r_k = \theta x_k$ because $x_k^* x_k = 1$. The norm of the rank-one matrix $r_k x_k^*$ is $\|r_k\|_2 \|x_k\|_2 = \|r_k\|_2$. $\square$

**Termination.** The loop of line L3 runs at most $\mathrm{kmax}$ times, and each step does a fixed finite amount of work, so the algorithm stops. The test of line L8 is also met eventually under the hypotheses of Theorem 1, in exact arithmetic with $\mathrm{tol} > 0$. Write $x_k = w_k + d_k$ with $w_k$ the nearest point of the eigenspace, so $\|d_k\|_2 \le 2 \sin\angle(x_k, \operatorname{null}(A - \lambda_J I)) \to 0$. Then $A w_k = \lambda_J w_k$, so $\|A x_k - \lambda_J x_k\|_2 = \|(A - \lambda_J I) d_k\|_2 \to 0$. The Rayleigh quotient minimizes the residual over all scalars for a unit vector, so $\|A x_k - \theta_k x_k\|_2 \le \|A x_k - \lambda_J x_k\|_2 \to 0$.

**Floating point.** Line L1 computes $L$ and $U$ with $L U = P(A - \sigma I + F)$, $\|F\|$ of order $n u \, \rho_n \|A\|$ for the growth factor $\rho_n$, and the triangular solves are backward stable. So the computed $\hat y$ satisfies $(A - \sigma I + E) \hat y = x_{k-1}$ with $\|E\|_2 \le c \, n \, u \, \rho_n \|A\|_2$. Then for $\hat x = \hat y / \|\hat y\|_2$,
$$\|(A - \sigma I) \hat x\|_2 = \frac{\|x_{k-1} - E \hat y\|_2}{\|\hat y\|_2} \le \frac{1}{\|\hat y\|_2} + \|E\|_2 .$$
When $\sigma$ is close to an eigenvalue, $\|\hat y\|_2$ is large, so the pair $(\sigma, \hat x)$ already has a residual of order $\|E\|_2$, that is, it is backward stable. The large error in $\hat y$ that the near-singular solve makes lies almost entirely along the wanted eigenvector, so it does no harm (Wilkinson 1965, Chapter 9; Peters and Wilkinson 1979).
