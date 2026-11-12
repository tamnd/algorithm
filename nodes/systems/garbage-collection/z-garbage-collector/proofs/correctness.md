---
title: The ZGC model keeps the to-space invariant, gives each moved object one copy, and frees no reachable object
proves: [correctness]
status: full
---

We use the heap model and the procedures of the page. Each step of a thread between two yields is atomic. A pause runs only when every mutator is between operations. Objects are named by identity; a copy has the identity of its original. We write $\textit{fw}(a)$ for the entry of $a$ in the current or the previous forwarding table, and $\textit{remap}(a)$ for $\textit{fw}(a)$ if it exists and $a$ otherwise. A pointer is *good* if its color is the good color.

**Invariant F.** (a) Each forwarding entry is written once and never changed until its table is dropped. (b) If $\textit{fw}(a) = b$, then the object at $b$ has the identity of the object at $a$, and $b$ is on a page outside the relocation set. (c) An entry is dropped only at line L13.

*Proof.* Entries are written at line L8, line L17 and in the relocate-start pause. Each of them first checks, in the same atomic step, that $\textit{remap}(a) = a$, so it writes only an empty entry; this is the compare-and-swap. The copy $b$ was made from $a$ in an earlier step, and nothing writes the fields of an object on a page of the relocation set during relocation (a store writes through a good register, which by Lemma 1 does not point there), so the copy still equals $a$. Copies go to pages taken from the free pages after the relocation set was chosen, so they are outside it. $\square$

**Lemma 1 (to-space invariant).** At every step, during relocation every register holds nil or a good pointer to a page that is allocating or used; at all times every register holds nil or a good pointer whose address holds an object.

*Proof.* By induction on the steps. A pause of line L10 or line L15 replaces each register by $\textit{remap}$ of its address with the good color; at line L15 the object is first moved if its page is in the relocation set, so the new address is outside it. Between pauses the good color does not change. A mutator step sets a register to a new object (good color, a page being allocated), to the value of another register (by induction), or to the value of line L3. At line L3, either the loaded value $v$ had a good color, or it is the result of line L9.

*A good value in a field.* During marking, the good color is a marked color that was not used in the last cycle, so a field holds it only if it was written in this cycle by line L12, line L9 or a store; in each case the value was $\textit{remap}$ of an address, or a register value, and so points to a live object outside any released page. During relocation, the good color is Remapped. A field with color Remapped was written either in this relocation (lines L9 and L17 write a forwarded address; a store writes a good register) or before the last marking. Every field of a marked object that was not good in the marking was rewritten by line L12 with the marked color; so a field of a live object with color Remapped at relocation was written after relocate start, and points outside the relocation set.

*A bad value.* Line L4 remaps. Line L6 checks the page of the remapped address; if it is in the relocation set, lines L7 and L8 make sure that $\textit{fw}(a)$ exists, and $a$ becomes $\textit{fw}(a)$, outside the relocation set by F(b). Line L8 looks in both tables, so the entry is found even when the collector has finished the relocation meanwhile. Line L9 returns $a$ with the good color. $\square$

**Lemma 2 (one copy).** For each moved object, all pointers to it that any thread uses after the move lead to the same copy.

*Proof.* Every use goes through $\textit{remap}$ (lines L4, L12, the pauses) or through a value written after a remap. By F(a) the entry is written once, so every remap of $a$ gives the same $b$. A thread that loses at line L8 or line L17 does not use its own copy. $\square$

**Lemma 3 (marking is complete).** When the mark-end pause finds the mark stack empty, every object reachable from the registers is marked or was allocated in this cycle.

*Proof.* Call an object *safe* if it is marked or new in this cycle. We show that at mark end, the registers point to safe objects and every field of a safe object points to a safe object, so the reachable objects are safe.

Registers: at line L10 every register target is marked. Later, a register gets a new object, the value of another register, or a loaded value. A loaded value with the good marked color was written in this marking, from a safe target (as in Lemma 1). A loaded value with a bad color is marked at line L5. So registers point to safe objects.

Fields: a marked object was pushed when it was marked and is popped before the stack is empty. When it is popped, line L12 marks the target of each field with a bad color; a field with the good color already points to a safe object. After that, each field changes only by a store of a register value (safe) or by a heal (lines L9 and L12, safe targets). A new object starts with nil fields and gets only register values. So every field of a safe object points to a safe object. $\square$

**Lemma 4 (no reachable object is freed, and no released memory is used).** Line L14 frees only pages with no marked object and not allocated in this cycle, so by Lemma 3 they hold no reachable object. A page released at line L18 has a forwarding entry for each of its marked objects. Its memory is reused only at the next line L13, after a full marking. In that marking every field of every reachable object has a bad color (Remapped) or was written in this marking, so line L12 or line L4 rewrites it with $\textit{remap}$; after mark end no reachable field points into a released page, and dropping the tables is safe. $\square$

**Theorem.** In every run of the model with the load barrier, every register satisfies the to-space invariant after every step, and the graph of objects reachable from the registers, by identity, is the same as in a run of the same operations with no collector.

*Proof.* Lemma 1 gives the invariant. A load returns $\textit{remap}$ of the value in the field, which by F(b) and Lemma 2 is the same object by identity. Stores write register values, so the graph changes as in the run with no collector. The collector changes fields only by writing $\textit{remap}$ of their address, which names the same object, and frees only unreachable memory (Lemma 4). $\blacksquare$

**Remark.** The proof uses the load barrier at three places: the bad color test at line L2, the remap at line L4, and the move at lines L6 to L8. Without it, a register may get a pointer into a page of the relocation set, which the tests detect in every one of their 40 seeded runs.
