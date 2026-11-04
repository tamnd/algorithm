---
tag: QN966N
kind: algorithm
slug: burstsort
name: Burstsort
aliases:
- Burst sort
- String burst sort
area: sorting/distribution-sorts
level: advanced
summary: Cache-efficient string sort that builds a trie of buckets which burst into subtries as they grow.
solves: [string-sorting]
model: word-ram
complexity:
  vars: {n: the number of strings, D: the total length of the distinguishing prefixes, R: the alphabet size, T: the bucket threshold}
  time: {worst: "O(n T + D T + R (n + D) / T)", average: "O(n log T + D + R (n + D) / T)"}
  space: {extra: "O(n + R (n + D) / T)"}
properties: {stable: false, in_place: false, adaptive: true, online: true, deterministic: false, comparison: false, recursive: false}
history: {year: 2003, people: [Ranjan Sinha, Justin Zobel], note: string sorting with a burst trie for cache efficiency}
prereqs: [trie, msd-radix-sort]
see_also: [burst-trie, trie, msd-radix-sort, multikey-quicksort, american-flag-sort, string-sorting, cache-oblivious-model, radix-tree]
sources:
  - paper: Ranjan Sinha and Justin Zobel, Cache-conscious sorting of large sets of strings with dynamic tries, ACM Journal of Experimental Algorithmics 9, 2004 (first presented at ALENEX 2003)
    locator: the description of burstsort (insertion into a burst trie, the bursting of a container above a threshold, and the in-order traversal that sorts each container with multikey quicksort) and the experiments on cache misses
  - paper: Steffen Heinz, Justin Zobel and Hugh E. Williams, Burst tries, a fast, efficient data structure for string keys, ACM Transactions on Information Systems 20(2), 2002, pages 192 to 223
    locator: the definition of the burst trie (access trie, containers, burst heuristics) on which burstsort is built
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.1, String Sorts (MSD string sort and three-way string quicksort, the methods that burstsort combines), and Section 5.2, Tries
---

Burstsort is a string sort that inserts the strings, one at a time, into a [burst trie](/burst-trie/): a [trie](/trie/) whose leaves are small unsorted buckets. When a bucket grows past a threshold $T$, it *bursts*: it becomes a trie node, and its strings move into new buckets by their next character. At the end, a traversal of the trie in order of the characters visits the buckets in sorted order, and each bucket is sorted on its own, usually with [multikey quicksort](/multikey-quicksort/). Sinha and Zobel (2003) designed it to use the cache well: the trie stays small, each string is read in order from memory, and each bucket fits in cache when it is sorted.

## In plain words

Imagine a mail room with a set of trays, one per first letter. Each incoming letter goes to the tray of the first letter of the name. When one tray gets too full, you replace it with a small rack of trays, one per second letter, and move the letters of the full tray into the rack. Later letters for that first letter go straight to the rack.

At the end, each tray holds only a few letters, all with the same start. Walk through the trays from A to Z, and inside each rack in the same order. Sort each small tray by hand, then put the letters in a row. The rack system keeps the work on each tray small, and small trays are fast to sort.

## The problem

The input is an array $A[0 \ldots n-1]$ of strings over $\{0, \ldots, R-1\}$. The output is the strings in [lexicographic order](/lexicographic-order/). As in [MSD radix sort](/msd-radix-sort/), $c(s, d) = s[d] + 1$ if $d < |s|$ and $c(s, d) = 0$ if $s$ has ended, so slot 0 is for strings that end and comes first.

## The algorithm

A trie node at depth $d$ has $R + 1$ slots, indexed by $c(\cdot, d)$. A slot is empty, holds a bucket (a list of strings), or holds a child node at depth $d + 1$.

```pseudo id=main
BURSTSORT(A, n, R, T)
L1  root ← a new node with R + 1 empty slots
L2  for each string s of A do
L3      v ← root; d ← 0
L4      while slot c(s, d) of v holds a node do v ← that node; d ← d + 1
L5      append s to the bucket in slot r = c(s, d) of v, creating it if needed
L6      if r ≠ 0 and the bucket has more than T strings then BURST(v, r, d + 1)
L7  k ← 0
L8  for each bucket B, in slot r of a node at depth d, in depth-first order of the slots do
L9      if r ≠ 0 then sort B by the suffixes from index d + 1
L10     copy B to A[k .. k + |B| − 1]; k ← k + |B|
L11 return A

BURST(v, r, d)
    u ← a new node with R + 1 empty slots
    for each string s of the bucket in slot r of v do append s to the bucket in slot c(s, d) of u
    replace the bucket in slot r of v by u
```

Every string in the bucket of slot $r \ge 1$ of a node at depth $d$ has the same first $d$ characters as the path to the node, and character $r - 1$ at index $d$. So the strings of a bucket agree on $d + 1$ characters, and line L9 sorts them by the rest. The bucket of slot 0 holds strings that ended at $d$; they are all equal, so they are never sorted and never burst. A traversal that visits the slots of each node in increasing order, and goes into a child node before the next slot, visits the buckets in lexicographic order.

## Example

Sort $A = [\text{she}, \text{sells}, \text{sea}, \text{shells}, \text{by}, \text{the}, \text{sea}, \text{shore}]$ with $T = 2$.

| String | Path | Bucket after the insert | Burst |
|---|---|---|---|
| she | root, s | she | no |
| sells | root, s | she sells | no |
| sea | root, s | she sells sea | yes, at depth 1: slot e gets sells sea, slot h gets she |
| shells | root, s, h | she shells | no |
| by | root, b | by | no |
| the | root, t | the | no |
| sea | root, s, e | sells sea sea | yes, at depth 2: slot l gets sells, slot a gets sea sea |
| shore | root, s, h | she shells shore | yes, at depth 2: slot e gets she shells, slot o gets shore |

The traversal visits the buckets by, then sea sea (slot a under s, e: sorted by the suffixes from index 3, which are both empty), sells, she shells (slot e under s, h: sorted by the suffixes from index 3, the empty string and lls), shore and the. The output is $[\text{by}, \text{sea}, \text{sea}, \text{sells}, \text{she}, \text{shells}, \text{shore}, \text{the}]$.

## Correctness

Each bucket holds strings that share the path to it, so all strings of one bucket agree on the characters of the path. Two strings in different buckets differ in the first slot where their paths split, or one of them ends there, and the traversal visits the smaller slot first. So the buckets come out in lexicographic order, and inside a bucket line L9 sorts by the part that is not yet fixed. A burst keeps the property, because it moves each string to the slot of its next character. Each string is inserted once and moves down in a burst at most once per character, so the method ends. The full proof is below.

## Complexity

Burstsort is an engineering method, and Sinha and Zobel judge it mainly by experiments. Simple bounds follow from the structure.

- **Insertion.** A string walks down the trie for at most $\ell(s) + 1$ levels, where $\ell(s)$ is the length of its distinguishing prefix, because a node at depth $d$ exists only if at least $T + 1 \ge 2$ strings share a prefix of length $d$. So the walks cost $O(n + D)$.
- **Bursts.** A burst moves each string of a bucket one level down. Each string moves at most $\ell(s) + 1$ times, so all bursts move $O(n + D)$ strings, and there are at most $(n + D)/(T + 1)$ bursts. Each burst creates a node of $R + 1$ slots, which costs $O(R(n + D)/T)$ in total for the nodes and for the traversal.
- **Bucket sorts.** At the end each bucket has at most $T + 1$ strings. Multikey quicksort on a bucket of $m$ strings costs $O(m \log m + D_B)$ in expectation, where $D_B$ is the part of $D$ for that bucket, so the total is $O(n \log T + D)$ in expectation.
- **Total.** $O(n \log T + D + R(n + D)/T)$ expected. A threshold of a few thousand strings makes the node cost small next to the rest.
- **Cache.** The trie has few nodes, so it stays in cache during the insertion phase, and each bucket of at most $T$ strings is small enough to sort in cache. Sinha and Zobel report large savings in cache misses over MSD radix sort and multikey quicksort on large sets of strings.

## Properties

- **Not stable.** The bucket sort is not stable.
- **Not in place.** The trie and the buckets take $O(n + R(n + D)/T)$ extra space.
- **Online.** The insertion phase takes the strings one at a time, so it can run while the input arrives.
- **Adaptive.** Bursts happen only where many strings share a prefix, so the trie follows the data.
- **Not a comparison sort.** Characters are slot indices in the trie.

## Variants and improvements

- **Copy-based burstsort.** Sinha, Ring and Zobel store the string suffixes inside the buckets, not only pointers, so the bucket sort does not follow pointers to strings that are far apart in memory. This removes most of the remaining cache misses.
- **Sampling.** Build the trie from a sample of the strings first, then insert all strings into the fixed trie. This avoids repeated bursts of the same buckets.
- **Bucket representation.** Buckets as growing arrays use the cache better than linked lists.
- **Parallel burstsort.** The buckets are independent once the trie is built, so they can be sorted in parallel.

## When to use it

Use burstsort for very large sets of strings in memory, such as the words of a large text collection or URLs, where cache misses dominate the cost of other string sorts. For small inputs, [multikey quicksort](/multikey-quicksort/) or [MSD radix sort](/msd-radix-sort/) is simpler and fast enough.

## Pitfalls

- **Bursting slot 0.** The strings that ended at a node are all equal. Bursting their bucket would put them all in slot 0 again, and the burst would never stop.
- **Sorting from the wrong index.** A bucket in slot $r$ of a node at depth $d$ agrees on $d + 1$ characters. Sorting from index $d$ is correct but slower; sorting from a larger index is wrong.
- **A threshold too small.** With $T$ small, each burst creates a node of $R + 1$ slots for few strings, and the trie becomes large and slow.
- **A threshold too large.** With $T$ large, the buckets do not fit in cache, which removes the point of the method.

## Implementations

## History

Heinz, Zobel and Williams introduced the burst trie in 2002 as a fast structure for sets of string keys. Sinha and Zobel turned it into a sort, burstsort, presented at ALENEX 2003 and in the ACM Journal of Experimental Algorithmics. Later papers of Sinha with Ring and Zobel added the copy-based form and other refinements.

## References
