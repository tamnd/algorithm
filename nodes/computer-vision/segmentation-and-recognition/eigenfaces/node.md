---
tag: 22X5JB
kind: algorithm
slug: eigenfaces
name: Eigenfaces
aliases:
- Turk-Pentland face recognition
area: computer-vision/segmentation-and-recognition
level: core
summary: "Recognize aligned face images by projecting them on the leading principal components of a training set, found from a small M x M matrix, and taking the nearest class."
solves: [object-recognition]
model: real-ram
complexity:
  vars: {M: the number of training images, P: the number of pixels per image, K: the number of eigenfaces kept}
  time: {worst: O(M^2 P + M^3), average: O(M^2 P + M^3), best: O(M^2 P + M^3)}
  space: {extra: O(M P + M^2)}
properties: {deterministic: true, linear: true, supervised: true, nearest_neighbor: true}
history:
  year: 1991
  people: [Matthew Turk, Alex Pentland]
  note: "Turk and Pentland (J. Cognitive Neuroscience 1991) used the principal components of face images, which Sirovich and Kirby (1987) had introduced for face representation, for detection and recognition."
prereqs: [principal-component-analysis, covariance-matrix, nearest-neighbor-search]
see_also: [linear-discriminant-analysis, singular-value-decomposition, kernel-pca, k-nearest-neighbors, face-detection, active-appearance-model, active-shape-model, viola-jones-detector]
sources:
  - paper: doi:10.1162/jocn.1991.3.1.71
    title: "Matthew Turk and Alex Pentland, Eigenfaces for recognition, Journal of Cognitive Neuroscience 3(1), 71-86, 1991"
    locator: "The computation of the eigenfaces from the M x M matrix, the classification by distance in face space, the distance from face space, and the experiments on 16 subjects"
  - paper: doi:10.1364/JOSAA.4.000519
    title: "L. Sirovich and M. Kirby, Low-dimensional procedure for the characterization of human faces, Journal of the Optical Society of America A 4(3), 519-524, 1987"
    locator: Principal components of face images and their use to represent faces
  - paper: doi:10.1109/34.598228
    title: "Peter N. Belhumeur, Joao P. Hespanha and David J. Kriegman, Eigenfaces vs. Fisherfaces, recognition using class specific linear projection, IEEE TPAMI 19(7), 711-720, 1997"
    locator: The comparison of eigenfaces with Fisherfaces under changes of lighting and expression
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Section 14.2.1, Eigenfaces"
---

Eigenfaces is an algorithm that recognizes faces in images that are already cropped and aligned. It treats each image as one long vector of pixel values, finds the directions in which a training set of faces varies most (the principal components, which look like ghostly faces and are called *eigenfaces*), and describes each face by a few weights on these directions. A new image is recognized as the person whose average weights are nearest. Turk and Pentland (1991) also used the distance from the space of eigenfaces to decide whether an image is a face at all. The main trick is to find the eigenfaces from an $M \times M$ matrix, with $M$ the number of training images, instead of a $P \times P$ matrix, with $P$ the number of pixels.

## In plain words

Each face photo has thousands of pixels, but faces are alike: two eyes, a nose, a mouth, in about the same places. So a face can be described as the average face plus a mix of a few typical patterns. The program learns these patterns from a set of photos. They are the ways in which the photos differ most from the average.

To recognize a new photo, the program finds how much of each pattern it contains. These few numbers are like a short code for the face. The program compares the code with the codes of known people and picks the closest one. If the photo cannot be built well from the patterns at all, it is probably not a face.

## The problem

The input is a training set of $M$ face images $\Gamma_1, \dots, \Gamma_M$, each a vector of $P$ gray values, with a person label for each image, and a number $K \le M - 1$. All images have the same size, and the faces are centered and scaled the same way. The output is a model that maps a new image $\Gamma$ to a person label, to "unknown", or to "not a face". This is a case of [object recognition](/object-recognition/) by [nearest neighbor search](/nearest-neighbor-search/) in a learned space.

## The algorithm

Let $\Psi$ be the mean image and $A = [\Phi_1 \cdots \Phi_M]$ the $P \times M$ matrix of the differences $\Phi_i = \Gamma_i - \Psi$. The eigenfaces are the leading eigenvectors of the scatter matrix $A A^T$, which is $M$ times the [covariance matrix](/covariance-matrix/) of the images. This is [principal component analysis](/principal-component-analysis/) of the faces. If $A^T A v = \lambda v$, then $A A^T (A v) = \lambda (A v)$, so the eigenvectors of the small matrix $A^T A$ give those of the big one.

```pseudo id=main
EIGENFACES-TRAIN(Γ_1, ..., Γ_M, labels, K)
L1  Ψ ← (1/M) Σ_i Γ_i
L2  Φ_i ← Γ_i - Ψ for each i;  A ← [Φ_1 ... Φ_M]
L3  B ← Aᵀ A                                ▷ M × M, entries Φ_iᵀ Φ_j
L4  (λ_l, v_l) ← eigenpairs of B, with λ_1 ≥ λ_2 ≥ ...
L5  u_l ← A v_l / ‖A v_l‖ for l = 1 .. K      ▷ only λ_l > 0
L6  Ω_c ← mean of (u_1ᵀ Φ_i, ..., u_Kᵀ Φ_i) over the images i of class c
L7  return Ψ, u_1 .. u_K, Ω
```

```pseudo id=recognize
EIGENFACES-RECOGNIZE(Γ, θ_face, θ_class)
L8  ω_l ← u_lᵀ (Γ - Ψ) for l = 1 .. K
L9  ε ← ‖(Γ - Ψ) - Σ_l ω_l u_l‖              ▷ distance from face space
L10 if ε > θ_face then return "not a face"
L11 c ← the class with the least ‖ω - Ω_c‖
L12 if ‖ω - Ω_c‖ > θ_class then return "unknown"
L13 return c
```

## Example

Take four training images of $2 \times 2$ pixels, written as vectors: person a has $(8, 3, 3, 6)$ and $(6, 3, 3, 8)$, and person b has $(3, 9, 5, 3)$ and $(3, 5, 9, 3)$. The mean is $\Psi = (5, 5, 5, 5)$. The small matrix of line L3 is
$$A^T A = \begin{pmatrix} 18 & 14 & -16 & -16 \\ 14 & 18 & -16 & -16 \\ -16 & -16 & 24 & 8 \\ -16 & -16 & 8 & 24 \end{pmatrix},$$
with the eigenvalues $64, 16, 4, 0$. The eigenvalue $0$ comes from the fact that the four differences sum to zero. The first eigenface is $u_1 = (0.5, -0.5, -0.5, 0.5)$: bright corners on one diagonal, dark on the other, which is what separates a from b. Keep $K = 1$. All images of a get the weight $4$ and those of b get $-4$, so $\Omega_a = 4$ and $\Omega_b = -4$.

The new image $(7, 4, 3, 6)$ has $\Phi = (2, -1, -2, 1)$ and the weight $\omega = 3$. It is at distance $1$ from $\Omega_a$ and $7$ from $\Omega_b$, so it is person a. Its distance from face space is $\lVert \Phi - 3 u_1 \rVert = 1$.

The image $(5, 9, 9, 5)$ has $\omega = -4$, exactly $\Omega_b$. But its distance from face space is $4$, larger than for any training image. With $\theta_{\text{face}} = 2$ it is rejected as "not a face". The test file checks these numbers.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The facts that are proved:

- **Theorem (small matrix).** Each eigenpair of $A^T A$ with $\lambda > 0$ gives a unit eigenvector $A v / \sqrt\lambda$ of $A A^T$ with the same eigenvalue. These vectors are orthonormal, and every positive eigenvalue of $A A^T$ arises this way.
- **Theorem (rank).** $A A^T$ has rank at most $M - 1$, because the differences sum to zero. So there are at most $M - 1$ useful eigenfaces.
- **Theorem (best subspace).** Among all $K$-dimensional subspaces, the span of the first $K$ eigenfaces has the least total squared distance to the training differences, and that distance is the sum of the dropped eigenvalues. This is the optimality of PCA.
- **Theorem (projection).** The weights $\omega$ give the nearest point of face space, and distances between weight vectors equal distances between the projected images.

These theorems are about the computation. Whether the nearest class is the right person is an empirical question, and the answer depends on lighting, pose and alignment.

## Complexity

The cost model is the [real-RAM](/real-ram/). Eigenvalues cannot be computed exactly with a finite number of field operations in general, so line L4 is counted as an eigen solver to a fixed precision, with $O(M^3)$ operations. This is standard for the QR method and is the practical cost of the Jacobi method of `cvla.py`, which makes a few sweeps of $O(M^3)$ each.

- **Training.** Line L3 costs $O(M^2 P)$, line L4 $O(M^3)$, line L5 $O(K M P)$ and line L6 $O(M K P)$. With $K < M$, the total is $O(M^2 P + M^3)$. The extra space is $O(MP)$ for $A$ and the eigenfaces and $O(M^2)$ for $A^T A$.
- **The direct way.** The $P \times P$ matrix $A A^T$ costs $O(P^2 M)$ to build, $O(P^2)$ space and $O(P^3)$ to decompose. For $256 \times 256$ images, $P = 65536$, and $P^2$ is over 4 billion entries. The small matrix trick makes the method practical when $M \ll P$.
- **A thin SVD of $A$** gives the same eigenfaces in $O(P M^2)$ time and is better conditioned, because it does not square the singular values. See [singular value decomposition](/singular-value-decomposition/).
- **Recognition.** Line L8 costs $O(KP)$, line L9 $O(KP)$, and the search of line L11 $O(K C)$ for $C$ classes, which is at most $O(KM)$.

## Properties

- **Linear and fast.** A query costs $K$ dot products with images, plus a search over $K$-dimensional vectors.
- **Optimal for reconstruction, not for recognition.** PCA keeps the directions of largest variance. These can come from lighting rather than identity, so the first eigenfaces may describe the light. This is a heuristic observation, shown in experiments by Belhumeur, Hespanha and Kriegman (1997).
- **Needs alignment.** The pixel vectors are compared position by position, so the faces must be cropped, centered and scaled the same way.
- **Detects non-faces.** The distance from face space measures how well the image fits the model at all.
- **Unsupervised features.** The labels are used only in line L6. The eigenfaces do not depend on them.

## Variants and improvements

- **Fisherfaces** (Belhumeur, Hespanha and Kriegman 1997) project first with PCA and then with [linear discriminant analysis](/linear-discriminant-analysis/), which uses the labels to separate the classes. They report lower error rates under changes of lighting and expression. That is a benchmark result on their data.
- **Dropping the first components.** Some systems drop the first few eigenfaces to reduce the effect of lighting. This is a heuristic.
- **Modular eigenspaces.** Pentland, Moghaddam and Starner (1994) used separate eigenspaces for views and for features such as eyes and nose.
- **Probabilistic and Bayesian versions** model the variation within a person and between persons with Gaussians.
- **Kernel PCA** finds nonlinear components, see [kernel PCA](/kernel-pca/).
- **Shape and texture models.** [Active appearance models](/active-appearance-model/) apply PCA to shape and to texture after warping, which removes much of the alignment problem.
- **Modern recognition** uses deep networks trained on very large data sets. Eigenfaces remain a baseline and a teaching example.

## When to use it

Use it as a simple baseline for recognition of aligned faces, or of other aligned objects, under controlled lighting and pose, and as a first step to reduce the dimension before another classifier. Use [linear discriminant analysis](/linear-discriminant-analysis/) when labels are available and the lighting varies. For faces in the wild, use a modern learned method. For finding faces in an image, use a detector such as [Viola-Jones](/viola-jones-detector/) first.

## Pitfalls

- **Unaligned faces.** A shift of a few pixels changes the vectors much more than a change of person. Align the eyes first.
- **Lighting.** Changes of light dominate the variance. Normalize the images or use Fisherfaces.
- **Forgetting the mean.** Project $\Gamma - \Psi$, not $\Gamma$.
- **Normalizing $A v$.** $\lVert A v \rVert = \sqrt\lambda$, not $1$. Without the division the weights have the wrong scale.
- **Zero eigenvalues.** At most $M - 1$ eigenvalues are positive. An eigenvector of a zero eigenvalue gives $A v = 0$, which cannot be normalized.
- **Squaring.** Forming $A^T A$ squares the condition number. A thin SVD of $A$ avoids that.
- **Thresholds.** $\theta_{\text{face}}$ and $\theta_{\text{class}}$ must be tuned on data. With infinite thresholds every image gets a label.

## Implementations

The Python code in `impl/python/eigenfaces.py` trains the model with the small matrix of lines L1 to L7, using the symmetric eigen solver of `cvla.py`, and recognizes with lines L8 to L13. It also computes the eigenvectors of the big matrix the direct way, for the tests. The tests check the example above, the agreement of the small and the big matrix, the orthonormality of the eigenfaces, the rank bound and the exact rebuild of the training images, the identity between the residual and the dropped eigenvalues, the optimality of PCA against random subspaces, and the recognition of noisy synthetic faces.

## History

Sirovich and Kirby (1987) showed that faces can be represented well by a small number of principal components of a face set, which they called eigenpictures. Turk and Pentland (1991) used these components for recognition and detection. They added the classification by distance in face space and the distance from face space. On a database of over 2500 images of 16 people, they reported about 96% correct classification over changes of lighting, 85% over changes of head orientation and 64% over changes of size. These are benchmark results. A shorter conference version appeared at CVPR the same year. Belhumeur, Hespanha and Kriegman (1997) showed the limits of PCA under changes of lighting and proposed Fisherfaces. Eigenfaces made appearance-based recognition popular, and their ideas carried over to [active appearance models](/active-appearance-model/) and to subspace methods in general.

## References
