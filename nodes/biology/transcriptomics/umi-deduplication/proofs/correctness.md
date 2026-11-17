---
title: The directional method returns a partition between the connected components and the distinct UMIs, and it is exact when the errors are single substitutions of well separated UMIs
proves: [correctness]
status: full
---

We prove what the directional method of UMI-tools computes on one bundle. Its groups partition the UMIs, the first UMI of each group has the highest count in the group (Lemma 2), and the number of groups lies between the number of connected components of the distance-1 graph and the number of distinct UMIs (Theorem 3). Under an explicit error model, single substitutions of true UMIs that are far apart, the groups are exactly the molecules (Theorem 4). Whether real data follow this model is not proved here; the tests measure the error on simulated reads.

**Setting.** One bundle has a set $U$ of $m$ distinct UMIs, all of length $\ell$, and a count $n(u) \ge 1$ for each $u \in U$. Let $d$ be the Hamming distance. The directional graph $D$ has an arc $u \to v$ when $d(u, v) = 1$ and $n(u) \ge 2n(v) - 1$ (lines L4 and L5). Write $u \preceq v$ when $u$ comes before $v$ in the visit order of line L3: decreasing count, then the UMI string. Let $R(u)$ be the set of UMIs reachable from $u$ along arcs, with $u \in R(u)$. Lines L6 to L10 visit $u_1 \prec u_2 \prec \dots \prec u_m$; when $u_i$ is not in $T$ (the set taken so far) they add the group $R(u_i) \setminus T$ and set $T \leftarrow T \cup R(u_i)$.

**Lemma 1 (counts along an arc).** If $u \to v$ is an arc, then $n(u) \ge n(v)$, with equality only when $n(u) = n(v) = 1$. So $n$ does not increase along a path of $D$.

*Proof.* $n(u) \ge 2n(v) - 1 = n(v) + (n(v) - 1) \ge n(v)$, since $n(v) \ge 1$. Equality needs $n(v) = 1$ and then $n(u) = 1$. $\square$

**Lemma 2 (partition and representative).** The groups are non-empty, pairwise disjoint and cover $U$. The UMI $u_i$ that starts a group is its first element in the visit order and has the highest count in it.

*Proof.* A group starts at $u_i$ only when $u_i \notin T$, and $u_i \in R(u_i)$, so $u_i$ is in its group and the group is not empty. Each group is $R(u_i) \setminus T$ and $T$ then grows by $R(u_i)$, so later groups avoid the UMIs of earlier groups. Every $u_i$ is either in $T$ when it is visited, so in an earlier group, or it starts a group, so the groups cover $U$. Let $x$ be in the group of $u_i$. By Lemma 1, $n(x) \le n(u_i)$. If $x \prec u_i$, then $x$ was visited before $u_i$, and at that moment $x$ was either in $T$ already or it started a group and entered $T$. In both cases $x \in T$ before $u_i$ is visited, which contradicts $x \in R(u_i) \setminus T$. So $u_i \preceq x$ for each $x$ of the group. $\square$

The code writes each group in visit order, so `group[0]` is the starting UMI and the representative.

**Theorem 3 (bounds).** Let $c$ be the number of connected components of the undirected graph $H$ on $U$ with an edge when $d(u, v) = 1$, and let $g$ be the number of directional groups. Then $c \le g \le m$.

*Proof.* The bound $g \le m$ follows from Lemma 2, because the groups are disjoint and non-empty. Every arc of $D$ is an edge of $H$, so $R(u)$ lies inside the component of $u$, and so does each group. Take a component $C$ and let $u$ be its first UMI in the visit order. Every UMI visited before $u$ is in another component, so it reaches nothing in $C$, and $u \notin T$ when $u$ is visited. So $u$ starts a group inside $C$. Different components give different groups, so $g \ge c$. $\square$

The "cluster" method returns the $c$ components and the "unique" method returns the $m$ UMIs, so the directional count always lies between the two. Both ends are reached: with no edges all three are equal, and on a path whose counts halve from one UMI to the next the directional method gives $g = c = 1$.

**Theorem 4 (exact under single substitution errors).** Let $t_1, \dots, t_k$ be the true UMIs of the $k$ molecules of the bundle, all distinct and all in $U$, with $d(t_a, t_b) \ge 4$ for $a \ne b$. Suppose that every other UMI $e \in U$ has $d(e, t_a) = 1$ for some $a$ and $n(t_a) \ge 2n(e) - 1$. Then the directional groups are exactly the families $F_a = \{t_a\} \cup \{e : d(e, t_a) = 1\}$, so $g = k$.

*Proof.* The families cover $U$, and they are disjoint because a UMI at distance 1 from $t_a$ and from $t_b$ would give $d(t_a, t_b) \le 2$. Two UMIs in different families are at distance at least $4 - 1 - 1 = 2$ by the triangle inequality, so every arc of $D$ joins two UMIs of one family, and $R(x) \subseteq F_a$ for $x \in F_a$. Inside $F_a$ there is an arc $t_a \to e$ for each error $e$, by the assumption on the counts, so $R(t_a) = F_a$.

Let $x$ be the first UMI of $F_a$ in the visit order. No UMI of another family reaches $x$, so $x$ starts a group, and the group is $R(x)$ minus UMIs of other families, that is $R(x)$. If $x = t_a$, the group is $F_a$. Otherwise $x$ is an error $e$ with $n(e) \ge n(t_a)$, and with Lemma 1 applied to the arc $t_a \to e$ this gives $n(e) = n(t_a) = 1$. Then $n(e) \ge 2n(t_a) - 1$ also holds, so there is an arc $e \to t_a$, and $R(e) \supseteq R(t_a) = F_a$. In both cases the group of $F_a$ is $F_a$. The first UMI of each family starts one group and the other UMIs of the family are then taken, so there are exactly $k$ groups. $\square$

The separation $d(t_a, t_b) \ge 4$ is a sufficient condition, not a necessary one. The point of the count rule shows when it fails: if $d(t_a, t_b) = 1$ and the two counts are similar, $n(t_a) < 2n(t_b) - 1$ and $n(t_b) < 2n(t_a) - 1$, then there is no arc between them, while the cluster method joins them. A read with two errors is at distance 2 from its true UMI and is never joined, so it is counted as an extra molecule.

**What the lines compute.** Line L1 counts the reads of each UMI in each bundle. Line L3 is the visit order $\preceq$. Lines L4 and L5 build the arcs of $D$, from the neighbors at distance 1. Lines L6 to L10 are the loop of the setting, with a breadth-first search for $R(u_i)$ at line L9. Line L11 returns $g$ for each bundle, and line L12 returns all bundles.

**Complexity.** Comparing all pairs at line L4 takes $O(m^2\ell)$ time per bundle; looking up the $\ell(|\Sigma| - 1)$ substitution variants of each UMI in a hash table takes $O(m\ell^2|\Sigma|)$ expected time. Each breadth-first search at line L9 is $O(m + a)$ for $a$ arcs, and there are at most $m$ of them, so lines L6 to L10 are $O(m(m + a))$ in the worst case. The sort is $O(m\log m)$.

**What the tests check.** The test file compares the groups with a brute force that computes reachability by a transitive closure, checks that the two ways to find neighbors agree, and checks Lemma 1, Lemma 2 and Theorem 3 on random bundles. It checks the cluster method against a brute-force merge of sets, the page example, the case of two UMIs with count 1, and the bundle keys. Two simulations of PCR copies with 1 percent base errors measure the error of the three methods; these are measurements, not theorems.
