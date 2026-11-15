---
title: SALSA scores are the in-degrees and out-degrees, weighted by component size
proves: [correctness]
status: full
---

Let $E$ be the set of links of the base set after self links and repeated links are removed, and let $m = |E| \ge 1$. Write $\mathrm{in}(p)$ and $\mathrm{out}(q)$ for the in-degree and out-degree. The hub side is $H = \{q : \mathrm{out}(q) > 0\}$ and the authority side is $A = \{p : \mathrm{in}(p) > 0\}$. The bipartite graph $\tilde G$ has a node $q_h$ for each $q \in H$, a node $p_a$ for each $p \in A$, and an undirected edge $\{q_h, p_a\}$ for each link $(q, p) \in E$. A page in both sets gives two different nodes.

The authority chain moves from an authority $i$ to a uniformly random hub $q$ with $(q, i) \in E$, and then to a uniformly random authority $j$ with $(q, j) \in E$. Its transition matrix is

$$P_A(i, j) = \sum_{q :\ (q, i) \in E,\ (q, j) \in E} \frac{1}{\mathrm{in}(i)\, \mathrm{out}(q)}.$$

The hub chain moves from a hub $q$ along a random out-link to $p$ and then back along a random in-link of $p$ to a hub $r$: $P_H(q, r) = \sum_{p :\ (q, p) \in E,\ (r, p) \in E} \frac{1}{\mathrm{out}(q)\, \mathrm{in}(p)}$.

SALSA defines the authority scores as $\lim_{k \to \infty} u_A P_A^k$, where $u_A$ is the uniform distribution on $A$, and the hub scores in the same way with $P_H$ and the uniform distribution $u_H$ on $H$. The lemmas below show that the limits exist and give them in closed form. We prove the authority case; the hub case is the same proof with the roles of in and out swapped.

**Lemma 1 (stochastic).** Each row of $P_A$ sums to $1$.

*Proof.* $\sum_j P_A(i, j) = \sum_{q : (q, i) \in E} \frac{1}{\mathrm{in}(i)} \sum_{j : (q, j) \in E} \frac{1}{\mathrm{out}(q)}$. The inner sum has $\mathrm{out}(q)$ terms equal to $1/\mathrm{out}(q)$, so it is $1$. The outer sum has $\mathrm{in}(i)$ terms equal to $1/\mathrm{in}(i)$. $\square$

**Lemma 2 (reversible).** For all authorities $i$ and $j$, $\mathrm{in}(i) P_A(i, j) = \mathrm{in}(j) P_A(j, i)$.

*Proof.* Both sides equal $\sum_{q : (q, i) \in E,\ (q, j) \in E} 1/\mathrm{out}(q)$, which is symmetric in $i$ and $j$. $\square$

**Lemma 3 (components).** $P_A(i, j) > 0$ if and only if some hub links to both $i$ and $j$. Two authorities $i$ and $j$ can reach each other in the chain if and only if $i_a$ and $j_a$ are in the same connected component of $\tilde G$. Each $P_A(i, i) > 0$.

*Proof.* The first claim holds because every term of the sum is positive. A path in $\tilde G$ alternates between hub nodes and authority nodes, so a path from $i_a$ to $j_a$ is a sequence of authorities $i = i_0, i_1, \ldots, i_r = j$ in which each consecutive pair shares a hub, which is a path of positive steps of the chain; the converse reads the same sequence backwards. Every authority $i$ has some hub $q$ with $(q, i) \in E$, and the term for $q$ in $P_A(i, i)$ is positive. $\square$

Let the components of $\tilde G$ be $c = 1, \ldots, C$, with authority sets $A_c$, hub sets $H_c$ and link sets $E_c$, so $m_c = |E_c| = \sum_{p \in A_c} \mathrm{in}(p) = \sum_{q \in H_c} \mathrm{out}(q)$. Each link lies in exactly one component, because its two ends are joined by an edge.

**Theorem 1 (connected case).** If $\tilde G$ is connected, the authority chain has the unique stationary distribution $\pi(i) = \mathrm{in}(i)/m$, and $u_A P_A^k \to \pi$.

*Proof.* $\pi$ is a distribution, because the in-degrees sum to $m$. By Lemma 2, $\sum_i \pi(i) P_A(i, j) = \frac{1}{m} \sum_i \mathrm{in}(j) P_A(j, i) = \pi(j)$, using Lemma 1 in the last step. So $\pi$ is stationary. By Lemma 3 the chain is irreducible and each state has a self loop, so it is aperiodic. A finite irreducible chain has exactly one [stationary distribution](/stationary-distribution/), and a finite irreducible aperiodic chain converges to it from every start (the convergence theorem for finite [Markov chains](/markov-chain/)). $\square$

**Theorem 2 (general case).** For each authority $p$ in component $c$,

$$\lim_{k \to \infty} (u_A P_A^k)(p) = \frac{|A_c|}{|A|} \cdot \frac{\mathrm{in}(p)}{m_c},$$

and for each hub $q$ in component $c$, $\lim_{k \to \infty} (u_H P_H^k)(q) = \frac{|H_c|}{|H|} \cdot \frac{\mathrm{out}(q)}{m_c}$.

*Proof.* By Lemma 3, $P_A(i, j) = 0$ when $i$ and $j$ lie in different components, so $P_A$ is block diagonal with one block $P_c$ for each component, and each block is a stochastic matrix by Lemma 1. Then $(u_A P_A^k)$ restricted to $A_c$ equals $\frac{|A_c|}{|A|} \cdot (u_c P_c^k)$, where $u_c$ is uniform on $A_c$: the start puts mass $|A_c|/|A|$ on the block, spread evenly, and the block never sends mass out. Component $c$ is a connected bipartite graph on its own, so Theorem 1 applied to it gives $u_c P_c^k \to \mathrm{in}(p)/m_c$. $\square$

This is Proposition 2 of Lempel and Moran in the unweighted case. The weight $|A_c|/|A|$ comes from the uniform start. With another start the limit gives the component other weights, while the scores inside a component stay proportional to in-degree. This is why SALSA fixes the start.

**Theorem 3 (the implementation).** The function salsa returns these limits.

*Proof.* Line L1 builds $E$. Line L2 builds $H$ and $A$ from the degrees. Line L3 labels the nodes of $\tilde G$ by a graph search from each node that is not yet labelled; a search labels exactly the nodes that are connected to its start, so two nodes get the same label if and only if they are in the same component. Line L4 counts, for each label, the hubs, the authorities and the links, a link being counted at its hub. Lines L5 and L6 then evaluate the formulas of Theorem 2. $\square$

**Cost.** Removing repeated links costs $O(m)$ expected time with a hash set. Building the adjacency lists, the search and the counts cost $O(n + m)$, and lines L5 and L6 cost $O(n)$. So SALSA costs $O(n + m)$ besides the duplicate removal, with no iteration. The implementation sorts the links once to fix their order, which adds $O(m \log m)$.
