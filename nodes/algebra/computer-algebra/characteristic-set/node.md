---
tag: DKT972
kind: concept
slug: characteristic-set
name: Characteristic set
aliases:
- Ritt-Wu characteristic set
- Wu characteristic set
- ascending chain of lowest rank
area: algebra/computer-algebra
level: advanced
summary: A triangular set of polynomials that determines the zeros of a polynomial system generically.
prereqs: [pseudo-division, polynomial-ideal]
see_also: [wu-characteristic-set-method, triangular-decomposition, regular-chain, groebner-basis, resultant, polynomial-system-solving, primary-decomposition]
sources:
  - paper: "Joseph Fels Ritt, Differential Algebra, American Mathematical Society Colloquium Publications 33, 1950"
    locator: Chapter I and Chapter IV (ascending sets, their ranks, characteristic sets of algebraic ideals and the reduction of a polynomial by an ascending set)
  - paper: "Wu Wen-tsün, On the decision problem and the mechanization of theorem-proving in elementary geometry, Scientia Sinica 21, 159-172, 1978"
    locator: the zero structure theorem and its use for proving geometry theorems
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 6, Section 4 (automatic geometric theorem proving) and Section 5 (Wu's method, pseudo-division by a triangular set and the characteristic set)
  - book: isbn:9783211832417
    title: Dongming Wang, Elimination Methods, Springer, 2001
    locator: Chapter 2 (characteristic sets, the Ritt-Wu algorithm and the zero decomposition theorems)
---

A characteristic set of a set $P$ of polynomials in $K[x_1, \ldots, x_n]$ is a triangular system $C = (f_1, \ldots, f_r)$, each polynomial introducing one new variable, such that every element of $P$ pseudo-reduces to zero by $C$ and $C$ lies in the ideal of $P$. It describes the zeros of $P$ outside the hypersurface where the leading coefficients of $C$ vanish. The notion is due to Ritt (1950), who used it in differential algebra; Wu Wen-tsün (1978) turned it into a practical method for solving systems and proving geometry theorems. A characteristic set is the triangular counterpart of a [Gröbner basis](/groebner-basis/): cheaper to obtain in many cases and closer to back substitution, but it captures the zeros only generically, not the ideal.

## In plain words

A system of polynomial equations is easy to solve when it is triangular: the first equation has only the first unknown, the second adds one more unknown, and so on. Then one solves the first equation, puts its roots into the second, and continues.

A characteristic set rewrites a system into this triangular shape. The price is that a few special cases can be lost along the way: the method divides by some expressions, so the places where those expressions are zero must be checked on the side. For most inputs those special cases are small, and the triangular form describes the solutions well.

## The idea

**Setting.** Let $K$ be a field and fix the variable order $x_1 < x_2 < \cdots < x_n$. This is an order on variables, not a monomial order; it plays the role that the lex order $x_n > \cdots > x_1$ plays for Gröbner bases. For a nonconstant $f \in K[x_1, \ldots, x_n]$:

- the *class* $\operatorname{cls}(f)$ is the largest $i$ such that $x_i$ occurs in $f$, and $x_i$ is the *leading variable*;
- the *leading degree* is $\deg_{x_i} f$;
- the *initial* $\operatorname{init}(f)$ is the coefficient of the highest power of $x_i$, a polynomial in $x_1, \ldots, x_{i-1}$.

Constants have class 0. A polynomial $g$ is *reduced* with respect to $f$ of class $i$ if $\deg_{x_i} g < \deg_{x_i} f$.

**Ascending chains.** An *ascending chain* is either a single nonzero constant or a sequence $C = (f_1, \ldots, f_r)$ with $0 < \operatorname{cls}(f_1) < \cdots < \operatorname{cls}(f_r)$ in which every $f_j$ is reduced with respect to every earlier $f_i$. (Wu's weaker *triangular set* asks only for increasing classes.) Polynomials are ranked first by class and then by leading degree, and chains are compared lexicographically by the ranks of their elements, with a longer chain ranked lower when one is a prefix of the other. The key fact is that this order on chains is well founded: every strictly decreasing sequence of chains is finite.

**Pseudo-remainder by a chain.** For a polynomial $g$, pseudo-divide by $f_r$ in its leading variable, then the remainder by $f_{r-1}$, and so on down to $f_1$ (see [pseudo-division](/pseudo-division/)). The result $\operatorname{prem}(g, C)$ is reduced with respect to every $f_i$ and satisfies

$$I_1^{s_1} \cdots I_r^{s_r} \, g = \sum_{i=1}^{r} q_i f_i + \operatorname{prem}(g, C), \qquad I_i = \operatorname{init}(f_i),$$

for some exponents $s_i \ge 0$ and polynomials $q_i$.

**Characteristic sets.** Ritt's characteristic set of a set or ideal $P$ is an ascending chain of lowest rank among the chains contained in $P$. Wu's characteristic set of a finite set $P$ is an ascending chain $C$ contained in the ideal $\langle P \rangle$ with $\operatorname{prem}(p, C) = 0$ for every $p \in P$. The Ritt-Wu process computes the second kind:

1. Let $Q = P$. Choose a *basic set* $B$ of $Q$: an ascending chain of lowest rank among the chains whose elements belong to $Q$.
2. Compute $R = \{\operatorname{prem}(q, B) : q \in Q \setminus B\} \setminus \{0\}$.
3. If $R$ is empty, return $B$. Otherwise set $Q = Q \cup R$ and go back to step 1.

Every element of $R$ is nonzero and reduced with respect to $B$, so the basic set of $Q \cup R$ has strictly lower rank than $B$. By the well-foundedness of ranks the process stops. If it returns a nonzero constant, $P$ has no zeros over the algebraic closure of $K$.

**Zero structure.** Write $\operatorname{Zero}(P)$ for the common zeros of $P$ over the algebraic closure of $K$, $J = I_1 \cdots I_r$ for the product of the initials, and $\operatorname{Zero}(C / J)$ for the zeros of $C$ at which $J \ne 0$. For a Wu characteristic set $C$ of $P$,

$$\operatorname{Zero}(C / J) \subseteq \operatorname{Zero}(P) \subseteq \operatorname{Zero}(C), \qquad \operatorname{Zero}(P) = \operatorname{Zero}(C / J) \cup \bigcup_{i=1}^{r} \operatorname{Zero}(P \cup \{I_i\}).$$

The second inclusion holds because $C \subseteq \langle P \rangle$. The first follows from the pseudo-remainder identity with remainder 0: at a zero of $C$ where $J \ne 0$, the right side is 0 and the left side is a nonzero product of powers of the initials times $p$, so $p = 0$. The decomposition follows by splitting $\operatorname{Zero}(P)$ into the points where $J \ne 0$ and the points where some $I_i = 0$. Applying the process again to each $P \cup \{I_i\}$, which has lower-dimensional zeros, gives Wu's decomposition of $\operatorname{Zero}(P)$ into finitely many quasi-varieties $\operatorname{Zero}(C_k / J_k)$; see [Wu's method](/wu-characteristic-set-method/) and [triangular decomposition](/triangular-decomposition/).

**What it does not give.** $\operatorname{prem}(g, C) = 0$ does not imply $g \in \langle P \rangle$; it implies only that $g$ vanishes on $\operatorname{Zero}(C / J)$. For Ritt's characteristic set of a *prime* ideal $\mathfrak{p}$, membership is exact: $g \in \mathfrak{p}$ if and only if $\operatorname{prem}(g, C) = 0$. For a general ideal, exact membership needs a Gröbner basis or a decomposition into [regular chains](/regular-chain/) with saturated ideals.

**Cost.** The cost is measured in operations in $K$. The Ritt-Wu process has no good bound in its plain form. Gallo and Mishra (1991) gave a variant whose output degrees are bounded by a single exponential function of $n$, of the form $d^{O(n^2)}$ for input degree $d$; in practice the main costs are the growth of the pseudo-remainders and the branching on initials. This is a single-exponential bound, in contrast to the doubly exponential worst case of Gröbner bases (Mayr and Meyer 1982), but the two objects carry different information.

## Examples

Both examples use two variables with $x < y$, so $y$ is the leading variable of any polynomial that contains it. The pseudo-remainders were checked by a script in exact integer arithmetic.

**A system with no degenerate part.** Let $P = \{x^2 + y^2 - 1,\ xy - 1\}$. Both polynomials have class 2. The basic set is $B = (xy - 1)$, of leading degree 1, with initial $x$. Pseudo-dividing $y^2 + x^2 - 1$ by $xy - 1$ in $y$ multiplies by $x^2$ and gives

$$\operatorname{prem}(x^2 + y^2 - 1,\ xy - 1) = x^4 - x^2 + 1 .$$

Adding it to $Q$, the basic set becomes $(x^4 - x^2 + 1,\ xy - 1)$, which has lower rank, and both elements of $P$ now pseudo-reduce to 0. So $C = (x^4 - x^2 + 1,\ xy - 1)$ is a characteristic set. Its initials are $1$ and $x$. Since $P \cup \{x\}$ contains $x$ and $xy - 1$, it has no zeros, and $\operatorname{Zero}(P) = \operatorname{Zero}(C / x)$: four points, one for each root $x$ of $x^4 - x^2 + 1$, with $y = 1/x$.

**A system with a degenerate component.** Let $P = \{xy - x,\ y^2 - 1\}$. The basic set is $B = (xy - x)$ with initial $x$, and

$$\operatorname{prem}(y^2 - 1,\ xy - x) = 0,$$

because $x^2 (y^2 - 1) = (xy - x)(xy + x)$. So $C = (xy - x)$ is a characteristic set. The quasi-variety $\operatorname{Zero}(C / x)$ is the line $y = 1$ without the point $x = 0$. The rest of the zeros is $\operatorname{Zero}(P \cup \{x\}) = \operatorname{Zero}(x,\ y^2 - 1) = \{(0, 1), (0, -1)\}$, with characteristic set $(x,\ y^2 - 1)$. So

$$\operatorname{Zero}(P) = \operatorname{Zero}((xy - x)/x) \cup \operatorname{Zero}(x,\ y^2 - 1).$$

The same example shows the limit on membership. The polynomial $g = y - 1$ has $\operatorname{prem}(y - 1,\ xy - x) = x(y - 1) - (xy - x) = 0$, yet $g \notin \langle P \rangle$, since $g(0, -1) = -2$ while every element of $\langle P \rangle$ vanishes at $(0, -1)$.

**Geometry theorems.** In Wu's method, the hypotheses of a theorem of plane geometry are written as polynomials in coordinates, ordered so that free parameters come first. The conclusion $g$ is proved, for all configurations in which the initials do not vanish, when $\operatorname{prem}(g, C) = 0$. The initials that appear are the *nondegeneracy conditions*, such as "the three points are not collinear". Cox, Little and O'Shea work through the theorem that the diagonals of a parallelogram bisect each other in this way.

## Where it is used

- **Mechanical theorem proving** in elementary and differential geometry, where Wu's method proved hundreds of theorems in the 1980s; see [Wu's method](/wu-characteristic-set-method/).
- **Solving polynomial systems** by decomposition into triangular sets, then back substitution or [real root isolation](/real-root-isolation/) one variable at a time; see [triangular decomposition](/triangular-decomposition/) and [polynomial system solving](/polynomial-system-solving/).
- **Regular chains**, the modern refinement, add a regularity condition on the initials so that the decomposition is unmixed and membership in the saturated ideal can be tested by pseudo-reduction; see [regular chain](/regular-chain/).
- **Differential algebra**, Ritt's original setting, where characteristic sets of differential ideals give the Rosenfeld-Gröbner algorithm and the elimination theory of systems of algebraic differential equations.

## References
