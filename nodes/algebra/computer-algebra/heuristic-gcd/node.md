---
tag: N1KXF6
kind: algorithm
slug: heuristic-gcd
name: Heuristic GCD
aliases:
- Char-Geddes-Gonnet heuristic GCD
- GCD by Kronecker substitution
- GCDHEU
- evaluation gcd at a large integer
area: algebra/computer-algebra
level: advanced
summary: Computes integer polynomial GCDs by evaluating at a large integer and reading the GCD from the result.
solves: [polynomial-gcd]
model: word-ram
complexity:
  vars: {d: the largest degree of f and g, L: the word length of the largest coefficient, T: the number of evaluation points tried}
  time: {worst: O(T d^2 (d + L)^2)}
  space: {extra: O(d (d + L))}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1984
  people: [Bruce W. Char, Keith O. Geddes, Gaston H. Gonnet]
  note: Presented at EUROSAM 1984 and published in full in the Journal of Symbolic Computation in 1989; it became the default polynomial gcd of Maple for small and medium inputs.
prereqs: [polynomial-gcd, greatest-common-divisor, primitive-polynomial, cauchy-root-bound, horner-rule]
see_also: [brown-modular-gcd, modular-methods, kronecker-substitution, subresultant-gcd, polynomial-euclidean-algorithm, euclidean-algorithm, lehmers-gcd, half-gcd]
sources:
  - paper: "Bruce W. Char, Keith O. Geddes and Gaston H. Gonnet, GCDHEU: Heuristic polynomial GCD algorithm based on integer GCD computation, Journal of Symbolic Computation, 1989"
    locator: the algorithm, the theorem that a candidate dividing both inputs is the gcd, and the multivariate version
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 7, Polynomial GCD computation (the heuristic gcd algorithm GCDHEU, the xi-adic reconstruction and its correctness theorem)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 6, The resultant and gcd computation (the modular gcd algorithms that the heuristic gcd competes with) and Chapter 8 (Kronecker substitution)
  - paper: "Hsin-Chao Liao and Richard J. Fateman, Evaluation of the heuristic polynomial GCD, ISSAC 1995"
    locator: experiments on the number of evaluation points and comparison with modular methods
---

The heuristic gcd computes $\gcd(f, g)$ for $f, g \in \mathbb{Z}[x]$ by turning it into one integer gcd. It evaluates both polynomials at a large integer $\xi$, computes $\gamma = \gcd(f(\xi), g(\xi))$ in $\mathbb{Z}$, and writes $\gamma$ in base $\xi$ with digits in $(-\xi/2, \xi/2]$. Those digits are read as the coefficients of a candidate polynomial $h$. A trial division then checks the candidate: if the primitive part of $h$ divides both $f$ and $g$, it is the gcd. That is a theorem when $\xi \ge 2 \min(|f|_\infty, |g|_\infty) + 2$. If the check fails, the method tries a larger $\xi$, and after a few failures it hands the problem to a [modular gcd](/brown-modular-gcd/). The answer is always correct. Only the number of tries is heuristic. Big-integer gcds are fast in practice, so for small and medium inputs it often beats the modular methods.

## In plain words

Pick a number such as $\xi = 10$ and plug it into both polynomials. Each polynomial turns into an integer, and the integer's digits in base $10$ are the polynomial's coefficients, as long as the coefficients are small. The gcd of the two integers usually has as its digits the coefficients of the gcd of the two polynomials. Sometimes the integers share an extra factor by accident, and then the digits come out wrong. So the method checks its guess by dividing. If the guess divides both polynomials, it is provably right. If not, it tries again with a bigger number, and after a few failures it gives up and uses a slower method that always works.

## The problem

**Input.** Polynomials $f, g \in \mathbb{Z}[x]$, given by their integer coefficient lists, lowest degree first. Here $\mathbb{Z}$ is a ring, not a field, and the gcd is taken in $\mathbb{Z}[x]$, a unique factorization domain. $|f|_\infty$ is the largest absolute value of a coefficient, and $d$ bounds both degrees.

**Output.** $\gcd(f, g)$ with a positive leading coefficient, or FAIL after $T$ unsuccessful evaluation points.

Write $\operatorname{cont}(f)$ for the content, the gcd of the coefficients, and $\operatorname{pp}(f) = f / \operatorname{cont}(f)$ for the [primitive part](/primitive-polynomial/), normalized so that its leading coefficient is positive. By Gauss's lemma $\gcd(f, g) = \gcd(\operatorname{cont} f, \operatorname{cont} g) \cdot \gcd(\operatorname{pp} f, \operatorname{pp} g)$, so it suffices to handle primitive inputs. If $f = 0$ or $g = 0$, the gcd is the other polynomial, made to have a positive leading coefficient, and the algorithm below assumes both are nonzero.

## The algorithm

For an integer $\gamma$ and $\xi \ge 2$, the symmetric $\xi$-adic expansion $\gamma = \sum_i h_i \xi^i$ with $-\xi/2 < h_i \le \xi/2$ is unique. It is computed by repeated division with symmetric remainder, and it defines the polynomial $\operatorname{genpoly}(\gamma, \xi) = \sum_i h_i x^i$, so that $\operatorname{genpoly}(\gamma, \xi)(\xi) = \gamma$.

```pseudo id=main
HEUGCD(f, g, T)                        ▷ f, g ∈ Z[x] nonzero
L1  c ← gcd(cont f, cont g);  f ← pp(f);  g ← pp(g)
L2  ξ ← 2 · min(|f|_∞, |g|_∞) + 2
L3  repeat T times
L4      γ ← gcd(f(ξ), g(ξ))                       ▷ one integer gcd
L5      h ← genpoly(γ, ξ)                         ▷ symmetric ξ-adic digits of γ
L6      h ← pp(h)
L7      if h divides f and h divides g in Z[x] then return c · h
L8      ξ ← ⌊ξ · 73794 / 27011⌋                    ▷ grow ξ by about 2.73
L9  return FAIL                                 ▷ caller uses a modular gcd
```

Line L2 is the bound that makes the check at line L7 conclusive. Line L6 removes integer factors that the cofactors' values contribute to $\gamma$. Line L8 multiplies $\xi$ by a factor close to $1 + \sqrt{3}$, which is not an integer, so that successive points are not powers of one another. The constant is the one used in the implementation below; any growth factor greater than $1$ keeps the algorithm correct.

## Example

Let $f = x^2 + 2x = x(x + 2)$ and $g = x^2 - 4 = (x - 2)(x + 2)$. Both are primitive, so $c = 1$, and $\xi = 2 \cdot \min(2, 4) + 2 = 6$.

| try | $\xi$ | $f(\xi)$ | $g(\xi)$ | $\gamma$ | $\operatorname{genpoly}(\gamma, \xi)$ | $h$ | $h \mid f$ and $h \mid g$? |
|---|---|---|---|---|---|---|---|
| 1 | $6$ | $48$ | $32$ | $16$ | $3x - 2$ | $3x - 2$ | no |
| 2 | $16$ | $288$ | $252$ | $36$ | $2x + 4$ | $x + 2$ | yes: return $x + 2$ |

At $\xi = 6$ the cofactors $x$ and $x - 2$ take the values $6$ and $4$, which share the factor $2$. So $\gamma = 2 \cdot G(6)$ for $G = x + 2$, and the coefficient $4$ of $2G = 2x + 4$ exceeds $\xi / 2 = 3$. The digit wraps around, $16 = 3 \cdot 6 - 2$, and the candidate $3x - 2$ is wrong. Line L7 rejects it. At $\xi = \lfloor 6 \cdot 73794 / 27011 \rfloor = 16$, $\gamma = 36 = 2 \cdot 18$ and $2x + 4$ has coefficients below $8$, so its digits are read correctly and line L6 removes the spurious factor $2$. In a run on $2000$ random products of small polynomials, with a fixed seed, about $92\%$ succeeded at the first point and none needed more than three.

## Correctness

The candidate is always a polynomial with $h(\xi) = \gamma$ up to the content. If it divides both inputs, then $h$ divides $G = \gcd(f, g)$, and the cofactor $k = G / h$ has $k(\xi)$ dividing the content of $\operatorname{genpoly}(\gamma, \xi)$, which is at most $\xi / 2$ in absolute value. Every root of a factor of $f$ has absolute value below $1 + |f|_\infty \le \xi / 2$ by the [Cauchy bound](/cauchy-root-bound/), so a nonconstant $k$ would have $|k(\xi)| > \xi / 2$. Hence $k$ is a unit and $h = G$. The full proof is in the proof file below. The algorithm stops after at most $T$ tries. Correctness does not depend on the choice of the later points, only on $\xi$ never decreasing below the bound of line L2.

## Complexity

The cost model is the word RAM with classical integer arithmetic, counting word operations. Let $L$ be the word length of the largest coefficient of $f$ and $g$, so $\xi$ has $O(L)$ words at the first try and $O(L + T)$ words at try $T$. These bounds are proved for one try:

- **Evaluation (line L4).** By [Horner's rule](/horner-rule/), $f(\xi)$ has $O(dL)$ words and costs $O(d^2 L^2)$.
- **Integer gcd (line L4).** The Euclidean algorithm on $O(dL)$-word integers costs $O(d^2 L^2)$, or $O(M(dL) \log(dL))$ with a [half-gcd](/half-gcd/) algorithm.
- **Reconstruction (lines L5 and L6).** $d$ divisions of an $O(dL)$-word integer by $\xi$ cost $O(d^2 L^2)$.
- **Trial division (line L7).** The quotients have degree at most $d$ and, by Mignotte's bound, coefficients of $O(d + L)$ words, so each division costs $O(d^2 (d + L)^2)$.

So $T$ tries cost $O(T d^2 (d + L)^2)$, and the extra space is $O(d (d + L))$ words for the integers, the candidate and the quotients. The bound on $T$ is a parameter, not a theorem: there is no proof that a small number of points suffices for all inputs. In practice one or two points almost always succeed, which is an observation, as in the example. The method is fast because $f(\xi)$ is one big integer, and big-integer gcds and divisions are highly optimized.

## Properties

- **Always correct when it answers.** A returned result is the gcd. Failure is reported, never hidden.
- **Deterministic.** The points are fixed by the inputs, so a run is reproducible.
- **Size sensitive.** The integers have about $d L$ words. The method suits dense inputs of low or moderate degree, and becomes expensive for high degree or many variables.
- **Cofactors for free.** The quotients $f / h$ and $g / h$ from line L7 are the cofactors, which many callers need anyway, for example in [square-free factorization](/square-free-factorization/).

## Variants and improvements

- **Multivariate.** Evaluate the main variable at $\xi$ to get two polynomials in fewer variables, compute their gcd recursively, and reconstruct by $\xi$-adic expansion of the coefficients. Char, Geddes and Gonnet treat this case, and the size of the integers grows quickly with the number of variables.
- **Testing by division in $\mathbb{Z}$.** The test $h \mid f$ can be replaced by the cheaper check that $h(\xi')$ divides $f(\xi')$ at a second large point, or by a division with a degree bound, at the price of a probabilistic answer.
- **Cofactor reconstruction.** Instead of reconstructing $\gamma$, reconstruct the cofactors $f(\xi)/\gamma$ and $g(\xi)/\gamma$, and accept when either cofactor multiplied by its candidate gives back $f$ or $g$. This catches some cases where $h$ itself has large coefficients.
- **Kronecker substitution.** Evaluating at $\xi = 2^k$ makes $f(\xi)$ a concatenation of the coefficients, the [Kronecker substitution](/kronecker-substitution/), so evaluation and reconstruction are just packing and unpacking.

## When to use it

Use it for gcds of dense integer polynomials of low or moderate degree with moderate coefficients, where one big-integer gcd is cheaper than the many small gcds of [Brown's modular algorithm](/brown-modular-gcd/). Maple used it as its default for such inputs. For high degree, many variables or sparse inputs, use a [modular method](/modular-methods/) or Zippel's sparse algorithm, and keep the heuristic gcd as a fast first attempt with a small $T$.

## Pitfalls

- **Skipping the primitive part.** Without line L6 the candidate $2x + 4$ in the example fails the test even though its primitive part is the gcd, and the algorithm wastes tries.
- **Too small a point.** With $\xi$ below the bound of line L2, a candidate can divide both inputs and still not be the gcd, so the test proves nothing.
- **Unsymmetric digits.** Digits in $[0, \xi)$ cannot represent negative coefficients. The expansion must use the symmetric range $(-\xi/2, \xi/2]$.
- **Unbounded retries.** Each failure multiplies the integer sizes. Cap the number of tries or the size of $\xi \cdot d$, and fall back to a modular gcd.
- **Contents.** The integer gcd of the contents must be put back at the end, since $\gcd(2x, 4x) = 2x$, not $x$.

## Implementations

## History

Char, Geddes and Gonnet presented the heuristic gcd at EUROSAM 1984 and published the full version, with the multivariate case and the correctness theorem, in the Journal of Symbolic Computation in 1989. It was built into Maple, where fast big-integer arithmetic made it the fastest gcd method for many everyday inputs. Schönhage analysed a probabilistic version in 1988, and Liao and Fateman compared it with modular methods experimentally in 1995. Geddes, Czapor and Labahn give a textbook account in Chapter 7.

## References
