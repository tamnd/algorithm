---
title: Reference counting is safe and keeps exactly the garbage that a dead cycle reaches
proves: [correctness]
status: full
---

The heap is the set $U$ of unfreed objects. One of them is the root object $\rho$, whose fields are the roots; it is never freed. For an object $y$, let $\mathrm{ref}(y)$ be the number of pairs $(x, j)$ with $x \in U$ and $x[j] = y$: the number of fields of unfreed objects that refer to $y$. An object is *reachable* if a path of fields leads to it from $\rho$. The mutator changes fields only with WRITE, and it calls WRITE only on an object $p$ that it reaches, with a value $y$ that is null or reachable. Each object made by NEW is stored by a WRITE right after it. We look at the states between two operations of the mutator.

**Invariant (C).** For each $y \in U$ other than $\rho$, $\mathrm{rc}(y) = \mathrm{ref}(y)$.

**Lemma 1.** (C) holds after each operation.

*Proof.* At the start, $U = \{\rho\}$ and (C) holds. NEW adds an object with no fields that refer to anything and with $\mathrm{rc} = 0$; no field refers to it, so (C) holds for it, and no other $\mathrm{ref}$ changes.

Consider WRITE$(p, i, y)$ with old value $z$. Line L4 adds 1 to $\mathrm{rc}(y)$, and line L6 adds the field $p[i]$ to the referrers of $y$ and removes it from the referrers of $z$. If $y = z$, nothing changes in total. Otherwise, after line L6, $\mathrm{rc}(y) = \mathrm{ref}(y)$ and $\mathrm{rc}(z) = \mathrm{ref}(z) + 1$. Line L8 restores (C) for $z$. If $\mathrm{rc}(z) > 0$, RELEASE ends here.

Otherwise the loop of line L11 runs. We show that the following holds each time line L11 tests the stack:

> **(L)** (C) holds for all objects of $U$. Each object on $S$ is in $U$, has $\mathrm{rc} = 0$, and is on $S$ only once. No object of $U$ that is not on $S$ has a count of 0 because of this RELEASE.

At the first test, $S = \{z\}$ and $\mathrm{rc}(z) = 0$, so (L) holds. In one turn of the loop, line L12 takes $x$ from $S$. Since $\mathrm{rc}(x) = \mathrm{ref}(x) = 0$, no field of an object of $U$ refers to $x$, not even a field of $x$ itself. For each field $x[j] = c$, the field of $x$ is a referrer of $c$, so $\mathrm{rc}(c) \ge 1$ before line L14, and $c \ne x$. Line L14 subtracts 1 for each such field, so after line L13 ends, $\mathrm{rc}(c) = \mathrm{ref}(c) - (\text{number of fields of } x \text{ that refer to } c)$. Line L16 removes $x$ from $U$, which removes exactly those referrers, so (C) holds again. A count reaches 0 at line L14 only once for each object, since counts only decrease in the loop, and line L15 then pushes that object. So no object is pushed twice, and each object with a count of 0 that this RELEASE made is on $S$ or freed. The loop ends because each turn frees one object of the finite set $U$. $\square$

**Lemma 2.** After each operation, $\mathrm{rc}(y) \ge 1$ for each $y \in U$ other than $\rho$ and the object that a NEW has just made.

*Proof.* A count is 0 only at its creation in line L2, or after a decrement in line L8 or L14. The first case ends at the WRITE that stores the new object, which adds 1. In the second case, line L9 or L15 puts the object on $S$, and by (L) it is freed before RELEASE returns. $\square$

**Theorem 1 (safety).** Reference counting never frees a reachable object.

*Proof.* Assume the contrary, and look at the first time that line L16 frees a reachable object $x$, in the heap as it is at that moment. Take a path $\rho = x_0 \to x_1 \to \cdots \to x_k = x$. Each $x_t$ is reachable, so by the choice of the first time, all of them are in $U$. Then the field of $x_{k-1}$ that refers to $x$ is a field of an object of $U$, so $\mathrm{ref}(x) \ge 1$. But $x$ was on $S$, so $\mathrm{rc}(x) = 0 = \mathrm{ref}(x)$ by (L). This is a contradiction. $\blacksquare$

**Theorem 2 (what is kept).** After each WRITE, every unreachable object of $U$ is reached by a path from a cycle of unreachable objects of $U$. With Theorem 1, $U$ is the set of reachable objects together with the garbage that a cycle of garbage reaches.

*Proof.* Let $x \in U$ be unreachable. By Lemma 2 and (C), $\mathrm{ref}(x) \ge 1$, so some $x' \in U$ has a field that refers to $x$. The object $x'$ is not $\rho$ and is not reachable, because otherwise $x$ would be reachable. So $x'$ is again an unreachable object of $U$, and it has a predecessor of the same kind. Walk back in this way. Since $U$ is finite, the walk repeats an object, and the objects between the two visits form a cycle of unreachable objects of $U$. The walk, read forward from that cycle, is a path to $x$. $\blacksquare$

**Corollary (the leak is permanent).** Let $K$ be a cycle of unreachable objects. No object of $K$ is ever freed.

*Proof.* An unreachable object stays unreachable, so the mutator never writes into $K$ again, and the fields of $K$ do not change. Assume that some object of $K$ is freed, and let $x$ be the first one. Its predecessor on $K$ is still in $U$ and refers to $x$, so $\mathrm{ref}(x) \ge 1$ when $x$ is freed, against (L). $\square$

By the theorem on the page about automatic memory reclamation, the set in Theorem 2 is the greatest fixed point of the map $S \mapsto \mathrm{Roots} \cup \mathrm{succ}(S)$ on the graph of $U$, while a tracing collector keeps only the least one, the reachable set.
