---
tag: ZKP8A0
kind: problem
slug: smt-problem
name: Satisfiability modulo theories (SMT) problem
aliases:
- SMT problem
- satisfiability modulo theories
- SMT
- ground T-satisfiability
area: logic-and-constraints/smt
level: intro
summary: Decide whether a formula with Boolean structure over atoms of background theories, such as arithmetic, arrays or bit-vectors, has a model in which those theories hold.
prereqs: [sat, conjunctive-normal-form, np-complete]
see_also: [euf-satisfiability, dpll-t, cdcl-t, lazy-smt, eager-smt-encoding, nelson-oppen, smt-lib, decision-procedure]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.1 (the problem and its two main approaches), Section 33.2.1 (syntax, semantics, theories as sets of models, the ground T-satisfiability problem), Section 33.2.2 (equality, arithmetic, arrays, bit-vectors, inductive data types, with their complexity)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 1 (theories, decision procedures and the satisfiability problem) and Chapter 3 (from propositional to quantifier-free theories)
  - paper: doi:10.1007/978-3-319-10575-8_11
    title: Clark Barrett and Cesare Tinelli, Satisfiability Modulo Theories, in Clarke, Henzinger, Veith and Bloem (eds.), Handbook of Model Checking, Springer, 2018, pages 305 to 343
    locator: the definitions of theories and of the SMT problem, and the survey of theories and solvers
  - paper: doi:10.1145/1995376.1995394
    title: Leonardo de Moura and Nikolaj Bjørner, Satisfiability modulo theories, introduction and applications, Communications of the ACM 54(9), 2011, pages 69 to 77
    locator: the applications in program analysis, test generation and verification
  - paper: doi:10.1145/322276.322287
    title: Christos H. Papadimitriou, On the complexity of integer programming, Journal of the ACM 28(4), 1981, pages 765 to 768
    locator: integer linear programming is in NP (small solutions), so conjunctions of integer linear constraints are NP-complete
  - paper: doi:10.1145/62212.62257
    title: John Canny, Some algebraic and geometric computations in PSPACE, STOC 1988, pages 460 to 469
    locator: the existential theory of the reals is decidable in polynomial space
  - paper: doi:10.1007/s00224-015-9653-1
    title: Gergely Kovásznai, Andreas Fröhlich and Armin Biere, Complexity of fixed-size bit-vector logics, Theory of Computing Systems 59(2), 2016, pages 323 to 376
    locator: the complexity of quantifier-free and quantified bit-vector logics with unary and binary encoded widths
  - url: https://smt-lib.org/
    title: The SMT-LIB initiative, the SMT-LIB standard and benchmark library
    locator: the logics such as QF_UF, QF_LRA, QF_LIA, QF_BV and QF_AX, and their theories
---

The satisfiability modulo theories (SMT) problem asks whether a formula has a model in which some *background theories* hold. The formula has the Boolean structure of [SAT](/sat/), but its atoms are not plain Boolean variables. They are facts such as $x + 2y \le 5$ over the integers, $f(a) = b$ for an unknown function $f$, $\mathrm{read}(A, i) = v$ for an array $A$, or $x + 1 <_u x$ for an 8-bit machine word $x$. The theory fixes the meaning of the symbols $+$, $\le$, read and $<_u$, and only the other symbols are free. Most SMT solvers decide the quantifier-free case, which is NP-complete for the common theories. Some theories make even this case undecidable, and quantifiers make most theories undecidable. This page is about the problem itself. The pages on [EUF satisfiability](/euf-satisfiability/), [linear real arithmetic](/linear-real-arithmetic-satisfiability/), [bit-vectors](/bit-vector-satisfiability/) and the others are about one theory each, and [DPLL(T)](/dpll-t/) and [CDCL(T)](/cdcl-t/) are the main algorithms.

## In plain words

A SAT solver answers this question: can I make all these rules true at the same time, if each switch can be on or off? Real problems are rarely only about switches. A program check asks about numbers, memory and calls to functions, for example "can this index be past the end of this array?".

SMT keeps the switch structure of SAT and lets each switch be a fact about numbers, arrays, words of bits or unknown functions. The solver must find values for all the unknowns so that the whole formula is true and every fact means what it should: a sum is a real sum, and an array read gives the value that was written last. If no such values exist, the answer is "unsatisfiable", which often means the program is safe.

## Definition

**Signatures and theories.** A *signature* $\Sigma$ is a set of function and predicate symbols, each with an arity. A $\Sigma$-*theory* $T$ is a set of $\Sigma$-models: for example, the one model of the integers with the usual $0, 1, +, -, \le$, or the class of all models of the array axioms. A theory given by axioms is the set of models of the axioms. The *empty theory*, which allows every model, is the theory of [equality with uninterpreted functions](/euf-satisfiability/) (EUF).

**Free symbols.** The formula can also use symbols that are not in $\Sigma$: constants that act as variables, propositional symbols and function symbols. They are *uninterpreted*: a model may give them any meaning, as long as its $\Sigma$-part is a model of $T$.

**The problem.** Given a theory $T$ and a ground (quantifier-free) formula $\varphi$ over $\Sigma$ and free symbols, decide whether some model of $T$, with some meaning for the free symbols, makes $\varphi$ true. Then $\varphi$ is $T$-*satisfiable*. Most solvers also return a *model*: values of the free constants and tables of the free functions, as far as the formula needs them. The dual problem asks whether $\varphi$ is $T$-*valid*, true in every model of $T$. It is the same problem, since $\varphi$ is $T$-valid exactly when $\neg \varphi$ is not $T$-satisfiable.

**Size.** $|\varphi|$ is the number of symbols of $\varphi$. In the bounds below, $n$ is the number of variables (free constants) and $m$ the number of atoms or constraints.

**The theory solver problem.** The special case where $\varphi$ is a conjunction of literals is the *$T$-satisfiability of conjunctions*. A procedure for it is a theory solver, see [decision procedure](/decision-procedure/). The two cases have different complexity, and the main SMT algorithms reduce the general case to many calls of the special case.

## Variants

- **By theory.** The [SMT-LIB](/smt-lib/) standard names *logics*, each a theory with a restriction on the formulas. QF_UF is EUF without quantifiers, QF_LRA is linear real arithmetic, QF_LIA is linear integer arithmetic, QF_IDL is [integer difference logic](/difference-logic-satisfiability/), QF_BV is [bit-vectors](/bit-vector-satisfiability/), QF_AX is [arrays](/array-theory-satisfiability/), and QF_S is [strings](/string-constraint-satisfiability/). A logic can combine theories, for example QF_AUFLIA for arrays, free functions and linear integer arithmetic.
- **Combined theories.** For theories $T_1$ and $T_2$ with disjoint signatures, $T_1 \oplus T_2$ is the set of models whose $\Sigma_i$-part is a model of $T_i$ for each $i$. The [Nelson-Oppen](/nelson-oppen/) method decides it from solvers for each part, under the conditions on the [stable infiniteness](/stable-infiniteness/) page.
- **With quantifiers.** Some solvers accept quantified formulas. For most theories the problem is then undecidable, and solvers use [quantifier instantiation](/quantifier-instantiation/), which is complete only for some fragments.
- **Optimization.** [MaxSMT](/maxsmt/) maximizes the weight of the satisfied soft constraints, and [optimization modulo theories](/optimization-modulo-theories/) minimizes a term of the theory, such as a cost in integer arithmetic.
- **Extra answers.** For an unsatisfiable input, a solver can return an [unsat core](/unsat-core/) or a proof. For a sequence of related queries, [incremental solving](/incremental-solving/) keeps the work done.
- **Synthesis.** [Syntax-guided synthesis](/syntax-guided-synthesis/) asks for a function body that makes a formula valid for all inputs. [CEGIS](/cegis/) solves it with SMT calls.

## Examples

Each answer below was checked by a short brute-force script.

1. **The theory matters.** Take $x < y \wedge \neg (x < y + 0)$. Over the integers it is unsatisfiable, because $y + 0 = y$. In the empty theory it is satisfiable: take the universe $\{0, 1\}$, $x = y = 1$, $0$ for the constant $0$, the relation $<$ that holds only for $(1, 1)$, and the function $+$ that always gives 0. Then $x < y$ is true and $x < y + 0$ is $1 < 0$, which is false. This is the opening example of the Handbook chapter.
2. **EUF.** $(a = b \vee a = c) \wedge f(a) \ne f(b) \wedge f(a) \ne f(c)$ is unsatisfiable. In each case of the disjunction, functional consistency gives $f(a) = f(b)$ or $f(a) = f(c)$. The Boolean structure alone does not show it, because the formula has three propositional models when its atoms are read as free Boolean variables. The [DPLL(T)](/dpll-t/) page solves this example step by step.
3. **Integers and reals.** $2x - 2y = 1$ has the real solution $x = 1/2$, $y = 0$, so it is satisfiable in QF_LRA. It is unsatisfiable in QF_LIA, because the left side is even for all integers.
4. **Bit-vectors.** For an 8-bit word $x$, $x + 1 <_u x$ is satisfiable, and $x = 255$ is its only solution: $255 + 1$ wraps around to 0. Over the integers the same formula is unsatisfiable.
5. **Arrays.** $\mathrm{read}(\mathrm{write}(A, i, v), j) = v \wedge i \ne j \wedge \mathrm{read}(A, j) \ne v$ is unsatisfiable, because for $i \ne j$ the read sees the old value $\mathrm{read}(A, j)$. Without $i \ne j$ it is satisfiable, for example with $i = j = 0$, $v = 1$ and an array that holds 0 at index 0.
6. **Combined theories.** $x \le y \wedge y \le x \wedge f(x) \ne f(y)$ over integers with a free function $f$ is unsatisfiable: arithmetic gives $x = y$, and then EUF gives $f(x) = f(y)$. Neither theory alone sees the conflict. Without $y \le x$ it is satisfiable, with $x = 0$, $y = 1$, $f(0) = 0$ and $f(1) = 1$. The [Nelson-Oppen](/nelson-oppen/) page solves such problems by exchanging equalities.

## Known algorithms

- **Lazy.** A [CDCL](/cdcl/) SAT solver runs on the [Boolean abstraction](/boolean-abstraction/) of the formula and asks a theory solver about the literals it assigns. See [lazy SMT](/lazy-smt/), [DPLL(T)](/dpll-t/) and [CDCL(T)](/cdcl-t/). This is the main method of today's solvers.
- **Eager.** Translate the whole formula into an equisatisfiable propositional formula and call a SAT solver once. See [eager SMT encoding](/eager-smt-encoding/), [Ackermannization](/ackermannization/) and [bit-blasting](/bit-blasting/).
- **Theory solvers.** [Congruence closure](/congruence-closure/) for EUF, [simplex](/simplex-for-smt/) for linear real arithmetic, [Bellman-Ford](/bellman-ford/) style negative cycle detection for difference logic, branch and bound and cuts or the [omega test](/omega-test/) for integers, and bit-blasting for bit-vectors.
- **Combination.** [Nelson-Oppen](/nelson-oppen/), [Shostak's method](/shostak-combination/) and [model-based theory combination](/model-based-theory-combination/).
- **Quantifiers.** [E-matching](/e-matching/) and other forms of [quantifier instantiation](/quantifier-instantiation/).

## Bounds

The table gives the complexity of the quantifier-free problem. "Conjunctions" is the case of a conjunction of literals, and "formulas" allows any Boolean structure.

| logic | conjunctions | formulas | source |
|---|---|---|---|
| QF_UF (EUF) | $O(n \log n)$ for input size $n$ | NP-complete | Downey, Sethi and Tarjan 1980; see [EUF satisfiability](/euf-satisfiability/) |
| QF_IDL (difference logic) | $O(n m)$, by negative cycle detection | NP-complete | see [difference logic](/difference-logic-satisfiability/) |
| QF_LRA | polynomial (by linear programming) | NP-complete | Handbook, Section 33.2.2.2 |
| QF_LIA | NP-complete | NP-complete | Papadimitriou 1981 |
| QF_AX (arrays) | in NP | NP-complete | Handbook, Section 33.2.2.3 |
| QF_BV, widths written in unary | NP-complete | NP-complete | Handbook, Section 33.2.2.4 |
| QF_BV, widths written in binary | | NEXPTIME-complete | Kovásznai, Fröhlich and Biere 2016 |
| QF_NRA (nonlinear reals) | NP-hard, in PSPACE | NP-hard, in PSPACE | Canny 1988 |
| QF_NIA (nonlinear integers) | undecidable | undecidable | Matiyasevich 1970, see [Hilbert's tenth problem](/hilberts-tenth-problem/) |

With quantifiers, EUF is full first-order logic, which is undecidable. [Presburger arithmetic](/presburger-arithmetic/), the full first-order theory of the integers with addition, is decidable, and Fischer and Rabin (1974) showed that every decision procedure for it needs doubly exponential time in the worst case. The first-order theory of the real numbers with addition and multiplication is decidable by the [Tarski decidability theorem](/tarski-decidability-theorem/), and quantifier elimination for it needs doubly exponential time in the worst case (Davenport and Heintz 1988).

**Upper bound for the Boolean structure.** If the satisfiability of conjunctions of $T$-literals is in NP, then the SMT problem for $T$ is in NP. *Proof.* A certificate is a truth value for each atom of $\varphi$, together with an NP certificate that the conjunction $\mu$ of the chosen literals is $T$-satisfiable. The checker evaluates $\varphi$ on the truth values in linear time and checks the certificate for $\mu$, whose size is at most $|\varphi|$. If $\varphi$ has a $T$-model $\mathcal{A}$, the truth values of the atoms in $\mathcal{A}$ make $\varphi$ true and $\mathcal{A}$ satisfies $\mu$, so a certificate exists. If a certificate exists, a $T$-model of $\mu$ makes every atom of $\varphi$ take its chosen value, so it makes $\varphi$ true. $\square$

**Lower bound.** SAT is the special case with no theory atoms, so the SMT problem is NP-hard for every theory. With the upper bound, it is NP-complete whenever conjunctions are in NP. So for QF_UF, QF_IDL and QF_LRA the hard part is the Boolean structure, while for QF_LIA conjunctions are already NP-complete.

These are worst-case bounds. How fast solvers are in practice is only measured, for example in the yearly SMT-COMP competition on the SMT-LIB benchmarks, and such results hold only for those benchmark sets.

## Reductions

- **SAT to SMT.** A CNF over propositional symbols is an SMT formula of any theory. This gives NP-hardness.
- **SMT to SAT, for some theories.** If $T$ has a bounded model property or a finite set of instances of its axioms that is enough, the formula can be translated to SAT. [Ackermannization](/ackermannization/) removes free functions with a quadratic number of new constraints, and a small-domain bound then encodes each variable with $O(\log n)$ Boolean variables. [Bit-blasting](/bit-blasting/) encodes a bit-vector formula as a circuit. See [eager SMT encoding](/eager-smt-encoding/).
- **SMT to many conjunction problems.** The lazy approach reduces the problem to a SAT search plus calls of a theory solver on conjunctions of literals. This is why a theory solver for conjunctions is the main part of each theory.
- **Combined theories to single theories.** Nelson-Oppen reduces satisfiability in $T_1 \oplus T_2$ to satisfiability in $T_1$ and in $T_2$, for signature-disjoint, stably infinite theories with decidable conjunctions.
- **Validity to unsatisfiability.** A verification condition $\psi$ is valid exactly when $\neg \psi$ is unsatisfiable, so program checkers send $\neg \psi$ to the solver.

## Applications

- **Program verification.** Tools such as Boogie, Dafny and Why3 turn a program with its specification into verification conditions and send their negations to an SMT solver. ESC/Java 2 and the Handbook list of tools use the same idea.
- **Test generation and symbolic execution.** [Symbolic execution](/symbolic-execution/) follows a path of a program and asks the solver for inputs that take the path. DART, EXE, CUTE and Pex are early tools of this kind.
- **Model checking.** [Bounded model checking](/bounded-model-checking/) of software and hardware with data needs arithmetic, arrays and bit-vectors, and [CEGAR](/cegar/) uses a solver to check abstract counterexamples.
- **Hardware verification.** Uninterpreted functions abstract a data path, as in the work of Burch and Dill on pipelined processors.
- **Synthesis and optimization.** [CEGIS](/cegis/) and [syntax-guided synthesis](/syntax-guided-synthesis/) use SMT calls to check candidates. Scheduling and planning use [optimization modulo theories](/optimization-modulo-theories/).
- **Interactive proof.** Proof assistants such as Isabelle send goals to SMT solvers and check the proofs they return.

## References
