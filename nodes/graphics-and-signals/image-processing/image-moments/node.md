---
tag: Q8B269
kind: concept
slug: image-moments
name: Image moments
aliases:
- geometric moments
- Hu moments
- Hu moment invariants
- central moments of an image
area: graphics-and-signals/image-processing
level: advanced
summary: "Sums of x^p y^q times the pixel values: area, centroid, orientation and spread of a shape, and, after centering and scaling, Hu's seven rotation invariants."
prereqs: [digital-image, covariance-matrix]
see_also: [connected-component-labeling, image-labeling, image-thresholding, template-matching, principal-component-analysis, eigenvalue, polygon-area, shoelace-formula]
sources:
  - paper: doi:10.1109/TIT.1962.1057692
    title: Ming-Kuei Hu, Visual pattern recognition by moment invariants, IRE Transactions on Information Theory 8(2), 179 to 187, 1962
    locator: the two-dimensional moments, the central and normalized moments, and the seven invariants under translation, similitude and orthogonal transformations, with the skew invariant for mirror images
  - paper: doi:10.1016/S0031-3203(99)00127-2
    title: Jan Flusser, On the independence of rotation moment invariants, Pattern Recognition 33(9), 1405 to 1410, 2000
    locator: rotation invariants from complex moments, a basis of independent invariants, and the proof that Hu's set is dependent and incomplete
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: the chapter on feature extraction, the section on moment invariants
---

The moments of an image are the sums $m_{pq} = \sum_{x, y} x^p y^q f(x, y)$ of the pixel values $f$ weighted by powers of the coordinates. They describe a shape in a few numbers. The moment of order 0 is the area, or the total brightness; the two of order 1 give the centroid; the three of order 2 give the orientation and the spread, which are the [covariance matrix](/covariance-matrix/) of the pixel positions. Moments about the centroid, the central moments, do not change when the shape moves. Divided by a power of the area, they do not change when it is scaled either. In 1962 Ming-Kuei Hu combined them into seven numbers that also stay the same under rotation. These Hu moments were among the first features for recognizing shapes independent of position, size and orientation, and moments are still the standard way to measure the blobs found by [connected component labeling](/connected-component-labeling/).

## In plain words

Imagine the shape cut out of cardboard. The total weight of the cardboard is its area. The point where it balances on a pin is its center. If you spin it about that center, it turns easily around one direction and less easily around the other; that tells you which way it points and how long and thin it is. Moments are these numbers, worked out by adding up every pixel, each counted by how far it is from the axes. Measured from the center, they do not depend on where the shape sits. Divided by the right power of the area, they do not depend on its size. Some careful mixtures of them do not even depend on how the shape is turned. So a computer can recognize a letter or a part on a belt from a short list of numbers.

## The idea

**Raw moments.** For an image $f$ on a grid, with $x$ the column and $y$ the row, the raw moment of order $p + q$ is

$$m_{pq} = \sum_{x, y} x^p \, y^q \, f(x, y).$$

For a binary image, $m_{00}$ is the number of object pixels. The centroid is $(\bar x, \bar y) = (m_{10} / m_{00}, \; m_{01} / m_{00})$. All moments up to order $r$ cost one pass over the $N$ pixels with $O(r^2)$ products per pixel. For a polygon, the integrals can instead be taken over the boundary by Green's theorem; $m_{00}$ is then the [polygon area](/polygon-area/) from the [shoelace formula](/shoelace-formula/).

**Central moments.** The moments about the centroid are

$$\mu_{pq} = \sum_{x, y} (x - \bar x)^p (y - \bar y)^q f(x, y) = \sum_{r \le p} \sum_{s \le q} \binom{p}{r} \binom{q}{s} (-\bar x)^{p - r} (-\bar y)^{q - s} m_{rs}.$$

So $\mu_{00} = m_{00}$, $\mu_{10} = \mu_{01} = 0$, and the central moments do not change under a translation. The matrix $\frac{1}{\mu_{00}} \begin{pmatrix} \mu_{20} & \mu_{11} \\ \mu_{11} & \mu_{02} \end{pmatrix}$ is the covariance of the pixel positions. Its [eigenvalues](/eigenvalue/) $\lambda_1 \ge \lambda_2$ are the variances along the principal axes, as in [principal component analysis](/principal-component-analysis/), the angle of the major axis is $\theta = \frac{1}{2} \operatorname{atan2}(2 \mu_{11}, \mu_{20} - \mu_{02})$, and the solid ellipse with semi-axes $2 \sqrt{\lambda_1}$ and $2 \sqrt{\lambda_2}$ along these axes has the same covariance as the shape. This is the equivalent ellipse that many libraries report.

**Normalized central moments.** Scaling the plane by $s$ multiplies each area by $s^2$, so it turns $\mu_{pq}$ into $s^{p + q + 2} \mu_{pq}$ and $\mu_{00}$ into $s^2 \mu_{00}$. Dividing by the matching power of $\mu_{00}$ cancels $s$:

$$\eta_{pq} = \frac{\mu_{pq}}{\mu_{00}^{1 + (p + q)/2}}, \qquad p + q \ge 2.$$

These are invariant under translation and uniform scaling. They are not invariant under a change of contrast $f \mapsto c f$, which multiplies $\eta_{pq}$ by $c^{-(p + q)/2}$, so for gray images the values must be normalized first, or the image made binary.

**Hu's invariants.** A rotation mixes the moments of one order among themselves. Complex moments make this simple. With $c_{pq} = \sum (\tilde x + i \tilde y)^p (\tilde x - i \tilde y)^q f$ in centered coordinates, a rotation by $\phi$ multiplies $c_{pq}$ by $e^{i (p - q) \phi}$, so every product of complex moments whose indices $p - q$ add up to 0 is invariant. Normalized as above, Hu's seven invariants are

| | in normalized moments | in complex moments |
|---|---|---|
| $\varphi_1$ | $\eta_{20} + \eta_{02}$ | $c_{11}$ |
| $\varphi_2$ | $(\eta_{20} - \eta_{02})^2 + 4 \eta_{11}^2$ | $\lvert c_{20} \rvert^2$ |
| $\varphi_3$ | $(\eta_{30} - 3 \eta_{12})^2 + (3 \eta_{21} - \eta_{03})^2$ | $\lvert c_{30} \rvert^2$ |
| $\varphi_4$ | $(\eta_{30} + \eta_{12})^2 + (\eta_{21} + \eta_{03})^2$ | $\lvert c_{21} \rvert^2$ |
| $\varphi_5$ | $(\eta_{30} - 3 \eta_{12})(\eta_{30} + \eta_{12})[(\eta_{30} + \eta_{12})^2 - 3 (\eta_{21} + \eta_{03})^2] + (3 \eta_{21} - \eta_{03})(\eta_{21} + \eta_{03})[3 (\eta_{30} + \eta_{12})^2 - (\eta_{21} + \eta_{03})^2]$ | $\operatorname{Re}(c_{30} c_{12}^3)$ |
| $\varphi_6$ | $(\eta_{20} - \eta_{02})[(\eta_{30} + \eta_{12})^2 - (\eta_{21} + \eta_{03})^2] + 4 \eta_{11} (\eta_{30} + \eta_{12})(\eta_{21} + \eta_{03})$ | $\operatorname{Re}(c_{20} c_{12}^2)$ |
| $\varphi_7$ | $(3 \eta_{21} - \eta_{03})(\eta_{30} + \eta_{12})[(\eta_{30} + \eta_{12})^2 - 3 (\eta_{21} + \eta_{03})^2] - (\eta_{30} - 3 \eta_{12})(\eta_{21} + \eta_{03})[3 (\eta_{30} + \eta_{12})^2 - (\eta_{21} + \eta_{03})^2]$ | $\operatorname{Im}(c_{30} c_{12}^3)$ |

where the complex moments are computed from the normalized moments. A reflection replaces each of these products by its complex conjugate, so $\varphi_1$ to $\varphi_6$ stay and $\varphi_7$ changes sign. Hu called it the skew invariant, and it tells a shape from its mirror image. Jan Flusser showed in 2000 that the set is neither independent nor complete. It is dependent, since $\lvert c_{30} c_{12}^3 \rvert^2 = \lvert c_{30} \rvert^2 \lvert c_{21} \rvert^6$ gives $\varphi_3 \varphi_4^3 = \varphi_5^2 + \varphi_7^2$. It is incomplete, since $\varphi_2 \varphi_4^2 - \varphi_6^2 = \operatorname{Im}(c_{20} c_{12}^2)^2$ gives that invariant only up to its sign, and the sign is part of Flusser's independent basis of order 3.

**Pixels as points or as squares.** The sums above treat each pixel as a point mass at its center. A digital image is better seen as a function that is constant on unit squares, and its moments are then integrals over the squares. The two agree up to order 1 and on $\mu_{11}$ and the third order moments, but each square adds $\frac{1}{12} f(x, y)$ to $\mu_{20}$ and to $\mu_{02}$. This matters for scale. Replicating every pixel of an image into a $k \times k$ block is an exact scaling of the square model, so its $\eta_{pq}$ and Hu moments do not change. In the point model, it adds a spread inside each block, and $\eta_{20}$ becomes $\eta_{20} + \frac{k^2 - 1}{12 k^2 m_{00}}$, with the same term for $\eta_{02}$. For real images, sampling and quantization add more error of this kind, so moment invariants of a digital image are invariant only approximately, and the error is largest for small shapes and high orders.

**Exact checks.** Everything above is polynomial in the data, so it can be checked in exact arithmetic. The implementation computes the moments with fractions and the Hu invariants from complex moments. The tests check the raw and central moments against direct sums, Hu's complex form against his polynomial formulas, translation and scale invariance as exact equalities, rotation invariance with the rational rotation $\cos \phi = 3/5$, $\sin \phi = 4/5$, the sign of $\varphi_7$ under reflection, the dependence of $\varphi_3$, and the pixel replication formula.

## Examples

**An L of five pixels.** Take the binary image with object pixels $(0, 0)$, $(0, 1)$, $(0, 2)$, $(1, 2)$, $(2, 2)$, a column of three with a foot of two to the right at the bottom ($y$ grows downward).

|  | $x = 0$ | 1 | 2 |
|---|---|---|---|
| $y = 0$ | 1 | 0 | 0 |
| $y = 1$ | 1 | 0 | 0 |
| $y = 2$ | 1 | 1 | 1 |

- $m_{00} = 5$, $m_{10} = 0 + 0 + 0 + 1 + 2 = 3$ and $m_{01} = 0 + 1 + 2 + 2 + 2 = 7$, so the centroid is $(3/5, 7/5)$, inside the corner of the L.
- $\mu_{20} = \mu_{02} = 16/5$ and $\mu_{11} = 9/5$. The covariance matrix is $\frac{1}{25} \begin{pmatrix} 16 & 9 \\ 9 & 16 \end{pmatrix}$, with eigenvalues $1$ and $7/25$. Since $\mu_{20} = \mu_{02}$ and $\mu_{11} > 0$, $\theta = 45°$: the major axis runs from the top of the column to the end of the foot.
- $\mu_{30} = 54/25$, $\mu_{03} = -54/25$, $\mu_{21} = 21/25$ and $\mu_{12} = -21/25$.
- $\varphi_1 = 32/125$, $\varphi_2 = 324/15625$, $\varphi_3 = 27378/1953125$ and $\varphi_4 = 2178/1953125$. The L is its own mirror image in the line $x + y = 2$, so $\varphi_7 = -\varphi_7 = 0$.
- A quarter turn of the image gives the pixels $(0, 0)$, $(1, 0)$, $(2, 0)$, $(0, 1)$, $(0, 2)$ and exactly the same seven values.
- With pixels as unit squares, $\mu_{20} = \mu_{02} = 16/5 + 5/12 = 217/60$, so $\varphi_1 = 217/750$, while $\mu_{11}$ and all third order moments stay the same.

**Scaling a digital image.** Double every pixel of the L into a $2 \times 2$ block. In the point model $\eta_{20}$ goes from $16/125 = 0.128$ to $0.128 + \frac{3}{12 \cdot 4 \cdot 5} = 0.1405$, a change of about 10 percent for this tiny shape. In the square model the value is $217/1500$ for both images.

**Measuring blobs.** After [thresholding](/image-thresholding/) and labeling, a single pass over the label image adds $1$, $x$, $y$, $x^2$, $x y$ and $y^2$ into six sums per label. These give the area, centroid, orientation and elongation $\sqrt{\lambda_1 / \lambda_2}$ of every object at once, which is how most vision libraries report region properties.

## Where it is used

- **Region properties.** Area, centroid, orientation, equivalent ellipse and eccentricity of the components from [image labeling](/image-labeling/), in microscopy, inspection and tracking.
- **Shape recognition.** Hu proposed the invariants for visual pattern recognition, and moment invariants have been used for characters, aircraft silhouettes and industrial parts. They are cheap, but they are global, so occlusion or a touching object changes every value.
- **Normalization.** The centroid and the principal axes give a position, scale and orientation to normalize a shape before [template matching](/template-matching/) or before comparing contours.
- **Orthogonal moments.** Zernike and Legendre moments use orthogonal polynomials instead of $x^p y^q$. They are numerically better and make reconstruction possible. Zernike moments are rotation invariant in magnitude by the same phase argument as complex moments.
- **Affine invariants.** Combinations of moments that are invariant under all affine maps, not only rotations and scaling, handle shapes seen at an angle.
- **Libraries.** OpenCV computes raw, central and normalized moments of a contour or image and Hu's seven invariants. Implementations differ on the point and square models. Users often compare the logarithms of the absolute values of the Hu invariants, since the invariants span many orders of magnitude.

## References
