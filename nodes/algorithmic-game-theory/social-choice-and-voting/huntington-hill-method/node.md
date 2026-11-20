---
tag: Y00758
kind: algorithm
slug: huntington-hill-method
name: Huntington-Hill method
aliases:
- method of equal proportions
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: A divisor method that rounds each quota at the geometric mean of consecutive integers. The US House of Representatives uses it.
model: word-ram
complexity:
  vars: {n: the number of states, h: the number of seats}
  time: {worst: O(n + h log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1911
  people: [Joseph A. Hill, Edward V. Huntington]
  note: "Hill proposed the method in 1911 and Huntington gave its theory in the 1920s. Congress adopted it in 1941, and the US House has used it since the census of 1940."
prereqs: [apportionment-problem, dhondt-method]
see_also: [apportionment-problem, sainte-lague-method, dhondt-method, hamilton-method, balinski-young-theorem, alabama-paradox, priority-queue, binary-heap]
sources:
  - book: isbn:9780815701118
    title: "Michel L. Balinski and H. Peyton Young, Fair Representation: Meeting the Ideal of One Man, One Vote, 2nd edition, Brookings Institution Press, 2001"
    locator: "Chapter 6 (The Controversy over Bias) and Appendix A (The Theory of Apportionment)"
  - paper: "Edward V. Huntington, The apportionment of representatives in Congress, Transactions of the American Mathematical Society 30(1) (1928), 85-110"
    locator: the pairwise tests of relative difference and the method of equal proportions
  - paper: doi:10.1007/978-3-319-13075-0_46
    title: "Zhanpeng Cheng and David Eppstein, Linear-time algorithms for proportional apportionment, Proc. 25th International Symposium on Algorithms and Computation (ISAAC 2014), LNCS 8889, 581-592"
    locator: divisor methods in O(n) time, independent of the number of seats
---

The Huntington-Hill method apportions $h$ seats among $n$ states in proportion to their populations, and gives every state at least one seat. It is the divisor method that rounds each quotient at the geometric mean $\sqrt{a(a + 1)}$ of the two integers around it. In the highest averages form, each seat after the first $n$ goes to the state with the largest priority $p_i/\sqrt{a_i(a_i + 1)}$. The US House of Representatives has used it since 1941.

## In plain words

Every state first gets one seat. The other seats are then given one at a time. For each state, compute a priority number: its population divided by the square root of its seats times its seats plus one. The next seat goes to the state with the highest priority, and that state's priority then drops. This is the same as finding a number of people per seat such that, when each population is divided by it and rounded, the seats add up to the house size. The rounding point between two whole numbers is not the midpoint but a little below it, which helps small states a little.

## The problem

The input is the populations $p_1, \ldots, p_n \ge 0$, integers with sum $P > 0$, and the number of seats $h \ge n$. The output is integers $a_i \ge 1$ with $\sum_i a_i = h$. The quota of state $i$ is $q_i = h p_i / P$. See the [apportionment problem](/apportionment-problem/) for the setting and the other methods.

In divisor form, the method finds a divisor $\lambda > 0$ and gives state $i$ the number $p_i/\lambda$ rounded at the geometric mean: a number $x$ with $a < x < a + 1$ rounds up when $x > \sqrt{a(a + 1)}$. Since $\sqrt{0 \cdot 1} = 0$, every state with $p_i > 0$ gets at least one seat. The highest averages form gives one seat to each state and then each further seat to the state with the largest $p_i/\sqrt{a_i(a_i + 1)}$, ties to the smallest index. The two forms give the same apportionments.

## The algorithm

The algorithm is the one of the [D'Hondt method](/dhondt-method/), with a different start and other divisors. To avoid square roots, a [priority queue](/priority-queue/) holds the squared priorities $p_i^2/(a_i(a_i + 1))$, and two keys $s_i/d_i$ and $s_j/d_j$ are compared by the integers $s_i d_j$ and $s_j d_i$.

```pseudo id=main
HUNTINGTON-HILL(p, h)                     ▷ p = (p_1, ..., p_n) populations, h seats
L1  if h < n then fail                     ▷ every state needs one seat
L2  a_i ← 1 for each i
L3  Q ← a max-priority queue of the states, with keys p_i^2 / 2
L4  repeat h - n times
L5      i ← extract from Q the largest key, the smallest index among ties
L6      a_i ← a_i + 1
L7      insert i into Q with key p_i^2 / (a_i (a_i + 1))
L8  return a
```

Each pass of lines L4 to L7 gives one seat. Since the priorities are not negative, the order of their squares is the order of the priorities.

## Example

Four states have populations 100000, 80000, 30000 and 20000, and $h = 8$ seats are to be filled. Each state first gets one seat. The table lists the priorities $p_i/\sqrt{a(a + 1)}$, rounded for display; the numbers in bold get seats 5 to 8, in the order given in brackets.

| seats so far $a$ | state 1 | state 2 | state 3 | state 4 |
|---|---|---|---|---|
| 1 ($\sqrt{2}$) | **70711** (5) | **56569** (6) | 21213 | 14142 |
| 2 ($\sqrt{6}$) | **40825** (7) | **32660** (8) | 12247 | 8165 |
| 3 ($\sqrt{12}$) | 28868 | 23094 | 8660 | 5774 |

The result is $(3, 3, 1, 1)$, the same as the [Sainte-Lague method](/sainte-lague-method/) and [Hamilton's method](/hamilton-method/) give. In divisor form, $\lambda = 30000$ works: $100000/30000 \approx 3.33$ and $80000/30000 \approx 2.67$ lie between $\sqrt{6} \approx 2.45$ and $\sqrt{12} \approx 3.46$, so they round to 3, and $1$ and $0.67$ lie below $\sqrt{2}$, so they round to 1. With $h = 4$ the method gives $(1, 1, 1, 1)$, while the Sainte-Lague method gives $(2, 1, 1, 0)$ and the [D'Hondt method](/dhondt-method/) gives $(2, 2, 0, 0)$.

## Correctness

The [proof](proofs/correctness.md) shows that the heap picks the same state as the greedy rule, and that the squared keys of the seats never increase. So the largest squared key left at the end, $\ell$, is at most $u = \min_{a_i \ge 2} p_i^2/((a_i - 1) a_i)$, and for every $M$ strictly between them, $\lambda = \sqrt{M}$ puts each $p_i/\lambda$ strictly between $\sqrt{(a_i - 1) a_i}$ and $\sqrt{a_i(a_i + 1)}$. The proof also shows Huntington's pairwise test, house and population monotonicity, and checks the quota violation below.

## Complexity

With a [binary heap](/binary-heap/), line L3 takes $O(n)$ time and each of the $h - n$ passes takes $O(\log n)$, so the time is $O(n + h \log n)$ and the extra space is $O(n)$. The keys $p_i^2$ and $a_i(a_i + 1)$ have $O(\log P + \log h)$ bits, and each comparison multiplies two of them. Cheng and Eppstein (2014) give an $O(n)$ time algorithm for every divisor method, independent of $h$.

## Properties

- **One seat for every state.** Rounding at $\sqrt{0 \cdot 1} = 0$ gives every state with a positive population at least one seat. The US Constitution requires this for the House.
- **Huntington's pairwise test.** No transfer of one seat between two states lowers the relative difference of their seats per person, $\max(r_i, r_j)/\min(r_i, r_j) - 1$ with $r_i = a_i/p_i$. The same holds for the relative difference of their people per seat. Huntington showed that this test picks out the method, which he called the method of equal proportions.
- **House and population monotone.** One more seat never takes a seat away, so there is no [Alabama paradox](/alabama-paradox/). A state that grows does not lose a seat to a state that shrinks, except through a tie.
- **Quota can fail.** With populations $(18, 7, 2, 1)$ and $h = 8$, the method gives $(4, 2, 1, 1)$, while the quota of state 1 is $36/7 \approx 5.14$; there is no tie. By the [Balinski-Young theorem](/balinski-young-theorem/), every population monotone method fails quota for some input with 4 or more states.
- **A small bias.** The geometric mean is below the midpoint, so small states round up a little more often than under the [Sainte-Lague method](/sainte-lague-method/). Balinski and Young show that the method favors small states on average, though much less than Adams's method.

## Variants and improvements

- **Priority list.** The US Census Bureau computes the priorities $p_i/\sqrt{a(a + 1)}$ for $a = 1, 2, \ldots$ for all states, sorts them, and gives seats 51 to 435 down the list. This is the same algorithm with a sort in place of the heap, and it gives the apportionment for every house size at once.
- **Other divisor methods.** The [D'Hondt method](/dhondt-method/) rounds down, Adams's method rounds up, the [Sainte-Lague method](/sainte-lague-method/) rounds at the midpoint $a + 1/2$, and Dean's method at the harmonic mean $2a(a + 1)/(2a + 1)$. Huntington compared all five with his pairwise tests.
- **Linear time.** For many states and seats, the method of Cheng and Eppstein finds a divisor in $O(n)$ time.

## When to use it

Use the Huntington-Hill method when every state must get at least one seat and the result must be free of the Alabama and population paradoxes, as for the US House. If small and large states must be treated alike on average, the Sainte-Lague method is the better choice; if a law must keep every state within its quota, use [Hamilton's method](/hamilton-method/) and accept its paradoxes.

## Pitfalls

- **Square roots in floating point.** The priorities $p/\sqrt{a(a + 1)}$ are irrational in general, and rounding errors can break or invent ties. Compare the squares $p^2/(a(a + 1))$ with integer cross products.
- **Fewer seats than states.** The method gives every state one seat first, so it needs $h \ge n$. A state with population 0 still gets a seat.
- **Not the same as rounding at one half.** Rounding at the arithmetic mean is the Sainte-Lague method. The two agree in the example, but with $h = 4$ they do not.
- **Ties.** If the last seat goes to one of two equal keys, the result depends on the tie rule. State the rule.

## Implementations

## History

Joseph A. Hill, a statistician at the Census Bureau, proposed the method in 1911. Edward V. Huntington, a mathematician at Harvard, built its theory in the 1920s: he compared the divisor methods by pairwise tests and showed that the test of relative difference gives this method. Walter Willcox argued for Webster's method of major fractions, and a committee of the National Academy of Sciences sided with Huntington in 1929. Congress adopted the method in 1941 for the census of 1940, and has used it with a House of 435 seats since then. In 1992 the US Supreme Court upheld it in United States Department of Commerce v. Montana, a case Montana brought after it lost its second seat.

## References
