---
title: A Baum-Welch round never decreases the likelihood and keeps the parameters stochastic
proves: [correctness]
status: full
---

Fix $R \ge 1$ observation sequences $O^{(1)}, \ldots, O^{(R)}$, each of length at least 1, and current parameters $\lambda = (\pi, A, B)$ with $P(O^{(r)} \mid \lambda) > 0$ for every $r$. Write $\mathbf{Q} = (Q^{(1)}, \ldots, Q^{(R)})$ for a choice of one state path per sequence, $\mathbf{O}$ for all the sequences, and

$$L(\lambda) = \sum_{r} \log P(O^{(r)} \mid \lambda), \qquad P(\mathbf{Q}, \mathbf{O} \mid \lambda) = \prod_r P(Q^{(r)}, O^{(r)} \mid \lambda).$$

The sequences are independent given $\lambda$, so $L(\lambda) = \log \sum_{\mathbf{Q}} P(\mathbf{Q}, \mathbf{O} \mid \lambda)$.

**Lemma 1 (the expected counts).** Let $s_i$, $e_{ij}$ and $f_{jk}$ be the totals of lines L4. Then $s_i$ is the expected number of sequences that start in $i$, $e_{ij}$ is the expected number of moves $i \to j$, and $f_{jk}$ is the expected number of times that state $j$ emits symbol $k$, all under $P(\mathbf{Q} \mid \mathbf{O}, \lambda)$.

*Proof.* The number of moves $i \to j$ in $\mathbf{Q}$ is $\sum_r \sum_{t < T_r} [q^{(r)}_t = i, q^{(r)}_{t+1} = j]$. By the linearity of expectation its expected value is $\sum_r \sum_t P(q^{(r)}_t = i, q^{(r)}_{t+1} = j \mid O^{(r)}, \lambda) = \sum_r \sum_t \xi^{(r)}_t(i, j)$, because the paths of different sequences are independent given the data. The forward-backward algorithm computes these $\xi$ exactly (see its page). The other two counts are the same argument with $\gamma$. $\square$

**Lemma 2 (the auxiliary function).** Define, for any parameters $\lambda'$,

$$\mathcal{Q}(\lambda') = \sum_{\mathbf{Q}} P(\mathbf{Q} \mid \mathbf{O}, \lambda) \log P(\mathbf{Q}, \mathbf{O} \mid \lambda'),$$

with $\log 0 = -\infty$ and $0 \cdot (-\infty) = 0$. Then $L(\lambda') - L(\lambda) \ge \mathcal{Q}(\lambda') - \mathcal{Q}(\lambda)$.

*Proof.* If $\mathcal{Q}(\lambda') = -\infty$ there is nothing to prove. Otherwise $P(\mathbf{Q}, \mathbf{O} \mid \lambda') > 0$ for every $\mathbf{Q}$ with $w(\mathbf{Q}) = P(\mathbf{Q} \mid \mathbf{O}, \lambda) > 0$. Sum only over those $\mathbf{Q}$. Since $\log$ is concave, [Jensen's inequality](/jensens-inequality/) gives

$$L(\lambda') = \log \sum_{\mathbf{Q}} P(\mathbf{Q}, \mathbf{O} \mid \lambda') \ge \log \sum_{w(\mathbf{Q}) > 0} w(\mathbf{Q}) \frac{P(\mathbf{Q}, \mathbf{O} \mid \lambda')}{w(\mathbf{Q})} \ge \sum_{w(\mathbf{Q}) > 0} w(\mathbf{Q}) \log \frac{P(\mathbf{Q}, \mathbf{O} \mid \lambda')}{w(\mathbf{Q})}.$$

The right side is $\mathcal{Q}(\lambda') - \sum w \log w$. For $\lambda' = \lambda$, $P(\mathbf{Q}, \mathbf{O} \mid \lambda) / w(\mathbf{Q}) = e^{L(\lambda)}$ is the same for every $\mathbf{Q}$, so the two inequalities are equalities and $L(\lambda) = \mathcal{Q}(\lambda) - \sum w \log w$. Subtract. $\square$

**Lemma 3 (the M step).** Lines L5 to L7 return parameters $\bar\lambda$ that maximize $\mathcal{Q}$ over all stochastic $(\pi', A', B')$.

*Proof.* Take the log of the product form of the joint and use Lemma 1:

$$\mathcal{Q}(\lambda') = \sum_i s_i \log \pi'_i + \sum_i \sum_j e_{ij} \log A'_{ij} + \sum_j \sum_k f_{jk} \log B'_j(k).$$

The three sums depend on separate rows, so each row can be maximized alone. For one row with non-negative counts $c_1, \ldots, c_m$ and total $c > 0$, and any probability vector $p$, Gibbs' inequality says $\sum_k c_k \log p_k \le \sum_k c_k \log (c_k / c)$, with equality at $p_k = c_k / c$. This is the normalized row of lines L5 to L7. If a row has $c = 0$ its term is $0$ for every $p$, so the old row, which the implementation keeps, is also a maximizer. The maximum is finite: $\bar p_k > 0$ wherever $c_k > 0$. $\square$

**Theorem (monotone likelihood).** $L(\bar\lambda) \ge L(\lambda)$, and $P(O^{(r)} \mid \bar\lambda) > 0$ for every $r$.

*Proof.* $\mathcal{Q}(\lambda)$ is finite, because $w(\mathbf{Q}) > 0$ implies $P(\mathbf{Q}, \mathbf{O} \mid \lambda) > 0$. By Lemma 3, $\mathcal{Q}(\bar\lambda) \ge \mathcal{Q}(\lambda) > -\infty$, and by Lemma 2, $L(\bar\lambda) - L(\lambda) \ge \mathcal{Q}(\bar\lambda) - \mathcal{Q}(\lambda) \ge 0$. As $L(\lambda)$ is finite, so is $L(\bar\lambda)$, so each sequence keeps a positive probability. $\square$

**Stochastic rows.** Every count is a sum of probabilities, so it is non-negative. A row with a positive total is divided by that total, so it is non-negative and sums to 1. A row with a zero total keeps the old row, which is stochastic. Also, if $A_{ij} = 0$ then $\xi^{(r)}_t(i, j) = 0$ for all $r$ and $t$, so $e_{ij} = 0$ and $\bar A_{ij} = 0$; the same holds for $\pi$ and $B$. A zero parameter stays zero.

**Convergence.** The sequence $L(\lambda^{(0)}) \le L(\lambda^{(1)}) \le \cdots$ is bounded above by 0, so it converges. This does not mean that the parameters converge to the global maximum. Wu (1983) gives conditions under which the limit points are stationary points of $L$; these may be local maxima or saddle points. A symmetric start is such a point. If $\pi$ and the rows of $A$ are uniform and all the rows of $B$ are equal, then the data give no information about the states, every $\gamma_t$ is uniform, and one round sets each row of $B$ to the symbol frequencies of the data and keeps $\pi$ and $A$ uniform. From then on nothing changes, although a model that tells the states apart can have a much larger likelihood. $\blacksquare$
