---
title: An incremental update barrier never lets the sweep free a reachable object
proves: [correctness]
status: full
---

We use the model of the page. A *step* is one mutator operation together with its barrier, or one MARK-STEP, or the whole FINAL-REMARK. Steps do not overlap. Colors are set only at line L7 (all white), by SHADE (white to gray, with a push on $W$), at line L6 (black to gray, with a push), and at line L13 (gray to black, after a pop).

**Lemma 1.** At the end of each step, an object is gray if and only if it is on $W$, and each gray object is on $W$ exactly once.

*Proof.* Line L7 empties $W$ and makes all objects white. A push happens only at SHADE or line L6, and each of them turns a non-gray object gray. A pop at line L11 is followed in the same step by line L13, which makes the popped object black. So the pushes and pops match the changes into and out of gray. $\square$

**Lemma 2 (strong invariant).** With either barrier, at the end of each step after line L9, no black object has a field that points to a white object.

*Proof.* By induction over the steps. After line L9 no object is black. Assume the invariant before a step.

- *MARK-STEP with $W$ not empty.* Line L12 shades every field of $x$, so after it no field of $x$ is white, and line L13 makes $x$ black. Shading only removes white objects, so no other black object gets a white target.
- *Load, clear.* They change only registers.
- *Allocate.* The new object is white and has nil fields. No field points to it, and it is not black.
- *Store with Dijkstra's barrier.* Line L1 sets $x.f = y$. If $y$ is nil or not white, no black-to-white field is created. Otherwise line L3 makes $y$ gray in the same step. Either way, every field that pointed to a non-white object still does, so the invariant holds after the step.
- *Store with Steele's barrier.* Line L4 sets $x.f = y$. If $x$ is not black, or $y$ is nil or not white, no black-to-white field is created. Otherwise line L6 makes $x$ gray, so $x$ is no longer black.
- *FINAL-REMARK.* Line L15 only shades, and line L16 repeats the mark step, which keeps the invariant by the first case. $\square$

**Theorem 1.** When FINAL-REMARK reaches line L18, every object that is reachable from the roots is black. So line L18 frees no reachable object.

*Proof.* The mutator is stopped during FINAL-REMARK, so the heap and the roots do not change in it. After line L15 every root is gray or black. Line L16 runs until $W$ is empty, and each round removes one object from $W$; it ends because, while the mutator is stopped, each push turns a white object gray (Dijkstra and the mark step) and there are finitely many white objects. By Lemma 1 no object is gray at the end. So every root is black. Let $B$ be the set of black objects. By Lemma 2 a field of a black object points to a black object, since its target is not white and not gray. So $B$ contains the roots and is closed under fields, and therefore it contains every reachable object. Line L18 frees only white objects. $\blacksquare$

**Lemma 3.** Every object that becomes gray during a cycle was reachable from the roots at some moment at or after line L7.

*Proof.* By induction over the order in which objects become gray. Line L8 and line L15 shade roots, which are reachable at that moment. Line L3 shades $y$, which the mutator holds in a register at that moment. Line L6 grays $x$, which is in a register. Line L12 shades a field $y$ of a gray object $x$. By induction $x$ was reachable at some moment $t$. If $x.f = y$ already at $t$, then $y$ was reachable at $t$. Otherwise the field was set to $y$ by a store after $t$, and the mutator held $y$ in a register at that store. $\square$

**Theorem 2.** Every object that is unreachable when line L7 runs is freed at line L18 of the same cycle.

*Proof.* The mutator obtains new references only by loads from objects that it holds and by allocation, so an object that is unreachable at a moment stays unreachable afterward. By Lemma 3 such an object never becomes gray, so it is never black, so it is white at line L18 and is freed. $\blacksquare$

**The order of the store and the shade.** The proofs use that the store and the shade happen in one step. If a concurrent marker can run between them, Lemma 2 needs the order of lines L1 to L3: after the store and before the shade, the edge $x \to y$ exists and $y$ may be white, but $y$ is held in a register, which FINAL-REMARK rescans, so it is not lost in this cycle. With the opposite order, a whole cycle can run between the shade and the store; the next cycle starts with $y$ white, and the store then creates a black-to-white field with no shade.
