---
title: Carry-save addition preserves the sum
proves: [correctness, termination]
status: full
---

Fix a base $\beta \ge 2$ and $n \ge 1$. A digit vector $d = (d_0, \ldots, d_{n-1})$ stands for $\langle d \rangle = \sum_{i=0}^{n-1} d_i \beta^i$; the digits of $c$ below are allowed to be any nonnegative integers in this formula.

**Termination.** CSA runs one pass over $n$ positions. CARRY-SAVE-SUM runs $m - 2$ calls of CSA and one addition. The tree form strictly decreases the number of operands at each level while there are more than 2, since a group of three becomes two.

**Lemma 1 (one step).** Let $x, y, z$ have digits in $[0, \beta)$ and $\langle x \rangle + \langle y \rangle + \langle z \rangle < \beta^n$. Then CSA returns $s$ and $c$ with $\langle s \rangle + \langle c \rangle = \langle x \rangle + \langle y \rangle + \langle z \rangle$, all $s_i \in [0, \beta)$, $c_0 = 0$, and $c_i \le 2$, with $c_i \le 1$ when $\beta = 2$.

*Proof.* At position $i$, line L1 forms $t_i = x_i + y_i + z_i$ with $0 \le t_i \le 3(\beta - 1)$, and line L2 writes $t_i = s_i + \beta q_i$ with $s_i = t_i \bmod \beta \in [0, \beta)$ and $q_i = \lfloor t_i / \beta \rfloor$. Since $3(\beta - 1) < 3\beta$, $q_i \le 2$; for $\beta = 2$, $t_i \le 3$ gives $q_i \le 1$. Line L2 stores $c_{i+1} = q_i$ for $i < n - 1$ and line L3 sets $c_0 = 0$. Then

$$\sum_{i=0}^{n-1} t_i \beta^i = \sum_{i=0}^{n-1} s_i \beta^i + \sum_{i=0}^{n-2} q_i \beta^{i+1} + q_{n-1} \beta^n = \langle s \rangle + \langle c \rangle + q_{n-1}\beta^n .$$

The left side is $\langle x \rangle + \langle y \rangle + \langle z \rangle < \beta^n$, and the right side is at least $q_{n-1} \beta^n$, so $q_{n-1} = 0$, and the identity is the claim. $\square$

**Lemma 2 (the outputs are valid inputs).** The digits of $c$ lie in $[0, \beta)$.

*Proof.* For $\beta = 2$, $c_i \le 1 < 2$. For $\beta \ge 3$, $c_i \le 2 < \beta$. $\square$

**Theorem (many operands).** Let $x_1, \ldots, x_m$, $m \ge 2$, have digits in $[0, \beta)$ and $\sum_j \langle x_j \rangle < \beta^n$. Then CARRY-SAVE-SUM returns $\sum_j \langle x_j \rangle$.

*Proof.* We show by induction on $j \ge 2$ that after the step for $j$ (line L5 for $j = 2$, line L6 for $j \ge 3$), the vectors $S$ and $C$ have digits in $[0, \beta)$ and $\langle S \rangle + \langle C \rangle = \sum_{k=1}^{j} \langle x_k \rangle$. For $j = 2$ this is the input. For the step to $j$, the three inputs $S$, $C$ and $x_j$ have digits in $[0, \beta)$ by the induction hypothesis, and their values add up to $\sum_{k \le j} \langle x_k \rangle \le \sum_{k \le m} \langle x_k \rangle < \beta^n$. Lemma 1 gives the sum identity and Lemma 2 the digit bounds. After $j = m$, line L7 adds $S$ and $C$ by an ordinary addition, which returns $\langle S \rangle + \langle C \rangle = \sum_{k=1}^{m} \langle x_k \rangle$; it fits in $n$ digits since this is less than $\beta^n$. $\blacksquare$

**The tree form.** Each level applies Lemma 1 to disjoint groups of three operands and keeps the others. By Lemmas 1 and 2, the multiset of operands after the level has digits in $[0, \beta)$ and the same total, which is below $\beta^n$, so the hypothesis of Lemma 1 holds for every group of the next level. When at most two operands remain, the final addition returns the total. $\blacksquare$
