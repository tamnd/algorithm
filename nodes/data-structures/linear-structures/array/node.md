---
tag: 43DJ9Z
kind: data-structure
slug: array
name: Array
aliases:
- static array
area: data-structures/linear-structures
level: intro
summary: Contiguous block of cells indexed by integer position, with O(1) access by index.
prereqs: [random-access-machine, asymptotic-notation]
see_also: [dynamic-array, linked-list, list, row-major-order, circular-buffer, binary-search, sparse-vector, gap-buffer]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1 (Simple array-based data structures), the part on arrays and their address arithmetic
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.2 (Sequential allocation) and Section 2.2.6 (Arrays and orthogonal lists)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.1, Arrays
  - paper: "J. W. Backus and others, The FORTRAN automatic coding system, Proceedings of the Western Joint Computer Conference (1957)"
    locator: the description of subscripted variables and the DIMENSION statement
---

An array is a block of $N$ memory cells of the same size, stored one after the other, where the cell with index $i$ is at address $a + i \cdot s$ for the base address $a$ and the cell size $s$. Because the address of each cell is one multiplication and one addition away, reading or writing $A[i]$ costs $\Theta(1)$ on the [random-access machine](/random-access-machine/). The price is a fixed capacity and a costly insert or delete in the middle: $\Theta(n - i)$ items must move. The array is the base of almost every other structure: [dynamic arrays](/dynamic-array/), heaps, hash tables, [circular buffers](/circular-buffer/) and the matrices of numerical code.

## In plain words

Think of a row of numbered mailboxes in a wall, all of the same width. If you know where the first box is and how wide a box is, you can walk straight to box number 500 without looking at the 499 boxes before it. That is why an array finds an item by its number in one step.

The row has a fixed length, because the wall around it is already built. To put a new letter between box 3 and box 4, you must move the letters of box 4 and of every box after it one place to the right. To take a letter out of the middle, you must move the later letters one place to the left. So an array is fast to read and slow to change in the middle.

## The abstract type

A plain array of length $N$ supports `new(N)`, `get(A, i)`, `set(A, i, x)` and `length(A)` for $0 \le i < N$. These are the operations of a fixed-length sequence.

With a count $n$ of the cells in use, the same block also implements the [list](/list/) type with a bounded size: `insert(A, i, x)` for $0 \le i \le n < N$, `delete(A, i)` for $0 \le i < n$, and `search(A, x)`. This page describes that partially filled array, because the cost of insert and delete is the main fact to know about arrays. A [dynamic array](/dynamic-array/) removes the bound $N$.

## Representation

The fields are the base address $a$, the cell size $s$, the capacity $N$, the count $n$ and the cells $A[0 \ldots N-1]$.

**Address rule.** The cell $A[i]$ occupies the bytes from $a + i s$ to $a + (i+1) s - 1$. The hardware reads it with one address computation and one memory access. For a matrix stored in [row-major order](/row-major-order/) with $c$ columns, the item $M[r][k]$ is the cell $A[r c + k]$.

**Invariant.** $0 \le n \le N$, and the list that the array holds is $(A[0], A[1], \ldots, A[n-1])$. The cells $A[n \ldots N-1]$ hold no item of the list, and their contents do not matter.

## Operations

```pseudo id=main
GET(A, i)                                  ▷ 0 ≤ i < n
L1  return A[i]                            ▷ the cell at address a + i · s
SET(A, i, x)                               ▷ 0 ≤ i < n
L2  A[i] ← x
INSERT(A, i, x)                            ▷ 0 ≤ i ≤ n < N
L3  for j ← n down to i + 1
L4      A[j] ← A[j − 1]
L5  A[i] ← x
L6  n ← n + 1
DELETE(A, i)                               ▷ 0 ≤ i < n
L7  x ← A[i]
L8  for j ← i to n − 2
L9      A[j] ← A[j + 1]
L10 n ← n − 1
L11 return x
```

GET and SET compute the address of cell $i$ and touch only that cell, so each costs $\Theta(1)$.

INSERT opens a hole at index $i$. The loop of lines L3 and L4 moves $A[n-1]$ to $A[n]$ first, then $A[n-2]$ to $A[n-1]$, and so on down to $A[i]$. It must go from the right to the left: a copy from the left would write $A[i]$ over $A[i+1]$ before $A[i+1]$ is read. Line L5 writes $x$ into the hole. The loop makes $n - i$ moves, so INSERT costs $\Theta(n - i + 1)$: $\Theta(1)$ at the end and $\Theta(n)$ at the front.

DELETE closes the hole at index $i$. The loop of lines L8 and L9 moves $A[i+1]$ to $A[i]$, then $A[i+2]$ to $A[i+1]$, from the left to the right. It makes $n - 1 - i$ moves, so DELETE costs $\Theta(n - i)$.

An unsorted array has no faster search than a scan from the left.

```pseudo id=search
SEARCH(A, x)                               ▷ the first index of x, or NIL
S1  for i ← 0 to n − 1
S2      if A[i] = x then return i
S3  return NIL
```

The scan makes at most $n$ comparisons, and exactly $n$ when $x$ is absent. If the items are sorted, [binary search](/binary-search/) finds $x$ with $O(\log n)$ comparisons instead.

## Example

Take capacity $N = 8$ and start with $n = 0$. The column "moves" counts the executions of line L4 or line L9.

| operation | cells $A[0 \ldots n-1]$ | $n$ | moves | result |
|---|---|---|---|---|
| insert(0, 5) | [5] | 1 | 0 | |
| insert(1, 8) | [5, 8] | 2 | 0 | |
| insert(1, 3) | [5, 3, 8] | 3 | 1 | |
| insert(0, 9) | [9, 5, 3, 8] | 4 | 3 | |
| get(2) | [9, 5, 3, 8] | 4 | 0 | 3 |
| set(3, 7) | [9, 5, 3, 7] | 4 | 0 | |
| delete(1) | [9, 3, 7] | 3 | 2 | 5 |
| search(7) | [9, 3, 7] | 3 | 0 | 2 |
| search(4) | [9, 3, 7] | 3 | 0 | NIL |

In insert(0, 9), the loop runs for $j = 3, 2, 1$: it copies 8 to $A[3]$, 3 to $A[2]$ and 5 to $A[1]$, and line L5 writes 9 to $A[0]$. In delete(1), the loop runs for $j = 1, 2$: it copies 3 to $A[1]$ and 7 to $A[2]$. The old value 7 stays in $A[3]$, but $n = 3$ says that it is no longer part of the list. The search for 7 makes 3 comparisons, and the search for 4 makes 3 comparisons and fails.

## Correctness

Each operation keeps the invariant and returns the value that the list type asks for. GET and SET read and write the cell that the invariant ties to position $i$. INSERT keeps this loop invariant at the test of line L3: $A[0 \ldots j-1]$ is unchanged and $A[j+1 \ldots n]$ holds the old $A[j \ldots n-1]$. At the end $j = i$, so line L5 writes $x$ into the only free cell between the two parts. DELETE has the mirror invariant for line L8. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

All costs are in the [random-access machine](/random-access-machine/), where one memory access at a computed address costs $O(1)$.

| operation | worst case | at index $i$ | notes |
|---|---|---|---|
| new(N) | $\Theta(1)$ or $\Theta(N)$ | | $\Theta(N)$ if the cells must be cleared |
| get, set | $\Theta(1)$ | $\Theta(1)$ | one address computation |
| insert | $\Theta(n)$ | $\Theta(n - i + 1)$ | $n - i$ moves |
| delete | $\Theta(n)$ | $\Theta(n - i)$ | $n - 1 - i$ moves |
| search, unsorted | $\Theta(n)$ | | at most $n$ comparisons |
| search, sorted | $\Theta(\log n)$ | | with binary search |
| space | $N s$ bytes | | no pointers, no per-item overhead |

If the index of an insert is uniform over $\{0, 1, \ldots, n\}$, the expected number of moves is $\frac{1}{n+1} \sum_{i=0}^{n} (n - i) = \frac{n}{2}$. If the index of a delete is uniform over $\{0, \ldots, n-1\}$, the expected number of moves is $\frac{1}{n} \sum_{i=0}^{n-1} (n - 1 - i) = \frac{n-1}{2}$. So a random insert or delete costs $\Theta(n)$ on average, not only in the worst case.

The constant factors are small. The cells are contiguous, so a scan reads whole cache lines and the hardware prefetcher predicts the next access. A [linked list](/linked-list/) has the same $\Theta(n)$ scan in theory but is often slower in practice, because each node can be anywhere in memory.

## Variants

- **Dynamic array.** A [dynamic array](/dynamic-array/) allocates a larger block when the array is full and copies the items. Appends then cost $O(1)$ amortized.
- **Circular buffer.** A [circular buffer](/circular-buffer/) keeps a start index and wraps around the end, so that insert and delete at both ends cost $O(1)$.
- **Gap buffer.** A [gap buffer](/gap-buffer/) keeps the free cells in the middle, at the place of the next edit.
- **Multidimensional arrays.** A matrix is stored in [row-major order](/row-major-order/) (C, and NumPy by default) or in column-major order (Fortran). The address of $M[r][k]$ is a linear function of $r$ and $k$.
- **Sparse arrays.** When most cells hold zero, a [sparse vector](/sparse-vector/) stores only the nonzero cells with their indices.
- **Bit arrays.** A [bit vector](/bit-set/) packs many one-bit cells into one machine word.

## When to use it

Use an array when the number of items has a known bound, and when the program reads items by index or scans them in order. Use a sorted array when the set is built once and then searched many times, since binary search on a sorted array is simple and fast. Do not use an array when the program inserts or deletes often in the middle of a long sequence. Then a [linked list](/linked-list/) (with a pointer to the place of the change), a balanced search tree or a [gap buffer](/gap-buffer/) is better. If the bound on the size is not known, use a [dynamic array](/dynamic-array/).

## Pitfalls

- **Off by one at the end.** The valid indices are $0$ to $n - 1$. A loop `for i ← 0 to n` reads the cell $A[n]$, which is outside the list and possibly outside the block. C does not check the bound, and an access outside the block is undefined behaviour.
- **Shift in the wrong direction.** If line L3 counts up, as in `for j ← i + 1 to n`, the first step writes $A[i]$ over $A[i+1]$, and every later cell gets a copy of $A[i]$. INSERT must copy from the right, and DELETE from the left. In C, `memmove` handles both directions, but `memcpy` on overlapping ranges is undefined.
- **Insert into a full array.** INSERT needs $n < N$. Without this test, line L4 with $j = N$ writes past the end of the block.
- **Confusing the count with the capacity.** After a delete, the old value stays in $A[n]$. Code that scans to $N$ instead of $n$ sees stale items.
- **Overflow of the address.** In a language with fixed-width integers, $i \cdot s$ can overflow for a large array. Compute indices in a type as wide as a pointer, such as `size_t` in C.

## Implementations

## History

Arrays came with the first stored-program computers, where a program reached the next item of a table by adding a constant to an address. FORTRAN, released by IBM in 1957, made arrays a part of a high-level language: the DIMENSION statement declared a subscripted variable with up to three subscripts. Knuth calls the layout of a list in consecutive cells *sequential allocation* and contrasts it with *linked allocation* (Sections 2.2.2 and 2.2.3).

## References
