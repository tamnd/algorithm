---
tag: 7HH64C
kind: theorem
slug: semi-unification-undecidability
name: Undecidability of semi-unification
aliases:
- semi-unification is undecidable
- Kfoury-Tiuryn-Urzyczyn theorem
area: logic-and-constraints/unification-and-resolution
level: research
summary: Semi-unification is undecidable, proved by Kfoury, Tiuryn and Urzyczyn with a reduction from Turing machine boundedness; so type inference with polymorphic recursion is undecidable.
prereqs: [semi-unification-problem, undecidability, turing-machine]
see_also: [semi-unification-problem, unification-problem, halting-problem, undecidability-of-unification-modulo-theories, post-correspondence-problem, lambda-calculus, mgu-existence-theorem]
sources:
  - paper: doi:10.1006/inco.1993.1003
    title: A. J. Kfoury, J. Tiuryn and P. Urzyczyn, The undecidability of the semi-unification problem, Information and Computation 102(1), 1993, pages 83 to 101
    locator: the main theorem and its proof by reduction from the boundedness problem for Turing machines
  - paper: "P. K. Hooper, The undecidability of the Turing machine immortality problem, Journal of Symbolic Logic 31(2), 1966, pages 219 to 234"
    locator: the theorem that it is undecidable whether a Turing machine has an immortal configuration
  - paper: "A. J. Kfoury, J. Tiuryn and P. Urzyczyn, Type reconstruction in the presence of polymorphic recursion, ACM Transactions on Programming Languages and Systems 15(2), 1993"
    locator: the log-space equivalence of typability with polymorphic recursion and semi-unification, and the resulting undecidability
  - paper: "F. Henglein, Type inference with polymorphic recursion, ACM Transactions on Programming Languages and Systems 15(2), 1993"
    locator: the reductions between type inference in the Milner-Mycroft calculus and semi-unification
  - paper: "A. Dudenhefner, Undecidability of semi-unification on a napkin, 5th International Conference on Formal Structures for Computation and Deduction (FSCD 2020), LIPIcs volume 167, 2020"
    locator: a simpler reduction from Turing machine boundedness through simple stack machines, mechanized in Coq
  - paper: "A. Mycroft, Polymorphic type schemes and recursive definitions, International Symposium on Programming, Lecture Notes in Computer Science 167, Springer, 1984"
    locator: the proposal of polymorphic recursion for ML-style type systems
---

The **undecidability of semi-unification** is the theorem that no algorithm decides, for every finite system of inequalities $s_i \le t_i$ between first-order terms, whether a [semi-unifier](/semi-unification-problem/) exists. A. J. Kfoury, J. Tiuryn and P. Urzyczyn proved it in 1990 (journal version 1993) by a reduction from the boundedness problem for [Turing machines](/turing-machine/), which is undecidable by Hooper's theorem on immortal configurations. Since typability in ML with polymorphic recursion is equivalent to semi-unification, the theorem also shows that type inference with polymorphic recursion is [undecidable](/undecidability/). It contrasts with the [unification problem](/unification-problem/), which is solvable in linear time.

## Statement

A **semi-unifier** of a finite system $\Gamma = \{s_1 \le t_1, \ldots, s_n \le t_n\}$ of inequalities between first-order terms is a substitution $\sigma$ such that, for each $i$, some substitution $\rho_i$ satisfies $s_i\sigma\rho_i = t_i\sigma$.

**Theorem (Kfoury, Tiuryn and Urzyczyn 1993).** The set of finite systems $\Gamma$ that have a semi-unifier is recursively enumerable but not decidable. So its complement is not recursively enumerable.

**Corollary (Kfoury, Tiuryn and Urzyczyn 1993, Henglein 1993).** Typability in the Milner-Mycroft calculus, the core of ML extended with polymorphic recursion, is undecidable.

## In plain words

Semi-unification asks for one way to fill the blanks of several pairs of patterns, so that in each pair the right pattern becomes a copy of the left pattern with its own extra filling. A computer can search all fillings, and it finds an answer whenever one exists. The theorem says that no program can also say "no" in every case where no answer exists.

The proof turns any Turing machine into such a set of pairs. The pairs have an answer exactly when the machine, started anywhere, always stops within some fixed number of steps. Whether a machine has this property is a known undecidable question. A type checker for functions that call themselves at new types would have to solve this question, which is why such languages ask the programmer for type annotations.

## Proof

The [proof file](proofs/main.md) has the status of a sketch: it proves the frame of the argument in full and outlines the central reduction. The argument has four parts.

1. **Semi-unifiability is semi-decidable.** List all tuples $(\sigma, \rho_1, \ldots, \rho_n)$ of finite substitutions and test each one. The search halts exactly on the semi-unifiable systems.
2. **Boundedness is undecidable.** A deterministic Turing machine $M$ is **bounded** if some $n$ bounds the number of steps before it halts, from every configuration: any state, any head position and any tape content. A configuration is **immortal** if $M$ never halts from it. The first $k$ steps from a configuration depend only on the state and the cells within distance $k$ of the head. With this locality and König's lemma, $M$ is bounded if and only if it has no immortal configuration. Hooper (1966) proved that the existence of an immortal configuration is undecidable, so boundedness is undecidable. Boundedness is semi-decidable, by testing all windows of radius $n$ for $n = 1, 2, \ldots$.
3. **The reduction.** Kfoury, Tiuryn and Urzyczyn give a computable map from a machine $M$ to a system $\Gamma_M$ such that $M$ is bounded if and only if $\Gamma_M$ is semi-unifiable. The idea is that configurations are coded by terms, the residual substitutions follow transitions, and the shared $\sigma$ must contain a finite record of all runs. A finite record exists exactly when all runs are bounded. Both problems are recursively enumerable, which fixes the direction: bounded machines map to semi-unifiable systems.
4. **Conclusion.** A decision procedure for semi-unification would, through $\Gamma_M$, decide boundedness, which contradicts part 2.

For the corollary, an expression of the Milner-Mycroft calculus gives one inequality for each recursive use of a function at an instance of its type. The expression is typable if and only if the system is semi-unifiable, and the translation also goes in the other direction. These reductions are in log space, so the two problems are equivalent.

## Consequences

- **No complete type inference for polymorphic recursion.** A compiler cannot infer the most general types of all programs that use polymorphic recursion. Haskell accepts polymorphic recursion only when the function has an explicit type signature, and OCaml needs an explicit polymorphic annotation. With the annotation, type checking needs only unification.
- **Only semi-decision procedures in general.** Since the complement is not recursively enumerable, every sound procedure that reports "not semi-unifiable" must fail to halt on some inputs, or must be restricted to a subclass.
- **Loop detection in rewriting.** Semi-unification gives a sufficient test for the nontermination of a [rewrite rule](/rewrite-rule/). The theorem shows that this test cannot be decided in full generality.
- **Separation from unification.** Unification is the special case of a single inequality $g(z, z) \le g(s, t)$, and it is solvable in linear time. Small changes to the definition move the problem from linear time to undecidable.

## Tightness

- **One inequality.** Semi-unification with a single inequality is decidable (Kapur, Musser, Narendran and Stillman 1991). Systems with one shared residual substitution reduce to one inequality by tupling, so uniform semi-unification is decidable too.
- **Unification and matching.** These special cases are decidable in linear time.
- **Recursive enumerability.** The theorem cannot be strengthened to say that the semi-unifiable systems are not recursively enumerable: they are, by part 1 of the proof.

## History

Semi-unification was studied in two areas. In term rewriting it arises in tests for looping rewrite sequences. In type theory, Mycroft (1984) proposed polymorphic recursion for ML, and the type inference problem for it was shown to be equivalent to semi-unification by Kfoury, Tiuryn and Urzyczyn and by Henglein. The decidability of semi-unification was then open. Kfoury, Tiuryn and Urzyczyn proved it undecidable in a paper at the ACM Symposium on Theory of Computing in 1990, with the journal version in Information and Computation in 1993, by reduction from Turing machine boundedness and Hooper's immortality theorem of 1966. Dudenhefner (2020) gave a simpler reduction and mechanized it in Coq.

## References
