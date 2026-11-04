---
title: The interval heap operations keep the interval invariants
proves: [correctness, termination]
status: full
---

We use the notation of the page: the node $j$ has the low key $\mathrm{LO}(j) = A[2j]$ and the high key $\mathrm{HI}(j)$, which is $A[2j + 1]$ if it exists and $A[2j]$ else; $P(j) = \lfloor (j - 1)/2 \rfloor$. The invariants are (N) $\mathrm{LO}(j) \le \mathrm{HI}(j)$, and (I) $\mathrm{LO}(P(j)) \le \mathrm{LO}(j)$ and $\mathrm{HI}(j) \le \mathrm{HI}(P(j))$ for $j \ge 1$. For an edge $(P(j), j)$, call the first inequality of (I) its *low side* and the second its *high side*.

**Lemma 0.** If (N) and (I) hold, then every key lies in $[A[0], \mathrm{HI}(0)]$. So FIND-MIN and FIND-MAX are correct.

*Proof.* By induction on the depth of a node $j$: its keys lie in $[\mathrm{LO}(j), \mathrm{HI}(j)]$ by (N), and by (I) this interval lies inside the interval of $P(j)$. $\square$

**Lemma 1 (sift-up on the low side).** Let $t$ be the last node, and suppose that (N) holds, that (I) holds except perhaps on the low side of the edge into $t$, and that $t \ge 1$ implies $\mathrm{LO}(t) \le \mathrm{HI}(P(t))$. Then SIFT-UP-MIN$(t)$ stops after at most $\lfloor \lg(t + 1) \rfloor$ iterations, and after it (N) and (I) hold.

*Proof.* We show that before each test of line L4, for the current node $j$:

> **(U)** (N) holds; (I) holds except perhaps on the low side of the edge into $j$; and if $j \ge 1$, then $\mathrm{LO}(j) \le \mathrm{HI}(P(j))$, $\mathrm{LO}(P(j)) \le \mathrm{LO}(c)$ for each child $c$ of $j$, and either $j$ holds one key or $\mathrm{LO}(P(j)) \le \mathrm{HI}(j)$.

*Start.* $j = t$ is the last node, so it has no children. If it holds two keys, one of them is the old key $w$ of the node, which lay in the interval of $P(t)$ before the insert, and $\mathrm{HI}(t)$ is the larger of the two keys, so $\mathrm{HI}(t) \ge w \ge \mathrm{LO}(P(t))$. The rest is the hypothesis.

*Step.* Let the test be true, with $q = P(j)$, $y = \mathrm{LO}(j)$ and $z = \mathrm{LO}(q)$, so $y < z$. Line L5 swaps $y$ and $z$.

- (N) at $q$: the new $\mathrm{LO}(q) = y < z \le \mathrm{HI}(q)$.
- (N) at $j$: if $j$ holds one key, it is $z$, and there is nothing to show. Else $\mathrm{HI}(j) \ge z$ by the last part of (U).
- The low side of $(q, j)$: $y < z$. The low side of $(q, s)$ for the other child $s$ of $q$: it held with $z$, so $\mathrm{LO}(s) \ge z > y$.
- The low sides of $(j, c)$ for the children $c$ of $j$: $\mathrm{LO}(c) \ge \mathrm{LO}(q)_{\text{old}} = z$ by (U).
- The high sides: no high key moved, except that a single-key node $j$ now has $\mathrm{HI}(j) = z \le \mathrm{HI}(q)$.

So (N) holds, and (I) holds except perhaps on the low side of the edge into $q$. For the rest of (U) at the new $j = q \ge 1$: $\mathrm{LO}(q) = y < z \le \mathrm{HI}(q) \le \mathrm{HI}(P(q))$; the children of $q$ have low keys $z$ and $\mathrm{LO}(s)$, and the old low side of the edge into $q$ gives $\mathrm{LO}(P(q)) \le z \le \mathrm{LO}(s)$; and $q$ holds two keys, since it is not the last node, with $\mathrm{HI}(q) \ge z \ge \mathrm{LO}(P(q))$.

*End.* Each iteration moves to the parent, so there are at most $\lfloor \lg(t + 1) \rfloor$ iterations. When the test is false, either $j = 0$, which has no edge into it, or the low side of the edge into $j$ holds. With (U), (N) and (I) hold. $\square$

**Lemma 1'.** The mirror statement holds for SIFT-UP-MAX on the high side, with the same proof and the order reversed.

**INSERT.** Before line L1 the invariants hold. Let $x$ be the new key and $j$ the last node.

*Line L2* orders the pair of $j$ if it has two keys, so (N) holds. The old key $w$ of $j$, if any, lay in $[\mathrm{LO}(P(j)), \mathrm{HI}(P(j))]$ by (I). The node $j$ has no children. So (I) can fail only at the edge $(P(j), j)$, and only through $x$: if $x < \mathrm{LO}(P(j))$, then $x$ is now $\mathrm{LO}(j)$ and only the low side fails, and $x < \mathrm{LO}(P(j)) \le \mathrm{HI}(P(j))$; if $x > \mathrm{HI}(P(j))$, then $x$ is now $\mathrm{HI}(j)$ and only the high side fails; else nothing fails.

In the first case, Lemma 1 applies to SIFT-UP-MIN$(j)$, and afterwards (N) and (I) hold, so SIFT-UP-MAX$(j)$ finds its test false at once, because each edge holds. The second case is symmetric with Lemma 1'. In the third case both sifts stop at once.

**EXTRACT-MIN.** By Lemma 0, $r = A[0]$ is a smallest key. If $n = 1$, the queue becomes empty. Else the last key $x$ is removed and written to $A[0]$. Removing the last key keeps (N) and (I) for all other nodes, since it deletes the high key of the last node or the whole last node; a node with one key left has $\mathrm{LO} = \mathrm{HI}$, and its key still lies in the parent's interval. The new $x$ is at most $\mathrm{HI}(0)$ by Lemma 0, so (N) holds at the root.

The claim before each test of line L11, for the current $j$: (N) holds everywhere; (I) holds except perhaps on the low sides of the edges from $j$ to its children; and if $j \ge 1$, then $\mathrm{LO}(P(j)) \le \mathrm{LO}(c)$ for each child $c$ of $j$. At the start, $j = 0$, and the last part is empty.

Let $c$ be the child with the smaller low key, and let the test of line L12 be true: $\mathrm{LO}(c) < \mathrm{LO}(j) = x'$. Line L13 swaps the two low keys. At $j$, the new low key $\mathrm{LO}(c)_{\text{old}}$ is at most the low key of the other child, so the low sides at $j$ hold; it is at least $\mathrm{LO}(P(j))$ by the last part of the claim; and it is less than $x' \le \mathrm{HI}(j)$, so (N) holds at $j$. At $c$, the low slot now holds $x'$. The high side of $(j, c)$ still holds, since $\mathrm{HI}(c)$ did not move. If $\mathrm{HI}(c) < x'$, line L13 swaps the two keys of $c$, so $c$ holds $(\mathrm{HI}(c)_{\text{old}}, x')$; then (N) holds at $c$, and the high side of $(j, c)$ holds because $x' \le \mathrm{HI}(j)$, which was true before since $x'$ was the low key of $j$. The new low key of $c$ is at least $\mathrm{LO}(c)_{\text{old}}$, which is now $\mathrm{LO}(j)$, so the low side of $(j, c)$ holds. For the children $d$ of $c$, $\mathrm{LO}(d) \ge \mathrm{LO}(c)_{\text{old}} = \mathrm{LO}(j)$, which is the last part of the claim at the new $j = c$; their low sides may now fail, and their high sides held and $\mathrm{HI}(c)$ did not decrease. So the claim holds after line L14.

When the loop returns at line L11 or L12, the low sides at $j$ hold, so (N) and (I) hold. Each iteration moves one level down, so the loop stops after at most the height of the tree.

**EXTRACT-MAX** is the mirror image for $n \ge 3$. For $n \le 2$, the last key is the largest by (N), and removing it leaves a valid heap.

**Theorem.** Starting from the empty array, each sequence of INSERT, EXTRACT-MIN and EXTRACT-MAX keeps (N) and (I), each operation stops in $O(\log n)$ steps, and the extracts and finds return a smallest or a largest key of the multiset. The array always holds exactly the current multiset.

*Proof.* The invariants and termination are the cases above, and the answers follow from Lemma 0. Each operation only appends, removes the last key, overwrites the removed extreme key with the removed last key, or swaps keys, so the multiset changes as the operation says. $\blacksquare$
