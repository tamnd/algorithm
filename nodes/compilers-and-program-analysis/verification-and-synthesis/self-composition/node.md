---
tag: D3FA1M
kind: technique
slug: self-composition
name: Self-composition
aliases:
- product programs
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: Reduces a property of two runs, such as noninterference or equivalence, to a safety property of one program that runs both copies.
prereqs: [noninterference, hoare-logic]
see_also: [verification-condition-generation, translation-validation, equivalence-checking, loop-invariant-synthesis, bounded-model-checking, k-induction, timing-attack, safety-property]
sources:
  - paper: doi:10.1109/CSFW.2004.1310735
    title: Gilles Barthe, Pedro R. D'Argenio and Tamara Rezk, Secure information flow by self-composition, Proceedings of the 17th IEEE Computer Security Foundations Workshop (CSFW 2004)
    locator: the self-composition of a program with a renamed copy of itself, and the characterization of noninterference by a Hoare triple of the composed program
  - paper: doi:10.1007/11547662_24
    title: Tachio Terauchi and Alex Aiken, Secure information flow as a safety problem, Proceedings of SAS 2005, LNCS 3672
    locator: the definition of 2-safety, the observation that plain self-composition needs hard invariants, and the type-directed transformation that interleaves the two copies
  - paper: doi:10.1007/978-3-642-21437-0_17
    title: Gilles Barthe, Juan Manuel Crespo and Cesar Kunz, Relational verification using product programs, Proceedings of FM 2011, LNCS 6664
    locator: pp. 200 to 214, product programs that align the two copies, with noninterference and loop optimizations as examples
  - paper: doi:10.1145/964001.964003
    title: Nick Benton, Simple relational correctness proofs for static analyses and program transformations, Proceedings of POPL 2004
    locator: pp. 14 to 25, relational Hoare logic, a proof system for judgments about two runs at once
  - paper: doi:10.3233/JCS-2009-0393
    title: Michael R. Clarkson and Fred B. Schneider, Hyperproperties, Journal of Computer Security 18(6), 2010
    locator: pp. 1157 to 1210, k-safety hyperproperties and their verification by self-composition
---

Self-composition checks a property of two runs of a program by checking an ordinary property of one run of a bigger program. The bigger program is the original followed by a copy of itself with every variable renamed, so one run of it is two independent runs of the original. A 2-safety property, such as [noninterference](/noninterference/), then becomes a single [Hoare triple](/hoare-triple/) that any one-run verifier can prove. Product programs refine the idea: they run the two copies in step, so that the loop invariants become simple.

## In plain words

Some questions are about two runs, not one. "Does the public output stay the same when only the secret changes?" compares a run with a secret and a run with another secret. Most checkers only know how to look at one run at a time. The trick is to glue two copies of the program into one program. The first copy uses its own variables, the second copy uses other ones, and they cannot touch each other. Start them in two related states, run them, and check that the end states are related. Now the question is about one run of the glued program, and the usual tools work. Running the two copies side by side, instead of one after the other, makes the proof much easier.

## When it applies

- The property is a *k-safety* property: it says that every $k$ runs of $P$ whose start states are related by a condition $\Phi$ end in states related by $\Psi$. For $k = 2$ this covers noninterference, constant-time execution, determinism and monotonicity, and, with two different programs, the equivalence of a program and its transformed version.
- The copies can be kept apart: each variable, array and heap cell can be duplicated, so the two runs do not interfere.
- The property is about terminating runs, in the sense of partial correctness. Properties that need a non-terminating run, or that ask for the existence of a matching run, as possibilistic noninterference does for nondeterministic programs, do not fit the plain form.

Deciding such properties is undecidable in general, by [Rice's theorem](/rice-theorem/), so self-composition does not remove the need for invariants; it moves the problem to a tool that can look for them.

## The template

```pseudo id=main
SELF-COMPOSE(P, Phi, Psi)
L1  P1 <- RENAME(P, 1)                 ▷ hole RENAME: x becomes x1 for every variable, array and heap
L2  P2 <- RENAME(P, 2)                 ▷ x becomes x2
L3  Q <- ALIGN(P1, P2)                 ▷ hole ALIGN: P1; P2, or a product that runs matching parts together
L4  pre <- Phi(x1, x2)                 ▷ for noninterference: l1 = l2 for every low l
L5  post <- Psi(x1, x2)                ▷ for noninterference: l1 = l2 for every low l
L6  prove {pre} Q {post}               ▷ hole PROVER: VC generation with invariants, a model checker, or testing
L7  if L6 succeeds then return "P has the 2-safety property"
L8  return the run of Q that breaks post, as a pair of runs of P
```

**Why it is exact.** Let $P$ be a program whose runs are the pairs $(s, t)$ of a start state and an end state. The copy $P_1$ reads and writes only the variables of copy 1, and $P_2$ only those of copy 2. So a run of $P_1; P_2$ from the joint state $(s_1, s_2)$ first changes the copy-1 part to $t_1$ with $(s_1, t_1)$ a run of $P$, and then the copy-2 part to $t_2$ with $(s_2, t_2)$ a run of $P$. Its end states are exactly the pairs $(t_1, t_2)$ of end states of two runs of $P$. Hence the triple $\{\Phi\}\ P_1; P_2\ \{\Psi\}$ is valid for partial correctness if and only if every two runs $(s_1, t_1)$ and $(s_2, t_2)$ of $P$ with $\Phi(s_1, s_2)$ have $\Psi(t_1, t_2)$. For noninterference, $\Phi$ and $\Psi$ are both "the low parts are equal", which is the triple of Barthe, D'Argenio and Rezk. If either copy does not stop, the triple says nothing, which matches termination-insensitive noninterference.

**Alignment.** The hole ALIGN may replace $P_1; P_2$ by any program with the same end states from each start state. Statements of different copies commute, since they touch disjoint variables. So straight-line code can be interleaved freely, and two loops can be fused:

$$\mathbf{while}\ e_1\ \mathbf{do}\ B_1;\ \mathbf{while}\ e_2\ \mathbf{do}\ B_2 \quad\text{has the same end states as}\quad \mathbf{while}\ e_1 \wedge e_2\ \mathbf{do}\ (B_1; B_2);\ \mathbf{while}\ e_1\ \mathbf{do}\ B_1;\ \mathbf{while}\ e_2\ \mathbf{do}\ B_2,$$

because the fused loop runs the first $\min$ of the two iteration counts of each copy, and the two tail loops run the rest. This is a product program. Its value is that the invariant of the fused loop can relate the two copies at the same point of their runs.

**Walk-through.** Take the program $x := 0;\ i := 0;\ \mathbf{while}\ i < n\ \mathbf{do}\ (x := x + i;\ i := i + 1)$ with $n$ and $x$ low, and a high variable $h$ that it does not read. With $P_1; P_2$, the proof needs an invariant for the first loop that tells what $x_1$ is at the end, such as $2 x_1 = i_1 (i_1 - 1)$, and the same for the second loop. These are nonlinear, and the proof of the program's security has become a proof of its function. With the fused loop, the precondition $n_1 = n_2$ gives the invariant $i_1 = i_2 \wedge x_1 = x_2 \wedge n_1 = n_2$. It is linear, it is preserved by one turn of $B_1; B_2$, and when the fused loop exits both guards are false at once, so the tail loops do nothing and $x_1 = x_2$ holds at the end. A [VC generator](/verification-condition-generation/) with this invariant proves the triple.

## Classic examples

- **Noninterference.** With $\Phi = \Psi = (=_L)$ the template proves [noninterference](/noninterference/), including programs that a security type system rejects, such as $l := h;\ l := 0$, where the weakest precondition of $l_1 = l_2$ is $0 = 0$.
- **Constant-time code.** Add a counter $c$ that each statement increases by its cost, and make $c$ an output. With $\Phi$ "the public inputs are equal" and $\Psi$ "$c_1 = c_2$", the triple says that the running time does not depend on the secret, the property that stops a [timing attack](/timing-attack/).
- **Program equivalence and optimizations.** Compose a program with a transformed version instead of itself, with $\Phi$ "the inputs are equal" and $\Psi$ "the outputs are equal". Barthe, Crespo and Kunz prove [loop unrolling](/loop-unrolling/), [loop-invariant code motion](/loop-invariant-code-motion/) and other optimizations this way, with a product that aligns the iterations. [Translation validation](/translation-validation/) and [equivalence checking](/equivalence-checking/) solve the same problem for one compiled program.
- **Determinism and monotonicity.** With $\Phi$ "the inputs are equal" and $\Psi$ "the outputs are equal", a program with internal choices is shown deterministic; with $\Phi$ "$x_1 \le x_2$" and $\Psi$ "$y_1 \le y_2$" it is shown monotone.
- **Bounded search for leaks.** Run [bounded model checking](/bounded-model-checking/) on $Q$: a counterexample is a concrete pair of runs that leaks. [k-induction](/k-induction/) on $Q$ can prove the property when the product has simple invariants.

## Variations

- **Relational Hoare logic.** Benton's logic proves judgments $\{\Phi\}\ P_1 \sim P_2\ \{\Psi\}$ directly, with rules that pair up the statements of the two programs. A proof in it can be read as a proof of a product program.
- **Type-directed products.** Terauchi and Aiken use a security type analysis to find the parts of $P$ that do not depend on secrets. Those parts run in step in both copies, and only the rest is duplicated, which gives a smaller program and simpler invariants.
- **Asymmetric products.** For $\forall\exists$ properties, such as refinement or possibilistic noninterference of nondeterministic programs, Barthe, Crespo and Kunz later built products in which the second copy is a choice to be made, not a run to be checked.
- **More copies.** A k-safety property needs $k$ copies; for example, the transitivity of a comparison function needs three runs. The template is the same with $k$ renamings.
- **Constraint solving.** Instead of a fixed product, a relational verifier can search for the alignment and the invariant together, as a system of constraints over unknown relations.

## Pitfalls

- **Sequential composition makes invariants hard.** In $P_1; P_2$ each loop runs alone, so its invariant must describe what the loop computes, not how the two copies relate. Align the loops when the copies take the same branches.
- **Alignment needs matching control flow.** The fused loop helps only if the two copies leave the loop at the same time, usually because the guard depends on low variables only. If the guard depends on a secret, the tail loops run, and the invariant must cover them.
- **Shared state breaks the reduction.** The copies must not share a variable, a heap cell, a file or a global. A missed sharing makes the two runs dependent, and the proof is about a different program.
- **Partial correctness only.** The triple is vacuous when a copy does not stop. It proves termination-insensitive properties, and a leak through termination needs a separate termination proof.
- **The model must contain the channel.** A proof of noninterference over the final state says nothing about time, memory traffic or power, unless the program is instrumented to make them outputs.

## Exercises

1. Self-compose $\mathbf{if}\ h > 0\ \mathbf{then}\ l := 1\ \mathbf{else}\ l := 0$ and find a state that breaks $\{l_1 = l_2\}\ P_1; P_2\ \{l_1 = l_2\}$. *Answer.* $l_1 = l_2 = 0$, $h_1 = 1$, $h_2 = 0$. The end state has $l_1 = 1$ and $l_2 = 0$.
2. Prove $\{l_1 = l_2\}\ P_1; P_2\ \{l_1 = l_2\}$ for $P = (l := h;\ l := 0)$ with weakest preconditions. *Answer.* Going backwards, $l_2 := 0$ turns $l_1 = l_2$ into $l_1 = 0$, then $l_2 := h_2$ leaves it, $l_1 := 0$ turns it into $0 = 0$, and $l_1 := h_1$ leaves it. The precondition $\mathit{true}$ follows from $l_1 = l_2$.
3. Why does a fused loop fail to give a simple proof for $i := 0;\ \mathbf{while}\ i < h\ \mathbf{do}\ i := i + 1;\ l := 0$, and why is the program still noninterfering? *Answer.* The two copies run $h_1$ and $h_2$ turns, so after the fused loop one tail loop runs and $i_1 \ne i_2$ in general. But $i$ is not low, and the final $l := 0$ makes $l_1 = l_2 = 0$, so the invariant "true" for all three loops is enough.
4. Show that statements of different copies commute: if $S_1$ uses only copy-1 variables and $S_2$ only copy-2 variables, then $S_1; S_2$ and $S_2; S_1$ have the same end states. *Answer.* From $(s_1, s_2)$ both orders end in $(t_1, t_2)$, where $t_1$ is an end state of $S_1$ from $s_1$ and $t_2$ one of $S_2$ from $s_2$, since neither statement reads or writes the other part.

## References
