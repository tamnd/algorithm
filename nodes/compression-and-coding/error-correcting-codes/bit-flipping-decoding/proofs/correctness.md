---
title: Bit flipping returns only codewords and corrects a single error in one round, and the density evolution recursion of Gallager's algorithm A is exact on a tree and monotone
proves: [correctness]
status: full
---

**Setting.** $H$ is an $m \times n$ binary matrix with Tanner graph $G$, $N(i)$ is the set of variables of check $i$, and $M(j)$ the set of checks of variable $j$. The received word is $r \in \{0, 1\}^n$. For a word $c$, check $i$ is *unsatisfied* when $\sum_{j \in N(i)} c_j$ is odd, and $u_j(c)$ is the number of unsatisfied checks in $M(j)$.

**Lemma 1 (the output).** Lines L1 to L7 stop after at most $I$ rounds of flips. If they return success, the word is a codeword. If $r$ is a codeword, they return $r$ with no flip.

*Proof.* Each pass of the loop either returns at line L3, or flips at line L6 and adds one to the round count; the loop has at most $I + 1$ passes. Line L3 returns success only when every check is satisfied, that is $H c^T = 0$. If $r \in C$, the syndrome of line L2 is zero in the first pass. $\square$

So a decoder with flag success never outputs a non-codeword. It can output a wrong codeword, as every decoder can.

**Lemma 2 (one error).** Let every column of $H$ have weight $\gamma \ge 2$, and let no two columns share more than one check, that is, $G$ has no 4-cycle. If $r = c + e_j$ for a codeword $c$ and a single error at $j$, one round of lines L2 to L6 flips only bit $j$, and the decoder returns $c$.

*Proof.* The syndrome of $r$ is $H e_j^T$, the column $j$, so the unsatisfied checks are exactly $M(j)$, and $u_j = \gamma$. Any other bit $k$ has $u_k = |M(k) \cap M(j)| \le 1 < \gamma$. So the largest count is $\gamma$, and only bit $j$ has it. After the flip the word is $c$, and the next pass returns it at line L3. $\square$

The tests check this, and also check by exhaustive search that all $\binom{49}{2}$ double errors are corrected on the array code of the page. For double errors the counts can tie, so a round can flip correct bits; the example on the page shows a case where they are flipped back in the next round. No general bound on the number of corrected errors follows from the counts alone. The [expander code](/expander-codes/) theorem of Sipser and Spielman gives one when the graph expands well.

**Lemma 3 (weighted flipping with equal reliabilities).** In the weighted rule, check $i$ has weight $w_i = \min_{j \in N(i)} |y_j|$ and bit $j$ has the score $E_j = \sum_{i \in M(j)} (2 s_i - 1) w_i$, where $s_i$ is 1 for an unsatisfied check. If all $|y_j|$ are equal to $a > 0$ and all columns have weight $\gamma$, then $E_j = a (2 u_j - \gamma)$, so the weighted rule flips one bit with the largest count $u_j$.

*Proof.* Every $w_i = a$, so $E_j = a \sum_{i \in M(j)} (2 s_i - 1) = a (2 u_j - \gamma)$, which is increasing in $u_j$. $\square$

So without reliability information, weighted flipping is a one-bit-at-a-time form of plain flipping, and it chooses the first index on a tie. With unequal $|y_j|$, a check whose weakest bit is weak has a small weight, and its vote counts less.

**Gallager's algorithm A.** Messages are bits. A check sends to each of its variables the XOR of the messages from its other variables. A variable $j$ of degree $d_v$ sends to check $i$ the complement of $r_j$ if all the $d_v - 1$ other checks sent the complement of $r_j$, and $r_j$ otherwise. Algorithm B with threshold $b$ sends the complement when at least $b$ of the other checks sent it. With $b = d_v - 1$ the two rules are the same, which is how the implementation defines A.

Fix the $(d_v, d_c)$-regular ensemble on BSC($p$), and assume the depth-$2t$ neighborhood of an edge is a tree. Let $x_t$ be the probability that a variable to check message in round $t$ is wrong, with $x_0 = p$.

**Lemma 4 (the recursion).** On a tree,

$$x_{t+1} = p - p \, g_t^{\,d_v - 1} + (1 - p) (1 - g_t)^{d_v - 1}, \qquad g_t = \frac{1 + (1 - 2 x_t)^{d_c - 1}}{2}.$$

*Proof.* By the symmetry of the channel and of the rules, the error probability does not depend on the codeword sent, so take the all-zero word. On a tree, the $d_c - 1$ messages that enter a check from below come from disjoint subtrees, so they are independent, each wrong with probability $x_t$. The check message is right when an even number of them is wrong. For independent bits that are 1 with probability $x$, $P(\text{even}) - P(\text{odd}) = (1 - 2x)^{d_c - 1}$, as in the tanh rule, so the check message is right with probability $g_t$. The $d_v - 1$ check messages that enter a variable from below are again independent, and independent of its channel bit. If the channel bit is wrong (probability $p$), the outgoing message is right only when all $d_v - 1$ check messages say so, with probability $g_t^{d_v - 1}$. If the channel bit is right (probability $1 - p$), the outgoing message is wrong only when all of them are wrong, with probability $(1 - g_t)^{d_v - 1}$. Adding the two cases gives the formula. $\square$

For algorithm B the same argument gives, with $\binom{\cdot}{\cdot}$ for the number of ways to choose the agreeing checks,

$$x_{t+1} = p - p \sum_{k = b}^{d_v - 1} \binom{d_v - 1}{k} g_t^{k} (1 - g_t)^{d_v - 1 - k} + (1 - p) \sum_{k = b}^{d_v - 1} \binom{d_v - 1}{k} (1 - g_t)^{k} g_t^{d_v - 1 - k},$$

which is the formula of Lemma 4 when $b = d_v - 1$. The tests check this equality numerically.

**Lemma 5 (monotonicity).** Write $x_{t+1} = f(x_t, p)$. Then $f$ is nondecreasing in $x$ on $[0, 1/2]$ and nondecreasing in $p$, so $x_t(p)$ is nondecreasing in $p$ for every $t$. The set of $p$ for which $x_t \to 0$ is therefore an interval that starts at 0, and its supremum is the threshold.

*Proof.* Let $p \le 1/2$. First, the recursion stays in $[0, 1/2]$: if $x \le 1/2$ then $g \ge 1/2$, and $f$ is an average of $1 - g^{d_v - 1}$ and $(1 - g)^{d_v - 1}$ with the weight $p \le 1/2$ on the larger one, $1 - g^{d_v - 1} \ge (1 - g)^{d_v - 1}$, so $f \le \tfrac12 (1 - g^{d_v - 1} + (1 - g)^{d_v - 1}) \le \tfrac12$. On $[0, 1/2]$, $g = (1 + (1 - 2x)^{d_c - 1})/2$ is nonincreasing in $x$, and $f$ is nonincreasing in $g$, since $-p g^{d_v - 1}$ and $(1 - p)(1 - g)^{d_v - 1}$ both decrease as $g$ grows. So $f$ is nondecreasing in $x$. For fixed $x$, $\partial f / \partial p = 1 - g^{d_v - 1} - (1 - g)^{d_v - 1} \ge 1 - g - (1 - g) = 0$, since $0 \le g \le 1$ and $d_v - 1 \ge 1$. Then $x_0 = p$ is nondecreasing in $p$, and if $x_t$ is, so is $x_{t+1} = f(x_t, p)$. If $x_t(p) \to 0$ and $p' < p$, then $0 \le x_t(p') \le x_t(p)$, so $x_t(p') \to 0$. $\square$

Lemma 5 is what makes the bisection of `gallager_a_threshold` correct: below the threshold the recursion goes to 0, and above it, it does not.
