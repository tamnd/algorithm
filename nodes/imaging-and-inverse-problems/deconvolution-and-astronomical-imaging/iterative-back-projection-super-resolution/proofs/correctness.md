---
title: Iterative back-projection is Landweber for the stacked frame operator, and with a complete set of shifts it is a spectral filter
proves: [correctness]
status: full
---

**Setting.** The high resolution signal $x$ has $n$ samples, with $L$ dividing $n$ (an image is the same with two indices, the 2D DFT and pairs of residues). Frame $k = 1, \ldots, K$ is $y_k = A_k x$ with $A_k = D B W_k$, where $(W_k x)_j = x_{(j + s_k) \bmod n}$ for an integer shift $s_k$, $B$ is periodic convolution with a real PSF $h$ (center at index $0$), and $(Dv)_j = v_{jL}$ for $j = 0, \ldots, n/L - 1$. $U = D^T$ puts $v_j$ at index $jL$ and zeros elsewhere. $P$ is periodic convolution with a real back projection kernel $p$. The iteration of lines L1 to L7, from $x_0$, is

$$x_{t+1} = x_t + \omega \sum_{k=1}^{K} W_k^T P U (y_k - A_k x_t), \qquad \omega = \beta / K.$$

The DFT is $\hat x_q = \sum_j x_j e^{-2\pi i jq/n}$, $H_q = \hat h_q$ and $P_q = \hat p_q$.

**Lemma 1 (adjoints).** $W_k^T$ is the shift by $-s_k$, $D^T = U$, and for $\tilde h_j = h_{-j}$ the convolution with $\tilde h$ is $B^T$. So with $p = \tilde h$, $W_k^T P U = (D B W_k)^T = A_k^T$.

*Proof.* $W_k$ is a permutation matrix, so its transpose is its inverse, the shift by $-s_k$. $D$ selects the rows $jL$ of the identity, so $D^T$ puts the entries back at those rows. $B_{ij} = h_{(i - j) \bmod n}$, so $(B^T)_{ij} = h_{(j - i) \bmod n} = \tilde h_{(i - j) \bmod n}$. Then $(DBW_k)^T = W_k^T B^T D^T$. $\square$

**Claim 1 (Landweber).** Let $A$ be the stacked operator with the blocks $A_1, \ldots, A_K$ and $y$ the stacked data. With $p = \tilde h$, the iteration is $x_{t+1} = x_t + \omega A^T (y - A x_t)$, the Landweber iteration for $Ax = y$ with step $\omega$. Hence for $0 < \omega < 2/\lVert A \rVert^2$ and $x_0 = 0$, $x_t$ converges to the minimum norm least squares solution $A^{+} y$, the residual norm $\lVert y - Ax_t\rVert$ never grows, and for $y = Ax^\dagger$ the error $\lVert x_t - A^{+}Ax^\dagger \rVert$ never grows.

*Proof.* By Lemma 1, $\sum_k A_k^T (y_k - A_k x) = A^T (y - Ax)$. The convergence and monotonicity statements are the standard properties of Landweber. In the singular basis of $A$ (singular values $\sigma_i$), from $x_0 = 0$ the iterate has the filter factors $1 - (1 - \omega \sigma_i^2)^t$, which tend to $1$ for $0 < \omega\sigma_i^2 < 2$, and the components in the null space of $A$ stay $0$. The error component along a right singular vector with $\sigma_i > 0$ is multiplied by $1 - \omega\sigma_i^2 \in (-1, 1)$ in each step, so its modulus does not grow; the residual components are multiplied by the same factors. $\square$

The test compares the code with the dense Landweber iteration on the stacked matrix in rational arithmetic, and the two agree exactly.

**Lemma 2 (complete set of shifts).** Let $M = UD$, the diagonal mask that keeps the indices $j \equiv 0 \pmod L$. Then $W_k^T M W_k$ keeps the indices $j$ with $j \equiv s_k \pmod L$. So if the residues $s_k \bmod L$ take each value of $\{0, \ldots, L-1\}$ exactly $c$ times, $\sum_k W_k^T M W_k = c\,I$.

*Proof.* $(W_k^T M W_k x)_i = (M W_k x)_{i - s_k} = [\, i - s_k \equiv 0 \,]\, x_i$. Summing over $k$ counts, for each $i$, the frames with $s_k \equiv i$, which is $c$. $\square$

**Claim 2 (spectral filter).** Let the residues take each value exactly once, so $K = L$ ($K = L^2$ pairs in 2D). Then for any kernel $p$ the error $e_t = x_t - x^\dagger$ for exact data $y_k = A_k x^\dagger$ satisfies

$$\hat e_{t+1, q} = (1 - \omega P_q H_q)\, \hat e_{t,q}.$$

So $x_t \to x^\dagger$ for every $x^\dagger$ if and only if $|1 - \omega P_q H_q| < 1$ at every frequency $q$. With $p = \tilde h$ the factor is $1 - \omega |H_q|^2$, and from $x_0 = 0$

$$\hat x_{t,q} = \bigl(1 - (1 - \omega |H_q|^2)^t\bigr)\, \frac{\hat z_q}{H_q}, \qquad z = \sum_k W_k^T U y_k,$$

for every data $y$ (not only exact data), at each $q$ with $H_q \ne 0$.

*Proof.* $B$, $P$ and $W_k$ are circulant, so they commute. With $y_k = A_k x^\dagger$, the update of the error is $e_{t+1} = e_t - \omega \sum_k W_k^T P U D B W_k e_t = e_t - \omega P \bigl(\sum_k W_k^T M W_k\bigr) B e_t = (I - \omega P B) e_t$ by Lemma 2 with $c = 1$. In the Fourier basis $PB$ is multiplication by $P_q H_q$. The factor $(1 - \omega P_q H_q)^t$ tends to $0$ if and only if its modulus is below $1$; if it is $1$ or more at some $q$, the error with only that frequency (and $-q$ for a real signal) does not tend to $0$. For general data and $p = \tilde h$, $\sum_k W_k^T B^T U y_k = B^T z$ and $\sum_k A_k^T A_k = B^T B$ by Lemma 2, so the iteration is $x_{t+1} = (I - \omega B^T B)x_t + \omega B^T z$. By induction $x_t = \omega \sum_{j<t} (I - \omega B^T B)^j B^T z$, and in the Fourier basis this is $\omega \sum_{j<t}(1 - \omega|H_q|^2)^j\, \overline{H_q}\, \hat z_q$, whose geometric sum is the formula. $\square$

So with a complete set of shifts the multiframe problem is a deblurring problem on the high resolution grid, and the factors are the Landweber factors $1 - (1 - \omega\sigma^2)^t$ with $\sigma = |H_q|$. The kernel condition $|1 - \omega P_q H_q| < 1$ is the frequency form of the condition on the back projection kernel; it fails for $p = \delta$ and a PSF whose OTF is negative somewhere, as for the Van Cittert iteration.

**Claim 3 (identifiability).** If the residues of the shifts do not cover $\{0, \ldots, L-1\}$, $A$ has a nontrivial null space. If they cover it and $H_q \ne 0$ for all $q$, $A$ is injective.

*Proof.* If $B$ is singular, any $v \ne 0$ with $Bv = 0$ gives $Av = 0$. Otherwise, let the residue $r$ be missing, let $e$ be the unit vector at index $r$, and let $v = B^{-1} e \ne 0$. Since $W_k$ and $B$ commute, $A_k v = D W_k e$, which reads $e$ at the indices $jL + s_k \equiv s_k \not\equiv r$, where $e$ is $0$. So $Av = 0$. If the residues are covered, $A^T A = \sum_k A_k^T A_k \succeq B^T (\sum_{k \in S} W_k^T M W_k) B = B^T B$ for a subset $S$ with each residue once, and $B^T B$ is invertible when every $H_q \ne 0$. $\square$

A shift by a multiple of $L$ (a whole low resolution pixel) gives no new information. In the test, two frames with the shifts $0$ and $2$ for $L = 2$ give the same data for two signals that differ at the odd indices, and the iterate from $0$ keeps those entries at $0$. $\blacksquare$
