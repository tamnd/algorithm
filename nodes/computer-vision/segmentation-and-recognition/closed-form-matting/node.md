---
tag: YQKAHR
kind: algorithm
slug: closed-form-matting
name: Closed-form matting
aliases:
- Levin-Lischinski-Weiss matting
- matting Laplacian
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Find a soft alpha matte from a few scribbles. Alpha is affine in the color in each small window, so F and B drop out and alpha solves one sparse linear system."
solves: [image-matting]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels}
  time: {worst: O(W^3 H^3), average: O(W^3 H^3), best: O(W^2 H^2)}
  space: {extra: O(W^2 H^2)}
properties: {deterministic: true, exact: true, global_optimum: true, soft_output: true, interactive: true}
history:
  year: 2006
  people: [Anat Levin, Dani Lischinski, Yair Weiss]
  note: "Levin, Lischinski and Weiss (CVPR 2006, TPAMI 2008) eliminated the foreground and background colors from a local linear model and got a quadratic cost in alpha alone, with the matting Laplacian."
prereqs: [image-matting, laplacian-matrix, ridge-regression]
see_also: [random-walker-segmentation, guided-filter, spectral-clustering, normalized-cut, porter-duff-compositing, conjugate-gradient-method, multigrid-method, grabcut]
sources:
  - paper: doi:10.1109/CVPR.2006.18
    title: "Anat Levin, Dani Lischinski and Yair Weiss, A closed form solution to natural image matting, CVPR 2006, vol. 1, 61-68"
    locator: "Section 2 (cost 3, Theorem 1, Laplacian 5), Section 2.1 (color model 9 to 12, Theorem 2), Section 3 (constraints 13, Theorem 3), Section 4 (spectral analysis), Section 5 (results and solvers)"
  - paper: doi:10.1109/TPAMI.2007.1177
    title: "Anat Levin, Dani Lischinski and Yair Weiss, A closed-form solution to natural image matting, IEEE TPAMI 30(2), 228-242, 2008"
    locator: "The journal version, with more analysis and experiments"
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Section 10.4, on image matting"
---

Closed-form matting is an algorithm that computes a soft alpha matte from a few strokes that the user paints on the foreground and on the background. It assumes that in each small window, alpha is an affine function of the color. With this model the unknown foreground and background colors drop out, and the matte minimizes a quadratic cost $\alpha^T L \alpha$, where $L$ is the *matting Laplacian*. With alpha fixed on the strokes, the minimum is the solution of one sparse linear system. This page covers the derivation, the solve and the properties of $L$. The general problem, with the compositing equation and other methods, is on [image matting](/image-matting/).

## In plain words

A photo of hair or smoke has pixels that are part foreground and part background. Matting finds, for each pixel, how much of it is foreground. That share is called alpha.

The user paints a few white strokes on the foreground and a few black strokes on the background. The method assumes that in each tiny patch of the image, alpha follows the color in a simple straight-line way. Within a patch, a brighter pixel is a bit more foreground, or a bit less, by a fixed rate.

These patches overlap, so the rule passes the painted values from patch to patch across the image. The best alpha for all patches at once comes from one large set of linear equations. No guess of the true foreground and background colors is needed.

## The problem

The input is an image $I$ with $N = WH$ pixels and colors $I_i \in \mathbb R^c$ ($c = 1$ for gray, $c = 3$ for color), a set $S$ of scribbled pixels with values $s_i$ (1 for foreground, 0 for background), and a small $\epsilon > 0$. The output is a matte $\alpha \in \mathbb R^N$ with $\alpha_i = s_i$ on $S$.

The image model is the compositing equation $I_i = \alpha_i F_i + (1 - \alpha_i) B_i$ (Levin, Lischinski and Weiss 2006, equation 1). For a gray image where $F$ and $B$ are about constant on a small window $w$, it gives
$$\alpha_i \approx a I_i + b, \qquad a = \frac{1}{F - B}, \quad b = -\frac{B}{F - B}, \qquad i \in w .$$
For color, the model is $\alpha_i \approx a^T I_i + b$ (equation 9). The cost is (equations 3 and 10)
$$J(\alpha, a, b) = \sum_k \Bigl( \sum_{i \in w_k} \bigl(\alpha_i - a_k^T I_i - b_k\bigr)^2 + \epsilon \lVert a_k \rVert^2 \Bigr),$$
with one $3 \times 3$ window $w_k$ around each pixel $k$. The term $\epsilon \lVert a_k \rVert^2$ makes the problem well posed in flat windows and prefers smooth mattes.

## The algorithm

Theorem 1 of the paper eliminates $a$ and $b$: $\min_{a, b} J(\alpha, a, b) = \alpha^T L \alpha$, with
$$L_{ij} = \sum_{k : i, j \in w_k} \Bigl( \delta_{ij} - \frac{1}{|w_k|}\Bigl(1 + (I_i - \mu_k)^T \bigl(\Sigma_k + \tfrac{\epsilon}{|w_k|} \mathrm{Id}\bigr)^{-1} (I_j - \mu_k)\Bigr) \Bigr),$$
where $\mu_k$ and $\Sigma_k$ are the mean and the covariance of the colors in $w_k$ (equation 12; equation 5 is the gray case). The matte is (equation 13)
$$\alpha = \arg\min_\alpha \alpha^T L \alpha \quad \text{subject to} \quad \alpha_i = s_i \text{ for } i \in S .$$

```pseudo id=main
CLOSED-FORM-MATTING(I, S, s, ε)
L1  L ← the N × N zero matrix                       ▷ sparse in practice
L2  for each 3 × 3 window w_k inside the image do
L3      μ_k ← mean of I over w_k;  Σ_k ← covariance of I over w_k
L4      M_k ← (Σ_k + ε / |w_k| · Id)⁻¹                ▷ a c × c inverse
L5      for each i, j in w_k do L_ij ← L_ij + δ_ij - (1 + (I_i - μ_k)ᵀ M_k (I_j - μ_k)) / |w_k|
L6  U ← the pixels not in S
L7  solve L_UU α_U = -L_US s
L8  α_S ← s;  return α
```

Lines L6 to L8 set the gradient of $\alpha^T L \alpha$ to zero on the free pixels, which solves equation 13 exactly. Many implementations use a soft form instead, with a large weight on the scribbles; as the weight grows, its solution tends to the hard one.

## Example

Take a gray image of 3 rows, each with the values $0.1, 0.2, 0.5, 0.9, 0.9$. This is a blurred edge between a background of $B = 0.1$ and a foreground of $F = 0.9$. The left column is scribbled as $0$ and the right column as $1$. The true matte is $\alpha = (I - 0.1)/0.8 = 0, 0.125, 0.5, 1, 1$ in each row. It is an affine function of $I$ in every window, so Theorem 3 of the paper says it is optimal for $\epsilon = 0$. The middle row of the result:

| $\epsilon$ | col 0 | col 1 | col 2 | col 3 | col 4 |
|---|---|---|---|---|---|
| $10^{-6}$ | 0 | 0.1250 | 0.5000 | 1.0000 | 1 |
| $0.1$ | 0 | 0.2295 | 0.5120 | 0.8615 | 1 |

With a small $\epsilon$ the method finds the true matte. With a large $\epsilon$ the term $\epsilon a^2$ pulls each window toward a flat alpha, and the matte gets smoother than the truth. The test file checks both rows.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The facts that are proved:

- **Theorem (elimination).** In each window, the minimum over $(a, b)$ is a [ridge regression](/ridge-regression/), and its value is $\alpha^T L_{w} \alpha$. Summing over the windows gives $\min_{a,b} J = \alpha^T L \alpha$. This is Theorem 1 of the paper.
- **Theorem (shape of $L$).** $L$ is symmetric and positive semidefinite, and each row sums to $0$. For $\epsilon > 0$ its null space is exactly the constant vectors. The paper calls $L$ positive definite, but $L \mathbf 1 = 0$, so it is only semidefinite.
- **Theorem (unique matte).** For $\epsilon > 0$ and at least one scribble, $L_{UU}$ is positive definite, so line L7 has exactly one solution, and it is the minimizer of equation 13.
- **Theorem (exact recovery).** If alpha is affine in the color in each window, the scribbles agree with it, and $\epsilon = 0$, then the true alpha is a minimizer. This is Theorem 3 of the paper. Its Theorem 2 shows that the affine model holds when the foreground and the background colors of each window each lie on a line in color space.

The method has no maximum principle. The matte can leave $[0, 1]$, and the test file has such a case. In practice the result is clipped to $[0, 1]$.

## Complexity

The cost model is the [real-RAM](/real-ram/). Let $N = WH$. Each window has 9 pixels, so lines L2 to L5 cost $O(N c^3 + 81 N) = O(N)$ time for a fixed $c$. In a sparse format $L$ has at most 25 nonzeros per row, because two pixels share a $3 \times 3$ window only when they are at most 2 apart in each direction.

- **Dense solve, as in the code.** The code stores $L$ as a dense matrix, which costs $O(N^2)$ space and $O(N^2)$ time to fill. Line L7 costs $O(N^3) = O(W^3 H^3)$ time by Gaussian elimination. These are the bounds in the front matter. They are theorems about the code.
- **Sparse direct solve.** With nested dissection on a grid with a fixed neighborhood, the factorization costs $O(N^{3/2})$ time. This is a theorem for grid-like sparsity.
- **Iterative solvers.** Each [conjugate gradient](/conjugate-gradient-method/) step costs $O(N)$, and the number of steps depends on the condition number of $L_{UU}$, which grows as $\epsilon$ shrinks.

The paper reports 20 seconds for a $200 \times 300$ image with the direct sparse solver of MATLAB on a 2.8 GHz CPU, and a [multigrid](/multigrid-method/) solver that takes a couple of seconds for very large images with a small loss in quality. These are benchmark results.

## Properties

- **Global optimum.** The cost is quadratic and convex, so the solve gives the exact minimizer, not a local one.
- **No estimate of $F$ and $B$.** The colors are eliminated, so the method does not need a model of the color distributions, unlike Bayesian matting.
- **Few scribbles.** The overlapping windows spread the scribbles over the image, so a few strokes can be enough. A full trimap also works.
- **Symmetry.** Swapping the scribble values $0$ and $1$ gives $1 - \alpha$, and a constant scribble value gives a constant matte.
- **Spectral view.** $L = D - W$ is a graph Laplacian with the *matting affinity*, which can be negative. Its eigenvectors with small eigenvalues look like soft segments, and the paper uses them to guide where the user should scribble (Section 4).
- **Window size.** Wider windows help when the colors are complex, but $L$ gets denser. The paper solves with $3 \times 3$ windows on a coarse image and moves the coefficients to the fine image.

## Variants and improvements

- **Foreground colors.** After $\alpha$ is known, $F$ and $B$ can be found from another quadratic problem, for compositing on a new background. The paper discusses this in Section 5.
- **Spectral matting.** Levin, Rav-Acha and Lischinski (2008) build mattes from the small eigenvectors of $L$ without scribbles, as a set of matting components.
- **Guided filter.** He, Sun and Tang (2010) use the same local linear model as an edge-preserving filter, and point out its link to the matting Laplacian. See [guided filter](/guided-filter/).
- **Learned and sampled methods.** Later methods combine $L$ with color sampling or with learned priors. Deep networks now lead the matting benchmarks.
- **Random walk matting.** Grady and others used a graph Laplacian with Gaussian weights, as in the [random walker](/random-walker-segmentation/). The matting Laplacian replaces those weights with the local linear model.

## When to use it

Use it to pull a soft matte for hair, fur, smoke or motion blur, when the user can paint a few strokes or give a trimap and the colors in small windows are simple. It is a good baseline and a good final step after a hard segmentation such as [GrabCut](/grabcut/). For a hard object mask, use a segmentation method. For complex or overlapping color distributions, a learned method may do better.

## Pitfalls

- **Choice of $\epsilon$.** A large $\epsilon$ smooths the matte. An $\epsilon$ near $0$ makes $L$ ill conditioned in flat or one-line windows, where $\Sigma_k$ is singular. The paper uses $\epsilon = 0.0001$ in its spectral example.
- **Scale of the colors.** The meaning of $\epsilon$ depends on whether colors are in $[0, 1]$ or in $[0, 255]$.
- **Values outside $[0, 1]$.** Clip the result.
- **Border windows.** The windows here lie inside the image. Each pixel is still in at least one window, but border pixels are in fewer windows, so they are less constrained.
- **Memory.** A dense $L$ is far too large for real images. Use a sparse matrix and a sparse or iterative solver.
- **No scribble on a part of the image.** With few scribbles, an area far from both can get an alpha near $0.5$, or a value set by the eigenvectors of $L$. Check the result and add strokes there.

## Implementations

The Python code in `impl/python/closed_form_matting.py` builds the dense matting Laplacian for gray or color images (lines L1 to L5), using the $3 \times 3$ inverse of `cvla.py`, and solves the hard constraints of lines L6 to L8. It also computes the cost $J$ by direct least squares in each window. The tests check the example above, the symmetry, the zero row sums and the semidefinite spectrum of $L$, Theorem 1 against the direct least squares, the null space for $\epsilon = 0$, exact recovery of a synthetic matte, the minimality of the solution, the $0$ and $1$ symmetry, and a case where alpha leaves $[0, 1]$.

## History

Blue screen matting goes back to film work, and Smith and Blinn (1996) showed that the matting equation is underdetermined without extra assumptions. Bayesian matting (Chuang and others, 2001) and Poisson matting (2004) needed a trimap and estimated $F$ and $B$. Levin, Lischinski and Weiss used the idea of their colorization method (2004), a quadratic cost spread by overlapping windows, and found the local linear model that removes $F$ and $B$. The CVPR paper appeared in 2006, and the journal version in 2008. The matting Laplacian became a standard tool: it was used for dehazing, for spectral matting, as a term in many later matting methods, and it led to the guided filter.

## References
