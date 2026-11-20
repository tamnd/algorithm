---
tag: 0PJPXR
kind: problem
slug: apportionment-problem
name: Apportionment problem
aliases:
- seat apportionment
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Allocate a fixed number of integer seats to states or parties in proportion to their populations or vote counts.
see_also: [hamilton-method, dhondt-method, sainte-lague-method, huntington-hill-method, alabama-paradox, balinski-young-theorem, single-transferable-vote, selection-problem]
sources:
  - book: isbn:9780815701118
    title: "Michel L. Balinski and H. Peyton Young, Fair Representation: Meeting the Ideal of One Man, One Vote, 2nd edition, Brookings Institution Press, 2001"
    locator: "Chapter 3 (The Methods of Jefferson and Hamilton), Chapter 10 (Staying within the Quota) and Appendix A (The Theory of Apportionment)"
  - paper: "Michel L. Balinski and H. Peyton Young, The quota method of apportionment, American Mathematical Monthly 82(7) (1975), 701-730"
    locator: the quota and house monotonicity conditions and a method that meets both
  - paper: doi:10.1007/978-3-319-13075-0_46
    title: "Zhanpeng Cheng and David Eppstein, Linear-time algorithms for proportional apportionment, Proc. 25th International Symposium on Algorithms and Computation (ISAAC 2014), LNCS 8889, 581-592"
    locator: divisor methods in O(n) time, independent of the number of seats
  - paper: doi:10.1287/opre.2022.0419
    title: "Paul Gölz, Dominik Peters and Ariel D. Procaccia, In this apportionment lottery, the house always wins, Operations Research 74(1) (2026), 390-407"
    locator: "Section 3.1, Theorem 1 (no method satisfies quota and population monotonicity for 5 states) and the definitions of the axioms"
---

The apportionment problem asks how to divide a fixed number of seats among states or parties in proportion to their populations or votes. The exact share, the quota, is almost never an integer, so some rounding rule must decide who gets the extra seats. The main rules are the largest remainder method of [Hamilton](/hamilton-method/) and the divisor methods of [D'Hondt](/dhondt-method/), [Sainte-Lague](/sainte-lague-method/) and [Huntington-Hill](/huntington-hill-method/). The [Balinski-Young theorem](/balinski-young-theorem/) shows that no rule has all the fairness properties one would like.

## In plain words

A parliament has a fixed number of seats, and each state or party should get seats in proportion to its size. If a state has a tenth of the people, it should get a tenth of the seats. But a tenth of the seats is usually not a whole number, and seats cannot be split. So the fractions must be rounded, and the rounded numbers must still add up to the total. There are many ways to do this. They differ in who gets the last seats, and some of them behave in strange ways: a state can lose a seat when the parliament grows, or when it grows faster than another state.

## Definition

The input is the populations $p = (p_1, \ldots, p_n)$, nonnegative integers with sum $P > 0$, and the house size $h \ge 0$. An apportionment is a vector of integers $a = (a_1, \ldots, a_n) \ge 0$ with $\sum_i a_i = h$. The quota of state $i$ is
$$q_i = \frac{h \, p_i}{P},$$
and the quotas sum to $h$. A method maps every input $(p, h)$ to an apportionment, or to a set of them when ties are allowed. Common requirements on a method $f$ are:

- **Quota.** $\lfloor q_i \rfloor \le a_i \le \lceil q_i \rceil$ for every $i$. Lower quota and upper quota are the two halves.
- **House monotone.** $f(p, h + 1) \ge f(p, h)$ in every entry. A method that fails this shows the [Alabama paradox](/alabama-paradox/).
- **Population monotone.** If $p'_i \ge p_i$ and $p'_j \le p_j$, then it is not the case that $a'_i < a_i$ and $a'_j > a_j$, where $a = f(p, h)$ and $a' = f(p', h)$. A method that fails this shows the population paradox.
- **Anonymous and homogeneous.** The result does not depend on the order of the states, and multiplying all populations by the same factor does not change it.

A divisor method is given by a rounding rule $d(a)$ with $a \le d(a) \le a + 1$: it picks a divisor $\lambda > 0$ and gives state $i$ the number $p_i/\lambda$ rounded up when it exceeds $d(\lfloor p_i/\lambda \rfloor)$, with $\lambda$ chosen so that the seats sum to $h$.

## Variants

- **Party lists.** The units are parties and the weights are votes. A legal threshold, such as 5 percent of the votes, often removes small parties first.
- **Minimum seats.** The US House gives every state at least one seat; other bodies use a minimum and a maximum per unit.
- **Biproportional apportionment.** Seats are divided among parties and districts at once, so that both the row sums and the column sums are fixed.
- **Degressive proportionality.** Some bodies, such as the European Parliament, give small units more seats per person on purpose.
- **Ranked ballots.** If voters rank candidates and not parties, proportional results come from rules such as the [single transferable vote](/single-transferable-vote/), which is a different problem.

## Examples

Four states have populations 100000, 80000, 30000 and 20000, with quotas $1.74, 1.39, 0.52, 0.35$ for $h = 4$ and $3.48, 2.78, 1.04, 0.70$ for $h = 8$. The four methods give:

| method | $h = 4$ | $h = 8$ |
|---|---|---|
| [Hamilton](/hamilton-method/) | (2, 1, 1, 0) | (3, 3, 1, 1) |
| [D'Hondt](/dhondt-method/) | (2, 2, 0, 0) | (4, 3, 1, 0) |
| [Sainte-Lague](/sainte-lague-method/) | (2, 1, 1, 0) | (3, 3, 1, 1) |
| [Huntington-Hill](/huntington-hill-method/) | (1, 1, 1, 1) | (3, 3, 1, 1) |

D'Hondt favors the large states, Huntington-Hill gives every state a seat, and the other two lie between. At $h = 8$, D'Hondt gives state 1 four seats against a quota of 3.48, so it breaks upper quota.

Hamilton's method shows the paradoxes on small inputs. With populations $(3, 3, 1)$ it gives $(1, 1, 1)$ for $h = 3$ but $(2, 2, 0)$ for $h = 4$. With $h = 5$, populations $(5, 1, 3)$ give $(3, 0, 2)$, and populations $(6, 1, 6)$ give $(2, 1, 2)$: state 1 grew and state 3 grew much faster, and state 1 lost a seat to state 2, which did not grow.

## Known algorithms

- **Hamilton's method** gives each state $\lfloor q_i \rfloor$ seats and the rest to the largest remainders. It meets quota but is neither house nor population monotone. With integer arithmetic it takes $O(n \log n)$ time by sorting, or $O(n)$ with a [selection](/selection-problem/) algorithm.
- **Divisor methods** give the seats one at a time to the largest $p_i/d(a_i)$. A heap gives $O(n + h \log n)$ time. They are house and population monotone, but each one fails quota on some input with 4 or more states. The D'Hondt method ($d(a) = a + 1$) meets lower quota, and Adams's method ($d(a) = a$) meets upper quota.
- **The quota method** of Balinski and Young (1975) gives the seats one at a time like D'Hondt, but only to states that would stay within upper quota. It meets quota and is house monotone, but it is not population monotone.

## Bounds

Every method must read all $n$ populations, so $\Omega(n)$ time is needed. Hamilton's method meets this bound with linear-time selection, and Cheng and Eppstein (2014) give an $O(n)$ time algorithm for every divisor method, independent of $h$; the heap method is slower when $h$ is much larger than $n$. On the side of axioms, the [Balinski-Young theorem](/balinski-young-theorem/) shows that no method is both within quota and population monotone for 4 or more states. The proof of Balinski and Young assumes that a larger state never gets fewer seats; Gölz, Peters and Procaccia drop that assumption with 5 states. With 3 states, Webster's method is both. Balinski and Young also show that, in their setting, the divisor methods are the only population monotone methods.

## Reductions

- **Hamilton to selection.** After the floors are given, the $s = h - \sum_i \lfloor q_i \rfloor < n$ extra seats go to the $s$ largest remainders, which is a selection problem.
- **Divisor methods to separable convex allocation.** The D'Hondt method minimizes $\sum_i a_i(a_i + 1)/p_i$ and Webster's method minimizes $\sum_i a_i^2/p_i$, over integers $a \ge 0$ with sum $h$. Each cost is a sum of marginal costs that increase, so the greedy rule that takes the cheapest next seat is optimal.
- **Divisor methods to selection in sorted lists.** The seats are the $h$ largest numbers in the $n$ sorted lists $p_i/d(0), p_i/d(1), \ldots$. Cheng and Eppstein solve this by finding a good divisor and then correcting by $O(n)$ seats.

## Applications

- The US House of Representatives divides its 435 seats among the states after each census with the Huntington-Hill method.
- Many countries with party list voting use the D'Hondt method or the Sainte-Lague method to turn votes into seats.
- Rounding a list of percentages or a budget split so that it still sums to the total is the same problem. Hamilton's method is common there.

## References
