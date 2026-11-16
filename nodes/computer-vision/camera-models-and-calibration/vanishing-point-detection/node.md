---
tag: 0V4VRY
kind: problem
slug: vanishing-point-detection
name: Vanishing point detection
aliases:
- vanishing point estimation
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "Find the points where the images of parallel scene lines meet, and decide which line segment belongs to which point, from the segments of one image with outliers."
prereqs: [line-detection, projective-plane, homogeneous-coordinates]
see_also: [vanishing-point-calibration, j-linkage, ransac, hough-transform, robust-model-fitting, image-of-the-absolute-conic, ransac-iteration-bound, canny-edge-detector]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 8.6, Vanishing points and vanishing lines (v = K d, the vanishing line of a plane, and the maximum likelihood estimate of a vanishing point from line segments)
  - paper: "Stephen T. Barnard, Interpreting perspective images, Artificial Intelligence 21(4), 1983, 435-462"
    title: Stephen T. Barnard, Interpreting perspective images, Artificial Intelligence 21(4), 1983, 435-462
    locator: the Gaussian sphere as the space of vanishing points and the accumulation of votes from lines on it
  - paper: doi:10.1109/ICCV.2009.5459328
    title: Jean-Philippe Tardif, Non-iterative approach for fast and accurate vanishing point detection, IEEE International Conference on Computer Vision, 2009, 1250-1257
    locator: the consistency measure of an edge and a vanishing point, and the use of J-linkage to find several vanishing points without a calibrated camera
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Feature detection and matching (the part on lines and vanishing points)
---

Vanishing point detection is the problem of finding, in one image, the points where the images of parallel scene lines meet, and of deciding which line segment belongs to which point. A set of parallel 3D lines with direction $d$ has the vanishing point $v \sim K R d$ for the camera $P = K [R \mid t]$, so each vanishing point gives a direction in the camera frame once $K$ is known. The input is a set of line segments from [line detection](/line-detection/), many of which belong to no useful direction. So the problem is a multi-model robust fitting problem: an unknown number of models, each a point of the [projective plane](/projective-plane/), with outliers. Its main use is [calibration from vanishing points](/vanishing-point-calibration/), which turns three orthogonal vanishing points into $K$ and $R$.

## In plain words

Railway tracks seem to meet at a point near the horizon. The same happens for every family of parallel lines in a scene: the edges of a road, the tops of windows, the vertical edges of a building. In a photo, each such family has its own meeting point. Some of these points lie inside the photo, some far outside, and some are infinitely far away, when the lines stay parallel in the picture too.

The task is to find these meeting points from the straight edges in a photo. It is hard because the edges are short and noisy, and many of them belong to things that do not share a direction with anything else. A detector must group the edges and place a point for each group at the same time.

## Definition

**Input.** Line segments $s_1, \ldots, s_n$ in one image, each given by two endpoints $p_i$ and $q_i$ in pixels. Usually also a threshold $\tau$ in pixels or in degrees, and sometimes the intrinsic matrix $K$.

**Output.** A set of vanishing points $v_1, \ldots, v_m$, each a nonzero vector of $\mathbb R^3$ up to scale, and an assignment of each segment to one of them or to the outliers. The number $m$ may be given (often $m = 3$) or part of the output.

**Homogeneous form.** The segment $s_i$ spans the line $l_i = \tilde p_i \times \tilde q_i$, with $\tilde p = (p, 1)$. Two lines meet at $v = l_1 \times l_2$. If the image lines are parallel, then $v$ has last entry 0, which is a point at infinity of the image. This case is common (the vertical edges of a building seen by a level camera) and needs no special code in [homogeneous coordinates](/homogeneous-coordinates/).

**Consistency of a segment and a point.** A segment does not pass exactly through its vanishing point, because the endpoints are noisy. A common measure, used by Tardif (2009), is this: draw the line $l = \tilde m_i \times v$ from the midpoint $m_i$ of the segment to $v$, and take the distance from the endpoint $p_i$ to $l$. The segment is consistent with $v$ if this distance is at most $\tau$. Other methods use the angle between the segment and the line from its midpoint to $v$. HZ Section 8.6 gives the maximum likelihood version: find $v$ and, for each segment, the line through $v$ that is closest to its endpoints.

**Objective.** The usual goal is to maximize the number of consistent segments over the set of points, with each segment counted once, or to minimize a robust sum of errors. With a known $K$ and the Manhattan assumption, the points must also satisfy $v_i^{\mathsf T} \omega v_j = 0$ for $i \ne j$, where $\omega = (K K^{\mathsf T})^{-1}$ is the [image of the absolute conic](/image-of-the-absolute-conic/).

## Variants

- **One point or several.** One vanishing point is a single model fit. Several unknown points form a multi-model problem.
- **Uncalibrated or calibrated.** With $K$ known, map each $v$ to the unit vector $K^{-1} v / \lVert K^{-1} v \rVert$ on the Gaussian sphere (Barnard 1983), and each segment to the great circle of directions that project onto it. Then a vanishing point is a point where many great circles meet, and points at infinity are not special.
- **Manhattan world.** Three mutually orthogonal directions. With $K$ known this is the estimation of one rotation (3 degrees of freedom). With $K$ unknown, the orthogonality also constrains $K$, which is how [calibration from vanishing points](/vanishing-point-calibration/) works.
- **Atlanta world.** One vertical direction and several horizontal ones. The horizontal vanishing points all lie on one line, the horizon.
- **Video.** The points move slowly from frame to frame, so a tracker can predict them.

## Examples

**Two lines.** The lines $y = 450 - 0.5 x$ and $y = 50 + 0.5 x$ have the homogeneous vectors $l_1 = (1, 2, -900)$ and $l_2 = (-1, 2, -100)$. Then
$$l_1 \times l_2 = (2 \cdot (-100) - (-900) \cdot 2, \; (-900) \cdot (-1) - 1 \cdot (-100), \; 1 \cdot 2 - 2 \cdot (-1)) = (1600, 1000, 4),$$
which is the pixel $(400, 250)$. Both equations hold there: $450 - 200 = 250$ and $50 + 200 = 250$.

**Parallel image lines.** For $l_1 = (1, 2, -900)$ and $l_3 = (1, 2, -100)$, the product is $(1600, -800, 0)$. The last entry is 0, so this is the point at infinity in the direction $(2, -1)$, which is the direction of both lines.

**Least squares for one cluster.** For segments $l_1, \ldots, l_k$ of one cluster, scaled so that the first two entries of each $l_i$ form a unit vector, the algebraic estimate is the unit vector $v$ that minimizes $\sum_i (l_i^{\mathsf T} v)^2$. It is the eigenvector of $\sum_i l_i l_i^{\mathsf T}$ with the smallest eigenvalue. For a finite $v$, $l_i^{\mathsf T} v / v_3$ is the distance of the point from the line $l_i$, so the estimate is close to the geometric one when $v$ is near the image. Far points need the angle measure or the method of HZ Section 8.6.

**Sample counts.** If half the segments belong to the dominant direction, a [RANSAC](/ransac/) sample of 2 segments has both from that direction with probability $w^2 = 0.25$. To see at least one such sample with probability 0.99, the [iteration bound](/ransac-iteration-bound/) gives $\lceil \log 0.01 / \log(1 - 0.25) \rceil = 17$ samples. At $w = 0.3$ it gives 49. These are bounds under the assumptions of that page (independent samples, a known $w$, and every clean sample gives a good point); noise makes them optimistic.

## Known algorithms

- **Hough voting on the Gaussian sphere.** Barnard (1983) maps each segment to its great circle and accumulates votes in cells of the sphere; the peaks are the vanishing points. It needs $K$ (or a guess of $f$), and the result depends on the cell size. It is the [Hough transform](/hough-transform/) for this problem.
- **Exhaustive pairs.** Take the intersection of every pair of segments as a candidate and score each candidate against all segments. This is $O(n^3)$ time in the real-RAM model for $n$ segments. Restricting the candidates to pairwise intersections is a heuristic: the best point need not be such an intersection, but it is near one when the data are good.
- **RANSAC and sequential RANSAC.** Sample 2 segments, form $v = l_1 \times l_2$, count the consistent segments, and keep the best. Remove its inliers and repeat for the next direction. Each iteration costs $O(n)$. Sequential removal is greedy, and an early wrong point can steal segments from a later one.
- **J-linkage.** Tardif (2009) generates many 2-segment hypotheses, describes each segment by the set of hypotheses it supports, and clusters the segments with [J-linkage](/j-linkage/). Each cluster gives one vanishing point by a refit. The method needs no $K$ and no number of points.
- **Expectation maximization.** Alternate a soft assignment of segments to the current points and a weighted refit of each point. It needs a good start, for example from voting.
- **Manhattan minimal solvers.** With $K$ known, 2 segments fix the first direction $d_1$, and 1 more segment fixes the second direction, because $d_2$ must be orthogonal to $d_1$ and lie on the great circle of that segment. The third is $d_1 \times d_2$. So 3 segments are a minimal sample for the Manhattan frame.
- **Learned detectors.** Networks predict vanishing points or the horizon from the image. Their accuracy is a benchmark result on data sets such as York Urban, and it depends on the data set version and the metric.

## Bounds

- Two distinct lines meet in exactly one point of the projective plane. So 2 segments determine a candidate, and $n$ segments give at most $n (n - 1) / 2$ distinct pairwise candidates.
- A point of the projective plane has 2 degrees of freedom, so each correct segment gives one equation $l_i^{\mathsf T} v = 0$ and 2 segments are the minimum for one point. With $K$ known, the Manhattan frame has 3 degrees of freedom and needs 3 segments.
- The RANSAC count above is a bound on the number of samples under its assumptions, not a worst case bound on the running time.
- No accuracy bound holds without a noise model. With independent Gaussian noise on the endpoints, the position error of a vanishing point grows with its distance from the segments, because a small change of angle moves a far intersection a long way.

## Reductions

- **To robust model fitting.** One vanishing point is a [robust model fitting](/robust-model-fitting/) problem with a 2-parameter model and a minimal sample of 2. Several points are a multi-model problem.
- **To rotation estimation.** With $K$ known, the Manhattan variant is the search for one rotation $R$ whose three columns explain the most segments.
- **From calibration.** [Calibration from vanishing points](/vanishing-point-calibration/) takes the output of this problem as input. The vanishing line of a plane, the line through two vanishing points of directions in that plane, gives the affine rectification of the plane (HZ Section 8.6).

## Applications

- Calibration from one image of a man-made scene, and a start value for the focal length in [structure from motion](/structure-from-motion-problem/).
- Estimation of the horizon and of the camera tilt for driving and for augmented reality.
- Rectification of building facades and measurements in one image.
- Layout estimation of rooms, where the walls, the floor and the ceiling follow three orthogonal directions.
- Checks on lens distortion: with distortion, segments that should share a vanishing point do not meet at one point.
