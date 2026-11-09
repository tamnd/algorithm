---
tag: 5F99Q0
kind: algorithm
slug: symbolic-reachability
name: Symbolic reachability analysis
aliases:
- Symbolic reachability fixpoint
- BDD-based reachability
- Image computation fixpoint
area: logic-and-constraints/model-checking
level: advanced
summary: Compute the set of reachable states as a least fixed point of image steps, where each set of states and the transition relation are BDDs and each image is one relational product.
solves: [reachability-problem, invariant-checking]
model: word-ram
complexity:
  vars: {n: the number of state variables, d: the largest distance of a reachable state from the initial states, c: "the cost of one image, a relational product, which can be exponential in n", b: the number of nodes of the largest BDD in the run}
  time: {worst: O((d + 1) · c)}
  space: {worst: O(b)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1990
  people: [Jerry R. Burch, Edmund M. Clarke, Kenneth L. McMillan, David L. Dill, L. J. Hwang]
  note: Burch, Clarke, McMillan, Dill and Hwang computed fixed points with relational products of BDDs, and checked systems with more than 10^20 states.
prereqs: [reachability-problem, reduced-ordered-bdd, bdd-quantification, fixed-point]
see_also: [symbolic-model-checking, saturation-algorithm, bdd-apply, variable-ordering, breadth-first-search, sat-based-bounded-model-checking, ic3-pdr, state-explosion-problem]
sources:
  - paper: doi:10.1016/0890-5401(92)90017-A
    title: J. R. Burch, E. M. Clarke, K. L. McMillan, D. L. Dill and L. J. Hwang, Symbolic model checking, 10^20 states and beyond, Information and Computation 98(2), 1992
    locator: the relational product, and the computation of fixed points by iteration of the image and preimage operators
  - book: isbn:9780792393801
    title: Kenneth L. McMillan, Symbolic Model Checking, Kluwer Academic Publishers, 1993
    locator: the chapters on BDDs, the representation of transition relations and the fixed-point algorithms
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 5 (binary decision diagrams) and Chapter 6 (symbolic model checking, the relational product and partitioned transition relations)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 6, Section 6.7 (symbolic CTL model checking, switching functions, the encoding of transition systems and the image operators)
---

Symbolic reachability computes the set of all reachable states of a finite transition system without listing the states one by one. It keeps the set of states found so far as one [BDD](/reduced-ordered-bdd/) $R$, and the transition relation as one BDD $T(x, x')$. One step, the *image*, gives all successors of a set in one BDD operation, the relational product $\exists x.\, R(x) \wedge T(x, x')$. The loop stops when the image adds no new state. This is the least [fixed point](/fixed-point/) $\mu Z.\, I \vee \mathrm{Post}(Z)$, and the loop reaches it after exactly $d + 1$ images, where $d$ is the largest distance of a reachable state from the initial states. The method is the core of [symbolic model checking](/symbolic-model-checking/), and it checks an [invariant](/invariant-checking/) when one intersects the result with the bad states.

## In plain words

A circuit has many on-off switches, so it has a very large number of states. Listing them one by one is too slow. Instead, we write the set of states as a compact formula, a decision diagram. Similar states share parts of the diagram, so a huge set can have a small diagram.

We start with the set of start states. In each step we compute, with one operation on diagrams, all the states that one move can reach from the set. We add them. When a step adds nothing, the set holds every reachable state. If a bad state is in the set, the system can fail.

## The problem

A finite transition system has $n$ Boolean state variables $x = (x_1, \ldots, x_n)$, so its state space is $\{0, 1\}^n$. The initial states are given as a Boolean function $I(x)$. The transition relation is a Boolean function $T(x, x')$ over the current variables $x$ and a copy $x'$ for the next state. A circuit with inputs $w$ has $T(x, x') = \exists w.\, \bigwedge_j (x'_j \leftrightarrow f_j(x, w))$, where $f_j$ is the next-state function of latch $j$. The task is to compute the set $\mathrm{Reach}$ of states that a path from an initial state reaches. With a set of bad states $B(x)$, the system is safe if and only if $\mathrm{Reach} \wedge B$ is false. This is the [reachability problem](/reachability-problem/) in its symbolic form.

For a set $F$ of states,

$$\mathrm{Post}(F)(x') = \exists x.\, F(x) \wedge T(x, x'), \qquad \mathrm{Pre}(F)(x) = \exists x'.\, T(x, x') \wedge F(x').$$

Both are *relational products*: a conjunction, followed by an existential quantification of one copy of the variables. The image $\mathrm{Post}(F)$ is over $x'$, so the algorithm renames $x'$ back to $x$.

## The algorithm

```pseudo id=main
SYMBOLIC-REACH(I, T)                         ▷ I(x) and T(x, x') are BDDs
L1  R ← I                                    ▷ the states found so far
L2  F ← I                                    ▷ the frontier: states found in the last step
L3  repeat
L4      N ← IMAGE(F, T)
L5      F ← N ∧ ¬R                           ▷ keep only the new states
L6      R ← R ∨ F
L7  until F = false
L8  return R

IMAGE(F, T)
L9  P ← AND-EXISTS(F, T, x)                  ▷ ∃x. F(x) ∧ T(x, x'), in one pass
L10 return P[x′ := x]                        ▷ rename the next-state variables
```

AND-EXISTS computes the conjunction and the quantification in one recursive pass over the two BDDs. Let $v$ be the top variable of $F$ and $T$, with cofactors $F_0, F_1$ and $T_0, T_1$. If $v$ is not quantified, the result is the node $(v, \mathrm{AE}(F_0, T_0), \mathrm{AE}(F_1, T_1))$. If $v$ is quantified, the result is $\mathrm{AE}(F_0, T_0) \vee \mathrm{AE}(F_1, T_1)$, and when the first part is already true the second is not needed. A [computed table](/computed-table/) stores the results, as in [BDD apply](/bdd-apply/). The BDD of $F \wedge T$ is never built.

The renaming in line L10 is cheap when the variables are ordered so that $x_j$ and $x'_j$ are next to each other, as in $x_1 < x'_1 < x_2 < x'_2 < \ldots$. Then the renaming keeps the order, and it only changes the labels of the nodes. This interleaved order is also the usual good [variable order](/variable-ordering/) for $T$, because $x'_j$ depends most on $x_j$.

The frontier $F$ in line L4 can be any set $G$ with $F \subseteq G \subseteq R$: the new states are the same. Implementations pick a $G$ with a small BDD. Imaging $R$ itself is the simplest choice and is also correct.

## Example

A 3-bit counter has the latches $x_0$ (low bit), $x_1$ and $x_2$, and one input $e$. When $e = 1$ it counts up by one; when $e = 0$ it keeps its value. In state 5 it goes back to 0. The initial state is 0. The variable order is $x_0 < x'_0 < x_1 < x'_1 < x_2 < x'_2 < e$. With this order the BDD of $T$ has 29 nodes, the two terminals included.

| images done | new states $F$ | $R$ | BDD nodes of $R$, terminals included |
|---|---|---|---|
| 0 | | {0} | 5 |
| 1 | {1} | {0, 1} | 4 |
| 2 | {2} | {0, 1, 2} | 5 |
| 3 | {3} | {0, 1, 2, 3} | 3 |
| 4 | {4} | {0, 1, 2, 3, 4} | 5 |
| 5 | {5} | {0, 1, 2, 3, 4, 5} | 4 |
| 6 | none | | |

The largest distance is $d = 5$ (state 5), and the loop makes $d + 1 = 6$ images. The sixth image gives $\{0\}$, which is not new. The final set is $\neg(x_1 \wedge x_2)$, a BDD with two inner nodes. The size of $R$ goes up and down: the set $\{0, 1, 2, 3\}$ is just $\neg x_2$, but $\{0, 1, 2\}$ needs more nodes. Backward search from state 7 with $\mathrm{Pre}$ finds $\{7, 6\}$, which does not meet $R$, so the invariant "the counter is never 7" holds.

## Correctness

After $i$ iterations, $F$ is the set of states at distance exactly $i$ from $I$, and $R$ is the set of states at distance at most $i$. This follows by induction from $\mathrm{Post}$ being correct: a state at distance $i + 1$ is a successor of a state at distance $i$ that is not at distance $i$ or less. The loop stops at the first $i$ with no state at distance $i$, which is $i = d + 1$, and then $R$ holds all states at a finite distance, that is $\mathrm{Reach}$. The correctness of AND-EXISTS comes from the [Shannon expansion](/shannon-expansion/) and from $\exists v.\, g = g|_{v=0} \vee g|_{v=1}$. The proofs are below.

## Complexity

The loop makes exactly $d + 1$ image computations, and $d \le 2^n - 1$. This is the number of BFS levels, not the number of states: a set of states at one distance can hold millions of states and still have a small BDD. Systems with a long counter have a large $d$ and are hard for this method.

There is no polynomial bound on the cost of one image. The BDD of a set of states over $n$ variables can have about $2^n / n$ nodes, and the relational product can make a result much larger than its inputs. The size of each BDD also depends on the [variable order](/variable-ordering/), and to find the best order is NP-hard ([variable ordering NP-hardness](/variable-ordering-np-hardness/)). In the worst case nothing better is possible: reachability for a circuit given by its next-state functions is PSPACE-complete, so a polynomial-time method would give $\mathrm{P} = \mathrm{PSPACE}$. In practice the cost depends on the BDD sizes, not on the number of states. This is why the method was the first to check systems with $10^{20}$ states and more.

## Properties

- **Exact.** The result is the exact set of reachable states, not an approximation.
- **Breadth-first.** The frontier at step $i$ is the BFS layer $i$. So the first step whose frontier meets the bad states gives a shortest counterexample, and a [counterexample](/counterexample-generation/) is read back with preimages of the stored frontiers.
- **Canonical sets.** Each set has one BDD for a fixed order, so the test $F = \text{false}$ in line L7 is a constant-time check.
- **Forward or backward.** The same loop with $\mathrm{Pre}$ in place of $\mathrm{Post}$ computes the states that can reach a set. Backward search from the bad states is the EF operator of [CTL model checking](/ctl-model-checking/).

## Variants and improvements

- **Partitioned transition relations.** The BDD of $T$ for a whole circuit is often too large. Keep instead the list of the conjuncts $T_j = (x'_j \leftrightarrow f_j)$, and quantify each variable as soon as no later conjunct uses it (early quantification). Burch, Clarke and Long (1991) described this conjunctive partitioning.
- **Frontier simplification.** Image any BDD between $F$ and $R$, for example the result of the generalized cofactor (restrict) of $F$ by $\neg R \vee F$, which is often smaller than both.
- **Chaining and saturation.** Fire the parts of an asynchronous relation one after the other, each on the result of the last. The [saturation algorithm](/saturation-algorithm/) pushes this idea to a fixed order on decision diagram levels, and is often much faster on asynchronous systems.
- **Approximate reachability.** Compute an over-approximation of $\mathrm{Reach}$ with smaller BDDs, for example by projecting onto groups of variables. If it does not meet the bad states, the property holds.
- **Dynamic variable reordering.** Change the variable order during the run (sifting) when the BDDs grow.

## When to use it

Use symbolic reachability for control-heavy hardware and protocols with a short diameter and a regular structure, where the BDDs stay small. It gives the full reachable set, which other methods can then reuse. Use [SAT-based bounded model checking](/sat-based-bounded-model-checking/) to find deep bugs in large circuits, and [IC3](/ic3-pdr/) to prove safety of large circuits: both scale better on many industrial designs, because they never build the full set of states. Use [explicit-state model checking](/explicit-state-model-checking/) for software with complex data, where BDDs grow out of control.

## Pitfalls

- **A bad variable order.** With $x$ before all of $x'$, the BDD of even a simple $T$ such as $x = x'$ is exponential. Interleave $x_j$ and $x'_j$.
- **Building $F \wedge T$ first.** The conjunction is often far larger than the result. Use the relational product.
- **Forgetting the inputs.** The inputs of a circuit must be quantified in the image, together with $x$. Else the result is a relation, not a set of states.
- **Testing the fixed point on $N$.** Stop when $N \wedge \neg R$ is false, not when $N$ is false: the image of a nonempty set is rarely empty.

## Implementations

## History

Coudert, Berthet and Madre (1989) computed the reachable states of sequential machines with BDDs to check machine equivalence. Burch, Clarke, McMillan, Dill and Hwang (LICS 1990, journal version 1992) gave symbolic model checking for the μ-calculus and CTL, with the relational product as the basic step and the reachable states as a least fixed point. They checked models with more than $10^{20}$ states. McMillan's thesis, published as a book in 1993, described the SMV model checker built on this method. Burch, Clarke and Long (1991) introduced the partitioned transition relations that made the method practical for large circuits.

## References
