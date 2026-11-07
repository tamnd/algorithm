---
tag: 7AZJ7A
kind: technique
slug: creative-telescoping
name: Creative telescoping
aliases:
- Zeilberger's creative telescoping
- telescoper and certificate method
area: algebra/computer-algebra
level: advanced
summary: Find a recurrence or differential equation for a definite sum or integral by telescoping a parametrized combination.
prereqs: [telescoping-sum, hypergeometric-term, indefinite-summation]
see_also: [zeilberger-algorithm, wz-method, definite-summation, gosper-algorithm, holonomic-function, ore-algebra, petkovsek-hyper-algorithm, hermite-reduction]
sources:
  - paper: doi:10.1016/S0747-7171(08)80044-2
    title: Doron Zeilberger, The method of creative telescoping, Journal of Symbolic Computation 11(3), 195-204, 1991
    locator: the definition of telescoper and certificate and the algorithm for proper hypergeometric summands
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 6 (Zeilberger's algorithm, the telescoping recurrence and its certificate) and Chapter 7 (the WZ phenomenon)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 23 (symbolic summation, Gosper's algorithm and its use for definite sums)
  - paper: "Gert Almkvist and Doron Zeilberger, The method of differentiating under the integral sign, Journal of Symbolic Computation 10(6), 571-591, 1990"
    locator: the continuous analogue for hyperexponential integrands
  - paper: "Frédéric Chyzak, An extension of Zeilberger's fast algorithm to general holonomic functions, Discrete Mathematics 217, 115-134, 2000"
    locator: creative telescoping in Ore algebras for holonomic summands and integrands
---

Creative telescoping is the technique of proving that a definite sum $S(n) = \sum_k F(n, k)$ satisfies a linear recurrence by finding a combination $\sum_{i=0}^{J} a_i(n) F(n + i, k)$ that is a difference $G(n, k+1) - G(n, k)$ in the summation variable. Summing over $k$, the right side telescopes to boundary terms, which vanish for natural boundaries, and the left side becomes $\sum_i a_i(n) S(n + i)$. The operator $\sum_i a_i(n) S_n^i$ is the *telescoper* and $G$ is the *certificate*. The same idea works for integrals with derivatives in place of differences. Zeilberger named and systematized the method around 1990, and it is the engine of [Zeilberger's algorithm](/zeilberger-algorithm/), the [WZ method](/wz-method/) and most of modern symbolic summation and integration.

## In plain words

A sum telescopes when each term cancels part of the next, so that only the two ends survive. Most sums with a parameter do not telescope. But a clever mix of the sum for one value of the parameter and the sums for the next few values often does.

Creative telescoping searches for that mix. The weights of the mix give an equation that links the sum at one value of the parameter to the sums at the next values. A second piece of output, the certificate, lets anyone check the equation with plain algebra. The equation can then be solved for a formula, or used as it is.

## When it applies

The setting: a field $K$ of characteristic 0, typically $\mathbb{Q}$ or a field of rational functions in extra parameters; a summand $F(n, k)$ that is hypergeometric in $n$ and $k$ over $K$, or more generally holonomic; and the shift operators $S_n F(n, k) = F(n + 1, k)$ and $\Delta_k G(n, k) = G(n, k + 1) - G(n, k)$.

It applies when:

- **a telescoper exists.** For proper hypergeometric $F$ this is guaranteed by the theorem of Wilf and Zeilberger (1992); for holonomic $F$ by the elimination property of holonomic modules (Zeilberger 1990);
- **the boundary terms are controlled.** Summing $\Delta_k G$ over $k$ from $a$ to $b$ gives $G(n, b + 1) - G(n, a)$, which must be computed or shown to be zero. With natural boundaries, $G(n, k) = 0$ for all but finitely many $k$ and the sum over $\mathbb{Z}$ is 0;
- **a recurrence is a useful answer:** to evaluate $S(n)$ quickly, to find a closed form by solving the recurrence, or to prove an identity by checking initial values.

The cost is counted in operations in $K$. Each trial order $J$ requires a parametrized Gosper step, a linear system whose size is set by a degree bound.

## The template

```pseudo id=main
CREATIVE-TELESCOPE(F)               ▷ F(n, k) hypergeometric in n and k
L1  for J = 0, 1, 2, ... do
L2      T(k) ← a_0 F(n, k) + a_1 F(n+1, k) + ... + a_J F(n+J, k), with unknowns a_0, ..., a_J in K(n)
L3      write T(k+1)/T(k) through the rational function F(n, k+1)/F(n, k)
L4      run parametrized Gosper on T in k: find a_i, not all 0, and rational R with T = Δ_k (R · F)
L5      if L4 succeeds then
L6          G ← R · F                                ▷ the certificate times the summand
L7          return telescoper Σ a_i S_n^i and certificate R
L8      ▷ otherwise no telescoper of order J exists: increase J
```

To use the output, sum $T(k) = G(n, k+1) - G(n, k)$ over all $k$. If $F$ and $G$ have natural boundaries, the result is

$$\sum_{i=0}^{J} a_i(n) \, S(n + i) = 0 .$$

To verify it, divide $\sum_i a_i F(n + i, k) = G(n, k + 1) - G(n, k)$ by $F(n, k)$: both sides become rational functions in $n$ and $k$, and the identity is a check of rational functions.

## Classic examples

Each identity below was checked by a script in exact integer arithmetic for $n < 40$ and all $k$ in a range that includes the boundaries.

- **Row sums of binomial coefficients.** For $F(n, k) = \binom{n}{k}$, the telescoper of order 1 is $S_n - 2$ with certificate $G(n, k) = -\binom{n}{k-1}$, that is $R(n, k) = -k/(n - k + 1)$:
$$\binom{n+1}{k} - 2\binom{n}{k} = \left(-\binom{n}{k}\right) - \left(-\binom{n}{k-1}\right),$$
which is Pascal's rule. Summing gives $S(n+1) = 2 S(n)$, so $S(n) = 2^n$.
- **Sum of squares.** For $F(n, k) = \binom{n}{k}^2$ the telescoper is $(n + 1) S_n - 2(2n + 1)$ and the certificate is
$$G(n, k) = -(3n + 3 - 2k) \binom{n}{k-1}^2, \qquad R(n, k) = -\frac{k^2 (3n + 3 - 2k)}{(n + 1 - k)^2}.$$
Summing gives $(n + 1) S(n + 1) = 2(2n + 1) S(n)$, so $S(n) = \binom{2n}{n}$. This is the computation of [Zeilberger's algorithm](/zeilberger-algorithm/) on this input; [definite summation](/definite-summation/) lists the WZ form of the same identity.
- **Apéry numbers.** For $F(n, k) = \binom{n}{k}^2 \binom{n+k}{k}^2$ the minimal telescoper has order 2, the recurrence $(n+1)^3 A(n+1) - (34n^3 + 51n^2 + 27n + 5) A(n) + n^3 A(n-1) = 0$ shifted by one.
- **Indefinite case.** With $J = 0$ the template is [Gosper's algorithm](/gosper-algorithm/): $F(k) = \Delta_k G$ means $\sum_{k=0}^{m-1} F(k) = G(m) - G(0)$.
- **Integrals.** For $F(n, x)$ hyperexponential in $x$, find $a_i(n)$ and $G$ with $\sum_i a_i(n) F(n + i, x) = \partial_x G(n, x)$; integrating over a path where $G$ vanishes at the ends gives a recurrence for $\int F\,dx$. For example, $I(n) = \int_0^\infty x^n e^{-x}\,dx$ has $F(n+1, x) - (n+1) F(n, x) = \partial_x(-x^{n+1} e^{-x})$, so $I(n+1) = (n+1) I(n)$ and $I(n) = n!$.

## Variations

- **Zeilberger's algorithm** for hypergeometric sums: the template with parametrized Gosper; see [Zeilberger's algorithm](/zeilberger-algorithm/).
- **WZ pairs.** When the identity $\sum_k F(n, k) = 1$ is known, the telescoper is $S_n - 1$ and only the certificate is needed; see the [WZ method](/wz-method/).
- **Almkvist-Zeilberger** for integrals of hyperexponential functions, with derivatives in place of shifts.
- **q-analogues** for $q$-hypergeometric terms, with $q$-shifts.
- **Holonomic functions and Ore algebras.** Chyzak's algorithm (2000) works in an [Ore algebra](/ore-algebra/) with a holonomic description of $F$ and finds telescopers by an ansatz on the certificate as an element of the module; Koutschan's heuristic ansatz speeds this up. See [holonomic function](/holonomic-function/).
- **Reduction-based telescoping.** Reduce $F(n + i, k)$ modulo differences with a Hermite-type reduction, then find a linear dependency among the remainders, without computing the certificate unless asked (Bostan, Chen, Chyzak and Li 2010 for rational integrands; later work for hyperexponential and hypergeometric terms). The [Hermite reduction](/hermite-reduction/) is the integration step this builds on.
- **Multiple sums** $\sum_{k_1, \ldots, k_m}$, with one certificate per summation variable.

## Pitfalls

- **Boundary terms.** If the summation range is not natural, or $G$ is not zero outside it, the recurrence gets an inhomogeneous part $G(n, b + 1) - G(n, a)$. It must be computed, not assumed to vanish.
- **Poles of the certificate.** The certificate $R(n, k)$ is a rational function and can have poles where $F(n, k)$ is zero. In the sum-of-squares example, $R$ has a pole at $k = n + 1$ where $F$ vanishes, and $G(n, n + 1) = -(n + 1) \ne 0$. Reading $G = R F$ as $0$ there breaks the telescoping identity. Write $G$ in a form without the cancellation, or check the identity at the special values separately.
- **Non-minimal telescopers.** The telescoper found is minimal for $F$, but $S(n)$ can satisfy a recurrence of lower order; the extra solutions must be ruled out with initial values.
- **The leading coefficient.** The recurrence $\sum a_i(n) S(n + i) = 0$ determines $S(n + J)$ from earlier values only when $a_J(n) \ne 0$. Integer roots of $a_J$ need extra initial values.
- **Cost of the certificate.** Certificates are often much larger than telescopers. When only the recurrence is needed, a reduction-based method or a modular method avoids computing it.

## Exercises

1. Find the telescoper and certificate for $F(n, k) = (-1)^k \binom{n}{k}$ and deduce $\sum_k (-1)^k \binom{n}{k} = [n = 0]$. Where do the boundary terms matter?
2. Check by rational function arithmetic that the certificate of the sum-of-squares example is correct, and locate the values of $k$ where $R$ has a pole.
3. Use the template on $F(n, k) = \binom{n}{k} \binom{m}{k}$ with $m$ as a parameter to find a first-order recurrence in $n$, and derive the Chu-Vandermonde identity $\sum_k \binom{n}{k} \binom{m}{k} = \binom{n + m}{n}$.
4. Show that the integral $\int_0^\infty x^n e^{-x^2}\,dx$ satisfies a recurrence of order 2 in $n$, using the continuous version.
5. Explain why the template, run on a summand that is not proper hypergeometric, such as $1/(n^2 + k^2)$, may never stop.

## References
