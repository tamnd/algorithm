---
tag: RM5DZP
kind: algorithm
slug: nister-visual-odometry
name: Nister visual odometry
aliases:
- feature-based visual odometry
area: computer-vision/structure-from-motion
level: advanced
summary: "Match corners between frames, find each new camera pose with a five-point or three-point solver inside preemptive RANSAC, and triangulate, for a single camera or a stereo rig."
solves: [visual-odometry]
model: real-ram
complexity:
  vars: {N: the number of frames, n: the number of tracks seen in a frame, M: the number of hypotheses per frame, B: the block size of the preemptive scoring, k: the number of Gauss-Newton iterations, f: the firewall spacing in frames}
  time: {worst: O(N (M B + M log M + k n + f n)), average: O(N (M B + M log M + k n + f n)), best: O(N (M B + M log M + n))}
  space: {extra: O(M + f n)}
properties: {deterministic: false, exact: false, online: true, iterative: true}
history:
  year: 2004
  people: [David Nistér, Oleg Naroditsky, James Bergen]
  note: "Nistér, Naroditsky and Bergen gave the name visual odometry to real-time camera motion estimation from matched corners, with the five-point and three-point solvers inside preemptive RANSAC."
prereqs: [visual-odometry, five-point-algorithm, preemptive-ransac, p3p]
see_also: [linear-triangulation, essential-matrix-decomposition, scale-drift, keyframe-selection, sliding-window-bundle-adjustment, harris-corner-detector, semi-direct-visual-odometry, orb-slam]
sources:
  - paper: doi:10.1109/CVPR.2004.1315094
    title: "David Nistér, Oleg Naroditsky and James Bergen, Visual odometry, Proceedings of the IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR 2004), volume 1, 652-659"
    locator: "the whole paper (corner detection and matching, the monocular scheme with the five-point solver and the three-point resection in preemptive RANSAC, the firewall, and the stereo scheme)"
  - paper: doi:10.1002/rob.20103
    title: "David Nistér, Oleg Naroditsky and James Bergen, Visual odometry for ground vehicle applications, Journal of Field Robotics 23(1), 2006, 3-20"
    locator: "the journal version of the same system, with the runs on ground vehicles"
  - paper: doi:10.1109/MRA.2011.943233
    title: "Davide Scaramuzza and Friedrich Fraundorfer, Visual odometry, Part I: the first 30 years and fundamentals, IEEE Robotics and Automation Magazine 18(4), 2011, 80-92"
    locator: "the history of the term, the comparison of 3D-to-3D and 3D-to-2D motion estimation, and the relative scale of monocular visual odometry"
  - paper: "David Nistér, Preemptive RANSAC for live structure and motion estimation, Proceedings of the Ninth IEEE International Conference on Computer Vision (ICCV 2003), 199-206"
    locator: "the preemptive scoring of hypotheses that the system uses"
  - paper: doi:10.1109/TPAMI.2004.17
    title: "David Nistér, An efficient solution to the five-point relative pose problem, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(6), 2004"
    locator: "the five-point solver that gives the motion hypotheses of the monocular scheme"
---

Nister visual odometry is the system of Nistér, Naroditsky and Bergen (CVPR 2004) that estimates the motion of a calibrated camera, frame by frame, from corner matches. It gave the name to the [visual odometry](/visual-odometry/) problem. Each new pose comes from a minimal solver inside [preemptive RANSAC](/preemptive-ransac/): the [five-point algorithm](/five-point-algorithm/) for the relative pose of a single camera at the start, and the three-point resection ([P3P](/p3p/)) against already triangulated points after that. A short Gauss-Newton refinement follows. New points are triangulated between the two most distant views that are allowed, and a "firewall" every few frames stops old frames from taking part in new triangulations, so an error does not pass forward for ever. With one camera the result has an unknown scale; with a calibrated stereo rig the same scheme gives metric motion.

## In plain words

You walk with a camera and want to know your path. In each picture, find many small corners, and match them with the corners of the next picture. From a few matches you can guess how the camera moved. Some matches are wrong, so you make many guesses from random small sets of matches and keep the guess that most matches agree with. To save time, you test all guesses on a few matches first, drop the worse half, test the rest on more matches, and so on. From the matches and the motion you also find where the corners are in space. Later pictures then need only three known points per guess. With one camera you never learn the real size of the steps, only their ratios. With two cameras side by side you do.

## The problem

The input is a sequence of $N$ frames of a calibrated camera and, for each frame $k$, a set of tracks: a track id and a point $x = (x, y)$ in normalized image coordinates $K^{-1}(u, v, 1)^{\mathsf T}$. Some points are wrong matches (outliers). A pose $(R_k, t_k)$ maps a world point into camera $k$ as $X_c = R_k X + t_k$, and the world frame is the camera of frame 0. The output is one pose per frame. For one camera the poses are found up to one global scale, which the algorithm fixes by setting $|t_2| = 1$. For a rectified stereo pair with known baseline $b$, the poses are metric.

The corner detection and matching are part of the system but not of the code here. In the paper, Harris corners are found in every frame and matched between frames by normalized correlation of small patches; they are matched again in each frame and not tracked by a flow method, which keeps the feature positions from drifting. The code takes the tracks as input.

## The algorithm

```pseudo id=main
NISTER-VO-MONO(tracks of frames 0 … N-1, firewall spacing f, threshold τ)
L1  pose[0] ← (I, 0)
L2  E ← preemptive RANSAC over five-point hypotheses on the tracks seen in frames 0 and 2
L3  (R, t) ← the decomposition of E that puts most inliers in front of both cameras;  pose[2] ← (R, t / |t|)
L4  map ← linear triangulation of the inliers from frames 0 and 2;  firewall ← 0
L5  for k in 1, 3, 4, …, N - 1 do
L6      (R, t) ← preemptive RANSAC over P3P hypotheses on the map points seen in frame k
L7      pose[k] ← Gauss-Newton refinement of (R, t) on the reprojection error of the inliers
L8      for each track seen in frame k do
L9          i ← the first frame ≥ firewall that sees the track
L10         if k - i ≥ 2 and the point from frames i and k is in front with error ≤ τ in both then map[track] ← that point
L11     if k mod f = 0 then firewall ← k
L12 return pose
```

Lines L2 and L6 use the preemptive scoring of [preemptive RANSAC](/preemptive-ransac/). The code draws $M$ minimal samples, keeps every solution of each sample as a hypothesis (up to 10 for five points, up to 4 for three points), puts the observations in random order and adds $\min(e^2, \tau^2)$ to each live hypothesis for each observation. After each block of $B$ observations it keeps the better half. For the essential matrix, $e$ is the Sampson distance; for a pose, $e$ is the reprojection error in normalized coordinates, and a point behind the camera costs $\tau^2$.

Line L3 is the [decomposition of the essential matrix](/essential-matrix-decomposition/) into four candidates $(R, \pm t)$, with $R = U W V^{\mathsf T}$ or $U W^{\mathsf T} V^{\mathsf T}$; the candidate is chosen by a vote over the inliers on the [cheirality](/cheirality/) test. Line L3 also fixes the scale of the whole run. Line L7 runs Gauss-Newton on $\sum_i |\pi(R X_i + t) - x_i|^2$ with the update $R \leftarrow \exp([\omega]_\times) R$, $t \leftarrow \exp([\omega]_\times) t + \delta t$ and keeps a step only if the cost goes down. Lines L8 to L10 triangulate with the [linear method](/linear-triangulation/) from the oldest view that the firewall allows, which is the widest baseline available. Line L11 moves the firewall; frames before it are no longer used to triangulate.

**Stereo.** For a rectified pair, the points are triangulated from the left and right images of frame $k - 1$, P3P in preemptive RANSAC against the left image of frame $k$ gives the motion between the two frames, and the poses are chained. Nistér and his coauthors reported that this 3D-to-2D scheme works much better than the alignment of two 3D point sets triangulated at frames $k - 1$ and $k$, because the triangulated depths are uncertain.

**Differences from the paper.** The paper runs the five-point preemptive RANSAC over three consecutive frames at the start. The code makes the start from frames 0 and 2 and then places frame 1 by P3P.

## Example

**Firewall bookkeeping.** Take $f = 4$ and a track that is seen in every frame. At $k = 1$ the first frame that sees it is 0, and $1 - 0 < 2$, so nothing changes. At $k = 3$ the point is triangulated again from frames 0 and 3. At $k = 4$ it is triangulated from frames 0 and 4, and then the firewall moves to 4. At $k = 5$ the first allowed frame is 4 and $5 - 4 < 2$, so the point keeps the value from frames 0 and 4. At $k = 6$ it is triangulated from frames 4 and 6. From now on frames 0 to 3 have no effect on the map.

**A synthetic run.** The test builds 8 frames of a camera with $f_x = f_y = 500$ and a $640 \times 480$ image that moves forward by $0.35$, right by $0.15$ and down by $0.02$ per frame and turns a little about all three axes. 60 points lie at depths 8 to 16 in front of all frames, and 10 percent of all observations are replaced by random points in the image. The camera of frame 2 is at distance $0.7626$ from frame 0, so the algorithm returns every translation multiplied by $1/0.7626 = 1.3113$. After this one scale is removed, the largest rotation error is $3 \times 10^{-15}$ radians and the largest translation error is $6 \times 10^{-14}$. The stereo version with a baseline of $0.5$ and the same kind of outliers returns the metric poses exactly. With Gaussian noise of $\sigma = 0.5$ pixels and 50 points, the stereo run over 6 frames had rotation errors up to $0.23$ degrees and position errors up to $0.05$ on a path of length $1.9$. That last result is one run on one synthetic scene, not a property of the method.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It covers the case without noise and makes one assumption about the robust steps: the hypothesis chosen at lines L2 and L6 is one that was made from a sample of correct matches, and no wrong match falls within $\tau$ of a consistent position. Under that assumption it shows that the algorithm returns the true poses multiplied by the single scale $1/|t_2|$. The steps are: the true essential matrix is among the five-point solutions; exactly one of the four decompositions puts a point in front of both cameras; linear triangulation with exact poses returns the scaled point; the true pose is among the P3P solutions, by the derivation of Grunert's quartic; and Gauss-Newton stays at an exact pose because the gradient there is zero. RANSAC itself gives no guarantee: whether a good sample is drawn and survives the preemption is a matter of probability, with the bound of [ransac-iteration-bound](/ransac-iteration-bound/) under its assumptions.

## Complexity

- **One hypothesis.** The five-point solver eliminates a fixed $10 \times 20$ matrix and finds the roots of a degree 10 polynomial; P3P solves a quartic. Each costs $O(1)$ in the [real RAM](/real-ram/), with constants of different sizes.
- **Preemptive scoring.** With $M$ hypotheses and blocks of $B$, the scorings are at most $B(M + M/2 + M/4 + \dots) \le 2BM$, and the sorts cost $O(M \log M)$. Shuffling $n$ observations is $O(n)$.
- **Refinement.** One Gauss-Newton iteration on $n$ points builds a $6 \times 6$ normal matrix in $O(n)$ and solves it in $O(1)$; $k$ iterations cost $O(kn)$. This is a cost per iteration, not a convergence bound.
- **Triangulation.** Finding the first allowed frame of a track looks at no more than $f$ frames, and each triangulation is a fixed size SVD, so $O(fn)$ per frame.
- **Total.** $O(N(MB + M \log M + kn + fn))$ time, and $O(M + fn)$ extra space for the hypotheses and the tracks behind the firewall. Time per frame does not grow with $N$, which is what makes the method real time.

## Properties

- **Online and bounded.** Each frame costs the same, set in advance by $M$ and $B$. This is the reason for the preemptive scoring.
- **Randomized.** Results depend on the random samples. A fixed seed gives a fixed result.
- **Scale.** With one camera the scale is set once at the start and then carried by the map. Errors in the map change it slowly over time; see [scale drift](/scale-drift/). A stereo rig gives the scale in every frame.
- **Drift.** Each pose is found from the previous map, so errors add up along the path. Without a global step such as [loop closure](/loop-closure-detection/), nothing removes them.
- **Matched, not tracked, corners.** Detecting corners in each frame and matching them keeps each position tied to the image, which avoids the slow slide of positions that a frame-to-frame tracker can have.

## Variants and improvements

- **Stereo scheme.** As above, with metric scale and three-point resection against stereo points. The journal version (J. Field Robotics 2006) describes the system in more detail and reports runs on ground vehicles.
- **Local bundle adjustment.** Later systems refine the last few poses and points together; see [sliding window bundle adjustment](/sliding-window-bundle-adjustment/). The tutorial of Scaramuzza and Fraundorfer cites a final position error 2 to 5 times smaller with it on a 10 km run by Konolige and others; that is a measured result.
- **Keyframes.** Use only frames where the view has changed enough for the triangulation and the resection; see [keyframe selection](/keyframe-selection/).
- **Other robust estimators.** Replace preemptive scoring by plain [RANSAC](/ransac/) or [MSAC](/msac/) when the time per frame need not be fixed.
- **Feature systems with a map.** PTAM and [ORB-SLAM](/orb-slam/) keep keyframes and a map, run bundle adjustment and close loops.
- **Direct methods.** [Semi-direct visual odometry](/semi-direct-visual-odometry/) and [direct sparse odometry](/direct-sparse-odometry/) use pixel intensities instead of matched corners.

## When to use it

Use this scheme when you have a calibrated camera or stereo rig, an image with enough corners, and a need for a fixed time per frame. It is the base of most feature-based visual odometry. Use stereo when you need metric scale and the scene is not too far for the baseline. Prefer a direct method when the image has little corner texture but many edges or smooth gradients, and add bundle adjustment and loop closure when you need a consistent map over long paths.

## Pitfalls

- **Small motion at the start.** If the camera barely moves between frames 0 and 2, the essential matrix is poorly fixed and the triangulated depths are noise. Choose start frames with enough parallax.
- **Pure rotation.** A rotation without translation gives no depth, and the essential matrix is not defined. The first motion must have a translation.
- **Planar scenes.** For points on a plane, the five-point problem has a twofold ambiguity. Score over more views or test a homography.
- **Scale from one step.** The whole monocular run takes its scale from $|t_2|$. If that step is wrong, all distances are wrong by the same factor.
- **Threshold $\tau$.** The inlier threshold is a tuned design choice. With no noise a tight value keeps wrong points out; with noise it must be a few times $\sigma$. A wrong match that lands close to a consistent position cannot be found by any threshold.
- **Firewall spacing.** A small $f$ limits how far an error can pass but also shortens the baselines. The spacing is a heuristic.

## Implementations

## History

Nistér, Naroditsky and Bergen presented the system at CVPR 2004 and used the name "visual odometry" for it, by analogy with wheel odometry. It built on Nistér's five-point solver and his preemptive RANSAC of 2003, both made for live structure from motion. The journal paper of 2006 in the Journal of Field Robotics described the use on ground vehicles. Earlier work, from Moravec in 1980 to the stereo systems of the Mars rovers, had estimated the motion of a robot from stereo images, mostly by aligning 3D points. The tutorial of Scaramuzza and Fraundorfer (2011) gives this history and compares the 3D-to-3D and 3D-to-2D schemes.

## References
