---
title: BUILD gives exactly the control dependences and the flow dependences
proves: [correctness]
status: full
---

We use the notation of the page. $G$ is the augmented CFG of line L1, $x$ is EXIT, and every node of $G$ reaches $x$. Post-dominance and $\mathrm{ipdom}$ are taken in $G$. The facts about the post-dominator tree that we use are those of the [post-dominance](/post-dominance/) page: the post-dominators of a node $v$ are exactly the ancestors of $v$ in the tree, with $v$ itself, and the strict post-dominators of $v \ne x$ are $\mathrm{ipdom}(v)$ and its ancestors.

## Part 1: the control edges

**Definition.** Block $Y$ is control dependent on block $X$ through the edge $X \to S$ if $Y \;\mathrm{pdom}\; S$ and $Y$ does not strictly post-dominate $X$. The [control dependence](/control-dependence/) page proves that this edge form is equivalent to the path form of Ferrante, Ottenstein and Warren.

**Lemma 1.** For every edge $a \to b$ of $G$, $\mathrm{ipdom}(a)$ post-dominates $b$.

*Proof.* The node $a$ has a successor, so $a \ne x$ and $\mathrm{ipdom}(a)$ exists. Let $Q$ be a path from $b$ to $x$. Then $a$ followed by $Q$ is a path from $a$ to $x$, so it contains $\mathrm{ipdom}(a)$. Since $\mathrm{ipdom}(a) \ne a$, the node is on $Q$. $\square$

**Lemma 2.** For an edge $a \to b$, the set $D(a, b) = \{Y : Y \;\mathrm{pdom}\; b \text{ and } Y \text{ does not strictly post-dominate } a\}$ is the set of nodes on the tree path from $b$ up to $\mathrm{ipdom}(a)$, with $\mathrm{ipdom}(a)$ left out. In particular it is empty when $b = \mathrm{ipdom}(a)$.

*Proof.* $Y \;\mathrm{pdom}\; b$ holds iff $Y$ is $b$ or an ancestor of $b$. $Y$ strictly post-dominates $a$ iff $Y$ is $\mathrm{ipdom}(a)$ or an ancestor of it. By Lemma 1, $\mathrm{ipdom}(a)$ is $b$ or an ancestor of $b$. So the ancestors of $b$ (with $b$) fall into two parts: those strictly below $\mathrm{ipdom}(a)$ on the path from $b$, and $\mathrm{ipdom}(a)$ with its ancestors. The first part is $D(a, b)$. $\square$

**Claim 1.** Lines L3 to L8 add the control edge $(\mathit{src}(a), i, b)$ for an instruction $i$ of block $Y$ exactly when $Y$ is control dependent on $a$ through $a \to b$, where $\mathit{src}(a)$ is ENTRY if $a$ is START and the terminator of $a$ otherwise.

*Proof.* If $b = \mathrm{ipdom}(a)$, line L3 skips the edge, and $D(a, b)$ is empty by Lemma 2. Otherwise the loop of lines L5 to L8 starts at $b$ and moves to the parent in the tree until it meets $\mathrm{ipdom}(a)$. It meets it, because $\mathrm{ipdom}(a)$ is an ancestor of $b$ by Lemma 1, and each step moves one level up. So the loop body runs for exactly the nodes of $D(a, b)$, and line L7 adds the edges for all instructions of each of them. The node EXIT is never in $D(a, b)$ for $a \ne x$, since it strictly post-dominates every other node, so line L7 always finds a real block. $\square$

Every instruction of a block runs exactly when the block runs, so giving all of them the control parents of the block is the instruction-level form of the same relation.

## Part 2: the data edges

A *position* is an instruction of a block, the terminator included. A definition $d$ of $v$ at a position, or of a parameter $v$ at ENTRY, *reaches* a position $u$ if there is a path in the CFG from just after $d$ to $u$ on which no position before $u$ defines $v$. For ENTRY, the path starts at the first position of the entry block. The specification is: $(d, u, v)$ is a data edge iff $u$ reads $v$ and the definition $d$ of $v$ reaches $u$.

**The equations.** For a block $B$, let $\mathrm{gen}(B)$ be the last definition in $B$ of each variable that $B$ defines, and $\mathrm{kill}(B)$ the set of variables that $B$ defines. The code computes, by round-robin iteration from $\mathrm{IN} = \emptyset$ and $\mathrm{OUT}(B) = \mathrm{gen}(B)$,

$$\mathrm{IN}(B) = \mathit{bnd}(B) \cup \bigcup_{P \to B} \mathrm{OUT}(P), \qquad \mathrm{OUT}(B) = \mathrm{gen}(B) \cup \{(d, v) \in \mathrm{IN}(B) : v \notin \mathrm{kill}(B)\},$$

where $\mathit{bnd}(B)$ is the set of parameter definitions at ENTRY if $B$ is the entry block and empty otherwise.

**Lemma 3.** The iteration stops, and then $(d, v) \in \mathrm{IN}(B)$ iff the definition $d$ of $v$ reaches the first position of $B$.

*Proof.* The right-hand sides are monotone in the sets, the sets only grow from their start values, and they are subsets of a finite set of pairs, so the iteration stops. Let $R(B)$ be the set of pairs $(d, v)$ such that $d$ reaches the first position of $B$.

($R \subseteq \mathrm{IN}$.) Take $(d, v) \in R(B)$ with a witness path, and use induction on the number of blocks that the path enters after $d$. If $d$ is a parameter and the path is empty, $B$ is the entry and $(d, v) \in \mathit{bnd}(B)$. If $d$ is in block $P$ and the next block is $B$, then $d$ is the last definition of $v$ in $P$, because the path after $d$ to the end of $P$ has no definition of $v$, so $(d, v) \in \mathrm{gen}(P) \subseteq \mathrm{OUT}(P) \subseteq \mathrm{IN}(B)$. Otherwise the path enters a block $P$ before $B$ and crosses all of it without defining $v$. By induction $(d, v) \in \mathrm{IN}(P)$, and $v \notin \mathrm{kill}(P)$, so $(d, v) \in \mathrm{OUT}(P) \subseteq \mathrm{IN}(B)$. These inclusions hold at the fixpoint because it satisfies the equations.

($\mathrm{IN} \subseteq R$.) Every value that the iteration produces is in $R$, by induction on the steps. The start values are empty or are $\mathrm{gen}(B)$, and a pair $(d, v)$ of $\mathrm{gen}(P)$ reaches the start of every successor of $P$. A pair that enters $\mathrm{IN}(B)$ comes from $\mathit{bnd}(B)$, which is in $R(B)$, or from some $\mathrm{OUT}(P)$ with $P \to B$. A pair of $\mathrm{OUT}(P)$ is in $\mathrm{gen}(P)$, or it is in $\mathrm{IN}(P) \subseteq R(P)$ with $v \notin \mathrm{kill}(P)$, so its witness path extends through $P$ and the edge $P \to B$ without a new definition of $v$. $\square$

**Claim 2.** Lines L10 to L14 add $(d, u, v)$ iff $u$ reads $v$ and $d$ reaches $u$.

*Proof.* Fix a block $B$. The invariant of the loop of line L12 is: before position $u$, the set $\mathit{cur}[v]$ is the set of definitions of $v$ that reach $u$. Before the first position this is Lemma 3, because line L11 groups $\mathrm{IN}(B)$. If position $u$ does not define $v$, a definition reaches the next position iff it reaches $u$, since the path can be extended by one step and no new definition of $v$ is crossed. If $u$ defines $v$, the only definition of $v$ that reaches the next position is $u$ itself, because every path from an earlier definition passes $u$. Line L14 sets $\mathit{cur}[v] = \{u\}$, which keeps the invariant. Line L13 runs before line L14, so a use of $v$ in an instruction that also defines $v$, such as `i = i + 1`, gets the definitions that reach it from before. The loop adds exactly the triples of the claim at each position. $\square$

Claims 1 and 2 together say that the graph built by BUILD has exactly the control edges and the flow dependence edges of its definition. SLICE returns the nodes from which $y$ is reachable along these edges, by the usual argument for a graph search: every node it adds has a path to $y$, and every node with a path to $y$ is added when the last edge of its path is examined. $\square$
