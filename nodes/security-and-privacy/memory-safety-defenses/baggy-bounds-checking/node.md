---
tag: 81GP9H
kind: algorithm
slug: baggy-bounds-checking
name: Baggy bounds checking
aliases:
- baggy bounds
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Pads each allocation to a power of two and stores its log size in a compact table, so that bounds checks need one lookup.
model: word-ram
complexity:
  vars: {n: the requested size of an allocation in bytes, m: the number of bytes of the address space}
  time: {worst: Θ(1)}
  space: {extra: Θ(m / 16)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2009
  people: [Periklis Akritidis, Manuel Costa, Miguel Castro, Steven Hand]
  note: "Presented at the USENIX Security Symposium 2009 as a referent-object bounds checker whose lookup is one table read instead of a tree search."
prereqs: [jones-kelly-bounds-checking, shadow-memory]
see_also: [jones-kelly-bounds-checking, buddy-system, shadow-memory, addresssanitizer, softbound, internal-fragmentation, bit-manipulation, buffer-overflow]
sources:
  - paper: "Periklis Akritidis, Manuel Costa, Miguel Castro and Steven Hand, Baggy bounds checking, an efficient and backwards-compatible defense against out-of-bounds errors, USENIX Security Symposium 2009"
    locator: "the sections on the bounds table with one byte per 16-byte slot, the xor check, out-of-bounds pointers within half a slot and the mark bit, the binary buddy allocator, the 64-bit variant and the evaluation"
  - paper: "Richard W. M. Jones and Paul H. J. Kelly, Backwards-compatible bounds checking for arrays and pointers in C programs, AADEBUG 1997, pages 13 to 25"
    locator: the referent-object approach and the object table that baggy bounds replaces
  - paper: "Olatunji Ruwase and Monica S. Lam, A practical dynamic buffer overflow detector, NDSS 2004, pages 159 to 169"
    locator: the out-of-bounds objects that the mark bit of baggy bounds replaces for pointers close to their object
---

Baggy bounds checking is a bounds checker for C that finds the object of a pointer in constant time. It pads every allocation to a power of two and aligns it to that size, with a binary buddy allocator. Then the size of an allocation is one small number, its base-two logarithm $e$, and the base of the allocation that holds an address $p$ is $p$ with its low $e$ bits cleared. A table with one byte for each 16-byte slot of memory holds $e$. Pointer arithmetic checks that the result is in the same padded allocation as the operand with one xor and one shift. Like [Jones-Kelly](/jones-kelly-bounds-checking/), it keeps pointers as plain addresses, so checked and unchecked code work together. The price is that the checks use the padded size: an access to the padding is not reported.

## In plain words

Every allocation is rounded up to a size of 16, 32, 64, 128 bytes and so on, and placed at an address that is a multiple of that size. Because of this, two facts describe an allocation fully: its size, and any address inside it.

The checker keeps a small table with one entry for each 16 bytes of memory. The entry says how big the allocation there is, as a power of two. One table read gives the size, and clearing the low bits of the address gives the start.

When the program moves a pointer, the checker looks at the entry for the old address and asks whether the new address is in the same rounded-up block. If it is just outside, the pointer gets a mark and may come back later. If it is far outside, the program stops.

## The problem

The problem is the one of [Jones-Kelly bounds checking](/jones-kelly-bounds-checking/): stop each pointer computation that leaves the object its operand points into, without changing the size of pointers. The object table of Jones-Kelly finds the object with a search in a [splay tree](/splay-tree/), on every pointer operation, and this search is most of the cost. The goal is a lookup in a constant number of instructions and a table small enough to stay in the cache, at the cost of less exact bounds.

## The algorithm

Memory is cut into slots of 16 bytes. The bounds table $T$ has one byte per slot. For an allocation of padded size $2^e$ at base $B$, with $B$ a multiple of $2^e$, every slot of $[B, B + 2^e)$ has $T = e$. The slots of memory that the checker did not allocate hold a default value that covers the whole address space, so checks on them always pass; the original uses 31 on 32-bit Windows. A pointer that is at most half a slot outside its allocation is marked by setting a bit above all valid addresses. In the original that is the top bit of a 32-bit address, which points into the kernel half of the address space, so a dereference of a marked pointer faults in hardware.

```pseudo id=main
ALLOC(n)
L1  e ← max(4, ⌈log2 n⌉)                      ▷ padded size 2^e, at least one slot
L2  B ← a free block of 2^e bytes, aligned to 2^e    ▷ binary buddy allocator
L3  for each slot s of [B, B + 2^e) do T[s] ← e
L4  clear the 2^e bytes, padding included
L5  return B

ADD(p, k)
L6  if p is marked then r ← p without the mark; ref ← r - 8 if r is in the low half of its slot, else r + 8
L7  else r ← p; ref ← p
L8  e ← T[ref >> 4]
L9  q ← r + k
L10 if (ref xor q) >> e = 0 then return q          ▷ in the padded allocation
L11 base ← ref with the low e bits cleared
L12 if base - 8 ≤ q < base + 2^e + 8 then return q with the mark
L13 report a bounds error

CHECK(p, w)                                       ▷ for an access of w bytes
L14 if p is marked then fault
L15 if (p xor (p + w - 1)) >> T[p >> 4] ≠ 0 then report a bounds error

FREE(p)
L16 if p is not the base of an allocation then report an error
L17 for each slot of the block do T[s] ← the default; give the block back
```

**The table.** Lines L1 to L3 make the bounds a function of the address. One byte per 16 bytes is $1/16$ of memory, a regular array indexed by the address shifted right by 4, which is a form of [shadow memory](/shadow-memory/).

**The xor check.** Line L10 tests whether $q$ and $ref$ agree in every bit from bit $e$ up. Because the block is aligned to $2^e$, those bits are exactly the base of the block, so the test is true exactly when $q$ is inside $[B, B + 2^e)$. There is no subtraction, no comparison of two bounds and no branch on the size.

**Out-of-bounds pointers.** C programs often form a pointer just past an array, or just before it, and then come back. Line L12 keeps such a pointer if it is less than half a slot outside the block, and marks it. A marked pointer cannot be used to access memory, but line L6 can still find its allocation. The allocation is at least one slot and ends on a slot boundary, so a pointer past the end lands in the low half of the next slot and a pointer before the base lands in the high half of the previous slot. Moving the address by half a slot back toward the block, as line L6 does, puts it inside the allocation again. A pointer further out is an error at once, in line L13.

**Wide accesses.** The arithmetic check alone shows that the first byte of an access is in the block. For an access of $w > 1$ bytes, line L15 also checks the last byte $p + w - 1$. The paper notes that this second check is not needed for accesses that are aligned to their own size, because an aligned access cannot cross a power-of-two boundary of a larger block.

## Example

A memory of 256 bytes, so 16 slots; slot 0 is reserved, so 0 is never a valid pointer. The default table value is 8.

| step | operation | result |
|---|---|---|
| 1 | $a$ ← ALLOC(20) | $e = 5$; $a = 32$, the block is $[32, 64)$; $T[2] = T[3] = 5$ |
| 2 | $b$ ← ALLOC(10) | $e = 4$; $b = 16$, the block is $[16, 32)$ |
| 3 | STORE(ADD($a$, 25), 1, 9) | allowed: byte 57 is padding, inside $[32, 64)$ |
| 4 | $p$ ← ADD($a$, 32) | $q = 64$; $(32 \oplus 64) \gg 5 = 3$; $24 \le 64 < 72$, so $p$ is 64 with the mark |
| 5 | LOAD($p$, 1) | fault at line L14 |
| 6 | ADD($p$, $-1$) | $r = 64$ is in the low half, so $ref = 56$ and $e = 5$; $q = 63$ and $(56 \oplus 63) \gg 5 = 0$: back in bounds |
| 7 | ADD($a$, 40) | $q = 72$ is not below $72$: bounds error at line L13 |
| 8 | STORE(ADD($a$, 30), 4, 1) | the bytes are 62 to 65; $(62 \oplus 65) \gg 5 = 3$: bounds error at line L15 |
| 9 | FREE($a$); LOAD($a$, 1) | $T[2], T[3]$ go back to 8; the load passes |

Step 3 shows the lost precision: byte 57 is not part of the 20 bytes the program asked for. Step 6 shows a pointer that leaves and comes back, which [Jones-Kelly](/jones-kelly-bounds-checking/) refuses. Step 9 shows that the scheme has no temporal check.

## Correctness

For a live allocation with base $B$ and padded size $P = 2^e$, call a pointer derived from it *at offset* $o$ if its address is $B + o$. The claim, proved in [the correctness proof](proofs/correctness.md), is an invariant on every such pointer: it is plain if $0 \le o < P$, it is marked if $-8 \le o < 0$ or $P \le o < P + 8$, and any ADD that would give another offset reports an error. The proof uses two facts. First, the table holds $e$ in every slot of the block, so line L8 reads the right size. Second, the block is aligned, so the xor test of line L10 is exactly the test $B \le q < B + P$, and line L6 maps a marked pointer back into its own block. From the invariant, CHECK passes exactly when $0 \le o$ and $o + w \le P$. So every access outside the padded block is caught, and no access inside it is refused.

## Complexity

Every check is $\Theta(1)$ in the [word RAM](/word-ram/) model: one table read, one xor, one shift and one compare, plus a second compare for marked pointers. ALLOC and FREE add $O(2^e / 16)$ table writes to the cost of the [buddy allocator](/buddy-system/), which is $O(\log m)$ for an address space of $m$ bytes. The table takes $m / 16$ bytes. The padding wastes up to half of each allocation, as [internal fragmentation](/internal-fragmentation/); on average it is much less, because many requests are already close to a power of two.

The measured cost is a property of the implementation and its workload. The paper reports, for its 32-bit Windows implementation in 2009, an 8% decrease of throughput for the Apache web server, and it compares run time on the SPECINT 2000 and Olden benchmarks with earlier checkers.

## Properties

- **Backwards compatible.** Pointers keep their size, and memory that the checker did not allocate passes every check.
- **Not exact.** The bounds are those of the padded block, so an overflow into the padding is allowed. It never reaches another object, because allocations do not overlap.
- **Spatial only.** It does not find use after free.
- **Constant-time lookup.** The size comes from an array, with no search.

## Variants and improvements

- **64-bit pointers.** On a 64-bit machine the paper stores $e$ in spare high bits of the pointer itself, which removes the table lookup at the cost of masking the pointer before each use.
- **Last-byte check only when needed.** Line L15 can be dropped for aligned accesses of built-in types, which leaves one check per pointer computation.
- **Other slot sizes.** A larger slot makes the table smaller and the minimum allocation larger. The half-slot rule then allows pointers further out of bounds.
- **Tighter bounds.** Later schemes store the exact size elsewhere, or use [shadow memory](/shadow-memory/) with one entry per small granule, as [AddressSanitizer](/addresssanitizer/) does, to catch the overflows into the padding.

## When to use it

Use baggy bounds when you need a spatial checker that is cheap enough for production, that works with libraries compiled without checks, and that stops an overflow from reaching a neighbouring object. It is a hardening technique, not a precise debugging tool: an overflow into the padding goes unseen, and a later access past the padding is reported far from the bug. For finding bugs in testing, a precise checker such as [AddressSanitizer](/addresssanitizer/) reports more of them. For exact per-pointer bounds and sub-object bounds, use [SoftBound](/softbound/).

## Pitfalls

- **Blocks that are not aligned.** If line L2 returns a block that is not aligned to $2^e$, the xor test of line L10 compares the wrong bits and accepts addresses in the neighbour. The allocator must align every block to its own padded size.
- **A stale table.** If line L17 does not reset the slots of a freed block, a later small allocation in that memory gets the old, larger $e$ for its other slots, and line L10 accepts a range that covers other objects. Reset on free and set again on each allocation.
- **The wrong half.** If line L6 moves a marked pointer away from its block, line L8 reads the size of the neighbour, and the pointer is judged against the wrong block. The low half of a slot belongs to the block below.
- **First byte only.** Without line L15, an unaligned 8-byte access at the last byte of a block writes 7 bytes into the next block.
- **Uncleared padding.** If line L4 clears only the $n$ requested bytes, a program that reads the padding sees data of an earlier allocation.

## Implementations

The Python code runs on a simulated memory of a few hundred bytes with its own buddy allocator and never reads real memory. The mark bit is one bit above the largest address of the simulated memory. The tests run random programs against an oracle that tracks every object, its padded size and the intended offset of every pointer, and they check that the value of each pointer, marked or plain, and the result of each access are exactly what the invariant predicts.

## History

Akritidis, Costa, Castro and Hand presented baggy bounds checking in 2009, after Jones-Kelly (1997), CRED (2004) and the pool-based tables of Dhurjati and Adve (2006). They kept the referent-object approach and the backwards compatibility of that line of work, and replaced the tree with an array lookup made possible by padding and alignment. The same idea, in which an allocator layout makes the metadata a function of the address, appears in later hardening allocators and in hardware with bounds in pointer bits.

## References
