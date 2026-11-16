---
title: For a permutation-invariant kernel the Gram matrix of all cyclic shifts is circulant, so the Fourier formulas of the kernelized correlation filter give exactly the kernel ridge regression solution and its responses
proves: [correctness]
status: full
---

Notation as on the page. Patches are real arrays on the group $G = \mathbb{Z}_r \times \mathbb{Z}_c$ of size $P = r c$, the shift is $(S_d x)(t) = x(t - d)$, and the DFT is $\hat a(k) = \sum_{s \in G} a(s) \omega_k(s)$ with the characters $\omega_k(s) = e^{-2\pi i (k_1 s_1 / r + k_2 s_2 / c)}$; the inverse has the factor $1/P$. A kernel $\kappa$ is symmetric and positive semidefinite, and it is **permutation invariant** for the shifts if $\kappa(S_d a, S_d b) = \kappa(a, b)$ for all $a$, $b$ and $d$.

## Claim 1: the Gram matrix of the shifts is circulant

Let $K_{d e} = \kappa(S_d x, S_e x)$ for $d, e \in G$. If $\kappa$ is permutation invariant, then $K_{d e} = k(e - d)$ with $k(s) = \kappa(x, S_s x)$.

*Proof.* $S_{-d} S_d = \mathrm{Id}$ and $S_{-d} S_e = S_{e - d}$, so $\kappa(S_d x, S_e x) = \kappa(S_{-d} S_d x, S_{-d} S_e x) = \kappa(x, S_{e-d} x)$. $\square$

The Gaussian kernel $\exp(-|a - b|^2 / (\sigma^2 P))$ and the linear kernel $\langle a, b \rangle / P$ are permutation invariant, because a shift permutes the entries and does not change a norm or an inner product. A kernel that weights pixel positions differently is not, and its Gram matrix is not circulant; the tests check both cases.

Also $k(-s) = \kappa(x, S_{-s} x) = \kappa(S_s x, x) = \kappa(x, S_s x) = k(s)$ by invariance and symmetry, so $k$ is even and $\hat k$ is real.

## Claim 2: the DFT diagonalizes a circulant matrix

For $(K a)(d) = \sum_e k(e - d)\, a(e)$, the transform is $\widehat{K a} = \hat k \odot \hat a$ when $k$ is even.

*Proof.* $(K a)(d) = \sum_e k(d - e) a(e)$ since $k$ is even, which is the circular convolution of $k$ and $a$. By the convolution theorem, $\widehat{k * a} = \hat k \odot \hat a$: substitute $s = d - e$ in $\sum_d \sum_e k(d - e) a(e) \omega_k(d)$ and use $\omega_k(s + e) = \omega_k(s) \omega_k(e)$. $\square$

So the eigenvalues of $K$ are the values $\hat k(\ell)$, $\ell \in G$, with the characters as eigenvectors. Because $K$ is positive semidefinite (a Gram matrix of a positive semidefinite kernel), every $\hat k(\ell) \ge 0$.

## Claim 3: the training formula gives the ridge regression coefficients

Kernel ridge regression on the samples $S_d x$ with labels $y(d)$ has the dual coefficients $\alpha = (K + \lambda I)^{-1} y$ for $\lambda > 0$. Then

$$
\hat \alpha = \frac{\hat y}{\hat k + \lambda} .
$$

*Proof.* By Claim 2, $(K + \lambda I) \alpha = y$ becomes $(\hat k + \lambda) \odot \hat \alpha = \hat y$ after the DFT, which is one to one. Each $\hat k(\ell) + \lambda \ge \lambda > 0$, so the division is defined and the solution is unique. $\square$

Lines L3 and L4 compute exactly this, with $k$ from line L1 and line L2.

## Claim 4: lines L1 and L2 compute the kernel at every shift

$\sum_t z(t) x(t - s) = \sum_{t'} z(t' + s) x(t')$, the circular correlation of $z$ with $x$ at $s$, has the transform $\hat z \odot \overline{\hat x}$ (the correlation theorem, proved on the [MOSSE filter](/mosse-filter/) page; $x$ is real). So line L1 gives $c(s) = \langle z, S_s x \rangle$ for every $s$. For the linear kernel $\kappa(z, S_s x) = c(s) / P$. For the Gaussian kernel $|z - S_s x|^2 = |z|^2 + |S_s x|^2 - 2 c(s) = |z|^2 + |x|^2 - 2 c(s)$, which is line L2. The clamp at 0 only removes negative rounding errors. $\square$

## Claim 5: the detection formula gives the regression value at every shift of the test patch

The regression function is $f(w) = \sum_e \alpha(e) \kappa(w, S_e x)$. The response is $\text{resp}(d) = f(S_{-d} z)$. With $k_z(s) = \kappa(z, S_s x)$ and permutation invariance, $\kappa(S_{-d} z, S_e x) = \kappa(z, S_{d + e} x) = k_z(d + e)$, so

$$
\text{resp}(d) = \sum_e \alpha(e)\, k_z(d + e),
$$

the circular correlation of $k_z$ with $\alpha$. Its transform is $\hat k_z \odot \overline{\hat \alpha}$, which is line L6. Since $y$ and $k$ are even, $\alpha$ is even and real, so $\hat \alpha$ is real and the conjugate changes nothing. $\square$

**Consequence for tracking.** If $z = S_d x$ exactly, then $S_{-d} z = x$, so $\text{resp}(d) = f(x)$, the fitted value at the unshifted training sample, which is near the label peak $y(0) = 1$ for small $\lambda$. This is why line L8 moves the target by the position of the peak.

## Claim 6: with the linear kernel the dual solution equals primal ridge regression

Let $\Phi$ be the $P \times P$ matrix whose rows are $\phi(S_d x) = S_d x / \sqrt P$. The primal solution $w = (\Phi^{\mathsf T} \Phi + \lambda I)^{-1} \Phi^{\mathsf T} y$ and the dual $\alpha = (\Phi \Phi^{\mathsf T} + \lambda I)^{-1} y$ satisfy $w = \Phi^{\mathsf T} \alpha$, and so $w^{\mathsf T} \phi(u) = \sum_e \alpha(e) \kappa(u, S_e x)$ for every patch $u$.

*Proof.* $\Phi^{\mathsf T} (\Phi \Phi^{\mathsf T} + \lambda I) = (\Phi^{\mathsf T} \Phi + \lambda I) \Phi^{\mathsf T}$. Both matrices in parentheses are invertible for $\lambda > 0$; multiply on the left by $(\Phi^{\mathsf T} \Phi + \lambda I)^{-1}$ and on the right by $(\Phi \Phi^{\mathsf T} + \lambda I)^{-1}$ and apply to $y$. Then $w^{\mathsf T} \phi(u) = \alpha^{\mathsf T} \Phi \phi(u) = \sum_e \alpha(e) \langle \phi(S_e x), \phi(u) \rangle$. $\square$

## What is not claimed

The claims are exact statements about the training set of all cyclic shifts. Real motion is not a cyclic shift: a moved target brings new background in at one side, and the cosine window and the padding around the target only reduce the effect. So the claim that the peak of the response is at the displacement of the target is a heuristic. The running averages of the model (line L10) are a heuristic too: unlike the MOSSE update, the average of two $\hat \alpha$ arrays is not the solution of a single regression problem.
