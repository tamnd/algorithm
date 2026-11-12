---
tag: 7XV9G3
kind: model
slug: pinhole-camera-model
name: Pinhole camera model
aliases:
- ideal pinhole camera
area: graphics-and-signals/ray-tracing
level: intro
summary: A camera with one center of projection, which maps each scene point to the image point where the line through the center meets the image plane, so that each pixel sees along one ray.
prereqs: [pixel]
see_also: [thin-lens-camera, primary-ray-generation, viewport-transform, perspective-correct-interpolation, graphics-pipeline, depth-of-field, ray-casting, z-buffer]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2003
    locator: Section 6.1 Finite cameras (the basic pinhole model, the calibration matrix and the camera matrix P = K[R | t])
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 6.2.2 The Perspective Camera
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 4, Ray Tracing (perspective views), and the chapter on viewing (the perspective transform)
---

The pinhole camera model is the camera with an aperture of size zero. All light that reaches the image passes through a single point, the center of projection, so a scene point $X$ appears at the one image point where the line from $X$ through the center meets the image plane. In the other direction, each image point sees the scene along one ray from the center. The model gives perspective, with far objects smaller and parallel lines meeting at vanishing points, and it has no blur: every depth is in focus. It is the default camera of ray tracers, where [primary ray generation](/primary-ray-generation/) inverts it, and of rasterizers, where the [graphics pipeline](/graphics-pipeline/) applies it as a projective transform.

## The machine

**The camera.** A pinhole camera has a center $e$, an orthonormal basis $(u, v, w)$ with the view direction $-w$, and an image plane at distance $f > 0$ in front of the center, the plane of the points $e + x\,u + y\,v - f\,w$. In graphics $f$ is usually 1 and the image is a window $[-a\tau, a\tau] \times [-\tau, \tau]$ on that plane, with $\tau = \tan(\theta / 2)$ for the vertical field of view $\theta$ and the aspect ratio $a = W / H$ of an image of $W \times H$ [pixels](/pixel/).

**The projection.** For a scene point $X$, write $X - e = X_c\,u + Y_c\,v - Z_c\,w$, so that $Z_c$ is its depth in front of the camera. If $Z_c > 0$, the image of $X$ is

$$x = f \frac{X_c}{Z_c}, \qquad y = f \frac{Y_c}{Z_c},$$

the point where the segment from $X$ to $e$, extended, meets the image plane. Points with $Z_c \le 0$ are behind the camera or in the plane of the center and have no image. In homogeneous coordinates this is the linear map $X \mapsto K\,[R \mid t]\,X$ followed by a division by the last coordinate, where $[R \mid t]$ maps world to camera coordinates and the calibration matrix $K$ holds $f$, the scale to pixels and the principal point (Hartley and Zisserman, Section 6.1). The map from the image plane to pixel coordinates is the [viewport transform](/viewport-transform/).

**The inverse.** An image point $(x, y)$ is the image of every point on the ray $e + t\,(x\,u + y\,v - f\,w)$, $t > 0$, and of no other point. So one image point corresponds to one ray, and a pixel with a single sample corresponds to the ray through its sample point.

**What costs one unit.** In a ray tracer, one sample of the image costs one primary ray, which then costs its query. In a rasterizer, one vertex costs one projection: a $4 \times 4$ matrix product and a division.

## What it counts

The model fixes which rays an image needs and what each pixel shows. With one sample per pixel, an image of $P$ pixels needs exactly $P$ primary rays, one per pixel, all from the same origin; with $s$ samples it needs $P s$. Since all rays share the origin $e$, the model counts no light that comes through any other point: there is no depth of field, no vignetting and no lens distortion. The amount of light per pixel is not modeled either; a renderer treats the pinhole as a sensor that measures the radiance along each ray.

## Relation to other models

- **The thin lens.** The [thin-lens camera](/thin-lens-camera/) replaces the center by a lens disk of radius $R$. Points on one plane of focus stay sharp and the others blur over a circle of confusion. With $R = 0$ it is the pinhole model, and for points in focus it gives the same image.
- **Orthographic projection.** Moving the center to infinity along $w$, while scaling the image to keep its size, gives parallel projection, with $x = X_c$ and $y = Y_c$. All rays are parallel, and sizes do not depend on depth.
- **Real lenses.** Systems of several lenses add distortion, vignetting and aberrations; renderers model them by tracing rays through the lens elements. Computer vision adds radial distortion terms to the pinhole map to calibrate real cameras.
- **Rasterization.** The perspective projection matrix of the graphics pipeline is the pinhole map in homogeneous form, with the depth kept for the [z-buffer](/z-buffer/).

## Known results in the model

- **Lines map to lines.** Central projection maps a segment in front of the camera to a segment of the image, so triangles in front of the camera project to triangles and [triangle rasterization](/triangle-rasterization/) applies.
- **Attributes are not linear in the image.** Depth and texture coordinates are not affine functions of the image position across a projected triangle, but their values divided by the depth, and $1 / Z_c$ itself, are. This is the basis of [perspective-correct interpolation](/perspective-correct-interpolation/).
- **Vanishing points.** Parallel lines with a direction $D$ that is not parallel to the image plane meet in the image at the image of the direction, $f\,(D_x / D_z, D_y / D_z)$.
- **Foreshortening.** An object of size $s$ at depth $Z_c$, parallel to the image plane, has an image of size $f s / Z_c$.
- **Ray generation.** The inverse map gives the rays of [primary ray generation](/primary-ray-generation/), which [ray casting](/ray-casting/) uses to decide visibility pixel by pixel.
- **The camera matrix.** A finite pinhole camera, with general $K$, has 11 degrees of freedom, and its matrix $P = K [R \mid t]$ can be estimated from 6 or more correspondences between known scene points and image points (Hartley and Zisserman, Chapter 7).

## References
