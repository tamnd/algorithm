---
title: Camellia decryption is encryption with the subkeys reversed
proves: [correctness]
status: full
---

Fix the subkeys $kw_1, \ldots, kw_4$, $k_1, \ldots, k_R$ and $ke_1, \ldots, ke_m$ with $m = R/3 - 2$. The proof holds for any values, so it does not depend on the key schedule. A state is a pair $(a, b)$ of 64-bit halves.

**The steps.** Define these maps on states:

- $W_{u,v}(a, b) = (a \oplus u, b \oplus v)$, the whitening.
- $H^{(2)}_k(a, b) = (a, b \oplus F(a, k))$ and $H^{(1)}_k(a, b) = (a \oplus F(b, k), b)$, the half-rounds of lines L6 and L7.
- $\Lambda_{u,v}(a, b) = (\mathrm{FL}(a, u), \mathrm{FL}^{-1}(b, v))$, the layer of line L5.
- $\sigma(a, b) = (b, a)$, the swap.

Lines L1 to L8 compute

$$E = W_{kw_3, kw_4} \circ \sigma \circ H^{(1)}_{k_R} \circ H^{(2)}_{k_{R-1}} \circ \cdots \circ \Lambda_{ke_1, ke_2} \circ \cdots \circ H^{(1)}_{k_2} \circ H^{(2)}_{k_1} \circ W_{kw_1, kw_2},$$

where the layer $\Lambda_{ke_{2i-1}, ke_{2i}}$ sits after the first $6i$ half-rounds, for $i = 1, \ldots, m/2$. Line L8 XORs $kw_3$ into $D_2$ and $kw_4$ into $D_1$ and then outputs $D_2$ first, which is $W_{kw_3, kw_4} \circ \sigma$.

**Each step is a bijection.**

1. $W_{u,v} \circ W_{u,v}$ is the identity, because $x \oplus u \oplus u = x$.
2. $H^{(2)}_k \circ H^{(2)}_k$ is the identity: the first map does not change $a$, so the second XORs the same value $F(a, k)$ into $b$ again. The same holds for $H^{(1)}_k$. No property of F is used.
3. $\mathrm{FL}^{-1}(\mathrm{FL}(x, k), k) = x$. FL is two steps: line L13 sets $x_2' = x_2 \oplus \mathrm{ROL}_1(x_1 \wedge k_1)$, and line L14 sets $x_1' = x_1 \oplus (x_2' \vee k_2)$. FL⁻¹ first computes $x_1' \oplus (x_2' \vee k_2) = x_1$, because $x_2'$ is unchanged, and then $x_2' \oplus \mathrm{ROL}_1(x_1 \wedge k_1) = x_2$. In the same way, $\mathrm{FL}(\mathrm{FL}^{-1}(y, k), k) = y$. So $\Lambda_{u,v}^{-1}(a, b) = (\mathrm{FL}^{-1}(a, u), \mathrm{FL}(b, v))$.
4. $\sigma \circ \sigma$ is the identity.

**Moving the swap.** Direct substitution gives these rules, for all $u, v, k$:

- $H^{(1)}_k \circ \sigma = \sigma \circ H^{(2)}_k$ and $H^{(2)}_k \circ \sigma = \sigma \circ H^{(1)}_k$. For example, $H^{(1)}_k(\sigma(a, b)) = (b \oplus F(a, k), a) = \sigma(a, b \oplus F(a, k))$.
- $\Lambda_{u,v}^{-1} \circ \sigma = \sigma \circ \Lambda_{v,u}$, because $\Lambda_{u,v}^{-1}(b, a) = (\mathrm{FL}^{-1}(b, u), \mathrm{FL}(a, v))$, which is $\sigma(\mathrm{FL}(a, v), \mathrm{FL}^{-1}(b, u))$.
- $W_{u,v} \circ \sigma = \sigma \circ W_{v,u}$.

**The inverse.** Invert the steps of $E$ in reverse order:

$$E^{-1} = W_{kw_1, kw_2} \circ H^{(2)}_{k_1} \circ H^{(1)}_{k_2} \circ \cdots \circ \Lambda^{-1}_{ke_1, ke_2} \circ \cdots \circ H^{(1)}_{k_R} \circ \sigma \circ W_{kw_3, kw_4}.$$

Move $\sigma$ to the left through each step with the rules above. Each $H^{(1)}$ becomes $H^{(2)}$ and each $H^{(2)}$ becomes $H^{(1)}$, each $\Lambda^{-1}_{u,v}$ becomes $\Lambda_{v,u}$, and $W_{kw_1, kw_2}$ becomes $W_{kw_2, kw_1}$ with the swap on its left. Then $\sigma \circ W_{kw_2, kw_1} = W_{kw_1, kw_2} \circ \sigma$, so

$$E^{-1} = W_{kw_1, kw_2} \circ \sigma \circ H^{(1)}_{k_1} \circ H^{(2)}_{k_2} \circ \cdots \circ \Lambda_{ke_2, ke_1} \circ \cdots \circ H^{(2)}_{k_R} \circ W_{kw_3, kw_4}.$$

This is the formula for $E$ with $(kw_1, kw_2, kw_3, kw_4)$ replaced by $(kw_3, kw_4, kw_1, kw_2)$, the round keys in the order $k_R, \ldots, k_1$, and the FL keys in the order $ke_m, \ldots, ke_1$. The layers stay in the right places: the layer that follows $6i$ half-rounds of $E$ follows $R - 6i$ half-rounds of $E^{-1}$, and the layer positions $6, 12$ (for $R = 18$) and $6, 12, 18$ (for $R = 24$) are symmetric under $6i \mapsto R - 6i$. The FL keys pair up correctly: the layer $\Lambda_{ke_{2i-1}, ke_{2i}}$ becomes $\Lambda_{ke_{2i}, ke_{2i-1}}$, which takes its keys in the reversed list in the same positions. So decryption, which runs lines L1 to L8 with the reversed subkeys, computes $E^{-1}$. $\square$

**Termination.** The loop of line L3 runs $R/2$ times and each call of F does a fixed amount of work, so encryption stops. The key schedule is a fixed sequence of 4 or 6 calls of F and a table of rotations.
