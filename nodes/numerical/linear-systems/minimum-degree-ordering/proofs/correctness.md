---
title: Minimum degree returns a permutation that greedily minimizes the current degree, the quotient graph computes the same degrees in bounded storage, and the approximate degree is an upper bound
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be the graph of a symmetric pattern, $|V| = n$, $|E| = m$. Line numbers refer to the pseudocode of the page. The elimination graphs are $G_0 = G$ and $G_k$, obtained from $G_{k-1}$ by deleting the $k$-th eliminated vertex $v_k$ and joining all its neighbours into a clique. $N_k(x)$ is the neighbourhood of $x$ in $G_k$ and $d_k(x) = |N_k(x)|$.

**Lemma 1 (the elimination graph models Cholesky; Parter, Rose).** Let $B = P A P^T$ be symmetric positive definite and assume no exact cancellation. Eliminating the first $k$ unknowns leaves a Schur complement whose graph is $G_k$, and column $k$ of the Cholesky factor has its off-diagonal nonzeros exactly at the neighbours $N_{k-1}(v_k)$. Hence the number of off-diagonal nonzeros of $L$ is $\sum_k d_{k-1}(v_k)$, and the fill is the number of clique edges that were not already present.

*Proof.* One step of elimination replaces $S$ by $S' = S_{22} - s_{21} s_{21}^T / s_{11}$. The entry $(i, j)$ of $s_{21}s_{21}^T$ is nonzero exactly when $i$ and $j$ are both neighbours of the pivot, so the pattern of $S'$ is the old pattern on the remaining vertices together with a clique on the neighbours of the pivot, unless a sum cancels exactly. The column of $L$ is $s_{21}/\sqrt{s_{11}}$, whose pattern is the neighbourhood of the pivot. $\square$

Without the no-cancellation assumption the same argument gives inclusion: the true pattern of $L$ is contained in the symbolic one. The tests check both, inclusion always and equality for random values, against an exact $LDL^T$ in rational arithmetic.

**Termination and permutation.** The heap holds pairs $(d, v)$. Invariant: for every uneliminated $v$ the heap holds the pair $(d_k(v), v)$. It holds initially, and after an elimination only the neighbours of the pivot change degree, and line L7 pushes their new pairs. A popped pair is used only if $v$ is uneliminated and $d$ equals its current degree; otherwise it is discarded. Each used pair eliminates a new vertex, and each iteration removes one pair from a heap that receives at most $n + \sum_k d_{k-1}(v_k)$ pairs in total, so the loop ends, and by the invariant it ends only after all $n$ vertices are appended. Each vertex is appended once, so the output is a permutation.

**Lemma 2 (greedy choice).** The vertex $v_k$ appended at line L4 minimizes $d_{k-1}$ over the uneliminated vertices, with ties broken by the smallest index.

*Proof.* By the invariant, the heap minimum over the valid pairs is $(\min_v d_{k-1}(v), \text{smallest such } v)$, and stale pairs either have an eliminated vertex or a degree that is no longer current, so they are skipped. Stale pairs that are smaller than every valid pair are popped first and discarded. $\square$

**Lemma 3 (quotient graph; George and Liu).** In the quotient graph version, each uneliminated variable $i$ keeps a set $A_i$ of variables and a set $E_i$ of elements, and each live element $e$ keeps a set $L_e$ of variables. Invariants after $k$ eliminations:

1. $e \in E_i$ if and only if $i \in L_e$;
2. for uneliminated $i \ne j$: $\{i, j\} \in G_k$ if and only if $j \in A_i$ or $i, j \in L_e$ for some live element $e$;
3. $A_i \cap L_e = \emptyset$ for every $e \in E_i$.

Consequently $N_k(i) = \mathrm{reach}(i) = \big(A_i \cup \bigcup_{e \in E_i} L_e\big) \setminus \{i\}$.

*Proof.* Initially there are no elements and $A_i = N_0(i)$. Suppose the invariants hold and $p$ is eliminated. By (2), $N(p) = A_p \cup \bigcup_{e \in E_p} L_e \setminus \{p\} = L_p$, the new element's list. The new graph adds the clique on $L_p$, which (2) now records through $L_p$. The absorbed elements $e \in E_p$ satisfy $L_e \setminus \{p\} \subseteq L_p$, so every pair they covered is still covered. Removing $L_p$ from $A_i$ loses only pairs inside the clique $L_p \ni i$, and removing $p$ loses only edges at the deleted vertex. So (2) holds. For (1), $p$ is added to $E_i$ exactly for $i \in L_p$, and the absorbed elements are removed from all lists. For (3), lists $A_i$ never grow, $A_i$ is pruned by $L_p$ when $p$ joins $E_i$, and an absorbed element's list is contained in its absorber's. $\square$

Hence the exact-degree quotient version computes the same degrees as the elimination graph and, with the same tie-breaking, returns the same order; the tests confirm this on 150 random graphs.

**Lemma 4 (storage).** The quantity $Z = \sum_{i \text{ uneliminated}} |A_i| + \sum_{e \text{ live}} |L_e|$ never increases, so it never exceeds its initial value $2m$.

*Proof.* When $p$ is eliminated, $|L_p| \le |A_p| + \sum_{e \in E_p}(|L_e| - 1)$, because each absorbed $L_e$ contains $p$, which is not in $L_p$. The lists $A_p$ and $L_e$, $e \in E_p$, are freed, and $L_p$ is added, so this part does not increase $Z$. The pruning of the $A_i$ only removes entries. $\square$

**Lemma 5 (the approximate degree).** Let $p$ be eliminated, let $i \in L_p$, let $r$ be the number of uneliminated variables after the step, and suppose $\bar d_i$ was an upper bound for the old degree of $i$. Then the new value
$$\bar d_i' = \min\Big(r - 1,\ \bar d_i + |L_p \setminus \{i\}|,\ |A_i| + |L_p \setminus \{i\}| + \sum_{e \in E_i,\ e \ne p} |L_e \setminus L_p|\Big)$$
satisfies $\bar d_i' \ge d(i)$, the exact new degree, with equality when $|E_i| \le 2$.

*Proof.* The first term bounds any degree. For the second, $N_{\text{new}}(i) = (N_{\text{old}}(i) \setminus \{p\}) \cup (L_p \setminus \{i\})$, so $d(i) \le d_{\text{old}}(i) - 1 + |L_p \setminus \{i\}| \le \bar d_i + |L_p \setminus \{i\}|$. For the third, by Lemma 3, $N(i) = A_i \cup (L_p \setminus \{i\}) \cup \bigcup_{e \ne p} (L_e \setminus L_p)$, where $i \notin A_i$, $i \in L_p$, and $A_i$ is disjoint from $L_p$ and from every $L_e$ by invariant (3). So the union is a disjoint union of $A_i$, $L_p \setminus \{i\}$ and the union of the sets $L_e \setminus L_p$, whose size is at most the sum, with equality when at most one $e \ne p$ is present, that is, when $|E_i| \le 2$. Then the third term is exact and the other two are upper bounds, so the minimum is exact. $\square$

The degrees used by AMD are therefore upper bounds, exact in the common case of at most two adjacent elements. The ordering produced need not equal the exact minimum degree ordering.

**Theorem (no fill on forests).** If $G$ is a forest, minimum degree produces no fill.

*Proof.* A forest has a vertex of degree at most $1$. Eliminating a vertex of degree $0$ or $1$ adds no edge and leaves a forest. By Lemma 2 the vertex chosen has degree at most $1$ at every step. $\square$

**What the greedy rule does not give.** Minimum degree does not minimize fill. Let $G$ consist of two cliques $\{0, 1, 2, 3\}$ and $\{5, 6, 7, 8\}$ and a vertex $4$ adjacent to $0$ and $5$. Vertex $4$ is the unique vertex of degree $2$, so it is eliminated first and creates the fill edge $\{0, 5\}$. The ordering $1, 2, 3, 6, 7, 8, 0, 4, 5$ eliminates only simplicial vertices and has no fill, so the graph is chordal and its minimum fill is $0$. Computing the minimum fill is NP-hard (Yannakakis, 1981), so no polynomial greedy rule can be optimal unless P = NP.
