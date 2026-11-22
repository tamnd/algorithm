---
tag: 2R0MXX
kind: algorithm
slug: dangling-pointer-nullification
name: Dangling pointer nullification
aliases:
- DangNull
- pointer nullification on free
area: security-and-privacy/memory-safety-defenses
level: research
summary: Tracks which heap pointers refer to each object and sets them to a null value when the object is freed, so a use after free hits the null page.
model: word-ram
complexity:
  vars: {t: the number of live heap objects, d: the number of tracked pointers into or out of the freed object, s: the number of tracked pointers}
  time: {worst: O(log t + d)}
  space: {extra: Θ(t + s)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2015
  people: [Byoungyoung Lee, Chengyu Song, Yeongjin Jang, Tielei Wang, Taesoo Kim, Long Lu, Wenke Lee]
  note: "Presented at NDSS 2015 as DangNull, which traces the pointers stored in heap objects and nullifies them on free."
prereqs: [memory-safety]
see_also: [lock-and-key-temporal-checking, addresssanitizer, red-black-tree, reference-counting, mark-and-sweep, heap-reachability, memory-tagging, garbage]
sources:
  - paper: "Byoungyoung Lee, Chengyu Song, Yeongjin Jang, Tielei Wang, Taesoo Kim, Long Lu and Wenke Lee, Preventing use-after-free with dangling pointers nullification, NDSS 2015"
    url: https://doi.org/10.14722/ndss.2015.23238
    locator: "Section III (the shadow object tree, trace and freeObj, the opt-out for stack locations, and the null value) and Section V (the evaluation on SPEC CPU2006 and Chromium)"
  - paper: "Yves Younan, FreeSentry, protecting against use-after-free vulnerabilities due to dangling pointers, NDSS 2015"
    locator: "the registration of pointers in a lookup table and their invalidation when the memory is released, including pointers on the stack"
---

Dangling pointer nullification removes dangling pointers at the moment they would be created. A run-time library keeps, for each live heap object, the set of heap locations that hold a pointer into it. The compiler adds a call after every store of a pointer into the heap that updates these sets. When the program frees an object, the library goes through its set and overwrites each location that still points into the object with a small null value. A later use of such a pointer reads or writes the null page and faults at once, and a second free of it is a free of null, which does nothing. The program does not need a check at each access. The cost is in pointer stores and in free, and pointers kept only in registers, on the stack or in globals are not changed.

## In plain words

Think of a guest list for every room in a hotel: who has written down that room's number. Every time someone notes a room number in their own records, the hotel adds them to that room's list.

When a room is closed, the hotel goes down the list and crosses out the room number in each record, so it now says "no room". Anyone who later tries to use that record finds nothing there and stops, instead of walking into a room that may now belong to someone else.

The hotel only watches records kept in its own filing cabinets, the heap. Numbers someone holds in their head, or on scrap paper on the stack, are not on any list and are not crossed out.

## The problem

The input is a C or C++ program that allocates and frees heap objects and stores pointers to them in other heap objects. A use after free happens when the program frees an object and later uses a pointer to it; by then the memory may hold a new object. The goal is to make each such use harmless without a check at every access, and without changing the layout of memory. [Lock and key checking](/lock-and-key-temporal-checking/) catches every use but checks every access; [AddressSanitizer](/addresssanitizer/) catches uses only while the freed memory is in its quarantine. Nullification makes the pointer itself invalid, so the reuse of the memory no longer matters.

## The algorithm

A tree of shadow objects holds one entry per live heap object: its range $[\mathit{base}, \mathit{end})$, an in-set of the heap locations that point into it, and an out-set of the locations inside it that point to other objects, each with its target. The paper uses a variant of a [red-black tree](/red-black-tree/) for the objects and for each set. The search FIND$(a)$ returns the shadow object whose range holds $a$. NULLIFY is a small non-negative value, such as 0, whose page is never mapped.

```pseudo id=main
TRACE(lhs, rhs)                      ▷ after each pointer store *lhs = rhs
L1  if lhs is not inside a live heap object then return    ▷ stack and globals opt out
L2  remove the old relation of lhs from the out-set of its object and the in-set of its target
L3  s ← FIND(lhs); d ← FIND(rhs)
L4  if d = none then return
L5  add (lhs → d) to s.out and lhs to d.in

ALLOC(n)
L6  b ← allocate n bytes; insert a shadow object [b, b + n) with empty sets
L7  return b

FREE(p)
L8  o ← the shadow object with base p
L9  for each lhs in o.in do
L10     remove lhs from the out-set of FIND(lhs)
L11     if o.base ≤ M[lhs] < o.end then M[lhs] ← NULLIFY    ▷ it still points into o
L12 for each (lhs → t) in o.out do remove lhs from t.in
L13 delete o from the tree; free the block
```

**Tracing.** Line L1 skips stores whose location is not in a heap object. The paper found that most pointers to heap objects that live long are themselves in the heap, while pointers on the stack are short-lived, so skipping the stack keeps the cost down. Line L2 drops the relation that lhs had before, because the store overwrites the old pointer. Line L3 finds the object of the location and the object that the new value points into. Because FIND uses ranges, pointer arithmetic needs no tracking: a pointer to the middle of an object is found by its range.

**Free.** Lines L9 to L11 handle the pointers into the object. Line L11 checks the current value of the location again, because the program may have overwritten it with an integer since the trace, and an integer store is not traced. Line L12 removes the object's own pointers from the in-sets of their targets, so that a later free of a target does not write into memory that is no longer this object.

**The null value.** With NULLIFY = 0, code that checks for null before a use keeps working, and a use without a check faults. The paper also allows other small values, and maps nothing in the low addresses, so that an access at a small offset from the null value also faults.

## Example

A memory of 128 bytes: the null page $[0, 16)$, globals at $[16, 32)$ and the heap from 32. Pointers take 4 bytes.

| step | operation | result |
|---|---|---|
| 1 | $a, b, c$ ← ALLOC(8) three times | $a = 32$, $b = 40$, $c = 48$ |
| 2 | STORE-PTR($b$, $a + 4$) | $b[0]$ points into $a$: $a.\mathit{in} = \{40\}$, $b.\mathit{out} = \{40 \to a\}$ |
| 3 | STORE-PTR($c + 4$, $a$) | $a.\mathit{in} = \{40, 52\}$ |
| 4 | STORE-PTR(16, $a$) | a global points to $a$; line L1 skips it |
| 5 | $r$ ← LOAD-PTR($b$) | a copy in a register: $r = 36$ |
| 6 | FREE($a$) | locations 40 and 52 now hold 0; the out-sets of $b$ and $c$ are empty |
| 7 | LOAD(LOAD-PTR($b$), 1) | the pointer is 0: a fault in the null page |
| 8 | LOAD-PTR(16), and $r$ | still 32 and 36: these copies are dangling |

Steps 6 and 7 are the point of the scheme: the two heap copies are null after the free, wherever they are in the heap. Step 8 shows its limit: the global and the register copy were never traced.

## Correctness

The claim is about traced pointers. Call a location $\ell$ *linked* to a live object $o$ if the last pointer store at $\ell$ happened while $\ell$ was inside a live heap object, and stored a value inside $o$. The in-set of $o$ is exactly the set of locations linked to $o$, and the out-sets mirror the in-sets; each TRACE and each FREE keeps this, by lines L2 and L5 and by lines L10 and L12. So FREE$(o)$ visits every linked location, and line L11 nullifies those that still hold a value inside $o$. After the free, no heap location that was linked to $o$ and not overwritten since holds a pointer into $o$. The proof is in [the correctness proof](proofs/correctness.md).

## Complexity

With balanced trees, FIND takes $O(\log t)$ time for $t$ live objects, so a traced pointer store costs $O(\log t)$ in the [word RAM](/word-ram/) model. FREE costs $O(\log t)$ to find the object plus $O(d \log t)$ for the $d$ tracked pointers into and out of it, or $O(\log t + d)$ with hash sets as in the Python code. The tree takes $\Theta(t)$ space and the sets $\Theta(s)$ for $s$ tracked pointers.

Measured costs depend on how often a program stores pointers. The paper reports, in 2015, an average slowdown of 80% on SPEC CPU2006, with a wide spread between benchmarks, and it ran the Chromium browser with the scheme.

## Properties

- **No per-access check.** Only pointer stores and frees cost extra.
- **Not complete.** Pointers that live only in registers, on the stack or in globals are not nullified, and a pointer computed from a dangling register copy is not caught.
- **Turns double free into free of null.** A second free through a nullified heap pointer does nothing.
- **Deterministic.** The same program and input give the same nullifications.

## Variants and improvements

- **Registering every pointer.** FreeSentry registers pointers, including some on the stack, in a lookup table and invalidates them when the memory is released, with the same range test before it changes a location.
- **Cheaper bookkeeping.** Later systems replace the trees with per-object logs that may hold stale entries, which makes the trace cheaper and pushes the clean-up to free, and they scale to programs with many threads.
- **Sweeping instead of tracing.** Instead of tracing each store, a sweeper can scan memory for values that point into freed objects, as a [mark-and-sweep](/mark-and-sweep/) collector scans for reachable ones, and delay the reuse of freed memory until the scan is done.
- **Checking instead of nullifying.** [Lock and key checking](/lock-and-key-temporal-checking/) leaves the pointers alone and checks a key at each access, which also catches register and stack copies.

## When to use it

Use nullification to harden a large C++ program, such as a browser, against use after free when a check at every access is too slow and most long-lived pointers are in heap objects. It is a mitigation, not a full checker: a dangling copy on the stack or in a register can still be used, and pointers stored by code compiled without the trace are not tracked. It changes program values, so a program that compares a freed pointer with another value can behave differently. For finding bugs in testing, [AddressSanitizer](/addresssanitizer/) is simpler; if every use must be caught, use [lock and key checking](/lock-and-key-temporal-checking/), and if the language can manage memory, [reference counting](/reference-counting/) or a garbage collector avoids the problem.

## Pitfalls

- **Nullifying without the range test.** If line L11 writes NULLIFY whatever the location holds, a location that the program has since overwritten with an integer or with a pointer stored by untraced code is corrupted. Test that the value still lies in $[o.\mathit{base}, o.\mathit{end})$.
- **Not removing the old relation.** Without line L2, a location that first pointed into $o$ and then into another object is still in $o.\mathit{in}$, and the free of $o$ visits it. The range test saves the value, but the sets grow without bound.
- **Forgetting the out-set.** Without line L12, the in-set of a target keeps locations inside the freed object. When that memory is reused and the target is freed, line L11 can write into the new object.
- **Overlapping stores.** If pointers can be stored at unaligned addresses, two traced locations can overlap, and the result of line L11 depends on the order of the loop. Store pointers at word-aligned addresses.
- **A null value in mapped memory.** If NULLIFY, or NULLIFY plus a small field offset, falls in mapped memory, a use of the nullified pointer reads real data instead of faulting.

## Implementations

The Python code runs on a simulated memory, a bytearray with a null page, a global region and a first-fit heap, and never reads real memory. A sorted list stands in for the tree of shadow objects, and Python sets and dictionaries for the in-sets and out-sets. The tests run random programs of allocations, frees, pointer and integer stores and loads, and compare the whole memory after every step with an oracle that tracks the last traced pointer at each location. They also count the dangling copies in registers and globals that the scheme does not reach.

## History

Lee, Song, Jang, Wang, Kim, Lu and Lee presented DangNull at NDSS 2015, with a study of use-after-free bugs in the Chromium browser as the motivation. Younan presented FreeSentry at the same conference with a closely related design. Later work made the tracking cheaper and safe for many threads, or replaced it with sweeps of memory, and the idea of delaying reuse of freed memory until no pointer to it remains links this line of work to garbage collection.

## References
