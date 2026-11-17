---
tag: NWSN9F
kind: definition
slug: point-cloud
name: Point cloud
aliases:
- 3D point cloud
- 3D point set
area: computer-vision/point-clouds-and-registration
level: intro
summary: "A finite set of 3D points sampled from surfaces, often with normals, colors or intensities, with no connectivity between the points. Laser scanners, depth cameras and stereo make them."
prereqs: []
see_also: [range-image, point-cloud-normal-estimation, voxel-grid-downsampling, statistical-outlier-removal, point-cloud-registration, surface-reconstruction, kd-tree, point-set-chamfer-distance]
sources:
  - paper: doi:10.1145/142920.134011
    title: "Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald and Werner Stuetzle, Surface reconstruction from unorganized points, Computer Graphics (Proceedings of SIGGRAPH 92) 26(2), 1992, 71-78"
    locator: "The unorganized point set as the input of surface reconstruction, and the tangent plane at each point from its nearest neighbors"
  - paper: doi:10.1109/ICRA.2011.5980567
    title: "Radu Bogdan Rusu and Steve Cousins, 3D is here: Point Cloud Library (PCL), IEEE International Conference on Robotics and Automation (ICRA), 2011"
    locator: "The Point Cloud Library, with the point cloud as its main data type, and an overview of its processing modules"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 13, 3D reconstruction (range scanning, range data merging and point-based representations)"
---

A point cloud is a finite set of points in 3D space, usually samples of the surfaces of a scene or an object, as measured by a laser scanner (lidar), a depth camera or [stereo matching](/stereo-matching/). Each point has three coordinates in the frame of the sensor, and it can carry more values, such as a surface normal, a color, an intensity or a time stamp. A point cloud has no connectivity: unlike a mesh, it does not say which points are neighbors on the surface. Neighbors must be found by a search, usually with a [k-d tree](/kd-tree/) or an [octree](/octree/). Point clouds are the input of normal estimation, downsampling, [registration](/point-cloud-registration/) and [surface reconstruction](/surface-reconstruction/).

## Definition

A **point cloud** is a finite set $P = \{p_1, \ldots, p_n\}$ with $p_i \in \mathbb{R}^3$. Each point can carry a vector of attributes $a_i$, so the cloud is the set of pairs $(p_i, a_i)$. Common attributes are a unit normal $\mathbf{n}_i$, a color, the intensity of the return, and the time of the measurement.

Two kinds are common.

- **Unorganized.** The points are a plain list. The order means nothing, and the neighbors of a point must be found by a spatial search. Hoppe et al. (1992) call such a set unorganized points.
- **Organized.** The points come in a grid of rows and columns, one per pixel of a sensor, as in a [range image](/range-image/). The neighbors in the grid are usually neighbors on the surface, except across edges of depth. Some cells have no valid point.

The coordinates are in the frame of the sensor. Clouds from different poses must be brought into one frame by [point cloud registration](/point-cloud-registration/) before they can be combined.

Real clouds have four properties that most methods must handle.

- **No order.** As a set, a point cloud does not change when its points are listed in another order. Methods that take a cloud as input should give the same result for every order.
- **Uneven density.** The density of points falls with the distance to the sensor and depends on the angle of the surface. Methods that assume an even density, such as fixed radius searches, can fail far from the sensor.
- **Noise and outliers.** Real points lie near the surface, not on it, and some are far from any surface. [Statistical outlier removal](/statistical-outlier-removal/) drops points whose neighbors are far away.
- **Holes.** Surfaces that the sensor cannot see, or that do not reflect, give no points.

## Examples and non-examples

- **A depth camera frame.** A pixel $(u, v)$ with depth $z$ gives the point $\big((u - c_x) z / f_x,\ (v - c_y) z / f_y,\ z\big)$, where $f_x, f_y, c_x, c_y$ are the entries of the [intrinsic matrix](/camera-intrinsic-matrix/). With $f_x = f_y = 500$, $(c_x, c_y) = (320, 240)$, the pixel $(400, 300)$ at depth $z = 2$ m gives the point $(0.32, 0.24, 2)$ m. A full frame is an organized cloud.
- **A lidar sweep.** A rotating lidar measures ranges along fixed angles. Each return gives a point, often with its intensity. The rows of beams make a partly organized cloud.
- **Structure from motion.** The triangulated feature points of [visual odometry](/visual-odometry/) or of [bundle adjustment](/bundle-adjustment/) form a sparse point cloud.
- **Not a mesh.** A triangle mesh has vertices that form a point set, but it also has faces that join them. A point cloud has no faces.
- **Not a voxel grid.** A voxel grid stores occupancy on a regular lattice of cells. A point cloud stores the measured positions themselves. [Voxel grid downsampling](/voxel-grid-downsampling/) maps a cloud to one point per occupied cell, which is again a point cloud.
- **Not a depth image by itself.** A depth image stores one number per pixel. It becomes an organized point cloud only with the intrinsic matrix, as in the first example.

## Related definitions

- A **normal** at a point is the normal of a plane fitted to its nearest neighbors, as in [point cloud normal estimation](/point-cloud-normal-estimation/); its sign needs [consistent normal orientation](/consistent-normal-orientation/).
- The **distance between two clouds** can be measured by the [Chamfer distance](/point-set-chamfer-distance/) or the [Hausdorff distance](/hausdorff-distance/).
- A **local descriptor** of a point, such as [point feature histograms](/point-feature-histograms/), [spin images](/spin-images/) or [SHOT](/shot-descriptor/), summarizes the shape of its neighborhood for matching.

## References
