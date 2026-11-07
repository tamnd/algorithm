---
tag: GRXPAQ
kind: concept
slug: hilbert-series
name: Hilbert series
aliases:
- Hilbert function
- Hilbert-Poincaré series
- Hilbert polynomial
area: algebra/computer-algebra
level: advanced
summary: Generating function counting the dimension of graded pieces of a graded ideal quotient.
prereqs: [polynomial-ideal, monomial-ordering, groebner-basis]
see_also: [hilbert-basis-theorem, hilbert-nullstellensatz, monomial, leading-term, f5-algorithm, macaulay-matrix, polynomial-system-solving, primary-decomposition]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 9, Section 2 (the Hilbert function of a monomial ideal and counting standard monomials), Section 3 (the Hilbert function of an ideal, via its ideal of leading terms) and Section 4 (dimension from the Hilbert polynomial); Chapter 10, Section 2 (Hilbert driven Buchberger algorithms)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 21, Gröbner bases (the dimension of a zero-dimensional quotient as the number of standard monomials)
  - paper: "Dave Bayer and Mike Stillman, Computation of Hilbert functions, Journal of Symbolic Computation 14(1), 1992"
    locator: the recursive algorithm for the Hilbert series of a monomial ideal
  - paper: "David Hilbert, Über die Theorie der algebraischen Formen, Mathematische Annalen 36, 473-534, 1890"
    locator: the rationality of the Hilbert series and the polynomial behaviour of the Hilbert function
---

The Hilbert series of a graded quotient $S/I$, where $S = K[x_1, \ldots, x_n]$ and $I$ is a homogeneous ideal, is the generating function $\mathrm{HS}_{S/I}(t) = \sum_{s \ge 0} \dim_K (S/I)_s \, t^s$ of the dimensions of its graded pieces. The coefficient sequence is the Hilbert function, and it agrees with a polynomial, the Hilbert polynomial, for large $s$. The series is rational, $Q(t)/(1 - t)^n$ with $Q \in \mathbb{Z}[t]$. It encodes the dimension and degree of the projective variety of $I$. By Macaulay's theorem it equals the Hilbert series of the monomial ideal $\langle \operatorname{LT}(I) \rangle$ for any graded monomial order, so a [Gröbner basis](/groebner-basis/) reduces its computation to counting monomials. Conversely, a known Hilbert series speeds up Gröbner basis computations.

## In plain words

Take all the polynomials, and cut them down by an ideal: two polynomials count as equal when their difference lies in the ideal. In each degree, ask how many independent polynomials are left. The answers, one number per degree, form the Hilbert function, and packed into a power series they give the Hilbert series. These numbers tell you how big the solution set of the equations is. A finite set of points gives numbers that settle at a constant, the number of points. A curve gives numbers that grow linearly, and a surface quadratically. You can read the numbers off a Gröbner basis by counting the monomials that no leading term divides.

## The idea

**Setup.** Let $K$ be a field, $S = K[x_1, \ldots, x_n]$ graded by total degree, and $S_s$ the space of homogeneous polynomials of degree $s$, of dimension $\binom{s + n - 1}{n - 1}$. For a homogeneous ideal $I$, $I_s = I \cap S_s$ and $(S/I)_s = S_s / I_s$. Then

$$\mathrm{HF}_{S/I}(s) = \dim_K S_s - \dim_K I_s, \qquad \mathrm{HS}_{S/I}(t) = \sum_{s \ge 0} \mathrm{HF}_{S/I}(s)\, t^s.$$

For a non-homogeneous ideal one uses the *affine* Hilbert function $s \mapsto \dim_K S_{\le s} / I_{\le s}$, or homogenizes first.

**Reduction to monomials (Macaulay).** Fix a graded order, such as grlex or grevlex, and let $\operatorname{LT}$ be the leading term for it. The monomials of degree $s$ not in $\langle \operatorname{LT}(I) \rangle$, the *standard monomials*, map to a basis of $(S/I)_s$. Division by a Gröbner basis shows they span, and they are independent because a nonzero combination of them in $I$ would have its leading term in $\langle \operatorname{LT}(I) \rangle$. So

$$\mathrm{HF}_{S/I} = \mathrm{HF}_{S/\langle \operatorname{LT}(I) \rangle}.$$

**Rationality and the Hilbert polynomial.** For a monomial ideal $J$ and a monomial $m$ of degree $e$, the exact sequence $0 \to S/(J : m)(-e) \to S/J \to S/(J + \langle m \rangle) \to 0$ gives

$$\mathrm{HS}_{S/(J + \langle m \rangle)}(t) = \mathrm{HS}_{S/J}(t) - t^{e}\, \mathrm{HS}_{S/(J : m)}(t).$$

Adding the generators of $J$ one at a time, starting from $\mathrm{HS}_S = 1/(1 - t)^n$, shows that $\mathrm{HS}_{S/J} = Q(t)/(1 - t)^n$ with $Q \in \mathbb{Z}[t]$. This recursion, with good pivot choices, is the algorithm of Bayer and Stillman (1992). After cancelling factors $1 - t$, $\mathrm{HS} = h(t)/(1 - t)^{D}$ with $h(1) \ne 0$. Then $\mathrm{HF}(s)$ equals a polynomial $\mathrm{HP}(s)$ of degree $D - 1$ for all large $s$. Here $D$ is the Krull dimension of $S/I$, $D - 1$ is the dimension of the projective variety $V(I) \subseteq \mathbb{P}^{n-1}$, and $h(1)$ is its degree. The leading term of $\mathrm{HP}$ is $\frac{h(1)}{(D - 1)!} s^{D - 1}$.

**Zero-dimensional affine case.** If $V(I) \subseteq \overline{K}^n$ is finite, the affine Hilbert function is eventually constant, and the constant is $\dim_K K[x]/I$, the number of solutions counted with multiplicity: the number of standard monomials of any Gröbner basis.

## Examples

**The polynomial ring.** $\mathrm{HS}_S = 1/(1 - t)^n$ and $\mathrm{HF}_S(s) = \binom{s + n - 1}{n - 1}$.

**A monomial ideal with an embedded point.** For $I = \langle x^2, xy \rangle$ in $K[x, y]$, the standard monomials are $1$; $x, y$; and $y^s$ in each degree $s \ge 2$. So $\mathrm{HF} = 1, 2, 1, 1, 1, \ldots$ and

$$\mathrm{HS} = 1 + 2t + \frac{t^2}{1 - t} = \frac{1 + t - t^2}{1 - t}.$$

The Hilbert polynomial is $1$: $V(I)$ is the single point $[0 : 1]$ of $\mathbb{P}^1$. The embedded component at the origin shows up only in low degrees.

**A complete intersection.** If $f_1, \ldots, f_r$ is a homogeneous regular sequence of degrees $d_1, \ldots, d_r$, then

$$\mathrm{HS}_{S/\langle f_1, \ldots, f_r \rangle}(t) = \frac{\prod_{i=1}^{r} (1 - t^{d_i})}{(1 - t)^n}.$$

For a plane curve $f$ of degree $d$ in $K[x, y, z]$, this gives $\mathrm{HF}(s) = \binom{s + 2}{2} - \binom{s - d + 2}{2} = ds - \frac{d(d - 3)}{2}$ for $s \ge d - 2$. Writing $\mathrm{HP}(s) = ds + 1 - g$ gives the genus $g = \frac{(d - 1)(d - 2)}{2}$ of a smooth plane curve. For a cubic, $\mathrm{HF} = 1, 3, 6, 9, 12, \ldots$.

**The twisted cubic.** For $I = \langle xz - y^2, xw - yz, yw - z^2 \rangle$ in $K[x, y, z, w]$, the leading terms of the grevlex Gröbner basis are $y^2$, $yz$ and $z^2$. Counting standard monomials gives $\mathrm{HF}(s) = 3s + 1$, that is $1, 4, 7, 10, 13, \ldots$, and $\mathrm{HS} = (1 + 2t)/(1 - t)^2$. So $V(I)$ is a curve ($D - 1 = 1$) of degree $h(1) = 3$.

## Where it is used

- **Dimension and degree.** The Hilbert polynomial computes the dimension and degree of a variety from one Gröbner basis (CLO, Chapter 9).
- **Hilbert-driven Gröbner bases.** If the Hilbert series of $S/I$ is known, for instance from a basis under another order, a Buchberger-type algorithm can stop processing a degree once the dimension count matches. This is Traverso's Hilbert-driven algorithm (CLO, Chapter 10, Section 2), used in [Gröbner basis conversion](/groebner-basis-conversion/).
- **Complexity of F5 and F4.** For a regular or semi-regular sequence, the Hilbert series is the series above (truncated at its first nonpositive coefficient for semi-regular sequences), and its first degree with a nonpositive coefficient, the degree of regularity, bounds the degrees reached by [F5](/f5-algorithm/) and the size of the [Macaulay matrices](/macaulay-matrix/) it reduces. Algebraic cryptanalysis estimates attack costs this way.
- **Counting solutions.** In the zero-dimensional case, the number of standard monomials is the number of solutions with multiplicity, used in [polynomial system solving](/polynomial-system-solving/).
- **Combinatorics and invariant theory.** The Hilbert series of a Stanley-Reisner ring encodes the face numbers of a simplicial complex. The Hilbert series of a ring of invariants of a finite group is given by Molien's formula, and guides the search for generators.

## References
