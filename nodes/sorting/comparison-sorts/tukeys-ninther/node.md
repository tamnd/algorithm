---
tag: FC1RHF
kind: technique
slug: tukeys-ninther
name: Tukey's ninther
aliases:
- ninther
- pseudomedian of nine
area: sorting/comparison-sorts
level: core
summary: Chooses a quicksort pivot as the median of three medians of three samples, giving a good approximation of the true median.
prereqs: [median-of-three-pivot]
see_also: [pivot-selection, quicksort, median-of-medians, introsort, bentley-mcilroy-partitioning, randomized-quicksort, quickselect, median]
sources:
  - paper: "John W. Tukey, The ninther, a technique for low-effort robust (resistant) location in large samples, in Contributions to Survey Sampling and Applied Statistics, edited by H. A. David, Academic Press, 1978"
    locator: the definition of the ninther as the median of three medians of three
  - paper: "Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software: Practice and Experience 23(11), 1993"
    locator: the choice of the partitioning element (the ninther for arrays of more than 40 items, and the code of med3)
  - paper: "Mireille Durand, Asymptotic analysis of an optimized quicksort algorithm, Information Processing Letters 85(2), 2003"
    locator: the mean number of comparisons of quicksort with the ninther
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (the median of a sample of 2t + 1 items, for comparison)
---

Tukey's ninther picks a pivot for [quicksort](/quicksort/) as the median of three medians of three. It takes nine items spread over the range, splits them into three groups of three, takes the [median of three](/median-of-three-pivot/) of each group, and returns the median of the three medians. It costs at most 12 comparisons, it always returns an item of rank 4, 5 or 6 among the nine, and on random input it brings the mean cost of quicksort down to about $1.5697\, n \ln n \approx 1.088\, n \lg n$ comparisons. Bentley and McIlroy use it for ranges of more than 40 items, and many library sorts follow them.

## In plain words

To pick a good pivot card, it helps to look at more than one card. The middle of three cards is better than one card. The ninther looks at nine cards. It puts them into three groups of three, finds the middle card of each group, and then takes the middle one of these three middle cards.

This is not always the exact middle of the nine cards, but it is always close to it. It needs only a few looks, fewer than to find the exact middle of nine. So it gives a good pivot for a large row at a low cost.

## When it applies

- **Quicksort on large ranges.** For a range of $m$ items, the 12 comparisons of the ninther are small next to the $m - 1$ comparisons of the partition only when $m$ is large. Bentley and McIlroy use it for $m > 40$.
- **A better pivot than the median of three is worth a few comparisons.** The ninther's pivot is closer to the median, so the partitions are more even.
- **No random generator is wanted, or the input is structured.** Nine items spread over the whole range see more of its shape. Inputs that are sorted, reversed, or made of a few sorted blocks give good pivots.
- **Robust estimates in statistics.** Tukey designed it as a cheap estimate of the median of a large sample.

## The template

MED3 returns the index of the median of three items, as in the [median-of-three pivot](/median-of-three-pivot/), with 2 or 3 comparisons.

```pseudo id=main
NINTHER(A, lo, hi)                           ▷ m = hi − lo ≥ 9; return an index
L1  s ← ⌊m/8⌋;  c ← lo + ⌊m/2⌋
L2  x ← MED3(A, lo, lo + s, lo + 2s)
L3  y ← MED3(A, c − s, c, c + s)
L4  z ← MED3(A, hi − 1 − 2s, hi − 1 − s, hi − 1)
L5  return MED3(A, x, y, z)
```

Lines L2 to L4 look at nine indices spread about $m/8$ apart, from the first to the last item of the range. Line L5 takes the median of the three medians. The routine changes nothing in the array. The caller swaps the item at the returned index to the place where its partition expects the pivot, as in the template of [pivot selection](/pivot-selection/).

**The rank among the nine.** Let $p$ be the returned item, the median of the medians $x, y, z$. At least one other median is at most $p$, and each median is at least one other item of its group. So at least 3 of the other 8 items are at most $p$, and in the same way at least 3 are at least $p$. So $p$ has rank 4, 5 or 6 among the nine. Over the $9!$ orders of nine distinct items, the rank is 5 in $207{,}360$ orders, which is a fraction of $4/7$, and it is 4 or 6 in $77{,}760$ orders each, a fraction of $3/14$ each.

**The cost.** Four calls of MED3 make at most 12 comparisons, and $4 \cdot 8/3 = 32/3 \approx 10.7$ on average for distinct items in random order.

**The mean cost of quicksort.** For large $m$, the ninther of a random range is the median of three medians of three uniform values. Its distribution has the density $6 G(u)(1 - G(u))\, g(u)$ on $[0, 1]$, where $g(u) = 6u(1-u)$ and $G(u) = 3u^2 - 2u^3$ are the density and the distribution function of a median of three. The leading term of the mean number of comparisons of quicksort is $n \ln n$ divided by the mean of $-(u \ln u + (1-u) \ln(1-u))$ under this density. The value is about $1.5697\, n \ln n$, as Durand computes.

| pivot rule | items looked at | leading term of the comparisons |
|---|---|---|
| one random item | 1 | $2 n \ln n \approx 1.386\, n \lg n$ |
| median of three | 3 | $\tfrac{12}{7} n \ln n \approx 1.188\, n \lg n$ |
| ninther | 9 | $1.5697\, n \ln n \approx 1.088\, n \lg n$ |
| exact median of 9 | 9 | $n \ln n / (H_{10} - H_5) \approx 1.074\, n \lg n$ |

The exact median of 9 random items is a little better, but it needs more comparisons to find.

## Classic examples

**Nine items.** Take the groups $(1, 2, 9)$, $(3, 4, 8)$ and $(5, 6, 7)$. Their medians are 2, 4 and 6, and the ninther is 4. The true median of the nine items is 5, so here the ninther has rank 4. For the groups $(2, 9, 4)$, $(7, 1, 8)$ and $(3, 6, 5)$, the medians are 4, 7 and 5, and the ninther is 5, the true median.

**A sorted range.** On a sorted range of $m = 81$ items $0, 1, \ldots, 80$, we have $s = 10$ and $c = 40$. The nine indices are $0, 10, 20$, then $30, 40, 50$, then $60, 70, 80$. The medians are 10, 40 and 70, and the ninther is 40, the true median. The same holds for a reversed range.

**Bentley and McIlroy's sort.** Their quicksort takes the middle item for ranges of at most 7 items, the median of the first, middle and last items for 8 to 40 items, and the ninther for more than 40 items. It also uses the [Bentley-McIlroy partition](/bentley-mcilroy-partitioning/) for equal keys. Many library sorts of the C language and others descend from this code.

## Variations

- **Random positions.** Take the nine items at random indices. Then the distribution of the rank holds for each input, and no fixed input is bad on purpose.
- **Repeated ninthers.** Apply the idea again: the median of three ninthers looks at 27 items, and so on. Each level brings the pivot closer to the median. Tukey and later authors use this to estimate the median of a very large sample in one pass.
- **Adapt the sample to the size.** Some sorts use the median of three for small ranges, the ninther for medium ranges, and a sample of size about $\sqrt m$ for very large ranges.
- **For selection.** [Quickselect](/quickselect/) can use the ninther as its pivot. It is cheap, but it is not a guarantee: only the [median of medians](/median-of-medians/), with groups of 5 and recursion, gives a linear worst case.

## Pitfalls

- **It is not the median.** The ninther has rank 4 or 6 among the nine in $3/7$ of the cases, and the nine items are only a sample. Do not use it where the exact median is needed.
- **Still a fixed rule.** With fixed positions, an adversary can build inputs that are quadratic, as for the median of three. Use random positions or [introsort](/introsort/) when the input can be hostile.
- **Small ranges.** For $m < 9$, some of the nine indices are the same, and the cost is not worth it below about 40 items. Use the median of three or insertion sort there.
- **Index arithmetic.** The indices must stay in $[lo, hi)$. With $s = \lfloor m/8 \rfloor$ and $m \ge 9$, the largest index is $hi - 1$ and the least is $lo$. Compute the middle as $lo + \lfloor m/2 \rfloor$ to avoid an overflow of $lo + hi$.
- **Equal keys.** The ninther does not help a two-way partition that puts all equal keys on one side. Use a three-way partition.

## Exercises

1. Show that the ninther of nine distinct items is never of rank 1, 2, 3, 7, 8 or 9, by the argument of the template.
2. Count the orders of nine distinct items for which the ninther is the true median, and check that the fraction is $4/7$.
3. On the range $[0, 1, \ldots, m-1]$ with $m = 8k + 1$, show that NINTHER returns the index of the true median.
4. Show that the ninther needs at most 12 comparisons, and find an order of nine items for which it needs exactly 12.
5. Show that the median of three ninthers, from 27 items, has a rank between 8 and 20 among the 27 items.

## References
