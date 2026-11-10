---
tag: 0RX5CX
kind: algorithm
slug: ziggurat-method
name: Ziggurat algorithm
aliases:
- Ziggurat method
- ziggurat
area: randomized/sampling
level: advanced
summary: Fast normal and exponential variate generation using a stack of rectangles covering the density.
solves: [random-variate-generation]
model: real-ram
complexity:
  vars: {n: the number of variates, N: the number of layers}
  time: {setup: Θ(N), expected: Θ(n)}
  space: {extra: Θ(N)}
properties: {deterministic: false, exact: true, online: true, recursive: false}
history:
  year: 2000
  people: [George Marsaglia, Wai Wan Tsang]
  note: Marsaglia and Tsang gave the method in 1984 and the fast form with 128 layers for the normal density in 2000.
prereqs: [rejection-sampling, probability-density-function, uniform-distribution]
see_also: [box-muller-transform, marsaglia-polar-method, rejection-sampling, alias-method, random-variate-generation, pseudorandom-number-generator, inverse-transform-sampling]
sources:
  - paper: doi:10.18637/jss.v005.i08
    title: George Marsaglia and Wai Wan Tsang, The ziggurat method for generating random variables, Journal of Statistical Software 5(8), 2000
    locator: the whole paper (the layers, the constants r and v for N = 128, the tail method)
  - paper: "George Marsaglia and Wai Wan Tsang, A fast, easily implemented method for sampling from decreasing or symmetric unimodal density functions, SIAM Journal on Scientific and Statistical Computing 5(2), 1984"
    locator: pages 349 to 359
  - paper: doi:10.18637/jss.v012.i07
    title: Philip H. W. Leong, Ganglie Zhang, Dong-U Lee, Wayne Luk and John D. Villasenor, A comment on the implementation of the ziggurat method, Journal of Statistical Software 12(7), 2005
    locator: pages 1 to 4
  - paper: "Jurgen A. Doornik, An improved ziggurat method to generate normal random samples, technical report, University of Oxford, 2005"
    locator: the whole report
  - paper: doi:10.1145/1287620.1287622
    title: David B. Thomas, Wayne Luk, Philip H. W. Leong and John D. Villasenor, Gaussian random number generators, ACM Computing Surveys 39(4), 2007
    locator: the section on the ziggurat method
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter VIII (table methods)
---

The ziggurat method generates normal (and exponential) variates by [rejection sampling](/rejection-sampling/) from a cover made of $N$ horizontal layers of equal area: a base layer that holds the tail, and $N - 1$ rectangles stacked on it like the steps of a ziggurat. Pick a layer uniformly and a uniform point in it; keep the point if it is under the density. The layers fit the density so closely that, for the normal density with $N = 128$, about 97% of tries end after one table lookup, one multiplication and one comparison, with no $\ln$, $\exp$ or $\sqrt{\ }$. Marsaglia and Tsang published the fast form in 2000.

## In plain words

Draw the right half of the bell curve. Cut the area under it into thin horizontal slices, and replace each slice by the smallest rectangle that holds it. Choose the slice heights so that every rectangle has the same area. The bottom slice is special: it holds the long thin tail too.

To get a number, pick one of the rectangles at random. Since they all have the same area, this is the same as picking a point uniformly from the whole stack. Then pick a random spot across the rectangle. Most rectangles stick out past the curve only at their right end. If the spot is left of the rectangle above, it is surely under the curve, and you are done. Only in the thin sliver at the right end do you need to compute the curve and check.

Flip a coin for the sign.

## The problem

Generate independent variates with the standard normal density $\varphi(x) = (2\pi)^{-1/2} e^{-x^2/2}$. This is a case of [random variate generation](/random-variate-generation/). Work with the unnormalized half density $f(x) = e^{-x^2/2}$ on $[0, \infty)$ and a random sign. The model is the [real RAM](/real-ram/) with independent uniform reals.

The table. Fix $N$ and a right edge $r$ for the base rectangle. Let $T = \int_r^\infty f$ be the tail area and $v = r f(r) + T$, the area of the base layer. Set $x_1 = r$, $y_1 = f(r)$, and for $i = 1, \dots, N - 2$,

$$y_{i+1} = y_i + v / x_i, \qquad x_{i+1} = f^{-1}(y_{i+1}) = \sqrt{-2 \ln y_{i+1}},$$

so that the rectangle $[0, x_i) \times [y_i, y_{i+1})$ has area $v$. The top layer has $y_N = y_{N-1} + v / x_{N-1}$ and $x_N = 0$. The value of $r$ is chosen so that $y_N = 1 = f(0)$: then the top layer just reaches the peak. The base layer gets a pseudo width $x_0 = v / f(r)$, so that a uniform $u \in [0, x_0)$ falls beyond $r$ with probability $T/v$, the share of the tail in the base layer.

For $N = 128$ Marsaglia and Tsang give $r = 3.442619855899$ and $v = 9.91256303526217 \times 10^{-3}$.

## The algorithm

```pseudo id=main
ZIGGURAT(x[0..N], y[0..N], r)
L1  loop
L2      i ← a uniform integer in {0, …, N−1};  s ← a uniform sign in {+1, −1}
L3      u ← U · x[i]                          ▷ U uniform in [0, 1)
L4      if u < x[i+1] then return s · u        ▷ fast path: under the layer above, so under f
L5      if i = 0 then return s · TAIL(r)       ▷ the base layer, beyond r
L6      h ← y[i] + U′ · (y[i+1] − y[i])        ▷ a uniform height in layer i
L7      if h < f(u) then return s · u          ▷ slow path: the sliver at the right end

TAIL(r)
T1  repeat
T2      E1 ← −ln(U1) / r;  E2 ← −ln(U2)
T3  until 2 · E2 > E1²
T4  return r + E1
```

Line L4 needs no function call: if $u < x_{i+1}$, then $f(u) > f(x_{i+1}) = y_{i+1}$, the top of layer $i$, so every height in the layer is under $f$. In the base layer the same test is $u < r$. Lines L6 and L7 run only for the points in the sliver $x_{i+1} \le u < x_i$. TAIL is Marsaglia's method for the normal tail beyond $r$: rejection from the exponential density $r e^{-r s}$ shifted to $r$, with acceptance probability $e^{-s^2/2}$.

## Example

Take $N = 128$ and the table built from $r = 3.44261985589$. Some entries:

| $i$ | $x_i$ | $x_{i+1}$ | $y_i$ | $y_{i+1}$ |
|---|---|---|---|---|
| 0 | 3.7131 | 3.4426 | 0 | 0.002670 |
| 1 | 3.4426 | 3.2231 | 0.002670 | 0.005549 |
| 5 | 2.8943 | 2.8231 | 0.015167 | 0.018592 |
| 127 | 0.2723 | 0 | 0.963600 | 1.000000 |

Three tries in layer $i = 5$:

1. $U = 0.5$. Then $u = 0.5 \cdot 2.8943 = 1.4472 < x_6 = 2.8231$. Line L4 returns $\pm 1.4472$ at once.
2. $U = 0.99$. Then $u = 2.8654 \ge 2.8231$, so the point is in the sliver. Here $f(u) = e^{-2.8654^2/2} = 0.016486$, between $y_5$ and $y_6$. With $U' = 0.2$, $h = 0.015167 + 0.2 \cdot 0.003425 = 0.015852 < f(u)$, and line L7 returns $\pm 2.8654$.
3. The same $u$ with $U' = 0.8$: $h = 0.017907 > f(u)$, so the try is rejected and the loop starts again with a new layer.

A try lands in the tail branch (line L5) only when $i = 0$ and $U \ge r / x_0 = 0.9272$, which has probability $(1 - 0.9272)/128 \approx 5.7 \times 10^{-4}$.

## Correctness

**Theorem.** If the layers have equal area $v$ and cover the region under $f$ (that is, $y_N \ge 1$), ZIGGURAT returns a standard normal variate. The number of tries is geometric with mean $Nv/\sqrt{\pi/2}$.

The layers are disjoint, and each point under $f$ lies in one of them: a point with height in $[y_i, y_{i+1})$ under $f$ has $f(x) > y_i = f(x_i)$, so $x < x_i$. Choosing a layer uniformly and a uniform point in it gives a uniform point in the union, because all layers have the same area. For the base layer, the branch $u \ge r$ is replaced by an exact sample of the tail, which is the $x$ coordinate of a uniform point under the tail. Keeping only points under $f$ is rejection sampling, so the kept $x$ has density proportional to $f$, the half-normal density. The random sign makes it normal. The full proof is below.

The proof needs equal areas and the cover, not $y_N = 1$ exactly. A top layer that reaches above 1 only wastes a little area. A top layer that ends below 1 leaves a gap near $x = 0$, and the method is then not exact.

## Complexity

- **Setup.** $\Theta(N)$ time and space for the table, once.
- **Tries.** For $N = 128$ the mean number of tries per variate is $Nv/\sqrt{\pi/2} \approx 1.0124$: the cover wastes only 1.2% of its area.
- **The fast path.** A try ends in line L4 with probability $\frac{1}{N}\bigl(\frac{r}{x_0} + \sum_{i=1}^{N-1} x_{i+1}/x_i\bigr) \approx 0.972$. This step costs one random integer, one multiplication and one comparison.
- **The slow path.** One $\exp$ per try in a sliver, and $1/0.93$ rounds with two logarithms each in the rare tail branch.
- **Total.** $n$ variates take $\Theta(N + n)$ expected time. There is no worst-case bound, as for any rejection method.

## Properties

- **Exact** in the real RAM model, when the table satisfies the cover condition.
- **Uses a table** of $2(N + 1)$ numbers.
- **Not monotone.** The output is not a monotone function of the uniforms, and the number of uniforms per output is random.
- **Fast.** On most hardware it is faster than the [Box-Muller transform](/box-muller-transform/) and the [Marsaglia polar method](/marsaglia-polar-method/), because the common case has no transcendental function.

## Variants and improvements

- **Integer form.** The code of Marsaglia and Tsang draws one 32-bit integer $j$, takes the layer index from its low bits and the signed value $u$ from $j$ itself, and compares $|j|$ with a precomputed integer threshold, so the fast path has no floating-point comparison.
- **Separate bits for the index.** Doornik (2005) noted that the published code takes the layer index and the value from the same random word, so they are not independent, and gave a variant that takes them from different bits. This page uses independent draws in line L2 and line L3.
- **The exponential density.** The same construction with $f(x) = e^{-x}$ and $N = 256$ layers gives exponential variates. The tail beyond $r$ needs no rejection there: by the memoryless property, $r$ plus a standard exponential has the right law.
- **Other densities.** Any monotone decreasing density, or a symmetric unimodal one, has a ziggurat. The tail needs its own exact method.
- **Table size.** More layers mean fewer slow tries and a larger table. $N = 128$ and $N = 256$ are common, because the index then comes from 7 or 8 random bits.

## When to use it

Use the ziggurat method when a program needs very many normal or exponential variates, as in large simulations. Use the [Box-Muller transform](/box-muller-transform/) or inversion when each output must use a fixed number of uniforms, as in quasi-Monte Carlo. Use inversion when the output must be a monotone function of the uniform. For a one-off variate, the setup is not worth it.

## Pitfalls

- **The uniform generator.** The method is exact only for independent uniforms. Leong, Zhang, Lee, Luk and Villasenor (2005) found that the C code published with the 2000 paper gives poorly distributed output in large samples because of the short period of its uniform generator, and that a uniform generator with a longer period fixes this. Use a good [pseudorandom number generator](/pseudorandom-number-generator/).
- **Index and value from the same bits.** See the variant above: they must be independent.
- **The cover.** Build the table so that the top layer reaches $f(0)$. With the 13-digit published $r$ and double precision, the top computed by the recursion ends about $4 \times 10^{-11}$ below 1. The error is far too small to see, but an exact table needs $r$ a little below the true root, as in the implementation here.
- **The tail.** Line L5 must sample the tail exactly. Returning $r$ plus an exponential with rate $r$, without the test in line T3, gives the wrong tail law.
- **The base layer width.** The base layer uses $x_0 = v/f(r)$, not $r$. With $x_0 = r$, the tail never comes out.
- **Floating point.** The table entries, $\ln$ and $\exp$ are rounded, and $u$ lies on a grid, so the method is exact only in exact arithmetic.

## Implementations

## History

Marsaglia and Tsang introduced the ziggurat for decreasing and symmetric unimodal densities in 1984. In 2000 they published a simpler and faster form with equal-area layers, $N = 128$ for the normal and $N = 256$ for the exponential, with C code. Leong and coauthors (2005) traced a failure of that code in large tests to its uniform generator, and Doornik (2005) proposed taking the layer index from separate bits. Thomas, Luk, Leong and Villasenor (2007) compared it with other Gaussian generators in a survey.

## References
