---
tag: KB8FWQ
kind: concept
slug: depth-of-field
name: Depth of field
aliases:
- defocus blur
area: graphics-and-signals/ray-tracing
level: intro
summary: The range of distances that a lens with a finite aperture renders acceptably sharp. Points outside it blur into disks, and the range shrinks as the aperture opens.
prereqs: [thin-lens-camera]
see_also: [primary-ray-generation, distributed-ray-tracing, pinhole-camera-model, monte-carlo-integration, stratified-sampling, path-tracing, supersampling-antialiasing]
sources:
  - paper: doi:10.1145/800224.806818
    title: Michael Potmesil and Indranil Chakravarty, A lens and aperture camera model for synthetic image generation, Computer Graphics (SIGGRAPH 81 Proceedings) 15(3), 1981, 297 to 305
    locator: the circle of confusion of the thin lens and the postprocess that spreads each point of a pinhole image over it
  - paper: doi:10.1145/800031.808590
    title: Robert L. Cook, Thomas Porter and Loren Carpenter, Distributed ray tracing, Computer Graphics (SIGGRAPH 84 Proceedings) 18(3), 1984, 137 to 145
    locator: the section on depth of field (rays from points of the lens through the point in focus)
  - paper: doi:10.1145/97880.97913
    title: Paul Haeberli and Kurt Akeley, The accumulation buffer, hardware support for high-quality rendering, Computer Graphics (SIGGRAPH 90 Proceedings) 24(4), 1990, 309 to 318
    locator: the section on depth of field (the average of images rendered from points of the lens)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 6.2.3, The Thin Lens Model and Depth of Field
---

Depth of field is the range of distances in front of a camera within which objects look sharp. A [pinhole camera](/pinhole-camera-model/) has an infinite depth of field: every point maps to a point. A real lens gathers light over an aperture of finite size, and it focuses only one plane exactly; a point at another distance becomes a small disk on the film, its circle of confusion, whose size the [thin-lens camera](/thin-lens-camera/) model gives. If the eye or the pixel grid cannot resolve the disk, the point still counts as sharp, and the distances for which this holds form the depth of field. Outside them the image shows defocus blur. Photographers use it to isolate a subject; renderers add it for realism and to guide the eye. A ray tracer gets it by sampling the lens, as in [distributed ray tracing](/distributed-ray-tracing/); a rasterizer approximates it by blurring a pinhole image with a kernel that depends on the depth.

## In plain words

Hold a finger close to your eye and look at a wall far away. The wall is sharp and the finger is a blur. Look at the finger, and the wall blurs. An eye or a camera can focus on one distance at a time.

Things a little nearer or farther than that distance are blurred too, but only a little. If the blur is too small to notice, they still look sharp. The band of distances that look sharp is the depth of field.

A small opening in front of the lens makes the band deep, so almost all of the picture is sharp. A wide opening makes it shallow, so only the subject is sharp and the rest melts into soft blobs. The shape of each blob is the shape of the opening.

## The idea

**The acceptable blur.** Let the lens have the focal length $f$ and the f-number $N$, so that the aperture diameter is $A = f / N$, and let it be focused at the distance $s$. A point at the distance $z$ images as a disk of diameter $C(z)$ on the film, by the formula of the [thin-lens camera](/thin-lens-camera/). With $A = f/N$ that formula reads

$$C(z) = \frac{f^2}{N} \cdot \frac{|z - s|}{z\,(s - f)}.$$

Choose the largest diameter $c$ that still looks sharp. For a 35 mm film or a full-frame sensor of 36 by 24 mm, $c = 0.03$ mm is a common choice, about 1/1440 of the diagonal; a renderer can take the size of a pixel on the film.

**The limits.** The depth of field is the set of $z$ with $C(z) \le c$. Solve $C(z) = c$ on both sides of $s$. With the hyperfocal distance

$$H = \frac{f^2}{N c} + f,$$

the near and far limits are

$$D_n = \frac{s\,(H - f)}{H + s - 2f}, \qquad D_f = \frac{s\,(H - f)}{H - s} \quad (s < H),$$

and $D_f = \infty$ for $s \ge H$. When $f \ll s \ll H$, the depth of field is about $D_f - D_n \approx 2 N c\,s^2 / f^2$: it grows with the f-number, with the square of the distance, and falls with the square of the focal length.

**The hyperfocal distance.** At $s = H$ a point at infinity has the blur $A f / (H - f) = c$ exactly, and the near limit is $D_n = H/2$. Focusing at $H$ makes everything from $H/2$ to infinity acceptably sharp, the largest depth of field that the lens has at that f-number.

**The same picture with other cameras.** A smaller sensor needs a shorter focal length for the same view and a smaller $c$ for the same print size. If both scale by a factor $k$, the depth of field stays the same when the f-number also scales by $k$, that is, when the aperture diameter $f/N$ stays the same. The depth of field of a scene seen from one place with one angle of view depends on the diameter of the aperture, not on the f-number alone.

**The shape of the blur.** A point out of focus images as a copy of the aperture, scaled by $C(z)/A$, and upside down if the point is behind the plane of focus. A round aperture gives disks; a diaphragm with six blades gives hexagons. Photographers call the look of these shapes bokeh. A defocused edge is the edge convolved with the disk: across it the brightness follows the area of a circular segment, and the transition is $C(z)$ wide on the film.

**Rendering it.** Three families of methods are in use.

- **Lens sampling.** For each image sample, a ray tracer picks a point on the lens disk and shoots the ray from it through the point in focus, as in [primary ray generation](/primary-ray-generation/), and averages many such rays. Cook, Porter and Carpenter (1984) did this with jittered lens positions. It is exact for the model, it handles occlusion right, and its noise falls with the number of samples, faster for [stratified](/stratified-sampling/) lens samples.
- **Accumulation.** Haeberli and Akeley (1990) render the whole image once from each of several points on the lens, with the projection sheared so that the plane of focus stays fixed, and average the images. It is lens sampling with the same lens points for every pixel, so few points give visible ghost copies instead of noise.
- **Postprocess.** Potmesil and Chakravarty (1981) render a pinhole image with depth, then spread each pixel over its circle of confusion. Real-time engines use gather or scatter versions of this. It is fast, but it is wrong at depth discontinuities: a blurred foreground object should let the lens see the background behind its edges, and a pinhole image does not contain that background. Sharp objects behind blurred ones also leak into them unless the filter respects depth.

## Examples

**A portrait lens.** A 50 mm lens on a full-frame camera, with $c = 0.03$ mm, focused at 3 m:

| f-number | hyperfocal $H$ | near limit | far limit | depth of field |
|---|---|---|---|---|
| f/2.8 | 29.81 m | 2.729 m | 3.330 m | 0.60 m |
| f/16 | 5.26 m | 1.915 m | 6.919 m | 5.00 m |

At f/2.8 the approximation $2 N c s^2 / f^2$ gives 0.605 m. A point at infinity has the blur $0.303$ mm, ten times $c$, so the background is far out of focus. At f/2.8 and focus at 1 m the sharp range is only 0.969 to 1.033 m, 6.4 cm; at 10 m it is 7.49 to 15.02 m. Focused at its hyperfocal distance of 29.81 m, the lens at f/2.8 is sharp from 14.9 m to infinity.

**Equivalent cameras.** A 25 mm lens at f/1.4 on a sensor half as large, with $c = 0.015$ mm, has the same view and the same aperture diameter of 17.9 mm as the 50 mm lens at f/2.8. Focused at 3 m it is sharp from 2.727 to 3.333 m, the same range up to the small term $f$ in the formulas.

**A defocused edge.** A 50 mm lens at f/2, with a lens radius of 12.5 mm, is focused at 3 m. The image of a bright half-plane at 1.5 m changes from dark to bright over a band whose width, measured on the plane of focus, is 25 mm, and the profile is the circular-segment area of the lens disk. A half-plane at 6 m blurs over 12.5 mm, half as much: on the film its circle of confusion is 0.212 mm against 0.424 mm, because the blur grows faster in front of the plane of focus than behind it. A Monte Carlo estimate with 20,000 uniform lens samples per film point matches the segment area within four binomial standard errors.

## Where it is used

- Film and animation renderers render depth of field by lens sampling in [path tracing](/path-tracing/), together with the samples of the pixel area for [supersampling](/supersampling-antialiasing/).
- Games and real-time engines blur a rendered image by its depth buffer, with the circle of confusion of the thin lens as the kernel size.
- Photographers and cinematographers plan shots with the depth of field tables of the formulas above, and focus at the hyperfocal distance for landscapes.
- Microscopy and machine vision trade the depth of field against the light and the resolution: a smaller aperture gives more depth but less light and, through diffraction, less resolution.

### History

The depth of field of lenses and the hyperfocal distance were known to photographers in the nineteenth century. In computer graphics, every early image was made by a pinhole camera and was sharp everywhere. Potmesil and Chakravarty (1981) introduced the thin lens model and its circle of confusion, as a postprocess of a pinhole image. Cook, Porter and Carpenter (1984) rendered depth of field exactly by tracing rays from points of the lens, as one of the effects of distributed ray tracing. Haeberli and Akeley (1990) brought it to graphics hardware with the accumulation buffer.

## References
