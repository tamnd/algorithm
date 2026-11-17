---
title: The Viterbi pass returns a most probable copy number path, and the forward pass returns the probability of the counts
proves: [correctness]
status: full
---

**Setting.** There are $n \ge 1$ windows with counts $x_0, \ldots, x_{n-1}$ and $K$ hidden states $0, \ldots, K - 1$, the copy numbers. The model is a hidden Markov chain $c_0, \ldots, c_{n-1}$ with start probabilities $\pi(c)$, transition probabilities $A(b, c) = P(c_t = c \mid c_{t-1} = b)$ and emission probabilities $e_c(x) = P(x_t = x \mid c_t = c)$. Given the states, the counts are independent, and $x_t$ depends only on $c_t$. So for a path $c = (c_0, \ldots, c_{n-1})$,

$$P(x, c) = \pi(c_0)\, e_{c_0}(x_0) \prod_{t=1}^{n-1} A(c_{t-1}, c_t)\, e_{c_t}(x_t).$$

In the code, $\pi(c) = 1/K$, $A(b, b) = 1 - p$, $A(b, c) = p / (K - 1)$ for $c \ne b$, and $e_c$ is the Poisson law with mean $\lambda \max(c, \varepsilon)/2$. The proof uses only the product form above, so it holds for any start, transition and emission tables. All values are logarithms: $E[t][c] = \ln e_c(x_t)$ (line L1), $T[b][c] = \ln A(b, c)$, and $\ln 0 = -\infty$.

**Lemma 1 (Viterbi table).** After line L2, and after lines L4 to L6 for step $t$, $V[t][c] = \max \ln P(x_0, \ldots, x_t, c_0, \ldots, c_t)$ over the paths $c_0, \ldots, c_t$ with $c_t = c$.

*Proof.* By induction on $t$. For $t = 0$ the only path is $(c)$, and line L2 sets $V[0][c] = \ln \pi(c) + E[0][c]$. For $t > 0$, by the product form,

$$\ln P(x_{0..t}, c_{0..t}) = \ln P(x_{0..t-1}, c_{0..t-1}) + T[c_{t-1}][c_t] + E[t][c_t].$$

Fix $c_t = c$ and split the paths by $b = c_{t-1}$. For fixed $b$, the largest value of the first term is $V[t-1][b]$ by the hypothesis, and the other two terms do not depend on $c_0, \ldots, c_{t-2}$. So the maximum over the paths is $\max_b (V[t-1][b] + T[b][c]) + E[t][c]$, which is line L5. $\square$

**Lemma 2 (back pointers).** For $t \ge 1$, the state $b = \mathrm{ptr}[t][c]$ of line L6 satisfies $V[t][c] = V[t-1][b] + T[b][c] + E[t][c]$.

*Proof.* Line L6 stores the $b$ that reaches the maximum of line L5, the smallest such $b$ if several do. $\square$

**Theorem 1 (Viterbi).** The path $c^*$ of lines L7 and L8 maximizes $P(x, c)$ over all $K^n$ paths, and $V[n-1][c^*_{n-1}] = \ln P(x, c^*)$. Among the maximizers, it is the one that the tie rule picks: the smallest last state, and then at each step back the smallest previous state.

*Proof.* By Lemma 1, $\max_c V[n-1][c]$ is the largest $\ln P(x, c)$ over all paths, and line L7 takes a state $c^*_{n-1}$ that reaches it. Line L8 sets $c^*_{t-1} = \mathrm{ptr}[t][c^*_t]$. By Lemma 2, for each $t \ge 1$, $V[t][c^*_t] = V[t-1][c^*_{t-1}] + T[c^*_{t-1}][c^*_t] + E[t][c^*_t]$. Adding these equations for $t = 1, \ldots, n-1$ to $V[0][c^*_0] = \ln \pi(c^*_0) + E[0][c^*_0]$ gives $V[n-1][c^*_{n-1}] = \ln P(x, c^*)$, so $c^*$ reaches the maximum. $\square$

The tests check Theorem 1 against a search over all $K^n$ paths for small $K$ and $n$.

**Theorem 2 (forward and posteriors).** The forward table satisfies $F[t][c] = \ln P(x_0, \ldots, x_t, c_t = c)$, and its last value is $\ln P(x) = \ln \sum_{c} F[n-1][c]$ in log space. The backward table satisfies $B[t][c] = \ln P(x_{t+1}, \ldots, x_{n-1} \mid c_t = c)$, and $\exp(F[t][c] + B[t][c] - \ln P(x)) = P(c_t = c \mid x)$.

*Proof.* The forward claim is Lemma 1 with the maximum over $b$ replaced by a sum over $b$, which is valid for the same reason: the sum over the paths with $c_t = c$ splits by $b = c_{t-1}$, and the last two factors do not depend on the earlier states. The code forms the sum of exponentials with log-sum-exp, $\ln \sum_b e^{u_b} = M + \ln \sum_b e^{u_b - M}$ with $M = \max_b u_b$, which is an identity. For the backward table, $B[n-1][c] = 0 = \ln 1$, and by the Markov property

$$P(x_{t+1..n-1} \mid c_t = c) = \sum_d A(c, d)\, e_d(x_{t+1})\, P(x_{t+2..n-1} \mid c_{t+1} = d),$$

which is the code. Last, $P(x, c_t = c) = P(x_{0..t}, c_t = c)\, P(x_{t+1..n-1} \mid c_t = c)$, because given $c_t$ the later counts do not depend on the earlier states and counts. Dividing by $P(x)$ gives the posterior. $\square$

**Viterbi and posterior decoding can differ.** Theorem 1 is about the whole path. The state of largest posterior at each window, from Theorem 2, need not lie on the best path. In the page example with $p = 0.1$, window 6 has posterior 0.512 for state 3 and 0.485 for state 2, while the Viterbi path has state 2 there.

**Cost.** Line L1 costs $\Theta(n K)$. Each step of line L3 does $K$ maximizations over $K$ values, so the Viterbi pass takes $\Theta(n K^2)$ time and keeps $\Theta(n K)$ back pointers; the forward and backward passes have the same cost. With the transition matrix of the code, $\max_b (V[b] + T[b][c])$ is the larger of $V[c] + \ln(1 - p)$ and $\max_{b \ne c} V[b] + \ln(p/(K-1))$. The two largest values of $V$ give $\max_{b \ne c} V[b]$ for every $c$, so a pass can be done in $\Theta(n K)$ time. The code uses the general $\Theta(n K^2)$ loop.
