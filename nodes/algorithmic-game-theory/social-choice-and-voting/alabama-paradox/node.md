---
tag: 30P4B2
kind: concept
slug: alabama-paradox
name: Alabama paradox
aliases:
- house size paradox
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Under Hamilton's method a state can lose a seat when the total number of seats rises.
prereqs: [apportionment-problem, hamilton-method]
see_also: [hamilton-method, apportionment-problem, balinski-young-theorem, dhondt-method, sainte-lague-method, huntington-hill-method, condorcet-paradox]
sources:
  - book: isbn:9780815701118
    title: "Michel L. Balinski and H. Peyton Young, Fair Representation: Meeting the Ideal of One Man, One Vote, 2nd edition, Brookings Institution Press, 2001"
    locator: "Chapter 5 (Paradoxes) and Appendix A (The Theory of Apportionment), on house monotonicity"
  - paper: "Michel L. Balinski and H. Peyton Young, The quota method of apportionment, American Mathematical Monthly 82(7) (1975), 701-730"
    locator: a method that stays within quota and is house monotone
---

The Alabama paradox is the fact that, under [Hamilton's method](/hamilton-method/) of apportionment, a state can lose a seat when the total number of seats grows and no population changes. It was found in 1880, when the Census Office computed the apportionment of the US House for many house sizes and saw that Alabama would get 8 seats in a House of 299 but 7 in a House of 300. A method that never shows it is called house monotone. All divisor methods are house monotone, and the paradox was one reason the US gave up Hamilton's method.

## In plain words

Suppose seats are shared out by giving each state the whole part of its fair share and then giving the leftover seats to the states with the largest fractions. Now add one seat to the parliament. Every fair share grows, but a large state's share grows faster than a small state's share. So the fraction of a large state can jump past the fraction of a small state. The small state can then drop out of the leftover seats and lose a seat, even though there are now more seats to share.

## The idea

Let the [apportionment problem](/apportionment-problem/) have populations $p_1, \ldots, p_n$ with sum $P$, and let $q_i(h) = h p_i / P$ be the quota of state $i$ for house size $h$. A method $f$ is house monotone if
$$f_i(p, h + 1) \ge f_i(p, h) \quad \text{for every } i \text{ and } h.$$
The Alabama paradox is a failure of this condition.

Hamilton's method gives state $i$ the floor $\lfloor q_i \rfloor$ and then gives the $h - \sum_i \lfloor q_i \rfloor$ leftover seats to the largest remainders $q_i - \lfloor q_i \rfloor$. When $h$ grows by one, $q_i$ grows by $p_i / P$, which is larger for a larger state. So the ranking of the remainders can change, and a small state can fall from the top places while the number of leftover seats stays the same or falls. Then it loses its leftover seat.

The divisor methods, such as the [D'Hondt](/dhondt-method/), [Sainte-Lague](/sainte-lague-method/) and [Huntington-Hill](/huntington-hill-method/) methods, give the seats one at a time in an order that does not depend on $h$. The apportionment for $h + 1$ seats is the one for $h$ seats plus one more seat, so they are house monotone. But each divisor method can give a state more than its upper quota or less than its lower quota. Balinski and Young (1975) found a method that stays within quota and is house monotone: give the seats one at a time as in the D'Hondt method, but only to states that would not exceed their upper quota.

## Examples

**A small example.** Three states have populations 3, 3 and 1, so $P = 7$.

| $h$ | quotas | floors | leftover seats | Hamilton |
|---|---|---|---|---|
| 3 | 1.29, 1.29, 0.43 | 1, 1, 0 | 1, to state 3 | (1, 1, 1) |
| 4 | 1.71, 1.71, 0.57 | 1, 1, 0 | 2, to states 1 and 2 | (2, 2, 0) |

With 3 seats, the remainder 0.43 of state 3 is the largest. With 4 seats it grows to 0.57, but the remainders of states 1 and 2 grow from 0.29 to 0.71, and state 3 loses its seat.

**Alabama in 1880.** The chief clerk of the Census Office, C. W. Seaton, computed the Hamilton apportionments for house sizes from 275 to 350. Alabama got 8 seats with 299 and 7 with 300.

**Related paradoxes.** In the population paradox, a state that grows loses a seat to a state that shrinks or stays the same. With 5 seats, populations $(5, 1, 3)$ give $(3, 0, 2)$ under Hamilton's method, and $(6, 1, 6)$ give $(2, 1, 2)$. In the new states paradox, a new state joins with its fair number of new seats, and the seats of the old states change. With 4 seats, populations $(8, 1)$ give $(4, 0)$; a new state of population 3 with 1 new seat gives $(3, 1, 1)$, and state 2 takes a seat from state 1. In 1907, when Oklahoma joined the Union with 5 new seats, Hamilton's method would have moved a seat from New York to Maine.

## Where it is used

- **Choosing an apportionment method.** House monotonicity is one of the basic tests in the theory of Balinski and Young. Hamilton's method fails it, and every divisor method passes it.
- **The Balinski-Young theorem.** The [Balinski-Young theorem](/balinski-young-theorem/) shows that no method for 4 or more states stays within quota and is free of the population paradox. Freedom from the Alabama paradox alone is possible with quota, as the quota method shows.
- **US history.** The House used Hamilton's method from 1850 to 1900. After the Alabama paradox of 1880 and similar cases after the census of 1900, Congress moved to Webster's method in 1911 and later to the Huntington-Hill method.
- **Party lists.** Countries that use the largest remainder method for party lists can show the same effect when the size of the assembly changes.

## References
