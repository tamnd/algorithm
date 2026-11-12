---
title: The tanh rule is exact for one check, and belief propagation gives the exact bitwise posteriors on a Tanner graph that is a tree
proves: [correctness]
status: full
---

**Setting.** $H$ is an $m \times n$ binary matrix with Tanner graph $G$; $N(i)$ is the set of variables of check $i$ and $M(j)$ the set of checks of variable $j$. The code is $C = \{c : H c^T = 0\}$, the codewords are equally likely, and the channel is memoryless with LLRs $L_j = \ln P(y_j \mid 0) / P(y_j \mid 1)$. Then

$$P(c \mid y) \propto \prod_{i=1}^{m} [\, \textstyle\sum_{j \in N(i)} c_j \equiv 0 \,] \prod_{j=1}^{n} e^{(1 - 2c_j) L_j / 2},$$

as in the definition of [symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/). All LLRs are $\ln P(0) / P(1)$.

**Lemma 1 (the tanh rule).** Let $b_1, \ldots, b_r$ be independent bits with LLRs $\ell_1, \ldots, \ell_r$. Then the LLR of $b_1 \oplus \cdots \oplus b_r$ is

$$2 \operatorname{artanh} \prod_{k=1}^{r} \tanh(\ell_k / 2).$$

*Proof.* For one bit with $P(0) = p$, $P(0) - P(1) = 2p - 1$, and $p = e^{\ell} / (1 + e^{\ell})$ gives $2p - 1 = (e^{\ell} - 1)/(e^{\ell} + 1) = \tanh(\ell / 2)$. For independent bits, $E[(-1)^{b_1 \oplus \cdots \oplus b_r}] = \prod_k E[(-1)^{b_k}]$, and $E[(-1)^{b}] = P(0) - P(1)$. So $P(\oplus = 0) - P(\oplus = 1) = \prod_k \tanh(\ell_k / 2)$, and inverting the first identity gives the LLR. $\square$

A check $i$ forces $c_j = \bigoplus_{k \in N(i) \setminus j} c_k$. So when the other bits of the check are independent with LLRs $\ell_k$, the check tells $c_j$ the LLR $2 \operatorname{artanh} \prod_{k \ne j} \tanh(\ell_k / 2)$. This is line L3.

**Trees.** Assume from now on that $G$ is a forest. Removing the edge $(i, j)$ splits the component into two trees. Let $T_{i \to j}$ be the part that contains $i$, and $T_{j \to i}$ the part that contains $j$. Define the exact messages:

- $\mu_{j \to i}$ is the LLR of $c_j$ in the model restricted to $T_{j \to i}$: only the checks and the channel values of the variables in $T_{j \to i}$ are used.
- $\nu_{i \to j}$ is the LLR that the checks and the channel values in $T_{i \to j}$ give about $c_j$, the variable just outside: the log of the ratio of $\sum P$ over the configurations of the variables of $T_{i \to j}$ that satisfy its checks with $c_j = 0$, to the same sum with $c_j = 1$.

**Lemma 2 (the tree recursions).**

$$\mu_{j \to i} = L_j + \sum_{i' \in M(j) \setminus i} \nu_{i' \to j}, \qquad \nu_{i \to j} = 2 \operatorname{artanh} \prod_{k \in N(i) \setminus j} \tanh(\mu_{k \to i} / 2),$$

and the exact posterior LLR of $c_j$ given all of $y$ is $L(c_j) = L_j + \sum_{i \in M(j)} \nu_{i \to j}$.

*Proof.* $T_{j \to i}$ is $j$ together with the disjoint trees $T_{i' \to j}$ for $i' \in M(j) \setminus i$. Fix $c_j$. The sum over the configurations of $T_{j \to i}$ is $e^{(1 - 2c_j) L_j / 2}$ times the product, over $i'$, of the sums over the configurations of $T_{i' \to j}$, because these trees share no variable and no check. Taking the ratio for $c_j = 0$ and $c_j = 1$ and the logarithm turns the product into the sum of the $\nu_{i' \to j}$. The posterior formula is the same argument with all of $M(j)$.

For $\nu_{i \to j}$: $T_{i \to j}$ is $i$ together with the disjoint trees $T_{k \to i}$ for $k \in N(i) \setminus j$. The configurations of these trees are independent in the restricted model, and in each the marginal LLR of $c_k$ is $\mu_{k \to i}$. The check $i$ then holds exactly when $c_j$ equals the XOR of the $c_k$, and Lemma 1 gives the LLR of that XOR. $\square$

**Theorem.** Let $G$ be a forest, and let $D$ be the largest number of check nodes on a path in $G$. Run lines L1 to L8 for $t \ge D$ iterations with `early_stop` off. Then the vector of line L4 is the exact posterior LLR $L(c_j)$ of every bit.

*Proof.* For a directed edge $i \to j$, let $d(i \to j)$ be the largest number of check nodes on a path in $T_{i \to j}$ that starts at $i$. Then $d(i \to j) \le D$, and $d(i' \to k) \le d(i \to j) - 1$ for every check $i'$ below $i$ in $T_{i \to j}$, that is $i' \in M(k) \setminus i$ for some $k \in N(i) \setminus j$.

*Claim: in every iteration $s \ge d(i \to j)$, line L3 sets the message on $i \to j$ to $\nu_{i \to j}$.* Induction on $d(i \to j)$.

If $d(i \to j) = 1$, every $k \in N(i) \setminus j$ has no check other than $i$, so $\mu_{k \to i} = L_k$. In iteration 1 the variable to check messages are $L_k$ (line L1). In a later iteration they are $\text{post}_k - \text{c2v}(i, k) = L_k + \sum_{i' \in M(k) \setminus i} \text{c2v}(i', k) = L_k$ (lines L4 and L7), since the sum is empty. Line L3 is then the formula of Lemma 2 for $\nu_{i \to j}$.

If $d(i \to j) = d > 1$ and $s \ge d$: the message from $k \in N(i) \setminus j$ that line L3 uses in iteration $s$ was formed by line L7 in iteration $s - 1 \ge d - 1$, and it is $L_k + \sum_{i' \in M(k) \setminus i} \text{c2v}(i', k)$ with the messages of iteration $s - 1$. Each $i'$ here has $d(i' \to k) \le d - 1 \le s - 1$, so by the induction hypothesis $\text{c2v}(i', k) = \nu_{i' \to k}$, and the message is $\mu_{k \to i}$ by Lemma 2. Line L3 then gives $\nu_{i \to j}$.

With $t \ge D$ every check to variable message is exact in iteration $t$, and line L4 computes $L_j + \sum_{i \in M(j)} \nu_{i \to j} = L(c_j)$ by Lemma 2. $\blacksquare$

**Remarks.**

- *Early stop.* Line L6 returns only when the hard decisions satisfy every check, so a returned word with flag true is always a codeword. On a tree it may return before the posteriors are exact; the decision is then a codeword, but not necessarily the bitwise MAP decision.
- *Clipping.* The implementation clips the product of line L3 to $\pm(1 - 10^{-15})$, so messages larger than about 35 in size are cut. The theorem holds for the implementation whenever no product reaches the clip.
- *Cycles.* With cycles, $T_{i \to j}$ is not defined, the incoming messages of a node are not independent, and the result is not exact in general. The page gives an example on the Hamming code, whose Tanner graph has girth 4. If the graph has girth $g$, the first $\lfloor (g - 2)/4 \rfloor$ iterations see only trees around each node, and in that range each message equals the exact message of the tree that the node sees to that depth.
