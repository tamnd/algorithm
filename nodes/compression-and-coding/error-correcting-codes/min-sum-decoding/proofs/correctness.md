---
title: The min-sum check rule is the max-log form of the tanh rule, min-sum gives the max-log LLRs on a tree, and its messages are never smaller than those of belief propagation
proves: [correctness]
status: full
---

LLRs are $\ln P(0) / P(1)$. A bit $b$ with LLR $\ell$ gets the log weight $w(b) = (1 - 2b)\ell / 2$, so $w(0) - w(1) = \ell$. The code is $C = \{c : H c^T = 0\}$ with Tanner graph $G$, $N(i)$ the variables of check $i$ and $M(j)$ the checks of variable $j$. Channel LLRs are $L_j$.

**Lemma 1 (the check rule).** Let $b_1, \ldots, b_r$ have LLRs $\ell_1, \ldots, \ell_r$. Then

$$\max_{b : \oplus b = 0} \sum_k w_k(b_k) - \max_{b : \oplus b = 1} \sum_k w_k(b_k) = \Bigl(\prod_k \operatorname{sgn} \ell_k\Bigr) \min_k |\ell_k|,$$

with $\operatorname{sgn} 0 = +1$.

*Proof.* The unconstrained maximum of $\sum_k w_k(b_k)$ takes each $b_k$ with $w_k(b_k) = |\ell_k|/2$, that is $b_k = 0$ when $\ell_k \ge 0$. Its parity is 1 exactly when an odd number of the $\ell_k$ are negative, that is when $\prod_k \operatorname{sgn} \ell_k = -1$. Changing a set $S$ of the bits costs $\sum_{k \in S} |\ell_k|$, and the parity changes when $|S|$ is odd, so the best configuration of the other parity changes only one bit, the one with the least $|\ell_k|$, at the cost $\min_k |\ell_k|$. If the free maximum has parity 0, the left side is $+\min_k |\ell_k|$; otherwise it is $-\min_k |\ell_k|$. $\square$

So lines L3 to L5 with mode "plain" compute, for each edge $(i, j)$, the max-log LLR of the XOR of the other bits of check $i$, which the check forces $c_j$ to equal.

**Lemma 2 (two least values).** Let $a$ be an index of a least magnitude, $m_1 = |x_a|$, and $m_2$ the least magnitude over the other indices. Then for each $b$, $\min_{k \ne b} |x_k|$ is $m_2$ if $b = a$ and $m_1$ otherwise. Also the product of the signs of the others is the product of all signs times the sign of $x_b$.

*Proof.* If $b \ne a$, the set $\{k \ne b\}$ contains $a$, and $m_1$ is the least over all indices, so the minimum is $m_1$. If $b = a$, it is $m_2$ by definition. For the signs, multiplying by $\operatorname{sgn} x_b$ twice gives 1. $\square$

Lemma 2 shows that lines L3 and L4 give the same messages as the direct rule that takes the minimum over the others for each edge; the implementation tests check this against a direct version.

**Theorem 1 (trees).** If $G$ is a forest, and $D$ is the largest number of checks on a path, then after $t \ge D$ iterations of plain min-sum without early stop, the posterior of line L6 is

$$\Lambda_j = \max_{c \in C,\ c_j = 0} \sum_k w_k(c_k) - \max_{c \in C,\ c_j = 1} \sum_k w_k(c_k) = \min_{c \in C,\ c_j = 1} \sum_k c_k L_k - \min_{c \in C,\ c_j = 0} \sum_k c_k L_k,$$

the max-log LLR of bit $j$. Its sign is the value of $c_j$ in the ML codeword when that codeword is unique.

*Proof.* This is the proof of exactness of [belief propagation](/belief-propagation-decoding/) on trees, in the $(\max, +)$ semiring instead of $(+, \times)$. Cutting the edge $(i, j)$ splits the tree into $T_{i \to j}$ and $T_{j \to i}$. Define $\nu_{i \to j}$ as the difference of the best total weights in $T_{i \to j}$ that satisfy its checks with $c_j = 0$ and with $c_j = 1$, and $\mu_{j \to i}$ as the same for $c_j$ inside $T_{j \to i}$. The subtrees below a node share no variable and no check, so the best total weight is a sum of the best weights of the subtrees, because $\max(a + x, a + y) = a + \max(x, y)$ and the maximum of a sum of independent terms is the sum of their maxima. This gives

$$\mu_{j \to i} = L_j + \sum_{i' \in M(j) \setminus i} \nu_{i' \to j}, \qquad \nu_{i \to j} = \Bigl(\prod_{k \in N(i) \setminus j} \operatorname{sgn} \mu_{k \to i}\Bigr) \min_{k \in N(i) \setminus j} |\mu_{k \to i}|,$$

where the second formula is Lemma 1 applied to the subtrees $T_{k \to i}$, each of which offers the two values of $c_k$ with best weights that differ by $\mu_{k \to i}$. The induction on the depth of $T_{i \to j}$ is then word for word that of belief propagation: line L1 starts the variable messages at $L_k$, line L8 sets them to $L_k$ plus the other incoming check messages, and after $d(i \to j)$ iterations the message on $i \to j$ is $\nu_{i \to j}$. Line L6 adds all $\nu_{i \to j}$ to $L_j$, which is the max-log LLR of $c_j$ over the whole tree. The second form follows from $\sum_k w_k(c_k) = \tfrac12 \sum_k L_k - \sum_k c_k L_k$. If the ML codeword $\hat c$ is unique, the maximum on the side of $\hat c_j$ is strictly larger, so $\operatorname{sgn} \Lambda_j$ gives $\hat c_j$. $\blacksquare$

**Theorem 2 (min-sum overestimates).** For any real $\ell_1, \ldots, \ell_r$,

$$\Bigl|\, 2 \operatorname{artanh} \prod_k \tanh(\ell_k / 2) \Bigr| \le \min_k |\ell_k|,$$

and the two sides have the same sign. So the plain min-sum message of a check is never smaller in size than the belief propagation message from the same inputs.

*Proof.* $\tanh$ is odd, so the sign of the product is $\prod_k \operatorname{sgn} \ell_k$, the sign of the min-sum message. For the size, each $|\tanh(\ell_k / 2)| \le 1$, so $\prod_k |\tanh(\ell_k / 2)| \le |\tanh(\ell_a / 2)|$ for the index $a$ of the least $|\ell_k|$. The map $x \mapsto 2 \operatorname{artanh} x$ is increasing on $[0, 1)$, which gives $2 \operatorname{artanh} \prod_k |\tanh(\ell_k/2)| \le |\ell_a|$. $\square$

This is why the corrections help. The normalized rule multiplies the size by $\alpha \in (0, 1]$ and the offset rule subtracts $\beta \ge 0$ and stops at 0; both move the message toward the belief propagation value without changing its sign (the offset rule can make it 0). With $\alpha = 1$ or $\beta = 0$ they are plain min-sum.

**Corollary (no noise estimate needed).** If every channel LLR is multiplied by $s > 0$, every message and posterior of plain min-sum is multiplied by $s$, and the decisions do not change. The proof is by induction on the iterations: sums, signs and minima commute with multiplication by $s > 0$. So plain min-sum needs only $y_j$ and not $\sigma^2$. Normalized min-sum has the same property, since $\alpha$ is a factor. The offset rule does not, because $\beta$ is in the units of the LLRs.

**The output.** Line L7 returns only words that satisfy all checks. With cycles, as for belief propagation, Theorem 1 does not apply, and the posterior is an approximation of the max-log LLR.
