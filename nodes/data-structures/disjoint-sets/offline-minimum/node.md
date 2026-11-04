---
tag: SM7G4C
kind: problem
slug: offline-minimum
name: Offline minimum
area: data-structures/disjoint-sets
level: advanced
summary: Given a sequence of inserts and extract-min operations, determine offline which key each extraction returns using disjoint-set union.
prereqs: [disjoint-set-forest, offline-algorithm, binary-heap]
see_also: [offline-subarray-painting, static-tree-set-union, gabow-tarjan-union-find, dynamic-equivalence-problem, offline-query-processing, binary-heap, arpa-offline-rmq]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19, the problem on the off-line minimum at the end of the chapter
  - paper: doi:10.1016/0022-0000(85)90014-5
    title: "Harold N. Gabow and Robert E. Tarjan, A linear-time algorithm for a special case of disjoint set union, Journal of Computer and System Sciences 30(2) (1985), 209-221"
    locator: the applications of static tree set union, among them the off-line minimum problem
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 4, the off-line MIN problem as an application of the set union algorithm
---

The offline minimum problem gives a sequence of INSERT and EXTRACT-MIN operations on a set of keys, all known in advance, and asks which key each EXTRACT-MIN returns. A [binary heap](/binary-heap/) answers it online in $O(n \log n)$ time. Because the whole sequence is known, the problem can be turned around: take the keys in increasing order, and give each key to the first extraction after its insertion that has not yet received a key. A [disjoint-set forest](/disjoint-set-forest/) on the extractions finds that extraction, so the whole problem takes $O(n\,\alpha(n))$ time after the keys are sorted, and $O(n)$ with the [Gabow-Tarjan](/gabow-tarjan-union-find/) structure. It is a classic exercise of CLRS and of Aho, Hopcroft and Ullman.

## In plain words

People put numbered cards into a box, and now and then someone takes out the smallest card in the box. You get the whole log of who put what and when someone took a card, but not which card each taker got. You must work it out.

Go through the cards from the smallest to the largest. The smallest card goes to the first taker after the moment it was put in. The next card goes to the first taker after its moment who has no card yet. And so on. A card that finds no free taker stays in the box.

To find "the next taker with no card yet" fast, each taker who already has a card points to the next taker. You follow the pointers and shorten them as you go.

## Definition

**Input.** A sequence $S$ of $n$ operations INSERT$(k)$ and $m$ operations EXTRACT-MIN, where the keys $k$ are distinct. After a sort, take the keys to be $1, \ldots, n$. Write $S$ as

$$S = I_1\ \mathrm{E}\ I_2\ \mathrm{E}\ \cdots\ I_m\ \mathrm{E}\ I_{m+1},$$

where E is one EXTRACT-MIN and each $I_j$ is a block of INSERT operations, possibly empty.

**Output.** The array $\mathrm{extracted}[1..m]$, where $\mathrm{extracted}[j]$ is the key that the $j$-th EXTRACT-MIN returns when $S$ is run on a priority queue that starts empty, or NONE if the queue is empty then.

The problem is *offline*: the whole of $S$ is given before any output is needed.

**The union-find method.** Let $\mathrm{blk}(i)$ be the index $j$ of the block $I_j$ that inserts key $i$. Keep a forest on the indices $1, \ldots, m + 1$, where $m + 1$ is a sentinel. An extraction $j$ is a root while it has no key. The root of $j$ is then the first extraction at or after $j$ with no key yet.

```pseudo
OFFLINE-MINIMUM(S)
    for j ← 1 to m + 1 do p[j] ← j; extracted[j] ← NONE
    for i ← 1 to n do                      ▷ keys in increasing order
        j ← FIND(blk(i))
        if j ≤ m then
            extracted[j] ← i
            p[j] ← j + 1                    ▷ extraction j is used; link it to the next one
    return extracted[1..m]
```

This is the method of CLRS, there phrased as sets of keys $K_j$: key $i$ is in the set $K_j$ of its extraction, and when $j$ gets its key, $K_j$ is merged into the next set that still exists.

**Why it is right.** Claim: the $j$-th extraction returns the least key $i$ such that $\mathrm{blk}(i) \le j$ and $i$ is not returned by an extraction before $j$. This holds because the queue at that time holds exactly the keys inserted before it and not yet removed. Now take the keys in increasing order. When key $i$ is processed, every smaller key already has its extraction. The extractions at or after $\mathrm{blk}(i)$ that have no key yet are exactly those whose queue, at their time, contains $i$ and no smaller key; the first of them returns $i$. If there is none, $i$ is never extracted.

## Variants

- **Online.** If the answers are needed one at a time, use a [binary heap](/binary-heap/) or another priority queue, in $O(\log n)$ time per operation.
- **Offline maximum.** Take the keys in decreasing order.
- **Keys with ties.** Break ties by the order of insertion, which makes the keys distinct.
- **Also deletions or decreases.** The method relies on keys that leave the queue only by extraction. With DELETE of a given key, mark it and skip it in the loop, as it then belongs to no extraction.
- **Deadlines.** The same forest, with links to the left, gives each job the latest free day at or before its deadline. See [painting subarrays offline](/offline-subarray-painting/).

## Examples

**The CLRS sequence.** Let $S$ be

$$4,\ 8,\ \mathrm{E},\ 3,\ \mathrm{E},\ 9,\ 2,\ 6,\ \mathrm{E},\ \mathrm{E},\ \mathrm{E},\ 1,\ 7,\ \mathrm{E},\ 5,$$

where a number is INSERT of that key. Then $n = 9$, $m = 6$, and the blocks are $I_1 = \{4, 8\}$, $I_2 = \{3\}$, $I_3 = \{9, 2, 6\}$, $I_4 = I_5 = \emptyset$, $I_6 = \{1, 7\}$ and $I_7 = \{5\}$. The forest is on $1, \ldots, 7$, with 7 the sentinel.

| key $i$ | $\mathrm{blk}(i)$ | FIND | result | parents of 1 to 7 after it |
|---|---|---|---|---|
| 1 | 6 | 6 | extracted[6] = 1 | 1 2 3 4 5 7 7 |
| 2 | 3 | 3 | extracted[3] = 2 | 1 2 4 4 5 7 7 |
| 3 | 2 | 2 | extracted[2] = 3 | 1 3 4 4 5 7 7 |
| 4 | 1 | 1 | extracted[1] = 4 | 2 3 4 4 5 7 7 |
| 5 | 7 | 7 | stays | |
| 6 | 3 | 3 → 4, so 4 | extracted[4] = 6 | 2 3 4 5 5 7 7 |
| 7 | 6 | 6 → 7, so 7 | stays | |
| 8 | 1 | 1 → 2 → 3 → 4 → 5, so 5 | extracted[5] = 8 | 2 3 4 5 7 7 7 |
| 9 | 3 | 3 → 4 → 5 → 7, so 7 | stays | |

The answer is $\mathrm{extracted} = [4, 3, 2, 6, 8, 1]$, which is what a heap gives when it runs $S$. The table shows the forest without path compression; with compression, the find of key 8 would also point 1, 2 and 3 to 5.

## Known algorithms

| method | time | notes |
|---|---|---|
| run $S$ on a [binary heap](/binary-heap/) | $O(n \log n)$ | also online |
| keys in order, linear scan for the next free extraction | $O(n + nm)$ | no data structure |
| keys in order, [disjoint-set forest](/disjoint-set-forest/) with [path compression](/path-compression/) | $O(n \log n)$ worst case, after the sort | links always go to $j + 1$, so no linking rule; this is the bound for compression alone |
| the same with union by rank and the largest index stored at each root | $O(n\,\alpha(n))$ after the sort | CLRS form, with sets $K_j$ |
| the same with the [Gabow-Tarjan](/gabow-tarjan-union-find/) structure | $O(n)$ after the sort | the links form a fixed path, a case of [static tree set union](/static-tree-set-union/) |

The sort costs $O(n \log n)$ for general keys, so the union-find method is better than a heap only when the keys are already sorted or can be sorted in linear time, for example small integers with radix sort, or when the problem gives the keys as $1, \ldots, n$, as in CLRS.

## Bounds

- **Upper bound.** $O(n + m)$ time on a RAM with words of $\Theta(\log n)$ bits, for keys $1, \ldots, n$, by the [Gabow-Tarjan](/gabow-tarjan-union-find/) algorithm: each extraction $j$ is linked only to $j + 1$, so the tree of the unions is the path $1, 2, \ldots, m + 1$, known in advance.
- **Lower bound.** $\Omega(n + m)$, to read the input.
- **With general keys.** In the comparison model, $\Omega(n \log n)$ comparisons are needed: if $m = n$ and every extraction comes after all the insertions, the answer is the sorted order of the keys.
- **The general union-find bound does not apply.** The [union-find lower bound](/union-find-lower-bound/) needs unions chosen by an adversary. Here their shape is fixed in advance.

## Reductions

- **To interval union-find.** The method does $n$ finds and at most $m$ links of a set with the next set on a line. This is the interval case of [static tree set union](/static-tree-set-union/).
- **Sorting reduces to it.** With all insertions before $n$ extractions, the output is the sorted list of the keys. So the problem with general keys is as hard as sorting.
- **The same forest as painting.** [Painting subarrays offline](/offline-subarray-painting/) uses the same links to the next free position, on cells instead of extractions.
- **Offline processing.** It is an instance of [offline query processing](/offline-query-processing/): process the keys in an order in which each answer is fixed once.

## Applications

- Checking a log of priority queue operations, or replaying it without a heap.
- Scheduling of unit jobs with release times: process the jobs by value, and give each the first free slot at or after its release.
- Computing the matching of a greedy algorithm offline, when items are offered to the first free slot after their arrival.
- An exercise in turning an online problem around, in the style of [offline algorithms](/offline-algorithm/).

## References
