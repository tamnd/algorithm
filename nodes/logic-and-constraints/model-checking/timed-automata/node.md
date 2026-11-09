---
tag: TNN2J6
kind: model
slug: timed-automata
name: Timed automata
aliases:
- Alur-Dill automata
- Timed automaton
area: logic-and-constraints/model-checking
level: advanced
summary: Finite automata with real-valued clocks that grow at rate 1 and are tested against integer constants. Reachability is PSPACE-complete, and universality is undecidable.
prereqs: [nondeterministic-finite-automaton, labelled-transition-system, reachability-problem]
see_also: [region-graph, difference-bound-matrix, hybrid-automata, buchi-automaton, pspace, bisimulation, safety-property, state-explosion-problem]
sources:
  - paper: doi:10.1016/0304-3975(94)90010-8
    title: Rajeev Alur and David L. Dill, A theory of timed automata, Theoretical Computer Science 126(2), 1994, pages 183 to 235
    locator: the definition of timed automata and timed Büchi automata, regions, the PSPACE-completeness of emptiness, the undecidability of universality and inclusion, and the closure properties
  - paper: "Rajeev Alur, Costas Courcoubetis and David L. Dill, Model-checking in dense real-time, Information and Computation 104(1), 1993, pages 2 to 34"
    title: Model-checking in dense real-time
    locator: the logic TCTL and its model checking over timed automata by the region graph
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 9 (timed automata, their semantics as transition systems, time divergence and Zeno behaviour, regions, and TCTL model checking)
  - paper: "Johan Bengtsson and Wang Yi, Timed automata: semantics, algorithms and tools, Lectures on Concurrency and Petri Nets, Lecture Notes in Computer Science 3098, Springer, 2004, pages 87 to 124"
    title: "Timed automata: semantics, algorithms and tools"
    locator: the syntax and semantics with invariants, zones, and the algorithms used in UPPAAL
  - paper: "Thomas A. Henzinger, Zohar Manna and Amir Pnueli, What good are digital clocks?, ICALP 1992, Lecture Notes in Computer Science 623, Springer, pages 545 to 558"
    title: What good are digital clocks?
    locator: digitization, by which integer time suffices for some properties when all constraints are non-strict
  - paper: "Patricia Bouyer, Forward analysis of updatable timed automata, Formal Methods in System Design 24(3), 2004, pages 281 to 320"
    title: Forward analysis of updatable timed automata
    locator: the exactness of zone extrapolation for diagonal-free timed automata and its failure with diagonal constraints
---

A *timed automaton* is a finite automaton with a finite set of real-valued *clocks*. All clocks grow at rate 1 while the automaton waits in a location. An edge can fire only when its *guard*, a condition such as $x \le 3 \wedge y > 1$, holds, and it can reset some clocks to 0. Location *invariants* such as $x \le 5$ force the automaton to leave before the bound runs out. Alur and Dill introduced the model in 1990 and gave the full theory in 1994. It describes real-time protocols, controllers and schedulers. Its state space is uncountable, but the [region graph](/region-graph/) shows that location reachability is decidable, and it is PSPACE-complete. In practice tools search with zones stored as [difference bound matrices](/difference-bound-matrix/). The model sits on a sharp border. Small extensions, such as clocks that can stop or run at other rates, give [hybrid automata](/hybrid-automata/), where reachability is undecidable. Also, language universality and inclusion are already undecidable for timed automata themselves.

## The machine

**Clock constraints.** Let $C$ be a finite set of clocks. A *clock constraint* is a conjunction of atomic constraints $x \sim c$, with $x \in C$, $\sim \in \{<, \le, =, \ge, >\}$ and $c \in \mathbb{N}$. Some definitions also allow *diagonal* constraints $x - y \sim c$. An automaton without them is *diagonal-free*. A *valuation* is a map $v : C \to \mathbb{R}_{\ge 0}$. For $d \ge 0$, $v + d$ adds $d$ to every clock, and for $Y \subseteq C$, $v[Y := 0]$ sets the clocks in $Y$ to 0.

**Syntax.** A *timed automaton* is a tuple $A = (L, \ell_0, \Sigma, C, E, \mathrm{Inv})$ with

- a finite set $L$ of *locations* and an initial location $\ell_0$;
- a finite alphabet $\Sigma$ of actions and a finite set $C$ of clocks;
- a finite set $E$ of edges $(\ell, a, g, Y, \ell')$, with a guard $g$ and a set $Y \subseteq C$ of clocks to reset;
- an *invariant* $\mathrm{Inv}(\ell)$ for each location, a clock constraint that uses only upper bounds $x < c$ and $x \le c$.

**Semantics.** The meaning of $A$ is an infinite [labelled transition system](/labelled-transition-system/). Its states are pairs $(\ell, v)$ such that $v$ satisfies $\mathrm{Inv}(\ell)$, and the initial state is $(\ell_0, \mathbf{0})$. There are two kinds of step:

- a *delay* $(\ell, v) \xrightarrow{d} (\ell, v + d)$ for $d \in \mathbb{R}_{\ge 0}$, allowed when $v + d$ satisfies $\mathrm{Inv}(\ell)$, which then holds for the whole delay because invariants are upper bounds;
- an *action* $(\ell, v) \xrightarrow{a} (\ell', v[Y := 0])$ for an edge $(\ell, a, g, Y, \ell')$, allowed when $v$ satisfies $g$ and $v[Y := 0]$ satisfies $\mathrm{Inv}(\ell')$.

A *run* alternates delays and actions. It reads the *timed word* $(a_1, t_1)(a_2, t_2) \cdots$, where $t_i$ is the total time at the $i$-th action. A run is *Zeno* when it has infinitely many actions in finite total time. Such runs are physically meaningless, and analyses usually exclude them. A *timed Büchi automaton* also has a set of accepting locations, and it accepts the infinite timed words that have a non-Zeno run through them infinitely often.

**Example.** A double-click detector has locations $\mathit{idle}$, $\mathit{one}$ and $\mathit{double}$ and one clock $x$:

- $\mathit{idle} \xrightarrow{\mathit{click},\ x := 0} \mathit{one}$;
- $\mathit{one} \xrightarrow{\mathit{click},\ x < 1} \mathit{double}$;
- $\mathit{one} \xrightarrow{\mathit{click},\ x \ge 1,\ x := 0} \mathit{one}$.

On the timed word $(\mathit{click}, 0.2)(\mathit{click}, 1.5)(\mathit{click}, 2.1)$ the run goes to $\mathit{one}$ with $x = 0$ at time 0.2. At time 1.5, $x = 1.3 \ge 1$, so it stays in $\mathit{one}$ and resets $x$. At time 2.1, $x = 0.6 < 1$, so it reaches $\mathit{double}$. The constant 1 is the only one, so by the [region graph](/region-graph/) only four classes of clock values matter: $x = 0$, $0 < x < 1$, $x = 1$ and $x > 1$.

**Networks.** Systems are written as networks of timed automata that synchronize on actions or on channels and share clocks or integer variables. A network is a product automaton. Its size is exponential in the number of components, which is the [state explosion problem](/state-explosion-problem/) again.

## What it counts

The model measures the cost of decision problems about $A$ in the size of its description: the number of locations, edges and clocks, and the constants written in binary. The main problems are:

- **Location reachability:** is some state $(\ell, v)$ reachable? This is also the emptiness of the language of finite timed words. Many [safety properties](/safety-property/) reduce to it with an observer automaton.
- **Büchi emptiness:** does a non-Zeno run visit accepting locations infinitely often?
- **Universality and inclusion:** does $A$ accept every timed word, or every word of $B$?
- **Model checking:** does $A$ satisfy a formula of a timed logic, such as TCTL or a metric temporal logic?
- **Optimization:** the least time or least cost to reach a location, in priced timed automata.

Time is a real number, and the answer does not change when all constants are scaled. Rational constants can be made integers this way. The cost comes from three sources: the number of clocks, the size of the constants (the number of regions grows with each constant), and the product of components.

## Relation to other models

- **Finite automata.** A timed automaton without clocks is a [nondeterministic finite automaton](/nondeterministic-finite-automaton/). The *untimed language*, the words of actions with the times dropped, of a timed automaton is regular. The [region graph](/region-graph/) recognizes it, with at most $|L| \cdot n! \, 2^n \prod_{x} (2 c_x + 2)$ states for $n$ clocks with largest constants $c_x$.
- **Region graph and zones.** Region equivalence is a finite time-abstract [bisimulation](/bisimulation/), which is why the model is decidable. Zones and [difference bound matrices](/difference-bound-matrix/) are the practical symbolic representation. Zone search with extrapolation is exact for diagonal-free automata (Bouyer 2004).
- **Discrete time.** If all constraints are non-strict, integer delays reach the same locations. This is the digitization result of Henzinger, Manna and Pnueli (1992). With strict constraints, integer time can miss behaviour: the guard $0 < x < 1$ never holds at an integer time after the last reset of $x$. Discrete time models are simpler to analyse, but in general they change the semantics.
- **Hybrid automata.** A clock is a variable with derivative 1. [Hybrid automata](/hybrid-automata/) allow other derivatives and general differential equations. Stopwatches, which are clocks that can be paused, are already enough to make reachability undecidable.
- **Counter machines.** With clock constraints that compare a clock with a sum of others, or with resets to other clocks' values plus constants, timed automata can encode the counters of a two-counter machine, so reachability becomes undecidable. Many such borders are known for "updatable" timed automata (Bouyer and others).
- **Timed Petri nets and probabilistic timed automata.** Time can also be added to Petri nets. Combining clocks with probabilities gives probabilistic timed automata, which tools analyse with regions or zones and the methods of [PCTL model checking](/pctl-model-checking/).

## Known results in the model

| Problem | Status | Source |
|---|---|---|
| Location reachability, emptiness | PSPACE-complete | Alur and Dill 1994 |
| Büchi emptiness of timed Büchi automata | PSPACE-complete | Alur and Dill 1994 |
| Reachability with a fixed small number of clocks | PSPACE-hard already with three clocks; NL-complete with one clock; PSPACE-complete with two clocks | Courcoubetis and Yannakakis 1992; Laroussinie, Markey and Schnoebelen 2004; Fearnley and Jurdziński 2013 |
| Universality, language inclusion | Undecidable | Alur and Dill 1994 |
| Complement | Not closed: some timed regular languages have complements that no timed automaton accepts | Alur and Dill 1994 |
| Inclusion $L(A) \subseteq L(B)$ with $B$ deterministic | Decidable, PSPACE-complete | Alur and Dill 1994 |
| TCTL model checking | PSPACE-complete | Alur, Courcoubetis and Dill 1993 |
| Zone search with $\mathrm{Extra}_M$ | Exact for diagonal-free automata; can be wrong with diagonal guards | Bouyer 2004 |

**Why reachability is in PSPACE.** The [region graph](/region-graph/) has exponentially many nodes, but a node is written in polynomial space. A nondeterministic search guesses a path one node at a time, so it needs only polynomial space. By [Savitch's theorem](/savitch-theorem/) a deterministic search also needs only polynomial space.

**Why it is PSPACE-hard.** Alur and Dill reduce the acceptance problem of linear-space Turing machines. The number of clocks grows with the length of the tape, and the clock values encode the tape contents. The constants needed are small, so the hardness comes from the number of clocks.

**Why universality is undecidable.** A timed word can encode the configurations of a Turing machine, one configuration per time unit. Its validity needs a check that each event is copied exactly one time unit later. A single nondeterministic timed automaton can guess an error in any copy. So it accepts all words that are not valid computations, and universality would decide halting. The same idea shows that complements need not be recognizable. The language of timed words with two events exactly one time unit apart is accepted by a timed automaton, but its complement is not.

## References
