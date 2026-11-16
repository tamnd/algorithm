---
tag: HXRXPQ
kind: algorithm
slug: monoslam
name: MonoSLAM
aliases:
- Davison monocular SLAM
area: robotics/localization-and-slam
level: advanced
summary: Davison's real-time EKF SLAM with one camera, a sparse map of image patch landmarks and a constant velocity motion model.
solves: [online-slam]
model: real-ram
complexity:
  vars: {m: the number of features in the map, k: the number of features measured in one frame}
  time: {frame: O(k m^2)}
  space: {extra: O(m^2)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 2003
  people: [Andrew Davison, Ian Reid, Nicholas Molton, Olivier Stasse]
  note: Davison showed real-time SLAM with a single camera in 2003. The 2007 paper with Reid, Molton and Stasse describes the full system and its use for augmented reality and on a humanoid robot.
prereqs: [ekf-slam, extended-kalman-filter, pinhole-camera-model]
see_also: [visual-odometry, bundle-adjustment, orb-slam, ekf-slam, shi-tomasi-corner-detector, normalized-cross-correlation, epipolar-geometry, keyframe-selection]
sources:
  - paper: "Andrew J. Davison, Ian D. Reid, Nicholas D. Molton and Olivier Stasse, MonoSLAM: Real-time single camera SLAM, IEEE Transactions on Pattern Analysis and Machine Intelligence 29(6), 2007, pages 1052 to 1067"
    locator: "Section 3 (the state, the constant velocity model, active search, the particle initialization of new features and the map management), Section 4 (augmented reality) and Section 5 (the humanoid robot)"
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 10 (EKF SLAM, the filter that MonoSLAM uses)"
---

MonoSLAM estimates the 3D motion of a single hand-held or robot-mounted camera and a sparse map of 3D points, in real time, from the images alone. It is [EKF SLAM](/ekf-slam/) with a camera as the only sensor: one extended Kalman filter holds the camera pose and velocity and all the map points, each frame is a prediction by a constant velocity model and an update with the image positions of a few points. It differs from [visual odometry](/visual-odometry/), which estimates the motion from frame to frame and keeps no lasting map, so its error grows without bound even when the camera returns to a place it has seen. It also differs from [bundle adjustment](/bundle-adjustment/), which optimizes all cameras and points together by nonlinear least squares. MonoSLAM never revisits old frames: it keeps one Gaussian over the present state and the map, and pays for the map with a cost that grows with the square of its size. Davison, Reid, Molton and Stasse (2007) ran it at 30 frames per second with about 12 visible features.

## In plain words

A person walks around a room with a single camera. The program keeps a small list of distinct image patches, such as corners of objects, and a guess of where each is in 3D. It also keeps a guess of where the camera is and how fast it moves. For each new image, it predicts where the camera is now and where each patch should appear. It looks for each patch only in a small area around that prediction, which is fast. The positions where it finds the patches correct both the camera and the patches. A new patch at first has an unknown distance, so the program tries many distances along its line of sight and keeps the ones that fit the next images.

## The problem

The input is a video from one calibrated camera, with no odometry. The output, at every frame, is the camera pose and a map of 3D points with their uncertainty. This is [online SLAM](/online-slam/) with a bearing-only sensor: one image point gives the direction to a map point but not its distance, so the depth of a new point is unknown, and with one camera the overall scale of the map and the motion cannot be found from the images alone. MonoSLAM fixes the scale at the start with a known target of about four features in front of the camera.

The state is the camera position $r$, its orientation as a unit quaternion $q$, its velocity $v$ and angular velocity $\omega$ (13 numbers), and three coordinates for each map point. The [pinhole camera model](/pinhole-camera-model/), with the radial distortion of the lens, maps a point to its image position.

## The algorithm

```pseudo id=main
MONOSLAM_FRAME(μ, Σ, image I_t, Δt)
L1  r ← r + v Δt;  q ← q ⊗ quat(ω Δt);  Σ ← F Σ Fᵀ + G Q Gᵀ     ▷ v, ω keep their mean; Q is the noise of V, Ω
L2  for each map point i that should be in view do
L3      ẑ_i ← project(r, q, y_i);  H_i ← ∂ẑ_i/∂(state);  S_i ← H_i Σ H_iᵀ + R
L4      search for the stored patch of point i by normalized cross-correlation, only inside the ellipse of S_i
L5  EKF update of μ and Σ with all matched points
L6  for each new point that is still a ray: weight its depth samples; if the spread is small, make it a 3D point
L7  if too few points are visible then start a new corner as a ray with depth samples from 0.5 m to 5 m
L8  delete points that often fail to match;  return μ, Σ
```

**The motion model.** The camera has no odometry, so the filter assumes that the velocity and the angular velocity stay the same, with an unknown random change in each frame. This "constant velocity, constant angular velocity" model with Gaussian accelerations lets the filter follow smooth hand motion. A sudden jerk larger than the noise allows makes the prediction wrong and the search regions miss.

**Active search (line L4).** The innovation covariance $S_i$ gives an ellipse in the image where the patch must be with high probability. Searching only there, by [normalized cross-correlation](/normalized-cross-correlation/) of the stored $11 \times 11$ pixel patch, keeps the image work small and avoids many false matches. The size of the ellipse also tells which points are most useful to measure.

**New points (lines L6 and L7).** A new point is found by the [Shi-Tomasi corner detector](/shi-tomasi-corner-detector/). Its depth is unknown, so it starts as a line in 3D with 100 depth samples spread uniformly from 0.5 m to 5 m. As the camera moves, the line projects to a line in the next images, along which the patch is searched; the samples that fit get more weight. When the ratio of the standard deviation of the depth to its mean drops below 0.3, the point becomes a normal 3D map point with a Gaussian. The later inverse depth form of Civera, Davison and Montiel lets a new point enter the filter at once.

**The code is a toy.** The Python file keeps the filter structure of lines L1 to L8 in a plane: the camera is $(x, y, \theta)$ with its velocities, the image has one coordinate, and there is no image processing, so a "detection" is a pixel with the id of its true point. It applies the matched points one at a time, which for a linear model gives the same result as one joint update. In a simulated run, a camera that moves 1.5 m to the side and speeds up from 0.3 m/s to 0.7 m/s ends within 5 cm of the true position on three seeds, while the prediction alone ends more than 0.5 m off. This is a measurement of the toy, not of MonoSLAM.

## Example

**The prediction.** At 30 frames per second, $\Delta t = 1/30$ s. A camera at the origin that moves with $v = (0.3, 0, 0)$ m/s is predicted at $r = (0.01, 0, 0)$ m in the next frame. If the random acceleration has a standard deviation of $4$ m/s², the velocity can change by $4 / 30 = 0.13$ m/s in one frame, and the position by about $0.13 / 30 = 0.004$ m more. These numbers are an example, not the values of the paper.

**The depth of a new point.** At the start, the 100 depth samples are uniform on $[0.5, 5]$ m: the mean is 2.75 m and the standard deviation is $4.5 / \sqrt{12} = 1.30$ m, a ratio of 0.47. After a few frames, suppose the samples that keep their weight are spread uniformly on $[1.5, 2.5]$ m. The mean is 2.0 m and the standard deviation is $1 / \sqrt{12} = 0.29$ m, a ratio of 0.14, below 0.3. The point now enters the map as a 3D point at depth 2.0 m along its ray.

## Correctness

MonoSLAM is an extended Kalman filter, so it has the properties of [EKF SLAM](/ekf-slam/), and no more. If the models were linear and Gaussian, the filter would give the exact posterior. They are not: the projection is nonlinear, and so is the quaternion motion. So the filter is a local approximation that works when the errors stay small compared with the curvature of the models, which the high frame rate helps with. Like nonlinear EKF SLAM, it can become inconsistent, that is, more confident than its errors justify. The scale of the map comes only from the known target at the start; after that it is held by the correlations in the filter and drifts slowly. These are measured properties of the system, not theorems. The paper reports its accuracy from experiments, such as the augmented reality results of its Section 4 and the humanoid robot runs of its Section 5.

## Complexity

- **Per frame:** $O(k m^2)$ for the EKF update with $k$ measured points and $m$ map points, as in EKF SLAM, plus the image work of the active search, which grows with the area of the search ellipses.
- **The prediction:** only the 13 camera rows and columns of the covariance change, $O(m)$.
- **Memory:** $O(m^2)$ for the covariance.

The quadratic cost limits the map to a small number of points, enough for a room or a desk. This is the main limit of the method.

## Properties

- **Real time with one camera.** It was among the first systems to show SLAM with a single camera at frame rate, with no odometry and no other sensor.
- **A persistent map.** Unlike visual odometry, it keeps the points and recognizes them when the camera returns, so the error does not grow without bound in a small area.
- **Sparse map.** It keeps only the points that it needs to track the camera, not a dense model of the scene.
- **Small area.** The $O(m^2)$ cost and the size of the patches limit it to a room-sized space.

## Variants and improvements

- **Inverse depth.** Civera, Davison and Montiel parametrize a new point by its inverse depth along its first ray. The filter can then use it from the first frame, including points that are very far away.
- **Keyframe methods.** Later systems such as PTAM and [ORB-SLAM](/orb-slam/) track the camera against the map in each frame and refine the map by [bundle adjustment](/bundle-adjustment/) over selected keyframes in a separate thread. They handle much larger maps than an EKF over all points.
- **Submaps.** Splitting the map into small local filters bounds the cost per frame.

## When to use it

MonoSLAM shows the ideas of filter-based visual SLAM in a compact form: one state, active search and delayed initialization of the depth. For a new system, keyframe methods with bundle adjustment usually give better accuracy for the same computation, as shown by the later systems above. A small EKF over the camera and a few points is still a reasonable choice on a very small processor or when a covariance is needed at every frame.

## Pitfalls

- **Fast motion.** If the camera moves faster than the motion noise allows, the patches fall outside the search ellipses and tracking is lost.
- **A wrong match.** A single wrong match in the EKF update can pull the whole state far off. Gate the matches, and check that the set of matches agrees.
- **Unknown scale.** Without the known target, or another source of scale, the map has an arbitrary scale.
- **Large maps.** The cost grows as $m^2$; the filter slows down as the map grows.
- **Patches that change.** A patch seen from a new angle looks different. MonoSLAM warps the stored patch by the predicted view to reduce this.

## Implementations

## History

Davison showed real-time SLAM with a single camera in 2003, as an extended Kalman filter with a sparse map of image patches. The paper by Davison, Reid, Molton and Stasse in the IEEE Transactions on Pattern Analysis and Machine Intelligence in 2007 describes the full system: the constant velocity model, active search, the particle initialization of the depth and the map management, with applications to augmented reality and to a humanoid robot. Keyframe methods with bundle adjustment, starting with PTAM in 2007, later took over most of visual SLAM.

## References
