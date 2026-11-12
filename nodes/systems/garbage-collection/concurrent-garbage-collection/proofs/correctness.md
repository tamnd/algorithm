---
title: Mostly concurrent mark-sweep with a card barrier never frees a reachable cell
proves: [correctness]
status: full
---

We use the heap model and the template of the page. Steps are atomic: each mutator operation with its barrier (lines L13 and L14), and each collector step (lines L2 and L3, lines L4 and L5, one cell of the sweep). INITIAL-MARK and REMARK run with the mutator stopped. Call a cell *black* if it is marked and not on $W$, *gray* if it is on $W$, and *white* if it is not marked. A cell is marked exactly when it is black or gray.

**Lemma 1 (the card invariant).** From line L1 until line L9, at the end of every step: if a black cell $x$ has a field that points to a white cell, then the card of $x$ is dirty.

*Proof.* At line L1 no cell is black, since every marked cell is a root that was just pushed. We check each step that can create a black cell with a white child, or clean a card.

- Lines L2 and L3 make $x$ black and shade every field of $x$, so $x$ has no white child after the step.
- A store $x.f \leftarrow y$ (line L13) is followed in the same step by line L14, which dirties the card of $x$.
- Line L4 cleans card $c$, and line L5 then shades every field of every marked cell on $c$, so after the step no black cell on $c$ has a white child. The step is atomic, so no store comes between them.
- SHADE only turns white cells gray, which removes white children and makes no cell black.
- A load into a register, a register clear, and an allocation (which marks the new cell during marking, and gives it nil fields) change no field of a black cell into a white pointer. $\square$

**Lemma 2 (the remark).** When line L9 runs, every cell reachable from the registers is marked.

*Proof.* The mutator is stopped during REMARK. After line L6 every root is marked. Line L7 cleans every dirty card and rescans its marked cells, so by Lemma 1 no black cell has a white child after it. Line L8 then pops every gray cell and shades its fields; this keeps the property that no black cell has a white child, and ends with no gray cell. So the marked set contains the roots and is closed under the fields: it contains every reachable cell. $\square$

**Lemma 3 (allocation).** A cell allocated after line L1 and before the sweep reaches its address is marked when the sweep reaches it.

*Proof.* Line L16 marks a cell allocated during the mark or preclean phase, and a cell allocated during the sweep at an address $x \ge s$. Marks are cleared only by line L10, at the sweep pointer. $\square$

**Theorem.** The sweep never frees a cell that is reachable at any later moment.

*Proof.* Line L11 frees a cell $s$ only if it is unmarked when the sweep reaches it. By Lemma 3 it was not allocated during the cycle. So it existed at line L9, and since it is unmarked, by Lemma 2 it was unreachable then. Between line L9 and its sweep, the mutator gets new references only by loading fields of cells that it reaches, or by allocation; so an unreachable cell that existed at line L9 stays unreachable. A freed cell is reachable again only after it is allocated anew, which is a new cell. $\blacksquare$

**The fallback.** Line L15 runs the remaining steps of the cycle with the mutator stopped. Lemma 1 to Lemma 3 hold for any interleaving, including one in which the mutator does not run, so the theorem covers the fallback too.

**What the proof uses about atomicity.** Lemma 1 needs two orders inside a step: the store comes before the card is dirtied (line L13 before line L14), and the card is cleaned before the rescan (line L4 before line L5). If either step is split and the order is reversed, there is an interleaving that breaks Lemma 1. On real hardware the collector must also see the store when it sees the dirty card, which needs the right memory fences.
