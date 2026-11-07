---
tag: KDEH3Q
kind: theorem
slug: hilbert-nullstellensatz
name: Hilbert's Nullstellensatz
aliases:
- Nullstellensatz
- weak Nullstellensatz
- strong Nullstellensatz
- Hilbert's zero theorem
- Rabinowitsch trick
area: algebra/computer-algebra
level: core
summary: Relates the radical of an ideal to the polynomials vanishing on its zero set.
prereqs: [polynomial-ideal, resultant, hilbert-basis-theorem]
see_also: [groebner-basis, ideal-membership-problem, polynomial-system-solving, primary-decomposition, elimination-theorem, reduced-groebner-basis]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 4, Section 1 (the weak Nullstellensatz, the strong Nullstellensatz and the proof by the Rabinowitsch trick) and Section 2 (radical membership and the consistency test with Gröbner bases); Chapter 3, Section 6 (resultants, the resultant lies in the ideal, and specialization)
  - paper: "Enrique Arrondo, Another elementary proof of the Nullstellensatz, American Mathematical Monthly 113, 2006"
    locator: the proof of the weak Nullstellensatz by induction on the number of variables with resultants
  - paper: "David Hilbert, Über die vollen Invariantensysteme, Mathematische Annalen 42, 1893"
    locator: the theorem on the zeros of a system of forms
  - paper: "J. L. Rabinowitsch, Zum Hilbertschen Nullstellensatz, Mathematische Annalen 102, 1929"
    locator: the extra variable that derives the strong form from the weak form
  - paper: "János Kollár, Sharp effective Nullstellensatz, Journal of the American Mathematical Society 1, 1988"
    locator: the degree bound for the cofactors of a Nullstellensatz certificate
---

Hilbert's Nullstellensatz describes exactly which polynomials vanish on the zero set of an ideal over an algebraically closed field. The weak form says that a system of polynomial equations has no common solution only when $1$ is a combination of the equations. The strong form says that a polynomial vanishes at each common solution only when some power of it is such a combination, so that the ideal of the zero set of $I$ is the radical $\sqrt{I}$. With a [Gröbner basis](/groebner-basis/) both forms become algorithms: a system is inconsistent exactly when its reduced basis is $\{1\}$.

## Statement

**Notation.** $K$ is an algebraically closed field, for example $\mathbb{C}$ or the algebraic closure of $\mathbb{Q}$ or of $\mathbb{F}_p$. For an ideal $I \subseteq K[x_1, \ldots, x_n]$, $V(I) = \{a \in K^n : f(a) = 0 \text{ for each } f \in I\}$. For a set $V \subseteq K^n$, $I(V) = \{f : f(a) = 0 \text{ for each } a \in V\}$. The radical is $\sqrt{I} = \{f : f^m \in I \text{ for some } m \ge 1\}$.

**Theorem (weak Nullstellensatz).** If $I \subseteq K[x_1, \ldots, x_n]$ is an ideal with $V(I) = \emptyset$, then $I = K[x_1, \ldots, x_n]$, that is, $1 \in I$.

**Theorem (strong Nullstellensatz).** Let $f, f_1, \ldots, f_s \in K[x_1, \ldots, x_n]$. If $f$ vanishes at each point of $V(f_1, \ldots, f_s)$, then $f^m \in \langle f_1, \ldots, f_s \rangle$ for some $m \ge 1$. Equivalently, $I(V(I)) = \sqrt{I}$ for each ideal $I$.

**Corollary (radical membership).** Over any field $k$ with algebraic closure $K$, and $f, f_1, \ldots, f_s \in k[x_1, \ldots, x_n]$: $f$ vanishes on $V(f_1, \ldots, f_s) \subseteq K^n$ exactly when $1 \in \langle f_1, \ldots, f_s, 1 - y f \rangle \subseteq k[x_1, \ldots, x_n, y]$, exactly when the reduced Gröbner basis of this ideal, for any monomial order, is $\{1\}$.

The hypothesis that $K$ is algebraically closed is needed: in $\mathbb{R}[x]$, $V(x^2 + 1) = \emptyset$ but $1 \notin \langle x^2 + 1 \rangle$.

## In plain words

Take a system of polynomial equations, and allow complex solutions. If the system has no solution at all, then there is a short reason: you can multiply the equations by suitable polynomials and add them up to get the equation "1 = 0". If a further polynomial is zero at every solution, then there is again an algebraic reason: some power of that polynomial is such a combination of the equations. So "has no solution" and "follows from the equations" can both be checked by algebra alone, and a computer can do it. The statement fails if you allow only real solutions.

## Proof

**Facts about resultants.** For $g, f \in A[t]$ over a commutative ring $A$, with formal degrees $d \ge 1$ and $e \ge 0$, the [resultant](/resultant/) $\operatorname{Res}_t(g, f) \in A$ is the determinant of the Sylvester matrix. We use two facts (Cox, Little and O'Shea, Chapter 3, Section 6). (R1) There are $p, q \in A[t]$ with $p g + q f = \operatorname{Res}_t(g, f)$, so the resultant lies in the ideal $\langle g, f \rangle \cap A$. (R2) Let $\phi : A \to K$ be a ring map, applied to coefficients. If $g$ is monic of degree $d$, then $\phi(\operatorname{Res}_t(g, f))$ is the resultant of $\phi(g)$ and $\phi(f)$ with the same formal degrees $d, e$. This holds because the determinant is a polynomial in the entries and $\phi$ is a ring map. If $\phi(f)$ is the constant $1$, the Sylvester matrix of $\phi(g)$ and $1$ with formal degrees $d, e$ is block triangular with determinant $\pm 1$, so $\phi(\operatorname{Res}_t(g, f)) = \pm 1$.

**Step 1: a change of coordinates.** Let $h \in K[x_1, \ldots, x_n]$ be nonzero of total degree $D \ge 1$, $n \ge 2$, and let $h_D$ be its homogeneous part of degree $D$. For $\lambda \in K^{n-1}$, substitute $x_i \mapsto x_i + \lambda_i x_n$ for $i < n$. The coefficient of $x_n^D$ in the new polynomial is $h_D(\lambda_1, \ldots, \lambda_{n-1}, 1)$. This is a nonzero polynomial in $\lambda$, because $h_D$ is a nonzero homogeneous polynomial and $h_D(\lambda, 1)$ recovers $h_D$ by homogenization. An algebraically closed field is infinite, so some $\lambda$ makes it nonzero, and after division by this constant $h$ becomes monic in $x_n$ of degree $D$. The substitution is a $K$-algebra automorphism of $K[x_1, \ldots, x_n]$ and an invertible linear map on $K^n$. It maps $I$ to an ideal $I^*$ with $1 \in I^*$ exactly when $1 \in I$, and $V(I^*)$ is the image of $V(I)$, so it is empty exactly when $V(I)$ is.

**Step 2: the weak Nullstellensatz, by induction on $n$.** We prove: if $1 \notin I$, then $V(I) \ne \emptyset$. For $n = 1$, $K[x_1]$ is a principal ideal domain, so $I = \langle g \rangle$. Since $1 \notin I$, either $g = 0$ and $V(I) = K$, or $g$ is not constant and has a root in $K$ because $K$ is algebraically closed. Let $n \ge 2$ and $1 \notin I$. If $I = \langle 0 \rangle$, then $V(I) = K^n$. Otherwise pick $h \in I$, $h \ne 0$. It is not a nonzero constant, because $1 \notin I$, so $D \ge 1$. By step 1 we may assume that $h$ is monic in $x_n$ of degree $D$. Let $I' = I \cap K[x_1, \ldots, x_{n-1}]$. It is an ideal, and $1 \notin I'$. By the induction hypothesis there is $a' \in K^{n-1}$ with $f(a') = 0$ for each $f \in I'$. Let $\phi$ be the evaluation $x_i \mapsto a'_i$ for $i < n$, and let $J = \{\phi(f) : f \in I\} \subseteq K[x_n]$. Since $\phi$ is a surjective ring map from $K[x_1, \ldots, x_n]$ onto $K[x_n]$, $J$ is an ideal. Suppose that $1 \in J$, say $\phi(f) = 1$ with $f \in I$. Take $A = K[x_1, \ldots, x_{n-1}]$, $t = x_n$, and the resultant $r = \operatorname{Res}_{x_n}(h, f)$, with $e$ the degree of $f$ in $x_n$. By (R1), $r \in I \cap A = I'$, so $\phi(r) = r(a') = 0$. By (R2), $\phi(r) = \pm 1$, because $h$ is monic in $x_n$ and $\phi(f) = 1$. This is a contradiction. So $1 \notin J$, and $J = \langle u \rangle$ with $u = 0$ or $u$ not constant. In both cases some $b \in K$ has $u(b) = 0$, so $\phi(f)(b) = f(a', b) = 0$ for each $f \in I$. The point $(a', b)$ lies in $V(I)$.

**Step 3: the strong form, by the Rabinowitsch trick.** Let $f$ vanish on $V(f_1, \ldots, f_s)$. If $f = 0$, take $m = 1$. Otherwise let $J = \langle f_1, \ldots, f_s, 1 - y f \rangle \subseteq K[x_1, \ldots, x_n, y]$. A point $(a, b) \in V(J)$ has $f_i(a) = 0$ for each $i$, so $f(a) = 0$, so $1 - b f(a) = 1 \ne 0$. Hence $V(J) = \emptyset$, and by step 2, $1 \in J$:

$$1 = \sum_{i=1}^{s} p_i(x, y) f_i + q(x, y) (1 - y f).$$

In the field of rational functions $K(x_1, \ldots, x_n)$, substitute $y = 1/f$. The last term vanishes, and $1 = \sum_i p_i(x, 1/f) f_i$. Let $m$ be the largest degree in $y$ of the $p_i$, and at least $1$. Multiply by $f^m$: each $f^m p_i(x, 1/f)$ is a polynomial $A_i$, and $f^m = \sum_i A_i f_i \in \langle f_1, \ldots, f_s \rangle$.

**Step 4: $I(V(I)) = \sqrt{I}$.** If $f^m \in I$, then $f^m$ vanishes on $V(I)$, and so does $f$, because $K$ has no nonzero nilpotents. So $\sqrt{I} \subseteq I(V(I))$. By the Hilbert basis theorem $I = \langle f_1, \ldots, f_s \rangle$ for finitely many $f_i$, and step 3 gives $I(V(I)) \subseteq \sqrt{I}$.

**Step 5: the corollary.** Steps 3 and 4, applied over $K$, show that $f$ vanishes on $V(f_1, \ldots, f_s)$ exactly when $1 \in \langle f_1, \ldots, f_s, 1 - yf \rangle$ in $K[x, y]$. A [reduced Gröbner basis](/reduced-groebner-basis/) does not change under a field extension, because Buchberger's algorithm on inputs with coefficients in $k$ performs only operations in $k$. So $1$ lies in the ideal over $K$ exactly when it lies in the ideal over $k$, exactly when the reduced basis is $\{1\}$. $\blacksquare$

## Consequences

- **Consistency test.** A system $f_1 = \cdots = f_s = 0$ has no solution over $\bar K$ exactly when the reduced Gröbner basis of $\langle f_1, \ldots, f_s \rangle$ is $\{1\}$. This is the first step of [polynomial system solving](/polynomial-system-solving/).
- **Radical membership.** The corollary decides $f \in \sqrt{I}$ with one Gröbner basis computation in one extra variable. Plain membership $f \in I$ is the [ideal membership problem](/ideal-membership-problem/).
- **Points and maximal ideals.** Over an algebraically closed field the maximal ideals of $K[x_1, \ldots, x_n]$ are exactly the ideals $\langle x_1 - a_1, \ldots, x_n - a_n \rangle$ with $a \in K^n$.
- **The ideal-variety correspondence.** $I \mapsto V(I)$ and $V \mapsto I(V)$ are inverse bijections between radical ideals and varieties, and they reverse inclusion. Prime ideals correspond to irreducible varieties, which is the basis of [primary decomposition](/primary-decomposition/).
- **Certificates.** A proof of inconsistency is a list of cofactors $h_i$ with $\sum h_i f_i = 1$. Checking it is one multiplication and one sum. Kollár (1988) proved that, for $f_i$ of degree at most $d \ge 3$ with no common zero, cofactors with $\deg(h_i f_i) \le d^n$ exist. Then the $h_i$ can be found by linear algebra on a [Macaulay matrix](/macaulay-matrix/) of that degree.

## Tightness

**Algebraic closure.** The example $x^2 + 1$ over $\mathbb{R}$ above shows that the weak form fails over a field that is not algebraically closed. The strong form fails too: over $\mathbb{R}$, the constant $1$ vanishes at each point of $V_{\mathbb{R}}(x^2 + 1) = \emptyset$, but no power of $1$ lies in $\langle x^2 + 1 \rangle$.

**The power is needed.** Let $I = \langle x^2, y^2 \rangle$ and $f = x + y$. Then $V(I) = \{(0, 0)\}$ and $f$ vanishes there. The remainders on division by $\{x^2, y^2\}$, a Gröbner basis, are $x + y$ for $f$, $2xy$ for $f^2$ and $0$ for $f^3$. So $m = 3$ is the smallest power that works.

**The degree of the cofactors.** Let $d \ge 2$, $n \ge 2$, and

$$f_1 = x_1^d, \quad f_i = x_{i-1} - x_i^d \ (2 \le i \le n - 1), \quad f_n = 1 - x_{n-1} x_n^{d-1}.$$

These have no common zero: $f_1 = 0$ forces $x_1 = 0$, then $x_2 = \cdots = x_{n-1} = 0$, and then $f_n = 1$. In any certificate $1 = \sum h_i f_i$, substitute $x_{n-1} = x_n^{1-d}$, then $x_{i-1} = x_i^d$ downward, in the field $K(x_n)$. This kills $f_2, \ldots, f_n$ and maps $x_1$ to $x_n^{-d^{n-2}(d-1)}$, so $1 = h_1^* \cdot x_n^{-d^{n-1}(d-1)}$, where $h_1^*$ is the image of $h_1$. A monomial $x^\beta$ maps to a power of $x_n$ with exponent at most $\beta_n$, because the other variables map to negative powers. So $h_1$ has a monomial with $\beta_n \ge d^{n-1}(d - 1)$, and $\deg(h_1 f_1) \ge d^{n-1}(d-1) + d \ge d^n - d^{n-1} + d$. So a degree of order $d^n$ is necessary, and Kollár's bound cannot be improved by more than a lower-order term.

## History

Hilbert proved the theorem in 1893, in a paper on complete systems of invariants. Rabinowitsch gave the one-page derivation of the strong form from the weak form in 1929. The proof above of the weak form by resultants follows Arrondo (2006). Kollár proved the sharp degree bound for certificates in 1988. The use of Gröbner bases to test consistency and radical membership is in Cox, Little and O'Shea, Chapter 4, Section 2.

## References
