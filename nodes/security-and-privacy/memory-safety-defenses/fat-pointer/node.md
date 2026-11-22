---
tag: QJJ3SE
kind: data-structure
slug: fat-pointer
name: Fat pointer
aliases:
- bounded pointer
- safe pointer
area: security-and-privacy/memory-safety-defenses
level: core
summary: A pointer that carries the base and bound of its object, so that each dereference can be checked against them.
model: word-ram
complexity:
  vars: {h: the number of holes in the free list of the allocator}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [memory-safety]
see_also: [softbound, lock-and-key-temporal-checking, jones-kelly-bounds-checking, baggy-bounds-checking, cheri-capability-model, buffer-overflow, first-fit-allocation, type-soundness]
sources:
  - paper: "Todd M. Austin, Scott E. Breach and Gurindar S. Sohi, Efficient detection of all pointer and array access errors, PLDI 1994, pages 290 to 301"
    locator: "Section 3 (the safe pointer with value, base, size, storage class and capability, the spatial and the temporal check, and the capability store)"
  - paper: "George C. Necula, Scott McPeak and Westley Weimer, CCured, type-safe retrofitting of legacy code, POPL 2002"
    locator: the SAFE, SEQ and WILD pointer kinds, and the inference that gives most pointers the cheap SAFE kind
  - paper: "Trevor Jim, Greg Morrisett, Dan Grossman, Michael Hicks, James Cheney and Yanling Wang, Cyclone, a safe dialect of C, USENIX Annual Technical Conference 2002"
    locator: the fat pointer type with bounds, and the never-null and thin pointer types beside it
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, IEEE Symposium on Security and Privacy 2013, pages 48 to 62"
    locator: Section on spatial safety (pointer-based bounds checking, fat pointers and the compatibility cost of a changed pointer layout)
---

A fat pointer is a pointer that carries the bounds of its object with it: the address, the base and the end of the block it was made from, and often a number that says which allocation it belongs to. Each load and store through the pointer first checks the address against the bounds, so an out-of-bounds access is caught at the access, and with the allocation number a use after free is caught too. This gives [spatial memory safety](/memory-safety/) at the cost of a larger pointer, which breaks the memory layout that unchecked C code expects. Austin, Breach and Sohi (1994) called it a safe pointer; CCured, Cyclone, the slices of Rust and Go, and [CHERI](/cheri-capability-model/) capabilities are all fat pointers of some kind.

## In plain words

A plain pointer is a street address. It says where to go and nothing else, so nothing stops a program from walking past the end of its own plot into the next one.

A fat pointer is the address plus the two ends of the plot it belongs to, written on the same card. Before each read or write, the program looks at the card and checks that the address is still inside the plot. If it is not, the program stops before it touches the neighbour.

The card can also carry a ticket number for the plot. When the plot is given back, its ticket is cancelled. A later visit with an old card shows a cancelled ticket and is refused, even if a new owner has moved onto the same land.

## The abstract type

A fat pointer implements a pointer with checked access. The operations are ALLOC$(n)$, which returns a pointer to a new block of $n$ bytes; ADD$(p, k)$, pointer arithmetic; LOAD$(p, w)$ and STORE$(p, w, v)$, which read or write $w$ bytes at $p$; and FREE$(p)$. The contract is the one of [memory safety](/memory-safety/): a LOAD or STORE succeeds exactly when the $w$ bytes lie inside a live block that $p$ was derived from, and otherwise it reports a spatial error (outside the block) or a temporal error (the block was freed). ADD is not checked: forming an out-of-bounds address is allowed, using it is not.

## Representation

A fat pointer is a record $p = (\mathit{value}, \mathit{base}, \mathit{bound}, \mathit{cap})$. The field $\mathit{value}$ is the address. The block is the half-open range $[\mathit{base}, \mathit{bound})$. The field $\mathit{cap}$ is a capability number, unique to one allocation and never reused. The heap keeps a capability store $\mathit{LIVE}$, a map from the number of each live allocation to its range. The null pointer is $(0, 0, 0, 0)$, and the number 0 is never issued.

**Invariant (F).** For each fat pointer $p$ that the program holds, $[p.\mathit{base}, p.\mathit{bound})$ is the block of the allocation with number $p.\mathit{cap}$, or $p$ is null. If $p.\mathit{cap} \in \mathit{LIVE}$, that block is still allocated, and the live blocks are pairwise disjoint.

The program can copy a fat pointer and change its value by ADD. It cannot write the other three fields. This is the point of the design: the bounds come from the allocator, not from the program.

## Operations

```pseudo id=main
ALLOC(n)
L1  base ← the first hole of at least n bytes      ▷ first fit; split the hole
L2  cap ← a new capability number                  ▷ never reused
L3  LIVE[cap] ← [base, base + n)
L4  return (base, base, base + n, cap)

ADD(p, k)
L5  return (p.value + k, p.base, p.bound, p.cap)  ▷ no check here

CHECK(p, w)
L6  if p.value < p.base or p.value + w > p.bound then
L7      report a spatial error
L8  if p.cap is not in LIVE then
L9      report a temporal error

LOAD(p, w) and STORE(p, w, v)
L10 CHECK(p, w)
L11 read or write the w bytes at p.value

FREE(p)
L12 if p.value ≠ p.base then report a spatial error   ▷ not the start of a block
L13 if p.cap is not in LIVE then report a temporal error   ▷ double free
L14 delete LIVE[p.cap]
L15 return the block [p.base, p.bound) to the allocator
```

**ALLOC.** Lines L1 to L4 take a block from the [allocator](/allocator/), here [first fit](/first-fit-allocation/), and give the pointer the bounds of exactly that block. A fresh capability number goes into the store. The cost is the search of the allocator, $O(h)$ for $h$ holes; the fat pointer itself adds $O(1)$.

**ADD.** Line L5 moves the address and copies the three other fields. The pointer may leave its block and come back; the bounds do not change, so the final access is judged against the right block. The cost is $O(1)$.

**CHECK, LOAD and STORE.** Lines L6 and L7 are the spatial check: two comparisons. Lines L8 and L9 are the temporal check: one lookup in the store, $O(1)$ expected with a hash table. The spatial check comes first, so a null pointer and a far-off pointer report a spatial error.

**FREE.** Lines L12 and L13 refuse a free of an interior pointer and a second free. Line L14 cancels the capability. Every copy of the pointer, wherever the program keeps it, now fails line L8, with no search for the copies.

## Example

A heap of 64 bytes; address 0 is never used, so the first block starts at 1. The table shows each operation and the result.

| step | operation | result |
|---|---|---|
| 1 | $a$ ← ALLOC(8) | $a = (1, 1, 9, 1)$ |
| 2 | $b$ ← ALLOC(4) | $b = (9, 9, 13, 2)$, the next block |
| 3 | $q$ ← ADD($a$, 6); STORE($q$, 2, 0x0102) | bytes 7 and 8 written; $7 + 2 \le 9$ |
| 4 | LOAD(ADD($a$, 7), 1) | 0x01, the high byte |
| 5 | STORE($q$, 4, 7) | spatial error: $7 + 4 = 11 > 9$, so the store would reach $b$ |
| 6 | $r$ ← ADD($a$, 8); LOAD($r$, 1) | $r = (9, 1, 9, 1)$ is formed; the load is a spatial error |
| 7 | FREE($a$) | capability 1 leaves the store |
| 8 | $c$ ← ALLOC(8) | $c = (1, 1, 9, 3)$, the same block, a new number |
| 9 | LOAD($a$, 1) | temporal error: the bounds pass, capability 1 is dead |
| 10 | LOAD($c$, 1) | 0, a new block is zeroed |

Step 5 is the [buffer overflow](/buffer-overflow/) that the structure exists to stop: a plain pointer would write two bytes of $b$. Step 6 shows that the address one past the end is a legal value and an illegal target. Step 9 shows why the bounds alone are not enough: after the block is reused, the old pointer's bounds describe the new object, and only the capability tells the two apart.

## Correctness

ALLOC sets the fields from the block it returns, ADD changes only the value, and nothing else makes a fat pointer, so invariant (F) holds for every pointer the program holds. Then line L6 passes exactly when the $w$ bytes lie inside the block of the allocation, and line L8 passes exactly when that allocation is live. So a LOAD or a STORE succeeds exactly when it is memory safe, and reports the kind of error otherwise. The full proof, by induction on the number of operations, is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/) model.

| operation | time | notes |
|---|---|---|
| ALLOC | $O(h)$ plus $O(1)$ | the allocator's search dominates; the fat pointer adds a store insert |
| ADD | $\Theta(1)$ | one addition and three copies |
| CHECK, LOAD, STORE | $\Theta(1)$ | two comparisons and one lookup in a hash table, expected $O(1)$ |
| FREE | $O(h)$ plus $O(1)$ | one delete from the store |

Space: each pointer takes four words instead of one, and the store takes $O(1)$ words for each live allocation. The extra words in every pointer are the real cost. They raise cache and memory traffic, and they change the size of every structure that holds a pointer. The slowdown of a real system with fat pointers is a measurement of that system, its compiler and its benchmarks, not a property of the structure.

## Variants

- **Base and size, or base and bound.** Austin, Breach and Sohi store the base and the size, plus a storage class and the capability. Bound and size are equivalent; the bound saves an addition in the check.
- **Spatial only.** Drop the capability and keep $(\mathit{value}, \mathit{base}, \mathit{bound})$. This is the slice of Rust (a pointer and a length) and of Go (a pointer, a length and a capacity), where the type system handles the temporal side.
- **Kinds of pointers.** CCured infers for each pointer one of three kinds: SAFE (no arithmetic, a null check only), SEQ (a fat pointer with bounds) and WILD (bounds plus run-time type tags). Most pointers end up SAFE, which removes most of the cost. Cyclone lets the programmer pick fat, thin and never-null pointers in the types.
- **Disjoint metadata.** [SoftBound](/softbound/) keeps the same base and bound, but in a table beside memory, so the pointer keeps its size and the memory layout does not change.
- **Lock and key.** [Lock and key temporal checking](/lock-and-key-temporal-checking/) replaces the capability store with a lock word per allocation that the check reads directly.
- **Hardware capabilities.** [CHERI](/cheri-capability-model/) makes the fat pointer a register type with a tag bit, so the hardware checks the bounds and the program cannot forge them.
- **Object-based checking.** [Jones-Kelly](/jones-kelly-bounds-checking/) and [baggy bounds](/baggy-bounds-checking/) keep the bounds per object, not per pointer, and keep plain pointers.

## When to use it

Use fat pointers when you control the language or the whole program, so that every pointer can change its layout: a safe dialect of C, a new language, an interpreter, or a capability machine. They give exact bounds per pointer, they handle pointers that leave their block and return, and with a capability or a key they also find use after free. Do not use them when checked code must share pointers and structures with libraries compiled without the checks, because the layouts differ; then keep the metadata outside the pointer, as in [SoftBound](/softbound/), or per object, as in [Jones-Kelly](/jones-kelly-bounds-checking/).

## Pitfalls

- **Checking at ADD instead of at the access.** If line L5 refuses an address outside the block, common C loops that form the address one past the end, or that step outside and come back, are refused. The check belongs in line L6, at the access.
- **Checking only the first byte.** The test $p.\mathit{value} < p.\mathit{bound}$ lets a 4-byte store at the last byte of a block write 3 bytes of the next block. Line L6 must test $p.\mathit{value} + w > p.\mathit{bound}$.
- **Bounds that the program can write.** If a fat pointer is stored in memory as plain bytes, and the program can write those bytes as integers, it can forge the bounds. The fields must be written only by the allocator and by ADD, as CCured enforces with its kinds and CHERI with a tag bit.
- **Bounds without a temporal check.** After FREE and a new ALLOC of the same block, the old pointer's bounds fit the new object. Without line L8, step 9 of the example reads another object's data.
- **A cast from an integer.** A pointer made from an integer has no block. Give it null bounds, so every access fails, not the bounds of the whole memory.

## Implementations

The Python code runs on a simulated heap of a few hundred bytes, a bytearray with a first-fit allocator, and never on real memory. The tests run random programs of allocations, arithmetic, loads, stores and frees, and compare every verdict with an oracle that tracks each object and the offset of each pointer.

## History

Austin, Breach and Sohi described the safe pointer in 1994, with a spatial check against base and size and a temporal check against a capability store, and they called the result the detection of all pointer and array access errors. CCured (Necula, McPeak and Weimer, 2002) and Cyclone (Jim and others, 2002) put fat pointers into the types of a C-like language, and they reduced the cost by using thin pointers wherever the analysis or the programmer could show that no arithmetic happens. Later work moved the metadata out of the pointer to keep the memory layout ([SoftBound](/softbound/), 2009) and into hardware ([CHERI](/cheri-capability-model/), 2014).

## References
