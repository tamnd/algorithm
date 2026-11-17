---
tag: 25W3H2
kind: model
slug: active-appearance-model
name: Active appearance model
aliases:
- AAM
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "A PCA model of landmark shape and of the texture warped to the mean shape, fitted to an image by updates computed from the texture residual."
history:
  year: 1998
  people: [Tim Cootes, Gareth Edwards, Christopher Taylor]
  note: "Cootes, Edwards and Taylor presented active appearance models at ECCV 1998 and in IEEE TPAMI (2001). Matthews and Baker (IJCV 2004) recast the fit as inverse compositional image alignment."
prereqs: [active-shape-model, eigenfaces, lucas-kanade-method]
see_also: [active-shape-model, eigenfaces, inverse-compositional-alignment, lucas-kanade-method, image-warping, delaunay-triangulation, gauss-newton-algorithm, face-detection]
sources:
  - paper: doi:10.1109/34.927467
    title: "Tim F. Cootes, Gareth J. Edwards and Christopher J. Taylor, Active appearance models, IEEE TPAMI 23(6), 681-685, 2001"
    locator: "the combined model of shape and gray levels, and the search with a linear update learned from known displacements"
  - paper: doi:10.1023/B:VISI.0000029666.37597.d3
    title: "Iain Matthews and Simon Baker, Active appearance models revisited, International Journal of Computer Vision 60(2), 135-164, 2004"
    locator: "the independent and combined models, the inverse compositional fit with the appearance projected out, and the analysis of the fixed linear update"
  - paper: doi:10.1006/cviu.1995.1004
    title: "Tim F. Cootes, Christopher J. Taylor, David H. Cooper and Jim Graham, Active shape models: their training and application, Computer Vision and Image Understanding 61(1), 38-59, 1995"
    locator: the shape model that the appearance model reuses
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Section 14.2.2, active appearance and 3D shape models"
---

An active appearance model (AAM) describes a class of objects, most often faces, by two linear models. The first is the landmark shape model of the [active shape model](/active-shape-model/). The second is a model of the texture, the gray levels or colors inside the object after a warp to the mean shape, built with [principal component analysis](/principal-component-analysis/) as in [eigenfaces](/eigenfaces/). A few parameters then produce a whole synthetic image of the object. To fit the model to a new image, the parameters are changed so that the synthetic image matches the image region under the current shape. Cootes, Edwards and Taylor (1998, 2001) predicted each change from the residual with a fixed linear map learned in training. Matthews and Baker (2004) showed that this map is only an approximation, and fitted the model instead with [inverse compositional alignment](/inverse-compositional-alignment/), a form of [Lucas-Kanade](/lucas-kanade-method/) image alignment.

## The machine

**Shape.** As in the active shape model, a shape is a vector $x$ of $n$ landmarks, the training shapes are aligned, and
$$x = \bar x + P_s b_s,$$
with $P_s$ the leading eigenvectors of the shape covariance.

**Texture.** The mean shape is split into triangles, for example by a [Delaunay triangulation](/delaunay-triangulation/) of its landmarks. Each training image is warped from its own landmarks to the mean shape, one affine map per triangle (a piecewise affine [warp](/image-warping/)), and the pixels inside the mean shape are read into a vector $g$ of length $N$. Each $g$ is normalized for brightness and contrast. PCA of these vectors gives
$$g = \bar g + P_g b_g.$$
So the texture of every example is compared in the same frame, and shape changes do not leak into the texture model.

**Combined model** (Cootes and others). Shape and texture weights are correlated, for example a smile changes both. The vector $(W_s b_s, b_g)$, with a diagonal $W_s$ that puts shape and texture in comparable units, goes through a third PCA, $(W_s b_s, b_g) = Q c$. Then one vector $c$ controls both:
$$x = \bar x + P_s W_s^{-1} Q_s c, \qquad g = \bar g + P_g Q_g c.$$
Matthews and Baker call the model without the third PCA an independent AAM, with separate shape weights $p$ and appearance weights $\lambda$.

**Synthesis.** For parameters $c$ and a pose $t$ (a similarity transform), the model texture $g$ is warped from the mean shape to the shape $x$ placed by $t$. This gives an image of the object.

**Fit by a learned update** (Cootes, Edwards and Taylor). Let $g_s$ be the image texture sampled under the current shape and warped back to the mean shape, and $r = g_s - g_m$ the residual against the model texture. The method assumes that the parameter error is a linear function of the residual, $\delta p = -R\, r$, with one matrix $R$ for all images. $R$ is found in training by moving the parameters of training images by known amounts and fitting the residuals with linear regression. In search, each step applies $\delta p$; if the error $\lVert r \rVert^2$ does not fall, smaller steps along the same direction are tried. The search runs from coarse to fine on an [image pyramid](/image-pyramid/).

**Fit by inverse compositional alignment** (Matthews and Baker). For an independent AAM with appearance basis images $A_1, \dots, A_m$, orthonormal, and the mean appearance $A_0$, the fit minimizes
$$\sum_{u} \Big[ A_0(u) + \sum_i \lambda_i A_i(u) - I(W(u; p)) \Big]^2$$
over the shape weights $p$ and the appearance weights $\lambda$. The appearance is projected out, so the cost in $p$ alone is the same sum restricted to the orthogonal complement of the span of the $A_i$. This cost is minimized by inverse compositional [Gauss-Newton](/gauss-newton-algorithm/) steps with a Hessian that is computed once.

## What it counts

The model counts the squared difference between the image region under the shape and the texture that the model synthesizes, measured in the frame of the mean shape. Training minimizes squared reconstruction errors of shapes and textures over linear subspaces, so each PCA is optimal in the sense of the [eigenfaces](/eigenfaces/) theorem. Fitting is a local search on a nonconvex cost, so it finds a local minimum near the start.

**Worked example of project-out.** Take a texture of $N = 3$ pixels, one appearance mode $A_1 = (1, 1, 1)/\sqrt3$, and the error image $E = I(W(u; p)) - A_0 = (3, 1, 2)$ at the current $p$. The best appearance weight is $\lambda_1 = A_1 \cdot E = 6/\sqrt3 = 3.4641$, which explains the part $(2, 2, 2)$, a uniform rise in brightness. What is left is $(1, -1, 0)$, with squared norm 2. Projecting out gives the same vector directly: $E - A_1 (A_1 \cdot E) = (1, -1, 0)$. The shape step then works only on this part, so a change of brightness alone does not move the landmarks.

## Relation to other models

- **Active shape model.** The [ASM](/active-shape-model/) uses the same shape model but looks only at profiles near the landmarks. The AAM uses all pixels inside the shape.
- **Eigenfaces.** The texture model is [eigenfaces](/eigenfaces/) computed after a warp to the mean shape, so that the pixels of different faces correspond.
- **Image alignment.** With no shape modes beyond the pose and no appearance modes, the fit is [Lucas-Kanade](/lucas-kanade-method/) alignment of a fixed template. The inverse compositional fit is the [inverse compositional](/inverse-compositional-alignment/) algorithm with a linear appearance model.
- **3D morphable models.** Blanz and Vetter built the same kind of linear model of shape and texture on 3D face scans, fitted through a camera and a lighting model.
- **Learned landmark detectors.** Later face landmark methods, such as cascades of regressors and deep networks, learn the map from image to landmarks directly and keep the linear shape model only as a prior, or not at all.

## Known results in the model

- **Project-out** (theorem). For orthonormal $A_1, \dots, A_m$, the minimum of the cost above over $\lambda$, for a fixed $p$, is the squared norm of the error image projected onto the orthogonal complement of the span of the $A_i$, and the best $\lambda_i$ is $A_i \cdot (I(W(\cdot; p)) - A_0)$. This is the projection theorem of linear least squares, and the worked example above is one case.
- **The fixed update is an approximation** (an argument of Matthews and Baker 2004, not a bound). The learned update assumes that the relation between the residual and the parameter error is the same at all parameters and for all images. In general the gradient of the residual depends on the current shape and on the appearance, so no single $R$ is exact.
- **Piecewise affine warps are not a group** (theorem). The composition of two piecewise affine warps on the same triangles is in general not a piecewise affine warp on those triangles, so the inverse compositional step needs a first order approximation of the composition. The algorithm is then not exactly the inverse compositional algorithm of Baker and Matthews, and the convergence results for that algorithm do not carry over unchanged.
- **Cost per iteration** (derived bound, real-RAM, $N$ pixels, $n$ shape weights). With the steepest descent images and the Hessian computed once, an iteration of the project-out fit warps the image ($O(N)$), forms the error ($O(N)$), multiplies by the steepest descent images ($O(n N)$), and solves with the fixed $n \times n$ inverse ($O(n^2)$). The update of the warp does not depend on $N$. This gives $O(n N + n^2)$ per iteration, independent of the number of appearance modes. The number of iterations has no bound.
- **Benchmark results.** Matthews and Baker report that their fit is faster and converges more often than the learned update on their face data. Cootes and others report fits of faces and medical images. All of these are benchmark results on the data in those papers.

## References
