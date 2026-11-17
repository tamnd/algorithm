---
tag: 8615G7
kind: model
slug: active-shape-model
name: Active shape model
aliases:
- ASM
- point distribution model
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "A shape is the mean of aligned landmark sets plus a few PCA modes with bounded weights; it is fitted to an image by moving each landmark along its normal and projecting back."
history:
  year: 1995
  people: [Tim Cootes, Christopher Taylor, David Cooper, Jim Graham]
  note: "Cootes, Taylor, Cooper and Graham described the statistical shape model and its image search in Computer Vision and Image Understanding (1995), after earlier conference papers. The model can deform only in ways seen in the training set."
prereqs: [principal-component-analysis, active-contours]
see_also: [active-appearance-model, eigenfaces, principal-component-analysis, kabsch-algorithm, active-contours, face-detection, image-pyramid, template-matching]
sources:
  - paper: doi:10.1006/cviu.1995.1004
    title: "Tim F. Cootes, Christopher J. Taylor, David H. Cooper and Jim Graham, Active shape models: their training and application, Computer Vision and Image Understanding 61(1), 38-59, 1995"
    locator: "the alignment of the training shapes, the shape model x = mean + P b with limits on b, and the iterative image search"
  - paper: doi:10.1109/34.927467
    title: "Tim F. Cootes, Gareth J. Edwards and Christopher J. Taylor, Active appearance models, IEEE TPAMI 23(6), 681-685, 2001"
    locator: the shape model reused as one part of the appearance model
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Section 14.2.2, active appearance and 3D shape models"
---

An active shape model (ASM) describes a class of shapes, such as faces, hands or a bone in an X-ray, by $n$ landmark points and a statistical model of how they move together. The training shapes are aligned to remove position, rotation and size. [Principal component analysis](/principal-component-analysis/) of the aligned shapes then gives a mean shape $\bar x$ and a few modes $P$, and every allowed shape is $x = \bar x + P b$ with each weight $b_i$ kept in a range seen in training. To find the shape in a new image, each landmark moves along the normal of the outline to a better image match, and the moved points are projected back onto the model. So the model can deform only in ways that it saw in training, which is the main difference from an [active contour](/active-contours/). The [active appearance model](/active-appearance-model/) adds a model of the gray levels inside the shape.

## The machine

**Shapes.** A shape is a vector of $n$ landmarks,
$$x = (x_1, y_1, x_2, y_2, \dots, x_n, y_n)^T \in \mathbb R^{2n},$$
where landmark $j$ marks the same part of the object (a corner of an eye, the tip of a finger) in every example. The training set has $s$ shapes, marked by hand.

**Alignment.** A similarity transform $T$ (shift, rotation, scale) has no meaning for the shape, so the training shapes are first put into one frame. Each shape is aligned to a current mean by the rotation, scale and shift that minimize the sum of squared distances between landmarks, as in the [Kabsch algorithm](/kabsch-algorithm/) with a scale. The mean is then recomputed and normalized, and the process repeats until the mean stops changing. This is generalized Procrustes analysis.

**The shape model.** With the aligned shapes $x_1, \dots, x_s$, the mean $\bar x$ and the covariance
$$S = \frac1s \sum_{i=1}^s (x_i - \bar x)(x_i - \bar x)^T,$$
let $p_1, \dots, p_t$ be the eigenvectors of the $t$ largest eigenvalues $\lambda_1 \ge \dots \ge \lambda_t$, and $P = [p_1 \cdots p_t]$. The number $t$ is chosen so that the modes explain a set part of the total variance, such as 98 percent. A shape in the model frame is
$$x = \bar x + P b, \qquad b = P^T (x - \bar x),$$
and a plausible shape has $\lvert b_i \rvert \le 3 \sqrt{\lambda_i}$ for each $i$. The limit $3\sqrt{\lambda_i}$ is a rule of thumb. A shape in the image is $T(\bar x + P b)$ for a similarity $T$.

**Search.** Given a start, usually the mean shape placed near the object:

1. At each landmark of the current shape, sample the image along the normal to the outline and pick the best position on it, for example the strongest edge, or the best fit to a model of the gray-level profile learned at that landmark.
2. Find the pose $T$ and the weights $b$ such that $T(\bar x + P b)$ is nearest to the picked points. This alternates between the pose (a Procrustes fit) and $b = P^T (y - \bar x)$, where $y$ is the picked set mapped into the model frame.
3. Clamp each $b_i$ to $\pm 3 \sqrt{\lambda_i}$.
4. Repeat until the shape stops moving. In practice the search runs from coarse to fine on an [image pyramid](/image-pyramid/).

## What it counts

The model counts two errors. In training, PCA picks the $t$ modes that leave the least squared distance between the aligned shapes and their projections, and that distance is $s$ times the sum of the dropped eigenvalues. The proof is the same as for [eigenfaces](/eigenfaces/), with shapes in place of images. In search, step 2 minimizes the sum of squared distances between the model points and the points that the image suggests, over pose and $b$, and step 3 keeps the result plausible. The image term enters only through step 1. So the model does not have one global cost over the image that the search provably minimizes.

**Worked example.** Take shapes of 3 landmarks that are already in the model frame: two fixed base points $(-1, 0)$ and $(1, 0)$ and an apex. The apexes of three training shapes are $(0, 1)$, $(0.2, 1.4)$ and $(-0.2, 0.6)$. The mean apex is $(0, 1)$, and only the apex coordinates vary, with deviations $(0, 0)$, $(0.2, 0.4)$ and $(-0.2, -0.4)$. The covariance has one nonzero eigenvalue, $\lambda_1 = (0.04 + 0.16 + 0.04 + 0.16)/3 = 0.1333$, with the mode $p_1 = (1, 2)/\sqrt5$ on the apex coordinates. So one mode explains all of the variance, and the limit is $3\sqrt{0.1333} = 1.0954$.

- The picked apex $(0.5, 1)$ has $b_1 = 0.5/\sqrt5 = 0.2236$, inside the limit. The model shape has the apex $(0, 1) + 0.2236\, p_1 = (0.1, 1.2)$. The model cannot move the apex sideways alone, because in training a move to the side always came with a change of height.
- The picked apex $(2, 4)$ has $b_1 = (2 + 6)/\sqrt5 = 3.578$, outside the limit. Clamping gives $b_1 = 1.0954$ and the apex $(0.4899, 1.9798)$.

## Relation to other models

- **Active contours.** A [snake](/active-contours/) has a generic smoothness prior and can take any smooth shape. An ASM has a prior learned from examples and can take only shapes near the span of its modes.
- **Eigenfaces.** [Eigenfaces](/eigenfaces/) apply PCA to the pixel values of aligned images. The ASM applies PCA to landmark positions, so it models geometry, not intensity.
- **Active appearance model.** The [AAM](/active-appearance-model/) combines this shape model with a PCA model of the texture in a shape-free frame, and fits both to the whole image region instead of to profiles at the landmarks.
- **Template matching.** [Template matching](/template-matching/) searches over a rigid template and its pose. The ASM adds the $t$ shape weights to the pose.
- **3D models.** The same construction on 3D landmarks or meshes gives the statistical shape models of medical imaging and the 3D morphable models of faces.

## Known results in the model

- **Best linear subspace** (theorem). Among all $t$-dimensional subspaces through $\bar x$, the span of $p_1, \dots, p_t$ has the least sum of squared distances to the aligned training shapes, and that sum is $s \sum_{i > t} \lambda_i$. This is the PCA theorem; see the proof on the [eigenfaces](/eigenfaces/) page.
- **Projection** (theorem). For fixed pose, $b = P^T (y - \bar x)$ gives the model shape nearest to $y$ in the model frame, because $P$ has orthonormal columns.
- **Rank** (theorem). $S$ has rank at most $s - 1$, because the deviations from the mean sum to zero. If the alignment fixes the centroid, the rotation and the scale by linear conditions, as when the aligned shapes are projected into the tangent space at the mean, the deviations also satisfy 4 linear constraints (2 for the shift, 1 for the rotation, 1 for the scale). Then at most $\min(s - 1, 2n - 4)$ modes have a positive eigenvalue.
- **Limits of $3\sqrt{\lambda_i}$** (heuristic). If the weights were Gaussian, each would lie within $3$ standard deviations with probability about 0.997. The shapes need not be Gaussian, and the limit on each $b_i$ alone allows the corners of a box, which are less likely than the bound suggests. A limit on $\sum_i b_i^2 / \lambda_i$ is a common alternative.
- **Search** (heuristic). The search is a local method. It needs a start near the object, and it can stop at a wrong edge. No convergence to a global optimum is claimed.
- **Benchmark results.** Cootes and others report search results on medical images and faces. The accuracy depends on the data, the start and the number of training shapes, so the published numbers are benchmark results, not bounds.

## References
