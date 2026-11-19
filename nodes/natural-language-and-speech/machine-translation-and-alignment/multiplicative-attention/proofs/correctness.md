---
title: Global and local multiplicative attention return the stated weights, and the gradients of the general score are as stated
proves: [correctness]
status: full
---

Fix the decoder state $h_t \in \mathbb{R}^d$ and the source states $\bar h_1, \ldots, \bar h_S \in \mathbb{R}^{d}$ with $S \ge 1$. The score is one of $\mathrm{dot}(h_t, \bar h_s) = h_t^\top \bar h_s$, $\mathrm{general}(h_t, \bar h_s) = h_t^\top W_a \bar h_s$ and $\mathrm{concat}(h_t, \bar h_s) = v_a^\top \tanh(W_a [h_t; \bar h_s])$. The window is $K = \{1, \ldots, S\}$ for global attention, and $K = \{s : 1 \le s \le S, |s - p| \le D\}$ for local attention, with $p = t$ (local-m) or $p = S \cdot \sigma(v_p^\top \tanh(W_p h_t))$ (local-p), where $\sigma$ is the logistic function. Luong et al. (2015) define

$$\mathrm{align}_s = \frac{\exp(e_s)}{\sum_{s' \in K} \exp(e_{s'})} \ (s \in K), \qquad a_s = \mathrm{align}_s \ \text{(global, local-m)}, \qquad a_s = \mathrm{align}_s \exp\Bigl(-\frac{(s - p)^2}{2 (D/2)^2}\Bigr) \ \text{(local-p)},$$

with $a_s = 0$ for $s \notin K$, the context $c = \sum_s a_s \bar h_s$ and the attentional state $\tilde h = \tanh(W_c [c; h_t])$.

**Theorem 1 (the output).** If $K$ is not empty, lines L1 to L9 return $c$, $a$ and $\tilde h$ of the definition. For global attention and local-m, $a_s \ge 0$ and $\sum_s a_s = 1$, so $c$ is a convex combination of the states in the window. For local-p, $0 \le a_s \le \mathrm{align}_s$ and $\sum_s a_s \le 1$, with equality only if the window is the single position $s = p$. For local-p, $p \in [0, S]$.

*Proof.* Lines L1 and L2 build $K$. Lines L3 and L4 compute $e_s$ for $s \in K$. Line L5 computes the softmax over $K$ with the maximum subtracted first, which multiplies the numerator and the denominator by the same positive factor, so it equals $\mathrm{align}_s$. Line L6 applies the Gaussian factor for local-p. Line L7 forms $c$, with $a_s = 0$ outside $K$, and line L8 forms $\tilde h$.

The softmax values are positive and sum to 1 over $K$, which gives the claim for global attention and local-m. For local-p, the Gaussian factor is in $(0, 1]$ and equals 1 only at $s = p$, so $a_s \le \mathrm{align}_s$ and the sum is at most 1. It equals 1 only if every $s \in K$ has $s = p$, that is $K = \{p\}$. The logistic function maps into $(0, 1)$, and in floating point into $[0, 1]$, so $p \in [0, S]$. $\square$

**Theorem 2 (relations between the scores).** (a) The dot score is the general score with $W_a = I$. (b) Global attention with the general score and $W_a = I / \sqrt{d}$ returns the output of [scaled dot-product attention](/scaled-dot-product-attention/) for the single query $h_t$, with the keys and the values both equal to the source states. (c) The concat score equals $v_a^\top \tanh(W_1 h_t + W_2 \bar h_s)$, where $W_a = [W_1\ W_2]$ is split by columns, which is the additive score of Bahdanau et al. with the current state $h_t$ in place of $s_{i-1}$.

*Proof.* (a) $h_t^\top I \bar h_s = h_t^\top \bar h_s$. (b) $h_t^\top (I / \sqrt{d}) \bar h_s = h_t^\top \bar h_s / \sqrt{d}$, and the softmax and the weighted sum of the values $\bar h_s$ are the same operations in both definitions. (c) $W_a [h_t; \bar h_s] = W_1 h_t + W_2 \bar h_s$ by the rules of block matrix products. $\square$

**Theorem 3 (the gradients of the general score).** For global attention with the general score and $L = g^\top \tilde h$, let $z = W_c [c; h_t]$, $r = g \odot (1 - \tilde h \odot \tilde h)$ and $[\,\bar g; g_h] = W_c^\top r$, split into the first $d$ and the last $d$ entries. With $\gamma_s = \bar g^\top \bar h_s$, $\bar\gamma = \sum_s a_s \gamma_s$ and $\delta_s = a_s (\gamma_s - \bar\gamma)$,

$$\frac{\partial L}{\partial W_c} = r\, [c; h_t]^\top, \quad \frac{\partial L}{\partial h_t} = g_h + \sum_s \delta_s W_a \bar h_s, \quad \frac{\partial L}{\partial \bar h_s} = a_s \bar g + \delta_s W_a^\top h_t, \quad \frac{\partial L}{\partial W_a} = \sum_s \delta_s\, h_t \bar h_s^\top.$$

*Proof.* $\tanh' = 1 - \tanh^2$ gives $\partial L / \partial z = r$, and $z$ is linear in $W_c$ and in $[c; h_t]$, which gives the first formula and the vector $[\bar g; g_h]$. The context $c = \sum_s a_s \bar h_s$ gives the term $a_s \bar g$ for $\bar h_s$, and $\partial L / \partial a_s = \gamma_s$. The softmax Jacobian $\partial a_k / \partial e_s = a_k([k = s] - a_s)$ gives $\partial L / \partial e_s = \delta_s$. Finally $e_s = h_t^\top W_a \bar h_s$ has the derivatives $W_a \bar h_s$ in $h_t$, $W_a^\top h_t$ in $\bar h_s$ and $h_t \bar h_s^\top$ in $W_a$. The term $g_h$ is the direct path from $h_t$ to $z$. $\square$

The tests compare these gradients with central finite differences, and they check Theorem 2 (b) against a separate implementation of scaled dot-product attention.

**Remark (local-p is differentiable almost everywhere).** The window $K$ changes only when some $|s - p|$ crosses $D$. Between these points $K$ is fixed and $a_s$ is a smooth function of $p$, so of $W_p$ and $v_p$. So gradient training works almost everywhere, and the sets of measure zero where the window changes do not matter in practice (a heuristic).

**Remark (complexity).** For global attention with the dot score, one step costs $O(S d)$; with the general score, precomputing $W_a \bar h_s$ once per sentence leaves $O(S d)$ per step. Local attention costs $O(\min(S, 2D + 1)\, d)$ per step plus $O(d^2)$ for $p$ and for the general product. Line L8 costs $O(d^2)$.
