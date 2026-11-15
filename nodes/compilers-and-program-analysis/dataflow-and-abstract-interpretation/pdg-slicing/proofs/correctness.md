---
title: The PDG slice is the dependence slice, and its projection keeps the criterion values on every run that returns
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a toy IR program with instructions `x = k`, `x = y` and `x = a op b` and terminators `jump`, `br` and `ret`, in which every block reaches a `ret`. Statements, the successor relation $n \to m$, $DEF$ and $REF$ are as on the page. The criterion is $C = \langle p, V \rangle$. Post-dominance is taken on blocks with a virtual EXIT after every `ret`; $d_\ell$ is the immediate post-dominator of block $\ell$. Block $y$ is *control dependent* on block $x$, written $y \in CD(x)$, if some successor $s$ of $x$ is post-dominated by $y$ ($y = s$ allowed) and $y$ does not strictly post-dominate $x$.

**The graph.** We use the two facts proved on the [program dependence graph](/program-dependence-graph/) page and checked by the tests against brute force: the control parents of a statement in block $y$ are the branches of the blocks $x$ with $y \in CD(x)$, plus ENTRY for some blocks; and the data parents of $t$ are the pairs $(s, x)$ with $x \in REF(t)$, $x \in DEF(s)$ and a path from the successor of $s$ to $t$ with no definition of $x$ before $t$, plus pairs $(\text{ENTRY}, x)$ for parameters. The reaching definitions at $p$ are the pairs $(s, x)$ with such a path from the successor of $s$ to $p$.

## 1. The search finds the dependence slice

Let $K^\ast$ be the dependence slice of [program slicing](/program-slicing/): the least set of instructions and branches that contains (rule 1) every $s$ that defines some $x \in V$ with a path from the successor of $s$ to $p$ free of definitions of $x$, (rule 2) every branch on which $p$ is control dependent, and (rule 3) every instruction or branch on which a member is data or control dependent.

**Lemma 1.** PDG-SLICE stops and returns $K^\ast$.

*Proof.* Lines L2 and L3 put into the start set exactly the statements of rules 1 and 2 (ENTRY is left out, and it is not a statement). The loop adds a node only if it is not yet in $S$, and there are finitely many statements, so it stops. Every node it adds is a parent of a node of $S$, so by induction on the order of addition every node of $S$ is in $K^\ast$ (rule 3). When the loop stops, every node of $S$ has been removed from the work list once and all its parents other than ENTRY are in $S$, so $S$ is closed under rule 3 and contains the sets of rules 1 and 2. Hence $K^\ast \subseteq S$, by the leastness of $K^\ast$. $\square$

Each node enters the work list at most once and each edge is read once, so the search costs $O(n + e)$ for $n$ statements and $e$ edges.

## 2. Relevant names of the slice

From here on, $S$ is any set of instructions and branches that contains the statements of rules 1 and 2 and is closed under rule 3. Lemma 1 shows that the PDG slice is one. For a statement $n$, let $R(n)$ be the set of names $x$ such that some path $n = n_0 \to n_1 \to \cdots \to n_k$, $k \ge 0$, has no definition of $x$ among $n_0, \ldots, n_{k-1}$ and ends either at $n_k = p$ with $x \in V$, or at some $n_k \in S$ with $x \in REF(n_k)$.

**Lemma 2.** For every statement $n$ and successor $m$:

- (F1) if $n \in S$, then $REF(n) \subseteq R(n)$; in all cases $R(m) \setminus DEF(n) \subseteq R(n)$;
- (F2) if $n$ is an instruction not in $S$, then $DEF(n) \cap R(m) = \emptyset$, so $R(m) \subseteq R(n)$;
- (F3) if $n$ is a terminator, then $R(m) \subseteq R(n)$;
- (F4) $V \subseteq R(p)$;
- (F5) for a `ret` statement $r$, $R(r) = V$ if $r = p$ and $R(r) = \emptyset$ otherwise.

*Proof.* F1: a path of length 0 for the first part; for the second, put $n$ in front of the path for $x$ from $m$, which is allowed since $n$ does not define $x$. F2: let $x \in DEF(n) \cap R(m)$ by a path from $m$. If it ends at $p$ with $x \in V$, then $n$ satisfies rule 1. If it ends at $u \in S$ that reads $x$, then $u$ is data dependent on $n$, and rule 3 puts $n$ in $S$. Both contradict $n \notin S$. The second part follows from F1. F3: a terminator defines nothing, so F1 applies. F4: a path of length 0. F5: a `ret` has no successor, so only paths of length 0 count, and a `ret` is never in $S$, because $S$ holds only instructions and branches. $\square$

## 3. Influence and control dependence

For a block $\ell$ that ends in a branch, let $INFL(\ell)$ be the set of blocks reachable from a successor of $\ell$ by a path that does not enter $d = d_\ell$. Two standard facts about post-dominance: (PD1) if $a$ and $b$ post-dominate each other, then $a = b$; (PD2) the strict post-dominators of a block form a chain under post-dominance, and the immediate one is post-dominated by all the others.

**Lemma 3.** Every $y \in INFL(\ell)$ is in $CD^+(\ell)$, the transitive closure of control dependence from $\ell$. Also, $d$ strictly post-dominates every $y \in INFL(\ell)$, and $INFL(\ell)$ holds no `ret` block when $d \ne$ EXIT.

*Proof.* (KF) $y \ne d$ by definition. Take any path from $y$ to EXIT and put in front of it the path from $\ell$ to $y$ that avoids $d$ after $\ell$. The result runs from $\ell$ to EXIT, so it meets $d$, and only in the part after $y$. So $d$ strictly post-dominates $y$. If $y$ were a `ret` block, the path $y \to$ EXIT would avoid $d \ne$ EXIT.

Now let $\ell = s_0, s_1, \ldots, s_k = y$, $k \ge 1$, be a path with $s_1, \ldots, s_k \ne d$. Induction on $k$. Let $j$ be the largest index in $0, \ldots, k - 1$ such that $y$ does not post-dominate $s_j$. If $j$ exists, $y$ post-dominates $s_{j+1}$ (for $j + 1 = k$ trivially), so $y \in CD(s_j)$. For $j = 0$ this gives $y \in CD(\ell)$. For $j \ge 1$, $s_j \in INFL(\ell)$ by a shorter path, so $s_j \in CD^+(\ell)$ by induction, and $y \in CD^+(\ell)$. If $j$ does not exist, $y$ post-dominates $\ell$ and $s_1$. If $y = \ell$, then $y \in CD(\ell)$ through $s_1$, since a block does not strictly post-dominate itself. If $y \ne \ell$, then $y$ and $d$ both strictly post-dominate $\ell$, so $y$ post-dominates $d$ by PD2, and $d$ post-dominates $y$ by KF, so $y = d$ by PD1, which is false. $\square$

**Lemma 4.** If the branch $b$ at the end of $\ell$ is not in $S$, then no block of $INFL(\ell)$ holds a statement of $S$ or the point $p$.

*Proof.* Suppose $y \in INFL(\ell)$ holds $u \in S$ or holds $p$. By Lemma 3 there is a chain $\ell = x_0, x_1, \ldots, x_r = y$ with $x_{i+1} \in CD(x_i)$ and $r \ge 1$. Each $x_i$ with $i < r$ ends in a branch $b_i$, since a block with one successor $s$ has $s$ as its immediate post-dominator and so has no control dependents. The statement $u$ or $p$ is control dependent on $b_{r-1}$, so $b_{r-1} \in S$ by rule 3 or rule 2. Each statement of $x_{i+1}$, in particular $b_{i+1}$, is control dependent on $b_i$, so going down from $i = r - 2$ to $0$, rule 3 gives $b_i \in S$. So $b = b_0 \in S$, a contradiction. $\square$

## 4. The projection

Let $Q$ be the projection of $P$ on $S$: instructions of $S$ stay, all jumps stay, a branch of $S$ stays, a branch $b \notin S$ at the end of $\ell$ becomes `jump` $d_\ell$, or `ret 0` if $d_\ell$ is EXIT, and a `ret a` keeps $a$ only when it is the statement $p$ and $a \in V$ (by F5, exactly when $a \in R$ there). For $n = (\ell, i)$, let $\pi(n) = (\ell, j)$ with $j$ the number of instructions of $S$ in $\ell$ before position $i$; it is the place in $Q$ of the first kept statement of $\ell$ at or after $n$, and $p_Q = \pi(p)$.

Consider a run of $P$ that reads no undefined name. Say $(n, \sigma) \sim (q, \tau)$ when $q = \pi(n)$ and, for each $x \in R(n)$, $\sigma(x)$ and $\tau(x)$ are both undefined or both defined and equal.

**Lemma 5 (one step).** Let $(n, \sigma) \sim (q, \tau)$.

1. $n$ an instruction not in $S$ that does not trap: $P$ moves to $(m, \sigma')$, $Q$ stays, and $(m, \sigma') \sim (q, \tau)$.
2. $n$ an instruction in $S$: $P$ traps at $n$ if and only if $Q$ traps at $q$; otherwise both move and the relation holds after the step.
3. $n$ a jump or a branch in $S$: both move to the start of the same block with unchanged environments, and the relation holds there.
4. $n$ a `ret`: both runs return, with the same value if $Q$ kept the operand.

*Proof.* (1) $\pi(m) = \pi(n)$ because $n$ is not kept, and by F2 $n$ writes no name of $R(m) \subseteq R(n)$. (2) $Q$ runs the same instruction on operands that agree, by F1, so both trap or both compute the same value for $x = DEF(n)$; $\pi(m)$ is the next statement of $Q$, and $R(m) \subseteq R(n) \cup \{x\}$ by F1. (3) The branch reads names of $R(n)$ by F1, so it goes the same way; $R(m) \subseteq R(n)$ by F3. (4) If the operand is kept, it is in $R(n)$ by F5. $\square$

**Lemma 6 (a dropped branch).** Let $(n, \sigma) \sim (q, \tau)$ with $n$ a branch $b \notin S$ at the end of $\ell$, and $d = d_\ell$. $Q$ makes one step to the start of $d$, or returns 0 if $d$ is EXIT. Until $P$ first enters $d$, it stays in blocks of $INFL(\ell)$, makes no observation and does not return if $d \ne$ EXIT; when it enters $d$, its configuration is related to $Q$'s.

*Proof.* By the definition of $INFL$ and Lemma 3. By Lemma 4 the blocks visited hold no statement of $S$ and not $p$, so every step there is case 1 of Lemma 5 or a terminator, and by F2 and F3 the sets $R$ shrink along the run and no relevant name of the later points is written. So the environment of $P$ at the start of $d$ agrees with $\tau$ on $R$ there. $\square$

**Theorem (Reps and Yang).** For every input $I$ on which the run of $P$ reads no undefined name and reaches a `ret`, the run of $Q$ reaches a `ret` and $\mathrm{obs}_Q(I, \langle p_Q, V \rangle) = \mathrm{obs}_P(I, \langle p, V \rangle)$. If the run of $P$ traps or does not end, $\mathrm{obs}_P$ is a prefix of $\mathrm{obs}_Q$.

*Proof.* At the start the relation holds. Lemmas 5 and 6 cut the run of $P$ into pieces, each matched with at most one step of $Q$, and keep the relation at the end of each piece. The block of $p$ is never inside a dropped region (Lemma 4), so the visits of the two runs to it match one to one. In a visit, $Q$ reaches $\pi(p)$ when $P$ reaches its last kept statement before $p$, or the block start, and the statements of $P$ between there and $p$ are dropped instructions, which keep the relation. So at each observation, the environments agree on $R(p) \supseteq V$ (F4), and the tuples are equal. If $P$ returns, $Q$ returns at the matching moment (Lemma 5 case 4, or Lemma 6 with $d$ = EXIT), and neither observes again. If $P$ traps at a dropped instruction, $Q$ may go on and observe more; at a kept one, $Q$ traps too. If $P$ does not end, each of its observations is matched in order. $\square$

**Corollary.** Since the PDG slice $S$ contains the data and control parents of each of its statements, the hypotheses of section 2 also hold for the criterion $\langle t, REF(t) \rangle$ for every $t \in S$. The projections for the two criteria differ only in the operands of `ret`, which change no observation before the return. So on every run of $P$ that returns, $Q$ reaches each statement $t$ of the slice as many times as $P$ does, with the same values of $REF(t)$ each time. This is the form in which Reps and Yang stated their slicing theorem for terminating runs.
