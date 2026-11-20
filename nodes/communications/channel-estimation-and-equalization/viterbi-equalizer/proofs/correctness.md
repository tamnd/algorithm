---
title: The Viterbi equalizer returns the maximum likelihood sequence on a channel with white Gaussian noise
proves: [correctness]
status: full
---

The channel taps are $f_0, \ldots, f_{L-1}$ and the alphabet $\mathcal{A}$ has $M$ points. The known symbols $x_{-L+1}, \ldots, x_{-1}$ come from `pre`, the unknown symbols are $x_0, \ldots, x_{n-1}$, and the known symbols $x_n, \ldots, x_{K-1}$ come from `tail`. The received samples are $y_k = \sum_{l=0}^{L-1} f_l x_{k-l} + n_k$ for $k = 0, \ldots, K-1$, with $n_k$ i.i.d. $\mathcal{CN}(0, N_0)$. Write $\hat y_k(x) = \sum_l f_l x_{k-l}$ and
$$J(x) = \sum_{k=0}^{K-1} |y_k - \hat y_k(x)|^2 .$$

**Lemma 1 (the metric).** The likelihood is $p(y \mid x) = (\pi N_0)^{-K} \exp(-J(x)/N_0)$. So a sequence maximizes the likelihood over $\mathcal{A}^n$ if and only if it minimizes $J$.

*Proof.* Given $x$, the samples $y_k$ are independent with $y_k \sim \mathcal{CN}(\hat y_k(x), N_0)$. Multiply the densities. The exponential is strictly decreasing in $J$. $\square$

**Lemma 2 (the state).** Let the state at time $k$ be $s_k = (x_{k-1}, \ldots, x_{k-L+1})$. Then $\hat y_k(x)$ depends only on $s_k$ and $x_k$, and $s_{k+1}$ is a function of $s_k$ and $x_k$. For $k < L - 1$, the entries of $s_k$ with negative index are the known `pre` symbols.

*Proof.* $\hat y_k$ uses $x_k, \ldots, x_{k-L+1}$, which are $x_k$ and the entries of $s_k$. The next state drops $x_{k-L+1}$ and puts $x_k$ in front. In the code, the state integer holds only the entries with index at least 0, and `out` reads the others from `pre` (line L5). So two partial sequences with the same last $L - 1$ symbols give the same branch metrics at every later time. $\square$

So $J(x) = \sum_k \lambda_k(s_k, x_k)$ with the branch metric $\lambda_k(s, a) = |y_k - \hat y_k|^2$. Each sequence $x$ is a path through the trellis with $M^{L-1}$ states per time, and $J$ is the sum of the branch metrics along the path.

**Lemma 3 (the survivors).** After step $k$ of the loop at line L3, `metric[s]` is the minimum of $\sum_{t \le k} \lambda_t$ over all paths of length $k+1$ that are allowed (they use the `tail` symbol at times $t \ge n$) and end in state $s$, or $\infty$ if there is no such path. Following the pointers from $s$ gives a path that reaches this minimum.

*Proof.* By induction on $k$. Before the loop there is one path of length 0, and it has metric 0 (line L2). The state label 0 is a placeholder: for $k < L-1$, line L5 reads the past symbols from `pre`, and the entries of the state that the code uses at time $k$ are only those with index $k - t \ge 0$. Assume the claim after step $k - 1$. A path of length $k+1$ that ends in $t$ is a path of length $k$ that ends in some $s$ with $\mathrm{next}(s, a) = t$, followed by the branch $a$. Its metric is the metric of the prefix plus $\lambda_k(s, a)$, and $\lambda_k(s, a)$ does not depend on the prefix by Lemma 2. So the best path into $t$ has the best prefix into its own $s$, which gives the minimum over $s$ and $a$ of `metric[s]` $+ \lambda_k(s, a)$. Lines L4 to L6 compute exactly this minimum and store the argument in the pointer. At times $k \ge n$, line L4 tries only the `tail` symbol, which is the set of allowed branches. $\square$

**Theorem 1 (maximum likelihood).** `viterbi_equalize` returns a sequence $\hat x \in \mathcal{A}^n$ with $J(\hat x) = \min_{x \in \mathcal{A}^n} J(x)$, with the `pre` and `tail` symbols fixed. So $\hat x$ is a maximum likelihood sequence.

*Proof.* By Lemma 3 with $k = K - 1$, the minimum of `metric` over all states (line L7) is the minimum of $J$ over all allowed paths, and the traceback at line L8 returns a path that reaches it. The allowed paths are exactly the sequences $x \in \mathcal{A}^n$ followed by the tail. Line L9 drops the tail. Lemma 1 ends the proof. $\square$

If two paths tie, the code keeps the first one it finds. The brute force in the tests may keep another one, so the tests compare the metrics too.

**Theorem 2 (the cost).** The loop runs $K$ times. Each step visits $M^{L-1}$ states and $M$ branches per state, and each branch metric costs $O(1)$ for $k \ge L - 1$, because the code computes the $M^L$ outputs $\hat y$ for each state and symbol once before the loop, in $O(L M^L)$. They do not depend on $k$ for $k \ge L - 1$. The first $L - 1$ steps cost $O(L)$ per branch. So the time is $O(K M^L + L^2 M^L)$, which is $O(K M^L)$ when $K \ge L^2$. The pointers need $O(K M^{L-1})$ space.

*Proof.* Count the operations in lines L3 to L6. The traceback costs $O(K)$. $\square$

**Theorem 3 (the high SNR error rate).** For BPSK with $\mathcal{A} = \{+1, -1\}$, define $d_{\min}^2 = \min \|f * e\|^2$ over error sequences $e \in \{-2, 0, 2\}^m$ with $e_0 \ne 0$. Then $d_{\min}^2 \le 4 \|f\|^2$. If the block is longer than the event that reaches $d_{\min}$, the probability that the output sequence is wrong is at least $c\,Q\big(\sqrt{d_{\min}^2/(2 N_0)}\big)$ for a constant $c > 0$. The probability of an error on a given symbol is at least $Q\big(\sqrt{2\|f\|^2/N_0}\big)$.

*Proof.* The single error $e = (2)$ gives $\|f * e\|^2 = 4\|f\|^2$, so the minimum is at most this. For the first bound, take the event $e$ that reaches $d_{\min}$, placed inside the block, and the transmitted data for which $x + e$ is in the alphabet. This data has probability $c = 2^{-w(e)}$, where $w(e)$ is the number of nonzero entries. With $u = f * e$, $J(x + e) < J(x)$ holds if and only if $\|n - u\|^2 < \|n\|^2$, that is $\mathrm{Re}\langle n, u\rangle / \|u\| > \|u\|/2$. The left side is real Gaussian with variance $N_0/2$, so this happens with probability $Q(d_{\min}/(2\sqrt{N_0/2}))$, and then the ML output is not $x$. For the second bound, give the detector all other symbols for free. Then deciding $x_k$ is a binary test between two points at the distance $2\|f\|$ and the best error probability is $Q(\|f\|/\sqrt{N_0/2})$. No detector beats the genie. $\square$

The union bound over all error events gives an upper bound of the same form $\sum_e w(e) 2^{-w(e)} Q(\|f * e\|/\sqrt{2 N_0})$, which the first term dominates at high SNR. The function `min_distance_bpsk` computes $d_{\min}^2$ by a depth-first search over $e$: it adds the energy of the outputs that one more entry fixes, prunes a branch once its partial energy reaches the best value found, and closes an event by adding the energy of the last $L - 1$ outputs.
