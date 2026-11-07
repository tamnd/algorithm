---
tag: HMZFQ8
kind: theorem
slug: vieta-formulas
name: Vieta's formulas
aliases:
- Vieta's relations
- relations between roots and coefficients
area: algebra/polynomial-arithmetic
level: intro
summary: Relate the elementary symmetric functions of the roots to the coefficients of a monic polynomial.
prereqs: [polynomial-ring, polynomial-degree, factor-theorem]
see_also: [factor-theorem, polynomial-remainder-theorem, subproduct-tree, discriminant, rational-root-theorem, wilson-theorem, quadratic-formula, power-series-inversion]
sources:
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 14.6, Galois groups of polynomials (the elementary symmetric functions and the coefficients of the general polynomial)
  - book: isbn:9781118072059
    title: David A. Cox, Galois Theory, second edition, Wiley, 2012
    locator: Chapter 2, Symmetric Polynomials (elementary symmetric polynomials, the fundamental theorem, Newton's identities)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 10.1, Fast multipoint evaluation (p. 295; the subproduct tree computes the coefficients of a product of linear factors)
  - url: https://mathshistory.st-andrews.ac.uk/Biographies/Girard_Albert/
    title: J. J. O'Connor and E. F. Robertson, Albert Girard, MacTutor History of Mathematics Archive
    locator: the account of Invention nouvelle en l'algèbre (1629), with the sums of roots, of products of pairs, and the power sums
---

Vieta's formulas express the coefficients of a polynomial that splits into linear factors through its roots: if $f = (x - r_1)(x - r_2) \cdots (x - r_n)$, then the coefficient of $x^{n-k}$ is $(-1)^k e_k(r_1, \ldots, r_n)$, where $e_k$ is the sum of all products of $k$ distinct roots. So the sum of the roots is minus the second coefficient, and the product of the roots is $(-1)^n$ times the constant term. The formulas hold over every commutative ring, and with Newton's identities they link the coefficients to the power sums of the roots.

## Statement

Let $R$ be a commutative ring and $r_1, \ldots, r_n \in R$. For $0 \le k \le n$, the **elementary symmetric polynomial** $e_k$ is

$$e_0 = 1, \qquad e_k(r_1, \ldots, r_n) = \sum_{1 \le i_1 < i_2 < \cdots < i_k \le n} r_{i_1} r_{i_2} \cdots r_{i_k} .$$

So $e_1 = r_1 + \cdots + r_n$ and $e_n = r_1 r_2 \cdots r_n$.

**Theorem (Vieta).** In $R[x]$,

$$\prod_{i=1}^{n} (x - r_i) = \sum_{k=0}^{n} (-1)^k e_k(r_1, \ldots, r_n)\, x^{n-k} .$$

Equivalently, if $f = c\, x^n + a_{n-1} x^{n-1} + \cdots + a_0 = c \prod_{i=1}^{n} (x - r_i)$, then

$$a_{n-k} = (-1)^k\, c\; e_k(r_1, \ldots, r_n) \qquad (1 \le k \le n);$$

in particular $r_1 + \cdots + r_n = -a_{n-1}/c$ and $r_1 \cdots r_n = (-1)^n a_0 / c$ when $c$ is a unit.

**Newton's identities.** Let $f = x^n + a_{n-1} x^{n-1} + \cdots + a_0 = \prod_{i=1}^n (x - r_i)$, set $a_n = 1$, $a_j = 0$ for $j < 0$, and let $p_k = r_1^k + \cdots + r_n^k$ be the power sums, with $p_0 = n$. Then for every $k \ge 1$,

$$p_k + a_{n-1} p_{k-1} + a_{n-2} p_{k-2} + \cdots + a_{n-k+1} p_1 + k\, a_{n-k} = 0 \qquad (k \le n),$$

$$p_k + a_{n-1} p_{k-1} + \cdots + a_0\, p_{k-n} = 0 \qquad (k > n).$$

In power series form, $\operatorname{rev}_{n-1}(f') = \operatorname{rev}_n(f) \cdot \sum_{k \ge 0} p_k y^k$ in $R[[y]]$, where $\operatorname{rev}$ is the reversal of [degree of a polynomial](/polynomial-degree/).

**When the formulas apply.** Over a field $F$, every polynomial splits into linear factors in some field that contains $F$, for example in $\mathbb{C}$ when $F \subseteq \mathbb{C}$, by the [fundamental theorem of algebra](/fundamental-theorem-of-algebra/). So for every $f$ over a field, the formulas hold for its roots counted with multiplicity in such a field.

## In plain words

If you know the roots of a polynomial whose top coefficient is one, you know its coefficients without expanding anything. The second coefficient is minus the sum of the roots. The next one is the sum of the products of all pairs of roots. The next one is minus the sum of the products of all triples, and so on, until the last one, which is the product of all roots, with a sign.

For the quadratic $x^2 + bx + c$ with roots $r$ and $s$, this is the school rule: $r + s = -b$ and $rs = c$.

You can read the formulas the other way too. You can find the sum and the product of the roots from the coefficients, without solving for the roots.

## Proof

**Vieta.** By induction on $n$. For $n = 0$, both sides are $1$. Write $e_k^{(m)} = e_k(r_1, \ldots, r_m)$, with $e_k^{(m)} = 0$ for $k > m$ or $k < 0$. Splitting the products of $k$ distinct indices from $\{1, \ldots, n\}$ by whether they contain $n$ gives

$$e_k^{(n)} = e_k^{(n-1)} + r_n\, e_{k-1}^{(n-1)} .$$

Assume the claim for $n - 1$. Then

$$\prod_{i=1}^{n} (x - r_i) = (x - r_n) \sum_{k=0}^{n-1} (-1)^k e_k^{(n-1)} x^{n-1-k} = \sum_{k=0}^{n} (-1)^k \big(e_k^{(n-1)} + r_n e_{k-1}^{(n-1)}\big) x^{n-k},$$

since $x \cdot (-1)^k e_k^{(n-1)} x^{n-1-k}$ contributes to $x^{n-k}$ with sign $(-1)^k$, and $-r_n \cdot (-1)^{k-1} e_{k-1}^{(n-1)} x^{n-k}$ contributes $(-1)^k r_n e_{k-1}^{(n-1)} x^{n-k}$. The bracket is $e_k^{(n)}$. The form with a leading coefficient $c$ follows by multiplying by $c$ and comparing coefficients. $\square$

**Newton's identities, $k > n$.** Each root satisfies $r_i^{k-n} f(r_i) = 0$, that is $r_i^k + a_{n-1} r_i^{k-1} + \cdots + a_0 r_i^{k-n} = 0$. Sum over $i$. $\square$

**Newton's identities, $1 \le k \le n$.** By the product rule for the formal derivative, $f' = \sum_{i=1}^{n} f_i$ with $f_i = \prod_{j \ne i} (x - r_j) = f / (x - r_i)$. By the [polynomial remainder theorem](/polynomial-remainder-theorem/), the quotient of $f$ by $x - r$ has the coefficient $\sum_{t = j+1}^{n} a_t r^{t-1-j}$ at $x^j$. Summing over the roots, the coefficient of $x^j$ in $f'$ is

$$(j + 1)\, a_{j+1} = \sum_{t = j+1}^{n} a_t\, p_{t-1-j} .$$

Put $j = n - 1 - k$ and $t = n - k + s$:

$$(n - k)\, a_{n-k} = \sum_{s=0}^{k} a_{n-k+s}\, p_s = n\, a_{n-k} + \sum_{s=1}^{k} a_{n-k+s}\, p_s ,$$

because $p_0 = n$. So $\sum_{s=1}^{k} a_{n-k+s} p_s + k\, a_{n-k} = 0$, which is the identity, since $a_n = 1$. $\square$

**Power series form.** The coefficient of $y^k$ in $\operatorname{rev}_n(f) \cdot \sum_s p_s y^s$ is $\sum_{s=0}^{k} a_{n-k+s}\, p_s$. For $k \le n - 1$ this is $(n - k) a_{n-k}$ by the last display, which is the coefficient of $x^{n-1-k}$ in $f'$, that is the coefficient of $y^k$ in $\operatorname{rev}_{n-1}(f')$. For $k = n$ it is $0$ by the identity with $k = n$, and for $k > n$ it is $0$ by the identity for $k > n$. $\blacksquare$

## Consequences

**Examples.**

| polynomial | roots | Vieta |
|---|---|---|
| $x^3 - 6x^2 + 11x - 6$ | $1, 2, 3$ | $e_1 = 6$, $e_2 = 1 \cdot 2 + 1 \cdot 3 + 2 \cdot 3 = 11$, $e_3 = 6$ |
| $2x^2 - 3x - 2 = 2(x - 2)(x + \tfrac12)$ | $2, -\tfrac12$ | sum $= 3/2 = -(-3)/2$, product $= -1 = -2/2$ |
| $x^2 + 1$ over $\mathbb{R}$ | $i, -i$ in $\mathbb{C}$ | sum $0$, product $1$ |
| $x^3 - x = x(x - 1)(x - 2)$ over $\mathbb{F}_3$ | $0, 1, 2$ | $e_1 = 3 = 0$, $e_2 = 2 = -1$, $e_3 = 0$ |

For the roots $1, 2, 3$, the power sums are $p_1 = 6$, $p_2 = 14$, $p_3 = 36$, $p_4 = 98$. Newton's identities give $p_2 = 6 p_1 - 2 \cdot 11 = 14$ and $p_3 = 6 p_2 - 11 p_1 + 3 \cdot 6 = 36$, and the series $(3 - 12y + 11y^2) / (1 - 6y + 11y^2 - 6y^3) = 3 + 6y + 14y^2 + 36y^3 + 98y^4 + \cdots$.

- **From roots to coefficients.** Computing all $e_k$ of $n$ given numbers is the expansion of $\prod (x - r_i)$. Multiplying in the factors one at a time costs $O(n^2)$ operations; the root of a [subproduct tree](/subproduct-tree/) gives them in $O(M(n) \log n)$.
- **From coefficients to power sums.** The power series form computes $p_1, \ldots, p_N$ with one [power series inversion](/power-series-inversion/) and one product, in $O(M(N))$ operations, over every commutative ring. The reverse direction divides by $k$, so it needs $k$ to be a unit, for example characteristic $0$ or characteristic greater than $n$.
- **Integer roots divide the constant term.** If $f \in \mathbb{Z}[x]$ is monic and $f = \prod (x - r_i)$ with integer roots, then each $r_i$ divides $a_0 = (-1)^n r_1 \cdots r_n$. The [rational root theorem](/rational-root-theorem/) is the general form.
- **Wilson's theorem.** Over $\mathbb{F}_p$, $x^{p-1} - 1$ has the $p - 1$ distinct roots $1, \ldots, p - 1$ by Fermat's little theorem, so by the [factor theorem](/factor-theorem/) $x^{p-1} - 1 = \prod_{a=1}^{p-1} (x - a)$. Vieta for the constant term gives $-1 = (-1)^{p-1} (p-1)!$, so $(p - 1)! \equiv -1 \pmod p$: this is [Wilson's theorem](/wilson-theorem/).
- **Symmetric functions of the roots.** Every polynomial in the roots that is symmetric under permutations is a polynomial in $e_1, \ldots, e_n$, so a polynomial in the coefficients (the fundamental theorem on symmetric polynomials; Cox, Chapter 2). The [discriminant](/discriminant/) $\prod_{i<j} (r_i - r_j)^2$ is such a function.
- **The quadratic case.** From $r + s = -b$ and $rs = c$, $(r - s)^2 = b^2 - 4c$, which gives the [quadratic formula](/quadratic-formula/).

## Tightness

- **The polynomial must split.** The formulas speak about $n$ roots counted with multiplicity. If $f$ has fewer roots in $R$, they hold only in a larger ring where $f$ splits, as for $x^2 + 1$ over $\mathbb{R}$.
- **Over a ring with zero divisors the roots are not determined.** Over $\mathbb{Z}/8\mathbb{Z}$, $x^2 - 1 = (x - 1)(x - 7) = (x - 3)(x - 5)$, and the polynomial has the four roots $1, 3, 5, 7$. Vieta's formulas hold for each factorization, but there is no single multiset of "the roots": the product $1 \cdot 3 \cdot 5 \cdot 7 = 105 \equiv 1$ of all four roots is not the constant term $-1 \equiv 7$. Over an integral domain the factorization into linear factors is unique up to order.
- **Commutativity is needed.** In a ring that is not commutative, the expansion of $\prod (x - r_i)$ depends on the order of the factors, and the coefficients are not symmetric functions of the $r_i$.
- **The division by $k$ in Newton's identities.** The identities hold over every commutative ring, but solving them for $a_{n-k}$ needs $k$ to be a unit. Over $\mathbb{F}_2$, $x^2$ and $x^2 + 1 = (x + 1)^2$ have the same power sums $p_k = 0$ for all $k \ge 1$, since both roots are equal and $2 = 0$.

## History

The formulas carry the name of François Viète. Albert Girard, in Invention nouvelle en l'algèbre (1629), gave the sums of the roots, of the products of pairs and of larger groups of roots as the coefficients of an equation of any degree, together with formulas for the power sums of the roots, and stated that an equation has as many roots as its degree (MacTutor biography of Girard).

## References
