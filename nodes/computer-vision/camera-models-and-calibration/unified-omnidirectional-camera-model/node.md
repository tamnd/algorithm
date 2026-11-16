---
tag: CCWFX3
kind: model
slug: unified-omnidirectional-camera-model
name: Unified omnidirectional camera model
aliases:
- unified camera model
- Geyer-Daniilidis model
- Mei camera model
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "Model every central catadioptric camera as a projection onto a unit sphere followed by a perspective projection from a point on the sphere axis at distance xi from the center."
prereqs: [pinhole-camera-model, camera-intrinsic-matrix]
see_also: [kannala-brandt-fisheye-model, division-distortion-model, brown-conrady-distortion-model, generalized-camera-model, camera-calibration, visual-odometry, homogeneous-coordinates, reprojection-error]
sources:
  - paper: doi:10.1007/3-540-45053-X_29
    title: Christopher Geyer and Kostas Daniilidis, A unifying theory for central panoramic systems and practical implications, European Conference on Computer Vision, 2000, 445-461
    locator: the equivalence of central catadioptric projections to a projection onto a sphere followed by a projection from a point on its axis, and the images of lines as conics
  - paper: doi:10.1023/A:1008128724364
    title: Simon Baker and Shree K. Nayar, A theory of single-viewpoint catadioptric image formation, International Journal of Computer Vision 35(2), 1999, 175-196
    locator: the classification of mirror and camera pairs that have a single effective viewpoint
  - paper: doi:10.1109/ROBOT.2007.364084
    title: Christopher Mei and Patrick Rives, Single view point omnidirectional camera calibration from planar grids, IEEE International Conference on Robotics and Automation, 2007, 3945-3950
    locator: the unified model with added radial and tangential distortion, and its calibration from images of a planar grid
  - paper: doi:10.1109/3DV.2018.00069
    title: Vladyslav Usenko, Nikolaus Demmel and Daniel Cremers, The double sphere camera model, International Conference on 3D Vision, 2018, 552-560
    locator: the unified model and its extensions as fisheye models, with closed form projection and unprojection
---

The unified model describes a central omnidirectional camera in two steps: first project the scene point onto a unit sphere around the center of the camera, then project the point on the sphere into an image plane from a second center that lies on the axis of the sphere at distance $\xi$ from its middle. Geyer and Daniilidis (2000) showed that every central catadioptric camera, a camera that looks at a curved mirror and still has one effective viewpoint, fits this scheme, with $\xi$ fixed by the shape of the mirror. The case $\xi = 0$ is the [pinhole camera](/pinhole-camera-model/). The model has a closed form in both directions, and with $\xi$ close to 1 it also fits many fisheye lenses, which is why it is a common alternative to the [Kannala-Brandt model](/kannala-brandt-fisheye-model/) in calibration tools and in [visual odometry](/visual-odometry/).

## The machine

**Input.** A point $X_c = (X, Y, Z)$ in the camera frame (after the pose), the parameter $\xi \ge 0$, the [intrinsic matrix](/camera-intrinsic-matrix/) $K$, and optionally distortion parameters.

**Step 1: onto the sphere.** $X_s = X_c / \lVert X_c \rVert = (x_s, y_s, z_s)$.

**Step 2: shift the center.** Move the center of projection to the point $(0, 0, -\xi)$, which is the same as adding $\xi$ to the third coordinate: $(x_s, \; y_s, \; z_s + \xi)$.

**Step 3: perspective division.** $m = \left( \dfrac{x_s}{z_s + \xi}, \; \dfrac{y_s}{z_s + \xi} \right)$.

**Step 4: distortion (optional).** Lens distortion acts on normalized coordinates: project, distort, then apply $K$. Mei and Rives (2007) apply the [Brown-Conrady](/brown-conrady-distortion-model/) radial and tangential terms to $m$ here, to absorb the errors of a real mirror and lens.

**Step 5: apply K.** $(u, v, 1)^{\mathsf T} = K (m, 1)^{\mathsf T}$. The focal length in $K$ now combines the focal length of the camera and the shape of the mirror, so it is often called the generalized focal length.

**Inverse (lifting).** Given $m = (x, y)$ with $r^2 = x^2 + y^2$, let
$$\eta = \frac{\xi + \sqrt{1 + (1 - \xi^2) r^2}}{1 + r^2}.$$
Then $X_s = (\eta x, \; \eta y, \; \eta - \xi)$ is the unit vector of the ray. This is a closed form, unlike the inverse of the Kannala-Brandt or Brown-Conrady models.

**Domain.** The division in Step 3 needs $z_s + \xi > 0$. For $\xi \le 1$ the model is one to one on the rays with $z_s > -\xi$, so the field of view is $2 \arccos(-\xi)$; at $\xi = 1$ this is all rays except the one straight back. For $\xi > 1$ two rays can map to the same point, and the model is used only for $z_s > -1/\xi$; the lifting then needs $r^2 \le 1 / (\xi^2 - 1)$.

## What it counts

The model gives the pixel of each ray of a central camera with 5 intrinsic numbers ($f_x$, $f_y$, $c_x$, $c_y$, $\xi$), plus distortion terms if used. Calibration fits them by minimizing the [reprojection error](/reprojection-error/). The parameters $\xi$ and the focal length are strongly correlated, so a good start matters; Mei and Rives start from images of straight lines, which map to conics in this model.

**Worked example.** Let $\xi = 0.8$. A ray at angle $\theta$ to the optical axis has $x_s = \sin\theta$ (in its own vertical plane) and $z_s = \cos\theta$, so $\lVert m \rVert = \sin\theta / (\cos\theta + 0.8)$. For $\theta$ = 0, 45, 90, 120 and 140 degrees this gives 0, 0.4692, 1.25, 2.8868 and 18.93. A pinhole camera gives $\tan 45^\circ = 1$ at 45 degrees and infinity at 90 degrees. The largest angle is $\arccos(-0.8) = 143.13$ degrees, a field of view of 286 degrees. The lifting formula recovers each of these rays (checked with a script). For $\xi = 1.5$ the limit is $\arccos(-1/1.5) = 131.81$ degrees, and the image radius stops at $1 / \sqrt{\xi^2 - 1} = 0.8944$.

## Relation to other models

- **Pinhole.** $\xi = 0$ gives $m = (X / Z, Y / Z)$.
- **Catadioptric cameras.** Baker and Nayar (1999) listed the mirror and camera pairs with a single effective viewpoint: a plane, an ellipsoid or a hyperboloid of two sheets with a perspective camera at the right point, and a paraboloid with an orthographic camera (the cone and the sphere give only degenerate cases). Geyer and Daniilidis (2000) showed that the useful ones are all the sphere model: the parabolic mirror gives $\xi = 1$, the hyperbolic and elliptic mirrors give $0 < \xi < 1$, and the plane gives $\xi = 0$.
- **Division model.** For $\xi = 1$ the lifting is the ray $(2x, 2y, 1 - r^2)$, which is the [division model](/division-distortion-model/) with $\lambda = -1/4$ in coordinates scaled by 2. So the parabolic camera is a one parameter division model.
- **Fisheye models.** The model is not derived from fisheye optics, but with $\xi$ near 1 it fits many fisheye lenses fairly well. The extended unified model and the double sphere model of Usenko, Demmel and Cremers (2018) add one parameter to fit them better, and keep the closed form inverse. The [Kannala-Brandt model](/kannala-brandt-fisheye-model/) fits with a polynomial instead and needs iteration to invert.
- **Generalized camera.** All these models are central. A mirror seen from the wrong point gives a non central camera, which needs the [generalized camera model](/generalized-camera-model/).

## Known results in the model

- **Unifying theorem.** Geyer and Daniilidis (2000): every central catadioptric projection is equal to the two step sphere projection for some $\xi \in [0, 1]$, up to the affine map $K$.
- **Lines map to conics (theorem).** A scene line and the center span a plane through the center of the sphere, which cuts the sphere in a great circle. The projection of a circle on the sphere from a point is a conic. So in the image every line becomes a conic, and for $\xi = 1$ a circle, because the projection from a point of the sphere onto a plane is stereographic and maps circles to circles or lines.
- **Closed form both ways (theorem).** Projection and lifting are both closed forms with one square root, as above. This makes the model cheap in bundle adjustment and direct methods, where many points are projected and lifted in each step.
- **Degeneracy in calibration (heuristic).** With a narrow field of view, $\xi$ and the focal length cannot be separated well, because the model is then close to a pinhole with a different focal length. Calibration data should cover the edge of the image.
