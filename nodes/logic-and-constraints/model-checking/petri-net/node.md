---
tag: 4WAJY4
kind: model
slug: petri-net
name: Petri net
aliases:
- Place/transition net
- P/T net
area: logic-and-constraints/model-checking
level: core
summary: A bipartite graph of places and transitions in which tokens move when transitions fire. It models concurrent systems with unbounded counters but no zero tests.
prereqs: [labelled-transition-system]
see_also: [coverability, karp-miller-tree, petri-net-reachability-decidability, reachability-problem, state-explosion-problem, partial-order-reduction, kripke-structure]
sources:
  - title: Carl Adam Petri, Kommunikation mit Automaten, doctoral dissertation, University of Bonn, 1962
    locator: the original definition of nets of conditions and events
  - paper: doi:10.1109/5.24143
    title: Tadao Murata, Petri nets, properties, analysis and applications, Proceedings of the IEEE 77(4), 1989, pages 541 to 580
    locator: the definitions of nets, firing, the incidence matrix, the state equation, invariants, and the survey of analysis methods
  - paper: "Javier Esparza and Mogens Nielsen, Decidability issues for Petri nets, a survey, Journal of Information Processing and Cybernetics (EIK) 30(3), 1994, pages 143 to 160"
    title: Decidability issues for Petri nets, a survey
    locator: the table of decidable and undecidable problems, and model checking of temporal logics on nets
  - paper: "John Hopcroft and Jean-Jacques Pansiot, On the reachability problem for 5-dimensional vector addition systems, Theoretical Computer Science 8(2), 1979, pages 135 to 159"
    title: John Hopcroft and Jean-Jacques Pansiot, On the reachability problem for 5-dimensional vector addition systems, Theoretical Computer Science 8(2), 1979, pages 135 to 159
    locator: the simulation of vector addition systems with states by vector addition systems, and the semilinearity of reachability sets in small dimension
  - paper: "Michel Hack, Decidability questions for Petri nets, PhD thesis, Massachusetts Institute of Technology, 1976"
    title: Decidability questions for Petri nets
    locator: the reduction between liveness and reachability, and the undecidability of the equality of reachability sets
  - paper: "Allan Cheng, Javier Esparza and Jens Palsberg, Complexity results for 1-safe nets, Theoretical Computer Science 147(1-2), 1995, pages 117 to 136"
    title: Complexity results for 1-safe nets
    locator: PSPACE-completeness of reachability and related problems for 1-safe nets
  - paper: doi:10.1016/0304-3975(78)90036-1
    title: Charles Rackoff, The covering and boundedness problems for vector addition systems, Theoretical Computer Science 6(2), 1978, pages 223 to 231
    locator: the EXPSPACE upper bound for coverability and boundedness
  - paper: "Wojciech Czerwiński and Łukasz Orlikowski, Reachability in vector addition systems is Ackermann-complete, 62nd IEEE Symposium on Foundations of Computer Science (FOCS 2021)"
    title: Reachability in vector addition systems is Ackermann-complete
    locator: the Ackermann lower bound for reachability
---

A *Petri net* is a model of concurrent systems in which the state is a distribution of tokens over places, and transitions consume and produce tokens. Carl Adam Petri introduced nets in his 1962 dissertation. A net can describe processes that run in parallel, synchronize, compete for resources, and create or destroy unboundedly many objects, all with a small finite description. The price is that the state space can be infinite. The central questions are whether a marking can be reached, whether it can be covered, and whether the net is bounded. These questions are all decidable, but they are among the hardest decidable problems in verification: [coverability](/coverability/) is EXPSPACE-complete and [reachability](/petri-net-reachability-decidability/) is Ackermann-complete.

## The machine

**Syntax.** A *Petri net* is a tuple $N = (P, T, \mathrm{pre}, \mathrm{post})$, where

- $P$ is a finite set of *places*, drawn as circles;
- $T$ is a finite set of *transitions*, disjoint from $P$, drawn as bars or boxes;
- $\mathrm{pre}, \mathrm{post} : T \to \mathbb{N}^P$ give the arc weights. There is an arc from $p$ to $t$ with weight $\mathrm{pre}(t)(p)$ when this is positive, and an arc from $t$ to $p$ with weight $\mathrm{post}(t)(p)$ when this is positive.

So a net is a bipartite directed graph with weighted arcs. The places with an arc into $t$ form the *preset* ${}^\bullet t$, and the places with an arc from $t$ form the *postset* $t^\bullet$.

**States.** A *marking* is a vector $M \in \mathbb{N}^P$: $M(p)$ is the number of tokens in place $p$, drawn as dots. A *marked net* is a pair $(N, M_0)$ with an initial marking.

**Firing.** A transition $t$ is *enabled* in $M$ when $M \ge \mathrm{pre}(t)$ in each place. An enabled transition can *fire*, and this gives

$$M' = M - \mathrm{pre}(t) + \mathrm{post}(t),$$

written $M \xrightarrow{t} M'$. For a sequence $\sigma = t_1 \cdots t_k$ we write $M \xrightarrow{\sigma} M'$ when there are markings with $M \xrightarrow{t_1} M_1 \to \cdots \xrightarrow{t_k} M'$. The marking $M'$ is *reachable* from $M_0$ when $M_0 \xrightarrow{\sigma} M'$ for some $\sigma$. The set of reachable markings is $R(N, M_0)$.

**The reachability graph.** The markings in $R(N, M_0)$, with an edge labelled $t$ from $M$ to $M'$ when $M \xrightarrow{t} M'$, form a [labelled transition system](/labelled-transition-system/), the *reachability graph*. This is the interleaving semantics of the net: at each step one enabled transition fires. Labelling the markings with atomic propositions such as "place $p$ is marked" gives a [Kripke structure](/kripke-structure/), so temporal logics can be interpreted on nets.

**Linear algebra.** The *incidence matrix* $C \in \mathbb{Z}^{P \times T}$ has columns $C_t = \mathrm{post}(t) - \mathrm{pre}(t)$. If $M_0 \xrightarrow{\sigma} M$ and $x \in \mathbb{N}^T$ counts how often each transition occurs in $\sigma$, then

$$M = M_0 + C x.$$

This *state equation* is a necessary condition for reachability, not a sufficient one, because it ignores the order of firings and whether each transition is enabled when it fires. A vector $y \in \mathbb{Z}^P$ with $y^\top C = 0$ is a *place invariant*: $y^\top M = y^\top M_0$ for every reachable $M$.

**Example.** A producer and a consumer share an unbounded buffer. The places are $\mathit{p_{ready}}$, $\mathit{p_{done}}$, $\mathit{buf}$, $\mathit{c_{ready}}$, $\mathit{c_{done}}$. The transition $\mathit{produce}$ moves the producer token from $\mathit{p_{ready}}$ to $\mathit{p_{done}}$; $\mathit{put}$ moves it back and adds a token to $\mathit{buf}$; $\mathit{take}$ needs a token in $\mathit{buf}$ and the consumer token in $\mathit{c_{ready}}$, and moves the consumer token to $\mathit{c_{done}}$; $\mathit{consume}$ moves it back. From $M_0$ with one token in $\mathit{p_{ready}}$ and one in $\mathit{c_{ready}}$, the sequence $\mathit{produce}\ \mathit{put}\ \mathit{produce}\ \mathit{put}$ gives two tokens in $\mathit{buf}$, and then $\mathit{take}$ fires. The net is unbounded in $\mathit{buf}$. The vectors $y = \mathbf{1}_{p_{ready}} + \mathbf{1}_{p_{done}}$ and $y = \mathbf{1}_{c_{ready}} + \mathbf{1}_{c_{done}}$ are place invariants, so each of the two processes is always in exactly one local state.

**Common restrictions.**

- A net is *$k$-bounded* when no reachable marking has more than $k$ tokens in a place, and *1-safe* when $k = 1$. A 1-safe net is a finite-state system written compactly: a net with $n$ places can have $2^n$ reachable markings.
- A *state machine* has $|{}^\bullet t| = |t^\bullet| = 1$ for every transition, and a *marked graph* has each place with one input and one output transition. *Free-choice nets* allow choice and synchronization only in a restricted pattern. These classes have polynomial or much cheaper algorithms for many questions.
- *Inhibitor arcs* let a transition fire only when a place is empty. They add zero tests, and with two places that can be tested for zero, nets can simulate two-counter machines, so reachability becomes undecidable.

## What it counts

The model measures the cost of decision problems about a marked net in the size of its description: the number of places and transitions and the bits of the arc weights and of the markings, all written in binary. Typical problems are:

- **Reachability:** is $M \in R(N, M_0)$?
- **[Coverability](/coverability/):** is there $M' \in R(N, M_0)$ with $M' \ge M$?
- **Boundedness:** is $R(N, M_0)$ finite?
- **Deadlock:** is there a reachable marking in which no transition is enabled?
- **Liveness:** can each transition be enabled again from every reachable marking?
- **Model checking:** does the reachability graph satisfy a temporal formula?

The reachability graph is often infinite, and when it is finite it is often exponential in the size of the net. This is the [state explosion problem](/state-explosion-problem/) in its purest form: $n$ independent components each with two states give one net with $2n$ places and a reachability graph with $2^n$ markings. Transitions with disjoint presets and postsets are *independent*: they can fire in either order with the same result. [Partial-order reduction](/partial-order-reduction/) and net unfoldings (McMillan 1992) exploit this to avoid exploring all interleavings.

## Relation to other models

- **Vector addition systems.** A $d$-dimensional *vector addition system* (VAS) is a finite set of vectors in $\mathbb{Z}^d$ and an initial vector in $\mathbb{N}^d$. A vector can be added when the sum stays in $\mathbb{N}^d$. A Petri net gives a VAS with the vectors $C_t$, except that a net can require tokens in a place it does not change, which a VAS cannot express directly. Adding one extra place per transition removes this difference, so nets and VAS have the same reachability, coverability and boundedness problems, up to polynomial-time reductions. A *vector addition system with states* (VASS) adds a finite control; Hopcroft and Pansiot (1979) showed that a $d$-dimensional VASS can be simulated by a $(d + 3)$-dimensional VAS.
- **Counter machines.** A net is a counter machine with nondeterminism and without zero tests. Each counter can be incremented and decremented, and a decrement blocks at zero. This lack of zero tests is what makes reachability decidable. A Minsky machine with two counters and zero tests is Turing complete, so its [halting problem](/halting-problem/) is undecidable.
- **Finite automata and transition systems.** The reachability graph of a bounded net is a finite [labelled transition system](/labelled-transition-system/). A 1-safe net with $n$ places is an exponentially succinct description of a finite automaton, and reachability for 1-safe nets is PSPACE-complete (Cheng, Esparza and Palsberg 1995).
- **Pushdown systems.** Nets count without order, while a [pushdown system](/pushdown-system/) has a stack with order but no counting across separate stacks. Neither model simulates the other, and for their combination, vector addition systems with a stack, the decidability of reachability is open in general.
- **Chemistry and biology.** A net is the same object as a chemical reaction network with integer molecule counts: places are species, transitions are reactions. Commutative semigroup presentations give the same reachability questions.

## Known results in the model

| Problem | Status | Source |
|---|---|---|
| Coverability, boundedness | EXPSPACE-complete | Lipton 1976, Rackoff 1978 |
| Coverability and boundedness by enumeration | Decidable by the [Karp-Miller tree](/karp-miller-tree/) | Karp and Miller 1969 |
| Reachability | Decidable; Ackermann-complete | Mayr 1981, Kosaraju 1982; Czerwiński and Orlikowski 2021, Leroux 2021 |
| Liveness | Decidable; recursively equivalent to reachability | Hack 1976 |
| Reachability for 1-safe nets | PSPACE-complete | Cheng, Esparza and Palsberg 1995 |
| Equality or inclusion of reachability sets | Undecidable | Rabin; Hack 1976 |
| Semilinearity of the reachability set | Holds for VAS of dimension at most 5, fails in dimension 6 | Hopcroft and Pansiot 1979 |
| Linear-time temporal logic over firing sequences | Decidable for many action-based logics | Esparza and Nielsen 1994 |
| Branching-time temporal logic | Undecidable even for weak fragments | Esparza and Nielsen 1994 |

The decidability of reachability is the main theorem of the area and has its own page, [decidability of Petri net reachability](/petri-net-reachability-decidability/). The gap between coverability and reachability is large: coverability needs only monotonicity and Dickson's lemma, while reachability needs the decomposition of Mayr, Kosaraju and Lambert, or the semilinear inductive invariants of Leroux.

## References

- Carl Adam Petri, Kommunikation mit Automaten, doctoral dissertation, University of Bonn, 1962.
- Tadao Murata, Petri nets, properties, analysis and applications, Proceedings of the IEEE 77(4), 1989, pages 541 to 580.
- Javier Esparza and Mogens Nielsen, Decidability issues for Petri nets, a survey, Journal of Information Processing and Cybernetics 30(3), 1994, pages 143 to 160.
- John Hopcroft and Jean-Jacques Pansiot, On the reachability problem for 5-dimensional vector addition systems, Theoretical Computer Science 8(2), 1979, pages 135 to 159.
- Michel Hack, Decidability questions for Petri nets, PhD thesis, MIT, 1976.
- Allan Cheng, Javier Esparza and Jens Palsberg, Complexity results for 1-safe nets, Theoretical Computer Science 147(1-2), 1995, pages 117 to 136.
- Charles Rackoff, The covering and boundedness problems for vector addition systems, Theoretical Computer Science 6(2), 1978, pages 223 to 231.
- Wojciech Czerwiński and Łukasz Orlikowski, Reachability in vector addition systems is Ackermann-complete, FOCS 2021.
