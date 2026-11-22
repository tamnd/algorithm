---
tag: NYGPH2
kind: algorithm
slug: lock-and-key-temporal-checking
name: Lock and key temporal checking
aliases:
- CETS
- compiler-enforced temporal safety
- identifier-based temporal checking
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Gives each allocation a unique key and lock, copies the key with each pointer, and checks that the lock still holds the key at each access.
model: word-ram
complexity:
  vars: {a: the number of live allocations, s: the number of memory locations that hold a pointer, h: the number of holes in the free list}
  time: {worst: Θ(1)}
  space: {extra: Θ(a + s)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2010
  people: [Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin, Steve Zdancewic]
  note: "Presented at ISMM 2010 as a compiler transformation for C that finds every use of a dangling pointer, with keys and locks kept in disjoint metadata."
prereqs: [softbound]
see_also: [softbound, fat-pointer, dangling-pointer-nullification, addresssanitizer, memory-tagging, free-list, hash-table, memory-safety]
sources:
  - paper: "Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin and Steve Zdancewic, CETS, compiler enforced temporal safety for C, International Symposium on Memory Management (ISMM) 2010, pages 31 to 40"
    locator: "the sections on the key and lock of each allocation, the disjoint metadata for pointers in memory, the stack frames and globals, and the evaluation"
  - paper: "Todd M. Austin, Scott E. Breach and Gurindar S. Sohi, Efficient detection of all pointer and array access errors, PLDI 1994, pages 290 to 301"
    locator: the capability of each allocation and the capability store that the temporal check looks up
  - paper: "Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin and Steve Zdancewic, SoftBound, highly compatible and complete spatial memory safety for C, PLDI 2009, pages 245 to 258"
    locator: the disjoint metadata table that the temporal scheme shares
---

Lock and key temporal checking finds every use of a dangling pointer, a pointer to memory that was freed. Each allocation gets a *key*, a number that is never used again, and a *lock*, a memory word that holds the key while the allocation is live. Every pointer carries the key of its allocation and the address of its lock. Before an access, the checker compares the lock with the key. Free writes an invalid value into the lock, so every pointer into the allocation, wherever its copies are, fails the next check. The check is a load and a compare, with no search for the copies and no table of live objects. When pointers are stored in memory, their keys and locks go to a disjoint table, as in [SoftBound](/softbound/), so the memory layout does not change.

## In plain words

When a block of memory is handed out, it gets a fresh ticket number that will never be issued again. The number is written on a small board, the lock, that belongs to the block, and a copy of the number goes with every pointer into the block.

Before using a pointer, the program walks to the board and compares the numbers. If they match, the block is still in use. When the block is given back, the board is wiped. Every old pointer now shows a number that is not on the board, so every use after the free is caught.

Boards can be reused for new blocks, because the new block gets a new number. An old pointer still holds the old number and still fails.

## The problem

The input is a C program with ALLOC, FREE, pointer arithmetic, loads and stores, and pointers stored in memory. The goal is temporal [memory safety](/memory-safety/): every access through a pointer whose allocation was freed must be caught, even when the memory was reused by a new allocation, and so is a second free of the same allocation. Checking the address is not enough, because after reuse a dangling pointer points to a valid object, and that object is not the one the pointer was made for. A table of live objects, as in [Jones-Kelly](/jones-kelly-bounds-checking/), cannot tell the two apart for the same reason.

## The algorithm

$\mathit{LOCKS}$ is an array of lock words. A free lock and a lock of a freed allocation hold the value INVALID, and no key equals INVALID. A pointer in a register is a triple $(p, \mathit{key}, \mathit{lock})$. $\mathit{META}$ maps the address of a pointer stored in memory to its key and lock.

```pseudo id=main
ALLOC(n)
L1  b ← a block of n bytes from the allocator
L2  key ← next_key; next_key ← next_key + 1       ▷ never reused
L3  lock ← a free lock location                     ▷ lock locations are reused
L4  LOCKS[lock] ← key
L5  return (b, key, lock)

ADD(p, k)
L6  return (p + k, p.key, p.lock)

CHECK(p)
L7  if LOCKS[p.lock] ≠ p.key then
L8      report a temporal error

LOAD(p, w) and STORE(p, w, v)
L9  CHECK(p)
L10 read or write the w bytes at p

FREE(p)
L11 CHECK(p)                                        ▷ a double free fails here
L12 LOCKS[p.lock] ← INVALID
L13 give back the lock location and the block

STOREPTR(loc, q)
L14 CHECK(loc); write q at loc; META[loc] ← (q.key, q.lock)

LOADPTR(loc)
L15 CHECK(loc); v ← the value at loc; return (v, META[loc]), or (v, 0, the null lock) if there is no entry
```

**Keys and locks.** Line L2 takes the next value of a counter, so two allocations never share a key. Line L3 can reuse a lock location, because what the check compares is the key in it. With 64-bit keys, the counter does not run out in practice.

**The check.** Line L7 is one load from the lock and one compare. It is correct for every copy of a pointer, because all copies carry the same key and lock address, and they read the same lock.

**Free.** Line L11 runs the check first, so a free through a dangling pointer, and a second free, are errors. Line L12 kills every pointer to the allocation at once. Compare this with [dangling pointer nullification](/dangling-pointer-nullification/), which must find and change each pointer.

**Stack and globals.** A stack frame gets a key and a lock when it is entered and the lock is set to INVALID when it returns, so a pointer to a local variable that outlives its frame fails too. Globals share one lock that is never invalidated.

## Example

A heap of 64 bytes with first fit; address 0 is not used. Lock location 0 is the null lock, which matches no key.

| step | operation | result |
|---|---|---|
| 1 | $a$ ← ALLOC(8) | $a = (1, 1, 1)$, $\mathit{LOCKS}[1] = 1$ |
| 2 | $c$ ← ALLOC(4) | $c = (9, 2, 2)$, a cell for one pointer |
| 3 | $q$ ← ADD($a$, 4); STOREPTR($c$, $q$) | memory at 9 holds 5; $\mathit{META}[9] = (1, 1)$ |
| 4 | FREE($a$) | $\mathit{LOCKS}[1] = $ INVALID; lock 1 and the block go back |
| 5 | LOAD($q$, 1) | temporal error: $\mathit{LOCKS}[1] \ne 1$ |
| 6 | $r$ ← LOADPTR($c$); LOAD($r$, 1) | $r = (5, 1, 1)$, the copy from memory; temporal error |
| 7 | $d$ ← ALLOC(8) | $d = (1, 3, 1)$: the same block and the same lock location, key 3 |
| 8 | LOAD($a$, 1) | temporal error: the lock holds 3, the pointer holds 1 |
| 9 | FREE($a$) | temporal error: a double free |

Step 6 shows that copies stored in memory are caught with no extra work at free. Step 8 shows why the key and not the lock decides: the old pointer reads a valid lock that now belongs to $d$, and the key tells them apart.

## Correctness

Every pointer derived from an allocation carries its key and lock address: ALLOC sets them, ADD copies them, and STOREPTR and LOADPTR keep them in $\mathit{META}$. The lock of a live allocation holds its key, because only line L4 writes a key into a lock, and only line L12 writes to the lock of a live allocation. After free, the lock holds INVALID or the key of a later allocation, and both differ from the old key, because keys are never reused. So line L7 passes exactly when the allocation of the pointer is live. The proof, by induction on the operations, is in [the correctness proof](proofs/correctness.md).

## Complexity

The check is $\Theta(1)$ in the [word RAM](/word-ram/) model: one load and one compare. ALLOC and FREE add $O(1)$ to the cost of the allocator: a counter step, and taking or giving back a lock location from a [free list](/free-list/) of locks. A pointer load or store adds one access to $\mathit{META}$, expected $O(1)$ with a [hash table](/hash-table/). The lock space has one word for each live allocation and stack frame, and $\mathit{META}$ one entry for each location that holds a pointer. Each pointer in a register takes two extra words.

The run-time cost of a real system depends on the compiler, the benchmarks and how many checks static analysis can remove. It is a measurement and not a property of the scheme.

## Properties

- **Complete for temporal errors.** Every access through a dangling pointer is caught, including after the memory is reused.
- **No search at free.** Free writes one word, whatever the number of copies of the pointer.
- **Compatible layout.** Pointers in memory stay one word; the key and lock live in disjoint metadata.
- **Temporal only.** A pointer that leaves its object is not caught; combine with [SoftBound](/softbound/) for spatial safety.

## Variants and improvements

- **Capability store.** Austin, Breach and Sohi kept a capability number in each [fat pointer](/fat-pointer/) and looked it up in a store of live capabilities. The lock replaces that lookup with a load from a known address.
- **With spatial checks.** The same metadata table can hold base, bound, key and lock, which gives full memory safety with one table lookup per pointer load or store.
- **In hardware.** The key and lock check can be done by the processor on each access, with the metadata in a shadow space.
- **Probabilistic versions.** [Memory tagging](/memory-tagging/) keeps a small tag, a short key, in the pointer and in the memory itself. It needs no lock load but catches a reuse only with high probability, since tags repeat.
- **Nullification.** [Dangling pointer nullification](/dangling-pointer-nullification/) changes the pointers instead of the lock, so later accesses need no check, but it must track every pointer.

## When to use it

Use lock and key checking when you need to catch every use after free and every double free, including after the memory is reused, and you can compile the whole program with the checks. It fits testing and hardened builds of C and C++ code where an exact answer matters more than speed. It needs metadata for every pointer, so code compiled without it, which copies pointers without their keys, produces pointers that fail or are not checked. If a probabilistic answer is enough, [memory tagging](/memory-tagging/) or the quarantine of [AddressSanitizer](/addresssanitizer/) is cheaper.

## Pitfalls

- **Reusing keys.** If line L2 takes a key from a pool of freed keys, a dangling pointer with the old key matches the lock of a new allocation, and step 8 passes. Keys must come from a counter.
- **Checking the lock address instead of the key.** If line L7 only tests that the lock location is in use, a pointer whose lock location was reused passes. Compare the value in the lock with the key.
- **Free without the check.** Without line L11, a double free writes INVALID into a lock that may now belong to another allocation, and that allocation's pointers then fail, far from the bug.
- **Losing metadata through memory.** If STOREPTR in line L14 does not write $\mathit{META}$, a pointer loaded back in line L15 gets stale or missing metadata. Every store of a pointer, including those in copies of whole structures, must update the table.
- **Forgetting the stack.** Without a lock per frame, a pointer to a local variable that is used after the function returns is not caught.

## Implementations

The Python code runs on a simulated heap, a bytearray with a first-fit allocator, a list of lock words and a dictionary as the metadata table, and never reads real memory. The tests keep all accesses in bounds, so that only temporal errors appear, and compare every check with an oracle that tracks whether the object of each pointer is live. They count uses after free with and without reuse of the memory, and double frees.

## History

Austin, Breach and Sohi gave each allocation a unique capability in 1994 and checked it against a store of live capabilities. Nagarakatte, Zhao, Martin and Zdancewic presented the lock and key scheme with disjoint metadata at ISMM 2010, as the temporal half of a design whose spatial half is [SoftBound](/softbound/), and they showed that it catches all temporal errors at a cost low enough for testing. Later work from the same group and others moved the check into hardware, and memory tagging made a probabilistic version of the idea part of commercial processors.

## References
