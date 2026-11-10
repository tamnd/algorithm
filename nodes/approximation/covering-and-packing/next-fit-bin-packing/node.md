---
tag: G0STDP
kind: algorithm
slug: next-fit-bin-packing
name: Next-fit bin packing
aliases:
- NF
- next fit
area: approximation/covering-and-packing
level: intro
summary: Place each item in the current bin or open a new one; at most twice optimal.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1974
  people: [David S. Johnson, Alan Demers, Jeffrey D. Ullman, Michael R. Garey, Ronald L. Graham]
  note: Johnson analysed next fit in his 1973 thesis, and the bound appears in the 1974 paper of Johnson, Demers, Ullman, Garey and Graham.
prereqs: [bin-packing, bin-packing-lower-bound, approximation-ratio]
see_also: [first-fit-bin-packing, best-fit-bin-packing, first-fit-decreasing, online-algorithm, next-fit-allocation]
sources:
  - paper: "D. S. Johnson, A. Demers, J. D. Ullman, M. R. Garey and R. L. Graham, Worst-case performance bounds for simple one-dimensional packing algorithms, SIAM Journal on Computing 3, 1974"
    title: Johnson, Demers, Ullman, Garey and Graham 1974
    locator: the section on next fit (the bound 2 and the worst-case lists)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 2, E. G. Coffman, M. R. Garey and D. S. Johnson, Approximation algorithms for bin packing, a survey (next fit and its variants)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 35, Problem 35-1 (bin packing)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (Bin packing)
---

Next fit is the simplest online algorithm for [bin packing](/bin-packing/): it keeps one open bin, puts each item into it if the item fits, and otherwise closes the bin for good and opens a new one. It runs in $\Theta(n)$ time with $O(1)$ extra memory. It uses at most $2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$ bins, where $S$ is the total size, and this bound is reached for each value of $\mathrm{OPT}$. Its analysis is the model for the analysis of the better rules [first fit](/first-fit-bin-packing/) and [best fit](/best-fit-bin-packing/).

## In plain words

You fill one box at a time. You take the objects in the order they come. If the next object fits into the box you are filling, you put it there. If it does not fit, you close that box, put it on the truck, and start a new box with the object. You never go back to a closed box.

This rule is fast and needs almost no memory, because you only look at one box. It wastes space: a closed box can be almost half empty. But two boxes in a row always hold more than one full box of objects, because the object that started the second box did not fit into the first. So you never use more than about twice the best number of boxes.

## The problem

The input is a list of $n$ sizes $s_1, \ldots, s_n$ with $0 < s_i \le 1$, in the order of arrival. The output is a partition of the items into bins, each with load at most 1. The goal is few bins. This is the [bin packing problem](/bin-packing/). We write $S = \sum_i s_i$, $\mathrm{OPT}$ for the least number of bins and $\mathrm{NF}$ for the number of bins that next fit uses.

The ratio convention is the one of the [bin packing](/bin-packing/) page: a bound $\mathrm{NF} \le \rho \cdot \mathrm{OPT}$ that holds for every input is an absolute ratio, and the bounds are worst case. The analysis compares with the [size bound](/bin-packing-lower-bound/) $\lceil S \rceil \le \mathrm{OPT}$.

## The algorithm

```pseudo id=main
NEXT-FIT(s[1 .. n])
L1  k ← 0, load ← 0                     ▷ no bin is open yet
L2  for i ← 1 to n do
L3      if k = 0 or load + s[i] > 1 then
L4          k ← k + 1, B[k] ← ∅, load ← 0  ▷ close B[k − 1] for good
L5      B[k] ← B[k] ∪ {i}, load ← load + s[i]
L6  return B[1 .. k]
```

Only the current bin $B[k]$ can receive items. The test of line L3 uses $>$: an item that fills the bin exactly goes into it.

## Example

Run next fit on $L = (0.2, 0.5, 0.4, 0.7, 0.1, 0.3, 0.8)$. The total size is $S = 3$, and $\mathrm{OPT} = 3$ with the bins $\{0.8, 0.2\}$, $\{0.7, 0.3\}$, $\{0.5, 0.4, 0.1\}$.

| item | size | load of current bin before | action | bins after |
|---|---|---|---|---|
| 1 | 0.2 | none | open $B_1$ | [0.2] |
| 2 | 0.5 | 0.2 | fits | [0.2 0.5] |
| 3 | 0.4 | 0.7 | $1.1 > 1$, open $B_2$ | [0.2 0.5] [0.4] |
| 4 | 0.7 | 0.4 | $1.1 > 1$, open $B_3$ | ... [0.4] [0.7] |
| 5 | 0.1 | 0.7 | fits | ... [0.7 0.1] |
| 6 | 0.3 | 0.8 | $1.1 > 1$, open $B_4$ | ... [0.7 0.1] [0.3] |
| 7 | 0.8 | 0.3 | $1.1 > 1$, open $B_5$ | ... [0.3] [0.8] |

Next fit uses 5 bins, which equals $2\lceil S \rceil - 1 = 5$. The bin $[0.4]$ has room for the item $0.1$ that comes later, and the bin $[0.3]$ has room for $0.2$, but next fit never looks back.

## Correctness

Next fit returns a valid packing: each item goes into exactly one bin, and line L3 adds an item to the open bin only when the new load is at most 1. The bound comes from one fact. The item that opens bin $B_{j+1}$ did not fit into $B_j$, and $B_j$ never changes after that, so

$$\mathrm{load}(B_j) + \mathrm{load}(B_{j+1}) > 1 \qquad (1 \le j < k).$$

Group the bins into $\lfloor k/2 \rfloor$ disjoint consecutive pairs. Each pair holds more than 1, so $S > \lfloor k/2 \rfloor$, hence $\lfloor k/2 \rfloor \le \lceil S \rceil - 1$ and $k \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$. The full proof, and the proof that the bound is reached for each value of $\mathrm{OPT}$, are below.

## Complexity

- **Time.** Each item costs one comparison and one addition, so the time is $\Theta(n)$ in each case, in the [real RAM](/real-ram/) model where one addition or comparison of sizes costs $O(1)$. With integer sizes and capacity $C$, the numbers have $O(\log C)$ digits.
- **Space.** Next fit keeps only the index and the load of the open bin: $\Theta(1)$ extra memory, plus the output. It is a *1-bounded-space* online algorithm: at each moment only one bin is open.

## Properties

| claim | statement | status |
|---|---|---|
| upper bound | $\mathrm{NF} \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$ for $n \ge 1$ | proved below |
| tight for each OPT | the list $f, b, f, \ldots, b, f$ with $k$ copies of $f = \frac{1}{2k}$ and $k-1$ copies of $b = 1 - \frac{1}{4k}$ has $\mathrm{OPT} = k$ and $\mathrm{NF} = 2k - 1$ | proved below |
| asymptotic ratio | exactly 2 | follows from the two rows above |
| small items | if each $s_i \le \alpha < 1$, then $\mathrm{NF} \le \frac{S}{1 - \alpha} + 1$ | proved below |

A second tight family shows the waste in a picture: the list $(\frac12, \frac{1}{2m})$ repeated $2m$ times. Each bin of next fit holds one item $\frac12$ and one small item, so $\mathrm{NF} = 2m$, while $m$ bins of two halves and one bin of all $2m$ small items give $\mathrm{OPT} = m + 1$. The ratio $\frac{2m}{m+1}$ tends to 2.

*Small items.* If each item is at most $\alpha$, each closed bin $B_j$ with $j < k$ has load more than $1 - \alpha$, because the next item, of size at most $\alpha$, did not fit. So $S > (k - 1)(1 - \alpha)$ and $k < \frac{S}{1-\alpha} + 1$. For $\alpha = \frac12$ this gives about $2S$; for small $\alpha$ it is close to $S$.

## Variants and improvements

- **Next-k-fit.** Keep the last $k$ bins open and put the item into the first of them where it fits. For $k \ge 2$ the asymptotic ratio is below 2 and tends to 1.7 as $k$ grows (see the survey of Coffman, Garey and Johnson for the exact values).
- **Next fit decreasing.** Sort the items by decreasing size first. Baker and Coffman (1981) showed an asymptotic ratio of about $1.691$.
- **Harmonic.** Lee and Lee (1985) classify items by size into the intervals $(\frac{1}{j+1}, \frac{1}{j}]$ and run next fit on each class. With enough classes the asymptotic ratio approaches $1.691$, the best possible for bounded-space online algorithms.
- **First fit and best fit.** Keep all bins open. This gives $\lfloor 1.7\,\mathrm{OPT} \rfloor$; see [first fit](/first-fit-bin-packing/) and [best fit](/best-fit-bin-packing/).

## When to use it

Use next fit when the bins must leave at once (a truck that departs when it is full, a buffer that is flushed, a disk block that is written) and memory is tiny. Use it as a baseline. If all bins may stay open, [first fit](/first-fit-bin-packing/) or [best fit](/best-fit-bin-packing/) is much better, and if the list is known in advance, [first fit decreasing](/first-fit-decreasing/) is better still.

## Pitfalls

- **Comparing with $\ge$.** The test of line L3 must be $load + s_i > 1$. With $\ge$, an item that fills the bin exactly opens a new bin, two consecutive bins then hold only at least 1 instead of more than 1, and the bound $2\lceil S \rceil - 1$ fails: two items of size $\frac12$ take two bins.
- **Floating-point sizes.** With binary floating point, $0.7 + 0.3$ may come out as more or less than 1. Use integer sizes with an integer capacity, or exact fractions.
- **Sorting does not help much.** Next fit decreasing still has asymptotic ratio about $1.691$, worse than first fit decreasing ($\frac{11}{9}$).

## Implementations

## History

Next fit is analysed in David S. Johnson's 1973 thesis and in the 1974 paper of Johnson, Demers, Ullman, Garey and Graham, which also gives the worst-case lists for next fit, first fit, best fit and first fit decreasing. The bounded-space line of work that grew from it, including next-k-fit and harmonic, is surveyed by Coffman, Garey and Johnson in Hochbaum's book.

## References
