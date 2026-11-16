---
tag: KEMWGG
kind: problem
slug: full-slam
name: Full SLAM
aliases:
- smoothing SLAM
area: robotics/localization-and-slam
level: core
summary: SLAM that estimates the whole path of the robot together with the map from all the data.
prereqs: [slam-problem, smoothing, nonlinear-least-squares]
see_also: [online-slam, slam-problem, graphslam, square-root-sam, isam2, pose-graph-optimization, factor-graph, bundle-adjustment]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 10 (the full SLAM problem) and Chapter 11 (GraphSLAM, the full problem as sparse least squares)"
  - paper: doi:10.1109/MRA.2006.1638022
    title: "Hugh Durrant-Whyte and Tim Bailey, Simultaneous localization and mapping, part I, IEEE Robotics and Automation Magazine 13(2), 2006, from page 99"
    locator: the probabilistic statement of SLAM
---

Full SLAM is the form of the [SLAM problem](/slam-problem/) that asks for the whole path of the robot and the map together, $p(x_{1:t}, m \mid z_{1:t}, u_{1:t})$, given all the data so far. It differs from [online SLAM](/online-slam/), which asks only for the current pose and the map, $p(x_t, m \mid z_{1:t}, u_{1:t})$, and integrates out each past pose as it goes. Full SLAM keeps every pose, so its state grows with time, but a new reading, such as a loop closure, can correct the whole past path, and the problem keeps a sparse structure. The general problem, with both forms, is on the [SLAM problem](/slam-problem/) page. Full SLAM is a [smoothing](/smoothing/) problem, and with Gaussian noise its most likely solution is a sparse [nonlinear least squares](/nonlinear-least-squares/) problem.

## In plain words

The robot keeps a record of every place it has been and every reading it has taken. Each wheel reading says how far it went between two places, and each sensor reading says where a landmark was seen from one place. These are like springs between the places and the landmarks. Full SLAM finds the positions that stretch all the springs as little as possible. When the robot comes back to a known place and sees a known landmark, the new spring pulls the whole chain into a better shape, and old places move too.

## Definition

**Input.** All the controls $u_{1:t}$ and readings $z_{1:t}$, the motion model $p(x_k \mid x_{k-1}, u_k)$, the measurement model $p(z_k \mid x_k, m)$, and a prior on the first pose, often $x_0 = 0$.

**Output.** The posterior $p(x_{1:t}, m \mid z_{1:t}, u_{1:t})$ over the path and the map, or its most likely value, the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/).

**The factorization.** By the Markov assumptions,

$$p(x_{1:t}, m \mid z_{1:t}, u_{1:t}) = \eta \, p(x_0) \prod_{k=1}^{t} p(x_k \mid x_{k-1}, u_k) \, p(z_k \mid x_k, m).$$

Each factor involves one pose and its predecessor, or one pose and the landmarks of one reading. This is a [factor graph](/factor-graph/).

**Least squares form.** If the motion is $x_k = g(x_{k-1}, u_k) + v_k$ with $v_k \sim N(0, Q_k)$ and a reading is $z_k = h(x_k, m) + w_k$ with $w_k \sim N(0, R_k)$, the negative log of the posterior is, up to a constant,

$$\sum_k \lVert x_k - g(x_{k-1}, u_k) \rVert^2_{Q_k^{-1}} + \sum_k \lVert z_k - h(x_k, m) \rVert^2_{R_k^{-1}},$$

plus the prior term, where $\lVert e \rVert^2_{A} = e^\top A e$. The maximum a posteriori path and map minimize this sum.

## Variants

- **Landmark SLAM and pose graph SLAM.** With landmarks, the map is part of the variables. In a [pose graph](/pose-graph/), the readings are first turned into relative pose constraints between poses, and the map is rebuilt from the optimized poses. See [pose graph optimization](/pose-graph-optimization/).
- **Batch and incremental.** A batch method solves the whole problem again. An incremental method, such as [iSAM](/isam/) or [iSAM2](/isam2/), updates the solution as new data arrive.
- **Visual full SLAM.** With cameras, full SLAM over keyframe poses and 3D points is [bundle adjustment](/bundle-adjustment/).
- **Robust forms.** Wrong data associations, such as false loop closures, are handled with robust costs or with [switchable constraints](/switchable-constraints/).

## Examples

**A loop closure on a line, by hand.** A robot starts at $x_0 = 0$. From there it reads a landmark $a$ at distance 3. It moves by 1 twice, by odometry, to $x_1$ and $x_2$. From $x_2$ it reads $a$ at distance 1.4. All four readings have variance 1. The constraints are

$$x_1 - x_0 = 1, \quad x_2 - x_1 = 1, \quad a - x_2 = 1.4, \quad a - x_0 = 3.$$

They do not agree: going round the loop $x_0 \to x_1 \to x_2 \to a$ gives $a = 3.4$, but the direct reading gives $a = 3$. Least squares spreads the gap of 0.4 equally over the four constraints of the loop, since they have the same variance, so each is off by 0.1:

$$x_1 = 0.9, \quad x_2 = 1.8, \quad a = 3.1.$$

Check: the information matrix over $(x_1, x_2, a)$ is $\begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}$ and the right side is $(1 - 1, \; 1 - 1.4, \; 3 + 1.4) = (0, -0.4, 4.4)$; the matrix times $(0.9, 1.8, 3.1)$ is $(0, -0.4, 4.4)$.

The past pose $x_1$ moved from 1.0, its value by odometry, to 0.9, because of a reading taken later at $x_2$. A filter for [online SLAM](/online-slam/) would have dropped $x_1$ before that reading came, and would report the same $x_2 = 1.8$ and $a = 3.1$, since the model is linear, but never the corrected $x_1$.

## Known algorithms

- **[GraphSLAM](/graphslam/).** Builds the information form of the least squares problem, removes the landmarks by a [Schur complement](/schur-complement/), and solves for the path.
- **[Square-root SAM](/square-root-sam/).** Solves the least squares problem by a sparse QR or Cholesky factorization.
- **[iSAM](/isam/) and [iSAM2](/isam2/).** Update the factorization incrementally as new data arrive.
- **[Pose graph optimization](/pose-graph-optimization/).** Gauss-Newton or Levenberg-Marquardt on the poses only. [SE-Sync](/se-sync/) solves a convex relaxation and certifies a global optimum when the relaxation is tight.
- **Particle filters over paths.** [FastSLAM](/fastslam/) and [grid-based RBPF SLAM](/grid-based-rbpf-slam/) represent the posterior over the full path by samples, and each sample carries its map.

## Bounds

- **Sparsity (theorem).** The information matrix of the least squares problem has a nonzero block only for pairs of variables that share a factor: consecutive poses, and a pose with the landmarks it read. So it has $O(t + K)$ nonzero blocks for $t$ poses and $K$ readings, not $O((t + m)^2)$.
- **Cost of a solve.** The cost of a sparse factorization depends on the order of elimination and the [fill-in](/fill-in/) it creates, not only on the number of variables. A good [elimination ordering](/elimination-ordering/), such as [nested dissection](/nested-dissection/) for a planar network of places, keeps the fill-in small. There is no general bound that is better than dense for every graph.
- **Nonconvexity.** With rotations in the poses, the least squares problem is nonconvex. Gauss-Newton or Levenberg-Marquardt can stop in a wrong local minimum from a bad start. SE-Sync can certify a global minimum when its relaxation is tight.
- **Same answer as online SLAM in the linear Gaussian case (theorem).** The marginal of the full Gaussian posterior on $(x_t, m)$ is the online posterior, as in the example above.

## Reductions

- **To nonlinear least squares.** With Gaussian noise, the maximum a posteriori path and map minimize the sum above; see [nonlinear least squares](/nonlinear-least-squares/).
- **To online SLAM.** Integrate out the past poses $x_{1:t-1}$.
- **To pose graph optimization.** Remove the landmarks, either by the Schur complement or by turning readings into relative pose constraints.
- **To mapping.** Given the path, building the map is mapping with known poses, as in [occupancy grid mapping](/occupancy-grid-mapping/).

## Applications

Most large SLAM systems solve full SLAM, or full SLAM over a set of keyframes, because it allows loop closures to correct the whole path: lidar mapping of buildings and cities, the maps used by self-driving cars, and visual SLAM systems such as [ORB-SLAM](/orb-slam/). Offline survey mapping, where all the data are known in advance, is a direct batch use.

## References
