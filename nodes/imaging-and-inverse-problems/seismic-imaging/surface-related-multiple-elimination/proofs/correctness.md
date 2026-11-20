---
title: Under the surface-multiple model P = P0 + a P0 P the data without surface multiples are P (I + a P)^(-1), the iteration gives the partial sums of a Neumann series that converge exactly when the spectral radius of aP is below 1, and the first prediction is the multidimensional autoconvolution of the data
proves: [correctness]
status: full
---

**Setting.** Fix one frequency $\omega$. The data form a complex $N \times N$ matrix $P$: entry $(i, j)$ is the spectrum at $\omega$ of the trace recorded at surface position $i$ from a source at surface position $j$, on one grid for sources and receivers. The surface operator $a$ is a complex number; it holds the reflection coefficient of the free surface, the inverse of the source spectrum and the step of the sum over surface positions. The data without surface multiples, $P_0$, are linked to $P$ by the model
$$P = P_0 + a P_0 P. \tag{M}$$
(M) is the feedback model of Verschuur, Berkhout and Wapenaar (1992), with the surface and source terms folded into one scalar: every surface multiple is a full event of $P$ from the source to some surface position $l$, a reflection there with the factor $a$, and an event of $P_0$ from $l$ to the receiver. The product $P_0 P$ sums over $l$. We take (M) as given; the claims are about what follows from it. The function srme_direct solves $X (I + aP) = P$ for $X$; lines L2 to L4 compute $P_0^{(0)} = P$ and $P_0^{(k+1)} = P - a P_0^{(k)} P$. $\rho(\cdot)$ is the spectral radius.

**Claim 1 (direct solution).** If $I + aP$ is invertible, (M) has exactly one solution, $P_0 = P (I + aP)^{-1}$. Conversely, for any $P_0$ with $I - aP_0$ invertible, the data $P = (I - aP_0)^{-1} P_0$ satisfy (M), and then $I + aP = (I - aP_0)^{-1}$ is invertible and srme_direct returns $P_0$.

*Proof.* (M) is $P_0 (I + aP) = P$, which has the one solution $P (I + aP)^{-1}$ when $I + aP$ is invertible. For the converse, $(I - aP_0)P = P_0$ gives $P = P_0 + aP_0 P$, which is (M). Since $P_0$ commutes with $I - aP_0$, also $P = P_0 (I - aP_0)^{-1}$, and $I + aP = \big((I - aP_0) + aP_0\big)(I - aP_0)^{-1} = (I - aP_0)^{-1}$. $\square$

So the direct form recovers $P_0$ exactly whenever the data obey (M), however strong the multiples are. The function add_surface_multiples, used in the tests, is the map of the converse.

**Claim 2 (the iteration gives the Neumann partial sums).** For every $k \ge 0$,
$$P_0^{(k)} = \sum_{j=0}^{k} (-a)^j P^{j+1}, \qquad P_0^{(k)} - P_0 = (-1)^k a^{k+1} P_0 P^{k+1},$$
where the second formula assumes (M).

*Proof.* For $k = 0$ the sum is $P$. If the formula holds for $k$, then $P - a P_0^{(k)} P = P + \sum_{j=0}^{k} (-a)^{j+1} P^{j+2}$, which is the sum for $k + 1$. For the error $E_k = P_0^{(k)} - P_0$, subtract (M), written as $P_0 = P - aP_0P$, from the iteration: $E_{k+1} = -a E_k P$. And $E_0 = P - P_0 = aP_0P$ by (M). So $E_k = (-a)^k a P_0 P^{k+1}$. $\square$

**Claim 3 (convergence).** If $\rho(aP) < 1$, then $P_0^{(k)} \to P_0$, and for every $\varepsilon > 0$ the error is $O((\rho(aP) + \varepsilon)^k)$. For $N = 1$ and $P_0 \ne 0$, the iteration converges if and only if $|aP| < 1$.

*Proof.* $E_k = (-1)^k P_0 (aP)^{k+1}$ by Claim 2, and $\|(aP)^k\| = O((\rho(aP) + \varepsilon)^k)$ for every $\varepsilon > 0$ by Gelfand's formula $\rho(B) = \lim_k \|B^k\|^{1/k}$. For $N = 1$, $|E_k| = |P_0|\,|aP|^{k+1}$, which tends to $0$ if and only if $|aP| < 1$. $\square$

**Claim 4 (when the iteration converges).** Let $P$ be given by $P_0$ as in Claim 1. Then $\rho(aP) < 1$ if and only if every eigenvalue $\lambda$ of $aP_0$ has real part below $1/2$.

*Proof.* $aP = aP_0 (I - aP_0)^{-1}$ is the rational function $g(\lambda) = \lambda/(1 - \lambda)$ of $aP_0$, and $g$ has no pole on the spectrum of $aP_0$ because $I - aP_0$ is invertible. By the spectral mapping theorem the eigenvalues of $aP$ are the $g(\lambda)$. Now $|g(\lambda)| < 1$ if and only if $|\lambda|^2 < |1 - \lambda|^2 = 1 - 2\,\mathrm{Re}\,\lambda + |\lambda|^2$, that is $\mathrm{Re}\,\lambda < 1/2$. $\square$

For one flat reflector with coefficient $r$ under a free surface with coefficient $-1$ and a unit impulse source, $P_0 = r z$ with $z = e^{-i\omega\tau}$ and $a = -1$, so $aP_0 = -rz$. At the frequencies with $z = -1$ this is $r$, so the iteration converges at every frequency if and only if $r < 1/2$, and the worst rate is $|aP| = r/(1 - r)$, which is $2/3$ for $r = 0.4$. For $r \ge 1/2$ the direct form of Claim 1 still works.

**Claim 5 (the first prediction).** The first step is $P_0^{(1)} = P - a P^2$, and the time-domain trace of $(P^2)_{ij}$ is $\sum_l p_{il} * p_{lj}$, the convolution in time of the trace from $j$ to $l$ with the trace from $l$ to $i$, summed over the surface positions $l$. For $N = 1$ it is the autoconvolution of the trace (circular on the periodic time axis of the code).

*Proof.* $(P^2)_{ij} = \sum_l P_{il} P_{lj}$ at every frequency; by the convolution theorem of the DFT the product of spectra is the spectrum of the circular convolution of the traces, and the inverse DFT is linear. $\square$

In the one-reflector case the data trace has $(-1)^{m+1} r^m$ at time $m\tau$ (the multiple of order $m - 1$), and the trace of $P^2 = r^2 z^2 / (1 + rz)^2$ has $(-1)^m (m - 1) r^m$ there. So $P + P^2$ has $(-1)^{m+1}(2 - m) r^m$: the first-order multiple ($m = 2$) is removed exactly, the primary is kept, and the higher orders remain with changed amplitudes. The later terms of the series correct them.

**Claim 6 (the least-squares scalar).** The function estimate_surface_scalar returns the $s$ that minimizes $\sum_k \|P_k - s M_k\|_F^2$ over complex $s$, namely $s = \sum_k \langle M_k, P_k\rangle / \sum_k \|M_k\|_F^2$, where $\langle M, P\rangle = \sum_{ij} \overline{M_{ij}} P_{ij}$.

*Proof.* The function is $\|P\|^2 - 2\,\mathrm{Re}(\bar s \langle M, P\rangle) + |s|^2 \|M\|^2$, summed over $k$; completing the square in $s$ gives the minimizer. $\square$

The claim is about the formula. That the minimum-energy scalar equals the true $-a$ is not a theorem: the primaries left in $P_k$ are not orthogonal to the prediction, and the rule pulls the scalar toward a value that also removes part of them. This is why adaptive subtraction is a heuristic.

**Claim 7 (cost).** With $n_f$ frequencies and $N$ surface positions, the direct form costs $O(n_f N^3)$ and $K$ steps of the iteration cost $O(n_f K N^3)$ with dense products, plus the transforms of the $N^2$ traces.

*Proof.* Each frequency needs one dense solve with $N$ right-hand sides, $O(N^3)$, or $K$ products of $N \times N$ matrices, $O(N^3)$ each. $\square$
