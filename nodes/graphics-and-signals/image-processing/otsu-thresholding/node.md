---
tag: 5FBGX8
kind: algorithm
slug: otsu-thresholding
name: Otsu's thresholding
aliases:
- Otsu's method
- maximum between-class variance thresholding
- Otsu threshold
area: graphics-and-signals/image-processing
level: intro
summary: Choose the global gray-level threshold that maximizes the between-class variance of the histogram, which is the same as minimizing the within-class variance, in O(N + L) time.
solves: [image-thresholding]
model: word-ram
complexity:
  vars: {N: the number of pixels, L: the number of gray levels}
  time: {worst: Θ(N + L), average: Θ(N + L), best: Θ(N + L)}
  space: {extra: Θ(L)}
properties: {deterministic: true, exact_optimum: true, global_threshold: true, parameter_free: true, histogram_only: true}
history:
  year: 1979
  people: [Nobuyuki Otsu]
  note: Otsu proposed choosing the threshold by discriminant analysis on the gray-level histogram, with the between-class variance as the criterion, in IEEE Transactions on Systems, Man and Cybernetics in 1979.
prereqs: [image-thresholding, image-histogram, variance]
see_also: [image-histogram, hysteresis-thresholding, k-means, prefix-sums, histogram-equalization, image-segmentation, linear-discriminant-analysis, gaussian-mixture-model]
sources:
  - paper: doi:10.1109/TSMC.1979.4310076
    title: Nobuyuki Otsu, A threshold selection method from gray-level histograms, IEEE Transactions on Systems, Man and Cybernetics 9(1), 62 to 66, 1979
    locator: the whole paper (the criteria λ, κ and η, the formula for the between-class variance as a function of the threshold k, and the extension to multithresholding)
  - paper: doi:10.1117/1.1631315
    title: Mehmet Sezgin and Bülent Sankur, Survey over image thresholding techniques and quantitative performance evaluation, Journal of Electronic Imaging 13(1), 2004
    locator: the section on clustering-based thresholding methods, where Otsu's method is listed and compared
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 10, Image segmentation, Section 10.3, Thresholding (optimum global thresholding using Otsu's method, and multiple thresholds)
---

Otsu's thresholding chooses one global threshold $t$ for a gray image from its [histogram](/image-histogram/) alone. The threshold splits the gray levels into a dark class $C_0 = \{0, \ldots, t\}$ and a bright class $C_1 = \{t+1, \ldots, L-1\}$, and Otsu's rule takes the $t$ for which the two classes are best separated in the sense of discriminant analysis: the between-class variance $\sigma_B^2(t)$ is largest. Because the total [variance](/variance/) of the image is the sum of the between-class and the within-class variance, the same $t$ makes the within-class variance smallest. With running sums over the histogram, every threshold is scored in constant time, so the method costs $\Theta(N + L)$ for $N$ pixels and $L$ levels, and it finds the exact best threshold, not an approximation. It is the most common answer to the [image thresholding](/image-thresholding/) problem when the histogram has two clear groups of values.

## In plain words

A gray picture of dark text on light paper has two groups of pixel values: dark ones and light ones. To turn it into pure black and white, you need a cut value. Otsu's method tries every possible cut. For each one, it puts the darker pixels in one group and the lighter pixels in the other, and asks how tight the two groups are around their own averages. The best cut makes the two groups as tight as possible, which is the same as pushing their averages as far apart as possible. The method needs only the count of pixels at each value, and it keeps a running count and a running total while it walks along the values, so each cut is scored at once. It has no setting to tune.

## The problem

The input is a gray [digital image](/digital-image/) with $N \ge 1$ pixels whose values are integers in $\{0, \ldots, L-1\}$, for example $L = 256$ for 8-bit data. Only the values matter, not the positions, so the image enters through its histogram $h_i$, the number of pixels with value $i$, and the probabilities $p_i = h_i / N$. Values can be gamma encoded or linear; the method works on whatever numbers it is given, and the two encodings give different thresholds. A threshold $t \in \{0, \ldots, L-2\}$ makes the binary image $B(p) = 1$ if $I(p) > t$ and $B(p) = 0$ otherwise.

For a threshold $t$ define, as Otsu does,

$$\omega(t) = \sum_{i=0}^{t} p_i, \qquad \mu(t) = \sum_{i=0}^{t} i\, p_i, \qquad \mu_T = \sum_{i=0}^{L-1} i\, p_i.$$

$\omega(t)$ is the share of pixels in $C_0$, $\mu(t)$ is the first moment of $C_0$, and $\mu_T$ is the mean of the whole image. The class means are $\mu_0 = \mu(t)/\omega(t)$ and $\mu_1 = (\mu_T - \mu(t))/(1 - \omega(t))$. The between-class variance is the variance of the two class means, weighted by the class sizes:

$$\sigma_B^2(t) = \omega(1-\omega)(\mu_1 - \mu_0)^2 = \frac{\bigl(\mu_T\, \omega(t) - \mu(t)\bigr)^2}{\omega(t)\bigl(1 - \omega(t)\bigr)}.$$

It is defined when both classes have pixels, that is when $0 < \omega(t) < 1$. Otsu's threshold is a $t$ that maximizes $\sigma_B^2(t)$. If the image has only one value, no threshold separates it, and the method returns nothing.

Otsu also gave the equivalent criteria $\lambda = \sigma_B^2 / \sigma_W^2$, $\kappa = \sigma_T^2 / \sigma_W^2$ and $\eta = \sigma_B^2 / \sigma_T^2$, where $\sigma_W^2$ is the within-class variance and $\sigma_T^2$ the total variance. Since $\sigma_T^2$ does not depend on $t$ and $\sigma_W^2 = \sigma_T^2 - \sigma_B^2$, all three have the same maximizer.

## The algorithm

```pseudo id=main
OTSU(h)                                         ▷ h[0..L−1] holds the histogram
L1  N ← Σ_i h[i]
L2  S ← Σ_i i · h[i]
L3  best ← −1;  t* ← NIL
L4  n0 ← 0;  s0 ← 0                             ▷ count and sum of class C0
L5  for t ← 0 to L − 2 do
L6      n0 ← n0 + h[t];  s0 ← s0 + t · h[t]
L7      if n0 = 0 or n0 = N then continue       ▷ one class is empty
L8      v ← (S · n0 − N · s0)² / (N² · n0 · (N − n0))      ▷ σ_B²(t)
L9      if v > best then
L10         best ← v;  t* ← t
L11 return t*
```

The histogram comes from one pass over the pixels before the call. Line L8 is the formula for $\sigma_B^2(t)$ written with counts: $\omega = n_0/N$ and $\mu = s_0/N$ give $\mu_T \omega - \mu = (S n_0 - N s_0)/N^2$ and $\omega(1-\omega) = n_0(N - n_0)/N^2$. The numbers $n_0$ and $s_0$ are [prefix sums](/prefix-sums/) of $h_i$ and $i h_i$. With integer counts the numerator and denominator are integers, so the comparison at line L9 can be exact (by cross multiplication, or with rationals as in the implementation here). The strict test at line L9 keeps the smallest maximizer.

## Example

Take the $6 \times 3$ image with $L = 8$ and the rows $(0, 1, 1, 2, 6, 7)$, $(1, 1, 2, 2, 6, 6)$ and $(1, 0, 2, 5, 6, 7)$. Its histogram is $h = (2, 5, 4, 0, 0, 1, 4, 2)$, so $N = 18$, $S = 56$ and $\mu_T = 28/9 \approx 3.111$. The total variance is $\sigma_T^2 = 288/18 - (28/9)^2 = 512/81 \approx 6.321$. Lines L5 to L10 give:

| $t$ | $n_0$ | $\mu_0$ | $\mu_1$ | $\sigma_B^2(t)$ |
|---|---|---|---|---|
| 0 | 2 | 0 | 7/2 | 98/81 ≈ 1.210 |
| 1 | 7 | 5/7 | 51/11 | 22801/6237 ≈ 3.656 |
| 2 | 11 | 13/11 | 43/7 | 36481/6237 ≈ 5.849 |
| 3 | 11 | 13/11 | 43/7 | 36481/6237 ≈ 5.849 |
| 4 | 11 | 13/11 | 43/7 | 36481/6237 ≈ 5.849 |
| 5 | 12 | 3/2 | 19/3 | 841/162 ≈ 5.191 |
| 6 | 16 | 21/8 | 7 | 1225/648 ≈ 1.890 |

For $t = 2$, line L8 computes $(56 \cdot 11 - 18 \cdot 13)^2 / (18^2 \cdot 11 \cdot 7) = 382^2 / 24948 = 36481/6237$. The maximum is reached at $t = 2, 3, 4$, because levels 3 and 4 are empty and the three thresholds make the same two classes. Line L9 keeps $t^\ast = 2$. The within-class variance there is $512/81 - 36481/6237 = 109/231 \approx 0.472$, and $\eta = 36481/39424 \approx 0.925$, so the split explains about 92.5% of the variance. The lone pixel of value 5 goes with the bright class: $t = 5$ would put it with the dark class and scores only $5.191$. The binary image has ones exactly at the pixels with values 5, 6 and 7.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three things. First, for each $t$ with both classes nonempty, $\sigma_W^2(t) + \sigma_B^2(t) = \sigma_T^2$, the law of total variance for the two classes, so maximizing $\sigma_B^2$ and minimizing $\sigma_W^2$ pick the same thresholds. Second, the two forms of $\sigma_B^2$ above are equal, and line L8 computes it from $n_0$ and $s_0$, which hold $\sum_{i \le t} h_i$ and $\sum_{i \le t} i h_i$ by induction on $t$. Third, lines L9 and L10 keep the first $t$ with the largest value among the valid ones, and line L7 skips exactly the thresholds with an empty class. So the result is the smallest maximizer of $\sigma_B^2$, or NIL if there is no valid threshold.

The proof file also shows that Otsu's split is the best two-group clustering of the pixel values in the least squares sense: no partition of the pixels into two groups, threshold or not, has a smaller sum of squared distances to the group means. Any two groups can be replaced by "values at most $t$" and "values above $t$" for a suitable $t$ without making the sum larger. So the threshold gives the global optimum of 2-means on the gray values, which [k-means](/k-means/) by Lloyd iteration only finds locally.

## Complexity

- The histogram costs $\Theta(N)$ time and $\Theta(L)$ space.
- Lines L1 and L2 read the histogram once: $\Theta(L)$.
- The loop of lines L5 to L10 runs $L - 1$ times with constant work each time: $\Theta(L)$.

The total is $\Theta(N + L)$ time and $\Theta(L)$ extra space. On the word RAM, $n_0$ and $s_0$ fit in a word of $O(\log N + \log L)$ binary digits, and the numerator of line L8 needs about four times that, so an exact comparison costs a constant number of word operations. Most libraries use double precision instead, which is safe except on near ties. Binarizing the image afterwards is another $\Theta(N)$.

## Properties

- **Exact.** The result is the true maximizer over all $L - 1$ thresholds. Nothing is iterated or approximated.
- **No parameters.** The method has nothing to tune. It needs the number of levels, which the data type fixes.
- **Histogram only.** Two images with the same histogram get the same threshold, whatever the positions of the pixels. The method does not see shape, edges or neighbors.
- **Invariant under an increasing affine map of the levels.** If every value $v$ becomes $a v + b$ with $a > 0$, $\sigma_B^2$ is multiplied by $a^2$ for every split, so the same split wins and the binary image does not change.
- **The cut sits between the class means.** At an optimum, every level in $C_0$ is at most $(\mu_0 + \mu_1)/2$ and every level in $C_1$ is at least that midpoint (proof in the proof file). In the example, $(13/11 + 43/7)/2 \approx 3.66$ lies between the last dark level 2 and the first bright level 5.
- **Plateaus.** Empty bins between two occupied levels give runs of thresholds with the same score. All of them give the same binary image of the input, but a different one for other images that use the threshold.
- **Separability measure.** $\eta^\ast = \sigma_B^2(t^\ast)/\sigma_T^2$ lies in $(0, 1]$. It equals 1 exactly when the image has two values, and a small value warns that the histogram has no clear two-group form.

## Variants and improvements

- **Multilevel Otsu.** For $M$ classes with thresholds $t_1 < \cdots < t_{M-1}$, the between-class variance is $\sum_k \omega_k \mu_k^2 - \mu_T^2$ with $\mu_k$ the mean of class $k$, which Otsu already described. It is a sum of one term per class, each a function of the two ends of the class, so a dynamic program over the last level of each class finds the optimum in $O(M L^2)$ time instead of trying all $\binom{L-1}{M-1}$ tuples. The implementation includes it, and the tests check it against the exhaustive search.
- **Iterative selection.** Ridler and Calvard's isodata method repeats $t \leftarrow (\mu_0 + \mu_1)/2$. It is Lloyd's [k-means](/k-means/) iteration with two clusters on the gray values. It is cheap, but it can stop at a split that is a fixed point and not the best one. Otsu's split is a fixed point of the update, by the midpoint property above, up to the rule for a level that falls exactly on the midpoint.
- **Minimum error thresholding.** Kittler and Illingworth fit two Gaussians with their own variances to the histogram and choose the threshold of least classification error. Otsu's criterion behaves like a fit with equal variances, see the [Gaussian mixture](/gaussian-mixture-model/) page for the general model.
- **Local Otsu.** Applying the method in tiles or in a sliding window gives a threshold that changes over the image, for uneven lighting. Small windows that hold only background then get a meaningless split, so implementations add a test on $\eta^\ast$ or on the local contrast.
- **Two-dimensional Otsu.** Some variants use a joint histogram of the pixel value and a local mean, which makes the split less sensitive to noise, at the cost of $L^2$ bins.
- **Hysteresis.** [Hysteresis thresholding](/hysteresis-thresholding/) uses two thresholds and connectivity. Otsu's value is a common choice for the high threshold.

## When to use it

Use Otsu's method when the image has two populations of values that overlap little, with sizes that are not extremely different: scanned documents, cells on a plain background, parts on a backlit table. It is a good default because it has no parameter and runs in one pass. Do not use one global threshold when the lighting changes across the image; use a local method or correct the background first. Be careful when the object covers a very small share of the image: the criterion is then dominated by the spread of the background, and the best split can fall inside the background hump. When the two classes have very different spreads, the minimum error method or a mixture fit puts the threshold closer to the point where the two densities cross. When the objects differ in color or texture but not in brightness, no gray threshold works, and a [segmentation](/image-segmentation/) method is needed.

## Pitfalls

- **Using the wrong side.** The class $C_0$ includes level $t$. Writing $B(p) = 1$ for $I(p) \ge t$ moves the pixels of value $t$ to the wrong class, which changes the result when $h_t > 0$.
- **Division by zero.** At thresholds where one class is empty, $\omega(1 - \omega) = 0$. Skip them (line L7). Treating them as a score of 0 is also safe, but dividing first gives NaN in floating point, and NaN compares false with everything, which can silently keep a wrong best.
- **Ties and float noise.** On a plateau of empty bins, float rounding can make one threshold of the plateau win by a tiny amount, so two libraries can return different values on the same image. The binary image is the same; a value reused on another image is not. Exact integer comparison avoids this.
- **Unequal class sizes.** When the object is a few percent of the image, or when one class has a much wider spread, the cut lands near the midpoint of the two means and can cut into the tail of the wider class. Check $\eta^\ast$ or use a mixture model.
- **Noise and smoothing.** Pixel noise widens both humps of the histogram and makes them overlap. Smoothing the image before thresholding, for example with a [Gaussian filter](/gaussian-filter/), usually helps more than any change of criterion.
- **Overflow.** The numerator $(S n_0 - N s_0)^2$ grows like $N^4 L^2$ before the division. In 32-bit integer arithmetic it overflows at small image sizes. Use 64-bit floats, 128-bit integers or the normalized form with $p_i$.

## Implementations

## History

Nobuyuki Otsu published the method in 1979 in IEEE Transactions on Systems, Man and Cybernetics. He framed threshold selection as discriminant analysis: the gray levels are split into classes, and the split is judged by the ratio of between-class to within-class or total variance, criteria that come from Fisher's [linear discriminant](/linear-discriminant-analysis/). He showed that the between-class variance as a function of the threshold needs only the zeroth and first cumulative moments of the histogram, gave the separability measure $\eta^\ast$, and extended the method to several thresholds. Ridler and Calvard's iterative method from 1978 is closely related. Later surveys, such as Sezgin and Sankur in 2004, classify Otsu's method among the clustering-based thresholding methods and use it as a reference in comparisons. It is the default global threshold in most image processing libraries.

## References
