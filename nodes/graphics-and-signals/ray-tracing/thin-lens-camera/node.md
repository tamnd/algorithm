---
tag: Q73QJA
kind: model
slug: thin-lens-camera
name: Thin-lens camera model
aliases:
- thin lens model
area: graphics-and-signals/ray-tracing
level: intro
summary: A camera with a lens disk of finite radius that obeys the Gaussian lens equation, so points on one plane of focus are sharp and other points blur into circles of confusion.
prereqs: [pinhole-camera-model]
see_also: [depth-of-field, primary-ray-generation, distributed-ray-tracing, monte-carlo-integration, stratified-sampling, path-tracing]
sources:
  - paper: doi:10.1145/800224.806818
    title: Michael Potmesil and Indranil Chakravarty, A lens and aperture camera model for synthetic image generation, Computer Graphics (SIGGRAPH 81 Proceedings) 15(3), 1981, 297 to 305
    locator: the thin lens model and the circle of confusion, and the focus processor that blurs a pinhole image (Section 3.2)
  - paper: doi:10.1145/800031.808590
    title: Robert L. Cook, Thomas Porter and Loren Carpenter, Distributed ray tracing, Computer Graphics (SIGGRAPH 84 Proceedings) 18(3), 1984, 137 to 145
    locator: the section on depth of field (rays from sample points of the lens through the point in focus)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 6.2.3 The Thin Lens Model and Depth of Field (Equations 6.1 and 6.2, the Gaussian lens equation and the circle of confusion)
---

The thin-lens camera model replaces the single center of the [pinhole camera](/pinhole-camera-model/) by a lens disk of radius $R$, idealized as having no thickness. All light from a scene point at distance $z_o$ in front of the lens that passes through the lens meets again at one point at distance $z_i$ behind it, with $1/f = 1/z_o + 1/z_i$ for the focal length $f$. A film at one distance therefore records one plane of the scene sharply, and a point off that plane as a disk, its circle of confusion. This is how a renderer gets [depth of field](/depth-of-field/). Potmesil and Chakravarty (1981) brought the model into computer graphics as a postprocess of a pinhole image; Cook, Porter and Carpenter (1984) rendered it by tracing rays from sample points of the lens.

## The machine

**The camera.** The lens is a disk of radius $R$ (aperture diameter $A = 2R$) centered at $e$ in the plane spanned by $u$ and $v$, with the optical axis $-w$ and the focal length $f > 0$. The film is a plane behind the lens at the image distance $z_i > f$, and a scene point is at the depth $z$ in front of the lens.

**The lens equation.** An ideal thin lens maps the point at depth $z_o > f$ on the axis to the point at image distance $z_i$ with the Gaussian lens equation

$$\frac{1}{f} = \frac{1}{z_o} + \frac{1}{z_i},$$

and a ray through the center of the lens is not bent. So the plane of focus is at $z_f = f z_i / (z_i - f)$, and the image of any scene point lies on the line through it and the lens center, as in the pinhole model.

**The circle of confusion.** A scene point at depth $z \ne z_f$ focuses at $f z / (z - f)$, in front of or behind the film, and the cone of its light through the lens cuts the film in a disk of diameter

$$C = A\,\frac{f\,|z - z_f|}{z\,(z_f - f)}.$$

**The renderer's form.** Ray tracers usually fix the plane of focus $z_f$ and the lens radius $R$ instead of $f$ and $z_i$, and keep the image plane of the pinhole model. A sample point of the image defines the pinhole ray from $e$; the point $p_f$ of that ray at the depth $z_f$ is in focus; the camera ray starts at a sample point $o$ of the lens and goes to $p_f$. This is the form of [primary ray generation](/primary-ray-generation/) and of PBRT (its Section 6.2.3). It is the same model as above with $z_i = f z_f / (z_f - f)$, and in it the rays of one image sample, measured in the scene at depth $z$, spread over a disk of diameter $2R\,|z - z_f| / z_f$.

**What costs one unit.** One camera ray is one sample of the pixel area and the lens together. The pixel value is an integral over the lens, so a renderer estimates it with many samples, by [Monte Carlo integration](/monte-carlo-integration/).

## What it counts

The model counts the light that reaches a film point through the whole lens: the value of a pixel is the average of the radiance over all rays from the lens disk through the point in focus, a two-dimensional integral per pixel on top of the integral over the pixel area. A renderer pays for it in samples: with $s$ rays per pixel, the noise of the blur falls like $1 / \sqrt{s}$ for independent samples, and faster for [stratified](/stratified-sampling/) ones. The model does not count the light lost at the rim of the lens, the aberrations of real lenses, or the thickness of the lens.

## Relation to other models

- **The pinhole camera.** With $R = 0$ every ray goes through the lens center, and the thin lens is the [pinhole camera model](/pinhole-camera-model/). Points on the plane of focus have the same image in both models.
- **Real lens systems.** A camera model that traces rays through the actual surfaces of a lens system, as introduced by Kolb, Mitchell and Hanrahan in 1995, adds distortion, aberrations and vignetting. The thin lens is its first-order approximation.
- **Thick lenses.** A thick lens is modeled by two principal planes; between them the ray moves parallel to the axis, and outside them it behaves like a thin lens.
- **Postprocess blur.** Potmesil and Chakravarty computed the circle of confusion of each point of a pinhole image and spread the point over it; it is fast but wrong at occlusion boundaries, where the lens sees around a foreground object. Ray tracing the lens, as Cook, Porter and Carpenter did, gets those boundaries right.

## Known results in the model

- **Depth of field.** Given an acceptable circle of confusion $c$ on the film, the depths with $C \le c$ form the depth of field, an interval around $z_f$ that grows as the aperture shrinks. Its size in photography is usually written with the f-number $N = f / A$; see [depth of field](/depth-of-field/).
- **Focus at a point.** All lens rays of one image sample pass through one point of the plane of focus, and only through it.
- **Sampling the lens.** Uniform samples of the disk need an area-preserving map from the square, such as the concentric map of Shirley and Chiu, so that stratified samples of the square stay stratified on the disk.
- **Distributed ray tracing.** Sampling the lens together with the pixel area, the light and time, in one set of rays, gives depth of field, soft shadows and motion blur together: [distributed ray tracing](/distributed-ray-tracing/), and later [path tracing](/path-tracing/).

## References
