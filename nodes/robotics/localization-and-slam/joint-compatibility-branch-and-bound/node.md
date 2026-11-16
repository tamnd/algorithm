---
tag: V4AT33
kind: algorithm
slug: joint-compatibility-branch-and-bound
name: Joint compatibility branch and bound
aliases:
- JCBB
area: robotics/localization-and-slam
level: advanced
summary: Neira and Tardos's search for the largest set of reading to landmark pairings that passes one joint chi-square test. It rejects pairings that only look right one at a time.
solves: [data-association-slam]
model: real-ram
complexity:
  vars: {m: the number of readings, n: the number of features, d: the dimension of one reading}
  time: {worst: O((n+1)^m (d m)^3), node: O((d m)^3)}
  space: {extra: O(n^2 d^2 + m)}
properties: {deterministic: true, exact: true, online: true}
history:
  year: 2001
  people: [José Neira, Juan D. Tardós]
  note: Neira and Tardos (2001) introduced the joint compatibility test and searched the interpretation tree of pairings by branch and bound to find the largest jointly compatible hypothesis.
prereqs: [data-association-slam, ekf-slam, chi-squared-goodness-of-fit-test, depth-first-branch-and-bound]
see_also: [ekf-localization, nearest-neighbor-search, maximum-clique, ransac, assignment-problem, hungarian-algorithm, loop-closure-detection, fastslam]
sources:
  - paper: "José Neira and Juan D. Tardós, Data association in stochastic mapping using the joint compatibility test, IEEE Transactions on Robotics and Automation 17(6), 2001, pages 890 to 897"
    locator: the individual and the joint compatibility tests, the incremental computation of the joint distance, the JCBB algorithm, and the comparison with sequential nearest neighbor
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: Chapter 10, Section 10.3 (EKF SLAM with unknown correspondences) for the nearest neighbor rule with a gate
  - paper: doi:10.1109/MRA.2006.1638022
    title: "Hugh Durrant-Whyte and Tim Bailey, Simultaneous localization and mapping, part I, IEEE Robotics and Automation Magazine 13(2), 2006, from page 99"
    locator: the role of data association in SLAM
---

Joint compatibility branch and bound (JCBB) finds which reading in a scan comes from which landmark of the map. It is a step of [EKF SLAM](/ekf-slam/) and of other Gaussian filters, not a filter itself. The simple rule, nearest neighbor with a gate, tests each reading alone and can pair several readings wrongly in the same way. JCBB tests a whole set of pairings together: the readings share the error of the robot pose, so their innovations are correlated, and one chi-square test on the stacked innovation catches a set that is consistent one by one but not as a whole. A depth-first branch and bound search finds the set with the most pairings that passes. The worst case is exponential in the number of readings.

## In plain words

The robot sees a few posts and must say which post on its map each one is. If its position estimate is off by half a meter, the closest post on the map is often the wrong one, and every reading is off in the same direction. Looking at one reading at a time cannot see this. JCBB looks at the readings together and asks if one shift of the robot explains all the pairings at once. It tries the pairings for the first reading, then for the second, and so on, and it stops on a branch as soon as the pairings so far cannot all be true. It keeps the answer that explains the most readings. Readings that fit no post, such as a passing person, stay unpaired.

## The problem

The input is one step of a Gaussian filter. The state estimate has the covariance $P$. There are $m$ readings $z_0, \dots, z_{m-1}$ and $n$ features of the map with predicted readings $h_0, \dots, h_{n-1}$ in $\mathbb{R}^d$, the Jacobians $H_j$ of the predictions with respect to the state, and the noise covariance $R$ of one reading. A hypothesis $\mathcal{H}$ gives each reading a feature or $*$ for none. Its pairings $E = ((i_1, j_1), \dots, (i_k, j_k))$ have the stacked innovation and covariance

$$\nu_E = \begin{pmatrix} z_{i_1} - h_{j_1} \\ \vdots \\ z_{i_k} - h_{j_k} \end{pmatrix}, \qquad C_E = \begin{pmatrix} H_{j_1} \\ \vdots \\ H_{j_k} \end{pmatrix} P \begin{pmatrix} H_{j_1} \\ \vdots \\ H_{j_k} \end{pmatrix}^\top + \mathrm{diag}(R, \dots, R),$$

and the joint distance $D^2(E) = \nu_E^\top C_E^{-1} \nu_E$. The set is *jointly compatible* if $D^2(E) \le \chi^2_{dk, \alpha}$, the $\alpha$ quantile of the chi-square distribution with $dk$ degrees of freedom; one pairing that passes alone is *individually compatible*. The off-diagonal blocks $H_{j_a} P H_{j_b}^\top$ carry the shared error of the state. The output is a hypothesis with the most pairings that JCBB can reach (defined below), with the smallest $D^2$ among those.

## The algorithm

```pseudo id=main
JCBB(H, i)                ▷ H: pairings of readings 0..i-1; Best: global, starts empty
L1  visit the node (H, i)
L2  if i = m then
L3      if |H| > |Best|, or |H| = |Best| and D²(H) < D²(Best) then
L4          Best ← H
        return
L5  for j ← 0 to n - 1 do
L6      if (i, j) is not individually compatible, or j is in H and pairings are unique then skip j
L7      if D²(H + (i, j)) ≤ χ²(d (|H| + 1), α) then
L8          JCBB(H + (i, j), i + 1)
L9  k_max ← |H| + (m - i - 1)                    ▷ the most pairings if reading i stays unpaired
L10 if k_max > |Best|, or k_max = |Best| and D²(H) < D²(Best) then
L11     JCBB(H + (i, *), i + 1)
L12 return Best                                  ▷ after the call JCBB(∅, 0)
```

The search is depth first over the interpretation tree: level $i$ chooses the feature of reading $i$, and the branch $*$ leaves it unpaired. Line L7 prunes a branch as soon as its pairings fail the joint test. Line L10 is the bound: if even pairing every later reading cannot beat the best hypothesis, the $*$ branch is not searched. The paper of Neira and Tardos keeps the first hypothesis with the most pairings and has only the first part of the tests of lines L3 and L10; the code calls this `tie_break=False`. The second part, the smaller $D^2$ among equal numbers of pairings, is an addition of this page, and it is safe because $D^2$ never decreases along a branch.

**Line L7, the joint test.** The code builds $C_E$ from blocks $H_j P H_k^\top$ that it computes once, and solves one linear system per node. Neira and Tardos also give an incremental form of $D^2$ that reuses the result of the parent node.

**Repeated features.** By default two readings may pair with the same feature, as in the paper; a feature can produce two readings, for example two corners of one segment. With `unique=True`, line L6 forbids it.

## Example

Three posts stand at $(0, 2)$, $(1, 2)$ and $(2.5, 2)$. The robot thinks it is at the origin with $P = \mathrm{diag}(0.25, 0.25)$, a standard deviation of 0.5 m on each axis, and it reads the position of each post relative to itself, $h_j = m_j - x$ with $H_j = -I$, with the noise $R = \mathrm{diag}(0.01, 0.01)$. The robot is really at $(-0.7, 0)$, so every reading is shifted by about $0.7$ m to the right. The readings are $z_0 = (0.72, 2.01)$, $z_1 = (1.69, 1.98)$ and $z_2 = (3.21, 2.02)$.

The individual distances $D^2$ for each reading and post are, with the gate $\chi^2_{2, 0.95} = 5.991$:

| | post 0 | post 1 | post 2 |
|---|---|---|---|
| $z_0$ | 1.994 | **0.302** | 12.187 |
| $z_1$ | 10.987 | **1.833** | 2.525 |
| $z_2$ | 39.633 | 18.787 | **1.940** |

Nearest neighbor takes the smallest value in each row and pairs $(z_0, z_1, z_2)$ with posts $(1, 1, 2)$. Each pairing passes alone. Together they imply shifts of the robot of $(-0.28, 0.01)$, $(0.69, -0.02)$ and $(0.71, 0.02)$, which do not agree, and $D^2 = 64.68$ is far above $\chi^2_{6, 0.95} = 12.592$. Already the first two pairings give $D^2 = 47.26 > \chi^2_{4, 0.95} = 9.488$.

JCBB starts with post 0 for $z_0$ ($D^2 = 1.994$), adds post 1 for $z_1$ ($D^2 = 2.039 \le 9.488$) and post 2 for $z_2$ ($D^2 = 2.105 \le 12.592$). This leaf has 3 pairings, the most possible, so no later $*$ branch passes line L10. The search then tries post 1 for $z_0$; with it, post 1 for $z_1$ gives $D^2 = 47.26$ and post 2 gives $D^2 = 15.25$, both above 9.488, and the $*$ branch can reach only 2 pairings. The answer is posts $(0, 1, 2)$, with implied shifts $(0.72, 0.01)$, $(0.69, -0.02)$ and $(0.71, 0.02)$ that agree. The search visits 5 nodes of the 85 in the full tree.

## Correctness

The [correctness proof](proofs/correctness.md) shows that JCBB returns the best hypothesis of its search space: among the hypotheses whose pairings are individually compatible and whose prefixes, in the order of the readings, are all jointly compatible, it returns one with the most pairings and then the smallest $D^2$. The proof uses that $D^2$ never decreases when a pairing is added, by a Schur complement, which makes both the pruning of line L7 and the bound of line L10 safe. The tests compare the result with a brute force search over all $(n + 1)^m$ hypotheses on 24 random scenes with clutter.

The joint test itself is not monotone: the threshold grows with the number of pairings, so a set can pass while one of its prefixes fails. Such a set is outside the search space. The result is also only as good as the Gaussian model: with a wrong $P$ or strong nonlinearity, the right hypothesis can fail the test.

## Complexity

Let $m$ be the number of readings, $n$ the number of features and $d$ the dimension of one reading. Costs are in the [real RAM](/real-ram/) model.

- **Nodes:** the tree has $(n + 1)^m$ leaves, and in the worst case the search visits all of them. This is a property of the tree, and Neira and Tardos state that the algorithm is exponential. In practice, the gates of lines L6 and L7 remove most branches, and the bound removes most $*$ branches once a good hypothesis is found. The number of visited nodes depends on the clutter and on $P$; it is a measurement, not a bound.
- **Per node:** solving the system of line L7 costs $O((dk)^3)$ for $k \le m$ pairings, so $O((dm)^3)$. An incremental update of a Cholesky factor brings it to $O((dm)^2)$.
- **Setup:** the blocks $H_j P H_k^\top$ cost $O(n^2 d^2 s + n d s^2)$ for a state of size $s$. For EKF SLAM with point landmarks, $H_j$ has a few nonzero columns, and the cost is much smaller.
- **Memory:** $O(n^2 d^2)$ for the blocks and $O(m)$ for the recursion.

Restricting the features to those that are near the robot keeps $n$ small, and that matters more than any other change.

## Properties

- **Exact search over its space.** The result is the best reachable hypothesis, a theorem proved on this page. It is not a claim that the result is the true association.
- **Robust to a shared error.** It handles a large pose error that shifts all readings the same way, which is the case where nearest neighbor fails. This is the main reason to use it, for example at a loop closure.
- **Rejects clutter.** A reading that fits no feature stays unpaired, since the $*$ branch is always possible.
- **Deterministic and order dependent.** The order of the readings changes the search space through the prefix rule, and can change the answer when the joint test is close.

## Variants and improvements

- **Sequential compatibility nearest neighbor.** Pair the readings one by one with their nearest neighbor and check the joint test as the set grows. Neira and Tardos compare JCBB with it.
- **Randomized joint compatibility.** Later work from the same group tests small random sets of pairings, as in [RANSAC](/ransac/), and grows the best one with the joint test, which avoids the exponential search.
- **Compatibility graphs.** Make a graph whose nodes are individually compatible pairings and whose edges join pairings that are compatible two by two, and look for a [maximum clique](/maximum-clique/). This tests pairs, not the full set.
- **Unique assignment.** If each feature can produce at most one reading, set `unique=True`. If a cost matrix is enough and the shared error is small, the [Hungarian algorithm](/hungarian-algorithm/) solves the [assignment problem](/assignment-problem/) in polynomial time.
- **Multiple hypotheses.** Particle methods such as [FastSLAM](/fastslam/) can draw a different association in each particle, which keeps several answers alive.

## When to use it

Use JCBB when several readings are taken at once and the pose error is large compared with the distance between features, for example when the robot comes back to a known area after a long loop. When the pose is well known and the features are far apart, nearest neighbor with a gate gives the same answer at a lower cost. With many readings and many nearby features, bound the search: split the readings into groups, or use a randomized variant.

## Pitfalls

- **The wrong quantile.** The threshold of a set of $k$ pairings uses $dk$ degrees of freedom, not $d$. Using the threshold of one reading for the whole set rejects almost everything.
- **Dropping the cross terms.** If $C_E$ is built with only the diagonal blocks, the test reduces to a sum of individual tests and loses the shared error, which is the point of JCBB.
- **Angles.** For bearing readings, wrap each innovation before stacking.
- **Too many readings.** The worst case is exponential. A scan of 30 readings with many features in each gate can take a very long time; set a limit on the nodes or on the readings.
- **An overconfident filter.** If $P$ is too small, the right hypothesis fails the joint test, and JCBB returns fewer pairings. The [EKF SLAM](/ekf-slam/) page describes how a nonlinear filter becomes overconfident.

## Implementations

## History

Data association with a gate on the Mahalanobis distance comes from target tracking. Neira and Tardos (2001) observed that in stochastic mapping, the readings of one scan are correlated through the robot pose, so individual gates accept wrong sets. They defined the joint compatibility test, gave an incremental way to compute it, and searched the interpretation tree, a tool of model based object recognition, by branch and bound. Their experiments compared JCBB with sequential compatibility nearest neighbor and showed that it is more robust when the pose error is large. JCBB is now a common data association step of EKF SLAM.

## References
