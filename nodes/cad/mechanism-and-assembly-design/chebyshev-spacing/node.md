---
tag: PFRWQN
kind: technique
slug: chebyshev-spacing
name: Chebyshev spacing of precision points
aliases:
- Chebyshev precision points
area: cad/mechanism-and-assembly-design
level: core
summary: Places the precision points of function generation at the mapped zeros of a Chebyshev polynomial, which minimizes the node factor of the structural error bound but not the error itself.
prereqs: [function-generation, chebyshev-nodes, freudenstein-equation]
see_also: [chebyshev-polynomials, polynomial-interpolation-error-theorem, minimax-approximation, chebyshev-equioscillation-theorem, remez-algorithm, optimization-based-linkage-synthesis, kinematic-synthesis, slider-crank-mechanism]
sources:
  - paper: "Ferdinand Freudenstein, Approximate synthesis of four-bar linkages, Transactions of the ASME 77(8), 1955, 853 to 861"
    locator: precision point function generation, the structural error, and the spacing of the precision points
  - book: "Richard S. Hartenberg and Jacques Denavit, Kinematic Synthesis of Linkages, McGraw-Hill, New York, 1964"
    locator: the chapter on precision point spacing and the structural error of function generators (general locator)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on the synthesis of linkages (precision positions, structural error and Chebychev spacing; chapter level only)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: Chapter 8, Introduction to Kinematic Synthesis (function generation and the choice of precision points)
  - book: isbn:9780471628965
    title: Theodore J. Rivlin, Chebyshev Polynomials, second edition, Wiley, 1990
    locator: Chapter 1 (zeros and extrema of T_n) and Chapter 2 (extremal properties, the monic polynomial of least deviation)
---

Chebyshev spacing is the rule that places the $n$ precision points of a [function generation](/function-generation/) design at the zeros of the Chebyshev polynomial $T_n$, mapped from $[-1, 1]$ to the interval of the input variable. For $[a, b]$ these points are $x_j = \frac{a + b}{2} - \frac{b - a}{2}\cos\frac{(2j - 1)\pi}{2n}$, $j = 1, \ldots, n$, the [Chebyshev nodes](/chebyshev-nodes/) of the interval. The rule comes from the error of polynomial interpolation: the structural error of a linkage that is exact at the points is a product of a derivative term and the node polynomial $\prod_j (x - x_j)$, and these points make the largest value of the node polynomial as small as possible. They do not minimize the structural error of the linkage itself, because the derivative term depends on the linkage, which depends on the points.

## In plain words

A linkage that generates a function is exact only at a few chosen values, the precision points. Between them it is a little wrong. Where you put the precision points changes how wrong it is.

If you space them evenly, the error is usually largest near the two ends of the range. Chebyshev spacing pushes the points toward the ends, so the ends get more help. The points are the shadows on a diameter of points spread evenly around a half circle.

This rule comes from a fact about polynomials, and it is a good first choice. It does not give the best linkage. The best linkage for the largest error usually has its points somewhere else, and an optimizer can find it.

## When it applies

- A function generator, path generator or other single-input design is exact at $n$ precision points of one variable $x$ on an interval $[a, b]$, and the goal is a small largest error over the interval.
- The structural error $e(x)$ is smooth (at least $n$ times differentiable) on $[a, b]$, which holds when the linkage stays on one branch away from its toggle positions.
- The number of precision points is fixed by the design method: three for [Freudenstein's equation](/freudenstein-equation/) with fixed ranges, up to five with free start angles.

It is a rule for choosing data, not a solver. It does not apply to motion generation, where positions are given by the task and not chosen.

## The template

The input is the function $f$ on $[x_0, x_1]$, the angle ranges, and the number $n$ of precision points.

```pseudo id=main
CHEBYSHEV-DESIGN(f, [x0, x1], φ0, Δφ, ψ0, Δψ, n)
L1  for j ← 1 to n
L2      tj ← cos((2j − 1)π/(2n))
L3      xj ← (x0 + x1)/2 − ((x1 − x0)/2)·tj
L4      φj ← φ0 + Δφ·(xj − x0)/(x1 − x0);  ψj ← ψ0 + Δψ·(f(xj) − f(x0))/(f(x1) − f(x0))
L5  solve the n precision point equations for the dimensions (Freudenstein's equation when n = 3)
L6  if there is no solution, or the precision points are not on one branch, then change the ranges and repeat
L7  e ← max |ψ(φ(x)) − ψd(x)| on a fine grid of x along that branch
L8  return the dimensions and e
```

Lines L1 to L3 are the spacing itself: L2 is the $j$-th zero of $T_n$ on $[-1, 1]$ and L3 maps it to $[x_0, x_1]$. The minus sign in L3 makes the points increase with $j$; the set is the same with a plus sign because the zeros are symmetric about 0. Line L4 scales the points to angles, as defined on the [function generation](/function-generation/) page. Line L5 is the synthesis method, for example the $3 \times 3$ linear system of [Freudenstein's equation](/freudenstein-equation/). Lines L6 and L7 are the checks that every precision point design needs: the linkage must pass the points on one branch, and the error between the points must be measured, not assumed.

### Derivation of the points

The Chebyshev polynomial is $T_n(t) = \cos(n \arccos t)$ on $[-1, 1]$, a polynomial of degree $n$ with leading coefficient $2^{n-1}$ for $n \ge 1$ (see [Chebyshev polynomials](/chebyshev-polynomials/)). Put $t = \cos\theta$ with $0 \le \theta \le \pi$. Then $T_n(t) = 0$ when $\cos(n\theta) = 0$, that is $n\theta = (2j - 1)\pi/2$, so

$$\theta_j = \frac{(2j - 1)\pi}{2n}, \qquad t_j = \cos\theta_j, \qquad j = 1, \ldots, n.$$

These are $n$ distinct values in $(-1, 1)$ because the $\theta_j$ are distinct in $(0, \pi)$ and cosine is one to one there, so they are all the zeros of $T_n$. The affine map $x = \frac{a + b}{2} + \frac{b - a}{2}t$ takes $[-1, 1]$ to $[a, b]$. Since $t_{n+1-j} = -t_j$, the images of the $t_j$ are the points $x_j = \frac{a + b}{2} - \frac{b - a}{2}t_j$ of line L3. The $\theta_j$ are equally spaced on the half circle, and the $x_j$ are their projections on the diameter, which is the picture in plain words.

### The node polynomial is smallest

Let $w(x) = \prod_{j=1}^{n}(x - x_j)$ for any $n$ points $x_j$ in $[a, b]$.

**Claim.** For the Chebyshev points, $\max_{[a, b]} |w| = (b - a)^n / 2^{2n - 1}$, and every other choice of $n$ points gives a larger maximum.

*Proof.* Write $x = \frac{a + b}{2} + h t$ with $h = \frac{b - a}{2}$, and $x_j = \frac{a + b}{2} + h s_j$. Then $x - x_j = h(t - s_j)$, so $w(x) = h^n q(t)$ with $q(t) = \prod_j (t - s_j)$, a monic polynomial of degree $n$ in $t$. The minimax property of the monic Chebyshev polynomial, proved on the [Chebyshev polynomials](/chebyshev-polynomials/) page, says that $\max_{[-1, 1]} |q| \ge 2^{1-n}$, with equality only for $q = 2^{1-n}T_n$. The proof there is short: if $\max|q| \le 2^{1-n}$, then $r = 2^{1-n}T_n - q$ has degree at most $n - 1$ and $(-1)^k r(\cos(k\pi/n)) \ge 0$ at the $n + 1$ extrema of $T_n$, which forces $n$ zeros counted with multiplicity, so $r = 0$. The polynomial $2^{1-n}T_n$ is monic with roots $t_j$, so it is $q$ exactly for the Chebyshev points. Then

$$\max_{[a, b]}|w| = h^n \cdot 2^{1-n} = \frac{(b - a)^n}{2^n} \cdot \frac{1}{2^{n-1}} = \frac{(b - a)^n}{2^{2n - 1}},$$

and any other points give $h^n \max|q| > h^n 2^{1-n}$. $\blacksquare$

### What this says about the linkage

Let $e(x)$ be the structural error of a design that is exact at $x_1, \ldots, x_n$, and suppose $e$ has $n$ continuous derivatives on $[a, b]$. Fix $x$ that is not a precision point, and let $F(s) = e(s) - e(x)\,w(s)/w(x)$. Then $F$ vanishes at $x_1, \ldots, x_n$ and at $x$, which is $n + 1$ points, so by Rolle's theorem applied $n$ times $F^{(n)}(\xi) = 0$ for some $\xi$ in $[a, b]$. Since $w^{(n)} = n!$, this gives

$$e(x) = \frac{e^{(n)}(\xi)}{n!}\,w(x), \qquad\text{so}\qquad \max_{[a, b]}|e| \le \frac{\max_{[a, b]}|e^{(n)}|}{n!}\,\max_{[a, b]}|w|.$$

This is the argument of the [polynomial interpolation error theorem](/polynomial-interpolation-error-theorem/), and it holds for any smooth $e$ with these zeros. For a polynomial interpolant, $e^{(n)} = f^{(n)}$ does not depend on the nodes, so Chebyshev points minimize the bound outright. For a linkage, $e = \psi(\varphi(x)) - \psi_d(x)$ and $\psi$ is the output of a linkage whose dimensions were computed from the points. Moving the points changes the linkage and so changes $e^{(n)}$. Chebyshev spacing minimizes only the second factor of the bound.

So the honest statement is: Chebyshev spacing reduces the node factor of the structural error bound to its least value $(b - a)^n/2^{2n-1}$. It does not minimize the largest structural error, and the linkage it gives is not the minimax linkage. The minimax design is characterized by an equioscillation of the error, and it is found by an exchange or by [optimization](/optimization-based-linkage-synthesis/), not by a formula.

### Cost

The points cost $O(n)$ cosines. The design cost is that of the synthesis method in line L5, and the check in line L7 costs one position analysis per grid point.

## Classic examples

**The three-point formula.** For $n = 3$, $\cos(\pi/6) = \sqrt 3/2$, so on $[a, b]$ the points are

$$x_{1,3} = \frac{a + b}{2} \mp \frac{\sqrt 3}{4}(b - a), \qquad x_2 = \frac{a + b}{2}.$$

On $[0, 1]$ they are $0.06699$, $0.5$, $0.93301$. The node polynomial has maximum $1/32 = 0.03125$ there, against $0.09375$ for the equally spaced interior points $0.25, 0.5, 0.75$ (reached at the ends) and $\sqrt 3/36 \approx 0.04811$ for the points $0, 0.5, 1$.

**An exponential generator with Freudenstein's equation.** Let $f(x) = e^x$ on $[0, 1]$, with $\varphi$ from $90°$ to $210°$ and $\psi$ from $195°$ to $255°$, and $d = 1$. The Chebyshev points give the angle pairs $(98.04°, 197.42°)$, $(150°, 217.65°)$, $(201.96°, 248.85°)$. [Freudenstein's equation](/freudenstein-equation/) gives $K = (0.61666, 0.61013, 0.34006)$, so $a = 1.6216$, $b = 2.1233$, $c = 1.6390$. The tests of this page measure the structural error at 1000 equally spaced values of $x$ along the branch through the three points:

| precision points | max $\lvert e\rvert$ | where | $\max \lvert w\rvert$ |
| --- | --- | --- | --- |
| Chebyshev $0.0670$, $0.5$, $0.9330$ | $0.165°$ | $x = 0$ | $0.03125$ |
| equal $0.25$, $0.5$, $0.75$ | $0.521°$ | $x = 0$ | $0.09375$ |
| ends and middle $0$, $0.5$, $1$ | $0.200°$ | $x = 0.179$ | $0.04811$ |
| found by a pattern search: $0.048$, $0.3773$, $1$ | $0.104°$ | three peaks | $0.06542$ |

Chebyshev spacing cuts the error of equal spacing by a factor of about 3.2 here. The last row shows that it is not the best choice of three points: a simple search over the points, with the same ranges, finds a design whose error peaks $-0.104°$, $+0.104°$, $-0.104°$ at $x = 0$, $0.183$ and $0.597$ are equal in size. That design has twice the node factor of the Chebyshev design and a smaller error, because its derivative factor is smaller. The Chebyshev design has end errors $-0.165°$ and $-0.077°$ and inner peaks $+0.126°$, $-0.026°$ and $+0.022°$, far from equal. Its error also crosses zero at $x = 0.755$, a fourth zero that was not prescribed.

**Polynomial interpolation.** For interpolation of a fixed $f$ by a polynomial of degree $n - 1$, the same points do minimize the bound, because there $e^{(n)} = f^{(n)}$. This is the setting of the [Chebyshev nodes](/chebyshev-nodes/) page, and it is where the rule comes from.

**A start for a minimax exchange.** The [Remez algorithm](/remez-algorithm/) for polynomial [minimax approximation](/minimax-approximation/) often starts from the Chebyshev extrema. In linkage design the Chebyshev design is likewise a start for a local search on the maximum error, as in the last row of the table.

## Variations

- **Other point counts.** Five points with free start angles, or more points for six-bars, use the same formula with $n = 5$ or more.
- **Chebyshev extrema.** Some texts use the $n$ points $\cos(k\pi/(n - 1))$, which include the ends of the interval. With precision points at the ends, the end errors are zero, but the maximum of the node polynomial is larger.
- **Weighted or derivative conditions.** If some precision points are double (a value and a slope), the node polynomial has squared factors and the Chebyshev argument no longer gives the least maximum.
- **Respacing.** After a first design, move the points so that the error peaks between them become equal. This is an exchange in the spirit of the Remez algorithm. In the example above it lowers the maximum error, but no convergence proof for linkages is given in the sources cited here.
- **Slider-crank generators.** The same spacing is used for a [slider-crank](/slider-crank-mechanism/) whose output is a slide.

## Pitfalls

- **Calling it optimal.** Chebyshev spacing minimizes a factor of a bound. The table above has a design with a 37 percent smaller error. State the measured error, and do not call the Chebyshev design minimax.
- **No measurement between the points.** The rule says nothing about the size of $e^{(n)}$. Always evaluate the error on a fine grid along the branch.
- **Branch and assembly.** Moving the points can move the linkage across a toggle position or onto another branch. Check that all precision points are on one branch, as in line L6.
- **Bad ranges.** The angle ranges change the linkage more than the spacing does. On the [function generation](/function-generation/) page, changing only the output start angle changes the error by a factor of three. Search the ranges as well.
- **Interpolation intuition at the ends.** With equal interior spacing the error is often largest at the ends, but with Chebyshev spacing the largest error can still be at an end, as here at $x = 0$.

## Exercises

1. Derive the five-point formula on $[0, 1]$ and compute $\max|w|$ for it and for the points $1/6, 2/6, \ldots, 5/6$.
2. Prove that the extrema of $w$ for the Chebyshev points are at $x = \frac{a + b}{2} + \frac{b - a}{2}\cos(k\pi/n)$, $k = 0, \ldots, n$, and that the signs alternate.
3. For the exponential example, change $\Delta\psi$ to $90°$, repeat the design with Chebyshev and equal spacing, and compare the measured errors.
4. The pattern search design in the table has a larger node factor than the Chebyshev design and a smaller error. Use the error formula $e(x) = e^{(3)}(\xi)w(x)/3!$ to explain how both can hold.
5. Implement the respacing exchange: move the points until the error peaks between and outside them are equal in size, and compare with the pattern search above.

## References
