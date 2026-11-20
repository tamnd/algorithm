---
tag: BBV2DJ
kind: algorithm
slug: svd-clutter-filter
name: SVD clutter filter
aliases:
- spatiotemporal SVD clutter filter
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: research
summary: Separate blood from tissue echoes by removing the largest singular components of the space by slow time Casorati matrix of the data.
model: real-ram
complexity:
  vars: {M: the number of pixels, N: the number of frames (the ensemble length)}
  time: {worst: O(M N^2 + N^3)}
  space: {extra: O(M N + N^2)}
properties: {deterministic: true, recursive: false, exact: false, linear_in_data: false}
history:
  year: 2015
  people: [Charlie Demene, Thomas Deffieux, Mathieu Pernot, Mickael Tanter]
  note: "Ledoux, Brands and Hoeks (1997) used the singular value decomposition to reduce clutter in simulated Doppler signals. Demene et al. (2015) applied it to the space by slow time Casorati matrix of ultrafast plane wave data."
prereqs: [singular-value-decomposition, plane-wave-compounding]
see_also: [robust-pca, truncated-svd, principal-component-analysis, low-rank-plus-sparse-mri, kasai-autocorrelation-estimator, moving-target-indication, speckle, lanczos-algorithm]
sources:
  - paper: doi:10.1109/TMI.2015.2428634
    title: "Charlie Demene, Thomas Deffieux, Mathieu Pernot, Bruno-Felix Osmanski, Valerie Biran, Jean-Luc Gennisson, Lim-Anna Sieu, Antoine Bergel, Stephanie Franqui, Jean-Michel Correas, Ivan Cohen, Olivier Baud and Mickael Tanter, Spatiotemporal clutter filtering of ultrafast ultrasound data highly increases Doppler and fUltrasound sensitivity, IEEE Transactions on Medical Imaging 34(11), 2015, 2271 to 2285"
    locator: "the Casorati matrix of the ultrafast data, its singular value decomposition, and the removal of the tissue singular components (general locator)"
  - paper: doi:10.1177/016173469701900101
    title: "L. A. F. Ledoux, P. J. Brands and A. P. G. Hoeks, Reduction of the clutter component in Doppler ultrasound signals based on singular value decomposition: a simulation study, Ultrasonic Imaging 19(1), 1997, 1 to 18"
    locator: "the first use of the singular value decomposition for Doppler clutter reduction (general locator)"
  - paper: doi:10.1109/TMI.2018.2789499
    title: "Jerome Baranger, Bastien Arnal, Fabienne Perren, Olivier Baud, Mickael Tanter and Charlie Demene, Adaptive spatiotemporal SVD clutter filtering for ultrafast Doppler imaging using similarity of spatial singular vectors, IEEE Transactions on Medical Imaging 37(7), 2018, 1574 to 1586"
    locator: "the choice of the cut-off ranks from the similarity of the spatial singular vectors (general locator)"
  - paper: doi:10.1109/58.985705
    title: "S. Bjaerum, H. Torp and K. Kristoffersen, Clutter filter design for ultrasound color flow imaging, IEEE Transactions on Ultrasonics, Ferroelectrics and Frequency Control 49(2), 2002, 204 to 216"
    locator: "the conventional clutter filters that act on each slow time signal separately (general locator)"
  - paper: doi:10.1007/BF02288367
    title: "Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 1936, 211 to 218"
    locator: "the best approximation of lower rank by truncating the singular value form"
---

The SVD clutter filter separates the echo of blood from the much stronger echo of tissue in ultrasound Doppler data. It stacks the $N$ complex frames of an acquisition into the Casorati matrix $S$, with one row per pixel and one column per frame, and computes its [singular value decomposition](/singular-value-decomposition/). Tissue moves slowly and together over large regions, so it fills the first few singular components, which hold almost all the energy. Blood moves fast and decorrelates in space, so it lies in the middle components, and noise in the last ones. The filter removes the first $k_1$ components, and optionally the components after $k_2$, and keeps $S_f = \sum_{j = k_1 + 1}^{k_2} \sigma_j u_j v_j^H$. The power of $S_f$ at each pixel is the power Doppler image. Unlike a high-pass filter on each pixel, the SVD filter uses the spatial coherence of tissue, and it removes tissue that moves as fast as blood. It needs many frames per pixel, which [plane wave compounding](/plane-wave-compounding/) gives at thousands of frames per second. The cut-off ranks $k_1$ and $k_2$ are choices, not outputs of the method.

## In plain words

Each pixel of an ultrasound movie has a signal over time. Tissue gives a strong signal that changes slowly, and the tissue in one region moves together, so many pixels show the same pattern in time. Blood gives a weak signal that changes fast and differs from pixel to pixel.

Put all the pixel signals in a table, one row per pixel and one column per frame. The singular value decomposition splits the table into layers, from the strongest pattern shared by many pixels to the weakest. The first few layers are tissue, because tissue is strong and moves together. The filter deletes them and keeps the rest, which is mostly blood and noise. The number of layers to delete is a setting that the user picks.

## The problem

**Input.** A stack of $N$ complex IQ frames $x_t(i, j)$, $t = 0 \ldots N-1$, of $M$ pixels each, and two cut-off ranks $0 \le k_1 \le k_2 \le N$.

**Model.** The data are the sum of a tissue part, a blood part and noise. The tissue echo is often tens of decibels stronger than the blood echo, and in a single pixel its Doppler spectrum can overlap that of slow blood, for example when the tissue moves with breathing or with the hand of the operator. A filter that acts on each slow time signal alone must separate the two by frequency. The SVD filter also uses the fact that tissue motion is coherent over many pixels.

**Output.** The filtered frames, with the tissue removed, and the power Doppler image $\mathrm{PD}(p) = \frac{1}{N} \sum_t |S_f(p, t)|^2$.

## The algorithm

```pseudo id=main
SVD-CLUTTER-FILTER(frames x_0 … x_{N-1}, k1, k2)
L1  S ← M × N Casorati matrix, row p = slow time signal of pixel p
L2  C ← S^H S                                   ▷ N × N Gram matrix
L3  (σ_j^2, v_j) ← eigenpairs of C, σ_1 ≥ … ≥ σ_N   ▷ right singular vectors of S
L4  check 0 ≤ k1 ≤ k2 ≤ N                       ▷ the cut-off ranks are chosen by the user
L5  P ← Σ_{j=k1+1}^{k2} v_j v_j^H               ▷ projector onto the kept components
L6  S_f ← S P                                   ▷ = Σ_{j=k1+1}^{k2} σ_j u_j v_j^H
L7  PD(p) ← (1/N) Σ_t |S_f[p, t]|^2             ▷ power Doppler image
L8  return frames of S_f, PD
```

The number of frames $N$ is much smaller than the number of pixels $M$ (for example 200 frames and $10^4$ pixels), so lines L2 and L3 solve a small $N \times N$ eigenproblem in place of the SVD of the large matrix. Line L6 never needs the left singular vectors $u_j$. The Python code computes the eigenpairs of the complex Hermitian matrix $C$ with a real symmetric eigensolver applied to the real $2N \times 2N$ matrix $\begin{pmatrix} \operatorname{Re} C & -\operatorname{Im} C \\ \operatorname{Im} C & \operatorname{Re} C \end{pmatrix}$, whose eigenvalues are those of $C$, each twice. The velocity image follows from $S_f$ with the [Kasai estimator](/kasai-autocorrelation-estimator/).

## Example

**Tissue that moves as fast as blood.** Take three pixels and $N = 4$ frames. Two tissue pixels have the amplitude 10 and the phase turns by a quarter turn per pulse, $e_1 = (1, i, -1, -i)$, a Doppler frequency of $+\mathrm{PRF}/4$. The blood pixel has the amplitude 1 and turns the other way, $e_3 = (1, -i, -1, i)$, a Doppler frequency of $-\mathrm{PRF}/4$:

$$S = \begin{pmatrix} 10 & 10i & -10 & -10i \\ 10 & 10i & -10 & -10i \\ 1 & -i & -1 & i \end{pmatrix}.$$

Both frequencies have the same magnitude, so a filter that removes frequencies near zero, or one that is symmetric in frequency, cannot remove the tissue and keep the blood. The vectors $e_1$ and $e_3$ are orthogonal: $\sum_t e_3(t) \overline{e_1(t)} = 1 - 1 + 1 - 1 = 0$. So

$$C = S^H S = 200\, \overline{e_1} e_1^T + \overline{e_3} e_3^T$$

has the eigenvalues $200 \cdot 4 = 800$ and $4$, and 0 twice. The singular values are $\sigma_1 = 20\sqrt{2} = 28.28$ and $\sigma_2 = 2$. With $k_1 = 1$ and $k_2 = 4$, $P = I - v_1 v_1^H$ with $v_1 = \overline{e_1}/2$. A tissue row gives $e_1^T P = e_1^T - (e_1^T \overline{e_1}/2)(e_1^T/2) = e_1^T - e_1^T = 0$, and the blood row gives $e_3^T v_1 = 0$, so it is unchanged. The power Doppler values change from $(100, 100, 1)$ to $(0, 0, 1)$. The code returns these values up to rounding.

**A simulated vessel.** The test simulates 8 by 6 pixels and 16 frames: tissue speckle with amplitude 10 and a slow common motion everywhere, a vessel of two rows with weak blood that decorrelates from pulse to pulse, and white noise. The first singular value holds 99.7 percent of the energy. The mean power Doppler inside the vessel divided by the mean outside is 0.10 without the filter, 130 with $k_1 = 1$, 35 with $k_1 = 2$ and 22 with $k_1 = 3$. In this simulation the tissue is close to rank one, and a cut that is too high removes blood.

## Correctness

By the orthonormality of the right singular vectors, $S v_l = \sigma_l u_l$, so line L6 gives $S_f = \sum_{j = k_1+1}^{k_2} \sigma_j u_j v_j^H$ and $\|S_f\|_F^2 = \sum_{j = k_1+1}^{k_2} \sigma_j^2$. With $k_2 = N$ the removed part $S - S_f$ is the truncated SVD of rank $k_1$, which by the Eckart-Young theorem is the matrix of rank at most $k_1$ closest to $S$ in the Frobenius norm. This is a theorem about energy: the filter removes the rank $k_1$ structure that explains the most energy. It is a heuristic that this structure is tissue.

The separation is exact in one case. Let $S = T + B$ where the tissue part $T$ has rank $k_1$, the columns of $T$ and $B$ are orthogonal (tissue and blood occupy orthogonal spatial patterns, for example disjoint pixels), and the rows of $T$ and $B$ are orthogonal (orthogonal slow time patterns, for example tones on disjoint DFT bins). Then the SVDs of $T$ and $B$ together form an SVD of $S$, and if every singular value of $T$ exceeds every singular value of $B$, the filter with $k_1$ returns $S_f = B$ exactly. If the parts overlap in both space and time, the singular vectors mix them and some blood is removed with the tissue.

The filter is equivariant under unitary changes of the pixels and of slow time: the data $\Pi S W$ give $\Pi S_f W$. A common shift of all Doppler frequencies is such a $W$, so the filter does not select by frequency. The real embedding used by the code has the eigenvalues of $C$ with doubled multiplicity, and its projector has $\operatorname{Re} P$ and $\operatorname{Im} P$ as its left blocks, so line L5 is computed correctly whenever the cuts fall between distinct singular values. The proofs are in proofs/correctness.md.

## Complexity

With $M$ pixels and $N$ frames, line L2 costs $O(M N^2)$, line L3 costs $O(N^3)$ with a dense eigensolver to working precision, line L5 costs $O(N^3)$ and line L6 costs $O(M N^2)$. The total is $O(M N^2 + N^3)$ time, which is $O(M N^2)$ because $N \le M$ in practice, and $O(M N + N^2)$ space. A filter that acts on each pixel alone with a fixed number of taps costs $O(M N)$, so the SVD filter is more expensive by a factor of order $N$. A partial eigensolver such as the [Lanczos algorithm](/lanczos-algorithm/) or a randomized SVD lowers the cost when $k_1$ and $N - k_2$ are small.

## Properties

- **Best rank $k_1$ removal** (theorem). The removed part is the best rank $k_1$ approximation of the data in the Frobenius norm, and the kept energy is $\sum_{j = k_1+1}^{k_2} \sigma_j^2$.
- **Exact separation** (theorem) when tissue and blood are orthogonal in space and in slow time and the tissue singular values are the largest.
- **Not tied to frequency.** A common frequency shift of the data shifts the output in the same way. Fast tissue motion is removed if it is coherent in space.
- **Independent of the pixel order.** A permutation of the rows of $S$ permutes the rows of $S_f$; the filter does not use the positions of the pixels, only the correlations between their signals.
- **Data adaptive and nonlinear.** The projector depends on the data, so the filter is not a linear time-invariant filter, and its frequency response changes from one acquisition to the next.
- **Needs many coherent frames.** With $N = 8$ to 16 frames, as in conventional color flow imaging, the tissue and blood subspaces are hard to tell apart; with hundreds of frames from ultrafast imaging the gain over frequency filters is large (Demene et al. 2015, a measurement on in vivo data).

## Variants and improvements

- **Choice of the cut-off ranks.** Fixed ranks, a threshold on the decay of the singular values, the mean Doppler frequency of each right singular vector, and the similarity of the spatial singular vectors (Baranger et al. 2018) are all used. Each is a heuristic.
- **Block-wise filtering.** Splitting the image into overlapping blocks and filtering each one alone adapts the cut-off to local tissue motion and reduces the cost of each SVD.
- **Higher order SVD** of a pixels by slow time by ensemble tensor, used when several acquisitions are combined.
- **Low rank plus sparse models.** [Robust PCA](/robust-pca/) writes the data as a low rank part plus a sparse part and solves a convex problem, as in [low-rank plus sparse MRI](/low-rank-plus-sparse-mri/). It replaces the hard cut of rank by a penalty, at the cost of an iterative solver.
- **Eigenvector regression filters.** In conventional color flow imaging, the eigenvectors of the slow time correlation matrix estimated over a region define a projection filter for each pixel; this is the same idea with a smaller $N$.

## When to use it

Use the SVD clutter filter for ultrafast Doppler and functional ultrasound, where plane wave imaging gives hundreds of frames per second per pixel and the blood signal is weak, as in small vessels or in the brain. Use it when the tissue moves, since a high-pass filter then either leaves tissue or removes slow blood. For conventional color flow imaging with short ensembles, a frequency filter of the kind reviewed by Bjaerum, Torp and Kristoffersen (2002) is cheaper. Use a robust PCA model when a sparse foreground (for example a contrast agent bubble) must be kept apart from the low rank background.

## Pitfalls

- **Cut-off too high.** Strong blood that is coherent over many pixels, as in a large vessel, appears in the first components and is removed with the tissue. In the test simulation the vessel contrast falls from 130 to 22 when $k_1$ goes from 1 to 3.
- **Cut-off too low.** Tissue that moves in several independent ways (breathing and the pulse, for example) needs more than one component, and a small $k_1$ leaves tissue that the Kasai estimator then reads as slow flow.
- **Ties in the singular values.** If $\sigma_{k_1} = \sigma_{k_1+1}$, the filter is not defined by the data, and a small change of the data changes the output a lot. Choose cuts at gaps in the singular value curve.
- **Too few frames.** With $N$ near the number of tissue components, there is no room for blood in the remaining subspace.
- **Cost of a full SVD.** Computing all $M \times N$ singular vectors is not needed; form the $N \times N$ Gram matrix or use a partial eigensolver.
- **Gram matrix accuracy.** Forming $S^H S$ squares the condition number, so singular values below about $10^{-8} \sigma_1$ lose their accuracy in double precision. This matters for the noise cut $k_2$, not for the tissue cut. Use the SVD of $S$ when the small singular values matter.

## Implementations

The Python code builds the Casorati matrix, forms the Gram matrix and finds its eigenpairs with the real symmetric Jacobi eigensolver of the shared imgla helper through the real embedding. The tests compare the result with the SVD of the real embedding of $S$ from imgla, check exact separation for orthogonal tissue and blood, the removed energy and the best rank fit, the noise cut, the invariances under a pixel permutation, a global phase and a frequency shift, and the vessel contrast on simulated data.

## History

Clutter filters for color flow imaging act on each slow time signal, for example with FIR, IIR or polynomial regression filters (Bjaerum, Torp and Kristoffersen 2002). Ledoux, Brands and Hoeks (1997) used the singular value decomposition to reduce clutter in simulated Doppler signals. With ultrafast plane wave imaging, long ensembles at every pixel became available, and Demene et al. (2015) applied the SVD to the Casorati matrix of all pixels and frames, which raised the sensitivity of Doppler and functional ultrasound. Baranger et al. (2018) proposed an adaptive choice of the cut-off ranks from the spatial singular vectors.

## References
