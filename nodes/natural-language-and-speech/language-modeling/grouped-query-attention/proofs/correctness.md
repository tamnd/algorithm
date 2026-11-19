---
title: GQA returns Concat(head_0, ..., head_(h-1)) W^O with head r reading group floor(r / (h/g)), it equals multi-head attention with copied key and value maps, and mean pooling keeps a model whose group heads agree
proves: [correctness]
status: full
---

We use the notation of the page. $g$ divides $h$, $k = h/g$ is the group size, and $s(r) = \lfloor r / k \rfloor$ for $r = 0, \ldots, h - 1$. For a matrix $W$ with $c$ columns per head, $W_r$ is its column block $r c, \ldots, (r + 1) c - 1$. The target output is

$$\mathrm{GQA}^\ast = \mathrm{Concat}\big(\mathrm{Att}(X_q W^Q_0, X_{kv} W^K_{s(0)}, X_{kv} W^V_{s(0)}), \ldots, \mathrm{Att}(X_q W^Q_{h-1}, X_{kv} W^K_{s(h-1)}, X_{kv} W^V_{s(h-1)})\big)\, W^O,$$

where Att is scaled dot-product attention, with or without the causal mask, the same for all heads.

**Lemma 1 (the map is onto the groups).** $s$ maps $\{0, \ldots, h-1\}$ onto $\{0, \ldots, g-1\}$, and each group $s$ receives exactly the $k$ heads $s k, \ldots, s k + k - 1$.

*Proof.* Write $r = s k + t$ with $0 \le t < k$ (division with remainder). Then $\lfloor r / k \rfloor = s$, and $r \le h - 1 = g k - 1$ gives $s \le g - 1$. Conversely each $s \le g - 1$ and $t < k$ gives a head $r = s k + t \le h - 1$. $\square$

**Lemma 2 (the procedure).** GQA returns $\mathrm{GQA}^\ast$.

*Proof.* The loop at line L1 runs for $s = 0, \ldots, g - 1$, and line L2 stores $K_s = X_{kv} W^K_s$ and $V_s = X_{kv} W^V_s$; these are not changed later. The loop at line L3 runs for each head $r$; line L4 sets $s = s(r)$, which by Lemma 1 is a stored index, line L5 forms $Q_r = X_q W^Q_r$, and line L6 sets $\mathrm{head}_r = \mathrm{Att}(Q_r, K_{s(r)}, V_{s(r)})$. Line L7 concatenates the heads in the order $r = 0, \ldots, h-1$ and multiplies by $W^O$, which is $\mathrm{GQA}^\ast$. $\square$

**Theorem 3 (multi-head attention with copied maps).** Let $\tilde W^K$ have the column blocks $\tilde W^K_r = W^K_{s(r)}$ for $r = 0, \ldots, h-1$, and $\tilde W^V$ likewise. Then GQA with $(W^Q, W^K, W^V, W^O, h, g)$ equals multi-head attention with $(W^Q, \tilde W^K, \tilde W^V, W^O, h)$, that is, GQA with $g = h$.

*Proof.* With $g = h$ the map is $s(r) = r$, so head $r$ of the second layer is $\mathrm{Att}(X_q W^Q_r, X_{kv} \tilde W^K_r, X_{kv} \tilde W^V_r) = \mathrm{Att}(X_q W^Q_r, X_{kv} W^K_{s(r)}, X_{kv} W^V_{s(r)})$, which is head $r$ of the first layer. The concatenation and $W^O$ are the same. Apply Lemma 2 to both. $\square$

**Corollary 4.** If $g$ divides $g'$ and $g'$ divides $h$, every function computed by GQA with $g$ groups is computed by GQA with $g'$ groups.

*Proof.* Let $k' = h/g'$ and $s'(r) = \lfloor r / k' \rfloor$. Given $W^K$ with $g$ blocks, define $W'^K_{s'} = W^K_{\lfloor s' g / g' \rfloor}$ for $s' = 0, \ldots, g' - 1$, and $W'^V$ likewise. For a head $r$, $s'(r) = \lfloor r g' / h \rfloor$ and $\lfloor s'(r)\, g / g' \rfloor = \lfloor \lfloor r g' / h \rfloor g / g' \rfloor = \lfloor r g / h \rfloor = s(r)$, by the rule $\lfloor \lfloor x \rfloor / a \rfloor = \lfloor x / a \rfloor$ for a positive integer $a = g'/g$. So both layers give head $r$ the same key and value maps, and by Lemma 2 they compute the same function. $\square$

**Theorem 5 (mean pooling).** Let a multi-head layer have key maps $\tilde W^K_0, \ldots, \tilde W^K_{h-1}$ with $\tilde W^K_r = \tilde W^K_{r'}$ whenever $s(r) = s(r')$. Mean pooling sets $W^K_s = \frac1k \sum_{t=0}^{k-1} \tilde W^K_{s k + t}$. Then $W^K_{s(r)} = \tilde W^K_r$ for every $r$, and with the same for the values, the GQA layer computes the same function as the multi-head layer.

*Proof.* By Lemma 1 the heads $s k + t$, $t < k$, are exactly the heads of group $s$, and they all equal $\tilde W^K_r$ for any $r$ in the group. The mean of $k$ equal matrices is that matrix. The claim then follows from Theorem 3. $\blacksquare$

**Cache size.** For each layer and token, GQA stores the rows of $K_0, \ldots, K_{g-1}$ and $V_0, \ldots, V_{g-1}$, that is $g (d_k + d_v)$ numbers, against $h (d_k + d_v)$ for multi-head attention: a factor $g / h$.
