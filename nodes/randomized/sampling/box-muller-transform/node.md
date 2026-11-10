---
tag: D2WV7Z
kind: algorithm
slug: box-muller-transform
name: Box-Muller transform
aliases:
- Box-Muller method
area: randomized/sampling
level: intro
summary: Turns two independent uniforms into two independent standard normal variates.
solves: [random-variate-generation]
model: real-ram
complexity:
  vars: {n: the number of normal variates}
  time: {worst: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: false, exact: true, online: true, recursive: false}
history:
  year: 1958
  people: [George E. P. Box, Mervin E. Muller]
  note: Box and Muller published the transform in the Annals of Mathematical Statistics in 1958.
prereqs: [uniform-distribution, probability-density-function, change-of-variables]
see_also: [marsaglia-polar-method, ziggurat-method, inverse-transform-sampling, random-variate-generation, ratio-of-uniforms, central-limit-theorem]
sources:
  - paper: doi:10.1214/aoms/1177706645
    title: George E. P. Box and Mervin E. Muller, A note on the generation of random normal deviates, Annals of Mathematical Statistics 29(2), 1958
    locator: pages 610 to 611
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter V, Section 4 (the polar method and radially symmetric distributions), and Chapter IX, Section 1 (the normal density)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.1, Part C (the normal distribution)
  - paper: doi:10.1137/1006063
    title: George Marsaglia and Thomas A. Bray, A convenient method for generating normal variables, SIAM Review 6(3), 1964
    locator: pages 260 to 264
  - paper: "Henry R. Neave, On using the Box-Muller transformation with multiplicative congruential pseudo-random number generators, Applied Statistics 22(1), 1973"
    locator: pages 92 to 97
---

The Box-Muller transform turns two independent uniform reals $U_1, U_2$ into two independent standard normal variates $Z_1 = \sqrt{-2 \ln U_1} \cos(2\pi U_2)$ and $Z_2 = \sqrt{-2 \ln U_1} \sin(2\pi U_2)$. It is a transformation method of [random variate generation](/random-variate-generation/): one formula, no loop and no rejection. The proof is a two-dimensional [change of variables](/change-of-variables/). The [Marsaglia polar method](/marsaglia-polar-method/) computes the same thing without the sine and cosine, and the [ziggurat method](/ziggurat-method/) is faster still.

## In plain words

One uniform number is not easy to turn into one bell-curve number, because the inverse of the bell-curve's cumulative function has no simple formula. Two at a time is easy.

Pick a random point in the plane whose two coordinates are independent bell-curve numbers. Its direction is uniform: every angle is equally likely, because the bell curve in two dimensions is round. Its squared distance from the center has a simple law, the exponential law, which one logarithm makes from a uniform number.

So the method goes backward. It makes a uniform angle from one uniform number and a distance from the other. The point at that angle and distance has two coordinates. They are exactly two independent bell-curve numbers.

## The problem

The task is to generate independent variates with the standard normal density $\varphi(x) = (2\pi)^{-1/2} e^{-x^2/2}$. Then $\mu + \sigma Z$ is normal with mean $\mu$ and variance $\sigma^2$. This is a case of the [random variate generation](/random-variate-generation/) problem.

The model is the [real RAM](/real-ram/) of Devroye: a source of independent uniform reals, exact arithmetic, and $\ln$, $\sqrt{\ }$, $\cos$ and $\sin$ at unit cost.

## The algorithm

```pseudo id=main
BOX-MULLER()
L1  U1 ← a uniform real in (0, 1]          ▷ not 0, because of ln
L2  U2 ← a uniform real in [0, 1)
L3  R ← √(−2 ln U1)                        ▷ the radius: R² is exponential with mean 2
L4  Θ ← 2π · U2                            ▷ the angle, uniform on [0, 2π)
L5  return (R cos Θ, R sin Θ)
```

Line L3 is [inverse transform sampling](/inverse-transform-sampling/) for $R^2$: if $\Pr[R^2 > s] = e^{-s/2}$, then $R^2 = -2 \ln U_1$ with a uniform $U_1$. Line L4 makes a uniform angle. Line L5 turns the polar coordinates $(R, \Theta)$ into Cartesian ones. A program usually returns $Z_1$ and keeps $Z_2$ for the next call.

## Example

| $U_1$ | $U_2$ | $R$ | $\Theta$ | $Z_1 = R \cos\Theta$ | $Z_2 = R \sin\Theta$ |
|---|---|---|---|---|---|
| 0.25 | 0.10 | 1.6651 | 0.6283 | 1.3471 | 0.9787 |
| 0.90 | 0.60 | 0.4590 | 3.7699 | $-0.3714$ | $-0.2698$ |
| 0.01 | 0.75 | 3.0349 | 4.7124 | 0.0000 | $-3.0349$ |

In the first row, $R = \sqrt{-2 \ln 0.25} = \sqrt{2.7726} = 1.6651$ and $\Theta = 0.2\pi$. A small $U_1$ gives a large radius: $U_1 = 0.01$ gives $R = \sqrt{-2 \ln 0.01} \approx 3.0349$, and $R$ exceeds this value exactly when $U_1 < 0.01$, which has probability $0.01$.

## Correctness

**Theorem.** If $U_1$ and $U_2$ are independent uniforms on $(0, 1]$ and $[0, 1)$, then the two outputs are independent, and each has the density $\varphi$.

The map $T(u_1, u_2) = (R\cos\Theta, R\sin\Theta)$ is a smooth bijection from $(0,1)^2$ onto the plane without a half-line. Its inverse is $u_1 = e^{-(z_1^2 + z_2^2)/2}$ and $u_2 = \arg z / (2\pi)$. The absolute value of the Jacobian determinant of the inverse is $\frac{1}{2\pi} e^{-(z_1^2 + z_2^2)/2}$. Since the uniform pair has density 1, the output has density $\frac{1}{2\pi} e^{-(z_1^2 + z_2^2)/2} = \varphi(z_1)\varphi(z_2)$, a product. A product density means independence. The full computation is in the proof below.

The method is exact for exact uniform reals and exact functions. In floating point it is not: see the pitfalls.

## Complexity

Each call costs one logarithm, one square root, one sine, one cosine and a few multiplications, and it uses two uniforms for two normals. So $n$ normal variates take $\Theta(n)$ time in the worst case: there is no loop and no rejection. In practice $\sin$ and $\cos$ are the slowest steps. The polar method replaces them by a division and a rejection loop that runs $4/\pi \approx 1.27$ times on average.

## Properties

- **Exact** in the real RAM model.
- **No rejection.** Each call uses exactly two uniforms. This matters for [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/), where the uniforms come from a low-discrepancy sequence and a rejection step would break the structure.
- **Not monotone.** $Z_1$ is not a monotone function of $(U_1, U_2)$, so the method does not keep the order of the inputs. The inversion $\Phi^{-1}(U)$ does, which helps with antithetic and stratified sampling.
- **Pairs.** The outputs come in independent pairs.

## Variants and improvements

- **[Marsaglia polar method](/marsaglia-polar-method/).** Draw a uniform point $(V_1, V_2)$ in the unit disk by rejection. Then $S = V_1^2 + V_2^2$ plays the role of $U_1$ and $(V_1, V_2)/\sqrt{S}$ is $(\cos\Theta, \sin\Theta)$. No trigonometric function is needed.
- **[Ziggurat method](/ziggurat-method/).** A table-based rejection method. It is several times faster when many variates are needed.
- **Inversion.** $Z = \Phi^{-1}(U)$ with an accurate rational approximation of $\Phi^{-1}$, such as Wichura's algorithm AS 241. It uses one uniform per normal and is monotone.
- **The [ratio-of-uniforms](/ratio-of-uniforms/) method.** The Kinderman-Monahan normal generator is another exact method without trigonometric functions.
- **Multivariate normal.** For a covariance matrix $\Sigma = LL^{\mathsf T}$, the vector $\mu + LZ$ with independent standard normal entries $Z_i$ has mean $\mu$ and covariance $\Sigma$.
- **The sum of uniforms.** $\sum_{i=1}^{12} U_i - 6$ has mean 0 and variance 1, and by the [central limit theorem](/central-limit-theorem/) it is close to normal. It is not exact: it never leaves $[-6, 6]$.

## When to use it

Use Box-Muller when simple, exact code matters more than speed, or when each output must use a fixed number of uniforms, as in quasi-Monte Carlo. Use the polar method when trigonometric functions are slow. Use the ziggurat method when you need many normals fast. Use inversion when the output must be a monotone function of the uniform.

## Pitfalls

- **$\ln 0$.** Most generators return values in $[0, 1)$. With $U_1 = 0$, line L3 fails. Line L1 must use $1 - U$, a value in $(0, 1]$.
- **The factor 2.** $R = \sqrt{-\ln U_1}$ in line L3 gives normals with variance $1/2$, not 1. A goodness-of-fit test rejects it at once.
- **Correlated uniforms.** The theorem needs independent $U_1$ and $U_2$. Neave (1973) showed that consecutive values of a multiplicative congruential generator give visibly wrong tails with Box-Muller. Use a good generator, such as the [Mersenne Twister](/mersenne-twister/) or [PCG](/pcg-random/).
- **The float tails.** With 53-bit uniforms, $U_1 \ge 2^{-53}$, so $|Z_i| \le \sqrt{106 \ln 2} \approx 8.5717$. The event $|Z_1| > 8.5717$ has probability about $10^{-17}$ under the true law, so the bias does not matter for usual sample sizes, but the method is exact only in exact arithmetic. Code that needs extreme tails needs a tail method.
- **$\sin$ from $\cos$.** Computing $Z_2$ as $R\sqrt{1 - \cos^2 \Theta}$ loses the sign of $\sin\Theta$ and makes $Z_2 \ge 0$. Use $\sin$, or the polar method.
- **A cached second value in shared code.** A generator that keeps $Z_2$ for the next call has hidden state. Two threads that share it, or a reseed that does not clear it, give wrong or repeated values.

## Implementations

## History

Box and Muller published the transform in 1958, in a two-page note. Marsaglia and Bray (1964) gave the polar form without trigonometric functions. Neave (1973) showed how a poor uniform generator spoils the output.

## References
