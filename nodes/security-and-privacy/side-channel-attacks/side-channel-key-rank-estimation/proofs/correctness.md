---
title: The histogram bounds always contain the rank of the true key
proves: [correctness]
status: full
---

Fix $d \ge 1$ parts, scores $s_i(x)$ for $x$ in a finite nonempty set $X_i$, a true key $k^\ast = (k^\ast_1, \ldots, k^\ast_d)$ and a width $w > 0$. Arithmetic is exact. Write $S(x) = \sum_i s_i(x_i)$ for a full key $x \in X_1 \times \cdots \times X_d$ and $\mathrm{rank}(k^\ast) = 1 + \#\{x : S(x) > S(k^\ast)\}$.

**Lemma 1 (line L2).** Shifting part $i$ by a constant $c_i$ does not change the rank.

*Proof.* Every full key gets the same added total $c = \sum_i c_i$, so $S(x) > S(k^\ast)$ if and only if $S(x) + c > S(k^\ast) + c$. $\square$

From now on the scores are the shifted ones, so $s_i(x) \ge 0$ and every bin index $b_i(x) = \lfloor s_i(x)/w \rfloor$ is a non-negative integer. Write $B(x) = \sum_i b_i(x_i)$ and $b^\ast = B(k^\ast)$, which is the value of line L7.

**Lemma 2 (the bin inequality).** For every full key $x$, $w B(x) \le S(x) < w (B(x) + d)$.

*Proof.* For a real $t$ and $b = \lfloor t \rfloor$, we have $b \le t < b + 1$. With $t = s_i(x_i)/w$ and $w > 0$ this gives $w b_i(x_i) \le s_i(x_i) < w(b_i(x_i) + 1)$. Add the $d$ inequalities. $\square$

**Lemma 3 (lines L5 and L6).** After the convolutions of line L6, $H[b] = \#\{x : B(x) = b\}$ for every integer $b \ge 0$.

*Proof.* By line L3, $H_i[b] = \#\{y \in X_i : b_i(y) = b\}$. Let $G_j$ be the value of $H$ after the parts $1, \ldots, j$, and claim $G_j[b] = \#\{(x_1, \ldots, x_j) : \sum_{i \le j} b_i(x_i) = b\}$. For $j = 1$ this is line L5. For the step, split the keys of the first $j + 1$ parts by the bin $c$ of the last part. The number with total $b$ is $\sum_c G_j[b - c] \, H_{j+1}[c]$, which is the convolution $(G_j \ast H_{j+1})[b]$. The claim for $j = d$ is the lemma. $\square$

**Theorem.** The values of lines L7 and L8 satisfy $\mathrm{lo} \le \mathrm{rank}(k^\ast) \le \mathrm{up}$.

*Proof.* By Lemma 3, $\mathrm{lo} = 1 + \#\{x : B(x) \ge b^\ast + d\}$ and $\mathrm{up} = \#\{x : B(x) \ge b^\ast - d + 1\}$.

Lower bound. Let $B(x) \ge b^\ast + d$. By Lemma 2 for $x$ and for $k^\ast$,

$$S(x) \ge w B(x) \ge w (b^\ast + d) > S(k^\ast).$$

So every key counted by lo, apart from the 1, is strictly better than $k^\ast$, and $\mathrm{lo} \le \mathrm{rank}(k^\ast)$.

Upper bound. Let $S(x) > S(k^\ast)$. By Lemma 2,

$$w (B(x) + d) > S(x) > S(k^\ast) \ge w b^\ast,$$

so $B(x) + d > b^\ast$, and because both sides are integers, $B(x) \ge b^\ast - d + 1$. So every strictly better key is in the set of up. The true key is in that set too, because $d \ge 1$ gives $b^\ast \ge b^\ast - d + 1$, and it is not strictly better than itself. The two sets are disjoint, so $\mathrm{up} \ge \#\{x : S(x) > S(k^\ast)\} + 1 = \mathrm{rank}(k^\ast)$. $\square$

**Proposition (fine bins).** Let $\gamma > 0$ be the smallest gap between two distinct values of $S$, and let $(2d - 1) w < \gamma$. Then $\mathrm{lo} = \mathrm{rank}(k^\ast)$. If, in addition, no key other than $k^\ast$ has $S(x) = S(k^\ast)$, then $\mathrm{up} = \mathrm{rank}(k^\ast)$.

*Proof.* Take a key $x$ with $b^\ast - d + 1 \le B(x) \le b^\ast + d - 1$, the band between the two sets. By Lemma 2,

$$S(x) - S(k^\ast) < w(B(x) + d) - w b^\ast \le w (2d - 1),$$
$$S(k^\ast) - S(x) < w(b^\ast + d) - w B(x) \le w (2d - 1).$$

So $|S(x) - S(k^\ast)| < (2d - 1)w < \gamma$, and so $S(x) = S(k^\ast)$. Hence no key in the band is strictly better than $k^\ast$. Every strictly better key has $B(x) \ge b^\ast - d + 1$ by the theorem, and it is not in the band, so $B(x) \ge b^\ast + d$. With the lower bound of the theorem, the strictly better keys are exactly the keys with $B(x) \ge b^\ast + d$, and $\mathrm{lo} = \mathrm{rank}(k^\ast)$. If no other key ties with $k^\ast$, the only key in the band is $k^\ast$ itself, so $\mathrm{up} = \mathrm{lo}$. $\blacksquare$

With floating point scores, Lemma 2 can fail for a score that is rounded across a bin edge, and the theorem then holds only up to the keys in the two bins at that edge. The tests use exact fractions to check the theorem and floating point scores from a continuous model, for which such a rounding is very unlikely.
