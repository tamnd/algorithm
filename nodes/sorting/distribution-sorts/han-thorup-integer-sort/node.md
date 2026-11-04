---
tag: B8DZ6B
kind: algorithm
slug: han-thorup-integer-sort
name: Han-Thorup randomized integer sorting
aliases:
- Randomized O(n sqrt(log log n)) integer sort
area: sorting/distribution-sorts
level: research
summary: Randomized word-RAM integer sort with expected time O(n sqrt(log log n)), faster than deterministic bounds.
solves: [integer-sorting]
model: word-ram
complexity:
  vars: {n: the number of keys, w: the word length in bits}
  time: {worst: "O(n √(log log n)) expected", average: "O(n √(log log n))", best: O(n)}
  space: {extra: O(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: false, comparison: false, recursive: true}
prereqs: [han-integer-sort, word-ram]
see_also: [han-integer-sort, integer-sorting, radix-sort, priority-queue, predecessor-problem, fusion-tree, string-sorting, bit-parallelism]
sources:
  - paper: doi:10.1109/SFCS.2002.1181890
    title: Yijie Han and Mikkel Thorup, Integer sorting in O(n √(log log n)) expected time and linear space, Proceedings of the 43rd IEEE Symposium on Foundations of Computer Science (FOCS 2002), pages 135 to 144
    locator: the abstract, the introduction (the improvement over the O(n log log n) bound and the consequences for string sorting and for sorting without multiplication), and the sections on splitting into small ordered subsets
  - paper: doi:10.1006/jcss.1998.1580
    title: Arne Andersson, Torben Hagerup, Stefan Nilsson and Rajeev Raman, Sorting in linear time?, Journal of Computer and System Sciences 57(1), 1998, pages 74 to 93
    locator: the sections on signature sort and packed sorting, and the O(n log log n) expected bound
  - paper: doi:10.1145/1314690.1314692
    title: Mikkel Thorup, Equivalence between priority queues and sorting, Journal of the ACM 54(6), 2007
    locator: the main theorem, which turns a sorting bound into a priority queue bound
---

Han-Thorup integer sorting is a randomized algorithm on the [word RAM](/word-ram/) that sorts $n$ integers in $O(n \sqrt{\log \log n})$ expected time and $O(n)$ space. Yijie Han and Mikkel Thorup published it at FOCS 2002. It is faster than the $O(n \log \log n)$ bound of the randomized sort of Andersson, Hagerup, Nilsson and Raman and of the deterministic sort of [Han](/han-integer-sort/), and it is the best known bound for integer sorting in linear space for general word lengths.

## In plain words

You must sort many whole numbers that each fit in one machine word. Pick some numbers at random from the input and sort them. They act as fences. Each number goes to the gap between two fences, and each gap is sorted the same way. Random fences are usually spread well, so no gap gets too many numbers, and the method checks this.

The new part is how the numbers find their gaps. A machine word has many bits, and one instruction works on all of them. Han and Thorup shorten the numbers so that several of them fit in one word, and they work on many at once. With random choices they can do this a little faster than earlier methods.

## The problem

The input is $n$ integers, each in one word of $w$ bits. The output is the same integers in non-decreasing order. This is [integer sorting](/integer-sorting/). The machine is the word RAM with the usual word instructions, and the algorithm may use random bits. Its running time is a random variable, and the bound is on its expected value, for every input.

## The algorithm

The pseudocode shows the frame: a splitter recursion with a random sample and a check of the part sizes. In the paper, the expensive step L5 is done for all keys with packed words and signature sort, and this step gives the $\sqrt{\log \log n}$ factor.

```pseudo id=main
HAN-THORUP-SORT(A, n)
L1  if n ≤ c then sort A by insertion sort; return A
L2  k ← ⌈√n⌉
L3  P ← k keys of A drawn uniformly at random
L4  P ← HAN-THORUP-SORT(P), with duplicates removed; let P = p_1 < ... < p_s
L5  split A into E_j (keys equal to p_j) and B_j (keys strictly between p_j and p_(j+1))
L6  if a part B_j is too large then draw a new sample (go to L3)
L7  for j ← 0 to s do B_j ← HAN-THORUP-SORT(B_j)
L8  return B_0, E_1, B_1, E_2, ..., E_s, B_s
```

The model in the implementation calls a part too large if it holds more than $n/2$ keys, and it accepts the fourth sample in any case, so it always ends. A random sample of $\sqrt{n}$ keys leaves parts of $O(\sqrt{n} \log n)$ keys with high probability, so a new sample is rarely needed.

The paper reaches the bound with the following tools, which the model replaces by binary search. Signature sort of Andersson, Hagerup, Nilsson and Raman replaces long keys by short hash signatures that keep the needed order information, so that many of them fit in one word. Packed sorting then sorts many short keys inside words in parallel. Han and Thorup combine these with a random splitting into ordered subsets, and they balance the cost of the levels so that the total is $O(n \sqrt{\log \log n})$ in expectation.

## Example

Take $A = [41, 7, 93, 18, 65, 30, 7, 88, 51, 24, 76, 3, 59, 12, 97, 35]$, so $n = 16$ and $k = 4$. Suppose that line L3 draws the keys 51, 18, 88 and 18. After sorting and the removal of duplicates, the splitters are $18 < 51 < 88$.

| set | keys |
|---|---|
| $B_0$ (less than 18) | 7 7 3 12 |
| $E_1$ (equal to 18) | 18 |
| $B_1$ (between 18 and 51) | 41 30 24 35 |
| $E_2$ (equal to 51) | 51 |
| $B_2$ (between 51 and 88) | 65 76 59 |
| $E_3$ (equal to 88) | 88 |
| $B_3$ (greater than 88) | 93 97 |

No part has more than $n/2 = 8$ keys, so line L6 accepts the sample. With $c = 4$, each part is small and goes to insertion sort. The result is $[3, 7, 7, 12, 18, 24, 30, 35, 41, 51, 59, 65, 76, 88, 93, 97]$.

## Correctness

The output does not depend on the random choices. The splitters are keys of $A$, so each part misses the keys equal to a splitter and is smaller than $A$. All keys of $B_{j-1}$ are less than $p_j$, all keys of $E_j$ equal $p_j$, and all keys of $B_j$ are greater. So the concatenation of sorted parts is sorted, and induction on $n$ gives the result. The algorithm is Las Vegas: the random bits change only its running time. The full proof is below.

## Complexity

- **Expected time.** $O(n \sqrt{\log \log n})$ for every input, by the analysis in the paper. The bound is on the expectation over the random bits, not over the inputs.
- **Space.** $O(n)$ words. Earlier sorts with fast word tricks often needed hash tables or space that grows with the key range; this one does not.
- **Large words.** If $w \ge (\log n)^{2 + \varepsilon}$, signature sort alone sorts in $O(n)$ expected time, so the hard case is $w$ between $\log n$ and $(\log n)^{2+\varepsilon}$.
- **The model.** The Python model places each key by binary search, so its expected time is $O(n \log n)$. It shows the frame and the correctness argument, not the bound.

## Properties

- **Randomized, Las Vegas.** The output is always correct, and only the time is random.
- **Not a comparison sort.** It uses word operations on packed keys and hashing.
- **Linear space.**
- **Not stable as stated.** To sort records stably, append the input index to each key.

## Variants and improvements

- **Deterministic.** [Han's sort](/han-integer-sort/) (2002) gives $O(n \log \log n)$ time with no randomness. No deterministic linear-space sort with the bound $O(n \sqrt{\log \log n})$ is known.
- **Priority queues.** By the equivalence of Thorup (2007), the bound gives a randomized [priority queue](/priority-queue/) with $O(\sqrt{\log \log n})$ expected time per operation.
- **Strings and weaker instruction sets.** The paper states that the result also improves the bounds for deterministic [string sorting](/string-sorting/) and for integer sorting without multiplication.
- **Open problem.** It is not known whether $n$ integers can be sorted in $O(n)$ time on the word RAM for all word lengths.

## When to use it

The algorithm is a theoretical result. It sets the best known upper bound for integer sorting in linear space, and proofs in other areas cite it to sort in $o(n \log \log n)$ expected time. For real programs, [LSD radix sort](/radix-sort/), [MSD radix sort](/msd-radix-sort/) or a comparison sort is faster at all practical sizes.

## Pitfalls

- **Expected, not worst case.** The bound is an expectation. A single run can take longer, and a proof that needs a worst-case bound must use a deterministic sort.
- **Keys equal to splitters.** If keys equal to a splitter stay in a part, a list with many equal keys may not shrink. Line L5 puts them in their own sets $E_j$.
- **A check that never gives up.** If line L6 asks for a new sample until all parts are small, the model must still end on inputs where no sample works well, such as lists with few distinct values. The model accepts the fourth sample, and termination does not depend on the check.

## Implementations

## History

Andersson, Hagerup, Nilsson and Raman (1995, journal 1998) gave a randomized sort in $O(n \log \log n)$ expected time with signature sort and packed sorting, and Thorup (1997) gave a randomized $O(n \log \log n)$ sort in linear space with addition, shift and bit-wise operations only. In 2002, Han gave the deterministic $O(n \log \log n)$ bound in linear space, and Han and Thorup lowered the randomized bound to $O(n \sqrt{\log \log n})$ at FOCS 2002.

## References
