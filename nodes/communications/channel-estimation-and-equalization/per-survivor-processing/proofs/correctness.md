---
title: Each survivor's estimate is the LMS estimate driven by that survivor's own symbols, and with the step size 0 the receiver is the maximum likelihood Viterbi equalizer
proves: [correctness]
status: full
---

The received samples are $y_n = \sum_{k=0}^{L-1} f_{n,k}\, x_{n-k} + w_n$ with real symbols $x_n$ from an alphabet of $M$ points, and the symbols $x_{-1}, \ldots, x_{-(L-1)}$ before the block are known (the argument `pre`). The trellis state at time $n$ is $s_n = (x_{n-1}, \ldots, x_{n-L+1})$, most recent first. For the state $s$ and the new symbol $a$, the branch vector is $\mathbf{x} = (a, s)$, of length $L$, and the next state is the first $L - 1$ entries of $\mathbf{x}$. Each state $s$ that is reached holds a metric $\Gamma(s)$, a channel estimate $\hat f(s)$ and a back pointer. The step size is $\beta \ge 0$.

**Lemma 1 (one survivor per state).** After time $n$, every state $t$ that is reached has exactly one survivor: the sequence $x_0, \ldots, x_n$ obtained by following the back pointers from $t$. Its metric is
$$\Gamma(t) = \sum_{i=0}^{n} \big(y_i - \hat f_i^{\top} \mathbf{x}_i\big)^2,$$
where $\mathbf{x}_i$ is the branch vector of the survivor at time $i$ and $\hat f_i$ is the estimate that the survivor held before time $i$.

*Proof.* By induction on $n$. Before time 0 only the known start state is reached, with metric 0 (line L1). At time $n$, line L3 extends every reached state $s$ by every symbol $a$, line L4 computes the error $e = y_n - \hat f(s)^{\top} \mathbf{x}$ with the estimate of $s$, and line L5 keeps, for each next state $t$, the branch with the smallest $\Gamma(s) + e^2$. The kept branch extends the survivor of $s$, so the survivor of $t$ is the survivor of $s$ followed by $a$, and its metric is the metric of $s$ plus the new term. $\square$

**Lemma 2 (the estimate follows its own survivor).** After time $n$, the estimate of the state $t$ is the result of the LMS recursion
$$\hat f_{i+1} = \hat f_i + \beta\, \big(y_i - \hat f_i^{\top} \mathbf{x}_i\big)\, \mathbf{x}_i, \qquad \hat f_0 = f_0,$$
run for $i = 0, \ldots, n$ on the symbols $\mathbf{x}_i$ of the survivor of $t$.

*Proof.* By induction on $n$, with Lemma 1. Line L6 computes the estimate of $t$ from the estimate of the winning predecessor $s$, with the error and the branch vector of the winning branch. By the induction hypothesis, the estimate of $s$ is the LMS result on the survivor of $s$, and the survivor of $t$ is that survivor followed by the winning branch. $\square$

So no estimate uses a symbol that its own survivor does not contain, and every estimate is updated at time $n$ with the symbol $x_n$ of its survivor, without a decision delay. A receiver with one estimator must wait until the survivors merge before it can trust a decision. Here each hypothesis is carried with its own channel.

**Theorem 1 (step size 0).** If $\beta = 0$, the decisions equal the maximum likelihood sequence for the channel $f_0$ and white Gaussian noise, and the returned estimate is $f_0$.

*Proof.* With $\beta = 0$, line L6 copies the estimate, so by Lemma 2 every estimate is $f_0$ at every time. Then the branch metric in line L4 is $(y_n - f_0^{\top} \mathbf{x})^2$, the same for every survivor, and the metric of Lemma 1 is the squared distance between $y$ and the noiseless output of the survivor. This is the add-compare-select of the Viterbi algorithm on the trellis of the channel $f_0$. The cost of a whole sequence is a sum of branch costs that depend only on the state and the new symbol, so the principle of optimality applies: if the best sequence passes through the state $t$ at time $n$, its first $n + 1$ symbols are the best path into $t$, which is the survivor of $t$. Line L7 takes the end state with the smallest metric and follows the back pointers, so it returns the sequence with the smallest squared distance. For white Gaussian noise this is the maximum likelihood sequence. $\square$

**Theorem 2 (the cost).** With $M^{L-1}$ states, each time step evaluates $M^L$ branches at $O(L)$ each and updates $M^{L-1}$ estimates at $O(L)$ each. A block of $N$ samples costs $O(N L M^L)$ time, the same order as the Viterbi equalizer with a known channel, and $O(N M^{L-1} + L M^{L-1})$ space for the back pointers and the estimates.

*Proof.* Count the work in lines L3 to L6 for one time step, and multiply by $N$. The traceback in line L7 costs $O(N)$. $\square$

With $\beta > 0$, the receiver is not the maximum likelihood detector for an unknown channel. Lemma 2 gives what it is: a Viterbi search in which every path is scored by the prediction errors of its own adaptive channel estimate. The page reports measured error counts for this case.
