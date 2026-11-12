---
title: The BCJR algorithm returns the exact a posteriori LLR of each input bit
proves: [correctness]
status: full
---

**Setting.** The trellis has steps $t = 0, \ldots, T-1$. Each edge $e$ of step $t$ goes from a state $s(e)$ at time $t$ to a state $s'(e)$ at time $t+1$ and carries an input bit $u(e)$ and an output block $x(e)$. The start state at time 0 is $0$. The end states at time $T$ form a set $F$ ($F = \{0\}$ for a terminated code). A *path* is a sequence of edges $e_0, \ldots, e_{T-1}$ with $s(e_0) = 0$, $s'(e_t) = s(e_{t+1})$ and $s'(e_{T-1}) \in F$. Distinct paths have distinct input sequences, because two edges out of the same state carry different inputs.

The input bits are independent with priors $P(u_t)$, and the channel is memoryless: given the path, $P(y \mid \text{path}) = \prod_t P(y_t \mid x(e_t))$. Let $\gamma_t(e) = P(u(e)) \, P(y_t \mid x(e))$ for an edge $e$ of step $t$, or any fixed positive multiple $c_t \gamma_t(e)$ with $c_t$ the same for all edges of step $t$. In the LLR form, $\ln \gamma_t(e) = \tfrac12 (1 - 2u(e)) L_a(u_t) + \tfrac12 \sum_j (1 - 2x_j(e)) L_c(y_{t,j})$ differs from $\ln P(u(e)) P(y_t \mid x(e))$ by a term that depends only on $t$ and $y_t$, so it is such a multiple.

**Lemma 1 (posterior of a path).** For each path $\pi = (e_0, \ldots, e_{T-1})$, $P(\pi \mid y) = w(\pi) / Z$, where $w(\pi) = \prod_t \gamma_t(e_t)$ and $Z = \sum_{\pi'} w(\pi')$ over all paths.

*Proof.* A path is fixed by its inputs, so its prior is $\prod_t P(u(e_t))$, and Bayes' rule gives $P(\pi \mid y) \propto \prod_t P(u(e_t)) P(y_t \mid x(e_t))$. Replacing each factor by $c_t$ times it multiplies every $w(\pi)$ by the same $\prod_t c_t$, which cancels in $w(\pi)/Z$. $\square$

Define, without normalization,

$$A_t(s) = \sum_{\text{partial paths } 0 \to s \text{ of length } t} \ \prod_{i<t} \gamma_i(e_i), \qquad B_t(s) = \sum_{\text{partial paths } s \to F \text{ from time } t} \ \prod_{i \ge t} \gamma_i(e_i),$$

with $A_0(0) = 1$, $A_0(s) = 0$ for $s \ne 0$, $B_T(s) = 1$ for $s \in F$ and $B_T(s) = 0$ otherwise.

**Lemma 2 (recursions).** $A_{t+1}(s') = \sum_{e : s'(e) = s'} A_t(s(e))\, \gamma_t(e)$ and $B_t(s) = \sum_{e : s(e) = s} \gamma_t(e)\, B_{t+1}(s'(e))$, with the sums over the edges of step $t$.

*Proof.* Each partial path from 0 to $s'$ of length $t+1$ is one partial path of length $t$ to some state $s$ followed by one edge $e$ from $s$ to $s'$, and each such pair gives one partial path. So the sum over the long paths splits by the last edge, and the product splits as the product over the prefix times $\gamma_t(e)$. The distributive law gives the formula. The proof for $B$ is the same with the first edge. $\square$

**Lemma 3 (edge marginal).** For an edge $e$ of step $t$, $\sum_{\pi \ni e} w(\pi) = A_t(s(e))\, \gamma_t(e)\, B_{t+1}(s'(e))$.

*Proof.* A path through $e$ is a partial path from 0 to $s(e)$, then $e$, then a partial path from $s'(e)$ to $F$, and each such triple is one path. The weight is the product of the three parts. Sum over all triples and use the distributive law. $\square$

**Theorem.** Lines L1 to L8 return, for each $t$,

$$L(u_t) = \ln \frac{P(u_t = 0 \mid y)}{P(u_t = 1 \mid y)}.$$

*Proof.* By Lemma 1 and Lemma 3, $P(u_t = b \mid y) = \frac{1}{Z} \sum_{e \text{ of step } t,\ u(e) = b} A_t(s(e))\, \gamma_t(e)\, B_{t+1}(s'(e))$.

The algorithm computes $\alpha_t = A_t / a_t$ and $\beta_t = B_t / b_t$ for positive numbers $a_t$, $b_t$. This holds at $t = 0$ (line L1, $a_0 = 1$) and at $t = T$ (line L4, $b_T = 1$; for an unterminated code all end states are in $F$). Line L2 applies Lemma 2 to $\alpha_t$, which gives $A_{t+1} / a_t$, and line L3 divides by the sum $z > 0$, so $a_{t+1} = a_t z$. Lines L5 and L6 do the same for $\beta$. The sum $z$ is positive: the state 0 at time 0 reaches every state that has a nonzero $A$, and each $\gamma_t(e) > 0$ for a channel with a positive density.

Line L7 forms $p_t(b) = \sum_{u(e) = b} \alpha_t(s(e))\, \gamma_t(e)\, \beta_{t+1}(s'(e)) = \frac{Z}{a_t b_{t+1}} P(u_t = b \mid y)$. The factor $Z / (a_t b_{t+1})$ is the same for $b = 0$ and $b = 1$, so line L8 returns $\ln p_t(0) - \ln p_t(1) = L(u_t)$. If one of the two is 0, no path has that input at step $t$, and the LLR is $\pm\infty$. $\blacksquare$

**The log domain.** Let $\max^*(a, b) = \ln(e^a + e^b) = \max(a, b) + \ln(1 + e^{-|a - b|})$. The identity holds because $e^a + e^b = e^{\max(a,b)} (1 + e^{-|a-b|})$. $\max^*$ is associative and commutative, so $\ln \sum_i e^{a_i}$ is the $\max^*$ of the $a_i$ in any order. The log-MAP recursions replace each product by a sum of logarithms and each sum by $\max^*$, so they compute $\ln A_t$, $\ln B_t$ and $L(u_t)$ exactly, without normalization.

**The max-log approximation.** Replacing $\max^*$ by $\max$ gives max-log-MAP. Then $\tilde A_t(s)$ is the largest log weight of a partial path to $s$, and the output is

$$\tilde L(u_t) = \max_{\pi : u_t = 0} \ln w(\pi) - \max_{\pi : u_t = 1} \ln w(\pi),$$

the difference of the best path metrics with $u_t = 0$ and with $u_t = 1$. Since $\max_i a_i \le \ln \sum_{i=1}^{N} e^{a_i} \le \max_i a_i + \ln N$, each of the two terms is within $\ln N$ of the exact one, where $N$ is the number of paths with that value of $u_t$. So $|\tilde L(u_t) - L(u_t)| \le \ln N_{\max}$. The sign of $\tilde L(u_t)$ is the value of $u_t$ on the best path, which is the Viterbi decision.
