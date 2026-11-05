---
title: OPTIMAL-MSF returns the minimum spanning forest for every behaviour of the soft heap
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite undirected multigraph with real weights; self-loops, parallel edges, ties and several components are allowed. Order the edges by the key $(w(e), \text{index of } e)$, so that all keys are distinct, and let $\operatorname{MSF}(H)$ be the unique minimum spanning forest of a graph $H$ for this order. Then OPTIMAL-MSF$(G)$ stops and returns $\operatorname{MSF}(G)$, whichever keys the soft heap corrupts. With ties in $w$, $\operatorname{MSF}(G)$ is a minimum spanning forest for $w$, since Kruskal's algorithm with the key order is a valid run of Kruskal's algorithm for $w$.

The running time bound $O(T^\ast(m, n))$ is the main theorem of Pettie and Ramachandran and is not proved here.

## Facts about minimum spanning forests

All graphs below have distinct keys. Contracting edges keeps the edge identities, and self-loops are removed after a contraction.

**Fact 1 (cut property).** If $S \subseteq V$ and $e$ is the least edge of $H$ with exactly one end in $S$, then $e \in \operatorname{MSF}(H)$.

**Fact 2 (subgraphs).** If $H' \subseteq H$ and $e \in \operatorname{MSF}(H) \cap H'$, then $e \in \operatorname{MSF}(H')$. *Proof.* An edge is outside the MSF of a graph if and only if it is the largest edge on some cycle of that graph (cycle property). A cycle of $H'$ is a cycle of $H$, so if $e$ were the largest edge on a cycle of $H'$, it would not be in $\operatorname{MSF}(H)$. $\square$

**Fact 3 (contraction).** If $F \subseteq \operatorname{MSF}(H)$, then $\operatorname{MSF}(H) = F \cup \operatorname{MSF}(H / F)$.

*Proof of Fact 3.* Let $T = \operatorname{MSF}(H)$ and $c$ the number of components of $H$, so $|T| = |V(H)| - c$. The set $T \setminus F$ is a forest of $H / F$: a cycle in it would lift to a cycle in $T$ through edges of $F$. It has $|T| - |F|$ edges, and $H/F$ has $|V(H)| - |F|$ vertices (each edge of the forest $F$ merges two vertices) and $c$ components, so $T \setminus F$ is a spanning forest of $H / F$. It is the minimum one: for $e \in (H/F) \setminus (T \setminus F)$, $e \notin T$, so $e$ is the largest edge on the cycle formed by $e$ and the path of $T$ between its ends (cycle property for spanning forests); contracting $F$ maps this cycle to a closed walk in $H/F$ through $e$ whose other edges are in $T \setminus F$ and lighter than $e$, which contains a cycle through $e$ (the edge $e$ is not a self-loop of $H/F$, since $e \in H / F$). So every edge of $H/F$ outside $T \setminus F$ is the largest on a cycle of $H/F$, and $T \setminus F = \operatorname{MSF}(H/F)$. $\square$

**Fact 4 (sandwich).** If $\operatorname{MSF}(H) \subseteq H' \subseteq H$, then $\operatorname{MSF}(H') = \operatorname{MSF}(H)$. *Proof.* By Fact 2, $\operatorname{MSF}(H) \subseteq \operatorname{MSF}(H')$. Both are spanning forests with the components of $H$, since $H'$ contains $\operatorname{MSF}(H)$ and lies inside $H$, so they have the same number of edges and are equal. $\square$

## Step 1: the forest F of line L4 lies in MSF(G \ C)

Consider the growth of one piece $S$ in PARTITION. Let $C$ be the final corrupted set of the call, which contains every edge whose key was raised in any heap.

**Lemma 1.** At each extraction of an uncorrupted edge $e$ from the heap of $S$, $e$ has the least key among the edges of $G \setminus C$ with exactly one end in $S$.

*Proof.* Let $f \ne e$ be an edge of $G \setminus C$ with one end $x \in S$ and the other end $y \notin S$. When $x$ joined $S$, $y$ was not in $S$, and $f$ was not in $C$ (it is never in $C$), so $f$ was inserted. It has not been extracted: an extracted edge is put into $C$ (if corrupted), skipped because both ends are in $S$, used as a link (which ends the growth), or used to grow $S$ (which puts its other end in $S$); none of these fits $f$. So $f$ is in the heap, with its true key, since it is not in $C$. The heap returns the least current key, and $e$ is uncorrupted, so the key of $e$ is less than the key of $f$. $\square$

By Fact 1 applied to $H = G \setminus C$, every edge that grows a piece and every link edge is in $\operatorname{MSF}(G \setminus C)$. Each growth edge has both ends in its piece and is not in $C$, so the growth edges of piece $i$ form a spanning tree $T_i$ of $M_i \setminus C$. By Fact 2, $T_i \subseteq \operatorname{MSF}(M_i \setminus C)$, and since $T_i$ spans the connected graph it lives in, $\operatorname{MSF}(M_i \setminus C) = T_i$. Lemma 1 also holds for earlier pieces after later pieces add edges to $C$, since adding edges to $C$ only removes competitors. No edge of $L$ or of a $T_i$ is ever put into $C$: it was extracted uncorrupted, and afterwards both of its ends are dead, so it never enters a heap again; a link edge that had been corrupted in an earlier heap would be in $C$ already and would not have been inserted. So

$$F = L \cup T_1 \cup \cdots \cup T_s \subseteq \operatorname{MSF}(G \setminus C).$$

## Step 2: G_B contains MSF(G)

By Fact 3 with $H = G \setminus C$, $\operatorname{MSF}(G \setminus C) = F \cup \operatorname{MSF}((G \setminus C)/F) = F \cup F_A$, where $F_A$ is the forest of line L6, read as edges of $G$. Each edge of $\operatorname{MSF}(G)$ is either in $C$, or in $G \setminus C$ and then, by Fact 2, in $\operatorname{MSF}(G \setminus C)$. So

$$\operatorname{MSF}(G) \subseteq F \cup F_A \cup C = G_B \subseteq G,$$

and by Fact 4, $\operatorname{MSF}(G_B) = \operatorname{MSF}(G)$.

## Step 3: the Borůvka steps and the recursion

In a Borůvka step on a graph $H$, each vertex chooses the least edge at it; by Fact 1 with $S$ the vertex, every chosen edge is in $\operatorname{MSF}(H)$. Contracting the chosen edges and applying Fact 3, $\operatorname{MSF}(H) = (\text{chosen}) \cup \operatorname{MSF}(H / \text{chosen})$. Two steps give $\operatorname{MSF}(G_B) = F_B \cup \operatorname{MSF}(G_C)$.

**Termination.** We use induction on the number of vertices. If $G$ has no edge other than self-loops, line L1 returns $\emptyset = \operatorname{MSF}(G)$. Otherwise $\operatorname{MSF}(G)$ is not empty and lies in $G_B$, so the first Borůvka step chooses at least one edge that is not a self-loop and $G_C$ has fewer vertices than $G$. By induction, line L9 returns $\operatorname{MSF}(G_C)$.

So line L10 returns $F_B \cup \operatorname{MSF}(G_C) = \operatorname{MSF}(G_B) = \operatorname{MSF}(G)$. The argument used no property of which keys the heap corrupts, so it holds for every soft heap, and also for an exact heap, where $C = \emptyset$. $\blacksquare$
