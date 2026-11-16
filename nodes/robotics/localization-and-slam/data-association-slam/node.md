---
tag: 21926G
kind: problem
slug: data-association-slam
name: Data association in SLAM
aliases:
- correspondence problem in SLAM
area: robotics/localization-and-slam
level: core
summary: Decide which map landmark, if any, each measurement comes from, where wrong choices can make the estimate diverge.
prereqs: [slam-problem, extended-kalman-filter, chi-squared-goodness-of-fit-test]
see_also: [joint-compatibility-branch-and-bound, data-association, nearest-neighbor-search, hungarian-algorithm, joint-probabilistic-data-association, multiple-hypothesis-tracking, loop-closure-detection, ransac]
sources:
  - paper: "José Neira and Juan D. Tardós, Data association in stochastic mapping using the joint compatibility test, IEEE Transactions on Robotics and Automation 17(6), 2001, pages 890 to 897"
    locator: the individual compatibility test, the failure of nearest neighbor when the pose is uncertain, the joint compatibility test and the JCBB search
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 10, Section 10.3 (EKF SLAM with unknown correspondences, the maximum likelihood choice with a gate for new landmarks) and Chapter 13 (data association per particle in FastSLAM)"
  - paper: "Tim Bailey and Hugh Durrant-Whyte, Simultaneous localization and mapping (SLAM), part II, IEEE Robotics and Automation Magazine 13(3), 2006, pages 108 to 117"
    locator: the section on data association
---

Data association in SLAM is the question of which landmark of the map each new reading comes from, or whether it comes from a landmark not yet in the map, or from no landmark at all. The [SLAM problem](/slam-problem/) is often stated with known correspondences, as if each reading came with the name of its landmark. Real sensors give no names: a laser sees a post, and a camera sees a corner, and the program must decide which post or corner of its map this is. The decision is hard because the map and the pose are uncertain, so several landmarks may fit one reading. A wrong decision is then used as if it were true, and it can pull the estimate so far off that the filter never recovers. The same question in tracking is [data association](/data-association/) between measurements and tracks; in SLAM the robot pose adds one shared error to all readings, which [joint compatibility branch and bound](/joint-compatibility-branch-and-bound/) uses.

## In plain words

A robot sees three trees. Its map holds ten trees, but the robot is not sure where it stands, so it is not sure which of the ten it sees now. For each tree it sees, it can ask which map trees are close enough to where it expects them. Sometimes only one tree fits, and the choice is easy. Sometimes two trees fit, or none does. If none fits, the tree may be new. If two fit and it picks the wrong one, it will move the map and itself to a wrong place, and it may never notice. Looking at the three trees together helps: a choice that is fine for each tree alone can be wrong when the three must agree on one robot position.

## Definition

**Input.** A Gaussian estimate of the robot pose and the map, with mean $\mu$ and covariance $\Sigma$, as kept by [EKF SLAM](/ekf-slam/). A set of $k$ readings $z_1, \dots, z_k$ taken at one time. A measurement model $z = h_j(x, m_j) + w$ for landmark $j$ of $n$, with noise $w \sim N(0, R)$.

**Output.** A hypothesis $\mathcal{H} = (j_1, \dots, j_k)$ that gives each reading $z_i$ a landmark $j_i$, or $*$ for "new landmark or spurious reading". Usually no two readings of one scan may take the same landmark.

**The test of one pairing.** For a pairing of $z_i$ with landmark $j$, the innovation is $\nu_{ij} = z_i - h_j(\mu)$, and its covariance is $S_{ij} = H_{ij} \Sigma H_{ij}^\top + R$, with $H_{ij}$ the Jacobian of $h_j$. The squared Mahalanobis distance is

$$D_{ij}^2 = \nu_{ij}^\top S_{ij}^{-1} \nu_{ij}.$$

If the pairing is right and the model is linear and Gaussian, $D_{ij}^2$ follows a chi-square distribution with $d$ degrees of freedom, where $d$ is the size of a reading. The gate accepts the pairing if $D_{ij}^2 \le \chi^2_{d, \alpha}$, and a right pairing fails the gate with probability $1 - \alpha$. For $d = 2$, the quantiles are $\chi^2_{2, 0.95} = 5.991$ and $\chi^2_{2, 0.99} = 9.210$.

**The question.** Find the hypothesis that best explains the readings: in the version of Neira and Tardós, the one with the most pairings whose stacked innovation, with all its correlations, passes one joint chi-square test.

## Variants

- **Local and global.** Local association pairs the readings of one scan with landmarks near the predicted pose. Global association, as in a loop closure or the [kidnapped robot problem](/kidnapped-robot-problem/), must work when the pose is almost unknown; it is then solved by appearance, see [loop closure detection](/loop-closure-detection/), or by robust search such as [RANSAC](/ransac/).
- **Single scan or several.** One can decide at each scan, or delay the decision and keep several hypotheses over time, as in [multiple hypothesis tracking](/multiple-hypothesis-tracking/).
- **Hard and soft.** A hard decision picks one landmark. A soft one weights all candidate landmarks, as in [joint probabilistic data association](/joint-probabilistic-data-association/).
- **Per particle.** In a particle filter such as [FastSLAM](/fastslam/), each particle can make its own choice with its own pose and map, so the filter keeps many hypotheses at no extra design cost.

## Examples

**The gate, by hand.** Two landmarks are predicted at $\hat z_1 = (2.0, 0.0)$ and $\hat z_2 = (2.5, 0.5)$, each with $S = \operatorname{diag}(0.1, 0.1)$. The gate is $\chi^2_{2, 0.95} = 5.991$.

| reading | $D^2$ to landmark 1 | $D^2$ to landmark 2 | inside the gate |
|---|---|---|---|
| $z_a = (2.3, 0.1)$ | $(0.09 + 0.01) / 0.1 = 1.0$ | $(0.04 + 0.16) / 0.1 = 2.0$ | both |
| $z_c = (2.2, 0.0)$ | $(0.04 + 0) / 0.1 = 0.4$ | $(0.09 + 0.25) / 0.1 = 3.4$ | both |
| $z_b = (4.0, 2.0)$ | $(4 + 4) / 0.1 = 80$ | $(2.25 + 2.25) / 0.1 = 45$ | none |

Reading $z_b$ fits no landmark, so it starts a new landmark, or it is dropped as spurious. Nearest neighbor alone gives landmark 1 to both $z_a$ and $z_c$, which cannot be right if one landmark gives one reading. If each landmark may be used once, the best total is $z_a \to 2$ and $z_c \to 1$, with $2.0 + 0.4 = 2.4$, against $1.0 + 3.4 = 4.4$ for the other way. With 2 landmarks and 3 readings, there are $(2 + 1)^3 = 27$ hypotheses in all, if each reading may also be $*$.

This example treats the readings as independent. In SLAM they are not: all of them share the error of the robot pose. The [JCBB page](/joint-compatibility-branch-and-bound/) shows a case where each nearest neighbor pairing passes its own gate, but the set fails the joint test by a wide margin.

## Known algorithms

- **Nearest neighbor with a gate.** For each reading, take the landmark with the smallest $D^2$ if it is inside the gate; else start a new landmark. This is the rule of EKF SLAM with unknown correspondences in Probabilistic Robotics. It costs $O(k n)$ tests, or less with a [nearest neighbor search](/nearest-neighbor-search/) structure for the candidates. It is a heuristic: it fails when the pose error is large compared with the distance between landmarks.
- **Global nearest neighbor.** Minimize the sum of the distances under the rule that each landmark takes at most one reading. This is an [assignment problem](/assignment-problem/), solved by the [Hungarian algorithm](/hungarian-algorithm/) in polynomial time.
- **[Joint compatibility branch and bound](/joint-compatibility-branch-and-bound/).** Neira and Tardós (2001) search the tree of hypotheses depth first and keep the largest set of pairings that passes the joint test, which accounts for the correlations through the pose.
- **Soft and multi-hypothesis methods.** [Joint probabilistic data association](/joint-probabilistic-data-association/), [multiple hypothesis tracking](/multiple-hypothesis-tracking/), and per particle association in [FastSLAM](/fastslam/).
- **Robust and appearance based methods.** [RANSAC](/ransac/) over small sets of pairings, appearance matching for [loop closure detection](/loop-closure-detection/), and robust back ends such as [switchable constraints](/switchable-constraints/) that can turn off a wrong association later.

## Bounds

- **Number of hypotheses.** With $n$ landmarks and $k$ readings, each reading can take one of $n + 1$ values, so there are up to $(n + 1)^k$ hypotheses. Exhaustive search is exponential in $k$.
- **JCBB is exponential in the worst case.** Its search tree is the tree of these hypotheses, and in the worst case the gates and the bound remove no branch, so it visits all of them. Neira and Tardós state that the algorithm is exponential. In practice the number of visited nodes is much smaller; that is a measurement, and it depends on the clutter and the pose uncertainty.
- **Independent scores.** If each pairing gets a score that does not depend on the other pairings, the best one-to-one choice is an assignment problem and takes polynomial time. The joint test couples the pairings through the shared pose error, and then this reduction no longer applies.
- **Probability of a wrong rejection.** A right pairing fails a gate at level $\alpha$ with probability $1 - \alpha$, if the model is linear and Gaussian and the covariance is right. If the filter is overconfident, true pairings fail more often than this.

## Reductions

- **To the assignment problem.** With independent scores and the rule of one reading per landmark, data association is a weighted bipartite matching between readings and landmarks plus "new" slots; see the [assignment problem](/assignment-problem/).
- **To maximum clique.** Make a graph whose vertices are the pairings that pass their own gate, with an edge between two pairings that pass a test together. A set of pairings that pass all their pairwise tests is a clique, so the largest such set is a [maximum clique](/maximum-clique/). Pairwise tests do not give the full joint test, so this is a relaxation.
- **From tracking.** Data association in multi-target tracking, [data association](/data-association/), is the same question with moving targets and without the shared robot pose.

## Applications

Every landmark SLAM system with sensors that do not identify landmarks needs a data association step: laser SLAM with posts or trees as features, visual SLAM with image features, where descriptors narrow the candidates first, and underwater SLAM with sonar. Loop closure is data association at a large scale: a wrong loop closure accepted by a graph optimizer can fold a map onto itself, which is why systems check loop closures with geometric tests and robust costs.

## References
