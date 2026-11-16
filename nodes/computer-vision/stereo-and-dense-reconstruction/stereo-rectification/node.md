---
tag: K5RE9X
kind: algorithm
slug: stereo-rectification
name: Stereo rectification
aliases:
- epipolar rectification
- Loop-Zhang rectification
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Warp both images of a stereo pair by homographies so that epipolar lines become matching horizontal scanlines.
model: real-ram
complexity:
  vars: {W: the width of the output images in pixels, H: the height of the output images in pixels}
  time: {worst: Θ(W H), average: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1999
  people: [Richard Hartley, Charles Loop, Zhengyou Zhang, Andrea Fusiello, Emanuele Trucco, Alessandro Verri]
  note: Hartley (1999) and Loop and Zhang (1999) gave rectification from the fundamental matrix alone. Fusiello, Trucco and Verri (2000) gave the short method for calibrated cameras that this page implements.
prereqs: [epipolar-geometry, homography, camera-projection-matrix]
see_also: [fundamental-matrix, stereo-camera-calibration, disparity, depth-from-disparity, stereo-matching, image-warping, bilinear-interpolation, essential-matrix]
sources:
  - paper: doi:10.1007/s001380050003
    title: Andrea Fusiello, Emanuele Trucco and Alessandro Verri, A compact algorithm for rectification of stereo pairs, Machine Vision and Applications 12(1), 2000, 16-22
    locator: the whole paper (the new rotation from the baseline and the old optical axis, the common intrinsic matrix, and the rectifying transformations)
  - paper: doi:10.1023/A:1008115206617
    title: Richard I. Hartley, Theory and practice of projective rectification, International Journal of Computer Vision 35(2), 1999, 115-127
    locator: the whole paper (rectification from the fundamental matrix, the epipole mapped to infinity, and the matching homography)
  - paper: "Charles Loop and Zhengyou Zhang, Computing rectifying homographies for stereo vision, IEEE Conference on Computer Vision and Pattern Recognition, 1999, volume 1, 125-131 (also Microsoft Research technical report MSR-TR-99-21)"
    locator: the whole paper (the split of each homography into a projective, a similarity and a shearing part)
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 11.12, Image rectification; Section 9.3 for the fundamental matrix of a pure translation
  - paper: "Marc Pollefeys, Reinhard Koch and Luc Van Gool, A simple and efficient rectification method for general motion, IEEE International Conference on Computer Vision, 1999"
    locator: the whole paper (polar rectification, for an epipole inside the image)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (the section on epipolar geometry and rectification)
---

Stereo rectification turns the two images of a stereo pair into a new pair in which every [epipolar line](/epipolar-geometry/) is a horizontal pixel row, and the epipolar line of row $v$ in one image is row $v$ in the other. It does this by one [homography](/homography/) per image, which is the same as turning each camera about its center until both look in one direction, perpendicular to the baseline, with one shared intrinsic matrix. After rectification the search for a match is a search along one row, and the shift along the row is the [disparity](/disparity/), from which [depth](/depth-from-disparity/) follows by $Z = f b / d$. This page gives the method for calibrated cameras of Fusiello, Trucco and Verri (2000), which needs $K_1$, $K_2$ and the relative pose from [stereo calibration](/stereo-camera-calibration/). The methods of Hartley (1999) and of Loop and Zhang (1999) need only the [fundamental matrix](/fundamental-matrix/); they are under the variants below. The homographies cost $\Theta(1)$ to compute, and the warp of the images costs $\Theta(WH)$ on the [real RAM](/real-ram/).

## In plain words

Two cameras look at the same scene from two places. A point seen in the first photo can be anywhere on a certain line in the second photo, and in general this line is tilted. Matching is easier if that line is always a plain row of pixels, the same row as the point. Rectification makes this true. It turns both cameras in your mind, without moving them, so that both point the same way, the line between them is horizontal in their view, and they have the same lens. Then it redraws each photo as the turned camera would see it. Turning a camera about its center needs no knowledge of the scene, so each photo is redrawn by one fixed formula for all of its pixels.

## The problem

**Input.** Two cameras $P_i = K_i [R_i \mid t_i]$, $i = 1, 2$, with centers $C_i = -R_i^{\mathsf T} t_i$, and their images. A world point $X$ maps to the frame of camera $i$ by $R_i X + t_i$; the frame has $X$ to the right, $Y$ down and $Z$ forward. $K_i = [[f_x, s, c_x], [0, f_y, c_y], [0, 0, 1]]$ in pixels. The pixel $(u, v)$ has its center at the point $(u, v)$, with $u$ the column and $v$ the row. Lens distortion is removed first: it acts on normalized coordinates, so the image is undistorted before, or in the same inverse map as, the rectification.

**Output.** Two homographies $H_1$, $H_2$ and new cameras $P'_i = K_n R_n [I \mid -C_i]$ with one rotation $R_n$ and one intrinsic matrix $K_n$, such that $H_i x_i \sim P'_i X$ for every point $X$ with $x_i \sim P_i X$, and such that $P'_2$ sits at the baseline $b = \lVert C_2 - C_1 \rVert$ along the $+X$ axis of $P'_1$. Then a point has the same row $v$ in both new images, and its disparity is $d = u_1 - u_2 = f_x b / Z$, with $Z$ its depth in the new frame of camera 1. The fundamental matrix of the new pair is, up to scale,

$$F' = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix}, \qquad x_2^{\mathsf T} F' x_1 = v_1 - v_2 .$$

Here $x_2^{\mathsf T} F x_1 = 0$ is the convention with the point of the second image on the left, as in Hartley and Zisserman.

## The algorithm

```pseudo id=main
RECTIFY(K1, R1, t1, K2, R2, t2)
L1  C1 ← -R1ᵀ t1;  C2 ← -R2ᵀ t2             ▷ the camera centers, in the world frame
L2  b ← ‖C2 - C1‖;  if b = 0 then fail       ▷ no baseline
L3  r1 ← (C2 - C1) / b                       ▷ the new X axis, along the baseline
L4  y ← z1 × r1, with z1 the third row of R1;  if y = 0 then fail
L5  r2 ← y / ‖y‖;  r3 ← r1 × r2             ▷ the new Y and Z axes
L6  Rn ← the matrix with rows r1, r2, r3;  Kn ← a common K with zero skew
L7  H1 ← Kn Rn R1ᵀ K1⁻¹;  H2 ← Kn Rn R2ᵀ K2⁻¹
L8  return H1, H2, Kn, Rn, b
```

```pseudo id=warp
WARP(I, H, W, H')                            ▷ output of W columns and H' rows
L9  G ← H⁻¹
L10 for each output pixel (u, v) do
L11     (x, y, w) ← G (u, v, 1)
L12     J[v][u] ← I sampled at (x / w, y / w) by bilinear interpolation, or a fill value outside I
L13 return J
```

Lines L1 and L2 find the centers and the baseline. Line L3 makes the baseline the new $X$ axis, so the second camera is to the right of the first. Line L4 takes the old optical axis $z_1$ of camera 1 (the third row of $R_1$, written in the world frame) and makes the new $Y$ axis perpendicular to both $z_1$ and the baseline. If the cameras already point along $+Z$ and the baseline is along $+X$, then $z_1 \times r_1 = e_Z \times e_X = e_Y$, so $Y$ stays down. Line L5 completes a right-handed frame: $r_3$ is the part of $z_1$ that is perpendicular to the baseline, so the new cameras look roughly where camera 1 looked. Line L6 chooses $K_n$; Fusiello, Trucco and Verri take the mean of $K_1$ and $K_2$ with the skew set to zero, and so does the code. Line L7 is the map "undo $K_i$, undo $R_i$, apply $R_n$, apply $K_n$", a rotation of camera $i$ about its center. The warp of lines L9 to L13 uses the inverse map, so every output pixel gets exactly one value, and it samples with [bilinear interpolation](/bilinear-interpolation/), as in [image warping](/image-warping/).

## Example

Take $K = [[500, 0, 320], [0, 500, 240], [0, 0, 1]]$ for both cameras. Camera 1 is at the origin and turned by $0.05$ rad about its $Y$ axis, $R_1 = R_y(0.05)$. Camera 2 is at $C_2 = (0.1, 0.01, 0)$ m with $R_2 = R_y(-0.05)$, so the two cameras turn toward each other, and camera 2 is 1 cm lower than camera 1. Then $b = \sqrt{0.1^2 + 0.01^2} = 0.100499$ m, and lines L3 to L6 give

$$R_n \approx \begin{pmatrix} 0.995037 & 0.099504 & 0 \\ -0.099503 & 0.995025 & -0.004979 \\ -0.000495 & 0.004955 & 0.999988 \end{pmatrix}, \qquad K_n = K .$$

The first row is the baseline direction. The new image axes are turned by $\arctan(0.01/0.1) \approx 5.71°$ against the old ones, because the baseline is not level. Line L7 gives

$$H_1 \approx \begin{pmatrix} 1.02546 & 0.102675 & -58.0517 \\ -0.075875 & 0.997403 & 24.6062 \\ 9.897 \cdot 10^{-5} & 9.909 \cdot 10^{-6} & 0.964715 \end{pmatrix}, \quad H_2 \approx \begin{pmatrix} 0.961491 & 0.102675 & 12.1348 \\ -0.123356 & 0.997403 & 34.8154 \\ -1.0095 \cdot 10^{-4} & 9.909 \cdot 10^{-6} & 1.02864 \end{pmatrix}.$$

Two world points, before and after:

| point $X$ (m) | $x_1$ | $x_2$ | $H_1 x_1$ | $H_2 x_2$ | $d$ | $f b / Z$ |
|---|---|---|---|---|---|---|
| $(0.2, 0.1, 2.0)$ | $(395.398, 265.157)$ | $(319.979, 262.472)$ | $(372.230, 257.408)$ | $(347.110, 257.408)$ | $25.120$ | $25.120$ |
| $(-0.3, -0.2, 4.0)$ | $(307.568, 215.062)$ | $(244.602, 213.585)$ | $(280.190, 216.361)$ | $(267.624, 216.361)$ | $12.565$ | $12.565$ |

Before the warp the rows differ by about 2.7 and 1.5 pixels. After it they are equal, and the disparity matches $f b / Z$ with $Z = 2.00037$ and $3.99911$, the depths in the new frame. With $C_2 = (0.1, 0, 0)$, $R_1 = R_2 = I$ and the same $K$, both homographies are the identity: the pair is already rectified, and a point at depth $2.5$ m has $d = 500 \cdot 0.1 / 2.5 = 20$ pixels.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows that $R_n$ is a rotation with $R_n (C_2 - C_1) = (b, 0, 0)$, that $H_i x_i \sim P'_i X$ for every point seen by camera $i$, and that the two new cameras then give the same row and the disparity $f_x b / Z$ for each point with $Z \ne 0$. The key fact is that $K_n e_X = f_x e_X$ for an upper triangular $K_n$, so a shift of the camera center along $X$ changes only the first image coordinate. The proof also shows that line L4 fails exactly when the baseline is parallel to the optical axis of camera 1, and it derives $F'$.

## Complexity

- Lines L1 to L8 work on $3 \times 3$ matrices: a fixed number of arithmetic operations and one square root per norm, so $\Theta(1)$ on the [real RAM](/real-ram/), independent of the image.
- The warp computes one $3 \times 3$ product, one division and one bilinear sample of four pixels per output pixel, so it costs $\Theta(WH)$ for an output of $W \times H$ pixels, in the best and the worst case. The output image takes $\Theta(WH)$ space.

A real system often combines undistortion and rectification in one lookup table of source positions, built once per camera pair. Then each new frame costs one table read and one interpolation per pixel.

## Properties

- **Rotation only.** Each $H_i$ is $K_n R K_i^{-1}$ with a rotation $R = R_n R_i^{\mathsf T}$. So it is exact for every scene, at every depth, and needs no knowledge of the scene.
- **Not unique.** Any rotation of both new cameras about the baseline, and any common change of $f$, $c_x$ (the same for both) and $c_y$, keeps the rows matched. The choice of $r_2$ from $z_1$ is one choice; others reduce the distortion.
- **Disparity offset.** If the two new cameras use different $c_x$, all disparities shift by $c_{x1} - c_{x2}$, so $d = f b / Z + (c_{x1} - c_{x2})$. The Middlebury data sets give this offset as a separate number.
- **Direction of the baseline.** If camera 2 is to the left of camera 1, line L3 points the new $X$ axis to the left, and the new images are the old ones turned by about $180°$. The disparities are still positive, but most programs then swap the two images instead.

## Variants and improvements

- **Uncalibrated rectification (Hartley 1999).** Find a homography $H_2$ that maps the epipole $e_2$ to the point at infinity $(1, 0, 0)$ and is close to a rigid motion near the image center. Then choose $H_1$ among the homographies that match the epipolar lines, by the linear least squares problem that makes the matched points as close as possible in $u$. It needs only the fundamental matrix and point matches, and the result is defined up to a projective change of the scene.
- **Loop and Zhang (1999).** Split each homography into a projective part, a similarity and a shear. Choose the projective part to make the images as close to affine as possible, and the shear to keep the right angles and the aspect ratio of the image.
- **Polar rectification (Pollefeys, Koch and Van Gool 1999).** When the epipole is inside an image, as for a camera that moves forward, no homography maps it to infinity without tearing the image. Polar rectification resamples the image along the epipolar lines around the epipole instead.
- **OpenCV's stereoRectify.** It splits the relative rotation into two halves, one for each camera, and then turns both to the baseline. It also has a free scaling parameter that trades the valid pixels against the black border.

## When to use it

Use rectification before any dense [stereo matching](/stereo-matching/) on two images: [block matching](/block-matching-stereo/), [semi-global matching](/semi-global-matching/) and the other methods in this group assume rectified input and search along rows. Use the calibrated method when $K_1$, $K_2$ and the pose are known, which gives depths in meters. Use the uncalibrated methods when only matches between the images are available. Skip rectification when there are more than two views; [plane sweep stereo](/plane-sweep-stereo/) and [PatchMatch stereo](/patchmatch-stereo/) handle general camera positions without it.

## Pitfalls

- **Forward motion.** If the baseline is close to the optical axis, line L4 divides by a small $\lVert y \rVert$, and the homographies send parts of the image to infinity. Test the angle between $z_1$ and the baseline, and use polar rectification when the epipole is inside or near the image.
- **Forward mapping.** Pushing each source pixel through $H_i$ leaves holes and overlaps in the output. Line L9 inverts $H_i$ and pulls one value per output pixel.
- **Distortion left in.** A radial distortion of one pixel at the border bends the epipolar lines by about one pixel, and a matcher that searches one row then finds wrong matches. Undistort first.
- **Different $K$ rows.** If $K_n$ differs between the two images in $f_y$ or $c_y$, the rows no longer match. Line L6 uses one $K_n$ for both; only $c_x$ may differ, and then the disparities shift by a constant.
- **Lost pixels.** The new images can be larger or smaller than the old ones. Choose the output size and $c_x$, $c_y$ so that the useful part of both images is inside, or many pixels of the far side of the image fall out.
- **Transposed $F$.** Some libraries write $x_1^{\mathsf T} F x_2 = 0$. Their rectified $F$ is the transpose of $F'$ above, with the opposite sign.

## Implementations

## History

Photogrammetry resampled image pairs to epipolar geometry long before computer vision did. In computer vision, Hartley (1999) and Loop and Zhang (1999) showed how to rectify from the fundamental matrix alone and how to choose the homographies to keep the images close to the originals. Fusiello, Trucco and Verri (2000) gave the calibrated method of this page, short enough to fit in 22 lines of MATLAB, and Pollefeys, Koch and Van Gool (1999) gave polar rectification for the case that a homography cannot handle. Hartley and Zisserman treat rectification in Section 11.12 of their book.

## References
