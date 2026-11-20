---
title: The frequency-domain solve returns the unique damped least-squares parabolic Radon model of the gather, the forward and adjoint operators are a pair, and the multiple prediction and the primaries add up to the data
proves: [correctness]
status: full
---

**Setting.** A gather has $n_x$ real traces $d_i$ at offsets $x_i$, each with $n$ samples at times $t\,\Delta t$, $t = 0, \ldots, n - 1$, and $n$ is odd. A model has $n_q$ real traces $m_j$ for the curvatures $q_j$. The DFT is $D_i[k] = \sum_t d_i[t]\, e^{-2\pi i t k/n}$ and the inverse has the factor $1/n$. For a bin $k$ let $k_s$ be the signed index, $k$ if $k \le n/2$ and $k - n$ otherwise, and $\omega_k = 2\pi k_s/(n \Delta t)$. Because $n$ is odd, there is no bin with $k_s = n/2$, and $\omega_{n-k} = -\omega_k$ for every $k \ne 0$. Line L3 forms the $n_x \times n_q$ matrix $(L_k)_{ij} = e^{-i\omega_k q_j x_i^2}$. The forward operator $L$ maps a model to the gather with spectra $L_k M_k$, where $M_k = (M_1[k], \ldots, M_{n_q}[k])^T$; the function adjoint maps a gather to the model with spectra $L_k^H D_k$. A family of vectors $(Z_k)$ is conjugate symmetric if $Z_{n-k} = \overline{Z_k}$ for all $k$ and $Z_0$ is real; the spectra of real signals are exactly the conjugate symmetric families. The inner product of real gathers or models is $\langle a, b\rangle = \sum a\, b$ over all traces and samples.

**Claim 1 (the forward operator is a sum of shifts).** For a real model, $Lm$ is real. If $q_j x_i^2 = s\,\Delta t$ for an integer $s$, the contribution of $m_j$ to trace $i$ is $m_j$ shifted by $s$ samples, circularly. In general it is the periodic trigonometric interpolant of $m_j$ evaluated at the times $t\,\Delta t - q_j x_i^2$.

*Proof.* Since $\overline{(L_k)_{ij}} = e^{i\omega_k q_j x_i^2} = (L_{n-k})_{ij}$ and $L_0$ is real, $L_{n-k} = \overline{L_k}$. If $(M_k)$ is conjugate symmetric, so is $(L_k M_k)$, and its inverse DFT is real. For an integer shift, $e^{-i\omega_k s \Delta t} = e^{-2\pi i k_s s/n} = e^{-2\pi i k s/n}$ because $k_s \equiv k \pmod n$, and multiplying the DFT by $e^{-2\pi i k s/n}$ shifts the signal circularly by $s$ samples (the shift theorem of the DFT). For a general delay $\tau$, the trigonometric polynomial $p(t') = \frac{1}{n}\sum_k M_j[k]\, e^{i\omega_k t'}$ with the signed frequencies takes the value $m_j[t]$ at $t' = t\,\Delta t$, and $\frac{1}{n}\sum_k M_j[k]\, e^{-i\omega_k \tau} e^{i\omega_k t \Delta t} = p(t\,\Delta t - \tau)$. $\square$

**Claim 2 (adjoint).** For a real model $m$ and a real gather $d$, $\langle Lm, d\rangle = \langle m, L^T d\rangle$, where $L^T d$ is the output of the function adjoint, which is real.

*Proof.* For real signals, Parseval's identity for this DFT is $\sum_t a[t]\,b[t] = \frac{1}{n}\sum_k \overline{A[k]}\, B[k]$. So $\langle Lm, d\rangle = \frac{1}{n}\sum_k (L_k M_k)^H D_k = \frac{1}{n}\sum_k M_k^H (L_k^H D_k)$. The family $(L_k^H D_k)$ is conjugate symmetric, by $L_{n-k} = \overline{L_k}$ and the symmetry of $(D_k)$, so it is the spectrum of a real model, and the last sum is $\langle m, L^T d\rangle$ by Parseval again. $\square$

**Claim 3 (the solve).** Let $\mu > 0$. Lines L1 to L4 and L7 return the unique real model $m^\ast$ that minimizes
$$J(m) = \|Lm - d\|^2 + \mu \|m\|^2$$
over all real models. It is the solution of $(L^T L + \mu I)\, m = L^T d$ in the time domain.

*Proof.* By Parseval, $J(m) = \frac{1}{n}\sum_k \big(\|L_k M_k - D_k\|^2 + \mu\|M_k\|^2\big)$, and the term of bin $k$ depends only on $M_k$. Each term is a strictly convex quadratic function of the complex vector $M_k$, because $L_k^H L_k + \mu I$ is Hermitian positive definite, and its unique minimizer is $M_k^\ast = (L_k^H L_k + \mu I)^{-1} L_k^H D_k$, which is line L4. Taking the complex conjugate of this equation and using $L_{n-k} = \overline{L_k}$ and $D_{n-k} = \overline{D_k}$ shows $M_{n-k}^\ast = \overline{M_k^\ast}$, and $M_0^\ast$ is real since $L_0$ and $D_0$ are real. So $(M_k^\ast)$ is the spectrum of a real model $m^\ast$, which line L7 returns. The family $(M_k^\ast)$ minimizes every term over all complex vectors, so $m^\ast$ minimizes $J$ over the smaller set of real models; any other real model differs in some bin and has a strictly larger term there. The gradient of $J$ at $m^\ast$ is $2(L^T L m^\ast - L^T d + \mu m^\ast)$ by Claim 2, and it is zero. $\square$

**Claim 4 (the split).** Let $P$ keep the model traces with $q_j > q_{\text{cut}}$ and set the others to zero. Lines L5, L6 and L8 return the multiples $L P m^\ast$ and the primaries $d - L P m^\ast$. So the primaries and the multiples add up to $d$ exactly, and the primaries are $L(I - P) m^\ast + (d - L m^\ast)$: the modeled events with $q_j \le q_{\text{cut}}$ plus the part of the data that the model does not fit.

*Proof.* Line L5 forms the spectra of $P m^\ast$, bin by bin, and line L6 multiplies them by $L_k$, which is the spectrum of $L P m^\ast$. The rest is linearity of $L$. $\square$

So the misfit $d - Lm^\ast$, which holds the noise and any event that is not a parabola in the range of $q$, stays with the primaries. This is a design choice of the method: it removes only what it can model as a multiple.

**Claim 5 (zero frequency).** At $k = 0$ all columns of $L_0$ are the vector of ones, and $M_0^\ast = \frac{S}{n_x n_q + \mu}(1, \ldots, 1)^T$ with $S = \sum_i D_i[0]$. So every model trace has the same mean, whatever the data, and the zero-frequency part of the data is split between primaries and multiples in the ratio of the numbers of curvatures at most and above $q_{\text{cut}}$.

*Proof.* $L_0^H L_0 = n_x \mathbf{1}\mathbf{1}^T$ and $L_0^H D_0 = S\,\mathbf{1}$. The vector $c\,\mathbf{1}$ solves $(n_x \mathbf{1}\mathbf{1}^T + \mu I) M = S\,\mathbf{1}$ when $n_x n_q c + \mu c = S$, and the solution is unique by Claim 3. $\square$

More generally, columns $j$ and $j'$ of $L_k$ differ by the phases $\omega_k (q_j - q_{j'}) x_i^2$. When $|\omega_k|\,|q_j - q_{j'}|\, x_{\max}^2$ is small, the two columns are nearly parallel, the normal matrix is badly conditioned, and the damping decides the split. So the method cannot be expected to separate events whose moveouts at the far offset differ by much less than one period of the dominant frequency. This is a heuristic resolution limit, not a theorem.

**Claim 6 (cost).** With $n$ samples, $n_x$ traces and $n_q$ curvatures, the solve costs $O(n (n_x n_q^2 + n_q^3))$ plus the transforms: $n_x + n_q$ forward DFTs and $n_x + n_q$ inverse DFTs. The direct DFT used for odd $n$ costs $O(n^2)$ per trace; an FFT costs $O(n \log n)$.

*Proof.* For each of the $n$ bins, line L3 costs $O(n_x n_q)$, the normal matrix $O(n_x n_q^2)$, the right-hand side $O(n_x n_q)$, the dense solve $O(n_q^3)$, and line L6 $O(n_x n_q)$. When the $q_j$ are equally spaced, $(L_k^H L_k)_{jj'} = \sum_i e^{i\omega_k (q_j - q_{j'}) x_i^2}$ depends only on $j - j'$, so the matrix is Hermitian Toeplitz and a Levinson-type solver costs $O(n_q^2)$ in place of $O(n_q^3)$. $\square$
