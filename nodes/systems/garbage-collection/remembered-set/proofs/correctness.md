---
title: The remembered set covers every old-to-young slot
proves: [correctness]
status: full
---

**Setting.** The heap has old and young objects. An *old-to-young slot* is a pair $(o, i)$ where $o$ is old and field $i$ of $o$ holds a young object. Let $E = H \cup B[0 \ldots top-1]$ be the set of entries. Say that $E$ *covers* $(o, i)$ when $(o, i) \in E$ with slot precision, or when $o \in E$ and $o$ has its remembered bit set with object precision.

**Claim.** Assume the two obligations of the users of the structure:

1. (barrier) after each mutator store that puts a young object into field $i$ of an old object $o$, RECORD$(o, i)$ runs;
2. (promotion) when the collector makes an object $p$ old, it calls RECORD$(p, i)$ for each field $i$ of $p$ that still holds a young object, before the next minor collection.

Also assume that RETAIN$(keep)$ is called with a predicate that holds for each entry that covers an old-to-young slot, and that FORGET$(D)$ is called only with old objects that are freed. Then invariant (I) holds between operations: $E$ covers every old-to-young slot. Further, ROOTS yields each old-to-young slot exactly once, and no other slot.

**Proof of (I).** By induction on the sequence of heap events and operations. At the start there are no objects, so (I) holds. Assume (I) before an event; we show it after the event.

*A store into field $i$ of $o$ of a value $v$.* Only the slot $(o, i)$ changes. If $o$ is young, or $v$ is not young, then $(o, i)$ is not old-to-young after the store, and the other slots keep their cover. Otherwise obligation 1 makes RECORD$(o, i)$ run. With slot precision, line L4 puts $(o, i)$ into $B$. With object precision, either the bit of $o$ was already set, and then $o \in E$ by (I) (the bit is set only at line L3, together with the append of line L4, and cleared only at line L11 together with the removal of $o$), or lines L3 and L4 set the bit and add $o$. In both cases $(o, i)$ is covered.

*DRAIN.* Lines L6 and L7 move each entry of $B$ into $H$ before $B$ is emptied. So $E$ after the drain equals $E$ before it, and the bits do not change.

*A minor collection that promotes a set $P$ of young objects and frees the young objects that are not reachable.* Consider a slot $(o, i)$ that is old-to-young after the collection. Either $o$ was old before, and field $i$ held a young object before too, because promotion turns young targets old and never turns old ones young, and the collection updates field $i$ to the new address of the same object. Then $(o, i)$ was covered before, and the collection removes no entry. Or $o \in P$, and obligation 2 calls RECORD$(o, i)$, which covers the slot as in the store case.

*RETAIN.* An entry is removed only if $keep$ is false for it. By assumption, such an entry covers no old-to-young slot. For object precision, line L11 clears the bit only of a removed object, which then has no young field. So each old-to-young slot keeps its cover.

*A major collection followed by FORGET$(D)$.* The objects of $D$ are freed, so no slot of theirs exists any more. The entries of other objects are not touched.

So (I) holds after each event. $\square$

**Proof of the claim on ROOTS.** Line L8 drains, so $E = H$. Line L9 visits each entry of $H$ once, because $H$ is a set. Line L10 yields a slot only if it is a field of an old object (each entry names an old object, since RECORD is called only for old objects, and FORGET removes the freed ones) and it holds a young object, so each yielded slot is old-to-young. With slot precision each entry gives at most the one slot it names, and distinct entries name distinct slots. With object precision each entry is an object, its fields are scanned once, and distinct objects have distinct slots. So no slot is yielded twice. Finally, by (I), each old-to-young slot $(o, i)$ is covered: either $(o, i) \in H$, and line L10 yields it, or $o \in H$, and the scan of the fields of $o$ yields it. $\blacksquare$
