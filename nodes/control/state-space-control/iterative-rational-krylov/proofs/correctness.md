---
title: A fixed point of IRKA interpolates G and G' at the mirrored reduced poles, so it satisfies the first-order conditions for H2 optimality
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$ be Hurwitz, $b \in \mathbb{R}^n$, $c \in \mathbb{R}^{1 \times n}$ and $G(s) = c (sI - A)^{-1} b$. For shifts $s_1, \dots, s_r$ that are closed under conjugation and are not eigenvalues of $A$, let $V, W \in \mathbb{C}^{n \times r}$ have the columns $x_i = (s_i I - A)^{-1} b$ and $y_i = (s_i I - A^T)^{-1} c^T$. Assume $E = W^T V$ is invertible. The projected model is

$$A_r = E^{-1} W^T A V, \qquad b_r = E^{-1} W^T b, \qquad c_r = c V, \qquad G_r(s) = c_r (sI - A_r)^{-1} b_r.$$

The $\mathcal{H}_2$ norm is $\|H\|_{\mathcal{H}_2}^2 = \frac{1}{2\pi} \int_{-\infty}^{\infty} |H(j\omega)|^2\, d\omega$ (see [H2 norm](/h2-norm/)). IRKA repeats the projection with the new shifts $s_i \leftarrow -\lambda_i(A_r)$ until the shifts do not change.

## Lemma 1: the reduced transfer function as a projection

Let $M(s) = W^T (sI - A) V$. Where $M(s)$ is invertible, $G_r(s) = c V M(s)^{-1} W^T b$, and $G_r$ depends only on the column spaces of $V$ and $W$.

*Proof.* $sI - A_r = E^{-1}(s E - W^T A V) = E^{-1} M(s)$, so $(sI - A_r)^{-1} b_r = M(s)^{-1} E E^{-1} W^T b = M(s)^{-1} W^T b$. If $V$ is replaced by $V R$ and $W$ by $W S$ with $R$ and $S$ invertible, $M$ becomes $S^T M R$ and $c V R (S^T M R)^{-1} S^T W^T b = c V M^{-1} W^T b$. $\square$

So the implementation may replace a conjugate pair of columns $x, \bar x$ by $\operatorname{Re} x, \operatorname{Im} x$, which span the same space because $\operatorname{Re} x = (x + \bar x)/2$ and $\operatorname{Im} x = (x - \bar x)/(2j)$. Here $\bar x = (\bar s I - A)^{-1} b$ because $A$ and $b$ are real. It may also orthonormalize the columns. Neither step changes $G_r$, and the reduced matrices become real.

## Lemma 2: Hermite interpolation

If $M(s_i)$ is invertible, then $G_r(s_i) = G(s_i)$ and $G_r'(s_i) = G'(s_i)$.

*Proof.* Fix $\sigma = s_i$, $M = M(\sigma)$, $x = x_i$ and $y = y_i$. Let $P = V M^{-1} W^T (\sigma I - A)$. Then $P V = V M^{-1} M = V$, so $P$ is the identity on the column space of $V$. As $x$ is a column of $V$, $P x = x$, that is, $V M^{-1} W^T b = x$. In the same way, $Q = (\sigma I - A) V M^{-1} W^T$ satisfies $W^T Q = W^T$, so $y^T Q = y^T$, that is, $c V M^{-1} W^T = c (\sigma I - A)^{-1} = y^T$. With Lemma 1:

$$G_r(\sigma) = c V M^{-1} W^T b = c x = G(\sigma).$$

For the derivative, $M'(s) = W^T V$ and $\frac{d}{ds} M(s)^{-1} = -M^{-1} M' M^{-1}$, so

$$G_r'(\sigma) = -(c V M^{-1} W^T)(V M^{-1} W^T b) = -y^T x = -c (\sigma I - A)^{-2} b = G'(\sigma). \qquad \square$$

Note that $M(s_i) = E (s_i I - A_r)$, so $M(s_i)$ is invertible when $s_i$ is not an eigenvalue of $A_r$.

## Lemma 3: the H2 inner product by residues

Let $H$ be real, strictly proper and with simple poles $\mu_1, \dots, \mu_r$ in the open left half plane and residues $\psi_k$, so $H(s) = \sum_k \psi_k / (s - \mu_k)$. Let $G$ be real, strictly proper and with all poles in the open left half plane. Then

$$\langle G, H \rangle = \frac{1}{2\pi} \int_{-\infty}^{\infty} G(j\omega) \overline{H(j\omega)}\, d\omega = \sum_{k=1}^{r} \psi_k\, G(-\mu_k).$$

*Proof.* $H$ is real, so $\overline{H(j\omega)} = H(-j\omega)$, and the integral is $\frac{1}{2\pi j} \int_{j\mathbb{R}} G(s) H(-s)\, ds$. The integrand is $O(|s|^{-2})$, so the contour can be closed by a large half circle in the right half plane, which runs clockwise. In the right half plane $G$ has no poles, and $H(-s) = -\sum_k \psi_k / (s + \mu_k)$ has simple poles at $s = -\mu_k$ with residues $-\psi_k G(-\mu_k)$ for the product. A clockwise contour gives minus the sum of the residues. $\square$

## Theorem 1: the first-order conditions of Meier and Luenberger

Let $G_r(s) = \sum_{i=1}^r \phi_i / (s - \lambda_i)$ be real, with simple poles $\lambda_i$ in the open left half plane. The gradient of $J = \|G - G_r\|_{\mathcal{H}_2}^2$ with respect to the poles and residues is zero if

$$G(-\lambda_i) = G_r(-\lambda_i) \quad \text{and} \quad G'(-\lambda_i) = G_r'(-\lambda_i), \qquad i = 1, \dots, r,$$

and when every $\phi_i \ne 0$ these conditions are also necessary.

*Proof.* By Lemma 3 with $H = G_r$, and again with $G = H = G_r$,

$$J = \|G\|^2 - 2 \sum_i \phi_i\, G(-\lambda_i) + \sum_i \sum_k \frac{\phi_i \phi_k}{-\lambda_i - \lambda_k}.$$

This formula defines a holomorphic function $J(\phi, \lambda)$ of the $2r$ complex parameters near the given point. Since $G_r(-\lambda_i) = \sum_k \phi_k / (-\lambda_i - \lambda_k)$ and $G_r'(-\lambda_i) = -\sum_k \phi_k / (\lambda_i + \lambda_k)^2$, direct differentiation gives

$$\frac{\partial J}{\partial \phi_i} = -2\big(G(-\lambda_i) - G_r(-\lambda_i)\big), \qquad \frac{\partial J}{\partial \lambda_i} = 2 \phi_i \big(G'(-\lambda_i) - G_r'(-\lambda_i)\big).$$

On the set of real models, the parameters are closed under conjugation: a real pole has a real residue, and a pair $(\lambda_i, \lambda_k = \bar\lambda_i)$ has residues $\phi_k = \bar\phi_i$. The real coordinates are the real parameters and the real and imaginary parts of one member of each pair. For a pair, $\partial / \partial (\operatorname{Re} \lambda_i) = \partial / \partial \lambda_i + \partial / \partial \lambda_k$ and $\partial / \partial (\operatorname{Im} \lambda_i) = j(\partial / \partial \lambda_i - \partial / \partial \lambda_k)$, and the same holds for the residues. Because $G$ and $G_r$ are real, the formulas above give $\partial J / \partial \lambda_k = \overline{\partial J / \partial \lambda_i}$ on this set. So both real derivatives are zero if and only if $\partial J / \partial \lambda_i = 0$. The interpolation conditions make every complex partial zero, which proves sufficiency. If the gradient is zero and every $\phi_i \ne 0$, the two formulas give the conditions. $\square$

## Theorem 2: a fixed point of IRKA is a stationary point of the H2 error

Assume IRKA reaches shifts with $s_i = -\lambda_i(A_r)$ for every $i$, where the eigenvalues $\lambda_i$ of $A_r$ are simple and lie in the open left half plane, and $E$ is invertible. Then $G_r$ satisfies the conditions of Theorem 1, so it is a stationary point of $\|G - G_r\|_{\mathcal{H}_2}$ over real models of order $r$ with simple poles.

*Proof.* Each $s_i = -\lambda_i$ lies in the open right half plane, so it is not an eigenvalue of the Hurwitz matrices $A$ and $A_r$. So $M(s_i) = E (s_i I - A_r)$ is invertible, and Lemma 2 gives $G_r(-\lambda_i) = G(-\lambda_i)$ and $G_r'(-\lambda_i) = G'(-\lambda_i)$. The poles of $G_r$ are among the $\lambda_i$, and Theorem 1 applies. $\square$

## What is not proved

A stationary point need not be a minimum, and the iteration need not converge. Flagg, Beattie and Gugercin (2012) proved that for state-space-symmetric systems ($A = A^T$ and $b = c^T$) the fixed point is locally attractive. For general systems, convergence is an open problem. The implementation therefore returns a flag `converged`, and the tests check the conclusions of Theorem 2 only on runs that converged.

The implementation stops when the largest relative change of the sorted shifts is below `tol`, so at the returned model the conditions of Theorem 2 hold up to an error of the size of `tol` times the sensitivity of the reduced poles.
