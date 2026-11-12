---
title: Weighted reference counting frees an object only after its last reference is gone
proves: [correctness]
status: full
---

The state of the system is the set $U$ of unfreed objects, the references that the processors hold (in roots and in fields of objects of $U$), and the multiset $M$ of DEC messages in flight. Each step is one call of NEW, COPY, DELETE, a move of a reference (into a field, a root, or a message to another processor), or the delivery of one message of $M$, chosen in any order. For an object $x \in U$, let

$$\sigma(x) = \sum_{r \text{ held}, \ \mathrm{target}(r) = x} w(r) \; + \sum_{\mathrm{DEC}(x, w) \in M} w.$$

**Invariant.**

- **(P)** Every held reference and every message in $M$ has a weight that is a power of two and at least 1.
- **(T)** $\mathrm{tw}(x) = \sigma(x)$ for each $x \in U$.

**Lemma.** Each step keeps (P) and (T).

*Proof.* NEW makes $x$ with $\mathrm{tw}(x) = W$ and one reference of weight $W$, a power of two. A move changes where a reference is held, not its weight.

COPY$(r)$ with $w(r) \ge 2$: the weight is a power of two, so $h = w(r)/2$ is an integer and a power of two, and lines L8 to L10 replace one weight $w(r)$ by two weights $h$ and $w(r) - h = h$, both at least 1. The sum $\sigma(\mathrm{target}(r))$ does not change.

COPY$(r)$ with $w(r) = 1$ and target $x$: line L5 makes a cell $c$ with $\mathrm{tw}(c) = W$. Line L6 puts the reference $(x, 1)$ into the field of $c$, and line L7 replaces $r$ by $(c, W)$. So the reference of weight 1 to $x$ now sits in $c$ instead of in $r$, and $\sigma(x)$ is unchanged. The only reference to $c$ is $r$, with weight $W = \mathrm{tw}(c)$. Then lines L8 to L10 split $W$ as in the first case.

DELETE$(r)$: line L11 removes the reference $r$ and adds a message with the same target and weight. The sum $\sigma$ of its target does not change, and the message weight is a power of two.

Delivery of DEC$(x, w)$: the message leaves $M$, so $\sigma(x)$ drops by $w$, and line L12 subtracts $w$ from $\mathrm{tw}(x)$. If $\mathrm{tw}(x) > 0$, (T) holds. If $\mathrm{tw}(x) = 0$, line L14 turns each field reference $s$ of $x$ into a message with the same weight, which keeps $\sigma$ of each target, and line L15 removes $x$ from $U$. $\square$

**Theorem (safety).** When line L15 frees $x$, no reference to $x$ is held anywhere and no message for $x$ is in flight. So no processor can reach $x$ again, and no later message names $x$.

*Proof.* At line L13, $\mathrm{tw}(x) = 0$, so $\sigma(x) = 0$ by (T). By (P), every term of $\sigma(x)$ is at least 1, so the sum has no terms. A new reference to $x$ arises only from COPY of a reference to $x$ or from NEW, which makes a new object, so none can arise after this point. A message for $x$ arises only from DELETE of a reference to $x$. $\blacksquare$

The theorem holds for every order of delivery, which is the point of the method: a message that is still in flight keeps its weight in $\sigma(x)$, so it keeps $\mathrm{tw}(x)$ above zero until it arrives.

**Liveness for acyclic garbage.** Assume that all messages are delivered in the end. If an object $x$ is not reached by any held reference through a chain of fields, and no cycle of objects reaches $x$, then $x$ is freed in the end. By induction on the longest chain of fields that leads to $x$ from an unfreed object: if no object refers to $x$, then all references to $x$ were deleted, their messages are delivered, and $\mathrm{tw}(x) = \sigma(x) = 0$ after the last one. Otherwise, each object that refers to $x$ has a shorter longest chain, so it is freed, and line L14 deletes its references to $x$. As with [reference counting](/reference-counting/), a cycle of garbage keeps a positive weight in each of its objects and is never freed.
