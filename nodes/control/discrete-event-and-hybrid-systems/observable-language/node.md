---
tag: 8J25QZ
kind: definition
slug: observable-language
name: Observable language
aliases:
- observability of languages
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: A language is observable if strings that look the same through the observation mask never need different control actions, so a supervisor that sees only the mask can enforce it.
prereqs: [controllable-language]
see_also: [normal-language, supervisory-control-theory, controllable-language, diagnosability, observability, state-estimation, subset-construction]
sources:
  - paper: doi:10.1016/0020-0255(88)90001-1
    title: "F. Lin and W. M. Wonham, On observability of discrete-event systems, Information Sciences 44(3), 1988, pages 173 to 198"
    locator: the definition of observability and the existence theorem for supervisors under partial observation
  - paper: doi:10.1109/9.402
    title: "R. Cieslak, C. Desclaux, A. S. Fawaz and P. Varaiya, Supervisory control of discrete-event processes with partial observations, IEEE Transactions on Automatic Control 33(3), 1988, pages 249 to 260"
    locator: the existence condition for supervisors that see only observable events
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 3, Supervisory Control (control under partial observation)
---

In [supervisory control](/supervisory-control-theory/) with partial observation, the supervisor does not see every event of the plant. It sees only the projection $P(s)$ of the string $s$, so it must give the same control action to all strings with the same projection. A language $K$ is observable if this never causes a conflict: when two legal strings look the same and a controllable event must stay enabled after one of them, that event is also legal after the other one whenever the plant can execute it. Together with [controllability](/controllable-language/), observability is the exact condition for a supervisor that sees only the projection to enforce $K$. Lin and Wonham, and Cieslak, Desclaux, Fawaz and Varaiya, gave it in 1988. It is not the [observability](/observability/) of a linear state-space system, which asks whether the outputs determine the state.

## Definition

Let $G$ be a plant over $\Sigma = \Sigma_c \cup \Sigma_{uc}$ with generated language $L(G)$. Split $\Sigma$ also into observable events $\Sigma_o$ and unobservable events $\Sigma_{uo}$. The natural projection $P : \Sigma^* \to \Sigma_o^*$ erases the unobservable events: $P(\varepsilon) = \varepsilon$, $P(s\sigma) = P(s)\sigma$ if $\sigma \in \Sigma_o$, and $P(s\sigma) = P(s)$ otherwise. Let $\overline{K}$ be the prefix closure of $K$.

> $K \subseteq L(G)$ is **observable** with respect to $L(G)$, $P$ and $\Sigma_c$ if for all $s, s' \in \overline{K}$ with $P(s) = P(s')$ and all $\sigma \in \Sigma_c$:
> $$s\sigma \in \overline{K} \text{ and } s'\sigma \in L(G) \implies s'\sigma \in \overline{K}.$$

This is the form in Cassandras and Lafortune. Lin and Wonham ask the same condition for all $\sigma \in \Sigma$, and add a condition on marked strings for languages that are not prefix-closed. For a controllable $K$ the condition with $\sigma \in \Sigma_{uc}$ holds already, so the two forms agree on $\overline{K}$.

A **$P$-supervisor** is a map $S_P : P(L(G)) \to 2^{\Sigma}$ with $\Sigma_{uc} \subseteq S_P(t)$. It acts on $G$ by $S(s) = S_P(P(s))$.

**Theorem** (Lin and Wonham 1988; Cieslak et al. 1988). Let $K \subseteq L(G)$ be nonempty. There is a $P$-supervisor with $L(S/G) = \overline{K}$ if and only if $K$ is controllable and observable. Such a supervisor is

$$S_P(t) = \Sigma_{uc} \cup \{\sigma \in \Sigma_c : s'\sigma \in \overline{K} \text{ for some } s' \in \overline{K} \text{ with } P(s') = t\}.$$

*Proof.* Let $K$ be controllable and observable. Show by induction on length that $s \in L(S/G)$ if and only if $s \in \overline{K}$. Both contain $\varepsilon$. Let $s \in L(S/G) = \overline{K}$ and $s\sigma \in L(G)$. If $\sigma \in \Sigma_{uc}$, then $s\sigma \in L(S/G)$, and $s\sigma \in \overline{K}$ by controllability. If $\sigma \in \Sigma_c$ and $s\sigma \in \overline{K}$, take $s' = s$ to see that $\sigma \in S_P(P(s))$. If $\sigma \in \Sigma_c$ and $\sigma \in S_P(P(s))$, there is $s' \in \overline{K}$ with $P(s') = P(s)$ and $s'\sigma \in \overline{K}$. Observability with the roles of $s$ and $s'$ exchanged gives $s\sigma \in \overline{K}$. Conversely, let a $P$-supervisor give $L(S/G) = \overline{K}$. Controllability follows as in the full observation case. For observability, let $s, s' \in \overline{K}$ with $P(s) = P(s')$, $\sigma \in \Sigma_c$, $s\sigma \in \overline{K}$ and $s'\sigma \in L(G)$. Then $\sigma \in S_P(P(s)) = S_P(P(s'))$, so $s'\sigma \in L(S/G) = \overline{K}$. $\blacksquare$

For marked languages, a nonblocking $P$-supervisor with $L_m(S/G) = K$ exists if and only if $K$ is controllable, observable and $L_m(G)$-closed, with the marking form of observability. See [nonblocking supervisor](/nonblocking-supervisor/) for the full observation case.

## Examples and non-examples

Let $\Sigma = \{a, u\}$ with $a$ observable and $u$ unobservable, and let both events be controllable. The plant generates $L(G) = \{\varepsilon, a, u, ua\}$. So $P(u) = \varepsilon$ and $P(ua) = a$. All languages below are prefix-closed and controllable, because $\Sigma_{uc}$ is empty.

| $K$ | observable | reason |
|---|---|---|
| $\{\varepsilon, a, u\}$ | no | $s = \varepsilon$ and $s' = u$ look the same; $a \in K$ and $ua \in L(G)$, but $ua \notin K$ |
| $\{\varepsilon, a\}$ | yes | no two strings of $K$ have the same projection |
| $\{\varepsilon, u\}$ | yes | $\varepsilon$ and $u$ look the same, but $a \notin K$, and $uu \notin L(G)$ |
| $\{\varepsilon\}$ | yes | only one string |

- **Not observable.** For $K = \{\varepsilon, a, u\}$, the supervisor must enable $a$ at the start and disable it after $u$. But it does not see $u$, so both strings give it the observation $\varepsilon$. No $P$-supervisor gives exactly $K$.
- **No largest observable sublanguage.** $\{\varepsilon, a\}$ and $\{\varepsilon, u\}$ are both observable, and each is maximal among the observable sublanguages of $K$. Their union is $K$, which is not observable. So observability is not closed under union, and $K$ has no supremal observable sublanguage. A designer must pick one of the maximal ones. This is the reason to use the stronger [normal language](/normal-language/), which is closed under union: here the largest normal sublanguage is $\{\varepsilon, u\}$.
- **Full observation.** If $\Sigma_o = \Sigma$, then $P$ is the identity, $P(s) = P(s')$ means $s = s'$, and every language is observable.
- **All events controllable but unobservable.** If $\Sigma_o = \emptyset$, every two strings look the same. Then $K$ is observable if and only if every controllable event that is legal after some string of $\overline{K}$ is legal after every string of $\overline{K}$ where the plant can execute it.

## Related definitions

- **Closure properties.** The intersection of two prefix-closed observable languages is observable: the condition for each language implies it for the intersection. So a smallest prefix-closed observable superlanguage of a given language exists. The union is not closed, as the example shows.
- **Normal language.** $K$ is [normal](/normal-language/) if $\overline{K} = P^{-1}(P(\overline{K})) \cap L(G)$. Normality implies observability. If $\Sigma_c \subseteq \Sigma_o$, a prefix-closed language that is controllable and observable is also normal.
- **Checking observability.** For regular $K$ and $G$, the condition is about pairs of strings with the same projection. A product of the automaton of $K$ with a copy of itself, which moves together on observable events and alone on unobservable ones, finds a violating pair in polynomial time. This is the same idea as the [twin plant](/twin-plant-diagnosability-test/) for diagnosability.
- **Diagnosability.** [Diagnosability](/diagnosability/) is the analogous question for fault detection: do two strings with the same projection, one with a fault and one without, stay apart for long.
- **State estimation.** A $P$-supervisor in practice keeps the set of plant states that agree with the observation so far, as in the [subset construction](/subset-construction/). This is the discrete form of [state estimation](/state-estimation/).
- **Coobservability.** With several local supervisors, each with its own projection, the analogous condition is called coobservability.
- **Observability of linear systems.** The [observability](/observability/) of $x' = Ax$, $y = Cx$ asks whether the output determines the state. It is a different notion with a similar name.

## References
