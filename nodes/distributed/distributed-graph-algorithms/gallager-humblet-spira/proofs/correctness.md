---
title: GHS marks exactly the minimum spanning tree and halts
proves: [correctness]
status: full
---

The graph $G = (V, E)$ is connected, $n \ge 2$, and the weights are distinct, so the MST $T$ is unique. Channels are FIFO and each message arrives after a finite delay. A node serves its queue in order and puts a deferred message back at the end. At least one node wakes up on its own. The line numbers are those of the pseudocode on the main page.

**Fragments.** We say that an edge $j = \{u, v\}$ is *joined* when a node accepts a Connect on $j$, that is, it runs line L6 or line L8 for it. At each time, the *fragments* are the connected components of $(V, \text{joined edges})$. Each fragment has a level and a core, defined by the events: a single node has level 0 and no core. When line L8 accepts a Connect on $j$, the two fragments at the ends of $j$ become one fragment with level $LN_v + 1$ and core $j$. When line L6 accepts a Connect, the union keeps the level and the core of the fragment of the receiver. The *name* of a fragment of level at least 1 is the weight of its core. We write $F(v)$ for the fragment of $v$, and $\ell(F)$ for its level.

A node sends Connect only on an edge that is not Branch (lines L3 and L34), and it marks the edge Branch at once. So a node sends at most one Connect on each edge, and each edge is a core at most once. Since fragments only grow, a fragment keeps its level and name until it merges or is absorbed, and no two fragments ever have the same name.

**Lemma 1 (what nodes know).** At each time and for each node $v$:

1. $LN_v$ never decreases, and $LN_v \le \ell(F(v))$.
2. If $LN_v \ge 1$, then $(LN_v, FN_v)$ is the level and the name of a fragment that contained $v$ at some time. So if $LN_v = \ell(F(v))$, then $FN_v$ is the name of $F(v)$.
3. If $SN_v = $ Find, then $LN_v = \ell(F(v))$, and the search of $F(v)$ at this level is not yet decided (line L30 or line L31 has not run for it).

*Proof.* $LN_v$ and $FN_v$ change only at line L9, so we look at each Initiate. An Initiate from line L8 carries the level and the name of the new fragment, which contains the receiver. An Initiate from line L6 or line L10 carries the values $(LN_x, FN_x)$ of its sender $x$, so by induction they are the level and name of a fragment that contained $x$. The receiver is in the same fragment as $x$ after the join, and fragments only grow, so part 2 holds. Levels in Initiates never go down on one edge, because $LN_x$ never goes down and the edge is FIFO, and an Initiate on an absorb carries $LN_x > L \ge LN_v$. This gives part 1, since the true level of a fragment also never goes down.

For part 3, Find is set only at line L9 by an Initiate with $S = $ Find. Such an Initiate comes from line L8, with the true values, or from a node $x$ in state Find at line L6 or line L10, with true values by induction. In both cases the sender adds one to its find-count, so it cannot report, and so the core cannot decide, until the receiver reports. The level of a fragment changes only after a Connect of this fragment is accepted (see Lemma 3), and a Connect is sent after the decision at line L30. So the level is still the same when the receiver sets Find, and it stays the same until the receiver leaves Find at line L24. $\square$

**Lemma 2 (Tests are answered correctly).** Let $u$ send Test$(L, F)$ on the edge $j = \{u, v\}$. When $v$ answers, it sends Reject (or, at line L19, it treats $j$ as rejected) if and only if $v \in F(u)$.

*Proof.* The Test is sent in state Find, so by Lemma 1.3, $(L, F)$ is the true level and name of $F(u)$, and $L \ge 1$. Node $u$ does not leave Find before the answer, so $F(u)$ keeps level $L$ and name $F$ until then. Node $v$ answers only when $LN_v \ge L$ (line L15).

If $v \in F(u)$ at the answer, then $LN_v \le \ell(F(u)) = L$ by Lemma 1.1, so $LN_v = L$, and by Lemma 1.2 $FN_v = F$. So line L16 does not send Accept.

If $v \notin F(u)$ and $FN_v = F$, then by Lemma 1.2, $v$ was in a fragment of name $F$ and level $LN_v \ge L$. Names are unique, so this is $F(u)$. Fragments only grow, so $v \in F(u)$, a contradiction. So $FN_v \ne F$, and line L16 sends Accept. $\square$

An edge becomes Rejected only at line L17 or line L22, after such a Test, so each Rejected edge joins two nodes of one fragment. A Branch edge also joins two nodes of one fragment once its Connect is accepted.

**Lemma 3 (Connects follow the rules).** Let a Connect$(L)$ from $u$ on $j = \{u, v\}$ be served at $v$. Then $j$ is the MOE of $F(u)$, $L = \ell(F(u))$, and $F(u)$ sends no other Connect until this one is accepted. Moreover $L \le LN_v$ when it is served. Line L6 runs only if $\ell(F(u)) < \ell(F(v))$ (absorb), and line L8 runs only if both fragments have level $L$ and the same MOE $j$ (merge).

*Proof.* A Connect$(0)$ from line L3 is on the lightest edge of a single node, which is its MOE. Another Connect comes from line L34 at the end of the Change-root path, after the core decided. Lemma 4 below shows that this edge is the MOE. A fragment decides once per level, so it sends one Connect per level, and its level does not change before the Connect is accepted: an absorb needs its own Connect, and a merge needs its own Connect on the merge edge, which is the same edge.

If $L \ge 1$, then $u$ tested $j$ at level $L$ and got Accept, so $LN_v \ge L$ then, and by Lemma 1.1 also later. If $L = 0$, then $L \le LN_v$ holds trivially. So line L7 defers only when $L = LN_v$.

If line L6 runs, then $L < LN_v \le \ell(F(v))$. If line L8 runs, then $L = LN_v$ and $SE_v[j] = $ Branch. The edge $j$ is not joined, because $u$ marked it Branch when it sent this Connect, so $v$ marked it Branch when $v$ sent its own Connect on $j$. Then by the first part, $j$ is the MOE of $F(v)$, and $\ell(F(v))$ is the level at which $v$ sent it. That Connect carried a true level, and since then neither $LN_v$ nor $\ell(F(v))$ changed, so $\ell(F(v)) = LN_v = L$. $\square$

**Lemma 4 (the search finds the MOE).** When a core node runs line L30 with $w > $ best-wt, the path of best-edge pointers from it leads to the MOE of its fragment. When line L31 runs, the fragment has no outgoing edge.

*Proof.* Take the search of a fragment $F$ at level $L$. Each node $x$ that gets the Find Initiate tests its Basic edges in increasing order of weight. Branch and Rejected edges are inside $F$, so by Lemma 2 the first Accept is on the lightest outgoing edge at $x$, and if no Accept comes, $x$ has no outgoing edge. The find-count of $x$ counts the Find Initiates that it sent, so $x$ reports only after all its children in the search. Each Report carries the minimum over the subtree, and best-edge points toward it. Each core node gets the Report of the other core node over the core and serves it only in state Found (line L29), so both halves are complete. The side with the smaller value is the side with best-wt $< w$, and it runs CHANGE-ROOT, which follows the best-edge pointers (lines L32 and L33). If both values are $\infty$, both core nodes halt.

The nodes that never got the Find Initiate need care. A node that joins $F$ during the search through a node $v$ in state Find gets a Find Initiate at line L6 and is counted. A node $y$ that joins through a node $v$ in state Found comes with its fragment $F'$, whose MOE $e$ ends at $v$. Node $v$ had reported while $e$ was still Basic at $v$. Node $v$ tested in increasing order and stopped at an Accept on an edge $e'$ with $w(e') < w(e)$, because a Test on $e$ would have waited at $F'$ until $F'$ reached level $L$, and $F'$ has a lower level. Each outgoing edge of $F'$ weighs at least $w(e) > w(e')$, and $e'$ does not enter $F'$, so the new nodes add no lighter outgoing edge. By Lemma 1.3, a node with a stale level is not in Find and will get the Find Initiate later through $v$, if the search still runs. $\square$

**Theorem.** Each Branch edge is in $T$. The run halts, and at the end the Branch edges are exactly $T$.

*Proof.* By Lemmas 3 and 4, each Connect is on the MOE of a fragment, and by the [cut property](/cut-property/) on the cut between the fragment and the rest, this edge is in $T$. An edge becomes Branch only at lines L2, L5 and L35, and each time it carries a Connect. So every joined edge and every Branch edge is in $T$.

*Levels are small.* A merge joins two disjoint fragments of level $L$, and an absorb adds nodes. By induction, a fragment of level $L$ has at least $2^L$ nodes, so each level is at most $\log_2 n$.

*No deadlock.* The total number of messages is finite (at most $5n \log_2 n + 2m$, see the main page). Suppose that the run reaches a state with no message in transit, in which each queued message is deferred, and that no node halted. Then every Initiate has arrived, so by Lemma 1 every awake node knows the true level and name of its fragment. A sleeping node got no message, so each neighbour of an awake node is awake: a Connect or a Test wakes its receiver (lines L4 and L15). Since $G$ is connected and some node woke, all nodes are awake, and there are at least two fragments, because the search of a single fragment $V$ ends at line L31.

Let $L$ be the lowest level, and let $F$ be the fragment of level $L$ whose MOE $e = \{x, y\}$, with $x \in F$, is lightest. A Test from $F$ goes to a node of true level at least $L$, so it is not deferred. A Report is deferred only at a core node that waits for its own half. So the search of $F$ is complete (or $L = 0$), and its Connect$(L)$ on $e$ waits at $y$. By Lemma 3 and line L7, $LN_y = L$ and $SE_y[e] = $ Basic, so $F' = F(y)$ has level $L$. By the same reasoning $F'$ has sent its Connect on its MOE $e'$, and $w(e') \le w(e)$, since $e$ leaves $F'$. The choice of $F$ gives $w(e) \le w(e')$, so $e' = e$ and $SE_y[e] = $ Branch, a contradiction.

So the run continues until a node halts. A core node halts only at line L31, so by Lemma 4 its fragment has no outgoing edge, and since $G$ is connected, the fragment is $V$. It is a tree of joined edges, all in $T$, with $n - 1$ edges, so it is $T$. An edge that is Branch at one end only would carry a Connect not yet accepted, and a fragment equal to $V$ has no outgoing edge to send it on, so no such edge is left. $\blacksquare$
