---
title: IKNP gives the receiver the chosen message of every transfer
proves: [correctness]
status: full
---

We prove that when both parties follow lines L1 to L8, the receiver outputs $z_j = x_j^{r_j}$ for every $j = 1, \ldots, m$.

**Setting.** $s = (s_1, \ldots, s_\kappa) \in \{0,1\}^\kappa$ is the sender's secret and $r = (r_1, \ldots, r_m) \in \{0,1\}^m$ is the receiver's choice vector. For a bit $b$ and a bit string $v$, $b \cdot v$ is $v$ if $b = 1$ and the zero string if $b = 0$. $G$ is a fixed function from seeds to $\{0,1\}^m$ and $H$ is a fixed function; the proof uses no property of $G$ or $H$ other than that they are functions, so both parties get the same value from the same input.

**Step 1 (columns).** For every $i$, $q^i = t^i \oplus s_i \cdot r$.

By line L3, the sender gets $k_i^{s_i}$. By line L4, $t^i = G(k_i^0)$ and $u^i = t^i \oplus G(k_i^1) \oplus r$. By line L5, $q^i = G(k_i^{s_i}) \oplus s_i \cdot u^i$.

- If $s_i = 0$: $q^i = G(k_i^0) = t^i = t^i \oplus 0 \cdot r$.
- If $s_i = 1$: $q^i = G(k_i^1) \oplus t^i \oplus G(k_i^1) \oplus r = t^i \oplus r = t^i \oplus 1 \cdot r$.

**Step 2 (rows).** For every $j$, $q_j = t_j \oplus r_j \cdot s$.

By line L6, bit $i$ of the row $q_j$ is bit $j$ of the column $q^i$, and the same for $t$. By Step 1, bit $j$ of $q^i$ is $t^i_j \oplus s_i r_j$. So bit $i$ of $q_j$ is bit $i$ of $t_j$ XOR $r_j s_i$, for every $i$. That is $q_j = t_j \oplus r_j \cdot s$.

**Step 3 (outputs).** By line L7, $y_j^0 = x_j^0 \oplus H(j, q_j)$ and $y_j^1 = x_j^1 \oplus H(j, q_j \oplus s)$. By line L8, $z_j = y_j^{r_j} \oplus H(j, t_j)$.

- If $r_j = 0$: by Step 2, $q_j = t_j$, so $z_j = x_j^0 \oplus H(j, t_j) \oplus H(j, t_j) = x_j^0$.
- If $r_j = 1$: by Step 2, $q_j \oplus s = t_j \oplus s \oplus s = t_j$, so $z_j = x_j^1 \oplus H(j, t_j) \oplus H(j, t_j) = x_j^1$.

So $z_j = x_j^{r_j}$ for every $j$. $\blacksquare$

**Remark.** Step 1 used that the receiver puts the same $r$ into every column. If it puts $r^{(i)}$ into column $i$, the same computation gives $q_j = t_j \oplus (s \wedge c_j)$, where $c_j = (r^{(1)}_j, \ldots, r^{(\kappa)}_j)$ and $\wedge$ is bitwise. For $c_j = 0$ or $c_j = 1^\kappa$ this is Step 2; for other $c_j$ the pad $H(j, q_j)$ depends on only some bits of $s$, which is the attack on the page.
