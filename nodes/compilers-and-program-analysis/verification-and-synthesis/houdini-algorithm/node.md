---
tag: 8FP30Z
kind: algorithm
slug: houdini-algorithm
name: Houdini
aliases:
- Houdini annotation inference
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: Guesses many candidate invariants and removes those a verifier refutes until the rest are inductive, the largest such subset.
model: word-ram
complexity:
  vars: {c: the number of candidate invariants, T: the cost of one call of the prover}
  time: {worst: O(c T + c^2)}
  space: {extra: O(c)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2001
  people: [Cormac Flanagan, K. Rustan M. Leino, Rajeev Joshi]
  note: Flanagan and Leino built Houdini as an annotation assistant for ESC/Java (FME 2001); Flanagan, Joshi and Leino gave the theory of the largest solution in the same year.
prereqs: [inductive-invariant, loop-invariant-synthesis]
see_also: [verification-condition-generation, farkas-invariant-generation, predicate-abstraction, abstract-interpretation, ic3-pdr, cegis, smt-problem, k-induction]
sources:
  - paper: doi:10.1007/3-540-45251-6_29
    title: Cormac Flanagan and K. Rustan M. Leino, Houdini, an annotation assistant for ESC/Java, Proceedings of FME 2001, LNCS 2021
    locator: pp. 500 to 517, Section 3 (the Houdini algorithm, the candidate annotations and the refutation loop) and the experience with ESC/Java
  - paper: doi:10.1016/S0020-0190(00)00196-4
    title: Cormac Flanagan, Rajeev Joshi and K. Rustan M. Leino, Annotation inference for modular checkers, Information Processing Letters 77(2-4), 2001
    locator: pp. 97 to 108, the annotation inference algorithm and the proof that it returns the largest valid set of candidate annotations
  - paper: doi:10.1145/360204.360220
    title: Cormac Flanagan and James B. Saxe, Avoiding exponential explosion, generating compact verification conditions, Proceedings of POPL 2001
    locator: pp. 193 to 205, the VC generator of ESC/Java that Houdini calls
---

Houdini finds loop invariants by elimination. It starts from a large set of candidate formulas, guessed from the program text, and asks a verifier whether their conjunction is an [inductive invariant](/inductive-invariant/). Each time the verifier gives a counterexample, Houdini removes every candidate that the counterexample refutes, and asks again. When the verifier accepts, the remaining conjunction is the largest inductive subset of the candidates, and with $c$ candidates this takes at most $c + 1$ verifier calls.

## In plain words

You cannot easily invent the right facts about a loop, but you can cheaply guess hundreds: "this variable is never negative", "this pointer is never null", "this index stays below that length". Most guesses are wrong. Assume all of them at once and ask a checker whether they hold at the start and whether one turn of the loop keeps them all. If not, the checker shows a state where some guesses break. Throw those guesses away and ask again. A wrong guess never comes back, so the list only gets shorter. When the checker is finally happy, the guesses that are left hold together, and no good guess was thrown away on the way, because each throw was forced by a real broken state.

## The problem

The input is a loop, given by its initial states $\mathit{Init}$, a guard $b$ and a body, a finite set $C$ of $c$ candidate formulas, and a prover. The output is the largest $H \subseteq C$ whose conjunction is inductive: every initial state satisfies $\bigwedge H$, and one turn of the body from a state of $\bigwedge H \wedge b$ ends in $\bigwedge H$. The [loop invariant synthesis](/loop-invariant-synthesis/) page explains why such sets matter; Houdini solves the special case where the language is "conjunctions of candidates from $C$".

The prover decides whether a conjunction is inductive and, if not, returns a counterexample. A real tool builds the two [verification conditions](/verification-condition-generation/) and asks an [SMT](/smt-problem/) solver, which is a decision procedure when the candidates and the loop lie in a decidable theory such as [Presburger arithmetic](/presburger-arithmetic/). This page has no solver. Its prover tries every state of a box of integers and returns the first counterexample in lexicographic order, so "inductive" here means inductive on the box, a bounded check, not a proof. The theorem below holds for any fixed domain of states, the box or all of $\mathbb{Z}^k$.

## The algorithm

```pseudo id=main
HOUDINI(C, PROVE)
L1  H <- C
L2  loop
L3      cex <- PROVE(H)
L4      if cex = none then return H
L5      if cex is an initial state s then H <- {h in H : s satisfies h}
L6      else cex is a step from s to t: H <- {h in H : t satisfies h}
```

PROVE gets the current set $H$. An initial counterexample is an initial state that falsifies $\bigwedge H$. A step counterexample is a state $s$ that satisfies $\bigwedge H$ and the guard, with a successor $t$ that falsifies $\bigwedge H$. Line L5 removes the candidates that are false at the start of the loop, and line L6 removes the candidates that one turn breaks. Line L6 looks only at $t$: a candidate that is false at $s$ is not removed, since $s$ may be a state that no run reaches.

## Example

The loop is $i := 0; j := 0; \mathbf{while}\ i < n\ \mathbf{do}\ (i := i + 1; j := j + 2)$, entered with $n \ge 0$. The eight candidates are $0 \le i$, $i \le n$, $j = 2i$, $j \le n$, $i = j$, $0 \le n$, $j \le 2n$ and $n \le 3$. The prover checks the box $[-4, 4]^3$ over $(i, j, n)$ in lexicographic order.

| call | candidates left | counterexample | removed |
|---|---|---|---|
| 1 | all 8 | initial state $(i, j, n) = (0, 0, 4)$ | $n \le 3$ |
| 2 | 7 | step from $(0, 0, 1)$ to $(1, 2, 1)$ | $j \le n$, $i = j$ |
| 3 | 5 | none | |

Houdini returns $0 \le i \wedge i \le n \wedge j = 2i \wedge 0 \le n \wedge j \le 2n$ after 3 calls, below the bound $c + 1 = 9$. Brute force over all 256 subsets gives the same largest inductive subset. With the exit condition $i \ge n$, the result gives $i = n$ and $j = 2n$, the postcondition one wants. The candidate $n \le 3$ is true on many runs, but the initial state with $n = 4$ refutes it. The step of call 2 removes two candidates at once.

## Correctness

The full proof is in the proof file. Fix the domain of states $B$ that the prover checks, and say "inductive" for "inductive on $B$".

1. **Inductive sets are closed under union.** If $H_1$ and $H_2$ are inductive, a state of $\bigwedge (H_1 \cup H_2) \wedge b$ satisfies both $\bigwedge H_1 \wedge b$ and $\bigwedge H_2 \wedge b$, so its successors satisfy both conjunctions. The empty set is inductive. So the union $H^\ast$ of all inductive subsets is inductive and is the unique largest one.
2. **The invariant $H^\ast \subseteq H$.** An initial counterexample satisfies $\bigwedge H^\ast$, since $H^\ast$ holds initially. A step counterexample starts in $\bigwedge H \wedge b$, hence in $\bigwedge H^\ast \wedge b$, so its end satisfies $\bigwedge H^\ast$. Either way, lines L5 and L6 remove no candidate of $H^\ast$.
3. **Progress.** A counterexample falsifies $\bigwedge H$ at $s$ or $t$, so at least one candidate goes. At most $c$ calls fail, and the call after the last failure succeeds: at most $c + 1$ calls.
4. **The end.** The returned $H$ is inductive, so $H \subseteq H^\ast$, and by step 2, $H = H^\ast$.

The proof needs an exact prover. With an incomplete prover, a spurious counterexample can remove a good candidate, and the result is inductive but smaller.

## Complexity

By step 3 there are at most $c + 1$ calls of PROVE. Each round filters $H$ with one evaluation per candidate, $O(c)$, so the total is $O(c T + c^2)$, where $T$ is the cost of one prover call. The bound $c + 1$ is tight: for $x := x + 1$ from $x = 0$ with the candidates $x \le 0, \dots, x \le c - 1$, each counterexample refutes one bound, and the tests check that $c = 3$ takes 4 calls. The box prover of this page costs $T = O(c\,(h - l + 1)^k)$ evaluations for the box $[l, h]^k$. A real prover pays one SMT call, and in the worst case that call is as hard as the theory: NP-complete for quantifier-free linear integer arithmetic.

## Properties

- **Largest, hence strongest.** The result is the strongest invariant that is a conjunction of candidates. Any proof that uses only candidates from $C$ also works with it.
- **Monotone removal.** A candidate, once removed, never returns, so the run is a descending chain in a finite lattice. This is the greatest fixed point of a monotone operator on subsets of $C$, and Houdini computes it by iteration from the top.
- **Independent of the order.** The result does not depend on which counterexample the prover returns, only on the set of candidates and the domain. The number of calls does depend on it.
- **Modular.** In ESC/Java the candidates are the preconditions, postconditions and invariants of all methods at once. One run of the modular checker refutes some of them, and the same argument shows that the largest consistent set is found.
- **Only conjunctions.** Houdini never builds a disjunction or a new formula. If the needed invariant is not a conjunction of candidates, it is not found.

## Variants and improvements

- **Whole-program Houdini.** The original tool guessed annotations for every method of a Java program, ran ESC/Java on the whole program, and removed every annotation with a warning. Each run of the checker can refute many candidates.
- **Predicate abstraction with conjunctions.** [Predicate abstraction](/predicate-abstraction/) over the candidates as predicates, restricted to the conjunction domain, gives the same result. With the full boolean domain over the same predicates, it can also find disjunctions, at an exponential cost.
- **Learning with counterexamples.** Data-driven methods, in the style of [CEGIS](/cegis/), also learn invariants from counterexamples, but they can add formulas, not only remove them, and they use implication counterexamples $(s, t)$ in both directions.
- **Seeding other tools.** Houdini output is a cheap first invariant for [k-induction](/k-induction/), [IC3](/ic3-pdr/) and [abstract interpretation](/abstract-interpretation/), which then strengthen it.
- **Parallel and incremental.** Since the checks of different procedures are independent, tools run them in parallel, and keep the solver state between calls because each query differs from the last only by removed candidates.

## When to use it

Use Houdini when cheap guesses are plentiful and most of the needed facts are simple: bounds of indices, signs, non-null pointers, relations between two variables. It is a good first pass before a verifier asks a person for invariants. Use [constraint-based generation](/farkas-invariant-generation/) when the needed invariant is a linear inequality whose coefficients you cannot guess, and [abstract interpretation](/abstract-interpretation/) when there is no target property and you want the strongest facts in a domain.

## Pitfalls

- **Expecting more than conjunctions.** For the loop $x := -x$ from $x = 1$, the candidates $x \ge -1$ and $x \le 1$ are both kept, but their conjunction allows $x = 0$ and cannot prove $x \ne 0$. Houdini finds $x \ne 0$ only when it is itself a candidate. The tests check both cases.
- **Removing at the wrong state.** Line L6 must test the candidates at the successor $t$. Testing them at $s$, or removing every candidate that is false somewhere in the domain, removes candidates of $H^\ast$ that only fail at unreachable states.
- **Assuming the result proves the property.** The largest inductive subset can still be too weak for the postcondition. Houdini then reports the property as unproved; it is not evidence that the program is wrong.
- **Taking a bounded check for a proof.** The prover of this page only checks a box. A conjunction can be inductive on $[-4, 4]^3$ and fail at a larger state, so the result is only evidence. With an SMT solver over a decidable theory, it is a proof.
- **A prover that times out.** If a timeout is treated as a counterexample with no state, there is nothing to remove and the loop does not progress. If it is treated as "none", the result is unsound. Real tools remove the candidate that the checker could not prove, and accept that the result may then be smaller than $H^\ast$.

## Implementations

## History

Flanagan and Leino presented Houdini at FME 2001 as an annotation assistant for ESC/Java. ESC/Java needed many annotations before it gave useful warnings, and Houdini filled in the simple ones by guessing candidates from the program text and letting ESC/Java refute them. Flanagan, Joshi and Leino gave the general theory in Information Processing Letters in the same year, for any modular checker, with the proof that the algorithm finds the largest valid set of candidate annotations. The same scheme now appears as the "candidate invariant" pass of many verifiers and as a building block of invariant learners.

## References
