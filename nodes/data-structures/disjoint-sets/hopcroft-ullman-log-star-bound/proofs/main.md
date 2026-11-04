---
title: Union by rank with path compression runs in O(m log* n) time
proves: [statement]
status: full
---

We prove that a sequence of $m$ operations MAKE-SET, UNION and FIND, of which $n$ are MAKE-SET, on a [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and [path compression](/path-compression/) takes $O(m \lg^* n)$ time. At the end we show that the same proof works for [union by size](/union-by-size/).

**Setup.** A UNION is two FINDs and one LINK of two roots, so the sequence becomes at most $3m$ operations MAKE-SET, FIND and LINK. MAKE-SET and LINK take $O(1)$ time, so they cost $O(m)$ in all. A FIND on the path $x_1, x_2, \ldots, x_s$, where $x_{j+1} = x_j.p$ and $x_s$ is the root, takes $O(s)$ time. We count one unit for each node $x_j$ with $j < s$ of each FIND, plus one unit per FIND; this is the time of the FINDs up to a constant factor.

**Rank facts.** From the [union by rank](/union-by-rank/) page:

1. For each non-root $x$, $x.rank < x.p.rank$. So ranks increase strictly along each path.
2. The rank of a node changes only while it is a root. Once a node is a non-root, it never becomes a root again, and its rank is fixed.
3. Each rank is at most $\lfloor \lg n \rfloor$.
4. For each $r \ge 0$, at most $n/2^r$ nodes ever have rank $r$.

**Blocks.** Define $t(0) = 1$ and $t(g) = 2^{t(g-1)}$ for $g \ge 1$, so $t(1) = 2$, $t(2) = 4$, $t(3) = 16$, $t(4) = 65536$. Put rank $r$ in block $B(r) = 0$ if $r \le 1$, and in block $B(r) = g$ if $t(g - 1) < r \le t(g)$ for $g \ge 1$. Each rank $r \ge 0$ is in exactly one block, and $B$ is non-decreasing in $r$.

*Number of blocks.* Let $G = \lg^* n$. We show that each rank $r \le \lfloor \lg n \rfloor$ has $B(r) \le G$. If $n \le 2$ then $r \le 1$ and $B(r) = 0$. Otherwise, $\lg^* n = G$ means that $G$ applications of $\lg$ take $n$ to a value at most 1, so $n \le t(G)$, since $\lg$ applied $G$ times to $t(G)$ gives $t(0) = 1$, and $\lg$ is increasing. Then $\lg n \le \lg t(G) = t(G - 1)$, so $r \le t(G - 1) \le t(G)$ and $B(r) \le G$. So all ranks lie in the $G + 1$ blocks $0, 1, \ldots, G$. Write $B(x)$ for $B(x.rank)$.

**Charging.** Consider one FIND on the path $x_1, \ldots, x_s$, before the compression, and a node $x_j$ with $j < s$, so $x_j$ is not the root. Charge the unit of $x_j$:

- to the FIND, if $x_j.p$ is the root ($j = s - 1$), or if $B(x_j.p) > B(x_j)$;
- to the node $x_j$, otherwise, that is, if $x_j.p$ is not the root and $B(x_j.p) = B(x_j)$.

By fact 1, $B(x_j.p) \ge B(x_j)$ always, so these cases cover all nodes.

**Charges to a FIND.** The units charged to one FIND are its own unit, at most one for $x_{s-1}$, and one for each $j$ with $B(x_{j+1}) > B(x_j)$. Along the path the blocks $B(x_1) \le B(x_2) \le \cdots \le B(x_s)$ do not decrease and lie in $0, \ldots, G$, so they increase at most $G$ times. So one FIND has at most $G + 2$ charges, and all FINDs together at most $3m(G + 2)$.

**Charges to a node.** Fix a node $x$. Its rank does not change once it is a non-root (fact 2), and it is charged only as a non-root, so $B(x)$ is fixed during all its charges. Let $g = B(x)$.

Each time $x$ is charged, in a FIND with $x = x_j$, its parent $y = x_{j+1}$ is not the root, so the root $x_s$ is a proper ancestor of $y$, and $x_s.rank > y.rank$ by fact 1. Path compression sets $x.p \leftarrow x_s$. So after each charge, $x.p.rank$ is larger than before the charge. Between charges, $x.p.rank$ does not fall: the parent of $x$ changes only by compression, to a proper ancestor of the old parent, which has a larger rank, and the old parent, if it stays, keeps or raises its rank.

So the ranks of the parent of $x$ at its successive charges strictly increase. At each charge, $B(x.p) = g$, so $x.p.rank \le t(g)$; and $x.p.rank > x.rank \ge 0$. A strictly increasing sequence of integers in $[1, t(g)]$ has at most $t(g)$ terms. So $x$ is charged at most $t(g)$ times. In block 0 this gives at most $t(0) = 1$ charge.

**Charges to the nodes of one block.** Let $N(g)$ be the number of nodes $x$ with $B(x) = g$ at the time they are charged; by fact 2 each node is counted in at most one block. For $g = 0$, $N(0) \le n$, so block 0 takes at most $n \cdot t(0) = n$ charges. For $g \ge 1$, by fact 4,
$$N(g) \le \sum_{r = t(g-1) + 1}^{\infty} \frac{n}{2^r} = \frac{n}{2^{t(g-1)}} = \frac{n}{t(g)}.$$
So the nodes of block $g$ take at most $N(g) \cdot t(g) \le n$ charges. Over the $G + 1$ blocks, the nodes take at most $n(G + 1)$ charges.

**Total.** Every unit of every FIND is charged once, to the FIND or to a node. So the FINDs cost at most $3m(G + 2) + n(G + 1)$ units, and the whole sequence costs
$$O(m) + 3m(\lg^* n + 2) + n(\lg^* n + 1) = O(m \lg^* n),$$
because $n \le m$. $\blacksquare$

**Union by size.** With union by size, define for a non-root $x$ the number $\rho(x) = \lfloor \lg s(x) \rfloor$, where $s(x)$ is the size of the tree of $x$ at the moment it was linked below another root, and for a root $\rho(x) = \lfloor \lg (\text{the size of its tree}) \rfloor$. We check facts 1 to 4 for $\rho$ in place of rank; the proof above uses nothing else.

*Fact 2:* $s(x)$ is fixed once $x$ is a non-root, and a root's size only grows. *Fact 3:* $\rho(x) \le \lfloor \lg n \rfloor$. *Fact 1:* when $x$ is linked below the root $y$, union by size gives $|T(y)| \ge s(x)$, so the new tree of $y$ has at least $2 s(x)$ nodes. Every later ancestor $z$ of $x$ has $y$ in its tree, so the size that $z$ has when it stops being a root, or its present size if it is a root, is at least the size of the tree of $y$ after this link, which is at least $2s(x)$. So $\rho(z) \ge \lfloor \lg (2 s(x)) \rfloor = \rho(x) + 1$. Compression only gives $x$ new parents that are ancestors, so $\rho$ increases strictly along each path. *Fact 4:* let $x \ne x'$ both be non-roots with $\rho = r$. Their trees at the time of their links have at least $2^r$ nodes each. If one of these trees contained the other node, say $x'$ in the tree of $x$, then $x$ is an ancestor of $x'$ and $\rho(x) > \rho(x')$ by fact 1, a contradiction. The trees of a union history are nested or disjoint, so the two trees are disjoint. So at most $n/2^r$ non-roots have $\rho = r$. Roots are never charged, and the counting of $N(g)$ is only over charged nodes, which are non-roots. So the proof holds for union by size, which is the form of Hopcroft and Ullman.
