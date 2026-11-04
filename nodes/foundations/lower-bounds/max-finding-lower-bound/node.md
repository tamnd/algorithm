---
tag: GBTMKG
kind: theorem
slug: max-finding-lower-bound
name: Maximum finding lower bound
aliases:
- n-1 comparisons for maximum
- finding the maximum lower bound
area: foundations/lower-bounds
level: intro
summary: Finding the maximum of n elements by comparisons needs exactly n-1 comparisons.
prereqs: [comparison-model, decision-tree-model, lower-bound]
see_also: [find-maximum, adversary-argument, decision-tree-method, max-min-lower-bound, second-largest-lower-bound, tournament-method, trivial-lower-bound, durr-hoyer-minimum-finding]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.1, Minimum and maximum (n - 1 comparisons are necessary and sufficient, by the argument that each element except the winner must lose a match)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the maximum needs n - 1 comparisons, and the tournament view)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, Analysis of an algorithm (Algorithm M, find the maximum, and the number of times the current maximum changes)
---

The maximum finding lower bound says that every algorithm that finds the largest of $n$ distinct items by comparing pairs of them makes at least $n - 1$ comparisons, and makes them on every input, not only on a bad one. A single scan makes exactly $n - 1$ comparisons, so the value is $n - 1$ exactly. The proof is a short [adversary argument](/adversary-argument/): each item other than the answer must lose at least one comparison, and each comparison has one loser. It is the simplest case where a path argument in the [decision tree model](/decision-tree-model/) beats the [information-theoretic bound](/information-theoretic-bound/), which gives only $\lceil \lg n \rceil$.

## Statement

**Theorem.** Let $n \ge 1$. In the [comparison model](/comparison-model/), let $A$ be a deterministic algorithm that, on each input $x_1, \dots, x_n$ of distinct keys, outputs the index of the largest key. Then on each input of distinct keys, $A$ makes at least $n - 1$ comparisons. The scan that keeps the largest key seen so far makes exactly $n - 1$ comparisons on every input. So the least worst-case number of comparisons is $M(n) = n - 1$, and the least average number over any distribution on inputs is also $n - 1$.

The same holds for the minimum, with "larger" and "smaller" swapped.

## In plain words

Think of a knockout contest where each match has a winner and a loser. To be sure who is the best player, every other player must have lost a match. If one player never lost, that player could be the best, and nothing seen so far rules it out. Each match makes only one player lose, so with many players you need one match fewer than the number of players.

The bound holds for each run, not only for the worst one. There is no lucky input that lets a method finish early. Going through the items once and keeping the best one seen so far meets the bound.

## Proof

Fix an input $x = (x_1, \dots, x_n)$ of distinct keys. Run $A$ on $x$, and let $m$ be its output, so $x_m$ is the largest key. Say that an item $y$ **loses** a comparison when the comparison is between $y$ and another item $z$, and the answer is $y < z$.

**Claim 1.** Each item $y \ne m$ loses at least one comparison in the run of $A$ on $x$.

*Proof.* Suppose that some $y \ne m$ loses no comparison in the run. Let $x'$ be the input that equals $x$ except that $x'_y = 1 + \max_i x_i$. The keys of $x'$ are distinct, and $y$ is the only largest key of $x'$.

Run $A$ on $x'$. By induction on the number of comparisons, the run makes the same comparisons as on $x$ and gets the same answers. Assume this is true for the first $t$ comparisons. Then $A$ has seen the same answers, so its next comparison is the same pair, or it stops in both runs. If that pair does not contain $y$, both keys are equal in $x$ and $x'$, so the answer is the same. If the pair is $y$ and $z$, then on $x$ the answer was $y > z$, because $y$ never lost. On $x'$, $x'_y$ is larger than every key, so the answer is again $y > z$.

So the run on $x'$ ends at the same point with the same output $m$. But the largest key of $x'$ is at $y \ne m$, so $A$ is wrong on $x'$. This contradicts the correctness of $A$. ∎

**Claim 2.** A comparison makes at most one item lose.

*Proof.* A comparison involves two items and has one answer, so at most one of the two items loses it. ∎

There are $n - 1$ items other than $m$. By Claim 1 each of them loses at least once, and by Claim 2 each comparison gives at most one loss. So the run on $x$ makes at least $n - 1$ comparisons. Since $x$ was any input of distinct keys, the bound holds on every such input, and so for the average over any distribution on them. ∎

**Upper bound.** The scan compares $x_2, x_3, \dots, x_n$ in turn with the largest key seen so far and keeps the larger one.

```pseudo id=scan
MAX-INDEX(x[1..n])
L1  m ← 1
L2  for i ← 2 to n do
L3      if x[i] > x[m] then
L4          m ← i
L5  return m
```

Line L3 runs $n - 1$ times on every input, and each other line makes no comparison. After the step for $i$, $x[m]$ is the largest of $x[1..i]$, by induction on $i$. So the scan is correct and makes exactly $n - 1$ comparisons.

## Consequences

- **Randomness does not help.** A randomized comparison algorithm is a distribution over deterministic ones, and each of them makes at least $n - 1$ comparisons on each input. So its expected number of comparisons on each input is at least $n - 1$. For most problems the randomized bound needs the [Yao minimax principle](/yao-minimax-principle/), but not here.
- **The shape of every optimal algorithm.** For each comparison, draw an edge from the loser to the winner when the loser loses for the first time. An algorithm that makes exactly $n - 1$ comparisons has each comparison give a first loss, so these edges form a tree on all $n$ items, rooted at the maximum. The scan gives a path, and a [knockout tournament](/tournament-method/) gives a balanced tree. Both are optimal.
- **Other problems.** Each algorithm that sorts, finds the median, or finds both the maximum and the minimum also identifies the maximum, so each needs at least $n - 1$ comparisons. For the [maximum and minimum](/max-min-lower-bound/) the true value is $\lceil 3n/2 \rceil - 2$, and for the [second largest](/second-largest-lower-bound/) it is $n + \lceil \lg n \rceil - 2$. Both proofs extend the idea of counting losses.
- **The size of the gap to counting.** Leaf counting gives $\lceil \lg n \rceil$, since there are $n$ possible answers.

| $n$ | counting bound $\lceil \lg n \rceil$ | true value $n - 1$ |
|---|---|---|
| 2 | 1 | 1 |
| 4 | 2 | 3 |
| 8 | 3 | 7 |
| 16 | 4 | 15 |
| 100 | 7 | 99 |
| 1000 | 10 | 999 |
| $10^6$ | 20 | 999999 |

## Tightness

The bound is exact for every $n$ and on every input, because the scan meets it on every input. It is also exact for many other algorithms, for example the knockout tournament, which makes $n - 1$ comparisons in $\lceil \lg n \rceil$ rounds of comparisons that can run at the same time.

The bound depends on the model.

- **Quantum queries.** A quantum algorithm with access to comparisons finds the maximum with bounded error using $O(\sqrt{n})$ queries, and $\Omega(\sqrt{n})$ is necessary. See [Dürr and Høyer minimum finding](/durr-hoyer-minimum-finding/).
- **Errors allowed.** An algorithm that may answer a key near the maximum, or be wrong with some probability, is not covered.
- **Data with structure.** If the input is a max-heap, or is sorted, the maximum is read in one step. The theorem is about inputs with no promise on the order.

### Pitfalls

- **"Each item must be compared" is too weak.** That argument gives only $\lceil n/2 \rceil$ comparisons, since one comparison touches two items. The right count is of losses, one per comparison.
- **Equal keys.** The theorem is stated for distinct keys. When equal keys are allowed, the inputs of distinct keys are still possible inputs, so the worst case is still at least $n - 1$. The claim "on every input" is then only for the inputs of distinct keys: on an input where all keys are equal, an algorithm with three-way comparisons can still need $n - 1$ comparisons, but the proof above does not show it.
- **Comparisons are not the whole cost.** On a computer the scan also moves data. The number of times the current maximum changes is between 0 and $n - 1$, and is $H_n - 1$ on average over random orders, where $H_n$ is the $n$th harmonic number (Knuth, Volume 1, Section 1.2.10). The theorem counts only comparisons.
- **The worst case and the average are the same here.** For most problems an average-case bound needs a separate argument. Here the bound holds on each input, which gives the average for free. Do not expect this for sorting or search.

## History

The bound is stated and proved by the count of losses in Knuth, Volume 3, Section 5.3.3, and in CLRS, Section 9.1, which both present it as the base case of minimum-comparison selection. Knuth, Volume 1, Section 1.2.10, uses the scan for the maximum (Algorithm M) as the first example of the analysis of an algorithm. The loss argument is the model for the stronger adversary proofs for the [maximum and minimum](/max-min-lower-bound/) and for the [second largest](/second-largest-lower-bound/).

## References
