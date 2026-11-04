---
tag: 0V80XQ
kind: algorithm
slug: han-integer-sort
name: Han's integer sorting
aliases:
- Deterministic O(n log log n) integer sort
area: sorting/distribution-sorts
level: research
summary: Deterministic word-RAM algorithm that sorts n integers of w bits in O(n log log n) time.
solves: [integer-sorting]
model: word-ram
complexity:
  vars: {n: the number of keys, m: the size of the key range, w: the word length in bits}
  time: {worst: O(n log log n), average: O(n log log n), best: O(n log log n)}
  space: {extra: O(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: true}
prereqs: [integer-sorting, word-ram, radix-sort]
see_also: [han-thorup-integer-sort, integer-sorting, radix-sort, fusion-tree, predecessor-problem, priority-queue, bit-parallelism, word-ram]
sources:
  - paper: doi:10.1016/j.jalgor.2003.09.001
    title: Yijie Han, Deterministic sorting in O(n log log n) time and linear space, Journal of Algorithms 50(1), 2004, pages 96 to 105
    locator: the abstract, the introduction (the comparison with earlier bounds), and the sections on passing integers down the exponential search tree in batches
  - paper: doi:10.1145/509907.509993
    title: Yijie Han, Deterministic sorting in O(n log log n) time and linear space, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC 2002), pages 602 to 608
    locator: the conference version, abstract and introduction
  - paper: doi:10.1006/jcss.1998.1580
    title: Arne Andersson, Torben Hagerup, Stefan Nilsson and Rajeev Raman, Sorting in linear time?, Journal of Computer and System Sciences 57(1), 1998, pages 74 to 93
    locator: the introduction (earlier bounds for integer sorting) and the sections on packed sorting and signature sort
  - paper: doi:10.1145/1314690.1314692
    title: Mikkel Thorup, Equivalence between priority queues and sorting, Journal of the ACM 54(6), 2007
    locator: the main theorem, which turns a sorting bound into a priority queue bound
---

Han's integer sorting is a deterministic algorithm on the [word RAM](/word-ram/) that sorts $n$ integers in $O(n \log \log n)$ time and $O(n)$ space. Yijie Han published it in 2002. It was the first deterministic sort with this time bound that uses only linear space: earlier deterministic sorts with the same time needed space that grows with the key range. Its main step passes the keys down a tree of splitters in batches, with many keys packed into one machine word.

## In plain words

You must sort many whole numbers, and each fits in one machine word. A computer word holds many bits, and one instruction works on all of them at once. So if you squeeze several short numbers into one word, you can work on all of them in one step.

The method first picks a small set of numbers from the input, sorts them, and uses them as fences. Each number then goes to the gap between two fences. Each gap is sorted the same way. The fences in a gap are far fewer than the numbers, so the levels shrink very fast. The hard part is to send all numbers to their gaps cheaply. Han does it in groups, and he packs the numbers so that one step moves many of them.

## The problem

The input is $n$ integers from the range $\{0, 1, \ldots, m - 1\}$, each in one word of $w \ge \log_2 (m + n)$ bits. The output is the same integers in non-decreasing order. This is [integer sorting](/integer-sorting/). The machine is the word RAM with the usual instructions on words, including multiplication. Han's algorithm is *conservative*: it needs words of only $O(\log (m + n))$ bits, so it does not depend on a large word length.

## The algorithm

The pseudocode shows the recursion that the algorithm is built on: a splitter step as in an exponential search tree, where a set of $n$ keys is split by about $\sqrt{n}$ splitters, and each part is sorted the same way. Han's contribution is line L5: it finds the parts of all keys in $O(n)$ total time for the level, which is the step that this page does not spell out at the word level.

```pseudo id=main
HAN-SORT(A, n)
L1  if n ≤ c then sort A by insertion sort; return A
L2  k ← ⌈√n⌉
L3  P ← a sample of about n / k keys of A          ▷ Han chooses it so that each part has O(√n) keys
L4  P ← HAN-SORT(P), with duplicates removed; let P = p_1 < ... < p_s
L5  for each key x of A, in packed batches, find j with p_j < x < p_(j+1), or j with x = p_j
L6  E_j ← the keys equal to p_j; B_j ← the keys strictly between p_j and p_(j+1) (with p_0 = −∞ and p_(s+1) = +∞)
L7  for j ← 0 to s do B_j ← HAN-SORT(B_j)
L8  return B_0, E_1, B_1, E_2, ..., E_s, B_s
```

The real algorithm keeps the splitters in an exponential search tree of Andersson, where a node with $d$ keys below it has about $d^{1/2}$ children, so the tree has depth $O(\log \log n)$. A key does not go down the tree alone. Han moves the keys of a node to its children in batches. Inside a batch, he shortens the keys so that each part of a key needs few bits, packs many shortened keys into one word, and divides them among the children with word operations. He calls the dividing of many keys at once *multi-dividing*. This gives $O(1)$ amortized time per key for each level of the tree.

## Example

The model in the implementation uses a sample of every $k$-th key. Sort $A = [41, 7, 93, 18, 65, 30, 7, 88, 51, 24, 76, 3, 59, 12, 97, 35]$ with $c = 4$. Then $n = 16$ and $k = 4$, and line L3 takes the keys at positions 0, 4, 8 and 12.

| step | keys | splitters | parts |
|---|---|---|---|
| top | all 16 keys | 41, 51, 59, 65 | $B_0$ = 7 18 30 7 24 3 12 35 · $B_1, B_2, B_3$ empty · $B_4$ = 93 88 76 97 |
| $B_0$ | 8 keys, $k = 3$ | 7, 12 | $B_0$ = 3 · $E_1$ = 7 7 · $B_1$ empty · $E_2$ = 12 · $B_2$ = 18 30 24 35 |
| small parts | at most 4 keys | none | insertion sort |

The result is $[3, 7, 7, 12, 18, 24, 30, 35, 41, 51, 59, 65, 76, 88, 93, 97]$. The sample of the top step is bad: it gives one part with 8 of the 16 keys and three empty parts. Han's algorithm avoids this. It chooses and maintains its splitters so that each part has $O(\sqrt{n})$ keys, which is what makes the depth $O(\log \log n)$.

## Correctness

The splitters come from $A$, so each part $B_j$ misses at least the keys equal to some splitter, and it is smaller than $A$. Each key of $B_j$ is greater than each key of $E_j$ and of the parts before it, and less than each key of $E_{j+1}$ and of the parts after it. So if each part is sorted, the concatenation of line L8 is sorted. Induction on $n$ gives the result for all inputs, whatever sample line L3 takes. The full proof is below.

## Complexity

- **Depth.** If each part has $O(\sqrt{n})$ keys, the part sizes go $n, n^{1/2}, n^{1/4}, \ldots$, and they reach a constant after $O(\log \log n)$ levels.
- **One level.** The splitters of all subproblems on one level are $O(n / \sqrt{\cdot})$ keys in total, and sorting them is a lower-order term. Han shows that line L5 runs in $O(n)$ time for all keys of one level together, with packed batches.
- **Total.** $O(n)$ per level for $O(\log \log n)$ levels gives $O(n \log \log n)$ time, in the worst case, with no randomness.
- **Space.** The tree and the batches take $O(n)$ words. Earlier deterministic algorithms with $O(n \log \log n)$ time used $O(m^{\varepsilon})$ space, which can be far more than $n$.
- **The model.** The Python model places each key by binary search, which costs $O(\log n)$, so one level costs $O(n \log n)$. It also uses a fixed sample, so on some inputs the parts are not balanced. It shows the structure and the correctness argument, not the bound.

## Properties

- **Deterministic.** It uses no random bits and no hashing. This is the point of the result, since randomized linear-space sorts with this bound were known before.
- **Not a comparison sort.** It uses word operations on packed keys. In the [decision tree model](/decision-tree-model/) no sort beats $\Omega(n \log n)$.
- **Linear space.** It uses $O(n)$ words for any key range.
- **Not stable as stated.** The algorithm sorts keys. To sort records stably, append the input index to each key.

## Variants and improvements

- **Randomized.** [Han and Thorup](/han-thorup-integer-sort/) (2002) sort in $O(n \sqrt{\log \log n})$ expected time and linear space.
- **Large words.** If $w \ge (\log n)^{2 + \varepsilon}$, the signature sort of Andersson, Hagerup, Nilsson and Raman sorts in $O(n)$ expected time.
- **Priority queues.** Thorup (2007) showed that a sort in $n \cdot S(n)$ time gives a [priority queue](/priority-queue/) with $O(S(n))$ time per operation. So Han's sort gives a deterministic priority queue with $O(\log \log n)$ time per operation in linear space.

## When to use it

Han's algorithm is a theoretical result. Its constant factors and its word-level tricks make it slower than [LSD radix sort](/radix-sort/) or a good comparison sort for all practical input sizes. It is the reference for what is possible deterministically: when a proof needs to sort integers in $o(n \log n)$ time and linear space without randomness, it can cite this bound.

## Pitfalls

- **Unbalanced splitters.** A splitter step with a bad sample, as in the example, can give a part with a constant fraction of the keys. Then the depth is not $O(\log \log n)$. The bound needs the splitters of the exponential search tree, not an arbitrary sample.
- **Keys equal to splitters.** A part that includes the keys equal to a splitter may not shrink, and the recursion does not end for many equal keys. Line L6 gives them their own sets $E_j$, which need no more work.
- **Reading the bound as practical.** $\log \log n$ is at most 5 for any $n$ below $2^{32}$, so the gain over $O(n \log n)$ appears only for huge $n$, and the constants hide it.

## Implementations

## History

Andersson introduced exponential search trees in 1996 and used them for deterministic sorting in linear space. Thorup (1998) and Han (2001) improved the deterministic linear-space bound step by step, the latter to $O(n \log \log n \log \log \log n)$. Han closed the gap to $O(n \log \log n)$ at STOC 2002, with the journal version in 2004. This matched the deterministic $O(n \log \log n)$ bound of earlier algorithms that needed more space, and the randomized linear-space bound of Thorup (1997).

## References
