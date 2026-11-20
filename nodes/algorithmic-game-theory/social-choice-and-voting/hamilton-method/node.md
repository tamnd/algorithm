---
tag: S01MQ4
kind: algorithm
slug: hamilton-method
name: Hamilton's method
aliases:
- largest remainder method
- Hare-Niemeyer method
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: Gives each party the integer part of its quota and the remaining seats to the parties with the largest fractional remainders.
model: word-ram
complexity:
  vars: {n: the number of states or parties, h: the number of seats}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1792
  people: [Alexander Hamilton]
  note: "Proposed for the US House after the census of 1790; Congress passed it in 1792, and Washington vetoed the bill. The US used it, with changes, for the censuses of 1850 to 1900."
prereqs: [apportionment-problem]
see_also: [apportionment-problem, alabama-paradox, balinski-young-theorem, dhondt-method, sainte-lague-method, huntington-hill-method, selection-problem, single-transferable-vote]
sources:
  - book: isbn:9780815701118
    title: "Michel L. Balinski and H. Peyton Young, Fair Representation: Meeting the Ideal of One Man, One Vote, 2nd edition, Brookings Institution Press, 2001"
    locator: "Chapter 3 (The Methods of Jefferson and Hamilton) and Chapter 5 (Paradoxes)"
  - paper: "M. L. Balinski and H. P. Young, The quota method of apportionment, American Mathematical Monthly 82(7) (1975), 701-730"
    locator: the quota property and house monotonicity, and why Hamilton's method has the first and not the second
  - paper: doi:10.1287/opre.2022.0419
    title: "Paul Gölz, Dominik Peters and Ariel D. Procaccia, In this apportionment lottery, the House always wins, Operations Research 74(1) (2026), 390-407"
    locator: "Section 3.1, Theorem 1: no deterministic method satisfies quota and population monotonicity"
---

Hamilton's method apportions $h$ seats among states or parties in proportion to their populations or votes. Each one first gets the whole part of its exact share, its quota, and the few seats that are left go to those with the largest fractional parts. The result always stays within quota, and it is the closest integer vector to the quotas. But it can take a seat away from a state when the house grows (the [Alabama paradox](/alabama-paradox/)) or when the state grows faster than another.

## In plain words

Work out the fair share of each state, which is usually not a whole number, for example 3.48 seats. Give each state the whole part of its share, here 3 seats. Some seats are still free, fewer than the number of states. Give them, one each, to the states whose shares were cut the most, that is, to the largest fractional parts. No state ends up more than one seat away from its fair share. The method is easy to explain and to check by hand.

## The problem

The input is the populations $p_1, \ldots, p_n \ge 0$, integers with sum $P > 0$, and the house size $h$. The quota of state $i$ is $q_i = h p_i / P$, its exact share, and $\sum_i q_i = h$. The output is integers $a_i \ge 0$ with $\sum_i a_i = h$. See the [apportionment problem](/apportionment-problem/) for the general setting and the other methods.

The method writes $q_i = \lfloor q_i \rfloor + \phi_i$ with $0 \le \phi_i < 1$, gives $\lfloor q_i \rfloor$ to every state and one more seat to each of the $s = h - \sum_i \lfloor q_i \rfloor$ states with the largest $\phi_i$. Ties go to the smallest index.

## The algorithm

All arithmetic is on integers: $\lfloor h p_i / P \rfloor$ is integer division, and the remainder $r_i = h p_i \bmod P$ is $P \phi_i$, so it orders the states in the same way as $\phi_i$.

```pseudo id=main
HAMILTON(p, h)                            ▷ p = (p_1, ..., p_n), h seats
L1  P ← p_1 + ... + p_n
L2  for i ← 1 to n do a_i ← ⌊h p_i / P⌋; r_i ← h p_i mod P
L3  s ← h - (a_1 + ... + a_n)            ▷ 0 ≤ s < n
L4  order the states by decreasing r_i, the smallest index among ties
L5  for each of the first s states i in this order do
L6      a_i ← a_i + 1
L7  return a
```

Line L2 gives the lower quotas and the remainders, line L3 counts the free seats, and lines L4 to L6 give them to the largest remainders.

## Example

Four parties have 100000, 80000, 30000 and 20000 votes, so $P = 230000$, and $h = 8$ seats are to be filled.

| party | votes | quota $q_i$ | $\lfloor q_i \rfloor$ | remainder $r_i$ | seats |
|---|---|---|---|---|---|
| 1 | 100000 | 3.478 | 3 | 110000 | 3 |
| 2 | 80000 | 2.783 | 2 | 180000 | 3 |
| 3 | 30000 | 1.043 | 1 | 10000 | 1 |
| 4 | 20000 | 0.696 | 0 | 160000 | 1 |

The lower quotas sum to 6, so $s = 2$ seats are free. The two largest remainders are those of parties 2 and 4, and the result is $(3, 3, 1, 1)$. The [Sainte-Lague method](/sainte-lague-method/) and the [Huntington-Hill method](/huntington-hill-method/) give the same result here, and the [D'Hondt method](/dhondt-method/) gives $(4, 3, 1, 0)$, which takes a seat from the smallest party.

## Correctness

The [proof](proofs/correctness.md) shows that $s = \sum_i \phi_i$, so $0 \le s < n$, and that a state with $\phi_i = 0$ never gets an extra seat. So the seats sum to $h$ and each state gets $\lfloor q_i \rfloor$ or $\lceil q_i \rceil$: the method satisfies quota. It also shows that the output minimizes $\sum_i (a_i - q_i)^2$ over all integer vectors with sum $h$. A transfer of one seat from $i$ to $j$ changes this sum by $2(d_j - d_i + 1)$, where $d = a - q$, so in an optimum all $d_i$ lie within 1 of each other, and the best choice of the extra seats is the one with the largest fractional parts.

## Complexity

Line L2 takes $O(n)$ operations on numbers of the size of $h P$. The sort of line L4 takes $O(n \log n)$ comparisons, and the rest is $O(n)$. A sort is not needed: a [selection](/selection-problem/) algorithm finds the $s$-th largest pair $(r_i, -i)$ in $O(n)$ worst-case time, by [median of medians](/median-of-medians/), and then one pass gives the extra seats. So the problem is solved in $O(n)$ time, independent of $h$. Extra space is $O(n)$.

## Properties

- **Quota.** Each state gets its lower or its upper quota, by construction.
- **Least squares.** The output minimizes $\sum_i (a_i - q_i)^2$, and also $\sum_i |a_i - q_i|^t$ for every $t \ge 1$, among all apportionments.
- **Alabama paradox.** With populations $(3, 3, 1)$, $h = 3$ gives $(1, 1, 1)$ and $h = 4$ gives $(2, 2, 0)$: the third state loses its seat when the house grows. See the [Alabama paradox](/alabama-paradox/).
- **Population paradox.** With $h = 5$, populations $(5, 1, 3)$ give $(3, 0, 2)$, and populations $(6, 1, 6)$ give $(2, 1, 2)$. State 1 grew and lost a seat to state 2, which did not change.
- **New states paradox.** Populations $(8, 1)$ with $h = 4$ give $(4, 0)$. Add a state of population 3 and one seat for it: populations $(8, 1, 3)$ with $h = 5$ give $(3, 1, 1)$, so the old states change their seats.
- **No divisor form.** Hamilton's method is not a divisor method. By the [Balinski-Young theorem](/balinski-young-theorem/), no method that satisfies quota is free of the population paradox.

## Variants and improvements

- **Other quotas.** Largest remainder methods for party lists divide the votes by a quota and give the remaining seats to the largest remainders. The Hare quota $P/h$ gives Hamilton's method. The Droop quota $\lfloor P/(h + 1) \rfloor + 1$ and the Imperiali quota $P/(h + 2)$ give fewer free seats, and with them the lower quotas can sum to more than $h$.
- **The quota method.** Balinski and Young (1975) gave a method that gives seats one at a time, as divisor methods do, but only to states that stay within upper quota. It satisfies quota and is house monotone, but it has the population paradox.
- **Divisor methods.** The [D'Hondt](/dhondt-method/), [Sainte-Lague](/sainte-lague-method/) and [Huntington-Hill](/huntington-hill-method/) methods have no Alabama or population paradox, but they can violate quota.
- **Lotteries.** A randomized method can give each state $\lfloor q_i \rfloor$ or $\lceil q_i \rceil$ seats with expected value exactly $q_i$. Gölz, Peters and Procaccia (2022) give one that is also house monotone.

## When to use it

Use Hamilton's method when the rule must be easy to explain and each party must get its quota rounded up or down. It suits a fixed house and a single election. It is a poor choice when the house size or the populations change over time and the changes must look fair, as in a census apportionment, because of the Alabama and population paradoxes.

## Pitfalls

- **Floating point.** Computing $h p_i / P$ in floating point can misorder two close remainders or even get the floor wrong. Use integer division and the remainder $h p_i \bmod P$.
- **Ties.** Two states with equal remainders can compete for the last seat. A law must say how to break the tie; this page uses the smallest index.
- **Zero populations.** A state with $p_i = 0$ has remainder 0 and never gets a seat. Do not let it win a tie at remainder 0; with the order of line L4 it cannot, because $s$ is less than the number of positive remainders.
- **The quota is not the result.** The method stays within quota, but it is not monotone in $h$. Do not assume that a larger house keeps the old seats.

## Implementations

## History

Alexander Hamilton proposed the method for the first apportionment of the US House after the census of 1790. Congress passed it in 1792, and George Washington vetoed the bill, his first veto; Jefferson's method was used instead. The method came back in 1850, proposed by Samuel Vinton, and was used with changes until the census of 1900. In 1880 C. W. Seaton, the chief clerk of the Census Office, found that Alabama would get 8 seats in a house of 299 and only 7 in a house of 300, the paradox that now carries its name. The population paradox appeared around 1900, and the new states paradox when Oklahoma joined in 1907. In Europe the same rule is called the Hare-Niemeyer method, and Germany used it for the Bundestag from 1987 to 2005. Balinski and Young (1975, 1982) studied it in their theory of apportionment.

## References
