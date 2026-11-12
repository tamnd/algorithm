---
title: The C4 model keeps mutators on good pointers, gives each moved object one copy, and frees no reachable object
proves: [correctness]
status: full
---

We use the heap model and the procedures of the page. Each step of a thread between two yields is atomic, and a checkpoint is one step taken when every mutator is between operations. Objects are named by identity; a copy has the identity of its original. We write $\textit{fw}(a)$ for the forwarding entry of $a$, and $\textit{remap}(a)$ for $\textit{fw}(a)$ if it exists and $a$ otherwise. A pointer $v$ is *good* if $\textit{nmt}(v) = e$ and the page of $v$ is not protected.

**Invariant F.** (a) Each forwarding entry is written once and is not changed until line L13 drops it. (b) If $\textit{fw}(a) = b$, then the object at $b$ has the identity of the object at $a$, and the page of $b$ is not protected. (c) A page that is protected and released has an entry for each of its marked objects.

*Proof.* Entries are written at line L6, line L16 and in the checkpoint of line L15, each time only if the entry is empty, in the same atomic step as the test; this is the compare-and-swap. The copy was made from $a$ in an earlier step. Between the copy and the install, nothing writes a field of $a$: a store writes through a register, and by Lemma 1 a register does not point into a protected page. So the copy equals $a$. Copies go to pages taken from the free pages after line L14, which are not protected. Line L17 releases a page only after line L16 has given an entry to each marked object on it. $\square$

**Lemma 1 (good registers).** After every step, every register holds nil or a good pointer whose address holds an object.

*Proof.* By induction on the steps. The checkpoint of line L10 sets each register to $\textit{remap}$ of its address with NMT bit $e$; no page is protected then except released pages, and $\textit{remap}$ leads out of them by F(c). The checkpoint of line L15 copies the object of each register that points into a newly protected page and sets the register to the copy, which is good by F(b). Between checkpoints, $e$ does not change and pages only become protected at line L15. A mutator step sets a register to a new object (NMT bit $e$, a page being allocated), to another register, or to the value of line L3. At line L3 the value is either good at line L2, or comes from line L9, which returns $a$ with NMT bit $e$, where $a$ is outside any protected page: if the page of the loaded address is protected, lines L6 and L7 replace it by $\textit{fw}(a)$, outside by F(b). $\square$

**Lemma 2 (one copy).** For each moved object, every pointer that any thread uses after the move leads to the same copy.

*Proof.* A pointer into a protected page is used only after line L7, line L12 or a checkpoint has replaced it by $\textit{remap}$. By F(a) the entry is written once. A thread that loses the compare-and-swap at line L6 or line L16 uses the entry, not its own copy. $\square$

**Lemma 3 (marking is complete).** When the checkpoint after line L12 finds the mark stack empty, every object reachable from the registers is marked or was allocated in this cycle.

*Proof.* Call an object *safe* if it is marked or new in this cycle. Registers: at line L10 every register target is marked. Afterwards a register gets a new object, another register, or a loaded value. A loaded value with NMT bit $e$ was written in this marking from a safe target, since every pointer written in this cycle came from a register, from line L9 or from line L12. A loaded value with the other NMT bit is marked at line L8. So registers point to safe objects.

Fields: a marked object is pushed when it is marked, and the stack is empty, so it was popped. Line L12 then marked the target of each field that was not good and rewrote it with bit $e$; a field that was good already had a safe target. After that, a field changes only by a store of a register value or by a heal of lines L9 or L12, all with safe targets. A new object starts with nil fields and gets only register values. So the safe objects are closed under the fields and contain the targets of the registers, and every reachable object is safe. $\square$

**Lemma 4 (frees and reuse).** Line L14 frees only pages that hold no marked object and were not taken in this cycle; by Lemma 3 they hold no reachable object. Line L13 unprotects and frees a released page only after a full marking. In that marking every field of every reachable object either was written in this marking from a remapped value, or had the old NMT bit and was rewritten by line L12 or line L9 with $\textit{remap}$ of its address. So after mark end no reachable field points into a released page, and dropping the forwarding data loses nothing. $\square$

**Theorem.** In every run of the model with the barrier, after every step every register holds a good pointer, and the graph of objects reachable from the registers, by identity, is the same as in a run of the same operations with no collector.

*Proof.* Lemma 1 gives the first part. A load returns $\textit{remap}$ of the field's address, the same object by identity by F(b) and Lemma 2. Stores write register values, so they change the graph as with no collector. The collector changes fields only to $\textit{remap}$ of their address, and frees only unreachable memory by Lemma 4. $\blacksquare$

**Remark.** The model takes each checkpoint for all threads at once. In C4 the threads pass a checkpoint one by one, so a thread that has not passed the flip yet may hold pointers with the old NMT bit while other threads already expect the new one. The real collector handles this window; the model does not, and the proof above does not cover it.
