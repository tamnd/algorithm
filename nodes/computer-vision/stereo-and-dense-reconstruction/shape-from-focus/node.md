---
tag: 09NTD3
kind: algorithm
slug: shape-from-focus
name: Shape from focus
aliases:
- depth from focus
- sum-modified-Laplacian shape from focus
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: "Take images at many focus settings and give each pixel the depth of the setting at which a local sharpness measure is largest, refined by a Gaussian fit."
model: real-ram
complexity:
  vars: {N: the number of images in the focal stack, W: the image width in pixels, H: the image height in pixels}
  time: {worst: Θ(N W H), average: Θ(N W H), best: Θ(N W H)}
  space: {extra: O(N W H)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1994
  people: [Shree K. Nayar, Yasuo Nakagawa]
  note: "Krotkov (1988) studied focus measures and searched for the best focus of a lens. Nayar and Nakagawa (1994) measured the focus of every pixel with the sum-modified-Laplacian over a stack of images and fitted a Gaussian to find the depth between frames."
prereqs: [gaussian-filter, integral-image]
see_also: [laplacian-of-gaussian, sobel-operator, fibonacci-search, parsevals-theorem, photometric-stereo, structured-light-scanning, depth-from-disparity, multi-view-stereo]
sources:
  - paper: doi:10.1109/34.308479
    title: "Shree K. Nayar and Yasuo Nakagawa, Shape from focus, IEEE Transactions on Pattern Analysis and Machine Intelligence 16(8), 1994, pages 824 to 831"
    locator: "the modified Laplacian and the sum-modified-Laplacian focus measure, the depth from the frame of largest focus, and the Gaussian interpolation over three frames"
  - paper: doi:10.1007/BF00127822
    title: "Eric Krotkov, Focusing, International Journal of Computer Vision 1(3), 1988, pages 223 to 237"
    locator: "the comparison of focus measures, including the Tenengrad gradient measure, and the Fibonacci search for the best focus"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.1.3, Shape from focus"
---

Shape from focus finds the depth of each pixel from a stack of images that one camera takes while it moves its plane of focus through the scene. A lens shows a point sharply only when the point is at the distance in focus; nearer and farther points are blurred. So for each pixel the method measures the local sharpness in every image, picks the image where it is largest, and gives the pixel the depth that is in focus in that image. A fit through the sharpness of the best image and its two neighbors gives a depth between the images. Unlike stereo, it needs one camera and no matching; unlike [photometric stereo](/photometric-stereo/), it needs texture, not control of the light. Depth from defocus is the related method that uses only two or three images and models the amount of blur.

## In plain words

Look at a textured object through a microscope and turn the focus knob slowly. Each part of the surface becomes sharp at one setting of the knob and blurred at the others. If you take a photo at every step of the knob and remember, for every pixel, the step where its small neighborhood looked sharpest, you know how far that part of the surface is from the lens. The sharpness is measured by how strongly the brightness changes between neighboring pixels, since blur smooths these changes away. A smooth curve through the sharpness values of three steps finds the depth between two steps.

## The problem

**Input.**

- A focal stack: $N$ gray images $I_0, \dots, I_{N-1}$ of size $W \times H$ from a fixed camera. Image $k$ is in focus at the depth $d_0 + k \Delta$. The images are aligned; a real lens also changes the magnification slightly with focus, which must be corrected first.
- A step $s$ for the modified Laplacian, a window radius $r$ and a threshold $T_1$.

**Model.** The scene has texture at the scale of the window, and the depth is nearly constant over one window. A point at depth $z$ appears in image $k$ blurred by an amount that grows with $|z - (d_0 + k \Delta)|$.

**Output.** A depth for each pixel. The best image of each pixel also gives an all-in-focus image of the scene.

**The focus measure.** The modified Laplacian of Nayar and Nakagawa is

$$\mathrm{ML}(u, v) = |2 I(u, v) - I(u - s, v) - I(u + s, v)| + |2 I(u, v) - I(u, v - s) - I(u, v + s)|.$$

It takes absolute values of the two second differences separately, so they cannot cancel as they do in the plain Laplacian on a saddle. The sum-modified-Laplacian $F$ is the sum of the values $\mathrm{ML} \ge T_1$ over the $(2r+1) \times (2r+1)$ window.

## The algorithm

```pseudo id=main
SHAPE-FROM-FOCUS(I_0..I_{N-1}, d_0, Δ, s, r, T_1)
L1  for k ← 0 to N - 1 do
L2      F_k ← the window sum of the values ML ≥ T_1 of the modified Laplacian of I_k
L3  for each pixel p do
L4      m ← the least k with the largest F_k(p)
L5      if 0 < m < N - 1 then δ ← the peak offset of the Gaussian through F_{m-1}(p), F_m(p), F_{m+1}(p), else δ ← 0
L6      depth[p] ← d_0 + Δ (m + δ)
L7  return depth
```

**Line L2, the window.** The window sum takes $O(1)$ per pixel with an [integral image](/integral-image/), for any $r$. Nayar and Nakagawa sum over a small window, because one pixel has too little texture to measure focus.

**Line L5, the Gaussian fit.** If the focus measure near its peak has the shape $A \exp(-(k - c)^2 / (2 s^2))$, then $\ln F$ is a parabola in $k$, and the peak is

$$\delta = \frac{1}{2} \cdot \frac{\ln F_{m-1} - \ln F_{m+1}}{\ln F_{m-1} - 2 \ln F_m + \ln F_{m+1}}.$$

The code skips the fit when a value is not positive or the denominator is not negative.

**Line L6, from frame to depth.** The depth that frame $k$ has in focus comes from the calibration of the lens, for example the thin lens law $1/f = 1/z + 1/z'$ with the distance $z'$ of the sensor. In a microscope that moves the stage in equal steps, it is simply $d_0 + k \Delta$.

## Example

**One modified Laplacian.** A pixel of value 10 with left and right neighbors 4 and 6 and upper and lower neighbors 7 and 9 has $\mathrm{ML} = |20 - 4 - 6| + |20 - 7 - 9| = 10 + 4 = 14$ for $s = 1$.

**One Gaussian fit.** If the best frame has $F_m = 100$ and its neighbors have $F_{m-1} = 40$ and $F_{m+1} = 70$, then $\ln 40 = 3.689$, $\ln 100 = 4.605$ and $\ln 70 = 4.248$. The denominator is $-1.273$, the numerator is $-0.560$, and $\delta = 0.5 \cdot 0.560 / 1.273 = 0.220$. The peak lies 0.22 of a step past frame $m$, toward the larger neighbor.

**A slanted plane.** The test file blurs a random $24 \times 24$ texture into 9 frames. The true depth grows from frame 2 at the left edge to frame 6 at the right, and the blur in frame $k$ is a Gaussian with standard deviation $0.8\,|k - d|$ pixels. With a $5 \times 5$ window, the best frame of every one of the 576 pixels is within one frame of the true depth, and the mean error of the best frame is 0.244 frames, which is close to the 0.25 of rounding to whole frames. After the Gaussian fit, the mean error is 0.057 frames and the largest is 0.21.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **The fit is exact for Gaussian profiles.** If the three values follow a Gaussian in $k$, their logarithms lie on a parabola, and the formula returns its vertex exactly.
2. **The fit stays near the best frame.** If $F_m$ is the largest of the three values, the step $\delta$ is at most $1/2$ in size, whatever the shape of the profile.
3. **Gain and offset.** Replacing every image by $a I + b$ with $a > 0$ multiplies the modified Laplacian by $a$, so the choice and the fit do not change when $T_1 = 0$.
4. **Why the Laplacian measures focus.** For a periodic texture blurred by a Gaussian, the energy of the Laplacian is $\sum |\omega|^4 |\hat T(\omega)|^2 e^{-\sigma^2 |\omega|^2}$ up to a constant, by [Parseval's theorem](/parsevals-theorem/), which strictly decreases as the blur $\sigma$ grows.

That the sum-modified-Laplacian peaks at the true depth is a heuristic, which Nayar and Nakagawa support by experiments. It uses absolute values, a small window and a threshold, and real blur is not an exact Gaussian.

## Complexity

The model is the real RAM. Line L2 costs $\Theta(W H)$ per frame: the modified Laplacian is $O(1)$ per pixel, and the window sums are $O(1)$ per pixel with the integral image. Lines L3 to L6 cost $\Theta(N)$ per pixel for the maximum. The total is $\Theta(N W H)$ in every case. The code keeps all focus measures, $O(N W H)$. A version that reads the stack as it is taken needs only the best value, its index and the values of its two neighbors per pixel, $\Theta(W H)$.

## Properties

- **One camera, no matching.** All images show the same pixel grid, so there is no correspondence problem.
- **Needs texture.** On a surface with no texture, every frame has the same low focus measure, and the depth is noise.
- **Resolution in depth.** The step $\Delta$ and the depth of field of the lens set the resolution. The Gaussian fit gives a fraction of a step.
- **Local.** Each pixel is decided on its own, so depth edges and noise are not smoothed.
- **Not exact.** The method estimates depth; the result depends on the texture and the lens.

## Variants and improvements

- **Other focus measures.** Krotkov compared several measures and used the Tenengrad, the sum of squared [Sobel](/sobel-operator/) gradient magnitudes above a threshold. Others use the variance of the gray values, the energy of the [Laplacian of Gaussian](/laplacian-of-gaussian/), or energies of wavelet bands.
- **Autofocus.** For a single region, the best focus can be searched instead of sampled, for example by [Fibonacci search](/fibonacci-search/) over the lens position, which Krotkov used.
- **Depth from defocus.** It models the blur as a function of depth and finds the depth from two or three images, so it needs far fewer images but a calibrated blur model.
- **Regularization.** A smoothness term between neighboring pixels, solved by graph cuts or a variational method, fills in the depth of textureless regions.
- **All-in-focus images.** Taking each pixel from its best frame gives an image that is sharp everywhere, as in focus stacking for macro photography and microscopy.

## When to use it

Use shape from focus for small textured objects under a microscope or a macro lens, where the depth of field is shallow and a motorized stage or focus drive is available. It needs many images of a static scene, so it is slow to capture, but the setup is one camera with no second view and no projector. For large scenes, the depth of field of normal lenses is too deep to give a useful depth resolution; use stereo or [structured light scanning](/structured-light-scanning/) there.

## Pitfalls

- **Magnification changes.** Moving the focus also changes the scale of the image slightly. Without alignment, the window of a pixel covers different points in different frames.
- **No texture.** Flat regions give a flat focus profile, and the argmax picks a random frame. Mark pixels whose largest $F$ is below a threshold as unknown.
- **Window too large.** A window that crosses a depth edge mixes two profiles and gives a depth between them.
- **Threshold $T_1$ and gain.** A fixed $T_1$ depends on the brightness of the image. Scale it with the gain, or use $T_1 = 0$.
- **Truncated blur.** A blur kernel that is cut off, or the blur of a real lens with its aperture shape, is not a Gaussian. Far from focus, the focus measure can then rise again. The test file shows this with a kernel cut at 3 pixels; the peak stays at the right frame.

## Implementations

## History

Krotkov (1988) studied how to bring a camera into focus automatically: he compared focus measures, found the gradient-based Tenengrad to be among the best, and searched for the lens position of best focus with a Fibonacci search. Nayar and Nakagawa (1994) turned focus into a dense depth method: they introduced the modified Laplacian and the sum-modified-Laplacian, took images while the object moved through the focus in steps, and found the depth of each pixel by a Gaussian fit to its focus measure. Later work added other focus measures, depth from defocus with few images, and regularized versions.

## References
