---
tag: ANWQA3
kind: model
slug: partial-separability-model
name: Partial separability model
aliases:
- low-rank model of dynamic MRI
area: imaging-and-inverse-problems/mri-reconstruction
level: research
summary: Model a dynamic image as a sum of few products of spatial and temporal functions, so that the space time matrix has low rank.
history:
  year: 2007
  people: [Zhi-Pei Liang]
  note: Liang wrote the dynamic k-space signal as a sum of L products of a spatial and a temporal function and recovered it in two steps, with navigator data for the temporal functions and sparse imaging data for the spatial ones.
prereqs: [mri-signal-equation, singular-value-decomposition]
see_also: [k-t-blast, low-rank-plus-sparse-mri, robust-pca, matrix-completion, principal-component-analysis, truncated-svd, compressed-sensing-mri, mr-fingerprinting]
sources:
  - paper: doi:10.1109/ISBI.2007.357020
    title: Zhi-Pei Liang, Spatiotemporal imaging with partially separable functions, Proc. IEEE International Symposium on Biomedical Imaging (ISBI), 2007, 988 to 991
    locator: the partially separable model of order L and the two step recovery with navigator and imaging data (general locator)
  - paper: doi:10.1007/BF02288367
    title: Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 1936, 211 to 218
    locator: the best approximation of lower rank by the truncated singular value decomposition (general locator)
---

The partial separability (PS) model is a forward model for dynamic MRI. It says that the image series $\rho(r, t)$ is a sum of $L$ products $u_l(r)\, v_l(t)$ of a spatial function and a temporal function, with $L$ much smaller than the number of pixels and of frames. In k-space the same model reads $s(k, t) = \sum_{l=1}^{L} c_l(k)\, \phi_l(t)$. So the space time (Casorati) matrix, with one row per pixel or k-space point and one column per frame, has rank at most $L$. Liang (2007) proposed the model and a two step recovery: navigator data, acquired often but only near the center of k-space, give the temporal functions by an [SVD](/singular-value-decomposition/); sparse imaging data then give the spatial functions by least squares. The model is the low rank part of [L+S](/low-rank-plus-sparse-mri/), which adds a sparse part, and it is close to the training step of k-t PCA in [k-t BLAST](/k-t-blast/).

## The machine

**The unknown.** The image series $\rho(r, t)$: a complex function of the position $r$ in the field of view and of the time $t$. On a grid with $N$ pixels and $T$ frames it is the Casorati matrix $X \in \mathbb{C}^{N \times T}$, whose column $t$ is frame $t$ and whose row $n$ is the time course of pixel $n$.

**The parameters.**

- The model order $L$, a positive integer with $L \ll \min(N, T)$.
- The temporal functions $\phi_1, \ldots, \phi_L$, the rows of $\Phi \in \mathbb{C}^{L \times T}$.
- The spatial functions $u_1, \ldots, u_L$, the columns of $U \in \mathbb{C}^{N \times L}$, and their spectra $c_l = F_u u_l$, the columns of $C = F_u U$.
- The sampling: the set of pairs $(k, t)$ that the scan acquires. Usually only a few k-space points are acquired in each frame.

**The forward map.** For each frame, the [MRI signal equation](/mri-signal-equation/) with one uniform coil, applied to the model image:

$$\rho(r, t) = \sum_{l=1}^{L} u_l(r)\, v_l(t), \qquad s(k, t) = \int \rho(r, t)\, e^{-2\pi i\, k \cdot r}\, dr + e(k, t) = \sum_{l=1}^{L} c_l(k)\, \phi_l(t) + e(k, t),$$

where $c_l$ is the Fourier transform of $u_l$, $\phi_l = v_l$, and $e$ is circular complex Gaussian noise. With several coils, each coil has its own $c_l$, or the coil maps multiply $u_l$ as in [SENSE](/sense/).

**The discrete model.** With the unitary DFT $F_u$ applied to each frame and a mask $\Omega$ that keeps the acquired $(k, t)$ pairs,

$$X = U \Phi, \qquad S = F_u X = C \Phi, \qquad y = \Omega(S) + e.$$

Here $S \in \mathbb{C}^{N \times T}$ is the k-space Casorati matrix: row $k$ is the time course of one k-space point.

**Where it holds (heuristic).** The model fits when few temporal patterns are shared by many pixels: periodic motion with few harmonics, contrast uptake curves, and slow signal changes. A pixel whose intensity follows a mix of these patterns adds no new term.

**Where it fails (heuristic, with a measurement below).**

- Motion of edges. When an edge moves, each pixel near it has its own time course, and the rank grows with the size of the motion. In the example below one disk whose radius changes made the singular values fall slowly instead of stopping at 3.
- Noise. Noisy data have full rank, so $L$ is a choice. Too small an $L$ leaves model error; too large an $L$ fits noise and asks for more samples per k-space point.
- Events in few pixels at a few times, for example a bright spot that flashes once. These do not share a temporal pattern. L+S puts them in the sparse part.

## What it counts

- **The data.** One complex number per acquired $(k, t)$ pair and per coil.
- **The degrees of freedom (theorem).** An $N \times T$ matrix of rank $L$ has $L(N + T - L)$ complex degrees of freedom, against $N T$ for a general matrix. The product $U \Phi$ has $N L + L T$ entries, and $U \Phi = (U G^{-1})(G \Phi)$ for every invertible $L \times L$ matrix $G$, which removes $L^2$. For $N = 128^2$, $T = 256$ and $L = 16$ this is $265{,}984$ against $4{,}194{,}304$, a factor of 15.8.
- **What the fit minimizes.** The two step method minimizes $\|P S - A \Phi\|_F$ over rank $L$ products on the navigator rows $P S$ (the truncated SVD), then $\|y_k - \Phi_k c(k)\|_2$ for each k-space point $k$, where $\Phi_k$ holds the columns of $\Phi$ at the frames in which $k$ was sampled. Other methods minimize $\|y - \Omega(S)\|^2$ with a rank constraint or a nuclear norm penalty on $S$; there is no nuclear norm page.
- **The cost (real-ram).** The SVD of the navigator matrix, of size $p \times T$, costs $O(p T \min(p, T))$. Each least squares fit costs $O(m_k L^2)$ for $m_k$ samples, so all fits together cost $O(M L^2)$ for $M$ samples. Forming the images costs $O(N T L)$, plus $T$ FFTs of $O(N \log N)$ each.

**A small example (measurement).** A $32 \times 32$ series with $T = 40$ frames: a static ellipse, a disk whose intensity is $0.6(1 + 0.3 \sin(2\pi t/7.3))$, like a heart, and a small disk with the uptake curve $0.4 / (1 + e^{-(t - 15)/3})$. This series is exactly PS of order 3. The scan acquires Cartesian lines: the center line $k_y = 0$ in every frame as the navigator, and 3 other lines per frame in a fixed cycle over the other 31 lines. That is 4 of 32 lines per frame, an acceleration of 8, and each line other than the center is acquired 3 or 4 times in the 40 frames. Errors are $\|\hat X - X\|_F / \|X\|_F$.

| method | relative error |
|---|---|
| zero filled inverse DFT of each frame | 0.490 |
| view sharing (the nearest acquired frame for each line) | 0.099 |
| PS, two step, $L = 1$ | 0.082 |
| PS, two step, $L = 2$ | 0.051 |
| PS, two step, $L = 3$ | $6.4 \times 10^{-16}$ |

The singular values of $X$, divided by the largest, were $1, 0.063, 0.049$ and then $1.5 \times 10^{-16}$. Recovery with $L = 3$ is exact up to rounding, as the theorems below predict. With $L = 4$ the fit fails on the 4 lines that were acquired only 3 times.

When a fourth disk with the radius $3 + \sin(2\pi t/7.3)$ pixels is added, the singular values become $1, 0.069, 0.051, 0.023, 0.014, 0.012, 0.0095, 0.0059$ and do not stop. With the same sampling, $L = 3$ gave 0.046, against 0.031 for the best rank 3 approximation of the true $X$ and 0.118 for view sharing. With 5 lines other than the center per frame (an acceleration of 5.3, 6 or 7 acquisitions of each line), $L = 3, 4, 5, 6$ gave 0.045, 0.032, 0.046 and 0.103. So a larger $L$ helps only until the extra temporal functions from the navigator are too weak to estimate well.

## Relation to other models

- **[MRI signal equation](/mri-signal-equation/).** Each frame follows the signal equation. The PS model adds a constraint across frames.
- **[Principal component analysis](/principal-component-analysis/) and the [Karhunen-Loeve transform](/karhunen-loeve-transform/).** The temporal functions from the SVD are the principal components of the time courses (without the mean removed). So PS is PCA of the time courses with $L$ components.
- **[k-t BLAST](/k-t-blast/) and k-t PCA.** k-t BLAST uses low resolution training data to weight a reconstruction in x-f space. k-t PCA takes a temporal basis from such training data by PCA, which is the first step of the PS method in another form (heuristic comparison).
- **[L+S](/low-rank-plus-sparse-mri/) and [robust PCA](/robust-pca/).** L+S writes $X = L + S$ with a low rank $L$ and a sparse $S$. The PS model is the case $S = 0$ with a fixed rank in place of the nuclear norm.
- **[Matrix completion](/matrix-completion/).** Recovering a PS series from samples of $S$ is a low rank matrix recovery problem. Haldar and Liang (ISBI 2010) treated it this way. The completion theorems assume random samples and an incoherence condition; the PS navigator sampling is not random, so the deterministic theorems below are the ones that apply to it.
- **[LORAKS](/loraks/).** LORAKS also uses low rank, but of a structured matrix built from one k-space, not of the space time matrix.
- **[MR fingerprinting](/mr-fingerprinting/).** The simulated signal evolutions of an MRF dictionary are close to a low dimensional subspace, and subspace methods for MRF use the same $U \Phi$ form (heuristic comparison).

## Known results in the model

**Rank (theorem).** If $X = U \Phi$ with $U \in \mathbb{C}^{N \times L}$ and $\Phi \in \mathbb{C}^{L \times T}$, then $\operatorname{rank} X \le L$, with equality if and only if $\operatorname{rank} U = \operatorname{rank} \Phi = L$. The same holds for $S = F_u X$.

*Proof.* $\operatorname{rank}(U \Phi) \le \min(\operatorname{rank} U, \operatorname{rank} \Phi) \le L$. If both ranks are $L$, then $U$ has a left inverse $U^{+}$ with $U^{+} U = I$, so $\Phi = U^{+} X$ and $L = \operatorname{rank} \Phi \le \operatorname{rank} X$. If one rank is less than $L$, so is $\operatorname{rank} X$ by the first inequality. $F_u$ is invertible, so $\operatorname{rank} S = \operatorname{rank} X$. $\square$

**Only the temporal subspace matters (theorem).** If $\hat\Phi = G \Phi$ with $G$ invertible, then $X = (U G^{-1}) \hat\Phi$. So any basis of the row space of $\Phi$ describes the same set of images, and the spatial functions adjust to it.

**The navigator gives the temporal subspace (theorem).** Let $P$ select $p$ rows of $S$ (the navigator k-space points, acquired in every frame), and let $A = P C$, a $p \times L$ matrix. If $\operatorname{rank} A = L$ and $\operatorname{rank} \Phi = L$, then the row space of $P S$ equals the row space of $\Phi$. So the first $L$ right singular vectors of $P S$ span it. This needs $p \ge L$.

*Proof.* $P S = A \Phi$, so every row of $P S$ is a combination of rows of $\Phi$. $A$ has a left inverse $A^{+}$, so $\Phi = A^{+} P S$ and every row of $\Phi$ is a combination of rows of $P S$. The two row spaces are equal, of dimension $L$, so $P S$ has exactly $L$ nonzero singular values and the first $L$ right singular vectors span the row space. $\square$

**One k-space point at a time (theorem).** Fix $\Phi$ and a k-space point $k$ acquired in the frames $t_1, \ldots, t_m$. Let $\Phi_k \in \mathbb{C}^{m \times L}$ have the entries $\phi_l(t_j)$, and let the data be $y_k = \Phi_k c(k) + e_k$. If $\operatorname{rank} \Phi_k = L$, the least squares solution $\hat c(k) = \Phi_k^{+} y_k$ is unique and $\|\hat c(k) - c(k)\|_2 \le \|e_k\|_2 / \sigma_{\min}(\Phi_k)$. If $\operatorname{rank} \Phi_k < L$, there is a $z \ne 0$ with $\Phi_k z = 0$, and $c(k)$ and $c(k) + z$ give the same data. So each point needs $m \ge L$ samples, at frames where the temporal functions are linearly independent.

*Proof.* With full column rank, $\Phi_k^{+} \Phi_k = I$, so $\hat c(k) - c(k) = \Phi_k^{+} e_k$, and $\|\Phi_k^{+}\|_2 = 1/\sigma_{\min}(\Phi_k)$. Without it, the null space of $\Phi_k$ is not trivial. $\square$

**Exact recovery (theorem).** Without noise, if $X$ is exactly PS of order $L$, the navigator condition above holds, and every k-space point has $\operatorname{rank} \Phi_k = L$, then the two step method returns $X$ exactly. This is a deterministic statement: it needs no random sampling. It follows from the last three theorems, applied with $\hat\Phi$ from the SVD and $\hat C = C G^{-1}$.

**Model error (theorem, Eckart and Young 1936).** For any $X$ with singular values $\sigma_1 \ge \sigma_2 \ge \cdots$, the best approximation of rank $L$ in the Frobenius norm is the [truncated SVD](/truncated-svd/), with the error $(\sum_{i > L} \sigma_i^2)^{1/2}$. When the true series is only close to PS, this is the floor that no method in the model can go below. In the example above the floor for $L = 3$ was 0.031 and the two step method reached 0.046.

**Periodic sampling can break the fit (a measurement of the last condition).** If the temporal functions, restricted to the frames in which a point $k$ was acquired, are linearly dependent, then $\Phi_k$ loses rank and the theorem above says that $c(k)$ is not determined. A periodic motion and a periodic sampling order can cause this. In the example with the heart period changed from 7.3 to 10 frames, the line cycle of about 10.3 frames put the visits of 8 of the 32 lines at frames like 2, 12, 22 and 33, where $\sin(2\pi t/10)$ has one value. Those 8 lines had condition numbers above $10^{6}$ for $L = 3$, and the error rose from $6.4 \times 10^{-16}$ to 0.0915. A sampling order that does not follow the period of the motion avoids this (heuristic).

**Choosing the navigator (heuristic).** Most of the energy of an image is near the center of k-space, so central navigator points give $A$ full rank with few samples in most images. The navigator also sets the time resolution: $\Phi$ is known only at the frames in which the navigator was acquired.

## References
