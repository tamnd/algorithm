---
tag: WZQ35M
kind: model
slug: neural-radiance-field
name: Neural radiance field
aliases:
- NeRF
area: computer-vision/stereo-and-dense-reconstruction
level: research
summary: Represent a scene as a function from 3D position and direction to density and color, fitted to posed images by differentiable volume rendering.
prereqs: [pinhole-camera-model, ray-marching, backpropagation]
see_also: [gaussian-splatting, multi-view-stereo, photo-consistency, porter-duff-compositing, importance-sampling, inverse-transform-sampling, adam, psnr]
sources:
  - paper: doi:10.1007/978-3-030-58452-8_24
    title: "Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi and Ren Ng, NeRF: representing scenes as neural radiance fields for view synthesis, ECCV 2020, Lecture Notes in Computer Science, pages 405 to 421"
    locator: Eq. 1 (the rendering integral), Eq. 2 (stratified sampling) and Eq. 3 (the quadrature), the positional encoding with L = 10 and L = 4, hierarchical volume sampling with 64 and 128 samples, the loss and the training settings, and Table 1 (PSNR, SSIM and LPIPS)
  - paper: doi:10.1109/2945.468400
    title: Nelson Max, Optical models for direct volume rendering, IEEE Transactions on Visualization and Computer Graphics 1(2), pages 99 to 108, 1995
    locator: the absorption and emission models and the integral of the emission and absorption model along a ray
---

A neural radiance field, or NeRF, describes a scene by a function that gives, for every point in space and every viewing direction, a density and a color. The density says how much the point blocks light, and the color is the light that leaves the point in that direction. A picture from any camera is made by sending a ray through each pixel, sampling the function along the ray, and adding up the colors with the weights of classical volume rendering. Mildenhall et al. (2020) represent the function by a small fully connected neural network and fit it to a few dozen photos with known cameras, so that the rendered pixels match the real ones. The result renders new views of high quality. Unlike [multi-view stereo](/multi-view-stereo/), which looks for a surface, NeRF fits a soft volume whose purpose is to reproduce images; [3D Gaussian splatting](/gaussian-splatting/) uses the same blending rule with an explicit set of Gaussians in place of the network. This page gives the representation and the rendering formula; the network itself has no correctness theorem and its cost is outside the page.

## The machine

**Representation.** The scene is a function

$$F_\Theta : (x, d) \mapsto (c, \sigma), \qquad x \in \mathbb{R}^3,\ d \in S^2,\ c \in [0, 1]^3,\ \sigma \ge 0.$$

The density $\sigma$ depends only on the position $x$, and the color $c$ depends on $x$ and the direction $d$. This lets the model show highlights that move with the view, while the geometry stays the same for all views. In the paper, $x$ goes through 8 fully connected layers of 256 units, which give $\sigma$ and a feature vector; the feature and the direction then go through one layer of 128 units, which gives $c$.

**Positional encoding.** A plain network of $(x, d)$ gives blurry results, because such networks learn low frequencies first. The paper maps each coordinate $p$ of $x$ and $d$ by

$$\gamma(p) = \big(\sin(2^0 \pi p), \cos(2^0 \pi p), \dots, \sin(2^{L-1} \pi p), \cos(2^{L-1} \pi p)\big),$$

with $L = 10$ for position and $L = 4$ for direction, before the network.

**Rendering a ray.** A pixel defines the ray $r(t) = o + t d$ from the camera center $o$, as in the [pinhole model](/pinhole-camera-model/). Its expected color between the near and far bounds $t_n$ and $t_f$ is the integral of the emission and absorption model of Max (1995):

$$C(r) = \int_{t_n}^{t_f} T(t)\, \sigma(r(t))\, c(r(t), d)\, dt, \qquad T(t) = \exp\Big(-\int_{t_n}^{t} \sigma(r(s))\, ds\Big).$$

$T(t)$ is the transmittance: the fraction of light from $r(t)$ that reaches the camera without being blocked.

**Quadrature.** The paper splits $[t_n, t_f]$ into $N$ equal bins and draws one sample $t_i$ uniformly in each bin (stratified sampling). With $\delta_i = t_{i+1} - t_i$ and the values $\sigma_i, c_i$ at $t_i$, the estimate is

$$\hat C(r) = \sum_{i=1}^{N} T_i\, \alpha_i\, c_i, \qquad \alpha_i = 1 - e^{-\sigma_i \delta_i}, \qquad T_i = \exp\Big(-\sum_{j<i} \sigma_j \delta_j\Big) = \prod_{j<i} (1 - \alpha_j).$$

This is exact when $\sigma$ and $c$ are constant on each interval $[t_i, t_{i+1})$, and it is differentiable in all $\sigma_i$ and $c_i$, so the network can be fitted by gradients ([backpropagation](/backpropagation/)). The last form shows that it is front-to-back alpha compositing, the "over" operator of [Porter-Duff compositing](/porter-duff-compositing/), with opacity $\alpha_i$.

**Hierarchical sampling.** Most samples of a ray fall in empty space or behind the surface. The paper evaluates a coarse network at $N_c = 64$ stratified samples, turns the weights $w_i = T_i \alpha_i$ into a piecewise constant density along the ray, draws $N_f = 128$ more samples from it by [inverse transform sampling](/inverse-transform-sampling/), and evaluates a fine network at all $N_c + N_f$ samples. This is [importance sampling](/importance-sampling/) of the rendering integral.

## What it counts

**What it predicts.** The color of any ray through the scene, so an image from any new camera inside the range of the training views. The weights $w_i$ also give an expected depth $\sum_i w_i t_i$ per ray, which is a by-product.

**What a fit minimizes.** For a batch $\mathcal{R}$ of rays from the training images with true colors $C(r)$, the loss is

$$\mathcal{L} = \sum_{r \in \mathcal{R}} \Big( \|\hat C_c(r) - C(r)\|_2^2 + \|\hat C_f(r) - C(r)\|_2^2 \Big),$$

the squared error of the coarse and the fine rendering. It is a photometric loss: an image space form of [photo-consistency](/photo-consistency/). The paper uses batches of 4096 rays, [Adam](/adam/) with a learning rate that decays from $5 \cdot 10^{-4}$ to $5 \cdot 10^{-5}$, and 100 to 300 thousand iterations, which took one to two days on one NVIDIA V100 GPU per scene. One scene is one fit; nothing is learned across scenes.

**Cost of one ray.** Rendering a ray takes $N_c + N_f = 192$ network evaluations and $O(N_c + N_f)$ work for the sums and the sampling. The cost of one evaluation of the network is outside the page.

## Relation to other models

- **Volume rendering.** The rendering integral is the emission and absorption model of Max (1995), used for decades to show medical and scientific volumes. NeRF adds a learned field and fits it to images.
- **Alpha compositing.** With $\alpha_i = 1 - e^{-\sigma_i \delta_i}$, the quadrature is the front-to-back "over" of Porter and Duff along the ray.
- **3D Gaussian splatting.** It uses the same sum $\sum_i T_i \alpha_i c_i$, but the $\alpha_i$ come from projected 3D Gaussians sorted by depth, not from samples of a network along the ray. This makes it much faster to render.
- **Multi-view stereo.** MVS seeks a surface on which the images agree. NeRF seeks a volume that reproduces the images. A NeRF can be dense where a surface is thin, and its geometry can be poor in regions where the color alone can explain the images.
- **Light fields.** A light field stores the color of every ray directly. NeRF stores a 3D field, and the rays follow from the rendering integral, which ties the views together through the geometry.

## Known results in the model

**Weights sum to one (a theorem).** For any values $\sigma_i \ge 0$ and $\delta_i > 0$,

$$\sum_{i=1}^{N} T_i \alpha_i + T_{N+1} = 1.$$

*Proof.* By the definition, $T_1 = 1$ and $T_{i+1} = T_i (1 - \alpha_i)$, so $T_i \alpha_i = T_i - T_{i+1}$. The sum telescopes to $T_1 - T_{N+1} = 1 - T_{N+1}$. $\blacksquare$

So $\hat C$ is a convex combination of the sample colors and of a background color with weight $T_{N+1}$. If the colors lie in $[0, 1]$, so does $\hat C$ with a black background.

**Check value (exact).** Constant density $\sigma$ over a length $L$ gives transmittance $e^{-\sigma L}$ and opacity $1 - e^{-\sigma L}$. With $\sigma = 2$ and $L = 0.5$, the opacity is $1 - e^{-1} \approx 0.632$. Splitting the segment into any number of bins gives the same result, since $\prod_j e^{-\sigma \delta_j} = e^{-\sigma L}$.

**A ray by hand.** Two samples have $\sigma_1 \delta_1 = \ln 2$ and $\sigma_2 \delta_2 = \ln 4$, so $\alpha_1 = 0.5$ and $\alpha_2 = 0.75$, with colors $c_1 = 1$ and $c_2 = 0$ (one channel). Then $T_1 = 1$, $T_2 = 0.5$, $T_3 = 0.125$, the weights are 0.5 and 0.375, and $\hat C = 0.5 \cdot 1 + 0.375 \cdot 0 = 0.5$. The weights and $T_3$ add to 1.

**Benchmark results.** The paper reports PSNR, SSIM and LPIPS on three data sets (Table 1): 40.15, 0.991 and 0.023 on Diffuse Synthetic 360; 31.01, 0.947 and 0.081 on Realistic Synthetic 360; and 26.50, 0.811 and 0.250 on Real Forward-Facing scenes. In that table NeRF is better than the earlier view synthesis methods it compares with. These are measurements on those data sets with that setup, not properties of the model. See [PSNR](/psnr/) for the first measure.

**What is not proved.** There is no theorem that the fit finds the true scene, or that the loss reaches its global minimum. The fitted density is not unique: a texture painted on a wrong surface can reproduce the training views. Rendering of views far from the training views has no error bound.

## References
