---
title: Each block of the turbo equalizer returns exact extrinsic LLRs for its own model with independent priors; the loop as a whole has no convergence guarantee
proves: [correctness]
status: full
---

**Setting.** LLRs are $L(b) = \ln P(b = 0) / P(b = 1)$, and a symbol $x = 1 - 2b$ has the LLR of its bit, so $P(x) \propto e^{x L / 2}$. Write $\mathrm{lse}(S) = \ln \sum_{v \in S} e^v$.

**Lemma 1 (posterior from path metrics).** Let a finite set of paths $p$ have the weights $e^{M(p)}$, with $M(p) = \sum_t \gamma_t(p)$, and let each path fix a bit $b_t(p)$. Then the forward and backward recursions
$$\alpha_{t+1}(s') = \mathrm{lse}_{(s \to s')} (\alpha_t(s) + \gamma_t(s \to s')), \qquad \beta_t(s) = \mathrm{lse}_{(s \to s')} (\gamma_t(s \to s') + \beta_{t+1}(s'))$$
give $\mathrm{lse}\{M(p) : b_t(p) = b\} = \mathrm{lse}_{(s \to s'),\, b} (\alpha_t(s) + \gamma_t(s \to s') + \beta_{t+1}(s'))$, where the edge set is the edges at step $t$ that set the bit to $b$.

*Proof.* By induction on $t$, $\alpha_t(s)$ is the lse of the metrics of all path prefixes that end in state $s$ at time $t$, and $\beta_t(s)$ is the lse of the metrics of all suffixes from $s$. Every path with $b_t = b$ is one prefix to some $s$, one edge $s \to s'$ with bit $b$, and one suffix from $s'$, in exactly one way. The lse of a sum over a product set is the sum of the lse values, so the claim follows. $\square$

**Theorem 1 (the equalizer).** For the channel model $y_m = \sum_l h_l x_{m-l} + w_m$ with $w_m \sim N(0, \sigma^2)$ independent, independent priors $L_a(x_t)$, and the known start (all symbols before the block are 0), line L3 returns $L_e(x_t) = \ln P(x_t = +1 \mid y) / P(x_t = -1 \mid y) - L_a(x_t)$.

*Proof.* A path is a symbol sequence $x_0, \ldots, x_{N-1}$. Its posterior is proportional to $p(y \mid x) \prod_t P(x_t)$, with
$$\ln p(y \mid x) = \text{const} - \frac{1}{2\sigma^2} \sum_{m=0}^{N+L-2} \Big(y_m - \sum_l h_l x_{m-l}\Big)^2.$$
Sample $m \le N - 1$ depends on $x_m$ and the state $(x_{m-1}, \ldots, x_{m-L+1})$, so it is part of $\gamma_m$. Samples $m = N, \ldots, N + L - 2$ depend only on the final state $(x_{N-1}, \ldots, x_{N-L+1})$; the code puts them in $\beta_N$. The prior term $x_t L_a(x_t) / 2$ is in $\gamma_t$, and the omitted constants $-\ln(2 \cosh(L_a/2))$ are the same for every path. So $M(p)$ is the log posterior of the path up to a constant, and Lemma 1 gives $\ln P(x_t = +1 \mid y) - \ln P(x_t = -1 \mid y)$ as the difference of two lse values. Subtracting $L_a(x_t)$ gives the extrinsic LLR. Since the posterior LLR is $L_a(x_t)$ plus a term in which $x_t$ enters only through $p(y \mid x)$ and the priors of the other symbols, the extrinsic LLR does not depend on $L_a(x_t)$. $\square$

**Theorem 2 (the decoder).** For the terminated (7, 5) code and independent priors $L_a(c_j)$ on the code bits, line L5 returns the exact posterior LLRs of the information bits and $L_e(c_j) = L(c_j \mid L_a) - L_a(c_j)$ for each code bit, where the information bits are uniform.

*Proof.* A path is a message $u \in \{0, 1\}^K$, and the trellis state is $(u_{t-1}, u_{t-2})$, starting and ending at 0 because of the two tail bits. The posterior of $u$ given the priors is proportional to $\prod_j P(c_j(u)) \propto \exp(\tfrac12 \sum_j (1 - 2 c_j(u)) L_a(c_j))$, which is $e^{M(p)}$ with the edge metric of line L5. Each edge fixes $u_t$ (for $t < K$) and the two code bits of step $t$. Lemma 1 gives each posterior LLR, and subtracting $L_a(c_j)$ gives the extrinsic one. $\square$

The tests check Theorem 1 for 8 symbols of the Proakis B channel and Theorem 2 for 6 information bits against sums over all $2^8$ and $2^6$ paths, to $10^{-9}$. For a channel with one tap, Theorem 1 reduces to $L_e(x_t) = 2 h_0 y_t / \sigma^2$, and a test checks this too.

**The loop.** Theorems 1 and 2 hold for any priors that are independent across bits. Inside the loop, the priors of line L3 are the extrinsic outputs of line L5 and the other way round. After the first iteration, these LLRs depend on overlapping parts of $y$, so they are not independent, and the outputs are not the true posteriors of the joint model. The joint model is a factor graph with cycles through the interleaver, and the loop is belief propagation on it.

**No convergence theorem.** No general result says that the loop converges, that its fixed point gives the MAP decisions, or that the error rate falls from one iteration to the next. This page does not claim any of these. What the test checks is a measurement: for one seeded block of 3000 bits at 3.5 dB on Proakis B, the Wilson intervals of the bit error rates after iterations 1 and 2 at $z = 3.29$ do not overlap. The table on the page includes a case where iteration 4 has more errors than iteration 3.
