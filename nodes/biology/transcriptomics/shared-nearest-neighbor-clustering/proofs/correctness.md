---
title: The shared neighbor weights are bounded, and the Louvain phase raises the modularity at every move and stops
proves: [correctness]
status: full
---

The clustering has no ground truth to be correct against: whether the communities of the graph are the cell types is a modelling question, which the tests measure on simulated data. What can be proved is what the steps compute. We show that every edge of the k-nearest-neighbor graph gets a Jaccard weight between $1/(2k+1)$ and 1 (Lemma 1), that the gain of the moving phase is the change of modularity (Lemma 2), that aggregation keeps the modularity (Lemma 3), and that the method stops with a partition whose modularity grew at each level, which no single move of a vertex of the last level can improve, and which never joins two connected components (Theorem 4). Maximizing modularity is NP-hard (Brandes et al. 2008), so the method is a heuristic and the proof gives no bound on the gap to the optimum.

**Setting.** Points $p_1, \dots, p_n$, the rows after line L1. Line L2 sets $N(i)$, the $k$ nearest other points of $i$, with ties broken by index, and $N^+(i) = N(i) \cup \{i\}$. Line L3 takes the edges $\{i, j\}$ with $j \in N(i)$ or $i \in N(j)$, and line L4 gives the weight $w_{ij} = |N^+(i) \cap N^+(j)| / |N^+(i) \cup N^+(j)|$. For a symmetric weight matrix $A$ with $A_{ij} \ge 0$, let $k_i = \sum_j A_{ij}$ and $2m = \sum_{i,j} A_{ij}$, with sums over ordered pairs. The modularity of a labeling $c$ at resolution $\gamma \ge 0$ is
$$Q(c) = \frac{1}{2m}\sum_{i,j}\Big(A_{ij} - \gamma\frac{k_ik_j}{2m}\Big)[c_i = c_j].$$
For the graph of line L4, which has no self-loops, this is the usual $\sum_C \big(L_C/m - \gamma(d_C/2m)^2\big)$, with $L_C$ the weight of the edges inside $C$ and $d_C$ the sum of the degrees in $C$.

**Lemma 1 (weights).** Every edge of line L3 has $1/(2k+1) \le w_{ij} \le 1$.

*Proof.* Let $j \in N(i)$. Then $j \in N^+(i)$ and $j \in N^+(j)$, so the intersection is not empty. Both sets have $k+1$ elements, so the union has at most $2(k+1) - 1 = 2k + 1$ elements. A ratio of a subset size to a superset size is at most 1. $\square$

So the weight of an edge is high when the two cells share most of their neighbors and low for an edge that crosses between two dense groups, where each end has its neighbors on its own side. With $N(i)$ in place of $N^+(i)$, as in PhenoGraph, an edge can get the weight 0.

**Lemma 2 (the gain of line L7).** Let vertex $i$ be alone in its community, let $C$ be a community not holding $i$, let $k_{i,C} = \sum_{j \in C}A_{ij}$, and let $\Sigma_C = \sum_{j \in C}k_j$. Moving $i$ into $C$ changes $Q$ by
$$\Delta Q = \frac{1}{m}\Big(k_{i,C} - \gamma\frac{k_i\Sigma_C}{2m}\Big).$$

*Proof.* The move adds to the sum the ordered pairs $(i, j)$ and $(j, i)$ for $j \in C$. Each pair adds $A_{ij} - \gamma k_ik_j/2m$, so the sum grows by $2k_{i,C} - 2\gamma k_i\Sigma_C/2m$. Divide by $2m$. The pair $(i, i)$ is in one community before and after, so it does not change. $\square$

Line L6 removes $i$ from its community $c_0$, which makes $i$ alone, and then line L7 compares the gains $g(C) = k_{i,C} - \gamma k_i\Sigma_C/2m$ of the neighboring communities and of $c_0$ itself. The factor $1/m$ is the same for all, so the largest gain is the largest $\Delta Q$. The code moves $i$ only when another community beats $c_0$ by more than $\varepsilon = 10^{-12}$, so each move raises $Q$ by more than $\varepsilon/m$.

**Lemma 3 (aggregation).** Let $c$ label the vertices with communities $0, \dots, r-1$, and let line L9 form $B_{CD} = \sum_{c_i = C,\, c_j = D}A_{ij}$. Then $B$ has the same total $2m$, the degree of $C$ in $B$ is $\sum_{c_i = C}k_i$, and for every labeling $d$ of the communities, $Q_B(d) = Q_A(d \circ c)$.

*Proof.* Each ordered pair $(i, j)$ adds $A_{ij}$ to exactly one entry $B_{c_ic_j}$, which gives the total and the degrees. In $Q_A(d \circ c)$, group the pairs $(i, j)$ by $(c_i, c_j) = (C, D)$. The condition $d_{c_i} = d_{c_j}$ depends only on $(C, D)$, the sum of $A_{ij}$ over the group is $B_{CD}$, and the sum of $k_ik_j$ is $K_CK_D$ with $K_C$ the degree of $C$. This is $Q_B(d)$ term by term. $\square$

This is why the code stores the self-loop weight of $C$ as the sum over ordered pairs inside $C$: then the formula of $Q$ needs no special case for self-loops.

**Theorem 4 (Louvain).** The method of lines L5 to L11 stops. The modularity of the input labeling after each level is strictly larger than after the level before, starting from the labeling with one vertex per community. At the end, no move of one vertex of the last graph from its community to a neighboring community raises $Q$ by more than $\varepsilon/m$. Two vertices in different connected components are never in one community, and with $\gamma = 0$ the communities are exactly the connected components, leaving out isolated vertices.

*Proof.* By Lemma 2 each move raises $Q$ of the current graph by more than $\varepsilon/m$, and by Lemma 3 this is the $Q$ of the input labeling. $Q$ is at most 1, so there are finitely many moves, the loop of line L8 stops, and each level with a move raises $Q$. The number of vertices does not grow and falls at each level with a move, because a move empties a community or joins two, so the levels stop too. The last level ends in line L10 when a full pass makes no move. In that pass every vertex starts alone (each vertex of the last graph is its own community), and no community beat staying by more than $\varepsilon$, so no single move raises $Q$ by more than $\varepsilon/m$. A vertex only joins communities with $k_{i,C} > 0$, that is, with an edge to it. By induction every community, and every vertex of every aggregated graph, lies in one connected component, so no community crosses two components. With $\gamma = 0$ the gain of a neighboring community is $k_{i,C} > 0$ and the gain of staying alone is 0. So if, at the last level, two vertices of one component were in different communities, some edge would join two of them, and the pass would move one of its ends. So at the end each component with an edge is one community. $\square$

Theorem 4 says nothing about the vertices of the input graph. A merge at a later level can make an input vertex better off in another community, and Traag, Waltman and van Eck (2019) show that the Louvain method can even return a community that is not connected inside. The Leiden algorithm adds a refinement step that rules this out.

**What the lines compute.** Line L1 is optional principal component analysis. Line L2 is the brute force neighbor search of the shared module, with ties by index. Lines L3 and L4 are Lemma 1. Lines L5 to L8 are the moving phase with the gain of Lemma 2, visiting vertices in index order and taking the community with the smaller label on ties. Line L9 is Lemma 3, line L10 the stop test of Theorem 4, and line L11 returns the labels of the input vertices.

**Complexity.** The neighbor search takes $O(n^2d)$ time for $d$ coordinates, and lines L3 and L4 take $O(nk^2)$ expected time with hash sets, for at most $nk$ edges. One pass of line L6 over all vertices takes $O(|E|\log k_{max})$ time, with $|E| \le nk$, because the communities next to a vertex are sorted. The number of passes and levels is finite by Theorem 4, but the proof gives no useful bound on it; the tests count them on small graphs.

**What the tests check.** The test file checks the page example, the bounds of Lemma 1 for $k = 1, 3, 6$, the modularity formula against the edge form, Lemma 3 on random graphs, that the moving phase ends where no single move raises $Q$, and that the levels raise $Q$ strictly. It compares the method with an exhaustive search over all partitions of graphs with at most 8 vertices: the result is never above the optimum, and it reaches it on at least 80 percent of the random graphs, which is a measurement. It checks that components are never merged and that $\gamma = 0$ gives the components. A simulation with three groups of cells measures that $k = 15$ finds the groups and that $k = 10$ splits one group but never mixes two.
