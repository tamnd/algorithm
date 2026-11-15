---
title: The Aho-Johnson cost vectors are the costs of the best normal-form programs
proves: [correctness]
status: full
---

We use the machine and the pseudocode of the page. The machine has $r \ge 2$ registers. Each instruction is a pattern $p$ with a cost $c(p) > 0$. A leaf of a pattern is a register operand, an immediate constant or a memory operand. A store costs $s > 0$ and a load of a memory operand into a register costs $c_{\mathrm{ld}} > 0$. For a node $v$ we write $T_v$ for its subtree. When $p$ matches at $v$, the register leaves of $p$ sit on nodes $h_1, \ldots, h_q$ and the memory leaves on nodes $m_1, \ldots, m_e$. These nodes are the *operand nodes* of $p$ at $v$, and their subtrees are disjoint.

## Part 1: enough registers

A *tiling* of $T_v$ is a pattern $p$ that matches at $v$, a tiling of $T_h$ for each register operand node $h$ of $p$, and nothing for a constant or a variable. Its cost is the sum of the costs of its patterns. Let $\tau(v)$ be the least cost of a tiling of $T_v$ in which every memory operand is a variable.

**Lemma 1.** $\tau(v) = \min_p \big( c(p) + \sum_{t=1}^{q} \tau(h_t) \big)$, where $p$ ranges over the patterns that match at $v$ and whose memory operands are variables.

*Proof.* A tiling of $T_v$ is a choice of $p$ and independent tilings of the disjoint subtrees $T_{h_t}$, and its cost is $c(p)$ plus their costs. For a fixed $p$ the sum is least when each part is least. Take the minimum over $p$. $\square$

This is the case of Part 2 with $r \ge n$, on the machine of the page. With $j \ge |T_v|$ free registers, the operand $h_t$ gets $j - t + 1 \ge |T_{h_t}|$ registers, so no register limit binds. A plan that stores a subtree $m$ pays $\tau(m) + s$ for it, and then either a load of cost 3 or the memory form ADDM of cost 3. The plan that keeps $m$ in a register pays $\tau(m)$ and the register form ADD of cost 1, or nothing for the load. So a store never helps there, and $C[\mathrm{root}][r] = \tau(\mathrm{root})$.

## Part 2: a limited number of registers

A program for $T$ computes nodes into registers by instructions, writes registers to temporaries by stores, and leaves the root in $R_0$. An instruction for $v$ reads the value of each register operand node from a register and the value of each memory operand node from a variable or a temporary. At each moment at most $r$ registers hold values that the program still needs.

**Normal-form plans.** For $0 \le j \le r$ define the set $\mathcal{P}(v, j)$ of plans, by induction on $T_v$:

- $j = 0$ (the value of $v$ ends in memory). If $v$ is a variable, the empty plan, of cost 0. Else a plan of $\mathcal{P}(v, r)$ followed by a store, of cost $\mathrm{cost} + s$.
- $j \ge 1$ (the value of $v$ ends in a register, and only $j$ registers are free). Either a reload: a plan of $\mathcal{P}(v, 0)$ when $v$ is not a variable, followed by a load. Or a pattern $p$ that matches at $v$ with $q \le j$ register operand nodes, an order $h_1, \ldots, h_q$ of them, a plan of $\mathcal{P}(m_i, 0)$ for each memory operand node, and a plan of $\mathcal{P}(h_t, j - t + 1)$ for each $t$. A variable as a memory operand needs the empty plan. The cost is $c(p)$ plus the costs of the parts.

**Lemma 2.** After LABEL$(v)$, $C[v][j]$ is the least cost of a plan in $\mathcal{P}(v, j)$, for each $0 \le j \le r$.

*Proof.* By induction on the height of $v$. Line L1 handles the children first, so the claim holds for each operand node. Lines L2 to L6 try each pattern that matches at $v$, each order of its register operand nodes, and each $j$ with $\max(1, q) \le j \le r$. For a fixed pattern and order, the cost of a plan is $c(p)$ plus a sum of independent parts. By the induction hypothesis the least part costs are $C[m_i][0]$ and $C[h_t][j - t + 1]$. Line L3 adds the first ones, and line L5 adds the second ones. A memory operand that is a variable adds 0. So after line L6, $C[v][j]$ is the least cost of a plan of the pattern kind, for $j \ge 1$.

Let $D[v][j]$ be this value. A reload plan for $j \ge 1$ costs at least $D[v][r] + s + c_{\mathrm{ld}} > D[v][r]$, because its inner plan of $\mathcal{P}(v, r)$ is a pattern plan or another reload, and a reload inside a reload only adds cost. So the least plan of $\mathcal{P}(v, r)$ is a pattern plan, of cost $D[v][r]$. Lines L7 and L8 then set $C[v][0]$ to the least cost in $\mathcal{P}(v, 0)$: 0 for a variable, and $D[v][r] + s$ else. Line L9 sets $C[v][j] = \min(D[v][j], C[v][0] + c_{\mathrm{ld}})$, which is the least cost over both kinds of plans of $\mathcal{P}(v, j)$. For $j = r$ this is still $D[v][r]$. $\square$

**Lemma 3.** GENERATE emits a program of cost $C[\mathrm{root}][r]$. It leaves the value of the tree in $R_0$, and at each moment at most $r$ registers hold needed values.

*Proof.* GENERATE follows the plan that LABEL remembered. Line L10 first runs each subtree that the plan puts in memory, with all registers free, and stores it. Such a subtree runs before the code that reads its temporary, and the subtrees that it puts in memory run before it. The temporaries are fresh, so later code does not overwrite them.

Then the code of a node $v$ with $j$ free registers $R_i, \ldots, R_{i+j-1}$ runs the operand $h_t$ with the $j - t + 1$ registers $R_{i+t-1}, \ldots, R_{i+j-1}$. By induction it leaves $h_t$ in $R_{i+t-1}$ and does not write $R_i, \ldots, R_{i+t-2}$, where the earlier operands wait. Then the instruction for $v$ reads its operands and writes $R_i$. So each part uses only its own registers, and the count of needed registers never exceeds $r$. A reload loads the temporary of $v$ into $R_i$. Each instruction and each store of the code belongs to exactly one part of the plan, so the cost of the code is the cost of the plan, which is $C[\mathrm{root}][r]$ by Lemma 2. $\square$

**Lemma 4.** $C[v][j] \ge C[v][j+1]$ for $1 \le j < r$.

*Proof.* By induction on the height of $v$. A pattern plan with $j$ registers is also allowed with $j + 1$ registers, and the induction hypothesis gives $C[h_t][j - t + 2] \le C[h_t][j - t + 1]$ for each operand. The reload term is the same for each $j$. $\square$

**Theorem.** For a tree $T$ and a machine of the class of Aho and Johnson, $C[\mathrm{root}][r]$ is the least cost of a program for $T$, and GENERATE emits a program with this cost.

*Proof.* Aho and Johnson prove that each tree has a cheapest program in *strong normal form*: the program first computes and stores some subtrees, each with all registers free, and then computes the root, where each instruction evaluates its register operands one after the other, each one in full before the next one starts. A program in strong normal form is exactly a plan of $\mathcal{P}(\mathrm{root}, r)$. So the least cost of a program is the least cost of a plan, which is $C[\mathrm{root}][r]$ by Lemma 2. Lemma 3 shows that GENERATE reaches it. $\blacksquare$

The normal form theorem is the deep step, and this file does not repeat its proof. It needs the assumptions of their class of machines, in particular that the registers are interchangeable and that a memory operand can be any variable or temporary. A machine with special registers, such as a multiply that writes a fixed register pair, is outside the class.

**Time.** For a fixed machine, the number of patterns, their size, the number $q$ of register operands of a pattern and $r$ are constants. LABEL does $O(\text{patterns} \cdot q! \cdot r \cdot q)$ work at each node, and GENERATE does constant work for each node and each emitted instruction. So both run in time linear in the number of nodes.
