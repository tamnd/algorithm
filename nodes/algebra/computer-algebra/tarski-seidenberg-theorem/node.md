---
tag: R34B36
kind: theorem
slug: tarski-seidenberg-theorem
name: Tarski-Seidenberg theorem
aliases: [Tarski's theorem on real quantifier elimination, Tarski-Seidenberg principle, projection theorem for semialgebraic sets, transfer principle for real closed fields]
area: algebra/computer-algebra
level: advanced
summary: Projections of semialgebraic sets are semialgebraic, so real quantifier elimination is possible.
prereqs: [semialgebraic-set, real-closed-field, pseudo-division]
see_also: [quantifier-elimination, cylindrical-algebraic-decomposition, tarski-decidability-theorem, sturm-theorem, hilbert-nullstellensatz, elimination-theorem, presburger-arithmetic]
sources:
  - paper: "Alfred Tarski, A Decision Method for Elementary Algebra and Geometry, RAND Corporation, 1948; second edition, University of California Press, 1951"
    locator: the elimination theorem for real closed fields and the decision method
  - paper: doi:10.2307/1969640
    title: Abraham Seidenberg, A new decision method for elementary algebra, Annals of Mathematics 60(2), 1954
    locator: pp. 365 to 374
  - paper: doi:10.1002/cpa.3160220202
    title: Paul J. Cohen, Decision procedures for real and p-adic fields, Communications on Pure and Applied Mathematics 22(2), 1969
    locator: pp. 131 to 151 (the elimination by sign tables on which the proof here is based)
  - book: isbn:9783540646631
    title: Jacek Bochnak, Michel Coste and Marie-Françoise Roy, Real Algebraic Geometry, Springer, 1998
    locator: Chapter 1, Ordered Fields, Real Closed Fields, and Chapter 2, Semi-algebraic Sets (the Tarski-Seidenberg principle and its consequences)
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 2, Real Closed Fields (the Tarski-Seidenberg principle, proved with Thom encodings and sign tables) and Chapter 14, Quantifier Elimination
  - paper: doi:10.1016/S0747-7171(88)80004-X
    title: James H. Davenport and Joos Heintz, Real quantifier elimination is doubly exponential, Journal of Symbolic Computation 5(1-2), 1988
    locator: pp. 29 to 35
---

## Statement

Let $R$ be a [real closed field](/real-closed-field/) and $\pi : R^{k+1} \to R^k$ the projection that forgets the last coordinate.

**Theorem (Tarski-Seidenberg).** If $S \subseteq R^{k+1}$ is [semialgebraic](/semialgebraic-set/), then $\pi(S) \subseteq R^k$ is semialgebraic. If $S$ is defined by polynomials with coefficients in a subring $D \subseteq R$, then $\pi(S)$ is defined by polynomials with coefficients in $D$, by a description that does not depend on $R$.

**Equivalent form (quantifier elimination).** Every first-order formula $\Phi(y_1, \ldots, y_k)$ in the language of ordered fields, with coefficients in $D$, is equivalent in every real closed field containing $D$ to a quantifier-free formula with coefficients in $D$.

**Transfer principle.** If $R \subseteq R'$ are real closed fields, a first-order sentence with coefficients in $R$ holds in $R$ exactly when it holds in $R'$.

## In plain words

Take a shape in space that is described by polynomial equations and inequalities, and look at its shadow on a lower-dimensional space. The theorem says that the shadow can also be described by polynomial equations and inequalities, with no "there exists" in the description. The shadow of a circle on a line is a closed interval, for example.

In the language of logic, this says that every statement about real numbers built from polynomials, "and", "or", "not", "there is" and "for all" can be rewritten without "there is" and "for all". The rewriting uses only the same kind of numbers as the input. So the truth of a statement without free variables is the same in all real closed fields, and it can be decided.

## Proof

The proof is the sign table method of Cohen and Hörmander. It uses only the intermediate value property and the mean value theorem for polynomials, which hold in every real closed field, and [pseudo-division](/pseudo-division/).

**Reduction to one quantifier and sign conditions.** A formula is built from atoms, connectives and quantifiers, and $\forall x \, \phi \Leftrightarrow \neg \exists x \, \neg \phi$. By induction on the formula, it is enough to remove one $\exists x$ in front of a quantifier-free $\phi(y, x)$. Let $P_1, \ldots, P_s \in D[y][x]$ be the polynomials in the atoms of $\phi$. Whether $\phi(y, x)$ holds depends only on the sign vector $(\operatorname{sign} P_1(y, x), \ldots, \operatorname{sign} P_s(y, x)) \in \{-1, 0, 1\}^s$. So $\exists x \, \phi$ is the finite disjunction, over the sign vectors $\sigma$ that make $\phi$ true, of $\exists x \, (\operatorname{sign} P(y, x) = \sigma)$. The theorem follows from the lemma below, because the set of $y$ where $\sigma$ occurs in the sign table is a union of fibers of the table.

**Sign tables.** For a list $L = (P_1, \ldots, P_s)$ in $D[y][x]$ and a point $y \in R^k$, let $\xi_1 < \cdots < \xi_N$ be the roots in $R$ of those $P_i(y, x)$ that are not the zero polynomial in $x$. The *sign table* $T_L(y)$ is the sequence of the sign vectors of $L$ on $(-\infty, \xi_1)$, at $\xi_1$, on $(\xi_1, \xi_2)$, and so on to $(\xi_N, \infty)$. On each open interval every $P_i(y, \cdot)$ has no root, so by the intermediate value property it has a constant sign, and the table is well defined. Some $x$ has the sign vector $\sigma$ exactly when $\sigma$ occurs in $T_L(y)$.

**Lemma.** For every finite list $L$ in $D[y][x]$, the map $y \mapsto T_L(y)$ takes finitely many values, and each fiber $\{y : T_L(y) = T\}$ is a semialgebraic subset of $R^k$ defined by sign conditions on polynomials in $D[y]$ that depend only on $L$.

*Proof.* **Step 1: fixed degrees.** Write $P_i = \sum_j c_{ij}(y) x^j$. Split $R^k$ by the signs of all the coefficients $c_{ij}(y)$; there are finitely many pieces, each defined by sign conditions on polynomials in $D[y]$. On a piece, each $P_i$ is either the zero polynomial in $x$ for all $y$, and it can be dropped, or it equals its truncation $\tilde P_i$ at the highest $j$ with $c_{ij} \ne 0$ on the piece, whose leading coefficient has a fixed nonzero sign. It is enough to prove the lemma on each piece for the truncated list. We now argue by induction on the multiset of the degrees in $x$ of the truncated list, ordered as multisets. This order is well founded.

**Step 2: the base.** If every member has degree $0$ in $x$, the table has one entry, the signs of the polynomials $c_{i0}(y)$, and its fibers are sign conditions on these.

**Step 3: the induction step.** Let $P$ be a member of largest degree $d \ge 1$, with leading coefficient $c(y)$ of fixed sign $\varepsilon$. Form the list $L'$ from $L$ by removing $P$ and adding $P' = \partial P / \partial x$, the pseudo-remainder $\operatorname{prem}(P, P')$, and $\operatorname{prem}(P, Q)$ for every other member $Q$ of positive degree. $P'$ has degree $d - 1$ with leading coefficient $d \cdot c(y) \ne 0$, because the characteristic is $0$, and every pseudo-remainder has degree less than the degree of its divisor, which is at most $d$. So $L'$ is smaller in the multiset order, and by induction $T_{L'}$ has finitely many values with semialgebraic fibers. We show that $T_L(y)$ is a function of $T_{L'}(y)$ on the piece. Then each fiber of $T_L$ is a finite union of fibers of $T_{L'}$, and the lemma follows.

Fix $y$ and read off $T_{L'}(y)$. Call a point of this table *relevant* if it is a root of $P'$ or of a member $Q \ne P$ of $L$; whether it is relevant can be seen in the table, from the zeros in its sign vector.

- *The sign of $P$ at a relevant point $\eta$.* If $Q(\eta) = 0$ for a member $Q$ with leading coefficient $b(y)$ and $e = d - \deg Q + 1$, then $b^e P = A Q + \operatorname{prem}(P, Q)$ gives $b(y)^e P(\eta) = \operatorname{prem}(P, Q)(\eta)$. The sign of $b(y)$ is fixed on the piece, and the sign of the right side is in the table. The same holds for $Q = P'$.
- *The sign of $P$ near $\pm\infty$.* For $|x|$ large, $P$ has the sign of its leading term: $\varepsilon$ near $+\infty$ and $(-1)^d \varepsilon$ near $-\infty$.
- *The roots of $P$.* Between two consecutive relevant points, and before the first and after the last, $P'$ has no root, so it has a constant nonzero sign there, and by the mean value theorem $P$ is strictly monotone there. So $P$ has at most one root in each such open interval, and it has one exactly when its signs at the two ends are opposite and nonzero, by the intermediate value property. If $P$ is $0$ at a relevant point, that point is a root of $P$.
- *The other members.* Each other $Q \in L$ has its roots among the relevant points, so its sign is constant on each open interval between relevant points and is given by $T_{L'}(y)$; its sign at a relevant point is also in $T_{L'}(y)$.

These four facts give the roots of all members of $L$ in their order, and the signs of all members at the roots and between them. That is $T_L(y)$, and it is computed from $T_{L'}(y)$ and the fixed signs of the leading coefficients only. $\square$

**End of the proof.** By the reduction, $\{y : \exists x \, \phi(y, x)\}$ is the union of the fibers $\{y : T_L(y) = T\}$, over the finitely many tables $T$ in which some sign vector satisfying $\phi$ occurs. By the lemma this set is defined by sign conditions on polynomials in $D[y]$, and the construction of $L'$ uses only ring operations in $D[y]$, so the description depends on $L$ and not on $R$. Projection of a semialgebraic set $S = \{(y, x) : \phi(y, x)\}$ is $\{y : \exists x \, \phi(y, x)\}$, which proves the first form. Induction on the quantifiers proves the second.

**The transfer principle.** Let $\Phi$ be a sentence with coefficients in $R$. By quantifier elimination with $D = R$, $\Phi$ is equivalent, in both $R$ and $R'$, to the same quantifier-free sentence $\Psi$, a Boolean combination of sign conditions on elements of $R$. The order of $R'$ extends the order of $R$: in both fields the nonnegative elements are the squares, a square in $R$ is a square in $R'$, and if $a < 0$ in $R$ were a square $c^2$ in $R'$, then with $-a = b^2$ in $R$ we would get $-1 = (c/b)^2$ in $R'$, which is not possible in a real field. So $\Psi$ has the same truth value in $R$ and $R'$, and so does $\Phi$. $\blacksquare$

## Consequences

- **Decidability.** For sentences with integer coefficients, $\Psi$ is a Boolean combination of sign conditions on integers, which can be evaluated. So the first-order theory of $\mathbb{R}$ as an ordered field is decidable, and it is the same as the theory of every real closed field. This is the [Tarski decidability theorem](/tarski-decidability-theorem/), and the algorithms are the subject of [quantifier elimination](/quantifier-elimination/).
- **Closure properties.** Images of semialgebraic sets under semialgebraic maps, closures, interiors, boundaries, and sets defined by any first-order formula are semialgebraic. For example, the set of polynomials of degree $d$ with exactly $r$ real roots is a semialgebraic subset of the coefficient space.
- **Proofs over $\mathbb{R}$ apply everywhere.** A statement proved for $\mathbb{R}$ with analysis transfers to $\mathbb{R}_{\text{alg}}$, to fields of Puiseux series and to every real closed field, if it can be written as a first-order sentence. Artin's solution of Hilbert's 17th problem and the infinitesimal perturbations of real algebraic algorithms use this.
- **Cylindrical algebraic decomposition.** The lemma is a first form of a cylindrical decomposition: over each fiber of $T_L$ the roots of $L$ come in a fixed number and order. [Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) makes this effective with a smaller projection, and it adds the condition that each fiber be connected.

## Tightness

- **Inequalities are needed.** Real algebraic sets are not closed under projection: the projection of $\{x^2 + y^2 = 1\}$ to the $y$-axis is $[-1, 1]$, which is not the zero set of any family of polynomials. The semialgebraic sets are the smallest class that contains the real algebraic sets and is closed under Boolean operations and projections: the projection of $\{y = x^2\}$ already gives $\{y \ge 0\}$.
- **Real closedness is needed.** Over $\mathbb{Q}$, $\exists x \, (x^2 = y)$ defines the set of rational squares. A quantifier-free formula in one variable over $\mathbb{Q}$ defines a finite union of points and of intervals intersected with $\mathbb{Q}$, while the squares are a dense subset of $[0, \infty) \cap \mathbb{Q}$ with dense complement. So no quantifier-free formula is equivalent. The proof fails exactly at the intermediate value property.
- **Integers.** For the ring $\mathbb{Z}$, the theory is undecidable by [Hilbert's tenth problem](/hilberts-tenth-problem/); with addition only it is [Presburger arithmetic](/presburger-arithmetic/), which admits elimination after divisibility predicates are added.
- **Cost.** The size of $\Psi$ can be doubly exponential in the number of variables: Davenport and Heintz (1988) gave formulas whose quantifier-free equivalents need polynomials of doubly exponential degree. The proof above costs much more, because the list grows at every step of the induction.
- **Algebraically closed fields.** The analogue over $\mathbb{C}$ is Chevalley's theorem: projections of constructible sets are constructible. There inequalities $P > 0$ do not exist, and inequations $P \ne 0$ suffice.

## History

Tarski found the elimination method around 1930 and announced it in 1931, but the full proof appeared only in the RAND report of 1948 and its 1951 edition. Seidenberg (1954) gave an independent and more algebraic proof, and the theorem is named after both. Cohen (1969) gave the short sign-table proof, and Hörmander included a version of it in his book on partial differential operators; the proof above follows this line. Collins (1975) turned the projection into the [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) algorithm, the first one whose cost is elementary, doubly exponential in the number of variables.

## References
