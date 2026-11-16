---
tag: BQGMR7
kind: algorithm
slug: local-binary-patterns
name: Local binary patterns
aliases:
- LBP
- LBP texture descriptor
area: computer-vision/local-features
level: core
summary: Code each pixel by the signs of the differences to P neighbors on a circle, then describe a region by the histogram of the codes, often in the uniform or rotation invariant form.
solves: [object-recognition]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, P: the number of neighbors on the circle}
  time: {worst: O(W H P + 2^P P), average: O(W H P + 2^P P), best: O(W H P + 2^P P)}
  space: {extra: O(2^P)}
properties: {deterministic: true, exact: true, gray_scale_invariant: true, rotation_invariant: false, heuristic: false}
history:
  year: 1996
  people: [Timo Ojala, Matti Pietikainen, David Harwood]
  note: Ojala, Pietikainen and Harwood compared texture measures in 1996 and introduced the 3 x 3 LBP code. Ojala, Pietikainen and Maenpaa gave the circular LBP with P and R and the uniform and rotation invariant codes in 2002.
prereqs: [feature-descriptor, image-histogram]
see_also: [census-transform, brief-descriptor, histogram-of-oriented-gradients, bilinear-interpolation, chi-squared-goodness-of-fit-test, spatial-pyramid-matching, face-detection, hamming-distance]
sources:
  - paper: doi:10.1016/0031-3203(95)00067-4
    title: Timo Ojala, Matti Pietikainen and David Harwood, A comparative study of texture measures with classification based on featured distributions, Pattern Recognition 29(1), 51-59, 1996
    locator: the whole paper (the 3 x 3 LBP code, the LBP/C pair with a contrast measure, classification by the distance of histograms)
  - paper: doi:10.1109/TPAMI.2002.1017623
    title: Timo Ojala, Matti Pietikainen and Topi Maenpaa, Multiresolution gray-scale and rotation invariant texture classification with local binary patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(7), 971-987, 2002
    locator: the section on gray-scale and rotation invariant local binary patterns (the circular neighbor set, the sign function, the ri and riu2 codes, the uniformity measure U)
  - paper: doi:10.1109/TPAMI.2006.244
    title: Timo Ahonen, Abdenour Hadid and Matti Pietikainen, Face description with local binary patterns, application to face recognition, IEEE Transactions on Pattern Analysis and Machine Intelligence 28(12), 2037-2041, 2006
    locator: the whole paper (a grid of regions, one u2 histogram per region, the concatenated histogram, the weighted chi-square distance)
---

Local binary patterns (LBP) describe the texture of a region of an image. For each pixel, the method compares $P$ neighbors on a circle of radius $R$ with the center. Each comparison gives one bit, so each pixel gets a $P$-bit code. The descriptor of the region is the histogram of the codes. Only the signs of the differences go into the code, so the code does not change when the brightness of the image changes by any increasing function. A mapping of the codes, such as the uniform code u2 or the rotation invariant uniform code riu2, makes the histogram shorter and more stable. LBP is a [feature descriptor](/feature-descriptor/) for regions and is a close relative of the [census transform](/census-transform/) in stereo.

## In plain words

Look at a pixel and at a ring of pixels around it. Write a 1 for each ring pixel that is at least as bright as the center, and a 0 for each that is darker. Read the bits around the ring as one binary number. A flat area, a spot, an edge and a corner give different numbers. Do this for every pixel of a region and count how often each number occurs. The counts describe the texture of the region. If you make the whole image brighter, or increase the contrast, each comparison gives the same answer, so the counts stay the same. Most counts come from simple patterns with at most two changes between 0 and 1 around the ring. Many methods keep these simple patterns and put all other patterns into one shared bin.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows, a number of neighbors $P \ge 1$, a radius $R > 0$ and a mapping of codes to labels. A pixel is $(u, v)$, with $u$ the column (to the right) and $v$ the row (down). Neighbor $p$, for $p = 0, \dots, P - 1$, of the center $c = (u, v)$ is at

$$\Big(u + R\cos\tfrac{2\pi p}{P},\; v - R\sin\tfrac{2\pi p}{P}\Big).$$

So neighbor 0 is to the right, and the neighbors go counterclockwise on the screen. If the point is not a pixel center, its value $g_p$ comes from [bilinear interpolation](/bilinear-interpolation/) of the four pixels around it. The paper of 2002 places neighbor $p$ at $(-R\sin(2\pi p/P), R\cos(2\pi p/P))$; another start or direction only turns the bit order by a fixed amount. With $g_c$ the value of the center and $s(x) = 1$ for $x \ge 0$ and $s(x) = 0$ for $x < 0$, the code is

$$\mathrm{LBP}_{P,R}(c) = \sum_{p=0}^{P-1} s(g_p - g_c)\, 2^p .$$

The number of circular 0/1 changes of a code is

$$U = \big|s(g_{P-1} - g_c) - s(g_0 - g_c)\big| + \sum_{p=1}^{P-1} \big|s(g_p - g_c) - s(g_{p-1} - g_c)\big| .$$

A code is uniform when $U \le 2$. The four common mappings are:

- none: the code itself, with $2^P$ labels.
- u2: one label for each uniform code and one shared label for all other codes. This gives $P(P - 1) + 3$ labels, 59 for $P = 8$.
- riu2: for a uniform code, the number of ones, which is $0, \dots, P$; for any other code, $P + 1$. This gives $P + 2$ labels, 10 for $P = 8$.
- ri: the smallest of the $P$ circular rotations of the code. This gives one label for each binary necklace of length $P$, 36 for $P = 8$.

The output is the histogram of the labels over all pixels whose circle is inside the image. A region descriptor is the same histogram over one region.

## The algorithm

```pseudo id=main
LBP(I, P, R, map)                     ▷ map gives the label of each P-bit code
L1  for p = 0 to P - 1 do (du_p, dv_p) ← (R cos(2πp/P), -R sin(2πp/P))
L2  h ← a histogram of zeros, one bin for each label of map
L3  for each pixel c = (u, v) whose circle is inside I do
L4      code ← 0
L5      for p = 0 to P - 1 do
L6          g_p ← the bilinear value of I at (u + du_p, v + dv_p)
L7          if g_p - g_c ≥ 0 then code ← code + 2^p
L8      h[map(code)] ← h[map(code)] + 1
L9  return h
```

The mapping is a table of $2^P$ entries that the code builds once. For u2 and riu2 it counts the changes $U$ of each code, and for ri it takes the smallest rotation. The comparison of two regions uses a distance of histograms. Ojala and his coauthors used the log-likelihood statistic and other distances; the chi-square distance $\sum_b (h_b - k_b)^2 / (h_b + k_b)$ is common, and Ahonen, Hadid and Pietikainen used a weighted form of it for faces.

## Example

Take the $3 \times 3$ image below with $P = 8$, $R = 1$ and the center value $g_c = 6$.

$$\begin{matrix} 6 & 5 & 2 \\ 7 & 6 & 1 \\ 9 & 8 & 7 \end{matrix}$$

The neighbors 0, 2, 4 and 6 are pixel centers: right 1, top 5, left 7 and bottom 8. The neighbors 1, 3, 5 and 7 are at a distance of about 0.707 along both axes and need interpolation. The weight of the nearest corner is $(1 - 0.2929)^2 \approx 0.5$, the two side weights are $0.2929 \times 0.7071 \approx 0.2071$ and the far weight is $0.2929^2 \approx 0.0858$. The values and bits are:

| $p$ | position | $g_p$ | bit |
|---|---|---|---|
| 0 | right | 1 | 0 |
| 1 | top right | 2.7574 | 0 |
| 2 | top | 5 | 0 |
| 3 | top left | 6.0000 | 1 |
| 4 | left | 7 | 1 |
| 5 | bottom left | 8.1213 | 1 |
| 6 | bottom | 8 | 1 |
| 7 | bottom right | 5.8787 | 0 |

Neighbor 3 is a tie. Its cell has the corners 6, 5, 7 and 6, and since $5 + 7 = 2 \times 6$ the interpolated value is exactly 6, so the bit is 1. The code is $2^3 + 2^4 + 2^5 + 2^6 = 120$, which is 01111000 in binary. It has two changes, so it is uniform. Its riu2 label is 4, the number of ones. Its u2 label in our table is 25, and its ri label is the smallest rotation 00001111, which is 15.

## Correctness

The method is a definition, so correctness means that the histogram counts the labels of the codes as defined, and that the mappings have the stated sizes and invariances. The proof in `proofs/correctness.md` shows these facts:

- Without interpolation, the code does not change under any strictly increasing change of the gray values. With interpolation, it does not change under $g \mapsto a g + b$ with $a > 0$.
- There are exactly $P(P - 1) + 2$ uniform codes, so u2 has $P(P - 1) + 3$ labels. Each uniform code with $k$ ones is a run of $k$ ones on the circle, so riu2 has $P + 2$ labels and is constant on each rotation class.
- If $4$ divides $P$, a rotation of the image by 90 degrees moves neighbor $p$ to neighbor $p + P/4$, and bilinear interpolation commutes with the rotation. So each code becomes a circular rotation of itself, and the riu2 and ri histograms do not change.

## Complexity

The model is the [word RAM](/word-ram/) with gray values in one word and $P \le w$ for the word size $w$.

- Line L1 takes $O(P)$ time. Building the table of the mapping takes $O(2^P P)$ time, since each code needs $O(P)$ time to count changes or to find the smallest rotation. The table needs $O(2^P)$ words.
- Lines L5 to L7 take $O(P)$ time per pixel, with $O(1)$ time for each bilinear value. Over at most $W H$ pixels this is $O(W H P)$.
- The histogram needs at most $2^P$ words, and $P + 2$ words for riu2.

So the time is $O(W H P + 2^P P)$ and the extra space is $O(2^P)$. For $P = 8$ the table has 256 entries, and the cost is close to 8 comparisons per pixel. Large $P$, such as 24, makes the table large, and implementations then compute $U$ and the number of ones on the fly.

## Properties

- **Gray-scale invariance.** Only signs of differences enter the code. Without interpolation, any strictly increasing change of the gray values keeps every code. With interpolation, an affine change with positive gain keeps every code; a nonlinear increasing change can move an interpolated value across the center value.
- **Rotation.** The plain code depends on the orientation of the texture. The ri and riu2 mappings remove the dependence for rotations by multiples of $360/P$ degrees about pixel centers, and only approximately for other angles, since the image grid is not rotation invariant.
- **Locality.** Each code depends on a disk of radius $R$. The histogram loses the position of the codes; a grid of regions with one histogram per region keeps a coarse position.
- **Noise.** On flat areas small noise flips many bits, because a difference near zero has a random sign. The uniform mappings move these random codes into the shared bin.
- **Not a contrast measure.** LBP keeps the pattern but drops the strength of the differences. The 1996 and 2002 papers pair it with a local variance or contrast measure for that reason.

## Variants and improvements

- **Multiresolution LBP.** Ojala, Pietikainen and Maenpaa combine histograms for several $(P, R)$, such as $(8, 1)$, $(16, 2)$ and $(24, 3)$.
- **LBP with contrast.** The joint histogram of the code and the local variance, LBP/VAR, adds the strength of the texture.
- **Spatially enhanced histograms.** Ahonen and his coauthors split a face into a grid of regions, take one u2 histogram per region and join them. A weighted chi-square distance gives more weight to regions such as the eyes. Compare the cells of [HOG](/histogram-of-oriented-gradients/) and [spatial pyramid matching](/spatial-pyramid-matching/).
- **Census transform.** The [census transform](/census-transform/) uses the same comparisons with a square window and compares the bit strings by [Hamming distance](/hamming-distance/) for stereo, without a histogram.
- **Binary descriptors.** [BRIEF](/brief-descriptor/) compares pairs of points in a patch with each other, not with the center, and keeps the bit string as the descriptor.
- **Other variants.** Local ternary patterns add a dead zone around the center value against noise, and LBP-TOP takes codes on three orthogonal planes of a video volume.

## When to use it

Use LBP for texture classification and for face description when you need a cheap descriptor that does not change with lighting. It works well on small regions with a lot of texture and on hardware with integer arithmetic only. Use riu2 when the texture can be rotated, and u2 when the orientation carries information. For matching keypoints between views, a descriptor made for keypoints, such as [SIFT](/sift/) or [ORB](/orb-features/), is a better choice, because LBP histograms need large regions to be stable.

## Pitfalls

- **The sign at zero.** The code uses $s(0) = 1$. A library that uses a strict test gives different codes on flat areas. Flat areas are common in 8-bit images.
- **Floating point ties.** An interpolated value can equal the center in exact arithmetic but differ from it by a rounding error. In the example above neighbor 3 is such a tie. Our code rounds the difference to 9 decimals before the sign test. Without this, the code of a pixel can change under a rotation of the image by 90 degrees.
- **Interpolation and monotone changes.** Interpolation breaks the invariance under nonlinear increasing changes. If you need that invariance, use integer offsets, such as $P = 4$ or $P = 8$ on the square of radius 1.
- **Bit order.** Libraries differ in the start neighbor and the direction. The ri and riu2 labels do not depend on this, but u2 labels and plain codes do. Do not compare histograms from two libraries.
- **The u2 label order.** The order of the 58 uniform labels is a convention. Our table numbers them in increasing code order.
- **Normalization.** Histograms of regions of different sizes need normalization to sum 1 before a distance.

## Implementations

## History

Ojala, Pietikainen and Harwood introduced the local binary pattern in 1996 in a comparison of texture measures. Their code thresholded a $3 \times 3$ neighborhood at the center value and used it with a contrast measure. In 2002 Ojala, Pietikainen and Maenpaa gave the circular form with $P$ neighbors at radius $R$ and bilinear interpolation, the uniformity measure $U$, and the rotation invariant uniform code riu2. Ahonen, Hadid and Pietikainen used grids of u2 histograms for face recognition in 2004 and 2006, and LBP became a standard face and texture descriptor before learned features.

## References
