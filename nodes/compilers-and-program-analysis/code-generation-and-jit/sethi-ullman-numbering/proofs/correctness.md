---
title: Sethi-Ullman labels are the minimum register count, and GEN reaches it
proves: [correctness]
status: full
---

We use the machine and the pseudocode of the page. A tree $T$ has leaves and inner nodes, and each inner node $v$ has a left child $a(v)$ and a right child $b(v)$. The label $\ell(v)$ is the value that LABEL returns for $v$ (lines L1 to L5). We write $T_v$ for the subtree of $v$.

## The game of registers

A store-free program for $T$ is a sequence of instructions. Each instruction computes one node into a register $R_i$. A load computes a leaf. An operation computes an inner node $v$, and it reads the value of $a(v)$ from a register and the value of $b(v)$ from a register, or from memory when $b(v)$ is a leaf. The register keeps the value until another instruction writes to it. The program ends with the value of the root in a register.

Let $S_t$ be the set of nodes whose value is in some register after $t$ instructions. One register holds the value of one node, so $|S_t|$ is at most the number of registers that the program uses. A step can add one node $v$ to $S$ when the operands of $v$ are in $S$ (a memory leaf needs nothing), and it can remove any node, because a register can be overwritten. So it is enough to bound $\max_t |S_t|$ from below.

**Lemma 1 (lower bound).** Let $v$ be a node, and let $s \le t$ be times such that $S_s \cap T_v = \varnothing$ and $v \in S_t$. Then $|S_\tau \cap T_v| \ge \ell(v)$ for some $\tau$ with $s \le \tau \le t$.

*Proof.* By induction on the height of $v$. If $v$ is a leaf, then $|S_t \cap T_v| = 1 \ge \ell(v)$, since $\ell(v) \in \{0, 1\}$.

Let $v$ be an inner node, with $a = a(v)$, $b = b(v)$, $\ell_a = \ell(a)$ and $\ell_b = \ell(b)$. Let $t_1$ be the first time in $(s, t]$ with $v \in S_{t_1}$. The step $t_1$ computes $v$, so $a \in S_{t_1 - 1}$, and $b \in S_{t_1 - 1}$ unless $b$ is a leaf that is read from memory. The subtree $T_a$ is empty at time $s$, so the induction hypothesis on $[s, t_1 - 1]$ gives a time with at least $\ell_a$ nodes of $T_a \subseteq T_v$ in $S$. If $b \in S_{t_1-1}$, the same holds for $b$. If $b$ is read from memory, then $b$ is a right leaf and $\ell_b = 0$. So some time in $[s, t]$ has at least $\max(\ell_a, \ell_b)$ nodes of $T_v$ in $S$. This proves the lemma when $\ell_a \ne \ell_b$, by line L5.

Now let $\ell_a = \ell_b = L$. A left child has label at least 1 (line L1 and line L4 or L5), so $L \ge 1$. Then $b$ is not a right leaf of label 0, so $b \in S_{t_1 - 1}$. Let $s_a$ be the last time in $[s, t_1 - 1]$ with $T_a \cap S_{s_a} = \varnothing$, and define $s_b$ in the same way. Both exist, because $s$ is such a time. By the choice of $s_a$, the subtree $T_a$ is not empty at each time in $(s_a, t_1 - 1]$, and the same holds for $b$.

Assume $s_a \le s_b$. The induction hypothesis for $b$ on $[s_b, t_1 - 1]$ gives a time $\tau$ with $|S_\tau \cap T_b| \ge L \ge 1$. At time $s_b$ the subtree $T_b$ is empty, so $\tau > s_b \ge s_a$. So $T_a$ is not empty at time $\tau$, and $T_a$ and $T_b$ are disjoint. This gives $|S_\tau \cap T_v| \ge L + 1 = \ell(v)$, by line L4. If $s_b < s_a$, swap the roles of $a$ and $b$. $\square$

At time 0 no node is in a register, and at the end the root is in a register. So Lemma 1 with $s = 0$ gives:

**Theorem 1.** Each store-free program for $T$ uses at least $\ell(\mathrm{root})$ registers. This holds for every order of the instructions, including orders that interleave the two subtrees of a node, and for programs that compute a node more than once.

## GEN reaches the bound

**Lemma 2.** Let $k \ge 1$ and $0 \le i < k$, and let $v$ be a node that is the root or a left child, or an inner node. Then GEN$(v, i)$ emits code that leaves the value of $v$ in $R_i$, writes only $R_i, \ldots, R_{k-1}$ and fresh temporaries, and reads only registers that it wrote before. If $\ell(v) \le k - i$, the code has no store and writes only $R_i, \ldots, R_{i + \ell(v) - 1}$.

*Proof.* By induction on the height of $v$. Let $r = k - i \ge 1$. A leaf that reaches line L6 is the root or a left child, so $\ell(v) = 1 \le r$. The load writes only $R_i$.

Let $v$ be an inner node with children $a$ and $b$ and labels $\ell_a \ge 1$ and $\ell_b$.

*Line L7, $b$ is a leaf.* Then $\ell_b = 0$ and $\ell(v) = \ell_a$ by line L5. By induction, GEN$(a, i)$ leaves $a$ in $R_i$, and the operation reads $b$ from memory and writes $R_i$. The bounds of $a$ carry over to $v$.

*Lines L8 to L10, $\ell_a \ge r$ and $\ell_b \ge r$.* GEN$(b, i)$ leaves $b$ in $R_i$, and the store saves it in a fresh temporary $t$. GEN$(a, i)$ then leaves $a$ in $R_i$ and does not write $t$. The operation reads $a$ from $R_i$ and $b$ from $t$. In this case $\ell(v) > r$: if $\ell_a = \ell_b$ then $\ell(v) = \ell_a + 1 > r$, and else $\ell(v) = \max(\ell_a, \ell_b) > r$. So the claim about $\ell(v) \le r$ is empty here.

*Line L11, $\ell_a \ge \ell_b$, not both at least $r$.* Then $\ell_b < r$: either $\ell_b < r$ directly, or $\ell_a < r$ and $\ell_b \le \ell_a$. Since $b$ is an inner node, $\ell_b \ge 1$, so $r \ge 2$ and $i + 1 < k$. GEN$(a, i)$ leaves $a$ in $R_i$. GEN$(b, i + 1)$ leaves $b$ in $R_{i+1}$, and it does not write $R_i$. The operation reads both and writes $R_i$. If $\ell(v) \le r$: then $\ell_a \le \ell(v)$, so GEN$(a, i)$ has no store and stays in $R_i, \ldots, R_{i + \ell_a - 1}$. Also $\ell_b \le \ell(v) - 1$: if $\ell_a > \ell_b$ this follows from $\ell(v) = \ell_a$, and if $\ell_a = \ell_b$ from $\ell(v) = \ell_a + 1$. So GEN$(b, i + 1)$ has no store and stays in $R_{i+1}, \ldots, R_{i + \ell(v) - 1}$.

*Line L12, $\ell_a < \ell_b$.* The same argument with $a$ and $b$ swapped. Here $\ell_a < \ell_b$ and not both at least $r$ give $\ell_a < r$, and $\ell_a \ge 1$ gives $r \ge 2$. The operation writes $R_i \leftarrow R_{i+1} \mathbin{op} R_i$, so the left operand is still $a$. If $\ell(v) \le r$, then $\ell(v) = \ell_b$, GEN$(b, i)$ stays in $R_i, \ldots, R_{i+\ell_b-1}$, and GEN$(a, i+1)$ stays in $R_{i+1}, \ldots, R_{i + \ell_a}$ with $\ell_a \le \ell_b - 1$. $\square$

**Theorem 2.** For each $k \ge 1$, GEN$(\mathrm{root}, 0)$ leaves the value of the tree in $R_0$ and uses only $R_0, \ldots, R_{k-1}$. If $k \ge \ell(\mathrm{root})$, the code has no store and uses exactly the registers $R_0, \ldots, R_{\ell(\mathrm{root}) - 1}$. With Theorem 1, $\ell(\mathrm{root})$ is the minimum number of registers of a store-free program for $T$.

*Proof.* Lemma 2 with $v = \mathrm{root}$ and $i = 0$ gives all claims except "exactly". Theorem 1 shows that the store-free code cannot use fewer than $\ell(\mathrm{root})$ registers, and Lemma 2 shows that it uses no register outside the first $\ell(\mathrm{root})$. $\blacksquare$

**The order.** The proof of Lemma 2 shows why the child with the larger label goes first. While the second child runs, the first child holds one register. If the first child has the smaller label $\ell_1 < \ell_2$, the peak is at least $\ell_2 + 1$ when the order is not interleaved, which is more than $\ell(v) = \ell_2$.

**Length.** Each inner node gives one operation, each leaf that is the root or a left child gives one load, and each pass through line L8 gives one store. No instruction loads a temporary. Sethi and Ullman prove that their algorithm gives a program with the fewest instructions on their machine when no algebraic law is used. This file does not repeat that proof.
