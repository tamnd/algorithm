---
title: Garbled evaluation with free XOR and half gates outputs C(x, y)
proves: [correctness]
status: full
---

We prove that if both parties follow the protocol of lines L1 to L23, the evaluator outputs $C(x, y)$. The proof uses only the algebra of the labels; it does not depend on any property of $H$ beyond being a function. Security is a separate claim (see the page).

**Setting.** Let $v_w$ be the value of wire $w$ when the circuit $C$ is evaluated in the clear on inputs $(x, y)$. The garbler has $\Delta$ with $\mathrm{lsb}(\Delta) = 1$ (line L1) and a label $W_w^0$ for each wire; we write $W_w^1 = W_w^0 \oplus \Delta$, so $W_w^v = W_w^0 \oplus v\Delta$ for $v \in \{0, 1\}$. Here $v\Delta$ is $\Delta$ if $v = 1$ and the zero string if $v = 0$. The evaluator's label on wire $w$ is $X_w$, and $p_w = \mathrm{lsb}(W_w^0)$ is the permute bit.

**Invariant (I).** After the evaluator processes a wire $w$, $X_w = W_w^{v_w}$.

**Input wires.** Line L2 picks $W_w^0$ for every input wire. For a garbler input wire, line L21 sends $W_w^{x_w}$. For an evaluator input wire, the OT of line L22 delivers $W_w^{y_w}$. So (I) holds on all input wires.

**Gates.** We process the gates in the topological order of lines L3 and L15, so (I) holds for both inputs $a$ and $b$ of gate $j$ when we reach it. Write $\alpha = v_a$ and $\beta = v_b$.

*XOR gate.* Line L4 sets $W_c^0 = W_a^0 \oplus W_b^0$, and line L16 sets $X_c = X_a \oplus X_b = W_a^0 \oplus \alpha\Delta \oplus W_b^0 \oplus \beta\Delta = W_c^0 \oplus (\alpha \oplus \beta)\Delta = W_c^{v_c}$.

*INV gate.* Line L5 sets $W_c^0 = W_a^0 \oplus \Delta$, so $W_c^{1 - \alpha} = W_c^0 \oplus (1 - \alpha)\Delta = W_a^0 \oplus \alpha\Delta = X_a$. Line L17 sets $X_c = X_a = W_c^{1-\alpha} = W_c^{v_c}$.

*AND gate.* Write $h_a(z) = H(z, 2j)$ and $h_b(z) = H(z, 2j+1)$. Lines L7 to L12 give

$$T_G = h_a(W_a^0) \oplus h_a(W_a^1) \oplus p_b\Delta, \quad W_G = h_a(W_a^0) \oplus p_a T_G,$$
$$T_E = h_b(W_b^0) \oplus h_b(W_b^1) \oplus W_a^0, \quad W_E = h_b(W_b^0) \oplus p_b (T_E \oplus W_a^0),$$

and $W_c^0 = W_G \oplus W_E$. Line L18 computes $s_a = \mathrm{lsb}(X_a) = p_a \oplus \alpha$, because $\mathrm{lsb}(\Delta) = 1$; in the same way $s_b = p_b \oplus \beta$. Line L19 computes $X_c = G \oplus E$ with $G = h_a(X_a) \oplus s_a T_G$ and $E = h_b(X_b) \oplus s_b(T_E \oplus X_a)$.

*Claim 1: $G = W_G \oplus (\alpha p_b)\Delta$.* If $\alpha = 0$, then $X_a = W_a^0$ and $s_a = p_a$, so $G = W_G$. If $\alpha = 1$, then $X_a = W_a^1$ and $s_a = 1 \oplus p_a$. From the definition of $T_G$, $h_a(W_a^1) = h_a(W_a^0) \oplus T_G \oplus p_b\Delta$. So $G = h_a(W_a^0) \oplus T_G \oplus p_b\Delta \oplus T_G \oplus p_a T_G = W_G \oplus p_b\Delta$.

*Claim 2: $E = W_E \oplus \alpha(\beta \oplus p_b)\Delta$.* Note $X_a \oplus W_a^0 = \alpha\Delta$.

- If $\beta = 0$: $X_b = W_b^0$ and $s_b = p_b$, so $E = h_b(W_b^0) \oplus p_b(T_E \oplus X_a) = W_E \oplus p_b \alpha \Delta$, and $\alpha(\beta \oplus p_b) = \alpha p_b$.
- If $\beta = 1$: $X_b = W_b^1$ and $s_b = 1 \oplus p_b$. From the definition of $T_E$, $h_b(W_b^1) = h_b(W_b^0) \oplus T_E \oplus W_a^0$. If $p_b = 0$, then $E = h_b(W_b^0) \oplus T_E \oplus W_a^0 \oplus T_E \oplus X_a = h_b(W_b^0) \oplus \alpha\Delta = W_E \oplus \alpha\Delta$, and $\alpha(\beta \oplus p_b) = \alpha$. If $p_b = 1$, then $s_b = 0$ and $E = h_b(W_b^0) \oplus T_E \oplus W_a^0 = W_E$, and $\alpha(\beta \oplus p_b) = 0$.

Adding the claims, $X_c = W_G \oplus W_E \oplus \big(\alpha p_b \oplus \alpha\beta \oplus \alpha p_b\big)\Delta = W_c^0 \oplus (\alpha\beta)\Delta = W_c^{v_c}$. So (I) holds for wire $c$.

**Outputs.** Line L13 sets $d_w = \mathrm{lsb}(W_w^0) = p_w$. By (I), the evaluator holds $X_w = W_w^0 \oplus v_w \Delta$ for each output wire, so $\mathrm{lsb}(X_w) = p_w \oplus v_w$, and line L20 returns $\mathrm{lsb}(X_w) \oplus d_w = v_w$. These are the output bits of $C(x, y)$. $\blacksquare$

**Remark.** The proof works for any labels $W_w^0$ and any function $H$. Randomness of the labels and properties of $H$ are needed only for security: the evaluator must not be able to tell $W_w^0$ from $W_w^1$, which needs $\Delta$ to stay hidden, and that in turn needs $H$ to be circular correlation robust.
