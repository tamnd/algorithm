---
title: The Shenandoah model installs one copy per object, loses no write, and leaves no pointer into a freed region
proves: [correctness]
status: full
---

We use the heap model and the procedures of the page, in either mode. Each step of a thread between two yields is atomic, and a pause is one step taken when every mutator is between operations. Objects are named by identity; a copy has the identity of its original. $\textit{CS}$ is the collection set, nonempty only from line L13 to line L16. An object is *live* in a cycle if it is marked or was allocated in that cycle.

**Lemma 1 (one copy).** The forwarding pointer of an object is set at most once in a cycle, and its target is a copy with the same identity, outside $\textit{CS}$.

*Proof.* It is set only at line L3, and only if it is empty, in the same atomic step as the test. The copy of line L2 goes to a region taken from the free regions after line L13 chose $\textit{CS}$, so it is outside $\textit{CS}$. Between line L2 and line L3 no write reaches $a$: a write to an object of $\textit{CS}$ is made, by Lemma 2, only before any copy of it exists, and line L2 is such a copy. So the installed copy has the fields of $a$ at the time of the install. $\square$

**Lemma 2 (no write to an old copy).** From line L13 to line L16, no store writes a field of an object of $\textit{CS}$.

*Proof.* *Load reference barrier.* Line L13 replaces every root in $\textit{CS}$ by a copy. After it, a register gets a new object (outside $\textit{CS}$), another register, or the result of line L7; line L6 replaces a loaded pointer into $\textit{CS}$ by $\textit{EVACUATE}$ of it, outside $\textit{CS}$ by Lemma 1. So no register points into $\textit{CS}$, and a store writes through a register. *Brooks mode.* Line L9 replaces a target in $\textit{CS}$ by the result of $\textit{EVACUATE}$, outside $\textit{CS}$, before the write at line L10, in the same thread with no pause in between. $\square$

So, by Lemmas 1 and 2, the copy installed for $a$ is the only object of its identity that is ever written after the install, and every read of it goes to the copy: with the load reference barrier because registers do not point into $\textit{CS}$, in Brooks mode because line L5 reads through $\textit{fwd}$.

**Lemma 3 (marking).** At line L13, every object reachable from the roots is live.

*Proof.* This is the argument of [snapshot-at-the-beginning](/snapshot-at-the-beginning/). Line L11 marks the roots of the snapshot. An object reachable at the end of marking that existed at its start was reachable at its start (no step makes an old unreachable object reachable), so a path from a snapshot root reaches it; each pointer of that path is still in place, or was overwritten by a store that logged it at line L8. Line L12 and the drain at line L13 follow every logged pointer and every field of every marked object. An object allocated during marking is live by definition. $\square$

**Lemma 4 (evacuation is complete).** When line L14 ends, every live object in $\textit{CS}$ has a forwarding pointer.

*Proof.* Regions allocated in this cycle are not chosen, so the live objects of $\textit{CS}$ are its marked objects, and line L14 calls $\textit{EVACUATE}$ on each one that has no forwarding pointer. $\square$

**Lemma 5 (update of references).** When line L16 frees $\textit{CS}$, no root and no field of a live object outside $\textit{CS}$ points into $\textit{CS}$.

*Proof.* Line L16 replaces every root in $\textit{CS}$ by its forwarding pointer, which exists by Lemmas 3 and 4. For fields: line L15 visits every live object outside $\textit{CS}$ that exists when it starts, and replaces each field into $\textit{CS}$ by its forwarding pointer, in one atomic step per object. A field changes after its visit only by a store or a heal. A heal writes a pointer outside $\textit{CS}$. A store writes a register value: with the load reference barrier it is outside $\textit{CS}$ by Lemma 2; in Brooks mode line L9 replaces it by $\textit{fwd}$, which is outside $\textit{CS}$ since every live object there is forwarded by Lemma 4. Objects allocated during line L15 get only such values. The copies themselves are outside $\textit{CS}$ and are new in this cycle, so line L15 visits them too. $\square$

**Theorem.** In every run of the model with the barriers, the graph of objects reachable from the registers, by identity, is the same after every step as in a run of the same operations with no collector; with the load reference barrier, no register points into $\textit{CS}$ between line L13 and line L16.

*Proof.* A load returns a pointer to the object that the field names by identity (Lemma 1, and $\textit{fwd}$ for Brooks reads). A store writes into the current copy (Lemma 2). The collector changes fields and roots only to the forwarding pointer of their target, the same identity. Line L13 frees only regions with no live object, which by Lemma 3 hold nothing reachable, and line L16 frees $\textit{CS}$ only when nothing reachable points into it (Lemma 5). The second part is the first paragraph of the proof of Lemma 2. $\blacksquare$
