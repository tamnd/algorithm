---
tag: 4BRYXV
kind: problem
slug: incompletely-specified-fsm-minimization
name: Incompletely specified FSM minimization
aliases:
- state reduction with don't-cares
- ISFSM state minimization
area: eda/logic-synthesis
level: advanced
summary: Find a machine with fewest states that covers an incompletely specified FSM. It is NP-hard, unlike DFA minimization, and is solved by compatibles and covering.
prereqs: [mealy-machine, dfa-minimization, binate-covering-problem]
see_also: [state-assignment, dont-care-condition, hopcroft-minimization, myhill-nerode-theorem, nfa-minimization, maximal-clique, clique-cover, chromatic-number]
sources:
  - paper: "M. C. Paull and S. H. Unger, Minimizing the number of states in incompletely specified sequential switching functions, IRE Transactions on Electronic Computers EC-8(3), 356 to 367, 1959"
    title: Minimizing the number of states in incompletely specified sequential switching functions
    locator: compatible states, implied pairs, closed covers, and the example that a minimum machine may need overlapping classes
  - paper: "A. Grasselli and F. Luccio, A method for minimizing the number of internal states in incompletely specified sequential networks, IEEE Transactions on Electronic Computers EC-14(3), 350 to 359, 1965"
    title: A method for minimizing the number of internal states in incompletely specified sequential networks
    locator: prime compatibles, and the selection of a minimum closed cover as a covering problem with closure conditions
  - paper: doi:10.1109/T-C.1973.223655
    title: Charles P. Pfleeger, State reduction in incompletely specified finite-state machines, IEEE Transactions on Computers, 1973
    locator: the NP-completeness of state reduction for incompletely specified machines
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9, Sequential Logic Optimization (state minimization of completely and incompletely specified machines)
---

Incompletely specified FSM minimization asks for a finite state machine with the fewest states that behaves like a given machine wherever the given machine is specified. Some next states and some outputs of the given machine are left open, as [don't-cares](/dont-care-condition/). For a completely specified machine, equivalent states form a partition, and [DFA minimization](/dfa-minimization/) finds the unique smallest machine in polynomial time. With don't-cares, the relation "these two states can be merged" is not transitive, a minimum machine may need a state to sit in two merged groups, and the problem is NP-hard. The classical exact method lists the compatible sets of states and then selects a smallest closed cover, which is a [binate covering problem](/binate-covering-problem/).

## In plain words

A controller is described by a table: in this state, on this input, go to that state and give that output. Some entries are blank, because the designer knows the case never happens or does not care. Fewer states mean fewer flip-flops and smaller logic, so you want to merge states. Two states can be merged if no input sequence makes them give clearly different outputs. With blanks, A may fit with B and B with C while A does not fit with C. So the groups of merged states can overlap, and you must also make sure that wherever a group goes on an input, the result lies inside some group you chose. Choosing the fewest such groups is a hard search problem.

## Definition

**Input.** A Mealy machine $M = (S, I, O, \delta, \lambda)$ with finite sets of states $S$, inputs $I$ and outputs $O$, a partial next state map $\delta : S \times I \rightharpoonup S$, and a partial output map $\lambda : S \times I \rightharpoonup O$. (A Moore machine is the special case where the output depends on the state only.)

**Specified behavior.** For a state $s$ and an input sequence $u = a_1 \cdots a_k$, run $M$ from $s$ while the next states are specified. The specified outputs along the run are the outputs that $M$ promises on $u$. Once a next state is unspecified, nothing more is promised.

**Feasible solutions.** A machine $M'$ covers $M$ when for every state $s$ of $M$ there is a state $s'$ of $M'$ such that, for every input sequence, $M'$ from $s'$ gives every output that $M$ from $s$ promises, at the same positions. $M'$ may be completely specified.

**Objective.** Minimize the number of states of $M'$.

**Decision version.** Given $M$ and $k$, is there a machine with at most $k$ states that covers $M$?

**Compatibles.** Two states are compatible when no input sequence makes both promise different outputs at the same position. A set of states is a compatible when its states are pairwise compatible. A compatible $C$ implies, for each input $a$, the set $\delta(C, a)$ of specified next states. A set of compatibles is closed when every implied set of every member lies inside some member. Paull and Unger (1959) showed that the minimum number of states of a covering machine is the least size of a closed set of compatibles that covers $S$, a minimum closed cover.

## Variants

- **Completely specified.** All entries are given. Compatibility is equivalence, the closed cover is the partition into equivalence classes, and [Hopcroft's algorithm](/hopcroft-minimization/) solves it in $O(|I|\, |S| \log |S|)$ time.
- **Unspecified outputs only.** All next states are given and some outputs are open. The problem stays NP-hard, since the reduction below has all next states specified.
- **Unspecified next states only.** All outputs are given and some next states are open. Compatibility is still not transitive in general, because a state with an open next state can be compatible with two states that are not compatible with each other.
- **Moore machines.** Outputs on states. The same theory applies, with output conflicts tested per state.
- **Input don't-cares from the environment.** Some input sequences never occur, because of the circuit around the machine. These sequential don't-cares give another form of incomplete specification.
- **Nondeterministic specifications.** If a state may move to any of a set of next states, the problem is close to [NFA minimization](/nfa-minimization/), which is PSPACE-hard.

## Examples

Take a Mealy machine with states $A, B, C, D$, one input bit $x$, and one output bit. A dash is a don't-care.

| state | next, $x = 0$ | next, $x = 1$ | out, $x = 0$ | out, $x = 1$ |
|---|---|---|---|---|
| $A$ | $A$ | $C$ | 0 | − |
| $B$ | $A$ | $D$ | − | 0 |
| $C$ | $B$ | $C$ | 1 | − |
| $D$ | $C$ | − | − | 1 |

**Pairs.** $A$ and $C$ conflict on $x = 0$, and $B$ and $D$ conflict on $x = 1$. The pair $AD$ implies $AC$ on $x = 0$, so it is incompatible too. The compatible pairs are $AB$, which implies $CD$; $BC$, which implies $AB$ and $CD$; and $CD$, which implies $BC$. No triple is compatible, so the maximal compatibles are $AB$, $BC$ and $CD$.

**Covers.** $\{AB, CD\}$ covers all four states with two classes, but it is not closed, since $CD$ implies $BC$. The only closed cover with three classes is $\{AB, BC, CD\}$, and the classes overlap at $B$ and at $C$. No partition of the states into three classes is closed. An exhaustive search over all machines with 1, 2 and 3 states confirms that no machine with 1 or 2 states covers $M$, and that 12 machines with 3 states do.

**A minimum machine.** With $P = AB$, $Q = BC$ and $R = CD$:

| state | next, $x = 0$ | next, $x = 1$ | out, $x = 0$ | out, $x = 1$ |
|---|---|---|---|---|
| $P$ | $P$ | $R$ | 0 | 0 |
| $Q$ | $P$ | $R$ | 1 | 0 |
| $R$ | $Q$ | $Q$ | 1 | 1 |

For example, $Q = \{B, C\}$ on $x = 0$ goes to $\{A, B\} = P$ and must output 1, because $C$ promises 1. State $A$ of $M$ is covered by $P$, $B$ by $P$ or $Q$, $C$ by $Q$ or $R$, and $D$ by $R$. The covering problem for this example is worked out on the [binate covering](/binate-covering-problem/) page.

## Known algorithms

- **Compatibles and closed covers.** Paull and Unger (1959). Find the incompatible pairs by a fixed point on implied pairs, list the compatibles, and search for a minimum closed cover. The search is exponential in the worst case.
- **Prime compatibles and binate covering.** Grasselli and Luccio (1965). A compatible is prime when no larger compatible implies only a subfamily of its implied sets. Some minimum closed cover uses only prime compatibles. The selection is a binate covering problem with one variable per prime compatible, clauses "some chosen compatible contains $s$" for each state, and closure clauses "if $C$ is chosen, some chosen compatible contains $\delta(C, a)$". Branch and bound, BDD-based, or 0-1 programming solvers then select the cover.
- **Maximal compatibles.** The maximal compatibles are the [maximal cliques](/maximal-clique/) of the graph of compatible pairs, listed for example by [Bron-Kerbosch](/bron-kerbosch/). When no compatible implies anything, a minimum cover by maximal compatibles is a minimum [clique cover](/clique-cover/).
- **Implicit methods.** Represent the sets of compatibles and the covering table by BDDs, to handle machines with very many compatibles.
- **Heuristics.** Merge compatible states greedily, or choose a closed cover without an optimality proof, for large machines.

## Bounds

**Upper bounds (proved).**

- The decision version is in NP: a machine with at most $k \le |S|$ states and, for each state of $M$, a covering state are a certificate, and the covering can be checked in polynomial time on the product of the two machines.
- The exact method by compatibles takes time exponential in $|S|$, since there can be $2^{\Theta(|S|)}$ compatibles.
- The incompatible pairs can be found in polynomial time, by a fixed point that marks a pair when its outputs conflict or when it implies a marked pair.

**Lower bounds (proved, as hardness).**

- The decision version is NP-complete (Pfleeger 1973). A short proof from [graph coloring](/graph-coloring/): for a graph $G$, build a machine with one state per vertex, one input symbol per edge, and one output bit. On the input of the edge $uv$, state $u$ outputs 0, state $v$ outputs 1, and the other states leave the output open. Every state goes to itself on every input. Two states are compatible exactly when their vertices are not adjacent, and a compatible $C$ implies only $C$ itself, so every set of compatibles is closed. So a minimum covering machine has $\chi(G)$ states, the [chromatic number](/chromatic-number/) of $G$.
- In contrast, the completely specified case has a unique minimum machine, found in $O(|I|\,|S| \log |S|)$ time.

**Measured.** No measured figures are quoted here. The covering table has one column per prime compatible, and that number can be exponential in the number of states, so it is the size that the exact tools must handle in practice.

## Reductions

- **From graph coloring.** As above. The same construction shows that the minimum can be far from the lower bound given by a largest set of pairwise incompatible states.
- **To binate covering.** The selection of a minimum closed cover from the prime compatibles is a [binate covering problem](/binate-covering-problem/), and so it can be given to a MaxSAT or 0-1 programming solver.
- **From and to DFA minimization.** A completely specified machine is a deterministic automaton with output, and the problem becomes [DFA minimization](/dfa-minimization/), with equivalence in the role of compatibility.

## Applications

- **Controller synthesis.** State tables written by hand, or derived from protocols and flow charts, leave many entries open. State reduction before [state assignment](/state-assignment/) gives fewer flip-flops and smaller next-state logic.
- **Sequential don't-cares.** A machine that drives or is driven by another machine sees only some input sequences. The unused behavior becomes don't-cares, and minimization uses them.
- **Asynchronous circuits.** Flow tables of asynchronous circuits are often incompletely specified, and the same method reduces them.

## References
