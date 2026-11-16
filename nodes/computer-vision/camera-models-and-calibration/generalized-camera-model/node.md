---
tag: GWFY8A
kind: model
slug: generalized-camera-model
name: Generalized camera model
aliases:
- non-central camera
- Pless generalized camera
area: computer-vision/camera-models-and-calibration
level: research
summary: "Model a camera as a set of rays in space, one per pixel, written in Plucker coordinates. Rays need not meet in one point, so central cameras and multi-camera rigs are special cases."
prereqs: [pinhole-camera-model, essential-matrix]
see_also: [relative-pose-problem, perspective-n-point, minimal-solver, rolling-shutter-camera-model, unified-omnidirectional-camera-model, bundle-adjustment, visual-odometry, polynomial-system-solving]
sources:
  - paper: doi:10.1109/ICCV.2001.937611
    title: Michael D. Grossberg and Shree K. Nayar, A general imaging model and a method for finding its parameters, IEEE International Conference on Computer Vision, 2001, volume 2, 108-115
    locator: the model of a camera as a map from pixels to rays (raxels), and its calibration with structured light
  - paper: doi:10.1109/CVPR.2003.1211520
    title: Robert Pless, Using many cameras as one, IEEE Conference on Computer Vision and Pattern Recognition, 2003, 587-593
    locator: rays in Plucker coordinates, the generalized epipolar constraint, and the analysis of motion estimation for camera rigs
  - paper: doi:10.1109/CVPR.2004.1315081
    title: David Nister, A minimal solution to the generalised 3-point pose problem, IEEE Conference on Computer Vision and Pattern Recognition, 2004
    locator: absolute pose of a generalized camera from 3 rays and 3 known points, with at most 8 solutions
  - paper: "Henrik Stewenius, David Nister, Magnus Oskarsson and Kalle Astrom, Solutions to minimal generalized relative pose problems, Workshop on Omnidirectional Vision (OMNIVIS), 2005"
    title: Henrik Stewenius, David Nister, Magnus Oskarsson and Kalle Astrom, Solutions to minimal generalized relative pose problems, Workshop on Omnidirectional Vision (OMNIVIS), 2005
    locator: relative pose of a generalized camera from 6 ray matches, with up to 64 solutions
  - paper: doi:10.1109/CVPR.2008.4587545
    title: Hongdong Li, Richard Hartley and Jae-hak Kim, A linear approach to motion estimation using generalized camera models, IEEE Conference on Computer Vision and Pattern Recognition, 2008
    locator: the degeneracy of the plain linear solution of the generalized epipolar constraint for common camera rigs, and a linear method that avoids it
---

The generalized camera model drops the one assumption that all other camera models on this list share: that every ray passes through one center. A generalized camera is just a map from pixels to rays in space, and each ray can be anywhere. Grossberg and Nayar (2001) used this form to describe any imaging system, and Pless (2003) wrote the rays in Plucker coordinates, which turns two view geometry for such cameras into linear algebra. The model covers rigs of several cameras treated as one, cameras that look at a mirror from a point where it has no single viewpoint, push-broom sensors, and a [rolling shutter camera](/rolling-shutter-camera-model/) in motion. The [pinhole camera](/pinhole-camera-model/) and all other central cameras are the special case where all rays meet in one point.

## The machine

**Input.** A pixel index $i$ (a pixel of one of the cameras of a rig, for example).

**Output.** A ray in space, a line $L_i$ with a direction.

**Plucker coordinates.** A line through the point $p$ with direction $q$ is the pair $(q, q')$ with $q' = p \times q$. The moment $q'$ does not depend on which point $p$ of the line is used, and $q^{\mathsf T} q' = 0$. Two lines $(a, a')$ and $(b, b')$ meet (or are parallel) exactly when
$$a^{\mathsf T} b' + b^{\mathsf T} a' = 0 .$$

**Rigid motion.** If points move by $X_2 = R X_1 + t$, a line $(q, q')$ moves to $(R q, \; R q' + t \times R q)$.

**The machine as a table.** In the most general form, calibration stores one ray per pixel, with no formula at all. In practice the rays come from a few parts: a rig of $m$ central cameras gives each pixel the ray from the center $c_j$ of its camera $j$ along the direction $R_j K_j^{-1} \tilde x$, so $q = R_j K_j^{-1} \tilde x$ and $q' = c_j \times q$.

**Special classes.**
- Central: all rays pass through one point. With that point at the origin, $q' = 0$ for every ray.
- Axial: all rays meet one line, as in a stereo pair or a camera placed on the axis of a mirror of revolution but not at its special point.
- X-slit: all rays meet two lines.
- Non-central: no such structure.

## What it counts

The model counts only the geometry of rays: which ray each pixel sees. It says nothing about the image formation inside each camera, which is left to the central models of each part. Problems in the model are posed on rays: relative pose from matched rays, absolute pose from rays and known points, triangulation, and [bundle adjustment](/bundle-adjustment/), where the residual can be the distance from a point to its ray or the reprojection error in the camera that owns the pixel.

**Generalized epipolar constraint.** If a scene point lies on the ray $(q_1, q_1')$ seen at time 1 and on the ray $(q_2, q_2')$ seen at time 2, then the moved first ray meets the second ray, and the intersection test gives
$$q_2^{\mathsf T} E \, q_1 + q_2^{\mathsf T} R \, q_1' + q_2'^{\mathsf T} R \, q_1 = 0, \qquad E = [t]_\times R .$$
In block form this is
$$\begin{pmatrix} q_2 \\ q_2' \end{pmatrix}^{\mathsf T} \begin{pmatrix} E & R \\ R & 0 \end{pmatrix} \begin{pmatrix} q_1 \\ q_1' \end{pmatrix} = 0 .$$
For a central camera $q_1' = q_2' = 0$, and only $q_2^{\mathsf T} E q_1 = 0$ is left, the constraint of the [essential matrix](/essential-matrix/).

**Worked example.** Let $R = I$ and $t = (1, 0, 0)$, and let the point be $P_1 = (0, 0, 2)$ at time 1, so $P_2 = (1, 0, 2)$. At time 1 a camera with center $c = (0, 1, 0)$ sees it along $q_1 = P_1 - c = (0, -1, 2)$, and $q_1' = c \times q_1 = (2, 0, 0)$. At time 2 a camera at the origin sees it along $q_2 = (1, 0, 2)$ with $q_2' = 0$. Then $E q_1 = t \times q_1 = (0, -2, -1)$, so $q_2^{\mathsf T} E q_1 = -2$, and $q_2^{\mathsf T} q_1' = 2$. The sum is 0, as the constraint requires. With $t = (2, 0, 0)$ instead, the first term becomes $-4$ and the sum is $-2 \ne 0$. So, unlike for a central camera, the length of $t$ is visible in the data. A script also checked the constraint on random rays and motions, with residuals of about $10^{-16}$.

## Relation to other models

- **Central models.** The pinhole, [Brown-Conrady](/brown-conrady-distortion-model/), [Kannala-Brandt](/kannala-brandt-fisheye-model/) and [unified](/unified-omnidirectional-camera-model/) models all describe central cameras. The generalized model contains them as the case where all rays meet in one point, and then the [relative pose problem](/relative-pose-problem/) loses its scale.
- **Catadioptric cameras.** A mirror seen from a point other than the special one of Baker and Nayar gives a non central camera, with rays that touch a caustic surface instead of meeting in one point.
- **Rolling shutter.** A [rolling shutter camera](/rolling-shutter-camera-model/) that moves during the exposure has a different center for each row, so its image is a generalized camera image.
- **Multi-camera rigs.** A rig of calibrated cameras with known relative poses, for example on a car, is one generalized camera. Its motion is then one rigid motion with 6 degrees of freedom, scale included.

## Known results in the model

- **Generalized epipolar constraint (theorem).** As above, after Pless (2003). It is linear in the 18 entries of $E$ and $R$, so with 17 matches in general position a linear method finds them up to scale.
- **Degeneracy of the linear method (theorem).** Li, Hartley and Kim (2008) showed that this linear method is degenerate for several common rig configurations, so that the linear system has more than a one dimensional solution space, and they gave a linear method that avoids the problem.
- **Minimal relative pose (theorem).** The motion has 6 degrees of freedom and each ray match gives one equation, so 6 matches are minimal. Stewenius, Nister, Oskarsson and Astrom (2005) solved this case with at most 64 solutions, with a [minimal solver](/minimal-solver/) for a [polynomial system](/polynomial-system-solving/).
- **Minimal absolute pose (theorem).** For [perspective-n-point](/perspective-n-point/) with a generalized camera, 3 rays and 3 known points are minimal, and Nister (2004) showed there are at most 8 solutions, twice the at most 4 of the central P3P problem.
- **Metric scale (theorem).** For a non central camera, the translation is found with its length, as the example shows. If the rays are close to central, for example a rig with a short baseline compared with the scene depth, the scale is poorly conditioned in practice.
