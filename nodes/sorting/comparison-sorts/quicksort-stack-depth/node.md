---
tag: Y45QJK
kind: technique
slug: quicksort-stack-depth
name: Quicksort stack depth
aliases:
- Stack depth for quicksort
area: sorting/comparison-sorts
level: core
summary: Removing the second recursive call of quicksort and recursing on the smaller part first to keep the stack depth logarithmic.
prereqs: [quicksort]
see_also: [randomized-quicksort, introsort, recursion, stack, in-place-algorithm, three-way-quicksort, quickselect, divide-and-conquer-paradigm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 7, the end-of-chapter problem Stack depth for quicksort (the procedure TRE-QUICKSORT and the change that makes the stack O(lg n))
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (Algorithm Q, which puts the larger subfile on a stack and needs at most lg N entries)
  - paper: "Robert Sedgewick, Implementing Quicksort programs, Communications of the ACM 21(10), 1978"
    locator: the removal of recursion and the bound on the stack size
---

The recursion of [quicksort](/quicksort/) can be $n$ calls deep, for example on a sorted input with the last item as pivot, and each call needs a frame on the stack. The stack depth technique removes the second recursive call by a loop, and it always recurses on the smaller of the two parts. Then each nested call has at most half the items of its caller, so at most $\lfloor \lg n \rfloor$ calls are nested below the first call, on every input. The time does not change, because the same partitions are made. Knuth's Algorithm Q and many library sorts do this with an explicit stack.

## In plain words

Quicksort splits a pile of cards into two smaller piles and then has to sort both. The usual way is to put one pile aside, sort the other one, and come back. Each pile that waits needs a note, and on a bad input the notes pile up: one note for almost every card.

The fix is to always work on the smaller pile first, and to leave a note only for the larger one. Better still, finish the smaller pile, and then continue with the larger pile without any note. The smaller pile has at most half of the cards. So each note is for a pile at most half the size of the one before, and only a few notes are ever needed at the same time.

## When it applies

- **Quicksort or a related method recurses on two parts** of a range, and the parts can be very uneven.
- **The stack is small or limited.** Threads often have small stacks, and some languages, such as Python, stop deep recursion early. An uneven split on a large input then crashes the program.
- **The worst case of the depth matters, not only its mean.** With a random pivot the depth is $O(\log n)$ with high probability, but not on each run, and inputs with many equal keys can still be deep.
- **The work after the calls is empty.** Quicksort does nothing after its second call, so that call can be replaced by a loop. This is the removal of a tail call.

## The template

```pseudo id=main
QUICKSORT(A, lo, hi)                       ▷ sort A[lo .. hi − 1]
L1  while hi − lo ≥ 2 do
L2      p ← PARTITION(A, lo, hi)           ▷ A[p] is in its final place
L3      if p − lo < hi − (p + 1) then      ▷ the left part is the smaller one
L4          QUICKSORT(A, lo, p)
L5          lo ← p + 1                     ▷ go on with the right part
L6      else
L7          QUICKSORT(A, p + 1, hi)
L8          hi ← p                         ▷ go on with the left part
```

Each turn of the loop partitions the current range, sorts the smaller part by a recursive call, and then makes the larger part the current range. The hole is PARTITION, which can be the [Lomuto partition](/lomuto-partition/), the [Hoare partition](/hoare-partition/) with its own split rule, or a three-way partition with two parts to skip.

**Why the depth is logarithmic.** A range of $m$ items splits into parts of $p - lo$ and $hi - p - 1$ items, which add up to $m - 1$. The smaller part has at most $\lfloor (m-1)/2 \rfloor < m/2$ items. The call of line L4 or L7 is on the smaller part, and a range keeps its frame while the loop shrinks it. So a call that is nested $d$ levels below the first call works on at most $n/2^d$ items. A call at level $d \ge 1$ exists only when its caller at level $d - 1$ partitions, and a caller that partitions has at least 2 items. So $2 \le n/2^{d-1}$, which gives $d \le \lg n$. So at most $\lfloor \lg n \rfloor$ levels of calls are nested below the first call.

**Why the time does not change.** The loop does, for the larger part, exactly what the second recursive call did. So the same ranges are partitioned with the same items, only in another order, and the comparisons and swaps are the same.

**An explicit stack.** The same idea works without recursion. Keep a stack of ranges. Partition the current range, push the larger part, and continue with the smaller part. When the current range has fewer than 2 items, pop the next range. The stack never holds more than $\lfloor \lg n \rfloor$ ranges, by the same argument. This is the form of Knuth's Algorithm Q.

## Classic examples

The table gives the largest number of calls that are active at the same time, counting the first call, for quicksort with the last item as pivot and the Lomuto partition. The middle column is CLRS's TRE-QUICKSORT, which recurses on the left part and loops on the right part, whatever their sizes. The input of 100,000 items is one random permutation.

| input | two recursive calls | recurse left, loop right | smaller part first |
|---|---|---|---|
| sorted, $n = 2000$ | 2000 | 2000 | 2 |
| reversed, $n = 2000$ | 2000 | 1001 | 2 |
| random, $n = 1000$ | 23 | 15 | 7 |
| random, $n = 100{,}000$ | 41 | 26 | 11 |

On a sorted input, each pivot is the largest item, so the left part has all other items. The version that always recurses on the left nests a call for each item. The version that picks the smaller part recurses only on the empty right part, and loops on the left part. The bound $\lfloor \lg n \rfloor + 1$ frames is 11 for $n = 2000$ and 17 for $n = 100{,}000$.

- **CLRS.** The problem Stack depth for quicksort at the end of Chapter 7 defines TRE-QUICKSORT, shows that its stack is $\Theta(n)$ deep in the worst case, and asks for the change to the smaller part, which gives $\Theta(\lg n)$.
- **Knuth's Algorithm Q.** It keeps the ranges on an explicit stack, puts the larger subfile on the stack, and needs at most $\lg N$ entries.
- **Sedgewick (1978)** studies the removal of recursion in quicksort, with the rule of the smaller part first, among other improvements.
- **[Introsort](/introsort/)** bounds the depth in another way: when it exceeds about $2 \lg n$, it sorts the range with heapsort.

## Variations

- **Tail calls in the language.** In a language that removes tail calls, write the second call as the last action of the procedure, and order the two calls so that the smaller part comes first. The compiler then makes the loop.
- **Quickselect.** [Quickselect](/quickselect/) recurses on one part only, so its recursion is a tail call and becomes a loop with $O(1)$ extra space.
- **Three-way partition.** With [three-way quicksort](/three-way-quicksort/), there are two parts to sort and one part of equal keys to skip. The rule is the same: recurse on the smaller of the two parts.
- **Small parts.** Do not push or recurse on a part of fewer than about 10 items; sort it by insertion sort at once or at the end. This makes the stack shorter still.
- **Parallel quicksort.** In a parallel sort, the two parts are sorted at the same time, and each task needs its own stack. The rule then bounds the stack of each task.

## Pitfalls

- **Recursing on a fixed side.** Removing the second call alone is not enough. If the code always recurses on the left part, a sorted input still gives $n$ nested calls, as the table shows.
- **Comparing the wrong sizes.** The sizes are $p - lo$ and $hi - p - 1$, without the pivot. With half-open ranges, an error by one here is easy. It does not break the sort, but it can break the bound.
- **Changing the range before the call.** In line L5 or L8 the range changes only after the call returns. If the code updates $lo$ or $hi$ first and then calls with the new values, it sorts the wrong part.
- **Expecting a better time.** The rule does not change the $\Theta(n^2)$ worst case of the time. It only bounds the space. Use a good [pivot rule](/pivot-selection/) for the time.
- **An explicit stack that is too small.** With the larger part pushed, $\lfloor \lg n \rfloor$ entries are enough, so 64 entries are enough for each $n < 2^{64}$. If the code pushes the smaller part instead, the stack can need $n$ entries.

## Exercises

1. Run the template by hand on $[1, 2, 3, 4, 5, 6, 7, 8]$ with the last item as pivot. How many calls are active at most?
2. Prove that the smaller of two parts of sizes $a$ and $b$ with $a + b = m - 1$ has at most $\lfloor (m-1)/2 \rfloor$ items, and that the bound is reached for each $m$.
3. Show that on an array of $n$ equal items with the Lomuto partition, the time of the template is $\Theta(n^2)$ but at most 2 calls are active at the same time.
4. Write the explicit-stack form, and prove that its stack holds at most $\lfloor \lg n \rfloor$ ranges at each moment.
5. Show that CLRS's TRE-QUICKSORT, which recurses on the left part and loops on the right part, reaches $n$ nested calls on a sorted input of $n$ items with the last item as pivot, and find an input of $n$ items on which it nests at most $\lfloor \lg n \rfloor + 1$ calls.

## References
