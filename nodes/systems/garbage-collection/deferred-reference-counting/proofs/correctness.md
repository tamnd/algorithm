---
title: Deferred reference counting frees only unreachable objects
proves: [correctness]
status: full
---

Let $U$ be the set of unfreed heap objects and $r_1, \ldots, r_m$ the roots. For $y \in U$, let $h(y)$ be the number of pairs $(x, j)$ with $x \in U$ and $x[j] = y$, and let $g(y)$ be the number of roots $r_i$ with $r_i = y$. An object is *reachable* if a path of fields leads to it from an object that a root refers to. The mutator writes only into reachable objects, stores only null or reachable values, and does not run during COLLECT.

**Invariants between operations.**

- **(I1)** $\mathrm{rc}(y) = h(y)$ for each $y \in U$.
- **(I2)** Each $y \in U$ with $\mathrm{rc}(y) = 0$ is in the ZCT.

**Lemma 1.** NEW, WRITE-ROOT and WRITE keep (I1) and (I2).

*Proof.* NEW adds an object with no fields set, so no $h$ changes. The new object has $h = 0 = \mathrm{rc}$, and line L2 puts it in the ZCT. WRITE-ROOT changes only $g$, which (I1) and (I2) do not mention. In WRITE$(p, i, y)$ with old value $z$, line L6 moves the field $p[i]$ from the referrers of $z$ to those of $y$. Line L5 adds 1 to $\mathrm{rc}(y)$ and line L8 subtracts 1 from $\mathrm{rc}(z)$, so (I1) holds after line L7 (if $y = z$, both changes cancel). Only $\mathrm{rc}(z)$ decreased, and if it is now 0, line L9 adds $z$ to the ZCT, so (I2) holds. $\square$

**Lemma 2.** During the loop of COLLECT, each time line L11 tests the ZCT:

- **(J1)** $\mathrm{rc}(y) = h(y) + g(y)$ for each $y \in U$;
- **(J2)** each $y \in U$ with $\mathrm{rc}(y) = 0$ is in the ZCT.

*Proof.* Before line L10, (I1) and (I2) hold. Line L10 adds $g(y)$ to each count, so (J1) holds at the first test. Counts only grew, so each object with count 0 had count 0 before, and (I2) gives (J2).

In one turn, line L12 removes $x$. If $\mathrm{rc}(x) > 0$, nothing else changes, and $x$ does not need to be in the ZCT. If $\mathrm{rc}(x) = 0$, then $h(x) = g(x) = 0$ by (J1): no field of an object of $U$ and no root refers to $x$, not even a field of $x$ itself. Each child $c = x[j]$ has $\mathrm{rc}(c) \ge 1$ because of this field, and line L14 subtracts 1 for each field of $x$ that refers to $c$. Line L15 removes $x$ and with it exactly these referrers from $U$, so (J1) holds again. A count that drops to 0 in line L14 is added to the ZCT by line L9, so (J2) holds. $\square$

The loop ends: each turn removes one entry, and entries are added only when a count drops to 0 at line L14, which happens at most once for each field of a freed object, and $U$ is finite.

**Theorem 1 (safety).** COLLECT frees no reachable object.

*Proof.* Assume that line L15 frees a reachable object, and take the first time it does so. Take a path to the object $x$ from a root object, $x_0 \to \cdots \to x_k = x$. All $x_t$ are reachable, so they are still in $U$. If $k = 0$, a root refers to $x$ and $g(x) \ge 1$. If $k \ge 1$, the field of $x_{k-1}$ gives $h(x) \ge 1$. In both cases (J1) gives $\mathrm{rc}(x) \ge 1$, but line L13 tested $\mathrm{rc}(x) = 0$. This is a contradiction. $\blacksquare$

**Theorem 2 (the state after a collection).** After COLLECT, (I1) and (I2) hold. Moreover:

1. the ZCT is exactly the set of $y \in U$ with $h(y) = 0$, and each of them has $g(y) \ge 1$;
2. each unreachable object of $U$ is reached by a path from a cycle of unreachable objects of $U$.

*Proof.* When the loop ends, the ZCT is empty, so by (J2) each $y \in U$ has $h(y) + g(y) \ge 1$. Line L16 subtracts $g(y)$ from each count, which gives (I1), and adds to the ZCT exactly the objects whose count becomes 0, which are those with $h(y) = 0$ and so $g(y) \ge 1$. This gives (I2) and part 1.

For part 2, let $x \in U$ be unreachable. Then $g(x) = 0$, so $h(x) \ge 1$, and some $x' \in U$ has a field that refers to $x$. The object $x'$ is unreachable, because otherwise $x$ would be reachable. Walk back in this way. Since $U$ is finite, the walk repeats an object, and the repeated part is a cycle of unreachable objects of $U$ from which a path leads to $x$. $\blacksquare$

So after each collection, deferred reference counting keeps the same set as [reference counting](/reference-counting/) does: the reachable objects and the garbage that a cycle of garbage reaches. Between collections it keeps, in addition, the acyclic garbage that has appeared since the last collection.
