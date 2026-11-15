---
tag: QSGJ5D
kind: definition
slug: controllable-language
name: Controllable language
aliases:
- controllability of languages
area: control/discrete-event-and-hybrid-systems
level: core
summary: A specification language is controllable if no uncontrollable event of the plant can lead a legal string out of its prefix closure. It is exactly the language a supervisor can enforce.
prereqs: [supervisory-control-theory]
see_also: [supremal-controllable-sublanguage, nonblocking-supervisor, observable-language, normal-language, controllability, control-invariant-set, reactive-synthesis, dynamic-controllability]
sources:
  - paper: doi:10.1137/0325013
    title: "P. J. Ramadge and W. M. Wonham, Supervisory control of a class of discrete event processes, SIAM Journal on Control and Optimization 25(1), 1987, pages 206 to 230"
    locator: the definition of controllability and the existence theorem for supervisors
  - paper: doi:10.1137/0325036
    title: "W. M. Wonham and P. J. Ramadge, On the supremal controllable sublanguage of a given language, SIAM Journal on Control and Optimization 25(3), 1987, pages 637 to 659"
    locator: closure under union and the supremal controllable sublanguage
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 3, Supervisory Control
  - book: isbn:9783319774510
    title: W. Murray Wonham and Kai Cai, Supervisory Control of Discrete-Event Systems, Springer, 2019
    locator: Chapter 3, Supervision of Discrete-Event Systems, Basics
---

A language $K$ is controllable with respect to a plant $G$ if no uncontrollable event that the plant can execute takes a prefix of $K$ outside the prefixes of $K$. This is the condition of [supervisory control theory](/supervisory-control-theory/): a supervisor that may only disable controllable events can make the closed-loop behavior equal to the prefixes of $K$ if and only if $K$ is controllable. The notion is about languages of a [discrete-event system](/discrete-event-system/). It is not the [controllability](/controllability/) of a linear state-space system (reaching every state with some input), and it is not the [dynamic controllability](/dynamic-controllability/) of temporal networks in AI planning.

## Definition

Let $G$ be a plant automaton over $\Sigma = \Sigma_c \cup \Sigma_{uc}$, with generated language $L(G)$; $\Sigma_{uc}$ is the set of uncontrollable events. For a language $K \subseteq \Sigma^*$, let $\overline{K}$ be its prefix closure, the set of all prefixes of strings of $K$.

> $K$ is **controllable** with respect to $L(G)$ and $\Sigma_{uc}$ if
> $$\overline{K}\,\Sigma_{uc} \cap L(G) \subseteq \overline{K}.$$

In words: for every $s \in \overline{K}$ and every $\sigma \in \Sigma_{uc}$, if $s\sigma \in L(G)$ then $s\sigma \in \overline{K}$. Strings that leave $L(G)$ do not count, because the plant cannot run them.

Facts that follow from the definition:

- Controllability depends only on $\overline{K}$. So $K$ is controllable if and only if $\overline{K}$ is.
- $\emptyset$ is controllable, and so is $L(G)$, and so is every $K$ with $\Sigma_{uc} = \emptyset$.
- **Closure under union.** If each $K_i$ is controllable, so is $\bigcup_i K_i$. Proof: $\overline{\bigcup_i K_i} = \bigcup_i \overline{K_i}$. If $s$ is in the left side and $s\sigma \in L(G)$ with $\sigma \in \Sigma_{uc}$, then $s \in \overline{K_i}$ for some $i$, so $s\sigma \in \overline{K_i}$. This gives the [supremal controllable sublanguage](/supremal-controllable-sublanguage/) $\sup C(E)$ of every language $E$: the union of all controllable sublanguages of $E$.
- **Intersection.** The intersection of two prefix-closed controllable languages is controllable. The intersection of two controllable languages that are not prefix-closed need not be, because $\overline{K_1 \cap K_2}$ can be smaller than $\overline{K_1} \cap \overline{K_2}$. An example is below.

**The controllability theorem** (Ramadge and Wonham 1987). Let $K \subseteq L(G)$ be nonempty. There is a supervisor $S$, which enables all uncontrollable events after every string, with $L(S/G) = \overline{K}$ if and only if $K$ is controllable. Such a supervisor is $S(s) = \Sigma_{uc} \cup \{\sigma \in \Sigma_c : s\sigma \in \overline{K}\}$. For the version with marked strings and no blocking, see [nonblocking supervisor](/nonblocking-supervisor/).

*Proof.* If $K$ is controllable, show $L(S/G) = \overline{K}$ by induction on the length of strings. $\varepsilon$ is in both. Let $s \in L(S/G) = \overline{K}$ at length $|s|$. If $\sigma \in \Sigma_c$, then $s\sigma \in L(S/G)$ if and only if $s\sigma \in L(G)$ and $s\sigma \in \overline{K}$, and $\overline{K} \subseteq L(G)$. If $\sigma \in \Sigma_{uc}$, then $s\sigma \in L(S/G)$ if and only if $s\sigma \in L(G)$, and by controllability this is the same as $s\sigma \in \overline{K}$. Conversely, if some $S$ gives $L(S/G) = \overline{K}$, take $s \in \overline{K}$ and $\sigma \in \Sigma_{uc}$ with $s\sigma \in L(G)$. $S$ enables $\sigma$ after $s$, so $s\sigma \in L(S/G) = \overline{K}$. $\blacksquare$

## Examples and non-examples

The plant is a machine with states idle $I$, working $W$ and down $D$, and with $I \xrightarrow{a} W$, $W \xrightarrow{b} I$, $W \xrightarrow{f} D$ and $D \xrightarrow{r} I$. The start $a$ and the repair $r$ are controllable, and the finish $b$ and the failure $f$ are not.

- **Not controllable: "the machine never fails".** Let $K$ be the set of strings of $L(G)$ without $f$. Then $a \in \overline{K}$, $f \in \Sigma_{uc}$ and $af \in L(G)$, but $af \notin \overline{K}$. The largest controllable sublanguage is $\{\varepsilon\}$: a supervisor can avoid failures only by never starting the machine. A brute force check over all strings of length at most 8 gives the same result.
- **Controllable: "start at most once".** $\overline{K} = \{\varepsilon, a, ab, af, afr\}$. After $\varepsilon$, $ab$ and $afr$ the machine is idle, and no uncontrollable event is possible. After $a$, both $b$ and $f$ lead into $\overline{K}$. After $af$ only $r$ is possible, and it is controllable. The supervisor disables $a$ after the first start.
- **Not controllable: a buffer that must not overflow.** Machine $M_1$ puts parts into a buffer with one slot by its uncontrollable finish $b_1$, and it starts by the controllable $a_1$. The specification forbids $b_1$ when the buffer is full. The string $a_1 b_1 a_1$ is legal (the buffer is full and $M_1$ works again), but then $b_1$ overflows the buffer. The fix is to disable $a_1$ one step earlier, when the buffer is full. The example on [supervisory control theory](/supervisory-control-theory/) works this out.
- **An intersection that is not controllable.** Let $L(G) = \overline{\{aub, auc\}}$ with $\Sigma_{uc} = \{u\}$, and let $K_1 = \{a, aub\}$ and $K_2 = \{a, auc\}$. Both are controllable, since $au$ is in both prefix closures. But $K_1 \cap K_2 = \{a\}$ has the prefix closure $\{\varepsilon, a\}$, and $au \in L(G)$ leaves it. So $\{a\}$ is not controllable.
- **Uncontrollable events outside $L(G)$ do not count.** If $\sigma \in \Sigma_{uc}$ but the plant never executes $\sigma$ after $s$, then $s\sigma \notin L(G)$ puts no condition on $K$.

## Related definitions

- **Supremal controllable sublanguage.** $\sup C(E)$ is the largest controllable sublanguage of $E$. For regular $E$ it is regular, and the [fixed point on the product automaton](/supremal-controllable-sublanguage/) computes it.
- **$L_m(G)$-closed.** $K \subseteq L_m(G)$ is $L_m(G)$-closed if $K = \overline{K} \cap L_m(G)$. Together with controllability it gives a [nonblocking supervisor](/nonblocking-supervisor/) with marked language $K$.
- **Observability and normality.** When some events are not observed, a supervisor also needs $K$ to be [observable](/observable-language/). [Normality](/normal-language/) is a stronger condition that is closed under union.
- **State-based form.** For a plant automaton and a set of states $Q$, the analog is a set that no uncontrollable transition leaves, and that the supervisor can keep the state in. This is the discrete form of a [control invariant set](/control-invariant-set/), and it is the safety part of a game in [reactive synthesis](/reactive-synthesis/).
- **Controllability of linear systems.** The [controllability](/controllability/) of $x' = A x + B u$ is a different notion with a similar name: it asks whether every state can be reached, not whether a specification can be enforced.

## References
