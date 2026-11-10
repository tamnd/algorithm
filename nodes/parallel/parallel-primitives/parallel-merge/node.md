---
tag: GDEWS9
kind: algorithm
slug: parallel-merge
name: Parallel merge
aliases:
- binary-search split merge
area: parallel/parallel-primitives
level: advanced
summary: Merge two sorted arrays with Θ(n) work and Θ(log^2 n) span. Take the median of the longer array, find its place in the other by binary search, write it, and merge the two sides in parallel.
solves: [merging-sorted-lists]
model: work-span-model
complexity:
  vars: {n: the total number of items in the two inputs}
  time: {worst: O(n)}
  depth: {worst: O(log^2 n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, in_place: false, stable: false}
prereqs: [merging-sorted-lists, binary-search, fork-join-model, work-span-model, divide-and-conquer-paradigm]
see_also: [parallel-merge-sort, merging-sorted-sequences, merge-path, valiant-parallel-merge, parallel-merging-problem, merge-sort, fork-join-parallelism, work-efficiency]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Chapter 27, Section 27.3, Multithreaded merge sort (P-MERGE with the median of the longer array, and P-MERGE-SORT)
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 4th edition, MIT Press, 2022
    locator: Chapter 26, Section 26.3, Parallel merge sort (the stable form of the merge without the swap)
  - paper: doi:10.1137/0204030
    title: Leslie G. Valiant, Parallelism in comparison problems, SIAM Journal on Computing 4(3), 1975
    locator: pp. 348 to 355 (merging in O(log log n) rounds of comparisons)
  - paper: doi:10.1109/IPDPSW.2012.202
    title: Saher Odeh, Oded Green, Zahi Mwassi, Oz Shmueli and Yitzhak Birk, Merge Path, parallel merging made simple, IPDPS Workshops, 2012
    locator: the cut of the output into equal pieces by binary search along cross diagonals
---

Parallel merge combines two sorted arrays into one sorted array in the [fork-join](/fork-join-parallelism/) style. It is the divide and conquer form of merge by ranking: take the median $x$ of the longer array, find by [binary search](/binary-search/) how many items of the shorter array come before $x$, write $x$ to its final place, and merge the items on each side of $x$ in two parallel calls. Each call has at most three quarters of the items, so there are $O(\log n)$ levels of calls, each with one binary search of $O(\log n)$ steps. The work is $\Theta(n)$, the same as the sequential [merge](/merging-sorted-lists/), and the span is $\Theta(\log^2 n)$. Used inside [merge sort](/merge-sort/), it gives a sort with span $\Theta(\log^3 n)$.

Notation on this page: $T$ is the source array that holds both inputs, $A$ the output array, and ranges are half open, so $T[p \ldots r - 1]$ has $r - p$ items. $N$ is the size of a call (the items in both of its ranges), and $n$ the size of the first call. $W$ is the work and $S$ the span in the [work-span model](/work-span-model/). $\lg$ is $\log_2$.

## In plain words

Two teams stand in two lines, each sorted by height, and they must form one sorted line.

Pick the person in the middle of the longer line. Look along the shorter line and find where this person would fit. Everyone in front of that point in both lines is shorter, and everyone behind is taller. So the middle person can walk straight to the right place in the final line: count the people in front in both lines.

Now there are two smaller jobs, the people in front and the people behind. They do not share anyone, so two helpers can do them at the same time. Each helper does the same thing again.

The jobs get smaller by at least a quarter each time, so after a small number of steps every job is empty.

## The problem

The input is two sorted ranges $T[p_1 \ldots r_1 - 1]$ and $T[p_2 \ldots r_2 - 1]$ and an output start $p_3$. The output is the sorted merge of the two ranges in $A[p_3 \ldots p_3 + N - 1]$, where $N = (r_1 - p_1) + (r_2 - p_2)$. The output range must share no cell with the inputs. The page [merging sorted sequences](/merging-sorted-sequences/) has the parallel problem in full, with the other methods, and the [parallel merging problem](/parallel-merging-problem/) page has the PRAM bounds.

## The algorithm

```pseudo id=main
P-MERGE(T, p₁, r₁, p₂, r₂, A, p₃)          ▷ merge T[p₁ .. r₁ − 1] and T[p₂ .. r₂ − 1] into A[p₃ ..]
L1  n₁ ← r₁ − p₁; n₂ ← r₂ − p₂
L2  if n₁ < n₂ then                        ▷ make the first range the longer one
L3      exchange p₁ with p₂, and r₁ with r₂
L4      exchange n₁ with n₂
L5  if n₁ = 0 then return                  ▷ both ranges are empty
L6  q₁ ← ⌊(p₁ + r₁) / 2⌋                    ▷ the median of the longer range
L7  q₂ ← LOWER-BOUND(T, p₂, r₂, T[q₁])      ▷ the least q₂ with q₂ = r₂ or T[q₁] ≤ T[q₂]
L8  q₃ ← p₃ + (q₁ − p₁) + (q₂ − p₂)
L9  A[q₃] ← T[q₁]
L10 spawn P-MERGE(T, p₁, q₁, p₂, q₂, A, p₃)
L11 P-MERGE(T, q₁ + 1, r₁, q₂, r₂, A, q₃ + 1)
L12 sync
```

This is P-MERGE of CLRS, 3rd edition, Section 27.3, written with half-open ranges. Lines L2 to L4 make sure that the median comes from the longer range; then both ranges are empty when line L5 finds the longer one empty. Line L7 counts the items of the shorter range that are less than $x = T[q_1]$, and line L8 adds the $q_1 - p_1$ items of the longer range before $x$, which gives the number of items that come before $x$ in the output. The `spawn` of line L10 lets the left call run while line L11 runs the right call, and `sync` waits for both.

P-MERGE-SORT uses it to sort. It sorts the two halves into a temporary array $T$ in parallel and then merges them into the output:

```pseudo
P-MERGE-SORT(A, p, r, B, s)               ▷ sort A[p .. r − 1] into B[s .. s + r − p − 1]
1  n ← r − p
2  if n ≤ 1 then copy A[p .. r − 1] to B[s ..]; return
3  let T[0 .. n − 1] be a new array
4  q ← ⌊(p + r) / 2⌋
5  spawn P-MERGE-SORT(A, p, q, T, 0)
6  P-MERGE-SORT(A, q, r, T, q − p); sync
7  P-MERGE(T, 0, q − p, q − p, n, B, s)
```

The [parallel merge sort](/parallel-merge-sort/) page covers the sort in full, with the stable merge of the 4th edition of CLRS. This page is about the merge and its exact bounds.

## Example

Merge $[1, 3, 5, 7, 9, 11]$ and $[2, 4, 4, 8, 10, 12, 14]$, so $N = 13$. Each row is one call with at least one item; an indent shows a call made by the row above it. The column $j$ is the number of items of the shorter range less than $x$ (line L7), and $q_3$ is the output place of $x$ (line L8).

| call | longer range | shorter range | $x$ | $j$ | probes | $q_3$ |
|---|---|---|---|---|---|---|
| top | 2, 4, 4, 8, 10, 12, 14 | 1, 3, 5, 7, 9, 11 | 8 | 4 | 3 | 7 |
| . left | 1, 3, 5, 7 | 2, 4, 4 | 5 | 3 | 2 | 5 |
| . . left | 2, 4, 4 | 1, 3 | 4 | 2 | 1 | 3 |
| . . . left | 1, 3 | 2 | 3 | 1 | 1 | 2 |
| . . . . left | 1 | 2 | 1 | 0 | 1 | 0 |
| . . . . . right | 2 | (empty) | 2 | 0 | 0 | 1 |
| . . . right | 4 | (empty) | 4 | 0 | 0 | 4 |
| . . right | 7 | (empty) | 7 | 0 | 0 | 6 |
| . right | 10, 12, 14 | 9, 11 | 12 | 2 | 1 | 11 |
| . . left | 9, 11 | 10 | 11 | 1 | 1 | 10 |
| . . . left | 9 | 10 | 9 | 0 | 1 | 8 |
| . . . . right | 10 | (empty) | 10 | 0 | 0 | 9 |
| . . right | 14 | (empty) | 14 | 0 | 0 | 12 |

The top call swaps the ranges, because the second one is longer. Its median is 8, and four items of the first range ($1, 3, 5, 7$) are less than 8, so 8 goes to place $3 + 4 = 7$. The left call then merges the seven items less than 8 into places 0 to 6, and the right call merges the five items greater than 8 into places 8 to 12. The output is $[1, 2, 3, 4, 4, 5, 7, 8, 9, 10, 11, 12, 14]$.

With the cost model of the implementation (2 units for a call plus one for each probe, and 1 for an empty call), the work is 51 and the span is 21: the longest chain is the top call, then left five times, then an empty call, with costs $5 + 4 + 3 + 3 + 3 + 2 + 1$.

## Correctness

The key fact is the split. The items of the longer range before $x$ are at most $x$, and the items after it are at least $x$, because that range is sorted. Line L7 puts the cut of the shorter range at its first item that is at least $x$. So the left call gets only items at most $x$, the right call gets only items at least $x$, and $x$ sits between them at place $p_3$ plus the size of the left call. By induction on $N$ each call writes the sorted merge of its items into its own output range. The two parallel calls only read $T$ and write disjoint parts of $A$, so they have no [determinacy race](/determinacy-race/). The [full proof](proofs/correctness.md) gives each step, and also shows that the merge is not stable and how to make it stable.

## Complexity

The [complexity proof](proofs/complexity.md) has the details. The main facts are:

- **Balanced split.** Since $x$ is the median of the longer range, each call of lines L10 and L11 gets at least $N/4 - 1$ and at most $3N/4$ items, and their sizes add up to $N - 1$.
- **Binary search.** The search of line L7 over $m$ items takes between $\lfloor \lg(m + 1) \rfloor$ and $\lceil \lg(m + 1) \rceil$ probes.
- **Work.** $W(N) = W(N_1) + W(N_2) + O(\log N)$ with $N_1 + N_2 = N - 1$ and both parts at least $N/4 - 1$. The substitution method gives $N \le W(N) \le 10N + 1 - \lg(N + 1)$, so $W = \Theta(n)$.
- **Span upper bound.** $S(N) \le S(3N/4) + O(\log N)$. A chain of calls has at most $\lfloor \log_{4/3} N \rfloor + 1$ calls with items, each of cost at most $\lceil \lg(N + 1) \rceil + 2$, so $S(N) \le (\lfloor \log_{4/3} N \rfloor + 1)(\lceil \lg(N + 1) \rceil + 2) + 1 = O(\log^2 n)$.
- **Span lower bound.** When the two inputs interleave (as the even and the odd numbers do), every call has interleaved inputs, the larger call has at least $(N - 1)/2$ items, and each binary search takes at least $\lg(N + 1) - 2$ probes. This gives $S(N) \ge x(x + 1)/2$ with $x = \lg(N + 1)$, so the span is $\Theta(\log^2 n)$ in the worst case, not only $O(\log^2 n)$.
- **Merge sort.** P-MERGE-SORT has span $S_{\text{sort}}(n) = S_{\text{sort}}(n/2) + \Theta(\log^2 n) = \Theta(\log^3 n)$ and work $\Theta(n \log n)$. The lower bound uses the bit reversal permutation, which makes every merge interleaved.
- **Space.** The output array is separate from the input, and the recursion has depth $O(\log n)$. P-MERGE-SORT allocates a temporary array at each call, $\Theta(n \log n)$ in total over the run, but only $O(n)$ along one chain of calls.

The parallelism is $W/S = \Theta(n / \log^2 n)$. On interleaved inputs of $N = 131072$ items the tests measure work $4.25N$ and span 175, between the lower bound 153 and the upper bound 821. On random inputs of $10^5$ items the work is $4.11N$ and the span is $0.66 \lg^2 N$.

## Properties

- **Deterministic.** There is no random choice.
- **Not in place.** The output goes into a separate array. If the output overlaps the input, line L9 can overwrite an item that a parallel call still has to read.
- **Not stable.** After the swap of lines L2 to L4 the median can come from the second input, and then an equal item of the first input goes after it. The correctness proof gives an example and the fix.
- **Any order.** It uses only comparisons of the form $a \le b$, so it works for any total order.
- **Cut points for free.** The values of $q_1$, $q_2$ and $q_3$ in the top call are a cut of both inputs that splits the output at a known place. The same idea, applied to many places at once, is the [merge path](/merge-path/) method.

## Variants and improvements

- **Stable merge.** Use the lower bound search when the median comes from the first input and the upper bound search (the least index with $x < T[q_2]$) when it comes from the second. CLRS, 4th edition, Section 26.3 does this by writing the two cases out without a swap; the [parallel merge sort](/parallel-merge-sort/) page has that form.
- **Coarse base case.** Below a grain size of some thousands of items, merge sequentially. The bounds stay the same, and the cost of the spawns becomes small against the work.
- **Merge by co-ranking.** Cut the output into $p$ equal pieces, find for each cut the matching places in both inputs by one binary search, and merge the pieces sequentially in parallel. With $p = n / \lg n$ the span is $O(\log n)$ and the work $O(n)$. See [merging sorted sequences](/merging-sorted-sequences/) and [merge path](/merge-path/) (Odeh, Green, Mwassi, Shmueli and Birk 2012).
- **Faster on a CREW PRAM.** [Valiant's merge](/valiant-parallel-merge/) (1975) uses $O(\log \log n)$ rounds of comparisons, and the [Shiloach and Vishkin merge](/shiloach-vishkin-merge/) (1981) reaches $O(\log n)$ time with $O(n)$ work.
- **Many inputs.** For $k$ sorted inputs, merge them in pairs in a tree of depth $\lceil \lg k \rceil$, or use a [$k$-way merge](/k-way-merge/) with a parallel cut of all inputs at once.

## When to use it

- Use it inside a fork-join merge sort on a multicore machine, where it removes the $\Theta(n)$ span of the sequential merge, which would cap the parallelism of merge sort at $O(\log n)$.
- Use it when the code must be short and needs no tuning: one binary search and two recursive calls.
- Use merge by co-ranking when the number of workers $p$ is known, as on a GPU or with a fixed thread pool. It does $p$ binary searches and then $p$ sequential merges with good memory locality, and has smaller span.
- Use a sequential merge for small inputs. The span of P-MERGE helps only when $n$ is much larger than the grain size times the number of workers.

## Pitfalls

- **Leaving out the swap.** Without lines L2 to L4, line L5 can return when the first range is empty and the second is not, and those items are lost. Even with a correct base case, the median of a much shorter first range does not split the longer one, so the bound of three quarters per call fails and so does the span bound.
- **Forgetting one input in the place.** Line L8 must add both counts, $q_1 - p_1$ from the longer range and $q_2 - p_2$ from the shorter one. With one of them, items land in the wrong places, and two calls can write the same cell.
- **Merging into the input.** If $A$ overlaps $T$, the write of line L9 races with the reads of the other calls. This is why P-MERGE-SORT merges from a temporary array.
- **Expecting a stable merge.** Line L7 sends items of the shorter range that are equal to $x$ to the right, whichever input that range came from. A sort that must be stable needs the stable variant.
- **Too fine a grain.** Line L10 spawns a task for every item down to the leaves. In practice the cost of a spawn is many times the cost of a comparison, so the base case must be a sequential merge of a block of items.

## Implementations

## History

Fast parallel merging was studied first for comparison models and the PRAM. Valiant (1975) showed that two sorted lists can be merged in $O(\log \log n)$ rounds of comparisons, and Shiloach and Vishkin (1981) gave a work-efficient merge for the CREW PRAM. The median split with a binary search in the other array is the divide and conquer form of merge by ranking. CLRS, 3rd edition (2009), Section 27.3, presents it as P-MERGE in the fork-join model and proves the bounds $\Theta(n)$ work and $\Theta(\log^2 n)$ span, with P-MERGE-SORT of span $\Theta(\log^3 n)$. The 4th edition (2022), Section 26.3, replaces it by a stable form without the swap. Odeh, Green, Mwassi, Shmueli and Birk (2012) described merge path, which cuts the output into equal pieces for a fixed number of workers.

## References
