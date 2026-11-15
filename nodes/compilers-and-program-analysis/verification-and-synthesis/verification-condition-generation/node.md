---
tag: 7VA8XP
kind: algorithm
slug: verification-condition-generation
name: Verification condition generation
aliases:
- VC generation
- VCGen
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Turns an annotated program into logical formulas, by weakest preconditions or symbolic paths, whose validity implies its correctness.
model: word-ram
complexity:
  vars: {n: the number of nodes of the program and its annotations, V: the number of variables}
  time: {worst: O(2^n)}
  space: {extra: O(2^n)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1967
  people: [Robert W. Floyd, Edsger W. Dijkstra, Cormac Flanagan, James B. Saxe]
  note: Floyd attached a verification condition to each path between assertions in 1967; Dijkstra's weakest preconditions (1975) gave the backward rules, and Flanagan and Saxe (2001) made the VCs compact.
prereqs: [weakest-precondition, hoare-logic, loop-invariant]
see_also: [strongest-postcondition, loop-invariant-synthesis, houdini-algorithm, smt-problem, symbolic-execution, floyd-inductive-assertions, proof-carrying-code, static-single-assignment-form]
sources:
  - paper: doi:10.1145/360204.360220
    title: Cormac Flanagan and James B. Saxe, Avoiding exponential explosion, generating compact verification conditions, Proceedings of POPL 2001
    locator: pp. 193 to 205, Figure 2 (wp), Sections 4 to 6 (the two causes of blow-up, passive form, the outcome predicates N and W), Theorems 1 to 3, Section 7.1 (loops)
  - paper: doi:10.1145/1108792.1108813
    title: Mike Barnett and K. Rustan M. Leino, Weakest-precondition of unstructured programs, Proceedings of PASTE 2005
    locator: pp. 82 to 87, the passive form of a control flow graph and its VC
  - paper: doi:10.1145/360933.360975
    title: Edsger W. Dijkstra, Guarded commands, nondeterminacy and formal derivation of programs, Communications of the ACM 18(8), 1975
    locator: pp. 453 to 457, the rules of wp for assignment, sequence and alternation
  - paper: "Robert W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, American Mathematical Society, 1967"
    locator: pp. 19 to 32, the verification conditions of a flowchart with a tagged assertion on each loop
---

Verification condition generation, or VCGen, turns a program with a precondition, a postcondition and a [loop invariant](/loop-invariant/) on each loop into a list of logical formulas, the verification conditions or VCs. If every VC is valid, the program is correct. The classic method walks backwards through the code with the rules of the [weakest precondition](/weakest-precondition/), cuts each loop at its invariant, and hands the VCs to a solver. This page gives that method, proves it sound, and shows why naive wp can grow exponentially while the passive form of Flanagan and Saxe stays polynomial.

## In plain words

You have a program, a claim about its input and a claim about its output. VCGen writes down a few plain statements of logic that do not mention the program at all. If those statements are true, the program keeps its promise. It works from the end of the program towards the start. Each line of code changes what must be true before it: an assignment replaces the variable by its new value, a branch splits the requirement into two cases. A loop is the hard part, so a person, or another tool, writes down a fact that holds every time the loop starts again. VCGen then asks three things: the fact holds when the loop is first reached, one turn of the loop keeps it, and the fact together with the loop exit gives what is needed after the loop. A solver checks each statement.

## The problem

The input is a precondition $P$, a statement $S$ and a postcondition $Q$. The statements are skip, $x := e$, assert $p$, assume $p$, sequence, if $b$ then $S_1$ else $S_2$, and while $b$ invariant $I$ do $B$, over integer variables with $+$, $-$ and $\times$. The output is a list of formulas such that, if all of them are valid, the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$ holds for [partial correctness](/partial-correctness/): every run of $S$ from a state of $P$ that stops passes its asserts and ends in a state of $Q$.

Whether a program meets its specification is undecidable by [Rice's theorem](/rice-theorem/). VCGen does not decide it. It moves the hard part into the invariants, which someone must supply, and into the validity of the VCs. Validity is decidable only in decidable theories: [Presburger arithmetic](/presburger-arithmetic/) for linear integer formulas, linear real arithmetic, [equality with uninterpreted functions](/euf-satisfiability/) and arrays, and their combinations. The VCs of the example below multiply two variables, and validity over the integers with multiplication is undecidable by [Hilbert's tenth problem](/hilberts-tenth-problem/). A real tool gives each VC to an [SMT](/smt-problem/) solver. This page has no solver. It checks each VC in every state of a small box of integers, which is a bounded check, not a proof.

## The algorithm

```pseudo id=main
VCGEN(P, S, Q)
L1  side <- an empty list
L2  return [P => WP(S, Q, side)] followed by side

WP(S, Q, side)
L3  case S of
L4    skip: return Q
L5    x := e: return Q[e/x]
L6    assert p: return p and Q
L7    assume p: return p => Q
L8    S1; S2: return WP(S1, WP(S2, Q, side), side)
L9    if b then S1 else S2: return (b => WP(S1, Q, side)) and (not b => WP(S2, Q, side))
L10   while b invariant I do B:
L11       append (I and b) => WP(B, I, side) to side
L12       append (I and not b) => Q to side
L13       return I
```

Lines L4 to L9 are the rules of the weakest precondition, with $Q[e/x]$ the formula $Q$ with $e$ in place of every free $x$. A loop is cut at its invariant (lines L10 to L13). The code before the loop must establish $I$, which is what line L13 asks for. Line L11 asks that one turn of the body keeps $I$, and line L12 asks that $I$ and the exit give $Q$. The side conditions are checked in every state, not only in the states that the code before the loop leaves. So the invariant must state every fact about the loop that the proof needs, even facts about variables that the loop does not change.

## Example

Integer division by repeated subtraction. The precondition is $x \ge 0 \wedge y > 0$, and the postcondition is $x = qy + r \wedge 0 \le r < y$.

```
q := 0; r := x;
while y <= r invariant x = q*y + r and r >= 0 do
  r := r - y; q := q + 1
```

WP of the loop body for the invariant $I$ is $I[q + 1/q][r - y/r]$, so VCGEN returns three VCs:

1. $x \ge 0 \wedge y > 0 \implies x = 0 \cdot y + x \wedge x \ge 0$ (the invariant holds at entry; 19 nodes),
2. $x = qy + r \wedge r \ge 0 \wedge y \le r \implies x = (q + 1)y + (r - y) \wedge r - y \ge 0$ (one turn keeps it; 33 nodes),
3. $x = qy + r \wedge r \ge 0 \wedge \neg(y \le r) \implies x = qy + r \wedge 0 \le r \wedge r < y$ (the exit gives the postcondition; 32 nodes).

All three hold in every state of $[-6, 6]^4$ over $(x, y, q, r)$, and they are valid over the integers by simple algebra. The run from $x = 7$, $y = 2$ visits the loop head four times. The table shows which VC covers each step.

| head visit | $q$ | $r$ | $I$ | guard $y \le r$ | VC used |
|---|---|---|---|---|---|
| 1 | 0 | 7 | $7 = 0 + 7$, $7 \ge 0$ | true | 1 to reach it, 2 to go on |
| 2 | 1 | 5 | $7 = 2 + 5$ | true | 2 |
| 3 | 2 | 3 | $7 = 4 + 3$ | true | 2 |
| 4 | 3 | 1 | $7 = 6 + 1$ | false | 3: $0 \le 1 < 2$ |

**The size of naive wp.** Let $S_n$ be $n$ copies of "if $0 < x$ then $x := x - 1$ else $x := x + 1$", with the precondition $-n \le x \le n$ and the postcondition $0 \le x \le 1$. The table counts the nodes of the VC as a tree, as a DAG that shares equal subterms, and the nodes of the compact VC of the section on variants. The counts come from the functions `size` and `dag_size` of the implementation; there is no randomness. All the VCs hold on $[-12, 12]$.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| naive wp, tree | 40 | 106 | 270 | 662 | 1574 | 3654 | 8326 | 18694 | 41478 | 91142 |
| naive wp, DAG | 21 | 42 | 82 | 162 | 322 | 642 | 1282 | 2562 | 5122 | 10242 |
| compact VC, tree | 41 | 67 | 93 | 119 | 145 | 171 | 197 | 223 | 249 | 275 |

The DAG size is exactly $10 \cdot 2^n + 2$ for $n \ge 2$, so sharing does not help: each of the $2^n$ paths substitutes a different term, such as $((x - 1) + 1) - 1$, into its copy of the postcondition. The compact VC grows by 26 nodes per if.

## Correctness

The full proof is in the proof file. The main steps:

1. **Exact on loop-free code.** For a loop-free $S$, a state satisfies $\mathrm{WP}(S, Q)$ exactly when the run from it passes its asserts and is blocked or ends in $Q$. This is an induction on $S$; the assignment case is the substitution lemma. So the single VC $P \Rightarrow \mathrm{WP}(S, Q)$ holds in every state of a set $B$ exactly when every run from a state of $B \cap P$ is correct. With $B$ all states, this is the [weakest precondition](/weakest-precondition/) property.
2. **Sound with loops.** If all VCs are valid, every run from $P$ that stops is correct. The proof is an induction on $S$, and inside a loop an induction on the number of turns: the main VC gives $I$ at the first visit of the loop head, the VC of line L11 carries $I$ from one visit to the next, and the VC of line L12 gives $Q$ at the exit.
3. **The bounded version.** The same proof only uses the VCs in the start state and in the states at loop heads. So if the VCs hold on a box $B$, every run whose start and loop-head states lie in $B$ is correct. The tests check this statement, and only this one, on random programs.
4. **No converse.** With a loop, a correct program can have an invalid VC, because the side VCs ask that the invariant is inductive in every state, also in states that no run reaches.

The conditions are only as good as the invariants. VCGen proves partial correctness; termination needs a [variant function](/variant-function/) and one more VC per loop, see [termination proof](/termination-proof/).

## Complexity

Each rule of WP does a constant amount of work plus a substitution, so the time is linear in the size of the output. The output can be exponential. A sequence of $k$ ifs doubles the formula $k$ times, as the table shows, and a sequence of assignments $x := x + x$ doubles the number of occurrences of $x$ each time. In both cases, the formula is at most $2^{O(n)}$ nodes. The compact VC below has $O(n + V k)$ nodes for a loop-free program with $k$ ifs, which is $O(n^2)$ in the worst case and $O(n)$ when $V$ is bounded. The brute-force check costs $(h - l + 1)^V$ evaluations for the box $[l, h]^V$. A real tool pays instead for the SMT calls, whose cost depends on the theory: NP-complete for quantifier-free linear integer arithmetic, and undecidable with multiplication.

## Properties

- **Sound, not complete.** Valid VCs imply correctness. An invalid VC does not mean the program is wrong; the invariant may be too weak.
- **Exact without loops.** For loop-free code, the VC is valid exactly when the program is correct.
- **Modular.** A procedure call can be replaced by assert of its precondition, havoc of what it changes, and assume of its postcondition, so each procedure is checked once against its contract, as in [design by contract](/design-by-contract/).
- **Syntax-directed.** The output depends only on the text of the program and the annotations, and one rule handles each kind of statement.
- **Backward or forward.** WP goes backwards with substitution. The forward version uses the [strongest postcondition](/strongest-postcondition/) and needs a fresh name for each old value, which is what [symbolic execution](/symbolic-execution/) does.

## Variants and improvements

- **Passive form (Flanagan and Saxe).** The two causes of blow-up are substitution, which copies $e$ into each occurrence of $x$, and branches, which copy the postcondition into both cases. The passive form gives each assignment a fresh version $x_k$ defined by $e$, as in [static single assignment form](/static-single-assignment-form/), and merges versions at a join. A passive statement has no assignments, so its wp needs no substitution, and Flanagan and Saxe state it as $\neg W.S \wedge (N.S \Rightarrow Q)$ with two predicates, N for normal termination and W for going wrong. The VC has size $O(|S|^2)$ in the worst case, and linear in the passive statement once repeated subformulas get names. The implementation of this page binds each version with a let, merges with if-then-else, and names the postcondition with a let at each join; the one-point rule $\forall x'. (x' = e \Rightarrow F) \equiv F[e/x']$ makes this equal to the form with assume. The table above shows the result: 26 nodes per if, not a doubling.
- **Unstructured programs.** Barnett and Leino generate the passive VC directly on a [control flow graph](/control-flow-graph/), with one boolean variable per block that says "the run from this block is correct". This is the method of Boogie.
- **Loops by havoc.** Flanagan and Saxe desugar a loop to: assert $I$, havoc the variables that the body changes, assume $I$, and then either assume $b$, run the body, assert $I$ and assume false, or assume $\neg b$. The VC of the cut program is the same as lines L10 to L13, but the havoc keeps the facts about variables that the loop does not change, so the invariant can omit them.
- **Forward VCs and path enumeration.** Floyd's original method takes each path between two assertions, computes its strongest postcondition, and asks that it implies the assertion at the end. [Symbolic execution](/symbolic-execution/) is the same with one path condition per path.
- **Without invariants.** [Bounded model checking](/bounded-model-checking/) unrolls each loop a fixed number of times and checks the unrolled program. [Loop invariant synthesis](/loop-invariant-synthesis/), for example the [Houdini algorithm](/houdini-algorithm/), finds invariants automatically.

## When to use it

Use VCGen in a deductive verifier, where a programmer writes contracts and invariants and expects a proof, not a test. Dafny, Why3, Frama-C with its WP plug-in, and ESC/Java all generate VCs and call SMT solvers. Use the passive form as soon as programs have more than a few branches in sequence. When no one will write invariants, use an invariant generator first, or use [abstract interpretation](/abstract-interpretation/) or a model checker such as [IC3](/ic3-pdr/), which find the inductive facts themselves.

## Pitfalls

- **An invariant that is true but not inductive.** With the invariant $x = qy + r$ alone, the division program is still correct, but VC 3 fails in the state $x = -6$, $y = -5$, $q = 0$, $r = -6$: the invariant and the exit hold, and $0 \le r$ does not. No run reaches that state, but the side VCs are checked in every state.
- **Forgetting facts the loop does not change.** The side VCs drop all context. If the body asserted $y > 0$, the invariant would have to repeat $y > 0$, although no statement changes $y$. The havoc form keeps such facts for the variables that the loop does not assign.
- **Taking partial correctness for termination.** With the precondition $x \ge 0$ only, all three VCs of the example are still valid, but the program loops forever when $y = 0$.
- **Taking a bounded check for a proof.** The VC of skip for the postcondition $x < 100$ holds in every state of $[-8, 8]$ and fails at $x = 100$. The brute-force check of this page is only evidence; an SMT solver gives a proof for decidable theories.
- **Naive wp on long code.** The table above shows the doubling. A VCGen that copies the postcondition at each branch can time out on code that a passive VCGen handles at once.
- **Substitution with capture.** $Q[e/x]$ must not substitute under a binder of $x$, and must rename a bound variable that occurs free in $e$. Quantified invariants make this a real bug.

## Implementations

## History

Floyd's 1967 paper attached assertions to the edges of a flowchart and derived a verification condition for each path between assertions, with a tagged assertion cutting each loop. Hoare's logic of 1969 gave the same method as rules for triples, and Dijkstra's weakest preconditions of 1975 turned the rules into a function that computes the condition backwards. King's verifier of 1969 and the Stanford Pascal Verifier of the 1970s generated VCs mechanically. In 2001 Flanagan and Saxe found the two causes of exponential VCs in ESC/Java, assignments and joins, and fixed both with the passive form. Barnett and Leino extended the method to unstructured programs in 2005, and it is the core of Boogie and of the verifiers built on it.

## References
