---
title: Both passes compute the dominance frontiers, and the worklist computes the iterated frontier
proves: [correctness]
status: full
---

**Setting.** $G$ is a directed graph with root $r$, and $R$ is the set of nodes that $r$ reaches. Only nodes of $R$ and edges between them take part: an edge from a node outside $R$ lies on no path from $r$ and changes no dominance relation, and the code never looks at such nodes. $x \operatorname{dom} y$ means that every path from $r$ to $y$ contains $x$, and $x \operatorname{sdom} y$ means $x \operatorname{dom} y$ and $x \ne y$. The input $\mathrm{idom}$ is correct: $\mathrm{idom}(r)$ is None, and for $y \ne r$, $\mathrm{idom}(y)$ is the strict dominator of $y$ that every other strict dominator of $y$ dominates. (The [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) page proves this for the routine used.) $T$ is the dominator tree, with parent $\mathrm{idom}$. We use one standard fact: the dominators of $y$ are exactly the ancestors of $y$ in $T$, $y$ included. So the dominators of $y$ form a chain, and $x \operatorname{sdom} y$ if and only if $x$ is a proper ancestor of $y$.

The target is $DF(x) = \{y : \exists (p, y) \in E,\ x \operatorname{dom} p,\ \text{not } x \operatorname{sdom} y\}$. For an edge $(p, y)$, let $W(p, y)$ be the set of nodes on the tree path from $p$ up to, but not including, $\mathrm{idom}(y)$. If $y = r$, the path goes up to $r$ and includes it.

**Lemma 1.** Let $(p, y) \in E$ with $p, y \in R$ and $y \ne r$. Then $\mathrm{idom}(y) \operatorname{dom} p$.

*Proof.* Let $d = \mathrm{idom}(y)$, so $d \ne y$. Suppose some path $P$ from $r$ to $p$ avoids $d$. Then $P$ followed by the edge $(p, y)$ is a path from $r$ to $y$. Its nodes are those of $P$ and $y$, and none of them is $d$. This contradicts $d \operatorname{dom} y$. $\square$

So $\mathrm{idom}(y)$ is an ancestor of $p$ in $T$, and $W(p, y)$ is a well defined part of the path from $p$ to the root.

**Lemma 2 (the edge form).** $y \in DF(x)$ if and only if $x \in W(p, y)$ for some edge $(p, y)$.

*Proof.* Fix an edge $(p, y)$. The nodes $x$ with $x \operatorname{dom} p$ are the ancestors of $p$, which form the path $A$ from $p$ up to $r$.

If $y = r$, no node strictly dominates $y$, since a strict dominator of $r$ would have to lie on the empty path from $r$ to $r$. So $x \operatorname{dom} p$ and not $x \operatorname{sdom} y$ holds for all $x \in A = W(p, y)$.

If $y \ne r$, let $d = \mathrm{idom}(y)$. By Lemma 1, $d \in A$. Take $x \in A$. Both $x$ and $d$ are on the chain $A$, so one is an ancestor of the other. The strict dominators of $y$ are the ancestors of $d$, $d$ included. So $x \operatorname{sdom} y$ if and only if $x$ is $d$ or above $d$. Hence the $x \in A$ with not $x \operatorname{sdom} y$ are exactly the nodes of $A$ below $d$, which is $W(p, y)$.

Taking the union over all edges into $y$ gives the claim. $\square$

**Lemma 3 (the bottom-up split).** For every node $x$,

$$DF(x) = \{y \in \mathrm{succ}(x) : \mathrm{idom}(y) \ne x\} \;\cup \bigcup_{z : \mathrm{idom}(z) = x} \{y \in DF(z) : \mathrm{idom}(y) \ne x\}.$$

(For $y = r$ the test $\mathrm{idom}(y) \ne x$ is true, since $\mathrm{idom}(r)$ is None.)

*Proof.* ($\subseteq$) Let $y \in DF(x)$. By Lemma 2 there is an edge $(p, y)$ with $x \in W(p, y)$. Then $x \ne \mathrm{idom}(y)$, because $W(p, y)$ excludes $\mathrm{idom}(y)$.

- If $x = p$, then $y$ is a successor of $x$ with $\mathrm{idom}(y) \ne x$, so $y$ is in the first set.
- If $x \ne p$, then $x$ is a proper ancestor of $p$. Let $z$ be the child of $x$ on the tree path from $x$ down to $p$. The node $z$ is between $p$ and $x$, so it is below $x$, and $x$ is below $\mathrm{idom}(y)$ (or $y = r$). So $z \in W(p, y)$, and by Lemma 2, $y \in DF(z)$. With $\mathrm{idom}(y) \ne x$, $y$ is in the second set.

($\supseteq$) Let $y$ be a successor of $x$ with $\mathrm{idom}(y) \ne x$. If $y = r$, then $x \in W(x, y)$ since that path runs from $x$ to the root. Otherwise, by Lemma 1 with $p = x$, $\mathrm{idom}(y)$ is an ancestor of $x$, and it is not $x$. So $x \in W(x, y)$ and $y \in DF(x)$ by Lemma 2.

Let $z$ be a child of $x$ and $y \in DF(z)$ with $\mathrm{idom}(y) \ne x$. By Lemma 2 there is an edge $(p, y)$ with $z \in W(p, y)$. If $y = r$, the path from $p$ to the root contains $z$ and so contains its parent $x$, and $x \in W(p, y)$. Otherwise $\mathrm{idom}(y)$ is a proper ancestor of $z$, so it is $x$ or above $x$. It is not $x$, so it is above $x$, and $x$ lies on the path from $z$ up to $\mathrm{idom}(y)$ with $\mathrm{idom}(y)$ excluded. Hence $x \in W(p, y)$ and $y \in DF(x)$. $\square$

**Theorem 1 (the bottom-up pass, lines L1 to L8).** When line L8 returns, $DF[x] = DF(x)$ for every $x \in R$.

*Proof.* Line L1 visits the nodes in a postorder of $T$, so every child $z$ of $x$ is finished before $x$ starts. By induction on this order, $DF[z] = DF(z)$ for each child when $x$ is visited. Lines L3 and L4 add the first set of Lemma 3, and lines L5 to L7 add the second set, reading the finished $DF[z]$. Nothing else is added. By Lemma 3 the result is $DF(x)$. Every node of $R$ is in $T$ and is visited once. $\square$

**Theorem 2 (the walk, lines L9 to L14).** When the walk ends, $DF[x] = DF(x)$ for every $x \in R$.

*Proof.* First take the walk without the early stop, that is, with the test `y not in DF[runner]` removed from line L12. For the edge $(p, y)$, lines L11 to L14 start at $p$ and move to the parent until they reach $\mathrm{idom}(y)$, or until they pass the root when $y = r$ (then $\mathrm{idom}(y)$ is None, and the parent of the root is None too). By Lemma 1 the walk does reach $\mathrm{idom}(y)$, so it stops, and the nodes it adds $y$ to are exactly $W(p, y)$. Line L9 skips a node $y \ne r$ with one predecessor $p$. For such a node every path from $r$ to $y$ ends with the edge $(p, y)$, so $p \operatorname{dom} y$, and the strict dominators of $y$ are $p$ and the dominators of $p$, which makes $\mathrm{idom}(y) = p$ and $W(p, y) = \emptyset$. So skipping it loses nothing. By Lemma 2, the union over all edges is $DF$.

Now the early stop. The walks for one node $y$ run one after the other, before the walks for any other node. Claim: whenever $y \in DF[u]$ during the walks for $y$, every node on the tree path from $u$ up to $\mathrm{idom}(y)$, with $\mathrm{idom}(y)$ excluded, also has $y$ in its set. This holds before the first walk for $y$, when no set holds $y$. A walk adds $y$ to a sequence of nodes $u_1, u_2, \ldots, u_k$ going up the tree. It stops either at $\mathrm{idom}(y)$, so the claim holds for all $u_i$, or at a node $u_{k+1}$ that already holds $y$, and then the claim for $u_{k+1}$ gives the rest of the path. So the early stop only skips nodes that already hold $y$, and the sets at the end are the same as without it. $\square$

**Lemma 4 (the iterated frontier).** Let $L$ be the limit of $DF_1 = DF(S)$, $DF_{i+1} = DF(S \cup DF_i)$. The worklist routine returns $L$.

*Proof.* Each $DF_i \subseteq DF_{i+1}$, by induction: $DF_1 = DF(S) \subseteq DF(S \cup DF_1)$, and if $DF_{i-1} \subseteq DF_i$ then $DF(S \cup DF_{i-1}) \subseteq DF(S \cup DF_i)$. The sets lie in the finite set $N$, so the sequence stops at some $L$ with $L = DF(S \cup L)$.

Let $W$ be the returned set. Every node put on the work list is in $S \cup W$, and is put there once.

($W \subseteq L$) A node $y$ enters $W$ as a member of $DF(x)$ for a node $x$ taken from the list. By induction on the order of the steps, $x \in S \cup L$, so $y \in DF(S \cup L) = L$. A node that enters the list is then in $S \cup L$, which keeps the induction going.

($L \subseteq W$) At the end the list is empty, so every node of $S \cup W$ was taken from it and its frontier was added to $W$. So $DF(S \cup W) \subseteq W$. Then $DF_1 = DF(S) \subseteq W$, and if $DF_i \subseteq W$ then $DF_{i+1} = DF(S \cup DF_i) \subseteq DF(S \cup W) \subseteq W$. So $L \subseteq W$. $\square$

**Running time.** Let $n = |R|$, $m$ the number of edges inside $R$, and $D = \sum_x |DF(x)|$. In the bottom-up pass, each node is visited once (L1, L2), each edge is looked at once (L3, L4), and each element of $DF(z)$ is looked at once, at the parent of $z$ (L6, L7). With a set that tests and adds in $O(1)$, for example a marker array stamped with $x$, the time is $\Theta(n + m + D)$. In the walk, each pass through line L13 adds a new pair $(\text{runner}, y)$, because of the early stop, so there are at most $D$ such passes. Each predecessor $p$ of $y$ costs $O(1)$ more for the test that ends its walk. So the time is $O(n + m + D)$. The worklist for $DF^+(S)$ takes each node at most once and reads its frontier once, so it takes $O(n + D)$ time.
