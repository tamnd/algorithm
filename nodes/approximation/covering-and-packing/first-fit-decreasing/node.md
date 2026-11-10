---
tag: Q1QQRH
kind: algorithm
slug: first-fit-decreasing
name: First-fit decreasing bin packing
aliases:
- FFD
- first fit decreasing
area: approximation/covering-and-packing
level: intro
summary: Sort items by decreasing size, then apply first-fit; within 11/9 OPT plus a constant.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1973
  people: [David S. Johnson, György Dósa]
  note: Johnson proved 11/9 OPT + 4 in his 1973 thesis, and Dósa (2007) found the tight constant 6/9.
prereqs: [bin-packing, first-fit-bin-packing, bin-packing-lower-bound, approximation-ratio]
see_also: [first-fit-bin-packing, best-fit-bin-packing, bin-packing-np-hardness, bin-packing-aptas, karmarkar-karp-bin-packing, longest-processing-time-first, cutting-stock-problem]
sources:
  - paper: doi:10.1016/j.tcs.2013.09.007
    title: "György Dósa, Rongheng Li, Xin Han and Zsolt Tuza, Tight absolute bound for First Fit Decreasing bin-packing: FFD(L) <= 11/9 OPT(L) + 6/9, Theoretical Computer Science 510, 2013"
    locator: pp. 13-61, the main theorem and the tight lists
  - paper: "G. Dósa, The tight bound of First Fit Decreasing bin-packing algorithm is FFD(I) <= 11/9 OPT(I) + 6/9, ESCAPE 2007, LNCS 4614, pp. 1-11"
    title: Dósa 2007
    locator: the statement of the tight bound and the lower bound lists
  - paper: "D. S. Johnson, Near-optimal bin packing algorithms, PhD thesis, Massachusetts Institute of Technology, 1973"
    title: Johnson 1973
    locator: the bound 11/9 OPT + 4 for first fit decreasing
  - paper: "D. Simchi-Levi, New worst-case results for the bin-packing problem, Naval Research Logistics 41, 1994"
    title: Simchi-Levi 1994
    locator: the absolute bound 3/2 for first fit decreasing and best fit decreasing
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 2, E. G. Coffman, M. R. Garey and D. S. Johnson, Approximation algorithms for bin packing, a survey (first fit decreasing)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.3 (bin packing)
---

First fit decreasing is the standard offline heuristic for [bin packing](/bin-packing/): sort the items from largest to smallest, then pack them with [first fit](/first-fit-bin-packing/). It runs in $O(n \log n)$ time. It uses at most $\frac{11}{9}\mathrm{OPT} + \frac69$ bins on every list, and lists exist where it uses exactly that many (Dósa 2007). It also uses at most $\frac32\mathrm{OPT}$ bins, which is the best absolute ratio of any polynomial-time algorithm unless P = NP. This page proves the $\frac32$ bound in full and sketches the $\frac{11}{9}$ bound.

## In plain words

Before you pack, you sort the objects from the biggest to the smallest. Then you pack them in that order: each object goes into the first box where it fits, and if it fits nowhere you start a new box.

Big objects are the hard part, because each one needs much room. If you pack them first, each gets its own box, and the small objects that come later fill the gaps that the big ones left. Packing the small objects first can leave no good place for the big ones. So sorting first wastes much less space: in the worst case about 22 percent more boxes than the best, against 70 percent for first fit without sorting.

## The problem

The input is a list of sizes $s_1, \ldots, s_n$ with $0 < s_i \le 1$, all known in advance, and the output is a partition into bins of load at most 1 with few bins. This is the [bin packing problem](/bin-packing/). We write $S = \sum_i s_i$, $\mathrm{OPT}$ for the least number of bins and $\mathrm{FFD}$ for the number of bins of first fit decreasing.

*Ratio convention.* Both bounds on this page are absolute: $\mathrm{FFD} \le \frac{11}{9}\mathrm{OPT} + \frac69$ and $\mathrm{FFD} \le \frac32\mathrm{OPT}$ hold for every list. The asymptotic ratio is $\frac{11}{9}$, and the absolute ratio is $\frac32$; both are tight for the algorithm, and $\frac32$ is also tight for the problem. The proof of $\frac32$ compares with two [lower bounds on OPT](/bin-packing-lower-bound/): the size bound $\lceil S \rceil$ and the number of items larger than $\frac12$.

## The algorithm

```pseudo id=main
FIRST-FIT-DECREASING(s[1 .. n])
L1  sort the items so that s[1] ≥ s[2] ≥ ... ≥ s[n]
L2  k ← 0
L3  for i ← 1 to n do
L4      j ← the least index in 1 .. k with load[j] + s[i] ≤ 1, or k + 1 if there is none
L5      if j = k + 1 then k ← k + 1, B[k] ← ∅, load[k] ← 0
L6      B[j] ← B[j] ∪ {i}, load[j] ← load[j] + s[i]
L7  return B[1 .. k]
```

Lines L2 to L7 are [first fit](/first-fit-bin-packing/). Line L4 uses the same max tree over the free space of the bins, so it takes $O(\log n)$ time.

## Example

Run first fit decreasing on $L = (0.2, 0.5, 0.4, 0.7, 0.1, 0.3, 0.8)$, where $S = 3$. Line L1 gives $(0.8, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1)$.

| item | loads before | choice | loads after |
|---|---|---|---|
| 0.8 | none | new $B_1$ | 0.8 |
| 0.7 | 0.8 | new $B_2$ | 0.8, 0.7 |
| 0.5 | 0.8, 0.7 | new $B_3$ | 0.8, 0.7, 0.5 |
| 0.4 | 0.8, 0.7, 0.5 | $B_3$ | 0.8, 0.7, 0.9 |
| 0.3 | 0.8, 0.7, 0.9 | $B_2$ | 0.8, 1.0, 0.9 |
| 0.2 | 0.8, 1.0, 0.9 | $B_1$ | 1.0, 1.0, 0.9 |
| 0.1 | 1.0, 1.0, 0.9 | $B_3$ | 1.0, 1.0, 1.0 |

First fit decreasing uses 3 bins, $[0.8\ 0.2]$, $[0.7\ 0.3]$, $[0.5\ 0.4\ 0.1]$, which is optimal because $\lceil S \rceil = 3$. On the same list, [next fit](/next-fit-bin-packing/) uses 5 bins and [first fit](/first-fit-bin-packing/) uses 4.

## Correctness

Each bin has load at most 1, because lines L2 to L7 are first fit. The key property is the one of first fit: an item in bin $B_t$ is larger than the final free space of each earlier bin. The sorted order adds a second fact: once an item of size at most $\frac12$ opens a bin, every later item is at most $\frac12$.

*The factor $\frac32$.* Let $j = \lceil 2\,\mathrm{FFD}/3 \rceil$. If bin $B_j$ has an item larger than $\frac12$, then so do $B_1, \ldots, B_{j-1}$, and $\mathrm{OPT} \ge j$ because no two such items share a bin. Otherwise the bins from $B_j$ on hold only items of size at most $\frac12$, each of them but the last holds at least two items, and so they hold at least $j - 1$ items. Each of these items overfills one of $B_1, \ldots, B_{j-1}$, so $S > j - 1$ and $\mathrm{OPT} \ge j$. In both cases $\mathrm{FFD} \le \frac32\,\mathrm{OPT}$.

*The factor $\frac{11}{9}$ (sketch).* The proof takes a minimal counterexample, shows that its smallest item is alone in the last bin, and uses a weight function with a long case analysis. The full proofs and the sketch are below.

## Complexity

- **Time.** Sorting takes $\Theta(n \log n)$ comparisons, and first fit with the max tree takes $\Theta(n \log n)$, so the total is $\Theta(n \log n)$ in the [real RAM](/real-ram/) model.
- **Space.** $\Theta(n)$ for the sorted order, the loads and the tree, plus the output.

## Properties

| claim | statement | status |
|---|---|---|
| absolute ratio | $\mathrm{FFD} \le \frac32\,\mathrm{OPT}$ | proved below |
| tight for $\frac32$ | capacity 8, sizes $(4, 3, 3, 2, 2, 2)$: $\mathrm{OPT} = 2$, $\mathrm{FFD} = 3$ | proved below |
| best possible | no polynomial-time algorithm has absolute ratio below $\frac32$ unless P = NP | [hardness theorem](/bin-packing-np-hardness/) |
| additive bound | $\mathrm{FFD} \le \frac{11}{9}\mathrm{OPT} + \frac69$ | Dósa 2007, sketched below |
| tight lists | $\mathrm{FFD} = \frac{11}{9}\mathrm{OPT} + \frac69$ for each $\mathrm{OPT} \equiv 6 \pmod 9$ | proved below |
| asymptotic ratio | exactly $\frac{11}{9}$ | follows from the two rows above |
| online | no; the sort needs the whole list | by definition |

*The tight lists.* Use $\varepsilon = \frac1{100}$ and four sizes $a = \frac12 + \varepsilon$, $b = \frac14 + 2\varepsilon$, $c = \frac14 + \varepsilon$, $d = \frac14 - 2\varepsilon$. With $6m$ items each of $a$, $b$, $c$ and $12m$ items of $d$, first fit decreasing makes $6m$ bins $\{a, b\}$, $2m$ bins $\{c, c, c\}$ and $3m$ bins $\{d, d, d, d\}$, so $11m$ bins, while the bins $\{a, c, d\}$ and $\{b, b, d, d\}$ have load exactly 1 and give $\mathrm{OPT} = 9m$. With $6m + 4$ items each of $a$, $b$, $c$ and $12m + 8$ items of $d$, it uses $11m + 8$ bins against $\mathrm{OPT} = 9m + 6$.

## Variants and improvements

- **Best fit decreasing.** Sort, then use [best fit](/best-fit-bin-packing/). Its asymptotic ratio is also $\frac{11}{9}$, and its absolute ratio is also $\frac32$.
- **Modified first fit decreasing.** Johnson and Garey (1985) treat the items in $(\frac16, \frac13]$ in a special way and get asymptotic ratio $\frac{71}{60}$.
- **Next fit decreasing.** Sort, then use [next fit](/next-fit-bin-packing/). Its asymptotic ratio is about $1.691$, much worse.
- **Asymptotic schemes.** For each $\varepsilon > 0$, the [asymptotic scheme](/bin-packing-aptas/) uses at most $(1 + \varepsilon)\mathrm{OPT} + 1$ bins, and [Karmarkar and Karp](/karmarkar-karp-bin-packing/) use $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$. They are much slower.
- **Scheduling.** The same "largest first" idea gives [longest processing time first](/longest-processing-time-first/) for makespan scheduling, and the MULTIFIT algorithm of Coffman, Garey and Johnson (1978) schedules jobs by a binary search over bin capacities with first fit decreasing inside.

## When to use it

Use first fit decreasing whenever the whole list is known in advance and a fast answer is needed. It is simple, it runs in $O(n \log n)$ time, and on random lists it is very close to optimal. Use it as the first step before an exact method: its value is an upper bound, and the [lower bounds](/bin-packing-lower-bound/) often meet it. For large instances with few distinct sizes, use the [cutting stock](/cutting-stock-problem/) model with column generation instead.

## Pitfalls

- **Sort in decreasing order.** Sorting in increasing order makes first fit much worse: small items first can fill each bin with many small items and leave the big items one to a bin.
- **Quote the right bound.** The bound $\frac{11}{9}\mathrm{OPT} + \frac69$ is the smaller one for $\mathrm{OPT} \ge 3$, and $\frac32\mathrm{OPT}$ is the smaller one for $\mathrm{OPT} \le 2$. The ratio $\frac{11}{9}$ alone, without the additive term, is false for small lists, as the partition example shows.
- **Floating-point sizes.** The tight lists depend on sums that are exactly 1. Use integer sizes or exact fractions.

## Implementations

## History

Johnson's 1973 thesis proved $\mathrm{FFD} \le \frac{11}{9}\mathrm{OPT} + 4$, and the 1974 paper of Johnson, Demers, Ullman, Garey and Graham gave the asymptotic ratio $\frac{11}{9}$. Later proofs lowered the additive term: Baker (1985) to 3, Yue (1991) to 1, and Li and Yue (2000) to $\frac79$. Dósa (2007) proved the tight term $\frac69$, with the full proof in Dósa, Li, Han and Tuza (2013). Simchi-Levi (1994) proved the absolute ratio $\frac32$.

## References
