---
tag: BVKC3J
kind: problem
slug: shape-from-shading
name: Shape from shading
aliases:
- photoclinometry
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: "Recover the shape of a surface from the shading of one image under known light and reflectance. Without boundary data the first-order PDE is ill-posed."
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels}
  time: {worst: Ω(W H)}
prereqs: [lambertian-reflectance, eikonal-equation]
see_also: [photometric-stereo, fast-marching-method, method-of-characteristics, level-set-method, upwind-scheme, poisson-equation, brdf, shape-from-focus]
sources:
  - url: https://dspace.mit.edu/handle/1721.1/149396
    title: "Berthold K. P. Horn, Shape from shading: a method for obtaining the shape of a smooth opaque object from one view, PhD thesis, Massachusetts Institute of Technology, 1970"
    locator: "the image irradiance equation as a first-order partial differential equation and its solution along characteristic strips"
  - book: isbn:9780262081832
    title: "Berthold K. P. Horn and Michael J. Brooks (editors), Shape from Shading, MIT Press, 1989"
    locator: the collected papers on the reflectance map and on variational and characteristic methods
  - paper: doi:10.1109/34.784284
    title: "Ruo Zhang, Ping-Sing Tsai, James Edwin Cryer and Mubarak Shah, Shape from shading: a survey, IEEE Transactions on Pattern Analysis and Machine Intelligence 21(8), 1999, pages 690 to 706"
    locator: "the classes of methods (minimization, propagation, local and linear) and their comparison on synthetic and real images"
  - paper: doi:10.1016/j.cviu.2007.09.003
    title: "Jean-Denis Durou, Maurizio Falcone and Manuela Sagona, Numerical methods for shape-from-shading: a new survey with benchmarks, Computer Vision and Image Understanding 109(1), 2008, pages 22 to 43"
    locator: "the sorting of methods into PDE methods, optimization methods and methods that approximate the image irradiance equation, and the benchmarks"
  - paper: doi:10.1109/CVPR.2005.319
    title: "Emmanuel Prados and Olivier Faugeras, Shape from shading: a well-posed problem?, IEEE Conference on Computer Vision and Pattern Recognition 2005"
    locator: "the perspective model with a light at the optical center and attenuation with the square of the distance, for which the problem is well-posed"
  - paper: doi:10.1109/34.3909
    title: "Robert T. Frankot and Rama Chellappa, A method for enforcing integrability in shape from shading algorithms, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(4), 1988, pages 439 to 451"
    locator: the projection of a gradient field onto integrable surfaces in the Fourier domain
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.1.1, Shape from shading and photometric stereo"
---

Shape from shading is the problem of finding the 3D shape of a surface from one image, using only how bright each pixel is. A surface patch that faces the light looks bright and a patch that turns away looks dark, so the brightness says something about the direction the surface faces. But one brightness value at a pixel cannot fix the two numbers of a surface direction, so the problem needs more: smoothness, boundary values, or a model that removes the ambiguity. Horn (1970) wrote it as a first-order partial differential equation and solved it along characteristic curves. In astronomy the same task, applied to images of the Moon and planets, is called photoclinometry. With several images under different lights, the problem becomes [photometric stereo](/photometric-stereo/), which has a unique solution at each pixel. Shape from shading uses only one image, so it is much harder, and in its simplest form it has more than one solution.

## In plain words

Look at a photo of a smooth white ball lit from the front. The middle is bright and the edge gets darker. From this alone you can guess that the middle faces you and the edge turns away. You cannot tell which way it turns: a ball that bulges toward you and a bowl that curves away give the same photo. The brightness of one pixel tells only how far the surface turns from the light, not in which direction. Shape from shading puts together the clues from all pixels, assumes the surface is smooth, and uses known points, such as the edge of the object, to choose one shape. The result is often good in its fine detail but can be wrong in its overall shape.

## Definition

**Frame.** As on [photometric stereo](/photometric-stereo/), this page uses the height-field frame of Horn: $x$ and $y$ lie in the image plane and $z$ points toward the viewer. The surface is $z(x, y)$ with slopes $p = z_x$ and $q = z_y$, and its unit normal is $n = (-p, -q, 1) / \sqrt{1 + p^2 + q^2}$.

**Input.**

- One gray image $E(x, y)$ of size $W \times H$, with a linear response.
- The reflectance map $R(p, q)$: the brightness of a surface patch with slopes $(p, q)$ under the known light. For a [Lambertian](/lambertian-reflectance/) surface with albedo $\rho$ and a distant light in the unit direction $s$,

$$R(p, q) = \rho\, \frac{-p s_x - q s_y + s_z}{\sqrt{1 + p^2 + q^2}}.$$

- Often, boundary data: the depth on the border of the image or of a region, or the points where the surface faces the light exactly.

**Output.** A height map $z(x, y)$ that satisfies the image irradiance equation

$$E(x, y) = R\big(z_x(x, y), z_y(x, y)\big)$$

at every pixel, together with the boundary data.

**The eikonal form.** With the light at the viewer, $s = (0, 0, 1)$, and $\rho = 1$, the equation is $E = 1 / \sqrt{1 + |\nabla z|^2}$, which is the [eikonal equation](/eikonal-equation/)

$$|\nabla z| = \sqrt{\frac{1}{E^2} - 1}.$$

The brightness fixes the steepness of the surface at each point, and nothing else. The points with $E = 1$, where the surface faces the light, are the singular points of the equation: there $\nabla z = 0$, and $z$ has a local maximum, a local minimum or a saddle.

**Ill-posed.** In this simple form, the problem does not have a unique solution. If $z$ solves it, so do $z + c$ for every constant $c$ and $-z$, since $|\nabla z|$ does not change. At each singular point, the surface can bulge up or down, and away from them, nonsmooth solutions can join pieces. Without boundary data and a rule that picks one solution, the image does not determine the shape.

## Variants

- **Light at the viewer or oblique.** With the light at the viewer, the problem is the eikonal equation. An oblique light gives a more general first-order equation of Hamilton and Jacobi type.
- **Orthographic or perspective camera.** The classical problem uses an orthographic camera. Prados and Faugeras (2005) use a perspective camera with a point light at the optical center whose light falls with the square of the distance. They show that this model is well-posed: the darkening with distance breaks the convex and concave ambiguity.
- **Known or unknown light and albedo.** With an unknown light direction or albedo, these must be estimated too, which adds more ambiguity. Natural light from all directions is often modeled with a few low-frequency terms.
- **Other reflectance.** Specular or rough surfaces need a different reflectance map, for example from a measured [BRDF](/brdf/).
- **Shading as a refinement.** Many systems use a rough depth map from stereo or a depth camera and use shading only to add fine detail. This removes most of the ambiguity.

## Examples

**One pixel.** With the light at the viewer and $\rho = 1$, a pixel of brightness $E = 0.8$ has $|\nabla z| = \sqrt{1/0.64 - 1} = 0.75$: the surface there slopes by $\arctan 0.75 \approx 36.9$ degrees, in a direction that the pixel does not tell. All slopes $(p, q)$ on the circle $p^2 + q^2 = 0.5625$ give the same brightness.

**A ball and a bowl.** The hemisphere $z = \sqrt{1 - x^2 - y^2}$ has $p = -x/z$ and $q = -y/z$, so $1 + p^2 + q^2 = 1/z^2$ and, with the light at the viewer, $E = z$. The image is brightest at the center and goes to 0 at the edge. The bowl $z = -\sqrt{1 - x^2 - y^2}$ has the same $|\nabla z|$ and gives exactly the same image. The center is the one singular point, and the choice between a maximum and a minimum there decides between the two shapes.

**A crater illusion.** A photo of a crater on the Moon, turned upside down, often looks like a hill. When the light direction is not known, a viewer assumes light from above, and turning the image changes the shape that the shading suggests. This is the same ambiguity, made worse by the unknown light.

## Known algorithms

Zhang et al. (1999) and Durou et al. (2008) survey the methods. Durou et al. sort them into PDE methods, optimization methods and methods that approximate the equation.

| Class | Method | Idea |
|---|---|---|
| PDE | characteristic strips (Horn 1970) | integrate ordinary differential equations along characteristic curves, by the [method of characteristics](/method-of-characteristics/), from a known start curve or from singular points |
| PDE | viscosity solutions | solve the eikonal or Hamilton-Jacobi form on the grid with an [upwind scheme](/upwind-scheme/), which picks one solution when the depth on the boundary and at the singular points is given |
| PDE | [fast marching](/fast-marching-method/) | solve the eikonal form in one pass, in order of increasing depth from the start points, in $O(W H \log(W H))$ time |
| Optimization | variational methods | minimize the squared brightness error plus a smoothness term, and often an integrability term, by iteration; see the papers collected by Horn and Brooks (1989) |
| Approximation | local linearization | replace the reflectance map by a linear function of $(p, q)$ or of the depth near the current estimate, and solve the linear problem; repeat |

Optimization methods often estimate the slopes first and then fit a height map. The fit is done by projecting the slopes onto integrable surfaces with the fast Fourier transform (Frankot and Chellappa 1988), or by solving a [Poisson equation](/poisson-equation/).

## Bounds

- **Input size.** On the real RAM, a method that gives a height for every pixel must read every pixel in the worst case, since the brightness of a pixel that it does not read can change the slope there. So any method takes $\Omega(W H)$ time. Fast marching and sweeping methods for the eikonal form come close: $O(W H \log(W H))$ and $O(W H)$ per sweep.
- **No unique answer from the image alone.** In the classical model, $z$ and $-z$ give the same image, so no method can decide between them without extra data. Under a known light that is not at the viewer, the image still gives only one equation for two unknowns at each pixel.
- **Accuracy.** The benchmarks of Zhang et al. and Durou et al. show that no method gives good results on all test images. The errors depend on the image, the noise and how well the model fits the real surface.

## Reductions

- **From photometric stereo.** Photometric stereo with $N$ images under different lights gives $N$ equations at each pixel. Shape from shading is the case $N = 1$, where the linear system has fewer equations than unknowns.
- **To the eikonal equation.** With the light at the viewer and constant albedo, the problem is the eikonal equation with speed $1 / \sqrt{1/E^2 - 1}$, so methods for shortest paths and wave fronts, such as fast marching, solve it.
- **To normal integration.** If the slopes are known, finding $z$ is a Poisson equation $\nabla^2 z = p_x + q_y$ with boundary conditions.

## Applications

- **Planetary maps.** Photoclinometry finds slopes and heights on the Moon and planets from orbital images, where only one image of an area may exist.
- **Shape refinement.** Fine detail from shading improves depth maps from stereo and from depth cameras, and meshes from [multi-view stereo](/multi-view-stereo/).
- **Endoscopy and inspection.** A camera with a light next to its lens is close to the model of Prados and Faugeras, for example in medical endoscopes.
- **Human vision.** The ambiguities explain how people see shape from shading and where they are fooled.

## References
