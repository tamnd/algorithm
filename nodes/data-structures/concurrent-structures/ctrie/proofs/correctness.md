---
title: The Ctrie is a linearizable, lock-free map
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, without snapshots. A READ and a CAS of the word $main$ of an I-node are atomic, and CAS compares by identity. All other nodes are immutable once created. For a hash $h$, write $h_d$ for the group $(h \gg dW) \bmod 2^W$; a node is *at depth* $d$ if it is reached from the root through $d$ C-node branches.

**Reachability.** An I-node, C-node, S-node, T-node or L-node is *reachable* if it can be reached from the root: from an I-node to its $main$, from a C-node to its branches, from a T-node to its S-node, from an L-node to its S-nodes. The *path* of a reachable node is the sequence of groups of the C-node branches on the way.

**The abstract map.** $M$ is the set of pairs (key, value) of the reachable S-nodes.

**Lemma 1 (final tombs).** Once the $main$ of an I-node is a T-node, it never changes again.

*Proof.* Every CAS on a $main$ expects the C-node or the L-node that was read before (lines L10, L13, L15, L21, L25, L26, L28), never a T-node. $\square$

**Lemma 2 (shape).** At every moment: (a) each reachable I-node has exactly one path, and so does each reachable S-node; (b) a reachable S-node of key $k$ whose path has length $d$ has a path equal to $hash(k)_0, \ldots, hash(k)_{d-1}$, and an S-node in an L-node has all bits of its hash equal to the bits of the path; (c) no key has two reachable S-nodes; (d) the root's $main$ is a C-node; (e) an I-node stops being reachable only at a successful CAS of line L26 or L28 that replaces it by the S-node of its T-node, and an I-node that is reachable and whose $main$ is not a T-node stays reachable with the same path until its $main$ becomes a T-node.

*Proof.* By induction on the successful CAS steps, which are the only steps that change any reachable node. Initially the root holds an empty C-node. Consider a successful CAS on $i.main$ from $m$ to $m'$. By (e) for the moment of the CAS, $i$ is reachable with a fixed path $P$ of length $d$: either it is the root, or its $main$ is $m$, which is not a T-node, and every CAS on it before kept it in place.

- Line L10 adds the S-node $s$ at the group $hash(s.key)_d$ of $m$, which was empty in $m$. The thread reached $i$ along the groups of $hash(s.key)$ (it chose each branch by FLAGPOS), so (b) holds for $s$. Since the group was empty, no S-node of the key was under $i$, and by (b) no S-node of the key exists elsewhere; so (c) holds.
- Line L12 and L13: if $b.key = s.key$, the S-node of the key is replaced at the same place. Otherwise DUAL builds a fresh subtree with $b$ and $s$, whose hashes agree on the groups below $d + 1$, splitting them at the first group where they differ, or in an L-node if they agree on all bits. Fresh I-nodes become reachable with one path each. (b) and (c) hold.
- Line L15 replaces the pair of the key in an L-node, or adds it, and line L25 removes it; both keep (b) and (c).
- Line L21 removes the S-node of the key, and CONTRACT may turn a C-node with one S-node into a T-node of it: the S-node keeps its path, since a T-node is entered without a new group. Not at the root, since $lev > 0$ is required, so (d) holds.
- Line L26 replaces each branch I-node $j$ of $m$ whose node was a T-node at the moment COMPRESS read it by that T-node's S-node $t.sn$. By Lemma 1, $j.main$ is still that T-node at the CAS. The S-node moves from path $P, g, $ (inside the T-node) to path $P, g$ (directly in the branch $g$), which is the same path, so (b) holds; $j$ stops being reachable, while its $main$ is a T-node, which is (e). CONTRACT then acts as above.
- Line L28 does the same for the single I-node $i'$, after it read a T-node in $i'.main$, which stays (Lemma 1).

No other step removes a branch that is an I-node, so (e) holds. $\square$

**Lemma 3 (the abstract map changes only at update points).** A successful CAS of line L10, L13 or L15 sets the pair of $s.key$ to $s.value$ in $M$ and changes nothing else. A successful CAS of line L21 or L25 removes the pair of $k$ from $M$, and the pair removed is the one returned. Every other successful CAS (lines L26 and L28) leaves $M$ unchanged.

*Proof.* The CAS changes $M$ only below $i$, which is reachable by Lemma 2(e). The cases are those of the proof of Lemma 2: lines L10, L13, L15 add or replace the S-node of the key; line L21 removes $b$, whose key is $k$, and returns $b.value$, with CONTRACT only regrouping the remaining S-node; line L25 removes the pair of $k$ from the L-node, whose value is returned. At lines L26 and L28, each S-node that moves is still reachable afterwards, and nothing else changes. $\square$

**Lemma 4 (reads).** Let an operation on key $k$ read $m$ from $i.main$ at line L2 or L17, at depth $d$, and let $m$ be a C-node or an L-node. At the moment of the read, $i$ is reachable with path $hash(k)_0, \ldots, hash(k)_{d-1}$.

*Proof.* The root is reachable with the empty path. The operation reached $i$ through branches chosen by FLAGPOS on $hash(k)$, from C-nodes it read in their I-nodes. By induction on $d$, its parent $p$ was reachable with the right path when the thread read the C-node $m_p$ of $p$, and $i$ was the branch of group $hash(k)_{d-1}$ of $m_p$. So $i$ was reachable just then. Afterwards, $i$ stays reachable with the same path until its $main$ becomes a T-node (Lemma 2(e)). At the later read, $i.main = m$ is not a T-node, and by Lemma 1 it was not a T-node at any moment in between. So $i$ is still reachable with the same path. $\square$

**Theorem 1 (linearizability).** Each history of the Ctrie is linearizable with respect to the sequential map.

*Proof.* Choose the points:

- insert: its successful CAS at line L10, L13 or L15;
- remove that returns a value: its successful CAS at line L21 or L25;
- lookup, and remove that returns NOTFOUND: the last READ of an I-node at line L2 or L17 in the last round, the one that did not restart.

Each point is inside its call; the order of the points respects real time. By Lemma 3 the updates change $M$ exactly as the sequential operations do at their points, with the right results.

A lookup or a remove that returns NOTFOUND or a value without a CAS read $m$ from $i$ at depth $d$, with $i$ reachable on the path of $k$ by Lemma 4. By Lemma 2(b) and (c), the S-node of $k$, if any, is under $i$, in the branch of group $hash(k)_d$ of $m$, or in $m$ if $m$ is an L-node. The node $m$ is immutable. If the group is empty, $k \notin M$ at that moment. If the branch is an S-node, it decides: its value, if its key is $k$, or NOTFOUND, since $k$ can be nowhere else. If the branch is an I-node, the read was not the last one. In an L-node, the value of $k$ in it decides. So the result is $M(k)$, or NOTFOUND, at the point. Rounds that restart do not change $M$ except through CLEAN, which changes nothing by Lemma 3. $\square$

**Theorem 2 (lock-freedom).** In every infinite execution in which some operation is pending, infinitely many operations finish.

*Proof.* Suppose that from some moment $\tau$ no operation finishes. Then after $\tau$ no CAS of an update point succeeds, since a call whose update CAS succeeds ends after its line L22 and CLEAN-PARENT, and CLEAN-PARENT goes back to line L27 only after a failed CAS on $p.main$, so only if some other CAS on $p.main$ succeeded. So after $\tau$ the only successful CASes are those of lines L26 and L28.

Count, for the reachable part of the trie, the potential $\Phi$ = the number of reachable I-nodes. Each successful CAS of line L28 removes one reachable I-node, and one of line L26 removes at least as many as it resurrects; a CAS of line L26 that resurrects nothing and changes nothing else replaces a C-node by an equal copy. After $\tau$ no CAS adds a reachable I-node, since only line L13 creates them. So the successful CASes of lines L26 and L28 that remove an I-node are finitely many. A thread does a CAS at line L26 only after it found a T-node in an I-node $j$ below $p$; if the CAS removes nothing, $j$ was not in $m$, so $j$ had already been detached, and after its restart from the root the thread cannot meet $j$ again (Lemma 2(e)). There are finitely many detached I-nodes with T-nodes (each was reachable before $\tau$ or has been detached since, and none is created). So after some moment $\tau' \ge \tau$ no CAS succeeds at all, and every reachable I-node has a fixed $main$. From then on, a thread that restarts goes down a trie that does not change; it does not meet a T-node, since any reachable T-node would be met by a cleaning CAS that succeeds, contradicting $\tau'$; so its next CAS, on the current node of a reachable I-node, succeeds, or it returns without one. Both contradict the assumption. $\blacksquare$
