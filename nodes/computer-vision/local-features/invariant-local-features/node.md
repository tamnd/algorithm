---
tag: MX501M
kind: concept
slug: invariant-local-features
name: Covariant and invariant local features
aliases:
- feature invariance
- affine covariant regions
area: computer-vision/local-features
level: core
summary: A detector is covariant when its regions move with the image under a class of transformations, and a descriptor is invariant when its value does not change under them.
prereqs: [feature-detection, scale-space-representation]
see_also: [detector-repeatability, automatic-scale-selection, harris-affine-detector, maximally-stable-extremal-regions, feature-descriptor, sift, homography, affine-camera-model]
sources:
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the introduction (local features, invariance and covariance, and the properties of a good feature)
  - paper: doi:10.1007/s11263-005-3848-x
    title: Krystian Mikolajczyk, Tinne Tuytelaars, Cordelia Schmid, Andrew Zisserman, Jiri Matas, Frederik Schaffalitzky, Timor Kadir and Luc Van Gool, A comparison of affine region detectors, International Journal of Computer Vision 65(1-2), 43-72, 2005
    locator: the introduction (why affine covariant regions model a local change of viewpoint) and the section on the detectors
  - paper: doi:10.1023/B:VISI.0000027790.02288.f2
    title: Krystian Mikolajczyk and Cordelia Schmid, Scale and affine invariant interest point detectors, International Journal of Computer Vision 60(1), 63-86, 2004
    locator: Section 3 (the affine normalization of a region by its second moment matrix)
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: Section 5 (the orientation assignment) and Section 6 (the descriptor computed in the frame of the keypoint)
  - paper: doi:10.1023/A:1008045108935
    title: Tony Lindeberg, Feature detection with automatic scale selection, International Journal of Computer Vision 30(2), 79-116, 1998
    locator: the sections on the scale invariance of the extrema of normalized derivatives
---

A local feature is a small region of an image, found by a detector, together with a descriptor that summarizes the image inside it. Let $T$ be a transformation of the image plane, such as a shift, a turn, a change of scale or an affine map, and let $f \circ T^{-1}$ be the image $f$ moved by $T$. A detector is *covariant* with a class of transformations when it finds the moved regions in the moved image: if it finds the region $R$ in $f$, it finds $T(R)$ in $f \circ T^{-1}$. A descriptor is *invariant* when it gives the same value for $R$ in $f$ and for $T(R)$ in $f \circ T^{-1}$. Covariance of the detector and invariance of the descriptor together let a program match the same piece of a scene in two photographs taken from different places, at different zoom or in different light. The usual word "invariant feature" means this pair of properties.

## In plain words

Two photographs of one building, taken from two places, show the same windows at different positions, sizes and angles. A good feature finder marks the same windows in both photographs, and its marks move, grow and turn with the windows. That is covariance. Then each mark gets a short summary of what is inside it. A good summary gives the same answer in both photographs, because it was measured inside the mark, after the mark was turned and scaled to a standard size. That is invariance. The price is that the summary cannot see what the standard form removed: a summary that ignores turning cannot tell a 6 from a 9.

## The idea

**Classes of transformations.** The useful classes form groups, each one inside the next:

| class | parameters | what a region must carry |
|---|---|---|
| translation | 2 | a position |
| translation and rotation | 3 | a position and an orientation |
| similarity | 4 | a position, a scale and an orientation |
| affine | 6 | a position, an ellipse and an orientation |
| [homography](/homography/) | 8 | a position and a full projective frame |

There are photometric classes too: an offset $I \mapsto I + b$, an affine change $I \mapsto aI + b$ with $a > 0$, and any increasing map of the gray values.

**Why the affine class.** A smooth surface is close to a plane in a small region, and two views of a plane differ by a homography. In a small region a homography is close to its first-order part, which is an [affine map](/affine-camera-model/). So affine covariance is the local model of a change of viewpoint. Full projective covariance is rarely needed for small regions.

**Covariance by construction.** A detector is covariant when it is built only from operations that are themselves covariant. Derivatives at a point turn with the image, so the eigenvalues of a $2 \times 2$ matrix of derivatives, as in the Harris or the Shi-Tomasi measure, do not change under rotation, and their maxima move with the image. [Automatic scale selection](/automatic-scale-selection/) makes the scale covariant: a structure $s$ times larger is found at a scale $s^2$ times larger in $t = \sigma^2$. Affine shape adaptation in [Harris-affine](/harris-affine-detector/) makes the ellipse covariant. [MSER](/maximally-stable-extremal-regions/) is covariant by its definition, because a connected component of a threshold set is mapped by any continuous map to the connected component of the mapped set.

**Invariance by normalization.** A covariant region defines a frame. Map the region to a fixed standard form, such as a disk of radius 1 with its orientation along the first axis, and compute the descriptor there. Two corresponding regions then give the same standard patch, so any descriptor computed on it is invariant. [SIFT](/sift/) does this for the similarity class with a position, a scale and a dominant gradient orientation. For an ellipse $\{\mathbf x : \mathbf x^\top \Sigma^{-1} \mathbf x \le 1\}$ the map $\Sigma^{-1/2}$ sends the ellipse to the unit disk. Under an affine map $A$ the ellipse becomes $\Sigma' = A \Sigma A^\top$, and the two normalized frames differ by the matrix $\Sigma'^{-1/2} A \Sigma^{1/2}$, which is orthogonal because its product with its transpose is $\Sigma'^{-1/2} A \Sigma A^\top \Sigma'^{-1/2} = I$. So the ellipse removes the affine map up to a rotation, and a dominant orientation removes the rest.

**Photometric invariance.** Derivatives do not see an offset $b$, so derivative based detectors are invariant to it. A gain $a$ multiplies a measure of order $M$ in the derivatives by $a^M$, which keeps the order of the responses but changes which ones pass a fixed threshold. A descriptor normalized to mean $0$ and length $1$ is invariant to the affine change $aI + b$. The set of extremal regions of MSER does not change under any increasing map of the gray values.

**The trade-off.** Each invariance removes information. A larger class needs more parameters per region, and each estimated parameter adds noise; an affine frame is less stable than a similarity frame when the true change is only a rotation and a scale. A detector should be covariant with the class that the application needs, and no larger.

## Examples

**A rotation by 90 degrees.** On the pixel grid, a rotation by 90 degrees and a shift by whole pixels are exact. The derivative matrix at a point becomes $R M R^\top$ with $R$ the rotation, with the same eigenvalues, so the Harris and Shi-Tomasi values are the same at the rotated point and the detected points rotate with the image. Rotations by other angles are only approximately exact, because the image is resampled.

**A blob that grows.** A Gaussian blob of variance $t_0$ has its normalized Laplacian maximum at $t = t_0$. Scale the image by $s = 2$: the blob has the variance $4t_0$, and the maximum moves to $t = 4t_0$. The ratio of the two selected scales is the ratio of the sizes squared, as covariance requires.

**A shear and its ellipse.** Take a circular region, $\Sigma = I$, and the shear $A = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$. Then $\Sigma' = A A^\top = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$, with eigenvalues $(3 \pm \sqrt 5)/2 = 2.618$ and $0.382$. The mapped region is an ellipse with semi-axes $1.618$ and $0.618$, whose product is $1 = \det A$, with the long axis at $31.7$ degrees to the $u$ axis. The matrix $\Sigma'^{-1/2} A$ is the rotation by $-26.6$ degrees, $\begin{pmatrix} 0.894 & 0.447 \\ -0.447 & 0.894 \end{pmatrix}$, so after normalization the two regions differ only by this rotation.

**A change of light.** Add $10$ to every gray value. The Harris measure, the DoG and the Hessian do not change, and MSER finds the same regions with every level shifted by $10$. Double every gray value: the Harris measure is multiplied by $16$ and the DoG by $2$.

## Where it is used

- **Wide-baseline matching and stereo.** Covariant regions and invariant descriptors find the same scene points in views that are far apart; MSER was introduced for this task.
- **[Image registration](/image-registration/) and panoramas.** Matched features give the correspondences for [homography estimation](/homography-estimation/).
- **Structure from motion.** Feature tracks over many photographs come from invariant features.
- **Object recognition and [image retrieval](/image-retrieval/).** Invariant descriptors of an object can be matched in new scenes, at any position, size and orientation.
- **Evaluation.** [Detector repeatability](/detector-repeatability/) measures how well a detector is covariant in practice.

## References
