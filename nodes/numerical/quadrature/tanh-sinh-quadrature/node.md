---
tag: FDAEA3
kind: algorithm
slug: tanh-sinh-quadrature
name: Tanh-sinh quadrature
aliases:
- double exponential quadrature
- DE quadrature
- Takahasi-Mori quadrature
- DE rule
area: numerical/quadrature
level: advanced
summary: Double-exponential variable change followed by the trapezoid rule; handles endpoint singularities well.
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {K: "the number of halvings of the step", T: "the truncation point t_max", N: "the number of evaluations, at most 2 T 2^K + 1"}
  time: {worst: Θ(T 2^K), average: Θ(T 2^K), best: Θ(T 2^K)}
  space: {extra: Θ(T 2^K)}
properties: {deterministic: true, recursive: false}
prereqs: [trapezoidal-rule, improper-integration]
see_also: [sinc-quadrature, gauss-jacobi-quadrature, gauss-legendre-quadrature, adaptive-quadrature, clenshaw-curtis-quadrature, euler-maclaurin-formula, quadrature-error, romberg-integration]
sources:
  - paper: "Hidetosi Takahasi and Masatake Mori, Double exponential formulas for numerical integration, Publications of the Research Institute for Mathematical Sciences, Kyoto University 9, 1974, 721-741"
    locator: the tanh-sinh transformation, the optimality of double exponential decay, and the error estimate exp(-c N / log N)
  - paper: doi:10.1137/130932132
    title: Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3), 2014, 385-458
    locator: Section 5, Theorem 5.1 (the trapezoidal rule on the real line for functions analytic in a strip), and the later section on transformations of finite intervals (tanh and tanh-sinh)
  - paper: "Masatake Mori and Masaaki Sugihara, The double-exponential transformation in numerical analysis, Journal of Computational and Applied Mathematics 127, 2001, 287-296"
    locator: Section 2, the double exponential formula on (-1, 1), half-infinite and infinite intervals
  - paper: "Ken'ichiro Tanaka, Masaaki Sugihara, Kazuo Murota and Masatake Mori, Function classes for double exponential integration formulas, Numerische Mathematik 111, 2009, 631-655"
    locator: the function spaces on which the DE formula is near optimal, with explicit error bounds
  - paper: "David H. Bailey, Karthik Jeyabalan and Xiaoye S. Li, A comparison of three high-precision quadrature schemes, Experimental Mathematics 14(3), 2005, 317-329"
    locator: tanh-sinh against Gauss-Legendre and error-function quadrature at hundreds of digits
---

Tanh-sinh quadrature integrates $f$ over $[a, b]$ by substituting

$$x = \varphi(t) = c + r \tanh\!\big(\tfrac{\pi}{2}\sinh t\big), \qquad c = \tfrac{a + b}{2},\ r = \tfrac{b - a}{2},$$

which maps the real line onto $(a, b)$, and then applying the [trapezoidal rule](/trapezoidal-rule/) to $g(t) = f(\varphi(t))\,\varphi'(t)$ on $\mathbb{R}$, truncated to $|t| \le T$. The weight $\varphi'(t)$ decays like $\exp(-\frac{\pi}{2} e^{|t|})$, doubly exponentially, which flattens any algebraic or logarithmic singularity of $f$ at $a$ or $b$. Because the trapezoidal rule on $\mathbb{R}$ is spectrally accurate for analytic integrands that decay fast, the error falls like $\exp(-c N / \log N)$ in the number $N$ of evaluations, and in practice the number of correct digits roughly doubles each time the step is halved, singularities included. Takahasi and Mori introduced it in 1974.

## In plain words

Endpoint trouble is the hardest part of many integrals: the function shoots up to infinity at an end, or has an infinitely steep slope there, and ordinary rules converge slowly.

Tanh-sinh stretches the interval. A new variable runs over the whole number line, and the old interval is squeezed onto it so that the ends are pushed infinitely far away. Near the ends the squeeze is so strong that whatever the function does there is crushed to almost nothing. What is left is a smooth bump that dies off extremely fast on both sides, and for such bumps the simplest rule, equally spaced points with equal weights, is astonishingly accurate. Halving the spacing roughly doubles the number of correct digits, and the old points are reused.

## The problem

Given an oracle for $f$, continuous on $(a, b)$ and absolutely integrable, possibly singular at $a$ or $b$, and a tolerance $\tau$, approximate $I(f) = \int_a^b f(x)\,dx$. The end points may be infinite. Cost is counted in evaluations of $f$; nodes and weights are computed on the fly at $O(1)$ cost each. See [numerical integration](/numerical-integration/) and [improper integration](/improper-integration/).

## The algorithm

```pseudo id=main
TANH-SINH(f, a, b, τ, K, T)                ▷ finite a < b; b < a by negation, a = b gives 0
L1  if a = b then return 0
L2  c ← (a + b)/2;  r ← (b − a)/2
L3  h ← 1;  S ← Σ_{j = −⌊T⌋}^{⌊T⌋} TERM(j)
L4  Q_0 ← h · S
L5  for k ← 1 to K do
L6      h ← h/2
L7      S ← S + Σ_{j odd, |j| ≤ ⌊T/h⌋} TERM(j h)
L8      Q_k ← h · S
L9      if |Q_k − Q_{k−1}| ≤ τ then return Q_k
L10 return Q_K

TERM(t)
L11 u ← (π/2) sinh|t|;  e ← exp(−2u);  δ ← 2e/(1 + e);  ω ← (π/2) cosh t · 4e/(1 + e)^2
L12 x ← b − rδ if t ≥ 0, else x ← a + rδ
L13 return r · ω · f(x)
```

Line L11 computes the distance $\delta = 1 - \tanh u$ from the node to the nearer end, and the weight $\varphi'/r$, from $e = e^{-2u}$, with no cancellation: far out, $\delta$ is $10^{-100}$ or smaller and still correct to full relative precision. Line L12 places the node at that distance from the end, so nodes near $a = 0$ are represented exactly as tiny numbers. Near an end that is not 0, $x = b - r\delta$ rounds to $b$ once $r\delta$ is below half an ulp of $b$; the implementation then evaluates $f(b)$ if it is finite and drops the term if $f$ is singular there, and it can instead pass the accurate distances $x - a$ and $b - x$ to $f$, so that an integrand like $(b - x)^{-1/2}$ is evaluated from $b - x$ directly. Lines L3 to L8 are the halving scheme of [Romberg integration](/romberg-integration/) without the extrapolation: every level keeps the previous sum and adds the odd multiples of the new step. Infinite intervals are first mapped to $[0, 1)$ by $x = a + u/(1 - u)$.

## Example

For $\int_0^1 \sqrt{x}\log x\,dx = -\tfrac49$, singular in the derivative at 0, and for $\int_{-1}^{1} (1 - x^2)^{-1/2}\,dx = \pi$, infinite at both ends, with $T = 4$ (the second with accurate distances):

| level $k$ | step $h$ | evaluations | error, $\sqrt{x}\log x$ | error, $(1 - x^2)^{-1/2}$ |
|---|---|---|---|---|
| 0 | 1 | 9 | $1.0 \times 10^{-2}$ | $1.9 \times 10^{-3}$ |
| 1 | 1/2 | 17 | $5.2 \times 10^{-6}$ | $2.0 \times 10^{-8}$ |
| 2 | 1/4 | 33 | $3.3 \times 10^{-13}$ | $4.4 \times 10^{-16}$ |
| 3 | 1/8 | 65 | $0$ | $0$ |

The exponent of the error roughly doubles from one level to the next. For comparison, [Gauss-Legendre](/gauss-legendre-quadrature/) with $n = 8, 16, 32, 64, 128$ points has errors $8.7 \times 10^{-4}$, $1.5 \times 10^{-4}$, $2.3 \times 10^{-5}$, $3.5 \times 10^{-6}$, $5.1 \times 10^{-7}$ on the first integral and $0.20$, $0.11$, $0.054$, $0.027$, $0.014$ on the second: algebraic convergence, $O(n^{-1})$ for the second, because the singularities are not resolved. A [Gauss-Jacobi rule](/gauss-jacobi-quadrature/) with the weight $(1 - x^2)^{-1/2}$ would be exact for the second integral, but only because the singularity is known in advance; tanh-sinh needs no such knowledge.

Other integrals, with default settings ($T = 6$, $\tau = 10^{-12}$): $\int_0^1 \log x = -1$, $\int_0^1 x^{-1/2} = 2$ and $\int_0^1 x^{-0.9} = 10$ all come out with errors below $2 \times 10^{-15}$ from fewer than 100 evaluations; $\int_0^\infty e^{-x} = 1$ and $\int_{-\infty}^{\infty} (1 + x^2)^{-1} = \pi$ have errors below $10^{-15}$.

## Correctness

The full proof is in the correctness file. The map $\varphi$ is a smooth increasing bijection of $\mathbb{R}$ onto $(a, b)$, so $I(f) = \int_{\mathbb{R}} g$ for $g = (f \circ \varphi)\varphi'$ (Lemma 1). Line L11 computes $b - \varphi(t)$ and $\varphi'(t)$ through identities in $e^{-2u}$ that involve no cancellation (Lemma 2). The running sum after level $k$ is exactly the trapezoidal sum with step $h_k = 2^{-k}$ over $|t| \le T$ (Lemma 3). If $g \in C^1$ with $g' \in L^1(\mathbb{R})$, then

$$\big|Q_k - I(f)\big| \le h_k \|g'\|_{L^1} + \int_{|t| > T - h_k} \big(|g| + h_k |g'|\big)\,dt,$$

which is proved there; this gives convergence. The fast rate is cited: if $f$ is analytic in a region whose preimage contains the strip $|\operatorname{Im} t| < d$, $d \le \pi/2$, with $g$ integrable on horizontal lines with bound $M$, the untruncated sum has error at most $2M/(e^{2\pi d/h} - 1)$ (Trefethen and Weideman 2014, Theorem 5.1), and the truncation error decays like $\exp(-c\, e^{T})$. Choosing $T \approx \log(N / \log N)$ gives an error $O(\exp(-c' N / \log N))$, with $c'$ depending on $d$ and on the strength of the endpoint singularities (Takahasi and Mori 1974; Tanaka et al. 2009). Each result is labelled in the proof as proved or cited.

## Complexity

A run that stops at level $K$ evaluates $f$ at most $2\lfloor T 2^K \rfloor + 1$ times, each point once; nodes and weights cost $O(1)$ each (one $\sinh$, one $\cosh$, one $\exp$). Arithmetic is $O(N)$ with $N$ the number of evaluations, and the implementation holds the new terms of one level for the compensated sum, $O(N)$ memory, though a running sum would need $O(1)$. For analytic $f$ with algebraic endpoint singularities, reaching error $\tau$ needs $N = O(\log(1/\tau)\, \log\log(1/\tau))$ evaluations (asymptotic, from the rate above). In double precision this is typically 50 to 200 evaluations; at hundreds of digits, tanh-sinh is the usual method because nodes and weights are cheap to compute at any precision while Gauss nodes are not.

## Properties

- **Weights are positive.** All $\varphi'(t_j) > 0$ and $h \sum_j \varphi'(t_j) \to b - a$, so the rule is stable: $\sum |w_i| = \sum w_i \approx b - a$.
- **Not polynomial.** It is not exact for polynomials, not even for constants, since every level carries a small discretization and truncation error; degree of exactness is the wrong measure of its quality.
- **Nested.** Halving the step reuses all earlier values, so the difference of two levels costs nothing extra.
- **Insensitive to endpoint behaviour.** Singularities of the form $(x - a)^{\alpha - 1}$, $\log(x - a)$ and their products are handled without being identified, as long as $f$ is analytic inside.
- **Sensitive to interior behaviour.** A kink, jump or near singularity inside $(a, b)$ becomes one inside $\mathbb{R}$ and limits the rate.

## Variants and improvements

- **Exp-sinh and sinh-sinh.** For $[0, \infty)$ use $x = \exp(\frac{\pi}{2}\sinh t)$, and for $\mathbb{R}$ use $x = \sinh(\frac{\pi}{2}\sinh t)$, which keep double exponential decay when $f$ decays only algebraically; the implementation here instead maps $[a, \infty)$ to $[0, 1)$ rationally, which is simpler and works well for exponentially and moderately algebraically decaying $f$. Mori and Sugihara (2001) list these transforms.
- **Oscillatory tails.** For $\int_0^\infty f(x)\sin(\omega x)\,dx$, the Ooura-Mori transformation puts the nodes asymptotically at the zeros of the sine. See [oscillatory integration](/oscillatory-integration/).
- **Other single exponential maps.** $x = \tanh t$ gives [sinc quadrature](/sinc-quadrature/) in Stenger's form, with error $\exp(-c\sqrt{N})$: slower, but with a clean theory in Hardy spaces.
- **Faster stopping.** Since digits about double per level, the error of $Q_k$ is close to $|Q_k - Q_{k-1}|^2 / |Q_{k-1} - Q_{k-2}|$; codes such as those of Bailey use such estimates to stop one level earlier than the conservative test of line L9.
- **Splitting.** For an interior singularity or kink at a known point $p$, integrate over $[a, p]$ and $[p, b]$: the point becomes an endpoint and is handled at full speed.
- **Multiple precision.** The same code works at any precision, with $T$ and the number of levels growing slowly with the number of digits.

## When to use it

- Integrands analytic in the interior and singular, or merely rough, at the ends, with the singularity unknown or awkward to factor out.
- High-precision work, from 30 to thousands of digits, as in experimental mathematics.
- Half-infinite and infinite intervals with smoothly decaying integrands.
- Not for smooth integrands where [Gauss-Legendre](/gauss-legendre-quadrature/) or [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) reach the same accuracy with fewer points, nor for interior kinks, jumps or peaks unless the interval is split there; [adaptive quadrature](/adaptive-quadrature/) is the general tool for those.

## Pitfalls

- **Lost precision at a nonzero end.** With $f(x) = (1 - x)^{-1/2}$ on $[0, 1]$ evaluated at $x$ itself, nodes within $10^{-16}$ of 1 round to $1$ or to a float whose distance to 1 is wrong in relative terms, and the error stalls at $1.5 \times 10^{-8}$ even with 3073 evaluations. Passing the accurate distance $b - x$ and writing the integrand in terms of it gives an error below $10^{-15}$ with under 100 evaluations.
- **Truncation too early.** For strong singularities the transformed integrand decays slowly at first: with $f = x^{-0.9}$ on $[0, 1]$ and 5 levels, the errors are $3.1$, $0.41$, $1.6 \times 10^{-3}$, $5.1 \times 10^{-10}$ and $1.8 \times 10^{-15}$ for $T = 2, 3, 4, 5, 6$.
- **Interior kinks and jumps.** $\int_0^1 |x - \tfrac13|\,dx$ with default settings gives an error of $1.0 \times 10^{-6}$ after 3073 evaluations; splitting at $\tfrac13$ gives errors below $10^{-16}$ with 194.
- **Near poles.** Poles close to $(a, b)$ in the complex plane, as for $1/(1 + 25 x^2)$, shrink the strip of analyticity in $t$ and slow convergence.
- **Overflow and underflow.** Evaluating $\cosh^2(\frac{\pi}{2}\sinh t)$ directly overflows near $t = 6.1$; the $e^{-2u}$ form of line L11 underflows gracefully to 0 instead.
- **The stopping test is heuristic.** It compares two levels; a function that is fooled by the nodes (see [quadrature error](/quadrature-error/)) fools it too.

## Implementations

## History

Hidetosi Takahasi and Masatake Mori introduced double exponential transformations in 1974, after studying the earlier single exponential map $x = \tanh t$ of Schwartz (1969) and showing that double exponential decay of the transformed integrand is in a sense optimal for the trapezoidal rule. Mori popularized the method and developed variants for infinite intervals and for oscillatory integrals with Ooura in the 1990s. Frank Stenger's sinc theory gave the single exponential analogue a rigorous foundation, and Tanaka, Sugihara, Murota and Mori (2009) identified function spaces on which the DE formula is near optimal. Bailey, Borwein and coworkers made tanh-sinh the standard tool of high-precision experimental mathematics from about 2000.

## References
