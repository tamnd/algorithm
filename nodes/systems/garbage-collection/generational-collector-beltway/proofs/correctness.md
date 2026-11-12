---
title: Beltway frees only garbage, and X.X.100 frees all of it
proves: [correctness]
status: full
---

**Setting.** The heap is a list of belts $0, \ldots, B$, each a sequence of increments. An increment $I$ has the key $\kappa(I) = (\text{belt}, n)$, where $n$ is a counter that grows each time an increment is made. Keys never change, and keys are compared in lexicographic order. Every increment holds at least one object: increments are made only to receive an object, and objects leave an increment only when it is collected and freed. A slot $(s, i)$ is *backward* if $s.f_i$ lies in an increment other than that of $s$, with a smaller key.

**Invariant (R).** Between collections, every backward slot is in the remembered set of the increment of its target.

*Proof.* At the start the heap is empty. A store runs RECORD (line L11), which adds the slot if it is backward (line L12). Allocation makes an object with empty fields. Now take a collection of $c$. Only objects of $c$ move, so a slot can change its status only if its source or its target moved. Line L6 runs RECORD on every field of every copied object. A slot $(p, i)$ that points to a copied object, with $p$ outside $c$, had its target in $c$, the increment with the smallest key, so it was backward and in the remembered set of $c$ by (R); line L7 runs RECORD on it again. A slot with $p$ in $c$ either has $p$ copied, which line L6 covers, or has $p$ freed. Keys of other increments do not change, so all other slots keep their status and their entries. $\square$

**Safety.** No reachable object is freed by a collection.

*Proof.* Line L1 picks $c$ with the smallest key among the nonempty increments. Let $z \in c$ be reachable by a path $r, y_1, \ldots, y_m = z$ from a root $r$. We show by induction on $j$ that each $y_j$ in $c$ is copied before line L8. If $j = 1$, a root points to $y_1$, and line L3 copies it. Otherwise let $p = y_{j-1}$. If $p$ is outside $c$, its increment has a larger key than $c$, so the slot from $p$ to $y_j$ is backward, in the remembered set of $c$ by (R), and line L3 copies $y_j$. If $p$ is in $c$, it is copied by the induction hypothesis, and the scan of lines L4 and L5 reaches every copied object, including those copied during the scan, so line L5 copies $y_j$. Line L9 copies each object at most once. So every reachable object of $c$ leaves $c$ before line L8. Copying keeps the identity and the fields of an object, so the graph of reachable objects is unchanged. $\square$

**No dangling slots.** A slot of a surviving object never points to a freed object: a slot into $c$ from outside $c$ is remembered, so line L3 copies its target, and a slot from a copied object into $c$ is handled by line L5.

**Completeness of Beltway X.X.100.** Let the top belt $B = 2$ have increments of the whole usable memory $U$. Assume that the mutator stops allocating and storing, and that collections keep running. Then after finitely many collections the heap holds only reachable objects.

*Proof.* First, belt $B$ has at most one increment between collections. It starts empty. Survivors of belt $B - 1$ go to its youngest increment, which has room, because the whole heap holds at most $U$ objects; so a new increment on belt $B$ is made only when it has none. A collection of belt $B$ copies into a new increment and frees the old one.

Let $\Phi = \sum_x (B - \text{belt}(x))$ over all objects $x$. A collection of an increment on a belt $b < B$ removes all objects of that increment from belt $b$: each is freed or copied to belt $b + 1$. Since the increment is not empty, $\Phi$ falls by at least one. No collection raises $\Phi$, because objects only move up, and the mutator adds nothing. So after finitely many collections the belts below $B$ are empty.

Then line L1 picks the single increment $c$ of belt $B$, which holds every object of the heap. Every reference into $c$ is a root or a slot inside $c$, so lines L3 to L5 copy exactly the objects reachable from the roots, and line L8 frees every other object. From then on each collection is a full copying collection that keeps only reachable objects. $\blacksquare$

The same argument holds for BSS and BA2, whose top belt also has increments of $U$. It fails for Beltway X.X with $X < 100$: there, a ring of objects that does not fit in one increment always has an object whose predecessor lies in a later increment, so the oldest increment that holds part of the ring always has a remembered slot into it, and that part survives. The tests show such a ring that lives forever under X.X and is freed in three collections under X.X.100.
