---
tag: 6DCHX4
kind: problem
slug: egg-dropping-problem
name: Egg dropping problem
aliases:
- Egg drop puzzle
area: techniques/dynamic-programming
level: intro
summary: Find the minimum number of drops needed to locate the critical floor with a limited number of eggs.
prereqs: [binary-search, binomial-coefficient, optimal-substructure]
see_also: [search-decision-tree, binary-search-on-answer, pascal-triangle-dp, memoization, tabulation, adversary-argument]
sources:
  - paper: doi:10.1080/0025570X.2004.11953281
    title: Michael Boardman, The egg-drop numbers, Mathematics Magazine 77(5), 2004
    locator: pp. 368 to 372
  - paper: doi:10.1287/ited.4.1.48
    title: Moshe Sniedovich, OR/MS Games 4, The joy of egg-dropping in Braunschweig and Hong Kong, INFORMS Transactions on Education 4(1), 2003
    locator: pp. 48 to 64
---

The egg dropping problem asks for the least number of drops that always suffices to find the highest safe floor of a building with $f$ floors, when you have $e$ identical eggs and an egg that breaks cannot be used again. With one egg the only safe method is to try the floors in order, and with unlimited eggs [binary search](/binary-search/) is optimal; the problem is the range between. The answer is the least $d$ with $\sum_{i=1}^{e} \binom{d}{i} \ge f$, which a dynamic program over eggs and floors, or a faster program over eggs and drops, computes. For two eggs and 100 floors the answer is 14.

## In plain words

You want to know the highest floor of a tall building from which an egg can fall without breaking. You have only a few eggs. An egg that survives can be used again, but a broken egg is gone. You want a plan that needs as few drops as possible in the worst case.

With one egg you must start at floor one and go up one floor at a time, because if the egg breaks you can try no more. With many eggs you can halve the range each time. With two eggs the clever plan drops the first egg from floors that are farther apart at the start and closer together later, so that the total work is the same whichever floor breaks it. Thinking about how many floors a plan can handle, rather than how many drops a building needs, gives a simple formula.

## Definition

**Model.** The floors are $1, \ldots, f$. There is an unknown *threshold* $s \in \{0, 1, \ldots, f\}$: an egg dropped from floor $x$ breaks if $x > s$ and survives if $x \le s$. All eggs behave the same, and a surviving egg is not weakened. A *strategy* chooses the next floor from the results so far. It *solves* the instance when, for every $s$, it names $s$ correctly without dropping an egg when none are left.

**Output.** $W(e, f)$, the least number $d$ such that some strategy with $e$ eggs solves $f$ floors with at most $d$ drops for every $s$. A strategy that attains it is the search version.

**The recurrence on floors.** $W(e, 0) = 0$, $W(1, f) = f$, and for $e \ge 2$ and $f \ge 1$
$$W(e, f) = 1 + \min_{1 \le k \le f} \max\bigl( W(e - 1, k - 1),\; W(e, f - k) \bigr).$$
If the first drop is from floor $k$ and the egg breaks, then $s \in \{0, \ldots, k-1\}$, which is a building of $k - 1$ floors with $e - 1$ eggs. If it survives, $s \in \{k, \ldots, f\}$, which is a building of $f - k$ floors (floors $k + 1$ to $f$) with $e$ eggs. The adversary picks the worse branch, and the strategy picks the best $k$. With one egg, a drop that breaks the egg ends the search, so a correct strategy must test the floors $1, 2, \ldots$ in order, and $s = f$ needs all $f$ drops.

**The dual: floors covered by $d$ drops.** Let $F(d, e)$ be the largest $f$ that $e$ eggs and $d$ drops can solve. Then $F(0, e) = F(d, 0) = 0$ and, for $d, e \ge 1$,
$$F(d, e) = F(d - 1, e - 1) + 1 + F(d - 1, e).$$

*Proof.* Use induction on $d$. Suppose a strategy solves $f$ floors with $d$ drops and $e$ eggs, and its first drop is from floor $k$. After a break, it solves $k - 1$ floors with $d - 1$ drops and $e - 1$ eggs, so $k - 1 \le F(d-1, e-1)$. After a survival, it solves $f - k$ floors with $d - 1$ drops and $e$ eggs, so $f - k \le F(d-1, e)$. Adding gives $f \le F(d-1, e-1) + 1 + F(d-1, e)$. Conversely, drop first from floor $k = F(d-1, e-1) + 1$; on a break use the strategy for $F(d-1, e-1)$ floors below, and on a survival use the strategy for $F(d-1, e)$ floors above. This solves exactly $F(d-1,e-1) + 1 + F(d-1,e)$ floors. With $e = 0$ no drop is allowed, and with $d = 0$ no drop is made, so only the building with 0 floors is solved. ∎

**Closed form.** For $d, e \ge 0$,
$$F(d, e) = \sum_{i=1}^{e} \binom{d}{i}.$$

*Proof.* Both sides are 0 when $d = 0$ or $e = 0$. For $d, e \ge 1$, by induction and $\binom{d-1}{0} = 1$,
$$F(d-1, e-1) + 1 + F(d-1, e) = \sum_{i=1}^{e-1} \binom{d-1}{i} + \binom{d-1}{0} + \sum_{i=1}^{e} \binom{d-1}{i} = \sum_{i=1}^{e} \left[ \binom{d-1}{i-1} + \binom{d-1}{i} \right] = \sum_{i=1}^{e} \binom{d}{i}$$
by Pascal's rule. ∎

Since $F(d, e)$ increases with $d$, and a strategy for $f$ floors also solves fewer floors, $W(e, f) = \min\{ d \ge 0 : F(d, e) \ge f \}$. Boardman calls the values $F(d, e)$ the egg-drop numbers and derives the same sum of [binomial coefficients](/binomial-coefficient/).

## Variants

- **Two eggs.** $F(d, 2) = d(d+1)/2$, so $W(2, f) = \lceil (\sqrt{8f + 1} - 1)/2 \rceil$, about $\sqrt{2f}$.
- **Many eggs.** If $e \ge d$ then $F(d, e) = 2^d - 1$. So with $e \ge \lceil \lg(f + 1) \rceil$ eggs the answer is $\lceil \lg(f + 1) \rceil$, the cost of binary search.
- **Average case.** Put a probability on $s$ and minimize the expected number of drops. The recurrence keeps its shape with a weighted sum in place of the max.
- **Costly breaks.** Give a broken egg a price and minimize the total of drops and eggs. This is a weighted version of the same decision tree.
- **Counting form.** Given $d$ drops and $e$ eggs, find the tallest building, which is $F(d, e)$ itself.

## Examples

**Values of $W(e, f)$.**

| $e$ \ $f$ | 1 | 2 | 3 | 4 | 6 | 10 | 36 | 100 | 1000 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 2 | 3 | 4 | 6 | 10 | 36 | 100 | 1000 |
| 2 | 1 | 2 | 2 | 3 | 3 | 4 | 8 | 14 | 45 |
| 3 | 1 | 2 | 2 | 3 | 3 | 4 | 6 | 9 | 19 |
| 4 | 1 | 2 | 2 | 3 | 3 | 4 | 6 | 8 | 13 |

With 7 eggs, 100 floors need 7 drops, and with 10 eggs, 1000 floors need 10 drops: these are the binary search values $\lceil \lg 101 \rceil$ and $\lceil \lg 1001 \rceil$.

**Two eggs, 100 floors.** $F(13, 2) = 91 < 100 \le 105 = F(14, 2)$, so $W(2, 100) = 14$. A plan that meets the bound drops the first egg from floors 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100, with gaps $14, 13, 12, \ldots$. If the first egg breaks at its $j$-th drop, the second egg tests the at most $14 - j$ floors of the last gap one by one, from the bottom, so the total is at most 14.

**Three eggs, 100 floors.** $F(8, 3) = 8 + 28 + 56 = 92 < 100 \le 129 = F(9, 3)$, so $W(3, 100) = 9$.

**A table of $F(d, e)$.** Each entry is the one above it plus the one above and to the left, plus 1.

| $d$ \ $e$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 3 | 3 | 3 |
| 3 | 3 | 6 | 7 | 7 |
| 4 | 4 | 10 | 14 | 15 |
| 5 | 5 | 15 | 25 | 30 |
| 6 | 6 | 21 | 41 | 56 |
| 7 | 7 | 28 | 63 | 98 |

## Known algorithms

- **DP over eggs and floors.** Fill $W(e', f')$ for $e' \le e$ and $f' \le f$ with the recurrence on floors: $O(e f^2)$ time and $O(f)$ space per egg row.
- **The same DP with binary search on $k$.** $W(e - 1, k - 1)$ does not decrease in $k$ and $W(e, f - k)$ does not increase, so the minimum of their max is at the crossing point, which binary search finds. Time $O(e f \log f)$.
- **DP over drops and eggs.** Fill $F(d, e')$ row by row in $d$ until $F(d, e) \ge f$. This takes $O(e \cdot W(e, f))$ time, and $W(e, f) \le f$.
- **Binary search on the answer.** Compute $\sum_{i=1}^{e} \binom{d}{i}$ in $O(e)$ arithmetic operations, stopping early once the sum reaches $f$, and [binary search](/binary-search-on-answer/) on $d$ in $[0, f]$. Time $O(e \log f)$ arithmetic operations on numbers of $O(\log f)$ bits.
- **Two eggs.** The closed form above in $O(1)$ arithmetic operations with an integer square root.

The search version follows from any of them: the first drop is from floor $F(d - 1, e - 1) + 1$ with $d = W(e, f)$, as in the proof of the dual recurrence.

## Bounds

- **Exact value.** $W(e, f) = \min\{ d : \sum_{i=1}^{e} \binom{d}{i} \ge f \}$, so the bounds are tight for every $e$ and $f$.
- **Information bound.** The strategy must tell apart $f + 1$ thresholds, and each drop has two outcomes, so $W(e, f) \ge \lceil \lg(f + 1) \rceil$ for every $e$. Equality holds when $e \ge \lceil \lg(f+1) \rceil$.
- **Growth for fixed $e$.** For $d \ge 2e$ the terms $\binom{d}{i}$ increase with $i$ for $i \le e$, so $(d/e)^e \le \binom{d}{e} \le F(d, e) \le e \binom{d}{e} \le e\, d^e / e!$. So $F(d, e) = \Theta(d^e)$, and $W(e, f) = \Theta(f^{1/e})$ as $f \to \infty$ with $e$ fixed.

## Reductions

- **A decision tree with a budget of breaks.** A strategy is a binary [search decision tree](/search-decision-tree/) whose leaves are the $f + 1$ thresholds, in which each root-to-leaf path takes the "break" branch at most $e$ times. A tree of depth $d$ has at most as many leaves as words of length $d$ with at most $e$ breaks, which is $\sum_{i=0}^{e} \binom{d}{i} = F(d, e) + 1$. This gives a second proof of the upper bound on $F$.
- **Search with costly overshoots.** Searching a sorted range where each probe that lands above the target uses up a resource is the same problem, with eggs as the resource.

## Applications

- **Destructive testing.** Finding the load, height or voltage at which a part fails, when each failure destroys a sample and samples are few. The thresholds must be ordered and the outcome must be monotone in the test level, as in the model.
- **Teaching dynamic programming.** The problem shows two different subproblem spaces for the same question: one indexed by floors, one by drops. The second is much smaller, a lesson in choosing the subproblems.
- **Interview puzzle.** The two-egg, 100-floor version is a well-known puzzle; its answer is 14.

## References
