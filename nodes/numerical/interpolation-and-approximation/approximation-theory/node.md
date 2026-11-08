---
tag: DA55J0
kind: concept
slug: approximation-theory
name: Approximation theory
aliases:
- theory of approximation
- constructive approximation
area: numerical/interpolation-and-approximation
level: intro
summary: The study of how well functions can be approximated by simpler ones (polynomials, splines, rational functions) in a given norm, which approximations are best, and how fast the error falls.
prereqs: [function-approximation, interpolation-problem]
see_also: [weierstrass-approximation-theorem, chebyshev-equioscillation-theorem, jackson-theorem, least-squares-approximation, minimax-approximation, lebesgue-constant, kolmogorov-width, rational-approximation]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapters 6 to 8 (Weierstrass theorem and convergence rates), Chapter 10 (best approximation), Chapter 16 (best and near-best) and Chapter 25 (two famous problems, the approximation of |x| and of exp on the negative axis)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapters 1 and 2 (existence and uniqueness of best approximations), Chapter 7 (the theory of minimax approximation), Chapter 11 (least squares) and Chapter 16 (the order of convergence of polynomial approximations)
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea, 1998
    locator: Chapter 1 (existence and uniqueness of best approximations) and Chapter 3 (Tchebycheff approximation of continuous functions)
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter VI (the Weierstrass theorem) and Chapter VII (best approximation in normed linear spaces)
  - paper: "S. N. Bernstein, Sur l'ordre de la meilleure approximation des fonctions continues par des polynômes de degré donné, Mémoires publiés par la Classe des Sciences de l'Académie Royale de Belgique (2) 4 (1912) 1-104"
    locator: the direct and inverse theorems linking the rate of best approximation with smoothness and analyticity
---

Approximation theory studies how well a function $f$ can be replaced by a function from a simpler class, such as polynomials of degree at most $n$, splines or rational functions, with the error measured in a chosen norm. Its central questions are whether a best approximation exists and is unique, how to recognize it, how fast the best error $E_n(f)$ falls as $n$ grows and how this rate depends on the smoothness of $f$, and how near to best a cheap method such as [interpolation](/interpolation-problem/) can come. It is the theory behind the [function approximation problem](/function-approximation/) and behind the routines that compute $e^x$ or $\sin x$ in a math library.

## In plain words

A computer computes a function such as the sine with a formula that uses only additions and multiplications, for example a polynomial. Approximation theory asks how good such a formula can be. For a fixed amount of work, is there a best formula, and is it the only one? How can you tell that a formula is the best? If you allow more work, how quickly does the error go down?

The answers depend on how you measure the error: the worst error at any point, or an average error. They also depend on the function. A smooth function can be matched very closely with little work, while a function with a corner or a jump needs much more. The theory makes these ideas exact. It also tells you when a simple method, such as a curve through well-chosen points, is almost as good as the best one.

## The idea

**Setting.** Let $X$ be a normed space of functions on $[a, b]$, for example $C[a, b]$ with $\|g\|_\infty = \max_{x \in [a,b]} |g(x)|$, or $L^2[a, b]$ with $\|g\|_2 = (\int_a^b |g|^2 w)^{1/2}$ for a weight $w > 0$. Let $V \subset X$ be a set of approximants, usually a linear subspace such as $\mathcal{P}_n$, the polynomials of degree at most $n$. The error of best approximation is
$$E_V(f) = \inf_{v \in V} \|f - v\|, \qquad E_n(f) = \min_{p \in \mathcal{P}_n} \|f - p\|_\infty,$$
and $v^* \in V$ is a best approximation when $\|f - v^*\| = E_V(f)$. Notation on these pages: $f$ is the function, usually on $[-1, 1]$; $p_n$ is the interpolating polynomial at nodes $x_0, \ldots, x_n$; $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/); $T_k$ is the [Chebyshev polynomial](/chebyshev-polynomials/) of degree $k$.

**1. Density.** Can the error go to zero at all? The [Weierstrass approximation theorem](/weierstrass-approximation-theorem/) says $E_n(f) \to 0$ for every $f \in C[a, b]$. The [Stone-Weierstrass theorem](/stone-weierstrass-theorem/) extends this to other algebras of functions on compact sets. Bernstein's proof uses the [Bernstein polynomials](/bernstein-polynomials/).

**2. Existence.** If $V$ is a finite-dimensional subspace of a normed space, every $f$ has at least one best approximation in $V$. *Proof.* Take any $v_0 \in V$. A best approximation, if one exists, lies in $K = \{v \in V : \|f - v\| \le \|f - v_0\|\}$, a closed and bounded subset of the finite-dimensional space $V$, hence compact. The map $v \mapsto \|f - v\|$ is continuous, so it attains its minimum on $K$, and that minimum is $E_V(f)$. $\square$ For nonlinear sets such as rational functions of fixed degrees, existence needs a separate argument (Powell, Chapter 10; Cheney, Chapter 5).

**3. Uniqueness.** In a strictly convex norm, such as the $L^2$ norm, the best approximation from a subspace is unique: if $v_1 \ne v_2$ were both best, then $\|f - \tfrac{1}{2}(v_1 + v_2)\| < E_V(f)$ by strict convexity, a contradiction. The maximum norm is not strictly convex, and uniqueness in $C[a, b]$ holds exactly when $V$ satisfies the Haar condition (each nonzero element of $V$ has at most $\dim V - 1$ zeros); $\mathcal{P}_n$ satisfies it (Haar's theorem; Cheney, Chapter 3).

**4. Characterization.** In $L^2$, $v^*$ is best exactly when $f - v^*$ is orthogonal to $V$, which leads to [orthogonal polynomials](/orthogonal-polynomials/) and [least-squares approximation](/least-squares-approximation/). In the maximum norm, $p^* \in \mathcal{P}_n$ is best exactly when $f - p^*$ attains its maximum absolute value with alternating signs at $n + 2$ points: the [equioscillation theorem](/chebyshev-equioscillation-theorem/). That theorem gives the [Remez algorithm](/remez-algorithm/) for [minimax approximation](/minimax-approximation/).

**5. Rates.** The decay of $E_n(f)$ measures the smoothness of $f$. [Jackson's theorem](/jackson-theorem/) gives upper bounds: if $f \in C^k[-1, 1]$, then $E_n(f) \le C_k\, \omega(f^{(k)}, 1/n)/n^k$ for $n \ge k$, where $\omega$ is the modulus of continuity. Bernstein's inverse theorems show that these rates characterize smoothness classes, and $E_n(f)$ falls geometrically, like $\rho^{-n}$, exactly when $f$ is analytic on $[-1, 1]$ (Bernstein, 1912; Trefethen, Chapter 8).

**6. Near-best linear methods.** Computing $p^*$ needs an iteration. A linear projection $L$ onto $\mathcal{P}_n$, such as interpolation at fixed nodes, is cheaper, and it is near-best:
$$\|f - Lf\| \le (1 + \|L\|)\, E_n(f).$$
*Proof.* For any $p \in \mathcal{P}_n$, $Lp = p$, so $f - Lf = (f - p) - L(f - p)$ and $\|f - Lf\| \le (1 + \|L\|)\|f - p\|$; take $p = p^*$. $\square$ For interpolation in the maximum norm, $\|L\| = \Lambda_n$, which is below $\tfrac{2}{\pi}\log(n+1) + 1$ at [Chebyshev points](/chebyshev-nodes/). So [Chebyshev interpolation](/chebyshev-interpolation/) loses at most a small factor against the best polynomial (Trefethen, Chapter 16).

**7. Beyond linear spaces.** [Rational approximation](/rational-approximation/) and splines with free knots form nonlinear families. They can approximate functions with singularities much better than polynomials of the same number of parameters. Newman (1964) showed (Trefethen, Chapter 25) that rational functions of degree $n$ approximate $|x|$ on $[-1, 1]$ with error of order $e^{-c\sqrt{n}}$, against order $1/n$ for polynomials. The [Kolmogorov width](/kolmogorov-width/) asks which $n$-dimensional subspace is best for a whole class of functions at once.

## Examples

**Four linear approximations of $e^x$ on $[-1, 1]$.** In $\mathcal{P}_1$:

| method | approximant | max error | $L^2$ error |
|---|---|---|---|
| Taylor at 0 | $1 + x$ | $0.718$ | |
| interpolation at $\pm 1/\sqrt{2}$ | $1.2606 + 1.0854\,x$ | $0.372$ | |
| least squares (Legendre) | $\sinh 1 + (3/e)\,x = 1.1752 + 1.1036\,x$ | $0.439$ | $0.229$ |
| minimax | $1.2643 + 1.1752\,x$ | $0.2788$ | $0.268$ |

The minimax line has slope $\sinh 1$ and touches its maximum error $0.2788$ with alternating signs at $-1$, $\ln(\sinh 1) \approx 0.161$ and $1$: three points, as the equioscillation theorem requires for $n = 1$. The least-squares line has the smallest $L^2$ error, the minimax line the smallest maximum error, and the interpolant at the zeros of $T_2$ is within a factor $1.34$ of the minimax error. The Taylor polynomial is accurate only near 0.

**Rates on three functions.** For $f = |x|$ on $[-1, 1]$, $n E_n(f)$ tends to Bernstein's constant $\beta \approx 0.2802$, a proved asymptotic result (Bernstein; Trefethen, Chapter 25). For $f \in C^\infty$ that is not analytic, $E_n(f)$ falls faster than any power of $n$. For $f = 1/(1 + 25 x^2)$, analytic in a neighborhood of $[-1, 1]$ with poles at $\pm i/5$, $E_n(f)$ falls like $\rho^{-n}$ with $\rho = (1 + \sqrt{26})/5 \approx 1.22$, the sum of the semiaxes of the Bernstein ellipse through the poles (Trefethen, Chapter 8). The same function is the example of the [Runge phenomenon](/runge-phenomenon/): its interpolants at equispaced nodes diverge, although its best approximations converge geometrically.

**A non-example of uniqueness.** In $C[0, 1]$ with the maximum norm, approximate $f(x) = 1$ from $V = \operatorname{span}\{x\}$. Every $v = cx$ has the error $1$ at $x = 0$, so $E_V(f) \ge 1$, and for $0 \le c \le 2$ the error $\max_{x \in [0,1]} |1 - cx|$ is exactly 1. So there are infinitely many best approximations. The space fails the Haar condition on $[0, 1]$: the element $x$ vanishes at the end point 0, and every element vanishes there, so the best approximations cannot be told apart at that point. On $[-1, 1]$ the same space gives $\|1 - cx\|_\infty = 1 + |c|$, with the unique best $c = 0$.

## Where it is used

- Math libraries: polynomial and rational [minimax approximations](/minimax-approximation/) of elementary functions on a reduced interval, after [range reduction](/cody-waite-range-reduction/).
- Numerical methods built on approximation: [interpolatory quadrature](/interpolatory-quadrature/), [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/), spectral methods, and the [Chebyshev iteration](/chebyshev-iteration/) for linear systems, which uses a minimax polynomial on the spectrum.
- Data: [curve fitting](/curve-fitting/), [least squares](/least-squares-approximation/), splines and [kriging](/kriging/).
- Complexity bounds: polynomial approximation degrees of Boolean functions, and the Chebyshev polynomial arguments in algorithms for linear algebra and optimization.

## References
