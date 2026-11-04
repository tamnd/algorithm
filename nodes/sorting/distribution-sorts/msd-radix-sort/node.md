---
tag: 5YMPGZ
kind: algorithm
slug: msd-radix-sort
name: MSD radix sort
aliases:
- Most-significant-digit radix sort
- Postman sort
area: sorting/distribution-sorts
level: core
summary: Partitions keys by their leading digit, then recursively sorts each bucket on the next digit.
solves: [string-sorting, integer-sorting]
model: word-ram
complexity:
  vars: {n: the number of strings, D: the total length of the distinguishing prefixes, R: the alphabet size}
  time: {worst: O(R (n + D)), best: Θ(n + R)}
  space: {extra: Θ(n + R)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: false, recursive: true}
prereqs: [radix-sort, counting-sort, lexicographic-order]
see_also: [radix-sort, american-flag-sort, three-way-radix-quicksort, multikey-quicksort, burstsort, string-sorting, sorting-variable-length-items, trie]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 5, Section 5.1, String Sorts, subsection MSD string sort (Algorithm 5.2) and its performance analysis
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.5, Sorting by Distribution (most significant digit first)
  - paper: Peter M. McIlroy, Keith Bostic and M. Douglas McIlroy, Engineering radix sort, Computing Systems 6(1), 1993, pages 5 to 27
    locator: the description of MSD radix sort with a stack of pending piles, and of the in-place permutation (American flag sort)
---

MSD radix sort sorts strings or integer keys from the most significant digit down: it splits the keys into buckets by their first character with a [counting sort](/counting-sort/), then sorts each bucket the same way on the next character. A bucket with one key, or with keys that have all ended, needs no more work, so the sort reads only the [distinguishing prefixes](/string-sorting/) of the keys. With a constant alphabet it runs in time linear in the total length $D$ of those prefixes, and it handles strings of different lengths. It is the base of fast string sorts such as [American flag sort](/american-flag-sort/), [three-way radix quicksort](/three-way-radix-quicksort/) and [burstsort](/burstsort/).

## In plain words

A post office sorts letters by postcode. First it puts the letters into piles by the first letter of the code. Then it takes one pile and splits it by the second letter of the code, and so on. A pile with only one letter in it is done. A letter whose code has no more letters goes to the front of its pile, because a short code that matches the start of a longer one comes first in a dictionary.

Each letter is looked at only until it is alone in its pile. So a list of very different words is sorted after a look at one or two characters of each word, even if the words are long. The price is the work to set up the piles: each split prepares one pile for each possible character, and many small piles make that cost large.

## The problem

The input is an array $A[0 \ldots n-1]$ of strings over the alphabet $\{0, \ldots, R-1\}$. The output is the strings in [lexicographic order](/lexicographic-order/): $s < t$ if $s$ is a proper prefix of $t$, or if $s[j] < t[j]$ at the first index $j$ where they differ. This is the [string sorting](/string-sorting/) problem. Integers of $w$ bits are the special case of strings of a fixed length $\lceil w/r \rceil$ over $R = 2^r$ symbols.

For a string $s$ and an index $d$, let $c(s, d) = s[d] + 1$ if $d < |s|$ and $c(s, d) = 0$ if $d \ge |s|$. The value 0 marks the end of the string, and it sorts before each real character.

## The algorithm

The recursion is written with an explicit stack of tasks. A task $(lo, hi, d)$ means: the strings of $A[lo \ldots hi-1]$ agree on their first $d$ characters, and they must be sorted by the rest.

```pseudo id=main
MSD-RADIX-SORT(A, n, R)
L1  S ← a stack that holds the task (0, n, 0)
L2  while S is not empty do
L3      (lo, hi, d) ← pop S
L4      if hi − lo ≤ 1 then continue
L5      C ← counts of c(A[i], d) for lo ≤ i < hi, over the R + 1 values 0 .. R
L6      start[r] ← C[0] + ... + C[r − 1] for r = 0 .. R + 1      ▷ bucket starts
L7      copy A[lo .. hi − 1] stably into a buffer B, by bucket c(A[i], d)
L8      copy B back to A[lo .. hi − 1]
L9      for r ← R down to 1 do                  ▷ bucket 0: strings that ended, all equal
L10         push (lo + start[r], lo + start[r + 1], d + 1) onto S
L11 return A
```

Lines L5 to L8 are one stable counting sort of the range on character $d$, with $R + 1$ buckets. After it, bucket $r$ holds the strings with $c(s, d) = r$, at $A[lo + start[r] \ldots lo + start[r+1] - 1]$. Bucket 0 holds the strings of length exactly $d$. They are all equal to the common prefix of the task, so they are in final position. Each other bucket becomes a new task one character deeper. Line L9 pushes them from the last to the first, so the stack pops the smaller characters first, but the order of the tasks does not matter for the result.

## Example

Sort $A = [\text{she}, \text{sells}, \text{sea}, \text{shells}, \text{by}, \text{the}, \text{sea}, \text{shore}]$. Each row is a task with at least two strings, in the order in which the stack pops them.

| $d$ | the strings of the task | buckets after lines L5 to L8 |
|---|---|---|
| 0 | she sells sea shells by the sea shore | b: by · s: she sells sea shells sea shore · t: the |
| 1 | she sells sea shells sea shore | e: sells sea sea · h: she shells shore |
| 2 | sells sea sea | a: sea sea · l: sells |
| 3 | sea sea | end: sea sea |
| 2 | she shells shore | e: she shells · o: shore |
| 3 | she shells | end: she · l: shells |

The result is $[\text{by}, \text{sea}, \text{sea}, \text{sells}, \text{she}, \text{shells}, \text{shore}, \text{the}]$. The sort reads 24 characters, including the end marks. The strings by and the are done after one character. The two copies of sea leave the sort when both end at $d = 3$, and she comes before shells for the same reason.

## Correctness

The invariant of the stack is: the tasks on $S$ cover disjoint ranges, the strings of each task agree on their first $d$ characters, and each string outside all tasks is in its final position relative to the others. A task splits its range into buckets in the order of character $d$. Strings in different buckets are then in lexicographic order, because they first differ at index $d$ (or one of them ends there). Strings in the same bucket agree on $d + 1$ characters and go back on the stack. The loop ends because each task reads the character at index $d$ of at least two strings, and $d$ is at most the length of the longest string. The full proof is below.

## Complexity

Let $\ell(s)$ be the length of the distinguishing prefix of $s$: the shortest prefix of $s$ that is not a prefix of another string of the input, or all of $s$ if there is no such prefix. Let $D = \sum_s \ell(s)$.

- **Characters read.** String $s$ is in a task with at least two strings at the depths $0, 1, \ldots$ as long as another string agrees with it on the first $d$ characters. That is true for $d < \ell(s)$, and for $d = |s|$ only when $\ell(s) = |s|$. So $s$ is read at most $\ell(s) + 1$ times, and the total number of reads is at most $n + D$.
- **Tasks.** Let $T$ be the number of tasks with at least two strings. Each of them reads at least two characters, so $T \le (n + D)/2$.
- **Time.** A task with $m \ge 2$ strings costs $\Theta(m + R)$ for lines L5 to L10. The sum is $O(n + D + R\,T)$, which is $O(R(n + D))$ in the worst case and $\Theta(n + D)$ for a constant $R$. A task with one string costs $O(1)$, and there are at most $(R+1)T + 1$ of them, which the same bound covers.
- **Best case.** If all first characters differ, one task does all the work in $\Theta(n + R)$ time.
- **Space.** The buffer $B$ and the counts take $\Theta(n + R)$ space, reused by all tasks. The stack holds at most $R$ tasks for each level of depth that is open, so it is $O(R \cdot \max_s \ell(s))$ in the worst case. Processing the largest bucket last, or using the explicit stack in a careful order, bounds it further.

Any algorithm that sorts strings must read each distinguishing prefix in the worst case, so $\Omega(D)$ is a lower bound, and MSD radix sort is optimal for a constant alphabet. For $n$ random strings over $R$ symbols, $D$ is about $n \log_R n$ (Sedgewick and Wayne, Section 5.1), much less than the total length when the strings are long.

## Properties

- **Stable.** Each split is a stable counting sort, and strings stay inside their bucket.
- **Not in place.** It uses a buffer of $n$ items. American flag sort removes the buffer, at the cost of stability.
- **Adaptive to the data.** It stops reading a string at its distinguishing prefix, so it reads few characters of strings that differ early.
- **Not a comparison sort.** It uses characters as array indices.

## Variants and improvements

- **Cut-off to insertion sort.** A task with $R + 1$ buckets is wasteful for a few strings. Sort tasks of fewer than about 10 to 15 strings with [insertion sort](/insertion-sort/) that compares from index $d$. Sedgewick and Wayne show that this cut-off is essential for large alphabets such as Unicode.
- **[American flag sort](/american-flag-sort/).** Permute each bucket in place along cycles instead of copying to a buffer. McIlroy, Bostic and McIlroy describe it with a stack of pending piles.
- **Integers.** For fixed-length integer keys, use $r$-bit digits from the top. With $r = 1$ this is [radix exchange sort](/radix-exchange-sort/).
- **[Three-way radix quicksort](/three-way-radix-quicksort/).** Split into three parts on one character, which avoids the $R$ cost of each task.
- **[Burstsort](/burstsort/).** Build a [trie](/trie/) of small buckets, which uses the cache better on large sets of strings.

## When to use it

Use MSD radix sort for strings or long keys with a small alphabet, such as bytes, when many strings differ in their first few characters. It is fast for large inputs of random-like keys. With a large alphabet, or with many long common prefixes and small buckets, the $R$ cost of each task dominates, and three-way radix quicksort or multikey quicksort is often faster. For short fixed-length integer keys, [LSD radix sort](/radix-sort/) is simpler and has no recursion.

## Pitfalls

- **No end mark.** If $c(s, d)$ is not defined for $d \ge |s|$, the sort reads past the end of short strings. Line L5 must give the end its own bucket 0, before all characters.
- **Recursing on bucket 0.** The strings that end at $d$ are all equal. Pushing a task for bucket 0 in line L9 makes a task that never shrinks: the strings never get a character at depth $d + 1$, so the loop does not end. Line L9 starts at $r = 1$.
- **No cut-off.** Without a cut-off, a range of two strings with a long common prefix costs $R$ per character of that prefix. For $R = 65536$ this is very slow.
- **Deep recursion.** A recursive version goes as deep as the longest common prefix, which can overflow the call stack for long equal strings. The explicit stack of line L1 avoids this.

## Implementations

## History

Card sorters could also sort from the most significant column, by sorting each pile again on the next column, but the operator then had to keep many piles apart. Knuth (Section 5.2.5) discusses this most significant digit first method and why the least significant digit first order was easier with cards. For strings on computers, McIlroy, Bostic and McIlroy (1993) engineered the MSD method with an explicit stack and in-place permutation.

## References
