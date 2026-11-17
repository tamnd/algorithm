---
title: The site sampler draws from the exact full conditional and leaves the posterior invariant
proves: [correctness]
status: full
---

Let $s_1, \ldots, s_n$ ($n \ge 2$) be DNA sequences, each with $W_i \ge 1$ windows of length $L$, let $b > 0$, and let $q(a) > 0$ for each letter. A state is a tuple $t = (t_1, \ldots, t_n)$ of starts. Let $w^{(i)} = s_i[t_i .. t_i + L - 1]$ be the site of $s_i$, $c_j(a)$ the number of sites with letter $a$ in column $j$, and $(b)_m = \prod_{k=0}^{m-1} (b + k)$. Define

$$\pi(t) = \frac{1}{Z} \cdot \frac{\prod_{j=1}^{L} \prod_{a} (b)_{c_j(a)}}{\prod_{i=1}^{n} \prod_{j=1}^{L} q(w^{(i)}_j)},$$

with $Z$ the sum of the fraction over all states.

**Where $\pi$ comes from.** Let column $j$ of the motif have letter probabilities $\theta_j$ with the Dirichlet prior of density $\Gamma(4b)\Gamma(b)^{-4} \prod_a \theta_j(a)^{b - 1}$, let all letters outside the sites have the probabilities $q$, and let the starts have a uniform prior. The likelihood of the sequences given $t$ and $\theta$ is $\prod_j \prod_a \theta_j(a)^{c_j(a)}$ times the product of $q$ over all letters, divided by the product of $q$ over the letters of the sites. The Dirichlet integral gives $\int \prod_a \theta_j(a)^{c_j(a) + b - 1} d\theta_j = \prod_a \Gamma(c_j(a) + b) / \Gamma(n + 4b)$. With $\Gamma(c + b) = \Gamma(b) (b)_c$ and after dropping the factors that do not depend on $t$, the posterior of $t$ is $\pi$.

**Lemma 1 (the exact full conditional).** For each $i$, each state $t$ and each start $x$ of $s_i$, let $t^{x}$ be $t$ with $t_i$ replaced by $x$, and let $A_x$ be the weight of line L6 computed from the counts $c^{-i}$ of the other $n - 1$ sites. Then

$$\frac{\pi(t^{x})}{\sum_y \pi(t^{y})} = \frac{A_x}{\sum_y A_y}.$$

*Proof.* Let $u$ be the window of $s_i$ at $x$. In $t^x$, the count of $u_j$ in column $j$ is $c^{-i}_j(u_j) + 1$, and every other count is $c^{-i}_j(a)$. Since $(b)_{m+1} = (b)_m (b + m)$, the numerator of $\pi(t^x)$ is $N \cdot \prod_j (b + c^{-i}_j(u_j))$, where $N = \prod_j \prod_a (b)_{c^{-i}_j(a)}$ does not depend on $x$. The denominator is $D \cdot \prod_j q(u_j)$, where $D$, the product over the other sites, does not depend on $x$. So $\pi(t^x) = (N / (Z D)) \prod_j (c^{-i}_j(u_j) + b)/q(u_j) = (N (n - 1 + 4b)^L / (Z D)) \, A_x$. The factor in front is the same for all $x$, so it cancels in the ratio. $\square$

**Lemma 2 (the code computes these weights).** Before line L6 runs for sequence $i$, the counts $c$ are $c^{-i}$.

*Proof.* Line L1 sets $c$ to the counts of all $n$ sites. Each update removes the old site of its sequence at line L5 and adds the new one at line L8, so between updates $c$ is the count of all current sites. Inside the update for $i$, after line L5, it is the count of the other sites. The code computes $\log A_x$, subtracts the largest value $m$ and draws with the weights $e^{\log A_x - m} = A_x e^{-m}$, which have the same normalized values. $\square$

**Lemma 3 (the draw).** If $U$ is uniform on $[0, 1)$ and $S = \sum_k w_k$, the function `draw` returns $k$ with probability $w_k / S$.

*Proof.* It returns the first $k$ with $U S < w_0 + \cdots + w_k$, which happens exactly when $U S$ is in $[w_0 + \cdots + w_{k-1}, w_0 + \cdots + w_k)$, an interval of length $w_k$ in $[0, S)$. The last line catches the case in which rounding makes the final sum a little smaller than $U S$. $\square$

In floating point Lemma 3 holds up to rounding; the tests check it with a chi-square test.

**Theorem (invariance and convergence).** Let $K_i$ be the kernel of one update of sequence $i$. Then $\pi K_i = \pi$ for each $i$. So the systematic scan $K_1 K_2 \cdots K_n$ and the random scan $\frac{1}{n} \sum_i K_i$ (each repeated $n$ times per iteration) leave $\pi$ invariant. Both chains are irreducible and aperiodic on the finite set of states, so $\pi$ is their unique stationary distribution, the distribution of the state converges to $\pi$, and the chain visits every state with probability 1.

*Proof.* By Lemmas 1 to 3, $K_i(t, t^x) = \pi(t^x) / \sum_y \pi(t^y)$, and $K_i(t, u) = 0$ when $u$ differs from $t$ outside position $i$. For $u$ and $t$ that agree outside position $i$, the sum $\sum_y \pi(t^y)$ is the same for $t$ and $u$, so $\pi(t) K_i(t, u) = \pi(t)\pi(u)/\sum_y \pi(t^y) = \pi(u) K_i(u, t)$. This is detailed balance, and summing over $t$ gives $(\pi K_i)(u) = \pi(u)$. A product or an average of kernels that keep $\pi$ keeps $\pi$.

Every $A_x$ is positive, since $b > 0$ and $q > 0$, so $\pi$ is positive on every state and $K_i(t, t^x) > 0$ for all $x$. The systematic scan moves from any state to any state in one iteration with positive probability. The random scan does too, since with positive probability its $n$ choices of $i$ are $1, \ldots, n$ in order. A chain with a positive one-step kernel on a finite set is irreducible and aperiodic, and the standard limit theorem for finite Markov chains gives the rest. $\square$

**Corollary (the output).** GIBBS-MOTIF returns a state that the chain visited at line L1 or at the end of some iteration, with the largest $\log \pi$ among these, since line L9 replaces $best$ only by a strictly larger value. As $T \to \infty$, the probability that the output is a mode of $\pi$ tends to 1, because the chain at the end of iterations is itself irreducible and visits every state.

**Cost.** An update takes $O(L)$ for lines L5 and L8 and $O(WL)$ for line L6 and line L7. An iteration takes $n$ updates and $O(nL)$ for line L9, so $O(nWL)$, and $T$ iterations take $O(TnWL)$. The extra space is $O(nL + W)$.

The theorem is about the limit. It gives no bound on the mixing time, and the measured success rates on the page show that finite runs can fail.

The tests check Lemma 1 exactly with fractions on all 27 states of a small input, check $\pi K_i = \pi$ for each $i$ and for the random scan exactly, check that differences of $\log \pi$ equal differences of $\log A_x$, check Lemma 3 with a chi-square test, and measure the planted success rate.
