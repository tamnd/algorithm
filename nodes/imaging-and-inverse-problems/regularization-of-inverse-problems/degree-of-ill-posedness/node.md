---
tag: Z2W37A
kind: definition
slug: degree-of-ill-posedness
name: Degree of ill-posedness
aliases:
- mildly and severely ill-posed problems
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: "The decay rate of the singular values of a compact forward operator. sigma_k ~ k^(-a) is mild for a <= 1 and moderate for a > 1; exponential decay is severe."
model: real-ram
prereqs: [singular-value-expansion, well-posed-problem]
see_also: [condition-number, picard-condition, source-condition, tikhonov-convergence-rates, fredholm-integral-equation-first-kind, truncated-svd, heat-equation, radon-transform]
sources:
  - book: "Bernd Hofmann, Regularization for Applied Inverse and Ill-Posed Problems, Teubner-Texte zur Mathematik 85, Teubner, Leipzig, 1986"
    locator: the degree of ill-posedness of a compact operator from the decay of its singular values (general locator)
  - paper: doi:10.4310/maa.2010.v17.n4.a8
    title: Bernd Hofmann and Stefan Kindermann, On the degree of ill-posedness for linear problems with noncompact operators, Methods and Applications of Analysis 17(4), 2010, 445 to 462
    locator: the introduction (the usual degree for compact operators and the mild, moderate and severe classes)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 2, Ill-Posed Linear Operator Equations (the singular values of a compact operator and the unbounded generalized inverse)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 2, Meet the Fredholm Integral Equation of the First Kind (the decay of the singular values)
---

The degree of ill-posedness of a linear inverse problem with a compact forward operator is the rate at which the singular values $\sigma_k$ of the operator tend to zero. If $\sigma_k$ decays like $k^{-a}$, the degree is $a$; the problem is called mildly ill posed for $0 < a \le 1$ and moderately ill posed for $a > 1$. If $\sigma_k$ decays exponentially, the problem is severely ill posed. A [well-posed problem](/well-posed-problem/) is a yes or no notion, and the [condition number](/condition-number/) measures one matrix; the degree measures how fast the instability of a compact operator grows as finer detail is asked for, and so how much of the unknown any data of a given quality can recover.

## Definition

Let $A: X \to Y$ be a compact operator between Hilbert spaces with an infinite singular system $(\sigma_k; v_k, u_k)$, $\sigma_1 \ge \sigma_2 \ge \cdots > 0$ (see [singular value expansion](/singular-value-expansion/)).

- The equation $A x = y$ is **ill posed of degree $a$** if the singular values decay at the polynomial rate $a > 0$: there are constants $0 < c \le C$ with $c\, k^{-a} \le \sigma_k \le C\, k^{-a}$ for all $k$. More generally, the degree is $\sup\{a > 0 : \sigma_k = O(k^{-a})\}$.
- It is **mildly ill posed** if $0 < a \le 1$ and **moderately ill posed** if $1 < a < \infty$.
- It is **severely ill posed** (or exponentially ill posed) if $\sigma_k$ decays exponentially, $\sigma_k \approx \exp(-c\, k^b)$ for some $b, c > 0$. Then $\sigma_k = O(k^{-a})$ for every $a$ and the degree is infinite.

**The convention of this page.** The three classes follow Hofmann (1986). Some books call every polynomial decay mild and keep only two classes, mild (polynomial) and severe (exponential). When a source says "mildly ill posed", check which convention it uses.

**The degree depends on the spaces.** The singular values change if the norms of $X$ or $Y$ change. Integration from $L^2$ to the Sobolev space $H^1$ is bounded with a bounded inverse, so it is well posed there, while from $L^2$ to $L^2$ it has degree 1. A statement of the degree must name the spaces, as the statement of well-posedness must.

**The discrete picture.** A discretization $A_n$ of size $n$ resolves about the first $n$ singular values, so its condition number grows like $n^a$ for a problem of degree $a$, and exponentially in $n$ (or in a power of $n$) for a severe one.

## Examples and non-examples

**Integration, degree 1 (mild).** $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0,1)$ has $\sigma_k = 2/((2k-1)\pi)$, so $\sigma_k \approx 1/(\pi k)$ and the degree is 1. The rectangle-rule matrix with $h = 1/n$ has condition number $10.65$, $20.92$, $41.34$ and $82.1$ for $n = 8$, $16$, $32$ and $64$: it doubles when $n$ doubles, as degree 1 predicts.

**Two derivatives, degree 2 (moderate).** The kernel $K(s,t) = s(1-t)$ for $s \le t$ and $t(1-s)$ for $s > t$, the Green's function of $-x''$ on $(0,1)$ with zero boundary values, has $\sigma_k = 1/(k\pi)^2$: $0.1013$, $0.02533$, $0.01126$, and $0.001013$ for $k = 10$. Recovering $x$ means differentiating the data twice.

**The backward heat equation, severe.** Recovering $u(\cdot, 0)$ from $u(\cdot, T)$ for $u_t = u_{xx}$ on $(0,1)$ with zero boundary values has $\sigma_k = \exp(-k^2\pi^2 T)$, exponential decay with $b = 2$. With $T = 0.01$: $\sigma_1 = 0.906$, $\sigma_5 = 0.0848$, $\sigma_{10} = 5.17 \times 10^{-5}$ and $\sigma_{20} = 7.2 \times 10^{-18}$ (see [heat equation](/heat-equation/)). The test problems shaw and baart of Regularization Tools, with analytic kernels, are severe too.

**How many components survive.** A rough count of the components that data with noise level $\delta$ can resolve is the number of $\sigma_k \ge \delta$:

| problem | $\delta = 10^{-3}$ | $\delta = 10^{-6}$ |
|---|---|---|
| integration, $\sigma_k = 2/((2k-1)\pi)$ | 318 | 318310 |
| two derivatives, $\sigma_k = 1/(k\pi)^2$ | 10 | 318 |
| backward heat, $T = 0.01$ | 8 | 11 |

For a problem of degree $a$, a thousand times better data give $1000^{1/a}$ times more components. For the severe problem the count grows only like $\sqrt{\log(1/\delta)}$: here a thousand times better data buy three more components.

**Non-example: a finite rank operator.** If the range is finite-dimensional, there is no infinite sequence of singular values and no degree. The problem is well posed in the least squares sense.

**Non-example: a non-compact operator.** A multiplication operator $(A x)(t) = t\, x(t)$ on $L^2(0,1)$ has an unbounded inverse but no singular values at all, since it is not compact. The definition above does not apply. Hofmann and Kindermann (2010) discuss extensions of the degree to such operators.

## Related definitions

- [Singular value expansion](/singular-value-expansion/): the source of the numbers $\sigma_k$.
- [Condition number](/condition-number/): the finite-dimensional measure $\sigma_1/\sigma_n$; for a discretized problem it grows with $n$ at a rate set by the degree.
- [Source condition](/source-condition/): $x^\dagger = (A^* A)^\nu w$. Its meaning depends on the degree. For a problem of degree $a$, it asks for about $2\nu a$ derivatives of smoothness in the scale where the degree is measured. For a severe problem it asks for analytic-type smoothness, and logarithmic source conditions are used instead.
- [Tikhonov convergence rates](/tikhonov-convergence-rates/): under a Hoelder source condition the rate $\delta^{2\nu/(2\nu+1)}$ does not depend on the degree, but under logarithmic conditions for severe problems only rates in powers of $1/\log(1/\delta)$ are possible.
- [Picard condition](/picard-condition/): the data coefficients must decay faster than the singular values, so the degree also sets how smooth consistent data must be.

## References
