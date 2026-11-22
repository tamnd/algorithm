---
title: DPA returns the first top-scoring guess, and it finds the key in the Hamming weight model
proves: [correctness]
status: full
---

We write $s(g)$ for the score that lines L6 to L8 give to the guess $g$, and $n = |S|$ for the number of guesses.

**Lemma 1 (the loop of line L2).** After the iteration for guess $g$, the value top is $\max_{h \le g} s(h)$, and best is the smallest $h \le g$ with $s(h) = $ top, or none if all these scores are $-\infty$.

*Proof.* By induction on $g$. Before the loop, line L1 sets best to none and top to $-\infty$, which is the claim for the empty set of guesses. In the iteration for $g$, line L9 compares $s(g)$ with the old top, which by the induction hypothesis is $\max_{h < g} s(h)$. If $s(g)$ is larger, line L10 makes $g$ the best guess and $s(g)$ the top, and $g$ is then the only guess with the top score among $0 \ldots g$. If $s(g)$ is not larger, nothing changes: the maximum is the same, and the smallest guess that reaches it is still the old best, because $g$ is larger than it. A score of $-\infty$ is never larger than top, so best stays none while all scores are $-\infty$. $\square$

So line L11 returns the first argmax of the scores, and the list of all $n$ scores.

**The model.** Let $k$ be the key. The inputs $p_1, p_2, \ldots$ are independent and uniform on $\{0, \ldots, 15\}$. At the leaking sample $j^\ast$, $\ell_i[j^\ast] = \varepsilon \cdot \mathrm{HW}(S(p_i \oplus k)) + N_{ij^\ast}$, and at every other sample $\ell_i[j] = N_{ij}$, with all $N_{ij}$ independent of each other and of the inputs, with mean 0 and finite variance. For a fixed bit $b$ and $\delta \in \{0, \ldots, 15\}$ define, for $X$ uniform,

$$D_b(\delta) = E[\mathrm{HW}(S(X)) \mid \text{bit } b \text{ of } S(X \oplus \delta) = 1] - E[\mathrm{HW}(S(X)) \mid \text{bit } b \text{ of } S(X \oplus \delta) = 0].$$

Both conditions have probability $1/2$, because $S$ is a bijection, so $S(X \oplus \delta)$ is uniform and each of its bits is 1 for exactly 8 of the 16 values of $X$.

**Lemma 2 (the limit of a score).** Fix a guess $g$ and put $\delta = g \oplus k$. With probability 1, as $m \to \infty$, the differential trace of line L7 converges to $\varepsilon D_b(\delta)$ at the sample $j^\ast$ and to 0 at every other sample. So $s(g)$ converges to $\varepsilon D_b(\delta)$ if $T = 1$, and to $\max(\varepsilon D_b(\delta), 0)$ if $T \ge 2$.

*Proof.* Let $c_i = 1$ if bit $b$ of $S(p_i \oplus g)$ is 1, and $c_i = 0$ if not. The pairs $(c_i, \ell_i)$ are independent and identically distributed. By the strong [law of large numbers](/law-of-large-numbers/), with probability 1,

$$\frac{1}{m}\sum_{i \le m} c_i \to \tfrac12, \qquad \frac{1}{m}\sum_{i \le m} c_i \, \ell_i[j] \to E[c_1 \ell_1[j]].$$

In particular both groups are not empty for all large $m$, so line L6 does not apply, and the mean of group G1 at sample $j$ converges to $E[c_1 \ell_1[j]] / \tfrac12 = E[\ell_1[j] \mid c_1 = 1]$. The same holds for group G0 with $1 - c_i$. For $j \ne j^\ast$, $\ell_1[j] = N_{1j}$ is independent of $c_1$ and has mean 0, so both group means tend to 0 and so does their difference. For $j = j^\ast$, the noise term again has conditional mean 0, and

$$E[\ell_1[j^\ast] \mid c_1 = 1] = \varepsilon \, E[\mathrm{HW}(S(p_1 \oplus k)) \mid \text{bit } b \text{ of } S(p_1 \oplus g) = 1].$$

Put $X = p_1 \oplus k$, which is uniform. Then $p_1 \oplus g = X \oplus \delta$, and the difference of the two group means tends to $\varepsilon D_b(\delta)$. Line L8 takes the maximum of finitely many values, and the maximum is continuous, so $s(g)$ converges to the maximum of the limits. $\square$

**Lemma 3 (the right guess).** $D_b(0) = 1$ for every bit $b$.

*Proof.* Put $Y = S(X)$. It is uniform on 4 bits, so its bits $Y_0, \ldots, Y_3$ are independent and each is uniform on $\{0, 1\}$. Then $\mathrm{HW}(Y) = \sum_c Y_c$. Under the condition $Y_b = 1$ the term $Y_b$ is 1, and under $Y_b = 0$ it is 0. Each other term $Y_c$ is independent of $Y_b$, so its conditional mean is $1/2$ under both conditions. The difference is $1 + 0 = 1$. $\square$

**Lemma 4 (the wrong guesses on bit 1).** For the PRESENT S-box $S = (\texttt{C}, 5, 6, \texttt{B}, 9, 0, \texttt{A}, \texttt{D}, 3, \texttt{E}, \texttt{F}, 8, 4, 7, 1, 2)$ and $b = 1$, the values $D_1(\delta)$ for $\delta = 0, 1, \ldots, 15$ are

$$1,\ 0,\ 0.25,\ -0.5,\ 0,\ 0.75,\ -1.25,\ -0.25,\ -0.25,\ 0.25,\ 0,\ 0.75,\ -0.25,\ -1,\ 0.5,\ 0 .$$

So $D_1(\delta) \le 0.75$ for every $\delta \ne 0$.

*Proof.* Each value is a finite sum over the 16 values of $X$: list the 8 values of $X$ with bit 1 of $S(X \oplus \delta)$ equal to 1, average $\mathrm{HW}(S(X))$ over them, and subtract the average over the other 8. For example, for $\delta = 5$ the first set is $\{3, 6, 7, 8, 10, 12, 13, 15\}$ with Hamming weights $3, 2, 3, 2, 4, 1, 3, 1$ of $S(X)$, mean $19/8$, and the other set has mean $13/8$, so $D_1(5) = 6/8 = 0.75$. The test file computes all 16 values in the same way and compares them with the scores of the code on noiseless balanced traces, for every key. $\square$

**Theorem (consistency).** In the model, with $b = 1$ and the PRESENT S-box, the probability that line L11 returns best $= k$ tends to 1 as $m \to \infty$.

*Proof.* By Lemma 2 and Lemma 3, $s(k) \to \varepsilon$ with probability 1 (for $T \ge 2$ the limit is $\max(\varepsilon, 0) = \varepsilon$, since $\varepsilon > 0$). By Lemma 2 and Lemma 4, for each $g \ne k$, $s(g)$ converges to a value of at most $\max(0.75\varepsilon, 0) = 0.75\varepsilon$. There are finitely many guesses, so with probability 1 there is an $M$ such that, for all $m \ge M$, $s(k) > 0.875\varepsilon > s(g)$ for every $g \ne k$. For these $m$ the key $k$ is the only guess with the top score, so by Lemma 1 line L11 returns $k$. Convergence with probability 1 implies convergence in probability, so the probability of success tends to 1. $\blacksquare$

**Remark.** The proof uses the sign of the score. With the absolute value in line L8, the limit for $g = k \oplus 6$ is $1.25\varepsilon > \varepsilon$ by Lemma 4, so the attack then fails with probability tending to 1. On bit 0 the value $D_0(\delta)$ equals 1 for $\delta \in \{7, 9, \texttt{E}\}$ as well as for $\delta = 0$, so the theorem does not hold for $b = 0$.
