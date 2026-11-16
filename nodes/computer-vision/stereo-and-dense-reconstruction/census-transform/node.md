---
tag: GZ7T8F
kind: algorithm
slug: census-transform
name: Census transform
aliases:
- census matching cost
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Replace each pixel by the bit string of whether each neighbor is darker than it, and match pixels by the Hamming distance of their strings.
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, r: the radius of the census window, D: the number of disparities}
  time: {worst: Θ(W H (r^2 + D)), average: Θ(W H (r^2 + D)), best: Θ(W H (r^2 + D))}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1994
  people: [Ramin Zabih, John Woodfill]
  note: Zabih and Woodfill introduced the census and the rank transforms as local transforms that depend only on the order of intensities, for correspondence that tolerates changes of brightness and outliers near depth edges.
prereqs: [stereo-matching-cost, hamming-distance, digital-image]
see_also: [cost-volume, block-matching-stereo, semi-global-matching, swar-popcount, kernighan-popcount, normalized-cross-correlation, adaptive-support-weights, stereo-matching]
sources:
  - paper: doi:10.1007/BFb0028345
    title: Ramin Zabih and John Woodfill, Non-parametric local transforms for computing visual correspondence, Computer Vision, ECCV '94, Lecture Notes in Computer Science 801, Springer, 1994, 151-158
    locator: the whole paper (the rank transform, the census transform, and the Hamming distance as the cost of the census)
  - paper: "Heiko Hirschmüller and Daniel Scharstein, Evaluation of stereo matching costs on images with radiometric differences, IEEE Transactions on Pattern Analysis and Machine Intelligence 31(9), 2009"
    locator: the comparison of census with other matching costs under changes of exposure and light
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (the matching costs of local methods, among them the census transform)
---

The census transform replaces each pixel by a string of bits, one for each neighbor in a small window, where a bit is 1 if that neighbor is darker than the center pixel. Two pixels then match well if their strings differ in few bits, and the [Hamming distance](/hamming-distance/) of the strings is the [matching cost](/stereo-matching-cost/). The string depends only on the order of the intensities in the window, so any strictly increasing change of brightness, such as a different gain, offset or gamma of the second camera, leaves it the same. Zabih and Woodfill (1994) introduced it with the rank transform, and it is the usual cost of [semi-global matching](/semi-global-matching/) and of hardware stereo. On the word RAM the transform costs $\Theta(W H r^2)$ and each cost of the [cost volume](/cost-volume/) costs $O(1)$, one XOR and one popcount of a word.

## In plain words

Look at a small square around a pixel. For each other pixel in the square, write 1 if it is darker than the middle one and 0 if not. The list of ones and zeros is the census of the pixel. To compare a pixel in the left image with one in the right image, compare their two lists and count the places where they differ. Fewer differences mean a better match. If one camera makes the whole picture brighter, darker or more contrasty, every comparison inside the square comes out the same, so the lists do not change. The price is that the list says only "darker or not", and not by how much.

## The problem

**Input.** A rectified pair of grayscale images $I_L$, $I_R$ of $W \times H$ pixels, with integer or real values. Pixel $(u, v)$ is in column $u$ and row $v$; in code it is `img[v][u]`. A window radius $r \ge 1$ and a disparity range $0 \le d < D$.

**Output.** For each pixel $p$ of each image, the census string $T(p)$ of $n = (2r + 1)^2 - 1$ bits:

$$T(p) = \big\Vert_{o \in O} \; \xi\big(I(p), I(p + o)\big), \qquad \xi(a, b) = \begin{cases} 1 & b < a \\ 0 & b \ge a \end{cases}$$

where $O$ is the list of offsets $(du, dv)$ of the window without $(0, 0)$, in row-major order, and $\Vert$ joins the bits, the first one most significant. For each left pixel $p = (u, v)$ and disparity $d$ with $u - d \ge 0$, the census cost

$$C(p, d) = \operatorname{popcount}\big(T_L(u, v) \oplus T_R(u - d, v)\big).$$

At the image border, a neighbor outside the image takes the value of the nearest border pixel. This is a choice of the code; other programs skip the border pixels.

## The algorithm

```pseudo id=main
CENSUS(I, r)
L1  for each pixel p = (u, v) of I do
L2      c ← 0
L3      for each offset o of the window, o ≠ (0, 0), in row-major order do
L4          c ← 2c + [I(p + o) < I(p)]            ▷ append one bit
L5      T(p) ← c
L6  return T

COST(T_L, T_R, u, v, d)
L7  return popcount(T_L(u, v) xor T_R(u - d, v))
```

Line L4 shifts the string left by one and appends the new bit, so after the loop of line L3 the string holds the bits of all $n$ offsets in order. Line L7 marks the bits where the two strings differ with an XOR and counts them. A stereo method calls COST for each pixel and each disparity to fill the [cost volume](/cost-volume/), then [aggregates](/cost-aggregation/) and chooses disparities, as [block matching](/block-matching-stereo/) or [semi-global matching](/semi-global-matching/) do. The code also gives the census cost volume and a winner-takes-all disparity map over a small box.

## Example

Take $r = 1$, so $n = 8$ bits, and these $3 \times 3$ windows around a left pixel and a right pixel, both with center 14:

$$\text{left: } \begin{pmatrix} 12 & 15 & 9 \\ 20 & \mathbf{14} & 14 \\ 7 & 30 & 13 \end{pmatrix}, \qquad \text{right: } \begin{pmatrix} 10 & 16 & 11 \\ 18 & \mathbf{14} & 12 \\ 8 & 29 & 15 \end{pmatrix}.$$

In row-major order the left neighbors are $12, 15, 9, 20, 14, 7, 30, 13$. Those less than 14 give the bits $1, 0, 1, 0, 0, 1, 0, 1$, so $T_L = 10100101_2 = 165$. The neighbor 14 equals the center and gives 0. The right neighbors $10, 16, 11, 18, 12, 8, 29, 15$ give $T_R = 10101100_2 = 172$. Then $T_L \oplus T_R = 00001001_2$, and the cost is 2: the two windows differ in the order of two neighbors against the center. The rank of the left center, the number of neighbors less than it, is $\operatorname{popcount}(165) = 4$.

Now add 20 to every value of the left window, or square every value: the order inside the window stays the same, so $T_L$ stays 165, and the cost stays 2. The sum of absolute differences of the two windows would change from 13 to 181 after adding 20.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three facts. First, after the loop of lines L3 and L4 the integer $c$ is the string $T(p)$ read as a binary number, by an invariant on the number of offsets done. Second, line L7 returns the number of offsets at which the two strings differ, because a bit of the XOR is 1 exactly when the two bits differ. Third, for any strictly increasing function $g$, the census of $g \circ I$ equals the census of $I$, so the census cost of a pair does not change when each image gets its own strictly increasing change of brightness. The proof also shows that a turn of the image by $90°$ permutes the bits of each interior string.

## Complexity

The model is the [word RAM](/word-ram/) with words of $w$ bits and $n = (2r + 1)^2 - 1 \le w$, so each string fits one word. For $r = 3$ the string has 48 bits, and a $9 \times 7$ window has 62 bits; both fit a 64-bit word. Popcount of one word is $O(1)$, as an instruction or by the [SWAR popcount](/swar-popcount/) in $O(\log w)$ word operations, which is $O(1)$ for a fixed $w$.

- **The transform.** Lines L1 to L5 do $n$ comparisons and shifts per pixel, so $\Theta(W H r^2)$ time for each image, and $\Theta(W H)$ words for the strings.
- **The costs.** Line L7 is $O(1)$, so the full cost volume of $W H D$ entries takes $\Theta(W H D)$ time, the same as the absolute difference cost.
- **Total.** The transform of both images and the full cost volume take $\Theta(W H (r^2 + D))$ time, the bound in the front matter.
- **Larger windows.** If $n > w$, each string takes $\lceil n / w \rceil$ words and each cost $O(n / w)$ time.

## Properties

- **Order only.** The census depends only on the order of the values in the window (a theorem). It is unchanged by any strictly increasing change of the image, so it tolerates differences in gain, offset, gamma and exposure between the two cameras, as long as the change is the same over the window.
- **Robust near depth edges.** A neighbor on another surface changes at most one bit, whatever its value, so it adds at most 1 to the cost. With the sum of squared differences, one such pixel can dominate the sum. Zabih and Woodfill gave this as the motivation for both transforms.
- **Loses magnitude.** Two windows with the same order but very different contrast get cost 0. In flat areas with noise, neighbors close to the center flip their bits at random, so the census of a flat area is noisy.
- **Not symmetric in the center.** A neighbor equal to the center gives 0, the same as a brighter one. On images with large flat areas of equal values this treats "equal" as "brighter".
- **Benchmark result.** Hirschmüller and Scharstein (2009) compared matching costs on images with changes of exposure and light, and census was among the best overall. This is an empirical finding on their data, not a theorem.

## Variants and improvements

- **Rank transform.** Zabih and Woodfill also proposed the rank transform: replace each pixel by the number of neighbors less than it, $\operatorname{popcount}(T(p))$, and match the ranks by absolute differences. It keeps less information than the census, because many strings have the same count.
- **Sparse census.** Use only every second offset in each direction. The string is about four times shorter, and the cost is close to that of the full window.
- **Center-symmetric census.** Compare pairs of pixels that are symmetric about the center, instead of each pixel with the center. The string has half the bits and does not depend on the center value alone.
- **Ternary census.** Use three states, darker, similar (within a threshold $\epsilon$) and brighter. It is more stable in flat areas, at the price of the threshold.
- **Modified census.** Compare each pixel of the window with the mean of the window instead of the center pixel.
- **Census with aggregation.** The census cost of one pixel is noisy, so it is summed over a window, as in [block matching](/block-matching-stereo/), or smoothed along paths, as in semi-global matching. This is what the code's `census_disparity` does with a box.

## When to use it

Use the census cost when the two cameras do not have the same response, which is the normal case outside the lab: different exposure, automatic gain, vignetting or a light that hits the two lenses differently. It is cheap in integer hardware, so FPGA and ASIC stereo cameras use it. Use [normalized cross-correlation](/normalized-cross-correlation/) when the change of brightness is affine and you want to keep the contrast information, and the absolute difference or the Birchfield-Tomasi cost when the two images are radiometrically close and fine texture matters. The census is a cost, not a full matcher: it still needs aggregation and a choice of disparities.

## Pitfalls

- **Strict or not strict.** Use $<$ in both images. Using $\le$ in one and $<$ in the other adds a bit of cost at every flat neighbor.
- **Bit order.** Both images must use the same order of offsets, or the Hamming distance compares unrelated bits.
- **Words too short.** A $9 \times 9$ window has 80 bits and does not fit a 64-bit word. Code that packs it into one word silently drops bits.
- **Border.** Pixels within $r$ of the border have windows outside the image. Clamping, as here, gives them strings that repeat the border; skipping them leaves a frame of invalid costs. Either way, do not trust the costs there.
- **Unmatched columns.** For $u - d < 0$ the right pixel does not exist. Give that cost a value larger than any real cost, here $n + 1$, so winner-takes-all never picks it.
- **Flat areas.** In a textureless area all costs are small and the census does not help. That is a limit of all local costs, not a bug.

## Implementations

## History

Zabih and Woodfill (1994) proposed the rank and the census transforms as non-parametric local transforms, to make correspondence robust against changes of brightness and against the outliers that a window collects near a depth edge. Woodfill later built census stereo into hardware. Hirschmüller and Scharstein (2009) found census to be one of the most robust costs in their evaluation, and census became the usual cost of semi-global matching in embedded and automotive stereo.

## References
