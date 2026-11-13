---
tag: KQQ4Z2
kind: algorithm
slug: grabcut
name: GrabCut
aliases:
- iterated graph cut segmentation
- Rother-Kolmogorov-Blake segmentation
area: graphics-and-signals/image-processing
level: advanced
summary: Extract the object in a user's rectangle by alternating two steps, fitting foreground and background Gaussian mixtures and taking a minimum cut, until the energy stops falling.
solves: [image-segmentation]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of components in each mixture, I: the number of rounds}
  time: {worst: O(I (N K + N^3)), average: O(I (N K + N^3)), best: O(N K)}
  space: {extra: Θ(N + K)}
properties: {deterministic: false, interactive: true, monotone_energy: true, globally_optimal: false, parameters: "K, γ"}
history:
  year: 2004
  people: [Carsten Rother, Vladimir Kolmogorov, Andrew Blake]
  note: Rother, Kolmogorov and Blake turned the one-shot graph cut of Boykov and Jolly into an iteration with color mixture models and a rectangle as the only input, at SIGGRAPH 2004.
prereqs: [image-segmentation-graph-cuts, gaussian-mixture-model]
see_also: [image-segmentation, k-means, expectation-maximization, edmonds-karp, max-flow-min-cut-theorem, markov-random-field, active-contours, mean-shift-segmentation]
sources:
  - paper: doi:10.1145/1015706.1015720
    title: Carsten Rother, Vladimir Kolmogorov and Andrew Blake, "GrabCut", interactive foreground extraction using iterated graph cuts, ACM Transactions on Graphics 23(3), 309 to 314, 2004 (SIGGRAPH 2004)
    locator: Section 2 (the Boykov-Jolly energy, β and γ = 50), Section 3 (the color mixtures with K = 5, Figure 3 with the iterative algorithm and user editing, the monotone energy, incomplete trimaps) and Section 4 (border matting)
  - paper: doi:10.1109/ICCV.2001.937505
    title: Yuri Y. Boykov and Marie-Pierre Jolly, Interactive graph cuts for optimal boundary and region segmentation of objects in N-D images, Proceedings of the Eighth IEEE International Conference on Computer Vision (ICCV), 2001
    locator: the energy with region and boundary terms, hard constraints from user seeds, and its global minimum by a minimum cut
  - paper: doi:10.1145/321694.321699
    title: Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2), 248 to 264, 1972
    locator: shortest augmenting paths and the O(V E^2) bound, used here for the minimum cut
  - book: isbn:9781848829343
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, Springer, 2011
    locator: Chapter 5, Segmentation, Section 5.5, Graph cuts and energy-based methods
---

GrabCut cuts an object out of a photograph when the user does little more than draw a rectangle around it. It models the colors of the background and of the foreground with two [Gaussian mixtures](/gaussian-mixture-model/), labels every pixel inside the rectangle as foreground or background by a minimum cut of a pixel graph, as in [graph-cut segmentation](/image-segmentation-graph-cuts/), and then refits the mixtures to the new labels. The two steps repeat. At the start the foreground model is polluted by the background pixels inside the rectangle, but each cut moves some of them out, and each refit makes the foreground model cleaner. Every step lowers one energy, so the method stops, at a point that no step can improve. It is not a global optimum of the whole problem, but each cut is a global optimum for the current color models. Carsten Rother, Vladimir Kolmogorov and Andrew Blake published it in 2004, and it is a standard interactive tool for [image segmentation](/image-segmentation/).

## In plain words

You draw a box around the thing you want. Everything outside the box is surely background. Inside the box the program first guesses that everything is foreground. It learns what the background colors look like from the outside, and what the foreground colors look like from the inside of the box. With these two color descriptions it decides, for each pixel in the box, which side it is on. A pixel pays a price for looking unlike its side, and two neighbors with similar colors pay a price for being on different sides. A minimum cut finds the cheapest decision for all pixels at once. Then the program learns the colors again from the new decision, which now has less background in the foreground, and decides again. It stops when the total price stops falling. A few brush strokes can fix what is still wrong.

## The problem

The image is an array $z = (z_1, \dots, z_N)$ of colors in $\mathbb{R}^3$ (or gray values in $\mathbb{R}$). The user gives a trimap: a set $T_B$ of pixels that are surely background, a set $T_F$ of pixels that are surely foreground, which may be empty, and the unknown rest $T_U$. With a rectangle, $T_U$ is the inside and $T_B$ the outside. The output is a hard segmentation $\alpha \in \{0, 1\}^N$, with $\alpha_n = 0$ on $T_B$, $\alpha_n = 1$ on $T_F$, and 1 for foreground.

The model $\theta$ has, for each label $a \in \{0, 1\}$, a mixture of $K$ Gaussians with weights $\pi(a, c)$, means $\mu(a, c)$ and full covariances $\Sigma(a, c)$, $c = 1, \dots, K$. A vector $k$ gives each pixel one component $k_n$ of the mixture of its own label. The data cost of a pixel is

$$D(a, c, \theta, z) = -\log \pi(a, c) + \tfrac{1}{2} \log \det \Sigma(a, c) + \tfrac{1}{2} (z - \mu(a, c))^\top \Sigma(a, c)^{-1} (z - \mu(a, c)),$$

the negative log likelihood up to a constant. The smoothness term sums over the set $C$ of 8-neighbor pairs:

$$V(\alpha, z) = \gamma \sum_{(m, n) \in C} \frac{[\alpha_m \ne \alpha_n]}{\mathrm{dist}(m, n)} \exp\bigl(-\beta \lVert z_m - z_n \rVert^2\bigr), \qquad \beta = \frac{1}{2 \langle \lVert z_m - z_n \rVert^2 \rangle},$$

where $\langle \cdot \rangle$ is the mean over $C$ and $\mathrm{dist}$ is 1 or $\sqrt 2$. A cut through a strong color edge costs little, a cut through a flat region costs up to $\gamma$ per unit length. The paper uses $\gamma = 50$ and $K = 5$. The goal is to make the energy

$$E(\alpha, k, \theta, z) = \sum_n D(\alpha_n, k_n, \theta, z_n) + V(\alpha, z)$$

small over all three of $\alpha$, $k$ and $\theta$.

## The algorithm

```pseudo id=main
GRABCUT(z, T_B, T_F, T_U, K)
L1  α_n ← 0 for n ∈ T_B;  α_n ← 1 for n ∈ T_F ∪ T_U
L2  cluster {z_n : α_n = 0} and {z_n : α_n = 1} into K groups each by k-means;  k_n ← the group of n;  θ ← LEARN(α, k)
L3  repeat
L4      for each pixel n do k_n ← argmin_c D(α_n, c, θ, z_n)
L5      θ ← LEARN(α, k)
L6      α on T_U ← the source side of a minimum s-t cut, with unary costs min_c D(a, c, θ, z_n) and pair weights from V
L7      for each pixel n do k_n ← argmin_c D(α_n, c, θ, z_n);  E ← E(α, k, θ, z)
L8  until E is not below the energy of the round before
L9  return α
```

LEARN fits, for each label $a$ and component $c$, the pixels $F(a, c) = \{ n : \alpha_n = a, k_n = c \}$: the weight is $|F(a, c)|$ divided by the number of pixels with label $a$, and the mean and covariance are the sample mean and sample covariance of their colors. Lines L4 to L6 are steps 1 to 3 of Figure 3 of the paper. Line L7 only measures the energy for the stopping test.

The graph at line L6 has one node per pixel of $T_U$, a source $s$ for foreground and a sink $t$ for background. The edge $s \to n$ has capacity $\min_c D(0, c, \theta, z_n)$, which the cut pays when $n$ ends on the background side, and $n \to t$ has capacity $\min_c D(1, c, \theta, z_n)$, paid when $n$ is foreground. Neighbors in $T_U$ are joined in both directions with their weight from $V$. A neighbor in $T_B$ or $T_F$ has a fixed label, so its weight goes on the unary edge of the label that disagrees with it. Subtracting $\min(\text{both unary costs})$ from both unary edges of a pixel changes every cut by the same constant and makes all capacities non-negative.

The implementation makes two choices that the paper leaves open. A sample covariance is singular for a flat patch of color, so LEARN adds $\varepsilon I$ to it, and the data cost gets the matching term $\tfrac{\varepsilon}{2} \operatorname{tr} \Sigma^{-1}$, the expected rise of the quadratic term when every color has a noise of variance $\varepsilon$. With this term, the regularized covariance is the exact minimizer of step 2, so the monotone energy argument still holds. The minimum cut is [Edmonds-Karp](/edmonds-karp/), which keeps the code short. Line L4 reassigns the components of all pixels. Figure 3 of the paper says "for each n in $T_U$", which leaves the components of $T_B$ at their initial values; both choices lower the energy.

## Example

Take the $6 \times 4$ gray image below, with a bright object of value near 200 on a background near 30. The user rectangle covers columns 1 to 4 of rows 1 and 2, which holds seven object pixels and one background pixel, the 30 at column 3 of row 1. Use $K = 1$, $\gamma = 50$ and $\varepsilon = 1$.

|  | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| row 0 | 30 | 32 | 31 | 29 | 30 | 31 |
| row 1 | 31 | **200** | **205** | **30** | **198** | 30 |
| row 2 | 29 | **202** | **199** | **201** | **203** | 32 |
| row 3 | 30 | 31 | 30 | 29 | 31 | 30 |

The 68 neighbor pairs have a mean squared difference of about 14586, so $\beta \approx 3.43 \times 10^{-5}$. A step of about 170 gray levels gives $\exp(-\beta \cdot 170^2) \approx e^{-1}$, so an edge across the object border weighs about 18 instead of 50.

Line L2 fits the background to the 16 outside pixels, mean 30.375 and variance 1.859 with $\varepsilon$, and the foreground to the 8 pixels in the rectangle, mean 179.75 and variance 3208.9. The polluted foreground model is wide, so the dark pixel at $(3, 1)$ costs only 7.53 as foreground against 0.62 as background. The smoothness term decides it: as foreground it would pay the three edges to the dark pixels above it, $35.4 + 50 + 35.4 = 120.7$, and as background it pays the five edges to its bright neighbors, $17.5 + 19.0 + 18.4 + 13.3 + 12.7 = 80.8$. The first cut puts it in the background and keeps the seven bright pixels. Then the refit at line L5 of round 2 gives the foreground model mean $1408/7 \approx 201.1$ and variance 5.98, and the energy goes from 607.2 at the start to 560.4 after the first cut and 541.4 after the second refit. The second cut keeps the same labels. The third round changes nothing and the energy stays at 541.4, so line L8 stops:

|  | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| row 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| row 2 | 0 | 1 | 1 | 1 | 1 | 0 |

Rows 0 and 3 are all background, as they are outside the rectangle.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows that each of lines L4, L5 and L6 minimizes the energy over one group of variables with the other two fixed. Line L4 is a separate choice per pixel. For line L5, the weights, sample means and regularized sample covariances minimize the data term of each component, which is the classical maximum likelihood fit. For line L6, the capacity of the cut that puts the foreground pixels on the source side equals the energy of that labeling, minimized over $k$, minus a constant, so by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) the cut found by the flow is a labeling of least energy. So the energy never rises. The loop stops at the first round that does not lower it, and this happens after finitely many rounds: the energy at the end of a round is fixed by the labels and components, which take finitely many values, and while the loop runs these energies strictly decrease, so none can repeat. The tests compare the cut with a brute-force search over all labelings of small images and check the monotone energy on random images.

## Complexity

- Lines L4 and L7 cost $O(N K)$ per round for a fixed number of color channels, since each pixel tries every component of its label. Line L5 costs $O(N)$.
- The graph has at most $N + 2$ nodes and $O(N)$ edges. Edmonds-Karp costs $O(V E^2)$, which is $O(N^3)$ here. That bound is loose; the [push-relabel](/push-relabel/) method and the Boykov-Kolmogorov augmenting path method that the authors use are much faster on image grids in practice.
- The total is $O(I (N K + N^3))$ for $I$ rounds. The paper reports that the energy of its example converges in 12 iterations. The best case is one round in which the cut needs few augmenting paths, $O(N K)$.
- Space is $\Theta(N)$ for the graph and labels and $\Theta(K)$ for the mixtures.

## Properties

- **Monotone.** The energy never increases from one step to the next, and the method always stops.
- **Local.** The result depends on the initial components from k-means and on the rectangle. The final point is one where no single step lowers the energy, not a global minimum over $\alpha$, $k$ and $\theta$ together.
- **Each cut is exact.** For fixed color models, line L6 finds a labeling of $T_U$ with the least energy, not an approximation.
- **Hard labels.** The output is 0 or 1 per pixel. Soft edges, hair and motion blur need the border matting step.
- **Firm background only.** With a rectangle, only $T_B$ is firm. Pixels inside may move to the background and back during the rounds, but no pixel outside ever becomes foreground.
- **Contrast-sensitive.** Because $\beta$ is set from the image, a cut between two neighbors whose squared difference equals the mean of the image costs $\gamma e^{-1/2}$ per unit length, whatever the contrast range of the image is.

## Variants and improvements

- **User editing.** After the first result, the user paints a few pixels with a foreground or background brush. They join $T_F$ or $T_B$, and one more cut (line L6) runs with the same models. A refine command runs the whole loop again.
- **Border matting.** The paper fits a soft alpha profile, a smooth step with a center and a width, in a ribbon of 6 pixels on each side of the hard boundary, with regularized parameters along the contour found by dynamic programming.
- **Soft assignments.** Replacing line L4 by soft responsibilities and line L5 by a weighted fit gives [expectation maximization](/expectation-maximization/) for the mixtures. The paper reports that it costs more and gains very little.
- **Other trimaps.** The paper takes $T_B$ as a strip of pixels just outside the rectangle. Common implementations, such as the one in OpenCV, mark everything outside the rectangle as background, as here. A firm foreground instead of a firm background works the same way.
- **Faster cuts.** Since the graph changes little from one round to the next, the flow of the previous round can be reused, which the paper does for user edits.
- **Boykov and Jolly.** With $T_B$ and $T_F$ both given by seed strokes, gray-value histograms in place of mixtures, and one cut instead of a loop, the method is the interactive graph cut of 2001 that GrabCut extends.

## When to use it

Use GrabCut when a person can point at the object and wants a clean cut-out, as in photo editing or when making training masks. It needs only a rectangle, it handles objects whose colors differ from the background even when the edges are weak, and a few strokes repair the rest. Do not use it when the object and the background have the same colors, because the color models then cannot tell them apart and only the smoothness term is left. For segmentation without a user, use [Felzenszwalb segmentation](/felzenszwalb-segmentation/), [mean shift segmentation](/mean-shift-segmentation/) or [SLIC superpixels](/slic-superpixels/), or a learned model. For a boundary that must follow a curve with a shape prior, consider [active contours](/active-contours/). For soft transparency, run a matting method after it.

## Pitfalls

- **Object outside the rectangle.** The outside is fixed background for good. A part of the object that the box cuts off is lost.
- **Singular covariances.** A component that holds a single color, or colors on a line, has $\det \Sigma = 0$ and an infinite data cost. Add a small multiple of the identity, and if you want the energy to stay monotone, add its matching term to the data cost as here.
- **Empty components.** A component can lose all its pixels. Give it weight 0 and skip it; do not refit it from nothing.
- **Shrinking bias.** The smoothness term pays per unit of boundary, so thin parts of the object, such as legs or antennas, are often cut off. A lower $\gamma$ or user strokes help.
- **Two forms of V.** Equation (4) of the paper divides each pair weight by the distance of the two pixels, and equation (11), the color version, does not. Implementations differ on this, and the results differ on diagonal edges.
- **Floating point stop test.** The energy is a sum of logarithms. With a stop test of exact non-decrease, rounding can end the loop one round early or late. Use a small tolerance and a cap on the rounds.

## Implementations

## History

Greig, Porteous and Seheult showed in 1989 that the maximum a posteriori labeling of a binary image under an Ising prior is a minimum cut, so it can be computed exactly. Yuri Boykov and Marie-Pierre Jolly used this in 2001 for interactive segmentation: the user marks seed pixels for object and background, gray-value histograms of the seeds give the region costs, and one minimum cut gives the global optimum of an energy with region and boundary terms. Carsten Rother, Vladimir Kolmogorov and Andrew Blake, at Microsoft Research Cambridge, presented GrabCut at SIGGRAPH 2004. They replaced the histograms with Gaussian mixtures in color, replaced the single cut with the iteration of model fitting and cutting, let the user give only a rectangle, and added border matting for soft edges. GrabCut became one of the standard interactive segmentation methods, and OpenCV has an implementation of the hard segmentation part.

## References
