---
title: The R*-tree operations keep the R-tree invariant, stop, and search reports exactly the rectangles that meet the query
proves: [correctness, termination]
status: full
---

We use the invariant (R) of the R-tree and its proof, and show only what differs. Heights are counted from the leaves: a leaf has height 0. Let $2 \le m \le M/2$, as in the paper, where $m$ is 40% of $M$, and $0 \le p \le M - m$. Only the termination argument uses $m \ge 2$.

**Search.** The tree satisfies (R), so the containment lemma of the R-tree holds: each stored rectangle in the subtree of an entry lies inside the rectangle of that entry. The search of line L17 is the R-tree search, which is correct and stops by that lemma.

**R*-SPLIT.** The input has $M + 1$ entries. Every cut considered in lines L10 and L12 has a first group of $k \ge m$ entries and a second group of $M + 1 - k \ge m$ entries, since $k$ runs from $m$ to $M + 1 - m$, and this range is not empty because $M + 1 - m \ge m + 1$. A cut of a sorted list is a partition of the entries. So the output is a partition into two groups of sizes between $m$ and $M + 1 - m \le M$.

**INSERT-AT keeps (R) except at the active node.** Claim: during INSERT-AT$(E, \ell)$, where $E$ has a subtree of height $\ell - 1$ if $\ell \ge 1$, at the start of each pass of line L4 with node $u$ at height $j$: (R) holds, except that $u$ may have $M + 1$ entries and the rectangles for $u$ and its ancestors may be stale; all leaves are at one depth; and the set of stored entries is the old set plus $E$. CHOOSE-SUBTREE (line L2) follows one entry per level down to a node of height $\ell$, whatever entry it picks at each node, so $E$ goes into a node at height $\ell$, and its subtree leaves are at the depth of all other leaves. So the claim holds at the first pass.

In a pass, three things can happen.

*Forced reinsert (line L5).* $u$ is not the root and has $M + 1$ entries. Removing $p$ of them leaves $M + 1 - p \ge m + 1$ entries, so $u$ is not underfull, and at most $M$ entries remain when $p \ge 1$. Then the rectangles from $u$ up are set to the MBRs of the children, which makes (R) hold everywhere for the stored set without the $p$ removed entries. Each removed entry has a subtree of height $j - 1$ (or is a leaf entry when $j = 0$), so INSERT-AT of it at height $j$ satisfies the precondition. By induction on the number of nested calls (see the termination argument below), each of these calls returns with (R) holding and the entry added. After all $p$ calls, the stored set is the old set plus $E$, and (R) holds.

*Split (lines L6 to L8).* By the split lemma, $u$ and the new node $v$ each have between $m$ and $M$ entries, and they are at the same height, so their leaves stay at one depth. If $u$ was the root, line L7 makes a root with two correct entries: (R) holds, and all leaves are one level deeper. Otherwise $v$'s entry is added to the parent, which may now have $M + 1$ entries.

*Move up (line L9).* The rectangle of $u$ in its parent becomes $\operatorname{MBR}(u)$, which is correct, and the pass goes to the parent at height $j + 1$. The claim holds there.

When $u$ becomes none, line L9 has fixed all rectangles up to the root and no node overflows, so (R) holds.

**Termination of INSERT.** The set done grows by one height at each forced reinsert, and line L5 never reinserts twice at one height during one top-level INSERT, since done is reset only in line L1. The number of stored leaf entries is fixed during the insertion (the old ones plus $E$), and by (R) a tree of height $j \ge 1$ holds at least $2 m^{j}$ leaf entries, so the height stays below a bound $H$ that depends only on that number. So at most $H$ forced reinserts happen in one insertion, where $H$ bounds the height. Each forced reinsert starts $p$ calls of INSERT-AT. A call of INSERT-AT that does no forced reinsert makes at most one pass per level, each pass going up one level, so it stops. By induction on the number of heights not yet in done, every call stops: a call that does a forced reinsert adds a height to done before it starts its nested calls, so the nested calls have fewer heights left.

**DELETE.** Lines L14 to L16 are the R-tree deletion, with INSERT-AT in place of the R-tree insertion. The R-tree proof shows that line L14 finds the entry if it is stored, that line L15 leaves all remaining nodes with between $m$ and $M$ entries (except perhaps the root) and with correct rectangles, and that each removed node's entries are kept with their heights. Each reinsertion is an INSERT-AT at the right height, which keeps (R) by the claim above, starting with an empty done. Line L16 removes roots with one child. So (R) holds, and the stored set is the old set minus $(r, id)$. The number of reinsertions is finite and each stops, so DELETE stops. $\blacksquare$
