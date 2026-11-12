---
title: The synchronous trial deletion collector frees exactly the garbage
proves: [correctness]
status: full
---

**Setting.** The heap holds a root record $\rho$, whose fields are the roots; it is never freed, never a child of an object, and never in Roots. An unfreed object $x \ne \rho$ is a *zombie* if $\mathrm{rc}(x) = 0$; by line L6 it is then buffered and black, and its children were already decremented at line L4. Let $A$ be the set of unfreed objects that are not zombies, $\rho$ included. An object is *reachable* if a path of fields leads to it from $\rho$. The mutator writes only into reachable objects, stores only null or reachable values, and does not run during COLLECT-CYCLES. Each new object is stored right after NEW.

For $x \in A$, let $\mathrm{in}(x)$ be the number of pairs $(y, j)$ with $y \in A$ and $y[j] = x$.

**Invariants between operations of the mutator.**

- **(R1)** $\mathrm{rc}(x) = \mathrm{in}(x) \ge 1$ for each $x \in A \setminus \{\rho\}$.
- **(R2)** $\mathrm{buffered}(x)$ holds exactly for the objects in Roots, and each is there once. Each zombie is in Roots. Each purple object is buffered.
- **(R3)** No object is gray or white.
- **(Q)** Each unreachable object of $A$ is reached, by a path inside $A$, from a purple object.

**Lemma 1.** A write keeps (R1) to (Q).

*Proof.* (R1) is the invariant of [reference counting](/reference-counting/), with zombies treated as freed: when a count drops to 0 at line L2, line L4 decrements all children, so the object's fields stop counting, and line L6 frees it unless it is buffered. A count that drops to a nonzero value stays at least 1. (R2): line L10 appends only an unbuffered object and sets its flag; a zombie is buffered, so it is in Roots; line L9 makes an object purple only together with line L10, unless it is already buffered. (R3): a write uses only black and purple.

(Q): An object of $A$ that was reachable and becomes unreachable did so because the write removed an edge $p \to z$ on all paths to it. So it was reached from $z$ by a path $z = y_0 \to y_1 \to \cdots \to y_k$. Let $y_m$ be the last object on this path that the write releases (count 0 at line L3); if there is none, set $m = -1$ and treat the decrement of $z$ as the last one. The object $y_{m+1}$ had its count decremented by this write and did not drop to 0, so line L7 made it purple. The objects after it are not released, so the path from $y_{m+1}$ to $y_k$ lies in $A$. For an object that was already unreachable, take its path from a purple object $q$, given by (Q) before the write. If this write releases an object of the path, the same argument gives a later purple object on it. An unreachable object never gets a new reference, so INCREMENT never turns it black, and a purple object stays purple until the next collection. $\square$

We now follow one run of COLLECT-CYCLES.

**Lemma 2 (MARK-ROOTS).** After line L17, there are no zombies, and the gray objects are exactly the set $G$ of objects that a path inside $A$ reaches from the purple objects that were in Roots. For each $x \in G$,

$$\mathrm{rc}(x) = \mathrm{in}(x) - |\{(y, j) : y \in G, \ y[j] = x\}| = \mathrm{ext}(x),$$

the number of references to $x$ from $\rho$ and from objects of $A \setminus G$. The counts of objects outside $G$ do not change.

*Proof.* A zombie is black with count 0, so line L15 frees it. Its fields were already uncounted, so this changes no $\mathrm{in}$. MARK-GRAY never reaches a zombie, because a child of an object of $A$ has $\mathrm{in} \ge 1$ and so is not a zombie. A purple object in Roots is either still purple when line L12 tests it, and then MARK-GRAY starts there, or a gray object, which an earlier call of MARK-GRAY reached. So the gray set is $G$. Line L23 colors each object gray once, and only then do lines L24 and L25 subtract 1 from the target of each of its fields. So each reference whose source is in $G$ is subtracted exactly once, and no other count changes. $\rho \notin G$, since no field refers to $\rho$. $\square$

Call $x \in G$ *externally held* if a path inside $G$ leads to $x$ from some $y \in G$ with $\mathrm{ext}(y) > 0$. Let $H$ be the set of these objects.

**Lemma 3 (SCAN).** After SCAN-ROOTS, every object of $G$ is black or white, the black objects of $G$ are exactly $H$, and

- for $x \in H$, $\mathrm{rc}(x) = \mathrm{in}(x) - |\{(y, j) : y \in G \setminus H, \ y[j] = x\}|$;
- for $x \in G \setminus H$, $\mathrm{rc}(x) = 0$, and no field of an object of $H$ refers to $x$.

*Proof.* SCAN-BLACK colors an object black and then, at lines L33 to L35, adds 1 to each child and calls itself on each child that is not black. So each object that SCAN-BLACK colors black has the counts of all its fields added back exactly once, and all its children end up black. During this phase, black objects are made only by SCAN-BLACK. Hence (a) the set of black objects is closed under the edges, and (b) for each $x \in G$, $\mathrm{rc}(x) = \mathrm{ext}(x) + (\text{the number of references to } x \text{ from black objects of } G)$ at each moment.

Every object of $G$ is visited by SCAN or SCAN-BLACK: SCAN starts at each candidate, follows the children of each object that it colors white, and stops only at objects that are white or black already; SCAN-BLACK covers everything below the objects where it starts. So no gray object remains.

*Black objects are in $H$.* Order the black objects by the time they turn black. Assume all earlier ones are in $H$. If $x$ turns black inside a SCAN-BLACK call from its parent, the parent is black and earlier, so it is in $H$, and $x$ is a child of it, so $x \in H$. Otherwise line L29 calls SCAN-BLACK$(x)$ because $\mathrm{rc}(x) > 0$. By (b), $\mathrm{ext}(x) > 0$, so $x \in H$, or an earlier black object refers to $x$, so $x \in H$.

*Objects of $H$ are black.* If $\mathrm{ext}(y) > 0$, then $\mathrm{rc}(y) > 0$ when SCAN or SCAN-BLACK first visits $y$, since counts only grow in this phase, so $y$ turns black. By (a), everything that $y$ reaches is black.

The counts follow from (b): a black object of $H$ has back the references from all black objects, and has lost those from white ones. A white object has $\mathrm{ext}(x) = 0$, because $x \notin H$, and no black object refers to it, by (a). $\square$

**Theorem 1 (safety).** COLLECT-ROOTS frees only unreachable objects, and after it, (R1) to (R3) hold and Roots is empty.

*Proof.* Each object $x \in G \setminus H$ is unreachable. Indeed, take a path from $\rho$ to $x$. The path cannot start in $G$, so let $y$ be its first object in $G$. Its predecessor is $\rho$ or an object of $A \setminus G$, so $\mathrm{ext}(y) > 0$. Since $G$ is closed under the edges of $A$, the rest of the path lies in $G$, so $x \in H$. This contradicts $x \notin H$.

COLLECT-WHITE frees only white objects, which are in $G \setminus H$. It frees all of them: a white object $w$ is reached from a candidate $p$ by a path inside $G$, and every object on that path is white, because a black object on it would make $w$ black by (a). COLLECT-WHITE follows white objects, and it stops only at a buffered one, which is a candidate whose own call at line L21 comes later and continues from there. Line L20 clears its flag first, and line L37 turns each object black before its children, so no object is freed twice.

After the frees, consider $x \in H$. By Lemma 3, its count no longer includes the references from the freed white objects, and it includes all others, so $\mathrm{rc}(x) = \mathrm{in}(x)$ in the new heap. Objects outside $G$ are not referred to by white objects, since white objects lie in $G$ and $G$ is closed under the edges, so their counts are also exact. An object of $H$ has a positive count because $\mathrm{ext} > 0$ or a black object refers to it. All remaining objects are black, and lines L14 and L20 cleared every flag while Roots was emptied. $\blacksquare$

**Theorem 2 (completeness).** After COLLECT-CYCLES, the unfreed objects are exactly the reachable objects.

*Proof.* By Theorem 1, no reachable object is freed. Let $x \in A$ be unreachable at the start of the collection. By (Q), a purple object reaches $x$ inside $A$. That purple object is buffered by (R2), and it is not a zombie because it is in $A$, so $x \in G$ by Lemma 2. Every unreachable object of $A$ is in $G$. Now let $y \in G$ have $\mathrm{ext}(y) > 0$. Then $\rho$ or an object of $A \setminus G$ refers to $y$; that object is reachable, so $y$ is reachable, and so is everything that $y$ reaches. So every object of $H$ is reachable, and the unreachable objects of $G$ are exactly $G \setminus H$, which Theorem 1 shows are all freed. The zombies were freed in MARK-ROOTS. $\blacksquare$

After the collection, the set of unreachable objects of $A$ is empty, so (Q) holds again, and Lemma 1 keeps it until the next collection.
