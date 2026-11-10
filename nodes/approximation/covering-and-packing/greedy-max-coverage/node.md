---
tag: CJWJGV
kind: algorithm
slug: greedy-max-coverage
name: Greedy maximum coverage algorithm
aliases:
- greedy k-coverage
- greedy algorithm for maximum coverage
area: approximation/covering-and-packing
level: intro
summary: Pick k times the set that covers the most new elements; the k sets cover at least 1 − (1 − 1/k)^k > 1 − 1/e of the optimum, and no polynomial-time algorithm does better unless P = NP.
solves: [max-coverage]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of sets, s: the total size of all sets, k: the number of sets to choose}
  time: {worst: O(k(m + s))}
  space: {extra: O(n + k)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1978
  people: [Marshall L. Fisher, George L. Nemhauser, Laurence A. Wolsey, Gérard Cornuéjols]
  note: The bound 1 − (1 − 1/k)^k for greedy on coverage and on monotone submodular functions dates from Cornuéjols, Fisher and Nemhauser (1977) and Nemhauser, Wolsey and Fisher (1978); Feige (1998) proved that it is the best possible.
prereqs: [max-coverage, greedy-algorithm, submodular-function]
see_also: [nemhauser-wolsey-fisher-theorem, greedy-set-cover, max-coverage-inapproximability, submodular-function, greedy-influence-maximization, pipage-rounding]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.5 (maximizing float in bank accounts, the greedy 1 − 1/e analysis)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 2, the exercises on maximum coverage
  - paper: doi:10.1007/BF01588971
    title: George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14(1), 1978
    locator: pages 265 to 294
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: pages 634 to 652 (1 − 1/e + ε is NP-hard for maximum coverage)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 3 (approximating covering and packing problems, the maximum coverage section)
---

The greedy algorithm for [maximum coverage](/max-coverage/) chooses $k$ sets one at a time, each time the set that covers the most elements not yet covered. The $k$ sets cover at least $1 - (1 - 1/k)^k$ of the best possible number, and this is more than $1 - 1/e \approx 0.632$. The ratio is tight for the algorithm, and Feige (1998) showed that no polynomial-time algorithm has a better ratio unless P = NP. The same proof works for each monotone [submodular function](/submodular-function/); that general form is the [Nemhauser-Wolsey-Fisher theorem](/nemhauser-wolsey-fisher-theorem/).

## In plain words

You may buy only a fixed number of groups, and you want to cover as many items as possible. At each step, buy the group that adds the most items that you do not have yet.

The best choice covers some number of items. While you are short of it, the missing items of the best choice are spread over its few groups, so one of these groups adds at least an equal share of what is missing. Your pick adds at least as much. So each step closes a fixed part of the gap, and after all steps the gap is less than about 37 percent of the best value.

## The problem

The input is a family of sets $S_1, \ldots, S_m$ over a universe of $n$ elements, and an integer $k \ge 1$. The output is a list $C$ of at most $k$ indices. The goal is a large number of covered elements, $\text{ALG} = |\bigcup_{j \in C} S_j|$. OPT is the largest value over all choices of $k$ sets, and the ratio convention is ALG $\ge \alpha \cdot$ OPT, with $\alpha \le 1$.

## The algorithm

```pseudo id=main
GREEDY-MAX-COVERAGE(S[1 .. m], k)
L1  R ← ∅, C ← empty list                       ▷ R holds the covered elements
L2  repeat k times
L3      choose j that maximizes |S[j] \ R|
L4      if |S[j] \ R| = 0 then stop the loop
L5      append j to C, R ← R ∪ S[j]
L6  return C, R
```

Line L3 picks the set with the largest gain, the number of new elements it adds. Ties may be broken in any way; the implementation takes the smallest index. Line L4 stops when no set adds anything; then each set is already inside $R$, and $R$ is the best possible.

## Example

The instance has four sets and $k = 3$.

| set | elements |
|---|---|
| $S_1$ | 1, 2, 3, 4 |
| $S_2$ | 5, 6, 7, 8 |
| $S_3$ | 2, 3, 6, 7, 9 |
| $S_4$ | 10, 11, 12 |

The table shows the gain $|S_j \setminus R|$ of each set in each round.

| round | $\lvert R \rvert$ before | $S_1$ | $S_2$ | $S_3$ | $S_4$ | pick |
|---|---|---|---|---|---|---|
| 1 | 0 | 4 | 4 | 5 | 3 | $S_3$ |
| 2 | 5 | 2 | 2 | 0 | 3 | $S_4$ |
| 3 | 8 | 2 | 2 | 0 | 0 | $S_1$ |

Greedy covers $5 + 3 + 2 = 10$ elements. The optimum is $\{S_1, S_2, S_4\}$, with OPT $= 11$. The bound promises at least $1 - (2/3)^3 = 19/27$ of 11, which is about 7.7, and greedy gets $10/11$. The first pick $S_3$ is the largest set, but it overlaps both $S_1$ and $S_2$, and this costs one element. With $k = 2$, greedy picks $S_3$ and $S_4$ and covers 8, which is optimal.

## Correctness

The output has at most $k$ sets, because the loop runs at most $k$ times. For the bound, let $c_i$ be the number of elements covered after $i$ picks. The sets of an optimal solution cover OPT elements, so at least $\text{OPT} - c_i$ of these are still uncovered. They lie in at most $k$ sets, so one of these sets has gain at least $(\text{OPT} - c_i)/k$, and greedy gains at least as much. This gives the step inequality

$$\text{OPT} - c_{i+1} \le \left(1 - \frac{1}{k}\right)(\text{OPT} - c_i).$$

**Theorem.** GREEDY-MAX-COVERAGE returns at most $k$ sets with ALG $\ge (1 - (1 - 1/k)^k)\,\text{OPT} \ge (1 - 1/e)\,\text{OPT}$, in the worst case.

Apply the step inequality $k$ times from $c_0 = 0$ to get $\text{OPT} - c_k \le (1 - 1/k)^k\,\text{OPT} \le \text{OPT}/e$. If the loop stops early, all sets are already covered, so ALG $\ge$ OPT. The full proof is in the proof file below.

**The upper bound used.** The analysis compares greedy with OPT itself, through the gains of the sets of an optimal solution. It does not use an LP.

**Tight example.** The ratio $1 - (1 - 1/k)^k$ is tight for each $k$. Take $k$ rows of $k^k$ elements each; the $k$ rows are $k$ sets, so OPT $= k \cdot k^k$, all elements. Split the columns into $k + 1$ blocks: block $i \le k$ has $a_i = k^{k-i}(k-1)^{i-1}$ columns, and the last block has the remaining $(k-1)^k$ columns. Add a set $G_i$ for each of the first $k$ blocks, with all elements of its columns. Before round $i$, each row has $k \cdot a_i$ uncovered elements, and $G_i$ also has $k \cdot a_i$ uncovered elements, so there is a tie. If ties go to $G_i$, greedy takes $G_1, \ldots, G_k$ and leaves the last block uncovered. The ratio is $1 - (k-1)^k / k^k = 1 - (1 - 1/k)^k$ exactly. For $k = 2$, rows of 4 elements, it is $6/8 = 3/4$.

**Hardness.** For each $\varepsilon > 0$, a $(1 - 1/e + \varepsilon)$-approximation for maximum coverage is NP-hard (Feige 1998). So greedy is optimal among polynomial-time algorithms, up to $\varepsilon$; see [max coverage inapproximability](/max-coverage-inapproximability/).

## Complexity

Let $s = \sum_j |S_j|$ be the total size of the input.

- **Time.** Each round computes the gain of each set in $O(|S_j|)$ time with a hash set or a flag array for $R$, so a round costs $O(m + s)$. With $k$ rounds, the total is $O(k(m + s))$ in the worst case, in the [word RAM](/word-ram/).
- **Faster.** Keep the gains in a max-heap. When an element is covered, lower the gain of each set that contains it. All updates together cost $O(s \log m)$, so the time is $O((s + k) \log m + n)$.
- **Space.** The covered set and the output take $O(n + k)$ extra space. The faster version needs $\Theta(n + m + s)$ for the lists of sets of each element.

## Properties

- **Deterministic.** With a fixed tie rule, the output depends only on the input.
- **A prefix property.** The first $i$ picks of greedy for $k$ are the picks of greedy for $i$, so one run gives a solution for each budget up to $k$, and each prefix meets the bound for its own budget.
- **Ratio depends only on $k$.** The bound $1 - (1 - 1/k)^k$ is 1 for $k = 1$, $3/4$ for $k = 2$, $19/27$ for $k = 3$, and falls toward $1 - 1/e$ as $k$ grows.
- **Any tie rule.** The bound holds for each tie rule in line L3.

## Variants and improvements

- **Weighted elements.** Give each element a weight and pick the set with the largest new weight. The same proof gives the same bound.
- **Monotone submodular functions.** Replace the coverage count by any monotone submodular function $F$. Greedy has the same ratio; this is the [Nemhauser-Wolsey-Fisher theorem](/nemhauser-wolsey-fisher-theorem/). [Influence maximization](/greedy-influence-maximization/) is a well-known use.
- **Lazy greedy.** A gain never grows as $R$ grows, so the gains from earlier rounds are upper bounds. Keep them in a heap and recompute only the top. This is often much faster in practice.
- **Set costs and a budget.** When sets have costs and the total cost is bounded, pick by gain per cost and compare with the best single set; with partial enumeration of the first three sets, the ratio is again $1 - 1/e$ (Khuller, Moss and Naor 1999).
- **Bounded frequency.** When each element is in at most $f$ sets, LP rounding with [pipage rounding](/pipage-rounding/) gives the better ratio $1 - (1 - 1/f)^f$ (Ageev and Sviridenko 2004), for example $3/4$ when $f = 2$.
- **Set cover.** Run greedy until all elements are covered. This is the [greedy set cover algorithm](/greedy-set-cover/), and its analysis with unit costs uses the same step inequality.

## When to use it

Use greedy for maximum coverage and for most monotone submodular objectives with a limit on the number of picks: sensor placement, facility siting by coverage, document summaries, and seed selection in networks. Its ratio is the best possible in polynomial time, it is simple, and its prefix property gives answers for all budgets at once. For small instances, integer programming finds OPT. When the sets have costs, use the budgeted variant, because plain greedy by gain can spend the whole budget on one large set.

## Pitfalls

- **Gain against size.** Line L3 must use the new elements $|S_j \setminus R|$, not the size $|S_j|$. Picking by size can choose $k$ copies of nearly the same set.
- **The same set twice.** A chosen set has gain 0, so it is not chosen again, but code that uses $|S_j|$ or that skips line L4 can append it again and waste picks.
- **Reading the bound as $1 - 1/e$ for small $k$.** For small $k$ the guarantee is stronger: $3/4$ for $k = 2$. The value $1 - 1/e$ is the limit.
- **Costs without the fix.** With set costs and a budget, greedy by gain per cost alone has no constant ratio. Also compare with the best single set that fits.

## Implementations

## History

Cornuéjols, Fisher and Nemhauser (1977) analysed greedy for a location problem with the coverage structure, and Nemhauser, Wolsey and Fisher (1978) proved the bound $1 - (1 - 1/k)^k$ for each monotone submodular function. Hochbaum and Pathria (1998) gave the analysis for maximum coverage in the form used here, and Hochbaum's book (1997) presents it in its chapter on covering problems. Feige (1998) proved that no polynomial-time algorithm does better than $1 - 1/e + \varepsilon$ unless P = NP, so greedy is optimal.

## References
