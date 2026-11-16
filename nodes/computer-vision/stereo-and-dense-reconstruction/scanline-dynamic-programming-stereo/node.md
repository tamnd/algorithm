---
tag: ZQ13H8
kind: algorithm
slug: scanline-dynamic-programming-stereo
name: Dynamic programming stereo
aliases: []
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Match each pair of scanlines separately by dynamic programming over monotone matchings, with a cost for each occluded pixel, in O(W D) time per line.
solves: [stereo-matching]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, D: the number of disparities}
  time: {worst: Θ(W H D), average: Θ(W H D), best: Θ(W H D)}
  space: {extra: Θ(W D)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1985
  people: [Yuichi Ohta, Takeo Kanade]
  note: Ohta and Kanade matched edge intervals along scanlines by dynamic programming. Cox, Hingorani, Rao and Maggs (1996) gave the pixel version with a maximum likelihood cost and a fixed cost per occluded pixel.
prereqs: [stereo-matching, disparity, stereo-matching-cost]
see_also: [semi-global-matching, graph-cut-stereo, block-matching-stereo, cost-volume, left-right-consistency-check, edit-distance, needleman-wunsch, viterbi-algorithm]
sources:
  - paper: doi:10.1109/TPAMI.1985.4767639
    title: Yuichi Ohta and Takeo Kanade, Stereo by intra- and inter-scanline search using dynamic programming, IEEE Transactions on Pattern Analysis and Machine Intelligence PAMI-7(2), 1985, 139-154
    locator: the matching of the edge intervals of a pair of scanlines as a path search by dynamic programming, and the inter-scanline search that ties the paths of adjacent lines
  - paper: doi:10.1006/cviu.1996.0040
    title: Ingemar J. Cox, Sunita L. Hingorani, Satish B. Rao and Bruce M. Maggs, A maximum likelihood stereo algorithm, Computer Vision and Image Understanding 63(3), 1996, 542-567
    locator: the cost of a matching of two scanlines with occluded pixels, derived as a maximum likelihood, and its minimization by dynamic programming
  - paper: doi:10.1023/A:1008160311296
    title: Stan Birchfield and Carlo Tomasi, Depth discontinuities by pixel-to-pixel stereo, International Journal of Computer Vision 35(3), 1999, 269-293
    locator: the pixel-to-pixel dynamic program with occlusions, and the use of a dissimilarity that is insensitive to image sampling
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the dynamic programming (DP) and scanline optimization (SO) methods of the taxonomy and their results on the benchmark
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (global optimization and dynamic programming along scanlines)
---

Dynamic programming stereo solves [stereo matching](/stereo-matching/) one scanline at a time. In a rectified pair, a pixel of a left row can only match a pixel of the same right row, a few columns to the left. The method looks for the best matching of the two rows as a whole, not pixel by pixel. A matching pairs left and right pixels in the same order in both rows (the ordering constraint), uses each pixel at most once, and leaves some pixels unmatched; these are the occluded pixels, which one camera sees and the other does not. Each matched pair pays a [matching cost](/stereo-matching-cost/) and each unmatched pixel pays a fixed occlusion cost $\kappa$. The best matching is a cheapest monotone path through a $W \times W$ grid, the same structure as in [edit distance](/edit-distance/) and [sequence alignment](/needleman-wunsch/), and dynamic programming finds it exactly. Only a band of width $D$ around the diagonal is needed, so a row costs $\Theta(W D)$ time and an image $\Theta(W H D)$. The method was a standard global stereo method before [semi-global matching](/semi-global-matching/) and [graph cuts](/graph-cut-stereo/); its main weakness is that the rows are solved independently, which leaves horizontal streaks.

## In plain words

Take one row of the left image and the same row of the right image. You want to say which pixel on the left is which pixel on the right. Walk along both rows from left to right at the same time. At each step you either pair the next left pixel with the next right pixel, paying for how different they look, or you skip one pixel in one of the rows, paying a fixed price because that pixel is hidden in the other view. Pixels stay in the same order, so you never go back. A table that stores the best price for every pair of positions finds the cheapest walk. The distance between paired pixels is the disparity. Do this for every row.

## The problem

**Input.** A rectified pair of images of width $W$ and height $H$, a number $D \ge 2$ of disparities, a match cost $c(a, b) \ge 0$ for two intensities, such as $|a - b|$, and an occlusion cost $\kappa \ge 0$. As on the other stereo pages, left pixel $i$ of a row may match right pixel $j = i - d$ of the same row with [disparity](/disparity/) $d \in [0, D)$.

**Output.** For each row, a matching $M$: a set of pairs $(i, j)$ with $0 \le i - j \le D - 1$ that is strictly increasing in both $i$ and $j$, with least cost

$$\mathrm{cost}(M) = \sum_{(i,j) \in M} c(l_i, r_j) + \kappa \cdot (\text{number of unmatched pixels in both rows}) = \sum_{(i,j) \in M} c(l_i, r_j) + 2\kappa (W - |M|).$$

Each matched left pixel $i$ gets disparity $i - j$. An unmatched left pixel is marked occluded.

## The algorithm

$C(i, j)$ is the least cost of matching the first $i$ left pixels with the first $j$ right pixels. Only points with $0 \le i - j \le D - 1$ are stored, as $C(i, k)$ with $k = i - j$.

```pseudo id=main
DP-STEREO-LINE(l, r, D, κ)
L1  C(0, 0) ← 0
L2  for i ← 0 to W do
L3      for k ← min(D - 1, i) down to 0 do   (j = i - k; skip the point (0, 0))
L4          match ← C(i - 1, j - 1) + c(l[i - 1], r[j - 1])      if j ≥ 1
L5          left ← C(i - 1, j) + κ                               if k ≥ 1
L6          right ← C(i, j - 1) + κ                              if j ≥ 1 and k + 1 ≤ D - 1
L7          C(i, j) ← the least of these, and remember which one it was
L8  walk back from (W, W) to (0, 0) along the remembered steps; each match step into (i, j) sets d[i - 1] ← i - j
L9  return C(W, W) and d, with the unmatched left pixels marked occluded
```

A match step keeps $k = i - j$, a left step raises it by 1 and a right step lowers it by 1. This is why $k$ runs downward in line L3: the right step reads $k + 1$ of the same $i$. The full image calls the procedure once per row.

## Example

Take one row with $l = (4, 8, 2, 6)$, $r = (8, 2, 6, 1)$, $D = 2$, $c(a, b) = |a - b|$ and $\kappa = 2$. The right row is the left row moved one pixel to the left, with a new pixel at its end.

| point $(i, j)$ | match | left | right | $C$ |
|---|---|---|---|---|
| (1, 0) | | $0 + 2$ | | 2 |
| (1, 1) | $0 + \lvert 4 - 8 \rvert = 4$ | | $2 + 2 = 4$ | 4 |
| (2, 1) | $2 + \lvert 8 - 8 \rvert = 2$ | $4 + 2 = 6$ | | 2 |
| (2, 2) | $4 + \lvert 8 - 2 \rvert = 10$ | | $2 + 2 = 4$ | 4 |
| (3, 2) | $2 + \lvert 2 - 2 \rvert = 2$ | $4 + 2 = 6$ | | 2 |
| (3, 3) | $4 + \lvert 2 - 6 \rvert = 8$ | | $2 + 2 = 4$ | 4 |
| (4, 3) | $2 + \lvert 6 - 6 \rvert = 2$ | $4 + 2 = 6$ | | 2 |
| (4, 4) | $4 + \lvert 6 - 1 \rvert = 9$ | | $2 + 2 = 4$ | 4 |

The walk back from $(4, 4)$ is: a right step (right pixel 3 is unmatched), match steps into $(4, 3)$, $(3, 2)$ and $(2, 1)$, and a left step (left pixel 0 is unmatched). The result is $d = (\text{occluded}, 1, 1, 1)$ with cost 4: three exact matches and two occluded pixels. Matching all pixels at disparity 0 would cost $4 + 6 + 4 + 5 = 19$. Left pixel 0 is the strip at the left border that the right camera does not see.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). A matching is the same thing as a monotone path from $(0, 0)$ to $(W, W)$ made of match, left and right steps, and the cost of the path is the cost of the matching. Every matching has such a path inside the band $0 \le i - j \le D - 1$ when $D \ge 2$: between two matches, first move the difference $i - j$ to the next value and then alternate left and right steps next to it. The last step into $(i, j)$ is one of three steps, so lines L4 to L7 give the least cost of a path to $(i, j)$ by induction, in an order in which all three inputs are already final. The walk back follows steps that attain the minimum, so it returns a path, and hence a matching, of the least cost $C(W, W)$.

## Complexity

The model is the word RAM with integer intensities and costs.

- **Time.** Each row has $(W + 1) D$ table entries, each found in $O(1)$, and the walk back has at most $2W$ steps: $\Theta(W D)$ per row and $\Theta(W H D)$ per image, the size of the [cost volume](/cost-volume/). The time does not depend on the data, so the worst, average and best cases are the same.
- **Space.** $\Theta(W D)$ for the table and the remembered steps of one row, besides the output.

## Properties

- **Exact per row.** The result is a least cost matching of each row, not an approximation.
- **Occlusions in the model.** Unmatched pixels are part of the answer. The strip at the left border that the right camera does not see can come out as occluded, as in the example, with no special code.
- **Ordering constraint.** Matches keep their order. This holds for most scenes, but fails for thin objects in front of a far background, such as a pole, where the order of points is different in the two views.
- **Rows are independent.** No term ties a row to the next one, so errors differ from row to row and show up as horizontal streaks.
- **Uniqueness.** Each pixel is matched at most once, in both images.

## Variants and improvements

- **Intervals instead of pixels.** Ohta and Kanade (1985) matched intervals between edges and added an inter-scanline search over connected edges, which ties adjacent rows.
- **Ties between rows.** Cox et al. (1996) and later authors add costs for disparity jumps, also across rows, or use the edges of the image to guide where a jump may happen.
- **Sampling-insensitive costs.** Birchfield and Tomasi (1999) used a dissimilarity that does not change when the pixel grid is shifted by part of a pixel.
- **Scanline optimization.** The SO method of Scharstein and Szeliski (2002) drops the occlusion model and instead runs a [Viterbi](/viterbi-algorithm/) pass over the disparity labels of one row, with a cost for each jump. [Semi-global matching](/semi-global-matching/) runs such passes along 8 or 16 directions and adds them, which removes most streaks.
- **Global methods.** [Graph cut stereo](/graph-cut-stereo/) minimizes an energy with occlusions over the whole image at once.

## When to use it

Use it when you need a fast method with an explicit model of occlusion along the baseline, for example on small embedded systems or as a teaching example of global stereo. For better quality at a similar cost, use [semi-global matching](/semi-global-matching/). Use [block matching](/block-matching-stereo/) when you need the simplest local method.

## Pitfalls

- **Disparity range of one.** With $D = 1$ the band is only the diagonal, so no pixel can be skipped and the band lemma fails. Use $D \ge 2$, or treat $D = 1$ on its own.
- **The direction of the shift.** The code assumes that left pixel $i$ matches right pixel $i - d$ with $d \ge 0$. With the cameras the other way round, swap the images or mirror the rows.
- **Choosing $\kappa$.** A small $\kappa$ makes skipping cheaper than matching, and the result is mostly occluded. A large $\kappa$ forces matches, also in true occlusions. Set $\kappa$ against the typical cost of a correct match.
- **Streaks.** Do not expect smooth results in the vertical direction. Filter the result across rows, or use a method that ties the rows.
- **Thin foreground objects.** The ordering constraint makes the method miss them; a [left-right consistency check](/left-right-consistency-check/) does not fix that.

## Implementations

## History

Ohta and Kanade (1985) introduced dynamic programming for stereo: they matched intervals between edges on pairs of scanlines and searched across scanlines as well. Cox, Hingorani, Rao and Maggs (1996) derived a pixel-based cost with a fixed price per occluded pixel from a maximum likelihood model and minimized it by dynamic programming per row. Birchfield and Tomasi (1999) combined this kind of program with their sampling-insensitive dissimilarity to find depth discontinuities. Scharstein and Szeliski (2002) included dynamic programming and scanline optimization in their taxonomy and measured them on a common benchmark against local methods and graph cuts.

## References
