---
tag: N9KT39
kind: algorithm
slug: generalized-median-voter-rule
name: Generalized median voter rule
aliases:
- Moulin phantom voters rule
- generalized median rule
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Takes the median of the reported peaks and n+1 fixed phantom points. On a single-peaked line these are exactly the anonymous strategyproof rules that use only the peaks."
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(n + m)}
  space: {extra: O(m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1980
  people: [Hervé Moulin, Kim C. Border, James S. Jordan, Duncan Black]
  note: "Black (1948) used the median of the peaks. Moulin (1980) showed that the medians with n+1 phantom peaks are the anonymous strategyproof rules on single-peaked preferences, and Border and Jordan (1983) named the extra points phantom voters."
prereqs: [single-peaked-preferences, median, dominant-strategy-incentive-compatibility]
see_also: [median-voter-theorem, gibbard-satterthwaite-theorem, facility-location-mechanism, single-peaked-recognition, pareto-optimality, counting-sort, selection-problem]
sources:
  - paper: doi:10.1007/BF00128122
    title: "Hervé Moulin, On strategy-proofness and single peakedness, Public Choice 35(4) (1980), 437-455"
    locator: "Proposition 2 (anonymous rules with n+1 phantoms) and Proposition 3 (the general min-max form)"
  - paper: doi:10.2307/2296962
    title: "Kim C. Border and James S. Jordan, Straightforward elections, unanimity and phantom voters, Review of Economic Studies 50(1) (1983), 153-170"
    locator: the characterization by phantom voters
  - paper: doi:10.1007/s13209-011-0064-5
    title: "John A. Weymark, A unified approach to strategy-proofness for single-peaked preferences, SERIEs 2(4) (2011), 529-550"
    locator: "Theorem 1 (tops-only and an interval range), Theorem 4 (Moulin's anonymous characterization) and Theorem 5 (with Pareto efficiency, n-1 phantoms)"
  - paper: doi:10.1086/256633
    title: "Duncan Black, On the rationale of group decision-making, Journal of Political Economy 56(1) (1948), 23-34"
    locator: the median optimum for single-peaked curves of preference
---

A generalized median voter rule chooses one point of a line from the peaks that the voters report. It adds a fixed list of extra points, the phantom peaks, and returns the [median](/median/) of all the points. With [single-peaked preferences](/single-peaked-preferences/) on the line, no voter can get a better outcome by reporting a false peak, for every choice of phantoms. Moulin (1980) proved the converse: with $n$ voters, the anonymous strategyproof rules that use only the peaks are exactly the medians with $n + 1$ phantoms.

## In plain words

Each voter names a favourite place on a line, for example a temperature for a shared office or a site on a road. The rule also has some fixed places of its own, set in advance and the same for every election. It puts all the named places and all the fixed places in order and takes the one in the middle. If the middle is to the left of your favourite, naming a place farther to the right does not move the middle, and naming a place to its left can only move the middle away from you. So the honest answer is always best. The fixed places let the designer choose how much the outcome leans to one side or how much a single voter can move it.

## The problem

The candidates are the points $0, 1, \ldots, m - 1$ of an axis. Each voter $i$ reports a peak $p_i$. The rule has $k$ phantom peaks $a_1, \ldots, a_k$, points of the axis fixed before the vote, with $n + k$ odd. The output is the median of the multiset $\{p_1, \ldots, p_n, a_1, \ldots, a_k\}$, the value in position $(n + k + 1)/2$ when the multiset is sorted. Moulin's rules have $k = n + 1$; the rules that are also [Pareto efficient](/pareto-optimality/) have $k = n - 1$.

Two choices give familiar rules. With $\lceil (n + 1)/2 \rceil$ phantoms at $0$ and the rest at $m - 1$, the rule is the median of the peaks for odd $n$, and on a single-peaked profile that is the [Condorcet winner](/condorcet-winner/) by the [median voter theorem](/median-voter-theorem/). With all $n + 1$ phantoms at one point $a$, the rule always returns $a$, a constant rule.

## The algorithm

```pseudo id=main
GEN-MEDIAN(p_1, ..., p_n; a_1, ..., a_k; m)        ▷ n + k odd, all values in 0, ..., m - 1
L1  cnt[x] ← 0 for x = 0, ..., m - 1
L2  for i ← 1 to n do cnt[p_i] ← cnt[p_i] + 1
L3  for j ← 1 to k do cnt[a_j] ← cnt[a_j] + 1
L4  need ← (n + k + 1) / 2; seen ← 0
L5  for x ← 0 to m - 1 do seen ← seen + cnt[x]
L6      if seen ≥ need then return x
```

Lines L1 to L3 count how many values sit at each point, as in [counting sort](/counting-sort/). Line L5 keeps the number of values at or to the left of $x$. The first point where this number reaches half of the values, rounded up, is the median, and line L6 returns it. If $m$ is much larger than $n$, the same median comes from linear-time [selection](/selection-problem/) on the $n + k$ values, without the table.

## Example

The axis has seven points $0, \ldots, 6$. Three voters report the peaks $1$, $4$ and $6$, and the rule has the four phantoms $0, 2, 2, 6$.

| values in order | position 4 of 7 | outcome |
|---|---|---|
| $0, 1, 2, 2, 4, 6, 6$ | $2$ | $2$ |

The outcome $2$ is to the left of the peaks $4$ and $6$. If the voter with peak $4$ reports $5$ or $6$, the values at or to the left of $2$ are still $0, 1, 2, 2$, and the outcome stays $2$. If it reports $0$, $1$ or $2$, the outcome can only move left, farther from $4$. The voter with peak $1$ is to the left of the outcome and has the mirror choices. The plain median of the peaks uses the phantoms $0, 0, 6, 6$ instead: the values $0, 0, 1, 4, 6, 6, 6$ give $4$, the middle peak.

## Correctness

The proof is in `proofs/correctness.md`. The median is the smallest $x$ such that at least half of the values, rounded up, are at most $x$, and lines L5 and L6 find exactly this $x$.

For strategyproofness, fix the other reports and let $x$ be the outcome with the true peak $p_i > x$. A false report $q > x$ does not change the number of values at or to the left of any $y \le x$, so the outcome stays $x$. A false report $q \le x$ only adds to these numbers, so the outcome moves to some $x' \le x$. Since the voter's ranking is single-peaked, a point farther left of the peak is worse, so $x'$ is not better than $x$. The case $p_i < x$ is the mirror image. The argument holds for any phantoms, so every rule of this form is strategyproof in the sense of [dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/).

With $n - 1$ phantoms the outcome lies between the smallest and the largest peak, and every such point is Pareto efficient on a single-peaked line. With $n + 1$ phantoms the rule is Pareto efficient if and only if there is a phantom at each end of the axis.

## Complexity

Lines L1 and L5 take $O(m)$ time, and lines L2 and L3 take $O(n + k)$ time. With $k = n + 1$ or $k = n - 1$ the total is $O(n + m)$ time in the [word RAM](/word-ram/) model, with $O(m)$ extra space for the counts. Linear selection gives $O(n)$ time and $O(n)$ space, which is better when $m$ is large or the axis is the real line.

## Properties

- **Strategyproof on the single-peaked domain**, for every choice of phantoms. On the full domain of rankings, a rule of this kind with three or more possible outcomes and no dictator can be manipulated, as the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) says it must.
- **Anonymous.** The output depends only on the multiset of peaks.
- **Peak-only.** It reads only the top of each ranking, so a voter reports one point, not a full ranking.
- **Not neutral.** The phantoms favour some points of the axis, and even the plain median treats points by their place on the axis, not by their names.
- **Unanimity.** If all voters report the same peak $p$, a rule with $n + 1$ phantoms returns $p$ moved into the interval from the smallest to the largest phantom. It returns $p$ for every $p$ exactly when there are phantoms at both ends.
- **The characterization.** On the single-peaked domain, a rule that depends only on the peaks is anonymous and strategyproof if and only if it is a median with $n + 1$ phantoms (Moulin 1980, Proposition 2; Weymark 2011, Theorem 4). It is also Pareto efficient if and only if it is a median with $n - 1$ phantoms (Weymark 2011, Theorem 5).

## Variants and improvements

- **Without anonymity.** Moulin (1980, Proposition 3) describes all strategyproof peak-only rules by a min-max formula with one parameter for each coalition of voters, $2^n$ parameters in all. The phantom medians are the anonymous case, where the parameter depends only on the size of the coalition.
- **Without the peak-only condition.** For strategyproof rules on the single-peaked domain, using only the peaks is equivalent to having an interval of the axis as the set of possible outcomes (Weymark 2011, Theorem 1).
- **Several dimensions.** Border and Jordan (1983) studied ideal points in a space of several dimensions, where the strategyproof rules that respect unanimity decompose coordinate by coordinate into one-dimensional rules of this kind.
- **Facility location.** In the [facility location mechanism](/facility-location-mechanism/) setting the agents are points on a line and the cost is distance. The median of the reports is strategyproof and minimizes the sum of the distances.

## When to use it

Use it to choose one value on an ordered scale, such as a budget level, a date, a temperature or a location on a road, when the voters can be assumed to have single-peaked preferences and honest reports matter. Use the plain median when the rule should treat both directions alike, and phantoms at chosen points when there is a default, a status quo or a bound the outcome should lean to. Check the profile with [single-peaked recognition](/single-peaked-recognition/) when the axis is not given by the problem.

## Pitfalls

- **An even number of values.** With an even total there is no single median. Moulin's rules use $n + 1$ phantoms so that the total $2n + 1$ is odd.
- **The wrong number of phantoms.** The characterization is for $n + 1$ phantoms, and the Pareto efficient case is for $n - 1$. Phantoms that leave out an end of the axis give a rule that ignores the voters even when they all agree on that end.
- **Using the mean.** The average of the peaks is not strategyproof: a voter can report an extreme peak to pull the average toward its own.
- **Preferences that are not single-peaked.** If a voter's ranking has a valley, a false peak can help, and the strategyproof guarantee is lost.

## Implementations

## History

Black (1948) observed that the median of the peaks wins every pairwise majority vote on a single-peaked profile. Moulin (1980) asked which rules make honest reports a dominant strategy on this domain, and found the medians with $n + 1$ fixed extra peaks, together with a min-max formula for the rules without anonymity. Border and Jordan (1983) gave the extra points the name phantom voters, in a study of several dimensions. Weymark (2011) gave a unified treatment of these results.

## References
