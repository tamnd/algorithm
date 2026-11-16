---
tag: BQH47W
kind: algorithm
slug: brief-descriptor
name: BRIEF descriptor
aliases:
- binary robust independent elementary features
area: computer-vision/local-features
level: core
summary: Describe a keypoint by a string of n_d bits, each the result of one intensity comparison between two random points of a smoothed patch, and compare strings by Hamming distance.
solves: [feature-matching]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, k: the number of keypoints, d: the number of tests, w: the word size}
  time: {worst: O(W H + k d), average: O(W H + k d), best: O(W H + k d)}
  space: {extra: O(W H + k d / w)}
properties: {deterministic: true, exact: true, rotation_invariant: false, scale_invariant: false, heuristic: true}
history:
  year: 2010
  people: [Michael Calonder, Vincent Lepetit, Christoph Strecha, Pascal Fua]
  note: Calonder, Lepetit, Strecha and Fua presented BRIEF at ECCV 2010. The 2012 journal version with Mustafa Ozuysal and Tomasz Trzcinski extended the experiments.
prereqs: [feature-descriptor, hamming-distance]
see_also: [orb-features, brisk-features, swar-popcount, census-transform, local-binary-patterns, locality-sensitive-hashing, fast-corner-detector, feature-matching]
sources:
  - paper: doi:10.1007/978-3-642-15561-1_56
    title: Michael Calonder, Vincent Lepetit, Christoph Strecha and Pascal Fua, BRIEF, binary robust independent elementary features, European Conference on Computer Vision (ECCV 2010), Part IV, LNCS 6314, 778-792
    locator: Section 3 (the test, the descriptor as a sum of powers of 2), Section 3.1 (smoothing), Section 3.2 (the five sampling geometries G I to G V), Section 3.3 (distance distributions), Section 4 (recognition rates and timings)
  - paper: doi:10.1109/TPAMI.2011.222
    title: Michael Calonder, Vincent Lepetit, Mustafa Ozuysal, Tomasz Trzcinski, Christoph Strecha and Pascal Fua, BRIEF, computing a local binary descriptor very fast, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(7), 1281-1298, 2012
    locator: the whole paper (the journal version with more experiments)
  - paper: doi:10.1109/ICCV.2011.6126544
    title: Ethan Rublee, Vincent Rabaud, Kurt Konolige and Gary Bradski, ORB, an efficient alternative to SIFT or SURF, IEEE International Conference on Computer Vision (ICCV), 2564-2571, 2011
    locator: Section 4 (the analysis of BRIEF under rotation and the variance and correlation of its tests)
---

BRIEF (binary robust independent elementary features) is a [feature descriptor](/feature-descriptor/) made of bits. It smooths the image, takes a square patch of side $S$ around a keypoint, and compares the intensities of $n_d$ pairs of points in the patch. Each comparison gives one bit, and the bits form a string of $n_d$ bits, usually 128, 256 or 512. Two descriptors are compared by the [Hamming distance](/hamming-distance/), the number of bits in which they differ, which a computer finds with an exclusive or and a population count. BRIEF does not detect keypoints and does not find an orientation or a scale. It is fast to compute and to match, but it changes when the patch turns by more than a few degrees. [ORB](/orb-features/) adds an orientation to it.

## In plain words

Pick 256 pairs of points in a small square around a keypoint, at random, once. Use the same pairs for all keypoints. For each pair, ask one question: is the first point darker than the second? Write 1 for yes and 0 for no. The 256 answers are the descriptor. To compare two keypoints, count the questions that got different answers. Two views of the same spot give mostly the same answers, so the count is small. Two different spots give answers that agree about half the time. The image is blurred first, so that one noisy pixel does not change an answer. The method does not care about the overall brightness, because the answer to "is this darker than that" stays the same.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with integer values, a list of keypoints $k = (u, v)$, a patch size $S$ and a number of tests $n_d$. A pixel is $(u, v)$, with $u$ the column (to the right) and $v$ the row (down). Let $J$ be $I$ smoothed by a low-pass filter. A test is a pair of offsets $(x_i, y_i)$ in $[-S/2, S/2]^2$, and

$$\tau_i(k) = \begin{cases} 1 & \text{if } J(k + x_i) < J(k + y_i), \\ 0 & \text{otherwise.} \end{cases}$$

The descriptor of $k$ is the number

$$f(k) = \sum_{i=1}^{n_d} 2^{i-1} \tau_i(k),$$

a string of $n_d$ bits. The tests are drawn once, before any image, and stay fixed. For two descriptors $a$ and $b$ the distance is the Hamming distance $\mathrm{popcount}(a \oplus b)$. The output is one descriptor for each keypoint whose patch, with the smoothing window, is inside the image.

Calonder and his coauthors smooth with a Gaussian of variance 2 on a $9 \times 9$ window, and they compare five ways to draw the tests in Section 3.2:

- G I: both points uniform on the patch.
- G II: both points i.i.d. Gaussian, with mean 0 and variance $S^2/25$.
- G III: $x_i$ Gaussian with variance $S^2/25$, and $y_i$ Gaussian around $x_i$ with variance $S^2/100$.
- G IV: points from a coarse polar grid.
- G V: $x_i = 0$ and $y_i$ on a coarse polar grid.

G II did slightly better than the others in their tests, and G V, which compares the center with other points, did worst. The sampling is a design choice, not a result. Points that fall outside the patch are clamped to the border.

## The algorithm

```pseudo id=main
BRIEF(I, keypoints, S, n_d)
L1  J ← I smoothed by the 9 × 9 kernel of variance 2
L2  draw n_d pairs (x_i, y_i), each coordinate Gaussian with variance S^2/25, rounded and clamped to [-S/2, S/2]
L3  for each keypoint k whose patch is inside the image do
L4      d ← 0
L5      for i = 1 to n_d do
L6          if J(k + x_i) < J(k + y_i) then d ← d + 2^(i-1)
L7      output d as the descriptor of k
HAMMING(a, b)
L8  return the number of ones of a XOR b, summed over the words of the strings
```

Our code smooths with the separable binomial kernel $(1, 8, 28, 56, 70, 56, 28, 8, 1)$. This kernel is the distribution of a sum of 8 fair coin flips, so its variance is exactly $8/4 = 2$ in each direction, the variance of the paper, and it is close to a Gaussian. The code keeps the integer sums and does not divide by $256^2$, so every test is an exact integer comparison. Matching takes, for each descriptor of one image, the descriptor of the other image with the smallest Hamming distance. The population count of a 64-bit word uses the [SWAR popcount](/swar-popcount/).

## Example

Take $n_d = 8$ tests on a $5 \times 5$ patch that is already smoothed, with the keypoint at the center. Offsets are $(\Delta u, \Delta v)$.

$$J = \begin{matrix} 10 & 12 & 15 & 19 & 22 \\ 11 & 14 & 18 & 23 & 27 \\ 13 & 17 & 22 & 28 & 33 \\ 14 & 19 & 26 & 34 & 40 \\ 15 & 21 & 29 & 38 & 47 \end{matrix}$$

| $i$ | $x_i$ | $y_i$ | $J(x_i)$ | $J(y_i)$ | $\tau_i$ |
|---|---|---|---|---|---|
| 1 | $(-2, -2)$ | $(2, 2)$ | 10 | 47 | 1 |
| 2 | $(1, 0)$ | $(-1, 0)$ | 28 | 17 | 0 |
| 3 | $(0, -2)$ | $(0, 2)$ | 15 | 29 | 1 |
| 4 | $(2, -1)$ | $(-2, 1)$ | 27 | 14 | 0 |
| 5 | $(-1, 1)$ | $(1, -1)$ | 19 | 23 | 1 |
| 6 | $(0, 0)$ | $(2, 0)$ | 22 | 33 | 1 |
| 7 | $(-2, 2)$ | $(2, -2)$ | 15 | 22 | 1 |
| 8 | $(1, 1)$ | $(0, 0)$ | 34 | 22 | 0 |

The bits from test 1 to test 8 are 10101110, so $f = 1 + 4 + 16 + 32 + 64 = 117$. Now take a second patch with about twice the contrast, 10 more brightness and some noise, for example the first row $30, 33, 37, 44, 49$ and the center 47. The eight comparisons give the same answers, so its descriptor is also 117 and the Hamming distance is 0. Turn the first patch by 90 degrees instead. The bits become 00001111, the number 240, and the Hamming distance to 117 is 3 of 8. Three answers changed because the patch has a gradient to the bottom right, and a turn moves the gradient.

## Correctness

BRIEF is a definition, so correctness means that the algorithm returns $f(k)$ and the Hamming distance as defined, and that the stated invariances hold. The proof in `proofs/correctness.md` shows that:

- Lines L4 to L7 return $f(k)$, and line L8 returns the Hamming distance.
- The descriptor does not change when the image changes by $I \mapsto a I + b$ with $a > 0$, because the smoothing is linear with positive weights that sum to a constant.
- A shift of the image by whole pixels shifts the descriptors with the keypoints.
- For a fixed descriptor and a uniformly random string, the Hamming distance has mean $n_d/2$. This is why unrelated keypoints have distances near $n_d/2$; for real patches the tests are not independent, and the spread is wider.

The ability of BRIEF to tell keypoints apart is a measured result, not a theorem. Calonder and his coauthors measured recognition rates on image sequences with SURF keypoints. In their tests BRIEF-64 did better than SURF and U-SURF on all sequences except Graffiti, BRIEF-32 did slightly worse than BRIEF-64 but compared well, and BRIEF-16 was too short.

## Complexity

The model is the [word RAM](/word-ram/) with integer pixels and a word of $w$ bits. Let $d = n_d$ be the number of tests and $k$ the number of keypoints.

- Line L1 takes $O(W H)$ time with a separable kernel of fixed size.
- Line L2 takes $O(d)$ time.
- Lines L4 to L7 take $O(d)$ time per keypoint, so $O(k d)$ in total.
- A descriptor takes $d / w$ words: 4 words for $d = 256$ and $w = 64$. Line L8 takes $O(d / w)$ time with a popcount of $O(1)$ time per word.
- Matching $m$ descriptors against $n$ by brute force takes $O(m n d / w)$ time.

The extra space is $O(W H)$ for the smoothed image and $O(k d / w)$ for the descriptors. Only the comparisons of line L6 touch the image, so the cost per keypoint does not depend on $S$.

The paper reports timings for 512 keypoints: about 8 to 10 ms for the BRIEF descriptors against 335 ms for SURF-64, and 2 to 8 ms for exact nearest neighbor matching against 28 ms for SURF. These are measurements on the hardware of the authors in 2010, not properties of the method.

## Properties

- **Affine change of intensity.** The descriptor does not change under $I \mapsto a I + b$ with $a > 0$. Each test would also allow an increasing change of the smoothed image, but the smoothing is linear, so a nonlinear change of $I$ can change a test.
- **Not rotation invariant.** The tests are fixed in the image frame. Calonder and his coauthors measured that the recognition rate stays high up to about 10 to 15 degrees and then drops quickly.
- **Not scale invariant.** The patch has a fixed size in pixels. Use it at the scale of a detector, or on a pyramid.
- **Compact.** 256 tests take 32 bytes, against 64 floats for SURF-64 or 128 for SIFT.
- **Cheap to match.** The distance is an exclusive or and a popcount per word.
- **Not learned.** The tests are random. Many of them are correlated, which wastes bits; ORB learns a set of tests with low correlation.

## Variants and improvements

- **BRIEF-16, BRIEF-32, BRIEF-64.** The names give the length in bytes: $n_d = 128$, 256 and 512.
- **U-BRIEF and O-BRIEF.** The upright form is the plain one. An oriented form turns the tests by the orientation of the keypoint, as in [ORB](/orb-features/).
- **rBRIEF.** ORB turns the tests by the orientation from the intensity centroid and learns tests with high variance and low correlation.
- **BRISK and FREAK.** [BRISK](/brisk-features/) uses a fixed pattern of points on circles, smooths each point by its own Gaussian, and takes the orientation from long pairs. FREAK uses a retina-like pattern.
- **Census transform.** The [census transform](/census-transform/) compares each pixel of a window with the center, and [local binary patterns](/local-binary-patterns/) do the same on a circle and keep a histogram.
- **Hashing.** Binary strings fit [locality-sensitive hashing](/locality-sensitive-hashing/) with bit sampling, and ORB uses multi-probe LSH.

## When to use it

Use BRIEF when speed and memory matter more than invariance, for example in tracking between video frames where the camera turns little. Pair it with a fast detector such as [FAST](/fast-corner-detector/). When the camera can turn, use ORB or BRISK, which add an orientation. When large changes of scale or viewpoint occur, a float descriptor such as [SIFT](/sift/) is often more robust.

## Pitfalls

- **No smoothing.** Without smoothing a single noisy pixel flips a test. The paper shows a large loss of recognition rate without it.
- **Different tests.** Two descriptors are comparable only if they use the same pairs in the same order. Fix the seed, or store the pattern.
- **Border.** The patch and the smoothing window must be inside the image. Drop keypoints near the border, or pad the image.
- **Ties.** On flat areas many tests compare equal values and give 0. The test is strict, so equal values always give 0. Our integer smoothing keeps ties exact; float smoothing can break them at random.
- **Rotation.** BRIEF fails when the camera turns by more than about 15 degrees. This is a property of the method, not of the implementation.
- **Popcount.** In Python, `bin(x).count("1")` or `int.bit_count` is the simplest popcount. In C, use the hardware instruction; the SWAR form is the portable fallback.

## Implementations

## History

Calonder, Lepetit, Strecha and Fua published BRIEF at ECCV 2010. Earlier keypoint classifiers of the same group, randomized trees and ferns, already used simple pairwise intensity tests, but they needed training for each scene. The 2012 journal paper added experiments and more authors. In 2011 Rublee and his coauthors built ORB on BRIEF, and Leutenegger, Chli and Siegwart built BRISK with a fixed pattern. Binary descriptors became the default in real-time systems such as ORB-SLAM.

## References
