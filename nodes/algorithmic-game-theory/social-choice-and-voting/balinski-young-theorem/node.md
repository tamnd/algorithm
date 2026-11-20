---
tag: 1PQ6WN
kind: theorem
slug: balinski-young-theorem
name: Balinski-Young theorem
aliases:
- apportionment impossibility theorem
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: No apportionment method for 4 or more states always stays within quota and is free of the population paradox.
prereqs: [apportionment-problem]
see_also: [apportionment-problem, hamilton-method, alabama-paradox, sainte-lague-method, huntington-hill-method, dhondt-method, arrow-impossibility-theorem, gibbard-satterthwaite-theorem]
sources:
  - book: isbn:9780815701118
    title: "Michel L. Balinski and H. Peyton Young, Fair Representation: Meeting the Ideal of One Man, One Vote, 2nd edition, Brookings Institution Press, 2001"
    locator: "Chapter 10 (Staying within the Quota) and Appendix A (The Theory of Apportionment), Section 6, on quota and population monotonicity"
  - paper: doi:10.1287/opre.2022.0419
    title: "Paul Gölz, Dominik Peters and Ariel D. Procaccia, In this apportionment lottery, the house always wins, Operations Research 74(1) (2026), 390-407"
    locator: "Section 3.1, Theorem 1 (a proof for 5 states that does not assume order preservation), and the remarks on 3 and 4 states"
  - paper: "Michel L. Balinski and H. Peyton Young, The quota method of apportionment, American Mathematical Monthly 82(7) (1975), 701-730"
    locator: a method that stays within quota and is house monotone
---

The Balinski-Young theorem says that no method of apportionment can always give every state its quota rounded up or down and also be free of the population paradox, as soon as there are enough states. Michel Balinski and H. Peyton Young proved it in 1982 for 4 or more states. It means that every method must give up one of the two properties: [Hamilton's method](/hamilton-method/) keeps quota and has paradoxes, and the divisor methods, such as the [Huntington-Hill method](/huntington-hill-method/), avoid the paradoxes and sometimes break quota. It plays the same role for the [apportionment problem](/apportionment-problem/) as [Arrow's theorem](/arrow-impossibility-theorem/) plays for voting.

## Statement

Let a method $f$ map populations $p = (p_1, \ldots, p_n)$, integers $p_i \ge 0$ with sum $P > 0$, and a house size $h$ to an apportionment $a = f(p, h)$: integers $a_i \ge 0$ with $\sum_i a_i = h$. The quota of state $i$ is $q_i = h p_i / P$.

- $f$ **satisfies quota** if $\lfloor q_i \rfloor \le a_i \le \lceil q_i \rceil$ for every input and every $i$.
- $f$ is **population monotone** if for all $p$, $p'$ with the same $n$ and $h$, and all states $i \ne j$ with $p'_i \ge p_i$ and $p'_j \le p_j$, it is not the case that $a'_i < a_i$ and $a'_j > a_j$, where $a = f(p, h)$ and $a' = f(p', h)$.

**Theorem.** For every $n \ge 5$ there is no method for $n$ states that satisfies quota and is population monotone. This holds already for $h = 10$.

Balinski and Young (1982) proved the theorem for every $n \ge 4$, under one more assumption on the method: it is order preserving, that is, $p_i > p_j$ implies $a_i \ge a_j$. The proof below, by Gölz, Peters and Procaccia, does not need that assumption.

## In plain words

When seats are shared among states, two rules seem fair. First, every state should get its exact fair share rounded up or down, never further away. Second, if one state grows and another shrinks, the growing state should not lose a seat to the shrinking one. The theorem says that once there are four or five states, no rule can follow both of these all the time. For every rule there is some list of populations for which it breaks one of them. So a country must decide which of the two it cares about more.

## Proof

Fix $n = 5$ and $h = 10$, and suppose $f$ satisfies quota and is population monotone. Consider the populations
$$A = (824, 44, 44, 44, 44), \qquad P = 1000,$$
with quotas $8.24$ for state 1 and $0.44$ for each other state. By quota, state 1 gets 8 or 9 seats and every other state gets 0 or 1.

*Case 1: state 1 gets 9 seats at $A$.* Then exactly one other state $k$ gets 1 seat, and the remaining three get 0. Let $B$ be $A$ with $p_k$ raised from 44 to 222. Then $P = 1178$, the quota of state 1 is $8240/1178 \approx 6.995$, the quota of state $k$ is $2220/1178 \approx 1.885$, and the quota of each of the other three is $440/1178 \approx 0.374$. By quota, state 1 gets at most 7 seats and state $k$ at most 2, so the other three states share at least $10 - 7 - 2 = 1$ seat. Let $j$ be one of them with a seat. Now compare $A$ with $B$. The populations of states 1 and $j$ did not change, so $p'_1 \ge p_1$ and $p'_j \le p_j$. But state 1 went from 9 seats to at most 7, and state $j$ went from 0 to 1. This breaks population monotonicity.

*Case 2: state 1 gets 8 seats at $A$.* Then two other states $k$ and $m$ get 1 seat each, and the remaining two states $r$ and $s$ get 0. Let $C$ be $A$ with $p_r$ and $p_s$ lowered from 44 to 1. Then $P = 914$, the quota of state 1 is $8240/914 \approx 9.015$, the quotas of $k$ and $m$ are $440/914 \approx 0.481$, and those of $r$ and $s$ are $10/914 \approx 0.011$. By quota, state 1 gets at least 9 seats, so $k$ and $m$ share at most 1 seat, and one of them, say $k$, gets 0. Compare $A$ with $C$. The populations of states $k$ and 1 did not change, so $p'_k \ge p_k$ and $p'_1 \le p_1$. But state $k$ went from 1 seat to 0, and state 1 went from 8 to at least 9. This again breaks population monotonicity.

Both cases lead to a contradiction, so no such $f$ exists for $n = 5$. For $n > 5$, add states with population 0 to $A$, $B$ and $C$. Their quotas are 0, so by quota they get no seats, and the argument is unchanged. $\square$

In both cases, the two states that are compared have the same populations before and after. The proof only uses that such a state cannot lose a seat to another such state when the populations of other states change. So the theorem holds even for this weaker form of population monotonicity.

## Consequences

- **Every method gives something up.** [Hamilton's method](/hamilton-method/) satisfies quota, so it shows the population paradox for some inputs. Every divisor method, such as the [D'Hondt](/dhondt-method/), [Sainte-Lague](/sainte-lague-method/) and [Huntington-Hill](/huntington-hill-method/) methods, is population monotone, so it breaks quota for some inputs.
- **Divisor methods are the monotone ones.** Balinski and Young also show that, in their setting, the population monotone methods are the divisor methods. Together with the theorem, the choice is between quota and the divisor methods.
- **Choosing among divisor methods.** Since some quota violations cannot be avoided, Balinski and Young compare the divisor methods by how often they break quota and by their bias toward large or small states. They recommend Webster's method, which is unbiased and rarely breaks quota for populations like those of the US states.
- **House monotonicity alone is not the problem.** The quota method of Balinski and Young (1975) satisfies quota and is free of the [Alabama paradox](/alabama-paradox/). The conflict is between quota and population monotonicity.

## Tightness

- **Two and three states.** With 2 states, Hamilton's method and Webster's method agree, and they satisfy both properties. With 3 states, Webster's method satisfies quota and is population monotone (Balinski and Young 1982, Proposition 6.2, as cited by Gölz, Peters and Procaccia). So the bound on $n$ cannot go below 4.
- **Four states.** For order preserving methods, the theorem of Balinski and Young covers $n = 4$. Gölz, Peters and Procaccia note that without order preservation the case $n = 4$ was open. A preprint of 2026 (Lav R. Varshney, arXiv:2608.02759) shows that for 4 states, quota is incompatible with a stronger form of population monotonicity that also compares different house sizes. It has not yet been refereed.
- **Each property alone is possible.** Hamilton's method satisfies quota, and every divisor method is population monotone. Neither condition of the theorem can be dropped.

## History

The Alabama and population paradoxes of Hamilton's method were seen in the US House apportionments between 1880 and 1900. In the debates of the 1920s, Willcox and Huntington argued only about divisor methods, which avoid these paradoxes but can break quota. Michel Balinski and H. Peyton Young built the axiomatic theory of apportionment in a series of papers in the 1970s, including the quota method of 1975, and proved the impossibility in their book Fair Representation in 1982. The second edition appeared in 2001. Paul Gölz, Dominik Peters and Ariel Procaccia gave the short 5-state proof without order preservation in their work on randomized apportionment, published in Operations Research.

## References
