---
title: The dynamic segment tree keeps its invariant and answers range queries
proves: [correctness, termination]
status: full
---

Let $(M, \oplus, e)$ be a commutative monoid, $U \ge 1$, and let $\mathcal T$ be the full segment tree over $[0, U)$: the root covers $[0, U)$, and a range $[lo, hi)$ with $hi - lo \ge 2$ has the children $[lo, mid)$ and $[mid, hi)$ with $mid = \lfloor (lo + hi) / 2 \rfloor$. Each node of the dynamic tree corresponds to one range of $\mathcal T$, found by the walk from the root. Write $A[lo, hi) = A[lo] \oplus \cdots \oplus A[hi - 1]$, with $A[lo, lo) = e$.

**Invariant (D).** (a) The created nodes form a subtree of $\mathcal T$ that contains the root. (b) Each created node $v$ over $[lo, hi)$ has $\mathit{val}[v] = A[lo, hi)$. (c) If a range of $\mathcal T$ has no created node, then $A[k] = e$ for each $k$ in it.

At the start only the root exists with $\mathit{val} = e$, and $A$ is all $e$, so (D) holds.

**Lemma 1 (termination of UPDATE).** UPDATE$(i, x)$ with $0 \le i < U$ stops after $d + 1$ passes of the loop, where $d \le \lceil \lg U \rceil$ is the depth of the leaf $[i, i+1)$ in $\mathcal T$, and $i \in [lo, hi)$ holds at each pass.

*Proof.* Initially $i \in [0, U)$. If $i < mid$, the new range is $[lo, mid) \ni i$, and otherwise it is $[mid, hi) \ni i$. Each pass replaces a range of length $h \ge 2$ by one of length $\lfloor h/2 \rfloor$ or $\lceil h/2 \rceil < h$, so the length reaches 1 after at most $\lceil \lg U \rceil$ passes, and the range is then $[i, i+1)$. $\square$

**Lemma 2 (UPDATE keeps (D)).** After UPDATE$(i, x)$ the invariant holds for the new array $A'$ with $A'[i] = A[i] \oplus x$ and $A'[k] = A[k]$ for $k \ne i$.

*Proof.* By Lemma 1, the loop visits exactly the ranges of $\mathcal T$ that contain $i$, from the root down to the leaf, and lines L7 and L10 create the missing ones, each as a child of a created node, so (a) holds. A node created at line L7 or L10 covers a range that had no node, so by (c) its items are all $e$, and $\mathit{val} = e = A[lo, hi)$ before line L3 adds $x$. For each visited node, line L3 turns $\mathit{val}[v] = A[lo, hi)$ into $A[lo, hi) \oplus x = A'[lo, hi)$, by commutativity and associativity, since $i \in [lo, hi)$. A node that is not visited covers a range without $i$, so its value is unchanged and still right. A range without a node after the update does not contain $i$, since every range with $i$ now has a node, so (c) holds for $A'$. $\square$

**Lemma 3 (QUERY).** For a created node $v$ over $[lo, hi)$, or $v = 0$ for an absent range $[lo, hi)$ of $\mathcal T$, and any $0 \le l \le r \le U$, QUERY$(v, lo, hi, l, r)$ returns $A[\max(l, lo), \min(r, hi))$, read as $e$ when the range is empty.

*Proof.* By induction on $hi - lo$. If $v = 0$, the range has no node, so by (c) every item in it is $e$, and the result $e$ is right. If $r \le lo$ or $hi \le l$, the overlap is empty and $e$ is right. If $l \le lo$ and $hi \le r$, the overlap is $[lo, hi)$ and $\mathit{val}[v]$ is right by (b). Otherwise the overlap is a proper part of $[lo, hi)$, so $hi - lo \ge 2$, and the node has the two child ranges. A missing child is passed as 0, which is covered by the first case. The overlap with $[lo, hi)$ is the overlap with $[lo, mid)$ followed by the overlap with $[mid, hi)$, so by the induction hypothesis and associativity line L15 returns the right value. $\square$

**Theorem.** After any sequence of updates, QUERY$(1, 0, U, l, r) = A[l, r)$ for $0 \le l \le r \le U$, and the tree has at most $\min(1 + m \lceil \lg U \rceil, 2U - 1)$ nodes after $m$ updates.

*Proof.* The first part follows from Lemma 2 by induction over the updates and from Lemma 3 with the root, since $[\max(l, 0), \min(r, U)) = [l, r)$. For the size, each update creates nodes only on one path of $\mathcal T$ below the root, at most $\lceil \lg U \rceil$ of them, and all created nodes are distinct nodes of $\mathcal T$, which has $2U - 1$ nodes. $\square$
