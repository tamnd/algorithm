---
title: Correctness of reverse-time migration
proves: [correctness, termination]
status: full
---

**Setting.** Grid fields are vectors indexed by the grid points. $L$ is the 5-point Laplacian with zero values outside the grid; it is a real symmetric matrix. $m$ is the background squared slowness, $W = \operatorname{diag}(\Delta t^2/m)$, and $R$ samples a field at the receivers, so $R^{\mathsf T}$ puts a receiver vector back at the receiver points. The background field $u_0$ solves the scheme
$$m \odot (u_0^{n+1} - 2u_0^n + u_0^{n-1}) = \Delta t^2 (L u_0^n + f^n), \qquad u_0^0 = u_0^{-1} = 0,$$
for $n = 0, \ldots, N - 1$, and $g^n = (u_0^{n+1} - 2u_0^n + u_0^{n-1})/\Delta t^2$ is its second time difference (the array `d2u0`). Born modeling $B$ maps a perturbation $\delta m$ to the data $(R\,u^n)_{n=0}^{N}$ of the scheme
$$u^{n+1} = 2u^n - u^{n-1} + W(L u^n + s^n), \qquad s^n = -\delta m \odot g^n, \qquad u^0 = u^{-1} = 0.$$
Dot products are the plain sums over all entries.

**Lemma 1 (Born modeling is the exact derivative).** Let $F(m)$ be the receiver data of the scheme for $u_0$ as a function of $m$. Then $F'(m)\,\delta m = B\,\delta m$.

*Proof.* Differentiate the scheme in the direction $\delta m$, with $\delta u^n$ the derivative of $u_0^n$: $\delta m \odot (u_0^{n+1} - 2u_0^n + u_0^{n-1}) + m \odot (\delta u^{n+1} - 2\delta u^n + \delta u^{n-1}) = \Delta t^2 L\,\delta u^n$, because $f$ does not depend on $m$. Divide by $m$: $\delta u^{n+1} = 2\delta u^n - \delta u^{n-1} + W(L\,\delta u^n - \delta m \odot g^n)$, with zero initial values. This is the Born scheme, and $R$ is linear. $\square$

So migration with the adjoint of $B$ is the adjoint of the linearized forward map of the same discrete model; no continuous approximation is involved.

**Theorem 1 (exact adjoint).** For every data set $y = (y^n)_{n=0}^{N}$, the array returned at line L7 is
$$B^{\mathsf T} y = -\sum_{n=1}^{N} g^{n-1} \odot W\lambda^n,$$
where $\lambda^{N+1} = \lambda^{N+2} = 0$ and, for $n = N, \ldots, 1$,
$$\lambda^n = R^{\mathsf T} y^n + 2\lambda^{n+1} + L(W\lambda^{n+1}) - \lambda^{n+2}.$$
So $\langle B\,\delta m, y\rangle = \langle \delta m, \mathrm{RTM}(y)\rangle$ for all $\delta m$ and $y$.

*Proof.* Collect $u = (u^1, \ldots, u^N)$. The Born scheme is the block lower-triangular system $A u = W s$, where
$$(A u)^k = u^k - (2I + WL)\,u^{k-1} + u^{k-2}, \qquad k = 1, \ldots, N,$$
with $u^0 = u^{-1} = 0$ and $(Ws)^k = W s^{k-1}$. $A$ has the identity on its block diagonal, so it is invertible. Its transpose is block upper triangular,
$$(A^{\mathsf T}\lambda)^k = \lambda^k - (2I + WL)^{\mathsf T}\lambda^{k+1} + \lambda^{k+2} = \lambda^k - 2\lambda^{k+1} - L W \lambda^{k+1} + \lambda^{k+2},$$
with $\lambda^{N+1} = \lambda^{N+2} = 0$, because $(WL)^{\mathsf T} = L^{\mathsf T}W^{\mathsf T} = LW$ ($L$ symmetric, $W$ diagonal). So the recursion for $\lambda$ is the solution of $A^{\mathsf T}\lambda = (R^{\mathsf T}y^k)_{k=1}^{N}$, solved from $k = N$ down to $k = 1$. Now, with $u^0 = 0$,
$$\langle B\,\delta m, y\rangle = \sum_{k=1}^{N}\langle u^k, R^{\mathsf T} y^k\rangle = \langle u, A^{\mathsf T}\lambda\rangle = \langle A u, \lambda\rangle = \sum_{k=1}^{N}\langle W s^{k-1}, \lambda^k\rangle = \Big\langle \delta m,\; -\sum_{k=1}^{N} g^{k-1} \odot W\lambda^k\Big\rangle,$$
where the last step uses $W$ diagonal and $s^{k-1} = -\delta m \odot g^{k-1}$.

It remains to match the code. Line L1 sets $N$. Line L2 sets the two stored fields to $\lambda^{N+1} = \lambda^{N+2} = 0$. Loop invariant: at the start of the pass for $n$ at line L3, `lam1` $= \lambda^{n+1}$, `lam2` $= \lambda^{n+2}$, and `image` $= -\sum_{k=n+1}^{N} g^{k-1}\odot W\lambda^k$. It holds for $n = N$. In the pass, line L4 computes $2\lambda^{n+1} + L(W\lambda^{n+1}) - \lambda^{n+2}$ and line L5 adds $R^{\mathsf T} y^n$, so `lam` $= \lambda^n$; line L6 subtracts $g^{n-1}\odot W\lambda^n$; the shift of the stored fields gives the invariant for $n - 1$. The loop has $N$ passes, so it stops, and line L7 returns the sum for $k = 1, \ldots, N$. The sample $y^0$ is not used, which is right because $u^0 = 0$. $\blacksquare$

**Corollary (the imaging condition).** The image is a zero-lag cross-correlation, summed over time, of the second time difference of the source field and the receiver field $\lambda$ propagated backward in time, weighted by $\Delta t^2/m$. This is the cross-correlation imaging condition applied to the data residual or to the data. For several shots, $B$ stacks the shot operators, so the adjoint is the sum of the shot images.

**What is not claimed.** $B^{\mathsf T}$ is not the inverse of $B$; amplitudes and the low-wavenumber artifacts of the correlation are not corrected (least-squares migration does that). The edges of the grid reflect waves, since $u = 0$ outside the grid; the adjoint statement holds with these edges, and it also holds with an absorbing layer if the same layer is used in both directions. Stability of the forward scheme needs the CFL condition $v\,\Delta t/h \le 1/\sqrt{2}$; with $\mu^n = W\lambda^n$ the backward recursion reads $\mu^n = 2\mu^{n+1} - \mu^{n+2} + W(L\mu^{n+1} + R^{\mathsf T}y^n)$, which is the forward scheme run backward in time, so it is stable under the same condition.
