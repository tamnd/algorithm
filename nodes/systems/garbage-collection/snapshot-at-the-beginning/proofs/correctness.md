---
title: Snapshot-at-the-beginning marks every object live at the start and every new object
proves: [correctness]
status: full
---

We use the model of the page. A *step* is one mutator operation with its barrier, or one MARK-STEP. Steps do not overlap. Let $t_0$ be the moment of line L8. The *snapshot* is the heap graph and the root set at $t_0$; $S$ is the set of objects reachable in it, and $N$ is the set of objects allocated after $t_0$. For an object $x$ that exists at $t_0$ and a field $f$, the *snapshot value* $x.f_0$ is the value of $x.f$ at $t_0$.

**Lemma 1.** Colors change only from white to gray (SHADE and line L3) and from gray to black (line L14). An object is gray exactly when it is on $W$, and it is on $W$ at most once. Hence each object is pushed at most once per cycle.

*Proof.* Line L8 makes all objects white and empties $W$. Each push turns a white object gray, and each pop at line L12 is followed by line L14, which makes the object black. Line L6 makes a new object black directly. No line turns an object white after line L8. $\square$

**Lemma 2.** Let $x$ exist at $t_0$, and let $x.f$ be overwritten at least once while marking is true. Then after the first such overwrite, $x.f_0$ is not white, or it is nil.

*Proof.* Between $t_0$ and the first overwrite during marking, nothing changes $x.f$: BEGIN-CYCLE does not change fields, and marking becomes true at line L10, before any mutator step of the cycle. So at line L2 of the first overwrite, $z = x.f_0$. Line L3 shades it if it is white. By Lemma 1 it never turns white again. $\square$

**Lemma 3.** When an object $x$ that exists at $t_0$ turns black at line L14, every snapshot value $x.f_0$ is nil or not white, and stays so.

*Proof.* Take a field $f$. If $x.f$ was never overwritten during marking before line L13 runs on $x$, then $x.f = x.f_0$ at that moment and line L13 shades it. Otherwise Lemma 2 applies. By Lemma 1 a non-white object stays non-white. $\square$

**Lemma 4.** An object that is unreachable from the roots at some moment stays unreachable at every later moment.

*Proof.* A mutator gets a reference only by loading a field of an object that it holds in a register, or by allocation, which makes a new object. A store writes into a field a reference that the mutator already holds. So by induction over the steps, every reference in a register or in a field of a reachable object names an object that was reachable before the step or is new. An unreachable object is not new, so it never enters a register or a reachable field again. $\square$

**Theorem.** When line L16 runs, every object of $S \cup N$ that has not been freed is black, and every object reachable from the roots at that moment is in $S \cup N$. So line L16 frees no reachable object.

*Proof.* At line L16, $W$ is empty, so by Lemma 1 there are no gray objects. Every object of $N$ is black by line L6, since marking is true for the whole cycle until line L15.

Now take $s \in S$. There is a path $r = s_0, s_1, \ldots, s_m = s$ in the snapshot, from a root $r$ at $t_0$, with $s_{i+1} = s_i.f_{i,0}$ for some fields. Line L9 shaded $r$, so $r$ is black now. Assume $s_i$ is black. By Lemma 3, $s_{i+1}$ is not white, and as there are no gray objects it is black. By induction $s$ is black.

Finally, let $y$ be reachable from the roots when line L16 runs. If $y$ is new, $y \in N$. Otherwise $y$ existed at $t_0$. If $y$ were not in $S$, it was unreachable at $t_0$, and by Lemma 4 it would be unreachable now. So $y \in S$. $\blacksquare$

**Corollary (floating garbage).** The objects that survive line L16 are exactly $S \cup N$: the sweep frees exactly the objects that were unreachable at $t_0$. So the floating garbage of the cycle is the set of objects of $S \cup N$ that are unreachable at the sweep.

*Proof.* By the theorem, every object of $S \cup N$ is black. We show by induction over the shades that every shaded object was reachable at some moment at or after $t_0$, and so lies in $S \cup N$ by Lemma 4. Line L9 shades roots at $t_0$. Line L3 shades the old value of a field of an object $x$ that the mutator holds in a register, so that value is reachable at that moment. Line L13 shades a field value $y$ of a shaded object $x$, which was reachable at some moment $t$; either $x.f = y$ already at $t$, so $y$ was reachable at $t$, or a later store wrote $y$ from a register. An object outside $S \cup N$ is therefore never shaded, stays white, and is freed. $\square$

**Comparison with incremental update.** Under the incremental update barrier with white allocation, every shaded object was reachable at some moment after $t_0$ (the proof of the incremental update page), so it is in $S \cup N$. Hence, if both collectors sweep at the same point of the same mutator program, so that they see the same heap graph, the survivors of the incremental update collector form a subset of $S \cup N$, which is the set of survivors of the snapshot collector, and its floating garbage is no larger.
