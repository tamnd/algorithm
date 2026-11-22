---
tag: ZD4SXZ
kind: data-structure
slug: shadow-memory
name: Shadow memory
aliases:
- memory shadowing
area: security-and-privacy/memory-safety-defenses
level: core
summary: A scaled copy of the address space that holds metadata for each byte or word, found from the address by a shift and an add.
model: word-ram
complexity:
  vars: {n: the number of bytes of the application address space, k: "log2 of the granule size, so one metadata byte covers 2^k bytes", c: log2 of the size of a chunk in the two-level table}
  time: {worst: Θ(1)}
  space: {extra: Θ(n / 2^k)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [memory-safety]
see_also: [addresssanitizer, memory-tagging, baggy-bounds-checking, softbound, radix-tree, hash-table, bit-manipulation, word-ram]
sources:
  - paper: "Nicholas Nethercote and Julian Seward, How to shadow every byte of memory used by a program, VEE 2007, pages 65 to 74"
    locator: the two-level shadow table of Memcheck, the distinguished secondary maps and their copy on write
  - paper: "Konstantin Serebryany, Derek Bruening, Alexander Potapenko and Dmitry Vyukov, AddressSanitizer, a fast address sanity checker, USENIX Annual Technical Conference 2012, pages 309 to 318"
    locator: the section on the shadow memory (one shadow byte for 8 application bytes, at the address shifted right by 3 plus an offset)
  - paper: "Nicholas Nethercote and Julian Seward, Valgrind, a framework for heavyweight dynamic binary instrumentation, PLDI 2007"
    locator: the shadow values that the framework keeps for registers and memory
---

Shadow memory is a second, smaller copy of the address space that holds metadata about the first. Each granule of $2^k$ application bytes has one metadata byte, and the address of that byte comes from the application address by a shift right by $k$ and an add of a fixed offset. A checker reads the shadow byte before each load or store and learns, in a constant number of instructions, whether the bytes are allocated, initialized, tagged or poisoned. [AddressSanitizer](/addresssanitizer/), Valgrind's Memcheck, [baggy bounds checking](/baggy-bounds-checking/) and many race and taint detectors are built on it. When the address space is large and sparse, a two-level table with shared read-only chunks takes the place of one flat region.

## In plain words

Think of a large building with numbered rooms, and a small notebook at the front desk. Each line of the notebook is about a block of rooms, for example eight rooms in a row. To find the line about a room, you divide the room number by eight and look at that line. No search is needed.

The notebook line says what the checker needs to know about those rooms: whether anyone is allowed in, or how many of the rooms are open. A guard looks at the line before letting anyone through a door.

If the building is huge and most floors are empty, a full notebook wastes paper. Then there is one page per floor, and all empty floors share one pre-printed page. A floor gets its own page only when something on it changes.

## The abstract type

Shadow memory is a total map from granules of the application address space to metadata values, here bytes from 0 to 255. Granule $g$ is the range $[g \cdot 2^k, (g+1) \cdot 2^k)$, and the granule of address $a$ is $a \gg k$. The operations are GET$(a)$, the value of the granule of $a$; SET$(a, v)$, which sets that value; and SETRANGE$(lo, hi, v)$, which sets every granule in $[lo, hi)$ for granule-aligned $lo$ and $hi$. Before any SET, every granule has a default value. The contract is that of an array indexed by granule: GET returns the value of the last SET that covered the granule, or the default.

## Representation

**Direct map.** The application bytes are $[0, N)$ and the shadow bytes are $[\mathit{off}, \mathit{off} + N/2^k)$ in the same address space. The shadow byte of address $a$ is at $(a \gg k) + \mathit{off}$. The region must not overlap the application region, and application code must never write to it; real systems reserve it and make it unreachable for normal code. In the Python code the whole space is one bytearray and $\mathit{off} = N$.

**Two-level table.** For an address space of $2^b$ bytes, a primary table has $2^{b-c}$ entries, one for each chunk of $2^c$ application bytes. Each entry refers to a secondary chunk of $2^{c-k}$ metadata bytes. A distinguished chunk for a value $v$ is a read-only chunk in which every byte is $v$; many entries may share it. A private chunk belongs to one entry and may be written.

**Invariant (S).** For every granule $g$, the stored byte for $g$ is the value of the map at $g$: in the direct map it is the byte at $g + \mathit{off}$; in the two-level table it is byte $g \bmod 2^{c-k}$ of the chunk in entry $g \gg (c-k)$. In addition, each distinguished chunk of value $v$ holds only $v$.

## Operations

```pseudo id=main
SHADOW-ADDR(a)                                ▷ direct map
L1  return (a >> k) + off                     ▷ one shift and one add

GET(a)
L2  return M[SHADOW-ADDR(a)]

SET(a, v)
L3  M[SHADOW-ADDR(a)] ← v

SETRANGE(lo, hi, v)
L4  for a ← lo, lo + 2^k, ..., hi - 2^k do
L5      SET(a, v)

TWO-LEVEL GET(a) and SET(a, v)
L6  i ← a >> c                                ▷ the high bits pick the chunk
L7  j ← (a mod 2^c) >> k                      ▷ the low bits pick the byte
    GET returns P[i][j]; SET goes on:
L8  if P[i] is a distinguished chunk then     ▷ never write a shared chunk
L9      P[i] ← a private copy of P[i]         ▷ copy on write; skip if P[i][j] = v
L10 P[i][j] ← v

TWO-LEVEL SETRANGE(lo, hi, v)
L11 for each whole chunk i inside [lo, hi) do
L12     P[i] ← the distinguished chunk of v   ▷ drop the private copy
L13 for each granule left at the two ends do SET(a, v)
```

**Direct map.** Line L1 is the whole point of the structure: a shift and an add, with no branch and no memory access. GET and SET then touch one byte. SETRANGE runs lines L4 and L5 once per granule, which is how an allocator poisons or unpoisons a block.

**Two-level GET and SET.** Lines L6 and L7 split the address: the high $b - c$ bits index the primary table, and the next $c - k$ bits index the chunk. GET is two memory reads. SET first checks whether the chunk is shared. Line L9 copies it before the first write that changes a byte, so the other entries that share it still see the default. A write of the value already there needs no copy.

**Two-level SETRANGE.** Line L12 sets a whole chunk by pointing its entry at a distinguished chunk, in $O(1)$ time, and this also gives back the private copy. Line L13 handles the partial chunks at the two ends granule by granule.

## Example

**Direct map,** $N = 64$, $k = 3$, $\mathit{off} = 64$, default 0. The shadow is the 8 bytes $[64, 72)$.

| step | operation | result |
|---|---|---|
| 1 | SHADOW-ADDR(37) | $(37 \gg 3) + 64 = 4 + 64 = 68$ |
| 2 | SETRANGE(16, 40, 5) | granules 2, 3 and 4 are set; bytes $[64, 72)$ are 0 0 5 5 5 0 0 0 |
| 3 | GET(15), GET(16), GET(39), GET(40) | 0, 5, 5, 0 |
| 4 | the program writes 99 to address 20 | the shadow does not change; GET(20) is still 5 |

**Two-level table,** $b = 16$, $c = 8$, $k = 3$, default 1. The primary table has 256 entries, each chunk has 32 bytes, and at the start all 256 entries share the distinguished chunk of 1.

| step | operation | result |
|---|---|---|
| 1 | GET(0x1234) | $i = 0x12$, $j = 0x34 \gg 3 = 6$; the value is 1 |
| 2 | SET(0x1234, 1) | the value is already 1, so no copy; 0 private chunks |
| 3 | SET(0x1234, 7) | entry 0x12 gets a private copy and byte 6 becomes 7; 1 private chunk |
| 4 | GET(0x1230), GET(0x1238) | 7 (the same granule), 1 (the next granule) |
| 5 | SETRANGE(0x1200, 0x1300, 1) | a whole chunk: entry 0x12 points at the distinguished chunk again; 0 private chunks |

## Correctness

Each operation keeps invariant (S). In the direct map, $g \mapsto g + \mathit{off}$ is one to one, so SET of one granule changes the stored byte of that granule only, and the application region does not overlap the shadow, so no application write changes a stored byte. In the two-level table, line L9 makes the chunk private before line L10 writes it, so no distinguished chunk is ever written, and the other entries that shared it keep their values. Line L12 sets every granule of a whole chunk to $v$ at once. Then GET reads the stored byte of the granule, which by (S) is the value of the map. The proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/) model.

| operation | direct map | two-level table |
|---|---|---|
| GET | $\Theta(1)$: a shift, an add and a read | $\Theta(1)$: two reads |
| SET | $\Theta(1)$ | $\Theta(1)$, or $\Theta(2^{c-k})$ for the first change of a shared chunk |
| SETRANGE over $m$ granules | $\Theta(m)$ | $O(m / 2^{c-k} + 2^{c-k})$ |

Space: the direct map reserves $N / 2^k$ bytes, one eighth of the address space for $k = 3$, whether the memory is used or not. Real systems reserve this range of virtual addresses and let the operating system give physical pages only to the parts that are touched. The two-level table uses $2^{b-c}$ entries plus $2^{c-k}$ bytes for each changed chunk. The run-time cost of a checker built on shadow memory is a measurement of that checker on its benchmarks, and it is not a property of the structure.

## Variants

- **Granule size.** With $k = 0$ the shadow has one byte per byte, which can say exactly which bytes are addressable. With $k = 3$, AddressSanitizer stores in one byte how many of the first bytes of an 8-byte granule are addressable, which works because its allocator aligns blocks to 8 bytes. A larger granule saves space and loses precision at the ends of objects.
- **Several bits per byte.** Memcheck keeps an addressable bit for each byte and a defined bit for each bit of memory, and it compresses the common cases into 2 bits per byte in its shadow.
- **A table per slot.** [Baggy bounds checking](/baggy-bounds-checking/) keeps one byte per 16-byte slot, holding the log of the size of the allocation that covers the slot.
- **Tags in hardware.** [Memory tagging](/memory-tagging/) keeps a small tag for each 16-byte granule in storage that the hardware manages, and compares it with a tag in the pointer on each access.
- **Multi-level tables.** The two-level table is a two-level [radix tree](/radix-tree/) on the address bits. A 64-bit space needs more levels, or a [hash table](/hash-table/) of chunks.
- **Shadow for registers.** Dynamic binary instrumentation frameworks also shadow each register, so that metadata follows a value through computation.

## When to use it

Use shadow memory when a checker needs a few bits of state for every byte or word of memory and must find them on every access, with no search. It fits dynamic checkers and sanitizers that run in testing, where the program can reserve a large range of addresses. Use the direct map when you control the layout of the address space and can reserve the shadow region, and the two-level table when you cannot, or when most of the space is never used. If the metadata is per object rather than per byte, an object table such as the one of [Jones-Kelly](/jones-kelly-bounds-checking/) can be smaller, and if it is per pointer, a table keyed by the address of the pointer, as in [SoftBound](/softbound/), is more precise.

## Pitfalls

- **An offset that lets the shadow overlap the application.** If $\mathit{off}$ is too small, line L1 maps some application addresses into the shadow region itself, and a program write can change metadata. Choose $\mathit{off}$ so that $[\mathit{off}, \mathit{off} + N/2^k)$ and $[0, N)$ are disjoint.
- **Writing a shared chunk.** If line L8 is left out, line L10 writes the distinguished chunk, and every entry that shares it changes at once. The test in line L8 and the copy in line L9 must come before every write.
- **An unaligned range.** SETRANGE with $lo$ or $hi$ inside a granule sets the whole granule, so a few bytes outside the range get the new value. Line L4 assumes aligned ends; for an unaligned end, use a value that encodes the partial granule, as AddressSanitizer does.
- **A multi-byte access across granules.** One GET for the first byte of an access of $w$ bytes says nothing about a second granule. Check both granules, or align accesses so they stay inside one.
- **Mixing up the shift.** With $c$ and $k$ swapped in line L7, or with $a \gg c$ used as the index inside a chunk, the code reads the wrong byte and still passes on default values. Test with values that differ from the default.

## Implementations

The Python code keeps both representations on a simulated address space, a bytearray for the direct map and a list of byte chunks for the two-level table, and never reads real memory. The tests compare both with a dictionary model on random sequences of SET and SETRANGE, and they also check that the number of private chunks stays at most the number of chunks that were changed.

## History

Shadow values go back to the early dynamic checkers for memory errors, such as Purify in the early 1990s, which kept state bits for each byte of memory. Nethercote and Seward described the two-level table of Valgrind's Memcheck, with its distinguished secondary maps, in 2007. Serebryany and others made the direct map with one byte per 8 bytes and a fixed offset the core of AddressSanitizer in 2012, which made a shadow check cheap enough to run in large test suites. The same layout now holds the metadata of many sanitizers for races, uninitialized reads and type errors.

## References
