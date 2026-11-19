---
title: The exact steps of the toy HMM synthesizer, durations of highest likelihood and the MLPG trajectory
proves: [correctness]
status: full
---

The full system has no single correct output, so this note proves the two steps that are exact for the model, and states what the toy code does around them. The code is a toy: one-dimensional streams, hand-made trees, dense linear algebra and a first-order filter as the vocoder.

## Durations (line L5)

Fix $N \ge 1$ states with duration means $m_k$ and variances $v_k > 0$, and a total $T$. Over real vectors $d$ with $\sum_k d_k = T$, maximize

$$\ell(d) = \sum_{k=1}^{N} \Bigl( -\tfrac{1}{2} \log (2 \pi v_k) - \frac{(d_k - m_k)^2}{2 v_k} \Bigr).$$

**Theorem 1.** The unique maximizer is $d_k = m_k + \rho v_k$ with $\rho = (T - \sum_k m_k) / \sum_k v_k$.

*Proof.* The function $\ell$ is a sum of strictly concave quadratics, so it is strictly concave, and the constraint set is an affine subspace. A point of that subspace is the unique maximum if and only if the gradient of $\ell$ there is orthogonal to the subspace, that is, all partial derivatives $-(d_k - m_k) / v_k$ are equal to one number $\rho$. This gives $d_k = m_k + \rho v_k$, and summing over $k$ gives $\sum_k m_k + \rho \sum_k v_k = T$, which fixes $\rho$. $\square$

With $\rho = 0$ the rule returns the means, the unconstrained maximum. Integer vectors with the same total form a subset of the real ones, so their likelihood is at most $\ell$ at the real maximizer; the tests check this against every integer vector for small $N$ and $T$. The code rounds each $d_k$ and raises it to at least 1, so the integer result is close to, but not always equal to, the best integer vector.

## Trajectory (lines L8 and L9)

For a fixed frame sequence with static means $\mu^s_t$, variances $v^s_t$, delta means $\mu^d_t$ and variances $v^d_t$, and the clamped delta window $\Delta c_t = \frac{1}{2}(c_{\min(t+1, T-1)} - c_{\max(t-1, 0)})$, the objective

$$J(c) = -\sum_{t} \Bigl( \frac{(c_t - \mu^s_t)^2}{2 v^s_t} + \frac{(\Delta c_t - \mu^d_t)^2}{2 v^d_t} \Bigr)$$

is a concave quadratic $-\frac{1}{2} c^\top P c + r^\top c + \text{const}$ with $P = \sum_{\text{rows}} w w^\top / v$ and $r = \sum_{\text{rows}} w \mu / v$, summed over the static and delta rows that the code builds.

**Theorem 2.** If all static variances are finite and positive, $P$ is positive definite and the unique maximizer of $J$ is $c^* = P^{-1} r$, which the code returns.

*Proof.* The static rows alone give the diagonal matrix with entries $1 / v^s_t > 0$, and the delta rows add positive semidefinite terms, so $P$ is positive definite. The gradient of $J$ is $r - P c$, which vanishes only at $c^* = P^{-1} r$, and strict concavity makes it the maximum. Gaussian elimination with partial pivoting solves $P c = r$ for any nonsingular $P$. $\square$

The code builds $P$ and $r$ from exactly these rows, so it maximizes $J$. The tests check the page example $(0.2, 0.3, 0.3, 0.7, 0.7, 0.8)$ and that random perturbations of the result lower $J$. When every row has infinite variance, $P = 0$ and the code raises an error. Line L9 applies the same solve to each run of voiced frames alone, which is the maximization of the same objective restricted to that run.

## The rest

Lines L1 to L4 and L6 are lookups and copies: each phone gets 5 states, each state gets the leaves its context reaches in each tree, and each state is copied $d_k$ times, so there are $\sum_k d_k$ frames. Lines L10 and L11 make $T \cdot \text{hop}$ samples from the excitation and the filter, with the filter coefficient clamped to $[-0.99, 0.99]$ so that it is stable.
