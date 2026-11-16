---
tag: 2RET3M
kind: definition
slug: disparity
name: Disparity
aliases:
- binocular disparity
- disparity map
area: computer-vision/stereo-and-dense-reconstruction
level: intro
summary: The shift along the scanline between the images of one point in a rectified stereo pair, inversely proportional to its depth.
prereqs: [pixel, camera-intrinsic-matrix, epipolar-geometry]
see_also: [depth-from-disparity, stereo-rectification, stereo-matching, cost-volume, left-right-consistency-check, optical-flow, scene-flow, range-image]
sources:
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the part that defines the disparity space, the disparity map d(x, y) of the reference image and its relation to depth
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (rectification, disparity and inverse depth)
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 11.12, Image rectification (the epipolar lines made parallel to the rows)
---

The disparity of a scene point in a rectified stereo pair is the difference $d = u_1 - u_2$ between its column $u_1$ in the first image and its column $u_2$ in the second image; after [rectification](/stereo-rectification/) the two rows are equal, so this one number gives the match. For cameras with focal length $f$ in pixels and baseline $b$, a point at depth $Z$ has $d = f b / Z$, so disparity is inverse depth up to the fixed factor $f b$. A disparity map gives one disparity for each pixel of a reference image, and it is the output of [stereo matching](/stereo-matching/). This page fixes the sign and the units; the page [depth from disparity](/depth-from-disparity/) turns disparities into depths and studies the error.

## Definition

**Rectified pair.** Two cameras have the same intrinsic matrix $K$ with focal length $f = f_x$, the same rotation, and centers $C_1$ and $C_2 = C_1 + b\, e_X$ with $b > 0$, so the second camera is at distance $b$ to the right of the first along the $X$ axis of the camera frame ($X$ right, $Y$ down, $Z$ forward). A pixel $(u, v)$ has column $u$ and row $v$, origin top left. In such a pair a point $X$ with depth $Z > 0$ in the frame of camera 1 has pixels $(u_1, v)$ and $(u_2, v)$ in the same row $v$.

**Disparity.** The disparity of $X$ is

$$d = u_1 - u_2 = \frac{f b}{Z} .$$

It is measured in pixels and is a real number. With the second camera on the right, $d > 0$ for every point in front of both cameras, and $d \to 0$ as $Z \to \infty$.

**Disparity map.** Take the first (left) image as the reference. Its disparity map is the function $d_L(u, v)$ that gives, for each pixel, the disparity of the scene point seen there. It is defined only where that point is also visible in the second image; at the other pixels, the occluded ones, it is undefined. The disparity map of the second image as reference is $d_R(u_2, v)$ with the same sign, so that $u_1 = u_2 + d_R(u_2, v)$. A program searches a disparity range $d_{\min} \le d \le d_{\max}$, often $0 \le d < D$ with $D$ disparity levels.

**Other conventions.** Some texts write $d = u_2 - u_1$ or put the second camera on the left. Then the sign flips. If the two rectified cameras have different principal points $c_{x1} \ne c_{x2}$, the measured disparity is $d = f b / Z + (c_{x1} - c_{x2})$, and the constant must be removed before use. In vision science, binocular disparity is an angle: the difference of the visual directions of a point in the two eyes.

## Examples and non-examples

- **Check value.** With $f = 500$ pixels and $b = 0.1$ m, a point at $Z = 2.5$ m has $d = 500 \cdot 0.1 / 2.5 = 20$ pixels. At $Z = 5$ m it has $d = 10$, and at $Z = 50$ m it has $d = 1$.
- **A tilted plane.** For the plane $Z = Z_0 + \alpha Y$ in front of a rectified pair, $1/Z$ is an affine function of the pixel, so $d(u, v) = a u + b' v + c$ for constants $a$, $b'$, $c$. A plane facing the cameras has constant disparity. This is why many stereo methods model the disparity map as piecewise planar.
- **An occluded pixel.** A pixel of the left image that sees a point hidden in the right image by a nearer object has no disparity. Near the left edge of a foreground object, the left image sees some background that the right image does not see, which is why a [left-right consistency check](/left-right-consistency-check/) is needed.
- **Non-example: an unrectified pair.** If the epipolar lines are not rows, the match of a pixel is a 2D displacement $(\Delta u, \Delta v)$ that depends on the camera geometry. This is a correspondence, not a disparity in the sense of this page, until the pair is rectified.
- **Non-example: optical flow.** The 2D motion of a pixel between two frames of a video is [optical flow](/optical-flow/). For a static scene and a camera that only moves sideways, the flow is a disparity, but in general it has two components and includes the motion of objects.

## Related definitions

- **Depth and inverse depth.** Depth $Z$ is the distance along the optical axis, not the distance $\lVert X \rVert$ from the center (the range). Disparity is proportional to inverse depth $1/Z$, so a uniform step in disparity is a uniform step in inverse depth. The page [depth from disparity](/depth-from-disparity/) gives the conversion and its error.
- **Disparity space.** The set of triples $(u, v, d)$ is the disparity space. A [cost volume](/cost-volume/) stores a matching cost at each point of a discrete disparity space.
- **Generalized disparity.** For more than two views, or for views that are not rectified, Szeliski and others use $1/Z$ itself, or a value proportional to it, as the generalized disparity. [Plane sweep stereo](/plane-sweep-stereo/) samples it at fixed steps.
- **Half occlusion.** A point visible in one image and not in the other is half occluded. Its pixel has no disparity in the sense above.
- **Range image.** A [range image](/range-image/) stores a distance or a depth per pixel. A disparity map turns into a depth map pixel by pixel.

## References
