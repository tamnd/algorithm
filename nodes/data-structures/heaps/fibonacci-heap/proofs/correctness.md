---
title: The operations of a Fibonacci heap keep its invariants and return a minimum
proves: [correctness, termination]
status: full
---

We write $\mathcal{N}(H)$ for the set of nodes of the trees of $H$, and $K(H)$ for the multiset of their keys. The *structure* invariant (S) says: the trees are disjoint rooted trees on $\mathcal{N}(H)$; the roots form the root list and have $x.p = \text{nil}$; the children of each node $x$ form its child list, each child $c$ has $c.p = x$, and $x.degree$ is the number of children; and $H.n = |\mathcal{N}(H)|$. The other invariants are

- **(O)** $x.p.key \le x.key$ for each non-root node $x$;
- **(M)** $H.min = \text{nil}$ if $H.n = 0$, and else $H.min$ is a root with $H.min.key \le x.key$ for each $x \in \mathcal{N}(H)$;
- **(L)** each non-root node $x$ has lost no child since it last became a child (by LINK) if $x.mark = \text{false}$, and exactly one if $x.mark = \text{true}$.

A node *loses a child* when a CUT removes that child from its child list. We show that each operation keeps (S), (O), (M) and (L), and changes $K(H)$ as the priority queue type says.

**Lemma 1 (LINK).** Let $x$ and $y$ be two different roots with $x.key \le y.key$. Then LINK$(H, y, x)$ keeps (S) and (O) and does not change $K(H)$; afterwards $y$ is a non-root with no lost child and no mark, so (L) holds at $y$.

*Proof.* Line L31 takes $y$ out of the root list and line L32 puts it in the child list of $x$ with $y.p = x$ and adds 1 to $x.degree$. So the trees stay disjoint and (S) holds. The only new edge is $(x, y)$, and $x.key \le y.key$, so (O) holds. Line L33 clears the mark, and $y$ has just become a child, so it has lost no child since. No node is added or removed. $\square$

**Lemma 2 (CUT).** Let $x$ be a child of $y$. Then CUT$(H, x, y)$ keeps (S) and (O) and does not change $K(H)$. It makes $x$ a root, and $y$ loses the child $x$.

*Proof.* Line L40 removes $x$ from the child list of $y$ and lowers $y.degree$ by 1, and line L41 puts $x$ in the root list with $x.p = \text{nil}$. The subtree of $x$ comes along unchanged. (S) holds. An edge was removed and none was added, so (O) holds. $\square$

**Lemma 3 (CASCADING-CUT).** Assume (S) and (O), and assume that (L) holds at each node except $y$, and that $y$, if it is not a root, has lost exactly one more child than (L) allows for its mark. Then CASCADING-CUT$(H, y)$ stops, keeps (S) and (O), restores (L), and does not change $K(H)$.

*Proof.* By induction on the depth of $y$. If $y$ is a root (line L43), (L) says nothing about $y$, and the procedure stops. Else let $z = y.p$. If $y$ is not marked, it had lost no child, and now it has lost one. Line L44 marks it, so (L) holds at $y$, and the procedure stops. If $y$ is marked, it had lost one child, and now it has lost two. Line L45 cuts $y$ from $z$. By Lemma 2, (S) and (O) hold, $y$ is a root, so (L) says nothing about it, and $z$ has lost one more child. The depth of $z$ is one less than the depth of $y$, so by induction the call CASCADING-CUT$(H, z)$ stops and restores (L). $\square$

**Insert.** Line L1 makes $x$ a tree of one node, and line L2 adds it to the root list, so (S) holds after line L4, and (O) holds because there is no new edge. Line L3 keeps (M), since the new minimum is the smaller of the old minimum and $x.key$. No node lost a child, so (L) holds. $K(H)$ gains $x.key$.

**Union.** Line L5 joins the two root lists, so the trees of $H_2$ become trees of $H_1$, and lines L7 and L8 keep the counts. (S), (O) and (L) hold, since they hold in each heap and no edge changes. A minimum of $K(H_1) \cup K(H_2)$ is the smaller of the two minima, which line L6 picks, so (M) holds. $H_2$ becomes empty, which satisfies all invariants.

**Extract-min.** Let $H.n \ge 1$. By (M), $z = H.min$ holds a minimum of $K(H)$. Line L11 makes each child of $z$ a root. These children were non-roots and become roots, so (L) says nothing about them now; the edges from $z$ to them are gone, and (O) loses edges only. Line L12 removes $z$, which is a root with no children left. So $K(H)$ loses one copy of its minimum, and (S) holds with $H.n$ lowered by 1 at line L15. If $H.n = 1$ before, the heap is now empty, and line L13 sets (M). Else CONSOLIDATE runs.

**Lemma 4 (CONSOLIDATE).** Assume (S), (O) and (L) and that the root list is not empty. Then CONSOLIDATE stops, keeps (S), (O) and (L), does not change $K(H)$, makes the degrees of the roots pairwise different, and sets (M).

*Proof.* Let $R$ be the list of roots at line L18, taken once before the loop. We claim that, before each iteration of line L18, the set $Q$ of roots that are entries of $T$, together with the roots of $R$ not yet visited, is the set of all roots, each entry $T[d]$ is a root of degree $d$, and the entries have pairwise different degrees.

At the start, $T$ is empty and $Q \cup R$ is the root list. In an iteration with $w$, the inner loop keeps this claim: $x$ is a root of degree $d$ that is not in $T$; if $T[d] = y$ is set, then $y$ is another root of degree $d$, and after line L22, $x.key \le y.key$. By Lemma 1, LINK keeps (S), (O) and (L), and makes $y$ a child of $x$; then $x$ has degree $d + 1$, and line L24 clears $T[d]$. Each LINK lowers the number of roots by 1, so the inner loop stops after at most $|R| - 1$ links in total. When it stops, $T[d]$ is empty and line L25 stores $x$ there. So the claim holds after the iteration, with $w$ visited. When the loop ends, the roots are exactly the entries of $T$, with pairwise different degrees.

Lines L26 to L29 rebuild the root list from these entries, and line L30 keeps the smallest key seen, so at the end $H.min$ is a root of least key among the roots. By (O) and the global form of the [heap property](/heap-property/), each key is at least the key of its root, so (M) holds. No node is added or removed, so $K(H)$ is unchanged. $\square$

So after line L16, the invariants hold, $K(H)$ has lost one minimum, and the returned node $z$ holds that minimum.

**Decrease-key.** Let $k \le x.key$, as line L34 checks. Line L35 lowers $x.key$. The edges from $x$ to its children stay ordered, because $x.key$ only got smaller. The only edge that may break (O) is $(y, x)$, where $y = x.p$. If $y = \text{nil}$ or $y.key \le x.key$, (O) holds. Else line L37 cuts $x$; by Lemma 2, (S) and (O) hold, and $y$ has lost one child. So the hypothesis of Lemma 3 holds at $y$, and line L38 restores (L). In both cases, line L39 keeps (M): the keys other than $x.key$ did not change, $x$ is a root if its key is now below its parent, and else $x.key \ge y.key \ge H.min.key$. $K(H)$ has the old key of $x$ replaced by $k$.

**Delete.** Line L46 decreases $x.key$ to a value below all keys, so by the case above $x$ becomes a root and line L39 sets $H.min = x$. Line L47 then removes $x$. So $K(H)$ loses $x.key$, and the invariants hold.

**Termination.** Each operation except CONSOLIDATE and CASCADING-CUT has no loop or a loop over a finite list. Lemma 3 and Lemma 4 show that these two stop.

**Theorem.** Starting from the empty heap, after each sequence of operations the invariants (S), (O), (M) and (L) hold, FIND-MIN and EXTRACT-MIN return a node of minimum key, and the multiset $K(H)$ is the one that the priority queue type gives for the same sequence.

*Proof.* The empty heap satisfies all invariants. Each operation keeps them and changes $K(H)$ as the type says, by the cases above. By (M), FIND-MIN returns a node of minimum key, and the case of EXTRACT-MIN shows the same for it. $\blacksquare$
