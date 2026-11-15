---
tag: 56VVW9
kind: problem
slug: loop-invariant-synthesis
name: Loop invariant synthesis
aliases:
- invariant generation
- invariant inference
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Find an inductive loop invariant strong enough to prove a program's specification. Undecidable in general, solved for restricted invariant shapes.
prereqs: [loop-invariant, inductive-invariant, verification-condition-generation]
see_also: [houdini-algorithm, farkas-invariant-generation, abstract-interpretation, predicate-abstraction, ic3-pdr, syntax-guided-synthesis, polyhedra-domain, rice-theorem]
sources:
  - paper: doi:10.1145/512760.512770
    title: Patrick Cousot and Nicolas Halbwachs, Automatic discovery of linear restraints among variables of a program, Proceedings of POPL 1978
    locator: pp. 84 to 96, the convex polyhedra analysis with widening
  - paper: doi:10.1007/3-540-45251-6_29
    title: Cormac Flanagan and K. Rustan M. Leino, Houdini, an annotation assistant for ESC/Java, Proceedings of FME 2001, LNCS 2021
    locator: pp. 500 to 517, the guess-and-check loop over candidate annotations
  - paper: doi:10.1007/978-3-540-45069-6_39
    title: Michael A. Colón, Sriram Sankaranarayanan and Henny B. Sipma, Linear invariant generation using non-linear constraint solving, Proceedings of CAV 2003, LNCS 2725
    locator: pp. 420 to 432, Sections 2 and 3 (inductive assertion maps, templates and the Farkas constraints) and Theorem 2
  - paper: doi:10.1016/j.ipl.2004.05.004
    title: Markus Müller-Olm and Helmut Seidl, Computing polynomial program invariants, Information Processing Letters 91(5), 2004
    locator: pp. 233 to 244, the computation of all polynomial equalities of bounded degree for affine programs
  - paper: doi:10.1145/3209108.3209142
    title: Ehud Hrushovski, Joël Ouaknine, Amaury Pouly and James Worrell, Polynomial invariants for affine programs, Proceedings of LICS 2018
    locator: pp. 530 to 539, the algorithm for the strongest polynomial invariant of an affine program
---

Loop invariant synthesis asks for a formula that holds at the head of a loop on every visit, is preserved by one turn of the body, and is strong enough to give the postcondition at the exit. Such an [inductive invariant](/inductive-invariant/) is exactly what [verification condition generation](/verification-condition-generation/) needs at each loop, and finding it is the creative part of a correctness proof. The problem is undecidable in general, by a reduction from the [halting problem](/halting-problem/). Every practical method restricts the shape of the invariant: conjunctions of given candidates, linear inequalities, polynomial equalities, or predicates from a fixed set.

## In plain words

To prove that a loop does its job, you need a fact that is true every time the loop is about to run its body again. The fact must be true the first time. If it is true before one turn, it must be true after that turn. And when the loop stops, the fact must be enough to show the result is right. Finding such a fact is hard. A fact that is true is often not enough, because it is too weak to survive one turn on its own, so you must add more to it. Tools search for these facts by guessing many simple ones and throwing out the bad ones, by solving equations for unknown numbers in a fixed pattern, or by running a rough version of the program that only tracks shapes such as ranges of values.

## Definition

A *loop* is a tuple $(P, b, S, Q)$: a precondition $P$ on the states that reach the loop, a guard $b$, a loop-free body $S$, and a postcondition $Q$. States map the program variables to integers. Write $\mathrm{wlp}(S, I)$ for the [weakest liberal precondition](/weakest-precondition/).

**Input.** A loop $(P, b, S, Q)$ and a set $\mathcal{L}$ of candidate invariants, given as formulas or as sets of states.

**Output.** An $I \in \mathcal{L}$ with

1. *initiation*: $P \implies I$,
2. *consecution*: $I \wedge b \implies \mathrm{wlp}(S, I)$,
3. *safety*: $I \wedge \neg b \implies Q$,

or the answer that there is none. An $I$ that meets 1 and 2 is an *inductive invariant*; condition 3 makes it *adequate* for $Q$. These are the three verification conditions of the loop.

**Fact (semantic completeness).** When $\mathcal{L}$ is the set of all sets of states, an adequate inductive invariant exists exactly when the triple $\{P\}\ \mathbf{while}\ b\ \mathbf{do}\ S\ \{Q\}$ holds for [partial correctness](/partial-correctness/). One direction is the soundness of the loop rule of [Hoare logic](/hoare-logic/). For the other, take $I = H$, the set of states that some run from $P$ has at the loop head. $P \subseteq H$. A state of $H \wedge b$ runs the body to another state of $H$. A state of $H \wedge \neg b$ is a final state of the loop, so it satisfies $Q$ because the triple holds. $H$ is the least fixed point in the loop rule of the [strongest postcondition](/strongest-postcondition/) page.

## Variants

- **Without a target.** Find the strongest invariant in $\mathcal{L}$, or any invariant in $\mathcal{L}$, with no $Q$. Abstract interpretation answers this form.
- **Template synthesis.** $\mathcal{L}$ is a fixed shape with unknown coefficients, such as $c_1 x + c_2 y + d \le 0$, and the answer is a choice of coefficients. See [constraint-based invariant generation](/farkas-invariant-generation/).
- **Candidate selection.** $\mathcal{L}$ is the set of conjunctions of a finite list of candidate formulas. See [Houdini](/houdini-algorithm/).
- **Programs, not single loops.** Several loops, nested loops and procedures need an invariant at each cut point at once. The conditions become a system of constrained Horn clauses over unknown predicates.
- **Integers or rationals.** Many methods work over $\mathbb{Q}$, where linear programming is available. An invariant that is inductive over $\mathbb{Z}$ need not be inductive over $\mathbb{Q}$, so these methods can miss it.
- **Other theories.** Arrays and heaps need quantified invariants, such as "every element before $i$ is sorted", and pointer programs need [separation logic](/separation-logic/).

## Examples

- **Division.** For $q := 0; r := x; \mathbf{while}\ y \le r\ \mathbf{do}\ (r := r - y; q := q + 1)$ with $P$: $x \ge 0 \wedge y > 0$ and $Q$: $x = qy + r \wedge 0 \le r < y$, the invariant $x = qy + r \wedge r \ge 0$ is adequate. The weaker $x = qy + r$ is inductive but not adequate. The [VC generation](/verification-condition-generation/) page works it out.
- **A true fact that is not inductive.** For $x := 0; y := 0; \mathbf{while}\ \ast\ \mathbf{do}\ (x := x + y; y := y + 1)$, every head state has $x \ge 0$. But $x \ge 0$ alone is not inductive: from $x = 0$, $y = -5$ one turn gives $x = -5$. The conjunction $x \ge 0 \wedge y \ge 0$ is inductive. Strengthening a true fact until it is inductive is the core of the problem.
- **Strengthening for the exit.** For $i := 0; j := 0; \mathbf{while}\ i < n\ \mathbf{do}\ (i := i + 1; j := j + 2)$ with $P$: $n \ge 0$ and $Q$: $j = 2n$, the formula $j = 2i$ is inductive, but at the exit it only gives $i \ge n \wedge j = 2i$. The adequate invariant is $j = 2i \wedge i \le n$, and the exit then forces $i = n$.
- **Only a polynomial works.** For $x := 0; y := 0; \mathbf{while}\ x < n\ \mathbf{do}\ (y := y + 2x + 1; x := x + 1)$ with $P$: $n \ge 0$ and $Q$: $y = n^2$, the adequate invariant is $y = x^2 \wedge x \le n$. No conjunction of linear inequalities over $x$, $y$, $n$ is adequate. Such a set is convex. The run with $n = 2$ has the head states $(x, y, n) = (0, 0, 2)$ and $(2, 4, 2)$, so a convex invariant also contains their midpoint $(1, 2, 2)$. Consecution then forces the next state $(2, 5, 2)$, where the loop exits with $y = 5 \ne 4$. So the methods for linear invariants fail here, and polynomial methods succeed.
- **An invariant that is not convex.** For $x := 1; \mathbf{while}\ x \ne 0\ \mathbf{do}\ x := x - 2$ with $Q$: $\mathit{false}$, the loop never exits, so the triple holds. An adequate invariant must contain $1$ and $-1$ and must not contain the exit state $0$, their midpoint. So no conjunction of linear inequalities works, and "$x$ is odd" does.
- **No invariant at all.** With the body $x := x - 1$ the loop exits at $x = 0$, the triple with $Q$: $\mathit{false}$ fails, and no adequate invariant exists in any language.

## Known algorithms

- **[Abstract interpretation](/abstract-interpretation/).** Computes an inductive invariant without a target, as a fixed point in an [abstract domain](/abstract-domain/): [intervals](/interval-domain/), [octagons](/octagon-domain/) or [convex polyhedra](/polyhedra-domain/) (Cousot and Halbwachs), with a [widening operator](/widening-operator/) to stop. Sound and terminating, but the result may be too weak for $Q$.
- **[Houdini](/houdini-algorithm/).** Finds the largest inductive conjunction of $c$ given candidates with at most $c + 1$ calls to a validity checker.
- **[Constraint-based generation](/farkas-invariant-generation/).** Fixes a linear template and turns the three conditions into constraints on the coefficients by [Farkas' lemma](/farkas-lemma/). Complete for the template over the rationals.
- **[Predicate abstraction](/predicate-abstraction/) with [CEGAR](/cegar/).** Finds the strongest invariant that is a boolean combination of a set of predicates, and adds predicates from spurious counterexamples.
- **Interpolation and [IC3/PDR](/ic3-pdr/).** Build the invariant from proofs that short runs cannot reach a bad state; see [interpolation-based model checking](/interpolation-based-model-checking/). [k-induction](/k-induction/) proves the property with a weaker form of induction instead.
- **Polynomial equalities.** For affine programs, Müller-Olm and Seidl compute all polynomial equalities up to a given degree by linear algebra, and Hrushovski, Ouaknine, Pouly and Worrell compute the strongest polynomial invariant of any degree. [Gröbner bases](/groebner-basis/) are the tool for the general case.
- **Learning from data.** Sample states, then fit a formula that separates good states from bad ones, and repair it with counterexamples from a solver, in the style of [CEGIS](/cegis/). [Syntax-guided synthesis](/syntax-guided-synthesis/) has a track for invariant problems in this form.

## Bounds

**Theorem.** It is undecidable whether a loop over integer variables, with assignments of the form $x := x + 1$, $x := x - 1$ and tests $x = 0$, has an adequate inductive invariant (with $\mathcal{L}$ all sets of states). The set of loops that have one is co-recursively enumerable and not recursively enumerable.

*Proof.* By the fact of the definition, the question is whether $\{P\}\ \mathbf{while}\ b\ \mathbf{do}\ S\ \{Q\}$ holds. We reduce from the halting problem of two-counter machines, which Minsky proved undecidable; such a machine can simulate any [Turing machine](/turing-machine/). A two-counter machine has a finite list of instructions: "add 1 to $c_i$ and go to $k$", and "if $c_i = 0$ go to $k$, else subtract 1 and go to $k'$", and a halt instruction $h$. Build the loop with variables $\mathit{pc}$, $c_1$ and $c_2$: $P$ is $\mathit{pc} = 1 \wedge c_1 = 0 \wedge c_2 = 0$, the guard is $\mathit{pc} \ne h$, the body is a chain of ifs on $\mathit{pc}$ that runs one instruction, and $Q$ is $\mathit{false}$. Each turn of the loop is one step of the machine, so the loop exits exactly when the machine halts. The triple with $Q = \mathit{false}$ holds exactly when the loop never exits, that is, when the machine does not halt. So deciding the existence of an invariant decides the halting problem. The complement, "the machine halts", is recursively enumerable and undecidable, so the set of loops with an invariant is co-r.e. and not r.e. $\square$

This is also an instance of [Rice's theorem](/rice-theorem/): "the triple holds" is a property of what the program computes, and it is not trivial. The same proof works for any language $\mathcal{L}$ that can define the set $H$ of head states, such as first-order arithmetic with $+$ and $\times$, which defines every set that a program reaches.

**Decidable cases.** The problem becomes decidable when the search space is finite or has a decidable structure, given a decision procedure for the three conditions:

- For conjunctions of $c$ candidates, Houdini decides it with at most $c + 1$ calls, when consecution is checked by a [decision procedure](/decision-procedure/), for example for [Presburger arithmetic](/presburger-arithmetic/).
- For a fixed linear template on a loop with linear guards and updates, over the rationals, the Farkas constraints are a formula of the first-order theory of the real numbers, which is decidable by the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/), for example by [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/).
- For Presburger invariants of a loop with linear guards and updates, the three conditions are Presburger formulas, so enumerating formulas and checking them is a semi-decision procedure: it finds an invariant when one exists, and may run forever otherwise.

## Reductions

- **To validity.** Checking a proposed $I$ is three validity questions, so synthesis reduces to search plus a decision procedure, which is the shape of Houdini and of [CEGIS](/cegis/).
- **From safety verification.** A program is safe exactly when its loops have adequate inductive invariants (semantic completeness), so every [model checking](/reachability-problem/) method for infinite-state programs is, in effect, an invariant synthesizer. Constrained Horn clause solvers state the problem in this form.
- **From termination.** A proof of termination with a [ranking function](/ranking-function-synthesis/) often needs a supporting invariant, such as $y > 0$, before the ranking function decreases. Tools synthesize both together.

## Applications

Deductive verifiers ask the programmer for invariants and use synthesis to fill the easy ones. ESC/Java used Houdini for this. Static analyzers for safety-critical code compute numeric invariants with abstract interpretation to rule out overflow and out-of-bounds access. Compilers use simple invariants, such as the range of an induction variable, to remove bounds checks. Termination provers and [proof-carrying code](/proof-carrying-code/) producers need invariants to build their certificates.

## References
