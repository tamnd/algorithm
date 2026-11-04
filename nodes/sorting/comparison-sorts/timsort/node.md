---
tag: PM6BZ3
kind: algorithm
slug: timsort
name: Timsort
aliases:
- Tim sort
area: sorting/comparison-sorts
level: advanced
summary: Hybrid stable sort that merges detected runs with galloping and insertion sort; the default in Python and Java objects.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, r: the number of runs}
  time: {worst: O(n log n), average: Θ(n log n), best: Θ(n)}
  space: {extra: O(n)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 2002
  people: [Tim Peters]
  note: Tim Peters wrote Timsort for the list sort of Python 2.3, and described it in the file listsort.txt of the CPython sources.
prereqs: [natural-merge-sort, insertion-sort, stable-sort]
see_also: [natural-merge-sort, merge-sort, insertion-sort, exponential-search, merging-lower-bound, adaptive-sorting, stable-sort, presortedness]
sources:
  - paper: "Tim Peters, listsort.txt, in the source code of CPython (Objects/listsort.txt), 2002 and later"
    locator: the sections on runs and minrun, the merge pattern and its invariants, merge memory, and galloping with MIN_GALLOP = 7
  - paper: "Stijn de Gouw, Jurriaan Rot, Frank S. de Boer, Richard Bubel and Reiner Hähnle, OpenJDK's java.utils.Collection.sort() is broken: the good, the bad and the worst case, Computer Aided Verification (CAV 2015), Lecture Notes in Computer Science 9206, Springer, 2015"
    locator: the failure of the invariant of merge_collapse, the input that breaks it, and the corrected check of four runs
  - paper: "Nicolas Auger, Vincent Jugé, Cyril Nicaud and Carine Pivoteau, On the worst-case complexity of TimSort, 26th European Symposium on Algorithms (ESA 2018), LIPIcs 112, 2018"
    locator: the main theorem, the bound O(n + n H) for the entropy H of the run lengths
  - paper: "J. Ian Munro and Sebastian Wild, Nearly-optimal mergesorts: fast, practical sorting methods that optimally adapt to existing runs, 26th European Symposium on Algorithms (ESA 2018), LIPIcs 112, 2018"
    locator: the analysis of the merge policy of Timsort, and Powersort
  - paper: "Peter McIlroy, Optimistic sorting and information theoretic complexity, Proceedings of the Fourth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1993"
    locator: the merge with exponential search, which Peters credits as the source of galloping
---

Timsort is a stable, adaptive merge sort, designed by Tim Peters in 2002 for Python's list sort and later adopted for objects in Java and in other languages. It scans the input for *runs*, parts that are already sorted, as [natural merge sort](/natural-merge-sort/) does, reverses the strictly decreasing ones, and extends short runs to a minimum length with binary [insertion sort](/insertion-sort/). It keeps the runs on a stack and merges neighbours so that the run lengths satisfy a few inequalities, which keeps the merges balanced and the stack short. Each merge uses a buffer of the smaller run and switches to *galloping*, an [exponential search](/exponential-search/), when one run wins many times in a row. Timsort takes $\Theta(n)$ time on sorted or reversed input and $O(n \log n)$ in the worst case; more precisely, $O(n + n H)$, where $H \le \lg r$ is the entropy of the run lengths. It is [stable](/stable-sort/) and needs at most $n/2$ items of extra space.

## In plain words

Real data is often partly sorted: a list that was sorted and then got a few new items at the end, or two sorted lists put one after the other. Timsort looks for the parts that are already in order, called runs, and keeps them. A part in reverse order is turned around. Very short runs are made longer with a simple insertion sort, because insertion sort is fast on a few items.

Then Timsort merges the runs, two neighbours at a time. It merges in an order that keeps the runs that it merges about equal in size, like a careful merge sort.

During a merge, if one run gives many items in a row, Timsort stops comparing item by item. It jumps ahead in larger and larger steps to find where the other run's next item goes, and copies the whole block at once.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order, and items with equal keys in their input order. This is the [sorting problem](/sorting-problem/) with the extra demand of [stability](/stable-sort/). Timsort uses a buffer of at most $\lfloor n/2 \rfloor$ items and a stack of $O(\log n)$ runs.

## The algorithm

```pseudo id=main
TIMSORT(A)                                 ▷ n is the length of A; n ≥ 2
L1  minrun ← MIN-RUN(n)                    ▷ n if n < 64, else a value in [32, 64]
L2  S ← an empty stack of runs;  lo ← 0
L3  while lo < n do
L4      find the run that starts at lo; if it is strictly decreasing, reverse it
L5      if the run is shorter than min(minrun, n − lo), extend it by binary insertion sort
L6      push the run on S;  lo ← the end of the run
L7      while the runs at the top of S break the invariants, merge two neighbours
L8  merge the runs of S from the top, until one run is left
```

**Runs.** Line L4 counts the longest prefix of $A[lo \ldots]$ that is non-decreasing, or that is strictly decreasing. A decreasing run must be strict: reversing two equal items would break the stability.

**minrun.** For $n < 64$, MIN-RUN returns $n$, so the whole array is one binary insertion sort. Otherwise it takes the six leading bits of $n$, and adds 1 if any of the other bits is 1. The result lies in $[32, 64]$, and $n / \text{minrun}$ is a power of 2 or a little less, so the final merges are balanced. For example, MIN-RUN gives 32 for $n = 64$, 33 for $n = 65$, 63 for $n = 2000$ and 49 for $n = 10^5$.

**Binary insertion sort.** Line L5 inserts each new item into the sorted run by binary search, after its equal items. This makes $O(m \log m)$ comparisons and $O(m^2)$ moves for $m \le 64$ items.

**The invariants.** Let the lengths of the four top runs be $W, X, Y, Z$, with $Z$ on top. Line L7 keeps

$$Y > Z, \qquad X > Y + Z, \qquad W > X + Y.$$

While one of them fails, it merges $Y$ with the smaller of its neighbours $X$ and $Z$ (with $Z$ when $X \ge Z$), and checks again. The third inequality is the fix of de Gouw et al. (2015): the original code checked only $X$, $Y$ and $Z$, and then the invariant could fail deeper in the stack. With the invariants, the run lengths grow at least as fast as the Fibonacci numbers from the top to the bottom, so the stack holds $O(\log n)$ runs.

**The merge.** To merge neighbours $A$ and $B$, Timsort first finds, by galloping, the items of $A$ at most $B[0]$ and the items of $B$ at least the last item of $A$. These are already in place. It copies the smaller of the rest to a buffer, and merges from the left if $A$ is the smaller, or from the right if $B$ is. On a tie the item of $A$ goes first. After one run has won $\text{min\_gallop}$ times in a row (7 at the start), the merge gallops: it finds how many items of one run come before the next item of the other with an exponential search, which takes $O(\log k)$ comparisons for a block of $k$ items, and copies the block. It returns to one item at a time when the blocks become shorter than 7. The value $\text{min\_gallop}$ goes down while galloping pays and up when it does not.

## Example

The input consists of five ascending runs of lengths 120, 80, 60, 50 and 40, with each run below the one before it, so $n = 350$ and MIN-RUN gives 44. All runs are long enough, so line L5 does nothing.

| step | the stack of run lengths, top at the right | action |
|---|---|---|
| push 120 | 120 | |
| push 80 | 120, 80 | $120 > 80$: no merge |
| push 60 | 120, 80, 60 | $120 \le 80 + 60$: merge $Y = 80$ with $Z = 60$ |
| | 120, 140 | $120 \le 140$: merge |
| | 260 | |
| push 50 | 260, 50 | no merge |
| push 40 | 260, 50, 40 | $260 > 90$ and $50 > 40$: no merge |
| line L8 | 260, 90 | merge 50 with 40, then 260 with 90 |
| | 350 | |

The merges are $(80, 60)$, $(120, 140)$, $(50, 40)$ and $(260, 90)$. Each later run is below the earlier one, so in each merge the run on the right wins every comparison. After 7 wins the merge gallops and moves the rest of the run in one block. The whole sort makes 432 comparisons, against about $350 \lg 350 \approx 2958$ for a plain merge sort.

**Comparisons for $n = 10^5$**, counted for the implementation on this page and for the list sort of CPython 3.14, which uses the merge order of Powersort:

| input | this page | CPython |
|---|---|---|
| sorted | 99,999 | 99,999 |
| reversed | 99,999 | 99,999 |
| sorted, then 10 random items | 100,303 | 100,282 |
| two sorted halves, random values | 200,001 | 200,000 |
| 4 distinct keys, random order | 562,421 | 564,261 |
| random permutation | 1,533,353 | 1,531,974 |

For comparison, $\lg(n!) \approx 1{,}516{,}704$ and $n \lg n \approx 1{,}660{,}964$ for this $n$.

## Correctness

Each run that line L6 pushes is a sorted segment of the array, and the runs on the stack are consecutive segments that together cover $A[0 \ldots lo-1]$. A merge of two neighbouring runs gives a sorted segment that covers both. When the loop ends, the runs cover the array, and line L8 merges them into one. So the array is sorted.

Stability follows from four rules: a decreasing run is strict, so no two equal items are reversed; binary insertion puts an item after its equal items; the runs that are merged are neighbours, so all items of $A$ come before all items of $B$ in the input; and each merge, in both directions and in galloping mode, puts the item of $A$ first on a tie. The full proof, with the invariant of the merge, is below.

## Complexity

**Best case.** On a sorted or a strictly decreasing input, line L4 finds one run with $n - 1$ comparisons, and there is no merge. So the time is $\Theta(n)$.

**Worst case.** Auger, Jugé, Nicaud and Pivoteau (2018) proved that Timsort makes $O(n + n H)$ comparisons, where for runs of lengths $r_1, \ldots, r_\rho$,

$$H = \sum_{i=1}^{\rho} \frac{r_i}{n} \lg \frac{n}{r_i} \le \lg \rho.$$

Since $\rho \le n$, this is $O(n \log n)$ in the worst case. It is optimal up to the constant factor for inputs with these run lengths: a merge sort of runs needs about $n H$ comparisons in the worst case, by the [merging lower bound](/merging-lower-bound/). The proof uses the invariants of the stack, and it is also the first proof of $O(n \log n)$ for Timsort.

**Galloping.** A block of $k$ items that one run wins costs about $2 \lg k$ comparisons in galloping mode against $k$ in the simple merge. For two runs that do not overlap, a merge costs $O(\log n)$ comparisons. On random data galloping does not pay, so the adaptive $\text{min\_gallop}$ grows and the merge stays in the simple mode.

**Space.** The buffer holds the smaller of the two runs of a merge, at most $\lfloor n/2 \rfloor$ items. The stack holds $O(\log n)$ runs.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst | $O(n + n H) \subseteq O(n \log n)$ |
| time | sorted or strictly decreasing input | $\Theta(n)$, with $n - 1$ comparisons |
| time | random permutation | $\Theta(n \log n)$ |
| extra space | | at most $\lfloor n/2 \rfloor$ items, and a stack of $O(\log n)$ runs |

## Properties

- **Stable.** Equal items keep their order, by the four rules of the section on correctness.
- **Adaptive.** The time is $O(n + n H)$ for the entropy $H$ of the run lengths, and galloping makes merges of runs that barely overlap cheap.
- **Not in place.** The buffer holds up to $n/2$ items.
- **Not online.** It needs the whole array, although the scan for runs reads it from left to right.

## Variants and improvements

- **Java.** The class TimSort of OpenJDK, used by `Arrays.sort` for objects since Java 7, is a port of Peters' code. After the report of de Gouw et al., OpenJDK made its run stack larger rather than add the fourth check.
- **Powersort.** Munro and Wild replace the merge rule of line L7 by a rule based on the "power" of the boundary between two runs, which gives a merge cost within $O(n)$ of the optimum $n H$. CPython uses this rule since version 3.11; the rest of Timsort is unchanged.
- **Other merge rules.** Auger et al. and later papers study rules such as $\alpha$-merge sort and adaptive Shivers sort, which also reach $O(n + n H)$ with small constants.
- **Merging without galloping.** A simple natural merge sort with a balanced merge order, as in [natural merge sort](/natural-merge-sort/), keeps most of the gain on runs but loses the gain on runs that barely overlap.

## When to use it

Timsort is a good default sort for general data in a library, when stability matters and the data may be partly sorted: logs that arrive almost in order, lists that are sorted again after small changes, or data that is the concatenation of sorted parts. It is the sort behind Python's `list.sort` and `sorted`, and behind Java's `Arrays.sort` for objects. For arrays of primitive numbers, where stability does not matter, an unstable sort such as dual-pivot quicksort or pdqsort is often faster.

## Pitfalls

- **The invariant on three runs only.** The original merge_collapse checked only the top three runs. On crafted inputs the invariant then failed deeper in the stack, and Java's fixed-size run stack overflowed with an exception. Check four runs, as in line L7.
- **Decreasing runs with equal items.** Reverse only strictly decreasing runs. A run such as 3, 2, 2, 1, reversed as a whole, swaps the two equal items.
- **The direction of the ties.** In the merge from the right, an item of $B$ must win a tie, so that the item of $A$ ends up first. A merge from the right that is a copy of the merge from the left with the comparison flipped gets this wrong.
- **The gallop searches.** Searching for the items of $A$ at most an item of $B$ needs the "right" search, and the items of $B$ less than an item of $A$ need the "left" search. Mixing them up breaks the stability but not the sorting, so the bug is easy to miss: test stability.
- **Comparisons that are not consistent.** Java's TimSort throws "Comparison method violates its general contract" when it detects an inconsistent comparator. Make sure the comparator is a total order.

## Implementations

## History

Tim Peters wrote Timsort in 2002 for Python 2.3, and he documented the design and its measurements in listsort.txt, crediting the idea of galloping to McIlroy's 1993 paper on optimistic sorting. Java adopted it for objects in Java 7, and Android, V8 and others followed. In 2015, de Gouw et al. tried to verify the Java code with the KeY system, found that the invariant of the run stack can fail, and built inputs that crash the Java sort. Auger, Jugé, Nicaud and Pivoteau gave the first proof of the $O(n \log n)$ bound in 2018, the same year as the Powersort paper of Munro and Wild, whose merge rule CPython adopted in 2022.

## References
