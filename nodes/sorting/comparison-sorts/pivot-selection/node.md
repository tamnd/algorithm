---
tag: BNKMP2
kind: technique
slug: pivot-selection
name: Pivot selection
aliases:
- median-of-three pivot
- pivot strategy
- random pivot
area: sorting/comparison-sorts
level: core
summary: Choice of the partitioning element (first, random, median-of-three, median-of-medians) that controls quicksort's balance.
prereqs: [quicksort]
see_also: [median-of-three-pivot, tukeys-ninther, randomized-quicksort, median-of-medians, quickselect, introsort, dual-pivot-quicksort, sample-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (the choice of the partitioning element, the median of three, and the median of a sample of 2t + 1 items)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (the shuffle, and the improvements with the median of three)
  - paper: "Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software: Practice and Experience 23(11), 1993"
    locator: the choice of the partitioning element (the middle item, the median of three and the ninther)
  - paper: "David R. Musser, Introspective sorting and selection algorithms, Software: Practice and Experience 27(8), 1997"
    locator: the inputs that make median-of-three quicksort quadratic
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 7.3, A randomized version of quicksort, and Section 9.3, Selection in worst-case linear time
---

Pivot selection is the rule that picks the item around which [quicksort](/quicksort/) or [quickselect](/quickselect/) partitions a range. The rule decides how even the split is, and so the cost: a pivot near the median gives about $n \lg n$ comparisons, and a pivot near an end at each step gives $\Theta(n^2)$. The common rules are a fixed position, a random item, the [median of three](/median-of-three-pivot/), [Tukey's ninther](/tukeys-ninther/), the median of a larger sample, and the [median of medians](/median-of-medians/). They trade the cost of the choice against the quality of the split and the safety against bad inputs.

## In plain words

Quicksort picks one card, the pivot, and splits the other cards into a small pile and a large pile. It is fast when the two piles are about the same size, and slow when one pile is almost empty. So the choice of the pivot matters.

To take the first card is fast, but a row that is already in order then always gives a bad split. To take a random card makes bad splits rare on every row. To look at three cards and take the middle one of the three makes good splits more likely. To find the true middle card is possible, but the search costs more than it saves in most programs.

## When it applies

- **An algorithm partitions around one item.** Quicksort, quickselect, and related methods such as [introsort](/introsort/) and [sample sort](/sample-sort/) need a pivot at each step.
- **The cost depends on the rank of the pivot.** A pivot of rank $r$ in a range of $m$ items leaves parts of sizes $r - 1$ and $m - r$. The total cost is a sum over these splits.
- **The input order is unknown or hostile.** A fixed rule is bad on some inputs. If those inputs are common, such as sorted data, or can be built by an attacker, the rule must be random or must give a guarantee.
- **The choice must be cheap.** The rule runs at each call, so it must cost $O(1)$ or at most $O(m)$ for a range of $m$ items.

## The template

```pseudo id=main
PARTITION-STEP(A, lo, hi)                    ▷ m = hi − lo ≥ 2
L1  q ← CHOOSE-PIVOT(A, lo, hi)              ▷ hole: the rule; lo ≤ q < hi
L2  swap A[q] and A[hi − 1]                  ▷ the partition expects the pivot at the end
L3  p ← PARTITION(A, lo, hi)                 ▷ for example the Lomuto partition
L4  return p
```

The only hole is CHOOSE-PIVOT. It returns an index in the range, and line L2 moves that item to the place where the partition expects the pivot. For the [Hoare partition](/hoare-partition/) or a partition with the pivot at $A[lo]$, line L2 swaps it there instead. Correctness does not depend on the rule: each rule that returns an index in the range gives a correct sort, because PARTITION works for each pivot. Only the time changes.

**The cost of a rule.** Let $C(m)$ be the expected number of comparisons of quicksort on a range of $m$ items. If the pivot has rank $r$ with probability $\pi_m(r)$, then

$$C(m) = (m - 1) + c(m) + \sum_{r=1}^{m} \pi_m(r) \big( C(r - 1) + C(m - r) \big),$$

where $c(m)$ is the cost of the rule. A random pivot has $\pi_m(r) = 1/m$, and the solution is $C(n) = 2(n+1)H_n - 4n \approx 2 n \ln n$. The median of a random sample of $2t + 1$ items has $\pi_m(r) = \binom{r-1}{t} \binom{m-r}{t} / \binom{m}{2t+1}$, and the leading term of $C(n)$ becomes $n \ln n / (H_{2t+2} - H_{t+1})$, where $H_k$ is a [harmonic number](/harmonic-series/). This is the result of Knuth, Section 5.2.2, and it counts the partition comparisons; the cost of the sample is in the lower terms for a fixed $t$.

| rule | sample | leading term of the comparisons |
|---|---|---|
| random item | 1 | $2 n \ln n \approx 1.386\, n \lg n$ |
| median of 3 random items | 3 | $\tfrac{12}{7} n \ln n \approx 1.188\, n \lg n$ |
| median of 5 random items | 5 | $\tfrac{60}{37} n \ln n \approx 1.124\, n \lg n$ |
| exact median | $m$ | $n \lg n$ for the partitions, plus the cost of the selection |

As $t$ grows, $H_{2t+2} - H_{t+1} \to \ln 2$, so the leading term tends to $n \lg n$, the [lower bound](/comparison-sort-lower-bound/). A sample of size about $\sqrt{m}$ reaches $n \lg n + o(n \log n)$.

## Classic examples

- **The last item or the first item.** CLRS uses the last item with the [Lomuto partition](/lomuto-partition/), and Hoare's first quicksort used a fixed position. The cost is $O(1)$. On a sorted or reversed input each pivot is the least or the largest item, and quicksort makes $n(n-1)/2$ comparisons. On a random input it is as good as a random pivot.
- **The middle item.** Take $A[\lfloor (lo + hi)/2 \rfloor]$. Sorted and reversed inputs now give good splits. But the rule is fixed, so other inputs still give bad splits, and anyone who knows the rule can build them.
- **A random item.** Take a uniform random index, as in [randomized quicksort](/randomized-quicksort/). The expected cost is $2(n+1)H_n - 4n$ on every input of distinct keys, and no fixed input is bad.
- **The median of three.** Take the median of the first, the middle and the last item. Sorted and reversed inputs give perfect splits, and on random input the cost falls to about $\tfrac{12}{7} n \ln n$. Sedgewick and Wayne and many libraries use it. See [median-of-three pivot](/median-of-three-pivot/).
- **Tukey's ninther.** Take the median of the medians of three groups of three items. Bentley and McIlroy use it for ranges of more than 40 items. It looks at 9 items with at most 12 comparisons. See [Tukey's ninther](/tukeys-ninther/).
- **The median of medians.** Split the range into groups of 5, take the median of each group, and find the median of these medians by recursion. The pivot then has a rank between about $3m/10$ and $7m/10$, so quicksort is $O(n \log n)$ in the worst case and quickselect is $O(n)$ in the worst case. The constant is large, so sorts rarely use it. See [median of medians](/median-of-medians/).
- **Two pivots.** [Dual-pivot quicksort](/dual-pivot-quicksort/) takes two pivots, often the second and fourth of five sampled items, and splits into three parts.

## Variations

- **Choose for selection, not for sorting.** In quickselect, only one side is kept, so a bad split costs more. A sample-based pivot near the rank $k$ that is sought, as in the Floyd-Rivest algorithm, saves more than a pivot near the median.
- **Adapt the rule to the size.** Bentley and McIlroy use the middle item for ranges of at most 7 items, the median of three up to 40 items, and the ninther above that.
- **Fall back on a bad split.** [Introsort](/introsort/) keeps a cheap rule and switches to [heapsort](/heapsort/) when the depth exceeds about $2 \lg n$. Pattern-defeating quicksort shuffles some items when a split is very uneven.
- **Sample once.** [Sample sort](/sample-sort/) chooses many pivots from one sample, and uses them to split the input into many buckets at once.

## Pitfalls

- **Fixed rules on common inputs.** The first or last item is quadratic on sorted and reversed data, which are frequent in practice. Do not use a fixed end position on unknown data.
- **Hostile inputs for the median of three.** Musser (1997) shows inputs that make median-of-three quicksort take $\Theta(n^2)$ time. A deterministic rule always has such inputs, so a service that sorts data from users needs a random rule or a worst-case fallback.
- **Many equal keys.** No pivot rule helps when the partition sends all items equal to the pivot to one side. With the Lomuto partition, an array of equal items is quadratic for every rule. Use a [three-way partition](/three-way-quicksort/).
- **A rule that costs too much.** The exact median of each range keeps the comparisons near $n \lg n$, but the selection costs more than it saves. A sample of fixed size, or of size about $\sqrt{m}$, is the practical balance.
- **Moving the pivot to the wrong place.** The rule returns an index, and the partition expects the pivot at a fixed place. Forgetting the swap of line L2 partitions around the wrong item, and the sort can loop forever or lose the pivot's place.

## Exercises

1. Compute the comparisons of quicksort with the middle-item rule, the swap of line L2 and the Lomuto partition on $[1, 2, \ldots, 7]$. (The answer is 10, against 21 for the last-item rule.)
2. Prove that with the median of three of the first, middle and last items, the pivot is never the least or the largest item of a range of at least 3 distinct items. Conclude that each part has at most $m - 2$ items.
3. Use the formula of the template to show that the median of three random items gives $\pi_m(r) = 6(r-1)(m-r)/(m(m-1)(m-2))$.
4. Show that $H_{2t+2} - H_{t+1} \to \ln 2$ as $t \to \infty$, and so the leading term of the comparisons tends to $n \lg n$.
5. Build an input of 8 distinct keys on which quicksort with the last-item rule and the Lomuto partition makes 28 comparisons, and one on which it makes the least number, which is 13.

## References
