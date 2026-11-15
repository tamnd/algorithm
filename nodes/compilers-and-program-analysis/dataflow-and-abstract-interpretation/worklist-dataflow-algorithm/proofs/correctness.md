---
title: The worklist dataflow algorithm terminates and computes the maximal fixed point
proves: [correctness, termination]
status: full
---

**Setting.** $(L, \sqcap)$ is a meet semilattice: $\sqcap$ is idempotent, commutative and associative. $x \sqsubseteq y$ means $x \sqcap y = x$; this is a partial order in which $x \sqcap y$ is the greatest lower bound of $x$ and $y$, and $\sqcap$ is monotone in each argument. $\top$ is the identity of $\sqcap$, so $x \sqsubseteq \top$ for all $x$. The height $h$ is finite: every chain $x_0 \sqsupset x_1 \sqsupset \cdots \sqsupset x_k$ has $k \le h$. $G = (V, E)$ is a directed graph with $n$ nodes and $m$ edges, $S \subseteq V$ is the set of start nodes, $\iota \in L$ is the boundary value, and each $f_v : L \to L$ is monotone: $x \sqsubseteq y$ implies $f_v(x) \sqsubseteq f_v(y)$. Let $init(s) = \iota$ for $s \in S$ and $init(s) = \top$ otherwise. An *assignment* $X$ gives each node a value, and $X \sqsubseteq Y$ means $X[v] \sqsubseteq Y[v]$ for all $v$. Define

$$F(X)[s] = init(s) \sqcap \bigsqcap_{(v, s) \in E} f_v(X[v]),$$

where the empty meet is $\top$. The maximal fixed-point solution (MFP) is the greatest $X$ with $X = F(X)$. $F$ is monotone, because each $f_v$ and the meet are.

We use the lines L1 to L11 of the pseudocode. An *iteration* is one pass through lines L5 to L11. Line L3 puts every node into $W$ exactly once. We write $c(s)$ for the number of times line L10 changes $IN[s]$, and $C = \sum_s c(s)$.

**Lemma 1 (values go down).** After line L2, $IN[s] = init(s)$ for every $s$. Every execution of lines L8 to L10 for an edge $(v, s)$ leaves $IN[s]$ equal to its old value met with $out$, and if line L10 runs, the new value is strictly below the old one.

*Proof.* Line L1 sets every value to $\top$ and line L2 sets the start nodes to $\iota$, which is $init$. Line L8 computes $new = IN[s] \sqcap out$. If $new = IN[s]$, nothing changes and $IN[s] = IN[s] \sqcap out$ already. Otherwise line L10 stores $new$, and $new = IN[s] \sqcap out \sqsubseteq IN[s]$ with $new \ne IN[s]$. $\square$

**Lemma 2 (the queue).** $W$ never holds a node twice. A node is added to $W$ only at line L3 or at line L11, and line L11 adds $s$ only right after line L10 has changed $IN[s]$.

*Proof.* Line L3 adds each node once, and line L11 adds $s$ only if it is not in $W$. The rest is read off the code. $\square$

**Theorem 1 (termination and counts).** Each $IN[s]$ changes at most $h$ times. The loop of line L4 runs at most $n + C \le n(h + 1)$ times, so line L6 applies at most $n(h + 1)$ transfer functions, and line L8 computes at most $m(h + 1)$ meets. In particular the algorithm terminates.

*Proof.* By Lemma 1 the values taken by $IN[s]$ form a strictly descending chain $init(s) \sqsupset \cdots$ with $c(s)$ steps, so $c(s) \le h$. By Lemma 2, $s$ is added to $W$ at most $1 + c(s)$ times, and each iteration removes one node at line L5, so $s$ is removed at most $1 + c(s) \le h + 1$ times. Summing over the nodes, there are at most $n + C \le n + n h$ iterations, each with one transfer function at line L6. An iteration that removes $v$ runs line L8 once per outgoing edge of $v$, so the number of meets is at most $\sum_v (1 + c(v))\, outdeg(v) \le (h + 1) \sum_v outdeg(v) = (h + 1) m$. Each iteration is finite, and there are finitely many, so the run ends. $\square$

**Lemma 3 (no safe value is lost).** Let $X$ be any assignment with $X \sqsubseteq F(X)$. Then $X \sqsubseteq IN$ holds after line L2 and after every later step.

*Proof.* After line L2, $X[s] \sqsubseteq F(X)[s] \sqsubseteq init(s) = IN[s]$, because a meet is below each of its terms. Values change only at line L10, for an edge $(v, s)$, with $new = IN[s] \sqcap out$ and $out = f_v(IN_0[v])$, where $IN_0[v]$ is the value of $IN[v]$ when line L6 ran in this iteration. By the claim at that time, $X[v] \sqsubseteq IN_0[v]$, so by monotonicity

$$X[s] \sqsubseteq F(X)[s] \sqsubseteq f_v(X[v]) \sqsubseteq f_v(IN_0[v]) = out.$$

By the claim before the change, $X[s] \sqsubseteq IN[s]$. So $X[s]$ is a lower bound of $IN[s]$ and $out$, hence $X[s] \sqsubseteq new$. $\square$

**Lemma 4 (the end is below $F$).** Let $R$ be the value of $IN$ when the algorithm stops. Then $R \sqsubseteq F(R)$.

*Proof.* We show that the following claim P holds before every iteration and after the last one: for every node $u \notin W$ and every edge $(u, s)$, $IN[s] \sqsubseteq f_u(IN[u])$.

Before the first iteration $W = V$, so P holds trivially. Assume P before an iteration that removes $v$, and look at the state after it.

- *The node $v$.* For each successor $s$, after line L8 and line L10, $IN[s] = IN[s] \sqcap out \sqsubseteq out$ by Lemma 1, and later steps of this iteration only lower $IN[s]$. If $IN[v]$ did not change in this iteration, then $out = f_v(IN[v])$, and P holds for $v$. If $IN[v]$ changed, which happens only through a self-loop $(v, v)$, then line L11 added $v$ back, since line L5 had removed it, so $v \in W$ and P says nothing about $v$.
- *Another node $u \notin W$.* Nodes leave $W$ only at line L5, so $u$ was not in $W$ before the iteration either, and P held for $u$. If $IN[u]$ had changed in this iteration, line L11 would have put $u$ into $W$, or $u$ would have been there already, so $IN[u]$ did not change. The values $IN[s]$ of the successors of $u$ can only have gone down by Lemma 1, so $IN[s] \sqsubseteq f_u(IN[u])$ still holds.

When the algorithm stops, $W$ is empty, so P gives $R[s] \sqsubseteq f_u(R[u])$ for every edge $(u, s)$. By Lemma 1, $R[s] \sqsubseteq init(s)$. So $R[s]$ is a lower bound of all terms of $F(R)[s]$, and $R[s] \sqsubseteq F(R)[s]$. $\square$

**Lemma 5 (the end is above $F$).** $F(R) \sqsubseteq R$.

*Proof.* By Lemma 1 and induction over the run, $R[s] = init(s) \sqcap o_1 \sqcap \cdots \sqcap o_k$, where $o_1, \ldots, o_k$ are all the values $out$ used at line L8 for edges into $s$. Each $o_j$ belongs to an edge $(v_j, s)$ and equals $f_{v_j}(IN_0[v_j])$ for a value $IN_0[v_j]$ that $IN[v_j]$ had during the run. By Lemma 1, $IN_0[v_j] \sqsupseteq R[v_j]$, so $o_j \sqsupseteq f_{v_j}(R[v_j])$ by monotonicity. Every node is removed from $W$ at least once, because it is in $W$ after line L3 and the run stops only when $W$ is empty, so every edge $(v, s)$ is among the $(v_j, s)$. Since the meet is monotone in each argument and idempotent,

$$R[s] \sqsupseteq init(s) \sqcap \bigsqcap_j f_{v_j}(R[v_j]) = init(s) \sqcap \bigsqcap_{(v, s) \in E} f_v(R[v]) = F(R)[s]. \qquad \square$$

**Theorem 2 (correctness).** $R$ is the maximal fixed-point solution. It is also the greatest assignment $X$ with $X \sqsubseteq F(X)$. In particular the MFP exists, and the result does not depend on the order of the queue in line L3.

*Proof.* By Lemmas 4 and 5 and antisymmetry, $R = F(R)$, so $R$ is a fixed point. If $X$ is any fixed point, or any assignment with $X \sqsubseteq F(X)$, then Lemma 3 at the end of the run gives $X \sqsubseteq R$. So $R$ is the greatest fixed point, and also the greatest such $X$. Greatest elements are unique, so every order of the queue gives the same $R$. $\square$

**Meet over all paths.** A path $\pi = v_0, v_1, \ldots, v_k$ in $G$ with $v_0 \in S$ is a path *to* $v_k$; its function is $f_\pi = f_{v_{k-1}} \circ \cdots \circ f_{v_0}$, the functions of the nodes before $v_k$, and the identity if $k = 0$. Let $P_s$ be the set of paths to $s$. The meet-over-all-paths solution is $\mathrm{MOP}[s] = \bigsqcap_{\pi \in P_s} f_\pi(\iota)$, which is $\top$ if $P_s$ is empty. $P_s$ can be infinite, so we first show that this meet exists.

**Lemma 6 (meets of arbitrary sets).** Every nonempty set $A \subseteq L$ has a greatest lower bound $\bigsqcap A$, and it is the meet of at most $h + 1$ members of $A$.

*Proof.* Pick $a_0 \in A$ and set $g_0 = a_0$. While some $a \in A$ has $g_i \sqcap a \ne g_i$, pick such an $a_{i+1}$ and set $g_{i+1} = g_i \sqcap a_{i+1}$, which is strictly below $g_i$. The chain $g_0 \sqsupset g_1 \sqsupset \cdots$ has at most $h$ steps, so it stops at some $g_k$, $k \le h$, with $g_k \sqsubseteq a$ for all $a \in A$. Any lower bound $b$ of $A$ is below $a_0, \ldots, a_k$, hence below their meet $g_k$. So $g_k$ is the greatest lower bound. $\square$

**Theorem 3 (MFP is below MOP).** For every monotone framework and every node $s$, $R[s] \sqsubseteq \mathrm{MOP}[s]$. So every fact of the result holds along every path, and the result is safe whenever each $f_v$ safely describes its node.

*Proof.* We show $R[v_k] \sqsubseteq f_\pi(\iota)$ for every path $\pi = v_0, \ldots, v_k$ with $v_0 \in S$, by induction on $k$. If $k = 0$, $v_0 \in S$ and $R[v_0] = F(R)[v_0] \sqsubseteq init(v_0) = \iota = f_\pi(\iota)$. If $k > 0$, let $\pi'$ be $\pi$ without its last node, a path to $v_{k-1}$, so $f_\pi = f_{v_{k-1}} \circ f_{\pi'}$. By Theorem 2, the induction hypothesis and monotonicity,

$$R[v_k] = F(R)[v_k] \sqsubseteq f_{v_{k-1}}(R[v_{k-1}]) \sqsubseteq f_{v_{k-1}}(f_{\pi'}(\iota)) = f_\pi(\iota).$$

So $R[s]$ is a lower bound of all $f_\pi(\iota)$ with $\pi \in P_s$, and $R[s] \sqsubseteq \mathrm{MOP}[s]$; if $P_s$ is empty this holds because $\mathrm{MOP}[s] = \top$. $\square$

**Theorem 4 (MFP equals MOP for distributive frameworks).** Suppose every $f_v$ is distributive, $f_v(x \sqcap y) = f_v(x) \sqcap f_v(y)$ for all $x, y$, and every node is reachable from $S$. Then $R = \mathrm{MOP}$.

*Proof.* A distributive $f$ is monotone: if $x \sqsubseteq y$, then $x = x \sqcap y$, so $f(x) = f(x) \sqcap f(y) \sqsubseteq f(y)$. It also distributes over every nonempty set $A$: by Lemma 6, $\bigsqcap A = a_0 \sqcap \cdots \sqcap a_k$ for some members, so $f(\bigsqcap A) = f(a_0) \sqcap \cdots \sqcap f(a_k) \sqsupseteq \bigsqcap f(A)$, and $f(\bigsqcap A) \sqsubseteq f(a)$ for every $a \in A$ by monotonicity, so $f(\bigsqcap A) = \bigsqcap f(A)$.

Let $M = \mathrm{MOP}$. We show $M \sqsubseteq F(M)$. Fix a node $s$. If $s \in S$, the path of length zero gives the term $\iota$, so $M[s] \sqsubseteq \iota = init(s)$; otherwise $init(s) = \top$. For an edge $(v, s)$, the set $P_v$ is nonempty because $v$ is reachable, so

$$f_v(M[v]) = f_v\Big(\bigsqcap_{\pi \in P_v} f_\pi(\iota)\Big) = \bigsqcap_{\pi \in P_v} f_v(f_\pi(\iota)).$$

Each $f_v(f_\pi(\iota))$ is $f_{\pi s}(\iota)$ for the path $\pi$ followed by $s$, which is in $P_s$, so it is above $M[s]$. Hence $M[s] \sqsubseteq f_v(M[v])$. So $M[s]$ is below every term of $F(M)[s]$, and $M \sqsubseteq F(M)$. Lemma 3, applied at the end of the run, gives $M \sqsubseteq R$, and Theorem 3 gives $R \sqsubseteq M$. $\square$

Reachability is needed. If $v$ is not reachable, $M[v] = \top$, and $f_v(\top)$ can be below $\top$. In reaching definitions, an unreachable block with a self-loop and a definition $d$ has $\mathrm{MOP} = \emptyset$, but $\{d\}$ is in its MFP.

**Lemma 7 (gen-kill functions are distributive).** On the subsets of a finite set $U$, let $f(x) = g \cup (x - k)$. Then $f(x \cup y) = f(x) \cup f(y)$ and $f(x \cap y) = f(x) \cap f(y)$. The composition of two such functions is again of this form.

*Proof.* Set difference distributes over union and intersection: $(x \cup y) - k = (x - k) \cup (y - k)$ and $(x \cap y) - k = (x - k) \cap (y - k)$. So $f(x \cup y) = g \cup (x - k) \cup (y - k) = f(x) \cup f(y)$, and $f(x \cap y) = g \cup ((x - k) \cap (y - k)) = (g \cup (x - k)) \cap (g \cup (y - k)) = f(x) \cap f(y)$, because union distributes over intersection. For the composition, with $f_1 = (g_1, k_1)$ applied first,

$$f_2(f_1(x)) = g_2 \cup ((g_1 \cup (x - k_1)) - k_2) = (g_2 \cup (g_1 - k_2)) \cup (x - (k_1 \cup k_2)),$$

which has gen set $g_2 \cup (g_1 - k_2)$ and kill set $k_1 \cup k_2$. $\square$

So the block functions of reaching definitions, live variables, available expressions and very busy expressions, which are compositions of the gen-kill functions of their instructions, are distributive for both meets. In the lattice of subsets of $U$ under $\cup$ or $\cap$, the height is $|U|$. By Theorems 2 and 4, the algorithm computes the MOP solution of these four problems on every CFG where every block is reachable from the entry (forward problems) or reaches a `ret` block (backward problems, on the reverse CFG).

**Theorem 5 (best case).** If $G$ is acyclic and line L3 orders the nodes so that every edge goes from an earlier node to a later one, then line L11 never adds a node, and the run applies exactly $n$ transfer functions and $m$ meets.

*Proof.* Suppose line L11 adds a node, and look at the first time it does, while $v$ is processed, for an edge $(v, s)$. Up to then no node was added, so $W$ holds exactly the nodes after $v$ in the initial order. The edge $(v, s)$ puts $s$ after $v$, so $s \in W$, and line L11 does not add it, a contradiction. So each node is removed exactly once, line L6 runs $n$ times, and line L8 runs once per edge. $\square$
