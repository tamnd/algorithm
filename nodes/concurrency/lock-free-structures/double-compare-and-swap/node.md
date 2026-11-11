---
tag: BGB111
kind: concept
slug: double-compare-and-swap
name: Double-compare-and-swap (DCAS)
aliases:
- DCAS
- CAS2
- two-word compare-and-swap
area: concurrency/lock-free-structures
level: advanced
summary: An atomic step that compares two arbitrary memory words and, if both match, updates both. The Motorola 68020 to 68040 had it as CAS2; current CPUs do not.
prereqs: [compare-and-swap]
see_also: [compare-and-swap, multi-word-cas, tagged-pointers, aba-problem, consensus-number, cas-has-infinite-consensus-number, load-linked-store-conditional, lock-freedom]
sources:
  - url: "https://www.nxp.com/docs/en/reference-manual/M68000PRM.pdf"
    title: Motorola, M68000 Family Programmer's Reference Manual, 1992
    locator: Section 4, pages 4-66 and 4-67 (CAS and CAS2, for the MC68020, MC68030 and MC68040)
  - paper: doi:10.1145/238721.238767
    title: Michael Greenwald and David Cheriton, The synergy between non-blocking synchronization and operating system structure, OSDI 1996
    locator: pages 123 to 136 (a kernel built on DCAS data structures)
  - paper: doi:10.1145/571825.571874
    title: Michael Greenwald, Two-handed emulation, how to build non-blocking implementations of complex data-structures using DCAS, PODC 2002
    locator: pages 260 to 269
  - paper: doi:10.1145/341800.341817
    title: Ole Agesen, David Detlefs, Christine Flood, Alexander Garthwaite, Paul Martin, Nir Shavit and Guy Steele, DCAS-based concurrent deques, SPAA 2000
    locator: pages 137 to 146
  - paper: doi:10.1007/3-540-40026-5_4
    title: David Detlefs, Christine Flood, Alexander Garthwaite, Paul Martin, Nir Shavit and Guy Steele, Even better DCAS-based concurrent deques, DISC 2000
    locator: pages 59 to 73 (the Snark deque)
  - paper: doi:10.1145/1007912.1007945
    title: Simon Doherty, David Detlefs, Lindsay Groves, Christine Flood, Victor Luchangco, Paul Martin, Mark Moir, Nir Shavit and Guy Steele, DCAS is not a silver bullet for nonblocking algorithm design, SPAA 2004
    locator: pages 216 to 224 (Sections 3 and 4, the bugs in Snark and the fix; Section 6, 3CAS)
  - paper: doi:10.1007/3-540-36108-1_18
    title: Timothy Harris, Keir Fraser and Ian Pratt, A practical multi-word compare-and-swap operation, DISC 2002
    locator: pages 265 to 279 (DCAS and k-word CAS built from single-word CAS)
  - url: "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html"
    title: Intel 64 and IA-32 Architectures Software Developer's Manual
    locator: Volume 2A, the entry CMPXCHG8B/CMPXCHG16B (double-width CAS on one aligned location)
---

## In plain words

[Compare-and-swap](/compare-and-swap/) changes one memory word, and only if it still holds the expected value. Double-compare-and-swap does the same for two words at two unrelated addresses, in one indivisible step: if both words hold their expected values, both get their new values; if not, nothing changes. Many data structures need two pointers to change together, for example the two links around a node in a doubly linked list. With DCAS this takes one step. With single-word CAS it needs a much more careful algorithm. A few Motorola 680x0 processors had DCAS as the CAS2 instruction, but no common processor today has it. The instruction that current x86 and Arm processors call a double-width CAS is a different thing: it updates two adjacent words, which act as one wide word.

## The idea

**Definition.** DCAS takes two addresses, two expected values and two new values:

```text
DCAS(a1, a2, e1, e2, n1, n2):      -- all one atomic step
  if *a1 = e1 and *a2 = e2 then
    *a1 := n1; *a2 := n2
    return true
  return false
```

The addresses $a_1 \ne a_2$ are arbitrary: they can be in different cache lines, different objects or different pages. The Motorola CAS2 instruction (MC68020, MC68030, MC68040) is this operation in a slightly richer form. On failure it writes the current values of both memory operands back into the compare registers, so the program also gets an atomic read of the two words.

**DCAS and double-width CAS are different.** Keep the two apart, because many texts and some APIs use similar names.

| | operands | where they are | hardware |
|---|---|---|---|
| CAS | 1 word | anywhere | every current multiprocessor (or LL/SC) |
| double-width CAS | 2 words that make one aligned location | adjacent, one cache line | x86 CMPXCHG8B (32-bit) and CMPXCHG16B (64-bit), Arm CASP (Armv8.1) and LDXP/STXP, IBM CDS |
| DCAS | 2 words | any two addresses | Motorola CAS2 (MC68020 to MC68040); not in current mainstream CPUs |
| [multi-word CAS](/multi-word-cas/) | $k$ words | any $k$ addresses | none; built in software from CAS |

A double-width CAS is a single-location CAS on a wider location. It is very useful for a pointer with a version counter beside it ([tagged pointers](/tagged-pointers/) against the [ABA problem](/aba-problem/)), or for a pointer with a small extra field. It cannot change two pointers that live in two different nodes. For that, a program needs DCAS or a software multi-word CAS.

**Its power in theory.** DCAS has [consensus number](/consensus-number/) $\infty$, but so does plain CAS ([CAS has infinite consensus number](/cas-has-infinite-consensus-number/)). DCAS does CAS on one word if the second address is a dummy word that always holds the same value. In the other direction, Harris, Fraser and Pratt (2002) build a linearizable lock-free DCAS, and in general a $k$-word CAS, from single-word CAS (see [multi-word CAS](/multi-word-cas/)). So in the consensus hierarchy DCAS is not stronger than CAS. Its advantage is ease of design and the cost of each operation: one hardware step, compared with several CAS steps, a descriptor and helping in software.

**Its power in practice.** Greenwald's Stanford thesis (1999) argued that DCAS is the right primitive to add to hardware. Systems built on it were simple: Greenwald and Cheriton (1996) built the Cache Kernel on DCAS data structures on the MC68040, and Massalin and Pu had earlier built the Synthesis kernel on CAS2. The thesis argues that with DCAS a $k$-word CAS costs $O(k)$ steps without the contention problems of CAS-only methods. Greenwald (2002) gave a general method ("two-handed emulation") to build non-blocking objects with DCAS. The counter-argument came from Doherty et al. (2004): even with DCAS, correct and efficient non-blocking structures stay hard to design and to verify, so DCAS does not give enough extra power over CAS to justify its hardware cost. Their case study is the Snark deque in the examples below.

**Why hardware dropped it.** An atomic update of two independent lines needs the cache to own both lines at once. Two processors that each own one of them must not wait for each other for ever, so the protocol must order or abort the requests. This is a small hardware transaction. Hardware transactional memory (for example Intel TSX and IBM POWER) later offered the general form, and it can emulate DCAS, but it gives no guarantee that a transaction ever commits, and some processors disable it. Current lock-free libraries use single-word CAS, double-width CAS, or a software multi-word CAS.

## Examples

**Move a value between two cells.** A token is in cell $a$ and must move to cell $b$. One DCAS does it: DCAS($a$, $b$, $t$, $\bot$, $\bot$, $t$). A reader that reads both cells in one atomic step (CAS2 on failure gives it) always finds the token in exactly one cell. With two separate CASes there is an intermediate state where it is in both cells (copy first) or in neither (clear first), and the code must tell other processes how to finish or undo the move. This is exactly what the descriptor of a software multi-word CAS does.

**Delete from a doubly linked list.** To unlink node $x$ between $p$ and $n$, both links must change: $p.\text{next}$ from $x$ to $n$, and $n.\text{prev}$ from $x$ to $p$. With DCAS:

```text
DCAS(&p.next, &n.prev, x, x, n, p)
```

It succeeds only if the neighbours are still linked to $x$ on both sides, so no other process can see a list that is correct forward but wrong backward. With single-word CAS, lock-free doubly linked lists exist (for example by Sundell and Tsigas), but they need extra marks on the links and helping, and their proofs are long.

**The Snark deque (non-example of "DCAS makes it easy").** Detlefs et al. (2000) published Snark, a lock-free deque on a doubly linked list that uses DCAS, with a semi-formal proof. Doherty et al. (2004) later found two bugs with the help of the PVS proof assistant. In one run a pop returns "empty" while the deque was never empty, so Snark was not linearizable. In another, the same node is removed twice and its value is returned twice. They gave a corrected Snark and verified it. They also showed that a CAS on three independent words would make the pop operation simple, because the whole effect of a pop happens in one atomic step.

**Array deques.** Agesen et al. (2000) gave DCAS-based deques on an array and on a linked list. On the array, a pop updates the end index and clears the slot in one DCAS, so the index and the slot can never disagree.

**Non-example: a tagged pointer.** The Treiber stack with an ABA counter needs the top pointer and its counter to change together. They are adjacent, in one 16-byte location, so a double-width CAS (CMPXCHG16B) is enough. This is not a use of DCAS.

## Where it is used

- **History and research.** Massalin and Pu's Synthesis kernel and Greenwald and Cheriton's Cache Kernel used CAS2 on Motorola processors. Sun Labs studied DCAS deques and DCAS-based memory reclamation around 2000; Doherty et al. note that this work led to later methods that use only CAS.
- **As a building block in software.** Lock-free code that needs two words to change together uses a software DCAS or [multi-word CAS](/multi-word-cas/), for example the operation of Harris, Fraser and Pratt, or the RDCSS step inside it.
- **In transactional memory.** A two-location hardware transaction is DCAS. It is fast when it commits, but code must always have a fallback path.
- **In models and lower bounds.** Papers on the cost of $k$-word CAS use DCAS as the case $k = 2$, and textbooks use it to show that a stronger primitive does not move an object up the consensus hierarchy.

## References
