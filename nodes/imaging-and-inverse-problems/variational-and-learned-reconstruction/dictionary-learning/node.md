---
tag: 58NV5M
kind: problem
slug: dictionary-learning
name: Dictionary learning
aliases:
- sparse dictionary learning
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Find a dictionary of atoms and sparse codes such that every training signal is close to a sparse combination of the atoms.
prereqs: [sparse-signal-recovery, k-means, singular-value-decomposition]
see_also: [k-svd, convolutional-sparse-coding, analysis-and-synthesis-sparsity, mutual-coherence, image-denoising, principal-component-analysis, independent-component-analysis, vector-quantization]
sources:
  - paper: doi:10.1038/381607a0
    title: Bruno A. Olshausen and David J. Field, Emergence of simple-cell receptive field properties by learning a sparse code for natural images, Nature 381(6583), 1996
    locator: pages 607 to 609 (the sparse coding objective, learning by alternating inference and gradient steps, and the localized oriented atoms learned from image patches)
  - paper: doi:10.1109/ICASSP.1999.760624
    title: Kjersti Engan, Sven Ole Aase and John Hakon Husoy, Method of optimal directions for frame design, Proceedings of ICASSP 1999
    locator: the whole paper (the least squares dictionary update D = Y X^T (X X^T)^-1)
  - paper: doi:10.1109/TSP.2006.881199
    title: Michal Aharon, Michael Elad and Alfred Bruckstein, K-SVD, an algorithm for designing overcomplete dictionaries for sparse representation, IEEE Transactions on Signal Processing 54(11), 2006
    locator: pages 4311 to 4322 (the problem with a sparsity constraint, the relation to k-means, and the atom by atom update)
  - paper: doi:10.1109/TIP.2006.881969
    title: Michael Elad and Michal Aharon, Image denoising via sparse and redundant representations over learned dictionaries, IEEE Transactions on Image Processing 15(12), 2006
    locator: pages 3736 to 3745 (dictionaries learned from the noisy image itself and patch averaging)
  - paper: doi:10.1109/LSP.2014.2345761
    title: Andreas M. Tillmann, On the computational intractability of exact and approximate dictionary learning, IEEE Signal Processing Letters 22(1), 2015
    locator: pages 45 to 49 (NP-hardness of exact dictionary learning and of approximating it)
  - paper: doi:10.1137/S0097539792240406
    title: B. K. Natarajan, Sparse approximate solutions to linear systems, SIAM Journal on Computing 24(2), 1995
    locator: pages 227 to 234 (sparse approximation with a fixed matrix is NP-hard)
---

Dictionary learning is the problem of finding, from many training signals, a set of atoms such that every signal is close to a combination of a few of them. It is the inverse of [sparse signal recovery](/sparse-signal-recovery/): there the matrix is given and only the sparse vector is unknown, here both are unknown and only the signals are given. It generalizes [k-means](/k-means/), where each signal uses one atom with coefficient 1, and [principal component analysis](/principal-component-analysis/), where all signals share one subspace. This page states the problem and what is known about it. [K-SVD](/k-svd/) is one algorithm for it, and [convolutional sparse coding](/convolutional-sparse-coding/) is the model in which the atoms are small filters shifted over a whole image.

## In plain words

Think of a box of stamps. Every picture in a large collection should be made by pressing only a few stamps, each with its own strength. You do not have the stamps yet. Dictionary learning asks for the box of stamps that does this best for the collection, together with the recipe for each picture. Two things are unknown at once, the stamps and the recipes, and this makes the problem hard. The usual methods fix one, improve the other, and repeat.

## Definition

**Input.** Training signals $y_1, \dots, y_N \in \mathbb{R}^n$, the columns of $Y \in \mathbb{R}^{n \times N}$, a number of atoms $K$ and a sparsity level $s \le K$.

**Output.** A dictionary $D = [d_1, \dots, d_K] \in \mathbb{R}^{n \times K}$ with $\|d_k\|_2 = 1$ and codes $X = [x_1, \dots, x_N] \in \mathbb{R}^{K \times N}$ that solve

$$\min_{D, X}\ \|Y - DX\|_F^2 = \sum_{i=1}^N\|y_i - Dx_i\|_2^2 \quad\text{subject to}\quad \|x_i\|_0 \le s \text{ for all } i.$$

Here $\|x\|_0$ counts the nonzero entries. The dictionary is overcomplete when $K > n$, complete when $K = n$.

**Forward model.** The usual generative model behind the problem is $y_i = D^\star x_i^\star + w_i$ with an unknown dictionary $D^\star$, codes $x_i^\star$ with at most $s$ nonzeros, and noise $w_i$, often Gaussian. The fit above is the maximum likelihood estimate under Gaussian noise when the codes are only known to be $s$-sparse.

**Ambiguities.** Permuting the atoms and permuting the rows of $X$ in the same way, or changing the sign of an atom and of its row of $X$, does not change $DX$. So a solution is at best unique up to these $2^K K!$ signed permutations. The norm constraint removes the scale ambiguity: without it, $D \to cD$ and $X \to X/c$ would make any penalty on the size of $X$ meaningless.

**Uniqueness and stability.** Aharon, Elad and Bruckstein showed in 2006 that if the signals are exactly $s$-sparse in $D^\star$ with $s$ below half the spark of $D^\star$, and the training set contains enough signals in general position on each $s$-dimensional span, then $D^\star$ is unique up to the ambiguities. The number of signals their argument needs is large. With noise, results on stability are local: they say that $D^\star$ is a local minimum of the objective, or of its $\ell_1$ form, for many random sparse codes.

## Variants

- **Penalized form.** $\min_{D, X}\sum_i \tfrac12\|y_i - Dx_i\|_2^2 + \lambda\|x_i\|_1$ with $\|d_k\|_2 \le 1$, as in online dictionary learning (Mairal, Bach, Ponce and Sapiro 2010). Olshausen and Field used a penalty of the same kind, a smooth function that favors sparse codes. For fixed $D$ it is a [LASSO](/lasso-regression/) problem per signal, which is convex.
- **Error target.** $\min\sum_i\|x_i\|_0$ subject to $\|y_i - Dx_i\|_2 \le \varepsilon$ for all $i$. This form is used for denoising, with $\varepsilon$ set by the noise level.
- **Complete and orthogonal dictionaries.** With $K = n$ and $D$ orthogonal, the codes are $D^TY$ thresholded, and the update of $D$ is an orthogonal Procrustes problem solved by one [singular value decomposition](/singular-value-decomposition/). With an invertible $D$ and independent sparse codes the problem is close to [independent component analysis](/independent-component-analysis/).
- **Analysis form.** Learn an operator $\Omega$ such that $\Omega y$ is sparse, instead of atoms that synthesize $y$. The two forms differ when $\Omega$ is redundant; see [analysis and synthesis sparsity](/analysis-and-synthesis-sparsity/).
- **Convolutional form.** The atoms are filters shifted to all positions of a signal. The dictionary is then a union of convolution matrices, and the problem is solved in the Fourier domain. See [convolutional sparse coding](/convolutional-sparse-coding/).
- **Structured dictionaries.** $D = BA$ with a fixed fast transform $B$, for example a [wavelet](/discrete-wavelet-transform/) basis, and a sparse matrix $A$. The product is fast to apply and needs fewer training signals.

## Examples

**Three signals in the plane.** Let $n = 2$, $s = 1$ and

$$Y = \begin{pmatrix}2 & 4 & 1\\ 1 & 2 & -2\end{pmatrix}, \qquad \|Y\|_F^2 = 5 + 20 + 5 = 30.$$

With $K = 2$ the signals lie on the two lines through $(2, 1)$ and $(1, -2)$. The dictionary $d_1 = (2, 1)/\sqrt5$, $d_2 = (1, -2)/\sqrt5$ with codes $x_1 = (\sqrt5, 0)$, $x_2 = (2\sqrt5, 0)$, $x_3 = (0, \sqrt5)$ gives the error 0, so it is optimal. Swapping the two atoms and changing their signs gives the other $2^2 \cdot 2! = 8$ optimal pairs, and there are no more: each atom must be parallel to a signal, and both lines must be used.

With $K = 1$ every signal uses the same atom $d$, the best code is $x_i = \langle d, y_i\rangle$, and the error is $\|Y\|_F^2 - d^TYY^Td$. So $d$ is the top eigenvector of

$$YY^T = \begin{pmatrix}21 & 8\\ 8 & 9\end{pmatrix},$$

with eigenvalues $15 \pm \sqrt{225 - 125} = 25$ and $5$. The top eigenvector is $(2, 1)/\sqrt5$, and the least error is $30 - 25 = 5$, which is $\|(1, -2)\|^2$: the third signal is lost.

**k-means.** If $s = 1$ and the coefficient of the one chosen atom must be 1, with no normalization of the atoms, the problem is exactly [k-means](/k-means/) clustering: each signal picks the nearest atom, and each atom is the mean of its signals. Without the coefficient rule, $s = 1$ is gain-shape [vector quantization](/vector-quantization/): each signal picks the atom with the largest $|\langle d_k, y_i\rangle|$.

**Image patches.** In the denoising method of Elad and Aharon, the signals are the overlapping $8 \times 8$ patches of an image, so $n = 64$, and the dictionary has $K = 256$ atoms. Learned atoms look like localized, oriented edges and textures. Olshausen and Field found the same kind of atoms in 1996 from natural image patches and compared them with the receptive fields of simple cells in the visual cortex.

## Known algorithms

| Method | Dictionary update | What is known |
|---|---|---|
| Alternating minimization (Olshausen and Field 1996) | gradient step on $D$ after sparse inference for each signal | the objective decreases with small steps; no global guarantee |
| MOD, method of optimal directions (Engan, Aase and Husoy 1999) | $D = YX^T(XX^T)^{-1}$, then normalize the atoms | the exact least squares update for fixed $X$; normalization can increase the error slightly |
| [K-SVD](/k-svd/) (Aharon, Elad and Bruckstein 2006) | one atom at a time, with its coefficients, by the top singular pair of the residual on the signals that use it | the objective does not increase with an exact sparse coder; with [OMP](/orthogonal-matching-pursuit/) it can |
| Online dictionary learning (Mairal, Bach, Ponce and Sapiro 2010) | block [coordinate descent](/coordinate-descent/) on accumulated statistics, one signal or batch at a time | for the $\ell_1$ form; scales to millions of signals |
| Methods with guarantees (Spielman, Wang and Wright 2012; Arora, Ge and Moitra 2014; Agarwal and coauthors 2014) | spectral or combinatorial starts, then alternating steps | recover $D^\star$ in polynomial time under random models of the codes, with incoherent atoms and sparsity of order at most about $\sqrt n$ |

All the practical methods alternate between two steps: a sparse coding step with $D$ fixed, which is a [sparse signal recovery](/sparse-signal-recovery/) problem per signal, solved by OMP, [basis pursuit](/basis-pursuit/) or [ISTA](/iterative-shrinkage-thresholding/), and a dictionary update with $X$ or its support fixed. Each step can only decrease the objective when it is solved exactly, but the coding step in the $\ell_0$ form is not solved exactly in practice, and the objective is not convex in $(D, X)$ together. The result depends on the start, often random signals or a DCT basis.

## Bounds

- **Complexity.** The sparse coding step alone, finding the best $s$-sparse code for one signal and a fixed dictionary, is [NP-hard](/np-hard/) (Natarajan 1995). Tillmann (2015) proved that dictionary learning itself is NP-hard: deciding whether $Y$ has an exact factorization $Y = DX$ with $K$ atoms and $s$-sparse columns of $X$ is NP-hard, and so is approximating the problem within certain factors. These are worst case results over all inputs.
- **Rank bound.** $DX$ has rank at most $K$, so by the Eckart-Young theorem every solution has error at least $\sum_{j > K}\sigma_j(Y)^2$, the sum of the squared singular values of $Y$ beyond the $K$-th. For $K \ge n$ this bound is 0 and says nothing.
- **Sample size (a count, not a theorem).** The data hold $nN$ numbers, and the unknowns are $nK$ dictionary entries plus $sN$ code values. For the data to have a chance to determine them, $nN \ge nK + sN$, that is $N \ge nK/(n - s)$. The known guarantees for polynomial time methods need many more signals than this count.
- **Local behavior.** The alternating methods have no bound on the number of iterations needed to reach a global minimum, and they can stop at local minima with atoms that are never used.

## Reductions

- **To k-means.** With $s = 1$, unit coefficients and no normalization, dictionary learning is k-means, and the alternating method is [Lloyd's algorithm](/lloyds-algorithm/). K-SVD was designed as its generalization.
- **To principal component analysis.** With $s = K \le n$, the sparsity constraint is empty and the problem is the best rank $K$ approximation of $Y$, solved by the truncated SVD. The atoms span the top $K$ left singular vectors.
- **From sparse coding.** With $D$ fixed, each column of $X$ is a separate sparse approximation problem. So every method for dictionary learning contains a sparse recovery solver, and its hardness carries over.
- **Union of subspaces.** An $s$-sparse code places each signal in one of the $\binom{K}{s}$ subspaces spanned by $s$ atoms. Dictionary learning is fitting a union of subspaces with a shared set of spanning vectors, a constrained form of subspace clustering.

## Applications

- **Denoising.** Learn the dictionary from the noisy image's own patches, code each patch with an error target set by the noise, and average the overlapping patches (Elad and Aharon 2006). See [image denoising](/image-denoising/).
- **Inpainting.** Code each patch from its known pixels only, then fill the missing pixels from the code. See [image inpainting](/image-inpainting/).
- **Compressed sensing with learned sparsity.** A dictionary learned from similar images replaces a fixed wavelet basis in the reconstruction, for example in MRI.
- **Compression.** Codes with few nonzeros, stored with the indices of their atoms, for classes of signals such as faces.
- **Neuroscience.** The sparse coding model of Olshausen and Field explains the shape of receptive fields in the primary visual cortex.

## References
