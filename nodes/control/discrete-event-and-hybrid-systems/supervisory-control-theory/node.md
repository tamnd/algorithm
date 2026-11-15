---
tag: GEW809
kind: concept
slug: supervisory-control-theory
name: Supervisory control theory
aliases:
- Ramadge-Wonham framework
- RW theory
area: control/discrete-event-and-hybrid-systems
level: core
summary: A theory in which a supervisor disables controllable events of a plant automaton so that the closed loop meets a language specification and stays nonblocking.
prereqs: [discrete-event-system, product-construction]
see_also: [controllable-language, supremal-controllable-sublanguage, nonblocking-supervisor, observable-language, reactive-synthesis, interface-synthesis, parity-game, supervision-based-on-place-invariants]
sources:
  - paper: doi:10.1137/0325013
    title: "P. J. Ramadge and W. M. Wonham, Supervisory control of a class of discrete event processes, SIAM Journal on Control and Optimization 25(1), 1987, pages 206 to 230"
    locator: the controllability condition and the existence of a supervisor for a given language
  - paper: doi:10.1137/0325036
    title: "W. M. Wonham and P. J. Ramadge, On the supremal controllable sublanguage of a given language, SIAM Journal on Control and Optimization 25(3), 1987, pages 637 to 659"
    locator: the supremal controllable sublanguage as the largest fixpoint of a monotone operator
  - paper: doi:10.1109/5.21072
    title: "P. J. G. Ramadge and W. M. Wonham, The control of discrete event systems, Proceedings of the IEEE 77(1), 1989, pages 81 to 98"
    locator: the survey of the framework
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 3, Supervisory Control
  - book: isbn:9783319774510
    title: W. Murray Wonham and Kai Cai, Supervisory Control of Discrete-Event Systems, Springer, 2019
    locator: Chapter 3, Supervision of Discrete-Event Systems, Basics
---

Supervisory control theory is a method to build a controller, called a supervisor, for a [discrete-event system](/discrete-event-system/): a plant modeled as an automaton whose transitions are events such as "start", "finish" or "fail". The supervisor watches the events and, after each one, decides which of the next events it allows. It can only block the controllable events. Events such as a failure or the end of a job are uncontrollable, and the supervisor must accept them. The goal is a closed loop whose strings of events stay inside a specification language, and that can always complete its task. Ramadge and Wonham introduced the theory in 1987, so it is also called the Ramadge-Wonham framework. It is close to [reactive synthesis](/reactive-synthesis/), which also builds a controller that plays against an environment. The differences are in the setting: here the plant is given as an automaton, the controller may only disable events and never forces one, the specification is a language (often regular) instead of a temporal logic formula, and the theory looks for the most permissive supervisor, the one that disables as little as possible.

## In plain words

Think of a plant as a board game where some moves are yours and some belong to nature. You may forbid any of your own moves at any time. You can never stop a move of nature. A rule book says which sequences of moves are acceptable. You want a policy for forbidding moves so that the game always stays within the rule book, and so that it can always reach a finished position. Among all such policies, you want the one that forbids the least.

Such a policy exists exactly when the rule book never asks you to stop a move of nature. If it does, you shrink the rule book until it no longer does. The largest shrunken rule book is unique, and a computer can find it.

## The idea

**Plant and supervisor.** The plant is an automaton $G$ over $\Sigma = \Sigma_c \cup \Sigma_{uc}$, with generated language $L(G)$ and marked language $L_m(G)$. A supervisor is a map $S : L(G) \to 2^{\Sigma}$ that gives, after each string $s$, the set of enabled events. It must always enable the uncontrollable events: $\Sigma_{uc} \subseteq S(s)$. The closed-loop language $L(S/G)$ is defined by induction: $\varepsilon \in L(S/G)$, and $s\sigma \in L(S/G)$ if and only if $s \in L(S/G)$, $s\sigma \in L(G)$ and $\sigma \in S(s)$. The marked closed-loop language is $L_m(S/G) = L(S/G) \cap L_m(G)$. $S/G$ is nonblocking if $\overline{L_m(S/G)} = L(S/G)$, where the bar is the prefix closure.

**Existence.** A language $K \subseteq L_m(G)$ is [controllable](/controllable-language/) if $\overline{K}\,\Sigma_{uc} \cap L(G) \subseteq \overline{K}$: no uncontrollable event leads a legal string out of the legal prefixes. The central theorem (Ramadge and Wonham 1987) says: for nonempty $K$, there is a supervisor with $L(S/G) = \overline{K}$ if and only if $K$ is controllable. With the marking condition, there is a [nonblocking supervisor](/nonblocking-supervisor/) with $L_m(S/G) = K$ if and only if $K$ is controllable and $L_m(G)$-closed ($K = \overline{K} \cap L_m(G)$). The supervisor is simple: $S(s) = \Sigma_{uc} \cup \{\sigma \in \Sigma_c : s\sigma \in \overline{K}\}$.

**When the specification is not controllable.** A union of controllable languages is controllable. So every specification $E$ has a largest controllable sublanguage $\sup C(E)$, the [supremal controllable sublanguage](/supremal-controllable-sublanguage/), and the supervisor for it is the least restrictive one that meets $E$. Wonham and Ramadge (1987) showed that it is the largest fixpoint of a monotone operator. For a regular $E$ given by an automaton $H$, the fixpoint is computed on the [product](/product-construction/) of $H$ and $G$, in time polynomial in the number of product states and events.

**Implementation.** In practice the supervisor is itself an automaton that runs in parallel with $G$ and shares its events. The trim automaton that the fixpoint returns is such a supervisor. In each of its states, the disabled events are the controllable events that $G$ allows but the supervisor does not.

**Extensions.** With unobservable events, the supervisor sees only the projection $P(s)$, and controllability is not enough: the language must also be [observable](/observable-language/). Observability is not closed under union, so there is no largest observable sublanguage in general. The stronger condition of [normality](/normal-language/) is closed under union. Other extensions are modular supervisors (one per specification), decentralized supervisors (several local agents), hierarchical control and supervisors of [Petri nets](/petri-net/), for example by [place invariants](/supervision-based-on-place-invariants/).

## Examples

**A machine that must not fail.** A machine goes from idle to working by the controllable event $a$, and back by the uncontrollable event $b$. From working it can also fail by the uncontrollable event $f$. The specification "never fail" is not controllable: after $a$, the event $f$ is possible and no supervisor can stop it. The supremal controllable sublanguage is $\{\varepsilon\}$, so the only safe supervisor never starts the machine. The page [discrete-event system](/discrete-event-system/) gives the full automaton.

**Two machines and a buffer.** Machine $M_1$ starts ($a_1$, controllable) and finishes ($b_1$, uncontrollable) and puts its part into a buffer with one slot. Machine $M_2$ starts ($a_2$, controllable) by taking the part from the buffer, and finishes ($b_2$, uncontrollable). The plant is the product of $M_1$ and $M_2$, with 4 states (each machine idle or working), and the state where both are idle is marked. The specification $H$ has two states, buffer empty and buffer full: $b_1$ goes from empty to full, $a_2$ from full to empty, and $b_1$ when full (overflow) and $a_2$ when empty (underflow) are not allowed. The product of $H$ and the plant has 8 reachable states and 12 transitions. The fixpoint removes the two states with a full buffer and $M_1$ working, because there the uncontrollable $b_1$ would overflow the buffer. What is left has 6 states and 8 transitions, and it is nonblocking. The supervisor does two things:

| state (buffer, $M_1$, $M_2$) | disabled event | reason |
|---|---|---|
| full, idle, idle | $a_1$ | $M_1$ would finish into a full buffer |
| full, idle, working | $a_1$ | the same |
| empty, idle, idle | $a_2$ | there is no part to take |
| empty, working, idle | $a_2$ | the same |

It never disables more than this, so it is the least restrictive supervisor. The implementation on [supremal controllable sublanguage](/supremal-controllable-sublanguage/) computes these numbers in its tests.

## Where it is used

- Manufacturing cells, automated guided vehicles, railway and traffic interlocking, and batch processes, where the plant is a set of machines and the specification forbids collisions, overflows and deadlocks.
- Communication protocols and software components. [Interface synthesis](/interface-synthesis/) in hardware design asks the same question for a controller that may only block some events.
- [Reactive synthesis](/reactive-synthesis/) and games on graphs, such as [parity games](/parity-game/), solve a more general problem for temporal logic specifications. A supervisory control problem with a safety and nonblocking specification is a game of this kind, with the uncontrollable events as the moves of the environment.
- Fault handling: a supervisor can be combined with a [diagnoser](/diagnoser-automaton/) that detects unobservable faults, and then switch to a recovery mode.
- Control of continuous plants through a finite abstraction, as in [symbolic control](/symbolic-control/).

## References
