---
title: CMA-ES keeps C positive definite, has standard paths under random selection, and is invariant under monotone changes of f and orthogonal maps
proves: [correctness]
status: full
---

We use the pseudocode of the page. Generation $t$ starts with $(m, \sigma, C, p_\sigma, p_c)$ and draws independent $z_1, \dots, z_\lambda \sim \mathcal{N}(0, I)$. The weights satisfy $w_1 \ge \dots \ge w_\mu > 0$ and $\sum w_i = 1$, and $\mu_{\mathrm{eff}} = 1/\sum w_i^2$.

**Claim 1 ($C$ stays symmetric positive definite).** If $c_1 \ge 0$, $c_\mu \ge 0$ and $c_1 + c_\mu < 1$, then every $C$ is symmetric positive definite.

*Proof.* By induction on $t$. The start $C = I$ is symmetric positive definite. Assume $C$ is, and let $C'$ be the matrix after line L8. The coefficient $a = 1 - c_1 - c_\mu + \delta$ is positive, because $\delta \ge 0$ and $c_1 + c_\mu < 1$. Each matrix $p_c p_c^\top$ and $y y^\top$ is symmetric, so $C'$ is symmetric. For $v \ne 0$,
$$v^\top C' v = a\, v^\top C v + c_1 (p_c^\top v)^2 + c_\mu \sum_{i=1}^{\mu} w_i (y_{i:\lambda}^\top v)^2 \ge a\, v^\top C v > 0,$$
since the last two terms are not negative and $v^\top C v > 0$. So $C'$ is positive definite. $\square$

The defaults satisfy the condition: $c_1 = 2/((n + 1.3)^2 + \mu_{\mathrm{eff}})$ and $c_\mu = \min\bigl(1 - c_1, 2(\mu_{\mathrm{eff}} - 2 + 1/\mu_{\mathrm{eff}})/((n + 2)^2 + \mu_{\mathrm{eff}})\bigr)$, and the tests check $c_1 + c_\mu < 1$ for $n = 1, \dots, 40$. In floating point, the implementation computes one half of $C$ and copies it, so $C$ is exactly symmetric, and the tests check that a Cholesky factorization succeeds at every generation of several runs.

**Claim 2 (the paths under random selection).** Assume that the ranks in line L4 do not depend on the samples, for example because $f$ is constant and ties are broken by a random permutation that is independent of the $z_k$. Then $C^{-1/2} y_w \sim \mathcal{N}(0, I/\mu_{\mathrm{eff}})$. If also $p_\sigma \sim \mathcal{N}(0, I)$ before line L6, independent of the new samples, then $p_\sigma \sim \mathcal{N}(0, I)$ after it.

*Proof.* Line L3 sets $y_k = B D z_k$, so $C^{-1/2} y_k = B D^{-1} B^\top B D z_k = B z_k$, and $B z_k \sim \mathcal{N}(0, I)$ since $B$ is orthogonal. The selected indices are a fixed set given the independent ranking, so $C^{-1/2} y_w = \sum_{i=1}^{\mu} w_i B z_{i:\lambda}$ is a sum of independent Gaussians with mean 0 and covariance $\sum w_i^2 I = I/\mu_{\mathrm{eff}}$. Then $p_\sigma' = (1 - c_\sigma) p_\sigma + \sqrt{c_\sigma(2 - c_\sigma)\mu_{\mathrm{eff}}}\, C^{-1/2} y_w$ is Gaussian with mean 0 and covariance $\bigl((1 - c_\sigma)^2 + c_\sigma(2 - c_\sigma)\bigr) I = I$. $\square$

So in that stationary state $E\lVert p_\sigma \rVert = \chi_n$, and the exponent in line L9 has the mean 0. The step size changes in a systematic way only because of selection: it grows when selected steps are correlated over generations, which makes $p_\sigma$ longer than a random path, and it shrinks when they cancel.

**Claim 3 (increasing transformations of $f$).** Let $g$ be strictly increasing. With the same random numbers and the same rule for ties, the runs on $f$ and on $g \circ f$ give the same states $(m, \sigma, C, p_\sigma, p_c)$ in every generation.

*Proof.* By induction on $t$. If the states are the same at the start of generation $t$, line L3 gives the same $z_k$, $y_k$ and $x_k$. Since $g(f(x)) < g(f(x'))$ holds if and only if $f(x) < f(x')$, and $g(f(x)) = g(f(x'))$ if and only if $f(x) = f(x')$, the sort in line L4 gives the same order. Lines L5 to L10 use only the $y_k$ in that order and the old state, never the values of $f$, so the new states are equal. The best point seen is chosen by comparisons too, so it is the same. $\square$

**Claim 4 (translations and orthogonal maps).**

1. With the same random numbers, the run on $f_c(x) = f(x - c)$ from $m_0 + c$ has the states $(m + c, \sigma, C, p_\sigma, p_c)$, where $(m, \sigma, C, p_\sigma, p_c)$ are the states of the run on $f$ from $m_0$.
2. Let $Q$ be orthogonal and $f_Q(x) = f(Q^\top x)$. The run on $f_Q$ from $Q m_0$ has the same distribution as the sequence $(Q m, \sigma, Q C Q^\top, Q p_\sigma, Q p_c)$ built from the run on $f$ from $m_0$.

*Proof.* Part 1. The samples are $m + c + \sigma y_k = x_k + c$, with the same $y_k$, and $f_c(x_k + c) = f(x_k)$, so the order is the same, $y_w$ is the same, the mean becomes $m + \sigma y_w + c$, and lines L6 to L10 do not involve $m$, so they give the same values.

Part 2. We show that if the state of the run on $f_Q$ is $(Q m, \sigma, Q C Q^\top, Q p_\sigma, Q p_c)$ at the start of a generation, then the next state has the same form, when the new samples are coupled suitably. Let $C = B D^2 B^\top$. Then $Q C Q^\top = (Q B) D^2 (Q B)^\top$ is an eigendecomposition with the orthogonal matrix $Q B$. The eigendecomposition is not unique, so the run on $f_Q$ may use a different orthogonal $B'$ with $Q C Q^\top = B' D^2 B'^\top$; but then $B' D z$ with $z \sim \mathcal{N}(0, I)$ has the distribution $\mathcal{N}(0, Q C Q^\top)$, the same as $Q B D z$, so we may couple the samples so that $y_k' = Q y_k$ for all $k$. The new points are $Q m + \sigma Q y_k = Q x_k$, and $f_Q(Q x_k) = f(x_k)$, so the order is the same and $y_w' = Q y_w$. Line L5 gives $Q m + \sigma Q y_w = Q(m + \sigma y_w)$. The symmetric root satisfies $(Q C Q^\top)^{-1/2} = Q C^{-1/2} Q^\top$, because the right side is symmetric positive definite and its square is $Q C^{-1} Q^\top$. So line L6 gives $(1 - c_\sigma) Q p_\sigma + a\, Q C^{-1/2} Q^\top Q y_w = Q p_\sigma'$, with $a$ the constant of L6. Since $\lVert Q p_\sigma' \rVert = \lVert p_\sigma' \rVert$, the flag $h_\sigma$ and the factor in line L9 are the same, so $\sigma$ is the same. Line L7 gives $Q p_c'$. In line L8, $(Q p_c)(Q p_c)^\top = Q p_c p_c^\top Q^\top$ and $(Q y)(Q y)^\top = Q y y^\top Q^\top$, so the new matrix is $Q C' Q^\top$. By induction over the generations, the coupled runs have the stated form at every generation, which proves the claim about the distributions. $\square$

Part 2 is about distributions, not single runs, because the two runs may choose different eigenvectors for the same $C$. The tests check part 1 and Claim 3 exactly for a fixed seed, and the measurement on the page compares the two distributions of part 2 for a tilted and an axis-parallel ellipse.
