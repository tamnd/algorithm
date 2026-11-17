---
title: The recalibrated quality is a product of bin error rates, and it is exact for independent effects
proves: [correctness]
status: full
---

Fix one read group $g$. The training data are base observations $(q, c, x, \mu)$: reported quality $q$, cycle $c$, context $x$ (or none for the first base of a read) and $\mu = 1$ for a mismatch with the reference, else 0. For a bin $B$, a set of observations given by fixed values of some of $q, c, x$, let $m_B$ and $n_B$ be its numbers of mismatches and of observations, and define

$$\hat p_B = \frac{m_B + 1}{n_B + 2}, \qquad \hat Q_B = -10 \log_{10} \hat p_B.$$

The bins are $G$ (all observations of $g$), $(q)$, $(q, c)$ and $(q, x)$.

**Lemma 1 (counts).** After lines L1 to L4, the table holds $m_B$ and $n_B$ for every bin with $n_B \ge 1$, and `qsum` holds $\sum_{o \in G} 10^{-q_o/10}$.

*Proof.* Line L3 adds each observation to its four bins, and only to those: one count to $n_B$, and $\mu$ to $m_B$. Line L4 adds its reported error probability to the group sum. Observations with no context are not added to any context bin, and only those bins are skipped. $\square$

**Lemma 2 (telescoping).** For an observation whose bins $(q)$, $(q, c)$ and $(q, x)$ are all non-empty in the training data,

$$Q_{\mathrm{recal}} = \hat Q_{(q, c)} + \hat Q_{(q, x)} - \hat Q_{(q)}, \qquad \text{that is,} \qquad 10^{-Q_{\mathrm{recal}}/10} = \frac{\hat p_{(q, c)}\, \hat p_{(q, x)}}{\hat p_{(q)}}.$$

Without a context, $Q_{\mathrm{recal}} = \hat Q_{(q, c)}$.

*Proof.* Write $d_0, d_1, d_c, d_x$ for the values of lines L5 to L7. By their definitions, $d_1 = \hat Q_{(q)} - (q + d_0)$, so $q + d_0 + d_1 = \hat Q_{(q)}$. Then $d_c = \hat Q_{(q, c)} - \hat Q_{(q)}$ and $d_x = \hat Q_{(q, x)} - \hat Q_{(q)}$. Line L8 returns $q + d_0 + d_1 + d_c + d_x$, which is the sum in the claim. Without a context, $d_x$ is not added. The second form takes $10^{-\cdot / 10}$ of both sides. $\square$

So in this plain version the global shift $d_0$ matters only for a base whose $(q)$ bin is empty in the training data. An empty $(q, c)$ or $(q, x)$ bin adds nothing, and the code falls back to the levels above. In GATK, each level is estimated with a prior centered on the level above, so the levels do not cancel in this way.

**Theorem (consistency).** Suppose that within the bin $(q)$ the true error probability of a base with cycle $c$ and context $x$ is $p_q\, \alpha_c\, \beta_x$, that the cycle and the context of a base are independent, and that every observation has a context. Let the number of training observations grow while the shares of the cycles and contexts stay fixed, and the observations stay independent given their covariates. Then $10^{-Q_{\mathrm{recal}}/10}$ tends to $p_q \alpha_c \beta_x$ with probability 1 for every cycle and context with positive share.

*Proof.* Write $\bar\alpha = E[\alpha_C]$ and $\bar\beta = E[\beta_X]$ for the means over the cycles and contexts of the bin $(q)$. The mismatch indicators of a bin are independent, with mean equal to the mean error probability of the bin. By the strong law of large numbers, $\hat p_B$ tends to that mean, because the pseudo-counts $1$ and $2$ become negligible as $n_B \to \infty$. By independence of cycle and context, the three means are

$$p_{(q, c)} = p_q \alpha_c \bar\beta, \qquad p_{(q, x)} = p_q \bar\alpha \beta_x, \qquad p_{(q)} = p_q \bar\alpha \bar\beta.$$

By Lemma 2 and the continuity of the product and the quotient, the limit of $10^{-Q_{\mathrm{recal}}/10}$ is $p_q \alpha_c \bar\beta \cdot p_q \bar\alpha \beta_x / (p_q \bar\alpha \bar\beta) = p_q \alpha_c \beta_x$. $\square$

The hypotheses matter. If the effect of the cycle depends on the context, the model can only reach the product of the two marginal effects. If the cycle and the context are dependent, the marginal means no longer split as above. If the training sites contain true variants that are not masked, the mismatch counts include real differences, and the recalibrated qualities come out too low.

**Rounding.** `recalibrate_read` rounds $Q_{\mathrm{recal}}$ to the nearest integer and clamps it to the range 1 to 93, the largest value that Phred+33 can print as one ASCII character. Rounding moves the quality by at most $1/2$, which changes the error probability by a factor of at most $10^{0.05} \approx 1.12$.

**Cost.** Fitting costs $O(1)$ expected time per observation with hash tables, so $O(n)$ for $n$ observations, and the tables have one entry per non-empty bin. Each recalibrated base costs $O(1)$ expected time.
