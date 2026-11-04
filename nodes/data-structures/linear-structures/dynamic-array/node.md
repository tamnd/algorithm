---
tag: 9C8NGV
kind: data-structure
slug: dynamic-array
name: Dynamic array
aliases:
- resizable array
- vector
- ArrayList
area: data-structures/linear-structures
level: intro
summary: Array that reallocates and copies when full, giving amortized O(1) append.
implements: [list, stack]
prereqs: [array, amortized-cost]
see_also: [dynamic-array-resizing, array-doubling, dynamic-table-contraction, potential-method, linked-list, circular-buffer, gap-buffer, persistent-vector]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.4 (Dynamic tables), Sections 16.4.1 and 16.4.2 for expansion and for expansion with contraction
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Resizing array (ResizingArrayStack, Algorithm 1.1) and its amortized analysis in Section 1.4
  - paper: "Andrej Brodnik, Svante Carlsson, Erik D. Demaine, J. Ian Munro and Robert Sedgewick, Resizable arrays in optimal time and space, Algorithms and Data Structures (WADS 1999), Lecture Notes in Computer Science 1663 (1999)"
    locator: the lower bound of order square root of n on the extra space, and the matching structure
---

A dynamic array is an [array](/array/) that grows: it keeps its items in a block of capacity $c$, and when an append finds the block full, it allocates a block of capacity $2c$, copies the $n$ items and frees the old block. A single append can cost $\Theta(n)$, but any sequence of $m$ appends and removals from the end costs $O(m)$ in total, so each costs $O(1)$ [amortized](/amortized-cost/). Reads and writes by index stay $\Theta(1)$ in the worst case. It is the `vector` of C++, the `ArrayList` of Java and the `list` of Python, and it is the default sequence type of most programs.

## In plain words

You keep a row of boxes for your items. When the row is full and a new item comes, you get a new row twice as long, move every item over, and throw the old row away. Moving all items is slow, but it happens rarely: after a move to a row of length 16, the next seven items go in with no move at all.

If you count the work over many appends, each append pays for itself plus a small, fixed share of the next big move. So appends are fast on average, even though one of them is now and then slow.

When many items are removed, the row is mostly empty. Then you move the items to a row half as long, so that the space stays in proportion to the number of items.

## The abstract type

A dynamic array implements the [list](/list/) type with fast access by index, and the [stack](/stack/) type with push and pop at the end. Its operations are `get(D, i)` and `set(D, i, x)` for $0 \le i < n$, `append(D, x)`, which adds $x$ at the end, and `pop(D)`, which removes and returns the last item. Insert and delete at a position $i$ work as in an [array](/array/), by shifting the items after $i$, and cost $\Theta(n - i + 1)$ plus a possible resize.

## Representation

The fields are a block $D.A$ of $D.cap$ cells, and the count $D.n$. The structure starts with $n = 0$ and $cap = 1$.

**Invariant.** (I1) $0 \le n \le cap$, and the list held is $(A[0], \ldots, A[n-1])$. (I2) $cap$ is a power of two, and $cap < 4 \max(n, 1)$.

Part (I2) says that the block is never more than four times larger than needed, so the space is $\Theta(n + 1)$.

## Operations

```pseudo id=main
APPEND(D, x)
L1  if D.n = D.cap then RESIZE(D, 2 · D.cap)
L2  D.A[D.n] ← x
L3  D.n ← D.n + 1
POP(D)                                     ▷ D.n > 0
L4  D.n ← D.n − 1
L5  x ← D.A[D.n]
L6  if D.n > 0 and 4 · D.n = D.cap then RESIZE(D, D.cap / 2)
L7  return x
RESIZE(D, c)                               ▷ c ≥ D.n
L8  B ← a new block of c cells
L9  for i ← 0 to D.n − 1
L10     B[i] ← D.A[i]
L11 D.A ← B, D.cap ← c
```

APPEND writes $x$ into the first free cell. If there is no free cell, line L1 first doubles the capacity. POP removes the last item. If the block is then only one quarter full, line L6 halves the capacity, which leaves the block half full. RESIZE copies the $n$ items to a new block, so it makes $n$ copies.

GET and SET are those of the [array](/array/): one access to $A[i]$, in $\Theta(1)$ worst-case time. They never resize.

The two thresholds differ on purpose. The array grows when it is full and shrinks when it is a quarter full. After any resize, it is exactly half full, so at least $cap/4$ more operations must happen before the next resize. With the same threshold for both, a sequence that alternates APPEND and POP at the boundary would resize at each step.

## Example

Start with $n = 0$ and $cap = 1$. The cost of an operation is 1 for the write or the read, plus the number of copies in RESIZE. The column $\Phi$ is the potential of the proof below, after the operation; at the start, $\Phi = 1/2$.

| operation | items | $n$ | $cap$ | copies | cost | $\Phi$ | amortized cost |
|---|---|---|---|---|---|---|---|
| append(1) | [1] | 1 | 1 | 0 | 1 | 1 | 1.5 |
| append(2) | [1, 2] | 2 | 2 | 1 | 2 | 2 | 3 |
| append(3) | [1, 2, 3] | 3 | 4 | 2 | 3 | 2 | 3 |
| append(4) | [1, 2, 3, 4] | 4 | 4 | 0 | 1 | 4 | 3 |
| append(5) | [1, 2, 3, 4, 5] | 5 | 8 | 4 | 5 | 2 | 3 |
| pop → 5 | [1, 2, 3, 4] | 4 | 8 | 0 | 1 | 0 | −1 |
| pop → 4 | [1, 2, 3] | 3 | 8 | 0 | 1 | 1 | 2 |
| pop → 3 | [1, 2] | 2 | 4 | 2 | 3 | 0 | 2 |
| pop → 2 | [1] | 1 | 2 | 1 | 2 | 0 | 2 |
| pop → 1 | [] | 0 | 2 | 0 | 1 | 1 | 2 |

The ten operations make 10 copies and cost 20 in total. The amortized costs add up to $20.5$, and the two totals agree by the identity of the potential method: $\sum \text{cost} = \sum \text{amortized} + \Phi_0 - \Phi_{\text{end}} = 20.5 + 0.5 - 1 = 20$. No amortized cost is above 3.

## Correctness

APPEND and POP keep (I1) as the array operations do: the new item goes to cell $n$, and POP returns the item of cell $n - 1$. RESIZE copies $A[0 \ldots n-1]$ to the same indices of the new block, so it does not change the list. For (I2), a grow happens only when $n = cap$, and it gives $cap = 2n < 4(n + 1)$; a shrink happens exactly when $n$ drops to $cap/4$, and it gives $cap = 2n$; and a power of two that is at least 4 is a multiple of 4, so it cannot lie strictly between $4(n-1)$ and $4n$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost model is the [random-access machine](/random-access-machine/). We count one unit for each item written or read by APPEND and POP, and one unit for each copy in line L10.

| operation | worst case | amortized |
|---|---|---|
| get, set | $\Theta(1)$ | $\Theta(1)$ |
| append | $\Theta(n)$ | $O(1)$, at most 3 |
| pop | $\Theta(n)$ | $O(1)$, at most 2 |
| insert, delete at index $i$ | $\Theta(n)$ | $\Theta(n - i + 1)$ |
| space | $cap < 4 \max(n, 1)$ cells | |

**Amortized bound.** Use the [potential method](/potential-method/) with

$$\Phi = \begin{cases} 2n - cap & \text{if } 2n \ge cap, \\ cap/2 - n & \text{if } 2n < cap. \end{cases}$$

The potential is never negative, and it is $1/2$ at the start. A grow happens at $n = cap$, where $\Phi = cap$; after it $n = cap + 1$ in a block of $2 \cdot cap$, so $\Phi = 2$. The copies cost $cap$, and the drop of $\Phi$ pays for them, so the amortized cost of that append is $1 + cap + (2 - cap) = 3$. A shrink happens when $n$ drops to $k = cap/4$ with $k \ge 2$; before it $\Phi = cap/2 - (k + 1) = k - 1$, after it $\Phi = 0$, so the amortized cost is $1 + k - (k - 1) = 2$. The other cases are checked in [the complexity proof](proofs/complexity.md). So $m$ operations from the start cost at most $3m + 1/2$ in total.

**Appends only.** For $m \ge 2$ appends from $cap = 1$, the resizes copy blocks of $1, 2, 4, \ldots, 2^k$ items with $2^k \le m - 1 < 2^{k+1}$, so the total number of copies is $2^{k+1} - 1 \le 2m - 3$. The total cost is less than $3m$.

**Any factor larger than 1.** If the capacity grows by a factor $r > 1$, the copies of $m$ appends add up to about $m \cdot r/(r - 1)$ at most, so append is still $O(1)$ amortized. A smaller $r$ wastes less space, and a larger $r$ copies less.

**Lower bound on space.** Brodnik, Carlsson, Demaine, Munro and Sedgewick (1999) showed that any resizable array with $O(1)$ time for access and for append must, at some point, use $\Omega(\sqrt{n})$ extra cells, and they gave a structure that meets this bound. The doubling array uses up to $n$ extra cells after a grow.

## Variants

- **Other growth factors.** Java's `ArrayList` grows to about 1.5 times its capacity. Python's `list` grows by about one eighth more than the new size. Any factor $r > 1$ gives $O(1)$ amortized appends.
- **No shrinking.** Most library vectors never shrink on their own. They offer a call such as `shrink_to_fit` in C++ or `trimToSize` in Java instead. Then (I2) does not hold, and the space is the largest size reached.
- **Worst-case $O(1)$ append.** Allocate the new block early and copy two old items with each append. When the old block is full, the new one already holds all items. This removes the long pauses, at the cost of two blocks in memory.
- **Circular dynamic array.** A [circular buffer](/circular-buffer/) that doubles when full gives a deque with $O(1)$ amortized operations at both ends.
- **Tiered and square-root structures.** The structure of Brodnik and others keeps $O(\sqrt{n})$ blocks of size $O(\sqrt{n})$, which meets the space lower bound.
- **Persistent vector.** A [persistent vector](/persistent-vector/) is a wide tree that keeps old versions; it trades $O(1)$ access for $O(\log_{32} n)$.

The general method of growing and shrinking a table by constant factors is described on the page [dynamic array resizing](/dynamic-array-resizing/).

## When to use it

Use a dynamic array as the default sequence: when the size is not known in advance, and the program appends, reads by index and scans. It uses less memory than a [linked list](/linked-list/), because there is no pointer per item, and it scans much faster, because the items are contiguous. Use a linked list instead when the program must insert or delete in the middle at a node it holds, or when items must never move in memory. Use a fixed [array](/array/) when the size is known, to avoid the extra capacity. In a real-time system, where a single $\Theta(n)$ pause is not allowed, use the worst-case variant or reserve the capacity in advance.

## Pitfalls

- **Growing by a constant.** Writing line L1 as `RESIZE(D, D.cap + 10)` makes $m$ appends copy about $m^2/20$ items, so the total time is $\Theta(m^2)$. Multiply the capacity, do not add to it.
- **Shrinking at one half.** With `if 2 · D.n = D.cap` in line L6, the sequence append, pop, append, pop at $n = cap$ resizes on every operation, and each costs $\Theta(n)$. Shrink at one quarter, as in line L6.
- **Capacity zero.** Starting with $cap = 0$ and doubling gives $0$ forever. Start with $cap \ge 1$, or use $\max(1, 2 \cdot cap)$.
- **Stale references.** A pointer, a reference or an iterator to a cell of the old block is invalid after RESIZE. In C++, `push_back` invalidates all iterators when it reallocates.
- **Overflow of the capacity.** In fixed-width arithmetic, $2 \cdot cap$ can overflow. Check it against the largest allowed size before line L1.

## Implementations

## History

The doubling table is a standard example of amortized analysis. CLRS analyses it with the accounting and potential methods in Section 16.4, with the same rule to contract at one quarter, and Sedgewick and Wayne use it for their resizing-array stack. In 1999, Brodnik, Carlsson, Demaine, Munro and Sedgewick proved that $\Omega(\sqrt{n})$ extra space is necessary for a resizable array with constant-time access and append, and that this space is enough.

## References
