---
tag: NT62MZ
kind: technique
slug: dynamic-array-resizing
name: Dynamic array resizing
aliases:
- Array resizing
area: data-structures/linear-structures
level: intro
summary: Keeps an array's capacity matched to its size by doubling when full and halving when sparse, giving constant amortized cost per operation.
prereqs: [dynamic-array, array-doubling, potential-method]
see_also: [dynamic-table-contraction, load-factor, rehashing, global-rebuilding, hash-table, circular-buffer, amortized-vs-worst-case, binary-heap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.4 (Dynamic tables), with 16.4.1 (Table expansion) and 16.4.2 (Table expansion and contraction)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Resizing array (ResizingArrayStack), and Section 1.4, the amortized analysis of array resizing
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
---

Dynamic array resizing is the technique of rebuilding an array-based structure at a new capacity whenever its size leaves a fixed band of load factors: grow by a constant factor when the array gets too full, and shrink by the same factor when it gets too empty. Each rebuild costs time in proportion to the capacity, but the band guarantees that a number of operations in proportion to the capacity happens between two rebuilds. So each insert and delete costs $O(1)$ [amortized](/amortized-cost/), and the space stays within a constant factor of the size. The [dynamic array](/dynamic-array/), the resizing [hash table](/hash-table/), the array [binary heap](/binary-heap/) and the growable [circular buffer](/circular-buffer/) all use it.

## In plain words

A structure keeps its items in a block of fixed size. When the block fills up, you build a larger block and move everything. When most of the block is empty, you build a smaller one. Moving everything is slow, so you want to do it rarely.

The trick is to change the size by a factor, for example two, and to leave a wide gap between the "too full" and the "too empty" rules. Right after a move, the block is comfortably in the middle. So many cheap operations must happen before the next move, and those operations pay for it. If the two rules were close to each other, a few operations could push the block back and forth between two sizes, and every one of them would be slow.

## When it applies

- The structure stores its items in one array of capacity $c$, and an operation is fast only while the size $n$ stays below some limit, such as $n \le c$ for a plain array or $n \le c/2$ for a hash table with open addressing.
- The program cannot know the final size in advance, or the size goes up and down a lot.
- A rebuild at a new capacity is possible in $O(c)$ time: copy the items, rehash them, or rebuild the structure from them.
- An amortized bound is enough. A single operation may take $\Theta(n)$ time. If that pause is not allowed, use a deamortized variant below.

## The template

The holes are the four constants HIGH, LOW, GROW and MIN-CAP, and the procedure PLACE that puts an item into a new block.

```pseudo id=main
AFTER-UPDATE(T)                            ▷ run after each insert or delete
L1  if T.n > HIGH · T.cap then
L2      REBUILD(T, GROW · T.cap)
L3  else if T.cap > MIN-CAP and T.n < LOW · T.cap then
L4      REBUILD(T, T.cap / GROW)
REBUILD(T, c)
L5  B ← an empty block of capacity c
L6  for each item x of T
L7      PLACE(B, x)                        ▷ copy to the same index, or rehash
L8  T.block ← B, T.cap ← c
```

Line L1 tests the upper limit of the load $n / cap$, and line L3 the lower limit. REBUILD makes a new block and moves each item with PLACE, which costs $O(1)$ per item, so a rebuild costs $O(cap)$.

**The rule that makes it work.** Choose the constants with $\text{GROW} > 1$ and

$$\text{LOW} \cdot \text{GROW} < \text{HIGH}.$$

After a grow, the load is about $\text{HIGH}/\text{GROW}$, and after a shrink it is about $\text{LOW} \cdot \text{GROW}$. The rule puts both values strictly inside the band $(\text{LOW}, \text{HIGH})$, since $\text{HIGH}/\text{GROW} > \text{LOW}$ is the same inequality. Let $\delta > 0$ be the smallest distance from these two loads to the ends of the band. Each insert or delete changes $n$ by 1, so after a rebuild to capacity $c$, at least $\delta c - 1$ operations must happen before the load leaves the band again (the $-1$ covers the rounding of $n$ to an integer). The next rebuild costs $O(c)$, and it can be charged to those operations, which gives $O(1/\delta)$ amortized time for each. For a precise constant, use the [potential method](/potential-method/): with $\text{HIGH} = 1$, $\text{GROW} = 2$ and $\text{LOW} = 1/4$, the potential $2n - cap$ above half load and $cap/2 - n$ below it gives at most 3 per insert and 2 per delete, as proved on the [dynamic array](/dynamic-array/) page.

The common choice is $\text{HIGH} = 1$, $\text{GROW} = 2$, $\text{LOW} = 1/4$: grow when full, shrink when a quarter full, and land at half load either way. The space is then less than $4n$ cells for $n \ge 1$.

## Classic examples

- **[Dynamic array](/dynamic-array/).** PLACE copies item $i$ to cell $i$. HIGH is 1, because an array cannot hold more items than cells. This is the simplest case and the one that the other examples copy.
- **Resizing stack.** Sedgewick and Wayne's resizing-array [stack](/stack/) doubles on a full push and halves when a pop leaves it a quarter full. It is the dynamic array with only the end operations.
- **[Circular buffer](/circular-buffer/) as an unbounded queue.** PLACE copies the items in queue order, from the head, to cells $0, 1, 2, \ldots$ of the new block, and resets the head to 0. A plain copy of the old block would break the wrap-around.
- **[Binary heap](/binary-heap/).** The heap lives in an array, so it grows by doubling. The heap order does not change, because PLACE keeps every index.
- **[Hash table](/hash-table/) with [rehashing](/rehashing/).** HIGH is the largest allowed [load factor](/load-factor/), for example $3/4$, and PLACE recomputes the slot of each key for the new size. For [open addressing](/open-addressing/), HIGH must stay below 1 to keep probe sequences short.
- **[Cuckoo hashing](/cuckoo-hashing/).** A rebuild is also triggered when an insert fails, not only by the load. The same accounting covers it if failures are rare.

## Variations

- **Other factors.** Any $\text{GROW} > 1$ works. A factor of 1.5 wastes less space after a grow than 2, and it lets a memory allocator reuse freed blocks. The cost is more rebuilds: $m$ appends make between about $m / (\text{GROW} - 1)$ and $m \cdot \text{GROW} / (\text{GROW} - 1)$ copies.
- **Grow only.** Many libraries never shrink, which removes the test of line L3. Then the space is the largest size ever reached, not the current size.
- **[Dynamic table contraction](/dynamic-table-contraction/).** The analysis of grow and shrink together, with the thresholds that avoid thrashing, is on its own page.
- **Incremental resizing.** Allocate the new block when the old one reaches the threshold, and move a constant number of items with each later operation. Every operation then costs $O(1)$ in the worst case. Linear hashing and incremental rehashing in hash tables use this idea.
- **[Global rebuilding](/global-rebuilding/).** The same accounting applies to any structure that is rebuilt from scratch after a number of updates in proportion to its size, for example to rebalance a tree or to clean up deleted entries.
- **Reserve.** When the final size is known, allocate it at once (`reserve` in C++, an initial capacity in Java). This removes all rebuilds.

## Pitfalls

- **Additive growth.** Writing line L2 as `REBUILD(T, T.cap + k)` for a constant $k$ makes $m$ appends cost $\Theta(m^2 / k)$. The growth must be by a factor.
- **Thresholds too close.** With $\text{LOW} = 1/2$ and $\text{GROW} = 2$, the rule $\text{LOW} \cdot \text{GROW} < \text{HIGH}$ fails for $\text{HIGH} = 1$. Then an insert at a full table grows it to half load, and one delete shrinks it back, so alternating inserts and deletes cost $\Theta(n)$ each.
- **Capacity zero.** If MIN-CAP is 0, a shrink can reach capacity 0, and line L2 then computes $2 \cdot 0 = 0$. Keep MIN-CAP at 1 or more, or grow to $\max(1, \text{GROW} \cdot cap)$.
- **Copying the block, not the items.** For a circular buffer or a hash table, the position of an item depends on the capacity. A raw copy of the old block into the new one puts items in the wrong cells. PLACE must recompute each position.
- **Stale pointers.** Any pointer or iterator into the old block is invalid after line L8.
- **Claiming a worst-case bound.** The bound is amortized. One operation can still take $\Theta(n)$ time, which matters in real-time code and under a lock.

## Exercises

1. Take $\text{HIGH} = 1$, $\text{GROW} = 3$ and $\text{LOW} = 1/6$. Check the rule $\text{LOW} \cdot \text{GROW} < \text{HIGH}$, give the load right after a grow and right after a shrink, and give the largest space used for $n$ items.
2. For $\text{HIGH} = 1$, $\text{GROW} = 2$ and $\text{LOW} = 1/2$, give a sequence of $2k$ operations on a table with $n$ items that makes $2k$ rebuilds, each of cost at least $n/2$.
3. A hash table with linear probing must keep its load factor at most $1/2$. Choose HIGH, LOW and GROW, and find the smallest number of operations between two rebuilds of a table of capacity $c$.
4. Show that growing the capacity from $c$ to $c + \lceil \sqrt{c} \rceil$ makes $m$ appends cost $\Theta(m^{3/2})$ in total.
5. Design an incremental version of the dynamic array in which each append moves at most two old items, and prove that the old block is empty before the new block is full.

## References
