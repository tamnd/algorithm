---
tag: Z0D3R7
kind: problem
slug: slam-problem
name: Simultaneous localization and mapping
aliases:
- SLAM
- concurrent mapping and localization
area: robotics/localization-and-slam
level: intro
summary: Build a map of an unknown environment and locate the robot in it at the same time, from motion and sensor data.
prereqs: [mobile-robot-localization, bayes-filter, robot-pose]
see_also: [online-slam, full-slam, data-association-slam, ekf-slam, fastslam, graphslam, pose-graph-optimization, occupancy-grid-mapping]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 10 (the SLAM problem, its online and full forms, and EKF SLAM), Chapter 11 (GraphSLAM), Chapter 12 (SEIF) and Chapter 13 (FastSLAM)"
  - paper: doi:10.1109/MRA.2006.1638022
    title: "Hugh Durrant-Whyte and Tim Bailey, Simultaneous localization and mapping, part I, IEEE Robotics and Automation Magazine 13(2), 2006, from page 99"
    locator: the statement of the problem, its probabilistic form and the history
  - paper: "Tim Bailey and Hugh Durrant-Whyte, Simultaneous localization and mapping (SLAM), part II, IEEE Robotics and Automation Magazine 13(3), 2006, pages 108 to 117"
    locator: the computational cost, data association and the representation of the environment
  - paper: doi:10.1177/027836498600500404
    title: "Randall C. Smith and Peter Cheeseman, On the representation and estimation of spatial uncertainty, International Journal of Robotics Research 5(4), 1986"
    locator: the representation of uncertain spatial relations by a mean and a covariance
  - paper: "M. W. M. Gamini Dissanayake, Paul Newman, Steven Clark, Hugh F. Durrant-Whyte and M. Csorba, A solution to the simultaneous localization and map building (SLAM) problem, IEEE Transactions on Robotics and Automation 17(3), 2001, pages 229 to 241"
    locator: Section III (the convergence of the map in the linear Gaussian case)
---

Simultaneous localization and mapping (SLAM) asks a robot that starts in an unknown place to build a map of it and, at the same time, find its own pose in that map, from its controls and its sensor readings only. This page is the general problem. It has two standard probabilistic forms, which have their own pages. [Online SLAM](/online-slam/) asks for the current pose and the map, $p(x_t, m \mid z_{1:t}, u_{1:t})$, and suits filters that run as the robot moves. [Full SLAM](/full-slam/) asks for the whole path and the map, $p(x_{1:t}, m \mid z_{1:t}, u_{1:t})$, and suits methods that optimize over all the data. The two halves of SLAM are simpler alone: [localization](/mobile-robot-localization/) with a known map, and [mapping with known poses](/occupancy-grid-mapping/). SLAM is hard because each half needs the answer of the other, and because the errors of the pose and of the map are correlated.

## In plain words

A robot is put in a building that it has never seen. It can count its wheel turns and it can see walls or marks around it, but both kinds of data have errors. It must draw a map and also say where it is on that map. If it knew where it was at every moment, drawing the map would be easy. If it had the map, finding itself would be easy. It has neither, so it must guess both together. A mistake in its position makes it draw the walls in the wrong place, and a wrong wall makes it place itself wrongly later. When the robot comes back to a place it has seen before and recognizes it, it can correct the errors that built up along the way.

## Definition

**Input.** A sequence of controls $u_{1:t}$, such as odometry readings, and a sequence of sensor readings $z_{1:t}$, such as laser scans, camera images or ranges and bearings to landmarks. A motion model $p(x_k \mid x_{k-1}, u_k)$ and a measurement model $p(z_k \mid x_k, m)$ describe the noise. The pose $x_0$ at the start defines the frame of the map, often $x_0 = 0$.

**Output.** An estimate of the map $m$ and of the robot pose, with its uncertainty. A planar [pose](/robot-pose/) is $(x, y, \theta)$. The map can be a list of landmark positions, an [occupancy grid](/occupancy-grid-map/), a set of points or a graph of places.

**The question.** In the probabilistic form, compute the posterior over the pose and the map given all the data. The online form keeps only the current pose, $p(x_t, m \mid z_{1:t}, u_{1:t})$. The full form keeps the whole path, $p(x_{1:t}, m \mid z_{1:t}, u_{1:t})$. The online posterior is the full posterior with the past poses integrated out.

**Correspondence.** A reading of a landmark does not always say which landmark it is. Deciding this is [data association](/data-association-slam/), a part of SLAM that is often harder than the estimation itself.

## Variants

- **Online and full.** See [online SLAM](/online-slam/) and [full SLAM](/full-slam/).
- **Map types.** Landmark maps, where the map is a vector of feature positions. Dense maps, such as occupancy grids or point clouds. Topological maps, a graph of places, see [topological map](/topological-map/).
- **Known or unknown correspondences.** With known correspondences each reading comes with the identity of its landmark. Without them, data association is part of the problem.
- **Sensors.** Laser or lidar SLAM, visual SLAM with one camera, as in [MonoSLAM](/monoslam/), or with several cameras, and SLAM with an inertial sensor.
- **Several robots.** [Multi-robot SLAM](/multi-robot-slam/) adds the unknown relative poses of the robots and the merging of maps.

## Examples

**A 1D world, by hand.** A robot moves on a line. It starts at $x_0 = 0$, known exactly. One landmark is at an unknown position $m$. The reading is $z = m - x + w$ with noise variance 1, and the motion is $x_1 = x_0 + u_1 + v$ with noise variance 1.

1. At $x_0$ the robot reads $z_0 = 5$. So $m \sim N(5, 1)$, and the map does not depend on the pose yet.
2. It moves with $u_1 = 2$, so $x_1 \sim N(2, 1)$, independent of $m$.
3. It reads $z_1 = 3.6$. The predicted reading is $5 - 2 = 3$, the innovation is $0.6$, and its variance is $1 + 1 + 1 = 3$. The covariance of the reading with $x_1$ is $-1$ and with $m$ is $+1$, so the Kalman gains are $-1/3$ and $+1/3$.
4. The new estimates are $x_1 = 2 - 0.2 = 1.8$ and $m = 5 + 0.2 = 5.2$. The variances are $1 - 1/3 = 2/3$ each, and the covariance of $x_1$ and $m$ is now $+1/3$, a correlation of $0.5$.

The last line is the heart of SLAM. The reading measures only the difference $m - x_1$, so it ties the errors of the pose and the map together: if the robot is in truth further than it thinks, the landmark is too. A method that keeps the pose and the map as two separate estimates, without this correlation, throws away information and becomes overconfident.

## Known algorithms

- **Filters for the online form.** [EKF SLAM](/ekf-slam/) keeps one Gaussian over the pose and all landmarks, at a cost of $O(m^2)$ per update for $m$ landmarks. The [extended information filter](/extended-information-filter/) and the [sparse extended information filter](/sparse-extended-information-filter/) work with the inverse covariance. [MonoSLAM](/monoslam/) is EKF SLAM with one camera.
- **Particle filters.** [FastSLAM](/fastslam/) samples paths and keeps one small filter per landmark, at $O(N \log m)$ per step with $N$ particles and a balanced tree. [Grid-based RBPF SLAM](/grid-based-rbpf-slam/) does the same with one grid per particle.
- **Optimization for the full form.** [GraphSLAM](/graphslam/), [square-root SAM](/square-root-sam/), [iSAM](/isam/) and [iSAM2](/isam2/) solve the full problem as sparse nonlinear least squares. [Pose graph optimization](/pose-graph-optimization/) keeps only the poses.
- **Systems.** [ORB-SLAM](/orb-slam/) and [lidar odometry and mapping](/lidar-odometry-and-mapping/) combine tracking, mapping and [loop closure detection](/loop-closure-detection/).

## Bounds

SLAM is an estimation problem, not a decision problem, so the usual bounds are on cost and memory, not on a complexity class.

- **Dense correlations (theorem).** In the linear Gaussian case, the [EKF SLAM convergence theorem](/ekf-slam-convergence-theorem/) of Dissanayake et al. (2001) shows that the landmark estimates become fully correlated in the limit. So an exact Gaussian over the pose and the map needs $\Theta(m^2)$ numbers, and EKF SLAM pays $O(m^2)$ per update.
- **A floor on the map uncertainty (theorem).** In the same setting, the uncertainty of each landmark never drops below the uncertainty of the robot when it first saw a landmark. The data measure only relative positions, so they cannot fix the map in the world better than the start pose does.
- **Sparse structure.** In the full form, the information matrix has one nonzero block per motion step and per reading, so it is sparse. The cost of solving it depends on the variable ordering and the fill-in; see [elimination ordering](/elimination-ordering/).
- **Nonconvexity.** With rotations, full SLAM is a nonconvex least squares problem, and local methods can stop in a wrong local minimum.

## Reductions

- **To localization.** If the map is known, SLAM becomes [mobile robot localization](/mobile-robot-localization/).
- **To mapping.** If the path is known, SLAM becomes mapping with known poses, such as [occupancy grid mapping](/occupancy-grid-mapping/). [FastSLAM](/fastslam/) and other [Rao-Blackwellized particle filters](/rao-blackwellized-particle-filter/) use exactly this: they sample paths and solve the mapping for each.
- **To least squares.** With Gaussian noise, the most likely path and map of full SLAM solve a [nonlinear least squares](/nonlinear-least-squares/) problem.
- **Online from full.** The online posterior is the full posterior with the past poses integrated out.

## Applications

Indoor service robots and warehouse robots build and use maps with SLAM. Self-driving cars use lidar and visual SLAM to build the maps in which they later localize. Augmented reality on phones and headsets tracks the camera with visual SLAM. Robots for mines, caves, underwater survey and planetary exploration use it where no satellite positioning works.

## References
