---
title: The carry-skip adder computes the sum of its inputs
proves: [correctness, termination]
status: full
---

Let $n \ge 1$, $a_i, b_i, c_{\text{in}} \in \{0, 1\}$, and block sizes $k_0, \ldots, k_{t-1} \ge 1$ with sum $n$. Block $j$ covers positions $\ell_j .. u_j$, consecutive and in order. Write $g_i = a_i \wedge b_i$ and $p_i = a_i \oplus b_i$.

**Termination.** The loops of lines L4 and L6 run over finite lists of blocks and positions, and the AND trees of line L2 halve the number of signals at each level.

**The reference values.** Define the ripple carries $c^{\ast}_0 = c_{\text{in}}$ and $c^{\ast}_{i+1} = g_i \vee (p_i \wedge c^{\ast}_i)$. For each position, $a_i + b_i + c^{\ast}_i = (p_i \oplus c^{\ast}_i) + 2c^{\ast}_{i+1}$: if $p_i = 1$, then $g_i = 0$ and both sides are $1 + c^{\ast}_i$; if $p_i = 0$, then $a_i = b_i = g_i$ and both sides are $2g_i + c^{\ast}_i$. Multiplying by $2^i$ and summing over $i$, the carries telescope:

$$a + b + c_{\text{in}} = \sum_{i=0}^{n-1} (p_i \oplus c^{\ast}_i)\, 2^i + c^{\ast}_n\, 2^n .$$

So it suffices to show that the algorithm sets $s_i = p_i \oplus c^{\ast}_i$ and returns $c^{\ast}_n$.

**Lemma 1 (a propagating block).** If $p_i = 1$ for every $i$ in block $j$, then $c^{\ast}_{u_j + 1} = c^{\ast}_{\ell_j}$.

*Proof.* For each such $i$, $g_i = a_i \wedge b_i = 0$ because $a_i \ne b_i$, so $c^{\ast}_{i+1} = 0 \vee (1 \wedge c^{\ast}_i) = c^{\ast}_i$. Apply this $k_j$ times. $\square$

**Lemma 2 (the invariant).** At the start of iteration $j$ of the loop of line L4, $c = c^{\ast}_{\ell_j}$. During the iteration, line L6 sets $s_i = p_i \oplus c^{\ast}_i$ for each position $i$ of block $j$, and at its end $c = c^{\ast}_{u_j + 1}$.

*Proof.* By induction on $j$. For $j = 0$, line L3 sets $c = c_{\text{in}} = c^{\ast}_0$. Assume $c = c^{\ast}_{\ell_j}$ at the start of iteration $j$. Line L5 sets $x = c^{\ast}_{\ell_j}$. Line L6 processes positions $\ell_j, \ldots, u_j$ in order; by induction on the position, when it reaches $i$ the value $c$ is $c^{\ast}_i$, so it sets $s_i = p_i \oplus c^{\ast}_i$ and then $c = g_i \vee (p_i \wedge c^{\ast}_i) = c^{\ast}_{i+1}$. After the block, $c = c^{\ast}_{u_j + 1}$. If $j = 0$, line L7 does nothing. If $j \ge 1$, line L2 gives $P_j = \bigwedge_{i = \ell_j}^{u_j} p_i$, and line L7 sets $c \leftarrow (P_j \wedge x) \vee (\neg P_j \wedge c)$:

- if $P_j = 0$, the new value is $c = c^{\ast}_{u_j + 1}$;
- if $P_j = 1$, the new value is $x = c^{\ast}_{\ell_j}$, which equals $c^{\ast}_{u_j + 1}$ by Lemma 1.

So $c = c^{\ast}_{u_j + 1} = c^{\ast}_{\ell_{j+1}}$ at the end of the iteration. $\square$

**Theorem.** CARRY-SKIP-ADD returns the bits of $a + b + c_{\text{in}}$.

*Proof.* By Lemma 2, every $s_i = p_i \oplus c^{\ast}_i$, and after the last block $c = c^{\ast}_{u_{t-1} + 1} = c^{\ast}_n$. By the identity above, these $n + 1$ bits represent $a + b + c_{\text{in}}$. $\blacksquare$
