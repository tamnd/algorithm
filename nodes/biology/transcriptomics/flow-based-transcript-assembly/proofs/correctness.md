---
title: The heaviest-path and max-flow loop stops, returns paths of the splice graph, and never assigns more reads than the fragments hold
proves: [correctness]
status: full
---

We use the pseudocode of the page. $G$ is a DAG on the nodes $1, \ldots, n$ with every edge $(u, v)$ having $u < v$. Each fragment $f$ is a path of $G$ with at least two nodes and a weight $w(f) \ge 0$, and $W(v)$ is the total weight of the fragments that hold $v$. $c_{\min} > 0$ is the threshold. A fragment $f$ is *explained* by a path $P = (v_1, \ldots, v_m)$ if $f = (v_a, \ldots, v_b)$ is a contiguous part of $P$; then $a < b$.

The network $N(P)$ of line L7 has a source $s$, a sink $t$, and for each $i$ two nodes $\mathrm{in}_i$ and $\mathrm{out}_i$. Its edges are $\mathrm{in}_i \to \mathrm{out}_i$ with capacity $c_i$, the total weight of the explained fragments that hold $v_i$; one edge $\mathrm{out}_a \to \mathrm{in}_b$ with capacity $w(f)$ for each explained fragment $f = (v_a, \ldots, v_b)$ of positive weight; and $s \to \mathrm{in}_1$ and $\mathrm{out}_m \to t$ with a capacity larger than the total weight.

## 1. The paths are paths of $G$

**Lemma 1.** Every path $P$ that lines L4 to L6 build is a path of $G$.

*Proof.* Line L4 starts with one node. Line L5 only prepends a predecessor $u$ of the first node of $P$, that is, a node with an edge $(u, \mathrm{first}(P))$, and line L6 only appends a successor of the last node. So consecutive nodes are joined by edges. The extensions stop, because each one adds a node with a smaller id (line L5) or a larger id (line L6), and the ids are in $1..n$. $\square$

## 2. The flow is well defined and is a set of fragment chains

$N(P)$ is a DAG: the order $s, \mathrm{in}_1, \mathrm{out}_1, \mathrm{in}_2, \mathrm{out}_2, \ldots, \mathrm{out}_m, t$ is topological, because each fragment edge goes from $\mathrm{out}_a$ to $\mathrm{in}_b$ with $a < b$. It has no pair of opposite edges, so the Edmonds-Karp algorithm of line L7 returns a maximum flow $\varphi$ and a flow $g$ on each edge, with $0 \le g_f \le w(f)$ on each fragment edge, by the max-flow min-cut theorem.

**Lemma 2.** Every unit of the flow follows a chain of explained fragments $f_1, \ldots, f_r$ in which $f_1$ starts at $v_1$, $f_r$ ends at $v_m$, and each $f_{j+1}$ starts at the node where $f_j$ ends. The value $\varphi$ equals the total flow on the fragment edges that leave $\mathrm{out}_1$.

*Proof.* A flow in a DAG splits into flows along $s$-$t$ paths. An $s$-$t$ path of $N(P)$ enters at $\mathrm{in}_1$, and from each $\mathrm{in}_i$ the only edge goes to $\mathrm{out}_i$. From $\mathrm{out}_i$ with $i < m$ the only edges are the fragment edges that start at $v_i$, and from $\mathrm{out}_m$ the edge to $t$. So the path is $s, \mathrm{in}_1, \mathrm{out}_1$, a fragment edge to some $\mathrm{in}_b$, then $\mathrm{out}_b$, and so on until $\mathrm{out}_m$ and $t$. This is the chain of the claim. All flow from $s$ passes $\mathrm{out}_1$, and if $m > 1$ it leaves $\mathrm{out}_1$ only on fragment edges. If $m = 1$, no fragment is explained, so $c_1 = 0$ and $\varphi = 0$. $\square$

So $\varphi$ is the largest number of reads that can be placed on $P$ as chains of explained fragments from the first node to the last, such that no fragment is used more often than its weight and no node more often than the weight of the fragments that hold it. It is a measure of the abundance of $P$ in the model, not a proof that $P$ is a transcript.

## 3. Weights stay valid, and the loop stops

**Lemma 3.** All weights stay at least 0. The sum of the abundances returned is at most the total initial weight.

*Proof.* Line L9 lowers $w(f)$ by $g_f \le w(f)$, and line L10 sets weights to 0. In a round that adds $(P, \varphi)$, the total weight falls by $\sum_f g_f \ge \varphi$, by Lemma 2, because the fragment edges that leave $\mathrm{out}_1$ are among all fragment edges. Adding over the rounds, the sum of the returned abundances is at most the total fall of the weight, which is at most the initial total. $\square$

**Theorem 1.** The loop stops after at most $\lfloor W_0 / c_{\min} \rfloor + 1$ rounds, where $W_0$ is the total initial weight. When it stops, every node has $W(v) < c_{\min}$.

*Proof.* Consider one round, with start node $v^*$ and $W(v^*) \ge c_{\min}$ by line L2. If line L8 accepts, the total weight falls by at least $\varphi \ge c_{\min}$ (Lemma 3). If not, line L10 sets to 0 every fragment that holds $v^*$, and these fragments have total weight $W(v^*) \ge c_{\min}$. In both cases the total weight, which is never negative, falls by at least $c_{\min}$. So there are at most $W_0 / c_{\min}$ rounds, and the loop ends only when the test of line L2 fails. $\square$

**Theorem 2.** Every returned pair $(P, \varphi)$ has a path $P$ of $G$ with at least two nodes and $\varphi \ge c_{\min}$.

*Proof.* $P$ is a path of $G$ by Lemma 1. Line L9 runs only when $\varphi \ge c_{\min} > 0$, and $\varphi > 0$ needs an explained fragment by Lemma 2, which has at least two nodes, so $m \ge 2$. $\square$

## 4. What is not true

The loop is a greedy heuristic. It does not find the fewest paths that explain the weights, and it does not always find the true transcripts. With only junction reads, the transcripts $v_1 v_2 v_3 v_4 v_5$ with 10 reads per junction and $v_1 v_3 v_5$ with 20 give the weights $v_1 v_2 = v_2 v_3 = v_3 v_4 = v_4 v_5 = 10$ and $v_1 v_3 = v_3 v_5 = 20$. The loop returns three paths, $v_1 v_3 v_4 v_5$, $v_1 v_2 v_3 v_5$ and $v_1 v_3 v_5$, each with 10, which explain the weights as well as the two true ones. No method can tell these apart from these weights alone, because both are flow decompositions of the same flow. Finding a decomposition into the fewest paths is NP-hard in the strong sense, even on DAGs (Vatinlen, Chauvet, Chrétienne and Mahey 2008). $\blacksquare$
