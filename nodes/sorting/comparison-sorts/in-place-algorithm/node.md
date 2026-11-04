---
tag: 32QFJ9
kind: definition
slug: in-place-algorithm
name: In-place algorithm
aliases:
- in-place sorting
area: sorting/comparison-sorts
level: intro
summary: An algorithm that uses only O(1) (or O(log n)) extra space beyond its input.
prereqs: [space-complexity, asymptotic-notation]
see_also: [heapsort, insertion-sort, quicksort-stack-depth, in-place-merge-sort, block-sort, vector-rotation, in-place-permutation, stable-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1 (sorting in place, with at most a constant number of items stored outside the array) and Chapter 6 introduction (heapsort sorts in place)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1, Elementary Sorts (the paragraph on extra memory, in-place sorts and the function-call stack)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4, Sorting by merging (the exercises on merging with a bounded amount of extra memory)
---

An in-place algorithm transforms its input inside the memory that holds the input, and uses only a small amount of extra memory: $O(1)$ items or words in the strict sense, and $O(\log n)$ words in the common relaxed sense. In-place sorts such as [insertion sort](/insertion-sort/) and [heapsort](/heapsort/) need no second array, while [merge sort](/merge-sort/) needs a buffer of $\Theta(n)$ items. The term matters most for large inputs, where a second copy does not fit in memory.

## Definition

Let an algorithm work on a writable input of $n$ items, stored in an array $A[0 \ldots n-1]$, on a [word RAM](/word-ram/) with words of $w \ge \lg n$ bits. Let $S(n)$ be the largest number of memory words, other than the words of $A$, that it uses at one time on an input of size $n$, counting its variables, its buffers and its call stack. The output is the final content of $A$.

- The algorithm is **in place in the strict sense** when $S(n) = O(1)$. Then it holds at most a constant number of items outside $A$ at one time, as in the definition of CLRS, Section 2.1, together with a constant number of indices. A constant number of indices is $O(\log n)$ bits.
- The algorithm is **in place in the relaxed sense** when $S(n) = O(\log n)$. This allows a recursion of depth $O(\log n)$ with $O(1)$ words in each frame, as in [quicksort](/quicksort/) with a bound on the stack depth.
- An algorithm that is not in place is **out of place**. It uses a separate output array or a buffer whose size grows faster than $\log n$, for example $\Theta(n)$ or $\Theta(\sqrt{n})$.

$S(n)$ is a worst-case measure. A recursive algorithm whose depth is $\Theta(n)$ on some input is not in place, even if the depth is small on typical inputs. The definition counts extra space only. The input itself takes $n$ words, so the total space of an in-place algorithm is $n + O(1)$ or $n + O(\log n)$ words.

## Examples and non-examples

**Examples.**

- [Insertion sort](/insertion-sort/), [selection sort](/selection-sort/), [bubble sort](/bubble-sort/) and [Shell sort](/shell-sort/) use a key and a few indices, so $S(n) = O(1)$.
- [Heapsort](/heapsort/) keeps the heap in the array itself, and its sift-down is a loop. So $S(n) = O(1)$. It is the classic sort that is in place in the strict sense and takes $O(n \log n)$ time in the worst case.
- [Quicksort](/quicksort/) that recurses on the smaller part and loops on the larger part has a stack depth of at most $\lfloor \lg n \rfloor$, because each frame on the stack covers at most half of the range of the frame below it. For $n = 10^6$ this is at most 19 frames. So it is in place in the relaxed sense. See [quicksort stack depth](/quicksort-stack-depth/).
- Reversing an array by exchanging $A[i]$ and $A[n-1-i]$ for $i < n/2$, and [rotating an array](/vector-rotation/) by three reversals, use $O(1)$ words.
- [In-place merge sort](/in-place-merge-sort/) and [block sort](/block-sort/) merge without a buffer of linear size, and block sort is also stable.

**Non-examples.**

- [Merge sort](/merge-sort/) on an array copies one half into a buffer. For $n = 10^6$ the buffer holds $500{,}000$ items, so $S(n) = \Theta(n)$.
- [Counting sort](/counting-sort/) and [radix sort](/radix-sort/) write the output into a second array of $n$ items, and counting sort also uses an array of counters.
- Quicksort that makes a recursive call for each of the two parts makes a chain of $n - 1$ nested calls on a sorted input with the first item as pivot. Its stack is $\Theta(n)$, so it is not in place in either sense, although it moves the items only inside $A$.
- An algorithm that copies the input into a buffer, works there and copies the result back has the same input and output as an in-place algorithm, but it is out of place.

**A boundary case.** An algorithm that marks each item with one extra bit uses $n$ bits, which is $\Theta(n / w)$ words. It is not in place by the definition, although the extra space is small in practice. Some algorithms that move items along the [cycles of a permutation](/in-place-permutation/) need these bits, or $\Theta(n^2)$ time to do without them.

## Related definitions

- **[Space complexity](/space-complexity/).** The general measure of memory use. In-place algorithms are those with extra space $O(1)$ or $O(\log n)$ words.
- **[Stable sort](/stable-sort/).** A sort that keeps equal keys in their input order. In-place and stable together, with $O(n \log n)$ comparisons, is possible but needs a complex merge, as in [block sort](/block-sort/).
- **[Comparison sort](/comparison-sort/).** Most in-place sorts are comparison sorts. Some distribution sorts, such as [American flag sort](/american-flag-sort/), are in place too, up to a table of counters whose size depends on the radix.
- **Logspace.** In complexity theory, [logspace](/logspace/) algorithms have a read-only input and $O(\log n)$ bits of work memory. An in-place algorithm may write to its input, so the two notions are different.

## References
