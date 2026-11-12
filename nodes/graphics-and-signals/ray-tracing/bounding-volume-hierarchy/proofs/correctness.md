---
title: The BVH operations keep the invariant and answer the ray queries exactly
proves: [correctness]
status: full
---

Let $P = \{p_0, \ldots, p_{n-1}\}$ be the primitives, each with a box $\beta(p)$ that contains it. For a node $v$ let $P(v)$ be the primitives of the leaves below $v$, and $B(v)$ the box stored at $v$. The invariant is

- **(B)** $p \subseteq B(v)$ for each node $v$ and each $p \in P(v)$, and
- **(P)** the leaf ranges partition the array $refs$, and $refs$ is a permutation of $0, \ldots, n - 1$.

For a ray $r(t) = o + t\,d$ and a set $X$ write $T(X) = \{t \ge 0 : r(t) \in X\}$. For a primitive $p$ let $\tau(p) = \min T(p)$ if $T(p)$ is not empty. The answer of CLOSEST-HIT is a pair $(\tau(p), p)$ with $\tau(p)$ least over $P$, or none if no primitive is hit.

**Lemma 1 (BUILD).** After BUILD, (B) and (P) hold, and $B(v)$ is the union of $\beta(p)$ over $p \in P(v)$.

*Proof.* Each item on the stack is a range $[first, first + count)$ of $refs$, with $count \ge 1$. Line L1 makes $refs$ a permutation and the first item is the full range. Lines L6 to L8 permute the elements inside a range only, and replace the range by two ranges that partition it, both not empty because $count > L \ge 1$ gives $\lfloor count/2 \rfloor \ge 1$. So at all times the ranges on the stack and the leaf ranges made so far partition $[0, n)$, and when the stack is empty the leaf ranges do. This is (P). The ranges of the children partition the range of their parent, so $P(v)$ is the set of primitives of the range of $v$. Line L3 sets $B(v)$ to the union of their boxes, which contains each of them. This is (B). Line L6 sorts the range before the children are pushed, and later steps change only the subranges, so the range of $v$ holds the same set of primitives when the build ends. $\square$

**Lemma 2 (REFIT).** If (P) holds and each child has a larger index than its parent, then after REFIT, (B) holds for the current positions of the primitives, and $B(v)$ is the union of $\beta(p)$ over $p \in P(v)$.

*Proof.* By induction on the order of line L16, which is from the largest index down. When node $i$ is done, its children have larger indices and are done already, so by the hypothesis $B(\text{left}(i)) = \bigcup_{p \in P(\text{left}(i))} \beta(p)$, and the same for the right child. Line L18 gives $B(i) = \bigcup_{p \in P(i)} \beta(p)$, since $P(i)$ is the disjoint union of the two child sets. For a leaf, line L17 gives this directly. REFIT does not change $refs$ or the ranges, so (P) still holds. $\square$

**Lemma 3 (pruning).** If $T(B(v)) \cap [0, t_{max}] = \emptyset$, then no $p \in P(v)$ has a hit with $t \le t_{max}$.

*Proof.* By (B), $p \subseteq B(v)$, so $T(p) \subseteq T(B(v))$. $\square$

**Theorem.** If (B) and (P) hold, CLOSEST-HIT returns $(\tau^*, p)$ with $\tau^* = \min_{q \in P} \tau(q)$ and $\tau(p) = \tau^*$, or none if no primitive is hit. ANY-HIT$(T, r, t_{max})$ returns true exactly when some primitive has a hit with $t \le t_{max}$.

*Proof.* The loop of lines L10 to L14 pops each node at most once: the root is pushed once, and a node is pushed only by its parent, which is popped at most once. So the loop ends. Let $t_{max}$ be the current value; it is $+\infty$ or the $t$ of the current best, and it only decreases.

Suppose a primitive $q$ has $\tau(q) = \tau^*$. Consider the leaf $\ell$ that holds $q$; it exists and is unique by (P). We claim every node on the path from the root to $\ell$ is popped and passes line L11. The root is pushed at line L9. If a node $v$ on the path is popped, then $q \in P(v)$, $\tau^* \in T(B(v))$ by (B), and $\tau^* \le t_{max}$ at that time, because $t_{max}$ is either $+\infty$ or the $t$ of some primitive, which is at least $\tau^*$. So $T(B(v)) \cap [0, t_{max}] \ne \emptyset$, line L11 does not skip $v$, and line L14 pushes its child on the path. At $\ell$, line L13 tests $q$, finds $t = \tau(q) = \tau^* \le t_{max}$, and sets best to $(\tau^*, q)$ unless best already has $t = \tau^*$. Line L13 only accepts a smaller $t$ later, and no $t < \tau^*$ exists. So the returned pair has $t = \tau^*$, and it is a true hit since line L13 records only true hits.

If no primitive is hit, line L13 never accepts and the answer is none.

For ANY-HIT, $t_{max}$ is fixed. A true return comes from a true hit with $t \le t_{max}$. Conversely, if $q$ has a hit with $t_q \le t_{max}$, the argument above with $t_q$ in place of $\tau^*$ shows that the path to the leaf of $q$ is not pruned, so $q$ is tested unless the loop returned true before. $\blacksquare$

**Remark.** The proof uses only containment in (B), not tightness, so it also holds for boxes that are rounded outward, for refitted boxes, and for boxes that are larger than needed. It does use (P) only to find a leaf that holds $q$; a structure in which a primitive is in several leaves, as with spatial splits, satisfies the same argument as long as each primitive is in at least one leaf whose path boxes contain the part of it that the ray meets.
