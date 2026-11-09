---
tag: HYJS00
kind: technique
slug: eager-smt-encoding
name: Eager SMT encoding
aliases:
- eager approach
- eager SMT
- SAT encoding of SMT
- small-domain encoding
- per-constraint encoding
area: logic-and-constraints/smt
level: advanced
summary: Translate the whole SMT formula into one equisatisfiable propositional formula, with all the theory facts that it needs, and call a SAT solver once.
prereqs: [smt-problem, sat, boolean-abstraction, ackermannization]
see_also: [lazy-smt, bit-blasting, euf-satisfiability, difference-logic-satisfiability, tseitin-transformation, dpll-t, bit-vector-satisfiability, linear-integer-arithmetic-satisfiability]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.3 (Eager Encodings to SAT, with Theorem 33.3.2 and Theorem 33.3.3, Table 33.1 on solution bounds and Table 33.2 on the size of direct encodings), Section 33.7.1 (combining eager and lazy approaches)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 4 (equality logic and uninterpreted functions, Ackermann's reduction and the small domain) and Chapter 11 (propositional encodings)
  - paper: doi:10.1007/3-540-45657-0_7
    title: Randal E. Bryant, Shuvendu K. Lahiri and Sanjit A. Seshia, Modeling and verifying systems using a logic of counter arithmetic with lambda expressions and uninterpreted functions, CAV 2002, LNCS 2404, pages 78 to 92
    locator: the UCLID logic and its translation to SAT
  - paper: doi:10.1145/371282.371364
    title: Randal E. Bryant, Steven German and Miroslav N. Velev, Processor verification using efficient reductions of the logic of uninterpreted functions to propositional logic, ACM Transactions on Computational Logic 2(1), 2001, pages 93 to 134
    locator: the ite elimination of function applications and positive equality
  - paper: doi:10.1145/566385.566390
    title: Randal E. Bryant and Miroslav N. Velev, Boolean satisfiability with transitivity constraints, ACM Transactions on Computational Logic 3(4), 2002, pages 604 to 627
    locator: transitivity constraints on a chordal constraint graph, the per-constraint encoding of equality logic
  - paper: doi:10.1006/inco.2002.3175
    title: Amir Pnueli, Yoav Rodeh, Ofer Shtrichman and Michael Siegel, The small model property, how small can it be?, Information and Computation 178(1), 2002, pages 279 to 293
    locator: range allocation, small domains for each variable of equality logic
  - paper: doi:10.1007/3-540-45657-0_16
    title: Ofer Strichman, Sanjit A. Seshia and Randal E. Bryant, Deciding separation formulas with SAT, CAV 2002, LNCS 2404, pages 209 to 222
    locator: the per-constraint encoding of difference logic by transitivity constraints
---

The eager approach decides an SMT formula $\varphi$ by one translation into a propositional formula $\varphi_{\mathrm{bool}}$ that is satisfiable exactly when $\varphi$ is, followed by one call of a SAT solver. The translation must put into $\varphi_{\mathrm{bool}}$ all the theory facts that can matter, before the search starts. That is what makes it *eager*. The Handbook compares it to an optimizing compiler, with the SMT formula as the program and the CNF as the object code. Its main use today is for theories with finite domains, above all [bit-vectors](/bit-vector-satisfiability/) by [bit-blasting](/bit-blasting/), and for equality with uninterpreted functions in hardware verification. The [lazy approach](/lazy-smt/) does the opposite: it gives the SAT solver only the [Boolean abstraction](/boolean-abstraction/), and adds theory facts as lemmas when a model needs them.

## In plain words

A SAT solver is very good, but it understands only switches. So the eager approach rewrites the whole problem in switches before it starts.

A number that can take eight values becomes three switches, because three switches have eight settings. A test such as "x equals y" becomes a small circuit that compares the switches of x and y. An unknown function f is removed: each use of it, such as f(a), gets its own new name, and a rule says that if a equals b, then the names for f(a) and f(b) must be equal.

The result is one big switch problem. If the SAT solver finds a setting, it can be read back as numbers and functions. The hard part is to keep the translation small.

## When it applies

- The theory has a *small model property*: if $\varphi$ has a model, it has one with values in a known finite range, as for equality logic, [difference logic](/difference-logic-satisfiability/) and [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/).
- Or the theory has a finite set of axiom instances that is enough, such as Ackermann's functional consistency constraints for free functions, or transitivity constraints for equalities.
- Or the domain is already finite and small in bits, as for fixed-width bit-vectors and floating-point numbers, see [floating-point satisfiability](/floating-point-satisfiability/).
- The translation is not much larger than the input. The theory reasoning is light compared with the Boolean reasoning, so one strong SAT call is better than many theory calls.

## The template

The holes are the removal of functions, the choice between the two encodings of the arithmetic part, and the size of each domain.

```pseudo id=main
EAGER(φ)
L1  remove lambda expressions and ite terms from φ               ▷ hole: preprocessing
L2  φ ← φ with function applications replaced by fresh constants, plus the functional consistency constraints FC   ▷ hole: Ackermann or Bryant-German-Velev
L3  split the constants into classes that are never compared with each other
L4  for each class C, choose the small-domain or the per-constraint encoding   ▷ hole: the choice, by hand or by a learned rule
L5      small domain: give each constant of C ⌈log2 d_C⌉ Boolean variables, for a domain bound d_C, and replace each atom of C by a comparison circuit
L6      per-constraint: replace each atom of C by a variable, and add F_cons, the theory constraints between these variables   ▷ hole: transitivity constraints, or more
L7  ν ← SAT(the CNF of the result)                                 ▷ for example by the Tseitin transformation
L8  if ν = nil then return UNSAT else return SAT, the values decoded from ν
```

**Function elimination (line L2).** [Ackermannization](/ackermannization/) replaces $f(t_1), \ldots, f(t_r)$ by fresh constants $F_1, \ldots, F_r$ and adds $t_i = t_j \rightarrow F_i = F_j$ for each pair. The Bryant, German and Velev method replaces $f(t_j)$ by the term $\mathrm{ite}(t_j = t_1, F_1, \mathrm{ite}(t_j = t_2, F_2, \ldots F_j))$, which keeps the polarity of equalities and allows the *positive equality* optimization. Both are equisatisfiable, and both add $O(r^2)$ for $r$ applications of one function. The Handbook (Section 33.3.1.4) notes that after lambda removal the growth is at most quadratic.

**Small-domain encoding (line L5).** It rests on a solution bound. For equality logic with $n$ constants, a satisfying assignment can use values in $\{0, \ldots, n - 1\}$ (Handbook, Theorem 33.3.2). *Proof.* Take any model, and number the distinct values of the $n$ constants in it as $0, 1, \ldots$. At most $n$ numbers are used. Two constants get the same number exactly when they had the same value, so every equality and disequality keeps its truth value. $\square$ So each constant needs $\lceil \log_2 n \rceil$ Boolean variables, and $x = y$ becomes the equality of two bit vectors. For difference logic over $n$ constants with constants of absolute value at most $b_{\max}$, the range $\{0, \ldots, n (b_{\max} + 1)\}$ is enough (Theorem 33.3.3), and Table 33.1 of the Handbook gives bounds for UTVPI and for general linear constraints. A smaller domain for each class, or for each constant by range allocation, keeps the encoding small.

**Per-constraint encoding (line L6).** It is also called the direct encoding. For equality logic, $F_\mathrm{cons}$ forbids each cycle of the constraint graph with exactly one false edge. Bryant and Velev make the graph chordal by adding edges, and then the transitivity constraints of its triangles are enough, with a worst-case size cubic in the number of equalities. For difference logic the added edges can be exponentially many, and for general linear arithmetic the Fourier-Motzkin style constraints can be doubly exponential (Handbook, Table 33.2).

**Correctness.** Each step keeps satisfiability: ite and function elimination are equisatisfiable rewrites, the small-domain bound keeps at least one model if any exists, and $F_\mathrm{cons}$ rules out exactly the propositional models whose refinement is not consistent in the theory. A model of $\varphi_{\mathrm{bool}}$ decodes into values, and these values with the functions read back from the $F_i$ satisfy $\varphi$.

### A worked example

Take the EUF formula $(a = b \vee a = c) \wedge f(a) \ne f(b) \wedge f(a) \ne f(c)$, which is unsatisfiable.

*Line L2.* Write $F_1, F_2, F_3$ for $f(a), f(b), f(c)$. Ackermannization gives

$$(a = b \vee a = c) \wedge F_1 \ne F_2 \wedge F_1 \ne F_3 \wedge (a = b \rightarrow F_1 = F_2) \wedge (a = c \rightarrow F_1 = F_3) \wedge (b = c \rightarrow F_2 = F_3).$$

This is an equality logic formula over $n = 6$ constants.

*Line L3.* The classes are $\{a, b, c\}$ and $\{F_1, F_2, F_3\}$, because no atom compares a constant of one class with one of the other.

*Small domain.* With one class of 6 constants, each needs $\lceil \log_2 6 \rceil = 3$ Boolean variables, 18 in all. With the two classes, each constant needs only values $\{0, 1, 2\}$, so 2 Boolean variables each, 12 in all. A script tried all $6^6$ assignments over $\{0, \ldots, 5\}$ and all $3^6$ over $\{0, 1, 2\}$, and found no solution in either.

*Per-constraint.* Use one variable for each edge of the constraint graph: $e_{ab}, e_{ac}, e_{bc}$ and $e_{12}, e_{13}, e_{23}$. The graph is two triangles, which are chordal already, so $F_\mathrm{cons}$ is the 6 clauses $e_{ab} \wedge e_{bc} \rightarrow e_{ac}$ and so on, three for each triangle. With the 3 consistency clauses and the abstracted body, the 64 assignments of the 6 variables give no model, so the formula is unsatisfiable.

*A satisfiable variant.* Drop $f(a) \ne f(c)$. The per-constraint encoding then has exactly one model: $e_{ac}$ and $e_{13}$ are true and the other four are false. It decodes to $a = c \ne b$ and $F_1 = F_3 \ne F_2$. The small-domain encoding over $\{0, 1, 2\}$ has 36 models, for example $a = 0, b = 1, c = 0, F_1 = 0, F_2 = 1, F_3 = 0$, which gives $f(0) = 0$ and $f(1) = 1$.

## Classic examples

- **UCLID.** Bryant, Lahiri and Seshia built a solver for counter arithmetic with lambda expressions and uninterpreted functions. It removes lambdas and functions, and then picks a small-domain or a per-constraint encoding for each class of constants, by a rule learned from earlier formulas (Handbook, Section 33.3.4).
- **[Bit-blasting](/bit-blasting/).** Each bit-vector variable becomes its bits, and each operation a circuit. Solvers such as STP, Boolector and Bitwuzla use it after word-level rewriting. It is the eager approach for a theory whose domain is finite by definition.
- **Processor verification with uninterpreted functions.** Burch and Dill, and later Bryant, German and Velev, abstracted the data path of a processor by free functions and decided the result by an eager encoding with positive equality.
- **[EUF satisfiability](/euf-satisfiability/) by [Ackermannization](/ackermannization/).** The reduction of free functions to equality logic is the first step of every eager EUF solver.
- **Separation logic.** Strichman, Seshia and Bryant gave the per-constraint encoding of [difference logic](/difference-logic-satisfiability/) by transitivity constraints.

## Variations

- **Hybrid encodings.** Encode some classes with a small domain and others per constraint, and choose for each class (Handbook, Section 33.3.4).
- **Lazy domain growth.** Kroening and others start with a small domain, and grow it only for the constants that a proof of unsatisfiability shows to be too small (Handbook, Section 33.7.1). This uses the eager encoding inside a lazy loop.
- **Lazy bit-blasting.** Bit-blast cheap operations at once, and expensive ones, such as multiplication and division, only when an abstract model needs them.
- **Ackermannization inside a lazy solver.** A lazy solver for a theory without free functions can remove them first by Ackermann's reduction (Handbook, Section 33.6.4), which avoids [theory combination](/nelson-oppen/) with EUF.
- **Static learning.** A lazy solver can add a few cheap theory clauses before the search. It is a small eager step inside the lazy approach, see [Boolean abstraction](/boolean-abstraction/).

## Pitfalls

- **Size blow-up.** The per-constraint encoding of difference logic can be exponential, and of linear arithmetic doubly exponential. The small-domain bound for general linear arithmetic has an $m \log m$ term in the number of bits, which makes the SAT problem too large for thousands of constraints (Handbook, Section 33.3.2).
- **Bounds that are too small.** A domain bound must hold for the whole class. If two classes are merged by a later rewrite, the old bound can be too small, and a satisfiable formula then gets the answer UNSAT.
- **Integer and real domains.** The small-domain bounds are for integers. Over the reals, a strict inequality has no small integer solution in general, so the formula must first be changed, for example by scaling.
- **Modular arithmetic.** A bit-vector circuit computes modulo $2^w$. An encoding of integer arithmetic with bit vectors must make the domain large enough that no intermediate result overflows, or add overflow checks.
- **Losing the structure.** After translation, the SAT solver sees only bits. A theory fact that a theory solver would see at once, such as $x < y \wedge y < x$, may need a long search over bits.

## Exercises

1. Prove that the Bryant, German and Velev ite elimination preserves satisfiability.
2. For an equality logic formula whose constraint graph is a cycle of length $\ell$, how many transitivity constraints does the chordal method add, and how many new edges?
3. Extend the proof of the small-domain bound to $n$ constants that may also be compared with numeric literals $c_1, \ldots, c_s$. What domain is enough?

## References
