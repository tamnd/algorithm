---
tag: B574DH
kind: algorithm
slug: addresssanitizer
name: AddressSanitizer
aliases:
- ASan
- redzone checking
area: security-and-privacy/memory-safety-defenses
level: core
summary: Puts poisoned redzones around objects and a quarantine for freed memory, and checks each access against shadow memory to find overflows and use after free.
model: word-ram
complexity:
  vars: {n: the size of an object in bytes, m: the size of the application memory in bytes}
  time: {worst: Θ(1)}
  space: {extra: Θ(m / 8)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2012
  people: [Konstantin Serebryany, Derek Bruening, Alexander Potapenko, Dmitry Vyukov]
  note: "Presented at USENIX ATC 2012 as a compiler pass and a run-time library, with one shadow byte for each 8 bytes of memory."
prereqs: [shadow-memory]
see_also: [shadow-memory, memory-tagging, baggy-bounds-checking, jones-kelly-bounds-checking, lock-and-key-temporal-checking, dangling-pointer-nullification, coverage-guided-fuzzing, fuzz-testing]
sources:
  - paper: "Konstantin Serebryany, Derek Bruening, Alexander Potapenko and Dmitry Vyukov, AddressSanitizer: a fast address sanity checker, USENIX ATC 2012, pages 309-318"
    url: https://www.usenix.org/conference/atc12/technical-sessions/presentation/serebryany
    locator: "Section 3 (the shadow mapping, the instrumentation of 1, 2, 4 and 8 byte accesses, the redzones and the quarantine) and Section 4 (the evaluation)"
  - paper: "Nicholas Nethercote and Julian Seward, How to shadow every byte of memory used by a program, VEE 2007, pages 65-74"
    locator: the layout of shadow memory and the cost of its lookups
---

AddressSanitizer finds out-of-bounds accesses and uses after free in C and C++ programs. Its allocator puts a *redzone* of memory that the program must not touch on each side of every heap object, and it does not reuse freed memory at once but keeps it in a *quarantine*. One byte of [shadow memory](/shadow-memory/) describes each aligned granule of 8 bytes: whether all of it, only a prefix of it, or none of it may be accessed. The compiler adds a few instructions before each load and store that read the shadow byte and report an error if the access touches a byte that is not addressable. An overflow that steps into a redzone and a use of memory that is still in the quarantine are reported at the faulting access. The tool is meant for testing, not for production, since it slows the program down and uses much more memory.

## In plain words

Picture a car park where every car gets a row of painted no-parking spaces at each end. A guard has a small notebook with one line for each group of eight spaces, saying how many of them are in use.

Before anyone parks, the guard looks up the line for that group. If the space is a no-parking space, or a space nobody has rented, the guard stops the driver at once.

When a car leaves, its spaces are not rented again straight away. They stay marked as "recently left" for a while, so a driver who comes back to the old space is caught. Only when enough newer spaces have been freed does the oldest group go back up for rent.

## The problem

The input is a program with heap objects, and the goal is to report the first load or store that touches a byte outside every live object: past the end of an object or before its start, or in an object that was freed. The check must be cheap enough to run on large programs and in fuzzing, so it must take constant time and must not change the layout of pointers. Exact per-pointer bounds, as in [SoftBound](/softbound/), or a lookup of the object, as in [Jones and Kelly bounds checking](/jones-kelly-bounds-checking/), cost more. AddressSanitizer instead asks a simpler question about the address only: is this byte inside some live object?

## The algorithm

The heap is split into granules of 8 bytes, and objects start on granule boundaries. The shadow byte of a granule is 0 if all 8 bytes are addressable, $k$ in 1 to 7 if only the first $k$ are, and a negative value if none are. Different negative values mark a redzone and a freed object, so that a report can say which it was. OFFSET is the start of the shadow region; real systems fix it for each platform. An access of $w$ bytes, with $w$ in $\{1, 2, 4, 8\}$, is aligned to $w$, so it lies in one granule. RZ is the redzone size, a multiple of 8.

```pseudo id=main
SHADOW(a)
L1  return M[(a >> 3) + OFFSET]

CHECK(a, w)                          ▷ before each load or store of w bytes at a
L2  k ← SHADOW(a), as a signed byte
L3  if k ≠ 0 and (a & 7) + w - 1 ≥ k then report an error at a

MALLOC(n)
L4  c ← a free chunk of RZ + ⌈n/8⌉·8 + RZ bytes; b ← c + RZ
L5  poison the shadow of [c, b) and of [b + ⌈n/8⌉·8, c + the chunk length) as a redzone
L6  set the shadow of the ⌊n/8⌋ full granules at b to 0, and of the next granule to n mod 8 if it is not 0
L7  return b

FREE(p)
L8  if p is not the start of a live object then report a double or bad free
L9  poison the shadow of the ⌈n/8⌉ granules at p as freed
L10 append the chunk to the end of the FIFO quarantine Q
L11 while the total size of Q exceeds its limit do
L12     remove the oldest chunk from Q and give it back to the allocator
```

**The check.** Line L3 is one comparison in the common case: most shadow bytes are 0, and then the access is allowed. If $k$ is between 1 and 7, the access is allowed when its last byte, at position $(a \mathbin{\&} 7) + w - 1$ inside the granule, is below $k$. If $k$ is negative, the comparison is true for every access, since the left side is never negative. For $w = 8$ the access covers the whole granule, so any nonzero $k$ is an error, and the formula gives this too.

**Malloc.** Lines L4 to L6 make exactly the $n$ bytes of the object addressable and poison everything else in the chunk. The bytes between $b + n$ and the end of the last granule are covered by the partial value $n \bmod 8$, so an overflow by one byte is caught even when $n$ is not a multiple of 8.

**Free and the quarantine.** Line L9 marks the object as freed, so that any later access reports a use after free. Lines L10 to L12 delay the reuse of the chunk: it goes back to the allocator only after enough other memory has been freed after it. While the chunk is in the quarantine, every stale pointer into it is caught.

## Example

A memory of 256 bytes, redzones of 16 bytes and a quarantine limit of 64 bytes. The shadow values $\mathtt{FA}$ (a redzone) and $\mathtt{FD}$ (freed) are negative as signed bytes.

| step | operation | result |
|---|---|---|
| 1 | $p$ ← MALLOC(13) | chunk $[0, 48)$, $p = 16$; the shadow of the six granules is FA, FA, 0, 5, FA, FA |
| 2 | $q$ ← MALLOC(8) | chunk $[48, 88)$, $q = 64$ |
| 3 | LOAD($p + 12$, 1) | granule 3 has $k = 5$; $4 + 0 < 5$: allowed |
| 4 | LOAD($p + 13$, 1) | $5 + 0 \ge 5$: heap buffer overflow |
| 5 | LOAD($p + 12$, 4) | $4 + 3 \ge 5$: heap buffer overflow, one byte in bounds is not enough |
| 6 | LOAD($p - 8$, 8) | $k$ is FA: overflow into the left redzone |
| 7 | FREE($p$) | the object granules become FD; the quarantine holds 48 bytes |
| 8 | LOAD($p$, 1) | $k$ is FD: heap use after free |
| 9 | FREE($p$) | $p$ is not live but is in the quarantine: double free |
| 10 | FREE($q$) | the quarantine would hold 88 bytes, so the chunk of $p$ leaves it |
| 11 | $r$ ← MALLOC(13) | first fit gives the chunk at 0 again: $r = 16 = p$ |
| 12 | LOAD($p$, 1) | allowed: the stale pointer now reads the new object |

Step 12 shows the limit of the design: once a chunk leaves the quarantine and is reused, a dangling pointer to it is no longer reported.

## Correctness

The check decides a property of the address, not of the pointer. Invariant S: for every granule, the shadow byte is 0 if all 8 bytes lie in live objects, $k$ in 1 to 7 if exactly the first $k$ do, and negative if none do. Objects start on granule boundaries and redzones are at least one granule, so these are the only cases. MALLOC sets the shadow of its chunk to match, and FREE poisons the object it frees; no other operation changes which bytes are live. Under S, line L3 reports an aligned access of $w \le 8$ bytes exactly when one of its bytes is outside every live object. So every overflow that ends in a redzone or in free memory is reported, and every use of an object whose chunk is still in the quarantine is reported, with no false reports. An access that leaves its object and lands inside another live object is not reported. The proof is in [the correctness proof](proofs/correctness.md).

## Complexity

In the [word RAM](/word-ram/) model the check takes $\Theta(1)$ time: one shift, one add, one load and at most two comparisons. MALLOC and FREE write $\Theta(n / 8)$ shadow bytes for an object of $n$ bytes, plus the cost of the allocator. The shadow takes $\Theta(m / 8)$ bytes for $m$ bytes of memory; redzones add $2 \cdot \mathrm{RZ}$ bytes per object, and the quarantine keeps up to its limit of freed memory out of use.

The paper reports, in 2012, an average slowdown of 73% on SPEC CPU2006 on 64-bit x86 Linux, and more than 300 bugs found in the Chromium browser.

## Properties

- **No false reports** for aligned accesses of 1, 2, 4 or 8 bytes: a report always means a byte outside every live object.
- **Not complete.** An overflow that jumps over the redzone into another object, and a use after free after the chunk is reused, are missed.
- **Address based.** The check needs no metadata in pointers, so code compiled without it can share pointers with code compiled with it.
- **Deterministic.** For the same program and input, the same accesses are reported.

## Variants and improvements

- **Stack and globals.** The compiler also puts redzones between local arrays and between global objects and poisons them in the shadow, so overflows of the stack and of globals are caught the same way.
- **Unaligned and larger accesses.** An access that crosses a granule, or is longer than 8 bytes, checks the shadow of its first and last bytes, or of every granule it covers.
- **Use after return and use after scope.** Locals can be moved to a heap-like area or poisoned when their scope ends, so that a pointer to a dead local is caught.
- **Tagging instead of redzones.** [Memory tagging](/memory-tagging/) stores a small tag in each pointer and in each granule and checks that they match, which also catches overflows that jump far and uses after reuse, with a probability set by the tag width.
- **Exact bounds.** [Baggy bounds checking](/baggy-bounds-checking/) and [SoftBound](/softbound/) check the bounds of the object that the pointer came from, so a jump into another object is caught.

## When to use it

Use AddressSanitizer in testing and in [fuzz testing](/fuzz-testing/) of C and C++ code: it finds most heap, stack and global overflows and many uses after free at the faulting access, with a small change to the build and a moderate cost. In [coverage-guided fuzzing](/coverage-guided-fuzzing/) it turns silent memory errors into crashes that the fuzzer can see. Do not use it as a production defense: the redzones and the quarantine use much memory, and the misses above mean it gives no guarantee. When every access must be checked against the bounds of the right object, use a bounds checker; when every use after free must be caught, use [lock and key checking](/lock-and-key-temporal-checking/).

## Pitfalls

- **A small redzone.** An overflow by more than the redzone can land inside the next object and is not reported. Larger redzones catch more and cost more memory.
- **A small quarantine.** Once a freed chunk is reused, a stale pointer to it reads the new object without a report. A larger quarantine delays reuse longer.
- **Forgetting the partial granule.** If MALLOC sets the last granule to 0 when $n$ is not a multiple of 8, overflows of up to 7 bytes are missed.
- **Treating the shadow byte as unsigned.** The test in line L3 relies on poisoned values being negative. As unsigned bytes they are large, and an access to a poisoned granule passes.
- **Unaligned accesses.** An unaligned access can cross into the next granule, and checking only the shadow of its first byte misses the second granule.
- **Code without instrumentation.** Accesses made by libraries compiled without the check are not checked, though their allocations still get redzones if they use the same allocator.

## Implementations

The Python code runs on a simulated memory, a bytearray that holds the application bytes and the shadow bytes after them, and never reads real memory. The shadow offset is the size of the simulated memory, not the value used on any real system. The allocator is first fit with redzones of 16 bytes and a FIFO quarantine with a limit in bytes. The tests compare every report of random programs with an oracle that tracks each object and checks every byte of each access against the live objects, and they count the overflows and the uses after free that land in other live objects and are not reported.

## History

Checking each access against a map of the state of memory goes back to tools such as Purify in the early 1990s and Valgrind's Memcheck in the 2000s, which used binary instrumentation and were slow. Serebryany, Bruening, Potapenko and Vyukov designed AddressSanitizer at Google and presented it at USENIX ATC 2012. It moved the checks into the compiler and used a compact shadow of one byte per 8 bytes, which made it fast enough to run on large programs and in continuous fuzzing. It became part of LLVM and GCC, and its design led to the later work on hardware-assisted and memory-tagging sanitizers.

## References
