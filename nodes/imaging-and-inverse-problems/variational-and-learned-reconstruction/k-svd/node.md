---
tag: 0XCKNF
kind: algorithm
slug: k-svd
name: K-SVD
aliases:
- K-SVD dictionary learning
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Learn a dictionary by alternating sparse coding with an update of each atom and its coefficients by a rank one SVD of the residual.
solves: [dictionary-learning]
model: real-ram
complexity:
  vars: {J: the number of iterations, N: the number of signals, K: the number of atoms, n: the length of a signal, s: the number of atoms per signal}
  time: {worst: O(J N s n (K + n))}
  space: {extra: O(n (K + N))}
properties: {deterministic: true, iterative: true, convex: false, monotone: with an exact sparse coder only, global_optimum: no guarantee}
history:
  year: 2006
  people: [Michal Aharon, Michael Elad, Alfred Bruckstein]
  note: Aharon, Elad and Bruckstein published K-SVD in 2006 as a generalization of k-means to sparse codes. Elad and Aharon used it in the same year for image denoising with dictionaries learned on the noisy image.
prereqs: [dictionary-learning, orthogonal-matching-pursuit, singular-value-decomposition, k-means]
see_also: [mutual-coherence, convolutional-sparse-coding, vector-quantization, principal-component-analysis, image-denoising, lloyds-algorithm, power-iteration, sparse-signal-recovery]
sources:
  - paper: doi:10.1109/TSP.2006.881199
    title: Michal Aharon, Michael Elad and Alfred Bruckstein, K-SVD, an algorithm for designing overcomplete dictionaries for sparse representation, IEEE Transactions on Signal Processing 54(11), 2006
    locator: pages 4311 to 4322 (the algorithm, the relation to k-means and the synthetic recovery experiments)
  - paper: doi:10.1109/TIP.2006.881969
    title: Michael Elad and Michal Aharon, Image denoising via sparse and redundant representations over learned dictionaries, IEEE Transactions on Image Processing 15(12), 2006
    locator: pages 3736 to 3745
  - paper: doi:10.1109/ICASSP.1999.760624
    title: Kjersti Engan, Sven Ole Aase and John Hakon Husoy, Method of optimal directions for frame design, IEEE International Conference on Acoustics, Speech, and Signal Processing, 1999
    locator: the dictionary update by least squares that K-SVD replaces
---

K-SVD is an algorithm for the [dictionary learning](/dictionary-learning/) problem: given $N$ signals $y_i \in \mathbb{R}^n$, find $K$ unit atoms $d_k$ and codes $x_i$ with at most $s$ nonzero entries each, so that $\|Y - DX\|_F^2$ is small. Like [k-means](/k-means/), it alternates two steps: code every signal with the current dictionary, then update the dictionary. With $s = 1$, coefficients fixed to 1 and no normalization of the atoms, it reduces to k-means. Its difference from the earlier method of optimal directions (MOD), which solves for all atoms at once by least squares, is the update: K-SVD updates one atom at a time, together with the coefficients of that atom, by a rank one [singular value decomposition](/singular-value-decomposition/) of the error on the signals that use the atom. The coding step uses a sparse coder such as [orthogonal matching pursuit](/orthogonal-matching-pursuit/). Compared with [convolutional sparse coding](/convolutional-sparse-coding/), K-SVD learns atoms for small independent patches, not filters for a whole image.

## The problem

Given the $n \times N$ signal matrix $Y$, a number of atoms $K$ (usually $K > n$, an overcomplete dictionary) and a sparsity $s$, find an $n \times K$ dictionary $D$ with unit columns and a $K \times N$ code matrix $X$ that minimize

$$F(D, X) = \|Y - DX\|_F^2 \quad\text{subject to}\quad \|x_i\|_0 \le s \text{ for every } i.$$

The output is $D$ and $X$. The problem is not convex and is NP-hard in general, so K-SVD is a local method: it lowers $F$ from a starting dictionary, often a random choice of normalized signals or a fixed transform such as an overcomplete DCT.

## The algorithm

Write $x^k$ for row $k$ of $X$, the coefficients of atom $k$ in all signals.

```pseudo id=main
K-SVD(Y, D, s, J)
L1  for j = 1 to J
L2      for i = 1 to N: x_i ← SparseCode(D, y_i, s)     ▷ for example OMP
L3      for k = 1 to K
L4          ω ← {i : x^k_i ≠ 0}                          ▷ the signals that use atom k
L5          if ω is empty: replace d_k by the worst represented signal, normalized; continue
L6          E ← columns ω of Y - Σ_{j≠k} d_j x^j         ▷ error without atom k
L7          (u, σ, v) ← largest singular triple of E
L8          d_k ← u, x^k_ω ← σ v                         ▷ best rank one fit of E
L9  return D, X
```

Line L6 keeps only the columns in $\omega$. This is the main idea: the new coefficients $\sigma v$ fill only the positions that were already nonzero, so the sparsity pattern of $X$ does not grow. A rank one fit of all columns would give a dense row. Line L6 uses the new values of the atoms $1, \dots, k - 1$ and of their coefficients, as in a Gauss-Seidel sweep.

## Example

Take $n = 2$, $K = 2$, $s = 1$, the start $D = (e_1, e_2)$ and three signals $y_1 = (2, 1)$, $y_2 = (4, 2)$, $y_3 = (1, -2)$.

Coding (L2). OMP with one atom picks the atom with the largest $|\langle d_k, y_i\rangle|$: $y_1 \mapsto 2e_1$, $y_2 \mapsto 4e_1$, $y_3 \mapsto -2e_2$. The residuals are $(0, 1)$, $(0, 2)$ and $(1, 0)$, so $F = 1 + 4 + 1 = 6$.

Atom 1 (L4 to L8). $\omega = \{1, 2\}$ and no other atom is used by these signals, so

$$E = \begin{pmatrix}2 & 4\\ 1 & 2\end{pmatrix} = \begin{pmatrix}2\\1\end{pmatrix}\begin{pmatrix}1 & 2\end{pmatrix}.$$

$E$ has rank 1, with $\sigma = 5$, $u = (2, 1)/\sqrt5$ and $v = (1, 2)/\sqrt5$. The new atom is $d_1 = (2, 1)/\sqrt5$ with coefficients $\sigma v = (\sqrt5, 2\sqrt5)$, which fit $y_1$ and $y_2$ exactly. Now $F = 1$.

Atom 2. $\omega = \{3\}$ and $E$ is the single column $y_3$. Its best rank one fit is $y_3$ itself: $d_2 = (1, -2)/\sqrt5$ (up to sign) with coefficient $\sqrt5$. Now $F = 0$.

One iteration found a dictionary in which each signal is one atom times a coefficient. The test file checks these numbers.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In short:

- The update of atom $k$ is the best rank one fit: for any matrix $E$, $\min\|E - dw^T\|_F^2$ over unit $d$ is $\|E\|_F^2 - \sigma_1^2$, reached at $d = u_1$, $w = \sigma_1v_1$. The old atom and its coefficients are one candidate, so the objective does not increase, and the support of each code does not grow.
- If the coder is exact (it returns the best code with at most $s$ atoms), the codes of the previous iteration are feasible for it, so the coding step does not increase the objective either. Then $F$ is nonincreasing over the whole run and converges.

Practical K-SVD uses OMP, which is not exact. Then only the atom update is guaranteed to help, and the coding step can raise the objective. The values converge to a limit, but the theorem says nothing about the global minimum or about recovering a true dictionary.

## Complexity

With OMP, coding one signal costs $O(snK)$ for the correlations plus the cost of small least squares problems, so the coding step costs $O(NsnK)$ when $s$ is small. In the update of atom $k$, building $E$ costs $O(ns)$ per column, and the columns of all atoms together number at most $Ns$. A rank one SVD of the $n \times |\omega|$ matrix costs $O(n|\omega|)$ per step of [power iteration](/power-iteration/), or $O(n|\omega|\min(n, |\omega|))$ per sweep of a full SVD, which is what the implementation uses. One iteration is therefore $O(Nsn(K + n))$, and $J$ iterations cost $O(JNsn(K + n))$. The memory beyond $Y$ is $O(nK)$ for the dictionary, $O(Ns)$ for sparse codes and $O(nN)$ in the worst case for the restricted error matrix. In practice the coding step dominates; batch OMP, which precomputes $D^TD$ and $D^TY$, makes it much faster.

## Properties

- It is a block coordinate method: each atom update is an exact minimization over one atom and its coefficients, with the support fixed.
- The atoms keep norm 1. The scale sits in the coefficients, and the sign of an atom is not determined.
- The sparsity pattern found by the coder is kept during the atom updates, and can only lose entries.
- It is not convex and depends on the start. Different starts give different dictionaries, and some atoms may stay unused or repeat.
- With $s = 1$, the coefficients forced to 1 and no normalization, the update of atom $k$ becomes the mean of its signals, and K-SVD is k-means. With $s = 1$ and free coefficients it is gain-shape [vector quantization](/vector-quantization/).

## Variants and improvements

- Approximate K-SVD replaces the SVD by one step of alternating updates, $d \leftarrow Ex/\|Ex\|$ then $x \leftarrow E^Td$, which avoids forming $E$ explicitly. Together with batch OMP this is the common fast version (Rubinstein, Zibulevsky and Elad, 2008).
- MOD updates all atoms at once by $D = YX^T(XX^T)^{-1}$ and then normalizes. Each iteration costs more, but it is simple.
- Error target coding codes each signal until $\|y_i - Dx_i\| \le \epsilon$ instead of with exactly $s$ atoms. This is the form used for denoising, with $\epsilon$ set from the noise level.
- Online dictionary learning (Mairal, Bach, Ponce and Sapiro) processes signals in small batches with an $\ell_1$ coder, which scales to millions of patches.
- Structured and multiscale variants learn dictionaries for color images, for several scales, or with a separable or sparse structure that gives a fast transform.
- Convolutional versions learn filters for whole images instead of atoms for patches; see [convolutional sparse coding](/convolutional-sparse-coding/).

## When to use it

Use K-SVD when there are many examples of a class of signals, such as image patches of $8 \times 8$ pixels, and a fixed transform such as a wavelet or DCT basis does not give codes that are sparse enough. The classic use is [image denoising](/image-denoising/) and [inpainting](/image-inpainting/) with dictionaries trained on the corrupted image itself. For very large training sets, online methods are faster. For signals with a known good transform, or when no training data is available, use a fixed dictionary. When the atoms must be shift invariant over a whole image, use convolutional sparse coding.

## Pitfalls

- The result depends on the start, and K-SVD often stops in a local minimum. In a measurement on planted problems with $n = 8$, $K = 10$, $s = 2$ and $N = 200$ noiseless signals, started from 10 normalized signals and run for 30 iterations, eight random seeds found 10, 8, 2, 8, 1, 9, 7 and 7 of the 10 true atoms (an atom counts as found when $1 - |\langle d, d_{\text{true}}\rangle| < 0.01$).
- With OMP, the objective is not monotone. In four measured runs with $n = 8$, $K = 12$, $s = 2$ and $N = 150$, the coding step raised the objective in at least 3 of the 25 iterations of every run. Monitor the objective after the atom updates, and do not use "the objective went up" as a sign of a bug.
- Even with every atom found, OMP can pick a wrong support for some signals when the atoms are coherent. In a measured run of the test file started near the true dictionary, all 10 atoms were found but the objective stayed at 4.7 (from 28.0 after the first coding step), not 0.
- Atoms can become unused, or two atoms can become almost equal. Replace such atoms, for example by the worst represented signal, and watch the [mutual coherence](/mutual-coherence/) of the dictionary.
- Remove the mean of each patch before training if the dictionary should model texture and not brightness; otherwise one atom is spent on the constant patch in many codes.
- The signs and the order of the atoms are arbitrary. Compare dictionaries up to sign and permutation.

## Implementations

## History

Olshausen and Field (1996) learned overcomplete dictionaries for natural image patches with a sparsity penalty and found atoms that look like the receptive fields of the visual cortex. Engan, Aase and Husoy (1999) proposed the method of optimal directions, which alternates sparse coding with a least squares dictionary update. Aharon, Elad and Bruckstein (2006) introduced K-SVD as a generalization of k-means, with the update of one atom and its coefficients by a rank one SVD, and showed on synthetic data that it recovers a planted dictionary more often than MOD. In the same year, Elad and Aharon used it for image denoising, which made it one of the standard tools of sparse representation in imaging. Later work made it faster (approximate K-SVD with batch OMP), online (Mairal and others, 2010) and convolutional.

## References
