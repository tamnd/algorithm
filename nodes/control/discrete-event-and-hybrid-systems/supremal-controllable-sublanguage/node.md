---
tag: 1CMXJG
kind: algorithm
slug: supremal-controllable-sublanguage
name: Supremal controllable sublanguage
aliases:
- supremal controllable sublanguage computation
area: control/discrete-event-and-hybrid-systems
level: core
summary: Computes the largest controllable sublanguage of a regular specification by a fixed point on the product automaton, in time polynomial in the number of product states.
model: word-ram
complexity:
  vars: {n: the number of states of the product of H and G, q: the number of events}
  time: {worst: O(n^2 q)}
  space: {extra: O(n q)}
properties: {deterministic: true, exact: true, online: false}
history:
  year: 1987
  people: [W. Murray Wonham, Peter J. Ramadge]
  note: "Wonham and Ramadge showed in 1987 that the supremal controllable sublanguage exists and is the largest fixpoint of a monotone operator, and that it is regular for regular data."
prereqs: [controllable-language, nonblocking-supervisor, product-construction]
see_also: [supervisory-control-theory, observable-language, normal-language, fixed-point, reactive-synthesis, deterministic-finite-automaton, strongly-connected-components, breadth-first-search]
sources:
  - paper: doi:10.1137/0325036
    title: "W. M. Wonham and P. J. Ramadge, On the supremal controllable sublanguage of a given language, SIAM Journal on Control and Optimization 25(3), 1987, pages 637 to 659"
    locator: the existence of the supremal controllable sublanguage, its characterization as the largest fixpoint of a monotone operator, and its computation for regular languages
  - paper: doi:10.1137/0325013
    title: "P. J. Ramadge and W. M. Wonham, Supervisory control of a class of discrete event processes, SIAM Journal on Control and Optimization 25(1), 1987, pages 206 to 230"
    locator: controllability and the existence of supervisors
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 3, Supervisory Control (the supremal controllable sublanguage and its computation on automata)
  - book: isbn:9783319774510
    title: W. Murray Wonham and Kai Cai, Supervisory Control of Discrete-Event Systems, Springer, 2019
    locator: Chapter 3, Supervision of Discrete-Event Systems, Basics
---

The supremal controllable sublanguage of a specification $K$ is the largest part of $K$ that a supervisor can enforce on a plant $G$, when it may disable only the controllable events. It always exists, because a union of [controllable languages](/controllable-language/) is controllable. When $G$ and the specification are finite automata, it is computed by a fixed point on their [product](/product-construction/): delete every product state where an uncontrollable event of the plant leads out of the remaining states, delete the states that can no longer reach a marked state, and repeat. What is left is a trim automaton. It is at the same time the least restrictive [nonblocking supervisor](/nonblocking-supervisor/) for $K$. The run takes $O(n^2 q)$ time for $n$ product states and $q$ events. Unlike the plain product construction, which only intersects two languages, this algorithm removes states for a reason that looks ahead: a state is bad if an event that nobody can stop leads to a bad state.

## In plain words

You have a machine and a list of rules. You can stop some of the machine's moves, but not all of them. Run the machine and the rule book side by side, so that each joint position says where both are. Some positions are traps: from there, a move you cannot stop breaks a rule. Delete those positions. Then delete every position from which you can no longer finish a job. Deleting positions can make new traps, because a move you cannot stop may now lead into a deleted position. So repeat both steps until nothing changes. The positions that are left, with their moves, are the best controller: it stops a move only when it must.

## The problem

The input is a plant $G = (X_G, \Sigma, \delta_G, x_{0}, X_{m})$, a specification automaton $H$ over the same alphabet, and the set $\Sigma_{uc} \subseteq \Sigma$ of uncontrollable events. Both automata are deterministic and finite. Let $K = L_m(H) \cap L_m(G)$. The output is a trim automaton $A_S$ with

$$L_m(A_S) = \sup C(K), \qquad L(A_S) = \overline{\sup C(K)},$$

where $\sup C(K)$ is the union of all sublanguages $M \subseteq K$ that are controllable, $\overline{M}\,\Sigma_{uc} \cap L(G) \subseteq \overline{M}$. The supervisor is $A_S$ itself, run in parallel with $G$. After a string $s$, it disables the controllable events that $G$ allows but $A_S$ does not.

## The algorithm

$A$ is the accessible part of $H \times G$. Its states are pairs $x = (h, g)$, and a state is marked when both parts are marked. $S$ is the set of states that are still alive.

```pseudo id=main
SUP-C(G, H, Σuc)
L1  A ← accessible part of H × G;  S ← the states of A
L2  repeat
L3      changed ← false
L4      for each state x = (h, g) in S do
L5          if some σ in Σuc has δ_G(g, σ) defined and δ_A(x, σ) undefined or not in S then remove x from S; changed ← true
L6      S' ← the states of S that are accessible and coaccessible inside S;  if S' ≠ S then S ← S'; changed ← true
L7  until not changed
L8  return A restricted to S
```

Line L5 is the controllability test. It looks at the events of the plant at $g$, not at the events of $A$. If the plant can execute an uncontrollable $\sigma$ and the specification does not allow it ($\delta_A(x, \sigma)$ is undefined), or allows it only into a dead state, then the state $x$ is a trap and goes. Line L6 is the nonblocking test. It is a forward [search](/breadth-first-search/) from the initial state and a backward search from the marked states, both inside $S$. The two tests feed each other. Removing a trap can cut the only path to a marked state, and removing a blocking state can make a new trap. So the loop runs until a round changes nothing. The result is the largest [fixed point](/fixed-point/) of the operator "remove traps, then trim", in the sense of Wonham and Ramadge (1987).

## Example

The plant $G$ has states 0 to 4 and the transitions

$$0 \xrightarrow{a} 1, \quad 1 \xrightarrow{u} 2, \quad 2 \xrightarrow{b} 3, \quad 3 \xrightarrow{v} 4, \quad 4 \xrightarrow{d} 0, \quad 0 \xrightarrow{e} 0, \quad 1 \xrightarrow{c} 0,$$

with $\Sigma_{uc} = \{u, v\}$ and the marked state 0. The specification $H$ is the same automaton without the $v$ transition, with all states marked: "the event $v$ must never occur". The product $A$ (line L1) has the 4 states $(0,0)$, $(1,1)$, $(2,2)$ and $(3,3)$ and 5 transitions; state 4 of $G$ is not reached, because $H$ has no $v$. Only $(0,0)$ is marked.

| round | removed at L5 | removed at L6 | $S$ after the round |
|---|---|---|---|
| 1 | $(3,3)$: $G$ can do $v$, $H$ cannot | $(2,2)$: it cannot reach $(0,0)$ any more | $(0,0)$, $(1,1)$ |
| 2 | $(1,1)$: $u$ leads to the removed $(2,2)$ | none | $(0,0)$ |
| 3 | none | none | $(0,0)$, stop |

The result is the state $(0,0)$ with its self-loop $e$, so $\sup C(K) = e^*$. The reason: after $a$, the uncontrollable $u$ may take the plant to state 2. From there, the only way back to the marked state is $b$ and then $v$, which is forbidden. So the supervisor must never enable $a$. The specification itself, $K = (e + ac)^*$, is not controllable, because $a \in \overline{K}$ and $au \in L(G)$ but $au \notin \overline{K}$.

A second example is the buffer of [supervisory control theory](/supervisory-control-theory/). There the product has 8 states and 12 transitions, round 1 removes the two states where the buffer is full and machine 1 works, and the result has 6 states and 8 transitions. The tests of the implementation check both examples.

## Correctness

Let $R$ be the set of states of $A$ that strings of $\overline{\sup C(K)}$ reach. The invariant is $R \subseteq S$: no state of $R$ is ever removed. A state of $R$ passes line L5, because $\sup C(K)$ is controllable, so each uncontrollable event of $G$ leads to another state of $R$. It passes line L6, because the strings of $\sup C(K)$ give paths inside $R$ from the initial state and to a marked state. When the loop stops, $A_S$ is trim and no state fails line L5, so $L_m(A_S)$ is a controllable sublanguage of $K$, and it holds $\sup C(K)$ by the invariant. The two inclusions give equality. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/) with hashing, and $n$ is the number of states of the product $A$ (at most $|X_H| \cdot |X_G|$), $q = |\Sigma|$. Each state has at most $q$ outgoing transitions.

- Line L1 is a search of the product: $O(n q)$.
- One round: line L5 looks at each event of $G$ at the $g$ part of each state of $S$, so $O(n q)$; line L6 is two searches, $O(n q)$.
- Each round except the last removes at least one state, so there are at most $n + 1$ rounds.

The total is $O(n^2 q)$ time and $O(n q)$ space. The bound is in the size of the product, not of $G$ and $H$ alone. In terms of the inputs it is $O(|X_H|^2 |X_G|^2 q)$. This page derives the bound for the program above. The cost of one round can drop with a worklist that, when a state goes, re-tests only its uncontrollable predecessors, but the alternation of the two tests can still need many rounds.

## Properties

- **Exact.** The result is the supremal controllable sublanguage, not an approximation.
- **Least restrictive.** Every other supervisor that keeps the closed loop in $K$ and is nonblocking has a marked language inside $\sup C(K)$.
- **Regular output.** The result is given by a subautomaton of $H \times G$, so $\sup C(K)$ is regular when $K$ is.
- **Possibly empty.** If the initial state goes, $\sup C(K) = \emptyset$, and no nonblocking supervisor exists for $K$.
- **Marking supervisor.** $A_S$ also marks strings. With a supervisor that only disables events, the marked closed-loop language is $\overline{\sup C(K)} \cap L_m(G)$, and it equals $\sup C(K)$ when $\sup C(K)$ is $L_m(G)$-closed. This holds when $K$ is $L_m(G)$-closed, for example when $H$ marks all its states, as in the example above. If $H$ marks only some states, use $A_S$ as a marking supervisor.

## Variants and improvements

- **Prefix-closed specifications.** If only safety matters, drop line L6 except the accessibility part. Then one backward search over uncontrollable transitions removes all traps in $O(n q)$ time, as for the safety part of a game in [reactive synthesis](/reactive-synthesis/).
- **Partial observation.** With unobservable events, the supremal controllable and [normal](/normal-language/) sublanguage replaces it. There is no supremal [observable](/observable-language/) sublanguage in general.
- **Modular and decentralized control.** One supervisor per specification avoids the product of all specifications. The modules must then be checked for conflicts, that is, for blocking of the joint closed loop.
- **Symbolic computation.** For large plants, the states are encoded with binary decision diagrams, and the fixed point is computed on sets of states, as in symbolic model checking.
- **Petri nets.** For nets, [supervision based on place invariants](/supervision-based-on-place-invariants/) adds control places instead of building the reachability graph.

## When to use it

Use it when the plant and the specification are finite automata of moderate size, and you want the least restrictive nonblocking supervisor. The product can be large: it is the product of all component machines and all specifications. If the product does not fit in memory, use modular or symbolic methods. If some events are unobservable, compute the supremal controllable and normal sublanguage instead. If the specification is a temporal logic formula, the problem is one of [reactive synthesis](/reactive-synthesis/).

## Pitfalls

- **Testing the events of $A$ instead of $G$ at line L5.** The test "some uncontrollable $\sigma$ is defined at $x$ in $A$ and leads to a removed state" misses the main case, where $G$ can do $\sigma$ but $H$ forbids it, so $\sigma$ is not defined in $A$ at all. Line L5 must iterate over the events of $G$ at $g$.
- **Stopping after one round.** One pass of line L5 and line L6 is not enough. In the example, round 1 leaves $(1,1)$, from which $u$ leads to a removed state. Line L7 must repeat until a round changes nothing. A test of the implementation checks exactly this case.
- **Trimming without the controllability test, or the reverse.** A trim product of $H$ and $G$ is nonblocking, but it may not be controllable. A controllable product may block. Both lines L5 and L6 are needed in each round.
- **Marking the product by $H$ only.** A state is marked only if both $H$ and $G$ mark it, at line L1. With the marking of $H$ alone, the target language is $L_m(H) \cap L(G)$, and the plant may be stopped in the middle of a task.

## Implementations

## History

Ramadge and Wonham introduced controllable languages and supervisors in 1987, in the SIAM Journal on Control and Optimization. In the same volume, Wonham and Ramadge proved that the supremal controllable sublanguage exists, that it is the largest fixpoint of a monotone operator, and that it can be computed for regular languages. The computation on the product automaton became the standard tool of the theory, and the TCT program of Wonham's group implements it.

## References
