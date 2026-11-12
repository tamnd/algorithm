---
tag: N3ZBGQ
kind: algorithm
slug: nonnegative-matrix-factorization
name: Nonnegative matrix factorization
aliases:
- NMF
- nonnegative matrix approximation
area: machine-learning/dimensionality-reduction
level: core
summary: "Approximate a nonnegative matrix V by W H with W and H nonnegative and of rank r. Lee and Seung's multiplicative updates never increase the loss, but exact NMF is NP-hard."
model: real-ram
complexity:
  vars: {m: the number of rows of V, n: the number of columns of V, r: the rank of the factorization, T: the number of iterations}
  time: {worst: "Θ(T (m n r + (m + n) r^2))"}
  space: {extra: "Θ((m + n) r + r^2)"}
properties: {deterministic: false, online: false, exact: false, recursive: false, supervised: false, linear: true}
history:
  year: 1999
  people: [Daniel D. Lee, H. Sebastian Seung, Pentti Paatero, Unto Tapper]
  note: Paatero and Tapper introduced positive matrix factorization in 1994. Lee and Seung's 1999 Nature paper on learning parts of objects made NMF popular, and their 2001 paper proved that the multiplicative updates are monotone.
prereqs: [singular-value-decomposition, matrix-norms]
see_also: [principal-component-analysis, latent-semantic-analysis, latent-dirichlet-allocation, blind-source-separation, independent-component-analysis, np-hard, coordinate-descent, k-means]
sources:
  - paper: doi:10.1038/44565
    title: Daniel D. Lee and H. Sebastian Seung, Learning the parts of objects by non-negative matrix factorization, Nature 401, 1999
    locator: pp. 788 to 791 (parts-based representations of faces and of text, the KL updates)
  - paper: "Daniel D. Lee and H. Sebastian Seung, Algorithms for non-negative matrix factorization, Advances in Neural Information Processing Systems 13 (NIPS 2000), MIT Press, 2001"
    locator: pp. 556 to 562 (the Frobenius and KL multiplicative updates, Theorems 1 and 2, the auxiliary function proofs)
  - paper: doi:10.1002/env.3170050203
    title: Pentti Paatero and Unto Tapper, Positive matrix factorization, a non-negative factor model with optimal utilization of error estimates of data values, Environmetrics 5(2), 1994
    locator: pp. 111 to 126 (the weighted least squares model with nonnegative factors)
  - paper: doi:10.1137/070709967
    title: Stephen A. Vavasis, On the complexity of nonnegative matrix factorization, SIAM Journal on Optimization 20(3), 2009
    locator: pp. 1364 to 1377 (deciding whether the nonnegative rank equals the rank is NP-hard)
  - paper: doi:10.1145/2213977.2214043
    title: Sanjeev Arora, Rong Ge, Ravi Kannan and Ankur Moitra, Computing a nonnegative matrix factorization, provably, Proceedings of the 44th ACM Symposium on Theory of Computing (STOC), 2012
    locator: pp. 145 to 162 (an algorithm polynomial for fixed r, hardness results, and a polynomial algorithm for separable NMF)
  - book: isbn:9781611976403
    title: Nicolas Gillis, Nonnegative Matrix Factorization, SIAM, 2020
    locator: Chapter 3 (nonnegative rank), Chapter 7 (separable NMF), Chapter 8 (iterative algorithms, multiplicative updates)
  - paper: "Joel E. Cohen and Uriel G. Rothblum, Nonnegative ranks, decompositions, and factorizations of nonnegative matrices, Linear Algebra and its Applications 190, 1993"
    locator: pp. 149 to 168 (nonnegative rank and examples where it exceeds the rank)
---

Nonnegative matrix factorization (NMF) approximates a nonnegative $m \times n$ matrix $V$ by a product $W H$ of a nonnegative $m \times r$ matrix $W$ and a nonnegative $r \times n$ matrix $H$, with $r$ small. Each column of $V$ becomes a nonnegative combination of the $r$ columns of $W$, so the factors can only add, never cancel. For images, spectra and word counts, the columns of $W$ then tend to be parts: facial features, chemical components, topics. The standard algorithm is the pair of multiplicative updates of Lee and Seung, which keep the factors nonnegative with no projection and never increase the loss. The problem itself is hard: deciding whether an exact factorization with $r$ equal to the rank exists is [NP-hard](/np-hard/) (Vavasis 2009). For separable matrices it can be solved in polynomial time (Arora, Ge, Kannan and Moitra 2012).

## In plain words

You have a table of nonnegative numbers, such as how often each word appears in each document, or the brightness of each pixel in each face image. NMF writes every column of the table as a mix of a few basic columns, with mixing weights that are never negative. The basic columns are also never negative.

Because nothing can be subtracted, each basic column must be a piece that is added to build the data. For faces, the pieces look like eyes, noses and mouths. For documents, they look like topics, each a group of words that occur together.

The method starts from random pieces and weights, and improves them in turns. Each turn multiplies every number by a ratio that is never negative, so all numbers stay nonnegative, and the error never goes up.

## The problem

Given $V \in \mathbb{R}_{\ge 0}^{m \times n}$ and $r \ge 1$, find
$$ \min_{W \ge 0,\ H \ge 0} \ \lVert V - W H \rVert_F^2 \qquad\text{or}\qquad \min_{W \ge 0,\ H \ge 0} \ D(V \Vert W H) , $$
where $W \in \mathbb{R}^{m \times r}$, $H \in \mathbb{R}^{r \times n}$, $\lVert \cdot \rVert_F$ is the Frobenius norm, and $D(A \Vert B) = \sum_{i j} (A_{i j} \log \frac{A_{i j}}{B_{i j}} - A_{i j} + B_{i j})$ is the generalized Kullback-Leibler divergence. The smallest $r$ with $V = W H$ exactly is the **nonnegative rank** of $V$. It is at least the ordinary rank and can be larger.

The problem is nonconvex in $(W, H)$ together, but convex in $W$ for fixed $H$ and in $H$ for fixed $W$. The solution is never unique: $W H = (W D)(D^{-1} H)$ for any positive diagonal $D$, and the columns of $W$ can be permuted.

## The algorithm

```pseudo id=main
NMF-MULTIPLICATIVE(V, r, T)
L1  W ← random positive m × r matrix;  H ← random positive r × n matrix
L2  for t = 1 to T do
L3      H ← H ∘ (Wᵀ V) ⊘ (Wᵀ W H)                       ▷ entry by entry
L4      W ← W ∘ (V Hᵀ) ⊘ (W H Hᵀ)
L5      if the loss ‖V − W H‖²_F decreased by less than tol times its value then stop
L6  return W, H
```

Here $\circ$ and $\oslash$ are the entrywise product and quotient. Line L3 is a gradient step on $H$ with a different step size for each entry, $\eta_{a j} = H_{a j} / (W^{\top} W H)_{a j}$; this choice cancels the term that could make an entry negative. For the KL divergence the updates are
$$ H_{a j} \leftarrow H_{a j} \frac{\sum_i W_{i a} V_{i j} / (W H)_{i j}}{\sum_i W_{i a}} , \qquad W_{i a} \leftarrow W_{i a} \frac{\sum_j H_{a j} V_{i j} / (W H)_{i j}}{\sum_j H_{a j}} . $$

## Example

Let $V = W_0 H_0$ with
$$ W_0 = \begin{pmatrix} 1 & 0 \\ 2 & 1 \\ 0 & 1 \\ 1 & 3 \end{pmatrix}, \quad H_0 = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 1 & 2 & 1 \end{pmatrix}, \quad V = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 2 & 5 & 2 & 3 \\ 0 & 1 & 2 & 1 \\ 1 & 5 & 6 & 4 \end{pmatrix} . $$
Start from $W$ with all entries 1 and $H = \begin{pmatrix} 1 & 0.5 & 0.5 & 1 \\ 0.5 & 1 & 1 & 0.5 \end{pmatrix}$, so $W H$ has all entries 1.5 and the loss $\lVert V - W H \rVert_F^2$ is 60. The loss after $t$ iterations of lines L3 and L4 is:

| $t$ | 0 | 1 | 2 | 5 | 10 | 50 | 200 | 1000 | 2000 |
|---|---|---|---|---|---|---|---|---|---|
| loss | 60 | 9.21 | 8.82 | 8.29 | 4.97 | 0.0317 | 0.0027 | 0.0001 | 0.000024 |

The loss falls fast at first and then slowly. After 2000 iterations,
$$ W \approx \begin{pmatrix} 1.045 & 0 \\ 2.093 & 0.775 \\ 0 & 0.779 \\ 1.046 & 2.335 \end{pmatrix}, \qquad H \approx \begin{pmatrix} 0.956 & 1.914 & 0.004 & 0.958 \\ 0 & 1.284 & 2.568 & 1.284 \end{pmatrix} . $$
These are $W_0 D$ and $D^{-1} H_0$ with $D \approx \operatorname{diag}(1.045, 0.779)$, up to the small entry 0.004 that is still moving toward 0. The zero pattern of the true factors is found, but a multiplicative update can only approach 0, never reach it.

**Nonnegative rank above the rank.** The matrix
$$ S = \begin{pmatrix} 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 1 \end{pmatrix} $$
has rank 3, because row 1 plus row 4 equals row 2 plus row 3, so the truncated [SVD](/singular-value-decomposition/) fits it exactly with 3 terms. Its nonnegative rank is 4. With $r = 3$, the best of twenty random starts of the multiplicative updates ends with loss about 0.586, not 0. With $r = 4$ the loss goes to 0, as it must, since $S = S I$.

## Correctness

Each update multiplies an entry by a nonnegative ratio, so the factors stay nonnegative, and an entry that is 0 stays 0. For the loss, Lee and Seung use an auxiliary function. For one column $h$ of $H$, the loss is a quadratic with Hessian $P = W^{\top} W$. Replacing $P$ by the diagonal matrix $K = \operatorname{diag}((P h^t)_a / h^t_a)$ gives an upper bound $G(h, h^t)$ that touches the loss at $h^t$, because $K - P$ is positive semidefinite: with $M_{a b} = h^t_a (K - P)_{a b} h^t_b$, $\nu^{\top} M \nu = \frac12 \sum_{a b} P_{a b} h^t_a h^t_b (\nu_a - \nu_b)^2 \ge 0$. The minimizer of $G$ is exactly line L3, so the loss does not increase. Line L4 is the same argument for $V^{\top} \approx H^{\top} W^{\top}$. For the KL updates, Jensen's inequality on the logarithm gives the auxiliary function. The full proofs are below.

## Complexity

The model is the [real RAM](/real-ram/), and the costs count arithmetic operations.

- **One iteration.** $W^{\top} V$ and $V H^{\top}$ cost $\Theta(m n r)$. $W^{\top} W$ and $H H^{\top}$ cost $\Theta((m + n) r^2)$, and multiplying them by $H$ or $W$ costs the same. So an iteration costs $\Theta(m n r + (m + n) r^2)$. Computing the loss for line L5 costs $\Theta(m n r)$, or less with the expansion $\lVert V \rVert_F^2 - 2 \operatorname{tr}(H^{\top} W^{\top} V) + \operatorname{tr}(W^{\top} W H H^{\top})$.
- **Sparse data.** For a sparse $V$ with $N$ nonzero entries, the products with $V$ cost $\Theta(N r)$.
- **Memory.** $\Theta((m + n) r + r^2)$ besides $V$.
- **Hardness.** Exact NMF is NP-hard in general (Vavasis 2009). For fixed $r$ it can be solved in polynomial time in $m$ and $n$ with an algebraic method of degree exponential in $r$ (Arora et al. 2012, improved by Moitra in 2013).

## Properties

- **Monotone, not convergent to a minimum.** The loss never increases, but the limit may be a saddle point or a point that is not stationary on the boundary.
- **Sparse, parts-based factors.** Nonnegativity often makes many entries of $W$ and $H$ small or zero, which is why the factors look like parts. This is a tendency, not a guarantee.
- **Not unique.** Scaling and permutation are always free, and in general there are other factorizations as well. Donoho and Stodden (2003) gave conditions, related to separability, under which the factorization is unique.
- **Not nested.** The best rank-$r$ factors are not the first $r$ of the best rank-$(r+1)$ factors, unlike in the SVD.
- **Loss of accuracy against the SVD.** By the Eckart-Young theorem, the truncated SVD has the smallest Frobenius error of any rank-$r$ factorization. NMF pays some error for nonnegativity.

## Variants and improvements

- **Alternating nonnegative least squares.** Solve for $H$ exactly with $W$ fixed, then for $W$, each by a nonnegative least squares method. It needs fewer iterations than the multiplicative updates.
- **Hierarchical alternating least squares (HALS).** Update one column of $W$ or one row of $H$ at a time in closed form; this is [coordinate descent](/coordinate-descent/) and is usually the fastest simple method.
- **Projected gradient.** Gradient steps followed by clipping at 0, with a line search (Lin 2007).
- **Separable NMF.** If every column of $W$ appears, up to scale, as a column of $V$ (an anchor or pure pixel), then the successive projection algorithm and the method of Arora et al. find the factors in polynomial time, and the result is robust to noise.
- **Sparse and regularized NMF.** Add $\ell_1$ penalties to make the factors sparser, or graph penalties for smooth factors.
- **Other divergences.** The KL divergence corresponds to Poisson noise; the Itakura-Saito divergence is used for audio spectrograms. With the KL loss and normalized factors, NMF is closely related to probabilistic latent semantic analysis.
- **Symmetric NMF.** $V \approx W W^{\top}$ for a similarity matrix, used in clustering. With orthogonality constraints, NMF becomes a relaxation of [k-means](/k-means/).

## When to use it

Use NMF when the data are naturally nonnegative and additive: word counts, images, audio magnitude spectrograms, chemical concentrations, gene expression, and ratings. It gives topics for text (compare [latent semantic analysis](/latent-semantic-analysis/) and [latent Dirichlet allocation](/latent-dirichlet-allocation/)), sources in hyperspectral unmixing and audio separation (a form of [blind source separation](/blind-source-separation/)), and parts for images. Use the SVD or [PCA](/principal-component-analysis/) when you need the smallest error, uniqueness, or orthogonal components, and when signs carry meaning.

## Pitfalls

- **Zero initial entries.** An entry that starts at 0 stays 0 forever. Start from strictly positive matrices.
- **Division by zero.** If a column of $W$ becomes 0, its denominators are 0. Add a tiny constant to the denominators, or detect and restart the column.
- **Slow convergence.** The multiplicative updates can need thousands of iterations, as in the example. Use HALS or alternating nonnegative least squares when speed matters.
- **Local minima.** Different starts give different factors. Run several starts, or use an initialization based on the SVD such as NNDSVD.
- **Choosing $r$.** The loss always falls as $r$ grows. Choose $r$ by held-out error, stability across starts, or the interpretability of the factors.
- **Scaling.** Since $W D$ and $D^{-1} H$ give the same product, normalize the columns of $W$ (or the rows of $H$) before you compare or interpret them.

## Implementations

## History

Pentti Paatero and Unto Tapper introduced positive matrix factorization in 1994, a weighted least squares model with nonnegative factors for environmental data such as air pollution sources. Daniel Lee and Sebastian Seung published the parts-based view in Nature in 1999, with examples on faces and text, and gave the multiplicative updates with monotonicity proofs in 2001. Cohen and Rothblum had already studied the nonnegative rank in 1993. Stephen Vavasis proved NP-hardness in 2009, and Arora, Ge, Kannan and Moitra gave provable algorithms in 2012, including a polynomial algorithm under separability. Nicolas Gillis's 2020 book surveys the field.

## References
