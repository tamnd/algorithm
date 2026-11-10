---
tag: Z0DHY7
kind: algorithm
slug: best-fit-bin-packing
name: Best-fit bin packing
aliases:
- BF
- best fit
area: approximation/covering-and-packing
level: intro
summary: Place each item in the fullest bin where it still fits; at most 1.7 OPT bins, rounded down.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1974
  people: [David S. Johnson, Alan Demers, Jeffrey D. Ullman, Michael R. Garey, Ronald L. Graham, György Dósa, Jiří Sgall]
  note: Johnson, Demers, Ullman, Garey and Graham (1974) proved the asymptotic ratio 1.7, and Dósa and Sgall (2014) proved the absolute bound, the floor of 1.7 OPT.
prereqs: [bin-packing, bin-packing-lower-bound, first-fit-bin-packing, approximation-ratio]
see_also: [first-fit-bin-packing, next-fit-bin-packing, first-fit-decreasing, online-algorithm, bin-packing-aptas]
sources:
  - paper: doi:10.1007/978-3-662-43948-7_36
    title: "György Dósa and Jiří Sgall, Optimal analysis of Best Fit bin packing, ICALP 2014, LNCS 8572"
    locator: pp. 429-441, the main theorem (BF is at most the floor of 1.7 OPT) and the lower bound lists for each OPT
  - paper: "J. Sgall, A new analysis of Best Fit bin packing, FUN 2012, LNCS 7288, pp. 315-321"
    title: Sgall 2012
    locator: the absolute bound 1.75 for best fit
  - paper: "D. S. Johnson, A. Demers, J. D. Ullman, M. R. Garey and R. L. Graham, Worst-case performance bounds for simple one-dimensional packing algorithms, SIAM Journal on Computing 3, 1974"
    title: Johnson, Demers, Ullman, Garey and Graham 1974
    locator: the asymptotic bound 1.7 for best fit and the any fit class
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 2, E. G. Coffman, M. R. Garey and D. S. Johnson, Approximation algorithms for bin packing, a survey (best fit and any fit algorithms)
---

Best fit is an online algorithm for [bin packing](/bin-packing/): it puts each item into the open bin with the least free space that still has room for it, and it opens a new bin only if no bin has room. It has the same worst case as [first fit](/first-fit-bin-packing/): at most $\lfloor 1.7\,\mathrm{OPT} \rfloor$ bins on every list (Dósa and Sgall 2014), and asymptotic ratio exactly 1.7. With a balanced search tree keyed by free space it runs in $O(n \log n)$ time. This page proves feasibility and the bound $2\,\mathrm{OPT} - 1$ in full and sketches the 1.7 bound.

## In plain words

You keep a row of boxes. When an object comes, you look at all the boxes where it fits and choose the box that is fullest. If it fits nowhere, you start a new box.

The idea is to keep the leftover spaces small, so that the boxes that are almost full get filled up, and the boxes with much room stay free for big objects. In the worst case best fit is as good and as bad as first fit: never much more than 1.7 times the best number of boxes. On some inputs best fit wins, and on others first fit wins.

## The problem

The input is a list of sizes $s_1, \ldots, s_n$ with $0 < s_i \le 1$, in the order of arrival, and the output is a partition into bins of load at most 1 with few bins. This is the [bin packing problem](/bin-packing/). We write $S = \sum_i s_i$, $\mathrm{OPT}$ for the least number of bins and $\mathrm{BF}$ for the number of bins of best fit.

*Ratio convention.* $\mathrm{BF} \le \lfloor 1.7\,\mathrm{OPT} \rfloor$ is an absolute bound, for every list. The asymptotic ratio is also 1.7. The simple analysis compares with the size bound $\lceil S \rceil$, and the 1.7 analysis compares with a weighted size, at most 1.7 per optimal bin; see [lower bounds for bin packing](/bin-packing-lower-bound/).

## The algorithm

```pseudo id=main
BEST-FIT(s[1 .. n])
L1  k ← 0                                   ▷ no bin is open yet
L2  for i ← 1 to n do
L3      j ← an index in 1 .. k with load[j] + s[i] ≤ 1 and load[j] largest, the least such index on ties, or k + 1 if there is none
L4      if j = k + 1 then k ← k + 1, B[k] ← ∅, load[k] ← 0
L5      B[j] ← B[j] ∪ {i}, load[j] ← load[j] + s[i]
L6  return B[1 .. k]
```

Line L3 asks for the smallest free space that is at least $s_i$. Keep the open bins in a balanced search tree keyed by the pair (free space, index). Then line L3 is a successor query for $(s_i, 0)$, and line L5 removes the bin and inserts it again with its new free space. Each step takes $O(\log n)$ time.

## Example

Run best fit on $L = (0.2, 0.5, 0.4, 0.7, 0.1, 0.3, 0.8)$, where $S = 3$ and $\mathrm{OPT} = 3$.

| item | size | loads before | bins with room | choice | loads after |
|---|---|---|---|---|---|
| 1 | 0.2 | none | none | new $B_1$ | 0.2 |
| 2 | 0.5 | 0.2 | $B_1$ | $B_1$ | 0.7 |
| 3 | 0.4 | 0.7 | none | new $B_2$ | 0.7, 0.4 |
| 4 | 0.7 | 0.7, 0.4 | none | new $B_3$ | 0.7, 0.4, 0.7 |
| 5 | 0.1 | 0.7, 0.4, 0.7 | all | $B_1$ (fullest, first on the tie) | 0.8, 0.4, 0.7 |
| 6 | 0.3 | 0.8, 0.4, 0.7 | $B_2$, $B_3$ | $B_3$ (fuller) | 0.8, 0.4, 1.0 |
| 7 | 0.8 | 0.8, 0.4, 1.0 | none | new $B_4$ | 0.8, 0.4, 1.0, 0.8 |

Best fit uses 4 bins: $[0.2\ 0.5\ 0.1]$, $[0.4]$, $[0.7\ 0.3]$, $[0.8]$. First fit also uses 4 bins here, but it puts $0.3$ into $B_2$.

Neither rule is always better. On $(0.5, 0.6, 0.9, 0.2, 0.3, 0.6, 0.4, 0.4)$ first fit uses 4 bins, best fit uses 5, and $\mathrm{OPT} = 4$. On $(0.3, 0.8, 0.9, 0.3, 0.8, 0.8, 0.2, 0.4)$ first fit uses 6 bins, best fit uses 5, and $\mathrm{OPT} = 5$.

## Correctness

Each bin has load at most 1, because line L3 picks only bins with room and a new bin has room for any item. For the bounds, the key fact is weaker than for first fit: only the *first* item of a bin is larger than the free space of each bin that was open at that time. A later item can go into a full bin although an emptier bin has room.

*The factor 2.* The first item fact is enough to show that at most one bin has load at most $\frac12$, and that this bin with any other bin holds more than 1. So $S > \mathrm{BF}/2$ when $\mathrm{BF} \ge 2$, and $\mathrm{BF} \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$. The same holds for every any fit algorithm, that is, every rule that opens a new bin only when no open bin has room.

*The factor 1.7 (sketch).* The proof of Dósa and Sgall uses the weight function of [first fit](/first-fit-bin-packing/): each set that fits in a bin has weight at most 1.7, and most bins of best fit have weight at least 1. The step that shows this second fact is new for best fit, because the first fit property fails. The proofs are below.

## Complexity

- **Time.** With a balanced search tree over the open bins, each item costs $\Theta(\log n)$ in the worst case, so the time is $\Theta(n \log n)$, in the [real RAM](/real-ram/) model. A direct scan of all bins costs $\Theta(n^2)$ in the worst case.
- **Space.** $\Theta(n)$ for the loads and the tree, plus the output.

## Properties

| claim | statement | status |
|---|---|---|
| simple bound | $\mathrm{BF} \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$ | proved below |
| absolute bound | $\mathrm{BF} \le \lfloor 1.7\,\mathrm{OPT} \rfloor$ | Dósa and Sgall 2014, sketched below |
| asymptotic ratio | exactly 1.7 | Johnson et al. 1974 |
| lower bound 5/3 | $\mathrm{BF} = \frac53\,\mathrm{OPT}$ on a simple family | proved below |
| lower bound 1.7 | for each $\mathrm{OPT}$ there is a list with $\mathrm{BF} = \lfloor 1.7\,\mathrm{OPT} \rfloor$ | Dósa and Sgall 2014, cited |
| online | yes | by definition |

*A family with ratio 5/3.* Take $6m$ items of size $\frac17 + \varepsilon$, then $6m$ of size $\frac13 + \varepsilon$, then $6m$ of size $\frac12 + \varepsilon$, with a small $\varepsilon > 0$. Best fit packs the first kind six to a bin, the second kind two to a bin and the third kind one to a bin, which gives $10m$ bins, while one item of each kind per bin gives $\mathrm{OPT} = 6m$.

## Variants and improvements

- **First fit.** Put the item into the first bin with room. Same worst case; see [first fit](/first-fit-bin-packing/).
- **Worst fit.** Put the item into the emptiest bin with room. It is an any fit algorithm, so it uses at most $2\,\mathrm{OPT} - 1$ bins, and its asymptotic ratio is 2.
- **Best fit decreasing.** Sort by decreasing size first. Its asymptotic ratio is $\frac{11}{9}$, the same as for [first fit decreasing](/first-fit-decreasing/) (Johnson 1973).
- **Bounded space.** Best-k-fit keeps only $k$ bins open. Its asymptotic ratio tends to 1.7 as $k$ grows (see the survey of Coffman, Garey and Johnson).

## When to use it

Use best fit for online packing when all bins may stay open. It often leaves fewer nearly empty bins than first fit on random data, and it has the same worst case. If the list is known in advance, sort it first. If memory allows only a few open bins, use [next fit](/next-fit-bin-packing/) or a bounded-space rule.

## Pitfalls

- **Ties.** The rule must fix how ties between bins with equal load are broken. The bounds hold for any tie rule, but the output, and so the tests, depend on it. This page breaks ties by the least index.
- **The first fit proof does not apply.** In first fit, each item of a later bin is larger than the free space of each earlier bin. In best fit this is true only for the first item of each bin, so the proof of the 1.7 bound must change.
- **Floating-point sizes.** Exact comparisons decide where an item goes. Use integer sizes or exact fractions.
## Implementations

## History

Johnson, Demers, Ullman, Garey and Graham (1974) proved that best fit, like first fit, has asymptotic ratio 1.7, and they gave the class of any fit algorithms. The absolute ratio took longer. Sgall (2012) proved 1.75, and Dósa and Sgall (2014) proved $\mathrm{BF} \le \lfloor 1.7\,\mathrm{OPT} \rfloor$ with matching lists for each value of $\mathrm{OPT}$.

## References
