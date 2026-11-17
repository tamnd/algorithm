---
tag: 23HK0D
kind: problem
slug: image-matting
name: Image matting
aliases:
- alpha matting
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Recover the opacity alpha of the foreground at each pixel, and often its color, from an image that is a blend alpha F + (1 - alpha) B and a trimap or scribbles."
model: real-ram
complexity:
  vars: {n: the number of pixels}
  time: {worst: O(n^3)}
prereqs: [porter-duff-compositing, interactive-segmentation]
see_also: [closed-form-matting, interactive-segmentation, image-compositing, guided-filter, grabcut, random-walker-segmentation, laplacian-matrix]
sources:
  - paper: doi:10.1145/800031.808606
    title: "Thomas Porter and Tom Duff, Compositing digital images, SIGGRAPH 1984, 253-259"
    locator: the alpha channel and the over operator
  - paper: doi:10.1145/237170.237263
    title: "Alvy Ray Smith and James F. Blinn, Blue screen matting, SIGGRAPH 1996, 259-268"
    locator: "the proof that matting against one known backing color has no unique solution in general, and triangulation with two backings"
  - paper: doi:10.1109/CVPR.2001.990970
    title: "Yung-Yu Chuang, Brian Curless, David H. Salesin and Richard Szeliski, A Bayesian approach to digital matting, CVPR 2001, vol. II, 264-271"
    locator: "the trimap, and the maximum a posteriori estimate of F, B and alpha with color clusters"
  - paper: doi:10.1109/CVPR.2006.18
    title: "Anat Levin, Dani Lischinski and Yair Weiss, A closed form solution to natural image matting, CVPR 2006, vol. 1, 61-68"
    locator: "Section 1, the count of 3 equations and 7 unknowns per color pixel"
  - paper: doi:10.1561/0600000019
    title: "Jue Wang and Michael F. Cohen, Image and video matting: a survey, Foundations and Trends in Computer Graphics and Vision 3(2), 97-175, 2008"
    locator: the chapters on color sampling methods and on matting affinities
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Section 10.4, image matting and compositing"
---

Image matting is the problem of pulling a soft foreground out of an image. Each pixel color $I$ is modeled as a blend $I = \alpha F + (1 - \alpha) B$ of a foreground color $F$ and a background color $B$, with an opacity $\alpha \in [0, 1]$. The task is to find $\alpha$, and usually $F$, at each pixel, so that the foreground can be put on a new background with [compositing](/porter-duff-compositing/). Unlike a hard mask from [interactive segmentation](/interactive-segmentation/), the matte keeps hair, fur, smoke, motion blur and the mixed pixels on every edge. With 3 equations and 7 unknowns per color pixel, the problem has no unique answer without more input. That input is a known backing color, two shots against two backings, or a trimap or scribbles from a user together with an assumption about the image.

## In plain words

When you cut out a person from a photo, the edge is not sharp. A strand of hair covers only part of a pixel, so the pixel color is a mix of the hair and the wall behind it. Matting finds, for each pixel, how much of it belongs to the person, from none to all, and what color the person has there.

One photo alone does not say this, because many mixes give the same color. So you need more help: a known wall color, two photos against two walls, or a rough map from the user that says "surely person", "surely wall" and "not sure".

## Definition

The input is an image $I$ with $n$ pixels and colors in $\mathbb R^3$. The model is the compositing equation

$$I_p = \alpha_p F_p + (1 - \alpha_p) B_p, \qquad \alpha_p \in [0, 1],$$

for each pixel $p$. Porter and Duff (1984) used the same equation, the over operator, to put a foreground with an alpha channel on a background. Matting runs it the other way. The output is $\alpha_p$ for each pixel, and in many uses also $F_p$ (and $B_p$).

At each color pixel there are 3 equations and 7 unknowns ($\alpha$, $F$ and $B$), so the problem must have more input. The common forms are:

- **Known backing.** $B$ is a known constant color, as in blue screen work.
- **Two backings.** Two images of the same foreground against two known backings $B_1$ and $B_2$.
- **Trimap.** The user marks each pixel as sure foreground ($\alpha = 1$), sure background ($\alpha = 0$) or unknown. Only the unknown band must be solved.
- **Scribbles.** A few strokes of sure foreground and background, with all other pixels unknown.

An answer is judged against a ground truth matte, for example by the sum of absolute differences or the mean squared error over the unknown pixels. These scores are benchmark results.

## Variants

- **Constant-color (blue screen) matting.** One known backing $B$. Smith and Blinn (1996) showed that this has no unique solution in general; it becomes solvable only with an extra rule on $F$, such as "the foreground has no blue".
- **Triangulation matting.** Two shots against two backings. This gives 6 equations for 4 unknowns ($\alpha$ and $F$), and the solution is unique when the backings differ at the pixel (Smith and Blinn 1996).
- **Natural image matting.** An arbitrary background, with a trimap or scribbles. This is the usual meaning of "image matting" today.
- **Video matting.** A matte for each frame that also stays stable in time.
- **Environment and shadow matting.** Extended models that also capture how the foreground bends or reflects the light from the background, or the shadow that it casts. They do not fit the equation above.

## Examples

**One backing is not enough.** Let the backing be blue, $B = (0, 0, 255)$, and the observed pixel $I = (120, 24, 126)$. The pair $\alpha = 0.6$, $F = (200, 40, 40)$ explains it, since $0.6 F + 0.4 B = (120, 24, 24) + (0, 0, 102)$. So do $\alpha = 1$ with $F = I$, and $\alpha = 0.8$ with $F = (150, 30, 93.75)$. Each $\alpha$ from $129/255 \approx 0.506$ to $1$ gives a valid $F$ with all channels in $[0, 255]$, so the data cannot pick one.

**Two backings fix it.** Shoot the same pixel again against green, $B_2 = (0, 255, 0)$, and get $I_2 = (120, 126, 24)$. Subtracting the two equations removes $F$:

$$I_1 - I_2 = (1 - \alpha)(B_1 - B_2).$$

Here $I_1 - I_2 = (0, -102, 102)$ and $B_1 - B_2 = (0, -255, 255)$, so $1 - \alpha = 0.4$ and $\alpha = 0.6$. In general, the least squares answer is $\alpha = 1 - (I_1 - I_2) \cdot (B_1 - B_2) / \lVert B_1 - B_2 \rVert^2$. Then $\alpha F = I_1 - (1 - \alpha) B_1 = (120, 24, 24)$, so $F = (200, 40, 40)$.

**A trimap with a natural background.** The [closed-form matting](/closed-form-matting/) page works through a small gray image with scribbles. It assumes that $F$ and $B$ are nearly constant in each small window, and then $\alpha$ is the solution of one sparse linear system.

## Known algorithms

| Method | Input | Main assumption | Cost | Kind of result |
|---|---|---|---|---|
| Triangulation (Smith and Blinn 1996) | two backings | the same $F$ and $\alpha$ in both shots | $O(n)$ | exact under the model |
| Blue screen rules (Vlahos and others) | one backing | a rule on the colors of $F$ | $O(n)$ | exact only if the rule holds |
| Bayesian matting (Chuang and others 2001) | trimap | $F$ and $B$ near Gaussian color clusters of nearby known pixels | iterative per pixel | local optimum of a posterior |
| Poisson matting (Sun and others 2004) | trimap | the gradient of $\alpha$ follows the image gradient | sparse Poisson systems | heuristic |
| [Closed-form matting](/closed-form-matting/) (Levin and others 2006) | scribbles or trimap | $F$ and $B$ nearly constant in each small window | one sparse linear system | global optimum of its cost |
| [Guided filter](/guided-filter/) refinement | rough matte | $\alpha$ is locally linear in the image | $O(n)$ | heuristic |
| learned matting (2017 on) | trimap, or none | trained on composites | one network pass | learned, no guarantee |

Wang and Cohen (2008) sort the classic methods into methods that sample colors of nearby known pixels, methods that spread $\alpha$ with affinities between pixels, and methods that combine both.

## Bounds

All bounds use the [real-RAM](/real-ram/) model with $n$ pixels, a fixed window size and a fixed number of neighbors per pixel.

- **Without more input there is no unique answer.** At each color pixel, 3 equations and 7 unknowns leave a 4-dimensional set of solutions, and with a known backing the set is still not a single point in general (Smith and Blinn 1996, first example above). This is a theorem about the model, not about any algorithm.
- **Two backings.** If $B_1 \ne B_2$ at the pixel, $\alpha$ and $F$ are unique and cost $O(1)$ per pixel, so $O(n)$ in total. This is a theorem.
- **Closed-form matting.** The cost is a quadratic form in $\alpha$ with a sparse, positive semidefinite [Laplacian](/laplacian-matrix/), so its minimum under the scribbles is a sparse linear system of size at most $n$. Gaussian elimination on it costs $O(n^3)$ in the worst case, which is the bound in the front matter. With the grid structure, sparse direct solvers and [conjugate gradients](/conjugate-gradient-method/) are much faster in practice; those times are benchmark results.
- **Lower bound.** Each pixel of the unknown band must be read, so $\Omega(n)$ in the worst case. This is a trivial theorem.

## Reductions

- **From compositing.** Matting inverts the over operator of [Porter-Duff compositing](/porter-duff-compositing/); a good matte makes [image compositing](/image-compositing/) on a new background look right.
- **From segmentation.** A hard mask from [interactive segmentation](/interactive-segmentation/), such as [GrabCut](/grabcut/), is eroded and dilated to give a trimap.
- **To a quadratic problem.** Under the local color line model, $F$ and $B$ drop out and matting becomes the minimization of $\alpha^T L \alpha$ under the scribbles; see [closed-form matting](/closed-form-matting/).
- **To harmonic interpolation.** With other pixel affinities in place of the matting Laplacian, the same system is a [random walker](/random-walker-segmentation/) with two labels.

## Applications

- **Film and television.** Blue and green screen keying, and pulling mattes of actors shot on real sets.
- **Photo editing.** Cutting out people and objects with their hair for a new background, or to blur or adjust only the background.
- **Video calls.** Replacing or blurring the background of a person in real time.
- **Data for learning.** Composites of matted foregrounds on many backgrounds give training data for segmentation and matting networks.

## References
