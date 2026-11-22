---
tag: 4RX746
kind: algorithm
slug: softbound
name: SoftBound
aliases:
- disjoint metadata bounds checking
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Keeps base and bound for each pointer in a disjoint table indexed by the address where the pointer is stored, for spatial safety in C with no change to memory layout.
model: word-ram
complexity:
  vars: {s: the number of memory locations that hold a pointer}
  time: {worst: Θ(1)}
  space: {extra: Θ(s)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2009
  people: [Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin, Steve Zdancewic]
  note: "Presented at PLDI 2009 as a compile-time transformation for C that gives complete spatial safety while keeping the memory layout."
prereqs: [fat-pointer]
see_also: [fat-pointer, lock-and-key-temporal-checking, jones-kelly-bounds-checking, baggy-bounds-checking, shadow-memory, hash-table, cheri-capability-model, buffer-overflow]
sources:
  - paper: "Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin and Steve Zdancewic, SoftBound, highly compatible and complete spatial memory safety for C, PLDI 2009, pages 245 to 258"
    url: https://people.cs.rutgers.edu/~santosh.nagarakatte/papers/pldi09_softbound.pdf
    locator: "the sections on pointer metadata, the disjoint metadata space (hash table and shadow space), the bounds narrowing for structure fields, the formal model and the evaluation"
  - paper: "Todd M. Austin, Scott E. Breach and Gurindar S. Sohi, Efficient detection of all pointer and array access errors, PLDI 1994, pages 290 to 301"
    locator: the fat-pointer design that SoftBound keeps in registers and moves out of memory
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, IEEE Symposium on Security and Privacy 2013, pages 48 to 62"
    locator: the comparison of pointer-based and object-based spatial safety
---

SoftBound is a compiler transformation for C that gives every pointer its own base and bound, like a [fat pointer](/fat-pointer/), but keeps those bounds out of the pointer. In registers a pointer travels with its two bounds. In memory a pointer stays a single word, and its bounds go to a separate table, keyed by the address where the pointer is stored. A store of a pointer writes the table entry, a load of a pointer reads it, and every load and store through a pointer checks the address against the bounds. Because the memory layout does not change, structures, arrays of pointers and the calls to libraries keep their usual form. Because the bounds are per pointer and not per object, SoftBound also catches an overflow from one field of a structure into the next.

## In plain words

Each pointer gets a pair of fences: where its object starts and where it ends. While the program works with the pointer, the fences go with it, and every read or write is checked against them.

When the program puts the pointer away in memory, only the bare address goes into the memory cell. The fences are written into a separate notebook, on the line for that memory cell. When the program later takes the pointer out of the cell, the checker reads the fences back from the same line.

Nothing else in memory moves, so other code that does not know about the notebook still sees normal pointers. A pointer that was made from a plain number has no line in the notebook, gets empty fences, and cannot be used.

## The problem

The input is a C program. The goal is complete spatial [memory safety](/memory-safety/): no load or store may touch a byte outside the object, or the sub-object, that the pointer was made for. Two other approaches each lose something. A [fat pointer](/fat-pointer/) changes the size of pointers, so checked code no longer matches the layout of structures in code compiled without checks. Object-based checkers such as [Jones-Kelly](/jones-kelly-bounds-checking/) keep the layout but know only whole objects, so they cannot see an overflow inside a structure, and they need a search to find the object. SoftBound wants the precision of the first and the compatibility of the second.

## The algorithm

Each pointer value $p$ in a register has two companion values, $p.\mathit{base}$ and $p.\mathit{bound}$, and the object is $[\mathit{base}, \mathit{bound})$. The metadata table $\mathit{META}$ maps an address $a$ to the bounds of the pointer last stored at $a$. A pointer takes $W$ bytes in memory.

```pseudo id=main
ALLOC(n)
L1  b ← a new block of n bytes
L2  return (b, b, b + n)

ADD(p, k)
L3  return (p + k, p.base, p.bound)                ▷ bounds go along, no check

FIELD(p, off, size)                                ▷ &p->field
L4  v ← p + off; return (v, max(v, p.base), min(v + size, p.bound))

CHECK(p, w)
L5  if p < p.base or p + w > p.bound then
L6      report a bounds error

LOAD(p, w) and STORE(p, w, v)                      ▷ integers
L7  CHECK(p, w)
L8  read or write the w bytes at p                 ▷ META does not change

STOREPTR(loc, q)                                   ▷ *loc = q
L9  CHECK(loc, W)
L10 write the value q at loc
L11 META[loc] ← (q.base, q.bound)

LOADPTR(loc)                                       ▷ q = *loc
L12 CHECK(loc, W)
L13 v ← the value at loc
L14 (b, e) ← META[loc], or (0, 0) if there is no entry
L15 return (v, b, e)

INT-TO-PTR(v)
L16 return (v, 0, 0)                               ▷ empty bounds
```

**Creating bounds.** Lines L1 and L2 give a new object its exact bounds. The same happens for a stack array or a global, with the size known from its type. Line L4 makes a pointer to a field of a structure and narrows the bounds to the field, so a write past the end of one field fails, although it stays inside the whole object.

**Propagation.** Line L3 copies the bounds through pointer arithmetic, and a copy from one register to another copies them too. The check is at the access, so a pointer may leave its object and come back.

**Disjoint metadata.** Lines L10 and L11 split a pointer store into two writes: the value goes to its usual place, and the bounds go to $\mathit{META}$. Lines L13 to L15 put them together again on a load. The table is indexed by the address of the location, not by the value of the pointer, so two pointers with the same value can have different bounds. The paper implements $\mathit{META}$ either as a hash table or as a shadow space, a large array indexed by the address shifted right, which is a form of [shadow memory](/shadow-memory/).

**Calls.** When a pointer is passed to a function or returned from one, its bounds are passed as extra arguments. A copy of memory with a library function also copies the table entries of any pointers in it.

## Example

A memory of 64 bytes and pointers of 4 bytes; addresses below 4 are not used. The struct $s$ has a field name of 8 bytes and a field count of 4 bytes.

| step | operation | result |
|---|---|---|
| 1 | $s$ ← ALLOC(12) | $s = (4, 4, 16)$ |
| 2 | $c$ ← ALLOC(4) | $c = (16, 16, 20)$, a cell for one pointer |
| 3 | $nm$ ← FIELD($s$, 0, 8) | $nm = (4, 4, 12)$: the bounds of the field only |
| 4 | STORE(ADD($nm$, 8), 1, 66) | bounds error: $12 + 1 > 12$, although byte 12 is in $s$ |
| 5 | STORE(ADD($s$, 8), 4, 3) | allowed: count is in the bounds of $s$ |
| 6 | STOREPTR($c$, $nm$) | memory at 16 holds 4; $\mathit{META}[16] = (4, 12)$ |
| 7 | $q$ ← LOADPTR($c$); LOAD(ADD($q$, 8), 1) | $q = (4, 4, 12)$; the load is a bounds error |
| 8 | $f$ ← INT-TO-PTR(8); LOAD($f$, 1) | bounds error: $f = (8, 0, 0)$ |

Step 4 is an overflow inside one object, which an object table cannot see. Step 7 shows that bounds survive a round trip through memory. Step 8 shows that a pointer forged from an integer is useless, even though address 8 is inside a real object.

## Correctness

Call a pair of bounds *valid* if it is empty or is the range of an allocated object, or a part of one. Lines L2 and L4 make only valid bounds, line L3 copies them, line L16 makes empty bounds, and line L11 stores only bounds that the program held in a register. So, by induction on the steps, every entry of $\mathit{META}$ and every pointer in a register has valid bounds. Then line L5 lets an access through only if all its bytes lie inside valid bounds, so every access that succeeds stays inside one object. The proof is in [the correctness proof](proofs/correctness.md). The paper itself formalizes the scheme for a subset of C and gives a mechanized proof of spatial safety.

## Complexity

Each operation is $\Theta(1)$ in the [word RAM](/word-ram/) model: two comparisons for a check, and one table access for a pointer load or store, expected $O(1)$ with a [hash table](/hash-table/) and worst-case $O(1)$ with a shadow space. The table holds one entry per memory location that holds a pointer, $\Theta(s)$ space for $s$ such locations with a hash table; the shadow space reserves room for every word of memory and uses only the parts that are touched. Registers hold three words per pointer instead of one.

Measured costs depend on the compiler, the benchmarks and the machine. The paper reports an average run-time overhead of 67% for full checking on its benchmarks in 2009, and a much lower overhead when only stores are checked.

## Properties

- **Complete spatial safety.** Every load and store is checked, against bounds that are exact for objects and for fields.
- **Compatible layout.** Memory holds plain pointers, so the layout of every structure is unchanged.
- **Spatial only.** A pointer to a freed object keeps valid-looking bounds; temporal safety needs [lock and key checking](/lock-and-key-temporal-checking/) on top.
- **Separate compilation.** Each function needs only the bounds of its own pointers, passed with the arguments.

## Variants and improvements

- **Store-only checking.** Check only stores, which stops overflows that corrupt memory but not those that read past an object. It is much cheaper.
- **Temporal checking.** [Lock and key temporal checking](/lock-and-key-temporal-checking/), from the same group, adds a key and a lock address to the metadata of each pointer and uses the same disjoint table.
- **Hardware support.** The same design, bounds per pointer in registers and in a table indexed by the address of the pointer, was later built into hardware, with bounds registers and instructions to check them and to load and store table entries.
- **Capabilities.** [CHERI](/cheri-capability-model/) keeps the bounds inside a wider pointer, protected by a tag bit, which gives the precision of SoftBound without a separate table but changes the layout.

## When to use it

Use SoftBound when you need exact spatial safety for C, including overflows inside structures, and you must keep the memory layout because the program shares structures with code you cannot recompile. It is a compiler-based tool: all checked code must be compiled with it, and a library that stores pointers without updating the table returns pointers with empty or stale bounds. If you only need to find bugs in testing, [AddressSanitizer](/addresssanitizer/) is cheaper and finds use after free too, but misses overflows that jump over its redzones and overflows inside an object.

## Pitfalls

- **Keying the table by the pointer value.** If line L11 uses $q$ instead of $loc$ as the key, two pointers with the same value share one entry, and a pointer to one past the end of one array gets the bounds of the next object. The key is the address of the location.
- **Widening at a field.** If line L4 takes $v + \mathit{size}$ without the minimum with $p.\mathit{bound}$, a bad offset gives a field pointer with bounds outside the object. Always intersect with the old bounds.
- **Checking at arithmetic.** If line L3 rejects a value outside the bounds, programs that form the address one past the end of an array fail. The check is in line L5.
- **Unchecked writers of pointers.** A library compiled without the pass that writes a pointer into memory does not run line L11. The next LOADPTR from there gets the old entry or the empty bounds of line L14. Wrap such libraries so they update the table.
- **Integer stores over a pointer.** Line L8 does not change $\mathit{META}$, so a pointer that is overwritten with an integer and loaded again gets its old bounds. This keeps spatial safety, because the old bounds are still valid, but it can hide a bug.

## Implementations

The Python code runs on a simulated memory, a bytearray with a bump allocator, with pointers of 4 bytes and a dictionary as the metadata table, and never reads real memory. The tests run random programs that allocate objects, take fields, store pointers in memory and load them back, and overwrite them with integers. An oracle tracks the object and the offset of every pointer. Each check must match the oracle exactly when the oracle knows the pointer, and every access that succeeds must lie inside the bounds of one object.

## History

Austin, Breach and Sohi described per-pointer bounds in 1994 with fat pointers, which change the layout. Nagarakatte, Zhao, Martin and Zdancewic presented SoftBound at PLDI 2009. They kept the per-pointer bounds and moved them into a disjoint table, which keeps the layout, and they formalized the scheme and proved it safe. The same group added temporal checking with locks and keys in 2010. Hardware versions of the design followed.

## References
