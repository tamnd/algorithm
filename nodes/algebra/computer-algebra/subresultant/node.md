---
tag: KKA742
kind: concept
slug: subresultant
name: Subresultant
aliases: [subresultant sequence, subresultant chain, principal subresultant coefficient]
area: algebra/computer-algebra
level: advanced
summary: Generalizes the resultant to a sequence of determinants that keeps coefficient growth under control.
prereqs: [sylvester-matrix, resultant, determinant]
see_also: [subresultant-prs, subresultant-gcd, primitive-prs, polynomial-gcd, cylindrical-algebraic-decomposition, sturm-sequence, hadamard-bound, discriminant]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.10 (subresultants and the degrees of the gcd) and Section 11.2, Subresultants (the structure theorem and the size bounds)
  - paper: doi:10.1145/321371.321381
    title: George E. Collins, Subresultants and reduced polynomial remainder sequences, Journal of the ACM 14(1), 1967
    locator: pp. 128 to 142
  - paper: doi:10.1145/321662.321665
    title: W. S. Brown and J. F. Traub, On Euclid's algorithm and the theory of subresultants, Journal of the ACM 18(4), 1971
    locator: pp. 505 to 514 (the fundamental theorem of subresultants)
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 4, Algebra (subresultants, signed subresultants and the structure theorem) and Chapter 9, Cauchy Index (subresultants and real roots)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 7, Polynomial GCD Computation (subresultants and the subresultant PRS)
---

The subresultants of two polynomials $f$ and $g$ are a sequence of polynomials $S_{n-1}, \ldots, S_1, S_0$ whose coefficients are determinants of submatrices of the [Sylvester matrix](/sylvester-matrix/). $S_0$ is the [resultant](/resultant/), and the others refine it: the degree of $\gcd(f, g)$ is the least $j$ with a nonzero $j$-th principal subresultant coefficient, and the first regular subresultant of that index is a multiple of the gcd. Up to known constant factors, the subresultants are the remainders of the Euclidean algorithm, but their coefficients are determinants and so stay small. This is the basis of the [subresultant PRS](/subresultant-prs/), of gcds over integral domains, and of elimination with parameters.

## In plain words

The resultant is one number made from two polynomials, and it is zero exactly when they share a factor. But it says nothing about how large the shared factor is. Subresultants are a list of smaller determinants, cut out of the same table of coefficients. The first of these numbers that is not zero tells the degree of the shared factor, and the polynomial that goes with it is that factor, times a constant.

There is a second reason to use them. The school method for the greatest common divisor gives remainders whose numbers grow very fast. The subresultants are the same remainders, only multiplied by suitable constants, and as determinants their numbers stay small. They also behave well when the coefficients contain a parameter and the parameter takes a value.

## The idea

**Notation.** $R$ is an integral domain with fraction field $F$, and $f = \sum_{i \le m} a_i x^i$, $g = \sum_{i \le n} b_i x^i$ are in $R[x]$ with $m \ge n \ge 1$ and $a_m b_n \ne 0$. Rows of matrices list coefficients from $x^{\text{high}}$ down, as on the [Sylvester matrix](/sylvester-matrix/) page.

**Definition.** For $0 \le j < n$, let $M_j$ be the $(m + n - 2j) \times (m + n - j)$ matrix whose rows are the coefficient vectors of

$$x^{n-1-j} f, \; \ldots, \; x f, \; f, \quad x^{m-1-j} g, \; \ldots, \; x g, \; g$$

on the monomials $x^{m+n-j-1}, \ldots, x, 1$. For $0 \le i \le j$, let $M_j^{(i)}$ be the square matrix formed by the first $m + n - 2j - 1$ columns of $M_j$ and the column of $x^i$. The $j$-th subresultant is

$$S_j = \sum_{i=0}^{j} \det M_j^{(i)} \, x^i \in R[x],$$

and its coefficient of $x^j$, $s_j = \det M_j^{(j)}$, is the $j$-th principal subresultant coefficient. $S_j$ is *regular* when $\deg S_j = j$ and *defective* when $\deg S_j < j$. For $j = 0$ the matrix $M_0$ is the full Sylvester matrix and $S_0 = s_0 = \operatorname{Res}(f, g)$.

**A combination of $f$ and $g$.** Expanding $\det M_j^{(i)}$ along its last column, as in the proof that the resultant is a combination of $f$ and $g$, gives

$$S_j = u_j f + v_j g, \qquad \deg u_j < n - j, \quad \deg v_j < m - j,$$

with $u_j, v_j \in R[x]$. The cofactors $u_j, v_j$ are the Bézout coefficients of the extended Euclidean algorithm, up to the same constant factor.

**The gcd degree.** Over $F$, $\deg \gcd(f, g)$ is the least $j$ with $s_j \ne 0$, and for that $j$, $S_j$ is an associate of $\gcd(f, g)$. *Proof.* $s_j$ is the determinant of the linear map $\varphi_j$ that sends $(u, v)$, with $\deg u < n - j$ and $\deg v < m - j$, to the coefficients of $x^{m+n-j-1}, \ldots, x^j$ in $u f + v g$. So $s_j \ne 0$ exactly when no nonzero $(u, v)$ in this space has $\deg(u f + v g) < j$. Let $h = \gcd(f, g)$ and $k = \deg h$. If $j < k$, then $(u, v) = (g / h, \, -f / h)$ has $\deg u = n - k < n - j$, $\deg v < m - j$ and $u f + v g = 0$, so $s_j = 0$. If $j = k$, then each $u f + v g$ is a multiple of $h$, so it is $0$ or has degree at least $k$. It is $0$ only if $u$ is a multiple of $g / h$, which has degree $n - k > \deg u$, so only if $u = v = 0$. Hence $s_k \ne 0$, and $S_k = u_k f + v_k g$ is a multiple of $h$ of degree $k$, an associate of $h$. $\square$

**Structure theorem.** Brown and Traub showed that the nonzero subresultants come in blocks. If $S_{j+1}$ is regular and $S_j \ne 0$ has degree $d \le j$, then $S_{j-1} = \cdots = S_{d+1} = 0$, $S_d$ is a multiple of $S_j$, namely $(\operatorname{LC}(S_j)/s_{j+1})^{j-d} S_j$, and $S_{d-1}$ is $\operatorname{prem}(S_{j+1}, S_j)$ divided by $(-s_{j+1})^{j-d+2}$. So the chain is a Euclidean remainder sequence in which each remainder is scaled by a constant that is known in advance. The [subresultant PRS](/subresultant-prs/) uses exactly this, and its correctness proof states the precise form.

**Specialization.** The subresultants are polynomials in the coefficients of $f$ and $g$, so they commute with ring homomorphisms $\phi: R \to R'$: if $\phi(a_m) \ne 0$ and $\phi(b_n) \ne 0$, then the subresultants of $\phi(f)$ and $\phi(g)$ are $\phi(S_j)$. The Euclidean remainders do not have this property, because the degrees of the remainders can change under $\phi$. This is why subresultants work for polynomials with parameters and for modular methods.

**Size.** Each coefficient of $S_j$ is the determinant of a matrix whose rows are rows of the Sylvester matrix restricted to some columns. Over $\mathbb{Z}$, the [Hadamard bound](/hadamard-bound/) gives $|\det M_j^{(i)}| \le \|f\|_2^{\,n-j} \|g\|_2^{\,m-j}$. So the coefficients have $O((m + n)(L + \log(m + n)))$ digits for inputs with $L$-digit coefficients, while plain pseudo-remainders can grow exponentially.

## Examples

- **A common root.** For $f = x^2 - 3x + 2 = (x-1)(x-2)$ and $g = x^2 - 1$, $m = n = 2$. $M_1$ has the rows $(1, -3, 2)$ and $(1, 0, -1)$, so $S_1 = \det\begin{pmatrix} 1 & -3 \\ 1 & 0 \end{pmatrix} x + \det\begin{pmatrix} 1 & 2 \\ 1 & -1 \end{pmatrix} = 3x - 3$, and $S_0 = \operatorname{Res}(f, g) = 0$. So $s_0 = 0$, $s_1 = 3 \ne 0$, the gcd has degree 1, and it is $S_1 / 3 = x - 1$.
- **A parameter.** For $f = x^2 - t$ and $g = x^2 - 3x + 2$ in $\mathbb{Z}[t][x]$, $S_1 = -3x + (t + 2)$ and $S_0 = (1 - t)(4 - t)$. The leading coefficients of $f$ and $g$ do not depend on $t$, so for each value $t_0$ the specialized polynomials have $\gcd$ of degree 1 exactly when $S_0(t_0) = 0$, that is $t_0 \in \{1, 4\}$, and then the gcd is $S_1$ at $t_0$: $-3x + 3$ for $t_0 = 1$, and $-3x + 6$ for $t_0 = 4$. Indeed $x^2 - 1$ and $x^2 - 4$ share the roots 1 and 2 with $g$.
- **A gap.** For $f = x^5 - x^4 - x^3 - x^2 + 1$ and $g = x^4 - x^3 - x$, the chain is $S_3 = -x^3 + 1$, $S_2 = -1$, $S_1 = 0$, $S_0 = -1$. $S_2$ is defective of degree 0, so $S_1 = 0$ and $S_0$ is the multiple $(\operatorname{LC}(S_2)/s_3)^2 S_2 = -1$. The worked trace is on [subresultant PRS](/subresultant-prs/).
- **Knuth's pair.** For $u = x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5$ and $v = 3x^6 + 5x^4 - 4x^2 - 9x + 21$, the sequence of subresultants ends with the constant $260708$, while pseudo-division without any reduction ends with a 35-digit constant. See [subresultant gcd](/subresultant-gcd/) and [primitive PRS](/primitive-prs/).

## Where it is used

- **Gcds over integral domains.** The [subresultant gcd](/subresultant-gcd/) and the [subresultant PRS](/subresultant-prs/) compute gcds in $\mathbb{Z}[x]$ and $K[y_1, \ldots, y_k][x]$ without fractions and without content gcds in the loop.
- **Elimination and cylindrical algebraic decomposition.** The projection step of [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) uses the principal subresultant coefficients of pairs of polynomials in $x_n$ as polynomials in the other variables: the degree of the gcd stays constant on each region where their signs are constant.
- **Real roots.** The signed subresultants of $f$ and $f'$ give the Sturm-Habicht sequence, whose sign changes count real roots like a [Sturm sequence](/sturm-sequence/), with integer coefficients of bounded size (Basu, Pollack and Roy).
- **Resultants and discriminants.** $S_0$ is the resultant, and the subresultants of $f$ and $f'$ refine the [discriminant](/discriminant/): the least $j$ with $s_j(f, f') \ne 0$ gives the degree of $\gcd(f, f')$, which measures the repeated roots.
- **Modular and fast algorithms.** Because subresultants commute with reduction modulo a prime when the leading coefficients survive, they can be computed modulo many primes and reconstructed. Over a field, the half-gcd algorithm computes them fast.

## References
