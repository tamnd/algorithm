---
tag: CATDWP
kind: technique
slug: array-doubling
name: Array doubling
aliases:
- doubling strategy
- dynamic array doubling
- dynamic table doubling
- geometric growth
area: foundations/amortized-analysis
level: intro
summary: Grow an array by doubling when full, so n appends cost O(n) total and O(1) amortized each.
prereqs: [amortized-cost, potential-method, geometric-series]
see_also: [dynamic-array, dynamic-array-resizing, dynamic-table-contraction, global-rebuilding, hash-table, rehashing, load-factor, amortized-vs-worst-case]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.4.1, Table expansion
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (resizing-array implementation of a stack) and Section 1.4 (amortized analysis)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
---

Array doubling is the rule that a [dynamic array](/dynamic-array/) follows when an append finds the array full: allocate a new array of twice the capacity, copy the items, and free the old array. One append can then copy all $n - 1$ items, but the copies of $n$ appends from an empty array add up to $2^{\lceil \lg n \rceil} - 1 < 2n$, so each append has [amortized cost](/amortized-cost/) at most 3. Each growth by a constant factor greater than 1 gives $O(1)$ amortized cost; growth by a constant number of slots gives $\Theta(n)$. The same rule resizes [hash tables](/hash-table/), heaps and buffers.

## In plain words

An array has a fixed size. To add an item to a full array, you must get a larger array and copy all items into it. If the new array has only one more slot, you copy at every append, and the work grows with the square of the number of items. If the new array is twice as large, a copy happens only when the number of items reaches 1, 2, 4, 8 and so on. Each copy is large, but the next one comes only after as many cheap appends as there are items. The sum of all copies is less than two times the number of items. So, on average over the run, each append costs a small constant, even though one append now and then is slow.

## When it applies

- A container must give $O(1)$ access by index, so its items must be in one block of memory, and the final size is not known in advance.
- The cost of growing is proportional to the current size (a copy, a rehash, a rebuild), and the structure stays usable up to a fixed fill level.
- The program can accept a rare slow operation. If it cannot, use the incremental version under [global rebuilding](/global-rebuilding/).
- If items are also removed, add a contraction rule; see [dynamic table contraction](/dynamic-table-contraction/).

## The template

The array has a capacity $c$ and a count $n \le c$ of items. It starts empty with $c = 0$.

```pseudo id=main
APPEND(T, x)
L1  if T.n = T.c then                        ▷ the array is full
L2      c' ← max(1, GROW(T.c))                ▷ hole: the growth rule, 2c for doubling
L3      B ← allocate an array of capacity c'
L4      copy T[0 .. T.n − 1] into B           ▷ T.n copies
L5      free the old array, T ← B, T.c ← c'
L6  T[T.n] ← x                                ▷ 1 write
L7  T.n ← T.n + 1
```

**Cost model.** An append costs 1 for the write of line L6, plus 1 for each item copied in line L4. Allocation and freeing are counted as $O(1)$; see the pitfalls for when this is false.

**Theorem.** With GROW$(c) = 2c$, $n \ge 1$ appends from the empty array copy exactly $2^{\lceil \lg n \rceil} - 1$ items and cost $n + 2^{\lceil \lg n \rceil} - 1 < 3n$ in total. Each append has amortized cost 3. For $n \ge 2$, the largest single cost among the first $n$ appends is $2^{\lceil \lg n \rceil - 1} + 1$, which is $\Theta(n)$.

### Proof by the aggregate method

The capacities are $0, 1, 2, 4, \ldots$. An expansion happens at the append that finds $n$ items in an array of capacity $n$, so at the appends number $1, 2, 3, 5, 9, \ldots, 2^j + 1$, and the one at number $2^j + 1$ copies $2^j$ items. Among the first $n$ appends, these are the ones with $2^j + 1 \le n$, that is $j \le \lceil \lg n \rceil - 1$. So the copies are

$$\sum_{j=0}^{\lceil \lg n \rceil - 1} 2^j = 2^{\lceil \lg n \rceil} - 1 < 2n,$$

since $2^{\lceil \lg n \rceil} < 2n$. Add $n$ writes to get the total. $\square$

### Proof by the accounting method

Charge 3 for each append. Invariant: after an expansion from capacity $c$ to $2c$, the $c$ copied items hold no coins, and each item appended after the copy holds 2 coins. An append pays 1 for its write and puts 2 coins on its item. When the array of capacity $2c$ is full again, $c$ items were appended after the last copy and they hold $2c$ coins, which pay for the $2c$ copies of the next expansion. Each new item pays for its own copy and for the copy of one old item. The first expansion copies nothing, and the second copies one item that holds 2 coins. The coins are never negative, so $n$ appends cost at most $3n$. $\square$

### Proof by the potential method

Let $\Phi = 2n - c$ for a non-empty array and $\Phi = 0$ for the empty array. Each reachable non-empty array is at least half full: after an expansion of a full array of capacity $c \ge 1$, it holds $c + 1$ items in capacity $2c$; the first append gives $n = c = 1$; and appends without expansion only raise $n$. So $\Phi \ge 0$ in each reachable state.

- **No expansion.** $\hat c = 1 + 2 = 3$.
- **Expansion from capacity $c \ge 1$.** Before: $n = c$, $\Phi = c$. After: $n = c + 1$, capacity $2c$, $\Phi = 2$. Actual cost $c + 1$. So $\hat c = c + 1 + 2 - c = 3$.
- **The first append.** From $\Phi = 0$ to $n = c = 1$, $\Phi = 1$, actual cost 1, so $\hat c = 2$.

So each append has $\hat c \le 3$ and the total is at most $3n$. $\square$

The constant 3 is tight: for $n = 2^j + 1$ the total is $2^j + 1 + 2^{j+1} - 1 = 3n - 3$. For $n = 1025$ this is 3072.

### Other growth factors

Let GROW$(c) = \lceil \gamma c \rceil$ for a constant $\gamma > 1$. Let $m_1 < m_2 < \cdots < m_r$ be the capacities at which an expansion happens among $n$ appends. The last one copies $m_r \le n - 1$ items, and $m_{j+1} \ge \gamma m_j$, so $m_{r-i} \le (n-1)/\gamma^i$. So

$$\text{copies} \le (n - 1) \sum_{i \ge 0} \gamma^{-i} = (n-1)\frac{\gamma}{\gamma - 1},$$

and the amortized cost of an append is at most $1 + \gamma/(\gamma - 1)$: 3 for $\gamma = 2$, 4 for $\gamma = \tfrac32$, 2.5 for $\gamma = 3$. The capacity can be up to $\gamma$ times the count, so a smaller $\gamma$ wastes less memory and copies more. For $n = 10^6$ appends the copies are 2,099,719 for $\gamma = \tfrac32$, 1,048,575 for $\gamma = 2$ and 797,161 for $\gamma = 3$, each below its bound.

**Additive growth is quadratic.** If GROW$(c) = c + K$ for a constant $K$, an expansion happens after each $K$ appends, and the $i$-th one copies $iK$ items. For $n = qK$ appends the copies are $K \cdot q(q-1)/2 = \Theta(n^2/K)$. For $K = 10$, 1000 appends cost 50,500 and 10,000 appends cost 5,005,000.

## Classic examples

- **[Dynamic array](/dynamic-array/).** The vector or list type of most languages appends in $O(1)$ amortized time by geometric growth.
- **[Hash table](/hash-table/) [rehashing](/rehashing/).** When the [load factor](/load-factor/) passes a threshold, the table doubles and reinserts each key. The doubling argument gives $O(1)$ amortized cost per insert for the rehashing, on top of the expected cost of the insert itself.
- **[Binary heap](/binary-heap/) and [stack](/stack/) in an array.** A heap or a stack of unknown size grows its array by doubling.
- **[Dynamic table contraction](/dynamic-table-contraction/).** With deletions, the table also halves when it is a quarter full, and both operations stay $O(1)$ amortized.
- **Buffers and string builders.** A buffer that collects output of unknown length doubles its capacity, so building a string of length $n$ by appends takes $O(n)$ time.

## Variations

- **A constant factor other than 2.** Any $\gamma > 1$ gives $O(1)$ amortized cost, with the bound $1 + \gamma/(\gamma - 1)$ above. The choice trades copies against unused memory.
- **Incremental copying.** Allocate the array of capacity $2c$ when the array of capacity $c$ is full, and move 2 old items at each later append. All old items have moved after $\lceil c/2 \rceil$ appends, long before the new array is full, and no append does more than 3 units of work. This is the [global rebuilding](/global-rebuilding/) of the array.
- **Contraction.** To keep the memory proportional to the count under deletions, halve the capacity when the array is a quarter full, not half full. See [dynamic table contraction](/dynamic-table-contraction/).
- **Blocks without copying.** Keep a list of blocks of sizes $1, 2, 4, \ldots$ and never copy. Access by index then needs the position of the highest 1 bit of the index to find the block, and the memory is not one block.

## Pitfalls

- **Additive growth.** Growing by a fixed number of slots, such as 10 or 4096, looks safe but costs $\Theta(n^2)$ for $n$ appends.
- **A potential that goes negative.** $\Phi = 2n - c$ is valid only because each reachable array is at least half full. If the program can call a "reserve" operation that sets a large capacity, or if the array shrinks, a reachable state can have $2n < c$ and $\Phi < 0$. Then use $\Phi = \max(0, 2n - c)$, and check the cases again: an append without expansion still raises it by at most 2.
- **Latency.** The amortized bound says nothing about one append. The append that grows an array of $2^{20}$ items copies 1,048,576 items. In a real-time or interactive program, use incremental copying or a fixed capacity.
- **The cost of allocation.** If the allocator fills new memory with zeros, the allocation of line L3 costs $\Theta(c')$, not $O(1)$. The bound stays $O(1)$ amortized, with a larger constant, but the incremental version is no longer $O(1)$ worst-case unless the memory is left uninitialized.
- **Peak memory.** During the copy, the old and the new arrays exist together: $c + 2c = 3c$ slots for $c$ items. After the copy, the capacity is up to twice the count.
- **References into the array.** After an expansion the items are in new memory, so pointers, iterators and references to the old array are invalid.
- **Persistence.** If old versions of the array are kept and appended to (for example, by copying the handle in a functional program), the same full array can be expanded many times, and the amortized bound is lost.

## Exercises

1. Show that with GROW$(c) = 2c$ and an array that starts with capacity $c_0 \ge 1$ and no items, $n$ appends cost less than $3n$.
2. A stack in an array doubles when full and never shrinks. Show that $n$ pushes and pops in any order cost $O(n)$.
3. For growth by a factor $\gamma > 1$ with $\gamma c$ an integer at each expansion, show that $\Phi = \frac{\gamma}{\gamma - 1}\left(n - \frac{c}{\gamma}\right)$ is a valid potential and gives the amortized cost $1 + \gamma/(\gamma - 1)$.

## References
