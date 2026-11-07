---
tag: XE8KS1
kind: problem
slug: polynomial-composition
name: Polynomial composition
aliases:
- f(g(x))
- functional composition of polynomials
- substitution of a polynomial
area: algebra/polynomial-arithmetic
level: advanced
summary: Compute f(g(x)) for two polynomials, or its truncation or its remainder modulo a third; the cost is central to power-series algorithms.
model: blum-shub-smale-machine
complexity:
  vars: {m: the degree of the outer polynomial f, n: the degree of the inner polynomial g, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(m n) log m)}
prereqs: [polynomial-ring, polynomial-multiplication, polynomial-evaluation]
see_also: [brent-kung-composition, horner-rule, paterson-stockmeyer-algorithm, power-series-inversion, polynomial-evaluation, newton-iteration, chebyshev-polynomials, matrix-multiplication-exponent]
sources:
  - paper: doi:10.1145/322092.322099
    title: Richard P. Brent and H. T. Kung, Fast algorithms for manipulating formal power series, Journal of the ACM 25(4), 1978
    locator: pp. 581 to 595 (composition and reversion of power series, and composition modulo a polynomial)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 12.2 (fast modular composition of polynomials by the Brent and Kung method with matrix multiplication)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.7, Manipulation of power series (composition and reversion)
  - paper: doi:10.1137/08073408X
    title: Kiran S. Kedlaya and Christopher Umans, Fast polynomial factorization and modular composition, SIAM Journal on Computing 40(6), 2011
    locator: pp. 1767 to 1802
  - paper: doi:10.1137/0204045
    title: Alfred V. Aho, Kenneth Steiglitz and Jeffrey D. Ullman, Evaluating polynomials at fixed sets of points, SIAM Journal on Computing 4(4), 1975
    locator: pp. 533 to 539 (the Taylor shift f(x + a) with one product)
  - url: https://arxiv.org/abs/2404.05177
    title: Yasunori Kinoshita and Baitian Li, Power series composition in near-linear time, FOCS 2024
    locator: Abstract (a softly linear algebraic algorithm for power series composition)
---

Polynomial composition asks for $f(g(x)) = \sum_i f_i\, g(x)^i$, given polynomials $f$ and $g$ over a commutative ring $R$. In its plain form the output has degree up to $m n$ for $\deg f = m$ and $\deg g = n$, and divide and conquer computes it with $O(M(m n) \log m)$ ring operations. Its two truncated forms are harder: power series composition $f(g) \bmod x^n$ and modular composition $f(g) \bmod h$. They have outputs of size $n$, yet the fast algorithms of Brent and Kung (1978) need about $\sqrt{n}\, M(n)$ operations, and only recent work comes close to linear time. Modular composition is the bottleneck of fast factoring over finite fields.

## In plain words

To compose two polynomials, we put the second one in place of x in the first. If the first is x squared plus one and the second is x plus one, we get x plus one, squared, plus one.

The result can be long: its degree is the product of the two degrees. To make it, we can follow the first polynomial term by term, as when we evaluate it at a number, but with a polynomial in place of the number.

Often we need only part of the result: its first terms, or its remainder after division by a third polynomial. Then the answer is short, but no simple method gets it quickly, and finding fast methods is still a research topic.

## Definition

Let $R$ be a commutative ring with $1$. For $f = \sum_{i=0}^{m} f_i x^i$ and $g$ in $R[x]$, the **composition** is

$$f \circ g = f(g) = \sum_{i=0}^{m} f_i\, g^i \in R[x].$$

The map $f \mapsto f(g)$ is the ring homomorphism $R[x] \to R[x]$ that fixes $R$ and sends $x$ to $g$, so $(f_1 + f_2)(g) = f_1(g) + f_2(g)$ and $(f_1 f_2)(g) = f_1(g)\, f_2(g)$. Composition is associative, $(f \circ g) \circ h = f \circ (g \circ h)$, both sides being the homomorphism that sends $x$ to $g(h)$. It is not commutative. If $\deg f = m \ge 1$ and $\deg g = n \ge 1$, the coefficient of $x^{mn}$ in $f(g)$ is $\operatorname{lc}(f) \operatorname{lc}(g)^m$, and every other term has a lower degree, so $\deg f(g) = m n$ when this product is nonzero, for example over an integral domain.

**Problems.**

1. **Composition.** Given $f$ and $g$, compute $f(g)$.
2. **Power series composition.** Given $n$ and $f, g$ modulo $x^n$ with $g(0) = 0$, compute $f(g) \bmod x^n$. The condition $g(0) = 0$ makes the answer depend only on $f_0, \ldots, f_{n-1}$, because $g^i \equiv 0 \pmod{x^n}$ for $i \ge n$.
3. **Modular composition.** Given a polynomial $h$ of degree $n$ with a unit leading coefficient and $f, g$ of degree less than $n$, compute $f(g) \bmod h$.

**Cost model.** Costs count ring operations of $R$ at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/), unless a bound says it counts bit operations. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$, with $M(n)/n$ nondecreasing.

## Variants

- **Evaluation.** If $g = a$ is a constant, $f(g) = f(a)$, and the problem is [polynomial evaluation](/polynomial-evaluation/).
- **Taylor shift.** $g = x + a$ gives $f(x + a)$, the expansion of $f$ around $-a$. It has an output of size $m + 1$ and is much easier than general composition.
- **Decomposition.** The inverse problem asks, for a given $F$, for $f$ and $g$ of degree at least $2$ with $F = f(g)$, if they exist.
- **Reversion.** Given a power series $g$ with $g(0) = 0$ and $g_1$ a unit, find $f$ with $f(g) \equiv x \pmod{x^n}$. Newton iteration reduces it to power series composition, as Brent and Kung show.
- **Multivariate composition.** Substitute polynomials for several variables at once.

## Examples

The values were checked by a script.

- $f = x^2 + 1$, $g = x + 1$: $f(g) = (x + 1)^2 + 1 = x^2 + 2x + 2$, while $g(f) = x^2 + 2$. So composition is not commutative.
- $x^2 \circ (x + 1) = x^2 + 2x + 1$ and $(x + 1) \circ x^2 = x^2 + 1$.
- **Chebyshev polynomials.** With $T_2 = 2x^2 - 1$ and $T_3 = 4x^3 - 3x$, $T_2(T_3) = 32x^6 - 48x^4 + 18x^2 - 1 = T_6$. In general $T_a(T_b) = T_{ab}$, because $T_k(\cos \theta) = \cos(k \theta)$; see [Chebyshev polynomials](/chebyshev-polynomials/).
- **A drop of degree.** Over $\mathbb{Z}/4\mathbb{Z}$, $f = 2x^2 + x$ and $g = 2x + 1$ give $f(g) = 8x^2 + 8x + 2 + 2x + 1 = 2x + 3$. Here $\operatorname{lc}(f) \operatorname{lc}(g)^2 = 8 = 0$, so the degree is $1$, not $m n = 2$.
- **Taylor shift.** $x^3 \circ (x + 2) = x^3 + 6x^2 + 12x + 8$.
- **Power series.** $1/(1 - x) = \sum_i x^i$ composed with $g = x + x^2$ is $1/(1 - x - x^2)$, and modulo $x^8$ it is $1 + x + 2x^2 + 3x^3 + 5x^4 + 8x^5 + 13x^6 + 21x^7$, the Fibonacci numbers. Only $f_0, \ldots, f_7$ are needed.

## Known algorithms

- **Horner's rule with a polynomial argument.** Set $r = f_m$ and repeat $r \leftarrow r g + f_i$ for $i = m - 1$ down to $0$, as in [Horner's rule](/horner-rule/). Step $i$ multiplies a polynomial of degree $(m - 1 - i) n$ by $g$, so the cost is at most $m\, M(m n + 1) + O(m)$ ring operations, and $O(m^2 n^2)$ with schoolbook products. The correctness is the same as for Horner's rule, because the map $x \mapsto g$ is a homomorphism.
- **Divide and conquer.** Write $f = f_{\mathrm{lo}} + x^k f_{\mathrm{hi}}$ with $k = \lceil (m + 1)/2 \rceil$ and $\deg f_{\mathrm{lo}} < k$, so that $f(g) = f_{\mathrm{lo}}(g) + g^k f_{\mathrm{hi}}(g)$. Compute the powers $g^{2}, g^{4}, \ldots$ once, by repeated squaring. When $m + 1$ is a power of $2$, recursion level $j$ makes $2^j$ products of degree about $m n / 2^j$, each costing at most $M(m n) / 2^j$ by the assumption on $M$, so a level costs $O(M(m n))$ and there are $\log_2 (m + 1)$ levels. The total is $O(M(m n) \log m)$. This is within a factor $O(\log m)$ of the output size $m n$ with FFT products.
- **Taylor shift by one product.** If $m!$ is a unit of $R$, then $k!\, [x^k] f(x + a) = \sum_{i \ge k} (i!\, f_i) \cdot a^{i-k}/(i-k)!$, which is one product of two sequences of length $m + 1$ after reversing one. So $f(x + a)$ costs $O(M(m))$. Aho, Steiglitz and Ullman (1975) give this method.
- **[Brent-Kung composition](/brent-kung-composition/).** For power series and modular composition, write $f$ in blocks of $k \approx \sqrt{n}$ coefficients. Compute the baby steps $g, g^2, \ldots, g^k$ modulo $x^n$ or $h$, evaluate all blocks at once as one matrix product, and combine the blocks by Horner's rule in $g^k$, the giant steps. This costs $O(\sqrt{n}\, M(n) + n^{(\omega + 1)/2})$, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/). Brent and Kung also give a power series method with about $(n \log n)^{1/2} M(n)$ operations, based on a Taylor expansion of $f$ around the low part of $g$. Von zur Gathen and Gerhard, Section 12.2, present the modular version.
- **Paterson and Stockmeyer.** The same baby-step giant-step idea, for evaluating a polynomial at a matrix or another ring element with few nonscalar multiplications, is the [Paterson-Stockmeyer algorithm](/paterson-stockmeyer-algorithm/).
- **Kedlaya and Umans.** Over a finite field $\mathbb{F}_q$, modular composition can be done with $n^{1 + o(1)} \log^{1 + o(1)} q$ bit operations. The method is not algebraic: it lifts the problem to the integers and uses multipoint evaluation in several variables.
- **Kinoshita and Li.** In 2024 they gave an algebraic algorithm for power series composition with a softly linear number of ring operations, building on the method of Bostan and Mori for rational power series.

## Bounds

- **Composition.** The output has $m n + 1$ coefficients, so $\Omega(m n)$ is needed in general, and divide and conquer gives $O(M(m n) \log m)$. With FFT multiplication this is $O(m n \log(m n) \log m)$ when $R$ supports the FFT.
- **Power series composition.** The lower bound $\Omega(n)$ is the only one known. The upper bound is softly linear by Kinoshita and Li (2024); before that, the best algebraic bounds were those of Brent and Kung (1978) and later improvements to about $n^{1.43}$.
- **Modular composition.** Algebraic bound $O(\sqrt{n}\, M(n) + n^{(\omega + 1)/2})$ by Brent and Kung; with $\omega < 2.38$ this is about $n^{1.69}$. Over finite fields, Kedlaya and Umans give $n^{1 + o(1)}$ bit operations up to the factor in $\log q$. Whether an algebraic algorithm with $n^{1 + o(1)}$ ring operations exists for modular composition over every field is open.

All the bounds stated here are proved bounds of the cited papers; none is an observed running time.

## Reductions

- **Evaluation reduces to composition** with a constant $g$.
- **Reversion reduces to composition.** Newton iteration for the equation $f(g) = x$ needs a constant number of compositions per step at doubling precisions, so reversion costs a constant times composition, as Brent and Kung show.
- **Factoring reduces to modular composition.** In the factoring algorithms of [polynomial factorization over finite fields](/polynomial-factorization-over-finite-fields/), the Frobenius powers $x^{q^i} \bmod h$ are computed by modular compositions $x^{q^{i+j}} = x^{q^i} \circ x^{q^j} \bmod h$, and this step dominates the cost. Fast modular composition gives Kedlaya and Umans' fast factoring algorithm.
- **Composition with $x + a$ reduces to one product**, when $m!$ is a unit, by the Taylor shift formula above.

## Applications

- **Power series algorithms**: reversion, solving functional equations, and the change of variables in generating functions.
- **Factoring over finite fields**, through modular composition, in the distinct-degree and equal-degree stages and in [irreducibility tests](/polynomial-irreducibility-testing/).
- **Computer algebra** for algebraic numbers, where a field $\mathbb{F}[x]/(h)$ is changed by a substitution, and for the minimal polynomials of such elements.
- **Real root isolation**, where the [Vincent-Collins-Akritas method](/vincent-collins-akritas/) uses the Taylor shift $f(x + 1)$ and the map $x \mapsto 1/x$ many times.
- **Iterated maps**, such as the Chebyshev identity $T_a(T_b) = T_{ab}$ and the iterates of a polynomial map.

## References
