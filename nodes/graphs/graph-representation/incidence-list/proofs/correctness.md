---
title: The incidence-list operations keep the slot invariant and report the incident edges
proves: [correctness]
status: full
---

We use the pseudocode of the page. An edge name $e$ is *live* when $alive[e]$ is true. The invariant is:

> **(I1)** Each live $e$ occurs exactly once in $out[tail[e]]$, at index $pos_{out}[e]$, and in no other $out$ list. **(I2)** Each live $e$ occurs exactly once in $in[head[e]]$, at index $pos_{in}[e]$, and in no other $in$ list. **(I3)** No list holds a name that is not live.

The empty structure, with no edge names and empty lists, meets (I1) to (I3) with nothing to check.

**Lemma 1 (swap-remove).** Let $L$ be a list in which the name $e$ occurs exactly once, at index $pos[e]$, and in which each other name $g$ of $L$ occurs once at index $pos[g]$. After SWAP-REMOVE$(L, pos, e)$, the list $L$ holds exactly the names of the old $L$ other than $e$, each once, and $pos[g]$ is the index of $g$ for each of them.

*Proof.* Let $k = |L| - 1$ be the index of the last cell and $f = L[k]$, and let $i = pos[e]$. If $i = k$, then $f = e$, line L12 writes $e$ over itself, and line L13 removes the last cell, which holds the only copy of $e$; the other names keep their cells. If $i < k$, then $f \ne e$. Line L12 writes $f$ into cell $i$ and sets $pos[f] = i$, so $f$ now occurs at cells $i$ and $k$, and $e$ occurs nowhere. Line L13 removes cell $k$. Now $f$ occurs once, at index $i = pos[f]$, and each other name $g \ne e, f$ is in its old cell, which is below $k$ and is not cell $i$. In both cases the claim holds. $\square$

**ADD-EDGE.** Line L1 picks $e = |tail|$, a name that no row of the table had, so by (I3) no list holds $e$. Line L2 appends $e$ to $out[u]$ and sets $pos_{out}[e]$ to its index; line L3 does the same in $in[v]$. So $e$ meets (I1) and (I2) with $tail[e] = u$ and $head[e] = v$. No other cell of any list moves, so (I1) and (I2) still hold for the other live edges, and (I3) holds because $e$ is live.

**REMOVE-EDGE.** Let $e$ be live, $u = tail[e]$ and $v = head[e]$. By (I1), the list $out[u]$ meets the condition of Lemma 1 for $e$ and $pos_{out}$: each name in it is live by (I3), so each occurs once at its recorded index by (I1). By Lemma 1, after line L8 the list $out[u]$ holds its old names without $e$, at their recorded indices. Line L9 does the same for $in[v]$ by (I2). These are the only lists that change, so (I1) and (I2) hold for each live edge other than $e$. Line L10 makes $e$ not live, and $e$ is in no list: it was only in $out[u]$ and $in[v]$, by (I1) and (I2), and it was removed from both. So (I3) holds. A self-loop, with $u = v$, needs no special case, because $out[u]$ and $in[u]$ are two different lists.

**INCIDENT.** Let $v$ be a vertex of an undirected graph. The edges incident to $v$ are the live $e$ with $tail[e] = v$ or $head[e] = v$. By (I1) and (I3), $out[v]$ holds exactly the live $e$ with $tail[e] = v$, each once; by (I2) and (I3), $in[v]$ holds exactly the live $e$ with $head[e] = v$, each once. Line L5 reports each $e$ of $out[v]$ with its other end $head[e]$, and line L6 each $e$ of $in[v]$ with its other end $tail[e]$. So each non-loop edge at $v$ is reported once, and each self-loop at $v$, which is in both lists, twice. The number of reports is $|out[v]| + |in[v]| = d(v)$, the degree with a self-loop counted twice. In a directed graph only line L5 runs, and it reports exactly the edges that leave $v$, each once.

**Sum of degrees.** By (I1) to (I3), each live edge has exactly one cell in the $out$ lists and one in the $in$ lists, so $\sum_v (|out[v]| + |in[v]|) = 2m$, where $m$ is the number of live edges.

**FIND-EDGE.** In a directed graph, an edge from $u$ to $v$ is a live $e$ with $tail[e] = u$ and $head[e] = v$. By (I1) and (I3), each such $e$ is in $out[u]$, and by (I2) and (I3), each is in $in[v]$. So a scan of either list for a name with the right other end finds such an edge if and only if one exists. In an undirected graph an edge between $u$ and $v$ is incident to both, so by the INCIDENT case a scan of the incident edges of either end finds it if and only if it exists.

**Cost.** Lines L1 to L4 are a constant number of appends, each $O(1)$ amortized for a dynamic array. Lines L7 to L13 are a constant number of array reads and writes, so REMOVE-EDGE is $O(1)$. INCIDENT does $O(1)$ work for each of the $d(v)$ cells it reads, plus $O(1)$. FIND-EDGE reads at most the length of the shorter list, plus $O(1)$. The structure has $2n$ lists, $2m'$ cells and $m'$ table rows, where $m' \ge m$ is the number of names ever given; with no removals $m' = m$, and the space is $\Theta(n + m)$. $\square$
