---
tag: T9MCYJ
kind: algorithm
slug: restir
name: ReSTIR
aliases:
- reservoir-based spatiotemporal importance resampling
area: graphics-and-signals/ray-tracing
level: research
summary: Pick one light per pixel by resampled importance sampling in a one-item reservoir, then merge the reservoirs of the last frame and of nearby pixels, so each pixel reuses many candidates.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {P: the number of pixels, M: the number of new candidates per pixel and frame, k: the number of spatial neighbors, c: the cost of one shadow ray}
  time: {worst: Θ(P (M + (k + 1) c))}
  space: {extra: Θ(P)}
properties: {deterministic: false, recursive: false, online: true, in_place: false}
history:
  year: 2020
  people: [Benedikt Bitterli, Chris Wyman, Matt Pharr, Peter Shirley, Aaron Lefohn, Wojciech Jarosz]
  note: Bitterli and others combined the resampled importance sampling of Talbot, Cline and Egbert (2005) with one-item weighted reservoirs and with reuse across pixels and frames, for real-time direct light from many lights, at SIGGRAPH 2020.
prereqs: [weighted-reservoir-sampling, next-event-estimation]
see_also: [importance-sampling, multiple-importance-sampling, reservoir-sampling, resampling, path-guiding, instant-radiosity, temporal-antialiasing, image-denoising]
sources:
  - paper: doi:10.1145/3386569.3392481
    title: Benedikt Bitterli, Chris Wyman, Matt Pharr, Peter Shirley, Aaron Lefohn and Wojciech Jarosz, Spatiotemporal reservoir resampling for real-time ray tracing with dynamic direct lighting, ACM Transactions on Graphics 39(4), SIGGRAPH 2020
    locator: streaming RIS with a reservoir, visibility reuse, temporal and spatial reuse, the biased and the unbiased combination
  - paper: doi:10.2312/EGWR/EGSR05/139-146
    title: Justin F. Talbot, David Cline and Parris Egbert, Importance resampling for global illumination, Rendering Techniques 2005 (Eurographics Symposium on Rendering), 139 to 146
    locator: resampled importance sampling and its weight
  - paper: "M. T. Chao, A general purpose unequal probability sampling plan, Biometrika 69(3), 1982, 653 to 656"
    locator: the one-pass weighted sampling that keeps each item with the probability of its weight over the running sum
  - paper: "Daqi Lin, Markus Kettunen, Benedikt Bitterli, Jacopo Pantaleoni, Cem Yuksel and Chris Wyman, Generalized resampled importance sampling: foundations of ReSTIR, ACM Transactions on Graphics 41(4), SIGGRAPH 2022"
    locator: unbiased contribution weights and the resampling MIS weights for samples from different domains
---

ReSTIR is a way to choose, for each pixel of a real-time ray tracer, one light to send a shadow ray to, from a scene with thousands or millions of lights. It draws a few cheap candidates per pixel and keeps one of them in a [weighted reservoir](/weighted-reservoir-sampling/) of size one, with the probability of a target function that is close to the light the light gives. This is resampled importance sampling (RIS), from Talbot, Cline and Egbert (2005). Then each pixel merges its reservoir with the reservoir it had in the last frame and with the reservoirs of a few pixels nearby. A reservoir stands for all the candidates that went into it, so after a few frames each pixel picks its light out of thousands of candidates, for the cost of a few. Bitterli, Wyman, Pharr, Shirley, Lefohn and Jarosz published it in 2020. Some versions are biased and some are not: the merge that divides by the count of all candidates makes the image too dark near shadows, and the merge that counts only the pixels that could have made the chosen light is unbiased.

## In plain words

You must pick one lamp out of thousands to light a spot on the floor, and you can check only one lamp for shadows. Most lamps are far away or dim, so a random pick is bad.

So you look at a few lamps at random and guess, without the shadow check, how much each gives. You keep one, with a chance that grows with its guess, and you remember how good the group looked.

Then you ask your neighbors, and yourself from the last moment, which lamps they kept. Each of them stands for a group too. You pick one lamp from all of these, again by the guesses. Now your lamp is the best of a large group, and you still check only one lamp for shadows. If you count a neighbor's group for a lamp that the neighbor could not see, the answer is too dark.

## The problem

Pixel $q$ is a shading point with a BSDF. For each light $y$ (a point light, or a point on an area light), the light it reflects toward the camera is

$$f_q(y) = \hat p_q(y)\, V_q(y),$$

where the target $\hat p_q(y)$ is the unshadowed contribution, for example $\frac{\rho}{\pi} I_y \cos\theta / d^2$ for a Lambertian point with albedo $\rho$ and a point light with intensity $I_y$ at distance $d$, and $V_q(y) \in \{0, 1\}$ is the visibility. The pixel value is the direct light $I_q = \sum_y f_q(y)$, a sum over all lights, or an integral for area lights. This is the direct light part of the [rendering equation](/rendering-equation/), the part that [next event estimation](/next-event-estimation/) estimates.

The goal is an estimate with low [variance](/variance/) that costs a small fixed number of shadow rays per pixel and frame. A source density $p(y)$ that is cheap to sample is given, for example uniform over the lights or in proportion to their power. It must be positive wherever $\hat p_q > 0$.

## The algorithm

A reservoir holds a light $y$, the sum $w_{\text{sum}}$ of the weights it saw, the count $M$ of candidates it stands for, and the contribution weight $W$. UPDATE$(r, x, w)$ adds $w$ to $w_{\text{sum}}$, adds $1$ to $M$, and sets $y \leftarrow x$ with the probability $w / w_{\text{sum}}$: Chao's one-pass rule, so that each item is kept with the probability of its weight over the total. The estimate of pixel $q$ is $f_q(y)\, W$.

```pseudo id=main
RESTIR-FRAME(prev)
L1  for each pixel q:  R_q ← empty reservoir
L2      for i ← 1 to M:  draw x from p;  UPDATE(R_q, x, p̂_q(x) / p(x))
L3      R_q.W ← R_q.w_sum / (R_q.M · p̂_q(R_q.y))                     ▷ RIS
L4      if the shadow ray from q to R_q.y is blocked then R_q.W ← 0    ▷ visibility reuse
L5      if prev exists then R_q ← COMBINE(q, R_q, prev_q with its M capped at 20 · M)   ▷ temporal reuse
L6  for each pixel q:  pick k pixels n_1, …, n_k near q
L7      S_q ← COMBINE(q, R_q, R_{n_1}, …, R_{n_k})                     ▷ spatial reuse, read from R only
L8      pixel q ← f_q(S_q.y) · S_q.W
L9  return S                                                          ▷ the prev of the next frame

COMBINE(q, r_1, …, r_m)                                                ▷ r_i belongs to pixel o_i
L10 S ← empty;  for each i:  UPDATE(S, r_i.y, p̂_q(r_i.y) · r_i.W · r_i.M);  then S.M ← Σ_i r_i.M
L11 unbiased:  Z ← Σ r_i.M over the i with p̂_{o_i}(S.y) V_{o_i}(S.y) > 0;  S.W ← S.w_sum / (Z · p̂_q(S.y))
L12 biased:  S.W ← S.w_sum / (S.M · p̂_q(S.y));  in both cases S.W ← 0 if q cannot see S.y
```

Line L10 gives each input reservoir the weight $\hat p_q(y_i) W_i M_i$. The factor $\hat p_q(y_i) W_i$ is the RIS weight of $y_i$ as a sample for pixel $q$, because $W_i$ plays the part of $1 / p$, and the factor $M_i$ lets a reservoir that stands for many candidates count as many. The unbiased choice of line L11 needs one more shadow ray per input, to test $V_{o_i}(S.y)$. A third choice, also unbiased, weights the chosen input $r$ by the balance heuristic $h_r(y) / \sum_i M_i h_i(y)$ with $h_i = \hat p_{o_i} V_{o_i}$, in place of $1 / Z$; the implementation has all three.

## Example

**A table scene, worked by hand.** Three lights, the source density $p = (\tfrac12, \tfrac14, \tfrac14)$, and pixel 0 with the target $\hat p_0 = (1, 2, 3)$. Draw the candidates $x = (0, 2)$. Their weights are $1 / \tfrac12 = 2$ and $3 / \tfrac14 = 12$, so $w_{\text{sum}} = 14$, and the reservoir keeps light 2 with the probability $\tfrac{12}{14} = \tfrac67$. Then $W = 14 / (2 \cdot 3) = \tfrac73$ for light 2, or $14 / (2 \cdot 1) = 7$ for light 0. If no light is blocked, $f_0 = \hat p_0$ and the estimate is $7$ in both cases: with a target equal to the integrand, RIS returns the mean of the $M$ values $\hat p / p$ but traces one shadow ray. If light 2 is blocked, the estimate is $0$ with the probability $\tfrac67$ and $7$ otherwise.

Listing every outcome with exact fractions, as the tests do, gives these values for pixel 0; the exact answer is $6$ with no shadow and $3$ when light 2 is blocked:

| candidates $M$ | $P(y = 2)$ | variance, no shadow | variance, light 2 blocked |
|---|---|---|---|
| 1 | 0.250 | 18 | 9 |
| 2 | 0.352 | 9 | 9 |
| 3 | 0.400 | 6 | 9 |
| 4 | 0.427 | 4.5 | 9 |
| 5 | 0.443 | 3.6 | 9 |

With no shadow the variance is exactly $18 / M$. With the shadow it does not fall at all here, because more candidates send more of the choices to light 2, which the target likes and the shadow ray then rejects. The target does not know about visibility; this is the reason for visibility reuse at line L4, which stops a blocked light from being passed on to other pixels.

Now merge pixel 0 ($M = 2$) with pixel 1 ($M = 1$, the target $(2, 1, 1)$), where pixel 1 sees lights 1 and 2 and pixel 0 sees lights 0 and 1. The unbiased merge of line L11 has the mean $3$, exactly. The biased merge of line L12 has the mean $\tfrac83$: light 0 can only come from pixel 0, so it gets the share $\tfrac{2}{2 + 1}$ of its weight.

**A row of pixels under 16 lights.** The test scene has 8 shading points on a floor, 16 point lights at random places above it, and a sphere that blocks between 1 and 7 lights for each point. The source is uniform, $M = 4$, $k = 2$ neighbors within two pixels, and the cap is $20 M$. The table gives the standard deviation of one frame's estimate divided by the exact value, averaged over the 8 pixels, from 4000 independent runs with seeded random numbers.

| method | frame 1 | frame 2 | frame 4 | frame 8 |
|---|---|---|---|---|
| one uniform light sample | 0.98 | | | |
| RIS, $M = 4$, no reuse | 0.71 | | | |
| RIS, $M = 16$, no reuse | 0.60 | | | |
| temporal reuse only, unbiased | 0.71 | 0.50 | 0.36 | 0.25 |
| temporal and spatial, unbiased ($1 / Z$) | 0.66 | 0.64 | 0.69 | 0.79 |
| temporal and spatial, unbiased (balance) | 0.67 | 0.64 | 0.69 | 0.76 |
| temporal and spatial, biased ($1 / M$) | 0.50 | 0.41 | 0.35 | 0.31 |

The unbiased rows all have means within the statistical error of the exact sums. The biased row is too dark: its mean is 13 percent below the exact value over the pixels in frame 1 and 46 percent below in frame 8. In this small scene, temporal reuse alone works best. Spatial reuse helps in frame 1, but here the neighbors are far apart and see different lights, and the mismatch is carried on from frame to frame, so the unbiased spatial rows do not improve after frame 2. These are measurements on one scene, not bounds.

## Correctness

The key notion is an *unbiased contribution weight*: a pair $(y, W)$ is one for a set $S$ of lights if $E[g(y) W] = \sum_{y \in S} g(y)$ for every function $g$. Then $E[f_q(y) W] = I_q$ when $S$ is the set $S_q$ of lights that pixel $q$ sees with $\hat p_q > 0$.

- **RIS.** Given the candidates, the reservoir keeps $x_i$ with probability $w_i / w_{\text{sum}}$, so $E[g(y) W \mid x] = \frac1M \sum_i g(x_i) / p(x_i)$ over the candidates with $\hat p_q > 0$, whose mean is $\sum_{y : \hat p_q(y) > 0} g(y)$. Setting $W = 0$ for blocked lights cuts the set to $S_q$.
- **COMBINE.** With the weights of line L10, the chosen input $r$ ends with $W = \mu_r(y)\, w_{\text{sum}} / (M_r \hat p_q(y))$, where $\mu_r = M_r / Z$ in line L11. For each light, the $\mu_r$ of the inputs that can produce it sum to $1$, the MIS condition, and linearity gives a UCW for the union of the input sets. No independence between the inputs is needed, which is what makes reuse between pixels legal.
- **The biased merge.** With $1 / \sum_i M_i$ in place of $1 / Z$, a light gets the share $c(y) = \sum_{r : y \in S_{o_r}} M_r / \sum_i M_i \le 1$, so the mean is $\sum_y f_q(y) c(y) \le I_q$. It is exact only where all merged pixels see the same lights.

By induction over the frames, every reservoir stored for pixel $q$ is a UCW for $S_q$, so every frame is unbiased with lines L11 or the balance weight. The [proof](proofs/correctness.md) gives the details. The tests check the RIS and the merge results exactly with Fraction, by listing every outcome, and check frames of the geometric scene within 4 standard errors.

## Complexity

One frame does $M$ target evaluations and one shadow ray per pixel for RIS and visibility reuse, a COMBINE of two inputs for temporal reuse and of $k + 1$ inputs for spatial reuse, and one shading evaluation. A target evaluation costs $O(1)$ and traces no ray. The unbiased merge adds one shadow ray per input. So a frame costs $\Theta(P (M + (k + 1) c))$ time, where $c$ is the cost of one shadow ray, and $\Theta(P)$ extra space for two buffers of reservoirs. The cost per pixel does not depend on the number of lights, except through the cost of sampling $p$, which is $O(1)$ for the uniform density and $O(\log L)$ for $L$ lights with an alias table or a tree.

The variance has no general bound. RIS with $M$ candidates and a target equal to $f_q$ has the variance of the mean of $M$ plain samples, as in the example, and reuse can make the effective $M$ large; but when the target ignores visibility, or the merged pixels differ, the gain can be small or negative.

## Properties

- **Unbiased or not, by choice.** The $1 / Z$ and the balance merges are unbiased; the $1 / M$ merge is biased toward dark. Bitterli and others give both and use the biased one where speed matters more.
- **Correlated.** Pixels share samples, and frames share samples. The error is not independent from pixel to pixel, so it looks like blotches, not like fine noise, and a denoiser must expect that.
- **Constant cost per pixel.** The number of shadow rays per pixel is fixed and small, whatever the number of lights.
- **Streaming.** A reservoir sees each candidate once and keeps $O(1)$ state.

## Variants and improvements

- **ReSTIR GI and ReSTIR PT.** The same reuse for the incident light at the first bounce (Ouyang and others, 2021) and for whole paths (Lin and others, 2022), where a reused sample must be moved to the new pixel by a shift map with its Jacobian.
- **Generalized RIS.** Lin, Kettunen, Bitterli, Pantaleoni, Yuksel and Wyman (2022) stated the theory for samples from different domains, with resampling MIS weights in the weights of line L10 in place of the $1 / Z$ count after the choice.
- **Better targets.** A target with a cheap visibility guess, or the BSDF in it, keeps blocked lights out.
- **Better candidates.** A light tree or a [path guiding](/path-guiding/) density as $p$, so that the candidates are already good.
- **Reservoirs of more lights.** A reservoir of size $s$ keeps $s$ lights, with $s$ shadow rays per pixel.

## When to use it

Use ReSTIR for real-time or interactive direct light from many lights with a budget of one or a few shadow rays per pixel, when the camera and the lights move slowly enough that the last frame is still useful. Use the unbiased merge when the image must converge to the right answer, for example for reference renders that average many frames. For offline rendering with many samples per pixel, plain [next event estimation](/next-event-estimation/) with a good light selection and [multiple importance sampling](/multiple-importance-sampling/) is simpler and has no correlation between pixels.

## Pitfalls

- **Dividing by all $M$ and calling it unbiased.** The $1 / M$ merge is biased. The darkening is worst at the edges of shadows and where neighbors have different normals or materials.
- **A target with zeros.** If $\hat p_q(y) = 0$ where $f_q(y) > 0$, those lights are never picked, and the estimate misses their light. The tests show the exact loss.
- **No cap on the temporal $M$.** Without the cap, the old reservoir stands for an ever larger count and new candidates hardly ever replace it, so the image reacts slowly to change.
- **Reading reservoirs that are being written.** Spatial reuse must read the buffer from before the spatial pass. Writing in place makes the result depend on the pixel order.
- **Stale samples in moving scenes.** A light from the last frame must be checked with the target and the visibility of this frame, or the weights are wrong.
- **Expecting reuse to always help.** Neighbors that see different lights add variance; in the example above, spatial reuse makes the unbiased estimate worse after frame 2. Reject neighbors with different normals or depths, as the paper does.

## Implementations

## History

Talbot, Cline and Egbert (2005) introduced resampled importance sampling for rendering: draw candidates from a simple density and resample one of them by a better target. Chao (1982) had given the one-pass rule for weighted sampling that a reservoir of size one uses. Bitterli, Wyman, Pharr, Shirley, Lefohn and Jarosz (2020) put the two together, added visibility, temporal and spatial reuse, and showed direct light from millions of lights in real time. Lin and others (2022) gave the general theory, and later work extended the method to indirect light and to whole paths.

## References
