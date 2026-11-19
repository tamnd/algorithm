---
title: Multi-head attention returns Concat(H_1, ..., H_h) W^O, this equals the sum of the head outputs H_r W^O_r, one full-size head is plain attention on projected inputs, and unmasked self-attention is permutation equivariant
proves: [correctness]
status: full
---

We use the notation of the page. $X_q$ is $n \times d$, $X_{kv}$ is $m \times d$, $W^Q_r$ and $W^K_r$ are $d \times d_k$, $W^V_r$ is $d \times d_v$ and $W^O$ is $h d_v \times d$. We split $W^O$ into $h$ blocks of $d_v$ consecutive rows, $W^O = \begin{pmatrix} W^O_1 \\ \vdots \\ W^O_h \end{pmatrix}$. The mask $M$ is the same for all heads, and every query sees at least one key. We use the correctness theorem of [scaled dot-product attention](/scaled-dot-product-attention/): ATTENTION$(Q, K, V, M)$ returns the row softmax of the masked scaled scores times $V$.

**Lemma 1 (the heads).** After iteration $r$ of line L1, $H_r = \operatorname{Attention}(X_q W^Q_r, X_{kv} W^K_r, X_{kv} W^V_r)$.

*Proof.* Lines L2 to L4 compute the three products of the definition, with the shapes $n \times d_k$, $m \times d_k$ and $m \times d_v$ that ATTENTION needs. Line L5 then returns the attention of these three matrices by the correctness of scaled dot-product attention. Iterations do not share state, so each $H_r$ is computed independently of the others. $\square$

**Theorem 2 (correctness).** MULTI-HEAD returns $\operatorname{Concat}(H_1, \ldots, H_h) W^O$.

*Proof.* By Lemma 1 all $h$ heads are correct when the loop ends. Line L6 forms the $n \times h d_v$ matrix whose columns $(r - 1) d_v + 1$ to $r d_v$ are $H_r$, which is the concatenation in the order of the heads. Line L7 multiplies it by $W^O$. $\square$

**Theorem 3 (sum of heads).** $\operatorname{Concat}(H_1, \ldots, H_h)\, W^O = \sum_{r=1}^{h} H_r W^O_r$.

*Proof.* Let $H = \operatorname{Concat}(H_1, \ldots, H_h)$. Entry $(i, c)$ of $H W^O$ is $\sum_{t=1}^{h d_v} H_{it} W^O_{tc}$. Split the index $t$ into the head $r$ and the place $b$ in the head, $t = (r - 1) d_v + b$ with $1 \le b \le d_v$. Then $H_{it} = (H_r)_{ib}$ and $W^O_{tc} = (W^O_r)_{bc}$, so

$$\sum_{t=1}^{h d_v} H_{it} W^O_{tc} = \sum_{r=1}^{h} \sum_{b=1}^{d_v} (H_r)_{ib} (W^O_r)_{bc} = \sum_{r=1}^{h} (H_r W^O_r)_{ic}. \qquad \square$$

**Corollary 4 (one head).** For $h = 1$ the output is $\operatorname{Attention}(X_q W^Q, X_{kv} W^K, X_{kv} W^V)\, W^O$, plain attention on projected inputs followed by a linear map.

*Proof.* Theorem 3 with a single term. $\square$

**Theorem 5 (permutation equivariance).** Take self-attention, $X_q = X_{kv} = X$, with no mask. Let $P$ be the $n \times n$ matrix of a permutation $\sigma$, so $(P X)_i = X_{\sigma(i)}$. Then $\operatorname{MultiHead}(P X, P X) = P \operatorname{MultiHead}(X, X)$.

*Proof.* For each head, $(P X) W^Q_r = P (X W^Q_r)$, and the same holds for $W^K_r$ and $W^V_r$. So the inputs of head $r$ on $P X$ are $P Q_r$, $P K_r$ and $P V_r$. By the permutation theorem of scaled dot-product attention, permuting the queries by $\sigma$ permutes the output rows by $\sigma$, and permuting the keys and the values together by the same $\sigma$ leaves the output unchanged. So head $r$ returns $P H_r$. Then

$$\operatorname{Concat}(P H_1, \ldots, P H_h)\, W^O = P \operatorname{Concat}(H_1, \ldots, H_h)\, W^O,$$

because $P$ acts on the rows and the concatenation acts on the columns. $\blacksquare$

With a causal mask Theorem 5 fails, since the mask depends on the positions. In its place, the row of token $i$ depends only on tokens $1, \ldots, i$: in every head, by the causal property of scaled dot-product attention, row $i$ of $H_r$ depends only on rows $j \le i$ of $K_r$ and $V_r$, which are functions of rows $j \le i$ of $X$; and line L7 maps each row of $H$ on its own.
