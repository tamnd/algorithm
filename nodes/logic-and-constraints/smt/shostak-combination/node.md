---
tag: 4D6QWA
kind: algorithm
slug: shostak-combination
name: Shostak's combination method
aliases:
- Shostak's method
- Shostak's algorithm
- Shostak's decision procedure
- canonizer and solver method
area: logic-and-constraints/smt
level: research
summary: Decides equalities in a theory with a canonizer and a solver, such as linear arithmetic, together with uninterpreted functions, by keeping one solved form instead of exchanging equalities.
solves: [smt-problem]
model: word-ram
complexity:
  vars: {n: the number of symbols in the input}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1984
  people: [Robert E. Shostak]
  note: Shostak published the method in the Journal of the ACM in 1984. The paper contains serious errors. Rueß and Shankar gave a corrected version with full proofs in 2001.
prereqs: [congruence-closure, nelson-oppen, convex-theory]
see_also: [model-based-theory-combination, euf-satisfiability, linear-real-arithmetic-satisfiability, e-graph, decision-procedure, ackermannization, dpll-t, smt-problem]
sources:
  - paper: doi:10.1145/2422.322411
    title: Robert E. Shostak, Deciding combinations of theories, Journal of the ACM 31(1), 1984, pages 1 to 12
    locator: the canonizer and solver conditions, the procedure for one theory with uninterpreted functions, and the claimed combination of several theories
  - paper: doi:10.1109/LICS.2001.932479
    title: Harald Rueß and Natarajan Shankar, Deconstructing Shostak, 16th Annual IEEE Symposium on Logic in Computer Science (LICS 2001), pages 19 to 28
    locator: the corrected procedure for a Shostak theory with uninterpreted functions, with proofs of termination, soundness and completeness
  - paper: doi:10.1007/3-540-45610-4_1
    title: Natarajan Shankar and Harald Rueß, Combining Shostak theories, Rewriting Techniques and Applications (RTA 2002), LNCS 2378, pages 1 to 18
    locator: a correct combination of several Shostak theories, built on the Nelson-Oppen framework
  - paper: doi:10.1007/978-3-540-45085-6_16
    title: Sava Krstić and Sylvain Conchon, Canonization for disjoint unions of theories, CADE-19, LNCS 2741, 2003, pages 197 to 211
    locator: canonizers combine, but solvers can almost never be combined
  - paper: doi:10.1007/3-540-61511-3_107
    title: David Cyrluk, Patrick Lincoln and Natarajan Shankar, On Shostak's decision procedure for combinations of theories, CADE-13, LNCS 1104, 1996, pages 463 to 477
    locator: an early analysis of the conditions of the method
  - paper: doi:10.1007/3-540-45988-x_11
    title: Clark W. Barrett, David L. Dill and Aaron Stump, A generalization of Shostak's method for combining decision procedures, FroCoS 2002, LNAI 2309, pages 132 to 146
    locator: Shostak's method as a refinement of Nelson-Oppen without purification
  - paper: doi:10.1016/j.entcs.2008.04.080
    title: Sylvain Conchon, Evelyne Contejean, Johannes Kanig and Stéphane Lescuyer, CC(X) - Semantic combination of congruence closure with solvable theories, Electronic Notes in Theoretical Computer Science 198(2), 2008, pages 51 to 69
    locator: congruence closure parameterized by a solvable theory, as used in the Alt-Ergo prover
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.5.1 (Definitions 33.5.1 to 33.5.3, Algorithm S1 in Figure 33.5, Example 33.5.4) and Section 33.5.1.1 (combining Shostak theories)
---

Shostak's method decides conjunctions of equalities and disequalities in a theory that has a *canonizer* and a *solver*, such as linear arithmetic over the rationals, and in the extension of such a theory with uninterpreted function symbols. The canonizer writes each term in a normal form, so that two terms are equal in the theory exactly when their normal forms are identical. The solver turns an equation into explicit substitutions, such as $x = 2y - z$. The method keeps one *solved form*, a set of such substitutions, applies it to every new equation, and solves the result. Equalities between function applications are found by comparing the canonical forms of their arguments. Robert Shostak published the method in 1984. His paper has serious errors: the procedure with uninterpreted functions was incomplete, and his claim that the solvers of two theories can be combined into one is false. Harald Rueß and Natarajan Shankar gave a corrected version with proofs in 2001. Unlike [Nelson-Oppen](/nelson-oppen/), the method does not run separate solvers that exchange equalities. Its correct combination of several theories is built on Nelson-Oppen.

## In plain words

Think of solving equations at school. You take the first equation and write one letter in terms of the others, for example "a = 1 − 3b + 2c". From then on, you replace a by this expression everywhere. You take the next equation, replace the letters you already know, and solve it for another letter.

At the end, every known letter is written in terms of the free ones. Two expressions are equal for sure exactly when they become the same after the replacements and simplification.

The method adds functions that you know nothing about. If two calls such as f(x) and f(y) get the same argument after the replacements, they must give the same result, so you add this as a new equation. If a "not equal" clue becomes "same thing is not equal to itself", the clues are contradictory.

## The problem

**Shostak theories.** Following the Handbook (Definition 33.5.3), a consistent theory $T$ with signature $\Sigma$ is a *Shostak theory* if:

1. $\Sigma$ has no predicate symbols other than equality.
2. There is a computable *canonizer* $\mathrm{canon}$ on $\Sigma$-terms such that $\models_T s = t$ exactly when $\mathrm{canon}(s)$ and $\mathrm{canon}(t)$ are identical.
3. There is a computable *solver* $\mathrm{solve}$ on $\Sigma$-equations. If $\models_T s \ne t$, it returns $\{\bot\}$. Otherwise it returns a set of equations in *solved form*, each with a left side that is a constant occurring nowhere else, that is equivalent to $s = t$ in $T$, up to fresh existentially quantified constants.

Linear arithmetic over $\mathbb{Q}$ with equality only is the standard example. The canonizer collects like terms in a fixed order of the variables, so that $c + 3b - a - 5c$ becomes $-a + 3b - 4c$. The solver solves for one variable. Linear arithmetic with $\le$ is not a Shostak theory, because $\le$ is a predicate; the theory of [linear real arithmetic](/linear-real-arithmetic-satisfiability/) needs other solvers, such as the simplex method.

**The input.** A set $\Gamma$ of equations and a set $\Delta$ of disequations between terms built from the symbols of $T$, free constants, and uninterpreted function symbols. The question is whether $\Gamma \cup \Delta$ is satisfiable in $T$ extended with these function symbols.

## The algorithm

Each application $f(t_1, \ldots, t_n)$ is first replaced by a *name* $u$, a fresh variable, with the *definition* $u \mapsto f(a_1, \ldots, a_n)$, where $a_i$ are the abstracted arguments. Two applications get the same name when their arguments have the same canonical forms. Then the theory sees only variables, and the definitions are used only for congruence. $S(p)$ applies the solved form $S$ to $p$, and $S^*(S)$ applies $S^*$ to each right side of $S$.

```pseudo id=main
SHOSTAK(Γ, Δ)                ▷ Γ: equations, Δ: disequations
L1  replace each application by a name u, record the definitions u ↦ f(a1, ..., an) in D
L2  S ← ∅; Q ← Γ             ▷ S: the solved form; Q: the equations to process
L3  loop
L4      if Q is not empty: take an equation s = t out of Q
L5      else if D has u ↦ f(ā) and v ↦ f(b̄) with canon(S(ā)) ≡ canon(S(b̄)) and canon(S(u)) ≢ canon(S(v)): let s = t be u = v
L6      else: leave the loop
L7      S* ← solve(canon(S(s)) = canon(S(t)))
L8      if S* = {⊥}: return UNSAT
L9      S ← S*(S) ∪ S*
L10 if canon(S(s)) ≡ canon(S(t)) for some s ≠ t in Δ: return UNSAT
L11 return SAT
```

Without function symbols, $D$ is empty and line L5 never applies. The procedure is then Algorithm S1 of the Handbook (Figure 33.5): process the equations one by one with the solver, then check the disequations with the canonizer. For linear arithmetic, S1 is Gaussian elimination with back-substitution.

Line L5 is congruence closure done modulo the theory. Two applications of $f$ are merged when the solved form makes their arguments equal, even if the arguments look different. The merge is just one more equation for the solver.

## Example

**The Handbook example.** Take $\Gamma = \{a + 3b - 2c = 1,\ a - b - 6c = 1\}$ and $\Delta = \{b + a \ne a - c\}$ (Handbook, Example 33.5.4). Solving the first equation for $a$ gives $S = \{a = 1 - 3b + 2c\}$. The second equation becomes $1 - 3b + 2c - b - 6c = 1$, that is, $-4b - 4c = 0$, solved as $b = -c$. Then $S = \{a = 1 + 5c,\ b = -c\}$. Now $S(b + a)$ and $S(a - c)$ are both $1 + 4c$, so line L10 answers UNSAT. With $f(b + a) \ne f(a - c)$ in place of the disequation, the answer is again UNSAT: the two names are merged at line L5.

**Arithmetic finds a congruence.** Take
$$\Gamma = \{f(x) = y + 1,\ x = 2y - z,\ z = y\}, \qquad \Delta = \{f(y) \ne y + 1\}.$$
Line L1 names $f(x)$ as $u_1$ and $f(y)$ as $u_2$. The implementation solves for the first variable in alphabetical order and gives this run:

| step | from | equation after $S$ | $S^*$ | $S$ after the step |
|---|---|---|---|---|
| 1 | $\Gamma$ | $u_1 - y - 1 = 0$ | $u_1 = y + 1$ | $u_1 = y + 1$ |
| 2 | $\Gamma$ | $x - 2y + z = 0$ | $x = 2y - z$ | $u_1 = y + 1,\ x = 2y - z$ |
| 3 | $\Gamma$ | $z - y = 0$ | $y = z$ | $u_1 = z + 1,\ x = z,\ y = z$ |
| 4 | L5 | $u_2 - z - 1 = 0$ | $u_2 = z + 1$ | $u_1 = z + 1,\ x = z,\ y = z,\ u_2 = z + 1$ |

After step 3, the arguments of $f(x)$ and $f(y)$ both become $z$, but $u_1$ is $z + 1$ and $u_2$ is not. So line L5 adds $u_2 = u_1$. At line L10, $S(u_2) = z + 1$ and $S(y + 1) = z + 1$, so the answer is UNSAT. Neither the arithmetic nor congruence closure alone finds this: the equality $x = y$ comes only from arithmetic, and $f(x) = f(y)$ only from congruence. Without $z = y$, the procedure answers SAT.

## Correctness

The [proof page](proofs/correctness.md) proves the procedure for linear equations over $\mathbb{Q}$ with uninterpreted functions. It is a special case of the theorem of Rueß and Shankar (2001) for convex Shostak theories.

- **UNSAT is correct.** Every model of the input satisfies $S$ at all times. Equations from $\Gamma$ hold in it. A merge at line L5 holds in it, because the arguments of $u$ and $v$ have equal values when $S$ holds. The solver result is equivalent to the equation it solves. So $\bot$ at line L8, or a disequation $s \ne t$ with $S(s)$ and $S(t)$ identical at line L10, rules out every model.
- **Termination.** Each step from line L5 solves a non-trivial equation, so it makes one more variable solitary, and solitary variables stay solitary. With $V$ variables and names, there are at most $|\Gamma| + V$ steps.
- **SAT is correct.** At the end, choose values of the free variables so that any two distinct canonical forms that occur get distinct values; this is possible because finitely many hyperplanes do not cover $\mathbb{Q}^k$. Define each $f$ by its definitions. Congruence at line L5 is exactly what makes this well defined, and line L10 is exactly what makes the disequations true.

**Tests.** The implementation was compared with an independent procedure on 600 random problems. The reference removes the function symbols by [Ackermann's reduction](/ackermannization/), searches over the case splits between pairs of applications, and decides each case by Gaussian elimination. The two agreed on all problems: 482 satisfiable and 118 unsatisfiable. A congruence step at line L5 was used in 87 problems. For every SAT answer, the test builds the model of the proof, with random values for the free variables, and checks it on the original terms. The tests also check the Handbook example and its solved form $a = 1 + 5c,\ b = -c$, and check the canonizer against evaluation.

## Complexity

Count operations on rationals as one step. Let $n$ be the number of symbols of the input, so there are at most $n$ equations, names and variables. The loop runs $O(n)$ times (Lemma 3 of the proof). In each pass, applying $S$ to an equation and composing $S^*$ into $S$ costs $O(n^2)$, because $S$ has at most $n$ equations with at most $n$ terms each. The search of line L5 canonizes the arguments of all definitions under $S$, which costs $O(n^2)$, and finds equal keys with a hash table. The total is $O(n^3)$ time. The implementation sorts the canonical forms, which adds a $\log n$ factor. The solved form takes $O(n^2)$ space.

The numbers can grow, as in any Gaussian elimination. With bit costs, the time is still polynomial, by the usual bounds on the sizes of the entries of eliminated systems.

## Properties

- **One data structure.** All equalities, from the theory and from congruence, live in one solved form. There is no exchange of equalities between separate solvers, and no purification of mixed terms such as $f(x + 1) - 1$.
- **Canonical forms.** Two terms are known equal exactly when their canonical forms under $S$ are identical. This gives a cheap test of entailed equalities, which is what a theory solver in an SMT solver must report.
- **Incremental.** Equations are processed one at a time, so new equations can be added to the solved form later.
- **Restricted.** The theory must have a canonizer and a solver and no predicates. Completeness of the check of line L10 needs a convex theory, or at most one disequation (Handbook, Section 33.5.1).

## Variants and improvements

- **Algorithm S1.** The theory alone, without line L5. It is the core of the method (Handbook, Figure 33.5).
- **The corrected procedure of Rueß and Shankar.** Their 2001 paper "Deconstructing Shostak" separates the solved form of the theory from the congruence closure of the uninterpreted part, and proves termination, soundness and completeness. The procedure on this page follows the same idea in a simple form.
- **Several Shostak theories.** Shankar and Rueß (2002) combine several Shostak theories. Their method combines the canonizers, but not the solvers: it runs each solver separately and exchanges equalities as in [Nelson-Oppen](/nelson-oppen/). Krstić and Conchon (2003) showed that solvers can almost never be combined.
- **Shostak as a refinement of Nelson-Oppen.** Barrett, Dill and Stump (2002) present the method as a Nelson-Oppen combination in which a Shostak theory is handled without purification. Ganzinger (2002) gave another reconstruction, "Shostak light".
- **CC(X).** Conchon, Contejean, Kanig and Lescuyer (2008) give a [congruence closure](/congruence-closure/) parameterized by any solvable theory $X$. It is the core of the Alt-Ergo prover.

## When to use it

Use the method when the main theory has a natural solved form: linear equalities over a field, the theory of tuples or records, or fixed-size bit-vector equalities with a solver. It gives a compact procedure for such a theory together with uninterpreted functions, and canonical forms make entailed equalities cheap to report. Do not use it to combine two theories by merging their solvers. For that, use [Nelson-Oppen](/nelson-oppen/) or [model-based theory combination](/model-based-theory-combination/), which is what modern SMT solvers do. For inequalities, such as linear real arithmetic with $\le$, use the simplex method instead.

## Pitfalls

- **Trusting the 1984 paper.** The Handbook says that "The original paper lacks rigor and contains serious errors" (Section 33.5.1). Implement a corrected version, such as Rueß and Shankar's, and not the original.
- **Combining two solvers.** Shostak claimed that the canonizers and solvers of two Shostak theories combine into a canonizer and a solver for their union. Canonizers do combine, but solvers almost never do (Krstić and Conchon, 2003).
- **Non-convex theories.** For a non-convex theory, line L10 checks each disequation alone and can miss a conflict among several of them. Completeness then needs case splits.
- **Applying congruence only to the input syntax.** $f(x + y)$ and $f(y + x)$ are the same term in the theory. The names and line L5 must compare canonical forms of arguments under $S$, not the arguments as written.
- **Fresh constants of the solver.** For some theories the solver introduces fresh existential constants. They must be kept apart from the input constants, or the answer can be wrong.

## Implementations

## History

Shostak gave a congruence closure algorithm in 1978 and published "Deciding combinations of theories" in the Journal of the ACM in 1984. Verification systems such as PVS and the validity checker SVC used variants of it. Its subtle points stayed unclear for many years. Cyrluk, Lincoln and Shankar studied it in 1996. In 2001 Rueß and Shankar gave the first correct version with full proofs, for one Shostak theory with uninterpreted functions. In 2002, Shankar and Rueß, Barrett, Dill and Stump, and Ganzinger gave further reconstructions, and in 2003 Krstić and Conchon showed that the claim about combining solvers is false. The Handbook summarizes that work since 1984 "has shed considerable light on the original claims" (Section 33.5.1). Modern SMT solvers combine theories with Nelson-Oppen, but canonizers and solved forms remain common inside theory solvers.

## References
