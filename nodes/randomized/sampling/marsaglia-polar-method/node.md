---
tag: E555BW
kind: algorithm
slug: marsaglia-polar-method
name: Marsaglia polar method
aliases:
- polar method
- Marsaglia-Bray polar method
area: randomized/sampling
level: intro
summary: Normal variate generation that avoids trigonometric functions by rejection in the unit disk.
solves: [random-variate-generation]
model: real-ram
complexity:
  vars: {n: the number of normal variates}
  time: {expected: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: false, exact: true, online: true, recursive: false}
history:
  year: 1964
  people: [George Marsaglia, Thomas A. Bray]
  note: Marsaglia and Bray published the method in SIAM Review in 1964.
prereqs: [box-muller-transform, rejection-sampling, uniform-distribution]
see_also: [box-muller-transform, ziggurat-method, rejection-sampling, random-variate-generation, ratio-of-uniforms, geometric-distribution]
sources:
  - paper: doi:10.1137/1006063
    title: George Marsaglia and Thomas A. Bray, A convenient method for generating normal variables, SIAM Review 6(3), 1964
    locator: pages 260 to 264
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.1, Part C, Algorithm P (the polar method for normal deviates)
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter V, Section 4 (the polar method)
---

The Marsaglia polar method generates two independent standard normal variates from a uniform random point $(V_1, V_2)$ in the unit disk: with $S = V_1^2 + V_2^2$, it returns $V_1 \sqrt{-2\ln S / S}$ and $V_2 \sqrt{-2 \ln S / S}$. It finds the point by [rejection sampling](/rejection-sampling/) from the square $[-1, 1)^2$, which succeeds with probability $\pi/4$ per try. It is the [Box-Muller transform](/box-muller-transform/) in disguise: $S$ is a uniform number and $(V_1, V_2)/\sqrt{S}$ is a uniform direction. So it needs a logarithm, a division and a square root, but no sine or cosine.

## In plain words

The Box-Muller method needs a random direction, and it makes one with a sine and a cosine. Those are slow on many machines.

There is a cheaper way to get a random direction. Throw darts at a square until one lands inside the circle drawn in it. That dart is a random point of the disk, and the line from the center to it points in a random direction. About four darts in five land inside, so this is quick.

The same dart gives more. Its squared distance from the center is itself a uniform random number, and it does not depend on the direction. So one dart gives both things that Box-Muller needs: a uniform number and a direction. A little arithmetic turns them into two bell-curve numbers.

## The problem

Generate independent variates with the standard normal density $\varphi(x) = (2\pi)^{-1/2} e^{-x^2/2}$. This is a case of [random variate generation](/random-variate-generation/). The model is the [real RAM](/real-ram/) with independent uniform reals, exact arithmetic, and unit-cost $\ln$ and $\sqrt{\ }$.

## The algorithm

```pseudo id=main
POLAR()
L1  repeat
L2      V1 ← a uniform real in [−1, 1);  V2 ← a uniform real in [−1, 1)
L3      S ← V1² + V2²
L4  until 0 < S < 1                        ▷ the point is in the disk, not the center
L5  F ← √(−2 ln S / S)
L6  return (V1 · F, V2 · F)
```

Lines L1 to L4 are rejection sampling of a uniform point in the disk. Line L5 is the only costly step. Since $V = \sqrt{S}\,(\cos\Theta, \sin\Theta)$, the output is $\sqrt{-2 \ln S}\,(\cos\Theta, \sin\Theta)$, the Box-Muller formula with $U_1 = S$ and $2\pi U_2 = \Theta$.

## Example

Four calls, with the points given directly. The first call needs two tries:

| call | try | $(V_1, V_2)$ | $S$ | result | $F$ | output |
|---|---|---|---|---|---|---|
| 1 | 1 | $(0.9, 0.9)$ | 1.62 | reject, outside the disk | | |
| 1 | 2 | $(-0.3, 0.4)$ | 0.25 | accept | 3.3302 | $(-0.9991, 1.3321)$ |
| 2 | 1 | $(0.6, 0.0)$ | 0.36 | accept | 2.3824 | $(1.4294, 0.0000)$ |
| 3 | 1 | $(0.5, -0.5)$ | 0.50 | accept | 1.6651 | $(0.8326, -0.8326)$ |
| 4 | 1 | $(0.1, 0.2)$ | 0.05 | accept | 10.9467 | $(1.0947, 2.1893)$ |

In the second row, $F = \sqrt{-2 \ln 0.25 / 0.25} = \sqrt{2.7726 / 0.25} = 3.3302$. The point $(0.5, -0.5)$ has $S = 0.5$, and its output has radius $\sqrt{-2 \ln 0.5} = 1.1774$: a point near the edge of the disk gives a small output, and a point near the center gives a large one.

## Correctness

**Theorem.** POLAR returns two independent standard normal variates. The number of tries is geometric with success probability $\pi/4$.

Each try is accepted with probability $\operatorname{area}(\text{disk}) / \operatorname{area}(\text{square}) = \pi/4$, and the accepted point is uniform on the disk, as for any rejection from a region. For a uniform point in the disk, $\Pr[S \le s, \Theta < t] = (st/2)/\pi = s \cdot \frac{t}{2\pi}$, the area of a sector over the area of the disk. This product form shows that $S$ is uniform on $(0, 1)$, $\Theta$ is uniform on $[0, 2\pi)$, and they are independent. Then the output is the Box-Muller transform of two independent uniforms, which is correct by the Jacobian argument of that page. The full proof is below.

The method is exact for exact uniform reals and exact arithmetic.

## Complexity

- **Tries.** The number of tries $N$ per pair is [geometric](/geometric-distribution/): $\mathbb{E}[N] = 4/\pi \approx 1.2732$ and $\Pr[N > k] = (1 - \pi/4)^k \approx 0.2146^k$.
- **Uniforms.** A pair uses $8/\pi \approx 2.5465$ uniforms in expectation, about $1.27$ per normal. Box-Muller uses exactly 1 per normal.
- **Time.** $n$ normals take $\Theta(n)$ expected time. There is no worst-case bound for every random string, since each try can fail.
- **Operations per pair.** One $\ln$, one division, one $\sqrt{\ }$, and $1.27$ tries of two multiplications and one comparison, in expectation.

## Properties

- **Exact** in the real RAM model.
- **No trigonometric functions.**
- **Rejection.** The number of uniforms per output is random. This breaks the structure of quasi-Monte Carlo point sets, where Box-Muller or inversion is the right choice.
- **Pairs.** The two outputs of one call are independent.

## Variants and improvements

- **[Box-Muller transform](/box-muller-transform/).** The same output law with $\sin$ and $\cos$ and no rejection.
- **[Ziggurat method](/ziggurat-method/).** Faster on most machines, since the common case needs one table lookup, one multiplication and one comparison.
- **Other radial laws.** For any spherically symmetric law in two dimensions, the direction $(V_1, V_2)/\sqrt{S}$ is uniform and independent of $S$. So the same rejection step gives a uniform direction for other radial laws, with a different radius in line L5. Devroye treats this family.
- **Higher dimensions.** A uniform point in the $d$-dimensional ball by rejection from the cube gives a uniform direction too, but the acceptance probability, the volume of the ball over $2^d$, falls fast: it is $\pi/6 \approx 0.52$ for $d = 3$ and below $0.0025$ for $d = 10$. For a direction in high dimension, normalize a vector of independent normals instead.

## When to use it

Use the polar method when you need an exact normal generator in a few lines of code and trigonometric functions are slow. Use Box-Muller when each output must use a fixed number of uniforms. Use the ziggurat method when speed matters most.

## Pitfalls

- **The center.** Line L4 must reject $S = 0$, or line L5 computes $\ln 0 / 0$. Some code tests only $S < 1$.
- **The boundary $S = 1$.** With $S = 1$, line L5 gives $F = 0$ and the output $(0, 0)$ more often than it should. Reject $S \ge 1$.
- **The division by $S$.** Line L5 needs $\sqrt{-2 \ln S / S}$. With $\sqrt{-2 \ln S}$, the output is $\sqrt{S}$ times too small in each coordinate, and the law is wrong.
- **Uniforms on $[0, 1)$.** The points must be uniform on the whole square $[-1, 1)^2$, so map $U \mapsto 2U - 1$. A point in $[0, 1)^2$ gives only positive outputs.
- **Floating point.** With 53-bit uniforms, $V_i$ is a multiple of $2^{-52}$, so $S \ge 2^{-104}$ and $|Z_i| \le \sqrt{208 \ln 2} \approx 12.01$. The output is a finite set of values, so the method is exact only in exact arithmetic, although the error is far below any test.

## Implementations

## History

Marsaglia and Bray published the method in 1964, as a fast way to get normal variates on the computers of the time. Knuth gives it as Algorithm P in Section 3.4.1. Devroye places it in a general family of polar methods for radially symmetric laws.

## References
