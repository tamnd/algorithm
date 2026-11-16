---
tag: X00NNP
kind: algorithm
slug: orb-features
name: ORB features
aliases:
- oriented FAST and rotated BRIEF
area: computer-vision/local-features
level: core
summary: FAST keypoints with an orientation from the intensity centroid and a BRIEF descriptor steered by that orientation, with test pairs learned for low correlation.
solves: [feature-matching]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, n: the number of keypoints, m: the number of binary tests}
  time: {worst: O(W H log(W H) + n m), average: O(W H log(W H) + n m), best: O(W H + n m)}
  space: {extra: O(W H + n m)}
properties: {deterministic: true, exact: false, rotation_invariant: true, scale_invariant: false, heuristic: true}
history:
  year: 2011
  people: [Ethan Rublee, Vincent Rabaud, Kurt Konolige, Gary Bradski]
  note: Rublee, Rabaud, Konolige and Bradski presented ORB at ICCV 2011 as a fast and free alternative to SIFT and SURF, and added it to OpenCV.
prereqs: [fast-corner-detector, brief-descriptor]
see_also: [harris-corner-detector, hamming-distance, multi-probe-lsh, feature-matching, orb-slam, brisk-features, surf, sift]
sources:
  - paper: doi:10.1109/ICCV.2011.6126544
    title: Ethan Rublee, Vincent Rabaud, Kurt Konolige and Gary Bradski, ORB, an efficient alternative to SIFT or SURF, IEEE International Conference on Computer Vision (ICCV), 2564-2571, 2011
    locator: the sections on oFAST (the Harris ranking, the pyramid, the intensity centroid), on rBRIEF (steered BRIEF, variance and correlation, the greedy learning), on matching with multi-probe LSH, and the timing table
  - paper: doi:10.1006/cviu.1998.0719
    title: Paul L. Rosin, Measuring corner properties, Computer Vision and Image Understanding 73(2), 291-307, 1999
    locator: the section on the orientation of a corner by the intensity centroid
  - paper: doi:10.1007/11744023_34
    title: Edward Rosten and Tom Drummond, Machine learning for high-speed corner detection, European Conference on Computer Vision (ECCV), Lecture Notes in Computer Science 3951, 430-443, 2006
    locator: the section on the segment test (the circle of 16 pixels and n contiguous pixels)
  - paper: doi:10.1109/TPAMI.2011.222
    title: Michael Calonder, Vincent Lepetit, Mustafa Ozuysal, Tomasz Trzcinski, Christoph Strecha and Pascal Fua, BRIEF, computing a local binary descriptor very fast, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(7), 1281-1298, 2012
    locator: the sections on the binary tests and their sampling
---

ORB (oriented FAST and rotated BRIEF) finds corners with the [FAST](/fast-corner-detector/) segment test and describes them with a [BRIEF](/brief-descriptor/) string of 256 binary tests. It adds what both lack: FAST gives no orientation, so ORB takes the direction from the corner to the centroid of the intensities in a disk around it; BRIEF is not invariant to rotation, so ORB turns the test pattern by that direction. It also learns a set of tests that have a mean near one half and a low correlation, which keeps the descriptor distinctive after the turning. Descriptors are compared by the [Hamming distance](/hamming-distance/), and the whole method runs more than ten times faster than SURF. ORB is the feature of [ORB-SLAM](/orb-slam/) and of much real-time work.

## In plain words

First find corners: points where a ring of 16 pixels around the point has 9 pixels in a row that are all much brighter, or all much darker, than the point. Keep the corners with the strongest corner score. For each corner, look at a round patch around it and find where its brightness is centered. The arrow from the corner to that center gives a direction that turns with the image. Then compare the brightness of 256 pairs of small squares in the patch, laid out in a fixed pattern that is turned to the direction of the arrow. Each comparison gives one bit. Two corners match when their 256 bits mostly agree, which a computer counts very fast.

## The problem

The input is a gray image $I$ with $W$ columns and $H$ rows; a pixel is $(u, v)$, with $u$ the column and $v$ the row, and angles grow from the $u$ axis toward the $v$ axis. The output is a set of keypoints with an orientation $\theta$, each with a binary string of $m = 256$ bits. As for every local feature, the same scene point in two views should give keypoints with near descriptors, here near in the Hamming distance, for [feature matching](/feature-matching/).

**oFAST.** FAST-9 finds the corners: on the circle of 16 pixels at radius 3, at least 9 contiguous pixels are brighter than $I(p) + t$, or at least 9 are darker than $I(p) - t$. FAST answers strongly along edges, so ORB ranks the corners by the [Harris](/harris-corner-detector/) measure and keeps the best $N$. For scale, it runs on each level of a pyramid with the factor $\sqrt{2}$; the paper uses 5 levels.

**Intensity centroid.** Rosin defines the moments of a patch as $m_{pq} = \sum_{x, y} x^p y^q I(x, y)$, with $(x, y)$ relative to the corner. The centroid is $(m_{10} / m_{00}, m_{01} / m_{00})$, and the orientation is

$$\theta = \operatorname{atan2}(m_{01}, m_{10}).$$

ORB sums over a disk of radius $r$, not a square, so that the region does not change when it is turned.

**Steered BRIEF.** A test compares two points $p_i$ and $q_i$ of the patch, $\tau_i = [S(k + p_i) < S(k + q_i)]$, where $S$ is the sum of a $5 \times 5$ window, so that one pixel of noise has less effect. The patch is $31 \times 31$ pixels. For the orientation $\theta$ the test points are turned by $R_\theta$. ORB rounds $\theta$ to a multiple of $2\pi / 30$, 12 degrees, and keeps a table of the turned patterns, so that no rotation is computed at run time.

## The algorithm

```pseudo id=main
ORB(I, N, t)                            ▷ pattern tables T_0, ..., T_29 built once
L1  C ← FAST-9 corners of I with threshold t (on each pyramid level)
L2  keep the corners that are local maxima of the Harris measure, then the N with the largest measure
L3  for each keypoint k: m_10, m_01 ← Σ x I, Σ y I over the disk of radius 15; θ ← atan2(m_01, m_10)
L4      b ← round(θ / (2π/30)) mod 30
L5      for each test i with the turned points (p_i, q_i) in T_b do
L6          bit i of the descriptor ← [S(k + p_i) < S(k + q_i)]
L7  return the keypoints with θ and their descriptors
```

**Learning the tests (rBRIEF).** Turning makes the tests less useful: for BRIEF on upright patches each test has a mean near $\frac12$, but once the patches are turned to their orientation, many tests have means far from $\frac12$ and are correlated. ORB therefore picks its tests by a greedy search. The paper enumerates the tests between $5 \times 5$ windows of the $31 \times 31$ patch, removes the tests whose windows overlap, and keeps $M = 205590$ candidates. It runs them on about 300000 keypoints from the PASCAL 2006 images.

1. Run each test on all training patches, turned to their orientation, and order the tests by the distance of their mean from $\frac12$.
2. Put the first test in the result.
3. Take the next test, and add it to the result if the absolute correlation with every test in the result is below a threshold. Repeat until there are 256 tests.
4. If the candidates run out first, raise the threshold and start again.

The code has the same search in `learn_tests`. Its default pattern is random, because the learned pattern needs the training set; OpenCV ships the learned pattern as a fixed table.

## Example

**Orientation.** Take the disk of radius 1, five pixels around a corner $k$: $I(k) = 10$, the right neighbor 20, the left neighbor 0, the neighbor above 10 and the neighbor below 30. Then $m_{10} = 1 \cdot 20 + (-1) \cdot 0 = 20$ and $m_{01} = 1 \cdot 30 + (-1) \cdot 10 = 20$, so $\theta = \operatorname{atan2}(20, 20) = 45°$, toward the lower right where the patch is bright. With bins of 12 degrees, $45 / 12 = 3.75$ rounds to bin 4, which is 48 degrees.

**A turned test.** The test point $(5, 0)$ turned by 48 degrees is $(5 \cos 48°, 5 \sin 48°) = (3.35, 3.72)$, which rounds to $(3, 4)$. So in bin 4 the test reads the $5 \times 5$ window centered 3 pixels to the right of and 4 pixels below the corner.

**Rotation by 90 degrees.** With 32 bins instead of 30, a quarter turn is exactly 8 bins. The code builds the bins 8 to 31 as exact quarter turns of the bins 0 to 7. If an image is turned by 90 degrees, the centroid turns with it, so $\theta$ grows by $\pi / 2$, and the descriptors of a keypoint and its turned copy are equal bit for bit. The tests check this on a $64 \times 64$ image: all keypoints are found again, all at Hamming distance 0, while the same tests without steering differ in more than 40 of the 256 bits on average.

## Correctness

ORB is a heuristic; its matching quality is a benchmark result. The proof in `proofs/correctness.md` shows that:

- The segment test of the code is the FAST-9 test: it finds a run of 9 in the circle of 16 pixels, including runs that wrap around.
- The centroid angle turns with the image: for a turn by $90°$ about a pixel, $\theta$ grows by exactly $\pi/2$. Adding a constant to the image does not change $\theta$, since $\sum x = \sum y = 0$ over a disk.
- When the number of bins is a multiple of 4 and the turned image keeps the bins, the descriptor of the turned image is the same.
- The greedy search ends, and every two chosen tests have an absolute correlation below the final threshold on the training set.

## Complexity

The model is the [word RAM](/word-ram/): pixel values, sums and descriptors of 64-bit words.

- Line L1 tests each pixel in $O(1)$ time, $O(W H)$ in total.
- Line L2 computes the Harris measure in $O(1)$ time per corner and sorts the corners, $O(W H \log(W H))$ in the worst case; a selection of the best $N$ is $O(W H)$.
- Line L3 takes $O(r^2)$ time per keypoint, a constant for $r = 15$.
- Lines L5 and L6 take $O(1)$ time per test with an integral image, so $O(n m)$ for all keypoints.

The total time is $O(W H \log(W H) + n m)$, and the space is $O(W H)$ for the image and the integral image and $O(n m)$ bits for the descriptors. A Hamming distance costs $m / 64$ XOR and popcount operations. Rublee and his coauthors report 15.3 ms per image of $640 \times 480$ pixels for ORB, against 217.3 ms for SURF and 5228.7 ms for SIFT, on one test computer.

## Properties

- **Rotation invariant.** The pattern follows $\theta$, up to the rounding of $\theta$ to 12 degrees and of the points to pixels.
- **Partly scale invariant.** The pyramid gives keypoints at several scales, but the patch has the same size in pixels at each level, and there is no scale selection as in SIFT.
- **Contrast invariant.** The tests compare two sums of equal size, so they do not change when a constant is added or the image is multiplied by a positive number. The centroid angle does not change either.
- **Binary.** 256 bits are 32 bytes, against 64 floats for SURF and 128 for SIFT, and the Hamming distance is a few machine instructions.
- **Free.** ORB is not patented, which was one reason for its design.

## Variants and improvements

- **Matching.** The paper matches with [multi-probe LSH](/multi-probe-lsh/), which suits binary strings; brute force with the Hamming distance is often fast enough.
- **OpenCV ORB.** It smooths the image with a Gaussian and compares single pixels instead of window sums, scores the corners by Harris or by the FAST score, and spreads the keypoints over the levels of the pyramid.
- **ORB-SLAM.** It spreads the keypoints over a grid of cells so that they cover the whole image, which matters for tracking.
- **BRISK and FREAK.** [BRISK](/brisk-features/) uses a fixed pattern of points on rings and takes the orientation from long pairs; FREAK uses a retina-like pattern.

## When to use it

Use ORB when speed or the absence of patents matters: on phones and robots, in visual SLAM and [visual odometry](/visual-odometry/), and in [image stitching](/image-stitching/) of many frames. For large changes of scale or strong blur, float descriptors such as [SIFT](/sift/) match better; learned features such as [SuperPoint](/superpoint/) are better still when a GPU is available.

## Pitfalls

- **Clustered corners.** FAST fires many times on one corner. Without non-maximum suppression the best $N$ corners lie in a few places.
- **The border.** The patch, turned and with its $5 \times 5$ windows, needs a margin of about 16 pixels; points nearer to the border have no descriptor.
- **Bins of 12 degrees.** Two views whose angles fall on both sides of a bin border get patterns turned 12 degrees apart, which flips some bits. This is a source of error, not a bug.
- **A flat patch.** When $m_{10}$ and $m_{01}$ are both near 0, $\theta$ is unstable, and so is the descriptor.
- **Tests and patterns.** A learned pattern must be the same at training and at matching time, and different libraries use different patterns.
- **Distance thresholds.** Thresholds on the Hamming distance depend on $m$; use the [Lowe ratio test](/lowe-ratio-test/) or [mutual nearest neighbors](/mutual-nearest-neighbor-matching/) instead of a fixed distance when possible.

## Implementations

## History

Calonder and his coauthors gave BRIEF in 2010. It was fast but not rotation invariant. Rublee, Rabaud, Konolige and Bradski, at Willow Garage, presented ORB at ICCV 2011, at the same conference as BRISK. They joined FAST of Rosten and Drummond (2006), the Harris measure (1988) and the intensity centroid of Rosin (1999) with a learned, steered BRIEF, and added ORB to OpenCV. Mur-Artal, Montiel and Tardos built ORB-SLAM on it in 2015, and ORB became a standard feature of visual SLAM.

## References
