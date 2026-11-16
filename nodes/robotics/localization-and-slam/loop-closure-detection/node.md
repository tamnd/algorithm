---
tag: GV4XBE
kind: problem
slug: loop-closure-detection
name: Loop closure detection
aliases:
- revisit detection
area: robotics/localization-and-slam
level: core
summary: Recognize that the robot has returned to a place it mapped before, to add a constraint that removes drift.
prereqs: [slam-problem, bag-of-visual-words, precision-and-recall]
see_also: [vocabulary-tree, inverted-index, tf-idf, ransac, pose-graph, switchable-constraints, orb-slam, kidnapped-robot-problem]
sources:
  - paper: doi:10.1109/TRO.2012.2197158
    title: "Dorian Gálvez-López and Juan D. Tardós, Bags of binary words for fast place recognition in image sequences, IEEE Transactions on Robotics 28(5), 2012, pages 1188 to 1197"
    locator: "the vocabulary tree of binary words, the inverted and direct indexes, the L1 score of tf-idf vectors, the grouping of matches by time, the temporal consistency check and the geometric check, and the precision and recall results"
  - paper: doi:10.1177/0278364908090961
    title: "Mark Cummins and Paul Newman, FAB-MAP: probabilistic localization and mapping in the space of appearance, International Journal of Robotics Research 27(6), 2008, pages 647 to 665"
    locator: "the probability that an observation comes from a known place or a new place, the Chow-Liu tree over word occurrences, and the precision and recall results"
  - paper: doi:10.1109/TRO.2016.2624754
    title: "Cesar Cadena, Luca Carlone, Henry Carrillo, Yasir Latif, Davide Scaramuzza, Jose Neira, Ian Reid and John J. Leonard, Past, present, and future of simultaneous localization and mapping: toward the robust-perception age, IEEE Transactions on Robotics 32(6), 2016, pages 1309 to 1332"
    locator: "the role of loop closures and of wrong data association in the front end"
---

Loop closure detection asks whether the robot is now at a place it has visited before. A SLAM system that only chains measurements, by odometry or by [visual odometry](/visual-odometry/), drifts without bound. When the robot comes back to a known place and recognizes it, the system can add an edge between the current pose and the old pose to the [pose graph](/pose-graph/). The back end then spreads the accumulated error over the loop. The problem has two parts: find candidate places, usually by comparing appearance, and verify each candidate by geometry, which also gives the relative pose for the new edge. A wrong loop closure can ruin the map, so detectors are tuned for high precision, and back ends may add protection such as [switchable constraints](/switchable-constraints/). There is no exact answer to compare against in general. Methods are judged by [precision and recall](/precision-and-recall/) measured on data sets with ground truth, so the results are measurements on those data sets.

## In plain words

A robot that walks around a building keeps track of where it is by adding up small steps, and the small errors add up too. When it comes back to the front door, it should notice that it has been here before. Then it can tell its map that the start and the end of its walk are the same place, and the whole map gets pulled into shape. The hard part is the noticing. Many places look alike, such as two corridors with the same doors, and the same place looks different in other light. So the robot first looks for old pictures that share many small details with the new one, and then checks that the details are in a matching layout before it trusts the match.

## Definition

**Input.** A sequence of observations $z_1, z_2, \dots, z_t$, for example camera images or lidar scans, taken at poses $x_1, \dots, x_t$ that are not known exactly. Optionally, the current pose estimate and its uncertainty.

**The question.** For the newest observation $z_t$, find the earlier times $j$ with $j < t - w$ at which the robot was at the same place, together with the relative pose $x_j^{-1} x_t$. The window $w$ excludes recent frames, which always look similar. "The same place" is defined for each data set, for example a ground truth distance below a threshold and an overlapping field of view.

**Measures.** Let TP be the number of reported loop closures that are true, FP the number that are false, and FN the number of true revisits that are not reported. Then precision is $\mathrm{TP} / (\mathrm{TP} + \mathrm{FP})$ and recall is $\mathrm{TP} / (\mathrm{TP} + \mathrm{FN})$. A detector has a threshold, and changing it trades precision against recall. Because one false loop closure can bend the map, many papers report the recall at 100% precision.

## Variants

- **Appearance only.** Only the observations are used. This also solves place recognition for relocalization after tracking is lost, the [kidnapped robot problem](/kidnapped-robot-problem/).
- **With a pose prior.** The current estimate and its covariance limit the search to places within the uncertainty. This is cheaper but fails when the drift is larger than the estimated uncertainty.
- **Cameras and lidars.** Images use local features and descriptors. Lidar scans use scan matching against old submaps, or global descriptors of the scan.
- **Single frames or sequences.** A match of one frame is noisy. Methods that require consistent matches over several frames, such as SeqSLAM of Milford and Wyeth, are more robust to changes of light and season.
- **Multi-robot.** Find places that two robots both visited, to join their maps.

## Examples

**Scoring with bags of words.** A vocabulary has 4 visual words. In a database of 4 images, word 1 appears in all 4 images, word 2 in 2, and words 3 and 4 in 1 each. With [tf-idf](/tf-idf/), the weight of word $i$ in an image is its share of the words of the image times $\ln(N / n_i)$, so the idf factors are $0$, $\ln 2$, $2\ln 2$ and $2\ln 2$. The query image has the word counts $(2, 1, 1, 0)$, so its weights are $(0, \tfrac14 \ln 2, \tfrac12 \ln 2, 0)$. After dividing by the sum, it is $q = (0, \tfrac13, \tfrac23, 0)$. Image $B$ has the counts $(1, 1, 1, 1)$, which gives $b = (0, \tfrac15, \tfrac25, \tfrac25)$. Image $C$ has the counts $(3, 0, 0, 1)$, which gives $c = (0, 0, 0, 1)$. The L1 score of DBoW2 is $s(u, v) = 1 - \tfrac12 \|u - v\|_1$. Then
$$s(q, b) = 1 - \tfrac12\left(\tfrac{2}{15} + \tfrac{4}{15} + \tfrac{6}{15}\right) = 0.6, \qquad s(q, c) = 1 - \tfrac12 (\tfrac13 + \tfrac23 + 1) = 0.$$
Word 1 is in every image and has weight 0, so it does not help. Image $B$ is the candidate. Before it becomes a loop closure, a geometric check must find enough feature matches that agree with one relative pose.

**Counting precision and recall.** A route has 10 true revisits. The detector reports 8 loop closures, and 7 of them are true. Precision is $7/8 = 0.875$ and recall is $7/10 = 0.7$. The one false report would add a wrong edge to the pose graph. If a higher threshold removes it and two true reports, precision becomes $5/5 = 1$ and recall $5/10 = 0.5$.

## Known algorithms

- **Bags of binary words (DBoW2).** Gálvez-López and Tardós quantize binary descriptors such as [BRIEF](/brief-descriptor/) or [ORB](/orb-features/) with a [vocabulary tree](/vocabulary-tree/), score images by tf-idf vectors with an [inverted index](/inverted-index/), group matches that are close in time, require consistency over consecutive frames, and verify the best candidate geometrically. A direct index speeds up the feature matching for the check.
- **FAB-MAP.** Cummins and Newman compute the probability that the observation comes from each known place or from a new place. A Chow-Liu tree models which words tend to appear together, which reduces false matches from common words.
- **Geometric verification.** Match features between the two images and fit an [essential matrix](/essential-matrix/), a [fundamental matrix](/fundamental-matrix/) or a [perspective-n-point](/perspective-n-point/) solution with [RANSAC](/ransac/). Accept the loop if enough matches are inliers. For lidar, align the scans by [iterative closest point](/iterative-closest-point/) or [correlative scan matching](/correlative-scan-matching/) and check the residual.
- **Covisibility checks.** [ORB-SLAM](/orb-slam/) requires that a candidate keyframe and its covisible neighbors match consecutive new keyframes before it accepts the loop.
- **Learned global descriptors.** Networks such as NetVLAD map an image to one vector, and the search becomes nearest neighbor search.

## Bounds

There is no exact solution to compare against, because "the same place" depends on the sensor and on the ground truth threshold, and different places can look the same (perceptual aliasing). Quality is reported as measured precision and recall on data sets, and the numbers depend on the data set, the vocabulary and the thresholds.

The cost can be stated. Comparing the query with all $t$ earlier observations costs $O(t)$ comparisons, so $O(t^2)$ over a whole run. With an inverted index, a query touches only the lists of its own words, and words that occur in many images have small idf weights and can be skipped. A geometric check with RANSAC costs a number of iterations that depends on the inlier ratio, times the number of matches.

## Reductions

- **Image retrieval.** The candidate search is content-based image retrieval with the old keyframes as the database, as in [bag of visual words](/bag-of-visual-words/) search.
- **Robust model fitting.** The verification is robust estimation of a relative pose from matches, usually by RANSAC.
- **Data association.** Loop closure is the data association problem of SLAM at the scale of whole places. See [data association in SLAM](/data-association-slam/).

## Applications

- Adding loop closure edges to the pose graph in visual SLAM, as in [ORB-SLAM](/orb-slam/), and in lidar SLAM, as in systems that add a loop module to [LOAM](/lidar-odometry-and-mapping/).
- Relocalization after tracking failure, and recognition of a known map at start up.
- Merging maps from several sessions or several robots.
- Long-term operation, where the same places must be recognized across days and seasons.

## References
