---
tag: JSG33Q
kind: problem
slug: inductive-theorem-proving
name: Inductive theorem proving
aliases:
- inductive validity
area: automata-and-parsing/term-rewriting
level: research
summary: Prove equations that hold in the initial algebra of a rewrite system.
prereqs: [equational-theory, term-rewriting-system, structural-induction, knuth-bendix-completion]
see_also: [rewriting-induction, term-algebra, birkhoff-completeness-theorem, unfailing-completion, presburger-arithmetic, godel-incompleteness-theorem, halting-problem, first-order-theorem-proving]
sources:
  - paper: doi:10.1016/0022-0000(82)90006-X
    title: Gérard Huet and Jean-Marie Hullot, Proofs by induction in equational theories with constructors, Journal of Computer and System Sciences 25(2) (1982)
    locator: pp. 239 to 266 (inductive theorems, free constructors, sufficient completeness, and proof by Knuth-Bendix completion)
  - paper: doi:10.1145/567446.567461
    title: David R. Musser, On proving inductive properties of abstract data types, Proceedings of the 7th ACM Symposium on Principles of Programming Languages (POPL 1980)
    locator: pp. 154 to 162 (inductive properties proved by completion, without an explicit induction)
  - book: isbn:9780121229504
    title: Robert S. Boyer and J Strother Moore, A Computational Logic, Academic Press, 1979
    locator: the chapters on induction schemes from recursive definitions, generalization and the heuristics of the prover
  - paper: doi:10.1016/0890-5401(89)90062-X
    title: Jean-Pierre Jouannaud and Emmanuel Kounalis, Automatic proofs by induction in theories without constructors, Information and Computation 82(1) (1989)
    locator: pp. 1 to 33 (proof by consistency with a ground reducibility test)
  - paper: doi:10.1007/3-540-52885-7_86
    title: Uday S. Reddy, Term rewriting induction, 10th International Conference on Automated Deduction (CADE-10), Lecture Notes in Computer Science 449 (1990)
    locator: pp. 162 to 177
  - paper: doi:10.1016/s0890-5401(03)00134-2
    title: Hubert Comon and Florent Jacquemard, Ground reducibility is EXPTIME-complete, Information and Computation 187(1) (2003)
    locator: pp. 123 to 153
---

**Inductive theorem proving** asks whether an equation $s = t$ holds for every ground instance of its variables, given an equational specification or a [term rewriting system](/term-rewriting-system/). Such an equation is an **inductive theorem**: it holds in the initial algebra, the algebra of ground terms modulo the equations, though it may not follow from the equations by equational reasoning. For the rules of addition, $x + 0 = x$ is an inductive theorem but not an equational consequence. The problem is undecidable, and for terminating, confluent systems it is complete for the co-recursively enumerable sets, so no algorithm proves all inductive theorems. The methods in use are explicit induction, in the tradition of Boyer and Moore, and methods based on rewriting: proof by consistency, also called inductionless induction (Musser, 1980; Huet and Hullot, 1982), and [rewriting induction](/rewriting-induction/) (Reddy, 1990).

## In plain words

A set of rules defines functions on data such as numbers or lists. Some statements are true for every concrete value, but you can check them only one value at a time, and there are infinitely many values.

For example, "a number plus zero is the same number" holds for 0, 1, 2 and so on. The rules alone do not let you rewrite "x plus zero" into "x" when x is unknown. You need an argument by induction: it holds for 0, and if it holds for a number, it holds for the next one.

The problem is to find such proofs by machine. Often the statement must first be made more general, or a helper statement must be proved first, and choosing these is the hard part.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, substitutions $\sigma$, and $\to^*$ for the reflexive transitive closure. The ground terms are $T(\Sigma)$, and we assume, as usual in this area, that $\Sigma$ is many-sorted and has a ground term of each sort, so that each variable ranges over the ground terms of its sort.

**Input.** A finite set $E$ of equations over $\Sigma$, often given as a set $R$ of rewrite rules, and an equation $s = t$ between terms of the same sort.

**Question.** Is $s\sigma =_E t\sigma$ for every substitution $\sigma$ that maps the variables of $s$ and $t$ to ground terms? Here $=_E$ is the [equational theory](/equational-theory/) of $E$. If so, $s = t$ is an **inductive theorem** of $E$, written $E \models_{ind} s = t$.

By [Birkhoff's theorem](/birkhoff-completeness-theorem/), $s =_E t$ means that $s = t$ holds in all models of $E$. The inductive theorems are the equations that hold in one model, the **initial algebra** $T(\Sigma)/{=_E}$, whose elements are the classes of ground terms. Every equational consequence is an inductive theorem, but not conversely.

**Constructors.** In most applications $\Sigma$ is split into **constructors**, such as $0$ and $s$ for numbers or $nil$ and $cons$ for lists, and **defined symbols**. The specification is **sufficiently complete** if every ground term is $E$-equal to a ground constructor term, and the constructors are **free** if distinct ground constructor terms are not $E$-equal. Under both conditions, the initial algebra is the set of ground constructor terms, the data values.

## Variants

- **Convergent rewriting systems.** If $R$ is terminating and confluent, $s = t$ is an inductive theorem if and only if $s\sigma$ and $t\sigma$ have the same normal form for every ground $\sigma$. This is the setting of the methods below and of the bounds.
- **With or without constructors.** Huet and Hullot need free constructors and sufficient completeness. Jouannaud and Kounalis replace these by a test for **ground reducibility**: a term is ground reducible if every ground instance of it is reducible.
- **Conditional equations.** Specifications with conditional rules $c \Rightarrow l \to r$, as in functional programs with guards, need conditional inductive theorems.
- **Inductive theorems of programs.** In program verification, the rules are the definitions of a functional program, and the conjectures are properties of the program: an equation, an inequality, or a formula with connectives.
- **Disproof.** Find a ground instance with $s\sigma \ne_E t\sigma$. For a convergent system this is a semi-decision procedure: enumerate the ground instances and compare normal forms.

## Examples

All the examples were checked by a program: the conjectures on all ground instances with numbers up to 5 or lists up to length 5, and the completion runs by computing every critical pair and its normal forms.

**Addition.** Let $R$ be $0 + y \to y$ and $s(x) + y \to s(x + y)$, with the constructors $0$ and $s$.

- $x + 0 = x$ is an inductive theorem. It is not an equational consequence: $x + 0$ and $x$ are distinct normal forms, and $R$ is convergent. Proof by induction on $x$: $0 + 0 \to 0$, and if $x + 0 =_R x$, then $s(x) + 0 \to s(x + 0) =_R s(x)$.
- The same conjecture by proof by consistency: add the rule $x + 0 \to x$. Its [critical pairs](/critical-pair/) with $R$ are $0 + 0$, which gives $0$ and $0$, and $s(x) + 0$, which gives $s(x + 0)$ and $s(x)$, both with the normal form $s(x)$. So $R \cup \{x + 0 \to x\}$ is convergent, its left sides all contain $+$, and the conjecture is proved without an explicit induction.
- $x + s(y) = s(x + y)$ and $(x + y) + z = x + (y + z)$ are proved in the same way: completion adds the oriented conjecture and finds only joinable critical pairs.
- $x + x = x$ is not an inductive theorem. Completion adds $x + x \to x$. The critical pair at $s(x) + s(x)$ gives $s(x + s(x)) = s(x)$, and its instance at $x := 0$ normalizes to $s(s(0)) = s(0)$, an equation between distinct constructor terms. This shows the conjecture is false; indeed $x = s(0)$ is a counterexample.
- $x + y = y + x$ is an inductive theorem, but completion cannot orient it, and an induction on $x$ gets stuck at $y = y + 0$ and $s(x + y) = y + s(x)$. With the two lemmas above it goes through. Finding such lemmas is the main difficulty in practice.

**Lists.** With $app(nil, ys) \to ys$, $app(cons(x, xs), ys) \to cons(x, app(xs, ys))$, $rev(nil) \to nil$ and $rev(cons(x, xs)) \to app(rev(xs), cons(x, nil))$, the conjecture $rev(rev(xs)) = xs$ is an inductive theorem. A direct induction on $xs$ needs $rev(app(ys, cons(x, nil))) = cons(x, rev(ys))$, or the more general lemma $rev(app(xs, ys)) = app(rev(ys), rev(xs))$, which in turn needs associativity of $app$ and $app(xs, nil) = xs$.

## Known algorithms

**Explicit induction.** Choose an induction scheme, often suggested by the recursion in the definitions (the cover set of the rules for a defined symbol), prove the base and step cases by rewriting, and use the induction hypothesis as a rule. Boyer and Moore built this into a prover with heuristics for choosing the scheme, generalizing subterms to variables, and discovering lemmas. Its successors include ACL2, and induction tactics in interactive provers follow the same pattern.

**Proof by consistency (inductionless induction).** Let $R$ be convergent and sufficiently complete, with free constructors. Run [Knuth-Bendix completion](/knuth-bendix-completion/) on $R \cup \{s = t\}$.

- If it stops with a convergent system $R'$ in which no left side is a constructor term, then $s = t$ is an inductive theorem.
- If it derives an equation between two distinct ground constructor terms, then $s = t$ is not an inductive theorem.

*Proof.* For the first claim, let $\sigma$ be ground. By sufficient completeness and convergence, $s\sigma \to_R^* c_1$ and $t\sigma \to_R^* c_2$ for ground constructor terms $c_1, c_2$. Completion preserves the equational theory, so $s\sigma =_{R'} t\sigma$, and $R \subseteq R'$ gives $c_1 =_{R'} c_2$. A ground constructor term contains only constructors, so no left side of $R'$ matches inside it, and $c_1, c_2$ are $R'$-normal forms. As $R'$ is convergent, $c_1 = c_2$, so $s\sigma =_R t\sigma$. For the second claim, if $s = t$ is an inductive theorem, then adding it does not change the ground equalities: a proof of a ground equation in $R \cup \{s = t\}$ can be done with ground terms only, because every sort has a ground term, so it uses only ground instances of $s = t$, each of which holds in $R$. So every ground equation derived by completion holds in $R$. Two distinct ground constructor terms are distinct $R$-normal forms, because no left side of $R$ is a constructor term, so they are not $R$-equal. $\blacksquare$

Jouannaud and Kounalis drop the constructor assumptions: the derived rules must have ground reducible left sides, a property that is decidable. Completion may also run forever, without success or failure.

**Rewriting induction.** Reddy's method uses the rewrite relation itself as the induction order. It expands a conjecture by all ways of rewriting its instances at a basic position, and uses the conjecture, oriented, as an induction hypothesis on the smaller terms. Reddy presented it as an explanation of proof by consistency as an induction on the rewrite relation, and it needs fewer critical pairs. Later systems extend it with lemma generation.

**Disproof by enumeration.** For a convergent system, enumerate ground substitutions and compare normal forms. This finds every counterexample, but proves nothing.

## Bounds

**Theorem.** For finite, terminating, confluent many-sorted systems $R$, the set of pairs $(R, s = t)$ such that $s = t$ is an inductive theorem of $R$ is complete for the class of co-recursively enumerable sets ($\Pi^0_1$).

*Proof.* Upper bound: $s = t$ fails to be an inductive theorem if and only if some ground $\sigma$ gives different normal forms. The ground substitutions can be enumerated, and the normal forms computed, because $R$ is finite and terminating. So the complement is recursively enumerable. Hardness: given a Turing machine $M$, write a finite, terminating, confluent constructor system that computes the primitive recursive function $h(n)$, which is $true$ if $M$ halts on the empty input within $n$ steps and $false$ otherwise. Then $h(x) = false$ is an inductive theorem, with $x$ of the sort of numbers, if and only if $M$ never halts. This reduces the complement of the [halting problem](/halting-problem/) to the problem. $\blacksquare$

So the inductive theorems are not recursively enumerable, and no sound proof system, in particular no prover, proves all of them. This is the rewriting form of [Gödel's incompleteness theorem](/godel-incompleteness-theorem/). For more general specifications, where $=_E$ itself is undecidable, the problem is harder still.

**Decidable parts.** Some classes are decidable: equations over the natural numbers with $0$, $s$ and $+$ fall within [Presburger arithmetic](/presburger-arithmetic/), and there are decidable classes of conjectures over restricted function definitions. Ground reducibility, the test used by proof by consistency without constructors, is decidable, and Comon and Jacquemard showed it is EXPTIME-complete.

## Reductions

- **From the halting problem**, for hardness, as in the theorem above.
- **To completion.** Proof by consistency reduces an inductive conjecture to a run of Knuth-Bendix completion, or of [unfailing completion](/unfailing-completion/) for equations that cannot be oriented, plus a consistency test.
- **To first-order proving with an induction schema.** An inductive theorem of a specification with constructors is a consequence of the equations, the freeness axioms, and the induction schema for the constructors, for each instance that the proof uses. A [first-order prover](/first-order-theorem-proving/) can then check each case, and the hard part is choosing the instance.

## Applications

- **Verification of functional programs.** Properties of recursive definitions, such as the correctness of a sorting function or of a compiler for expressions, are inductive theorems. ACL2, Isabelle, Coq and other provers use induction tactics, many with rewriting at their core.
- **Algebraic specification of abstract data types.** The behaviour of a data type defined by equations is given by its initial algebra, and its properties are inductive theorems (Musser, 1980).
- **Properties of rewrite systems.** Sufficient completeness, ground confluence, and the correctness of a transformation on a rewrite system are themselves inductive properties.

## References
