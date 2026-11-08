---
tag: T9V8KG
kind: algorithm
slug: sinc-quadrature
name: Sinc quadrature
aliases:
- Stenger sinc quadrature
- single exponential quadrature
- SE quadrature
- sinc rule
area: numerical/quadrature
level: research
summary: Sinc-function-based transformed trapezoid rule with exponential convergence for analytic integrands.
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {n: "the parameter of the rule, the number of nodes on the side of a", P: "the number of points, n + ceil(alpha n / beta) + 1 for decay rates alpha at a and beta at b"}
  time: {worst: Θ(P), average: Θ(P), best: Θ(P)}
  space: {extra: Θ(P)}
properties: {deterministic: true, recursive: false}
prereqs: [trapezoidal-rule]
see_also: [tanh-sinh-quadrature, improper-integration, gauss-jacobi-quadrature, euler-maclaurin-formula, quadrature-error, adaptive-quadrature, oscillatory-integration]
sources:
  - book: "Frank Stenger, Numerical Methods Based on Sinc and Analytic Functions, Springer Series in Computational Mathematics 20, Springer, 1993"
    locator: Chapter 3 (sinc approximation and the trapezoidal rule in a strip) and Chapter 4 (sinc quadrature on an interval via conformal maps, with the error bound exp(-sqrt(2 pi d alpha n)))
  - paper: doi:10.1137/1023037
    title: Frank Stenger, Numerical methods based on Whittaker cardinal, or sinc functions, SIAM Review 23(2), 1981, 165-224
    locator: the sections on quadrature over a finite interval, the map log((x - a)/(b - x)) and the choice of h, M, N
  - book: "John Lund and Kenneth L. Bowers, Sinc Methods for Quadrature and Differential Equations, SIAM, 1992"
    locator: the chapter on sinc quadrature, with the parameter selection M, N, h and worked examples
  - paper: doi:10.1137/130932132
    title: Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3), 2014, 385-458
    locator: Section 5, Theorem 5.1 (the trapezoidal rule on the real line for functions analytic in a strip), and the section on transformations of finite intervals
  - paper: "Hidetosi Takahasi and Masatake Mori, Double exponential formulas for numerical integration, Publications of the Research Institute for Mathematical Sciences, Kyoto University 9, 1974, 721-741"
    locator: the comparison of single exponential (tanh) and double exponential transformations
---

Sinc quadrature integrates $f$ over a finite interval $[a, b]$ by substituting

$$x = \psi(t) = \frac{a + b\,e^t}{1 + e^t}, \qquad t = \varphi(x) = \log\frac{x - a}{b - x},$$

which maps the real line onto $(a, b)$, and applying the [trapezoidal rule](/trapezoidal-rule/) with step $h$ to $g(t) = f(\psi(t))\,\psi'(t)$, truncated to $-Mh \le t \le Nh$. The weight $\psi'(t) = (x - a)(b - x)/(b - a)$ decays like $e^{-|t|}$, single exponentially, so an endpoint singularity of the form $(x - a)^{\alpha - 1}$ becomes a tail $e^{\alpha t}$. If $f$ is analytic in an eye-shaped region of angle $d$ around $(a, b)$, the rule with $2n + 1$ points (for equal decay at both ends) has error $O(e^{-\sqrt{2\pi d \alpha n}})$. Stenger developed it from the theory of the Whittaker cardinal (sinc) function in the 1970s.

## In plain words

Some integrals are hard only at their ends: the function blows up there, or rises infinitely steeply. Sinc quadrature moves the ends away. It uses a new variable that runs over the whole number line, and the interval is stretched onto it so that the two ends lie infinitely far out. What the function did near the ends turns into tails that die off at a steady exponential pace.

The simplest possible rule, equally spaced points with equal weights, is extremely accurate on smooth functions that die off like that, provided the spacing and the place where the tails are cut are chosen together. Then each extra pair of points buys a fixed fraction of a digit more, growing like a square root, until the full precision is reached.

## The problem

Given an oracle for $f$, continuous on $(a, b)$, $a < b$ finite, and absolutely integrable, possibly singular at $a$ or $b$, and a tolerance $\tau$, approximate $I(f) = \int_a^b f(x)\,dx$. The user supplies, or guesses, the decay rates $\alpha, \beta > 0$ such that $|f(x)|\,(x - a)(b - x)/(b - a)$ is $O((x - a)^\alpha)$ near $a$ and $O((b - x)^\beta)$ near $b$, and the half-angle $0 < d < \pi$ of the region of analyticity. Cost is counted in evaluations of $f$; nodes and weights cost $O(1)$ each. See [numerical integration](/numerical-integration/) and [improper integration](/improper-integration/).

## The algorithm

```pseudo id=main
SINC(f, a, b, n, α, β, d)                  ▷ finite a < b; b < a by negation, a = b gives 0
L1  M ← n;  N ← ⌈α n / β⌉;  h ← sqrt(2π d / (α n));  S ← 0
L2  for k ← −M to N do
L3      t ← k h;  x_k ← (a + b e^t)/(1 + e^t);  w_k ← h (x_k − a)(b − x_k)/(b − a)
L4      S ← S + w_k f(x_k)
L5  return S
```

Line L1 is Stenger's parameter choice. It makes the two truncation errors $e^{-\alpha M h}$ and $e^{-\beta N h}$ at most $e^{-\alpha n h}$, and it balances them against the discretization error $e^{-2\pi d/h}$ of the trapezoidal rule: $\alpha n h = 2\pi d / h$ gives $h = \sqrt{2\pi d/(\alpha n)}$ and a common exponent $\sqrt{2\pi d \alpha n}$. Line L3 is evaluated in the implementation through $e = e^{-|t|}$: for $t \le 0$, $x - a = Le/(1 + e)$ and $b - x = L/(1 + e)$, and symmetrically for $t > 0$, with $L = b - a$, so the distances to the ends are computed to full relative precision even when they are $10^{-30}$; the implementation can pass them to $f$. A node that rounds onto an end point is evaluated there if $f$ is finite, and skipped otherwise. Line L4 is accumulated with compensated summation.

## Example

For $\int_0^1 e^x\,dx$, $\int_0^1 \log x\,dx = -1$ (both with $\alpha = \beta = 1$) and $\int_0^1 x^{-1/2}\,dx = 2$ (with $\alpha = \tfrac12$, $\beta = 1$), all with $d = \pi/2$:

| $n$ | points | error, $e^x$ | error, $\log x$ | points | error, $x^{-1/2}$ | $e^{-\pi\sqrt n}$ |
|---|---|---|---|---|---|---|
| 4 | 9 | $2.9 \times 10^{-3}$ | $6.5 \times 10^{-3}$ | 7 | $1.4 \times 10^{-2}$ | $1.9 \times 10^{-3}$ |
| 8 | 17 | $2.8 \times 10^{-4}$ | $8.0 \times 10^{-4}$ | 13 | $3.2 \times 10^{-3}$ | $1.4 \times 10^{-4}$ |
| 16 | 33 | $8.5 \times 10^{-6}$ | $3.2 \times 10^{-5}$ | 25 | $2.8 \times 10^{-4}$ | $3.5 \times 10^{-6}$ |
| 32 | 65 | $5.3 \times 10^{-8}$ | $2.7 \times 10^{-7}$ | 49 | $8.0 \times 10^{-6}$ | $1.9 \times 10^{-8}$ |
| 64 | 129 | $3.7 \times 10^{-11}$ | $2.6 \times 10^{-10}$ | 97 | $4.8 \times 10^{-8}$ | $1.2 \times 10^{-11}$ |

The last column is the predicted rate $e^{-\sqrt{2\pi d \alpha n}}$ for $\alpha = 1$, $d = \pi/2$. The errors follow it up to a modest constant: quadrupling $n$ doubles the exponent. The logarithmic singularity costs almost nothing, and the inverse square root, with half the decay rate, converges like $e^{-\pi\sqrt{n/2}}$. To reach $10^{-13}$, sinc needs 233 points for $\log x$ and 295 for $x^{-1/2}$, while [tanh-sinh](/tanh-sinh-quadrature/) with $T = 4$ is accurate to the last digit after 65 points on both.

## Correctness

The full proof is in the correctness file. The map $\psi$ is a smooth increasing bijection of $\mathbb{R}$ onto $(a, b)$ with $\psi' = (x - a)(b - x)/(b - a)$, so $I(f) = \int_{\mathbb{R}} g$ (Lemma 1), and line L3 computes nodes, distances and weights without cancellation (Lemma 2), so the returned value is $h \sum_{k = -M}^{N} g(kh)$. Two results are proved there:

- **Convergence (proved).** If $g \in C^1$ with $g' \in L^1$, the error is at most $h \|g'\|_{L^1}$ plus the integrals of $|g| + h|g'|$ over $t < -Mh$ and $t > Nh$.
- **Truncation (proved).** If $|g(t)| \le C e^{\alpha t}$ for $t \le 0$ and $\le C e^{-\beta t}$ for $t \ge 0$, then the two tails are at most $C(1/\alpha + 1/\beta)\, e^{-\sqrt{2\pi d \alpha n}}$ with the parameters of line L1.

The fast discretization rate is cited: if $f$ is analytic in $D_d = \{z : |\arg((z - a)/(b - z))| < d\}$, so that $g$ is analytic in the strip $|\operatorname{Im} t| < d$, and $g$ is integrable along horizontal lines with bound $B$, the full trapezoidal sum has error at most $2B/(e^{2\pi d/h} - 1)$ (Stenger 1993; Trefethen and Weideman 2014, Theorem 5.1). Together they give Stenger's bound $|Q - I(f)| \le C' e^{-\sqrt{2\pi d \alpha n}}$.

## Complexity

The rule uses $M + N + 1 = n + \lceil \alpha n / \beta \rceil + 1$ evaluations of $f$, and $O(1)$ arithmetic with one exponential per node. For $\alpha = \beta$ that is $2n + 1$ points and error $O(e^{-\sqrt{2\pi d\alpha n}})$, so reaching tolerance $\tau$ needs about

$$n \approx \frac{(\log \tau)^2}{2\pi d \alpha}$$

(asymptotic): about 54 for $\tau = 10^{-10}$ with $\alpha = 1$, $d = \pi/2$, a total of 109 points. The rules for different $n$ are not nested, since $h$ depends on $n$. The implementation stores the terms for the compensated sum, $O(n)$ memory; a running sum needs $O(1)$.

## Properties

- **Positive weights.** All $w_k > 0$ and $\sum_k w_k \to b - a$, so the rule is stable: rounding errors in $f$ are not amplified.
- **Not polynomial.** The rule is not exact for constants; degree of exactness is the wrong measure of its quality.
- **Near optimal in its class.** For functions analytic in $D_d$ with algebraic decay of order $\alpha$ at the ends, no $n$-point rule can do better than $e^{-c\sqrt n}$ uniformly, so the square root in the exponent is not a weakness of the method but of the class (Stenger 1993; Sugihara 1997 for the comparison with double exponential rules).
- **Needs the decay rates.** Unlike [tanh-sinh](/tanh-sinh-quadrature/), the parameters depend on $\alpha$, $\beta$ and $d$; wrong values slow it down but do not make it diverge.
- **Not nested.** Halving $h$ alone does not keep the balance of line L1.

## Variants and improvements

- **Other intervals.** The same scheme with $\varphi(x) = \log x$ on $(0, \infty)$ for algebraically decaying $f$, $\varphi(x) = \log\sinh x$ for exponentially decaying $f$, and $\varphi(x) = x$ or $\operatorname{arcsinh} x$ on $\mathbb{R}$; Stenger's books give the matching $M$, $N$, $h$.
- **Double exponential.** Replacing $\varphi$ by the map of [tanh-sinh quadrature](/tanh-sinh-quadrature/) gives error $O(e^{-cN/\log N})$ instead of $O(e^{-c\sqrt N})$, at the price of a less clean function space; Takahasi and Mori (1974) introduced it after comparing the two.
- **Sinc indefinite integration and sinc collocation.** The same nodes support approximation of $f$ by sums of shifted sinc functions $\operatorname{sinc}((\varphi(x) - kh)/h)$, of $\int_a^x f$, and of solutions of differential and integral equations (Stenger 1993; Lund and Bowers 1992).
- **Chosen d.** If $f$ has a pole at distance $\delta$ from $(a, b)$, the eye-shaped region must exclude it, which forces $d$ down to roughly the angle under which the pole sees the interval; passing that smaller $d$ restores the rate.
- **Split at interior trouble.** A kink or jump at a known point $p$ is handled by integrating over $[a, p]$ and $[p, b]$, where $p$ becomes an endpoint.

## When to use it

- Integrands analytic inside $(a, b)$ with algebraic or logarithmic endpoint singularities of known strength, especially when an error bound with explicit constants is wanted.
- As a building block of sinc methods for integral and differential equations, where the same nodes and the same function class are used throughout.
- Not when the singularity is unknown and only speed matters: [tanh-sinh](/tanh-sinh-quadrature/) needs no decay rates and fewer points. Not for smooth integrands, where [Gauss-Legendre](/gauss-legendre-quadrature/) or [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) are faster, and not for known weights such as $(1 - x)^{\alpha}(1 + x)^{\beta}$, where [Gauss-Jacobi](/gauss-jacobi-quadrature/) is exact for polynomial factors.

## Pitfalls

- **An overstated decay rate.** For $\int_0^1 x^{-0.9}\,dx = 10$, the true rate is $\alpha = 0.1$. With the default $\alpha = 1$ the errors for $n = 16, 64, 256$ are $2.7$, $0.79$ and $0.065$; with $\alpha = 0.1$ they are $0.17$, $3.4 \times 10^{-3}$ and $1.3 \times 10^{-6}$, using $16 + 2 + 1$, $64 + 7 + 1$ and $256 + 26 + 1$ points.
- **An understated decay rate costs less.** For $x^{-1/2}$ with $\alpha = 1$ instead of $\tfrac12$, the errors for $n = 16, 64, 256$ are $3.1 \times 10^{-3}$, $6.3 \times 10^{-6}$ and $2.3 \times 10^{-11}$, the rate of the true $\alpha$ with the extra points wasted.
- **Nearby poles.** $\int_{-1}^1 (1 + 25x^2)^{-1}\,dx$ has poles at $\pm i/5$, so the region $D_d$ must have $d$ below about $2\arctan(1/5) \approx 0.39$. With $d = \pi/2$ the errors for $n = 16, 64, 256$ are $5.6 \times 10^{-2}$, $2.3 \times 10^{-3}$ and $4.1 \times 10^{-6}$; with $d = 0.39$ they are $2.0 \times 10^{-3}$, $3.4 \times 10^{-6}$ and $1.0 \times 10^{-11}$.
- **Interior kinks and jumps.** $\int_0^1 |x - \tfrac13|\,dx$ has errors $1.6 \times 10^{-3}$, $1.5 \times 10^{-4}$ and $1.6 \times 10^{-4}$ for $n = 16, 64, 256$, and a jump at $0.3$ gives $6.7 \times 10^{-2}$, $2.8 \times 10^{-2}$ and $7.7 \times 10^{-3}$; the transformed integrand is no longer analytic in any strip. Split the interval.
- **Lost precision at a nonzero end.** With $f(x) = (1 - x)^{-1/2}$ on $[0, 1]$ computed from $x$, nodes near 1 lose their relative distance to 1 in rounding, and the error stalls at $1.6 \times 10^{-8}$ for $n = 64$ and $256$. Computing $f$ from the accurate distance $b - x$ gives $3.2 \times 10^{-11}$ and $0$.
- **Infinite intervals need another map.** The implementation rejects them rather than silently truncating.

## Implementations

## History

The cardinal function $\sum_k f(kh)\operatorname{sinc}((x - kh)/h)$ was studied by E. T. Whittaker in 1915 and J. M. Whittaker in the 1920s and 1930s, and it underlies the sampling theorem. Frank Stenger, from the early 1970s, turned it into a numerical method: approximation, quadrature, and later the solution of differential and integral equations, with conformal maps carrying the real line to intervals and arcs. His 1981 SIAM Review survey and his 1993 book are the standard accounts, and Lund and Bowers (1992) gave a textbook treatment. The tanh map for quadrature, the single exponential precursor of [tanh-sinh](/tanh-sinh-quadrature/), was proposed by Schwartz (1969); Takahasi and Mori (1974) compared single and double exponential decay and introduced the latter. Trefethen and Weideman (2014) placed both in the general theory of the exponentially convergent trapezoidal rule.

## References
