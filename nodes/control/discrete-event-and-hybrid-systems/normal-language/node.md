---
tag: DXX7YB
kind: definition
slug: normal-language
name: Normal language
aliases:
- normality of languages
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: A language is normal if every plant string that looks like one of its strings through the projection is also in it. Normality implies observability and is closed under union.
prereqs: [observable-language]
see_also: [observable-language, controllable-language, supremal-controllable-sublanguage, supervisory-control-theory, subset-construction, diagnosability]
sources:
  - paper: doi:10.1016/0020-0255(88)90001-1
    title: "F. Lin and W. M. Wonham, On observability of discrete-event systems, Information Sciences 44(3), 1988, pages 173 to 198"
    locator: the definition of normality, its relation to observability and closure under union
  - paper: doi:10.1016/0167-6911(90)90004-e
    title: "R. D. Brandt, V. Garg, R. Kumar, F. Lin, S. I. Marcus and W. M. Wonham, Formulas for calculating supremal controllable and normal sublanguages, Systems and Control Letters 15(2), 1990, pages 111 to 117"
    locator: the closed formulas for the supremal normal and the supremal controllable normal sublanguage
  - book: isbn:9783030722722
    title: Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems, third edition, Springer, 2021
    locator: Chapter 3, Supervisory Control (control under partial observation)
---

A language $K$ is normal with respect to a plant when the projection of a string alone tells whether the string is in $K$: every plant string that has the same projection as some string of $K$ is itself in $K$. In [supervisory control](/supervisory-control-theory/) with partial observation, a normal specification is easy to enforce, because the supervisor never has to tell apart two strings that look the same. Normality is stronger than [observability](/observable-language/), but unlike observability it is closed under union, so every language has a largest normal sublanguage. Lin and Wonham introduced it in 1988.

## Definition

Let $G$ be a plant over $\Sigma$ with generated language $L(G)$, let $\Sigma_o \subseteq \Sigma$ be the observable events, and let $P : \Sigma^* \to \Sigma_o^*$ be the natural projection that erases the unobservable events. For $T \subseteq \Sigma_o^*$, the inverse projection is $P^{-1}(T) = \{s \in \Sigma^* : P(s) \in T\}$.

> A language $K \subseteq M$ is **normal** with respect to $M$ and $P$ if
> $$K = P^{-1}(P(K)) \cap M.$$

The inclusion $\subseteq$ always holds, so the condition says: if $s \in M$ and $P(s) = P(s')$ for some $s' \in K$, then $s \in K$. In supervisory control the usual case is a prefix-closed specification with $M = L(G)$: $\overline{K}$ is normal if $\overline{K} = P^{-1}(P(\overline{K})) \cap L(G)$.

**Normal implies observable.** Let $\overline{K}$ be normal with respect to $L(G)$. Take $s, s' \in \overline{K}$ with $P(s) = P(s')$ and an event $\sigma$ with $s\sigma \in \overline{K}$ and $s'\sigma \in L(G)$. Then $P(s'\sigma) = P(s\sigma)$, so $s'\sigma \in P^{-1}(P(\overline{K})) \cap L(G) = \overline{K}$. This holds for every $\sigma$, controllable or not.

**The converse when all controllable events are observable.** Let $\Sigma_c \subseteq \Sigma_o$ and let $\overline{K} \subseteq L(G)$ be controllable and observable. Then $\overline{K}$ is normal.

*Proof.* Show by induction on $|s|$: if $s \in L(G)$, $s'' \in \overline{K}$ and $P(s) = P(s'')$, then $s \in \overline{K}$. For $s = \varepsilon$ this holds since $\overline{K}$ is nonempty. Let $s = t\sigma$. If $\sigma$ is unobservable, then $P(t) = P(s'')$, so $t \in \overline{K}$ by induction. Also $\sigma \in \Sigma_{uc}$, because $\Sigma_c \subseteq \Sigma_o$, so controllability gives $t\sigma \in \overline{K}$. If $\sigma$ is observable, write $s'' = s_1 \sigma s_2$ with $P(s_1) = P(t)$ and $s_2$ unobservable. Then $s_1 \sigma \in \overline{K}$, and $t \in \overline{K}$ by induction. If $\sigma \in \Sigma_{uc}$, controllability gives $t\sigma \in \overline{K}$. If $\sigma \in \Sigma_c$, observability with the pair $s_1$, $t$ gives $t\sigma \in \overline{K}$. $\blacksquare$

**Closure under union.** $P$, $P^{-1}$ and the intersection with $M$ commute with unions, so a union of normal languages is normal. So every $K$ has a largest normal sublanguage $\sup N(K)$, and, since controllability is also closed under union, a largest controllable and normal sublanguage $\sup CN(K)$. For a prefix-closed $K \subseteq L(G)$, Brandt et al. (1990) give closed formulas. The one for normality is

$$\sup N(K) = K - P^{-1}\big(P(L(G) - K)\big)\,\Sigma^*.$$

In words: drop $s$ from $K$ if some prefix of $s$ has the same projection as a plant string outside $K$. The projection step needs a [subset construction](/subset-construction/) in general, so the automaton for $\sup N(K)$ can be much larger than those for $K$ and $G$.

## Examples and non-examples

Let $\Sigma = \{a, u\}$ with $a$ observable and $u$ unobservable, both controllable, and $L(G) = \{\varepsilon, a, u, ua\}$. So $P(u) = \varepsilon$ and $P(ua) = a$. This is the plant of the example on [observable language](/observable-language/).

| $K$ | $P^{-1}(P(K)) \cap L(G)$ | normal | observable |
|---|---|---|---|
| $\{\varepsilon, a, u\}$ | $\{\varepsilon, a, u, ua\}$ | no | no |
| $\{\varepsilon, a\}$ | $\{\varepsilon, a, u, ua\}$ | no | yes |
| $\{\varepsilon, u\}$ | $\{\varepsilon, u\}$ | yes | yes |
| $\{\varepsilon\}$ | $\{\varepsilon, u\}$ | no | yes |

- **Normal.** $\{\varepsilon, u\}$ is normal: the only plant strings with projection $\varepsilon$ are $\varepsilon$ and $u$, and both are in it.
- **Observable but not normal.** $\{\varepsilon, a\}$ is observable, but $ua$ looks like $a$ and is not in it. This does not contradict the converse above: $u$ is controllable and unobservable, so $\Sigma_c \subseteq \Sigma_o$ is false here. $\{\varepsilon\}$ fails for the same reason, because $u$ looks like $\varepsilon$.
- **The supremal normal sublanguage.** For $K = \{\varepsilon, a, u\}$, the plant strings outside $K$ are $\{ua\}$, with projection $a$. The strings of $K$ with a prefix of projection $a$ are $\{a\}$. So $\sup N(K) = \{\varepsilon, u\}$. A brute force check over all sublanguages agrees. By contrast, $K$ has two maximal observable sublanguages, $\{\varepsilon, a\}$ and $\{\varepsilon, u\}$, and no largest one.
- **Full observation.** If $\Sigma_o = \Sigma$, then $P$ is the identity and every $K \subseteq M$ is normal.

## Related definitions

- **Observable language.** The weaker condition that is exact for the existence of a supervisor under partial observation. See [observable language](/observable-language/).
- **Controllable language.** See [controllable language](/controllable-language/). The supremal controllable and normal sublanguage is the least restrictive specification that a supervisor under partial observation can enforce among the normal ones. It can be smaller than a maximal controllable and observable sublanguage.
- **Supremal controllable sublanguage.** For full observation, $\sup C(K)$ is computed by a fixed point on a product automaton; see [supremal controllable sublanguage](/supremal-controllable-sublanguage/).
- **Normality in diagnosis.** The inverse projection $P^{-1}(P(s)) \cap L(G)$ is the set of strings that the [diagnosability](/diagnosability/) analysis must tell apart: the strings that the observer cannot distinguish from $s$.

## References
