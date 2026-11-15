---
title: Probabilistic interleaving has a posterior that factorizes by position, and its marginalized outcome is unbiased
proves: [correctness]
status: full
---

Let $A$ and $B$ be orderings of the same set $D$ of $n$ documents, and let $\tau > 0$. Lines refer to the pseudocode on the page. For a ranking $x \in \{1, 2\}$ (1 for $A$, 2 for $B$) and a document $d$ at rank $r_x(d)$, from 1, let $w_x(d) = r_x(d)^{-\tau}$, and for a set $R \subseteq D$ let $Z_x(R) = \sum_{e \in R} w_x(e)$. All weights are positive.

**Claim 1 (the sampler).** INTERLEAVE returns an ordering $L$ of $D$ and an assignment $a \in \{1, 2\}^n$ with

$$\Pr[L, a] = 2^{-n} \prod_{r=1}^{n} \frac{w_{a_r}(L_r)}{Z_{a_r}(R_r)}, \qquad R_r = D \setminus \{L_1, \ldots, L_{r-1}\}.$$

*Proof.* Before the test of line L3 for position $r$, the list of remaining documents holds $R_r$, because line L5 removes each drawn document and line L6 appends it to $L$. So the loop runs $n$ times and $L$ is an ordering of $D$. At position $r$, line L4 gives $a_r = x$ with probability $1/2$, independent of all earlier draws. The roulette draw takes $u$ uniform in $[0, Z_x(R_r))$ and returns the first remaining document whose prefix sum of weights exceeds $u$, so it returns $d \in R_r$ with probability $w_x(d) / Z_x(R_r)$. The product of these conditional probabilities is the formula. $\square$

Note that $R_r$ depends only on $L$, not on $a$. Write $f_x(r) = w_x(L_r) / Z_x(R_r)$, so $\Pr[L, a] = 2^{-n} \prod_r f_{a_r}(r)$.

**Claim 2 (the posterior factorizes).** Given $L$, the components of $a$ are independent, and $\Pr[a_r = 1 \mid L] = q_r = f_1(r) / (f_1(r) + f_2(r))$.

*Proof.* Summing the product over all $a$ gives $\Pr[L] = 2^{-n} \prod_r (f_1(r) + f_2(r))$, because the sum over $a$ of a product of one factor per position is the product of the sums. Every factor is positive, so $\Pr[L] > 0$ for every ordering $L$, and

$$\Pr[a \mid L] = \prod_{r=1}^{n} \frac{f_{a_r}(r)}{f_1(r) + f_2(r)},$$

which is a product of one Bernoulli term per position with parameter $q_r$. $\square$

Function POSTERIOR computes $Z_x(R_r)$ as the suffix sum $\sum_{s \ge r} w_x(L_s)$, which is the same set, and then $q_r$ in line L10.

**Claim 3 (the dynamic program).** For a set $C$ of clicked positions, MARGINAL returns $m(L, C) = \sum_a \Pr[a \mid L] \, o(a, C)$, where $o(a, C)$ is the outcome of lines L8 and L9.

*Proof.* The outcome $o(a, C)$ is the sign of $\Delta = \sum_{r \in C} s_r$, with $s_r = +1$ if $a_r = 1$ and $s_r = -1$ otherwise, so it depends only on the components $a_r$ with $r \in C$. By Claim 2 these are independent with $\Pr[s_r = 1] = q_r$. After the loop of line L12 has processed the first $j$ clicked positions, the table holds the exact distribution of the sum of their $s_r$: this is true for $j = 0$ (the sum is 0 with probability 1), and each step convolves the table with the two values of the next independent $s_r$. After all of $C$, line L13 returns $\Pr[\Delta > 0] - \Pr[\Delta < 0] = \mathbb{E}[\operatorname{sign} \Delta \mid L] = m(L, C)$. $\square$

**Claim 4 (unbiased).** Let the clicks $C$ be drawn from any distribution $\Pr[C \mid L]$ that depends on the shown list but not on $a$. Then $\mathbb{E}[m(L, C)] = \mathbb{E}[o(a, C)]$.

*Proof.* As $C$ and $a$ are independent given $L$, $\Pr[a \mid L, C] = \Pr[a \mid L]$, so $\mathbb{E}[o(a, C) \mid L, C] = m(L, C)$ by Claim 3. Taking the expectation of both sides over $(L, C)$ gives the claim. $\square$

The hypothesis holds for every click model in which the user sees only the page: the assignment is not shown. So the marginalized outcome has the same expected value as the outcome of the sampled assignment, and it has no larger variance, because it is a conditional expectation of it.

**Claim 5 (no preference under random clicks).** If $C$ is drawn from a distribution on positions that is independent of $(L, a)$, then $\mathbb{E}[o(a, C)] = 0$ and $\mathbb{E}[m(L, C)] = 0$.

*Proof.* By line L4 each $a_r$ is a fair coin drawn independently of everything before it, so the marginal distribution of $a$ is uniform on $\{1, 2\}^n$. Let $\bar{a}$ swap 1 and 2 in every component. This map is a bijection that keeps the uniform distribution, and $o(\bar{a}, C) = -o(a, C)$ for every $C$, since it swaps the two counts. So for each fixed $C$, $\sum_a 2^{-n} o(a, C) = 0$, and averaging over the independent $C$ gives $\mathbb{E}[o(a, C)] = 0$. The second equality follows by Claim 4. $\square$

**Cost.** INTERLEAVE makes $n$ draws, and each scans the remaining documents, so it takes $O(n^2)$ time; a balanced tree of weights would make each draw $O(\log n)$. POSTERIOR makes two passes over $L$, $O(n)$ time. In MARGINAL, after $j$ clicks the table has at most $j + 1$ keys, so the loop costs $O(c^2)$ for $c = |C|$, and sorting $C$ costs $O(c \log c)$. With POSTERIOR the total is $O(n + c^2)$, against $2^n$ terms for the plain sum over assignments. $\blacksquare$
