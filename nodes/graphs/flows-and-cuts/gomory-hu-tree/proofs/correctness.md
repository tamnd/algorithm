---
title: Gusfield's method builds a Gomory-Hu tree, and the queries read it correctly
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be undirected with $V = \{0, \dots, n - 1\}$ and weights $w \ge 0$. For $A \subseteq V$, $c(A)$ is the total weight of edges with exactly one end in $A$, so $c(A) = c(V \setminus A)$, and $\lambda(a, b)$ is the least $c(A)$ with $a \in A$, $b \notin A$. We use two facts proved on the page of the [Gomory-Hu algorithm](/gomory-hu-algorithm/): **submodularity**, $c(A) + c(B) \ge c(A \cap B) + c(A \cup B)$, and the **triangle inequality**, $\lambda(a, c) \ge \min(\lambda(a, b), \lambda(b, c))$.

**Termination.** BUILD runs the loop of line L2 exactly $n - 1$ times; each iteration runs one maximum flow, which terminates, and a constant number of loops over the vertices. LIGHTEST ends because each iteration replaces the deeper of $u$, $v$ by its parent, which lowers $depth[u] + depth[v]$, and the walk stops at their lowest common ancestor.

**Subtrees.** For a vertex $k \ne 0$, let $D_k$ be the set of vertices whose chain of parents passes through $k$, including $k$.

**Invariant.** Before the iteration with $s$ (and at the end, with $s = n$), call $0, \dots, s - 1$ processed. Then: (a) the parent of every vertex other than 0 is processed and following parents from any vertex reaches 0; (b) for every processed $k \ne 0$, $\lambda(k, parent[k]) = weight[k] = c(D_k)$.

Read it as a tree $T$ whose nodes are the groups $N_k = \{k\} \cup \{j \ge s : parent[j] = k\}$ for processed $k$, with an edge $(N_k, N_{parent[k]})$ of weight $weight[k]$ and witness pair $(k, parent[k])$. The set $D_k$ is then the union of the groups on the side of $N_k$ when that edge is removed.

At the start only 0 is processed, every parent is 0, and (b) is empty. Assume the invariant before the iteration with $s$, and let $t = parent[s]$, which is processed, so $s \in N_t =: X$. Let $Z$ be the cut of line L4, a minimum $s$-$t$ cut with $s \in Z$, $t \notin Z$.

The components of $T - X$ are: for each processed child $k$ of $t$, the component with vertex set $D_k$ and top vertex $k$; and, if $t \ne 0$, the component containing $parent[t]$, with vertex set $V \setminus D_t$ and top vertex $y = parent[t]$. Each is a minimum cut between its top vertex $y$ and a vertex $x$ of $X$: for a child $k$, $D_k$ is a minimum $k$-$t$ cut by (b); for the parent side, $V \setminus D_t$ is a minimum $parent[t]$-$t$ cut by (b). Call this set $D$ in each case; it is disjoint from $X$, contains $y$, and does not contain $x = t$.

**Claim 1.** There is a minimum $s$-$t$ cut $Z'$ with $Z' \cap X = Z \cap X$ such that for every component $D$, $D \subseteq Z'$ if its top vertex $y \in Z$, and $D \cap Z' = \emptyset$ otherwise. *Proof.* Treat the components one by one. If $y \in Z$: the set $Z \cap D$ contains $y$ and not $x$, so $c(Z \cap D) \ge c(D)$; submodularity gives $c(Z \cup D) \le c(Z)$, and $Z \cup D$ contains $s$ and not $t$, so it is again a minimum $s$-$t$ cut. If $y \notin Z$: the set $Z \cup (V \setminus D)$ contains $x$ and not $y$, so its value is at least $c(D) = c(V \setminus D)$; submodularity gives $c(Z \setminus D) \le c(Z)$, and $Z \setminus D$ contains $s$, not $t$. Each step only adds or removes a whole $D$, which is disjoint from $X$ and from the other components, so it does not change $Z \cap X$, the membership of other top vertices, or components already treated. $\square$

**Claim 2.** If the top vertex $y$ of a component $D$ lies in $Z$, then $\lambda(s, y) = c(D)$. *Proof.* By Claim 1, $D \subseteq Z'$, so $D$ contains $y$ and not $s$, and $\lambda(s, y) \le c(D)$. Let $W$ be a minimum $s$-$y$ cut with $y \in W$, $s \notin W$. If $t \notin W$, then $W$ separates $t$ from $y$ and $c(W) \ge \lambda(t, y) = c(D)$. If $t \in W$, then $W \cup (V \setminus Z')$ contains $t$ and not $s$, so its value is at least $c(Z') = \lambda(s, t)$, and submodularity gives $c(W \cap (V \setminus Z')) \le c(W)$; that set contains $t$ and not $y$, so $c(W) \ge \lambda(t, y) = c(D)$. Hence $\lambda(s, y) = c(D)$. $\square$

**The update.** Lines L5 and L6 set $parent[v] \leftarrow s$ for every $v \ne s$ with $parent[v] = t$ and $v \in Z$. For an unprocessed $v$ this moves it from the group of $t$ to the group of $s$, so the new groups are $N_s = X \cap Z$ and $N_t = X \setminus Z$. For a processed child $k$, this moves the component $D_k$ to hang below $s$ exactly when its top vertex $k$ lies in $Z$. Lines L7 and L8 do the same for the parent component: if $parent[t] \in Z$, it hangs on $s$ instead of $t$, and $t$ goes below $s$. Now compute the new subtrees.

- The edge between $s$ and $t$. If there is no swap, $parent[s] = t$ and $D_s$ is $N_s$ together with the components below $s$, which is $Z'$. If there is a swap, $parent[t] = s$ and $D_t$ is $N_t$ together with the components on the side of $t$, which is $V \setminus Z'$. Either way the edge has weight $\lambda$, which is $\lambda(s, t) = c(Z') = c(V \setminus Z')$ by Claim 1, so (b) holds for it.
- A child $k$ of $t$ that stays: $D_k$ is unchanged, its witness $(k, t)$ is unchanged.
- A child $k$ moved to $s$: $D_k$ is unchanged, and by Claim 2 $\lambda(k, s) = c(D_k) = weight[k]$.
- The parent edge after a swap: the edge is now $(s, parent[s])$ with $parent[s]$ the old $parent[t]$ and $weight[s]$ the old $weight[t]$. Its subtree $D_s$ is $V$ minus the parent component, the same set as the old $D_t$, so $c(D_s)$ equals the old $weight[t]$, and by Claim 2, $\lambda(s, parent[s])$ equals it too. Without a swap the parent edge of $t$ is unchanged.
- All other edges keep their subtrees.

After the update $s$ is processed, every parent is processed, and the parent chains still reach 0: the only changes point vertices at $s$, whose own chain avoids them, or make $s$ the parent of $t$ while $s$ takes the old parent of $t$. So the invariant holds before the next iteration.

**The tree at the end.** After the last iteration every vertex is processed and every group is a single vertex. For each edge $(k, parent[k])$, (b) says $\lambda(k, parent[k]) = weight[k] = c(D_k)$. Take $u \ne v$ and the tree path $u = x_0, \dots, x_r = v$. Each edge on the path has a subtree containing exactly one of $u$, $v$, so $\lambda(u, v)$ is at most its weight. By the triangle inequality along the path, $\lambda(u, v) \ge \min_i \lambda(x_{i-1}, x_i)$, the least edge weight on the path. So $\lambda(u, v)$ equals the least weight on the path, and the subtree of a lightest path edge, or its complement, is a minimum $u$-$v$ cut.

**The queries.** LIGHTEST moves the deeper of $u$ and $v$ to its parent until they meet; the edges $(u, parent[u])$ it passes are exactly the edges of the tree path, each once, and it returns the lower end $b$ of a lightest one. MIN-CUT-VALUE returns $weight[b] = \lambda(u, v)$. MIN-CUT returns $D_b$ or its complement, whichever holds $u$; it does not hold $v$, since the edge $(b, parent[b])$ lies on the path, and its value is $c(D_b) = weight[b] = \lambda(u, v)$. GLOBAL-MIN-CUT picks the lightest edge of the tree; every global cut separates some pair $u, v$ and so has value at least $\lambda(u, v)$, which is at least the lightest tree weight, and $D_b$ attains it. $\blacksquare$
