---
tag: F1X4NS
kind: algorithm
slug: jones-kelly-bounds-checking
name: Jones-Kelly bounds checking
aliases:
- object table bounds checking
- referent object bounds checking
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Keeps a table of live objects and checks that each pointer arithmetic result stays in the object the operand points to, or one past its end.
model: word-ram
complexity:
  vars: {t: the number of live objects in the object table, h: the number of holes in the free list}
  time: {worst: O(log t), amortized: O(log t)}
  space: {extra: Θ(t)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1997
  people: [Richard W. M. Jones, Paul H. J. Kelly]
  note: "Presented at AADEBUG 1997 as a bounds checker for C that keeps the representation of pointers, so checked and unchecked code can be mixed."
prereqs: [memory-safety]
see_also: [baggy-bounds-checking, fat-pointer, softbound, splay-tree, addresssanitizer, shadow-memory, buffer-overflow, red-black-tree]
sources:
  - paper: "Richard W. M. Jones and Paul H. J. Kelly, Backwards-compatible bounds checking for arrays and pointers in C programs, Third International Workshop on Automatic Debugging (AADEBUG) 1997, pages 13 to 25"
    locator: the object table in a splay tree, the check of each pointer arithmetic result against the object of the operand, the extra byte after each object, and the value ILLEGAL
  - paper: "Olatunji Ruwase and Monica S. Lam, A practical dynamic buffer overflow detector, NDSS 2004, pages 159 to 169"
    locator: the out-of-bounds objects of CRED and the four steps for creating, checking and removing them
  - paper: "Dinakar Dhurjati and Vikram Adve, Backwards-compatible array bounds checking for C with very low overhead, ICSE 2006"
    locator: the use of automatic pool allocation to split the object table into small per-pool tables
  - paper: "Periklis Akritidis, Manuel Costa, Miguel Castro and Steven Hand, Baggy bounds checking, USENIX Security Symposium 2009"
    locator: the description of earlier referent-object schemes and the cost of their splay tree lookups
---

Jones-Kelly bounds checking finds out-of-bounds pointers in C without changing the size or layout of pointers. The checker keeps a table of all live objects, with the base and the size of each. Each time the program computes a pointer by arithmetic, the checker finds the object that the operand points into, its *referent object*, and checks that the result is still inside that object or exactly one past its end. A result outside that range becomes the special value ILLEGAL, which cannot be used. Because pointers stay plain addresses, checked code and libraries compiled without checks can pass pointers to each other. The cost is a search in the object table on every pointer operation.

## In plain words

Every allocated block is written into a register book: where it starts and how long it is. Pointers are left as plain addresses.

When the program moves a pointer, the checker looks the starting address up in the book and finds the block it is in. If the new address is still in that block, or just after its last byte, the move is fine. If it lands anywhere else, even inside some other block, the checker replaces it with a marker that means "bad pointer", and any later use of the marker stops the program.

When the program reads or writes, the checker looks the address up once more and checks that the whole access fits in the block.

Each block gets one spare byte at its end, so the address just after a block never looks like the start of the next one.

## The problem

The input is a C program whose pointer operations are the allocation of an object, pointer arithmetic $q = p + k$, loads and stores of $w$ bytes through a pointer, and free. The goal is to stop every access that leaves the object a pointer was derived from, the spatial part of [memory safety](/memory-safety/), while each pointer stays a single address, so that its size, the layout of structures and the calling conventions do not change. A [fat pointer](/fat-pointer/) solves the first part and breaks the second. The C standard permits a pointer to the elements of an array and to one past its last element, and nothing else, so a check at arithmetic time matches the language rule.

## The algorithm

The checker keeps an object table $T$ of the live objects, each a pair $(b, n)$ of a base and a size, in a search tree keyed by $b$. Every object occupies $n + 1$ bytes: the extra pad byte at $b + n$ belongs to the object, so a pointer one past the end is inside $[b, b + n]$ and not at the start of the next object. ILLEGAL is a fixed value that is never the address of an object; Jones and Kelly use $(\text{void}*)\,{-2}$.

```pseudo id=main
ALLOC(n)
L1  b ← a block of n + 1 bytes from the allocator   ▷ one pad byte at b + n
L2  insert (b, n) into the object table T
L3  return b

LOOKUP(p)
L4  return the object (b, n) in T with b ≤ p ≤ b + n, or none

ADD(p, k)
L5  if p = ILLEGAL then report an error
L6  o ← LOOKUP(p)                                 ▷ the referent object
L7  if o = none then return p + k                 ▷ unchecked memory: not checked
L8  if o.b ≤ p + k ≤ o.b + o.n then return p + k  ▷ one past the end is allowed
L9  return ILLEGAL

CHECK(p, w)                                       ▷ before each load or store
L10 if p = ILLEGAL then report an error
L11 o ← LOOKUP(p)
L12 if o = none then report an error              ▷ when all memory is in T
L13 if p + w > o.b + o.n then report an error

FREE(p)
L14 if no object in T has base p then report an error
L15 delete (p, n) from T; return its n + 1 bytes to the allocator
```

**Allocation.** Lines L1 to L3 allocate one extra byte and record the object. Stack and static objects of checked code are recorded the same way when their scope starts and removed when it ends.

**Arithmetic.** Line L6 finds the referent object of the operand with a search in $T$ for the last base that is at most $p$, then a test that $p \le b + n$. Line L8 accepts a result in $[b, b + n]$, which covers every element and the one-past-the-end pointer. Line L9 marks every other result. Line L7 lets a pointer that is in no checked object, for example a pointer into memory of a library compiled without checks, go through unchecked.

**Access.** Line L13 checks the last byte of the access, so an access of $w$ bytes at the last element, or at the one-past-the-end pointer, is refused. In the original system, a pointer in no checked object is allowed at line L12, because it can point into unchecked memory; in a model where every object is in $T$, as in the Python code, line L12 refuses it.

**Free.** Line L14 refuses a free of an address that is not the base of a live object, which catches a free of an interior pointer and many double frees.

## Example

A heap of 64 bytes; address 0 is not used. The table shows each operation and the result.

| step | operation | result |
|---|---|---|
| 1 | $a$ ← ALLOC(8) | $a = 1$; the object is bytes 1 to 8, the pad byte is 9 |
| 2 | $b$ ← ALLOC(4) | $b = 10$; LOOKUP(9) is $a$ and LOOKUP(10) is $b$ |
| 3 | ADD($a$, 8) | 9, one past the end, allowed by line L8 |
| 4 | LOAD(9, 1) | error at line L13: $9 + 1 > 1 + 8$ |
| 5 | ADD($a$, 9) | ILLEGAL: 10 is outside $[1, 9]$, although it is the base of $b$ |
| 6 | $q$ ← ADD($a$, 6); STORE($q$, 4, 7) | error at line L13: $7 + 4 > 9$ |
| 7 | ADD(ADD($a$, 12), $-12$) | the inner ADD gives ILLEGAL; the outer one is an error at line L5 |
| 8 | FREE($a$); LOAD($a$, 1) | error at line L12: address 1 is in no object |
| 9 | $c$ ← ALLOC(8); LOAD($a$, 1) | $c = 1$; the old pointer now finds $c$, and the load passes |

Step 5 shows why the check is against the referent object and not against all of memory: address 10 is valid memory, but not memory of the object that $a$ points into. Step 7 is a false alarm. C forbids the intermediate pointer, but real programs form it and come back, and they then stop with an error. Step 9 is a missed use after free: the checker knows objects, not allocations, so a dangling pointer into a new object looks valid.

## Correctness

Assume that each pointer the program uses comes from ALLOC or ADD, that the objects in $T$ with their pad bytes are disjoint, and that the referent object of a pointer stays live while the pointer is used. Then by induction on the ADD steps, each pointer derived from an object $(b, n)$ is either ILLEGAL or in $[b, b + n]$: ALLOC returns $b$, and line L8 keeps a result only if it is in that range, which by disjointness LOOKUP maps back to the same object. So at an access, LOOKUP finds the object the pointer was derived from, and line L13 refuses exactly the accesses whose last byte is past $b + n - 1$. Every out-of-bounds access through such a pointer is reported, and every in-bounds access through a pointer that never left $[b, b + n]$ passes. The guarantee does not cover a pointer that left and came back, which line L9 marks, or a pointer whose object was freed.

## Complexity

With the object table in a [splay tree](/splay-tree/), as in the original, each LOOKUP takes $O(\log t)$ amortized time for $t$ live objects; a [red-black tree](/red-black-tree/) gives $O(\log t)$ in the worst case. ADD and CHECK each do one LOOKUP plus $O(1)$ work. ALLOC and FREE add an insert or a delete in $O(\log t)$ to the cost of the allocator, $O(h)$ for first fit with $h$ holes. The table takes $\Theta(t)$ space, and each object one extra byte. The Python code keeps the table as a sorted list searched with [binary search](/binary-search/), so its inserts and deletes cost $O(t)$.

The search on every pointer operation is the main cost, and the reported slowdowns of this class of checker are large. Later work used the table less often, made it smaller, or replaced it with a constant-time lookup.

## Properties

- **Compatible.** Pointers keep their size and meaning, so checked code can call unchecked libraries and the other way round.
- **Spatial only.** It does not track whether an allocation is live, only whether some live object holds the address.
- **Checks arithmetic, not only access.** It refuses a pointer as soon as it leaves its object, which is stricter than many programs expect.
- **Online and deterministic.** Each check uses only the current table.

## Variants and improvements

- **CRED.** Ruwase and Lam replace ILLEGAL with an out-of-bounds object that holds the out-of-bounds address and its referent object. The OOB objects live in their own hash table, not in the object table. Arithmetic and comparisons on such a pointer consult that table, a pointer that comes back into its object becomes normal again, and freeing an object removes the OOB objects that refer to it. This removes the false alarm of step 7. To keep the cost low, CRED checks only string operations by default.
- **Pool-based tables.** Dhurjati and Adve split the object table into one table per memory pool, found by pointer analysis, so that each search runs on a much smaller tree.
- **Baggy bounds.** [Baggy bounds checking](/baggy-bounds-checking/) pads each object to a power of two, so the referent object is found in constant time from a table indexed by the address.
- **Shadow memory.** [AddressSanitizer](/addresssanitizer/) drops the referent object altogether and asks a [shadow memory](/shadow-memory/) whether each byte is addressable, which finds most but not all overflows in constant time.
- **Per-pointer metadata.** [SoftBound](/softbound/) keeps base and bound per pointer in a disjoint table, which handles sub-object bounds that an object table cannot see.

## When to use it

Use an object-table checker when the program must stay binary compatible with code compiled without checks and when you want to catch arithmetic that leaves an object, not only accesses that fall in unallocated memory. It is a debugging tool: the cost of a tree search per pointer operation is too high for most production use. It does not find overflows inside an object, from one field of a structure into the next, because the table only knows whole objects. Use [baggy bounds](/baggy-bounds-checking/) or [AddressSanitizer](/addresssanitizer/) when the speed matters more than the exact bounds, and add a temporal checker if you need to find use after free.

## Pitfalls

- **No pad byte.** If line L1 allocates only $n$ bytes, the pointer one past the end of an object is the base of the next object, LOOKUP in line L6 returns the wrong object, and a later access through it passes. The pad byte keeps the ranges $[b, b + n]$ disjoint.
- **Checking only the first byte.** If line L13 tests $p > o.b + o.n - 1$ instead of $p + w > o.b + o.n$, a 4-byte store at the last byte writes 3 bytes past the object.
- **Checking against all memory.** If line L8 accepts any result in some live object, step 5 of the example passes and a pointer can move from one object into the next, which is exactly the overflow to stop. The test must use the object of the operand found in line L6.
- **Treating ILLEGAL as an address.** If line L10 is left out, an ILLEGAL value can fall inside an object in a memory model where it is a valid address, and a bad pointer passes. Pick a value that is never inside an object and test for it first.
- **Expecting temporal safety.** After a free and a new allocation at the same address, step 9 passes. Do not report the checker as a use-after-free detector.

## Implementations

The Python code runs on a simulated heap, a bytearray with a first-fit allocator, and never reads real memory. The object table is a sorted list with binary search in place of the splay tree. The tests compare each result with an oracle that scans all live objects, and check two claims on random programs: every access out of bounds of a live object is caught, and every access through a pointer that never left its object passes.

## History

Jones and Kelly presented the scheme at AADEBUG in 1997 as a patch to GCC, with the goal of checking C programs while keeping the pointer representation, so that checked and unchecked modules could be linked together. Ruwase and Lam built CRED on it in 2004 and removed most false alarms with out-of-bounds objects. Dhurjati and Adve made the table searches faster with pool allocation, and Akritidis and others replaced the tree with a constant-time table in [baggy bounds checking](/baggy-bounds-checking/) in 2009.

## References
