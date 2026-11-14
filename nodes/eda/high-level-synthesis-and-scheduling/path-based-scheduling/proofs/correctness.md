---
title: Correctness of path-based scheduling
proves: [correctness]
status: full
---

We use the model of the page. The control flow graph $G$ is a DAG of operations with types $k(v)$ and delays $0 \le d(v) \le T$, and some types are limited to one unit. For a path $p = p_0, \ldots, p_{m-1}$ and a set $H$ of edges, the states of $p$ are the maximal runs of consecutive operations with no edge of $H$ between them. $H$ is valid when every state of every path holds at most one operation of each limited type and has a total delay of at most $T$.

## Lemma 1 (the intervals are exact)

Fix a path $p$ and a set $H$ of edges. Every state of $p$ meets both rules exactly when $H$ holds an edge $(p_t, p_{t+1})$ with $lo \le t \le hi$ for every constraint $[lo, hi]$ of $p$.

*Proof.* Operations $p_i$ and $p_j$ with $i < j$ are in one state exactly when none of the edges at positions $i, \ldots, j - 1$ is in $H$.

Suppose every constraint holds a cut. If $p_i$ and $p_j$, with $i < j$, share a limited type, the constraint $[i, j - 1]$ holds a cut, so they are in different states. If a state $p_i, \ldots, p_{j'}$ had a total delay above $T$, let $j$ be the least index with $d(p_i) + \cdots + d(p_j) > T$. Then $j \le j'$ and $j > i$, since $d(p_i) \le T$. The constraint $[i, j - 1]$ holds a cut at a position between $i$ and $j - 1 < j'$, so $p_i$ and $p_{j'}$ are in different states, a contradiction.

Conversely, suppose some constraint $[lo, hi]$ holds no cut. Then $p_{lo}, \ldots, p_{hi + 1}$ are in one state. If the constraint came from two operations of one limited type, both are in the state. If it came from a run with delay above $T$, that run is in the state. Either way a rule fails. $\square$

So $H$ is valid exactly when it meets the edge set of every constraint of every path, which is the family $R$ of line L5.

## Lemma 2 (one path, the right end greedy is optimal)

For a finite family $I$ of integer intervals, the scan of line L4 returns a set $c$ that meets every interval, and no set with fewer points does.

*Proof.* The scan takes the intervals in order of right end. Let the chosen points be $c_1 < c_2 < \cdots < c_q$, where $c_r$ is the right end of the interval $J_r$ that was open when it was chosen.

Every interval is met. When the scan reaches an interval $[lo, hi]$, the last point so far is the right end of an earlier interval, so it is at most $hi$. If it is at least $lo$, it meets the interval. If not, the scan adds $hi$, which meets it.

The intervals $J_1, \ldots, J_q$ are pairwise disjoint. Take $r < r'$. When $J_{r'} = [lo', hi']$ was reached, the last point was at least $c_r$ and below $lo'$, so $lo' > c_r = hi(J_r)$. So any set that meets every interval needs a different point in each $J_r$, at least $q$ points. $\square$

**Corollary.** For every valid $H$ and every path $p$, the positions of $p$ whose edges lie in $H$ meet every interval of $p$ by Lemma 1, so $|H| \ge |H \cap p| \ge |c_p|$. Hence $\max_p |c_p|$ is a lower bound for the fewest cuts, and $1 + |c_p|$ is the fewest states that path $p$ can have.

## Theorem 1 (valid output)

The set $H$ of line L11 is valid.

*Proof.* Each pass of lines L7 to L9 removes from $U$ the sets that hold $e$, and $e$ is in at least one set of $U$, so the loop ends after at most $|R|$ passes. When it ends, every set of $R$ holds an edge of the list. Line L10 drops an edge only when the remaining edges still meet every set of $R$, so this stays true. By Lemma 1, $H$ is valid. $\square$

The greedy loop of lines L7 to L9 is the greedy set cover method on the dual instance, in which each edge $e$ is the set of constraints that hold $e$. Its ratio $H_D$, with $D$ the largest such set, is proved on the greedy set cover page. Line L10 only removes edges, so the ratio still holds.

## Theorem 2 (the merge is NP-hard)

Given a DAG, a family of subpaths of it and an integer $K$, deciding whether some set of at most $K$ edges meets every subpath is NP-complete.

*Proof.* The problem is in NP, since a set of edges is checked in polynomial time. We reduce from vertex cover. Let $G' = (N, F)$ be a graph with $N = \{1, \ldots, n\}$, and $K$ an integer. Build a DAG with nodes $a_1, b_1, \ldots, a_n, b_n$, an edge $x_i = (a_i, b_i)$ for each $i$, and for each $\{i, k\} \in F$ with $i < k$ a connector edge $y_{ik} = (b_i, a_k)$. Every edge goes forward in the order $a_1, b_1, a_2, b_2, \ldots$, so the graph has no cycle. For each $\{i, k\} \in F$, take the subpath $Q_{ik} = x_i, y_{ik}, x_k$. The build takes polynomial time. A single entry joined to every $a_i$ and an exit joined from every $b_i$ make each $Q_{ik}$ part of an entry to exit path, and these extra edges lie in no $Q_{ik}$.

If $S \subseteq N$ is a vertex cover, the edges $\{x_i : i \in S\}$ meet every $Q_{ik}$, since $i \in S$ or $k \in S$.

Conversely, let $H$ meet every $Q_{ik}$ with $|H| \le K$. Drop from $H$ the edges that lie in no $Q_{ik}$. Replace each connector $y_{ik} \in H$ by $x_i$. The connector $y_{ik}$ lies only in $Q_{ik}$, and $x_i$ also lies in $Q_{ik}$, so every subpath is still met, and the size does not grow. Now $H = \{x_i : i \in S\}$ for some $S$ with $|S| \le K$, and $S$ is a vertex cover, since each $Q_{ik}$ holds $x_i$ or $x_k$. Vertex cover is NP-complete (Karp, 1972), so the problem is NP-complete. $\square$

The reduction lives in the abstract model of subpaths. Whether every family of subpaths arises from operations, delays and limited units as on the page is not claimed here.

## What is not claimed

- The greedy merge is not exact. In the measured run on the page it used more cuts than the exhaustive search on 4 of 150 random graphs.
- The page does not reproduce Camposano's own merge step, and the bounds above concern the version on the page.
- The number of cut edges is the measure that the page minimizes. The number of states of the final controller can be smaller, when cuts on several edges into one operation start the same state.
