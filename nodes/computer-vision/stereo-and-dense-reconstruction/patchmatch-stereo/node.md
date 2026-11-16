---
tag: G3M5MP
kind: algorithm
slug: patchmatch-stereo
name: PatchMatch stereo
aliases:
- slanted support window stereo
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Estimate a slanted disparity plane per pixel by PatchMatch propagation and random refinement, so that windows on slanted surfaces match well.
solves: [stereo-matching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, s: the number of pixels in a window, D: the largest disparity in pixels, T: the number of iterations}
  time: {worst: Θ(T W H s log D), average: Θ(T W H s log D), best: Θ(T W H s log D)}
  space: {extra: Θ(W H)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2011
  people: [Michael Bleyer, Christoph Rhemann, Carsten Rother]
  note: Bleyer, Rhemann and Rother (BMVC 2011) gave each pixel its own slanted support window and searched the infinite set of planes with PatchMatch, which put their local method at the top of the Middlebury table for some images.
prereqs: [patchmatch, stereo-matching, adaptive-support-weights]
see_also: [block-matching-stereo, semi-global-matching, left-right-consistency-check, cost-aggregation, stereo-matching-cost, subpixel-disparity-refinement, multi-view-stereo, graph-cut-stereo]
sources:
  - paper: doi:10.5244/C.25.14
    title: Michael Bleyer, Christoph Rhemann and Carsten Rother, PatchMatch Stereo, stereo matching with slanted support windows, British Machine Vision Conference 2011, pages 14.1 to 14.11
    locator: Section 2 (the plane model, the cost with adaptive weights and truncated color and gradient terms, the random initialization, spatial, view and temporal propagation, plane refinement, and the post-processing), Section 2.4 (the data term for global methods) and Section 3 (the parameters and the Middlebury results)
  - paper: doi:10.1145/1531326.1531330
    title: "Connelly Barnes, Eli Shechtman, Adam Finkelstein and Dan B Goldman, PatchMatch: a randomized correspondence algorithm for structural image editing, ACM Transactions on Graphics 28(3), Article 24, 2009"
    locator: Section 3 (random initialization, propagation in alternating scan order and random search, which PatchMatch stereo applies to planes)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (local methods with slanted windows)
---

PatchMatch stereo is a local method for [stereo matching](/stereo-matching/) that gives every pixel its own plane in disparity space, $d = a x + b y + c$, instead of one disparity. The cost of a pixel is computed over a window whose pixels are shifted by the disparities of that plane, so a window on a slanted surface is matched with the slant, and not as a fronto-parallel square. The planes are continuous, so there are infinitely many of them, and an exhaustive search is not possible. Bleyer, Rhemann and Rother (2011) search them with the scheme of [PatchMatch](/patchmatch/): random planes at the start, then propagation of good planes to neighbors, to the other view, and to the next frame, and a random refinement around the current plane. It differs from [block matching](/block-matching-stereo/) in the window shape and from [semi-global matching](/semi-global-matching/) in having no smoothness term: neighbors agree only because they share good planes.

## In plain words

Usual stereo methods compare a square around each pixel with a square in the other image. On a road or a wall seen at an angle, the square in one image is stretched in the other, so the comparison is poor. PatchMatch stereo lets each pixel guess a tilted plane, so its square can be stretched to fit. There are too many planes to try all of them. So each pixel starts with a random plane, and then the image is swept several times. At each pixel, the program tries the planes of its neighbors, the plane of the matching pixel in the other image, and a few small random changes to its own plane, and keeps whatever matches best. A good plane found anywhere on a surface spreads over the whole surface.

## The problem

**Input.** A rectified pair of images, the left view $I_0$ and the right view $I_1$, of $W \times H$ pixels, the right camera to the right of the left one. Pixel $(x, y)$ is `img[y][x]`. A largest disparity $D$, a window radius, and the parameters $\gamma, \alpha, \tau_{col}, \tau_{grad}$ of the cost.

**Output.** For each pixel $p$ of each view, a plane $f_p = (a, b, c)$ with $0 \le d_p \le D$, where $d_p = a p_x + b p_y + c$ is the disparity of $p$. The aim is

$$f_p = \operatorname*{arg\,min}_{f} m(p, f), \qquad m(p, f) = \sum_{q \in W_p} w(p, q)\, \rho\big(q,\ q - (a_f q_x + b_f q_y + c_f)\big),$$

with $W_p$ the square window of $p$, the adaptive weight $w(p, q) = e^{-|I(p) - I(q)| / \gamma}$, and the pixel dissimilarity

$$\rho(q, q') = (1 - \alpha) \min(|I(q) - I'(q')|, \tau_{col}) + \alpha \min(\|\nabla I(q) - \nabla I'(q')\|_1, \tau_{grad}).$$

Here $I'$ is the other view, $q'$ has a fractional $x$ and is read by linear interpolation, and for a pixel of the right view the disparity is added instead of subtracted. The paper uses RGB colors and the L1 color distance; the code on this page uses gray values. The method returns a local optimum of $m$ per pixel, found by random search, not the exact minimum.

## The algorithm

```pseudo id=main
PATCHMATCH-STEREO(I_0, I_1, D, T)
L1  for each view v and pixel p do f_v[p] ← the plane through a random z_0 in [0, D] at p with a random unit normal; m_v[p] ← m(p, f_v[p])
L2  for k ← 0 to T - 1 do
L3      for v ← 0, 1 do                                 ▷ all left pixels, then all right pixels
L4          if k is even then scan from the top left and set s ← -1 else from the bottom right and set s ← +1
L5          for each pixel p = (x, y) of view v in that order do
L6              for q in {(x + s, y), (x, y + s)} inside the image do TRY(p, f_v[q])        ▷ spatial propagation
L7              for each pixel p' of view 1 - v whose match rounds to p do TRY(p, TRANSFER(f_{1-v}[p']))   ▷ view propagation
L8              Δz ← D / 2; Δn ← 1
L9              while Δz ≥ 0.1 do                                                     ▷ plane refinement
L10                 z_0 ← d_p + a random value in [-Δz, Δz]; n ← unit(n_p + a random vector in [-Δn, Δn]^3)
L11                 TRY(p, the plane through z_0 at p with normal n)
L12                 Δz ← Δz / 2; Δn ← Δn / 2
L13 return f_0, f_1

TRY(p, f): if 0 ≤ f(p) ≤ D and m(p, f) < m_v[p] then f_v[p] ← f; m_v[p] ← m(p, f)
```

**Planes.** A point $(x_0, y_0, z_0)$ of disparity space and a unit normal $n$ with $n_z \ne 0$ give the plane $a = -n_x / n_z$, $b = -n_y / n_z$, $c = (n_x x_0 + n_y y_0 + n_z z_0) / n_z$, so that $a x_0 + b y_0 + c = z_0$. Line L1 draws $z_0$ uniformly in the continuous range and $n$ as a random unit vector. Line L10 uses the same form: it moves the disparity at $p$ and the normal, and line L11 builds the new plane through the new disparity at $p$.

**Propagation.** Lines L4 to L6 are the propagation of PatchMatch with the scan order reversed on odd iterations. Line L7 is new: a pixel $p'$ of the other view with disparity $d'$ matches the point $(p'_x \pm d', p'_y)$ of this view, and every $p'$ whose match rounds to $p$ offers its plane. A right plane $(a, b, c)$ describes in left coordinates the plane $(a, b, c) / (1 + a)$, and a left plane describes in right coordinates the plane $(a, b, c) / (1 - a)$. To see the first, put $x = x' + d$ into $d = a x' + b y + c$ and solve for $d$. The paper also has temporal propagation from the previous frame of a video. The code has one frame and leaves it out.

**Refinement.** Lines L8 to L12 try one random change per scale. The ranges start at $D / 2$ for the disparity and 1 for each normal component, and halve until the disparity range is below 0.1 pixel. This is the random search of PatchMatch in the space of planes.

**Post-processing.** After the iterations, the paper (1) marks a left pixel invalid when its disparity differs by more than 1 from the disparity of its match in the right map ([left-right check](/left-right-consistency-check/)), (2) fills an invalid pixel with the lower of the disparities that the planes of the nearest valid pixels to its left and right give at the pixel, since occluded pixels lie on the background, and (3) smooths the filled pixels with a weighted median filter. The code has (1) and (2).

## Example

**Planes.** At pixel $(5, 3)$, take $z_0 = 4$ and the normal $n = (0.6, 0, 0.8)$. Then $a = -0.75$, $b = 0$ and $c = (0.6 \cdot 5 + 0.8 \cdot 4) / 0.8 = 7.75$, and indeed $-0.75 \cdot 5 + 7.75 = 4$. In the right view, the same surface is the plane $(-0.75, 0, 7.75) / 1.75 = (-0.4286, 0, 4.4286)$. The left pixel $x = 5$ with disparity 4 matches the right pixel $x' = 1$, and the right plane gives $-0.4286 + 4.4286 = 4$ there, as it must.

**A slanted surface.** The test file builds a $20 \times 12$ pair from a smooth texture on the plane $d = 0.15 x + 0.05 y + 2$, with a $7 \times 7$ window, $D = 8$, the parameters $\{\gamma, \alpha, \tau_{col}, \tau_{grad}\} = \{10, 0.9, 10, 2\}$ of the paper, and seed 3. The sum of the left costs after each step is:

| after | L1 | iteration 1 | iteration 2 | iteration 3 |
|---|---|---|---|---|
| sum of $m_0[p]$ | 3992.4 | 3493.4 | 3292.5 | 3239.7 |

Over the 48 interior pixels, the mean disparity error is 0.047 pixel and the largest is 0.42 pixel. The same code with the normal fixed to $(0, 0, 1)$, which allows only fronto-parallel windows, has a mean error of 0.21 pixel. The window spans 7 columns, over which the true disparity changes by 0.9 pixel, so a fronto-parallel window cannot fit it.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts.

1. **Plane algebra.** The plane built in lines L1 and L11 has disparity $z_0$ at $p$ and normal $n$. TRANSFER maps a plane of one view to the plane of the same surface in the other view: if $d$ is the disparity of the left plane at $x$, then the right plane has the same disparity $d$ at $x - d$. TRANSFER from left to right and back is the identity.
2. **Invariant.** At all times $m_v[p] = m(p, f_v[p])$ and $0 \le f_v[p](p) \le D$, and $m_v[p]$ never increases, because TRY accepts only a strictly lower cost.
3. **What is computed.** The output is, at each pixel, the best of all planes the run has tried at that pixel. No result bounds the gap to the true minimum of $m(p, \cdot)$, which is a nonconvex function of three real parameters.

## Complexity

The model is the real RAM: plane parameters and costs are real numbers, and $\exp$ and linear interpolation cost $O(1)$. Let $s$ be the number of pixels in a window.

- **One cost.** $m(p, f)$ sums over $s$ pixels, so it takes $\Theta(s)$ time.
- **One iteration.** Each pixel of each view gets 2 spatial candidates and $\lfloor \log_2(5 D) \rfloor + 1$ refinement candidates (the number of halvings of $D/2$ down to 0.1). Every pixel of the other view offers its plane to exactly one pixel in line L7, so the view candidates add $W H$ per view. One iteration takes $\Theta(W H s \log D)$ time for $D \ge 1$.
- **Number of iterations.** $T$ is a parameter; the paper uses 3. The total is $\Theta(T W H s \log D)$, plus $\Theta(W H s)$ for the start.
- **Space.** Two plane maps and two cost maps, $\Theta(W H)$. The code also caches the weights of every window, which takes $\Theta(W H s)$.

The paper uses a $35 \times 35$ window, so $s = 1225$, and reports about one minute per Middlebury pair for unoptimized C code (measured, 2011).

## Properties

- **Slanted support.** The window follows a plane, so slanted surfaces match without the bias of fronto-parallel windows. The plane also gives subpixel disparities with no separate refinement step.
- **Adaptive weights.** The weight $w(p, q)$ removes most pixels of other surfaces from the window, as in [adaptive support weights](/adaptive-support-weights/). Large windows then help without blurring edges.
- **Randomized.** The output depends on the random numbers. The cost of each pixel never increases from one step to the next.
- **No smoothness term.** Each pixel minimizes its own cost. Neighbors agree because good planes propagate.
- **Robust cost.** The truncation at $\tau_{col}$ and $\tau_{grad}$ limits the effect of pixels that do not match, for example in occlusions.

## Variants and improvements

- **Fronto-parallel windows.** Fix $n = (0, 0, 1)$, as the paper notes, and the method searches constant disparities with continuous values. The example above shows what this loses on a slanted plane.
- **Data term for global methods.** Section 2.4 of the paper uses the costs of the planes of a pixel and its neighbors as labels in an energy minimized with [alpha-expansion](/alpha-expansion/).
- **Multi-view PatchMatch.** Galliani et al. (2015) and Schönberger et al. (2016) propagate depth and normal per pixel over many views, with view selection, in [multi-view stereo](/multi-view-stereo/).
- **Faster propagation.** Galliani et al. (2015) propagate in a red and black checkerboard pattern on the GPU, so that half of the pixels update in parallel.
- **Other costs.** The [census transform](/census-transform/) or [normalized cross-correlation](/normalized-cross-correlation/) replaces the color and gradient term when the cameras differ in gain.

## When to use it

Use PatchMatch stereo when the scene has large slanted surfaces (roads, walls, floors) and you need subpixel disparities from a local method. It is slower than [block matching](/block-matching-stereo/) and [semi-global matching](/semi-global-matching/) with small windows, because each cost covers a large window and many candidates. Use semi-global matching when you need a predictable run time or a smoothness prior over textureless areas.

## Pitfalls

- **Sign of the disparity.** For the left view the match is at $q_x - d$, for the right view at $q_x + d$. Mixing them up in the cost or in TRANSFER gives planes that never agree between views.
- **Degenerate planes.** A normal with $n_z$ near 0 gives huge $a$ or $b$. Reject such normals in line L10, and skip TRANSFER when $1 \pm a = 0$.
- **Disparity range at $p$ only.** TRY checks the range at $p$, not over the window. Window pixels can then read the other image outside its border; clamp the interpolation there.
- **Strict acceptance.** TRY must use $<$, or a pixel can flip between planes of equal cost and the costs are no longer monotone.
- **Stale view map.** Line L7 needs the planes of the other view at the time of the pass. Build the map from other-view pixels to the pixels they hit at the start of each pass, after the other view has finished.
- **Fill direction.** The fill step takes the lower disparity, which belongs to the background. Taking the higher one smears the foreground over the occluded area.

## Implementations

## History

Slanted windows and plane fitting have a long history in stereo, but earlier methods used a few planes per segment or a discrete set of slants. Bleyer, Rhemann and Rother (2011) let each pixel have its own continuous plane and used [PatchMatch](/patchmatch/) of Barnes et al. (2009) to search them. With a $35 \times 35$ window and $\{\gamma, \alpha, \tau_{col}, \tau_{grad}\} = \{10, 0.9, 10, 2\}$ they reported the best result of the Middlebury table on the Teddy pair at the time (error above 1 pixel, unoccluded regions). The same propagation of depths and normals then became the core of multi-view PatchMatch methods, including COLMAP.

## References
