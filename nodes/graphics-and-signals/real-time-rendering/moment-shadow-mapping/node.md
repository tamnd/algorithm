---
tag: ZPXE0M
kind: algorithm
slug: moment-shadow-mapping
name: Moment shadow mapping
aliases:
- moment shadow maps
area: graphics-and-signals/real-time-rendering
level: research
summary: Store four power moments of depth and compute the sharp lower bound on the occluded fraction, an upper bound on the lit fraction with less light leaking than variance shadow maps.
solves: [shadow-determination]
model: real-ram
complexity:
  vars: {w: the map width in texels, h: the map height in texels, q: the number of shadow lookups}
  time: {worst: Θ(w h + q)}
  space: {extra: Θ(w h)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2015
  people: [Christoph Peters, Reinhard Klein]
  note: Peters and Klein presented moment shadow mapping at I3D 2015. The bound is a classical result on the moment problem, which they made fast enough for a pixel shader.
prereqs: [variance-shadow-maps, cholesky-decomposition]
see_also: [percentage-closer-filtering, percentage-closer-soft-shadows, cascaded-shadow-maps, shadow-mapping, chebyshev-inequality, mipmap]
sources:
  - paper: doi:10.1145/2699276.2699277
    title: Christoph Peters and Reinhard Klein, Moment shadow mapping, Proceedings of the 19th Symposium on Interactive 3D Graphics and Games (I3D 2015), 7 to 14
    locator: the Hamburger 4MSM lookup (the Cholesky solve, the quadratic and the three cases), the moment bias with alpha = 3e-5 in the supplementary Algorithm 3, and the comparison with variance shadow maps
  - paper: "M. G. Krein and A. A. Nudel'man, The Markov Moment Problem and Extremal Problems, Translations of Mathematical Monographs 50, American Mathematical Society, 1977"
    locator: Theorem IV.3.1 (the sharp bound from the canonical representation, as cited by Peters and Klein)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 7, the part on filtered shadow maps (general locator)
---

Moment shadow mapping stores the first four powers of the depth, $z, z^2, z^3, z^4$, at each texel and filters them like [variance shadow maps](/variance-shadow-maps/) filter their two moments. The lookup solves a small linear system and a quadratic to get the sharp lower bound on the occluded fraction for these four moments, so $1 - G$ is an upper bound on the lit fraction. With four moments the bound is never weaker than the two-moment Chebyshev bound of variance shadow maps, and in scenes with several occluders it is much tighter, so the light leaking is smaller. It costs twice the storage and more arithmetic per lookup.

## In plain words

Variance shadow maps keep two summary numbers for the distances near each dot of the shadow map: the average and the spread. From them they estimate how much of the area is behind a point. When objects at very different distances overlap, the estimate is far too bright.

This method keeps two more numbers, from the cube and the fourth power of the distance. With four numbers it can tell more about the mix of distances. The lookup finds the mix of at most three distances that agrees with the four numbers and makes the point as bright as possible, and uses that brightness. The answer is never darker than the truth, and it is never brighter than the answer from two numbers.

## The problem

The input is a map of depths in the Direct3D range $[0, 1]$, smaller nearer, a filter, and lookups with a receiver depth $z$. The filter defines a distribution of the depths under it, as on the [variance shadow maps](/variance-shadow-maps/) page. The map stores the filtered power moments $b = (b_1, b_2, b_3, b_4)$ with $b_k$ the filtered mean of $z^k$. The *lit fraction* is the probability that a depth is at least $z_f$, the receiver depth after the bias. The output is the smallest value that is an upper bound on the lit fraction for every distribution with the moments $b$, together with tunings that make the computation stable.

## The algorithm

```pseudo id=main
MSM-LOOKUP(b, z, α, β)                            ▷ b = (b1, b2, b3, b4), receiver depth z
L1  b' ← (1 - α) b + α (1/2, 1/2, 1/2, 1/2)       ▷ the moment bias
L2  z_f ← z - β                                    ▷ the depth bias
L3  solve B c = (1, z_f, z_f^2) for B = [[1, b'1, b'2], [b'1, b'2, b'3], [b'2, b'3, b'4]] by Cholesky
L4  z2 < z3 ← the two roots of c3 x^2 + c2 x + c1
L5  if z_f ≤ z2 then G ← 0
L6  else if z_f ≤ z3 then G ← (z_f z3 - b'1 (z_f + z3) + b'2) / ((z3 - z2)(z_f - z2))
L7  else G ← 1 - (z2 z3 - b'1 (z2 + z3) + b'2) / ((z_f - z2)(z_f - z3))
L8  return 1 - clamp(G, 0, 1)                      ▷ the lit estimate
```

Line L3 uses the [Cholesky decomposition](/cholesky-decomposition/) $B = L D L^T$ of the Hankel matrix of the moments. Its two pivots are $d_1 = b_2 - b_1^2$, the variance, and $d_2$; both are positive when the filter holds at least three distinct depths. The roots $z_f$, $z_2$ and $z_3$ are the support of the *canonical distribution*: the distribution on three points with the moments $b$ that has a point at $z_f$. The value $G$ is its weight below $z_f$. Lines L6 and L7 are that weight in closed form, so the lookup needs no explicit solve for the weights.

The bias of line L1 mixes in a small amount of the distribution with half its mass at 0 and half at 1, whose moments are all $\tfrac12$. It keeps $B$ positive definite for maps with one or two distinct depths, such as a plane over a plane, and it hides the rounding of moments stored with few bits. Peters and Klein use $\alpha = 3 \cdot 10^{-5}$; this value is a tuning.

## Example

A filter holds three depths 0.2, 0.4 and 0.6 with equal weights. Then $b = (2/5, 14/75, 12/125, 98/1875)$, with the mean 0.4 and the variance $2/75$. There is no bias.

| receiver $z$ | VSM bound | MSM $1 - G$ | true lit fraction | support points |
|---|---|---|---|---|
| 0.8 | $1/7 = 0.1429$ | 0.01754 | 0 | 0.8, 0.22380, 0.53620 |
| 0.5 | $8/11 = 0.7273$ | 0.57961 | $1/3$ | 0.5, 0.21729, 0.66271 |
| 0.3 | 1 | 0.88416 | $2/3$ | 0.3 and two more |

At $z = 0.8$ all three depths are in front of the receiver. The variance bound shows 14 percent of the light, and the moment bound 1.75 percent. At $z = 0.3$ the receiver is in front of the mean, so the variance bound gives no information, but the moment bound still says that at least 11.6 percent is occluded.

**Two depths.** A filter with the depths 0.2 and 0.6 has a singular Hankel matrix, and line L3 cannot be solved. With $\alpha = 3 \cdot 10^{-5}$, the lookup at $z = 0.8$ returns 0.000122, where the true value is 0 and the variance bound is $0.04/(0.04 + 0.16) = 0.2$.

## Correctness

The proof file gives the full argument, and the tests check each claim against the true lit fraction of random distributions and against a direct solve of the canonical weights.

- **The kernel polynomial.** The solution $c$ of line L3 defines $K(x) = c_1 + c_2 x + c_3 x^2$ with $\int K q \, d\mu = q(z_f)$ for every quadratic $q$. From this, $K(z_f) > 0$, and $K$ has two real roots that differ from $z_f$, by a sum of squares argument.
- **The canonical distribution.** The three points $z_f, z_2, z_3$ carry positive weights that sum to 1 and reproduce all four moments.
- **The bound.** For each of the three cases of lines L5 to L7 there is a polynomial of degree 4 that lies above the step function of the lit set and meets it at the three points. Integrating it against any distribution with the moments $b$ gives lit fraction $\le 1 - G$, and the canonical distribution reaches it. So $G$ is the sharp lower bound on the occluded fraction, and $1 - G$ is the sharp upper bound on the lit fraction, over all distributions on the real line.
- **Better than two moments.** The set of distributions with four given moments is a subset of the set with two of them, so $1 - G$ is at most the variance bound.
- **The bias.** With the bias of line L1, the result is at least the true lit fraction minus $\alpha / 2$.

The depths lie in $[0, 1]$, but the support points can lie outside it. The bound is then still valid, but a distribution on $[0, 1]$ may not reach it.

## Complexity

The map pass computes four moments per texel, and any linear filter acts on them as on the two moments of variance shadow maps, in $\Theta(w h)$ for a summed-area table or a fixed-size blur. A lookup is $O(1)$: a $3 \times 3$ Cholesky solve, a quadratic and a few divisions, so $q$ lookups cost $\Theta(w h + q)$ in the worst case. The map takes four values per texel. Peters and Klein store them in 64 bits per texel with a quantization transform, or in 128 bits as floats.

## Properties

- **Sharp for four moments.** No lookup that sees only $b_1$ to $b_4$ can give a lower upper bound on the lit fraction (a proved property).
- **At most the variance bound.** The leak is never larger than that of variance shadow maps for the same filter (a proved property).
- **Filterable.** The moments are linear in the weights, so blurs, mipmaps and summed-area tables apply before the lookup.
- **Still leaks.** The bound is an upper bound, not the lit fraction. In the example it shows 58 percent of the light where the truth is 33 percent.
- **Sensitive to precision.** Without the bias of line L1, moments of one or two distinct depths, or moments rounded to 16 bits, make line L3 singular or unstable.

## Variants and improvements

- **Optimized quantization.** Peters and Klein store an affine transform of the moments in place of the raw powers, so that 16 bits per moment are enough with a small $\alpha$.
- **Hausdorff moments.** A variant uses the moment problem on a bounded interval, which knows that the depths lie in $[0, 1]$; it needs more work per lookup.
- **Soft shadows.** The filtered moments also give an estimate of the average blocker depth, so the blocker search of [percentage-closer soft shadows](/percentage-closer-soft-shadows/) can run on a summed-area table of moments.
- **Fewer moments.** [Variance shadow maps](/variance-shadow-maps/) keep two moments and the Chebyshev bound; exponential maps keep one moment of a warped depth.

## When to use it

Use moment shadow maps where filtered shadows are needed, as for variance shadow maps, and the light leaking of two moments is visible: scenes with several layers of occluders, such as foliage or buildings, or a large filter on a distant cascade. If the filter is small, [PCF](/percentage-closer-filtering/) is cheaper and exact for its taps. If memory bandwidth is tight, the four moments cost twice as much as two.

## Pitfalls

- **No moment bias.** With $\alpha = 0$ in line L1, a texel that holds one plane, or a plane over a plane, gives a singular $B$, and line L3 divides by zero.
- **Unsorted roots.** If line L4 does not order the roots so that $z_2 < z_3$, lines L5 and L6 test the wrong case and return a weight of the wrong node.
- **No depth bias.** With $\beta = 0$ in line L2, a lit receiver can lie a rounding error behind its own depth in the map, and the bound then darkens it a little; peaks of this kind show as acne.
- **Raw powers in 16 bits.** Storing $z^3$ and $z^4$ in 16 bits destroys the information that the lookup needs; use 32-bit floats or the quantization transform.
- **No clamp.** In floating point, $G$ from lines L6 and L7 can fall slightly outside $[0, 1]$; line L8 must clamp it.

## Implementations

## History

The bound that moment shadow mapping uses is a classical result on the moment problem, treated in the book of Krein and Nudel'man (1977) on the Markov moment problem. Peters and Klein brought it to shadows at I3D 2015, as the next step after the two moments of [variance shadow maps](/variance-shadow-maps/). They gave a closed form for four moments that fits in a pixel shader, the moment bias, and a quantization of the moments for 64 bits per texel. Later work by Peters and others used the same bounds for transparency and for other filterable signals.

## References
