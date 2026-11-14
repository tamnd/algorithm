---
title: Phi-functions at the iterated dominance frontier give minimal SSA form, and renaming over the dominator tree is correct
proves: [correctness]
status: full
---

**Setting.** $G = (N, E, r)$ is the control flow graph of the input program. Every block is reachable from $r$, and $r$ has no predecessors (the toy IR gives the entry no predecessors; a compiler can add an empty entry block). $x \operatorname{dom} y$ means that every path from $r$ to $y$ contains $x$, and $\operatorname{sdom}$ is the strict version. The dominators of $y$ are the ancestors of $y$ in the dominator tree, $y$ included, so they form a chain. A *path* is a sequence of blocks joined by edges, and it is *non-empty* if it has at least one edge.

Fix a variable $v$. Let $S$ be the set of blocks that assign $v$, plus $r$. The block $r$ counts as a definition because it holds the value of $v$ on entry: the parameter itself, or the name $v.0$ when $v$ is not a parameter.

**Lemma 1.** If $d \operatorname{sdom} y$ and $(p, y) \in E$, then $d \operatorname{dom} p$.

*Proof.* A path from $r$ to $p$ that avoids $d$, followed by the edge $(p, y)$, is a path from $r$ to $y$ that avoids $d$, since $d \ne y$. $\square$

## Part 1. The placement is minimal

**Join sets.** $y \in J(X)$ if there are two non-empty paths $P_1$ from $x_1$ to $y$ and $P_2$ from $x_2$ to $y$ with $x_1 \ne x_2$ in $X$, such that $y$ is the only node the two paths share. (So $y$ occurs in each path only at the end, except that $P_1$ may start at $x_1 = y$.)

**What minimal means.** After the construction, the definitions of $v$ are the blocks of $S$ and the blocks $\Phi$ that get a phi-function for $v$. If two of them reach a block $y$ along paths that meet first at $y$, a use at the top of $y$ would have two reaching definitions, so $y$ needs a phi-function. So a valid placement is a set $\Phi$ with $J(S \cup \Phi) \subseteq \Phi$. $J$ is monotone and $N$ is finite, so the least such set exists. It is $J^+(S)$, the limit of $J_1 = J(S)$, $J_{i+1} = J(S \cup J_i)$: by induction each $J_i$ lies in every valid $\Phi$, and the limit is valid. Minimal SSA form places phi-functions for $v$ exactly at $J^+(S)$. We show that this set is $DF^+(S)$, the set that lines L3 to L8 compute.

**Lemma 2.** If $x \ne r$, then $DF(x) \subseteq J(\{r, x\})$.

*Proof.* Let $y \in DF(x)$: there is an edge $(p, y)$ with $x \operatorname{dom} p$ and not $x \operatorname{sdom} y$. As $r$ has no predecessors, $y \ne r$.

The first path. Take a path from $r$ to $p$. It contains $x$. Keep the part after the last $x$, so we get a path from $x$ to $p$ in which $x$ occurs only at the start. Every node $u$ on it is dominated by $x$: a path from $r$ to $u$ that avoids $x$, followed by the rest of this path to $p$, would avoid $x$ and contradict $x \operatorname{dom} p$. Add the edge $(p, y)$, and cut the path at the first $y$ after the start. The result $P_1$ is a non-empty path from $x$ to $y$, and every node of $P_1$ except the last is dominated by $x$.

The second path. Take a path from $r$ to $y$ and cut it at the first $y$. If $x \ne y$, choose it to avoid $x$, which is possible because $x$ does not dominate $y$. The result $P_2$ is non-empty, because $r \ne y$. No node $u$ of $P_2$ before $y$ is dominated by $x$: the part of $P_2$ from $r$ to $u$ avoids $x$ (if $x = y$, because $y$ occurs only at the end).

So the only node the two paths share is $y$, and they start at $x$ and $r$, which differ. Hence $y \in J(\{r, x\})$. $\square$

**Lemma 3.** For every set $X$ with $r \in X$, $J(X) \subseteq DF^+(X)$.

*Proof.* Let $T = X \cup DF^+(X)$. By the definition of $DF^+$ as a limit, $DF(T) = DF^+(X) \subseteq T$. For each node $w$, let $d(w)$ be the deepest dominator of $w$ that is in $T$, with $w$ itself allowed. It exists, since $r \in T$ dominates every node.

*Claim.* If $(p, w) \in E$ and $w \notin T$, then $d(w) = d(p)$. Let $u = d(p)$, so $u \in T$ and $u \operatorname{dom} p$. If $u$ did not strictly dominate $w$, then $w \in DF(u) \subseteq T$, which is false. So $u \operatorname{sdom} w$, and $d(w)$ is $u$ or a node below $u$. As $w \notin T$, $d(w) \operatorname{sdom} w$, so by Lemma 1 $d(w) \operatorname{dom} p$, and $d(w)$ is $u$ or a node above $u$. So $d(w) = u$.

Now let $y \in J(X)$ through $P_1 = a_0, \ldots, a_k$ and $P_2 = b_0, \ldots, b_l$, with $a_k = b_l = y$. Let $a_i$ be the last node of $a_0, \ldots, a_{k-1}$ that is in $T$. It exists, as $a_0 \in X$. The nodes $a_{i+1}, \ldots, a_{k-1}$ are not in $T$, so the claim gives $d(a_{k-1}) = d(a_i) = a_i$. So $a_i \operatorname{dom} a_{k-1}$. If $a_i$ does not strictly dominate $y$, then $y \in DF(a_i) \subseteq DF^+(X)$ and we are done. In the same way, with $b_j$ the last node of $b_0, \ldots, b_{l-1}$ in $T$, either $y \in DF^+(X)$ or $b_j \operatorname{sdom} y$.

Suppose $a_i \operatorname{sdom} y$ and $b_j \operatorname{sdom} y$. Both are on the dominator chain of $y$, so one dominates the other; say $b_j \operatorname{dom} a_i$. They are not equal: they are nodes of $P_1$ and $P_2$ other than $y$. So $a_i$ does not dominate $b_j$, and some path from $r$ to $b_j$ avoids $a_i$. Follow it with the part of $P_2$ from $b_j$ to $y$. The nodes of $P_2$ other than $y$ are not on $P_1$, and $a_i \ne y$, so the whole path avoids $a_i$. This contradicts $a_i \operatorname{sdom} y$. $\square$

**Lemma 4.** $DF^+(S \cup DF^+(S)) = DF^+(S)$.

*Proof.* Let $X = S \cup DF^+(S)$. Then $DF(X) = DF^+(S)$, and $DF(X \cup DF^+(S)) = DF(X) = DF^+(S)$. So $DF^+(S)$ contains $DF(X)$ and is closed, and $DF^+(X)$ is the least such set, so $DF^+(X) \subseteq DF^+(S)$. The other inclusion holds because $DF^+$ is monotone. $\square$

**Theorem 1.** $J^+(S) = DF^+(S)$. So lines L3 to L8 place a phi-function for $v$ at exactly the blocks where minimal SSA form needs one.

*Proof.* ($\supseteq$) By induction on the sequence $DF_1 = DF(S)$, $DF_{i+1} = DF(S \cup DF_i)$, each $DF_i \subseteq J^+(S)$. Every $x$ with $x \ne r$ in $S \cup J^+(S)$ has $DF(x) \subseteq J(\{r, x\}) \subseteq J(S \cup J^+(S)) = J^+(S)$, by Lemma 2 and monotonicity, and $DF(r) = \emptyset$ because $r$ strictly dominates every other node and has no predecessors. So $DF_1 \subseteq J^+(S)$, and if $DF_i \subseteq J^+(S)$, then $DF_{i+1} = DF(S \cup DF_i) \subseteq J^+(S)$.

($\subseteq$) Let $\Phi = DF^+(S)$. By Lemmas 3 and 4, $J(S \cup \Phi) \subseteq DF^+(S \cup \Phi) = \Phi$. So $\Phi$ is a valid placement, and the least one, $J^+(S)$, lies inside it. $\square$

Lines L4 to L8 compute $DF^+(S)$ by the standard worklist, which returns the limit of the sequence (this is Lemma 4 of the [dominance frontier computation](/dominance-frontier-computation/) proof). The flag `has_phi` puts at most one phi-function for $v$ in each block.

## Part 2. Renaming is correct

Fix $v$ again. After line L8, the *definition points* of $v$ are: the entry definition at the top of $r$, each phi-function for $v$ at the top of a block of $\Phi$, and each instruction that assigns $v$. A *point* is a position between two instructions of a block, or the end of a block (after the last instruction, before the terminator). A definition point $D$ in block $c$ *dominates* a point $q$ in block $b$ if $c \operatorname{sdom} b$, or $c = b$ and $D$ comes before $q$. For each point $q$, the definition points that dominate it form a chain: those in strict dominators of $b$, ordered by depth in the tree and then by position, followed by those above $q$ in $b$. The entry definition is always in it. Let $dd(q)$ be the last one, the *nearest dominating definition*.

**Lemma 5.** Let $(p, w)$ be an edge and let $w$ have no phi-function for $v$. Then $dd(\text{top of } w) = dd(\text{end of } p)$.

*Proof.* Let $D = dd(\text{end of } p)$, in block $c$. Then $c \operatorname{dom} p$, and $c \in S \cup \Phi$. If $c$ did not strictly dominate $w$, then $w \in DF(c) \subseteq DF^+(S) = \Phi$ (by Lemma 4, $DF(S \cup \Phi) \subseteq \Phi$), and $w$ would have a phi-function. So $c \operatorname{sdom} w$, and $D$ dominates the top of $w$.

Every definition point that dominates the top of $w$ lies in a block $c'$ with $c' \operatorname{sdom} w$, because $w$ has no definition point at its top. By Lemma 1, $c' \operatorname{dom} p$, so the point also dominates the end of $p$. So the chain for the top of $w$ is part of the chain for the end of $p$, and it contains $D$, the last element of the larger chain. Hence $D$ is its last element too. $\square$

**Theorem 2 (the dynamic meaning).** Along every path from $r$, and so in every run, at every point $q$, the last definition point of $v$ that was passed is $dd(q)$. Phi-functions count as passed when their block is entered.

*Proof.* Let $E$ be the last definition point passed before $q$; it exists because the entry definition runs first. Right after $E$, the nearest dominating definition is $E$ itself. Between $E$ and $q$, the run executes no definition point of $v$. Moving inside a block past instructions that do not define $v$ does not change $dd$. Moving along an edge $(p, w)$ into a block that has no phi-function for $v$ does not change $dd$, by Lemma 5. A block with a phi-function for $v$ cannot be entered in this stretch, because the phi-function would be executed. So $dd(q) = E$. $\square$

**Theorem 3 (the walk).** Lines L9 to L17 give each use of $v$ at a point $q$ the name of $dd(q)$. For a phi operand of $v$ in block $w$ that belongs to the edge $(p, w)$, the use is at the end of $p$, and the walk gives it the name of $dd(\text{end of } p)$.

*Proof.* Invariant: when the walk is at a point $q$ of block $b$, the stack of $v$ holds the names of the definition points of $v$ that dominate $q$, in chain order, except that the entry definition of a variable that is not a parameter is left implicit. This holds at the top of $r$: line L9 pushes each parameter, and the stacks of the other variables are empty. Lines L11 and L13 push a name exactly when the walk passes a definition point, which then dominates the following points of $b$. When the walk enters a child $c$ of $b$ in the tree, at line L16, the points of $b$ above the end all dominate the top of $c$, and no other definition points do except those in the strict dominators of $b$, which are already on the stack below them. Line L17 pops what $b$ pushed, so the stacks are restored when the walk goes back up. So the top of the stack is $dd(q)$, or the stack is empty and $dd(q)$ is the entry definition $v.0$, which the function `top` returns.

Lines L12 and L13 read the top before they push the new definition, so an instruction like `x = x + 1` reads the old name. Lines L14 and L15 run after all instructions of $b$, so they fill the operand of the edge $(b, s)$ with $dd(\text{end of } b)$. $\square$

**Corollary (correctness of the output).** Take a run of the input program that never reads a variable before it has a value. In the matching run of the output, each instruction reads, at each use, the name of the last definition of that variable that was executed, by Theorems 2 and 3, and that name holds the value the input program would read. The branches go the same way, so the two runs follow the same blocks and return the same value. A phi operand $v.0$ is read only on a path where the input program does not read $v$, because $v.0$ is never the last definition before a real use in such a run. Every use names the definition at $dd(q)$, which dominates $q$, so the output is strict. Each name has one definition point, so each use has exactly one reaching definition.

**Corollary (the output is conventional).** At any point $q$, the only version of $v$ that is live is the one defined at $dd(q)$. If $v.k$ is live at $q$, there is a path from $q$ to a use of $v.k$ with no definition of $v.k$ on it. If that path had any definition point of $v$, the last one before the use would be $dd$ of the use, which is the definition of $v.k$, so the use would not see $v.k$ from $q$. So the path has no definition point of $v$, and by Theorem 2, applied to a run through $q$ along that path, $dd(q)$ is the definition of $v.k$. So the versions of one variable never interfere, and mapping each $v.k$ back to $v$ and deleting the phi-functions, as `strip_versions` does, keeps the meaning.

**Running time.** Lines L1 and L2 read each instruction once. For one variable, the worklist of lines L4 to L8 takes each block of $S \cup \Phi$ once and reads its frontier once, which costs $O(|S| + |\Phi| + \sum_{x \in S \cup \Phi} |DF(x)|) = O(n + D)$, with $D$ the total size of the frontiers. Over $V$ variables this is $O(V (n + D))$, and the sum of $|S|$ over all variables is at most the number of instructions plus $V$. The walk visits each block once, each instruction once and each phi operand once, so it takes time linear in the size of the output, which is $O(I + V m)$ for $I$ instructions and $m$ edges.
