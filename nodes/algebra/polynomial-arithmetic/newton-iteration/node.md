---
tag: YS15W6
kind: technique
slug: newton-iteration
name: Newton iteration for power series
aliases:
- Newton-Raphson for power series
- Newton lifting
- precision doubling
area: algebra/polynomial-arithmetic
level: advanced
summary: Doubles the precision of a power series approximation each step, giving inversion and division in multiplication time.
prereqs: [polynomial, dense-polynomial-representation, factor-theorem, fft-polynomial-multiplication]
see_also: [newton-power-series-inversion, fast-polynomial-division, power-series-inversion, hensel-lifting, hensel-lemma, newton-raphson-method, newton-raphson-division, brent-kung-composition]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 9, Newton iteration (Section 9.1, Division with remainder using Newton iteration; Section 9.4, Solving polynomial equations via Newton iteration; Section 9.5, Computing integer roots); Section 15.4, Hensel lifting
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 4.2, Newton's method (4.2.4, Newton's method for formal power series; 4.2.5, Newton's method for functional inverses)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.7, Manipulation of power series
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 17.6, Faster polynomial arithmetic (Newton iteration for inversion of power series and fast division with remainder)
---

Newton iteration for power series solves an equation $\varphi(y) = 0$ for a power series $y$ by doubling the number of correct terms at each step. Each step costs a few multiplications at the current precision, and the precisions $1, 2, 4, \ldots, N$ form a geometric series, so the whole computation costs a constant times one multiplication at precision $N$. This gives the reciprocal of a power series, fast division with remainder, square roots, logarithms and exponentials of power series, and, with $p$ in place of $x$, Hensel lifting over the $p$-adic integers.

Throughout, $R$ is a commutative ring with $1$, "precision $m$" means "modulo $x^m$", and $M(n)$ is the cost of multiplying two polynomials of degree less than $n$ over $R$. Costs count ring operations of $R$ in the algebraic complexity model, and we assume, as von zur Gathen and Gerhard do, that $M(n)/n$ is nondecreasing.

## In plain words

Newton's method from calculus finds a root of an equation by starting with a guess and replacing it by a better guess, using the slope at the current point. Each step roughly doubles the number of correct digits. The same step works for power series, where "correct digits" means "correct coefficients". If the first few coefficients of the answer are right, one step makes twice as many coefficients right, and nothing goes wrong with rounding because the arithmetic is exact. So the method starts with one coefficient, then gets two, four, eight, and so on. The last step does most of the work, and the earlier steps together cost no more than the last one.

## When it applies

The technique fits a problem when these conditions hold.

1. **The answer is a root of an equation over power series.** We want $y \in R[[x]]$ modulo $x^N$ with $\varphi(y) \equiv 0 \pmod{x^N}$, where $\varphi$ is a polynomial in $y$ with coefficients in $R[[x]]$, or a function such as $1/y$ or $\log y$ that has a Taylor expansion with the same form.
2. **There is a simple starting root.** Some $y_0 \in R$ satisfies $\varphi(y_0) \equiv 0 \pmod x$, and $\varphi'(y_0)$ is a unit modulo $x$, that is, its constant term is a unit of $R$. This is a condition on constant terms only.
3. **The step is cheap.** One can compute $\varphi(y)$ and an approximation to $\varphi'(y)^{-1}$ at precision $2m$ in $O(M(m))$ operations, or at least in time $C(m)$ with $C(m)/m$ nondecreasing.

The same applies with $x$ replaced by any ideal of a commutative ring, for example $p \mathbb{Z}$, which gives $p$-adic Newton iteration, or $(x - a)$, which gives Taylor expansion at $a$.

## The template

```pseudo id=template
NEWTON(φ, y_0, N)
N1  y ← y_0; m ← 1                       ▷ φ(y) ≡ 0 mod x, φ'(y) a unit mod x
N2  u ← (constant term of φ'(y))^{−1}      ▷ u ≡ φ'(y)^{−1} mod x
N3  while m < N do
N4      m ← min(2m, N)
N5      y ← y − φ(y) · u   mod x^m           ▷ the Newton step
N6      u ← u · (2 − φ'(y) · u)   mod x^m     ▷ refresh the inverse, also by Newton
N7  return y
```

Many concrete instances do not keep $u$ separately: for the reciprocal, $\varphi'(y)^{-1}$ is $-y^2$ and the step simplifies, and for Hensel lifting the inverse is lifted together with the factors.

**Why it is correct.** For a polynomial $\varphi$ in $y$ over the commutative ring $A = R[[x]]$, expand $(y + h)^k$ by the binomial theorem. Collecting terms gives

$$\varphi(y + h) = \varphi(y) + \varphi'(y)\, h + h^2\, \psi(y, h)$$

for a polynomial $\psi$ with coefficients in $A$. We show by induction that at the start of each round, with current precision $m$, $\varphi(y) \equiv 0 \pmod{x^m}$ and $u\, \varphi'(y) \equiv 1 \pmod{x^m}$. Lines N1 and N2 give this for $m = 1$. In a round, let $m' = \min(2m, N)$ and put $h = -\varphi(y) u$. Then $h \equiv 0 \pmod{x^m}$, so $h^2 \equiv 0 \pmod{x^{2m}}$, and

$$\varphi(y + h) \equiv \varphi(y)\,(1 - \varphi'(y)\, u) \pmod{x^{2m}}.$$

Both factors are divisible by $x^m$, so the product is divisible by $x^{2m}$, and line N5 gives $\varphi(y) \equiv 0 \pmod{x^{m'}}$. The new $y$ agrees with the old one modulo $x^m$, so $\varphi'(y)$ is unchanged modulo $x^m$ and the old $u$ is still its inverse modulo $x^m$. Line N6 is the same Newton step for the equation $1/u - \varphi'(y) = 0$, and by the reciprocal identity $1 - \varphi'(y)\, u_{\text{new}} = (1 - \varphi'(y)\, u)^2$ it makes $u$ an inverse modulo $x^{2m}$, hence modulo $x^{m'}$. So the claim holds for $m'$, and the precision doubles at each step until it reaches $N$.

**Uniqueness.** If $z \equiv y \pmod{x^m}$ and both are roots modulo $x^{2m}$, write $z = y + h$. Then $0 \equiv \varphi'(y) h + h^2 \psi \equiv \varphi'(y) h \pmod{x^{2m}}$, and $\varphi'(y)$ is a unit, so $h \equiv 0 \pmod{x^{2m}}$. So the iteration finds the unique root that lifts $y_0$, and the starting value fixes the branch.

**Cost.** Let one step from precision $m$ to $2m$ cost $C(2m)$ with $C(m)/m$ nondecreasing. For $N = 2^k$ the total is

$$\sum_{i=1}^{k} C(2^i) \le \sum_{i=1}^{k} 2^{i-k} C(N) < 2\, C(N).$$

For general $N$ the same bound holds up to lower order terms if the precisions are taken as $\lceil N/2^i \rceil$, going from the top down, as von zur Gathen and Gerhard do in Chapter 9. So Newton iteration costs at most about twice its last step. This is proved. In practice, the constant depends on how many products a step needs and on whether the transforms of one product can be reused in the next, which is an implementation choice.

## Classic examples

**Reciprocal of a power series.** For $f$ with $f(0)$ a unit, take $\varphi(y) = 1/y - f$. Then $\varphi'(y) = -1/y^2$ and the step is $y \leftarrow y - (1/y - f)(-y^2) = y\,(2 - f y)$. It can be checked directly: $1 - f\, y(2 - f y) = (1 - f y)^2$, so the error is squared. One step needs two products, and the total is at most $3 M(N) + O(N)$ ring operations with care (von zur Gathen and Gerhard, Section 9.1). Example over $\mathbb{Z}$: for $f = 1 - x - x^2$, start with $y = 1$. The steps give $1 + x$ at precision 2, then $1 + x + 2x^2 + 3x^3$ at precision 4, then $1 + x + 2x^2 + 3x^3 + 5x^4 + 8x^5 + 13x^6 + 21x^7$ at precision 8, the Fibonacci numbers. See [Newton power series inversion](/newton-power-series-inversion/) and the problem [power series inversion](/power-series-inversion/).

**Division with remainder.** For $a = qb + r$ with $\deg a = n$, $\deg b = m$, reverse the coefficient lists: $\operatorname{rev}(a) = \operatorname{rev}(q) \operatorname{rev}(b) \pmod{x^{n-m+1}}$. So $\operatorname{rev}(q)$ is $\operatorname{rev}(a)$ times the reciprocal of $\operatorname{rev}(b)$ modulo $x^{n-m+1}$, which Newton iteration gives in $O(M(n))$ when $\operatorname{lc}(b)$ is a unit. Then $r = a - qb$. See [fast polynomial division](/fast-polynomial-division/).

**Square root.** Over a ring where $2$ is a unit, take $\varphi(y) = y^2 - f$ with $f(0) = c^2$ for a unit $c$. The step is $y \leftarrow (y + f/y)/2$. For $f = 1 + x$ over $\mathbb{Q}$, the steps give $1 + \tfrac12 x$, then $1 + \tfrac12 x - \tfrac18 x^2 + \tfrac1{16} x^3$, then the binomial series up to $\tfrac{33}{2048} x^7$. The cost is $O(M(N))$. A better variant iterates on $1/\sqrt f$ and avoids the division.

**Logarithm and exponential.** For $f(0) = 1$, $\log f = \int f'/f$ costs one inversion, one product and $O(N)$ for the derivative and the integral, if $1, 2, \ldots, N - 1$ are units. For $\exp g$ with $g(0) = 0$, take $\varphi(y) = \log y - g$, so the step is $y \leftarrow y\,(1 + g - \log y)$. For $g = x$ the steps give $1 + x$, then $1 + x + \tfrac12 x^2 + \tfrac16 x^3$, then $\sum_{k<8} x^k/k!$. Powers $f^e = \exp(e \log f)$ follow, and so does the square root as $\exp(\tfrac12 \log f)$.

**Composition inverse.** For $g$ with $g(0) = 0$ and $g'(0)$ a unit, the series $y$ with $g(y) = x$ is a root of $\varphi(y) = g(y) - x$. Each step needs a composition $g(y)$ modulo $x^{2m}$, so the total cost is that of a constant number of compositions, which the [Brent-Kung algorithm](/brent-kung-composition/) does in $O(\sqrt{N \log N}\, M(N))$ (Brent and Zimmermann, Section 4.2.5).

**$p$-adic Newton iteration and Hensel lifting.** Replace $x$ by a prime $p$. If $\varphi \in \mathbb{Z}[y]$, $\varphi(y_0) \equiv 0 \pmod p$ and $p \nmid \varphi'(y_0)$, the step $y \leftarrow y - \varphi(y)\varphi'(y)^{-1} \bmod p^{2m}$ doubles the $p$-adic precision. For $\sqrt 2$ in the $7$-adic integers: $3^2 \equiv 2 \pmod 7$, and the steps give $10 \bmod 49$, $2166 \bmod 2401$ and $1802916 \bmod 7^8$. This is [Hensel's lemma](/hensel-lemma/), and [Hensel lifting](/hensel-lifting/) of a factorization is the same iteration for the system of equations $f = gh$.

**Integer reciprocals and roots.** For integers, the "precision" is the number of correct leading digits, and the step $y \leftarrow y(2 - a y)$ gives [Newton-Raphson division](/newton-raphson-division/) at a constant times the cost of one $n$-digit integer multiplication; integer square roots and $k$-th roots work the same way (von zur Gathen and Gerhard, Section 9.5). Rounding errors make this harder than the exact power series case.

## Variations

- **Top-down precisions.** Computing the list $N, \lceil N/2 \rceil, \lceil N/4 \rceil, \ldots, 1$ first and then climbing it avoids overshooting $N$ by up to a factor of 2 and is what implementations use.
- **Reuse of transforms.** In the reciprocal step $y(2 - fy)$, the transform of $y$ is used twice, and half of the product $f y$ is already known to be $1$ followed by zeros. Exploiting this, with the middle product of Brent and Zimmermann, Section 3.3.2, lowers the constant from 3 to about 2 or less in FFT-based implementations. The best constants are observed or derived for specific transforms, not for general $M(n)$.
- **Higher order iteration.** A step that triples or quadruples the precision, such as $y \leftarrow y(1 + e + e^2)$ with $e = 1 - fy$ for the reciprocal, can be cheaper per correct coefficient for some multiplication algorithms. The identity $1 - f y(1 + e + e^2) = e^3$ shows that the precision triples (Brent and Zimmermann, Section 4.2).
- **Systems of equations.** For a vector $y$ and a system $\Phi(y) = 0$, the step uses the inverse of the Jacobian matrix, which is itself lifted by Newton iteration. Multifactor Hensel lifting and lifting of matrix inverses are instances.
- **Linear differential equations.** The solution of $y' = a y$ with $y(0) = 1$ is $\exp(\int a)$, and $y' = a y + b$ reduces to it with one more product and one integral. So first-order linear equations with power series coefficients cost $O(M(N))$, when $1, \ldots, N - 1$ are units.

## Pitfalls

- **A starting value that is not a simple root.** If $\varphi'(y_0)$ is not a unit modulo $x$, the step may divide by a non-unit, and quadratic convergence is lost. Over $\mathbb{F}_2$, $y^2 - (1 + x)$ has $\varphi' = 2y = 0$, and the square root does not exist as a power series at all.
- **Divisions by small integers.** Square roots need $2$ to be a unit, and $\log$ and $\exp$ need $1, \ldots, N - 1$ to be units, because of the integral. Over $\mathbb{F}_p$ with $N > p$, use other methods.
- **Working at too high a precision.** The Newton step at target precision $2m$ only needs $\varphi(y)$ modulo $x^{2m}$, and the correction is divisible by $x^m$. Computing the full product, or truncating at the end only, costs much more than the bound.
- **Off-by-one in the precision.** The step from precision $m$ gives precision $2m$, not $2m + 1$. A loop that doubles the wrong quantity either stops one step early or never stops for $N = 1$.
- **Floating point.** Over $\mathbb{R}$ or $\mathbb{C}$, with an FFT in floating point, the error in each step adds to the truncation error. The exact arguments above do not apply, and the precision of the arithmetic must grow with $N$.

## Exercises

1. Show that the reciprocal step satisfies $1 - f\, y_{\text{new}} = (1 - f y)^2$, and conclude that the precision doubles. *Answer:* $1 - f y(2 - f y) = 1 - 2 f y + (f y)^2 = (1 - f y)^2$.
2. Compute $1/(1 - x)$ modulo $x^8$ by Newton iteration from $y = 1$. *Answer:* $1 + x$, $1 + x + x^2 + x^3$, $1 + x + \cdots + x^7$.
3. Show that if a step at precision $m$ costs $c\, M(m)$, the total cost of Newton iteration to precision $N = 2^k$ is less than $2c\, M(N)$. *Answer:* sum the geometric series, using $M(2^i) \le 2^{i-k} M(2^k)$.
4. For $\varphi(y) = y^2 - f$, write the step without division, by iterating on $z \approx f^{-1/2}$. *Answer:* $z \leftarrow z + \tfrac12 z (1 - f z^2)$; then $\sqrt f = f z$.
5. Find $y \in \mathbb{Z}/5^4\mathbb{Z}$ with $y^2 \equiv -1$ and $y \equiv 2 \pmod 5$. *Answer:* $y = 182$, since the steps give $7 \bmod 25$ and $182 \bmod 625$, and $182^2 + 1 = 33125 = 53 \cdot 625$.

## References
