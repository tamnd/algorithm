---
title: Pettis-Hansen block positioning returns a legal layout, and optimal layout is NP-hard
proves: [correctness]
status: full
---

**Setting.** A procedure has blocks $b_1, \ldots, b_V$ with entry $b_1$, and a weight $w(a, b) \ge 0$ on each CFG edge. A *layout* is a sequence that holds every block exactly once and starts with $b_1$. The fall-through weight of a layout $\ell_1, \ldots, \ell_V$ is $F(\ell) = \sum_{j < V} w(\ell_j, \ell_{j+1})$, with $w = 0$ for pairs that are not edges. PETTIS-HANSEN-BLOCKS is lines L1 to L10 of the page.

**Theorem 1.** PETTIS-HANSEN-BLOCKS returns a layout. Each pair of consecutive blocks inside a chain is an edge of positive weight. In the toy IR, the program with its blocks in this order has the same outcome as the original on every input.

*Proof.* Invariant of lines L1 to L5: the chains are nonempty lists that partition the set of blocks, the entry is the head of its chain, and every two consecutive blocks in a chain form an edge $a \to b$ with $w(a, b) > 0$.

L1 makes it true: each block forms its own chain. Assume it before a step of L2 with edge $a \to b$. If L3 or L4 skips the edge, nothing changes. Otherwise $a$ and $b$ are in different chains $c_a$ and $c_b$, $a$ is the tail of $c_a$, $b$ is the head of $c_b$, and $b$ is not the entry. L5 replaces the two chains by $c_a$ followed by $c_b$. The partition is kept, since the two chains were disjoint and both are replaced by their concatenation. The new consecutive pairs are the old ones plus $(a, b)$, which is an edge with $w(a, b) > 0$ by L2. The entry was the head of its chain. That chain is not $c_b$, because the head of $c_b$ is $b \ne b_1$. If it is $c_a$, the entry is still the head of the joined chain, and otherwise its chain did not change.

So after L5 there is exactly one chain whose head is the entry. L6 places it first, and L7 to L9 place each other chain exactly once, since each round removes one unplaced chain. The concatenation in L10 holds every block exactly once and starts with $b_1$: it is a layout.

For the toy IR: a run starts at the first block of the dict, which is $b_1$ in both programs. After that, every transfer of control is named by a terminator, by label, and the blocks are unchanged. So by induction on the steps of a run, both programs execute the same block with the same environment and memory at every step, and they have the same outcome. $\square$

**Theorem 2.** The problem "given a CFG with edge weights and a number $k$, is there a layout $\ell$ with $F(\ell) \ge k$?" is NP-complete, even when every block has at most two successors, every weight is 1, and every block is reachable from the entry.

*Proof.* It is in NP: a layout is a certificate of linear size, and $F(\ell)$ is computed in linear time.

For hardness, reduce from the Hamiltonian cycle problem on digraphs in which every node has in-degree at most 2 and out-degree at most 2, which is NP-complete (Plesník 1979). Let $G$ be such a digraph with $n \ge 2$ nodes, and pick any node $v$. If some node of $G$ cannot be reached from $v$, then $G$ has no Hamiltonian cycle; map the instance to a fixed "no" instance (for example two blocks with no edge between them and $k = 1$). Otherwise build $G'$:

- the blocks are the nodes of $G$ other than $v$, plus two new blocks $v_{\mathrm{out}}$ and $v_{\mathrm{in}}$;
- each arc $x \to y$ of $G$ with $x, y \ne v$ stays;
- each arc $v \to y$ becomes $v_{\mathrm{out}} \to y$, each arc $x \to v$ becomes $x \to v_{\mathrm{in}}$, and a loop $v \to v$ is dropped;
- the entry is $v_{\mathrm{out}}$, every arc has weight 1, and $k = n$.

Every block has at most two successors, $v_{\mathrm{in}}$ has none, and $v_{\mathrm{out}}$ has no predecessor. Every block is reachable from $v_{\mathrm{out}}$, because every node of $G$ is reachable from $v$. $G'$ has $n + 1$ blocks, and the construction takes linear time.

A layout of $G'$ has $n$ consecutive pairs, each contributing 1 if it is an arc and 0 otherwise. So $F(\ell) \ge n$ if and only if every consecutive pair is an arc, that is, the layout is a Hamiltonian path of $G'$ starting at $v_{\mathrm{out}}$.

If $G$ has a Hamiltonian cycle, write it as $v, u_1, \ldots, u_{n-1}, v$. Then $v_{\mathrm{out}}, u_1, \ldots, u_{n-1}, v_{\mathrm{in}}$ is a Hamiltonian path of $G'$: the first arc comes from $v \to u_1$, the last from $u_{n-1} \to v$, and the others are arcs of $G$ between nodes other than $v$.

Conversely, let $v_{\mathrm{out}}, u_1, \ldots, u_n$ be a Hamiltonian path of $G'$. The block $v_{\mathrm{in}}$ has no successor, so it can only be last: $u_n = v_{\mathrm{in}}$. Then $u_1, \ldots, u_{n-1}$ are the $n - 1$ nodes of $G$ other than $v$, and $v, u_1, \ldots, u_{n-1}, v$ is a Hamiltonian cycle of $G$, by reading the arcs back.

So $G$ has a Hamiltonian cycle if and only if $G'$ has a layout with $F \ge n$. $\square$

**Corollary.** Unless P = NP, no polynomial-time algorithm returns a layout of maximum fall-through weight on every input. In particular PETTIS-HANSEN-BLOCKS, which runs in polynomial time, is not optimal on every input. The page gives an input where it returns weight 57 and the optimum is 65.
