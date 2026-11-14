---
title: BUILD followed by SCHEDULE keeps the outcome of every run
proves: [correctness]
status: full
---

We use the notation of the page. $P$ is a toy IR procedure with const, copy and op instructions, every block is reachable, the entry has no predecessor, and no run of $P$ reads a name before it is defined. $G_0$ is the graph after line L14, $G$ the graph after line L15, and $O$ the program that SCHEDULE gives. We show that for all arguments, $P$ and $O$ return the same value, or both trap.

## 1. Values along a run

Fix the arguments and the run of $P$. A *time* is a position in the run between two steps. Control enters blocks one after the other. For a block $B$ with $k \ge 2$ predecessors and a time $t$ after the first entry into $B$, let $j$ be the index of the edge of the last entry into $B$ at or before $t$, and $s$ the time just before that entry, at the end of the predecessor. Define the value $V_t(m)$ of a node $m$ of $G_0$ (or of $G$) by

- $V_t(\mathrm{PARAM}\ p)$ is the argument $p$, $V_t(\mathrm{CONST}\ k) = k$, $V_t(\mathrm{UNDEF}) = 0$;
- $V_t(\mathrm{OP}(op, a, b)) = op(V_t(a), V_t(b))$, which is undefined if $op$ traps on these values (a control input is ignored);
- $V_t(\mathrm{PHI})$ at $B$ is $V_s(\text{input } j)$, with $j$ and $s$ as above.

The recursion is well founded, because a PHI refers to an earlier time and the OP inputs of a node were made before it. Between two block entries no $V_t$ changes, and entering $B$ changes only the values of PHIs of $B$ and of nodes that depend on them.

**Lemma 1 (BUILD is faithful on $G_0$).** At every time $t$ in the run of $P$, inside block $B$ before instruction $i$, every name $x$ that is defined at that point has the value $V_t(\mathit{map}[x])$, where $\mathit{map}$ is the map of lines L3 to L9 at that point. A terminator `br a` or `ret a` reads $V_t(\mathit{map}[a])$, and an instruction with a trapping operator traps exactly when the value of its OP node is undefined.

*Proof.* By induction over the run. At the start, the parameters map to PARAM nodes. An instruction `x = k` or `x = a` changes the value of $x$ and $\mathit{map}[x]$ in the same way. For `x = a op b`, the new value is $op(V_t(\mathit{map}[a]), V_t(\mathit{map}[b]))$, which is $V_t$ of the OP node of lines L7 and L8. When line L8 returns an older node from the hash table, that node has the same operator and the same inputs, so it has the same value. At an edge into a block $B$ with one predecessor, the map is copied and no value changes. At the $j$-th edge into a block $B$ with two or more predecessors, every name $x$ maps to the PHI of $x$ at $B$, whose new value is $V_s(\mathit{out}[P_j][x])$, the value of $x$ at the end of $P_j$ by induction. $\square$

## 2. Homes and freshness

Define the *home* of a node: the entry for PARAM, CONST and UNDEF, the block of a PHI or of a pinned OP, and for a floating OP the deepest home of its inputs in the dominator tree. This is the block early$[n]$ of line L18.

**Lemma 2.** In $G_0$, the homes of the inputs of a floating OP lie on one path of the dominator tree, and the home of every node that appears in $\mathit{map}$ at a point of block $B$, or in $\mathit{out}[B]$, dominates $B$.

*Proof.* By induction over BUILD. The entry map holds nodes with home the entry. A block with one predecessor $P$ copies $\mathit{out}[P]$, and $P$ dominates it. A block with two or more predecessors maps every name to its own PHIs. A new OP in $B$ has inputs whose homes dominate $B$. The dominators of $B$ form a path of the tree, so the deepest home is well defined and dominates $B$. A node returned by the hash table has the same inputs and so the same home. $\square$

The *cone* of a node is the node with all nodes that it reaches through data inputs, without going through a PHI's inputs. A value $V_t(m)$ depends only on the PHIs in the cone of $m$, and on their last entries. Every PHI in the cone of $m$ has a home that dominates the home of $m$, by the definition of home.

**Lemma 3 (freshness).** Let $X$ be a block that the home of every PHI in the cone of $m$ dominates. Let $r$ be a time in a visit of $X$ after its PHIs have been assigned, and $t \ge r$ a time in a block $Y$ that $X$ dominates, such that the run does not enter $X$ between $r$ and $t$. Then $V_t(m) = V_r(m)$.

*Proof.* Suppose not. Then some PHI $\varphi$ in the cone is at a block $H$ that is entered at a time $u$ with $r < u \le t$. $H \ne X$, since $X$ is not entered again. $H$ dominates $X$, so a path from the entry to the first visit of $H$ does not pass $X$. Join it with the part of the run from $u$ to $t$, which does not pass $X$. This is a path from the entry to $Y$ that avoids $X$, which contradicts that $X$ dominates $Y$. $\square$

## 3. Removing trivial PHIs

**Lemma 4.** Let $\varphi$ be a PHI at block $B$ whose inputs are all $\varphi$ or $w$, with $w \ne \varphi$. Then the home of $w$ strictly dominates $B$, and $V_t(\varphi) = V_t(w)$ at every time $t$ in a block that $B$ dominates.

*Proof.* By Lemma 2, an edge $P \to B$ with input $\varphi$ has $\varphi$ in $\mathit{out}[P]$, so $B$ dominates $P$. The first entry into $B$ on any path comes from a predecessor that $B$ does not dominate, so through an edge with input $w$, whose predecessor the home of $w$ dominates. So every path to $B$ passes the home of $w$. That home is not $B$: otherwise $B$ would dominate the predecessor of that edge. So the home of $w$ strictly dominates $B$.

Now fix $t$. Following the last entries into $B$ backward, each through an edge with input $\varphi$, we reach a last entry through an edge with input $w$ at time $s$, and $V_t(\varphi) = V_s(w)$. All entries into $B$ in $(s, t]$ come from predecessors that $B$ dominates. Suppose the run enters the home $X$ of $w$ at a time $u \in (s, t]$. The part of the run from $u$ to the next entry into $B$ ends with an entry from a predecessor that $B$ dominates, and before that entry it does not pass $B$. Joined with a path from the entry to the first visit of $X$, which avoids $B$, it gives a path to that predecessor that avoids $B$, a contradiction. If there is no entry into $B$ after $u$, the same argument applies with $t$ in place of that entry, since $B$ dominates the block of $t$. So $X$ is not entered in $(s, t]$, and Lemma 3, with $X$ the home of $w$, gives $V_t(w) = V_s(w)$. $\square$

By Lemma 2, every place where $\varphi$ is read, through a map or through the inputs of a node, is at a time in a block that $B$ dominates. So replacing $\varphi$ by $w$ changes no value that is ever read, and Lemma 1 holds for $G$ as well. Repeating the step for each removed PHI gives the same for line L15.

## 4. SCHEDULE

Let $\mathit{block}[n]$ be the placement of lines L17 to L23. For a pinned node it is its own block. For a floating node, line L22 picks a block on the dominator tree path from the LCA of its use blocks up to early$[n]$. This path exists: by induction in the order of line L19, each use block is dominated by the block of the user, which the home of the user dominates, and the home of $n$ dominates the home of each user. So:

- (S1) the block of each input of $n$ dominates $\mathit{block}[n]$, and within one block line L24 puts the inputs first;
- (S2) $\mathit{block}[n]$ dominates the block of every non-PHI use, and the predecessor through which every PHI use reads $n$.

**Lemma 5.** The runs of $P$ and $O$ on the same arguments visit the same blocks through the same edges, up to the first trap or return. At every time $t$ at which $O$ reads the name of a node $n$, the name holds $V_t(n)$.

*Proof.* By induction over the run. Suppose $O$ reads the name of $n$ at time $t$ in block $Y$, where $Y$ is the use block of (S2). $\mathit{block}[n]$ dominates $Y$, so it was visited, and its last visit at or before $t$ ran the instruction of $n$ at a time $r$, before the read if both are in the same block visit (S1). By induction, the inputs read at $r$ held $V_r$ of the input nodes, so the name of $n$ got $V_r(n)$. The homes of the PHIs in the cone of $n$ dominate the home of $n$, which dominates $\mathit{block}[n]$, and the run does not enter $\mathit{block}[n]$ in $(r, t]$. Lemma 3 with $X = \mathit{block}[n]$ gives $V_t(n) = V_r(n)$. A PHI instruction of $O$ at $B$, entered through the edge $j$, reads its $j$-th input at the end of $P_j$ and so gets $V_s(\text{input } j)$, which is the new $V$ of the PHI. A `br` reads $V_t$ of its condition node, the same value that $P$ reads by Lemma 1, so both runs take the same edge. $\square$

**Theorem.** $P$ and $O$ have the same outcome on all arguments.

*Proof.* By Lemma 5 both runs pass the same blocks. If $P$ returns in block $B$, it returns $V_t$ of the RETURN input, and so does $O$. If $P$ traps in a visit of $B$, it traps at an instruction whose OP has an undefined value. That OP is pinned to $B$, and $O$ runs every pinned OP of $B$ in that visit before the terminator, while floating OPs never trap. Values do not change inside a block visit, so $O$ traps in the same visit, at that instruction or at another one that also traps. If $P$ does not trap in a visit, no pinned OP of that block has an undefined value, so $O$ does not trap there either. $\square$
