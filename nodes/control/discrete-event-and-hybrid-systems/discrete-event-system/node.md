---
tag: 2756H2
kind: model
slug: discrete-event-system
name: Discrete-event system
aliases:
- discrete event dynamic system
area: control/discrete-event-and-hybrid-systems
level: intro
summary: A system whose state is discrete and changes only when an event occurs. It is modeled by an automaton or a Petri net, and its behavior is a language of event strings.
prereqs: [deterministic-finite-automaton, regular-language]
see_also: [supervisory-control-theory, diagnosability, petri-net, timed-automata, hybrid-automata, timed-event-graph, markov-chain, product-construction]
sources:
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 2 (Languages and Automata), Chapter 4 (Petri Nets) and Chapter 5 (Timed and Hybrid Models)
  - book: isbn:9783319774510
    title: W. Murray Wonham and Kai Cai, Supervisory Control of Discrete-Event Systems, Springer, 2019
    locator: Chapter 3, Supervision of Discrete-Event Systems, Basics (generators and their languages)
  - paper: doi:10.1109/5.21072
    title: "P. J. G. Ramadge and W. M. Wonham, The control of discrete event systems, Proceedings of the IEEE 77(1), 1989, pages 81 to 98"
    locator: the model of a discrete event system as a generator of a language
---

A discrete-event system (DES) is a dynamical system whose state takes values in a discrete set and changes only when an event occurs. An event is an instant action such as "machine 1 starts", "a part arrives" or "a valve fails". Between two events nothing changes, and there is no clock in the basic model: only the order of the events counts. Manufacturing cells, communication protocols, traffic lights, elevators and fault-prone plants are modeled in this way. The standard model is an automaton that generates strings of events, so the theory uses the tools of [deterministic finite automata](/deterministic-finite-automaton/) and [regular languages](/regular-language/). It differs from a DFA in what it is for: the automaton is a model of a physical process to be controlled or diagnosed, not a recognizer of an input word. [Petri nets](/petri-net/) are a second standard model. Adding clocks gives [timed automata](/timed-automata/), and adding continuous dynamics gives [hybrid automata](/hybrid-automata/).

## The machine

A DES is a generator, an automaton

$$G = (X, \Sigma, \delta, x_0, X_m),$$

with a set of states $X$, a finite alphabet of events $\Sigma$, a partial transition function $\delta : X \times \Sigma \to X$, an initial state $x_0$ and a set of marked states $X_m \subseteq X$. The time axis is the event count: step $k$ is the $k$-th event, and its real time is not part of the model. Event $\sigma$ can occur in state $x$ only if $\delta(x, \sigma)$ is defined. Then the state becomes $\delta(x, \sigma)$. We extend $\delta$ to strings in the usual way.

The standing assumptions of this area are these. $X$ and $\Sigma$ are finite, unless a page says otherwise (a Petri net can have an infinite reachable state set). $G$ is deterministic: one event from one state leads to at most one state. Nondeterminism is modeled by unobservable events, as below. Events are not simultaneous: two events always occur in some order.

For control and diagnosis the alphabet is split in two ways:

- $\Sigma = \Sigma_c \cup \Sigma_{uc}$: a supervisor can prevent a controllable event in $\Sigma_c$, but not an uncontrollable event in $\Sigma_{uc}$, such as a failure or the end of a task.
- $\Sigma = \Sigma_o \cup \Sigma_{uo}$: a sensor records the observable events in $\Sigma_o$, and the unobservable events in $\Sigma_{uo}$ are not seen. The natural projection $P : \Sigma^* \to \Sigma_o^*$ erases the unobservable events of a string, so $P(s)$ is what an observer sees when $G$ runs $s$.

## What it counts

The model predicts which sequences of events can occur. Two languages describe it:

- the generated language $L(G) = \{s \in \Sigma^* : \delta(x_0, s) \text{ is defined}\}$, all the strings that the plant can run; it is prefix-closed;
- the marked language $L_m(G) = \{s \in L(G) : \delta(x_0, s) \in X_m\}$, the strings that end in a marked state, which usually means that a task is complete.

$\overline{K}$ is the prefix closure of a language $K$, the set of all prefixes of its strings. $G$ is nonblocking if $\overline{L_m(G)} = L(G)$: from each reachable state, some string leads to a marked state. A blocking state is a deadlock (no event is possible) or part of a livelock (events are possible, but none leads to a marked state). The questions of the theory are about these languages: can a supervisor restrict $L(G)$ to a given specification, can an observer find out from $P(s)$ that a fault occurred, and is the result nonblocking.

The size of a finite DES is its number of states $|X|$ and its number of events $|\Sigma|$. The algorithms of this area are analyzed in the [word RAM](/word-ram/) model with these numbers as the size, and a bound is often in the size of a product of two automata, built by the [product construction](/product-construction/).

**Example.** A machine has three states: idle $I$, working $W$ and down $D$. The events are $a$ (start), $b$ (finish), $f$ (fail) and $r$ (repair):

$$\delta(I, a) = W, \quad \delta(W, b) = I, \quad \delta(W, f) = D, \quad \delta(D, r) = I, \qquad x_0 = I, \quad X_m = \{I\}.$$

$a$ and $r$ are controllable, and $b$ and $f$ are not. The strings of $L(G)$ of length 0 to 8 number 1, 1, 2, 2, 3, 4, 5, 7 and 9, and those of $L_m(G)$ number 1, 0, 1, 1, 1, 2, 2, 3 and 4. For example $L(G)$ has the two strings $aba$ and $afr$ of length 3, and only $afr$ is marked. Every state can reach $I$, so $G$ is nonblocking. The specification "the machine never fails" is the set of strings without $f$. A supervisor cannot meet it, because after $a$ it cannot stop $f$. The largest part of it that a supervisor can enforce is $\{\varepsilon\}$: never start the machine. The page [controllable language](/controllable-language/) makes this exact.

## Relation to other models

- **Finite automata.** As a mathematical object, $G$ is a [DFA](/deterministic-finite-automaton/) with a partial transition function, and $L_m(G)$ is the language that the DFA accepts. The [Moore machine](/moore-machine/) is closer when states have outputs. With unobservable events, $G$ seen through $P$ acts as a [nondeterministic automaton](/nondeterministic-finite-automaton/) over $\Sigma_o$, and an observer of $G$ is its [subset construction](/subset-construction/).
- **Petri nets.** A [Petri net](/petri-net/) is a DES whose state is a marking (a vector of token counts). A bounded net has a finite reachability graph, which is an automaton as above. An unbounded net can have an infinite state set, and some of its languages are not regular. [Supervision based on place invariants](/supervision-based-on-place-invariants/) uses the net structure directly.
- **Timed models.** A [timed event graph](/timed-event-graph/) is a Petri net with delays, and it is linear in the [max-plus algebra](/max-plus-algebra/). [Timed automata](/timed-automata/) add clocks to the states and transitions.
- **Stochastic models.** A DES with event probabilities or random lifetimes is a [Markov chain](/markov-chain/) or a semi-Markov process. A [hidden Markov model](/hidden-markov-model/) is the stochastic form of a partially observed DES.
- **Hybrid models.** A [hybrid automaton](/hybrid-automata/) has a continuous state that follows a differential equation in each discrete state. A [switched system](/switched-system/) is the special case where the discrete state is an input or a free signal.
- **Games.** A supervisor plays against the uncontrollable events. [Reactive synthesis](/reactive-synthesis/) studies the same kind of game for temporal logic specifications, with the environment as the opponent.

## Known results in the model

- **Supervisory control.** A supervisor that disables controllable events can give exactly the closed-loop language $\overline{K}$ if and only if $K$ is [controllable](/controllable-language/) (Ramadge and Wonham 1987). The largest controllable sublanguage always exists, and for regular $K$ the [fixed point on the product automaton](/supremal-controllable-sublanguage/) computes it in time polynomial in the size of the product. The framework is on [supervisory control theory](/supervisory-control-theory/), and the nonblocking version on [nonblocking supervisor](/nonblocking-supervisor/).
- **Partial observation.** With unobservable events, the condition becomes controllability plus [observability](/observable-language/). Observability is not closed under union, so a largest observable sublanguage need not exist. [Normality](/normal-language/) is closed under union and gives a largest sublanguage (Lin and Wonham 1988).
- **Diagnosis.** A fault event that is unobservable can be detected within a bounded delay if and only if the system is [diagnosable](/diagnosability/). The [diagnoser](/diagnoser-automaton/) decides this and can be exponential in $|X|$. The [twin plant test](/twin-plant-diagnosability-test/) decides it in time polynomial in $|X|$.
- **Petri nets.** Reachability of a marking in a Petri net is decidable; see [Petri net reachability decidability](/petri-net-reachability-decidability/). For finite automata, reachability is a [graph search](/breadth-first-search/).
- **Abstraction.** [Symbolic control](/symbolic-control/) builds a finite DES that abstracts a continuous plant, and then uses the methods of this page on the abstraction.

## References
