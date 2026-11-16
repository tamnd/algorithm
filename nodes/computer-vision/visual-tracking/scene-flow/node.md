---
tag: 056XYG
kind: problem
slug: scene-flow
name: Scene flow
aliases:
- 3D motion field
area: computer-vision/visual-tracking
level: advanced
summary: Estimate the 3D motion vector of every visible surface point between two time steps, from stereo pairs, depth images or point clouds.
model: real-ram
complexity:
  vars: {W: the width of the reference image in pixels, H: the height of the reference image in pixels}
  time: {worst: Θ(W H)}
prereqs: [optical-flow, depth-from-disparity]
see_also: [stereo-matching, disparity, point-cloud-registration, iterative-closest-point, rigid-body-transformation, camera-projection-matrix, visual-odometry, depth-map-fusion]
sources:
  - paper: doi:10.1109/TPAMI.2005.63
    title: Sundar Vedula, Peter Rander, Robert Collins and Takeo Kanade, Three-dimensional scene flow, IEEE Transactions on Pattern Analysis and Machine Intelligence 27(3), 2005, 475 to 480
    locator: the whole paper (the definition of scene flow, its relation to the optical flow in several cameras, and its computation from flow and known geometry)
  - paper: doi:10.1109/CVPR.2015.7298925
    title: Moritz Menze and Andreas Geiger, Object scene flow for autonomous vehicles, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015, 3061 to 3070
    locator: the whole paper (scene flow from two stereo pairs with planar pieces that move rigidly with a few objects, and the scene flow benchmark of KITTI 2015)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, 2nd edition, Springer, 2022
    locator: the chapters on motion estimation and on depth estimation (optical flow, stereo and the combination of the two)
---

Scene flow is the three-dimensional motion of the visible surfaces of a scene. For each point of a reference image at time $t$, it asks for the vector that takes the surface point seen there to its position at time $t + 1$. [Optical flow](/optical-flow/) is the projection of this motion into one image, so it loses the motion along the viewing ray. Scene flow restores it with depth, from a stereo pair at each time, from depth images, from several calibrated cameras or from point clouds. With a stereo rig the output is often given in image terms: the [disparity](/disparity/) at time $t$, the optical flow, and the disparity at time $t + 1$ at the moved point. These four numbers per pixel give the 3D position and motion through [depth from disparity](/depth-from-disparity/). Vedula, Rander, Collins and Kanade defined the problem in 1999. It is used in driving, robots and the capture of moving people. Like optical flow, it is ill-posed without assumptions, because a point can be hidden at one of the times and a surface without texture does not show its motion.

## In plain words

Film a moving scene with two cameras side by side. Each pair of pictures tells how far away each spot is, and the next pair tells it again. Scene flow is the arrow, in real space, from where each spot was to where it is a moment later: left or right, up or down, and nearer or farther. One camera alone sees only the sideways part of the arrow, because a spot that moves straight toward the camera stays at the same place in the picture. Depth adds the part that one picture cannot show.

## Definition

**Input.** Two time steps $t$ and $t + 1$, each with one of the following: a rectified stereo pair with focal length $f$ and baseline $b$; a color image with a depth image; images from several calibrated cameras with [projection matrices](/camera-projection-matrix/) $P_j$; or a point cloud. One image of $W \times H$ pixels at time $t$ is the reference.

**Output.** For every reference pixel $(u, v)$ whose surface point $\mathbf X = (X, Y, Z)$ is visible at time $t$, the motion $\Delta \mathbf X = \mathbf X' - \mathbf X$, where $\mathbf X'$ is the position of the same material point at time $t + 1$. Pixels whose point is hidden at $t + 1$ may be marked, or given a motion that is only inferred.

**Stereo form.** In camera coordinates, with the principal point at the origin, a point has $u = f X / Z$, $v = f Y / Z$ and disparity $d = f b / Z$. The output can be written as the disparity $d$ at $(u, v)$, the optical flow $(\Delta u, \Delta v)$ and the disparity $d'$ at $(u + \Delta u, v + \Delta v)$ at time $t + 1$. Then

$$
\mathbf X = \frac{b}{d} (u, v, f), \qquad \mathbf X' = \frac{b}{d'} (u + \Delta u, v + \Delta v, f), \qquad \Delta \mathbf X = \mathbf X' - \mathbf X .
$$

**Relation to optical flow.** For a small motion, differentiate $u = f X / Z$:

$$
\dot u = f \Big( \frac{\dot X}{Z} - \frac{X \dot Z}{Z^2} \Big), \qquad \dot v = f \Big( \frac{\dot Y}{Z} - \frac{Y \dot Z}{Z^2} \Big).
$$

In one camera these are two linear equations in the three unknowns $(\dot X, \dot Y, \dot Z)$. The missing direction is the viewing ray: $\dot{\mathbf X} = s \mathbf X$ gives $\dot u = \dot v = 0$. Each further camera adds two equations, so two cameras in general position fix the motion, and more cameras give a [least-squares problem](/least-squares-problem/). This is the computation of Vedula and colleagues.

**Quality.** Benchmarks compare the disparities and the flow with ground truth per pixel. The KITTI 2015 benchmark of Menze and Geiger counts a pixel as wrong when an error is above both a fixed number of pixels and a fraction of the true value, separately for the disparity at each time and for the flow, and also reports the fraction of pixels that are wrong in any of them.

## Variants

- **Stereo scene flow.** Two stereo pairs, as above. This is the most studied form.
- **RGB-D scene flow.** A color image and a depth image at each time. The depth is given, so only the motion must be found.
- **Multi-view scene flow.** Many calibrated cameras around a scene, often with a reconstructed surface, as in the capture of moving people.
- **Point cloud scene flow.** Two point clouds, for example from a lidar, with no images. The points of the two clouds are different samples of the surface, so the motion is not a match of points.
- **Monocular scene flow.** One camera only. The depth must come from a learned model or from strong assumptions, and the scale of the scene is unknown.
- **Rigid and piecewise rigid scenes.** If the scene is one rigid body, scene flow is a [rigid-body transformation](/rigid-body-transformation/), and finding it is [visual odometry](/visual-odometry/) or [point cloud registration](/point-cloud-registration/). Most street scenes are a static background and a few rigid vehicles.

## Examples

**A point that moves.** Take $f = 500$ pixels and $b = 0.1$ m. The point $\mathbf X = (0.5, 0.2, 2.5)$ m projects to $(u, v) = (100, 40)$ with disparity $d = 50 / 2.5 = 20$. At time $t + 1$ it is at $\mathbf X' = (0.6, 0.2, 2.0)$, which projects to $(150, 50)$ with $d' = 25$. So the stereo form of the output is $d = 20$, flow $(50, 10)$ and $d' = 25$, and the formulas above return $\mathbf X = (0.1 / 20)(100, 40, 500) = (0.5, 0.2, 2.5)$, $\mathbf X' = (0.1 / 25)(150, 50, 500) = (0.6, 0.2, 2.0)$ and the scene flow $\Delta \mathbf X = (0.1, 0, -0.5)$.

**The linear model is first order.** The derivative formula with $\dot{\mathbf X} = (0.1, 0, -0.5)$ at $\mathbf X$ gives $\dot u = 500 (0.04 + 0.04) = 40$ and $\dot v = 500 (0 + 0.016) = 8$, against the true flow $(50, 10)$. The motion of 0.5 m is a fifth of the depth, and the linear model gives only 80 percent of the true flow. Methods that use it need small motions, or a scheme from coarse to fine.

**Motion along the viewing ray.** The point $(0.5, 0.2, 2.5)$ moves to $(0.6, 0.24, 3.0)$, away from the camera along its ray. It projects to $(100, 40)$ at both times, so the optical flow is 0. Only the disparity shows the motion: it changes from 20 to $16.\overline{6}$, and the scene flow is $(0.1, 0.04, 0.5)$.

**Depth error.** With $d = 20$ the depth is 2.5 m, and an error of 0.5 pixel in $d$ changes it by about $Z^2 / (f b) \cdot 0.5 = 0.0625$ m. The error in the motion along $Z$ adds the errors of $d$ and $d'$, so it is often larger than the motion of a slow object. Depth errors grow with $Z^2$, so scene flow far from the camera is mostly noise along $Z$.

## Known algorithms

| Approach | Input | Main idea |
|---|---|---|
| Flow in several views (Vedula and colleagues, 1999) | calibrated cameras and a surface | solve the linear equations of the optical flow in every camera by least squares |
| Variational stereo scene flow (Huguet and Devernay, 2007; Wedel and colleagues, 2008) | two stereo pairs | brightness constancy in all four images plus smoothness, solved from coarse to fine |
| Piecewise rigid scene flow (Vogel, Schindler and Roth; Menze and Geiger, 2015) | two stereo pairs | the scene is made of planar pieces, each moving with one of a few rigid motions |
| RGB-D scene flow | color and depth images | flow in the image and a fit of the depth change, often with rigid pieces |
| Point cloud methods | two point clouds | nearest neighbors or learned point features, with smoothness or rigid parts; [ICP](/iterative-closest-point/) for one rigid body |
| Learned methods | any of the above | a network predicts disparity and flow or 3D motion directly |

The [stereo matching](/stereo-matching/) and [optical flow](/optical-flow/) pages describe the two parts that most stereo methods combine.

## Bounds

- **Output size.** The output has one vector for each of the $W H$ reference pixels, so any method needs $\Omega(W H)$ time. Local methods with a fixed window and a fixed search range meet this up to the cost per pixel, which gives the bound $\Theta(W H)$ in the front matter for a fixed range. A search over $D$ disparities and $R$ flow vectors per pixel costs $\Theta(W H (D + R))$.
- **Not observable.** A pixel whose point is hidden at time $t + 1$ in every view has no measured motion. On a surface without texture, any motion that keeps the surface on itself gives the same images. In these regions the answer comes from the prior, such as smoothness or rigidity, and no method can do better than its prior.
- **One camera loses one dimension.** By the derivative formula, motion along the viewing ray gives no flow. So one camera without depth cannot recover scene flow, whatever the algorithm.

## Reductions

- **To stereo and optical flow.** Compute the disparity at both times and the optical flow of the reference camera, then combine them with the formulas of the definition. Errors in the three parts add, and occlusions must be handled in each.
- **To optical flow in several views.** With a known surface, scene flow is the least-squares solution of the flow equations of all cameras.
- **To registration.** If the scene is rigid, scene flow is one rigid motion, found by [point cloud registration](/point-cloud-registration/) or [visual odometry](/visual-odometry/). If it is piecewise rigid, it is a segmentation into parts plus one registration per part.
- **From depth fusion.** Systems that build a deforming model of a scene from depth images, in the style of [depth map fusion](/depth-map-fusion/), estimate a dense motion field as part of their work.

## Applications

- Driving: the motion of other vehicles, bicycles and people in 3D, for prediction and planning.
- Robots that act among moving objects or people.
- Capture of moving people and clothes from many cameras, and new views of dynamic scenes.
- Separation of moving objects from the static background for mapping.
- Training signals for learned depth and flow without labels, through the consistency of the two.

## References
