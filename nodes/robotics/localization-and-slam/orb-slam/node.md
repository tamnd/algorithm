---
tag: TY0PRT
kind: algorithm
slug: orb-slam
name: "ORB-SLAM"
aliases:
- ORB-SLAM2
area: robotics/localization-and-slam
level: research
summary: Keyframe visual SLAM with ORB features for tracking, local mapping and loop closing, with pose graph and bundle adjustment back ends.
solves: [slam-problem]
model: real-ram
complexity:
  vars: {n: the number of keyframes, f: the number of features of one keyframe, c: the number of covisible neighbors of a keyframe, l: the total length of the inverted lists of the words of one keyframe}
  time: {loop_query: O(l + c f), toy_geometric_check: O(f^3), toy_essential_graph_step: O(n^3)}
  space: {map: O(n f)}
properties: {deterministic: true, exact: false, online: true, toy_code: true}
history:
  year: 2015
  people: [Raúl Mur-Artal, J. M. M. Montiel, Juan D. Tardós]
  note: Mur-Artal, Montiel and Tardós built a complete monocular SLAM system on one kind of feature, ORB, used for tracking, mapping, relocalization and loop closing. ORB-SLAM2 (2017) added stereo and RGB-D cameras.
prereqs: [orb-features, bundle-adjustment, loop-closure-detection, pose-graph-optimization]
see_also: [visual-odometry, keyframe-selection, bag-of-visual-words, vocabulary-tree, monoslam, perspective-n-point, lidar-odometry-and-mapping, isam2]
sources:
  - paper: doi:10.1109/TRO.2015.2463671
    title: "Raúl Mur-Artal, J. M. M. Montiel and Juan D. Tardós, ORB-SLAM: a versatile and accurate monocular SLAM system, IEEE Transactions on Robotics 31(5), 2015, pages 1147 to 1163"
    locator: "the three threads, the covisibility graph and the essential graph, the place recognition with DBoW2, the loop candidates and their consistency check, the Sim(3) fit, the loop fusion and the essential graph optimization"
  - paper: doi:10.1109/TRO.2017.2705103
    title: "Raúl Mur-Artal and Juan D. Tardós, ORB-SLAM2: an open-source SLAM system for monocular, stereo, and RGB-D cameras, IEEE Transactions on Robotics 33(5), 2017"
    locator: "the extension to stereo and RGB-D input and the full bundle adjustment after a loop closure"
  - paper: doi:10.1109/TRO.2012.2197158
    title: "Dorian Gálvez-López and Juan D. Tardós, Bags of binary words for fast place recognition in image sequences, IEEE Transactions on Robotics 28(5), 2012, pages 1188 to 1197"
    locator: "the bag of binary words, the L1 score and the inverted index that ORB-SLAM uses for place recognition"
---

ORB-SLAM is a keyframe-based visual SLAM system. It uses one kind of feature, [ORB](/orb-features/), for every task: tracking the camera, building the map, recognizing places and closing loops. Three threads run in parallel. Tracking estimates the pose of each frame from the map points that it sees, and decides when to make a new keyframe. Local mapping adds the keyframe to the map, creates new map points by triangulation, and runs a local [bundle adjustment](/bundle-adjustment/) over the keyframe, its covisible neighbors and their points. Loop closing looks for a [loop](/loop-closure-detection/) with a bag of words index each time a keyframe arrives. When it finds and verifies one, it fuses the duplicated map points and corrects the drift by [pose graph optimization](/pose-graph-optimization/) over a sparse subgraph, the essential graph. Two graphs carry the structure. In the covisibility graph, two keyframes are joined when they see enough of the same map points (at least 15 in the paper), and the weight is the number of shared points. The essential graph keeps only a spanning tree, the strong covisibility edges (at least 100 shared points), and the loop edges. ORB-SLAM was monocular. ORB-SLAM2 added stereo and RGB-D input and a full bundle adjustment after each loop closure; the alias on this page names that later system.

The code on this page is a toy. It has no images, no ORB features, no tracking and no bundle adjustment. It keeps only the core of the loop closing thread, in the plane, with simulated features.

## In plain words

A camera moves through a building. The system remembers some of the views, the keyframes, and the 3D points that those views see. Two keyframes are friends when they see many of the same points. For each new keyframe, the system asks whether it looks like an old keyframe that is not one of its friends. To answer fast, it turns each view into a list of visual words and keeps, for each word, the list of keyframes that contain it. A match must hold for three new keyframes in a row and must pass a geometric check. Then the system knows that it has come back, joins the old and the new points, and pulls the whole chain of keyframes into place.

## The problem

The input is a stream of camera frames with a calibrated camera. The output, after each frame, is the camera pose and a map of 3D points with their ORB descriptors, held in keyframes. The system must run in real time, keep the map small by adding and removing keyframes, recover when tracking is lost, and remove drift when the camera returns to a mapped place.

The toy works with planar poses $(x, y, \theta)$. A keyframe gets the odometry from the previous keyframe and a list of features. A feature is a word (an integer that stands for a quantized ORB descriptor) and a 2D point in the frame of the keyframe (which stands for a triangulated map point).

## The algorithm

The pseudocode is the toy. Lines L3 to L9 follow the loop closing thread of ORB-SLAM. Lines L1 and L2 stand in for tracking and local mapping.

```pseudo id=main
PROCESS-KEYFRAME(odometry u, features F)
L1  K ← a new keyframe at pose(last keyframe) ⊕ u; match each feature to a point of the local map with the same word and a close position, else make a new map point
L2  update the covisibility weights of K; parent(K) ← the earlier keyframe that shares the most map points with K
L3  s_min ← the least score between the bag of words of K and those of its covisible neighbors
L4  C ← the keyframes from the inverted index with score ≥ s_min that share no map point with K
L5  for each J in C: group(J) ← {J} ∪ the neighbors of J; count(J) ← 1 + the largest count of an overlapping group of the last keyframe, or 1
L6  for each J with count(J) ≥ 3, best score first: match the features of K and J by word, and fit a rigid transform to the matches
L7      if at least m matches are inliers then
L8          add the loop edge (J, K); fuse the matched map points of K into those of J
L9          optimize the essential graph (spanning tree, strong covisibility edges, loop edges) by Gauss-Newton; stop
L10 add K to the inverted index
```

**The score (lines L3 and L4).** The bag of words vector of a keyframe has tf-idf weights, divided by their sum. The score of DBoW2 is $s(u, v) = 1 - \tfrac12 \|u - v\|_1$, which equals $\sum_w \min(u_w, v_w)$, so the inverted index can compute it from the shared words alone. The least score $s_{\min}$ against the covisible neighbors adapts the threshold to the place: a keyframe that is not a neighbor must look at least as much like $K$ as the neighbors do. Keyframes that already share points with $K$ are not loops.

**Consistency (line L5).** A candidate, with its neighbors, forms a group. The candidate is accepted only when groups that overlap have been found for three keyframes in a row. One look-alike place seldom survives this.

**The geometric check (lines L6 and L7).** ORB-SLAM computes a similarity transform, Sim(3), between the two keyframes with RANSAC on the 3D matches, because a monocular map has an unknown scale that drifts. It then searches for more matches and refines the transform. The toy fits a 2D rigid transform: it tries every pair of matches as a sample, keeps the largest inlier set, and refits on it in closed form.

**The correction (lines L8 and L9).** The edges of the essential graph get the relative poses of the current estimates, so before the loop edge is added the graph has zero error. Only the loop edge pulls. The edges are taken before the fusion. The fusion creates links between keyframes on both sides of the loop, and their relative poses from the drifted estimates must not become edges. ORB-SLAM optimizes the essential graph in Sim(3) and then moves each map point with its reference keyframe. The toy uses SE(2), and a map point stores its position in the frame of its first keyframe, so it moves with that keyframe.

## Example

The toy robot drives on a circle of radius 5 m, with 24 keyframes per lap and 32 keyframes in total. Sixty landmarks lie in two rings, at radii near 3 m and 7 m, and each one has one of 40 words. The robot sees the landmarks within 3 m, with noise 0.02 m. The odometry turns 0.015 rad too much at every keyframe, plus noise. The seed is 1. The system makes 88 map points, and each keyframe has 7 to 11 features. Loop detection starts at keyframe 10.

| keyframe | $s_{\min}$ | candidates (score) | counts of the groups |
|---|---|---|---|
| 11 | 0.396 | 6 (0.435), 7 (0.480) | 1, 1 |
| 17 | 0.372 | 4 (0.376) | 1 |
| 18 | 0.427 | 4 (0.473) | 2 |
| 22 | 0.419 | 0 (0.648), 1 (0.465) | 1, 1 |
| 23 | 0.284 | 0 (0.788), 1 (0.597), 2 (0.346), 3 (0.311) | 2, 2, 2, 2 |
| 24 | 0.648 | 0 (1.000), 1 (0.778) | 3, 3 |

Keyframe 4 lies on the other side of the circle from keyframes 17 and 18. It is a look-alike place, and its group dies at keyframe 19 because no candidate there overlaps it. At keyframe 24 the robot is back at the start. Keyframe 0 has the same words and the score 1. The geometric check finds 7 inliers and the relative pose $(-0.001, -0.019, 0.0006)$, against the true $(0, 0, 0)$. Before the correction, the relative pose between keyframes 0 and 24 is wrong by 1.747 m and 0.345 rad. After it, the error is 0.019 m and 0.012 rad, and the largest position error over keyframes 0 to 24 falls from 1.762 m to 0.094 m. The keyframes after the loop drift again at the rate of the odometry.

On eight seeds the toy closed exactly one loop each time, between one of the keyframes 0 to 3 and one of the keyframes 23 to 27. The error of the loop relative pose after the correction was at most 0.02 m. The largest position error up to the loop keyframe fell from 1.39 to 1.98 m to 0.07 to 0.71 m. It stays large when the loop joins keyframe 3 instead of keyframe 0, because the drift of the first keyframes is not observed by the loop. These are measurements of a toy on simulated data.

## Correctness

ORB-SLAM as a whole has no correctness proof. It is judged by measured accuracy on data sets such as KITTI, EuRoC and TUM RGB-D. The [correctness proof](proofs/correctness.md) covers the toy. It shows that the L1 score equals the sum of the smaller weights of the shared words, so the inverted index gives exact scores; that the closed form rigid fit is the least squares solution; that a candidate is accepted only after three consecutive overlapping groups; that the covisibility weights stay equal to the counts of shared map points through the fusion; and that the essential graph without loop edges has zero error, so only loop edges move the poses. The tests check the hand example of the score, the index against brute force, the rigid fit with outliers, a local minimum of the pose graph, the closing of the loop with the error before and after on three seeds, no loop on a run without a revisit, and the consistency rule.

## Complexity

Let $n$ be the number of keyframes, $f$ the number of features of a keyframe, $c$ the number of covisible neighbors and $l$ the total length of the inverted lists of the words of a keyframe.

- The loop query costs $O(l)$ for the scores and $O(c f)$ for $s_{\min}$ with sparse vectors.
- ORB-SLAM fits Sim(3) with RANSAC on a few candidates. The exhaustive two point search of the toy costs $O(f^3)$.
- The essential graph is sparse, with $O(n)$ edges, and ORB-SLAM optimizes it with a sparse solver. The dense Gauss-Newton step of the toy costs $O(n^3)$.
- The map takes $O(n f)$ space. Keyframe culling in ORB-SLAM removes redundant keyframes, so $n$ grows with the explored area, not with the time.

## Properties

- **One feature for all tasks.** ORB features are fast to compute and to match, and their binary descriptors feed the bag of words.
- **Survival of the fittest.** Keyframes and map points are added generously and culled when they are redundant.
- **Monocular scale.** With one camera, the scale is not observed and drifts. Sim(3) loop correction fixes the scale drift too.
- **Relocalization.** When tracking is lost, the same bag of words index finds candidate keyframes, and a [perspective-n-point](/perspective-n-point/) solution with RANSAC recovers the pose.
- **Measured, not guaranteed.** Accuracy and robustness are measured on data sets.

## Variants and improvements

- **ORB-SLAM2.** Stereo and RGB-D cameras, which observe the scale; a full bundle adjustment in a separate thread after a loop closure; a localization only mode.
- **ORB-SLAM3.** Visual-inertial input, fisheye cameras, and a set of maps that can be merged when the robot returns to an old map.
- **Other back ends.** The essential graph can be replaced by an incremental smoother such as [iSAM2](/isam2/), and the bag of words by learned place recognition.
- **Robust loops.** [Switchable constraints](/switchable-constraints/) or consistency checks guard against wrong loops that pass the checks.

## When to use it

Use ORB-SLAM, or one of its successors, for real-time SLAM with a camera in scenes with enough texture, when loops are expected and a sparse map is enough. For dense maps, low texture or fast motion, other systems fit better, and with a lidar, a system such as [LOAM](/lidar-odometry-and-mapping/) is the usual choice. Use the toy only to study the loop closing logic.

## Pitfalls

- **Pure rotation and initialization.** A monocular system needs parallax to start. ORB-SLAM chooses between a homography and a fundamental matrix model for the first two frames.
- **Low texture and motion blur.** Few features mean lost tracking. Relocalization helps only at mapped places.
- **Perceptual aliasing.** Repeated structures produce look-alike places. The consistency and geometric checks reduce wrong loops but cannot exclude them.
- **Edges from the fusion.** Covisibility links that the fusion makes across a loop must not enter the correction with their drifted relative poses. The toy builds the essential graph before the fusion for this reason.
- **Scale drift.** A monocular map corrected in SE(3) instead of Sim(3) keeps the scale error.

## Implementations

## History

PTAM of Klein and Murray (2007) split tracking and mapping into two threads and used keyframes with bundle adjustment. Strasdat and colleagues showed the value of covisibility-based local windows and of Sim(3) pose graph optimization for monocular scale drift. Gálvez-López and Tardós (2012) gave the fast bag of binary words. Mur-Artal, Montiel and Tardós (2015) joined these ideas into ORB-SLAM, with one feature for all tasks and the essential graph for loop correction. Mur-Artal and Tardós (2017) extended it to stereo and RGB-D as ORB-SLAM2, and Campos and colleagues released ORB-SLAM3 in 2021.

## References
