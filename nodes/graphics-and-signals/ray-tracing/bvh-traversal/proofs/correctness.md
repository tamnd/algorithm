---
title: Ordered BVH traversal returns the closest hit
proves: [correctness]
status: full
---

The tree has nodes with boxes $B(v)$. Each primitive is in at least one leaf, and for each node $v$ and each primitive $p$ of a leaf below $v$, $p \subseteq B(v)$. The ray is $r(t) = o + t\,d$, $d \ne 0$. For a set $X$ let $T(X) = \{t \ge 0 : r(t) \in X\}$, and for a primitive $p$ with $T(p) \ne \emptyset$ let $\tau(p) = \min T(p)$, the value that INTERSECT returns. SLAB$(B, [0, s])$ returns $\min (T(B) \cap [0, s])$, or MISS if the set is empty; this is the [slab method](/slab-method/) in exact arithmetic.

**Lemma 1 (termination and bounds).** Each node is pushed at most once, and the loop runs at most $2n - 1$ times for a tree with $n$ leaves.

*Proof.* Line L3 pushes the root, and lines L11 and L12 push only children of the popped node. A node has one parent, and the parent is popped at most once, since it was pushed at most once. A binary tree with $n$ leaves has $2n - 1$ nodes. $\square$

**Lemma 2 (facts about tmax).** At all times $t_{max} = +\infty$ if best is none, and $t_{max} = t$ if best $= (t, p)$, with $t = \tau(p)$. Moreover $t_{max}$ never increases.

*Proof.* Line L1 sets both. Line L8 changes them together, to a value $t \le t_{max}$ that INTERSECT returned. $\square$

**Theorem.** CLOSEST-HIT returns none if no primitive meets the ray, and otherwise a pair $(\tau^*, q')$ with $\tau(q') = \tau^* = \min_p \tau(p)$.

*Proof.* If no primitive is hit, line L8 never changes best, and line L13 returns none.

Otherwise fix a primitive $q$ with $\tau(q) = \tau^*$ and a leaf $\ell$ that holds it, with root path $v_0, v_1, \ldots, v_k = \ell$. Since $q \subseteq B(v_i)$, we have $\tau^* \in T(B(v_i))$ for each $i$. By Lemma 2 and the minimality of $\tau^*$, $t_{max} \ge \tau^*$ at all times. So for each $i$ and at every time, $T(B(v_i)) \cap [0, t_{max}]$ contains $\tau^*$ and SLAB returns a value $t_{v_i} \le \tau^*$.

We show by induction on $i$ that $v_i$ is pushed, and that when it is popped, either best already has the parameter $\tau^*$, or $v_i$ passes line L6. For $i = 0$, line L2 does not return, since SLAB finds $t_{root} \le \tau^*$, and line L3 pushes the root. When $v_i$ is popped with its value $t_{v_i} \le \tau^* \le t_{max}$, line L6 does not skip it. If $v_i$ is not the leaf, line L10 computes a value $\le \tau^*$ for the child $v_{i+1}$, so lines L11 and L12 push it.

So $\ell$ is popped and passes line L6, unless best already has the parameter $\tau^*$. At $\ell$, line L8 tests $q$ and gets $t = \tau^* \le t_{max}$. If best has a larger parameter, it is replaced by $(\tau^*, q)$. From then on line L8 only accepts a parameter that beats $\tau^*$, and none exists. In both cases the loop ends with best $= (\tau^*, q')$ for some $q'$ with $\tau(q') = \tau^*$, by Lemma 2. By Lemma 1 the loop ends. $\blacksquare$

**Corollary (ANY-HIT).** With a fixed $t_{max}$, ANY-HIT returns true if and only if some primitive has $\tau(p) \le t_{max}$.

*Proof.* A true return comes from line L8 with a hit $t \le t_{max}$. Conversely, if $\tau(q) \le t_{max}$, the induction above with $\tau(q)$ in place of $\tau^*$ shows that the path to a leaf of $q$ is never pruned, so $q$ is tested and the loop returns true, unless it returned true before. $\square$

**Remark.** The proof never uses the order of line L11. The order only makes the first hits close, so that line L6 prunes more. The proof also allows a primitive in several leaves and boxes that are larger than needed, so it covers spatial splits and refitted trees.
