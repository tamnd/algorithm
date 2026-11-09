---
tag: WZ22QB
kind: algorithm
slug: cegar
name: Counterexample-guided abstraction refinement
aliases:
- CEGAR
- Abstraction refinement loop
area: logic-and-constraints/model-checking
level: advanced
summary: Check a property on a small existential abstraction; if the abstract counterexample is spurious, split the abstract state where it fails and check again.
solves: [invariant-checking]
model: word-ram
complexity:
  vars: {n: the number of concrete states, m: the number of concrete transitions}
  time: {total: O(n · (n + m))}
  space: {total: O(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 2000
  people: [Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, Helmut Veith]
  note: Clarke, Grumberg, Jha, Lu and Veith presented the automatic abstraction refinement loop for ACTL and LTL at CAV 2000, and a longer version in the Journal of the ACM in 2003.
prereqs: [kripke-structure, abstract-interpretation, computation-tree-logic, invariant-checking]
see_also: [predicate-abstraction, lazy-abstraction, simulation-relation, counterexample-generation, cegis, interpolation-based-model-checking, partition-refinement, state-explosion-problem]
sources:
  - paper: doi:10.1007/10722167_15
    title: Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu and Helmut Veith, Counterexample-guided abstraction refinement, CAV 2000, LNCS 1855
    locator: pages 154 to 169 (existential abstraction, the check of path and loop counterexamples, the refinement by splitting the failure state)
  - paper: doi:10.1145/876638.876643
    title: Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu and Helmut Veith, Counterexample-guided abstraction refinement for symbolic model checking, Journal of the ACM 50(5), 2003
    locator: pages 752 to 794 (the full method for ACTL with BDDs, the soundness of existential abstraction, termination, and the NP-hardness of the coarsest refinement)
  - paper: doi:10.1145/186025.186051
    title: Edmund M. Clarke, Orna Grumberg and David E. Long, Model checking and abstraction, ACM Transactions on Programming Languages and Systems 16(5), 1994
    locator: pages 1512 to 1542 (existential abstraction and the preservation of ACTL* from the abstract to the concrete system)
---

Counterexample-guided abstraction refinement (CEGAR) checks a property on a small abstract system instead of the large concrete one. An abstraction function $h$ maps concrete states to abstract states. The *existential abstraction* has an abstract transition from $\hat a$ to $\hat b$ when some concrete state in $\hat a$ has a successor in $\hat b$. So every concrete behaviour has an abstract copy, and a universal property such as an invariant, an [ACTL](/computation-tree-logic/) formula or an [LTL](/linear-temporal-logic/) formula that holds in the abstraction also holds in the concrete system. If the abstract model checker finds a counterexample, CEGAR checks it against the concrete system. A real counterexample is a bug. A *spurious* one fails at some abstract state, where the concrete states that the trace can reach have no concrete successor in the next abstract state. CEGAR splits that abstract state so that the spurious trace disappears, and checks again. Clarke, Grumberg, Jha, Lu and Veith introduced the loop in 2000. It is the basis of [predicate abstraction](/predicate-abstraction/) tools such as SLAM and of [lazy abstraction](/lazy-abstraction/) in BLAST.

## In plain words

A big system is hard to check, so we first check a rough sketch of it. In the sketch, many real states are merged into one box. A box has an arrow to another box if any state inside it can move into the other box. So the sketch can do everything the real system can do, and maybe more.

If the sketch is safe, the real system is safe too. If the sketch shows a path to an error, we replay it on the real system. If the real system can follow it, we found a real bug. If it cannot, we find the box where the replay gets stuck. We cut that box in two pieces: the states the replay actually reached, and the others. Then we check the finer sketch.

## The problem

A concrete system $M$ has a finite state set $S$, initial states $I \subseteq S$, a transition relation $R \subseteq S \times S$, and atomic propositions. The task here is [invariant checking](/invariant-checking/): is a set $\mathit{Bad}$ of states unreachable from $I$? That is the ACTL formula $\mathbf{AG}\,\neg \mathit{bad}$.

An abstraction is a partition of $S$ into blocks, or equally a function $h$ from $S$ to the blocks. It must respect the propositions: each block lies inside $\mathit{Bad}$ or outside it. The existential abstraction $\hat M$ has the blocks as states. A block is initial if it meets $I$, and $\hat R(B, C)$ holds if $R(s, t)$ for some $s \in B$ and $t \in C$. The map $h$ sends each path of $M$ to a path of $\hat M$, so $\hat M$ *simulates* $M$ (see [simulation relation](/simulation-relation/)).

## The algorithm

```pseudo id=main
CEGAR(S, I, R, Bad, P0)
L1  blocks ← P0, with each part split into its states in Bad and the others
L2  loop
L3      build the existential abstraction: B → C iff some s ∈ B has a successor in C
L4      π ← a shortest abstract path B_0, ..., B_L from a block meeting I to a block in Bad
L5      if there is no such path then return HOLDS
L6      S_0 ← I ∩ B_0; S_j ← post(S_j−1) ∩ B_j for j = 1, 2, ... while S_j ≠ ∅; let S_i be the last nonempty set
L7      if i = L then return FAILS, with a concrete path through S_0, ..., S_L
L8      split B_i into the dead-end states S_i and the rest B_i \ S_i
```

The sets $S_j$ are the concrete states that can follow the abstract path for $j$ steps. If $S_L$ is not empty, a concrete path through $S_0, \ldots, S_L$ ends in a bad state, and backward search inside the sets gives it. If the path dies at step $i + 1$, the states $S_i$ are *dead-end states*: they are reachable along the path, but none of them has a successor in $B_{i+1}$. The abstract edge from $B_i$ to $B_{i+1}$ exists only because of other states of $B_i$. Splitting $B_i$ into $S_i$ and the rest removes the spurious path.

## Example

The concrete system has states $0, \ldots, 5$, the initial state 0, the bad state 5, and the transitions $0 \to 1$, $1 \to 0$, $1 \to 2$, $2 \to 2$, $3 \to 4$, $4 \to 5$, $5 \to 5$. Only 0, 1 and 2 are reachable, so the property holds. The states 3 and 4 form an unreachable path to the bad state.

1. The blocks are $\{5\}$ and $\{0, 1, 2, 3, 4\}$. The abstract path is $\{0, \ldots, 4\} \to \{5\}$, because of $4 \to 5$. Simulation: $S_0 = \{0\}$, and $\mathrm{post}(\{0\}) \cap \{5\} = \emptyset$. So $\{0, \ldots, 4\}$ is split into $\{0\}$ and $\{1, 2, 3, 4\}$.
2. The path is $\{0\} \to \{1, 2, 3, 4\} \to \{5\}$. $S_1 = \{1\}$, and 1 has no successor in $\{5\}$. Split into $\{1\}$ and $\{2, 3, 4\}$.
3. The path is $\{0\} \to \{1\} \to \{2, 3, 4\} \to \{5\}$. $S_2 = \{2\}$, which has no successor in $\{5\}$. Split into $\{2\}$ and $\{3, 4\}$.
4. Now no abstract path leads from $\{0\}$ to $\{5\}$, so the answer is HOLDS after 4 rounds.

The final abstraction has 5 blocks for 6 states. The unreachable states 3 and 4 stay merged, because no spurious path needed them apart. If the transition $2 \to 3$ is added, the third round finds the real path $0, 1, 2, 3, 4, 5$ instead.

## Correctness

**HOLDS is sound.** Every concrete path from $I$ maps under $h$ to an abstract path from an initial block, and each block is inside or outside $\mathit{Bad}$. So if no abstract path reaches a bad block, no concrete path reaches a bad state. The same argument, with the simulation of $M$ by $\hat M$, gives the general theorem of Clarke, Grumberg and Long (1994): if $\hat M$ satisfies an ACTL* formula over propositions that $h$ respects, so does $M$.

**FAILS is sound.** $S_L$ is not empty, and each state of $S_j$ has a predecessor in $S_{j-1}$, with $S_0 \subseteq I$, so a concrete path to a bad state exists.

**Termination.** $S_i$ is not empty, and $B_i \setminus S_i$ is not empty, since some state of $B_i$ has a successor in $B_{i+1}$ and no state of $S_i$ has one. So each refinement adds one block. A partition of $S$ has at most $|S|$ blocks, so there are at most $|S|$ rounds. The full proof is below.

## Complexity

In this explicit-state form, each round takes $O(n + m)$ time: building the abstract edges, the breadth-first search, and the simulation, whose sets $S_j$ lie in distinct blocks. With at most $n$ rounds, the total time is $O(n (n + m))$, and the space is $O(n + m)$. This form only shows the logic of the loop. The point of CEGAR is to never build the concrete system: real tools represent blocks by predicates or BDDs, compute abstract edges with SAT or SMT calls, and simulate the path with a BMC query of the length of the path.

Clarke et al. (2003) show that finding the coarsest refinement that removes a spurious counterexample is NP-hard, so tools use heuristics such as the split above.

## Properties

- **Sound both ways.** HOLDS is a proof, and FAILS comes with a concrete counterexample.
- **Complete for finite systems.** Each round refines the partition, so the loop ends after at most $|S|$ rounds. For infinite-state systems the loop may not end.
- **Universal properties only.** Existential abstraction preserves ACTL* and LTL, not formulas with existential path quantifiers. For full CTL one needs both over- and under-approximations, as in modal or three-valued abstraction.
- **Local refinement.** Only the blocks on spurious paths are split; the rest of the system stays coarse.

## Variants and improvements

- **Loop counterexamples.** For liveness properties and LTL, the abstract counterexample is a lasso. Clarke et al. check it by unrolling the loop a bounded number of times.
- **Predicate abstraction.** The blocks are the cubes over a set of predicates, and refinement adds predicates, for example by weakest preconditions or by interpolation. See [predicate abstraction](/predicate-abstraction/).
- **Lazy abstraction.** Refine only the part of the abstract reachability tree where the spurious path occurred, with different predicates at different program locations. See [lazy abstraction](/lazy-abstraction/).
- **SAT-based refinement.** Later work checks abstract counterexamples with BMC and chooses the refinement from an UNSAT core or an interpolant.
- **Synthesis.** The same guess-and-check pattern, with a learner and a verifier, appears in [CEGIS](/cegis/).

## When to use it

Use CEGAR when the system is too large to model check directly, but the property depends on a small part of its state. This is typical of software, where most variables do not matter for a given assertion. It is less useful when the property depends on almost every state bit, since the refinement then rebuilds most of the concrete system, one split at a time.

## Pitfalls

- **Labels not respected.** If a block contains both bad and good states, the abstract proposition is not defined, and either answer of the loop can be wrong.
- **Under-approximate abstraction.** The abstract transition relation must contain every concrete transition. If an abstract edge is missed, HOLDS is unsound.
- **Existential properties.** A positive result on $\hat M$ says nothing about a formula such as $\mathbf{EF}\,p$.
- **Refining the wrong block.** The split must happen at the failure block $B_i$, between the dead-end states and the others. Splitting another block can leave the same spurious path in place, and the loop can stall.

## Implementations

## History

Abstraction for model checking goes back to Clarke, Grumberg and Long (1994), who proved that existential abstraction preserves ACTL*. Kurshan's localization reduction for hardware also refined abstractions from counterexamples. Clarke, Grumberg, Jha, Lu and Veith (CAV 2000, Journal of the ACM 2003) made the loop automatic for ACTL and LTL with BDDs. The same idea drives the software model checkers SLAM by Ball and Rajamani and BLAST by Henzinger, Jhala, Majumdar and Sutre, which use predicate abstraction.

## References
