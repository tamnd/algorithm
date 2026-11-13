---
tag: VP4ADQ
kind: problem
slug: line-detection
name: Line detection
aliases:
- straight line detection
area: graphics-and-signals/image-processing
level: advanced
summary: Find the straight lines or line segments of an image that many edge pixels support, with their angle and position, in spite of gaps, noise and other structures.
model: word-ram
complexity:
  vars: {N: number of edge points}
  time: {worst: Ω(N)}
prereqs: [edge-detection]
see_also: [hough-transform, collinear-points, line-representation, point-to-line-distance, linear-regression, ramer-douglas-peucker, 3sum-hardness, random-sampling]
sources:
  - paper: doi:10.1145/361237.361242
    title: Richard O. Duda and Peter E. Hart, Use of the Hough transformation to detect lines and curves in pictures, Communications of the ACM 15(1), 11 to 15, 1972
    locator: the statement of the problem of detecting collinear subsets of figure points, and the normal parameterization of lines
  - paper: doi:10.1145/358669.358692
    title: Martin A. Fischler and Robert C. Bolles, Random sample consensus, a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 381 to 395, 1981
    locator: the RANSAC procedure, and the number of random samples needed for a given probability of success
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsections Line Detection and Linking Edge Points (global processing using the Hough transform)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.4, Lines and vanishing points
---

Line detection is the problem of finding the straight lines in an image. The input is usually an edge map, a set of edge points from [edge detection](/edge-detection/), and the output is a list of lines or line segments, each with the edge points that support it. Real images make this hard: a line has gaps, its points are a little off the ideal line because of the pixel grid and noise, and most edge points belong to other structures. So the problem asks for the lines with enough support, not for an exact fit of all points. The classic method is the [Hough transform](/hough-transform/), which votes in a grid over the angle and the distance of lines.

## In plain words

You have a picture with many small dots, where the edges were found. Some rows of dots are on straight lines, such as the edge of a table, a road marking or a line of text. Other dots are noise or belong to curved shapes. Line detection must say where the straight lines are. A line counts if many dots are close to it. The dots of one line do not have to touch: a line can be broken by shadows or by objects in front of it, and it should still be found as one line. Often you also want the two ends of each piece of line.

## Definition

The input is a set $P$ of $N$ edge points of a $W \times H$ image. A point $(x, y)$ is the center of a pixel, with integer coordinates, $x$ to the right and $y$ downward. Each point can also carry the direction of the image gradient at that point. A line is written in the normal form $x \cos\theta + y \sin\theta = \rho$, with $0 \le \theta < \pi$ and $\rho$ the signed distance from the origin, see [line representation](/line-representation/). The support of a line $\ell$ at the tolerance $\delta$ is the set of points of $P$ whose [distance to the line](/point-to-line-distance/) is at most $\delta$:

$$S_\delta(\ell) = \{\, p \in P : |x \cos\theta + y \sin\theta - \rho| \le \delta \,\}.$$

The problem is to output the lines whose support has at least $\tau$ points, with each group of near lines reported once. Typical values are $\delta$ from $\tfrac{1}{2}$ to 2 pixels. Since every point is near many lines, "near lines are reported once" needs a rule, for example a minimum difference in angle and in distance between reported lines, or the removal of the support of a line before the next one is searched.

This page is about straight lines in an edge map. The detection of thin bright or dark lines by a mask that responds to lines, such as a $3 \times 3$ line mask, is a filtering step that gives such a map. Grouping edge points into curves of other shapes is a related problem, see [active contours](/active-contours/) and the variants of the [Hough transform](/hough-transform/).

## Variants

- **Lines or segments.** The output can be infinite lines, or segments with two endpoints. Segments need a rule for gaps: two collinear pieces are one segment if the gap is shorter than a limit.
- **One line or many.** Fitting one line to points that are mostly on it is a regression problem. Finding all the lines in a cluttered edge map is a search problem.
- **With gradient directions.** If each point has a gradient direction, a point can only support lines nearly at 90 degrees to that direction. This removes most wrong support and makes the search cheaper.
- **The exact form.** With $\delta = 0$ and real coordinates, the problem is to find the lines that hold at least $\tau$ points of the set, the problem of [collinear points](/collinear-points/).
- **Subpixel lines.** The output gives $\theta$ and $\rho$ more exactly than one grid cell, by a fit to the support.
- **Vanishing points.** In a photograph of a scene, parallel 3D lines meet at a vanishing point. Grouping the detected lines by their vanishing points is a common next step.

## Examples

- A vertical line $x = 12$ in a $40 \times 40$ image, with all 40 of its pixels as edge points, has the parameters $\theta = 0$ and $\rho = 12$. With 40 random noise points added, it is still the line with the largest support.
- The anti-diagonal $x + y = 30$ has $\theta = 45°$ and $\rho = 30/\sqrt{2} \approx 21.2$. Its 31 pixels are exactly on the line.
- A line at 60 degrees whose points are rounded to the pixel grid has points up to $\tfrac{1}{2}\sqrt{2}$ pixels off the line, so the tolerance $\delta$ must be at least about $0.71$ to keep its full support.
- A dashed line, with gaps between the dashes, is one line with a support that is not connected.
- A circle has no line with a large support, but a polygon with 20 sides has 20 short ones. The threshold $\tau$ decides which of them count.

## Known algorithms

| Algorithm | Output | Cost | Notes |
|---|---|---|---|
| [Hough transform](/hough-transform/) | lines | $\Theta(N T + T D)$ worst case | $T$ angle bins, $D$ the image diagonal, many lines at once |
| Probabilistic Hough transform | lines or segments | votes for a sample of the points | stops when a peak is clear |
| RANSAC (random sample consensus) | one line at a time | $O(k N)$ for $k$ samples | robust when most points are outliers |
| Least squares fit | one line | $\Theta(N)$ | fast, but one outlier can move the line far |
| Edge linking and splitting | segments | $O(N \log N)$ expected for the splitting | follow edge chains, split with [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) |
| Segment detectors from gradients | segments | linear in the pixels, observed | group pixels with similar gradient direction into rectangles |
| Exact collinear sets | lines | $O(N^2 \log N)$ worst case | [collinear points](/collinear-points/), for exact coordinates |

**RANSAC.** Martin Fischler and Robert Bolles gave this method in 1981. Pick 2 points at random by [random sampling](/random-sampling/), take the line through them, and count its support. Repeat $k$ times and keep the line with the largest support, then fit it again by least squares to that support. Each repeat costs $O(N)$. If a fraction $w$ of the points are on the line, a sample of 2 points is all on the line with probability about $w^2$, so $k \ge \ln \eta / \ln(1 - w^2)$ samples find such a sample with probability at least $1 - \eta$. For $w = 0.2$ and $\eta = 0.01$, this is about 113 samples. For many lines, run it again on the points that are left.

**Least squares.** When the support is known, the best line in the sense of the sum of the squared perpendicular distances goes through the centroid, along the main axis of the 2 by 2 covariance matrix of the points. This is the total least squares fit. The fit of $y$ as a function of $x$, as in [linear regression](/linear-regression/), fails for vertical lines.

**Segment detectors from gradients.** These group adjacent pixels with nearly the same gradient direction into regions, approximate each region by a rectangle, and keep the rectangles that a statistical test finds unlikely in noise. The LSD detector of von Gioi, Jakubowicz, Morel and Randall from 2010 is a known example. They need no edge map and no threshold on the number of votes.

## Bounds

- **Reading the input.** Every point can change the answer, so every algorithm needs $\Omega(N)$ time in the worst case. A least squares fit of one line meets this bound.
- **Exact lines are 3SUM-hard.** With $\delta = 0$ and $\tau = 3$, the question whether some line holds 3 points of the set is the problem of 3 collinear points. Gajentaan and Overmars showed in 1995 that it is [3SUM-hard](/3sum-hardness/), so no algorithm in $O(N^{2 - \varepsilon})$ time is expected for it. The exact problem can be solved in $O(N^2)$ time with the dual line arrangement.
- **The cost of a grid.** The Hough transform avoids this bound by a grid of $T$ angles, with $T$ about the length of the longest line, so its cost $\Theta(N T)$ grows with the resolution, and its answer is exact only to one cell.
- **Random sampling.** RANSAC finds a line with $w N$ points in expected $O(N / w^2)$ time, since the expected number of samples until both points are on the line is about $1/w^2$.

## Reductions

- **From edge detection.** The edge points come from an edge detector such as the [Canny edge detector](/canny-edge-detector/). Thin edges are important: an edge 3 pixels wide gives 3 parallel lines.
- **To voting.** The Hough transform reduces line detection to the search for peaks in an array of counts, a form of [non-maximum suppression](/non-maximum-suppression/) in 2D.
- **To point-line duality.** The map from a point to the set of lines through it turns collinear points into lines that meet in one point. So the exact problem becomes a search for a vertex of a [line arrangement](/line-arrangement/) with many lines through it.
- **To regression.** Once the support is known, the problem is a [least squares problem](/least-squares-problem/) with 2 unknowns.
- **From segmentation.** The boundaries of regions in a [segmentation](/image-segmentation/) can be split into segments by [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) and then merged.

## Applications

- The detection of lane markings on roads for driver assistance.
- The correction of the skew of scanned documents, and the detection of table lines and of text lines.
- The calibration of cameras from the lines of a pattern, and the estimation of vanishing points.
- The reconstruction of buildings and rooms from photographs, where most edges are straight.
- The inspection of manufactured parts, and the analysis of particle tracks, the first use of the Hough transform.

## References
