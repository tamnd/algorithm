---
tag: MHBWKQ
kind: model
slug: gaussian-splatting
name: 3D Gaussian splatting
aliases:
- 3DGS
area: computer-vision/stereo-and-dense-reconstruction
level: research
summary: Represent a scene by many anisotropic 3D Gaussians with color, rendered by sorted alpha blending of their projections and fitted to posed images by gradients.
prereqs: [pinhole-camera-model, covariance-matrix, alpha-blending]
see_also: [neural-radiance-field, multi-view-stereo, porter-duff-compositing, tiled-rasterization, radix-sort, incremental-structure-from-motion, point-cloud, adam]
sources:
  - paper: doi:10.1145/3592433
    title: Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler and George Drettakis, 3D Gaussian splatting for real-time radiance field rendering, ACM Transactions on Graphics 42(4), Article 139, 2023
    locator: the representation (Eq. 5 for the projected covariance and Eq. 6 for the covariance from rotation and scale), the blending formula, the optimization with its loss and the adaptive control of the Gaussians, the tile-based rasterizer, and Table 1
  - paper: doi:10.1109/VISUAL.2001.964490
    title: Matthias Zwicker, Hanspeter Pfister, Jeroen van Baar and Markus Gross, EWA volume splatting, IEEE Visualization 2001
    locator: the projection of a 3D Gaussian kernel to a 2D Gaussian footprint by the local affine approximation of the perspective map
---

3D Gaussian splatting, or 3DGS, describes a scene by a large set of 3D Gaussians: small soft blobs, each with a position, a shape and orientation, an opacity and a color that can change with the viewing direction. To render an image, each Gaussian is projected to a 2D Gaussian on the screen, the Gaussians are sorted by depth, and their colors are blended front to back, as with transparent sheets. Kerbl et al. (2023) start the Gaussians from the sparse points of [structure from motion](/incremental-structure-from-motion/) and fit all their values to the photos by gradient descent, adding and removing Gaussians as the fit goes on. The blending rule is the same as the volume rendering sum of a [neural radiance field](/neural-radiance-field/), but there is no network and no sampling along rays, so rendering runs at real-time rates. Like NeRF, and unlike [multi-view stereo](/multi-view-stereo/), the model aims to reproduce images, not to find a surface. This page gives the representation and the rendering formulas.

## The machine

**Representation.** The scene is a set of $M$ Gaussians. Gaussian $i$ has:

- a mean $\mu_i \in \mathbb{R}^3$;
- a covariance $\Sigma_i = R_i S_i S_i^{\mathsf T} R_i^{\mathsf T}$, where $R_i$ is a rotation stored as a unit quaternion and $S_i = \mathrm{diag}(s_i)$ holds three scales (Eq. 6 of the paper);
- an opacity $o_i \in [0, 1]$;
- color coefficients of spherical harmonics up to degree 3, which give the color $c_i(d)$ as a smooth function of the viewing direction $d$.

Its density is $G_i(x) = \exp\big(-\tfrac12 (x - \mu_i)^{\mathsf T} \Sigma_i^{-1} (x - \mu_i)\big)$. Writing $\Sigma_i$ through $R_i$ and $S_i$ keeps it symmetric and positive semidefinite for any values of the parameters, which a free $3 \times 3$ matrix under gradient steps would not.

**Projection.** Let $W$ be the rotation of the camera and $t = W \mu_i + t_W$ the center in camera coordinates, with $t_z > 0$. The perspective map $(x, y, z) \mapsto (f_x x / z + c_x, f_y y / z + c_y)$ is not affine, so a 3D Gaussian does not map to an exact 2D Gaussian. Following the EWA splatting of Zwicker et al. (2001), the map is replaced near $t$ by its first-order Taylor expansion, with the Jacobian

$$J = \begin{pmatrix} f_x / t_z & 0 & -f_x t_x / t_z^2 \\ 0 & f_y / t_z & -f_y t_y / t_z^2 \end{pmatrix}.$$

Then the screen footprint is a 2D Gaussian with mean $\mu'_i$, the projection of $t$, and covariance

$$\Sigma'_i = J W \Sigma_i W^{\mathsf T} J^{\mathsf T},$$

Eq. 5 of the paper (which writes the full $3 \times 3$ form and drops the third row and column).

**Blending.** At a pixel $p$, let the Gaussians that cover it be sorted by depth, nearest first. Each gets the alpha

$$\alpha_i = o_i \exp\big(-\tfrac12 (p - \mu'_i)^{\mathsf T} {\Sigma'_i}^{-1} (p - \mu'_i)\big),$$

and the pixel color is

$$C(p) = \sum_{i} c_i\, \alpha_i\, T_i, \qquad T_i = \prod_{j < i} (1 - \alpha_j).$$

This is front-to-back [alpha blending](/alpha-blending/), the "over" operator of [Porter-Duff compositing](/porter-duff-compositing/).

**The rasterizer.** The paper splits the screen into tiles of $16 \times 16$ pixels. Each Gaussian is listed once for each tile that its footprint (cut at a few standard deviations) touches, with a 64-bit key: the tile number in the high bits and the depth in the low bits. One GPU [radix sort](/radix-sort/) of all keys then sorts by tile and, within a tile, by depth. Each tile is blended by one thread block, one thread per pixel, front to back. A Gaussian with $\alpha_i < 1/255$ at the pixel is skipped, $\alpha_i$ is clamped to at most 0.99, and a pixel stops when its accumulated opacity reaches 0.9999. This is a form of [tiled rasterization](/tiled-rasterization/).

## What it counts

**What it predicts.** The color of every pixel of a view from any camera, by the blending formula above. The depth order is per tile, by the depth of the centers, not per pixel, so it is an approximation where Gaussians overlap in depth.

**What a fit minimizes.** For a training image $I$ and its rendering $\hat I$, the loss is

$$\mathcal{L} = (1 - \lambda)\, \mathcal{L}_1(\hat I, I) + \lambda\, \mathcal{L}_{\text{D-SSIM}}(\hat I, I), \qquad \lambda = 0.2,$$

the mean absolute error plus a term from the structural similarity index. It is an image space form of [photo-consistency](/photo-consistency/). The parameters are fitted by stochastic gradient steps with [Adam](/adam/); the gradients go back through the blending, the projection and the covariance.

**Adaptive control.** The fit also changes the number of Gaussians. Every 100 iterations the paper finds Gaussians whose view space position gradient has a mean size above $\tau_{\text{pos}} = 0.0002$. A small one is cloned, to fill a region with too few Gaussians; a large one is split into two smaller ones, with scales divided by $\phi = 1.6$, placed by sampling from the old Gaussian. Gaussians with very low opacity are removed, and every 3000 iterations all opacities are set close to zero, so that Gaussians that are not needed fade and are removed. These rules and values are heuristics of the paper.

**Cost.** For one view, the projection is $O(M)$. If the Gaussians produce $K$ pairs of a Gaussian and a tile, the sort is $O(K)$ with radix sort on keys of fixed width, and blending is $O(\sum_p n_p)$, where $n_p$ is the number of Gaussians that pixel $p$ visits before it stops. There is no network.

## Relation to other models

- **Neural radiance field.** NeRF computes $\alpha_i = 1 - e^{-\sigma_i \delta_i}$ from network samples along a ray and uses the same sum $\sum_i T_i \alpha_i c_i$. Gaussian splatting gets $\alpha_i$ from projected Gaussians, so it needs no samples in empty space and no network evaluation. It also stores the scene explicitly, which takes more memory.
- **EWA splatting.** Zwicker et al. (2001) render volumes and point sets by splatting Gaussian kernels with the same projected covariance. 3DGS keeps the projection and blending and makes all the parameters trainable.
- **Point clouds and MVS.** The Gaussians start from a sparse [point cloud](/point-cloud/) and play the role of fuzzy oriented points, like the patches of [patch-based multi-view stereo](/patch-based-multi-view-stereo/). But the fit only asks that images match; the Gaussians need not lie on a surface.
- **Alpha compositing.** The per-pixel sum is standard front-to-back compositing, which needs the correct depth order to be exact.

## Known results in the model

**Affine maps of Gaussians (a theorem).** If $x$ has a Gaussian density with mean $\mu$ and covariance $\Sigma$, then for any matrix $A$ and vector $b$, $Ax + b$ has mean $A\mu + b$ and covariance $A \Sigma A^{\mathsf T}$, and it is Gaussian (degenerate if $A \Sigma A^{\mathsf T}$ is singular). With $A = J W$ this gives the projected covariance exactly for the affine approximation of the camera; for the true perspective map it holds only to first order near the center.

**The parameterization is valid (a theorem).** For any rotation $R$ and diagonal $S$, $R S S^{\mathsf T} R^{\mathsf T} = (R S)(R S)^{\mathsf T}$ is symmetric and positive semidefinite, and positive definite when all scales are nonzero. Every covariance matrix has this form, by its eigendecomposition.

**Weights.** As for NeRF, $\sum_i T_i \alpha_i + T_{\text{end}} = 1$ by telescoping, so each pixel is a convex combination of the Gaussian colors and the background. The clamp $\alpha_i \le 0.99$ keeps every $T_i > 0$, which keeps the gradients defined.

**A footprint by hand.** A Gaussian with $\Sigma = 0.01\, I$ (standard deviation 0.1 in every direction) has its center at $t = (0, 0, 2)$ in camera coordinates, with $f_x = f_y = 100$ and $W = I$. Then $J = \begin{pmatrix} 50 & 0 & 0 \\ 0 & 50 & 0 \end{pmatrix}$ and $\Sigma' = 0.01 \cdot 2500\, I = 25\, I$, a standard deviation of 5 pixels, which is the size $100 \cdot 0.1 / 2$ of a ball of radius 0.1 at depth 2. Moved to $t = (0.2, 0, 2)$, the first row of $J$ becomes $(50, 0, -5)$ and $\Sigma'_{11} = 0.01 (2500 + 25) = 25.25$: the footprint stretches a little away from the image center.

**A pixel by hand.** Two Gaussians cover a pixel with $\alpha_1 = 0.6$ and color 1, then $\alpha_2 = 0.5$ and color 0.2 (one channel). Then $C = 0.6 \cdot 1 + 0.4 \cdot 0.5 \cdot 0.2 = 0.64$, and the remaining transmittance is $0.4 \cdot 0.5 = 0.2$.

**Benchmark results.** On the Mip-NeRF360 scenes, the paper reports (Table 1) for 3DGS after 30 thousand iterations an SSIM of 0.815, a PSNR of 27.21 and an LPIPS of 0.214, with 41 minutes of training, 134 frames per second and 734 MB of memory. For Mip-NeRF360 on the same scenes it reports 0.792, 27.69 and 0.237, with 48 hours of training and 0.06 frames per second. These are measurements with the hardware and settings of the paper, not properties of the model.

**What is not proved.** There is no theorem that the fit converges to the true scene or to a global minimum. The densification rules are heuristics. Sorting per tile by center depth can blend in the wrong order, which shows as popping when the view moves.

## References
