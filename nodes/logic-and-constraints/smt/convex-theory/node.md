---
tag: 8VM2TR
kind: definition
slug: convex-theory
name: Convex theory
aliases:
- convexity
- convex first-order theory
area: logic-and-constraints/smt
level: advanced
summary: A theory in which a set of literals that entails a disjunction of equalities between constants already entails one of them. In combination, convex theories only need to exchange single equalities.
prereqs: [smt-problem]
see_also: [nelson-oppen, stable-infiniteness, shostak-combination, model-based-theory-combination, linear-real-arithmetic-satisfiability, linear-integer-arithmetic-satisfiability, euf-satisfiability, array-theory-satisfiability]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.2.1.2 (the definition of a convex theory), Section 33.4.1 (deduction of interface equalities, single or disjunctive), Section 33.6.2 (the Nelson-Oppen procedure for convex and non-convex theories)
  - paper: doi:10.1016/0304-3975(80)90059-6
    title: Derek C. Oppen, Complexity, convexity and combinations of theories, Theoretical Computer Science 12(3), 1980, pages 291 to 302
    locator: convex theories, the deterministic combination for convex theories, and the complexity of combinations
  - paper: doi:10.1145/357073.357079
    title: Greg Nelson and Derek C. Oppen, Simplification by cooperating decision procedures, ACM Transactions on Programming Languages and Systems 1(2), 1979, pages 245 to 257
    locator: the combination procedure with case splits on disjunctions of equalities for non-convex theories
  - paper: doi:10.1007/3-540-45988-x_11
    title: Clark W. Barrett, David L. Dill and Aaron Stump, A generalization of Shostak's method for combining decision procedures, FroCoS 2002, LNAI 2309, pages 132 to 146
    locator: a convex theory with no trivial models is stably infinite
  - paper: doi:10.1007/978-3-540-74113-8_10
    title: Aaron R. Bradley and Zohar Manna, Combining decision procedures, Chapter 10 of The Calculus of Computation, Springer, 2007, pages 269 to 289
    locator: convex and non-convex theories in the Nelson-Oppen method, with the integer example
---

A theory is convex when it never entails a disjunction of equalities between constants without entailing one of the disjuncts. In a convex theory, if a set of facts forces "$x = y$ or $u = v$", then it forces $x = y$ or it forces $u = v$; it can never leave the choice open. The property matters for theory combination. In the [Nelson-Oppen](/nelson-oppen/) method, the solvers of convex theories only need to tell each other single equalities between shared variables, and the method is deterministic and polynomial on top of the solvers. For a non-convex theory, a solver must also report disjunctions of equalities, and the method has to split cases. Oppen introduced the notion in 1980. Equality with uninterpreted functions and linear real arithmetic are convex; linear integer arithmetic, arrays and bit-vectors are not.

## Definition

Let $T$ be a $\Sigma$-theory. $T$ is **convex** if for every set $\mu$ of ground literals over $\Sigma'$, where $\Sigma'$ extends $\Sigma$ with fresh constants, and for every finite non-empty set $E$ of equalities between constants of $\Sigma'$,

$$\mu \models_T \bigvee_{e \in E} e \quad\text{if and only if}\quad \mu \models_T e \text{ for some } e \in E.$$

The direction from right to left always holds, so the content is the direction from left to right (Handbook, Section 33.2.1.2).

Remarks on the definition.

- If $\mu$ is $T$-unsatisfiable, it entails every equality, so the condition holds. Only satisfiable $\mu$ can break it.
- The disjuncts are equalities between *constants*, that is, between the shared variables of a combination. Disjunctions of other literals are not part of the definition.
- The word comes from geometry. For linear real arithmetic, the solution set of a set of linear constraints is a convex set, and a convex set that lies in a finite union of hyperplanes lies in one of them.

**Convex theories in combination.** In the deterministic [Nelson-Oppen](/nelson-oppen/) procedure, each solver reports the equalities between shared variables that its part of the formula entails, and the other solver adds them. For convex theories this is complete: if no single entailed equality is left to send and both parts are satisfiable, then the formula is satisfiable. For a non-convex theory, the solver must report each entailed disjunction of equalities, and the procedure must try each disjunct, which makes the search exponential in the number of shared variables in the worst case.

**Theorem (Barrett, Dill and Stump).** If $T$ is convex and has no model with exactly one element, then $T$ is [stably infinite](/stable-infiniteness/).

*Proof.* It is enough to treat a $T$-satisfiable conjunction of ground literals $\mu$, because a ground formula is satisfiable exactly when one disjunct of its disjunctive normal form is. Suppose $\mu$ has no infinite $T$-model. Take fresh constants $c_1, c_2, \ldots$. The set $T \cup \mu \cup \{c_i \ne c_j : i < j\}$ has no model, since a model would be infinite. By compactness, a finite part of it has no model, so for some $n$ the set $T \cup \mu \cup \{c_i \ne c_j : 1 \le i < j \le n\}$ has no model. If $n \le 1$, the disequalities are absent and $\mu$ itself is unsatisfiable, which is false. So $n \ge 2$ and $\mu \models_T \bigvee_{i < j \le n} c_i = c_j$. By convexity, $\mu \models_T c_i = c_j$ for one pair. The constants $c_i$ and $c_j$ do not occur in $\mu$, so in any $T$-model $M$ of $\mu$ they can be given any two elements $d$ and $e$ of $M$, and $M$ stays a model of $\mu$. Thus $d = e$ for all $d, e$, and $M$ has one element, which the hypothesis excludes. $\square$

## Examples and non-examples

- **Horn theories are convex.** Suppose all axioms of $T$ are universal Horn clauses, with at most one positive literal each. The models of such a theory are closed under direct products. Let $\mu$ be satisfiable and $\mu \not\models_T e$ for each $e \in E$, and take for each $e$ a model $M_e$ of $\mu$ in which $e$ is false. In the product $\prod_e M_e$, a positive ground literal is true when it is true in every factor, and a negative one is true when it is true in some factor. So the product satisfies $\mu$, and each $e \in E$ is false in it, because it is false in one factor. Thus $\mu \not\models_T \bigvee E$.
- **EUF is convex.** The axioms of equality and the congruence axioms are Horn clauses, so the previous point applies. This is why the EUF solver in a combination only sends single equalities, read off its congruence classes.
- **Linear real arithmetic is convex.** Let $K$ be the set of solutions of the equalities and inequalities of $\mu$. It is convex. The disequalities remove finitely many hyperplanes. If they remove all of $K$, $\mu$ is unsatisfiable. Otherwise the remaining set is dense in $K$, relative to the affine hull of $K$. If it lies in the union of the hyperplanes $x = y$ for $(x = y) \in E$, then one of these hyperplanes contains the whole affine hull of $K$, because a convex set of dimension $d$ cannot be covered by finitely many affine subspaces of smaller dimension. So $\mu$ entails that one equality.
- **Linear integer arithmetic is not convex.** Let $\mu = \{1 \le x,\ x \le 2,\ y = 1,\ z = 2\}$. Every integer solution has $x = 1$ or $x = 2$, so $\mu \models x = y \vee x = z$. But $x = 1$ is a solution with $x \ne z$, and $x = 2$ is a solution with $x \ne y$, so neither equality is entailed. Over the reals the same $\mu$ allows $x = 1.5$, and it entails neither the disjunction nor the equalities.
- **Arrays are not convex.** Let $\mu = \{\mathrm{read}(\mathrm{write}(a, i, v), j) = w,\ \mathrm{read}(a, j) = u\}$. If $i = j$ then $w = v$, and otherwise $w = \mathrm{read}(a, j) = u$, so $\mu \models w = v \vee w = u$. A model with $i = j$ and $v \ne u$ has $w \ne u$, and a model with $i \ne j$ and $v \ne u$ has $w \ne v$.
- **Bit-vectors and other finite domains are not convex.** For bit-vectors of width 1 and $\mu$ empty, $\models x = y \vee x = z \vee y = z$, because there are only two values, but no single equality is valid. In general, a theory whose models all have at most $k$ elements, and some of which have at least two, is not convex: $k + 1$ constants must have two equal.

## Related definitions

- [Stable infiniteness](/stable-infiniteness/): the condition for the completeness of [Nelson-Oppen](/nelson-oppen/). By the theorem above, convexity together with the absence of one-element models implies it.
- [Nelson-Oppen](/nelson-oppen/): deterministic equality propagation for convex theories, case splits for non-convex ones. [Model-based theory combination](/model-based-theory-combination/) avoids the computation of entailed disjunctions in the non-convex case by guessing equalities from models.
- [Shostak's method](/shostak-combination/): the Handbook (Section 33.5) states that its basic algorithm for a theory with a canonizer and a solver is sound and complete when the theory is convex, or when the input has at most one disequality.
- **Interface equalities:** the equalities $x_i = x_j$ between shared variables that the solvers exchange. Their deduction, single or disjunctive, is listed in the Handbook among the features of theory solvers.

## References
