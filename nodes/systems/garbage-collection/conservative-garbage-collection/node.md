---
tag: BZ71R7
kind: technique
slug: conservative-garbage-collection
name: Conservative garbage collection
aliases:
- conservative GC
- ambiguous roots collection
area: systems/garbage-collection
level: advanced
summary: "Collect without type information: treat every word that could be a pointer into the heap as one, and never move the objects it might point to."
prereqs: [gc-roots, tracing-garbage-collection, mark-and-sweep]
see_also: [precise-garbage-collection, boehm-gc, mostly-copying-collection, heap-reachability, segregated-free-lists, copying-collection]
sources:
  - paper: doi:10.1002/spe.4380180902
    title: Hans-Juergen Boehm and Mark Weiser, Garbage collection in an uncooperative environment, Software Practice and Experience 18(9), 807-820, 1988
    locator: the collector for C that treats every word in the registers, stack, static data and heap objects as a possible pointer, with its test for valid object addresses and its measurements of false retention
  - paper: doi:10.1145/155090.155109
    title: Hans-Juergen Boehm, Space efficient conservative garbage collection, PLDI 1993, 197-206
    locator: the sources of false retention, blacklisting of addresses that hold false references, and the cost of recognising interior pointers
  - paper: "Joel F. Bartlett, Compacting garbage collection with ambiguous roots, DEC Western Research Laboratory, Research Report 88/2, February 1988"
    locator: the term ambiguous roots, and a collector that is conservative only for the roots
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 11.2, Finding pointers, on conservative pointer finding, interior pointers and the cost of false retention
---

## In plain words

Some languages, such as C, do not tell the collector which values in memory are pointers. A number and an address are both just words. A conservative collector solves this by assuming the worst: if a word has a value that could be the address of an object, the collector treats it as a pointer and keeps that object.

This never frees an object that is in use, because every real pointer is also a word that looks like a pointer. But it can keep some garbage: a number that by chance equals an address keeps a dead object alive. And the collector must not move objects, because it cannot change a word that might be a number.

## When it applies

Use a conservative collector when these signals are present.

- **No type information for the roots or the heap.** The compiler gives no stack maps (see [precise collection](/precise-garbage-collection/)), or the code is C or C++, or there is foreign code whose frames the collector cannot decode.
- **Pointers are stored as plain words.** A pointer is a full machine word that holds the address of the object or of a place inside it. Programs that hide pointers, for example by XOR-linking a list or by writing them to a file, break the technique.
- **The address space is sparse.** The heap covers a small part of the possible word values, so few integers fall inside it by chance. This holds well for 64-bit addresses, and less well on 32-bit machines with large heaps.
- **Non-moving collection is acceptable.** Objects that ambiguous words point to cannot move. A [mark-sweep](/mark-and-sweep/) collector with [segregated free lists](/segregated-free-lists/) fits. A collector that wants to compact can be conservative only for the roots, as in [mostly-copying collection](/mostly-copying-collection/).

## The template

The model: the heap is the range $[lo, hi)$ of addresses. It holds allocated objects, each a range of words, and free space. The roots are a list of words: the registers, the stack and static data. Nothing says which words are pointers. The holes of the template are the pointer test (only starts of objects, or interior addresses too), the way to find the object that contains an address, and the sweep.

```pseudo id=main
COLLECT(roots)
L1  for each word w in the roots do MARK-IF-POINTER(w)
L2  while the mark stack is not empty do
L3      o ← pop the mark stack
L4      for each word w of o do MARK-IF-POINTER(w)
L5  for each allocated object o do
L6      if o is not marked then free o
L7      else clear the mark of o

MARK-IF-POINTER(w)                           ▷ the conservative pointer test
L8  if lo ≤ w < hi then
L9      o ← the allocated object that starts at w, or that contains w if interior pointers are allowed
L10     if o exists and is not marked then mark o; push o
```

**Walk-through.** The only change to a [tracing collector](/tracing-garbage-collection/) is line L8 to line L10, the pointer test. Line L8 is a cheap filter on the heap bounds. Line L9 must map an address to its object: a real collector uses the block structure of the heap (each block holds objects of one size, so the object start is found by a division), or a bitmap of object starts. Here it is a binary search over the sorted object starts. A word that points into free space, or into the gap between objects, is not a pointer. The marks of lines L1 to L4 are the closure of the roots under the relation "contains a word that looks like a pointer to". The sweep of lines L5 to L7 frees the rest. No object moves.

### Example

The heap is $[1000, 1012)$ with five objects: $A$ at 1000 (3 words), $B$ at 1003 (2 words), $C$ at 1005 (2 words), $D$ at 1007 (3 words) and $E$ at 1010 (2 words). The program really uses $A$ and $B$.

| object | words | what the words really are |
|---|---|---|
| $A$ | 1003, 7, 2000 | a pointer to $B$, a number, a number above the heap |
| $B$ | 42, 0 | numbers |
| $C$ | 1003, 0 | a pointer to $B$ (but $C$ is garbage) |
| $D$ | 1010, 0, 1 | a pointer to $E$, numbers |
| $E$ | 0, 0 | numbers |

The roots are $[1000, 1008, 5]$: a pointer to $A$, a loop counter that happens to be 1008, and a small number.

| step | word | result |
|---|---|---|
| L1 | 1000 | the start of $A$: mark $A$ |
| L1 | 1008 | inside $D$ (1007 to 1009): mark $D$ |
| L1 | 5 | below $lo$: not a pointer |
| L4, scan $D$ | 1010 | the start of $E$: mark $E$ |
| L4, scan $A$ | 1003 | the start of $B$: mark $B$ |
| L4 | 7, 2000, 42, 0, 1 | not in the heap |
| L5 to L7 | | free $C$; keep $A$, $B$, $D$, $E$ |

$D$ and $E$ are garbage, but the counter keeps them: this is *false retention*. If the collector accepts only pointers to the start of an object, 1008 is not a pointer, and $C$, $D$ and $E$ are all freed. That choice is cheaper and retains less, but it is wrong for a program that keeps only a pointer into the middle of an array. The tests run both versions.

### Correctness

**Claim.** COLLECT frees no object that the program can reach, provided that every real pointer in the roots and in reachable objects is stored as a word that MARK-IF-POINTER accepts.

*Proof.* Let $z$ be reachable, by a path of real pointers $r \to x_1 \to \cdots \to x_m = z$ from a root word $r$. The word $r$ is a pointer to $x_1$, so line L8 accepts it, line L9 finds $x_1$, and line L10 marks it, if it was not marked already. Every marked object is pushed once and popped once (lines L2 to L4), so all its words are tested. By induction along the path, each $x_j$ is marked: the word in $x_{j-1}$ that points to $x_j$ is tested at line L4. So $z$ is marked, and line L6 does not free it. Objects are never moved, so no word, real pointer or not, needs to change. $\blacksquare$

The converse fails: the set of marked objects is the closure of the roots under all words that look like pointers, which contains the reachable objects and possibly more. The tests check both facts on random programs, with the true types kept aside: the kept objects contain every reachable object, and they are exactly the closure of the pointer-looking words.

The proviso matters. With interior pointers turned off, a program that keeps only $p + 2$ for an array $p$ loses the array. A compiler that keeps a pointer only in a derived form, such as $p - 1000$ in a loop, also breaks the claim. Boehm calls this the problem of *GC safety* of compiler optimizations.

### Cost

Marking costs $O(R + W \log n)$ for $R$ root words, $W$ words in marked objects and $n$ objects, with a binary search at line L9. A block-structured heap does the test in $O(1)$, so marking is linear in the words scanned. The sweep is linear in the heap. The real cost is space: every word of every marked object is scanned, including large arrays of numbers, and false references retain whole data structures. A single false reference to the head of a long linked list keeps the entire list.

## Classic examples

- **The Boehm-Demers-Weiser collector.** A conservative [mark-sweep collector](/boehm-gc/) for C and C++ that replaces `malloc` with a collected allocator. It is used in many language runtimes that compile to C or need a collector without compiler support.
- **Conservative stacks, precise heap.** Many runtimes scan the stacks and registers conservatively but know the layout of each heap object. The [mostly-copying collector](/mostly-copying-collection/) of Bartlett pins the pages that ambiguous roots point to and copies the rest.
- **JavaScript engines.** Some engines, such as WebKit's JavaScriptCore, scan the machine stack conservatively and keep precise layouts for heap objects. This lets native code hold object pointers in local variables without registering them.
- **Runtimes without stack maps.** Scheme implementations that compile to C, the early Mono runtime for .NET, and the GNU Compiler for Java used a conservative collector, because their compilers did not give the collector stack maps.

## Variations

- **Interior pointers or not.** Accepting pointers into the middle of objects is needed for C arrays and for some compiler optimizations, but it makes each object a larger target for false references.
- **Pointer-free objects.** An allocator call that marks an object as holding no pointers, such as Boehm's `GC_malloc_atomic`, keeps large numeric arrays and strings from being scanned, which saves time and removes most false references.
- **Typed layouts.** A program can describe which words of an object type are pointers. The collector is then precise in the heap and conservative only in the roots.
- **Blacklisting.** Boehm's collector notes the addresses of free memory that false references point to and does not allocate objects there, so that the false references keep nothing alive.
- **Conservative roots with a moving heap.** Pin the objects or pages that ambiguous roots point to, and move the rest.

## Pitfalls

- **Hidden pointers.** A pointer that the program stores in a disguised form (XOR, tagged in high bits, written to disk, kept only in memory that the collector does not scan, such as memory from the system `malloc`) is invisible, and its object is freed while in use.
- **Derived pointers.** An optimizing compiler can keep only $p + k$ for a large $k$, or a pointer one past the end of an array, which points into the next object or outside the heap.
- **Unbounded false retention.** A false reference to one node of a linked structure retains everything reachable from that node. Data structures that are "lazy" or grow without limit, such as a queue whose removed nodes still point to the next node, can keep unbounded memory alive. Clearing the link fields of removed nodes limits the damage.
- **Pinning.** An ambiguous word may be a number, so the object it points to cannot move. A conservative collector cannot compact, and fragmentation can grow.
- **Scanning everything.** Without pointer-free allocation, large buffers of data are scanned word by word, and each random word is a possible false reference.

## Exercises

1. In the example, which objects are kept if the roots are $[1004, 1011]$ with interior pointers allowed, and with them not allowed?
2. A heap of $2^{26}$ bytes sits in a 32-bit address space. If the root and heap words were uniform random 32-bit values, what fraction of them would pass line L8? Why do real programs do worse than this estimate?
3. Prove that the set of marked objects does not depend on the order in which the words are tested.

## References
