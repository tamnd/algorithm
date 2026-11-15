---
title: Sparse conditional constant propagation computes the greatest fixed point of the combined system
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a program in strict SSA form: every name $x$ has exactly one definition $s_x$, in block $blk(x)$, and that definition dominates every use of $x$ (for a phi operand, the use is at the end of the predecessor). The entry block has no predecessor. $L$ is the flat lattice $\top \sqsupset c \sqsupset \bot$ for every integer $c$; its height is 2. $\gamma(\top) = \emptyset$, $\gamma(c) = \{c\}$ and $\gamma(\bot) = \mathbb{Z}$ give the concrete values that a lattice value describes. $e_0 = (\mathit{start}, entry)$ is a pseudo edge. A *state* is a pair $(V, E)$: $V$ maps every name to $L$, and $E$ is a set of CFG edges together with $e_0$. $Reach(E)$ is the set of blocks $b$ with some $(p, b) \in E$. States are ordered by

$$(V, E) \sqsubseteq (V', E') \iff V[x] \sqsubseteq V'[x] \text{ for every } x \text{ and } E \supseteq E'.$$

A higher state knows more: higher values and fewer edges. The states form a finite complete lattice, with top $(\top, \{\})$.

For an instruction $s$ in block $b$, $ev_E(s, V)$ is its abstract value: for a phi, the meet of $V[a_p]$ over the operands $a_p$ with $(p, b) \in E$ (the empty meet is $\top$); for $x = k$, the constant $k$; for a copy of $a$, $V[a]$; for $a \mathbin{op} c$, $fold(op, V[a], V[c])$, where any $\top$ operand gives $\top$, else any $\bot$ gives $\bot$, else the operation runs and a trap gives $\bot$; for a call, $\bot$. An int operand $k$ has the value $k$. $allowed(b, V)$ is the set of successors that the terminator of $b$ may take: both targets of `br a L1 L2` when $V[a] = \bot$, none when $V[a] = \top$, and only `L1` (if $c \ne 0$) or only `L2` (if $c = 0$) when $V[a] = c$; the target of a `jump`; none for `ret`. The combined map is $\Phi(V, E) = (V', E')$ with

- $V'[p] = \bot$ for each parameter $p$; $V'[x] = ev_E(s_x, V)$ if $blk(x) \in Reach(E)$, and $V'[x] = \top$ otherwise;
- $E' = \{e_0\} \cup \{(b, t) : b \in Reach(E),\ t \in allowed(b, V)\}$.

We use the lines L1 to L15 of the pseudocode.

**Lemma 1 (Φ is monotone).** If $(V, E) \sqsubseteq (W, F)$ then $\Phi(V, E) \sqsubseteq \Phi(W, F)$.

*Proof.* From $E \supseteq F$ we get $Reach(E) \supseteq Reach(F)$. Take a name $x$. If $blk(x) \notin Reach(F)$, the right side gives $\top$, which is above anything. Otherwise $blk(x)$ is in both sets. A phi meets fewer operands under $F$ than under $E$, and each operand value is higher in $W$, so its value under $(W, F)$ is higher. $fold$ is monotone in each operand: going up from $\bot$ to $c$ to $\top$ gives $\bot$, then a constant or $\bot$, then $\top$. So $ev_E(s_x, V) \sqsubseteq ev_F(s_x, W)$. For the edges, $allowed(b, \cdot)$ is antitone: a higher condition value allows fewer targets ($\bot$ allows two, $c$ one, $\top$ none). With $Reach(E) \supseteq Reach(F)$ this gives $E' \supseteq F'$. $\square$

By the Knaster-Tarski theorem, $\Phi$ has a greatest fixed point $G = (V_G, E_G)$, and $G$ is the join of all states $S$ with $S \sqsubseteq \Phi(S)$.

**Lemma 2 (values only go down).** Every assignment to $V[x]$ at line L13 replaces the old value by a value strictly below it.

*Proof.* Only the visits of $s_x$ write $V[x]$. Line L13 writes only when the new value differs from the old one. Use induction over time. The first write replaces $\top$, and any other value is below $\top$. For a later write, compare the current visit of $s_x$ with the visit that made the previous write. By the induction hypothesis no value went up in between, and $Exec$ only grows. Since $ev$ is monotone in $V$ and antitone in $E$ (Lemma 1), the new value is below or equal to the old one, and it differs, so it is strictly below. $\square$

**Lemma 3 (termination and the bounds).** Each name changes at most twice. Each SSA edge $(x, u)$ is put on SSAWL at most twice and taken off at most twice. Each CFG edge is put on FlowWL at most once. So the main loop runs at most $1 + m + 2s$ times, where $m$ is the number of CFG edges and $s$ the number of SSA edges.

*Proof.* By Lemma 2 the values of $x$ form a strictly falling chain in $L$, which has height 2, so there are at most two changes. Line L13 puts $(x, u)$ on SSAWL once per change of $V[x]$. FlowWL takes an edge only if it was never put there before. Each turn of the loop at line L4 removes one item from one list. $\square$

**Lemma 4 (the state stays above $G$).** At all times $V[x] \sqsupseteq V_G[x]$ for every $x$ and $Exec \subseteq E_G$.

*Proof.* Induction over time. At line L1 the parameters get $\bot = V_G[p]$ and every other name gets $\top$; $Exec$ is empty. Every edge on FlowWL is in $E_G$: $e_0$ is in $E_G$; any other edge $(b, t)$ was put there by the visit of the terminator of a block $b \in Visited = Reach(Exec) \subseteq Reach(E_G)$, with $t \in allowed(b, V)$ for the values $V$ of that moment. Those values are above $V_G$, and $allowed$ is antitone, so $t \in allowed(b, V_G)$ and $(b, t) \in \Phi(G)$'s edge set, which is $E_G$. So line L7 keeps $Exec \subseteq E_G$. A write at line L13 stores $ev_{Exec}(s_x, V)$ for a block in $Visited \subseteq Reach(E_G)$; by Lemma 1 this is above $ev_{E_G}(s_x, V_G) = V_G[x]$. $\square$

**Lemma 5 (the final state is a fixed point).** When both lists are empty, $(V, Exec) = \Phi(V, Exec)$ and $Visited = Reach(Exec)$.

*Proof.* A block enters $Visited$ exactly when the first edge into it is taken at line L7, so $Visited = Reach(Exec)$. Take an instruction $s_x$ in a block $b \in Visited$. Its value under $ev$ depends on $V$ at its operands and, for a phi, on the edges into $b$ in $Exec$. Each of these inputs changes only at a moment that leads to a new visit of $s_x$: when $b$ enters $Visited$, line L8 visits every instruction of $b$; when an edge into $b$ joins $Exec$, line L7 visits every phi of $b$; when an operand $y$ changes, line L13 puts $(y, s_x)$ on SSAWL, and since $b \in Visited$ from then on, line L10 visits $s_x$ when that item comes off. So the last visit of $s_x$ came after the last change of its inputs, and $V[x] = ev_{Exec}(s_x, V)$. A name whose block is not in $Visited$ is never visited, so it keeps $\top$, as $\Phi$ asks. The same argument for the terminator of $b$ shows that its last visit saw the final value of its condition, so every edge of $allowed(b, V)$ was put on FlowWL and is now in $Exec$. Conversely, each edge in $Exec$ other than $e_0$ was put there for values above the final ones, and $allowed$ is antitone, so it is in $allowed(b, V)$ for the final $V$. So $Exec$ is exactly the edge set of $\Phi(V, Exec)$. $\square$

**Theorem 1 (correctness).** SCCP terminates and returns $(V, Exec) = G$, the greatest fixed point of $\Phi$.

*Proof.* Lemma 3 gives termination. By Lemma 5 the result is a fixed point, so it is below the greatest fixed point $G$. By Lemma 4 it is above $G$. $\square$

**Lemma 6 (nothing reachable stays ⊤).** In $G$, every name defined in a block of $Reach(E_G)$ has a value below $\top$. The same holds for the greatest fixed point of any CP pass below, whose blocks are all reachable.

*Proof.* Order the blocks of $Reach(E_G)$ by the first time SCCP takes an edge into them, and the instructions of a block by position. Use induction on this order. A phi in $b$ has an operand along the first edge $(p, b)$ that SCCP took. $p$ was reached before $b$, so $p \ne b$ and $p$ is not dominated by $b$; the definition of the operand dominates the end of $p$, so it lies in a block reached before $b$ (or is a parameter or an int). By induction its value is below $\top$, and a meet with it stays below $\top$. Any other instruction reads names defined earlier in $b$ or in blocks that strictly dominate $b$, which are reached before $b$; operands below $\top$ give $fold$ a value below $\top$. $\square$

So in the result of SCCP, the condition of every reachable branch is a constant or $\bot$, and the rewrite never meets a $\top$.

**Theorem 2 (soundness).** Let a run of $P$ on any arguments assign the value $v$ to a name $x$. Then $v \in \gamma(V[x])$. Every block the run enters is in $Visited$, and every edge it takes is in $Exec$.

*Proof.* Induction on the steps of the run. The run starts at the entry along $e_0 \in Exec$, and the parameters have $V = \bot$. When the run executes $s_x$ in a block $b$, the induction hypothesis says $b \in Visited$ and the edge $(p, b)$ it came by is in $Exec$. Every operand $y$ that $s_x$ reads holds the value assigned at the last run of $s_y$, because $y$ has only one definition, and by hypothesis that value is in $\gamma(V[y])$. For a phi, the run reads the operand $a_p$ of the edge it came by; $(p, b) \in Exec$, so $V[x] \sqsubseteq V[a_p]$ and $\gamma(V[a_p]) \subseteq \gamma(V[x])$. For $a \mathbin{op} c$: if both operand values are constants, they are the run's values and $fold$ computes the same result (if the operation traps, the run stops there). Otherwise some operand value is $\bot$ (it is not $\top$, since $\gamma(\top)$ is empty), and $fold$ gives $\bot$. At a branch on $a$ with run value $v_a \in \gamma(V[a])$: if $V[a] = \bot$ both edges are in $Exec$; if $V[a] = c$ then $v_a = c$ and the edge that $c$ picks is in $Exec$. $\square$

So the rewrite is safe: it replaces a name by a constant only where every run computes that constant, and it removes only blocks and edges that no run reaches.

**Theorem 3 (at least as strong as any order of CP and DBE).** A CP pass runs simple constant propagation on the current program, counting every remaining edge, and replaces each name with a constant value by that constant (both its definition and its uses; a branch keeps its form with a literal condition). A DBE pass turns each branch on a literal into a jump, then removes the blocks that the entry no longer reaches and the phi operands of the removed edges. Let $Q$ be the program after any finite sequence of such passes, applied to $P$. Then every block of $Reach(E_G)$ is still in $Q$, and every name that $Q$ defines as a constant $k$ has $V_G[x] \in \{k, \top\}$.

*Proof.* Describe a program $Q$ by the state $S_Q = (V_Q, E_Q)$: $E_Q$ is $e_0$ plus the edges of $Q$ (each one is an edge of $P$); $V_Q[x] = k$ if $Q$ defines $x$ as the constant $k$, $V_Q[x] = \top$ if $blk(x)$ is not in $Q$, and $V_Q[x] = \bot$ otherwise. The claim says $S_Q \sqsubseteq G$. Since $G$ is the join of all post-fixed points, it is enough to show $S_Q \sqsubseteq \Phi(S_Q)$ for every $Q$ in the sequence. Two facts hold by induction along the sequence. (a) Every block of $Q$ is reachable in $Q$: $P$ has no unreachable block, CP removes no edge, and DBE removes the blocks it cuts off. So $Reach(E_Q)$ is the block set of $Q$. (b) The known constants only grow: a CP pass keeps every constant definition, because each one is a fixed point of its own equation; and DBE removes a constant definition only together with its block.

*Edges.* Take a block $b$ of $Q$. If its terminator in $Q$ is a branch, both edges are in $E_Q$, and $allowed(b, V_Q)$ is a subset of them. If it is a jump made by DBE from a branch on $y$, then DBE saw a literal $c$, which CP wrote because $Q$ then defined $y$ as $c$; by (b) $V_Q[y] = c$ still, so $allowed(b, V_Q)$ is the one target of the jump. Other jumps and returns are as in $P$. So $\Phi(S_Q)$ has no edge outside $E_Q$.

*Values.* If $V_Q[x]$ is $\bot$ or $x$ is a parameter, there is nothing to show. If $blk(x)$ is not in $Q$, then $blk(x) \notin Reach(E_Q)$ and $\Phi$ gives $\top$ as well. Otherwise $Q$ defines $x$ as $k$, and a CP pass on an earlier program $Q'$ found the value $k$ for $x$ as the greatest fixed point of simple constant propagation on $Q'$, with $E_{Q'} \supseteq E_Q$. In that fixed point every operand of $s_x$ that reaches $b$ by an edge of $E_{Q'}$ had a value below $\top$ (Lemma 6 applied to $Q'$), so it was a constant (an operand with value $\bot$ would make $fold$ give $\bot$, and a phi with a $\bot$ operand gives $\bot$). That CP pass made each of those operands a constant definition, so by (b) $V_Q$ gives each of them the same constant. Now $ev_{E_Q}(s_x, V_Q)$ reads the same constants, over a subset of the phi operands; it is $k$, or $\top$ for an empty meet. Either way it is above $V_Q[x] = k$. $\square$

**Proposition 4 (without loops the gap closes).** If the CFG of $P$ has no cycle, every sequence of CP and DBE passes that runs until neither pass changes the program ends with $S_Q = G$.

*Proof.* At the end, CP finds no new constant, so on the blocks of $Q$ the values $V_Q$ are the greatest fixed point of simple constant propagation over $E_Q$, with $\bot$ for the rest; and DBE finds no literal branch, so each remaining branch has a condition of value $\bot$ (Lemma 6 rules out $\top$). Then $\Phi(S_Q) = S_Q$: the edges agree because a branch on $\bot$ allows both targets, and the values agree because they solve the same equations. Now show that an acyclic $P$ has only one fixed point of $\Phi$. Take the blocks in a topological order. Whether a block is in $Reach(E)$ depends only on the terminators and the values of earlier blocks; the value of a name depends only on names defined earlier in the same block, in dominating blocks, or at the ends of predecessors, all of which come earlier in the order. So the fixed point equations fix every component one after the other, and $S_Q = G$. $\square$

With a loop the equations can have several fixed points, and the passes can stop at a lower one. The example on the page is such a case: simple constant propagation sees `i = 2` flow around the loop, so it never makes the branch literal, while SCCP never takes the edge into the block that sets `i = 2`.
