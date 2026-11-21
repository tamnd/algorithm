---
tag: 41Z2MF
kind: algorithm
slug: common-lines-method
name: Common lines method
aliases:
- angular reconstitution
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: Find the relative orientations of projection images from the lines along which pairs of their 2D Fourier transforms agree, as the slice theorem requires.
model: real-ram
complexity:
  vars: {m: "the number of images", n: "the side of an n x n image", a: "the number of angles in the sinogram of one image", d: "the number of bins in one line projection"}
  time: {per_iteration: "O(a^2 d)", total: "O(m a n^2 + m^2 a^2 d + m^4)"}
  space: {extra: "O(a n^2 + m a d + m^2)"}
properties: {deterministic: true, iterative: false, exact_on_exact_lines: true, handedness_resolved: false, needs_three_images: true, in_place: false, recursive: false}
history:
  year: 1987
  people: [Marin van Heel]
  note: "Crowther, DeRosier and Klug (1970) used central sections of the 3D Fourier transform for reconstruction from electron micrographs; van Heel (1987) assigned the projection directions of unknown views from their common lines and named the method angular reconstitution."
prereqs: [fourier-slice-theorem, radon-transform, sinogram]
see_also: [single-particle-reconstruction, rotation-averaging, kabsch-algorithm, wahba-problem, power-iteration, semidefinite-programming, euler-rotation-theorem, cross-correlation]
sources:
  - paper: doi:10.1098/rspa.1970.0119
    title: R. A. Crowther, D. J. DeRosier and A. Klug, The reconstruction of a three-dimensional structure from projections and its application to electron microscopy, Proceedings of the Royal Society of London A 317(1530), 1970
    locator: pp. 319 to 340 (reconstruction from projections through central sections of the Fourier transform; general locator, section not confirmed)
  - paper: doi:10.1016/0304-3991(87)90078-7
    title: M. van Heel, Angular reconstitution, a posteriori assignment of projection directions for 3D reconstruction, Ultramicroscopy 21(2), 1987
    locator: pp. 111 to 123 (the orientations of unknown projections from their common lines)
  - paper: doi:10.1137/090767777
    title: A. Singer and Y. Shkolnisky, Three-dimensional structure determination from common lines in cryo-EM by eigenvectors and semidefinite programming, SIAM Journal on Imaging Sciences 4(2), 2011
    locator: pp. 543 to 572 (all common lines at once, by an eigenvector method and by a semidefinite relaxation)
  - book: isbn:9780195182187
    title: J. Frank, Three-Dimensional Electron Microscopy of Macromolecular Assemblies, Oxford University Press, 2006
    locator: general locator (the single-particle methods, angular reconstitution among them)
---

The common lines method finds the orientations of 2D projection images of one 3D object when the orientations are not known. It is a basic step of [single-particle reconstruction](/single-particle-reconstruction/) in cryo-electron microscopy. By the [Fourier slice theorem](/fourier-slice-theorem/), the 2D Fourier transform of each image is a central plane of the 3D Fourier transform of the object. Two central planes meet in a line through the origin, so any two images share one line of Fourier values, their common line. In real space the same fact says that two images have one pair of equal line projections. The method finds the common line of each pair of images by a search in their [sinograms](/sinogram/). From the common lines of three images it computes their relative rotations exactly, and from these it places the other images one by one. The data fix the rotations only up to a global rotation and up to a reflection: the mirror image of the object gives the same images, so the handedness stays open.

## In plain words

A microscope takes flat shadow pictures of many copies of one molecule. Each copy lies in an unknown direction. To build the 3D shape, you first need to know how each picture is turned.

Any two shadow pictures of one object have one thing in common. If you squash each picture onto a line at the right angle, the two squashed profiles are the same, because both show the object squashed onto one direction in space. The method searches each pair of pictures for this matching pair of angles.

The matching angles of three pictures fix how the three are turned against each other, like three hinged plates. Each further picture is then placed from two pictures that are already placed. One question stays open: a mirror copy of the molecule gives exactly the same pictures, so the pictures alone cannot tell left from right.

## The problem

There is a density $f$ on $\mathbb{R}^3$ and there are $m \ge 3$ unknown rotations $R_1, \dots, R_m$. The input is the images
$$P_i(x, y) = \int f\big(R_i (x, y, z)^T\big)\, dz, \qquad i = 1, \dots, m,$$
sampled on $n \times n$ grids. The columns of $R_i$ are the image axes and the beam direction $\nu_i = R_i e_3$, written in the frame of the object. An $n \times n$ image covers $[-1, 1]^2$, with the pixel centers $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$; the images must be centered, so that the origin of the object projects to the center of every image. The output is rotations $\hat R_1, \dots, \hat R_m$ with $\hat R_i^T \hat R_j = R_i^T R_j$ for all pairs, or the same with every $R_i$ replaced by $J R_i J$, where $J = \mathrm{diag}(1, 1, -1)$.

**Common lines.** For a unit vector $c$ in the image plane, let $p_i(c, s) = \int P_i(s c + t c^\perp)\, dt$ be the line projection of image $i$ in the direction $c$, one line of its sinogram. If $\nu_i \ne \pm \nu_j$, the unit vector $q$ along $\nu_i \times \nu_j$ lies in both central planes. In the coordinates of image $i$ it is the direction $c_{ij} = (R_i^T q)_{1,2}$, and in image $j$ it is $c_{ji} = (R_j^T q)_{1,2}$. Then
$$p_i(c_{ij}, s) = p_j(c_{ji}, s) \quad \text{for all } s,$$
because both sides are the integral of $f$ over the plane $\{x : x \cdot q = s\}$, that is the 3D [Radon transform](/radon-transform/) of $f$ at $(q, s)$ (a theorem, proved in the correctness proof). In Fourier space, with $\mathcal{F} g(\xi) = \int g(x) e^{-2\pi i x \cdot \xi}\, dx$, the 1D transform of this line projection is $\mathcal{F} f$ on the line through the origin in the direction $q$. A line in the direction $-c$ is the line in the direction $c$ read in reverse, so a search over the angles $[0, \pi)$ must also try each line of the second image reversed.

## The algorithm

$\mathrm{FRAME}(u, v)$ is the rotation with the columns $u/|u|$, the unit vector along the part of $v$ orthogonal to $u$, and the cross product of these two. A 2D direction $c$ is used as the 3D vector $(c_1, c_2, 0)$. The angle $\omega(\alpha)$ is the direction $(\cos\alpha, \sin\alpha)$.

```pseudo id=main
COMMON-LINES(P_1..P_m, a)
L1  S_i ← the line projections of P_i at the angles πl/a, l = 0..a-1, for each i
L2  for each pair i < j, find the line α of S_i and the line β of S_j, forward or reversed, with the smallest distance, refined by a parabola
L3      c_ij ← ω(α); c_ji ← ω(β), or -ω(β) for a reversed match
L4  pick the triple (r, b, d) whose smallest |sin| between the two common lines in any of its three images is largest
L5  q_rb ← c_rb; q_rd ← c_rd                                  ▷ R_r = I
L6  q_bd ← the unit vector with q_bd·q_rb = c_br·c_bd, q_bd·q_rd = c_dr·c_db and third coordinate ≥ 0
L7  R_b ← FRAME(q_rb, q_bd) FRAME(c_br, c_bd)^T; R_d ← FRAME(q_rd, q_bd) FRAME(c_dr, c_db)^T
L8  while some image has no rotation, pick an unplaced k and placed u, v with the largest |sin| between c_ku and c_kv
L9      R_k ← FRAME(R_u c_uk, R_v c_vk) FRAME(c_ku, c_kv)^T
L10 return R_1..R_m
```

Line L6 is the triangle step. In the frame of image $r$, the common directions $q_{rb}$ and $q_{rd}$ lie in the plane $z = 0$, and the unknown $q_{bd}$ has known dot products with both, because the angle between two common lines inside image $b$ is the angle between the corresponding directions in space. Two linear equations give the first two coordinates of $q_{bd}$, and its length 1 gives the third up to the sign. The sign is the handedness, and the algorithm takes the positive one. Line L9 maps the two known directions $c_{ku}$, $c_{kv}$ of image $k$ to their known places $R_u c_{uk}$, $R_v c_{vk}$ in space; a rotation is fixed by where it sends two independent vectors.

## Example

**By hand.** Take $R_1 = I$, $R_2$ the rotation by 90 degrees about the $x$ axis, and $R_3$ the rotation by 90 degrees about the $y$ axis. The beams are $\nu_1 = e_3$, $\nu_2 = (0, -1, 0)$ and $\nu_3 = (1, 0, 0)$. The common directions are $q_{12} = e_1$, $q_{13} = e_2$ and $q_{23} = e_3$. In the images they are $c_{12} = (1, 0)$, $c_{21} = (1, 0)$, $c_{13} = (0, 1)$, $c_{31} = (0, 1)$, $c_{23} = (0, 1)$ and $c_{32} = (-1, 0)$. Line L5 gives $q_{12} = e_1$ and $q_{13} = e_2$. In line L6, $c_{21} \cdot c_{23} = 0$ and $c_{31} \cdot c_{32} = 0$, so $q_{23}$ is orthogonal to $e_1$ and $e_2$, and the positive sign gives $q_{23} = e_3$. Line L7 gives
$$R_2 = \mathrm{FRAME}(e_1, e_3)\, \mathrm{FRAME}(e_1, e_2)^T = [e_1, e_3, -e_2] = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix},$$
the true rotation about $x$, and in the same way $R_3 = \mathrm{FRAME}(e_2, e_3)\, \mathrm{FRAME}(e_2, -e_1)^T$, the true rotation about $y$. The negative sign would give $J R_2 J$ and $J R_3 J$, the answer for the mirror image of the object.

**From images (a measurement).** The tests use a density of 6 Gaussian blobs with random weights, centers in $[-0.45, 0.45]^3$ and widths from 0.12 to 0.2, and 5 random rotations (seed 1). Each image is $32 \times 32$, with $a = 60$ angles (3 degree steps) and $d = 23$ bins. The 10 common lines found in the sinograms are within 0.25 to 1.40 degrees of the true ones, with the right signs. The rotations after removing the global rotation and the reflection are within 0.26, 0.68, 0.91 and 1.00 degrees of the truth (the comparison is relative to the first image, so its error is 0). With only the first three images, the error is 1.35 degrees. With exact common lines, the error is below $10^{-15}$ radians.

## Correctness

The [correctness proof](proofs/correctness.md) proves the common-line identity above. It then proves that lines L4 to L9 are exact: if the common lines are exact, no two beams are equal or opposite, and the beams of some three images are linearly independent, the output is $\hat R_i = G R_i$ for all $i$ or $\hat R_i = J G R_i J$ for all $i$, with one rotation $G$ (a theorem). The key facts are that $\mathrm{FRAME}(T u, T v) = T\, \mathrm{FRAME}(u, v)$ for a rotation $T$, and $\mathrm{FRAME}(J u, J v) = J\, \mathrm{FRAME}(u, v)\, J$. The proof also shows that the reflection cannot be resolved from the images: the images of $f(J x)$ at the rotations $J R_i J$ are the images of $f$ at $R_i$. So three images in general position fix the orientations up to a global rotation and the handedness, and no more data of this kind can fix the handedness. The search for the lines in lines L1 to L3 is not exact; its accuracy is a measurement.

## Complexity

In the real-RAM model, let $m$ be the number of images, $n$ the image side, $a$ the number of sinogram angles and $d$ the number of bins. Line L1 builds one projector with $O(a n^2)$ entries and applies it to every image, $O(m a n^2)$. Line L2 compares $a$ lines with $2a$ lines for each of the $m(m-1)/2$ pairs, $O(a^2 d)$ per pair (the per-iteration cost in the front matter) and $O(m^2 a^2 d)$ in all; this is the main cost for small $m$. Line L4 is $O(m^3)$. The code scans all unplaced images and all placed pairs at each of the $m$ steps of line L8, $O(m^4)$ in total; keeping the best pair of each unplaced image and updating it when one image is placed makes it $O(m^3)$. Lines L5 to L7 and L9 are $O(1)$ each. Memory is $O(a n^2)$ for the projector, $O(m a d)$ for the sinograms and $O(m^2)$ for the common lines. On the example above, one run takes about 0.5 s in pure Python (a measurement on a loaded machine).

## Properties

- **Exact on exact lines.** With exact common lines and beams in general position, the output is exact up to a global rotation and the reflection (a theorem).
- **Handedness open.** The method returns one of two mirror solutions; the images cannot tell which is right (a theorem). The choice must come from other data, such as tilted pairs of images or known features of the reconstructed map.
- **Needs at least three images.** Two images fix only the angle between their beams and the common line, not the full relative rotation.
- **No reference.** The method needs no starting model, so it can give the first model of an unknown structure.
- **Greedy.** Each image uses only two common lines, so an error in one line passes to the images placed after it.
- **Deterministic.** The same images give the same output.

## Variants and improvements

- **Fourier-space search.** The common line can be found by comparing central lines of the 2D Fourier transforms of the images, often with weights for each frequency, in place of the real-space line projections. By the slice theorem the two searches look for the same line.
- **All common lines at once.** Singer and Shkolnisky (2011) put the common lines of all pairs into one matrix whose top eigenvectors give all rotations together, and a [semidefinite](/semidefinite-programming/) relaxation of the same least squares problem. These methods use every pair, so a few wrong lines do not spoil the result, and they can work at noise levels where the greedy method fails. The top eigenvectors come from [power iteration](/power-iteration/) or a Lanczos method.
- **Voting.** Each third image votes for the angle between two beams that its common lines imply; the most voted angle is used for each pair. This keeps the triangle step and reduces the effect of wrong lines.
- **Refinement.** The rough orientations become the start of a refinement by projection matching or by maximum likelihood, which uses the whole images and not only the common lines.
- **Symmetric particles.** For particles with point group symmetry, one image has common lines with itself, and the orientation of a single image can be found. Icosahedral viruses were an early use of this.
- **Rotation averaging.** The relative rotations from many triangles can be combined by [rotation averaging](/rotation-averaging/), the same problem as in structure from motion.

## When to use it

Use the common lines method when the orientations of projection images are unknown and no reference model exists, the images have a good signal-to-noise ratio (in cryo-EM, after averaging similar images into class averages), and the particle has no strong preferred orientation that puts all beams in one plane. When a reference model exists, matching the images against its projections is more robust. With raw noisy single images, use the global eigenvector or semidefinite methods, or a maximum likelihood method such as expectation maximization over the orientations.

## Pitfalls

- **Noise.** The search for each line is a minimum over $2a^2$ distances and breaks down quickly with noise. On the example above with Gaussian noise added to the pixels (three noise seeds per level, a measurement): with a standard deviation of 1 percent of the image peak, 30 of 30 lines are within 5 degrees and the rotations within 1.1 to 1.8 degrees; with 3 percent, 28 of 30 lines and rotations within 2.6 to 11.8 degrees; with 5 percent, 21 of 30 lines and errors of 36 to 74 degrees; with 10 percent, 7 of 30 lines and errors above 68 degrees. Raw cryo-EM images are far noisier than this.
- **A badly shaped anchor triangle.** If the beams of the three anchor images are nearly in one plane, or the two common lines inside an image are nearly parallel, the triangle step divides by a small number and small line errors become large rotation errors. With a fixed anchor (the first three images, and every other image placed from the first two), 20 random cases of the example type gave a median error of 10.9 degrees and a largest error of 108.6 degrees, with 4 cases above 20 degrees. With the choice of lines L4 and L8, the same cases gave a median of 3.5 degrees, a largest error of 19.6 degrees, and none above 20 degrees (a measurement).
- **Beams in one plane.** If all beams lie in one plane, as in a single-axis tilt series, every pair has the same common direction, the axis, and the rotations about the axis cannot be found (a theorem). The code raises an error in this case.
- **The reversed line.** The line at angle $\alpha + \pi$ is the line at $\alpha$ read in reverse. A search over $[0, \pi)$ that does not try the reversed lines finds the wrong line, or the right line with the wrong sign, for every pair whose match needs the reversal.
- **Centering.** A shift of an image shifts its line projections, by a different amount at each angle. The common-line identity holds only for centered images, so the images must be centered first.
- **Comparing with the truth.** An error measure must remove both the global rotation and the reflection. Comparing $\hat R_i$ with $R_i$ directly reports large errors for correct answers.

## Implementations

The Python code takes the images, the number of angles $a$ and the number of bins $d$. It builds the sinograms with the pixel-driven projector of the shared helper `imgkit`, searches the common line of every pair with the parabola refinement, and then runs lines L4 to L9. It also has helpers for test data: random rotations from random unit quaternions, the exact projection of Gaussian blobs, and the exact common lines of two rotations. The tests check that $\mathrm{FRAME}$ commutes with rotations, that the exact common lines satisfy $R_i c_{ij} = R_j c_{ji}$, the hand example, exact rotations from exact lines for 3, 4 and 8 images, that a global rotation does not change the lines, that the mirror object gives the same images, the error for coplanar beams and for fewer than 3 images, and the accuracy of the lines and the rotations found from the images of the example.

## History

Crowther, DeRosier and Klug (1970) set out the reconstruction of a 3D structure from electron micrographs through central sections of its Fourier transform, and the common lines between central sections were used to find the orientations of images of symmetric virus particles. Van Heel (1987) gave angular reconstitution, which assigns the projection directions of images of an asymmetric particle a posteriori from their common lines, found in the sinograms of the images. Frank's book (2006) describes the method in the context of single-particle cryo-EM. Singer and Shkolnisky (2011) replaced the triangle steps by an eigenvector method and a semidefinite relaxation that use all common lines at once.

## References
