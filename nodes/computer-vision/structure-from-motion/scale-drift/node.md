---
tag: V2XG7H
kind: concept
slug: scale-drift
name: Scale drift
aliases:
- monocular scale ambiguity
area: computer-vision/structure-from-motion
level: advanced
summary: A single camera fixes motion only up to scale, and the scale estimate wanders over a long trajectory unless loop closure, stereo or inertia fixes it.
prereqs: [visual-odometry]
see_also: [gauge-freedom, nister-visual-odometry, direct-sparse-odometry, semi-direct-visual-odometry, loop-closure-detection, orb-slam, pose-graph-optimization, bundle-adjustment]
sources:
  - paper: "Hauke Strasdat, J. M. M. Montiel and Andrew J. Davison, Scale drift-aware large scale monocular SLAM, Robotics: Science and Systems (RSS), 2010"
    locator: "the analysis of scale drift in monocular SLAM and the pose graph optimization over similarity transformations (7 degrees of freedom) that corrects it at loop closures"
  - paper: doi:10.1109/MRA.2011.943233
    title: "Davide Scaramuzza and Friedrich Fraundorfer, Visual odometry, Part I: the first 30 years and fundamentals, IEEE Robotics and Automation Magazine 18(4), 2011, 80-92"
    locator: "the monocular case, where the relative scale of each new motion must be computed from triangulated points"
  - paper: doi:10.1109/TRO.2015.2463671
    title: "Raul Mur-Artal, J. M. M. Montiel and Juan D. Tardos, ORB-SLAM: a versatile and accurate monocular SLAM system, IEEE Transactions on Robotics 31(5), 2015, 1147-1163"
    locator: "the loop closing, which computes a similarity transformation and corrects the scale drift in a pose graph"
---

## In plain words

One camera cannot measure size. A photo of a toy car close by can look the same as a photo of a real car far away. So a single moving camera can find the shape of its path, but not how long it is: a path of 1 meter and a path of 10 meters can give the same pictures. A method picks a scale at the start. Later frames get their scale from points seen before, and each time a little error enters. Over a long path these small errors multiply, and the scale wanders. The far end of the path can be too small or too large, even if every single step looks right.

## The idea

**The ambiguity (a theorem).** Let a scene with points $X_i$ be seen by calibrated cameras with poses $(R_k, t_k)$, so $X_c = R_k X + t_k$. For any $s > 0$, the scene $s X_i$ with poses $(R_k, s t_k)$ gives the same normalized image points, because $R_k (s X_i) + s t_k = s (R_k X_i + t_k)$ and the projection divides by depth. So images alone determine the scene and the path only up to a similarity: a rotation, a translation and a scale, 7 degrees of freedom in all. Fixing the first pose removes 6; the scale is left (see [gauge freedom](/gauge-freedom/)). A monocular method fixes it by a choice, for example by setting the length of the first translation to 1 or by giving the depths of the first points.

**How the scale is passed on.** After the start, [visual odometry](/visual-odometry/) passes the scale from frame to frame through the 3D points it shares. A new relative motion from two images has an unknown length; it is scaled so that the points triangulated from it agree with the points already in the map, or the new pose is found with [perspective-n-point](/perspective-n-point/) against those points. Either way, the new scale is only as good as the depths of the shared points. If those depths are all 2 percent too large, the new part of the path is 2 percent too large.

**Why it drifts (a theorem for a simple model).** Let the scale factor passed on at step $k$ be $1 + \varepsilon_k$ with small independent errors $\varepsilon_k$ of mean 0 and variance $\sigma^2$. Then the scale after $n$ steps is $s_n = \prod_{k=1}^{n} (1 + \varepsilon_k)$, and $\log s_n \approx \sum_k \varepsilon_k$ is a random walk with standard deviation about $\sigma \sqrt{n}$. The error is multiplicative and has no restoring force, so nothing brings the scale back. Real errors are not independent: few points, short baselines and points far away give larger $\varepsilon_k$, and the errors of neighboring steps are correlated. The random walk is a model, not a measurement.

**Why the scale is weaker than the rest.** The rotation is measured in each image pair from the directions of the rays, so its error stays small for each step. The scale has no direct measurement at all: it comes only from the chain of shared points. Points far away give little depth information, so a camera that moves through open space with far points has worse scale drift than one in a room.

**What fixes it.**
- **Another sensor.** A stereo pair has a known baseline, and an inertial sensor measures acceleration in meters per second squared. Both make the scale observable, and the drift of the scale then stays bounded in the same way as the other errors.
- **Loop closure with a similarity.** When the camera comes back to a known place, the loop constraint gives the scale error around the loop. A pose graph whose edges are similarity transformations (rotation, translation and scale) can spread the correction along the loop. Strasdat, Montiel and Davison showed that a pose graph with only rigid edges cannot correct the scale drift, and that edges with 7 degrees of freedom can. See [loop closure detection](/loop-closure-detection/) and [pose graph optimization](/pose-graph-optimization/).
- **Windowed optimization.** [Bundle adjustment](/bundle-adjustment/) over a window of keyframes uses all shared points at once, so the scale of the window rests on more points than one pair. This reduces the size of each $\varepsilon_k$; it does not stop the drift.
- **Known sizes.** A known object size, the known height of the camera over a flat ground, or a known speed fixes the scale where it is seen.

## Examples

**Same images, different scale.** A camera at the origin and a camera at $(1, 0, 0)$, both with $R = I$, see the point $(0, 0, 5)$ at the normalized points $(0, 0)$ and $(-0.2, 0)$. A camera at the origin and a camera at $(2, 0, 0)$ see the point $(0, 0, 10)$ at $(0, 0)$ and $(-0.2, 0)$. The images are the same, so no method can choose between the two.

**A chain of scale errors.** A path has 10 legs of true length 1. The first leg is given the length 1. Each later leg gets its scale from points of the leg before, with depths that are 2 percent too large. Then leg $k$ has length $1.02^{k-1}$, and the last leg has length $1.02^9 = 1.195$. The total length is $\sum_{k=0}^{9} 1.02^k = (1.02^{10} - 1)/0.02 = 10.95$ instead of 10. If the errors alternate between $+2$ and $-2$ percent, the scale stays between $1$ and $1.02$: the drift depends on how the errors add up, not on their size alone.

**A random walk of the scale.** With independent errors of 1 percent per step ($\sigma = 0.01$), after 100 steps the standard deviation of $\log s$ is about $0.01 \cdot 10 = 0.1$. A scale that is off by a factor $e^{0.1} = 1.105$ is a typical result, and factors of $1.2$ are not rare. After 10000 steps, the typical factor is $e^{1} = 2.7$.

## Where it is used

- **Monocular visual odometry and SLAM.** [Nister visual odometry](/nister-visual-odometry/), [direct sparse odometry](/direct-sparse-odometry/) and [semi-direct visual odometry](/semi-direct-visual-odometry/) all fix the scale at the start and carry it along, so they all have scale drift. Their windowed optimizations reduce it.
- **Loop closing in monocular SLAM.** [ORB-SLAM](/orb-slam/) computes a similarity transformation at each loop closure and corrects the path with a pose graph, following the idea of Strasdat, Montiel and Davison.
- **Evaluation.** Monocular methods are compared with the ground truth after an alignment by a similarity, which removes the global scale but not the drift within the path.
- **Sensor design.** The size of the scale drift of a monocular system is one reason to add a stereo camera or an inertial sensor.

## References
