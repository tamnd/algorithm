---
tag: EMBMJW
kind: algorithm
slug: signal-correspondence
name: Signal correspondence
aliases:
- van Eijk's method
- induction-based register correspondence
area: eda/hardware-verification
level: advanced
summary: Van Eijk's method that guesses classes of equal signals by simulation and refines them by induction until they are an inductive invariant that proves sequential equivalence.
solves: [sequential-equivalence-checking]
model: word-ram
complexity:
  vars: {V: "the number of nodes and gate inputs of the product machine", L: the number of latches of the product machine, I: the number of primary inputs}
  time: {worst: "O(V^2 4^(L + 2I))"}
  space: {extra: "O(V^2 4^(L + 2I))"}
properties: {deterministic: true, exact: false, complete: false, recursive: true}
history:
  year: 1998
  people: [Cornelis A. J. van Eijk]
  note: Van Eijk gave the method at DATE 1998 and in IEEE TCAD in 2000. Bjesse and Claessen did the induction step with SAT in 2000.
prereqs: [sequential-equivalence-checking, product-machine, inductive-invariant, reduced-ordered-bdd]
see_also: [k-induction, partition-refinement, sat-sweeping, cutpoint-equivalence-checking, latch-mapping, fixed-point, ic3-pdr, bounded-model-checking]
sources:
  - paper: "C. A. J. van Eijk, Sequential equivalence checking based on structural similarities, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 19(7), 814 to 819, 2000"
    title: C. A. J. van Eijk, Sequential equivalence checking based on structural similarities, IEEE TCAD 19(7), 814 to 819, July 2000
    locator: the candidate classes from simulation, the inductive check with BDDs, and the refinement to a fixed point
  - paper: doi:10.1109/DATE.1998.655922
    title: C. A. J. van Eijk, Sequential equivalence checking without state space traversal, DATE 1998, 618 to 623
    locator: the first version of the method
  - paper: "Per Bjesse and Koen Claessen, SAT-based verification without state space traversal, Formal Methods in Computer-Aided Design (FMCAD 2000), Lecture Notes in Computer Science 1954, 2000"
    title: P. Bjesse and K. Claessen, SAT-based verification without state space traversal, FMCAD 2000
    locator: the induction step of van Eijk's method done with SAT, and its use with stronger induction
  - book: doi:10.1007/978-1-4615-0817-5_13
    title: A. Kuehlmann and C. A. J. van Eijk, Combinational and sequential equivalence checking, in S. Hassoun and T. Sasao (editors), Logic Synthesis and Verification, Kluwer, 2002, 343 to 372
    locator: the section on sequential equivalence checking by signal correspondence
---

Signal correspondence proves that two sequential circuits are equivalent without exploring their states. It works on the [product machine](/product-machine/) of the two circuits. Random simulation from the initial state groups the latches and gates into classes of signals that seem equal at every step. The method then splits the classes until the equalities hold in the initial state and are kept by one step of the machine. Such a set of equalities is an [inductive invariant](/inductive-invariant/), so it holds in every reachable state. If each pair of outputs ends in one class, the circuits are equivalent. The method is sound but not complete: an equivalence that needs a fact about unreachable states is missed.

## In plain words

Two versions of the same design usually still have many wires and registers that carry the same value at every clock tick. Simulate both versions together for a few hundred ticks from reset. Wires that always showed the same value go into one group.

Now test the guess. Assume that every group is right at some tick. Is every group still right one tick later, for every input? If yes, the groups are right forever, because they are right at reset. If not, the test gives a state that breaks some group. Split the groups by the values in that state and test again.

When nothing breaks, look at the outputs. Two outputs in one group are equal forever. Two outputs in different groups may still be equal, so the answer is only "unknown".

## The problem

The input is a product machine $P$ with latches $s \in \{0, 1\}^L$, inputs $x \in \{0, 1\}^I$, initial state $s_0$, next-state function $\delta(s, x)$, and output pairs $(o_j, o_j')$. Each node $u$ (a latch, a gate, or a constant) has a value $u(s, x)$. The task is the [sequential equivalence](/sequential-equivalence-checking/) question: is $o_j(s, x) = o_j'(s, x)$ for every reachable state $s$ and every $x$? Signal correspondence answers "equivalent" or "unknown".

A partition $\Pi$ of the nodes gives the formula $E_\Pi(s, x)$: all members of each class have equal values at $(s, x)$. $\Pi$ is *inductive* when $E_\Pi(s_0, x)$ holds for every $x$, and $E_\Pi(s, x_0)$ implies $E_\Pi(\delta(s, x_0), x_1)$ for all $s, x_0, x_1$. The method returns the coarsest inductive partition that refines the simulation classes.

## The algorithm

```pseudo id=main
SIGNAL-CORRESPONDENCE(P, pairs)
L1  simulate P from s₀ on random inputs; classes ← groups of nodes with equal values (the constants 0 and 1 are nodes)
L2  while some class K has a node u with u(s₀, x) ≠ rep(K)(s₀, x) for some x do
L3      split every class by the values of its nodes at (s₀, x)
L4  repeat
L5      C(s, x₀) ← ∧ over classes K and u ∈ K of [u(s, x₀) = rep(K)(s, x₀)]
L6      if some (s, x₀, x₁) with C(s, x₀) = 1 has a node u of a class K with u(δ(s, x₀), x₁) ≠ rep(K)(δ(s, x₀), x₁) then
L7          split every class by the values of its nodes at (δ(s, x₀), x₁)
L8  until line L6 found no such point
L9  if every pair (o, o') lies in one class then return "equivalent"
L10 return "unknown"
```

Line L1 is cheap. It only guesses, but every class it makes holds on the simulated runs. Lines L2 and L3 make the guess hold in the initial state for every input, not only for the random ones. This is the base case of the induction.

Lines L4 to L8 are the induction step. Line L5 builds the hypothesis $C$, the conjunction of all equalities in frame 0. Line L6 asks whether some state and inputs satisfy $C$ but break an equality in frame 1, one step later. The code does this with BDDs over $s$, $x_0$ and $x_1$; a SAT solver works as well. A point found there is a real counterexample to the induction, though its state may not be reachable. Line L7 splits by the frame-1 values at that point, which separates at least the node and its representative. The loop ends when the hypothesis is inductive.

The difference from [k-induction](/k-induction/) is the invariant. K-induction tries to prove the output equality itself, with a longer hypothesis. Signal correspondence makes the invariant stronger instead, with the equalities of all internal signals, and keeps the induction one step long. The difference from [cutpoint equivalence checking](/cutpoint-equivalence-checking/) is time: there the equal nodes are equal as functions of the inputs, here they are equal only in reachable states.

## Example

Circuit $A$ is a one-hot ring of three latches $h_0, h_1, h_2$ with initial state $(1, 0, 0)$ and next state $(h_2, h_0, h_1)$. Its output is $o = h_0 \wedge h_1$. Circuit $B$ has the output $z = 0$. The reachable states of $A$ are $(1, 0, 0)$, $(0, 1, 0)$ and $(0, 0, 1)$, so $o$ is always 0, and the circuits are equivalent. There are no primary inputs.

Simulation for 8 cycles gives $h_0 = 10010010$, $h_1 = 01001001$, $h_2 = 00100100$, and 0 for $o$ and $z$.

| step | classes | hypothesis $C(s)$ | check | outcome |
|---|---|---|---|---|
| L1 | $\{0, o, z\}, \{1\}, \{h_0\}, \{h_1\}, \{h_2\}$ | | | |
| L2 | same | | at $s_0 = (1, 0, 0)$: $o = 0$, $z = 0$ | no split |
| L5, L6 | same | $o = 0$, that is $\neg(h_0 \wedge h_1)$ | frame 1: $o' = h_2 \wedge h_0$; $C \wedge o' = h_0 \wedge \neg h_1 \wedge h_2$ | point $s = (1, 0, 1)$ |
| L7 | $\{0, z\}, \{o\}, \{1\}, \{h_0\}, \{h_1\}, \{h_2\}$ | | at $\delta(s) = (1, 1, 0)$: $o = 1$, $z = 0$ | 1 split |
| L5, L6 | same | true | $z' = 0$ everywhere | no point; stop |
| L9 | | | $o$ and $z$ in different classes | "unknown" |

The state $(1, 0, 1)$ is not reachable, but the one-step hypothesis "$o = 0$" does not exclude it. This is the miss. No inductive partition at all keeps $o$ and $z$ together, as the proof shows, so a different simulation cannot help.

Add two gates $u = h_1 \wedge h_2$ and $w = h_0 \wedge h_2$ to $A$, outside its outputs. Then line L1 gives the class $\{0, o, u, w, z\}$, whose hypothesis says that at most one latch is 1. One step of the ring keeps that, so line L6 finds no point, there are 0 splits, and the answer is "equivalent". The extra signals made the invariant strong enough.

## Correctness

Two facts are proved in [the correctness proof](proofs/correctness.md). Soundness: if the final partition is inductive and puts each output pair in one class, then by induction over reachable states the equalities hold in every reachable state, so the circuits give the same outputs on every input sequence. Optimality: the result is the coarsest inductive partition below the simulation classes, the greatest fixed point of the refinement. The key invariant is that every inductive partition that refines the simulation classes also refines the current one; each split is forced, because a point found at line L6 satisfies the hypothesis of every finer partition. The proof also shows that the method is incomplete, with the example above.

## Complexity

Let $V$ count the nodes and gate inputs of the product machine. Each split adds at least one class, so lines L3 and L7 run at most $V$ times in total. Each pass of lines L5 and L6 makes $O(V)$ BDD applies: one equality per class member for $C$, and one check per member. The BDDs are over $L + 2I$ variables ($s$, $x_0$, $x_1$), so each has at most $2^{L + 2I} + 1$ nodes and each apply costs $O(4^{L + 2I})$ with the cache. Building the frame-0, frame-1 and initial-state BDDs once costs $O(V)$ applies. The total is $O(V^2 \, 4^{L + 2I})$ time in the worst case on the word RAM with expected constant-time hashing, and the tables hold at most one entry per step of work, which gives the same space bound.

The exponential factor is the worst case of BDDs, not the usual case. The point of the method is that the hypothesis $C$ relates two similar circuits, so its BDD, or the SAT instance in a SAT-based version, stays near the size of the circuits. No step enumerates states. With SAT in place of BDDs, each check is one call on two copies of the combinational logic, with at most $V$ calls per pass and at most $V + 1$ passes.

## Properties

- Sound: "equivalent" is always right.
- Incomplete: "unknown" does not mean different. The example above is equivalent and not proved.
- The result does not depend on the order of the checks or on which counterexample is found, because the coarsest inductive partition below the start is unique. It does depend on the simulation, but only through the start partition.
- Deterministic for a fixed seed.

## Variants and improvements

- **SAT-based induction.** Bjesse and Claessen (FMCAD 2000) did line L6 with SAT on two time frames. Each counterexample splits the classes, as here.
- **Longer induction.** Assume the equalities in $k$ consecutive frames and prove them in the next. In the ring example, 3-step induction proves $o = 0$ and 2-step induction does not: the unreachable state $(0, 1, 1)$ has $o = 0$ and then $o = 0$ again at $(1, 0, 1)$, but $o = 1$ one step later. See [k-induction](/k-induction/).
- **Complemented equalities.** Classes can hold nodes equal up to complement, so a latch and its inverted copy also match.
- **Other invariants.** Implications between signals, or the constraints found by [IC3](/ic3-pdr/), give a stronger hypothesis when equalities are not enough.
- **Synthesis.** The same fixed point finds sequentially equivalent signals in one circuit, which can then be merged. This is the sequential form of [SAT sweeping](/sat-sweeping/).

## When to use it

Use it when the two circuits keep most of their state encoding, as after combinational optimization, small sequential changes, or a pipeline with the same registers. Then the latches correspond, many internal signals match, and the induction succeeds. It is much cheaper than a full reachability analysis of the product machine and needs no [latch mapping](/latch-mapping/) step: corresponding latches are found as a side effect. When the state encoding changed, after state reencoding or deep [retiming](/retiming/), few signals match, the hypothesis is too weak, and the answer is often "unknown". Then use reachability, [bounded model checking](/bounded-model-checking/) to find a difference, or [IC3](/ic3-pdr/).

## Pitfalls

- **Skipping the base case.** Simulation checks the initial state only for the random inputs. A version that goes from line L1 to line L4 can accept classes that fail in the initial state for some other input, and then line L9 is unsound. Lines L2 and L3 must check every input at $s_0$.
- **Checking frame 1 under the wrong hypothesis.** The hypothesis $C$ at line L5 must be rebuilt from the current classes after every split. Using the hypothesis of the first pass keeps equalities that were already refuted and makes the induction step unsound.
- **Reading "unknown" as "different".** A missed equivalence such as the ring example is not a bug in the design. Only a reachable counterexample, for example from [bounded model checking](/bounded-model-checking/), shows a real difference.
- **No reset state.** The base case needs one initial state. Circuits without reset need a different notion, such as [safe replaceability](/safe-replaceability/).

## Implementations

## History

Van Eijk gave the method at DATE 1998, under the title "Sequential equivalence checking without state space traversal", and in the journal version in IEEE TCAD 19(7), 2000. He used BDDs for the induction step. Bjesse and Claessen (2000) did the step with SAT. The fixed point over equivalence classes has the same shape as [partition refinement](/partition-refinement/) for automata, but the splitting test is an induction check, not a transition count.

## References
