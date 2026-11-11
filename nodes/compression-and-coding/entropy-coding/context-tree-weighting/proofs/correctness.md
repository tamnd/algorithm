---
title: The sequential updates of CTW compute the weighted probability, the decoder follows the encoder, and the code length is within the model cost and the parameter cost of every tree source of depth at most D
proves: [correctness, termination, length]
status: full
---

Notation. The input is $x_1 \ldots x_n \in \{0, 1\}^n$, and the $D$ bits before $x_1$ are zeros. A node is a string $s$ of at most $D$ bits, read from the most recent bit back; the context of depth $d$ of $x_t$ is $x_{t-1} \ldots x_{t-d}$, and the children of $s$ are $s0$ and $s1$. After $t$ bits, $a_s$ and $b_s$ count the zeros and ones among the bits $x_u$, $u \le t$, whose context starts with $s$. The KT block probability is

$$P_e(a, b) = \frac{\prod_{i<a}(i + \tfrac12) \prod_{j<b}(j + \tfrac12)}{\prod_{k<a+b}(k + 1)},$$

and the weighted probability is $P_w(s) = P_e(a_s, b_s)$ if $s$ has length $D$, and $P_w(s) = \tfrac12 P_e(a_s, b_s) + \tfrac12 P_w(s0) P_w(s1)$ otherwise. A node that no context has reached has $a_s = b_s = 0$ and $P_e = P_w = 1$, as line L1 sets.

**Lemma 1 (the updates keep the definition).** After lines L6 to L10 run for $x_t$, every node holds $a_s$, $b_s$, $P_e(a_s, b_s)$ and $P_w(s)$ for the counts after $t$ bits.

*Proof.* By induction on $t$. The bit $x_t$ changes the counts only of the $D + 1$ nodes on its path, the prefixes of its context. For such a node, $P_e(a + 1, b) = P_e(a, b) \cdot (a + \tfrac12)/(a + b + 1)$ and $P_e(a, b + 1) = P_e(a, b) \cdot (b + \tfrac12)/(a + b + 1)$ by the product formula, which is line L7. The loop runs from depth $D$ to the root, so when it reaches a node of depth $d < D$, the child on the path is already updated, and the other child is not on the path and has not changed. Lines L9 and L10 then apply the definition. Nodes off the path keep their counts and values, and their $P_w$ depends only on nodes below them, which are also off the path. $\square$

**Lemma 2 (the predictions are a distribution).** For every node $s$ on the path of $x_t$, let $P_w^x(s)$ be the value $P_w(s)$ would take if the next bit were $x$. Then $P_w^0(s) + P_w^1(s) = P_w(s)$.

*Proof.* By induction from depth $D$ up. The KT estimator satisfies $P_e(a + 1, b) + P_e(a, b + 1) = P_e(a, b) \cdot (a + b + 1)/(a + b + 1) = P_e(a, b)$. This proves the claim at depth $D$. At depth $d < D$, let $c$ be the child on the path and $c'$ the other child; then $P_w^0(s) + P_w^1(s) = \tfrac12 (P_e^0 + P_e^1) + \tfrac12 P_w(c') (P_w^0(c) + P_w^1(c)) = \tfrac12 P_e(s) + \tfrac12 P_w(c') P_w(c) = P_w(s)$. $\square$

So the value $p = q_1/(q_0 + q_1)$ of lines L3 and L4 is $P_w^1(\lambda)/P_w(\lambda)$, and $1 - p = P_w^0(\lambda)/P_w(\lambda)$. Both are positive, since every KT factor is positive. By Lemma 1, the product of the probabilities that CTW gives to $x_1, \ldots, x_n$ telescopes to the final $P_w(\lambda)$.

**Theorem 1 (correctness).** DECODE returns $x_1 \ldots x_n$.

*Proof.* Both sides start with the same empty tree and the same zero past. Suppose that before step $t$ the decoder has output $x_1 \ldots x_{t-1}$ and has the same tree as the encoder. Then it computes the same $p$, with the same floating-point operations in the same order, and the same 16-bit count $c_1 \in [1, 2^{16} - 1]$. After each renormalization the coder width $r$ is above $2^{30}$, so both sub-intervals have width at least $r \cdot 2^{-16} - 1 > 0$. By the correctness of the integer arithmetic coder (the [arithmetic coding](/arithmetic-coding/) page), the decoder gets back $x_t$ and makes the same change to its registers. Line L15 then makes the same update as the encoder. Induction on $t$ ends the proof. $\square$

**Theorem 2 (redundancy).** Let $\mathcal S$ be a set of nodes that forms the leaves of a full binary tree of depth at most $D$, and let $\theta_s \in [0, 1]$ for $s \in \mathcal S$. Let $P_a(x)$ be the probability of $x_1 \ldots x_n$ under the tree source that emits a 1 with probability $\theta_s$ in the leaf $s$ that the context ends in. Then

$$\lg \frac{1}{P_w(\lambda)} \le \lg \frac{1}{P_a(x)} + \Gamma_D(\mathcal S) + |\mathcal S| \, \gamma\!\left(\frac{n}{|\mathcal S|}\right),$$

where $\Gamma_D(\mathcal S) = 2|\mathcal S| - 1 - |\{s \in \mathcal S : |s| = D\}|$, $\gamma(z) = z$ for $0 \le z < 1$ and $\gamma(z) = \tfrac12 \lg z + 1$ for $z \ge 1$.

*Proof.* Step 1. For each node $s$ of depth below $D$, the definition gives $P_w(s) \ge \tfrac12 P_e(s)$ and $P_w(s) \ge \tfrac12 P_w(s0) P_w(s1)$. Apply the second bound at each inner node of the tree and the first at each leaf of depth below $D$; at a leaf of depth $D$, $P_w = P_e$. The tree has $|\mathcal S| - 1$ inner nodes, so

$$P_w(\lambda) \ge 2^{-\Gamma_D(\mathcal S)} \prod_{s \in \mathcal S} P_e(a_s, b_s).$$

Step 2. Every bit falls in exactly one leaf, so $P_a(x) = \prod_{s} (1 - \theta_s)^{a_s} \theta_s^{b_s}$, and $\sum_s (a_s + b_s) = n$. Willems, Shtarkov and Tjalkens prove that for $a + b \ge 1$, $P_e(a, b) \ge \frac{1}{2\sqrt{a + b}} \left(\frac{a}{a+b}\right)^a \left(\frac{b}{a+b}\right)^b$. The right side is at least $\frac{1}{2\sqrt{a+b}} (1 - \theta)^a \theta^b$ for every $\theta$, since the ML parameter maximizes $(1 - \theta)^a \theta^b$. So $\lg(1/P_e(a_s, b_s)) \le \lg(1/((1 - \theta_s)^{a_s} \theta_s^{b_s})) + \gamma(a_s + b_s)$; for $a_s + b_s = 0$ both sides are 0. (The test `test_kt_bound` checks the KT inequality for all $a + b < 150$.)

Step 3. The function $\gamma$ is concave on $[0, \infty)$: it is linear on $[0, 1]$, concave on $[1, \infty)$, continuous at 1, and its slope falls at 1 from 1 to $1/(2 \ln 2) < 1$. By Jensen's inequality, $\sum_s \gamma(a_s + b_s) \le |\mathcal S| \, \gamma(n / |\mathcal S|)$. Adding the three steps gives the claim. $\square$

Since the bound holds for every $\theta$, it holds for the ML parameters of $\mathcal S$, which give the shortest code that any tree source with the leaves $\mathcal S$ gives to $x$. The proof of Step 1 also shows that $\lg(1/P_w(\lambda))$ is at most the minimum, over all trees, of the bits that describe the tree plus $\sum_s \lg(1/P_e(s))$; the function `best_tree_cost` computes this minimum.

**Theorem 3 (code length).** Let $\hat p_t$ be the quantized probability that the coder gives to $x_t$. The output has at most $\sum_t \lg(1/\hat p_t) + n \lg \frac{1}{1 - 2^{-14}} + 2$ bits before the padding to a byte.

*Proof.* The width before an event is above $2^{30}$ and $\hat p_t \ge 2^{-16}$, so the new width is at least $r \hat p_t - 1 \ge r \hat p_t (1 - 2^{-14})$. Each renormalization step doubles the width, which stays at most $2^{32}$, and adds one bit; the final step adds 2 bits. $\square$

With the exact $p$ in place of $\hat p_t$, the first term is $\lg(1/P_w(\lambda))$ and the bound of Theorem 2 gets the $+2$ of the coder, as in the theorem of Willems, Shtarkov and Tjalkens. Rounding $p$ to 16 bits adds a small cost per bit, which is large only when $p$ is within about $2^{-16}$ of 0 or 1.

**Termination.** Each step visits the $D + 1$ nodes of one path three times (twice for the two predictions and once for the update), and each renormalization loop ends because the width doubles at each pass. So encoding and decoding take $O(n D)$ steps. $\blacksquare$
