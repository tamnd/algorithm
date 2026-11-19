---
title: The SimCSE loss is computed exactly in log space and its gradient is exact
proves: [correctness]
status: full
---

We use the pseudocode of the page. The batch has $N \ge 1$ sentences. The vectors $h_i$, $h^+_i$ and, when hard negatives are given, $h^-_i$ are nonzero vectors of $\mathbb{R}^d$. The temperature is $\tau > 0$. Write $s_{ij} = \cos(h_i, h^+_j)$ and $s'_{ij} = \cos(h_i, h^-_j)$, so that $z_{ij} = s_{ij} / \tau$ and $z'_{ij} = s'_{ij} / \tau$. The loss of the paper is

$$L = \frac{1}{N} \sum_{i=1}^{N} \ell_i, \qquad \ell_i = -\log \frac{e^{z_{ii}}}{Z_i}, \qquad Z_i = \sum_{j=1}^{N} e^{z_{ij}} + \sum_{j=1}^{N} e^{z'_{ij}},$$

where the second sum is absent when there are no hard negatives (equation 1 of Gao, Yao and Chen 2021 without it, equation 5 with it).

**Lemma 1 (the loss).** Lines L1 to L6 return $L$.

*Proof.* For a finite list $x_1, \ldots, x_m$ with maximum $M$, $\log \sum_k e^{x_k} = M + \log \sum_k e^{x_k - M}$, because $e^{x_k} = e^M e^{x_k - M}$. The helper log_sum computes the right side, so line L5 sets $lz_i = \log Z_i$. Then $\ell_i = -\log e^{z_{ii}} + \log Z_i = lz_i - z_{ii}$, which is what line L5 stores, and line L6 takes the mean. Every exponent in the right side is at most 0, so no term overflows, whatever the size of $1 / \tau$. $\square$

**Lemma 2 (the gradient of the cosine).** For nonzero $a, b$ with $c = \cos(a, b)$,

$$\frac{\partial c}{\partial a} = \frac{b}{\|a\| \|b\|} - c \frac{a}{\|a\|^2},$$

and the same with $a$ and $b$ swapped. This gradient is orthogonal to $a$.

*Proof.* $c = (a \cdot b) \|a\|^{-1} \|b\|^{-1}$, and $\partial \|a\| / \partial a = a / \|a\|$. The product rule gives $b \|a\|^{-1} \|b\|^{-1} - (a \cdot b) \|a\|^{-2} \|b\|^{-1} a / \|a\|$, which is the formula. Its inner product with $a$ is $(a \cdot b) / (\|a\| \|b\|) - c = 0$. $\square$

**Lemma 3 (the gradient with respect to the logits).** $\partial \ell_i / \partial z_{ij} = p_{ij} - [i = j]$ and $\partial \ell_i / \partial z'_{ij} = p'_{ij}$, where $p_{ij} = e^{z_{ij}} / Z_i$ and $p'_{ij} = e^{z'_{ij}} / Z_i$. The row $i$ of the logits does not enter $\ell_k$ for $k \ne i$.

*Proof.* $\ell_i = \log Z_i - z_{ii}$. The derivative of $\log Z_i$ with respect to $z_{ij}$ is $e^{z_{ij}} / Z_i$, and the derivative of $z_{ii}$ is $[i = j]$. The same holds for $z'_{ij}$, which never equals $z_{ii}$. The second statement holds because $\ell_k$ uses only $z_{kj}$ and $z'_{kj}$. $\square$

**Theorem.** Lines L7 to L11, with the hard-negative terms of the code, return $\partial L / \partial h_i$, $\partial L / \partial h^+_j$ and $\partial L / \partial h^-_j$ exactly.

*Proof.* Line L7 computes $\exp(z_{ij} - lz_i) = e^{z_{ij}} / Z_i = p_{ij}$ by Lemma 1, and the code computes $p'_{ij}$ the same way. By Lemma 3 and $z_{ij} = s_{ij} / \tau$,

$$\frac{\partial L}{\partial s_{ij}} = \frac{p_{ij} - [i = j]}{N \tau}, \qquad \frac{\partial L}{\partial s'_{ij}} = \frac{p'_{ij}}{N \tau}.$$

The first is the value $g$ of line L8, and the second is the value g2 of the code. The vector $h_i$ enters only the similarities $s_{ij}$ and $s'_{ij}$ of row $i$, the vector $h^+_j$ only the similarities $s_{ij}$ of column $j$, and $h^-_j$ only the $s'_{ij}$ of column $j$. By the chain rule,

$$\frac{\partial L}{\partial h_i} = \sum_j \frac{\partial L}{\partial s_{ij}} \frac{\partial s_{ij}}{\partial h_i} + \sum_j \frac{\partial L}{\partial s'_{ij}} \frac{\partial s'_{ij}}{\partial h_i}, \qquad \frac{\partial L}{\partial h^+_j} = \sum_i \frac{\partial L}{\partial s_{ij}} \frac{\partial s_{ij}}{\partial h^+_j},$$

and the same for $h^-_j$. Lines L9 and L10 add exactly these terms, with the cosine gradients of Lemma 2, once for each pair $(i, j)$. The accumulators start at 0, so after the loop they hold the sums. Line L11 returns them. $\blacksquare$

**Consequences used by the tests.**

- $\ell_i = \log(1 + \sum_{j \ne i} e^{z_{ij} - z_{ii}} + \sum_j e^{z'_{ij} - z_{ii}}) \ge 0$. Since every cosine is in $[-1, 1]$, each difference $z_{ij} - z_{ii}$ is at least $-2 / \tau$, so without hard negatives $\ell_i \ge \log(1 + (N - 1) e^{-2/\tau})$.
- For $N = 1$ and no hard negatives, $Z_1 = e^{z_{11}}$, so $L = 0$, $p_{11} = 1$ and every gradient is 0.
- Each gradient is a sum of cosine gradients of Lemma 2 taken at the same vector, so it is orthogonal to that vector. The loss does not change when a vector is multiplied by a positive number, since the cosines do not change.
- If the $h_i = h^+_i$ are orthonormal, then $z_{ii} = 1 / \tau$, $z_{ij} = 0$ for $i \ne j$, and $L = \log(1 + (N - 1) e^{-1/\tau})$.
