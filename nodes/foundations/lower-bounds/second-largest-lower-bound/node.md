---
tag: NE27WB
kind: theorem
slug: second-largest-lower-bound
name: Second largest lower bound
aliases:
- Kislitsyn bound
- second maximum lower bound
area: foundations/lower-bounds
level: core
summary: Finding the second largest of n elements needs n + ceil(log2 n) - 2 comparisons.
prereqs: [max-finding-lower-bound, adversary-argument, tournament-method]
see_also: [tournament-method, tournament-tree, max-finding-lower-bound, max-min-lower-bound, adversary-argument, small-order-statistics, selection-lower-bound, ford-johnson-algorithm]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the value V_2(n) = n + ceil(lg n) - 2, the proof with weights, and the history from Lewis Carroll, Schreier and Kislitsyn)
  - paper: "S. S. Kislitsyn, On the selection of the kth element of an ordered set by pairwise comparisons, Sibirskii Matematicheskii Zhurnal 5 (1964), in Russian"
    locator: pp. 557 to 564 (the first complete proof of the lower bound for the second largest)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.1, Minimum and maximum, Exercise 9.1-1 (the second smallest with n + ceil(lg n) - 2 comparisons in the worst case)
---

The second largest lower bound says that every comparison algorithm that finds the second largest of $n$ distinct items makes at least $n + \lceil \lg n \rceil - 2$ comparisons in the worst case. A [knockout tournament](/tournament-method/) followed by a short playoff among the items that lost to the winner meets the bound, so the value is exact for every $n \ge 2$. The first complete proof is due to Kislitsyn (1964). The proof here is an [adversary argument](/adversary-argument/) with weights: it forces the largest item to beat at least $\lceil \lg n \rceil$ other items, and each of those, except one, must also lose to someone else.

## Statement

**Theorem (Kislitsyn, 1964).** Let $n \ge 2$, and let $V_2(n)$ be the least number $t$ such that some deterministic comparison algorithm finds the index of the second largest of any $n$ distinct keys with at most $t$ comparisons. Then

$$V_2(n) = n + \lceil \lg n \rceil - 2.$$

The same holds for the second smallest.

## In plain words

Picture a tennis contest where the best player always wins. The runner-up of the final is often not the second best, because the second best may have met the best player in an early round. So after the contest you must also look at every player who lost to the champion.

The bound says that this extra work cannot be avoided, and that a fair bracket keeps it as small as possible. Every player except the champion must lose once. Also, every player who lost to the champion, except the true second best, must lose a second time to someone else. An opponent who decides the results can make sure the champion meets many players, because it lets the player with the larger following win each match. Then the champion's following doubles at most at each win, so the champion must win many matches.

## Proof

Fix a correct algorithm $A$. Say that an item $y$ **loses to** $z$ when $y$ and $z$ are compared and the answer is $y < z$. Each comparison has exactly one loser.

**Step 1, what must be known at the stop.** Let $x$ be an input of distinct keys, with largest key at $m$ and second largest at $s$, so $A$ outputs $s$ on $x$. Consider the run of $A$ on $x$.

*(a) Each item other than $m$ loses at least once.* Suppose $y \ne m$ never loses. Raise $x_y$ above all keys. Every comparison of the run that involves $y$ was won by $y$, and still is, and the others do not change. So $A$ makes the same comparisons, gets the same answers and outputs $s$. On the new input the largest key is at $y$ and the second largest is at $m$. Since $s \ne m$, the output is wrong.

*(b) Each item $y \notin \{m, s\}$ that loses to $m$ also loses to some item other than $m$.* Suppose that all the losses of $y$ are to $m$. Change $x_y$ to a value below $x_m$ and above all other keys. Each comparison of $y$ with $m$ still gives $y < m$, each other comparison of $y$ was won by $y$ and still is, and the others do not change. So $A$ again outputs $s$, but now the second largest key is at $y \ne s$. The output is wrong.

*(c) The count.* Let $k$ be the number of different items that lose to $m$ in the run. By (a) there are at least $n - 1$ losses, one for each item other than $m$. By (b), each of the $k$ items that lose to $m$, other than $s$, has at least two losses: one to $m$ and one to another item. So there are at least $k - 1$ further losses. Since each comparison gives one loss,

$$\text{number of comparisons on } x \ \ge\ (n - 1) + (k - 1) = n + k - 2.$$

**Step 2, the adversary forces $k \ge \lceil \lg n \rceil$.** The adversary keeps a value for each item, all values distinct, and a weight $w(y) \ge 0$ for each item. At the start every weight is 1. Call an item **undefeated** if it has not lost yet. The adversary keeps this invariant: the weight of a defeated item is 0, and the weights sum to $n$. When the algorithm compares $a$ with $b$:

1. Both undefeated: the one with the larger weight wins (either one if the weights are equal). The adversary raises the winner above all values. The winner takes the weight of the loser: $w(\text{winner}) \leftarrow w(a) + w(b)$, $w(\text{loser}) \leftarrow 0$.
2. One undefeated, one defeated: the undefeated item wins. The adversary raises it above all values. No weight changes.
3. Both defeated: the adversary answers by the current values. No weight changes.

Raising an undefeated item keeps all earlier answers true, because that item has won each of its comparisons. So at each step, the current values form an input of distinct keys that agrees with all answers. The invariant holds after each step, because only rule 1 makes an item defeated, and it moves the whole weight of the loser to the winner.

In rule 1 the winner has the larger weight, so its new weight is at most twice its old weight. Rules 2 and 3 do not change weights. So the weight of an item at most doubles each time it beats an undefeated item, and does not change otherwise.

Now let the algorithm stop, and let $x$ be the current values, with largest key at $m$. By Step 1(a) applied to $x$, every item other than $m$ has lost, so $m$ is the only undefeated item, and by the invariant $w(m) = n$. The weight of $m$ started at 1 and at most doubled each time $m$ beat an undefeated item. So $m$ beat at least $\lceil \lg n \rceil$ undefeated items. Each of these is a different item, since an item is undefeated only until its first loss. So $k \ge \lceil \lg n \rceil$, and Step 1(c) gives at least $n + \lceil \lg n \rceil - 2$ comparisons. So $V_2(n) \ge n + \lceil \lg n \rceil - 2$.

**Step 3, the upper bound.** Run a knockout tournament on a balanced bracket: pair the items, let the larger of each pair go on, and repeat. This makes $n - 1$ comparisons, since each comparison removes one item, and finds the maximum $m$. In a balanced bracket each item plays at most $\lceil \lg n \rceil$ rounds, so $m$ beat at most $\lceil \lg n \rceil$ items. The second largest key can lose only to $m$, so it is among the items that lost to $m$, and it is their maximum. Finding the maximum of at most $\lceil \lg n \rceil$ items takes at most $\lceil \lg n \rceil - 1$ comparisons. The total is at most $n + \lceil \lg n \rceil - 2$. ∎

```pseudo id=tournament
SECOND-LARGEST(x[1..n])                    ▷ n ≥ 2
L1  C ← list of (index i, beaten list B_i = empty) for i ← 1 to n
L2  while C has more than one entry do
L3      C' ← empty list
L4      for each consecutive pair (a, B_a), (b, B_b) in C do
L5          if x[a] > x[b] then append (a, B_a + [b]) to C' else append (b, B_b + [a]) to C'
L6      if C has an odd number of entries then append its last entry to C'
L7      C ← C'
L8  (m, B) ← the only entry of C
L9  return the index of the largest x[j] with j in B      ▷ |B| − 1 comparisons
```

## Consequences

- **The cost of the runner-up is logarithmic.** After the maximum, the second largest costs only $\lceil \lg n \rceil - 1$ more comparisons, against $n - 2$ for a second scan.
- **The tournament keeps its information.** The bracket remembers who lost to whom, which a scan forgets. The same idea, used again, gives [tournament sort](/tournament-tree/) and the selection of the $t$ largest items with about $n + (t - 1) \lceil \lg n \rceil$ comparisons. See [small order statistics](/small-order-statistics/).
- **Bounds for larger ranks.** For the $t$-th largest with $t \ge 3$, exact values are not known for all $n$, and lower bounds use refinements of the same adversary. See the [selection lower bound](/selection-lower-bound/).

| $n$ | $\lceil \lg n \rceil$ | $V_2(n) = n + \lceil \lg n \rceil - 2$ | two scans $2n - 3$ |
|---|---|---|---|
| 2 | 1 | 1 | 1 |
| 3 | 2 | 3 | 3 |
| 4 | 2 | 4 | 5 |
| 5 | 3 | 6 | 7 |
| 8 | 3 | 9 | 13 |
| 10 | 4 | 12 | 17 |
| 16 | 4 | 18 | 29 |
| 100 | 7 | 105 | 197 |
| 1000 | 10 | 1008 | 1997 |
| $10^6$ | 20 | 1000018 | 1999997 |

## Tightness

The bound is exact for every $n \ge 2$, by the tournament. The adversary also shows that every optimal algorithm must make the maximum beat at least $\lceil \lg n \rceil$ items on a hard input, so a bracket that is far from balanced, such as a scan, is not optimal: the scan lets the final maximum beat up to $n - 1$ items.

The bound is for the worst case. On some inputs a correct algorithm finishes with fewer comparisons, for example a scan in which the first item is the largest and the second item is the second largest.

### Pitfalls

- **The runner-up of the final is not the answer.** In a bracket, the item that loses the final is the second largest only if the second largest did not meet the maximum earlier.
- **A bracket that is not balanced.** If the maximum plays more than $\lceil \lg n \rceil$ matches, the playoff costs more. With $n$ not a power of 2, the byes must be placed so that no item plays more than $\lceil \lg n \rceil$ rounds. Pairing consecutive entries and carrying the odd one up, as in the code, does this.
- **The adversary weights must move to the winner.** If the adversary lets the lighter item win, the weight of the winner can grow more than twice in one step, and the doubling argument fails.
- **Counting by leaves is weak.** There are $n$ possible outputs, so the [information-theoretic bound](/information-theoretic-bound/) gives only $\lceil \lg n \rceil$.
- **Storage.** The tournament keeps, for each remaining item, the list of items it beat. The lists have total length $n - 1$, so the extra memory is $\Theta(n)$, against $O(1)$ for a scan.

## History

Knuth, Volume 3, Section 5.3.3, tells the history. Lewis Carroll wrote in 1883 about the unfairness of tennis tournaments, where the second best player may lose early to the best. J. Schreier (1932) gave the method that uses $n + \lceil \lg n \rceil - 2$ comparisons and an argument for the lower bound that was not complete. S. S. Kislitsyn (1964) gave the first complete proof that the bound is exact. The proof with weights given here follows the presentation in Knuth. CLRS, Exercise 9.1-1, asks for the upper bound.

## References
