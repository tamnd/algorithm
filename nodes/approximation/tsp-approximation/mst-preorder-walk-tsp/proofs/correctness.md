---
title: The MST preorder walk is a shortcut full walk and costs at most 2(1 − 1/n) OPT
proves: [correctness]
status: full
---

The costs $c$ on $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. $T$ is a minimum spanning tree rooted at $r$, and each vertex $v$ has an ordered list of children $u_1, \ldots, u_k$. For a walk $P = (p_0, \ldots, p_m)$, $c(P) = \sum_{i=1}^{m} c(p_{i-1}, p_i)$.

**Definitions.** The preorder of the subtree $T_v$ is $\text{pre}(v) = v, \text{pre}(u_1), \ldots, \text{pre}(u_k)$. The full walk of $T_v$ is $\text{full}(v) = v, \text{full}(u_1), v, \text{full}(u_2), v, \ldots, \text{full}(u_k), v$, where each $\text{full}(u_i)$ starts and ends at $u_i$. For a leaf both are the single vertex $v$.

**Lemma 1 (the loop computes the preorder).** At the end, $H = \text{pre}(r)$.

*Proof.* We show the invariant: the list $H$ followed by $\text{pre}(s_1), \text{pre}(s_2), \ldots, \text{pre}(s_t)$, where $s_1, \ldots, s_t$ is the stack read from the top down, equals $\text{pre}(r)$. After line L2, $H$ is empty and the stack is $(r)$, so it holds. A step of lines L4 to L6 pops $s_1 = v$, appends $v$ to $H$ and pushes the children of $v$ so that $u_1$ is on top. The new list is $H, v, \text{pre}(u_1), \ldots, \text{pre}(u_k), \text{pre}(s_2), \ldots$, which by the definition of $\text{pre}(v)$ is the old list. Each step removes one vertex from the stack for good, because a vertex is a child of only one parent, so the loop stops after $n$ steps with an empty stack, and then $H = \text{pre}(r)$. $\square$

**Lemma 2 (the full walk).** $\text{full}(r)$ is a closed walk that uses each edge of $T$ exactly two times, so $c(\text{full}(r)) = 2\,c(T)$. Its list of first visits is $\text{pre}(r)$.

*Proof.* By induction on the height of $T_v$. The walk $\text{full}(v)$ uses the edge $\{v, u_i\}$ two times, once into $\text{full}(u_i)$ and once out of it, and by induction it uses each edge of $T_{u_i}$ two times inside $\text{full}(u_i)$. The subtrees are disjoint, so no other edge is used. For the first visits: $v$ comes first, and the vertices of $T_{u_i}$ appear for the first time inside $\text{full}(u_i)$, in the order $\text{pre}(u_i)$ by induction. The repeated copies of $v$ are not first visits. So the first visits are $v, \text{pre}(u_1), \ldots, \text{pre}(u_k) = \text{pre}(v)$. $\square$

**Lemma 3 (each Euler circuit is a full walk).** Each Euler circuit $W$ of the doubled tree that starts at $r$ equals $\text{full}(r)$ for some order of the children.

*Proof.* Take a tree edge $\{u, v\}$ with $u$ the parent of $v$. Deleting it splits $T$ into $T_v$ and a part that holds $r$. The walk $W$ starts and ends outside $T_v$, and it can cross between the two parts only on the two copies of $\{u, v\}$. So it crosses down one time, stays in $T_v$, and crosses up one time. While it is in $T_v$ it uses all edges of $T_v$ two times, because no other part of $W$ enters $T_v$. So the visit to $T_v$ is an Euler circuit of the doubled $T_v$ from $v$, and induction on the size of the subtree, with the children ordered by the time of their visits, gives the claim. $\square$

So the preorder walk and the double-tree algorithm have the same set of possible outputs.

**Lemma 4 (shortcuts).** Let $W = (w_0, \ldots, w_L)$ be a closed walk with $w_0 = w_L$ that visits each vertex, and let $H = (h_1, \ldots, h_n)$ be its list of first visits. Then $c(H) \le c(W)$, where $c(H)$ includes the closing edge $c(h_n, h_1)$.

*Proof.* For each walk $(p_0, \ldots, p_m)$, induction on $m$ with the triangle inequality gives $c(p_0, p_m) \le c(p_0, \ldots, p_m)$. Let $h_i$ first appear at index $j_i$, so $0 = j_1 < j_2 < \cdots < j_n \le L$. Then $c(h_i, h_{i+1}) \le c(w_{j_i}, \ldots, w_{j_{i+1}})$ for $i < n$, and $c(h_n, h_1) \le c(w_{j_n}, \ldots, w_L)$ because $w_L = w_0 = h_1$. These parts of $W$ do not overlap, so the sum gives $c(H) \le c(W)$. $\square$

**Lemma 5 (the lower bound).** $c(T) \le (1 - 1/n) \cdot \text{OPT}$.

*Proof.* An optimal tour has $n$ edges, so its most costly edge costs at least OPT$/n$. Without that edge, the tour is a spanning path, so a spanning tree, of cost at most $(1 - 1/n) \cdot \text{OPT}$. The minimum spanning tree costs no more. $\square$

**Theorem.** APPROX-TSP-TOUR returns a tour of cost at most $2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$.

*Proof.* By Lemma 1 the output is $\text{pre}(r)$, which holds each vertex one time, so it is a tour. By Lemma 2 it is the list of first visits of $\text{full}(r)$, a closed walk of cost $2\,c(T)$ that visits each vertex. By Lemma 4 the tour costs at most $2\,c(T)$, and by Lemma 5 this is at most $2(1 - 1/n) \cdot \text{OPT}$. $\blacksquare$
