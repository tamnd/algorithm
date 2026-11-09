---
tag: 88HCN5
kind: problem
slug: euf-satisfiability
name: Equality with uninterpreted functions (EUF) satisfiability
aliases:
- EUF
- equality logic with uninterpreted functions
- QF_UF satisfiability
area: logic-and-constraints/smt
level: core
summary: Decide whether a quantifier-free formula of equalities between terms built from free function symbols has a model. Conjunctions take O(n log n) time; with Boolean structure it is NP-complete.
prereqs: [smt-problem, sat, equivalence-relation]
see_also: [congruence-closure, e-graph, ackermannization, eager-smt-encoding, dpll-t, nelson-oppen, smt-lib, word-problem]
sources:
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 4, Equality Logic and Uninterpreted Functions, and Chapter 11, Propositional Encodings
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.2.2.1, Equality, and Section 33.3, Eager Encodings to SAT
  - paper: doi:10.1145/322217.322228
    title: Peter J. Downey, Ravi Sethi and Robert E. Tarjan, Variations on the common subexpression problem, Journal of the ACM 27(4), 1980, pages 758 to 771
    locator: the O(n log n) algorithm for congruence closure
  - paper: doi:10.1006/inco.2002.3175
    title: Amir Pnueli, Yoav Rodeh, Ofer Shtrichman and Michael Siegel, The small model property, how small can it be?, Information and Computation 178(1), 2002, pages 279 to 293
    locator: the small model property of equality logic and the reduction of the domain sizes
  - paper: doi:10.1145/371282.371364
    title: Randal E. Bryant, Steven German and Miroslav N. Velev, Processor verification using efficient reductions of the logic of uninterpreted functions to propositional logic, ACM Transactions on Computational Logic 2(1), 2001, pages 93 to 134
    locator: the elimination of function applications and positive equality
  - paper: doi:10.1007/3-540-58179-0_44
    title: Jerry R. Burch and David L. Dill, Automatic verification of pipelined microprocessor control, CAV 1994, LNCS 818, pages 68 to 80
    locator: the use of uninterpreted functions to abstract the data path
  - paper: doi:10.1145/800105.803406
    title: Dexter Kozen, Complexity of finitely presented algebras, STOC 1977, pages 164 to 177
    locator: the uniform word problem for finitely presented algebras is in polynomial time
  - paper: doi:10.1007/bfb0054170
    title: Amir Pnueli, Michael Siegel and Eli Singerman, Translation validation, TACAS 1998, LNCS 1384, pages 151 to 166
    locator: the use of uninterpreted functions in the validation of a compiler output
---

EUF satisfiability asks whether a formula built from equalities $s = t$ between terms, with the Boolean connectives, has a model when the function symbols have no fixed meaning. A model may choose any domain and any functions, but it must give equal results for equal arguments. This is the theory of equality with uninterpreted functions, the logic QF_UF of [SMT-LIB](/smt-lib/). A conjunction of equalities and disequalities is decided by [congruence closure](/congruence-closure/) in $O(n \log n)$ time. A formula with full Boolean structure is NP-complete, and SMT solvers decide it with a SAT solver and congruence closure in the [lazy](/lazy-smt/) scheme, or by an [eager encoding](/eager-smt-encoding/) to SAT.

## In plain words

You get some facts and some claims of the form "this thing equals that thing", where the things are names and functions applied to them. You know nothing about what the functions do. You only know the rule that a function gives the same output for the same input.

The question is whether some choice of values and functions makes all the facts true at once. For example, "a equals b, but f of a is not f of b" is impossible: if a and b are the same, any function must give the same output for them.

This is useful because a hard part of a program, such as a multiplier, can be replaced by an unknown function. If the claim holds for every function, it holds for the real one too.

## Definition

**Terms.** Fix a set of constants and of function symbols, each with an arity $k \ge 1$. A term is a constant or $f(t_1, \ldots, t_k)$ for terms $t_i$. All terms are ground: there are no variables bound by quantifiers. Uninterpreted predicate symbols can be added, or written as $p(t) = \top$ with a fresh constant $\top$.

**Formulas.** An atom is $s = t$ for terms $s$ and $t$. A formula is built from atoms with $\neg$, $\wedge$, $\vee$, $\to$, or is a conjunction of literals in the conjunctive version.

**Models.** A model $M$ is a nonempty set $U$ with an element $a^M \in U$ for each constant and a function $f^M : U^k \to U$ for each symbol of arity $k$. The value $M(t)$ of a term is defined by $M(f(t_1, \ldots, t_k)) = f^M(M(t_1), \ldots, M(t_k))$. The atom $s = t$ is true in $M$ when $M(s) = M(t)$.

**The problem.** Given a formula $\varphi$, decide whether some model makes it true. The size $n$ of the input is the number of distinct subterms of $\varphi$ plus the number of its connectives.

The only fact the theory knows is *functional consistency*: $s_1 = t_1 \wedge \cdots \wedge s_k = t_k \to f(s_1, \ldots, s_k) = f(t_1, \ldots, t_k)$. Together with reflexivity, symmetry and transitivity of $=$, this is the theory of equality.

## Variants

- **Conjunctive EUF.** The input is a conjunction of equalities and disequalities. This is the problem that a theory solver for EUF answers in an SMT solver. It is in P.
- **Equality logic.** No function symbols, only constants. Ackermann's reduction turns EUF into equality logic, see [Ackermannization](/ackermannization/).
- **Validity.** $\varphi$ is valid when $\neg \varphi$ is not satisfiable. A typical query is "does $x_1 = y_1 \wedge x_2 = y_2$ imply $g(x_1, x_2) = g(y_1, y_2)$".
- **The uniform word problem.** Given ground equations $E$ and an equation $s = t$, decide whether $E \models s = t$. This is conjunctive EUF with one disequation, and Kozen showed in 1977 that it is in P.
- **With quantifiers.** First-order logic with equality and function symbols is undecidable. SMT solvers handle quantified EUF by [quantifier instantiation](/quantifier-instantiation/), which is incomplete in general.
- **In combination.** EUF is often one of several theories, as in QF_UFLIA, and it is joined to the others by [Nelson-Oppen](/nelson-oppen/) combination or a [variant](/model-based-theory-combination/).

## Examples

Write $f^k(a)$ for $f$ applied $k$ times to $a$.

1. $a = b \wedge f(a) \ne f(b)$ is unsatisfiable, by functional consistency.
2. $f^3(a) = a \wedge f^5(a) = a \wedge f(a) \ne a$ is unsatisfiable. From $f^3(a) = a$, apply $f$ twice to get $f^5(a) = f^2(a)$, so $f^2(a) = a$. Then $f^3(a) = f(a)$, so $f(a) = a$. The [congruence closure](/congruence-closure/) page traces this case.
3. $(a = b \vee a = c) \wedge f(a) \ne f(b) \wedge f(a) \ne f(c)$ is unsatisfiable, but no single conjunction shows it: each disjunct gives a conflict with one disequation. A solver must split on the disjunction.
4. $(a = b \vee b = c) \wedge f(a) \ne f(c)$ is satisfiable. A model has $U = \{0, 1\}$, $a = b = 0$, $c = 1$, and $f$ the identity. Then $f(a) = 0 \ne 1 = f(c)$.
5. $x_1 = y_1 \wedge x_2 = y_2 \wedge g(x_1, x_2) \ne g(y_1, y_2)$ is unsatisfiable. So the implication of the validity variant is valid.

A brute force check over all models of size at most the number of subterms confirms the answers for examples 2 to 5. The small model property below says that this check is complete.

## Known algorithms

| algorithm | input | time |
|---|---|---|
| [Congruence closure](/congruence-closure/) (Downey, Sethi and Tarjan) | conjunction | $O(n \log n)$ |
| [Congruence closure](/congruence-closure/) (Nelson and Oppen) | conjunction | $O(n^2)$ |
| [E-graph](/e-graph/) with deferred rebuilding | many merges and queries | $O(n \log n)$ table operations for a fixed arity |
| [DPLL(T)](/dpll-t/) or [CDCL(T)](/cdcl-t/) with congruence closure | any formula | exponential in the worst case |
| [Ackermannization](/ackermannization/) and an [eager encoding](/eager-smt-encoding/) to SAT | any formula | polynomial reduction, then a SAT solver |

The lazy approach uses congruence closure as the theory solver. It needs the solver to be incremental, to backtrack, and to [explain](/theory-conflict-explanation/) its conflicts. The eager approach replaces each application by a fresh constant with Ackermann's constraints or with the nested if-then-else terms of Bryant, German and Velev, and then encodes equality logic in propositional logic. Two encodings are common: a small domain with a few bits for each constant, and one Boolean variable for each equality with transitivity constraints.

## Bounds

**Small model property.** If $\varphi$ is satisfiable and has $m$ distinct subterms, it has a model with at most $m$ elements. *Proof.* Take a model $M$, and let $V$ be the set of values $M(t)$ of the subterms $t$ of $\varphi$, so $|V| \le m$. Pick $v_0 \in V$. Define $M'$ on $V$ with the same constants, and $f^{M'}(\bar v) = f^M(\bar v)$ when this is in $V$, else $v_0$. For each subterm $f(t_1, \ldots, t_k)$, by induction $M'(t_i) = M(t_i)$, and $f^M(M(t_1), \ldots) = M(f(t_1, \ldots))$ is in $V$, so $M'$ gives each subterm the same value as $M$. So each atom, and $\varphi$, has the same truth value. $\square$ Pnueli, Rodeh, Shtrichman and Siegel give smaller domains for each constant.

**Conjunctive EUF is in P.** Congruence closure takes $O(n \log n)$ time, and this is the best bound known. Reading the input needs $\Omega(n)$ time.

**EUF with Boolean structure is NP-complete.** *In NP:* guess, for each pair of subterms, whether they are equal, and check with congruence closure that the guess is a consistent equivalence and makes $\varphi$ true. By the small model property a guessed partition of the subterms is enough. *NP-hard:* a propositional formula $\psi$ over $p_1, \ldots, p_r$ is satisfiable if and only if the EUF formula that replaces each $p_i$ by $a_i = c$, for fresh constants $a_1, \ldots, a_r, c$, is satisfiable. Given a truth assignment, take $U = \{0, 1\}$, $c = 1$, and $a_i = 1$ exactly when $p_i$ is true. Given an EUF model, set $p_i$ true exactly when $a_i = c$.

## Reductions

- **To equality logic.** [Ackermannization](/ackermannization/) replaces each application $f(\bar t)$ by a fresh constant and adds $\bar t = \bar u \to f_{\bar t} = f_{\bar u}$ for each pair of applications of the same symbol. The result is equisatisfiable and its size is quadratic.
- **To SAT.** Equality logic over $m$ constants can be encoded with a domain of size $m$ and $\lceil \log_2 m \rceil$ bits for each constant, or with one variable for each equality atom and transitivity constraints. See [eager SMT encoding](/eager-smt-encoding/) and [bit-blasting](/bit-blasting/).
- **From SAT.** The reduction in the bounds section shows NP-hardness.
- **Abstraction of other theories.** Any theory can be over-approximated by treating its function symbols as uninterpreted. If the abstract formula is unsatisfiable, so is the original. Burch and Dill used this for pipelined processors, where the data path is replaced by uninterpreted functions.

## Applications

- **Hardware verification.** Burch and Dill checked pipelined processor control in 1994 with the arithmetic units replaced by uninterpreted functions. Bryant, German and Velev made the reduction to SAT efficient with positive equality.
- **Translation validation.** Pnueli, Siegel and Singerman check that a compiler output is equivalent to its source, with the operations of the source language as uninterpreted functions.
- **SMT solvers.** EUF is the theory that connects the others in a [combination](/nelson-oppen/), and congruence closure is the core of the EUF solver.
- **Program verification and optimization.** Common subexpression elimination, value numbering and equality saturation use the same closure. See [e-graph](/e-graph/).

## References
