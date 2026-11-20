---
title: Correctness of full waveform inversion
proves: [correctness, termination]
status: full
---

**Setting.** The model is a vector $m > 0$ of squared slownesses on the cells of a 1D grid. $L$ is the second difference with zero values outside the grid, a real symmetric matrix; $M = \operatorname{diag}(m)$; $R$ samples a field at the receiver cells. The forward scheme of line L1 is, for $n = 0, \ldots, N - 1$,
$$M(u^{n+1} - 2u^n + u^{n-1}) = \Delta t^2 (L u^n + f^n), \qquad u^0 = u^{-1} = 0,$$
where $f^n$ does not depend on $m$. Put $e^n = u^{n+1} - 2u^n + u^{n-1}$. The data residual is $\mathrm{res}^n = R u^n - d_{\mathrm{obs}}^n$ for $n = 0, \ldots, N$, and the misfit is $J(m) = \frac12 \sum_{n=0}^{N}\|\mathrm{res}^n\|^2$. Each $u^n$ is a rational function of $m$ without poles on $m > 0$, so $J$ is smooth there.

**Theorem 1 (the exact gradient).** Let $\mu^{N+1} = \mu^{N+2} = 0$ and, for $k = N, \ldots, 1$,
$$\mu^k = 2\mu^{k+1} - \mu^{k+2} + \Delta t^2 M^{-1} L \mu^{k+1} + M^{-1} R^{\mathsf T}\,\mathrm{res}^k.$$
Then
$$\frac{\partial J}{\partial m_i} = -\sum_{k=1}^{N} \mu^k_i\, e^{k-1}_i,$$
and the function `gradient` returns $J(m)$ and this vector at line L7.

*Proof.* Differentiate the scheme in a direction $\delta m$, with $\delta u^n$ the derivative of $u^n$. Since $f^n$ is fixed,
$$M(\delta u^{n+1} - 2\delta u^n + \delta u^{n-1}) - \Delta t^2 L\,\delta u^n = -\delta m \odot e^n, \qquad \delta u^0 = \delta u^{-1} = 0.$$
Collect $\delta u = (\delta u^1, \ldots, \delta u^N)$. This is the block lower-triangular system $A\,\delta u = b$ with
$$(A\,\delta u)^k = M(\delta u^k - 2\delta u^{k-1} + \delta u^{k-2}) - \Delta t^2 L\,\delta u^{k-1}, \qquad b^k = -\delta m \odot e^{k-1},$$
for $k = 1, \ldots, N$ (terms with an index below 1 are zero). $A$ has the invertible block $M$ on its diagonal. Its transpose is
$$(A^{\mathsf T}\mu)^k = M(\mu^k - 2\mu^{k+1} + \mu^{k+2}) - \Delta t^2 L\,\mu^{k+1},$$
with $\mu^{N+1} = \mu^{N+2} = 0$, because $M$ is diagonal and $L$ is symmetric. The recursion of the theorem is $A^{\mathsf T}\mu = (R^{\mathsf T}\mathrm{res}^k)_{k=1}^{N}$ solved for $\mu^k$ from $k = N$ down to 1. The derivative of $J$ is
$$\delta J = \sum_{n=0}^{N}\langle \mathrm{res}^n, R\,\delta u^n\rangle = \sum_{k=1}^{N}\langle R^{\mathsf T}\mathrm{res}^k, \delta u^k\rangle = \langle A^{\mathsf T}\mu, \delta u\rangle = \langle \mu, A\,\delta u\rangle = -\sum_{k=1}^{N}\langle \mu^k, \delta m \odot e^{k-1}\rangle,$$
where the term $n = 0$ is 0 because $\delta u^0 = 0$. Read off the coefficient of $\delta m_i$.

Now the code. Line L1 runs the scheme and stores $u^0, \ldots, u^N$. Line L2 forms $\mathrm{res}^n$, and $J$ is computed from it. Line L3 sets $\mu^{N+1} = \mu^{N+2} = 0$. Loop invariant: at the start of the pass for $k$ at line L4, `lam1` $= \mu^{k+1}$, `lam2` $= \mu^{k+2}$, and `g` $= -\sum_{k' > k}\mu^{k'} \odot e^{k'-1}$. In the pass, line L4 computes $2\mu^{k+1} - \mu^{k+2} + \Delta t^2 M^{-1}L\mu^{k+1}$, and line L5 adds $M^{-1}R^{\mathsf T}\mathrm{res}^k$ (a cell that holds two receivers gets both terms, as $R^{\mathsf T}$ requires), so `lam` $= \mu^k$. Line L6 subtracts $\mu^k \odot (u^k - 2u^{k-1} + u^{k-2}) = \mu^k \odot e^{k-1}$, with $u^{-1} = 0$ for $k = 1$. The shift gives the invariant for $k - 1$. After $N$ passes, line L7 returns $J$ and the full sum. $\blacksquare$

So the gradient costs one forward and one backward propagation, whatever the number of cells. It is the gradient of the discrete misfit, so a central-difference check agrees with it up to the truncation and rounding error of the check.

**Theorem 2 (the descent loop).** In `full_waveform_inversion`, every accepted model is positive, the list of misfits is non-increasing, and the loop stops after at most `iters` gradient evaluations and $30 \cdot$ `iters` $+ 1$ extra forward runs. If $g \ne 0$, the Armijo condition $J(m - a g) \le J(m) - c\,a\|g\|^2$ with $c = 10^{-4}$ holds for every small enough $a > 0$.

*Proof.* A trial is accepted only if all its entries are positive and $J(\text{trial}) \le J(m) - c\,a\|g\|^2 \le J(m)$. If no trial is accepted in 30 halvings, the loop stops with $m$ unchanged. So consecutive entries of the history do not increase, and the last entry is $J$ of the returned model. The counts follow from the two loop bounds. For the last claim, $J$ is smooth near $m > 0$, so $J(m - ag) = J(m) - a\|g\|^2 + o(a)$, which is below $J(m) - c\,a\|g\|^2$ for small $a$ since $c < 1$; also $m - ag > 0$ for small $a$. $\square$

**What is not claimed.** Theorem 2 gives decrease, not convergence to the true model. $J$ is not convex in $m$: if the predicted arrival differs from the observed one by more than about half a period, the descent moves toward a wrong local minimum (cycle skipping). The test with a constant true velocity of 2000 m/s shows such a minimum near 1625 m/s. Starting from a good model, or inverting the low frequencies first, are heuristics that reduce this risk, not theorems. The 30 halvings may also end before the Armijo condition holds, and then the loop stops early.
