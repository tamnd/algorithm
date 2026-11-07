---
title: The carry-select adder computes the sum of its inputs
proves: [correctness, termination]
status: full
---

Let $n \ge 1$, $a_i, b_i, c_{\text{in}} \in \{0, 1\}$, and block sizes $k_0, \ldots, k_{t-1} \ge 1$ with $\sum_j k_j = n$. Block $j$ covers the positions $\ell_j .. u_j$ with $\ell_0 = 0$, $u_j = \ell_j + k_j - 1$ and $\ell_{j+1} = u_j + 1$. Write $A_j = \sum_{i=\ell_j}^{u_j} a_i 2^{i - \ell_j}$ and $B_j$ likewise.

**Termination.** Every loop runs over a finite list of blocks or positions, once.

**Ripple steps.** For a block and a carry-in $c \in \{0, 1\}$, the ripple of lines L2 and L4 sets $c_{\ell} = c$, $s_i = p_i \oplus c_i$ and $c_{i+1} = g_i \vee (p_i \wedge c_i)$ for $i = \ell..u$, with $g_i = a_i \wedge b_i$ and $p_i = a_i \oplus b_i$. The simplified first steps with a constant carry compute the same values: with $c = 0$, $s = p$ and $c_{\ell+1} = g$; with $c = 1$, $s = p \oplus 1$ and $c_{\ell+1} = g \vee p$.

**Lemma 1.** The ripple through block $j$ with carry-in $c$ returns bits $s_{\ell_j}, \ldots, s_{u_j}$ and a carry out $C$ with $\sum_i s_i 2^{i - \ell_j} + C\, 2^{k_j} = A_j + B_j + c$.

*Proof.* For each position, $a_i + b_i + c_i = s_i + 2c_{i+1}$: if $p_i = 1$ then $a_i + b_i = 1$ and $g_i = 0$, so both sides are $1 + c_i$; if $p_i = 0$ then $a_i = b_i = g_i$, $s_i = c_i$ and $c_{i+1} = g_i$, so both sides are $2g_i + c_i$. Multiply by $2^{i - \ell_j}$ and sum over the block; the terms $c_i$ for $\ell_j < i \le u_j$ cancel, which leaves the claim with $C = c_{u_j + 1}$. $\square$

**Lemma 2 (monotone carries).** In line L4, $C^0[j] \le C^1[j]$.

*Proof.* By Lemma 1, $C^c[j] = \lfloor (A_j + B_j + c) / 2^{k_j} \rfloor$, which does not decrease when $c$ goes from 0 to 1. $\square$

**Lemma 3 (selection).** If $x \in \{0, 1\}$, then $s^0_i \oplus (x \wedge (s^0_i \oplus s^1_i)) = s^x_i$ and $C^0[j] \vee (C^1[j] \wedge x) = C^x[j]$.

*Proof.* For $x = 0$, the first expression is $s^0_i$ and the second is $C^0[j]$. For $x = 1$, the first is $s^0_i \oplus s^0_i \oplus s^1_i = s^1_i$, and the second is $C^0[j] \vee C^1[j] = C^1[j]$ by Lemma 2. $\square$

**Lemma 4.** Let $c^{\ast}_j$ be the true carry into block $j$, that is, $c^{\ast}_0 = c_{\text{in}}$ and $c^{\ast}_{j+1} = \lfloor (A_j + B_j + c^{\ast}_j) / 2^{k_j} \rfloor$. Then the value $x$ of line L6 at step $j$ is $c^{\ast}_j$, and the value $C$ after line L8 at step $j$ is $c^{\ast}_{j+1}$.

*Proof.* By induction on $j$. Before the loop, $C$ is the carry out of block 0 with carry-in $c_{\text{in}}$, which is $c^{\ast}_1$ by Lemma 1. At step $j$, line L6 sets $x = C = c^{\ast}_j$ by the induction hypothesis, and line L8 sets $C = C^x[j]$ by Lemma 3, which is $\lfloor (A_j + B_j + c^{\ast}_j) / 2^{k_j} \rfloor = c^{\ast}_{j+1}$ by Lemma 1. $\square$

**Theorem.** CARRY-SELECT-ADD returns the $n + 1$ bits of $a + b + c_{\text{in}}$.

*Proof.* By Lemmas 1, 3 and 4, the bits that the algorithm writes for block $j$ are the low $k_j$ bits of $A_j + B_j + c^{\ast}_j$, so with $S_j$ their value, $S_j + c^{\ast}_{j+1} 2^{k_j} = A_j + B_j + c^{\ast}_j$. Multiply by $2^{\ell_j}$ and sum over $j$. Since $\ell_j + k_j = \ell_{j+1}$, the carry terms telescope, and

$$\sum_j S_j 2^{\ell_j} + c^{\ast}_t 2^n = \sum_j (A_j + B_j) 2^{\ell_j} + c^{\ast}_0 = a + b + c_{\text{in}} .$$

The returned carry is $C = c^{\ast}_t$ by Lemma 4 (or by Lemma 1 when $t = 1$), so the output represents $a + b + c_{\text{in}}$. $\blacksquare$
