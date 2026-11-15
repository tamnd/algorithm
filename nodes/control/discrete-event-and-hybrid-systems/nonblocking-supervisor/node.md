---
tag: CG0Q66
kind: definition
slug: nonblocking-supervisor
name: Nonblocking supervisor
aliases:
- nonblocking supervisory control
area: control/discrete-event-and-hybrid-systems
level: core
summary: A supervisor under which every string the closed loop can produce can be extended to a marked string, so the controlled plant has no deadlock and no livelock.
prereqs: [controllable-language]
see_also: [supervisory-control-theory, supremal-controllable-sublanguage, discrete-event-system, reactive-synthesis, cycle-detection, strongly-connected-components]
sources:
  - paper: doi:10.1137/0325013
    title: "P. J. Ramadge and W. M. Wonham, Supervisory control of a class of discrete event processes, SIAM Journal on Control and Optimization 25(1), 1987, pages 206 to 230"
    locator: nonblocking supervisors and the conditions for their existence
  - paper: doi:10.1109/5.21072
    title: "P. J. G. Ramadge and W. M. Wonham, The control of discrete event systems, Proceedings of the IEEE 77(1), 1989, pages 81 to 98"
    locator: the survey of the framework (marked languages and blocking)
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 3, Supervisory Control (the nonblocking controllability theorem and marking supervisors)
  - book: isbn:9783319774510
    title: W. Murray Wonham and Kai Cai, Supervisory Control of Discrete-Event Systems, Springer, 2019
    locator: Chapter 3, Supervision of Discrete-Event Systems, Basics
---

A supervisor of a [discrete-event system](/discrete-event-system/) is nonblocking if, under its control, the plant can always still complete a task: every string of events that the closed loop can produce extends to a marked string. A blocking closed loop can reach a deadlock, where no event is possible, or a livelock, where events go on forever but no task ever completes. Nonblocking is the liveness half of [supervisory control](/supervisory-control-theory/); the [controllability](/controllable-language/) of the specification is the safety half. The [supremal controllable sublanguage](/supremal-controllable-sublanguage/) gives the least restrictive supervisor that has both.

## Definition

Let $G$ be a plant with generated language $L(G)$, marked language $L_m(G)$ and uncontrollable events $\Sigma_{uc}$. A supervisor $S$ maps each string $s \in L(G)$ to a set $S(s)$ of enabled events with $\Sigma_{uc} \subseteq S(s)$. The closed-loop language $L(S/G)$ is the smallest set with $\varepsilon \in L(S/G)$ and $s\sigma \in L(S/G)$ whenever $s \in L(S/G)$, $s\sigma \in L(G)$ and $\sigma \in S(s)$. The marked closed-loop language is

$$L_m(S/G) = L(S/G) \cap L_m(G).$$

> $S$ is **nonblocking** for $G$ if $\overline{L_m(S/G)} = L(S/G)$,

where the bar is the prefix closure. The inclusion $\subseteq$ always holds, so the condition says: every $s \in L(S/G)$ has an extension $t$ with $st \in L_m(S/G)$.

A **marking supervisor** also decides which strings count as complete: it is a pair $(S, K)$ with $L_m(S/G) = L(S/G) \cap K$ for a language $K \subseteq L_m(G)$. Nonblocking is defined in the same way.

**The nonblocking controllability theorem.** Let $K \subseteq L_m(G)$ be nonempty.

1. There is a nonblocking supervisor $S$ with $L_m(S/G) = K$ and $L(S/G) = \overline{K}$ if and only if $K$ is controllable and $L_m(G)$-closed, that is, $K = \overline{K} \cap L_m(G)$.
2. There is a nonblocking marking supervisor with $L_m(S/G) = K$ if and only if $K$ is controllable.

*Proof of 1.* If $K$ is controllable, the supervisor $S(s) = \Sigma_{uc} \cup \{\sigma \in \Sigma_c : s\sigma \in \overline{K}\}$ gives $L(S/G) = \overline{K}$ (this is the controllability theorem on [controllable language](/controllable-language/)). Then $L_m(S/G) = \overline{K} \cap L_m(G) = K$ by closedness, and $\overline{L_m(S/G)} = \overline{K} = L(S/G)$, so $S$ is nonblocking. Conversely, if $S$ is nonblocking and $L_m(S/G) = K$, then $L(S/G) = \overline{K}$, so $K$ is controllable by the same theorem, and $K = L(S/G) \cap L_m(G) = \overline{K} \cap L_m(G)$. *Proof of 2.* Use the same $S$ with the marking $K$: then $L_m(S/G) = \overline{K} \cap K = K$. The converse is as in part 1. $\blacksquare$

If $K$ is not controllable, replace it by $\sup C(K)$. If $K$ is $L_m(G)$-closed, so is $\sup C(K)$: the language $K' = \overline{\sup C(K)} \cap L_m(G)$ lies in $K$, has the same prefix closure as $\sup C(K)$, so it is controllable, and therefore $K' \subseteq \sup C(K)$.

In automaton terms, a supervisor realized by an automaton $R$ that runs in parallel with $G$ is nonblocking if and only if the reachable part of the product $R \times G$ is coaccessible: from every reachable product state some marked product state can be reached. This is a backward [graph search](/breadth-first-search/) in time linear in the size of the product.

## Examples and non-examples

- **Nonblocking: the least restrictive supervisor.** In the buffer example of [supervisory control theory](/supervisory-control-theory/), the supervisor from the fixed point has 6 states, and each of them can reach the state where both machines are idle and the buffer is empty. So it is nonblocking.
- **Blocking: a supervisor that only enforces safety.** Take the plant with $0 \xrightarrow{a} 1 \xrightarrow{u} 2 \xrightarrow{b} 3 \xrightarrow{v} 4 \xrightarrow{d} 0$, $0 \xrightarrow{e} 0$ and $1 \xrightarrow{c} 0$, the marked state 0, uncontrollable $u$ and $v$, and the rule "$v$ never occurs". A supervisor that disables $b$ in state 2 keeps $v$ from occurring. But after $au$ the plant sits in state 2, where every possible event is disabled: a deadlock, and state 2 is not marked. The nonblocking supervisor for this rule disables $a$ in state 0 instead, and the closed loop is $e^*$. The page [supremal controllable sublanguage](/supremal-controllable-sublanguage/) computes this.
- **Blocking by livelock.** Let $0 \xrightarrow{a} 1$, $1 \xrightarrow{d} 1$ and $1 \xrightarrow{c} 0$ with state 0 marked. A supervisor that disables $c$ in state 1 lets the plant run $d d d \cdots$ forever, and it never returns to a marked state. The closed loop has events, so it is not a deadlock, but it is blocking.
- **Nonblocking, but with the wrong marked language.** Let $0 \xrightarrow{a} 1 \xrightarrow{a} 2$ with $L_m(G) = \{a, aa\}$, and $K = \{aa\}$. $K$ is controllable, but $\overline{K} \cap L_m(G) = \{a, aa\} \neq K$, so it is not $L_m(G)$-closed. A supervisor that enables both $a$ events gives $L_m(S/G) = \{a, aa\}$. Only a marking supervisor gives exactly $K$.
- **Two nonblocking supervisors that block together.** Two supervisors can each be nonblocking for $G$ and still block when they run at the same time. Their marked languages $K_1$ and $K_2$ are then conflicting: $\overline{K_1 \cap K_2} \neq \overline{K_1} \cap \overline{K_2}$. Modular control must check this.

## Related definitions

- **Nonblocking automaton.** An automaton $G$ is nonblocking if $\overline{L_m(G)} = L(G)$, that is, its reachable part is coaccessible. A trim automaton is nonblocking. See [discrete-event system](/discrete-event-system/).
- **Deadlock and livelock.** A deadlock state has no possible event and is not marked. A livelock is a set of states closed under the possible events, with no marked state. A livelock is a terminal [strongly connected component](/strongly-connected-components/) without a marked state, or a set of such components.
- **Controllable language.** The safety condition; see [controllable language](/controllable-language/).
- **$L_m(G)$-closed.** $K = \overline{K} \cap L_m(G)$: every marked plant string inside the legal prefixes is itself legal.
- **Nonconflicting languages.** $K_1$ and $K_2$ are nonconflicting if $\overline{K_1 \cap K_2} = \overline{K_1} \cap \overline{K_2}$. This is the condition for modular supervisors to be nonblocking together.
- **Liveness in games.** In [reactive synthesis](/reactive-synthesis/), the analog is a reachability or Büchi objective. Nonblocking is weaker than "a marked state is reached": it asks only that one stays reachable.

## References
