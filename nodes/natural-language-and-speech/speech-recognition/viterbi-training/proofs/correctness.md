---
title: Viterbi training never lowers the best-path likelihood and stops
proves: [correctness]
status: full
---

We use the notation of the page: a discrete HMM $\lambda = (\pi, A, B)$ with $N$ states and $M$ symbols, and training sequences $O^1, \ldots, O^R$. All logs are natural logs, and $\log 0 = -\infty$. For a tuple of state paths $\mathbf{Q} = (Q^1, \ldots, Q^R)$, one path per sequence, write

$$G(\lambda; \mathbf{Q}) = \sum_{r=1}^{R} \log P(O^r, Q^r \mid \lambda), \qquad F(\lambda) = \sum_{r=1}^{R} \max_{Q} \log P(O^r, Q \mid \lambda) = \max_{\mathbf{Q}} G(\lambda; \mathbf{Q}).$$

Round $k$ of the algorithm starts with the model $\lambda_k$. Lines L3 and L4 compute a tuple $\mathbf{Q}_k$ of Viterbi paths and $F_k = G(\lambda_k; \mathbf{Q}_k)$. The Viterbi algorithm returns a best path (see the viterbi-algorithm page), so $F_k = F(\lambda_k)$. If the round does not stop at line L5, lines L7 and L8 set $\lambda_{k+1}$ to the relative frequencies of the counts along $\mathbf{Q}_k$.

**Lemma 1 (the update step).** For a fixed tuple $\mathbf{Q}$, the relative frequencies of lines L7 and L8 maximize $G(\lambda; \mathbf{Q})$ over all models $\lambda$. A row with no counts may take any value without changing $G$.

*Proof.* Let $n_i$ be the number of paths that start in $i$, $n_{ij}$ the number of steps $i \to j$ and $c_{jk}$ the number of frames in state $j$ with the symbol $k$. Then

$$G(\lambda; \mathbf{Q}) = \sum_i n_i \log \pi_i + \sum_i \sum_j n_{ij} \log a_{ij} + \sum_j \sum_k c_{jk} \log b_j(k).$$

The rows $\pi$, $a_{i\cdot}$ and $b_{j\cdot}$ appear in separate terms, and each term has the form $\sum_x c_x \log p_x$ with counts $c_x \ge 0$ and a distribution $p$. If $C = \sum_x c_x > 0$, Gibbs' inequality gives $\sum_x c_x \log p_x \le \sum_x c_x \log (c_x / C)$, with equality at $p_x = c_x / C$. If $C = 0$ the term is $0$ for every $p$. $\square$

**Theorem 1 (monotone objective).** $F(\lambda_{k+1}) \ge F(\lambda_k)$ for every round $k$ that updates the model.

*Proof.* $F(\lambda_{k+1}) = \max_{\mathbf{Q}} G(\lambda_{k+1}; \mathbf{Q}) \ge G(\lambda_{k+1}; \mathbf{Q}_k) \ge G(\lambda_k; \mathbf{Q}_k) = F(\lambda_k)$. The first inequality is the definition of $F$, and the second is Lemma 1. $\square$

Write $M(\mathbf{Q}) = \max_\lambda G(\lambda; \mathbf{Q})$. The proof of Theorem 1 also gives the sandwich

$$M(\mathbf{Q}_k) = G(\lambda_{k+1}; \mathbf{Q}_k) \le F_{k+1} = G(\lambda_{k+1}; \mathbf{Q}_{k+1}) \le M(\mathbf{Q}_{k+1}). \tag{S}$$

**Theorem 2 (termination).** In exact arithmetic with tol $= 0$, the algorithm stops after finitely many rounds. If $Z$ is the number of tuples of state paths, at most $Z + 1$ rounds update the model.

*Proof.* A round $b \ge 2$ updates the model only if $F_b > F_{b-1}$, so the values $F_k$ strictly increase along the rounds that update the model. Assume that two updating rounds $a < b$ have $\mathbf{Q}_a = \mathbf{Q}_b$. By (S), $F_b \le M(\mathbf{Q}_b) = M(\mathbf{Q}_a) \le F_{a+1}$. If $b > a + 1$, then $F_b > F_{a+1}$, which is false. So $b = a + 1$. Then $\lambda_{a+2}$ comes from the same counts as $\lambda_{a+1}$. The relative frequencies are the same, and a row with no counts keeps the value of $\lambda_{a+1}$, so $\lambda_{a+2} = \lambda_{a+1}$. Then $F_{a+2} = F_{a+1}$ and round $a + 2$ stops at line L5. So a tuple of paths repeats at most once, in two consecutive rounds, and only just before the end. There are $Z \le \prod_r N^{T_r}$ tuples, which is finite. $\square$

With tol $> 0$ or with the round limit, the code stops no later. In floating point the values $F_k$ are rounded, so Theorem 1 holds up to rounding errors; the tests allow $10^{-9}$.

**Proposition (the total likelihood can go down).** Theorem 1 is about $F$, the log likelihood of the best path. The total log likelihood $\sum_r \log P(O^r \mid \lambda)$ can decrease in a round.

*Proof by example.* Take $N = 2$, $M = 2$ with the symbols $x, y$, one sequence $O = (x, y, x)$, $\pi = (0.2, 0.8)$, $a_{ij} = 0.5$ for all $i, j$, $b_1 = (0.8, 0.2)$ and $b_2 = (0.5, 0.5)$. With uniform transitions, the best path takes the state of largest $\pi_i b_i(o_1)$ at the first frame and of largest $b_i(o_t)$ later: $Q = (2, 2, 1)$, with $P(O, Q) = 0.8 \cdot 0.5 \cdot 0.5 \cdot 0.5 \cdot 0.5 \cdot 0.8 = 0.04$. The total is $P(O) = \sum_{q_1} \pi_{q_1} b_{q_1}(x) \cdot 0.5 \cdot (0.2 + 0.5) \cdot 0.5 \cdot (0.8 + 0.5) = (0.16 + 0.4) \cdot 0.35 \cdot 0.65 = 0.1274$. The counts on $Q$ give $\pi = (0, 1)$, $a_{2 1} = a_{2 2} = 0.5$, row 1 of $A$ unchanged, $b_1 = (1, 0)$ and $b_2 = (0.5, 0.5)$. Now every path starts in state 2, so $P(O) = 0.5 \cdot 0.5 \cdot (0 + 0.5) \cdot 0.5 \cdot (1 + 0.5) = 0.09375 < 0.1274$, while the best path has $P(O, Q) = 1 \cdot 0.5 \cdot 0.5 \cdot 0.5 \cdot 0.5 \cdot 1 = 0.0625 > 0.04$. The test test_total_likelihood_can_decrease checks these numbers. $\square$
