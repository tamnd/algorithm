---
tag: 99A606
kind: algorithm
slug: fast-corner-detector
name: FAST corner detector
aliases:
- features from accelerated segment test
area: computer-vision/local-features
level: core
summary: Call a pixel a corner when n contiguous pixels of the 16 on a circle around it are all brighter or all darker by a threshold, tested in an order learned by a decision tree.
solves: [corner-detection]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, n: the length of the arc}
  time: {worst: O(W H n), average: O(W H), best: O(W H)}
  space: {extra: O(W H)}
properties: {deterministic: true, exact: true, rotation_invariant_response: false, scale_invariant: false, heuristic: true}
history:
  year: 2006
  people: [Edward Rosten, Tom Drummond]
  note: Rosten and Drummond presented the learned detector at ECCV 2006; the 2010 journal version with Reid Porter added the FAST-ER variant.
prereqs: [corner-detection, digital-image]
see_also: [moravec-corner-detector, shi-tomasi-corner-detector, harris-corner-detector, orb-features, brisk-features, decision-tree, id3, non-maximum-suppression]
sources:
  - paper: doi:10.1007/11744023_34
    title: Edward Rosten and Tom Drummond, Machine learning for high-speed corner detection, European Conference on Computer Vision (ECCV), LNCS 3951, 2006, pages 430-443
    locator: the whole paper (the segment test, the learned decision tree and the non-maximal suppression)
  - paper: doi:10.1109/TPAMI.2008.275
    title: Edward Rosten, Reid Porter and Tom Drummond, Faster and better, a machine learning approach to corner detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(1), 105-119, 2010 (arXiv 0810.2434)
    locator: Section III-A (the segment test and the high-speed test), equation 8 (the three states), Section III-B (the ID3 tree and the 3^16 configurations), Section III-C (the score and the 3 x 3 suppression)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Section 7.1.1, Feature detectors
---

The FAST corner detector (features from accelerated segment test) solves [corner detection](/corner-detection/) with comparisons only. It looks at the 16 pixels on a circle of radius 3 around a pixel $p$ and calls $p$ a corner when $n$ contiguous pixels of the circle are all brighter than $I_p + t$ or all darker than $I_p - t$. This is the segment test. Unlike the [Harris](/harris-corner-detector/) and [Shi-Tomasi](/shi-tomasi-corner-detector/) detectors it computes no gradients and no sums, and most pixels are rejected after two comparisons. Edward Rosten and Tom Drummond made the test fast by learning, with a [decision tree](/decision-tree/), the order in which to read the circle pixels. The cost is $O(WH)$ for a $W \times H$ image. The score that ranks the corners for [non-maximum suppression](/non-maximum-suppression/) is the largest threshold for which the pixel is still a corner. FAST is the detector inside [ORB](/orb-features/).

## In plain words

Draw a small circle of 16 pixels around a pixel. If a long unbroken part of the circle, say 9 pixels in a row, is clearly brighter than the center, or clearly darker, then the center is a corner. On a flat area the circle looks like the center. On a straight edge about half of the circle is brighter and half is the same, and half of 16 is not enough. Only near a corner or a small spot does a long arc differ from the center. The test needs no arithmetic beyond comparisons, and most pixels fail it after a look at two circle pixels. To keep one point per corner, give each corner a score, the largest threshold at which it still passes, and drop corners with a stronger neighbour.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows of integer values, an integer threshold $t \ge 1$ and an arc length $n$ with $1 \le n \le 16$. A pixel has integer coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down. The circle is the discrete circle of radius 3 with 16 pixels, numbered 1 to 16 clockwise from the top:

$$(0, -3), (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3), (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3).$$

Pixels 1, 5, 9 and 13 are the top, right, bottom and left. Only the pixels with $3 \le u \le W - 4$ and $3 \le v \le H - 4$ are tested, so the circle is inside the image. A circle pixel $x$ is brighter when $I(x) \ge I_p + t$ and darker when $I(x) \le I_p - t$; this follows equation 8 of the 2010 paper. Some implementations use strict inequalities, which for integer images is the same test with $t + 1$. The pixel $p$ is a corner when there is a run of $n$ contiguous circle pixels, with the run allowed to wrap from pixel 16 to pixel 1, that are all brighter or all darker.

The score $V(p)$ is the largest $t$ for which $p$ is still a corner. For integer images it has a closed form. For an arc $A$ of $n$ contiguous circle pixels, all pixels of $A$ are brighter for threshold $t$ exactly when $t \le \min_{x \in A} (I(x) - I_p)$, and all are darker exactly when $t \le \min_{x \in A} (I_p - I(x))$. So

$$V(p) = \max_{A} \max\Big(\min_{x \in A} \big(I(x) - I_p\big), \; \min_{x \in A} \big(I_p - I(x)\big)\Big),$$

and $p$ is a corner for the threshold $t$ exactly when $V(p) \ge t$. The output is the set of corners whose score is not smaller than the score of any corner among their eight neighbours.

## The algorithm

```pseudo id=main
FAST(I, t, n)                         ▷ I is W × H with integer values, t ≥ 1
L1  for each pixel p with 3 ≤ u ≤ W - 4 and 3 ≤ v ≤ H - 4 do
L2      if n = 12 and fewer than 3 of the pixels 1, 5, 9, 13 are brighter and fewer than 3 are darker then skip p
L3      V(p) ← the largest, over the 16 arcs A of n contiguous circle pixels, of max(min over A of I(x) - I_p, min over A of I_p - I(x))
L4      if V(p) ≥ t then add p to the candidates C
L5  corners ← ∅
L6  for each p in C do
L7      if V(p) ≥ V(q) for each q in C with q one of the 8 neighbours of p then
L8          add p to corners
L9  return corners
```

Line L2 is the high-speed test of the original detector. It is valid only for $n = 12$: a run of 12 contiguous pixels leaves out a run of 4, and any 4 contiguous pixels hold exactly one of the pixels 1, 5, 9 and 13, so a corner has at least 3 of the four brighter or at least 3 darker. For $n = 9$ a run can hold only two of them, and the test would reject real corners. Line L3 computes the score, and line L4 is the segment test, since $V(p) \ge t$ is the same as a run of $n$ brighter or darker pixels. Lines L5 to L8 are a $3 \times 3$ [non-maximum suppression](/non-maximum-suppression/) on the scores, as in Section III-C of the 2010 paper. The test at line L7 is not strict, so a group of neighbours with the same score is kept whole.

A real FAST detector does not run line L3 on every pixel. It first runs the segment test as a learned [decision tree](/decision-tree/) that reads one circle pixel at a time and stops as soon as the answer is known, and it computes the score only for the few pixels that pass. The tree changes the speed, not the output.

### The learned tree

Each circle pixel $x$ of $p$ is in one of three states: darker, similar or brighter. Rosten and Drummond collect the 16 states of every pixel in a set of training images, label each pixel by the segment test, and grow a tree with the [ID3](/id3/) rule: at each node, read the circle pixel whose state gives the most information about the label. They add all $3^{16} = 43046721$ state patterns with a low weight, so the tree computes the segment test exactly and not only on the training images. The tree is then written out as nested if-else code. The order of the questions is tuned to the images, which is the source of the speed. The paper also forces the second question to be the same on every branch, so the first two tests can run on a strip of pixels with vector instructions; most pixels are rejected after these two tests.

## Example

Take an $11 \times 11$ image with $0$ everywhere except a block of $9$s at $u \ge 5$ and $v \ge 5$, with $t = 1$ and $n = 9$. At the corner pixel $p = (5, 5)$ the 16 circle values, from pixel 1 to pixel 16, are

$$0, 0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0 .$$

The 11 zeros from pixel 10 around to pixel 4 are one run, all darker than $9 - t$. An arc of 9 of them gives $\min(I_p - I(x)) = 9$, so $V(5, 5) = 9$. A pixel just outside the block, such as $(4, 4)$, sees only 3 bright pixels on its circle and fails.

The corners are the six pixels $(5, 5)$, $(6, 5)$, $(7, 5)$, $(5, 6)$, $(6, 6)$ and $(5, 7)$, all with score 9. Since the scores are equal, the suppression keeps all six; a strict test would drop all six. For $n = 12$ there are no corners at all: a right angle leaves only 11 darker pixels on the circle. This is one reason why FAST-9 replaced FAST-12. For $t = 10$ there are no corners either, since no score is above 9.

## Correctness

The output is the set defined in The problem. The proof in [proofs/correctness.md](proofs/correctness.md) shows three facts:

- the closed form of $V(p)$ is the largest threshold for which $p$ passes the segment test, and the test passes for $t$ exactly when $V(p) \ge t$;
- the high-speed test of line L2 never rejects a corner when $n = 12$, so it changes the speed and not the output;
- lines L5 to L9 return exactly the candidates that are not smaller than any candidate neighbour.

For $n = 9$ the second fact fails: the circle with pixels 2 to 10 darker and the rest equal to the center is a corner, but only two of the pixels 1, 5, 9 and 13 are darker. That a FAST corner is a good corner for a given task is not a theorem; the 2010 paper measures it as repeatability on image sequences.

## Complexity

The model is the [word RAM](/word-ram/) with integer pixels.

- Line L2 reads 4 pixels, and line L3 reads 16 pixels and takes the minimum over 16 arcs of $n$ pixels, which is $O(n)$ time per pixel with the direct loop, or $O(1)$ with a sliding minimum over the circle. Over $WH$ pixels this is $O(WHn)$, which is $O(WH)$ since $n \le 16$.
- Lines L6 and L7 cost $O(1)$ per candidate.
- A hash set or a $W \times H$ table of scores takes $O(WH)$ extra space.

The decision tree reads at most 16 pixels per pixel and, for most pixels of typical images, two. The output does not depend on the tree, only the time does.

## Properties

- **Comparisons only.** The segment test uses comparisons with $I_p \pm t$, so it suits 8-bit images and simple hardware.
- **Offset invariant.** Adding a constant to the image changes nothing. A gain changes which pixels pass for a fixed $t$, since $t$ is absolute.
- **Rotation.** The circle maps to itself under a rotation by $90°$ (a cyclic shift by 4 positions) and under a mirror, so the detector commutes with these. For other angles the discrete circle is only close to rotation invariant.
- **Not scale invariant.** The circle has a fixed radius of 3 pixels. ORB and BRISK run FAST on each level of an image pyramid.
- **Clusters.** The test is true for several adjacent pixels at one corner, as the example shows. The suppression thins them only when the scores differ.
- **Spots and lines.** A single bright pixel passes for any $n$, and a thin line passes for small $n$. The segment test answers "a long arc differs from the center", which includes more than corners.

## Variants and improvements

- **FAST-12 and FAST-9.** The original test used $n = 12$ because of the high-speed test. The 2010 paper reports that $n = 9$ gives the best repeatability.
- **FAST-ER.** The 2010 paper also learns the shape of the test itself, with a larger set of pixels around $p$, by simulated annealing that maximizes repeatability. The result is slower than FAST-9 and more repeatable.
- **AGAST.** Mair and others build the tree adaptively, so it does not need training on images of the target domain.
- **Scores.** Other scores are the sum of the absolute differences over the arc, or a Harris response computed at each FAST corner; ORB uses the Harris response to rank the corners.
- **Pyramids.** Detect on each level of an image pyramid to cover scales, as in [ORB](/orb-features/) and [BRISK](/brisk-features/).

## When to use it

Use it when time is short: real-time tracking, visual odometry, SLAM on embedded processors, or a first stage that proposes candidates for a slower descriptor. Pair it with a pyramid for scale and with a Harris or Shi-Tomasi score if the corner quality matters. For precise localization or for matching under large changes of scale or viewpoint, use a detector with scale selection such as the [DoG detector](/difference-of-gaussians-detector/).

## Pitfalls

- **High-speed test with $n \ne 12$.** The test with pixels 1, 5, 9 and 13 is only valid for $n = 12$. For $n = 9$ it rejects true corners, as the example in Correctness shows.
- **Threshold zero.** With $t = 0$ and the non-strict inequalities, a circle pixel equal to the center is both brighter and darker, and every pixel is a corner. Use $t \ge 1$.
- **Wrap around.** A run can cross from pixel 16 to pixel 1. Code that scans the circle once from pixel 1 misses those runs.
- **Border.** The circle needs 3 pixels on each side. Pixels within 3 of the border cannot be tested.
- **Plateaus in the suppression.** Equal scores on neighbours, as in the example, are kept by a test with $\ge$ and all dropped by a test with $>$. Neither is right in general; break ties by position if one point per corner is needed.

## Implementations

## History

Rosten and Drummond first used the segment test with $n = 12$ and the high-speed test in a system for real-time tracking. At ECCV 2006 they presented the learned version: a decision tree, grown by ID3 from the states of the circle pixels, that computes the segment test with few comparisons. In the 2010 journal version, with Reid Porter, they extended the evaluation, chose $n = 9$, defined the score as the largest threshold and introduced FAST-ER. FAST became the standard fast detector, and ORB (2011) made it a part of a complete feature pipeline.

## References
