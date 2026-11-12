---
title: Immix keeps the object graph and never hands out a byte of a live object
proves: [correctness]
status: full
---

We use the heap model and the procedures of the page. A *cycle* is the time from the end of one collection to the end of the next. Line size $s$, lines per block $l$. Objects never cross a block, and a small object has size at most $s$, so it lies in its first line $j$ and at most the line $j + 1$ of the same block.

**Lemma 1 (each object is copied at most once).** PROCESS copies $x$ only if $x$ is neither forwarded nor marked (lines L12 and L13), and then sets the forwarding address of $x$ and marks the copy in the same call. A later call on $x$ returns at line L12, and a later call on the copy returns at line L13. Copies are placed in free blocks, which are not in $C$ (line L7 picks only blocks with marked lines), so a copy is never a candidate. $\square$

**Lemma 2 (the trace keeps the graph).** Name objects by identity: a copy has the identity of its original. After COLLECT: (a) every root and every field of a marked object holds the current address of the object it named before, or nil; (b) the marked objects are exactly the objects reachable from the roots, each at one address.

*Proof.* Every root goes through PROCESS at line L8 and every field of every pushed object at line L10. PROCESS returns $x$ itself, or the address of the copy of $x$, which has the same identity and the same fields; so (a) holds for each value it writes. Each marked object is pushed once (line L16), so all its fields are processed. The marking argument of mark-and-sweep then gives (b): a marked object was reached from a root by a chain of processed fields, and every field of a marked object leads to a marked object. $\square$

**Lemma 3 (live bytes are covered).** After COLLECT, let $j$ be a line that holds a byte of a live object $x$. Then $j$ is marked, or $j - 1$ is a marked line of the same block.

*Proof.* By Lemma 2 the live object is marked at its current address. If $x$ is medium, line L15 marks every line it covers. If $x$ is small, it lies in its first line $f$, which is marked, and possibly in $f + 1$, in the same block. So $j = f$ is marked, or $j = f + 1$ and $j - 1 = f$ is marked. $\square$

**Lemma 4 (holes are free).** A hole found by line L6 holds no byte of a live object.

*Proof.* A line $j$ of a hole is not marked, and either $j$ is the first line of its block or line L6 found $j - 1$ not marked (for the first line of the hole) or $j - 1$ is itself an unmarked line of the hole (for the other lines). In every case neither $j$ nor $j - 1$ in the same block is marked, so by Lemma 3 no live byte lies in $j$. $\square$

**Lemma 5 (no byte is handed out twice in a cycle).** The mutator's region, the overflow region and the copy region are disjoint, and each allocation takes bytes that no earlier allocation of the cycle took.

*Proof.* A free block is taken from the free list by at most one of the three allocators, once. A recyclable block is taken from its list once, and within it line L6 finds the holes in increasing order of lines, starting after the end of the previous hole. Within a region the cursor only grows. Line marks do not change during a cycle after the sweep, so line L6 always sees the same holes. $\square$

**Theorem.** In every run, (1) after each collection the graph of objects reachable from the roots, by identity, is the same as before it, and (2) no allocation returns a byte of an object that is reachable at the time of the allocation.

*Proof.* (1) is Lemma 2. For (2), take an allocation in some cycle and a reachable object $x$ at that time. If $x$ was allocated in this cycle, its bytes are disjoint from the new bytes by Lemma 5. Otherwise $x$ was reachable at the end of the collection that started the cycle (no object becomes reachable again after it is unreachable, and objects do not move between collections), so it was marked there. Its bytes are not in any hole by Lemma 4, are not in a free block (a block with a live byte has a marked line by Lemma 3), and the copies of the previous collection are marked objects too. The new bytes come from a hole, a free block or an overflow block taken from the free list, so they miss $x$. $\blacksquare$

**Remark.** Lemma 4 is the only place where the skip of line L6 is used. Without it, a small live object whose first line is marked and whose tail is in the next line leaves that next line in a hole, and the page shows an allocation at address 128 inside a live object at $[64, 164)$.
