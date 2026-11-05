---
title: Wilson's algorithm returns each spanning tree with probability proportional to the product of its weights
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite connected undirected multigraph with $n \ge 1$ vertices and a weight $c_e > 0$ on each edge; parallel edges and self-loops are allowed. For each root $r$ and each order of the vertices in line L2, WILSON stops with probability 1, and its output $T$ satisfies

$$\Pr[T = t] = \frac{c(t)}{Z}, \qquad c(t) = \prod_{e \in t} c_e, \qquad Z = \sum_{t'} c(t'),$$

for each spanning tree $t$, the sum over all spanning trees $t'$. With all weights 1, $\Pr[T = t] = 1 / \tau(G)$.

## Setup

For a vertex $x$, let $c(x)$ be the sum of $c_e$ over the edges at $x$, with a self-loop counted twice. A *step* at $x$ chooses an edge $e$ at $x$ with probability $c_e / c(x)$ (a self-loop with probability $2 c_e / c(x)$) and moves to its other end. An *arrow* at $x$ is an edge at $x$ read as pointing from $x$ to its other end.

A *rooted spanning tree* at $r$ is a choice of one arrow $a(x)$ at each $x \ne r$ such that following arrows from any vertex reaches $r$. Forgetting the directions gives a bijection between rooted spanning trees at $r$ and spanning trees $t$ of $G$: in a spanning tree, each $x \ne r$ has exactly one edge on its path to $r$, and that edge must be $a(x)$. So it is enough to show $\Pr[\text{arrows} = a] \propto \prod_{x \ne r} c_{a(x)}$, because $\prod_{x \ne r} c_{a(x)} = c(t)$.

## Termination

Each walk of lines L4 to L6 is a random walk on a finite connected graph, and it stops when it reaches a vertex in the tree, which contains $r$. From any vertex, some path of at most $n - 1$ steps reaches $r$, and the walk follows it with probability at least some $\delta > 0$. So the probability that a walk has not stopped after $j(n-1)$ steps is at most $(1 - \delta)^j \to 0$. There are at most $n$ walks, so the algorithm stops with probability 1.

## The stack model

Before the run, attach to each vertex $x \ne r$ an infinite stack $S_x = (S_x^1, S_x^2, \ldots)$ of arrows at $x$, all independent, each with the law of a step at $x$. Let line L5 at vertex $u$ use the next unused entry of $S_u$. The run is then a function of the stacks, and it has the same law as before, since each use of line L5 gets a fresh independent step.

At each time, the *visible graph* has, for each $x \ne r$, the topmost unused entry of $S_x$ as its arrow. Each $x \ne r$ has out-degree 1 and $r$ has out-degree 0. So the visible graph is either a rooted spanning tree at $r$, or it has a directed cycle; a self-loop arrow is a cycle of length 1. *Popping* a visible cycle marks the top entry of each vertex on it as used, so the next entry of each of these stacks becomes visible.

A *colored cycle* is a cycle together with the level of the stack entry at each of its vertices. Popping makes sense for colored cycles: the colored cycle $C$ is *poppable* when each of its entries is at the top of its stack and they form a cycle.

## Step 1: the run pops cycles

**Lemma 1.** The run of WILSON on fixed stacks is a sequence of cycle pops, and when no cycle is visible the arrows of the tree it returns are the visible graph.

*Proof.* We keep the invariant: at the start of each pass of line L2, the visible arrows of the tree vertices other than $r$ are the arrows $\text{Next}$ that the tree uses, and they lead to $r$.

During a walk from $i$, keep the current loop-erased path $u_0 = i, u_1, \ldots, u_k$ of distinct vertices not in the tree, where each $u_j \to u_{j+1}$ is the visible arrow of $u_j$. The walk stands at $u_k$, and line L5 reads the visible arrow of $u_k$. If it leads to a vertex in the tree, the walk stops. If it leads to a new vertex, that vertex is appended to the path. If it leads to a vertex $u_j$ of the path (with $j = k$ for a self-loop), the visible arrows of $u_j, \ldots, u_k$ form a cycle; we pop it at once. The walk now stands at $u_j$, the path becomes $u_0, \ldots, u_j$, and the visible arrow of $u_j$ is the next entry of its stack, which is exactly the entry that line L5 reads at the next step. The entries of $u_{j+1}, \ldots, u_k$ are popped too; if the walk comes back to one of them later, line L5 reads its next entry, which is again the visible one. So the walk with these pops reads the same entries as line L5, and each read entry is visible when it is read.

When the walk reaches the tree, the visible arrows of $u_0, \ldots, u_k$ lead into the tree, and they equal $\text{Next}[u_0], \ldots, \text{Next}[u_k]$, since $\text{Next}[u]$ always holds the last entry read at $u$. Lines L8 to L11 add exactly these vertices with these arrows. A vertex that was on an erased loop and not on the final path stays out of the tree, and its visible arrow is an entry not yet read. So the invariant holds after the pass. When the run ends, every vertex is in the tree, so the visible graph is the returned tree, which has no cycle, and the run was a sequence of pops of visible colored cycles. $\square$

## Step 2: the order of popping does not matter

**Lemma 2.** Fix the stacks. Suppose some sequence of pops, each of a poppable colored cycle, ends with no visible cycle after $k$ pops. Then every sequence of pops of poppable colored cycles ends after exactly $k$ pops, pops the same set of colored cycles, and leaves the same visible tree.

*Proof.* Two different cycles visible at the same time share no vertex, since each vertex has one visible arrow. A colored cycle $C$, once poppable, stays poppable until one of its vertices has its top entry used, and the only pop that uses the top entry of a vertex of $C$ while $C$ is visible is the pop of $C$ itself.

Induction on $k$. If $k = 0$, no cycle is visible, so no pop is possible, and the claim holds. Let $k \ge 1$ and let $C_1, \ldots, C_k$ be the given sequence. Let $C$ be any poppable colored cycle at the start. The cycle $C$ is visible at the start and the sequence ends with no visible cycle, so some $C_j$ uses an entry of $C$; take the least such $j$. Before step $j$, no pop touched $C$, so $C$ was still visible, and $C_j$ shares a vertex with $C$, so $C_j = C$. The cycles $C_1, \ldots, C_{j-1}$ are disjoint from $C$, so popping $C$ first does not change whether they are poppable. Hence $C, C_1, \ldots, C_{j-1}, C_{j+1}, \ldots, C_k$ is also a valid sequence that ends with no visible cycle, with the same set of colored cycles. After popping $C$, the rest has $k - 1$ pops, so by induction every sequence from that state has $k - 1$ pops, the same set, and the same final tree. Each sequence starts with some poppable $C$, so the claim holds for all sequences. $\square$

## Step 3: the law of the tree

The run stops with probability 1, so by Lemma 1, with probability 1 the stacks admit a finite popping sequence. Call the set $\mathcal{C}$ of colored cycles popped and the final tree $a$ the *outcome*. By Lemma 2 the outcome depends only on the stacks.

Fix a finite set $\mathcal{C}$ of colored cycles that occurs as the popped set for some stacks with positive probability, and fix a rooted spanning tree $a$. For each vertex $x$, let $\ell_x$ be the number of cycles in $\mathcal{C}$ through $x$. The outcome is $(\mathcal{C}, a)$ if and only if

1. for each colored cycle in $\mathcal{C}$, the stack entries at its positions are the arrows of the cycle, and
2. for each $x \ne r$, the entry $S_x^{\ell_x + 1}$ is $a(x)$.

*Only if* is clear: after popping $\mathcal{C}$, the top of $S_x$ is the entry at level $\ell_x + 1$, and it is the arrow of the final tree. *If*: since $\mathcal{C}$ occurs for some stacks, its colored cycles can be popped in some order when the entries of condition 1 hold, because poppability depends only on these entries. After these pops, the visible graph is $a$, which has no cycle. So this is a popping sequence that ends, and by Lemma 2 the outcome is $(\mathcal{C}, a)$.

The two conditions fix different stack entries, which are independent. Writing $p_x(e) = c_e / c(x)$ for the probability of an arrow (with the factor 2 for a self-loop), we get

$$\Pr[\text{outcome} = (\mathcal{C}, a)] = \Big( \prod_{C \in \mathcal{C}} \prod_{(x, e) \in C} p_x(e) \Big) \cdot \prod_{x \ne r} p_x(a(x)) = \Psi(\mathcal{C}) \cdot \frac{\prod_{x \ne r} c_{a(x)}}{\prod_{x \ne r} c(x)}.$$

Tree arrows are never self-loops, so the factor 2 does not appear in the second product. The first factor depends only on $\mathcal{C}$, and the set of possible $\mathcal{C}$ does not depend on $a$, since condition 1 alone decides whether $\mathcal{C}$ can be popped. Summing over $\mathcal{C}$,

$$\Pr[\text{arrows} = a] = \Big( \sum_{\mathcal{C}} \Psi(\mathcal{C}) \Big) \cdot \frac{1}{\prod_{x \ne r} c(x)} \cdot \prod_{x \ne r} c_{a(x)}.$$

The first two factors do not depend on $a$, so $\Pr[\text{arrows} = a] \propto \prod_{x \ne r} c_{a(x)} = c(t)$ for the spanning tree $t$ of $a$. The probabilities sum to 1 over all spanning trees, so $\Pr[T = t] = c(t) / Z$.

The order of the vertices in line L2 changes only the order of popping, so by Lemma 2 it does not change the outcome for fixed stacks, and the law is the same for every order.

## Disconnected graphs

The implementation picks a root in each component. A walk never leaves its component, so the runs in different components use disjoint stacks and are independent, and each gives a tree of its component with the law above. The forest $F$ then has probability proportional to $\prod_{e \in F} c_e$ among the spanning forests with one tree in each component, and with all weights 1 it is uniform among them. $\blacksquare$
