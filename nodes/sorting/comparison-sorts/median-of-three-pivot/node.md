---
tag: VWP3T9
kind: technique
slug: median-of-three-pivot
name: Median-of-three pivot
aliases:
- Median-of-3 partition
area: sorting/comparison-sorts
level: core
summary: A quicksort pivot rule that takes the median of three chosen elements, improving the split quality and reducing the chance of bad partitions.
prereqs: [pivot-selection]
see_also: [tukeys-ninther, quicksort, randomized-quicksort, introsort, median-of-medians, hoare-partition, lomuto-partition, quickselect]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (the median-of-three rule, credited to Singleton, and the mean of 12/7 n ln n comparisons)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (Median-of-three partitioning, among the improvements)
  - paper: "R. C. Singleton, Algorithm 347: An efficient algorithm for sorting with minimal storage, Communications of the ACM 12(3), 1969"
    locator: the choice of the median of the first, middle and last items
  - paper: "David R. Musser, Introspective sorting and selection algorithms, Software: Practice and Experience 27(8), 1997"
    locator: the median-of-3 killer sequences
---

The median-of-three rule picks the [quicksort](/quicksort/) pivot as the median of three items of the range, usually the first, the middle and the last. It costs at most 3 comparisons. It makes sorted and reversed inputs fast, it never picks the least or the largest item of a range of 3 or more distinct items, and on random input it cuts the mean number of comparisons from about $2 n \ln n$ to about $\tfrac{12}{7} n \ln n$, which is about 14% less. It is a deterministic rule, so some inputs are still quadratic. It is one of the rules of [pivot selection](/pivot-selection/), and [Tukey's ninther](/tukeys-ninther/) applies it twice.

## In plain words

Quicksort works best when its pivot card is near the middle of the cards. A card from one fixed place can be far from the middle. So look at three cards, the first, the middle and the last, and take the one whose value is between the other two.

The middle one of three cards is never the smallest or the largest card of the row. On a row that is already in order, it is exactly the middle card. On a row in random order, it is more often near the middle than one card picked alone. The extra cost is a few looks at each step, and the saving is larger.

## When it applies

- **A quicksort or quickselect on arrays** with $O(1)$ access to the first, the middle and the last item.
- **The input may be sorted, reversed, or almost sorted.** These orders are common, and the fixed first-item or last-item rules are quadratic on them.
- **A random generator is not wanted.** The rule is deterministic, so a run is repeatable, and no generator is called in the inner loop.
- **The ranges are of moderate size.** For very large ranges, a larger sample such as the ninther gives better pivots. For ranges of fewer than about 10 items, [insertion sort](/insertion-sort/) is better than any partition.

## The template

```pseudo id=main
MEDIAN-OF-THREE(A, lo, hi)                 ▷ hi − lo ≥ 3; return an index
L1  i ← lo;  j ← ⌊(lo + hi)/2⌋;  k ← hi − 1
L2  if A[j] < A[i] then swap i and j       ▷ now A[i] ≤ A[j]
L3  if A[k] < A[j] then
L4      j ← k                              ▷ A[k] is below A[j]
L5      if A[j] < A[i] then j ← i          ▷ the median is the larger of A[i] and A[k]
L6  return j
```

The routine swaps indices, not items, so it does not change the array. After line L2, $A[i] \le A[j]$. If also $A[j] \le A[k]$, then $A[j]$ is the median. Otherwise $A[k] < A[j]$, and the median is the larger of $A[i]$ and $A[k]$, which lines L4 and L5 pick. It makes 2 or 3 comparisons. On three distinct items in random order, it makes 2 comparisons with probability $1/3$, so $8/3$ on average.

The caller swaps $A[j]$ to the place where the partition expects the pivot, as in the template of [pivot selection](/pivot-selection/), and partitions. Ranges of 2 items use any pivot.

**Sentinels.** Many programs sort the three items in place instead, so that $A[lo] \le A[mid] \le A[hi-1]$, and then swap the median to $A[hi-2]$. Now $A[lo]$ is at most the pivot and $A[hi-1]$ is at least the pivot, so the inner scans of a [Hoare partition](/hoare-partition/) on $A[lo+1 \ldots hi-3]$ need no test for the ends of the range. Sedgewick's and Knuth's versions use this trick.

**The mean cost.** On a uniform random permutation of $n$ distinct items, the median of three items in fixed places has the rank distribution of the median of three random items. A range of $m$ items then has the pivot rank $r$ with probability $6(r-1)(m-r)/(m(m-1)(m-2))$. With this distribution, the recurrence of the partition comparisons has the leading term $\tfrac{12}{7} n \ln n \approx 1.188\, n \lg n$ (Knuth, Section 5.2.2), against $2 n \ln n \approx 1.386\, n \lg n$ for one random pivot. The analysis assumes that each part is again in uniform random order. For $n = 1000$ the recurrence gives about $9{,}315$ partition comparisons, close to the mean of about $9{,}340$ that the Lomuto partition with this rule makes on random inputs.

## Classic examples

**A short array.** Sort $A = [6, 3, 9, 1, 7, 2, 8, 5]$ with the Lomuto partition and the median of three.

| range | first, middle, last | pivot | partition comparisons |
|---|---|---|---|
| 6 3 9 1 7 2 8 5 | 6, 7, 5 | 6 | 7 |
| 5 3 1 2 | 5, 1, 2 | 2 | 3 |
| 5 3 | (2 items, the last item) | 3 | 1 |
| 9 8 7 | 9, 8, 7 | 8 | 2 |

The partitions make 13 comparisons, against 15 with the last item as pivot. The three medians add at most 9 more, so on so small an input the rule does not pay. It pays on large ranges, where 3 comparisons are small next to the $m - 1$ of the partition.

**A sorted input.** On $[0, 1, \ldots, 14]$, quicksort with the last item makes $105$ partition comparisons. With the median of three, the first pivot is the middle item 7, and the partitions make 34 comparisons. For $n = 1000$ sorted items, the partitions make $7{,}987$ comparisons, against $499{,}500$ with the last item.

**A random input.** On random permutations of 1000 items, the partitions make about $9{,}340$ comparisons on average, against about $10{,}986$ with a random pivot.

**In libraries.** Singleton (1969) proposed the median of the first, middle and last items. Sedgewick and Wayne list it among the improvements of quicksort, and Bentley and McIlroy use it for ranges of 8 to 40 items, with the ninther for larger ranges. [Introsort](/introsort/) in C++ libraries also uses a median of three.

## Variations

- **Three random items.** Take the median of three random items. Then the mean of $\tfrac{12}{7} n \ln n$ holds on every input, not only on random ones, and no input is bad on purpose.
- **[Tukey's ninther](/tukeys-ninther/).** Take the median of three medians of three. It looks at 9 items and gives a pivot nearer the median, at the cost of up to 12 comparisons.
- **Larger samples.** The median of $2t + 1$ items gives a leading term of $n \ln n / (H_{2t+2} - H_{t+1})$. For 5 items this is about $1.124\, n \lg n$.
- **For selection.** [Quickselect](/quickselect/) with the median of three makes fewer comparisons on average than with one random pivot, but it is still quadratic in the worst case. The [median of medians](/median-of-medians/) gives the linear worst case.

## Pitfalls

- **Killer inputs.** Musser (1997) gives inputs, the median-of-3 killer sequences, on which quicksort with this rule takes $\Theta(n^2)$ time. A deterministic rule always has bad inputs. Use [introsort](/introsort/) or random items when an attacker can choose the input.
- **Equal keys.** The rule does not help when many keys are equal and the partition puts all of them on one side. Use a three-way or Hoare partition.
- **Lost items when sorting the three.** In the sentinel form, the three items are swapped in place. If the code then also swaps the median with $A[hi - 1]$ instead of $A[hi - 2]$, the sentinel at the end is lost, and the scan can run past the range.
- **Ranges that are too small.** For fewer than 3 items there is no median of three, and the middle index can equal an end. Handle small ranges first, usually with insertion sort.
- **An overflow in the middle index.** In a language with fixed-size integers, $(lo + hi)/2$ can overflow. Use $lo + (hi - lo)/2$.

## Exercises

1. Prove that MEDIAN-OF-THREE returns the index of a median of $A[i], A[j], A[k]$ for each order of the three items, including equal items.
2. Show that on a range of $m \ge 3$ distinct items, the median of three is never the least or the largest item, so each part has at most $m - 2$ items. Conclude that the depth of the recursion is at most about $n/2$.
3. Show that on a sorted input of $n = 2^k - 1$ items, quicksort with the median of three and a partition that keeps the parts in order takes each pivot at the middle of its range. How many partition comparisons does it make?
4. Use the distribution $6(r-1)(m-r)/(m(m-1)(m-2))$ to show that the expected size of the larger part is about $11m/16$, against $3m/4$ for one random pivot.
5. Show that the median of three is at most 3 comparisons, and that no method finds the median of three distinct items in 2 comparisons in the worst case.

## References
