---
tag: AA4MHK
kind: theorem
slug: gauss-lemma
name: Gauss's lemma for polynomials
aliases:
- Gauss's lemma
- Gauss's lemma on primitive polynomials
- content multiplicativity
area: algebra/polynomial-arithmetic
level: advanced
summary: The product of two primitive polynomials is primitive, so factorisations over Z and Q correspond.
prereqs: [polynomial, irreducible-polynomial, monic-polynomial]
see_also: [primitive-polynomial, eisenstein-criterion, polynomial-factorization-over-integers, brown-modular-gcd, polynomial-gcd, pseudo-division, rational-root-theorem, zassenhaus-algorithm]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.2, Gauss' lemma (content, primitive part, and the normal form in R[x] for a UFD R); Section 6.6, Mignotte's factor bound and a modular gcd algorithm in Z[x]
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of polynomials (content, primitive part, and Gauss's lemma over a unique factorization domain)
  - book: isbn:9780387953854
    title: Serge Lang, Algebra, revised third edition, Graduate Texts in Mathematics 211, Springer, 2002
    locator: Chapter IV, Section 2, Polynomials over a factorial ring
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 9.3, Polynomial rings that are unique factorization domains
---

Gauss's lemma says that over the integers, or over any unique factorization domain, the product of two primitive polynomials is again primitive. Its main consequence is that a polynomial with integer coefficients factors over the rationals only if it factors over the integers with the same degrees. This is why algorithms for factoring and gcd over $\mathbb{Z}[x]$ can split off the content, work with primitive polynomials, and never need fractions.

## Statement

Let $R$ be a unique factorization domain with fraction field $K$; the main case is $R = \mathbb{Z}$, $K = \mathbb{Q}$. For a nonzero $f = \sum_k f_k x^k \in R[x]$, the content $\operatorname{cont}(f)$ is a gcd of the coefficients $f_k$, defined up to a unit factor. The polynomial $f$ is primitive if $\operatorname{cont}(f)$ is a unit. Every nonzero $f$ is $f = \operatorname{cont}(f) \cdot \operatorname{pp}(f)$ with the primitive part $\operatorname{pp}(f)$ primitive. Over $\mathbb{Z}$ the usual normal form takes $\operatorname{cont}(f) > 0$ with the sign chosen so that $\operatorname{lc}(\operatorname{pp}(f)) > 0$.

**Theorem 1 (Gauss's lemma).** If $g, h \in R[x]$ are primitive, then $gh$ is primitive.

**Corollary 2 (content is multiplicative).** For nonzero $g, h \in R[x]$, $\operatorname{cont}(gh) = \operatorname{cont}(g) \operatorname{cont}(h)$ and $\operatorname{pp}(gh) = \operatorname{pp}(g) \operatorname{pp}(h)$, up to units.

**Theorem 3 (factorizations over $R$ and $K$).** Let $f \in R[x]$ and suppose $f = GH$ with $G, H \in K[x]$. Then there is $\lambda \in K \setminus \{0\}$ with $\lambda G \in R[x]$ and $\lambda^{-1} H \in R[x]$, so $f = (\lambda G)(\lambda^{-1} H)$ is a factorization in $R[x]$ with the same degrees. If $f$ is primitive, $\lambda G$ and $\lambda^{-1} H$ can be taken primitive.

**Corollary 4 (irreducible elements of $R[x]$).** A polynomial $f \in R[x]$ of positive degree is irreducible in $R[x]$ exactly when it is primitive and irreducible in $K[x]$. The irreducible constants are the irreducible elements of $R$. Hence $R[x]$ is again a unique factorization domain.

**Corollary 5 (monic factors).** If $f \in R[x]$ is [monic](/monic-polynomial/) and $f = GH$ with $G, H \in K[x]$ monic, then $G, H \in R[x]$. In particular, a rational root of a monic integer polynomial is an integer.

## In plain words

The content of an integer polynomial is the greatest common divisor of its coefficients, and the polynomial is primitive when that number is 1. Gauss's lemma says that if two polynomials are both primitive, their product is primitive too, so no prime can divide every coefficient of the product. As a result, if an integer polynomial splits into two factors with fractions in them, you can move the denominators around and get two factors with integer coefficients and the same degrees. So to factor over the rationals, it is enough to factor over the integers, and an algorithm can work with whole numbers only.

## Proof

*Theorem 1.* Suppose $gh$ is not primitive. Then some prime element $p$ of $R$ divides every coefficient of $gh$, because $R$ is a unique factorization domain and a nonunit content has a prime factor. Let $g = \sum_i g_i x^i$ and $h = \sum_j h_j x^j$. Since $g$ and $h$ are primitive, $p$ does not divide all $g_i$ and does not divide all $h_j$. Let $u$ be the least index with $p \nmid g_u$ and $v$ the least index with $p \nmid h_v$. The coefficient of $x^{u+v}$ in $gh$ is

$$g_u h_v + \sum_{i < u} g_i h_{u+v-i} + \sum_{j < v} g_{u+v-j} h_j.$$

Each term of the two sums contains a factor $g_i$ with $i < u$ or $h_j$ with $j < v$, so it is divisible by $p$. The coefficient itself is divisible by $p$. So $p \mid g_u h_v$, and since $p$ is prime, $p \mid g_u$ or $p \mid h_v$. Both are false by the choice of $u$ and $v$. So $gh$ is primitive.

*Corollary 2.* Write $g = \operatorname{cont}(g)\, g^*$ and $h = \operatorname{cont}(h)\, h^*$ with $g^*, h^*$ primitive. Then $gh = \operatorname{cont}(g) \operatorname{cont}(h)\, g^* h^*$ and $g^* h^*$ is primitive by Theorem 1. A constant $c$ times a primitive polynomial $q$ has content $c$: the gcd of the $c q_k$ is $c$ times the gcd of the $q_k$. So $\operatorname{cont}(gh) = \operatorname{cont}(g) \operatorname{cont}(h)$, and the primitive part of $gh$ is $g^* h^*$, both up to units.

*Theorem 3.* If $f = 0$, then $G = 0$ or $H = 0$. If $G = 0$, take $\lambda = 1/b$ for a nonzero $b \in R$ with $bH \in R[x]$; the case $H = 0$ is symmetric. So let $f \ne 0$. Clear denominators: there are nonzero $a, b \in R$ with $aG \in R[x]$ and $bH \in R[x]$. Write $aG = \alpha\, G^*$ and $bH = \beta\, H^*$ with $\alpha = \operatorname{cont}(aG)$, $\beta = \operatorname{cont}(bH)$ and $G^*, H^*$ primitive. Then

$$ab\, f = \alpha \beta\, G^* H^*.$$

Take contents on both sides. By Theorem 1, $G^* H^*$ is primitive, so $\operatorname{cont}(ab f) = \alpha\beta$ up to a unit. Also $\operatorname{cont}(ab f) = ab \operatorname{cont}(f)$. So $\alpha\beta = \epsilon\, ab \operatorname{cont}(f)$ for a unit $\epsilon$, and

$$f = \epsilon \operatorname{cont}(f)\, G^* H^*.$$

The polynomials $\epsilon \operatorname{cont}(f)\, G^*$ and $H^*$ are in $R[x]$, and they are $\lambda G$ and $\lambda^{-1} H$ for $\lambda = \epsilon \operatorname{cont}(f)\, a/\alpha$, since $H^* = (b/\beta) H$ and $(b/\beta)(\epsilon \operatorname{cont}(f) a / \alpha) = \epsilon \operatorname{cont}(f) ab / (\alpha \beta) = 1$. If $f$ is primitive, $\operatorname{cont}(f)$ is a unit and both factors are primitive.

*Corollary 4.* Let $\deg f \ge 1$. If $f$ is not primitive, $f = \operatorname{cont}(f)\, \operatorname{pp}(f)$ is a product of two nonunits of $R[x]$. If $f$ is primitive and $f = GH$ in $K[x]$ with $\deg G, \deg H \ge 1$, Theorem 3 gives a factorization in $R[x]$ with the same positive degrees. So an irreducible $f$ in $R[x]$ is primitive and irreducible in $K[x]$. Conversely, let $f$ be primitive and irreducible in $K[x]$, and let $f = gh$ in $R[x]$. One of $g, h$ has degree $0$, say $g = c \in R$; then $c$ divides every coefficient of $f$, so $c$ is a unit. So $f$ is irreducible in $R[x]$. For unique factorization: factor $f = \operatorname{cont}(f) \operatorname{pp}(f)$, factor the content in $R$, and factor $\operatorname{pp}(f)$ in the unique factorization domain $K[x]$ and move the factors into $R[x]$ by Theorem 3 repeatedly. Each factor is primitive and irreducible in $K[x]$, hence irreducible in $R[x]$. Uniqueness follows from uniqueness in $R$ and in $K[x]$, with Corollary 2 to match the contents and the primitive parts.

*Corollary 5.* By Theorem 3 with $f$ primitive (a monic polynomial is primitive), $f = (\lambda G)(\lambda^{-1} H)$ with both factors in $R[x]$. The leading coefficients $\lambda$ and $\lambda^{-1}$ are in $R$ and their product is $1$, so $\lambda$ is a unit of $R$, and $G = \lambda^{-1} (\lambda G) \in R[x]$, $H = \lambda (\lambda^{-1} H) \in R[x]$. For a root $r \in K$ of $f$, apply this to $G = x - r$. $\blacksquare$

## Consequences

- **Factoring over $\mathbb{Z}$ and $\mathbb{Q}$ are the same problem.** To factor $f \in \mathbb{Z}[x]$, factor the integer $\operatorname{cont}(f)$ and factor $\operatorname{pp}(f)$ into primitive irreducible polynomials. The [Zassenhaus algorithm](/zassenhaus-algorithm/) and [factorization over the integers](/polynomial-factorization-over-integers/) never leave $\mathbb{Z}[x]$, and by Corollary 2 the leading coefficient of each factor divides $\operatorname{lc}(f)$.
- **Gcd in $\mathbb{Z}[x]$.** For primitive $f, g$, the [gcd](/polynomial-gcd/) in $\mathbb{Z}[x]$ is the primitive part of the gcd in $\mathbb{Q}[x]$, and in general $\gcd(f, g) = \gcd(\operatorname{cont} f, \operatorname{cont} g) \cdot \gcd(\operatorname{pp} f, \operatorname{pp} g)$. Its leading coefficient divides $\gcd(\operatorname{lc} f, \operatorname{lc} g)$. [Brown's modular gcd](/brown-modular-gcd/) uses this to fix the leading coefficient of the image before it reconstructs the gcd from residues. The primitive variant of [pseudo-division](/pseudo-division/) divides out contents at each step to keep the numbers small.
- **Rational roots.** By Theorem 3, a root $r/s$ in lowest terms of $f \in \mathbb{Z}[x]$ gives a factor $sx - r$, so $s \mid \operatorname{lc}(f)$ and $r \mid f(0)$. This is the [rational root theorem](/rational-root-theorem/). Corollary 5 is the monic case.
- **Eisenstein's criterion.** The step from "no factorization in $\mathbb{Z}[x]$" to "irreducible in $\mathbb{Q}[x]$" in [Eisenstein's criterion](/eisenstein-criterion/) is Theorem 3.
- **Polynomials in several variables.** By Corollary 4 and induction, $R[x_1, \ldots, x_n]$ is a unique factorization domain, as $R[x_1, \ldots, x_n] = R[x_1, \ldots, x_{n-1}][x_n]$. Multivariate gcd algorithms use contents with respect to one variable in the same way.

**Worked examples.** The products were checked by a short script.

- $g = 2x + 4$ has content $2$ and $h = 3x + 9$ has content $3$. Their product $6x^2 + 30x + 36$ has content $6 = 2 \cdot 3$, and primitive part $x^2 + 5x + 6 = (x + 2)(x + 3) = \operatorname{pp}(g) \operatorname{pp}(h)$.
- $f = 6x^2 + 5x + 1$ factors over $\mathbb{Q}$ as $(x + \tfrac12)(6x + 2)$. Here $a = 2$, $aG = 2x + 1$ with $\alpha = 1$, and $H = 6x + 2$ with $\beta = 2$, $H^* = 3x + 1$. Theorem 3 gives $f = (2x + 1)(3x + 1)$.
- $x^2 + 3x + 1$ has no root $\pm 1$, so by the rational root theorem it has no rational root and is irreducible over $\mathbb{Q}$, and it is primitive, so it is irreducible in $\mathbb{Z}[x]$.

## Tightness

- **Primitivity is needed in Corollary 4.** $2x + 2$ is irreducible in $\mathbb{Q}[x]$, since it has degree $1$, but $2x + 2 = 2 (x + 1)$ is a product of two nonunits in $\mathbb{Z}[x]$.
- **The UFD hypothesis is needed.** Let $R = \mathbb{Z}[2i] = \{ a + 2bi : a, b \in \mathbb{Z} \}$, with fraction field $\mathbb{Q}(i)$. The polynomial $x^2 + 1$ is monic and factors as $(x - i)(x + i)$ over $\mathbb{Q}(i)$, but $i \notin R$, so Corollary 5 fails. It is also irreducible in $R[x]$: a factorization into two linear factors would have leading coefficients $c$ and $c^{-1}$ in $R$, so $c = \pm 1$, and then a factor would be $\pm (x - i)$ or $\pm (x + i)$, which is not in $R[x]$. The ring $R$ is not a unique factorization domain; for example, $2 \cdot 2 = (2i)(-2i)$ with $2$, $2i$ and $-2i$ irreducible and not associates in $R$.
- **The lemma is about the coefficient gcd only.** It says nothing about factors of the leading coefficient alone. For example, $\operatorname{lc}((2x + 1)(3x + 1)) = 6$ although both factors are primitive.

## History

Gauss proved the monic form, Corollary 5 over $\mathbb{Z}$, in Article 42 of the Disquisitiones Arithmeticae (1801): if a monic integer polynomial is a product of two monic polynomials with rational coefficients, then these have integer coefficients. The general statement for unique factorization domains, and the corollary that $R[x]$ is again a unique factorization domain, became standard in the algebra of the late 19th and early 20th century. In computer algebra the content and primitive part were made explicit by the subresultant and modular gcd algorithms of Collins and Brown around 1967 to 1971, and Knuth, Section 4.6.1, and von zur Gathen and Gerhard, Section 6.2, present the lemma in this algorithmic role.

## References
