---
tag: M2GT7G
kind: problem
slug: simple-temporal-network-with-uncertainty
name: Simple temporal network with uncertainty
aliases:
- STNU
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: research
summary: An STP in which some durations are chosen by nature within known bounds. The questions are strong, weak and dynamic controllability; strong and dynamic are polynomial.
prereqs: [simple-temporal-problem]
see_also: [dynamic-controllability, morris-dynamic-controllability, temporal-constraint-satisfaction-problem, disjunctive-temporal-problem, temporal-planning, bellman-ford]
sources:
  - paper: doi:10.1080/095281399146607
    title: Thierry Vidal and Hélène Fargier, Handling contingency in temporal constraint networks, from consistency to controllabilities, Journal of Experimental and Theoretical Artificial Intelligence 11(1), 1999
    locator: pages 23 to 45 (contingent and requirement links, projections, strong, weak and dynamic controllability, and the reduction of strong controllability to an STP)
  - paper: "Paul Morris, Nicola Muscettola and Thierry Vidal, Dynamic control of plans with temporal uncertainty, Proceedings of IJCAI-01, Morgan Kaufmann, 2001"
    locator: pages 494 to 502 in dblp (the first check of dynamic controllability, pseudo-polynomial)
  - paper: "Paul Morris and Nicola Muscettola, Temporal dynamic controllability revisited, Proceedings of AAAI-05, AAAI Press, 2005"
    locator: pages 1193 to 1198 (the labelled distance graph and an O(N^5) check)
  - paper: doi:10.4230/LIPIcs.TIME.2018.8
    title: Massimo Cairo, Luke Hunsberger and Romeo Rizzi, Faster dynamic controllability checking for simple temporal networks with uncertainty, TIME 2018, LIPIcs 120, 2018
    locator: pages 8:1 to 8:16 (the RUL- algorithm, in O(mn + k^2 n + kn log n) time)
  - paper: doi:10.1007/11889205_28
    title: Paul Morris, A structural characterization of temporal dynamic controllability, CP 2006, Lecture Notes in Computer Science 4204, Springer, 2006
    locator: pages 375 to 389 (the labelled distance graph, semi-reducible negative cycles and an O(N^4) check)
  - paper: doi:10.1007/978-3-319-07046-9_33
    title: Paul Morris, Dynamic controllability and dispatchability relationships, CPAIOR 2014, Lecture Notes in Computer Science 8451, Springer, 2014
    locator: pages 464 to 479 (an O(N^3) check of dynamic controllability)
  - paper: doi:10.1109/TIME.2009.25
    title: Luke Hunsberger, Fixing the semantics for dynamic controllability and providing a more practical characterization of dynamic execution strategies, TIME 2009, IEEE, 2009
    locator: pages 155 to 162 (execution strategies and the precise definition of dynamic controllability)
---

A simple temporal network with uncertainty (STNU) is a [simple temporal problem](/simple-temporal-problem/) in which some durations are not chosen by the agent: for a *contingent link* the agent starts an activity and nature ends it at some time within known bounds. The agent must then schedule its own time points so that every constraint holds for all the choices of nature. Vidal and Fargier (1999) defined three versions of this question: strong, weak and [dynamic controllability](/dynamic-controllability/), which differ in what the agent knows when it decides. Strong and dynamic controllability can be checked in polynomial time.

## In plain words

You plan a day with a delivery truck. You decide when the truck leaves. The road decides when it arrives, somewhere between one and three hours later. Other rules say, for example, that you must unload within an hour of the arrival.

Is the plan safe? It depends on what you know when you act. If you must fix every time in the morning, the plan must work for every arrival time with the same times. If you may wait and watch, you can react to the arrival. If you knew the arrival in advance, you could fit the plan to it. These are three different questions, and a plan can pass one and fail another.

## Definition

An STNU has time points $0, \ldots, n-1$, *requirement links* $lo \le t_v - t_u \le hi$ as in an STP, and $K$ *contingent links* $A \Rightarrow C$ with bounds $0 \le x \le y$. The agent executes the activation point $A$ and every other point that is not the end of a contingent link. Nature chooses the duration $\omega_C = t_C - t_A \in [x, y]$. The contingent points $C$ are distinct.

A *situation* $\omega$ is a choice of one duration for each contingent link. The *projection* of the STNU on $\omega$ is the STP in which each contingent link becomes the requirement $t_C - t_A = \omega_C$. A *schedule* gives a time to every point. Then:

- the STNU is *strongly controllable* (SC) if one assignment of the agent's points works for every situation;
- it is *weakly controllable* (WC) if every projection is consistent, so that an agent that knew $\omega$ in advance could choose its times;
- it is *dynamically controllable* (DC) if a strategy exists that decides each agent point from the durations that have ended so far; see [dynamic controllability](/dynamic-controllability/).

SC implies DC and DC implies WC, and both implications are strict.

## Variants

- **STP.** With $K = 0$ all three questions are the consistency of an STP.
- **Probabilistic STNs.** The durations have distributions in place of bounds, and the question is the probability that a strategy succeeds.
- **Conditional STNUs.** Observations at some points decide which parts of the network must hold, as in plans with branches.
- **Disjunctive constraints with uncertainty.** Requirement links may be disjunctions, as in a [DTP](/disjunctive-temporal-problem/) or a [TCSP](/temporal-constraint-satisfaction-problem/), which makes the problems harder.
- **Semantics of reaction.** Hunsberger (2009) fixed the precise meaning of dynamic strategies. Some later work requires that a reaction come strictly after the observation; the two semantics give different answers on some networks.

## Examples

Each example has one contingent link $A \Rightarrow C$ with bounds $[1, 3]$ and one agent point $B$.

**SC.** Let $3 \le t_B - t_A \le 5$ and $0 \le t_B - t_C \le 4$. The fixed choice $t_B = t_A + 3$ gives $t_B - t_C = 3 - \omega_C \in [0, 2]$ for every duration, so the network is strongly controllable, and so also DC and WC.

**DC but not SC.** Let $0 \le t_B - t_C \le 1$. A fixed offset $s = t_B - t_A$ needs $0 \le s - \omega_C \le 1$ for all $\omega_C \in [1, 3]$, that is $s \ge 3$ and $s \le 2$, so the network is not SC. But the agent can wait until $C$ happens and then execute $B$ at once, so it is DC.

**WC but not DC.** Let $t_C - t_B = 1$, so $B$ comes one unit before $C$. For each duration the schedule $t_B = t_C - 1$ works, so every projection is consistent and the network is WC. But $B$ happens before $C$, so the agent must fix $t_B$ before it sees $\omega_C$, and no single value works for both $\omega_C = 1$ and $\omega_C = 3$. The network is not DC. The [Morris algorithm](/morris-dynamic-controllability/) page traces its check on this network.

## Known algorithms

| question | method | worst-case time | notes |
| --- | --- | --- | --- |
| SC | rewrite to an STP (Vidal and Fargier, 1999), then [Bellman-Ford](/bellman-ford/) or [Floyd-Warshall](/floyd-warshall/) | $O(N^3)$ | see Reductions |
| WC | test the $2^K$ projections with extreme durations | $O(2^K N^3)$ | correct by the convexity argument in Bounds |
| DC | Morris, Muscettola and Vidal (2001) | pseudo-polynomial | reductions with waits |
| DC | Morris and Muscettola (2005) | $O(N^5)$ | the first strongly polynomial check |
| DC | [Morris (2006)](/morris-dynamic-controllability/) | $O(N^4)$ | $K$ rounds of propagation from the lower-case edges |
| DC | Morris (2014) | $O(N^3)$ | one negative node at a time |
| DC | RUL- (Cairo, Hunsberger and Rizzi, 2018) | $O(mn + k^2 n + kn \log n)$ | $m$ edges and $k$ contingent links |

Here $N$ is the number of time points, after any normal form that the method uses.

## Bounds

**Strong controllability (word-RAM).** SC is decided in $O(N^3)$ time, since it is the consistency of one STP on the same points (Vidal and Fargier, 1999).

**Weak controllability.** Fix the agent's points as variables. For a situation $\omega$, the projection is consistent if and only if every cycle of its distance graph has non-negative weight. The weight of each cycle is an affine function of $\omega$, so the set of situations with a consistent projection is an intersection of half-spaces, which is convex. The box $\prod [x_C, y_C]$ is the convex hull of its $2^K$ corners, so the network is WC if and only if the projections at the corners are consistent. A corner with a negative cycle is a short certificate that the network is not WC, so WC is in co-NP (Turing model). The sources cited here give no polynomial algorithm for it.

**Dynamic controllability (word-RAM).** DC is decided in $O(N^3)$ time (Morris, 2014). The bound does not depend on the size of the numbers in the bounds.

## Reductions

- **SC to an STP.** Replace each requirement that touches a contingent point by one on its activation point. For $lo \le t_v - t_C \le hi$ with $C$ the end of $A \Rightarrow C$ in $[x, y]$, the requirement $lo \le t_v - t_A - \omega \le hi$ must hold for all $\omega \in [x, y]$, which is $lo + y \le t_v - t_A \le hi + x$. A requirement between two contingent points is treated in the same way on both ends. The network is SC if and only if the resulting STP on the agent's points is consistent.
- **DC to negative cycles.** By Morris (2006), an STNU is DC if and only if its labelled distance graph has no semi-reducible negative cycle; the algorithms above find such cycles with shortest paths.
- **From the STP.** An STP is an STNU with no contingent links, and every question is STP consistency.

## Applications

- [Temporal planning](/temporal-planning/) and plan execution for spacecraft and robots, where the duration of a move or an observation depends on the environment.
- Workflow and business process systems with tasks whose durations are set by outside parties.
- Multi-agent scheduling, where the actions of other agents are treated as contingent.

## References
