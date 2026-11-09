---
tag: B5EQZD
kind: concept
slug: state-explosion-problem
name: State explosion problem
aliases:
- State space explosion
- combinatorial explosion of states
area: logic-and-constraints/model-checking
level: core
summary: The number of states of a system grows exponentially with its processes and variables. It is the main limit of model checking, and every reduction only pushes it back.
prereqs: [kripke-structure, explicit-state-model-checking]
see_also: [partial-order-reduction, symmetry-reduction, symbolic-model-checking, bitstate-hashing, compositional-verification, predicate-abstraction, reachability-problem, dining-philosophers-problem]
sources:
  - paper: "Antti Valmari, The state explosion problem, Lectures on Petri Nets I: Basic Models, Lecture Notes in Computer Science 1491, Springer, 1998"
    locator: the survey of the sources of explosion and of the reduction methods (stubborn sets, symmetry, compositional methods)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 2, Section 2.3 (the state-space explosion problem, with the size of interleavings and of program graphs with variables)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 1 (the state explosion problem) and Chapters 10 to 14 (partial-order reduction, abstraction, symmetry and compositional reasoning)
  - paper: "Dexter Kozen, Lower bounds for natural proof systems, 18th Annual Symposium on Foundations of Computer Science (FOCS 1977), IEEE, 1977"
    locator: PSPACE-completeness of the emptiness of the intersection of finite automata
  - paper: "Edmund M. Clarke, William Klieber, Miloš Nováček and Paolo Zuliani, Model checking and the state explosion problem, Tools for Practical Software Verification (LASER Summer School 2011), Lecture Notes in Computer Science 7682, Springer, 2012"
    locator: overview of symbolic methods, partial-order reduction, abstraction and bounded model checking as answers to state explosion
---

The state explosion problem is the fact that the state space of a system grows exponentially with the size of its description. A system of $n$ processes, each with $k$ local states, can have $k^n$ global states, and each Boolean variable doubles the count. Model checking algorithms are linear or polynomial in the number of states, so the exponential lives in the input to them. It is the main practical limit of model checking. Partial-order reduction, symmetry, symbolic representations, abstraction and compositional methods each push the limit back on many real systems, but none of them removes it in the worst case, because the underlying question is [PSPACE](/pspace/)-hard in the size of the description.

## In plain words

A light switch has two positions. Ten switches have $2^{10} = 1024$ combinations, and forty switches have more than a million million. A program is like a row of switches: every variable, every thread position and every message in a queue is one more switch. A checker that looks at each combination of the whole program runs out of time and memory long before the program looks big to a person.

The many orders in which threads can take turns make it worse. Three threads that each do four steps can interleave in tens of thousands of ways. Most of these orders lead to the same result, but a plain search does not know that. The methods against state explosion try to skip work that cannot change the answer, or to handle many states at once.

## The idea

**The product bound.** Let a system have $n$ processes with local state sets $L_1, \ldots, L_n$ and shared variables with finite domains $D_1, \ldots, D_v$. A global state is a choice of one local state per process and one value per variable, so the set $S$ of states satisfies

$$|S| \;\le\; \prod_{i=1}^{n} |L_i| \cdot \prod_{j=1}^{v} |D_j| \;\le\; k^n \cdot \prod_{j=1}^{v} |D_j| \quad \text{when each } |L_i| \le k.$$

Channels count as variables: a channel of capacity $c$ over an alphabet of size $a$ has $\sum_{i=0}^{c} a^i$ contents.

**The bound is reached.** Take $n$ processes without shared variables, where process $i$ cycles through local states $0, 1, \ldots, k-1$. Every vector $(\ell_1, \ldots, \ell_n)$ is reachable: move process 1 $\ell_1$ times, then process 2 $\ell_2$ times, and so on. So exactly $k^n$ states are reachable, while the description has size $O(nk)$. In the same way, a circuit with $n$ latches can reach all $2^n$ valuations.

**Interleavings.** Even without shared state, the runs multiply. If $n$ processes each make $k$ steps, the number of different orders of the $nk$ steps is the multinomial coefficient

$$\frac{(nk)!}{(k!)^n},$$

which is $20$ for two processes of three steps, $90$ for three processes of two steps, and $34{,}650$ for three processes of four steps. All these runs end in the same state. A search over states visits only the $(k+1)^n$ states, but a search over runs, as in [stateless model checking](/stateless-model-checking/), sees every order unless it uses [sleep sets](/sleep-sets/) or [dynamic partial-order reduction](/dynamic-partial-order-reduction/).

**A hardness statement.** The question "is a product state reachable in the product of $n$ finite automata, each given explicitly?" is PSPACE-complete, because the emptiness of the intersection of $n$ [deterministic finite automata](/deterministic-finite-automaton/) is PSPACE-complete (Kozen 1977). The same holds for [LTL model checking](/ltl-model-checking/) of a system given as a parallel composition. So an algorithm that ran in time polynomial in the size of the components would prove P = PSPACE. This does not say that every system explodes; it says that no method can avoid the explosion on every system unless P = PSPACE.

**What the reductions do.** Each method exploits a structure that many real systems have and some do not:

| Method | Structure it exploits | Worst case |
|---|---|---|
| [Partial-order reduction](/partial-order-reduction/) | independent steps of different processes | no gain when all steps are dependent |
| [Symmetry reduction](/symmetry-reduction/) | identical processes or data that can be permuted | no gain without symmetry; computing canonical forms can be as hard as [graph isomorphism](/graph-isomorphism-problem/) |
| [Symbolic model checking](/symbolic-model-checking/) with BDDs | regular structure of the transition relation | the BDDs can be exponential in every variable order (multiplication) |
| [Bounded model checking](/bounded-model-checking/) with SAT | short counterexamples | the bound needed for a proof can be as large as the diameter |
| [Predicate abstraction](/predicate-abstraction/) and [CEGAR](/cegar/) | properties that depend on few facts about the data | refinement may not terminate, or may need many predicates |
| [Compositional verification](/compositional-verification/) | interfaces smaller than components | the right assumptions can be as large as the components |
| [Bitstate hashing](/bitstate-hashing/) | memory per state, not number of states | the search can miss states |

Papers on each method report large gains on their benchmark sets, often by several orders of magnitude, and these gains are measured, not proved. The worst case stays exponential.

## Examples

**Independent counters.** Three processes, each a counter from 0 to 2 with private variables, have $3^3 = 27$ states. A static partial-order reduction explores one order of the independent steps and visits only $n(k-1) + 1 = 3 \cdot 2 + 1 = 7$ states, which keeps the single deadlock state at the end. The implementation on the [partial-order reduction](/partial-order-reduction/) page reproduces these counts for $(n, k) = (2, 4), (3, 3)$ and $(4, 3)$.

**Dining philosophers.** In the [dining philosophers](/dining-philosophers-problem/) model where each philosopher thinks, takes the left fork, takes the right fork, eats, and puts both forks down, an exhaustive search gives these numbers of reachable states:

| $n$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| states | 6 | 14 | 34 | 82 | 198 | 478 | 1154 | 2786 | 6726 |

Each value is twice the one before plus the one before that, and the values equal $(1+\sqrt{2})^n + (1-\sqrt{2})^n$, so the count grows by a factor of about $2.41$ per philosopher. For each $n$ there is exactly one deadlock: every philosopher holds the left fork. Finding it needs only one path of $n$ steps, but proving that there is no other deadlock needs all states.

**Peterson's algorithm with data.** The two-process Peterson model on the [explicit-state model checking](/explicit-state-model-checking/) page has 34 reachable states. If each process also keeps a private 8-bit counter that it increments in the critical section, the number of states can grow up to $256^2$ times, although the counters are irrelevant to mutual exclusion. Removing such variables, by slicing or abstraction, is often the most effective reduction.

## Where it is used

- It sets the agenda of the field: the methods of the table above, and the choice between explicit and symbolic tools, are all answers to it.
- It decides how a model is written: designers of models keep the number of atomic steps small, bound buffers and data, and abstract away irrelevant variables, because each detail multiplies the state count.
- It explains the shift from proving properties to finding bugs: [bounded model checking](/bounded-model-checking/), [stateless model checking](/stateless-model-checking/) and [bitstate hashing](/bitstate-hashing/) trade completeness for coverage of the parts of the state space where bugs usually are.
- It is the reason for parameterized and inductive methods, such as [k-induction](/k-induction/) and [IC3](/ic3-pdr/), which prove properties without listing the reachable states.

## References
