---
tag: GCQCHN
kind: algorithm
slug: merge-shuffle
name: Merge shuffle
aliases:
- MergeShuffle
- MERGESHUFFLE
area: randomized/shuffling
level: research
summary: A divide-and-conquer shuffle that shuffles two halves and merges them with fair coin flips, then places the leftover items by inside-out Fisher-Yates. Exact, parallel, n log2 n + O(n) random bits.
solves: [random-permutation]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(log n)}
properties: {in_place: true, online: false, deterministic: false, recursive: true}
history:
  year: 2015
  people: [Axel Bacher, Olivier Bodini, Alexandros Hollender, Jérémie Lumbroso]
  note: MergeShuffle was published on arXiv in 2015 as a fast parallel shuffle that uses close to the minimum number of random bits.
prereqs: [fisher-yates-shuffle, merge-sort, random-permutation]
see_also: [shuffling-a-linked-list, sort-based-shuffle, permute-by-sorting, naive-shuffle, coupon-collector-problem, stirling-approximation, randomized-algorithm, binomial-distribution]
sources:
  - paper: "Axel Bacher, Olivier Bodini, Alexandros Hollender and Jérémie Lumbroso, MergeShuffle, a very fast, parallel random permutation algorithm, arXiv:1508.03167, 2015"
    locator: Section 2, the procedures MergeShuffle and Merge; Lemma 1 (the merge gives a uniform result) and Lemma 2 (the number of random bits of one merge)
    url: https://arxiv.org/abs/1508.03167
  - paper: "C. Radhakrishna Rao, Generation of random permutations of given number of elements using random sampling numbers, Sankhya Series A 23, 1961"
    locator: pp. 305 to 307 (the split by random bits that MergeShuffle reverses)
  - paper: "Martin Sandelius, A simple randomization procedure, Journal of the Royal Statistical Society Series B 24, 1962"
    locator: pp. 472 to 481
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Algorithm P
---

MergeShuffle is an exact shuffle in the style of [merge sort](/merge-sort/). It shuffles the two halves of the array recursively and then merges them. The merge takes the next item from the left or the right half by a fair coin flip, and it stops as soon as a coin asks for a half that is empty. The few items that are left are then put in place by the inside-out step of the [Fisher-Yates shuffle](/fisher-yates-shuffle/). The output is a uniform [random permutation](/random-permutation/). It runs in $\Theta(n \log n)$ time, in place, and uses $n \log_2 n + O(n)$ random bits, close to the minimum $\log_2 n! = n \log_2 n - \Theta(n)$. The two halves are independent, so the method is easy to run in parallel. This is the correct form of the "merge with coin flips" idea; the plain fair-coin merge is biased.

## In plain words

Split the deck into two halves and shuffle each half, by the same method. Now make one pile out of the two: toss a coin, and take the next card from the left half on heads and from the right half on tails.

If you did only this, the result would be unfair, because the last cards of the longer half would gather at the bottom. MergeShuffle has a fix. It stops at the first toss that asks for a half that is already empty. A few cards are then left over, and it puts each of them at a random place in the pile, with all places equally likely. Then every order of the deck has the same chance. Most of the work is cheap coin tosses, so it uses very few random bits, and the two halves can be shuffled at the same time by different processors.

## The problem

The input is an array $T[s \ldots s+n-1]$. The output is the same items in an order that is uniform on all $n!$ orders. The source of randomness is FLIP(), a fair bit, and RANDOM$(a, b)$, uniform on $\{a, \ldots, b\}$; all calls are independent. This is the [random permutation](/random-permutation/) problem in the fair-bit model, where the cost of RANDOM$(a, b)$ is about $\log_2 (b - a + 1)$ bits.

## The algorithm

```pseudo id=main
MERGE-SHUFFLE(T, s, n)                     ▷ shuffle T[s .. s + n − 1]
L1  if n ≤ 1 then return
L2  n₁ ← ⌊n / 2⌋
L3  MERGE-SHUFFLE(T, s, n₁); MERGE-SHUFFLE(T, s + n₁, n − n₁)
L4  MERGE(T, s, n₁, n − n₁)

MERGE(T, s, n₁, n₂)
L5  i ← s; j ← s + n₁; e ← s + n₁ + n₂
L6  loop
L7      if FLIP() = 0 then                 ▷ take from the left half
L8          if i = j then exit the loop    ▷ the left half is empty
L9      else                               ▷ take from the right half
L10         if j = e then exit the loop    ▷ the right half is empty
L11         exchange T[i] and T[j]; j ← j + 1
L12     i ← i + 1
L13 while i < e do                         ▷ the leftover items: inside-out Fisher-Yates
L14     m ← RANDOM(s, i); exchange T[i] and T[m]; i ← i + 1
```

During the loop, $T[s \ldots i-1]$ is the merged prefix, $T[i \ldots j-1]$ holds the left items not yet taken, and $T[j \ldots e-1]$ holds the right items not yet taken, in their order. Taking a right item swaps it with the first remaining left item, which moves that left item to the end of the left block. The paper stops the recursion at a small size and uses Fisher-Yates there, which does not change the output distribution.

## Example

Merge the halves $[a, b, c]$ and $[d, e, f]$, already shuffled, with $s = 0$. Suppose the coins are $1, 0, 1, 0, 0, 0$ and then RANDOM$(0, 5)$ returns 1.

| step | coin | action | $T$ | $i$ | $j$ |
|---|---|---|---|---|---|
| start | | | a b c d e f | 0 | 3 |
| 1 | 1 | take $d$, swap $T[0]$ and $T[3]$ | d b c a e f | 1 | 4 |
| 2 | 0 | take $b$ | d b c a e f | 2 | 4 |
| 3 | 1 | take $e$, swap $T[2]$ and $T[4]$ | d b e a c f | 3 | 5 |
| 4 | 0 | take $a$ | d b e a c f | 4 | 5 |
| 5 | 0 | take $c$ | d b e a c f | 5 | 5 |
| 6 | 0 | the left half is empty: stop | d b e a c f | 5 | 5 |
| 7 | | $f$ goes to position RANDOM$(0, 5) = 1$ | d f e a c b | 6 | |

The loop used 6 coin flips and placed 5 items; one item was left over and needed one uniform integer from 6 values.

## Correctness

**Theorem.** If the two halves are uniformly shuffled and independent, MERGE leaves $T[s \ldots e-1]$ uniformly shuffled. Hence, by induction on $n$, MERGE-SHUFFLE returns a uniform random permutation.

The proof has two steps. (1) Condition on how the loop stops: $a$ left items and $b$ right items were taken, and one half is empty. Each pattern of $a$ zeros and $b$ ones has the same probability $2^{-(a+b+1)}$, and every such pattern is possible. The right items come out in their order, which is uniform. The left items come out in an order that, for a fixed pattern, is a fixed rearrangement of the left order, which is uniform. So the merged prefix is a uniform order of its set of items. (2) Each leftover item is put at a uniform position among the prefix and the end, which is the inside-out step of Fisher-Yates and keeps the prefix uniform. The full proof is in the proof file. The test file checks the merge exactly for all splits up to $3 + 3$ items and the whole algorithm for $n \le 4$, with exact fractions.

**Why the fix is needed.** Without lines L8, L10 and L13 to L14, the merge would take coins until one half is empty and append the rest. Then each interleaving of $n_1$ and $n_2$ items has probability $2^{-k}$ for some $k$, which is not $1/\binom{n}{n_1}$ in general. For three items, $[0, 1, 2]$ gets $1/4$ and $[1, 2, 0]$ gets $1/8$. See [sort-based shuffle](/sort-based-shuffle/) and [shuffling a linked list](/shuffling-a-linked-list/).

## Complexity

**Time.** One merge is $\Theta(n)$ plus the leftover items, so the time is $\Theta(n \log n)$, as for merge sort. The recursion depth is $\lceil \log_2 n \rceil$, and the extra space is that stack.

**Random bits.** A merge of $n$ items uses at most $n + 1$ flips in its loop. Let $R$ be the number of leftover items. Each needs one uniform integer from at most $n$ values, about $\log_2 n$ bits. $E[R] = \Theta(\sqrt n)$: a recurrence over the numbers of items left in each half gives $E[R] = 0.875, 2.338, 7.04, 24.25, 49.47$ for $n = 4, 16, 100, 1000, 4000$, about $0.78 \sqrt n$ for the last value. So one merge costs $n + \Theta(\sqrt n \log n)$ bits (Lemma 2 of the paper), and the whole algorithm $n \log_2 n + O(n)$ bits. The lower bound is $\log_2 n! = n \log_2 n - n \log_2 e + O(\log n)$, by [Stirling's approximation](/stirling-approximation/). Fisher-Yates with rejection on fair bits uses more: about 12508 bits on average for $n = 1000$, where $\log_2 1000! \approx 8529$ (see its page).

## Properties

- **Exact.** Uniform in the model of fair bits and exact uniform integers.
- **In place,** with $O(\log n)$ stack, or $O(1)$ with a bottom-up loop.
- **Parallel.** The halves are independent. With $p$ processors, split into $p$ parts, shuffle each with Fisher-Yates, and merge in a tree.
- **Las Vegas in its bits.** The number of flips is random but bounded by $n + 1$ per merge; only the leftover step uses RANDOM, which needs rejection on fair bits.
- **Local memory access.** The merge reads both halves from left to right, which suits caches better than the random accesses of Fisher-Yates on large arrays.

## Variants and improvements

- **Cutoff to Fisher-Yates.** For small blocks, Fisher-Yates is faster; the paper uses a cutoff.
- **Many parts.** Split into $k$ parts and merge by $k$-sided dice, or merge in a balanced tree of pairs.
- **The reverse direction: splitting.** The methods of Rao (1961) and Sandelius (1962) split the items into two groups by one random bit each and recurse on the groups. MergeShuffle is the bottom-up form of the same idea. The splits have random sizes; the merges here have fixed sizes.
- **Merges with weighted coins.** A merge that takes the left item with probability $\ell / (\ell + r)$ is also exact, without the leftover step, but needs non-dyadic coins. It is the natural method for a [linked list](/shuffling-a-linked-list/).

## When to use it

Use MergeShuffle when random bits are expensive, as with a cryptographic generator, when many processors share the work, or when the array is so large that the random accesses of Fisher-Yates hurt. In ordinary code on one processor, [Fisher-Yates](/fisher-yates-shuffle/) is simpler and fast enough.

## Pitfalls

- **Leaving out the stop rule.** A merge that runs until one half is empty and appends the rest is biased, as shown above.
- **A biased last step.** RANDOM$(s, i)$ in line L14 must be exactly uniform. A modulo of a random word is biased; see [modulo bias](/modulo-bias/).
- **Halves that are not independent.** The proof needs the two halves to be shuffled with separate random bits. Two processors that use copies of one seed break it.

## Implementations

## History

Rao in 1961 and Sandelius in 1962 shuffled by splitting items into groups by random digits or bits. Bacher, Bodini, Hollender and Lumbroso published MergeShuffle in 2015. They proved that the merge is exact and that the algorithm uses $n \log_2 n + O(n)$ random bits, and they showed that it is faster than Fisher-Yates in practice with many threads.

## References
