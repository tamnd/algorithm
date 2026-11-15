---
tag: DD6K06
kind: definition
slug: dynamic-controllability
name: Dynamic controllability
aliases:
- dynamically controllable STNU
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: research
summary: An STNU is dynamically controllable if a strategy that decides each point from the durations seen so far meets every constraint in every situation. It lies between strong and weak controllability.
prereqs: [simple-temporal-network-with-uncertainty]
see_also: [morris-dynamic-controllability, simple-temporal-problem, temporal-planning]
sources:
  - paper: "Paul Morris, Nicola Muscettola and Thierry Vidal, Dynamic control of plans with temporal uncertainty, Proceedings of IJCAI-01, Morgan Kaufmann, 2001"
    locator: pages 494 to 502 in dblp (execution strategies, histories, the definition of a dynamic strategy and of dynamic controllability)
  - paper: doi:10.1080/095281399146607
    title: Thierry Vidal and Hélène Fargier, Handling contingency in temporal constraint networks, from consistency to controllabilities, Journal of Experimental and Theoretical Artificial Intelligence 11(1), 1999
    locator: pages 23 to 45 (strong, weak and dynamic controllability)
  - paper: doi:10.1109/TIME.2009.25
    title: Luke Hunsberger, Fixing the semantics for dynamic controllability and providing a more practical characterization of dynamic execution strategies, TIME 2009, IEEE, 2009
    locator: pages 155 to 162 (a corrected definition of dynamic execution strategies)
  - paper: doi:10.1007/11889205_28
    title: Paul Morris, A structural characterization of temporal dynamic controllability, CP 2006, Lecture Notes in Computer Science 4204, Springer, 2006
    locator: pages 375 to 389 (Theorem 1, dynamic controllability as the absence of semi-reducible negative cycles)
  - paper: "Paul Morris and Nicola Muscettola, Managing temporal uncertainty through waypoint controllability, Proceedings of IJCAI-99, Morgan Kaufmann, 1999"
    locator: pages 1253 to 1258 (waypoint controllability and its propagation algorithm)
---

Dynamic controllability is the property of a [simple temporal network with uncertainty](/simple-temporal-network-with-uncertainty/) that an agent can execute it safely while it watches the uncertain durations end: there is a strategy that fixes the time of each of the agent's points from the durations it has seen so far, and that meets every constraint whatever durations nature chooses. Vidal and Fargier (1999) and Morris, Muscettola and Vidal (2001) gave the definition. It is the controllability notion used in plan execution, and it can be checked in polynomial time, for example by [Morris's algorithm](/morris-dynamic-controllability/).

## Definition

Let an STNU have contingent links $A \Rightarrow C$ with bounds $[x_C, y_C]$. A *situation* $\omega$ gives each contingent link a duration $\omega_C \in [x_C, y_C]$, and the *projection* $P_\omega$ is the STP in which $t_C - t_A = \omega_C$. An *execution strategy* $S$ maps each situation $\omega$ to a schedule $S(\omega)$, a time for every point, in which each contingent point is at $t_A + \omega_C$. It is *viable* if $S(\omega)$ is a solution of $P_\omega$ for every $\omega$.

For a schedule $T$ and a time $t$, the *history* of $t$ in $T$ is the set of durations of the contingent links whose end point $C$ has $T(C) \le t$. A strategy is *dynamic* if for every two situations $\omega, \omega'$ and every point $X$ that the agent executes: if the history of $t = S(\omega)(X)$ in $S(\omega)$ equals the history of $t$ in $S(\omega')$, then $S(\omega')(X) = t$. In words, the time of $X$ may depend only on the durations that have ended by that time.

The STNU is *dynamically controllable* (DC) if it has a viable dynamic strategy.

This is the form used by Morris (2006), where the agent may react at the same instant as an observed end. Hunsberger (2009) showed that the earlier wording of the condition was not quite right and gave a corrected one in terms of real-time execution decisions; later papers also study a semantics in which a reaction must come strictly after the observation.

## Examples and non-examples

All four examples have one contingent link $A \Rightarrow C$ with bounds $[1, 3]$ and one agent point $B$; $\omega$ is the duration of the link.

**DC and strongly controllable.** With $3 \le t_B - t_A \le 5$ and $0 \le t_B - t_C \le 4$, the strategy $t_B = t_A + 3$ ignores $\omega$ and works for every $\omega$. A strategy that uses no observation is dynamic, so strong controllability implies DC.

**DC but not strongly controllable.** With $0 \le t_B - t_C \le 1$, the strategy "execute $B$ when $C$ happens" is dynamic, because the time of $B$ depends on $\omega$ only after $C$ has ended, and it is viable. No fixed offset $s = t_B - t_A$ works, since it would need $s \ge 3$ and $s \le 2$.

**DC with a wait.** With $-1 \le t_B - t_C \le 0$, $B$ must come at most one unit before $C$, or with it. The strategy "execute $B$ when $C$ happens, but not later than $t_A + 2$" works: if $\omega \le 2$, then $t_B = t_C$; else $t_B = t_A + 2$ and $t_B - t_C = 2 - \omega \in [-1, 0)$. The time of $B$ depends on whether $C$ has happened by $t_A + 2$, which the agent knows then. No fixed offset works, since it would need $s \ge 2$ for $\omega = 3$ and $s \le 1$ for $\omega = 1$.

**Weakly controllable but not DC.** With $t_C - t_B = 1$, every projection is consistent, with $t_B = t_A + \omega - 1$. A strategy with that schedule is viable but not dynamic: for $\omega = 1$ and $\omega' = 3$ the history at $t_B = t_A$ is empty in both, but the times of $B$ differ. Any dynamic strategy fixes $t_B$ before $C$ ends, so it gives $B$ the same time for both situations, and then one of them breaks the constraint. The network is weakly but not dynamically controllable.

**Non-example: a contingent link alone.** A single link $A \Rightarrow C$ with no requirements is DC; nature's choice never breaks a constraint. A propagation from $C$ that follows the upper-case edge of the same link, $C \to A$ with weight $-y$, finds a negative path at once and would wrongly reject it. This is one of the [pitfalls of the Morris check](/morris-dynamic-controllability/).

## Related definitions

- **Strong controllability.** One schedule of the agent's points works for every situation. It implies DC, and it is checked by one STP; see [simple temporal network with uncertainty](/simple-temporal-network-with-uncertainty/).
- **Weak controllability.** Every projection is consistent. DC implies it. It is the right notion only when the agent learns all durations before it acts.
- **Waypoint controllability.** Morris and Muscettola (1999) introduced waypoint controllability as a practical way to make sure that a network can be executed, before polynomial checks of DC were known.
- **Semi-reducible negative cycle.** Morris (2006, Theorem 1): an STNU is DC if and only if its labelled distance graph has no negative cycle that the reductions can turn into one without lower-case edges.
- **Dispatchability.** A DC network can be put into a form in which a simple real-time dispatcher, which propagates bounds to neighbours only, carries out a dynamic strategy; Morris (2014) relates the two notions.
- **Projection and the STP.** Each projection is a [simple temporal problem](/simple-temporal-problem/), and with no contingent links DC is STP consistency.

## References
