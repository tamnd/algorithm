---
tag: CNQBEV
kind: definition
slug: smt-lib
name: SMT-LIB standard
aliases:
- SMT-LIB
- SMT-LIB 2
- SMT-LIB language
- SMT-LIB format
area: logic-and-constraints/smt
level: intro
summary: The common standard of SMT solvers. It defines a sorted first-order logic, a catalog of theories and logics, and a command language for scripts with push, pop, check-sat and get-model.
prereqs: [smt-problem]
see_also: [incremental-solving, unsat-core, decision-procedure, euf-satisfiability, linear-integer-arithmetic-satisfiability, bit-vector-satisfiability, array-theory-satisfiability, e-matching]
sources:
  - url: https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf
    title: Clark Barrett, Pascal Fontaine and Cesare Tinelli, The SMT-LIB Standard, Version 2.7, release of July 7, 2025
    locator: Section 1.1.2 (changes from Version 2.6), Section 1.2 (the initiative and its goals), Chapter 2 (logic, theories, logics, scripts), Sections 3.6.5, 3.7, 3.10 and 3.11, Chapter 4 (operational semantics), Sections 5.4 and 5.5
  - url: https://smt-lib.org/logics.shtml
    title: The SMT-LIB Initiative, SMT-LIB logics
    locator: the list of logics, the naming conventions for logic names, and the note on array sorts in QF_AUFLIA
  - url: https://smt-lib.org/theories.shtml
    title: The SMT-LIB Initiative, SMT-LIB theories
    locator: the catalog of theory declarations (Core, ArraysEx, FixedSizeBitVectors, FloatingPoint, HO-Core, Ints, Reals, Reals_Ints, Strings)
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.2 (theories and the ground T-satisfiability problem that SMT-LIB standardizes)
---

SMT-LIB is the common standard of SMT solvers. It is the work of the SMT-LIB initiative, which started in 2003, and its reference document is written by Clark Barrett, Pascal Fontaine and Cesare Tinelli. The current version, 2.7, defines four things: a language of terms and formulas in a sorted version of first-order logic, a language to specify background theories, a language to specify logics, and a command language to talk to a solver through a text interface. The same name also refers to the library of benchmarks in this format. Because almost all SMT solvers read SMT-LIB scripts, a tool can change its solver without changing its encoding, and solvers can be compared on the same benchmarks, as in the yearly competition SMT-COMP. This page describes the standard only as its reference document and the SMT-LIB web pages state it.

## Definition

**The initiative and its goals.** The standard (Section 1.2) gives three goals: to give standard rigorous descriptions of background theories used in SMT systems, to develop and promote common input and output languages for SMT solvers, and to collect a large library of benchmarks. The standard says that the library contains more than 400,000 benchmarks.

**The problem.** The standard (Section 2.1) states the SMT problem as the question of whether a formula $\varphi$ is satisfiable in a background theory $T$, that is, "whether there is a model of $T$ that makes $\varphi$ true". SMT-LIB deals only with satisfiability. Entailment is checked through the unsatisfiability of a negation. See [SMT problem](/smt-problem/).

**The underlying logic.** The logic is a many-sorted first-order logic with equality (Section 2.2). Formulas are terms of the sort `Bool`, so there is no separate syntax category for formulas. Sorts can be built from sort constructors, for example `(List (Array Int Real))`. Terms have the binders `let`, `forall`, `exists` and `match`. Version 2.6 added algebraic datatypes, and Version 2.7 adds three things: a sort constructor `->` for maps, a binder `lambda` with an application symbol `@`, and rank-1 polymorphism by the command `declare-sort-parameter`. Maps are values like all others, and they are not identified with declared functions, so the logic stays first order. The standard says that Version 3 will be based on higher-order logic. All sorts have non-empty domains.

**Theories.** In SMT-LIB, a $\Sigma$-theory is a class of $\Sigma$-structures, not a set of axioms (Section 5.4, Definition 12). Typical theories have one model, such as the integers, or are the class of all models of a set of axioms, which need not be finite or even recursive. A *theory declaration* (Section 3.7) gives a name, the sorts, the function symbols with their ranks, and, mostly in English text, the definition. The standard calls theory declarations mostly documentation: only the signature is formal, and only when it is finite. The bit-vector theory has infinitely many sorts, one for each width, so its signature is given in English. The catalog on the web site has the theories Core, ArraysEx, FixedSizeBitVectors, FloatingPoint, HO-Core, Ints, Reals, Reals_Ints and Strings. Core defines the Boolean operators, equality, `distinct` and `ite`, and the standard says that it is implicitly included in every other theory declaration. *Combined theories* are combinations $T_1 + \cdots + T_n$ of basic ones, defined as all structures whose restriction to the signature of each $T_i$ is isomorphic to a model of $T_i$ (Definition 13).

**Logics.** A *logic* (Sections 2.4 and 5.5) fixes a signature, restricts the structures to the models of a theory, and restricts the formulas to a sublanguage. A logic declaration has the attributes `:theories` and `:language`, each exactly once, and may have `:extensions`, `:values` and `:notes` (Section 3.10). The language is described in English. For example, QF_LIA is the logic of closed quantifier-free formulas over the integers with free constants, in which every atom is linear, so `*` occurs only with a numeral as one argument.

**Logic names.** The logics page gives the conventions for the names, and it calls them "mostly historical".

| part of name | meaning |
|---|---|
| `QF_` | quantifier-free formulas only |
| `A` or `AX` | the theory ArraysEx |
| `UF` | free sort and function symbols |
| `BV` | the theory FixedSizeBitVectors |
| `FP` | the theory FloatingPoint |
| `IA`, `RA`, `IRA` | the theory Ints, Reals or Reals_Ints |
| `L` before `IA`, `RA`, `IRA` | linear arithmetic only |
| `N` before `IA`, `RA`, `IRA` | arithmetic that can be nonlinear |
| `IDL`, `RDL` | integer or real difference logic |

The parts appear in the order of this table. So QF_UFLIA is quantifier-free formulas over free symbols and linear integer arithmetic, and AUFLIRA is formulas with quantifiers over arrays, free symbols and linear arithmetic over the integers and the reals. Each benchmark in the library is classified under the smallest logic that contains it.

**Scripts and commands.** A *script* is a sequence of commands (Section 3.11). The syntax uses S-expressions, as in Lisp. A solver is meant to work as a read-eval-print loop: it reads a command, writes a response, and waits for the next one. Reading a script from a file must give the same output. The main commands are the following.

- `set-logic` chooses the logic. `set-option` and `set-info` set options and information.
- `declare-sort`, `declare-fun`, `declare-const`, `define-fun`, `define-fun-rec`, `define-const` and `declare-datatypes` introduce symbols.
- `assert` adds a formula to the current *assertion level*. `push n` adds $n$ levels to the *assertion stack*, and `pop n` removes the $n$ top levels, with their assertions and, by default, their declarations. The first level cannot be removed (Section 4.2.2). See [incremental solving](/incremental-solving/).
- `check-sat-assuming (a1 ... an)` checks whether the conjunction of all asserted formulas and the assumptions $a_1, \ldots, a_n$ is satisfiable. `check-sat` is the same command with no assumptions. The context must be the same after the command as before it (Section 4.2.5).
- After `sat`, the commands `get-model`, `get-value` and `get-assignment` show a model. After `unsat`, the commands `get-unsat-core`, `get-unsat-assumptions` and `get-proof` show why. Each needs an option to be set first, such as `:produce-models` or `:produce-unsat-cores`.
- `reset`, `reset-assertions` and `exit` end or restart the session.

**Responses.** The answer to a check is `sat`, `unsat` or `unknown`. The standard says that `sat` means that the solver has found a model, `unsat` that it has established that there is no model, and `unknown` that "the search was inconclusive", because of resource limits, incompleteness or other reasons. Other commands answer `success`, `unsupported`, or `(error "...")`. A compliant solver is always in one of four *modes*: start mode, assert mode, sat mode and unsat mode (Section 4.1.1). Commands that are not allowed in the current mode give an error.

## Examples and non-examples

**A script from the standard.** This is the example script of Figure 3.11, with the expected responses as comments.

```text
(set-option :print-success true)   ; success
(set-info :smt-lib-version 2.7)    ; success
(set-logic QF_LIA)                 ; success
(declare-const w Int)              ; success
(declare-const x Int)              ; success
(declare-const y Int)              ; success
(declare-const z Int)              ; success
(assert (> x y))                   ; success
(assert (> y z))                   ; success
(push 1)                           ; success
(assert (> z x))                   ; success
(check-sat)                        ; unsat
(get-info :all-statistics)         ; (:time 0.01 :memory 0.2)
(pop 1)                            ; success
(push 1)                           ; success
(check-sat)                        ; sat
(exit)                             ; success
```

The first `check-sat` sees $x > y > z > x$, which has no integer solution. The `pop` removes $z > x$, and the second check sees only $x > y > z$, which has one. The output of `get-info :all-statistics` is specific to the solver, and the standard shows it only as an illustration.

**Names that are logics.** QF_UF ([EUF satisfiability](/euf-satisfiability/)), QF_LIA ([linear integer arithmetic](/linear-integer-arithmetic-satisfiability/)), QF_LRA, QF_IDL ([difference logic](/difference-logic-satisfiability/)), QF_BV ([bit-vectors](/bit-vector-satisfiability/)), QF_AX ([arrays](/array-theory-satisfiability/)), QF_NRA, QF_UFLIA, AUFLIA and UFNIA are all on the list of the logics page.

**A name that does not mean what it seems.** QF_AX is not a sublogic of QF_AUFLIA. The logics page notes that in the logics with `A` and `LIA` the only array sort is `(Array Int Int)`, while QF_AX has arrays over free sorts. So the naming rules do not define the inclusion order of the logics.

**A logic that is not on the list.** The standard (Section 3.10.1) shows that propositional logic and quantified Boolean formulas can also be defined as SMT-LIB logics, both as instances of Core. These declarations are examples in the document, not part of the official catalog.

**Annotations.** The attribute `:named` gives a name to a formula, so that `get-unsat-core` can report it. The attribute `:pattern` gives instantiation patterns for a quantifier. The standard says that patterns "provide heuristic information" to solvers that use quantifier instantiation, as in [E-matching](/e-matching/). They do not change the meaning of the formula.

**Non-example: the proof format.** The command `get-proof` exists, but the standard does not fix the format of the proof: it is specific to each solver. Two compliant solvers can give proofs that no common checker reads.

**Non-example: minimality of cores.** The standard does not require `get-unsat-core` or `get-unsat-assumptions` to give a minimal set. A note in Section 4.2.7 says that the minimization problem alone is NP-hard in general. See [unsat core](/unsat-core/).

**Non-example: a solver API.** The programming interfaces of solvers, such as the C or Python bindings of a solver, are not part of SMT-LIB, and each solver has its own. SMT-LIB is a text format. Also, the DIMACS CNF format of SAT solvers is not part of SMT-LIB, though a CNF formula can be written as a QF_UF script with Boolean constants only.

**Non-example: a decision procedure.** A logic in SMT-LIB need not be decidable. AUFLIA and UFNIA have quantifiers, and QF_NIA has nonlinear integer arithmetic, which is undecidable. A compliant solver may answer `unknown`. Compliance concerns the language and the behaviour of commands, not the power of the solver. See [decision procedure](/decision-procedure/).

## Related definitions

- [SMT problem](/smt-problem/): the problem that an SMT-LIB script states. A script with one `check-sat` is an instance of it, in the logic set by `set-logic`.
- [Incremental solving](/incremental-solving/): the solver technique behind `push`, `pop` and `check-sat-assuming`.
- [Unsat core](/unsat-core/): the answer of `get-unsat-core`, over the assertions labeled with `:named`.
- [Decision procedure](/decision-procedure/): an algorithm that always answers `sat` or `unsat`, never `unknown`, on a decidable logic.
- **Theory** and **logic**: in SMT-LIB, a theory is a class of structures, and a logic is a theory together with a language of formulas. The same theory, such as Ints, is the base of several logics, such as QF_LIA, QF_NIA and QF_IDL.

## References
