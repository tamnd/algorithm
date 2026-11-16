---
title: What the SEIF computes exactly, and where it approximates
proves: [correctness]
status: full
---

**Setting.** The state is $y = (x, m)$ with the pose $x$ and the landmarks $m$. The belief is stored as $\Omega$, $\xi$ and an estimate $\mu$ of the mean $\Omega^{-1} \xi$. A landmark $m_j$ is active if the block $\Omega_{x, m_j}$ is not zero. The filter keeps the invariant that every landmark that $\Omega$ links to $x$ is in the active list. We prove four claims. The motion step (lines L1 to L5) and the update (lines L6 to L9) are the EIF steps of the [extended information filter](/extended-information-filter/), done on the local block only. The sparsification (lines L10 to L12) removes the links from the pose to $m_0$ and keeps some marginals exact, but it is an approximation. The mean recovery (line L13) never moves away from the solution of $\Omega \mu = \xi$. The claims about $\xi$ assume that $\mu = \Omega^{-1} \xi$ when the step starts; with an approximate $\mu$, each step linearizes at, and keeps, that approximate mean.

## The motion step is the EIF prediction (lines L1 to L5)

Line L1 computes the offset $\delta$ and the pose Jacobian $G_x$ at $\mu$, so the linearized motion is $y \mapsto G y + c$ with $G = \mathrm{diag}(G_x, I)$, and the predicted mean is $\bar\mu = \mu + F_x^\top \delta$, where $F_x$ selects the pose. The motion noise is $F_x^\top R F_x$ with $R$ positive semidefinite. The EIF prediction is $\bar\Omega = (G \Omega^{-1} G^\top + F_x^\top R F_x)^{-1}$ and $\bar\xi = \bar\Omega \bar\mu$.

**The transport.** $G$ is invertible, because the motion Jacobian $G_x$ has determinant 1 in the code's model. Let $T = G^{-1} = \mathrm{diag}(G_x^{-1}, I)$. Then $(G \Omega^{-1} G^\top)^{-1} = T^\top \Omega T = \Phi$, which line L2 computes.

**The noise.** Write $U = F_x^\top$. We claim $(\Phi^{-1} + U R U^\top)^{-1} = \Phi - \Phi U R (I + U^\top \Phi U R)^{-1} U^\top \Phi$, which is $\Phi - \kappa$ with $\kappa$ from line L3. First, $I + U^\top \Phi U R = I + \Phi_{xx} R$ is invertible: $\Phi_{xx} R$ has the same nonzero eigenvalues as $R^{1/2} \Phi_{xx} R^{1/2}$, which is positive semidefinite. Write $B = (I + U^\top \Phi U R)^{-1}$. Then

$$(\Phi^{-1} + U R U^\top)(\Phi - \Phi U R B U^\top \Phi) = I + U R U^\top \Phi - U R B U^\top \Phi - U R (U^\top \Phi U R) B U^\top \Phi = I + U R U^\top \Phi - U R (I + U^\top \Phi U R) B U^\top \Phi = I.$$

This form needs no inverse of $R$, so it also holds for a singular $R$, as for straight motion with no noise on one axis. So line L4 sets $\bar\Omega = \Phi - \kappa$, the EIF result.

**Locality.** $T$ changes only the pose columns, so $\Phi$ differs from $\Omega$ only in the pose rows and columns, and $\Phi_{x, m_j} = G_x^{-\top} \Omega_{x, m_j}$ is zero for every passive $m_j$. The matrix $\kappa = \Phi U R B U^\top \Phi$ is the outer product of the pose columns of $\Phi$, so it is zero outside the rows and columns of the pose and the active landmarks. So the code, which computes $\Phi$ and $\kappa$ on this local block only, gives the full result, and the motion does not make a passive landmark active.

**The vector.** Line L4 adds $(\bar\Omega - \Omega) \mu + \bar\Omega F_x^\top \delta$ to $\xi$. If $\xi = \Omega \mu$, the result is $\bar\Omega (\mu + F_x^\top \delta) = \bar\Omega \bar\mu$, and line L5 sets $\bar\mu$. The added vector is zero outside the local block, because $\bar\Omega - \Omega$ and the pose columns of $\bar\Omega$ are.

## The update is additive and local (lines L6 to L9)

Line L7 adds a new landmark with zero information, so it does not change the belief of the other variables. Lines L8 and L9 are the EIF update linearized at $\mu$; the EIF page proves that they give the information form of the EKF posterior. The Jacobian $H$ has nonzero columns only for the pose and the observed landmark, so the update changes a 5 by 5 block of $\Omega$ and 5 entries of $\xi$ in the plane. It links the pose to the observed landmark, which the code therefore makes active, so the invariant holds.

## The sparsification (lines L10 to L12)

Let $m_0$ be the landmarks to deactivate, $m_+$ the active landmarks to keep and $m_-$ the passive landmarks. The exact belief factors as $p(x, m) = p(x \mid m_0, m_+, m_-) \, p(m)$. Line L12 replaces it by

$$\tilde p(x, m) = p(x \mid m_+, m_- = \mu_-) \, p(m).$$

**The formula.** Let $S$ hold $x$, $m_0$ and $m_+$. Fixing $m_-$ at any value leaves a Gaussian over $S$ with information matrix $\Omega_{SS}$. Removing variables by integration gives the Schur complement on the rest (see the [Schur complement](/schur-complement/)). So $\Omega_1$, the Schur complement of $m_0$ in $\Omega_{SS}$, is the information matrix of $p(x, m_+ \mid m_-)$, and $\Omega_2$, the Schur complement of $(x, m_0)$ in $\Omega_{SS}$, is that of $p(m_+ \mid m_-)$. The exponent of a ratio of densities is the difference of the exponents, so $\Omega_1 - \Omega_2$ (with $\Omega_2$ placed on the $m_+$ block) is the information matrix of $p(x \mid m_+, m_-)$ as a function of $(x, m_+)$. It does not depend on the value of $m_-$, which shifts only the linear term. $\Omega_3$, the Schur complement of $x$ in $\Omega$, is the information matrix of $p(m)$. The exponent of a product is the sum, so $\tilde\Omega = \Omega_1 - \Omega_2 + \Omega_3$ is the information matrix of $\tilde p$. The test file checks the code against this formula, built from full size matrices, on random cases.

**Claim 1: the links from $x$ to $m_0$ are zero.** $\Omega_1 - \Omega_2$ has entries only in the rows and columns of $x$ and $m_+$, and $\Omega_3$ has no row or column of $x$. So $\tilde\Omega_{x, m_0} = 0$ and $\tilde\Omega_{x, m_-} = 0$. The code writes exact zeros there, to remove the rounding.

**Claim 2: only the block $S \times S$ changes.** $\Omega_1$ and $\Omega_2$ live on $S$. $\Omega_3 = \Omega_{mm} - \Omega_{mx} \Omega_{xx}^{-1} \Omega_{xm}$, and $\Omega_{xm}$ is zero outside the columns of $m_0$ and $m_+$, because of the invariant. So $\Omega_3$ differs from $\Omega_{mm}$ only on $S$.

**Claim 3: $\tilde\Omega$ is positive definite.** $\tilde p$ is the product of a Gaussian conditional with a positive definite conditional covariance and a Gaussian marginal with a positive definite covariance. So it is a proper Gaussian density, and its information matrix is positive definite.

**Claim 4: the mean does not change.** Line L12 sets $\tilde\xi = \xi + (\tilde\Omega - \Omega) \mu$. If $\xi = \Omega \mu$, then $\tilde\xi = \tilde\Omega \mu$, so $\tilde\Omega^{-1} \tilde\xi = \mu$. This agrees with the densities: under $p$, the mean of $x$ given $m_+ = \mu_+$ and $m_- = \mu_-$ is $\mu_x$, and $p(m)$ has the mean $\mu_m$.

**Claim 5: the map marginal is exact.** $\tilde p(m) = \int p(x \mid m_+, \mu_-) \, dx \; p(m) = p(m)$. So the covariance of the landmarks does not change in this step. Only the covariances that involve the pose can change.

**Claim 6: with no passive landmarks, the marginal of $(x, m_+)$ is exact.** If $m_-$ is empty, then $\tilde p(x, m_+) = p(x \mid m_+) \, p(m_+) = p(x, m_+)$. The only change is the dependence between $x$ and $m_0$ given $m_+$, which the step removes.

**Where the approximation is.** If $m_-$ is not empty, the conditional is taken at the fixed value $m_- = \mu_-$ in place of the uncertain $m_-$. For Gaussians, $\mathrm{Cov}(x \mid m_+, m_-) \preceq \mathrm{Cov}(x \mid m_+)$: conditioning on more variables never adds uncertainty. So the step treats the passive landmarks as known when it describes the pose. This does not make every marginal variance of the pose smaller: on random positive definite matrices, the pose variances shrank in only some of the cases that we tried. So the overconfidence of the SEIF is a measurement, not a theorem. Eustice, Walter and Leonard (2005) showed it in experiments for the global map and found the map relative to a local frame close to consistent. The test file measures the same effect: the mean normalized landmark error is larger with a small bound on the active landmarks than without sparsification.

## The mean recovery (line L13)

$\mu^\ast = \Omega^{-1} \xi$ is the unique minimizer of $f(\mu) = \tfrac12 \mu^\top \Omega \mu - \xi^\top \mu$, because $\Omega$ is positive definite. Line L13 solves $\Omega_{bb} \mu_b = \xi_b - \Omega_{b, \bar b} \mu_{\bar b}$ for a block $b$, with the other entries fixed. This sets $\mu_b$ to the minimizer of $f$ over $\mu_b$, because $\Omega_{bb}$ is positive definite. So $f$ never increases, and $\mu^\ast$ is a fixed point. If all blocks are visited in turn on a fixed $\Omega$, this is block Gauss-Seidel on a positive definite system, which converges to $\mu^\ast$ (see the [Gauss-Seidel method](/gauss-seidel-method/)). The rate can be slow when the map is strongly correlated, and the SEIF visits only a few passive blocks per step while $\Omega$ changes. So the mean is an approximation in each step, and its error is not bounded by a theorem.
