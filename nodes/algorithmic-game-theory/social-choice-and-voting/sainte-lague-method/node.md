---
tag: YHWSF5
kind: algorithm
slug: sainte-lague-method
name: "Sainte-Lague method"
aliases:
- Webster method
- major fractions method
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Assigns seats one at a time to the party with the largest votes divided by 2s + 1, where s is its current number of seats.
model: word-ram
complexity:
  vars: {n: the number of parties, h: the number of seats}
  time: {worst: O(n + h log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1832
  people: [Daniel Webster, Andre Sainte-Lague]
  note: "Webster proposed rounding at one half for the US House in 1832, and it was used after the census of 1840. Sainte-Lague derived the same rule from least squares in 1910."
prereqs: [apportionment-problem, dhondt-method]
see_also: [apportionment-problem, dhondt-method, huntington-hill-method, hamilton-method, balinski-young-theorem, alabama-paradox, priority-queue, single-transferable-vote]
sources:
  - book: isbn:9780815701118
    title: "Michel L. Balinski and H. Peyton Young, Fair Representation: Meeting the Ideal of One Man, One Vote, 2nd edition, Brookings Institution Press, 2001"
    locator: "Chapter 4 (The Method of Webster), Chapter 9 (Eliminating Bias) and Appendix A (The Theory of Apportionment)"
  - paper: doi:10.24033/asens.627
    title: "André Sainte-Laguë, La représentation proportionnelle et la méthode des moindres carrés, Annales scientifiques de l'École Normale Supérieure, 3e série, 27 (1910), 529-542"
    locator: the rule as the minimum of a sum of squares
  - paper: doi:10.1007/978-3-319-13075-0_46
    title: "Zhanpeng Cheng and David Eppstein, Linear-time algorithms for proportional apportionment, Proc. 25th International Symposium on Algorithms and Computation (ISAAC 2014), LNCS 8889, 581-592"
    locator: divisor methods in O(n) time, independent of the number of seats
---

The Sainte-Lague method apportions $h$ seats among parties or states in proportion to their votes. It gives the seats one at a time, each to the party with the largest quotient of its votes divided by $2s + 1$, where $s$ is its number of seats so far. It is the same as Webster's method, the divisor method that rounds every quotient to the nearest integer. Unlike the [D'Hondt method](/dhondt-method/), it favors neither large nor small parties, and it has no Alabama or population paradox, but in rare cases it gives a party less than its lower quota or more than its upper quota.

## In plain words

Write each party's vote total at the top of a column. Below it write the total divided by 3, by 5, by 7, and so on, using only odd numbers. Give the seats to the largest numbers in the whole table, one seat for each number. This is the same as finding a number of votes per seat such that, when each party's votes are divided by it and rounded in the usual way, the seats add up to the house size. The usual rounding treats large and small parties alike, so neither group gains on average.

## The problem

The input is the votes $p_1, \ldots, p_n \ge 0$, integers with sum $P > 0$, and the number of seats $h$. The output is integers $a_i \ge 0$ with $\sum_i a_i = h$. The quota of party $i$ is $q_i = h p_i / P$. See the [apportionment problem](/apportionment-problem/) for the setting and the other methods.

Webster's method in divisor form is: find a divisor $\lambda > 0$ such that the numbers $p_i / \lambda$, each rounded to the nearest integer, sum to $h$, and give party $i$ that rounded number. A number between $a$ and $a + 1$ rounds up when it is above $a + 1/2$, the arithmetic mean. The Sainte-Lague rule in highest averages form gives each seat to the party with the largest $p_i/(a_i + 1/2)$, or equivalently $p_i/(2 a_i + 1)$, ties to the smallest index. The two forms give the same apportionments.

## The algorithm

The algorithm is the one of the D'Hondt method with other divisors. A [priority queue](/priority-queue/) holds one key per party, and two keys $p_i/d_i$ and $p_j/d_j$ are compared by the integers $p_i d_j$ and $p_j d_i$.

```pseudo id=main
SAINTE-LAGUE(p, h)                        ▷ p = (p_1, ..., p_n) votes, h seats
L1  a_i ← 0 for each i
L2  Q ← a max-priority queue of the parties, with keys p_i / 1
L3  repeat h times
L4      i ← extract from Q the largest key, the smallest index among ties
L5      a_i ← a_i + 1
L6      insert i into Q with key p_i / (2 a_i + 1)
L7  return a
```

Each pass of lines L3 to L6 gives one seat. Only line L6 differs from the D'Hondt method: it divides by $2 a_i + 1$, not by $a_i + 1$.

## Example

Four parties have 100000, 80000, 30000 and 20000 votes, and $h = 8$ seats are to be filled. The table lists the quotients $p_i / d$, rounded for display; the numbers in bold get the seats, in the order given in brackets.

| divisor | party 1 | party 2 | party 3 | party 4 |
|---|---|---|---|---|
| 1 | **100000** (1) | **80000** (2) | **30000** (4) | **20000** (7) |
| 3 | **33333** (3) | **26667** (5) | 10000 | 6667 |
| 5 | **20000** (6) | **16000** (8) | 6000 | 4000 |
| 7 | 14286 | 11429 | 4286 | 2857 |

The result is $(3, 3, 1, 1)$, the same as [Hamilton's method](/hamilton-method/) and the [Huntington-Hill method](/huntington-hill-method/) give, while the [D'Hondt method](/dhondt-method/) gives $(4, 3, 1, 0)$. Seats 6 and 7 tie at 20000; both go to their parties, so the tie does not matter for $h = 8$, but for $h = 6$ it gives the seat to party 1. In divisor form, $\lambda = 30000$ works: $100000/30000 = 3.33$, $80000/30000 = 2.67$, $30000/30000 = 1$ and $20000/30000 = 0.67$ round to $3, 3, 1, 1$. With $h = 4$, the method gives $(2, 1, 1, 0)$, and the Huntington-Hill method gives $(1, 1, 1, 1)$.

## Correctness

The [proof](proofs/correctness.md) shows that the keys of the seats never increase, so the largest key left at the end, $\ell$, is at most the smallest key that won a seat, $u = \min_i p_i/(2 a_i - 1)$. For every $\mu$ strictly between them, $\lambda = 2\mu$ puts each $p_i/\lambda$ strictly between $a_i - 1/2$ and $a_i + 1/2$, so the seats are the rounded quotients. The proof also shows least squares, house monotonicity and population monotonicity, and checks the quota violation below.

## Complexity

As for the D'Hondt method, a binary heap gives $O(n + h \log n)$ time and $O(n)$ extra space, a linear scan gives $O(n h)$, and the method of Cheng and Eppstein (2014) gives $O(n)$ time for any divisor method. The comparisons use products of numbers of $O(\log P + \log h)$ bits.

## Properties

- **Least squares.** The result minimizes $\sum_i a_i^2/p_i$, which equals $\sum_i p_i (a_i/p_i - h/P)^2 + h^2/P$: it makes the seats per voter as equal as possible in this weighted sense. The cost of the next seat of party $i$ is $(2 a_i + 1)/p_i$, which grows with $a_i$, and the method always takes the cheapest one. This is how Sainte-Lague (1910) derived it.
- **No bias.** Balinski and Young show that, among divisor methods, Webster's method is the one that favors neither large nor small states on average.
- **House and population monotone.** One more seat never takes a seat away, and a party that gains votes does not lose a seat to a party that loses votes, except through a tie.
- **Quota can fail.** With votes $(26, 5, 3, 1)$ and $h = 19$, the method gives $(13, 3, 2, 1)$, while the quota of party 1 is $494/35 \approx 14.11$; there is no tie. By the [Balinski-Young theorem](/balinski-young-theorem/), every population monotone method fails quota for some input with 4 or more parties. With 3 parties, Webster's method stays within quota.
- **Small parties.** The first divisor 1 makes the first seat cheap, so a party with about half a quota can win a seat.

## Variants and improvements

- **Modified Sainte-Lague.** The first divisor is raised from 1 to a larger value, such as 1.4 in Norway, so that a party needs more votes for its first seat.
- **Sainte-Lague/Schepers.** The rounding form with a divisor found by search, used in Germany. It gives the same seats as the highest averages form, up to ties.
- **Other divisor methods.** The [D'Hondt method](/dhondt-method/) rounds down, Adams's method rounds up, the [Huntington-Hill method](/huntington-hill-method/) rounds at the geometric mean $\sqrt{a(a + 1)}$, and Dean's method at the harmonic mean $2a(a + 1)/(2a + 1)$.
- **Biproportional apportionment.** Seats are apportioned to parties and districts at once, with Webster rounding and one divisor per row and per column.

## When to use it

Use the Sainte-Lague method for party lists or for states when large and small units must be treated alike, and the paradoxes of [Hamilton's method](/hamilton-method/) are not acceptable. Balinski and Young recommend Webster's method for the US House. If a law must guarantee that no party gets less than its lower quota, use the D'Hondt method; if it must guarantee both quotas, use Hamilton's method and accept the paradoxes.

## Pitfalls

- **Dividing by $a + 1/2$ in floating point.** Use the odd divisors $2a + 1$ and integer cross products, so that ties are seen as ties.
- **Ties.** In the example, seats 6 and 7 tie at 20000. If only one seat were left, the tie rule would decide it. State the rule.
- **Not the same as Hamilton's method.** The two often agree, as in the example, but not always: with votes $(26, 5, 3, 1)$ and $h = 19$, Hamilton's method stays within quota and Sainte-Lague does not.
- **Modified first divisor.** Laws that use 1.4 or 1.2 as the first divisor are not Webster's method. Check which one the law means.

## Implementations

## History

Daniel Webster proposed rounding at one half for the US House in 1832. Congress used his method for the census of 1840, and again for those of 1910 and 1930, when Walter Willcox argued for it as the method of major fractions. André Sainte-Laguë derived the same rule in 1910 as the solution of a least squares problem. Germany has used it for the Bundestag since 2009, and New Zealand uses it for its list seats. Balinski and Young (1982) showed that it is the unbiased divisor method and argued for its use in the US.

## References
