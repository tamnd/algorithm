---
title: HyParView keeps valid symmetric views, connects every joiner, and a repair round removes every crashed active neighbour
proves: [correctness]
status: full
---

**Setting.** Nodes run lines L1 to L9. Each join, each repair of one broken link, and each shuffle runs to the end before the next one starts. A crashed node takes no steps. A live node can tell whether a node in its active view has crashed, as an open connection shows. In a *repair round*, every live node checks its active view once and runs lines L7 and L8 for each crashed neighbour.

**Claim.**

1. *Valid views.* At all times, for every node $p$: $|\mathrm{active}(p)| \le a$, $|\mathrm{passive}(p)| \le q$, $p$ is in neither view, and the two views are disjoint.
2. *Symmetry.* For two live nodes $x$ and $y$, $x \in \mathrm{active}(y)$ if and only if $y \in \mathrm{active}(x)$.
3. *Join.* After the join of $n$, the active view of $n$ is not empty.
4. *Repair.* When the repair of $p$ (lines L7 and L8) ends, $\mathrm{active}(p)$ is not empty, or $\mathrm{passive}(p)$ holds no live node.
5. *Repair round.* After a repair round, no live node has a crashed node in its active view.

**Proof of 1.** By induction over the steps. ADD-ACTIVE($p$, $x$) does nothing if $x = p$ or $x$ is already active. Otherwise, for each side whose active view is full, line L6 removes one node first, so the size stays at most $a$; it then removes $x$ from passive($p$) and $p$ from passive($x$) before adding the link, so the views stay disjoint. A node is added to a passive view only if it is not the owner, not active and not passive yet, and a full passive view first loses one entry, so the size stays at most $q$. Line L6 moves $r$ into passive($p$) after removing it from active($p$), so disjointness holds. Lines L7, L8 and L9 only remove active entries, call ADD-ACTIVE, or add passive entries in the same checked way. $\square$

**Proof of 2.** Every step that adds an active entry is ADD-ACTIVE, which adds both directions. Every step that removes an active entry between two live nodes is line L6, where DISCONNECT makes $r$ remove $p$ as well. Line L7 removes an entry only when the other node has crashed, which the claim does not cover. $\square$

**Proof of 3.** Line L1 runs ADD-ACTIVE(contact, $n$), so $n$ gets the contact. Later steps of the same join can only make $n$ lose the contact through line L6 at $n$, which runs only when the active view of $n$ is full, so it is not empty afterwards. $\square$

**Proof of 4.** Line L8 tries the nodes of passive($p$) one by one. A crashed node is removed. If the active view of $p$ is empty, the request has high priority, and a live node accepts a high priority request, so the first live node tried becomes a neighbour of $p$ and the repair ends with a non-empty active view. If the active view of $p$ is not empty when line L8 starts, it stays not empty, because line L8 only adds to it. So the repair ends with an empty active view only if every node of passive($p$) was tried and found crashed. $\square$

**Proof of 5.** Every step adds to an active view only nodes that are live at that time: the joiner in lines L1 and L3, and a node that answered a NEIGHBOR request in line L8. A node crashed before the round stays crashed. In the round, each live node $p$ removes every crashed node of active($p$) in line L7, and later steps of the round add only live nodes to active($p$). $\square$

**What is not proved.** The claims do not show that the active overlay of the live nodes is connected after a failure. A node can lose its last active link through a DISCONNECT in line L6, which the paper does not repair; the implementation offers an optional refill for it. Connectivity after massive failures and the freshness of the passive views are measured on the page.
