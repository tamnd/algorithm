---
title: One generation costs O(N (n + c)), and the (1+1) EA needs expected Θ(n log n) iterations on OneMax
proves: [time.worst, space.extra]
status: full
---

**Claim 1 (the cost of a run).** With tournaments of a fixed size $k$, a run of $G$ generations takes $O(G N (n + c))$ time and $O(N n)$ extra space, where $c$ is the cost of one evaluation of $f$.

*Proof.* Line L4 needs the fitness of the $N$ strings of $P$, which costs $O(N c)$, and the $e$ largest values, which cost $O(N \log N)$ by sorting or $O(N)$ by selection. In the code, the values are computed once per generation and kept. The loop of lines L5 to L9 runs at most $N$ times. Each pass makes two tournaments of $O(k)$ work, one crossover of $O(n)$ work and two mutations of $O(n)$ work, and it copies two strings of length $n$. Line L11 scans the $N$ new values. So one generation costs $O(N(n + c) + N \log N)$, which is $O(N(n + c))$ when $\log N = O(n + c)$, and $G$ generations cost $G$ times this. The populations $P$ and $Q$ and the array of fitness values take $O(N n)$ space. $\square$

The rest of this proof is about the number of iterations, for the simplest evolutionary algorithm. The $(1+1)$ EA keeps one string $x$, drawn uniformly at the start. In each iteration it makes $y$ by flipping each bit of $x$ independently with probability $1/n$, and it sets $x \leftarrow y$ if $f(y) \ge f(x)$. OneMax is $f(x) = \sum_i x_i$, with optimum $1^n$. Let $T$ be the number of iterations until $x = 1^n$, and $H_n = \sum_{j=1}^{n} 1/j$. We use $(1 - 1/n)^{n-1} \ge 1/e$ for $n \ge 2$.

**Claim 2 (upper bound).** $\mathrm{E}[T] \le e n H_n \le e n (\ln n + 1)$.

*Proof.* This is the method of fitness levels. Let level $i$ be the set of strings with $i$ ones. The algorithm accepts only $y$ with $f(y) \ge f(x)$, so the level never goes down. If $x$ is on level $i < n$, the iteration leaves level $i$ upward when it flips exactly one of the $n - i$ zeros and no other bit. This event has probability
$$s_i = (n - i) \cdot \frac{1}{n} \left(1 - \frac{1}{n}\right)^{n-1} \ge \frac{n - i}{e n}.$$
The probability to leave level $i$ is at least $s_i$ in each iteration, whatever happened before, so the expected number of iterations spent on level $i$ is at most $1/s_i$, by the mean of a [geometric distribution](/geometric-distribution/). The run visits each level at most once, so by [linearity of expectation](/linearity-of-expectation/)
$$\mathrm{E}[T] \le \sum_{i=0}^{n-1} \frac{e n}{n - i} = e n \sum_{j=1}^{n} \frac{1}{j} = e n H_n \le e n (\ln n + 1). \qquad \square$$

**Claim 3 (lower bound).** For $n \ge 2$ and $t = \lfloor (n - 1) \ln n \rfloor$, $\Pr[T > t] \ge \frac{1}{2}(1 - e^{-1/2})$. Hence $\mathrm{E}[T] \ge \frac{1}{2}(1 - e^{-1/2}) \, t = \Omega(n \log n)$.

*Proof.* Write each iteration as the choice of a mask $M_s \in \{0,1\}^n$, where $M_s(j) = 1$ means that bit $j$ flips in iteration $s$. The masks are independent of each other and of the start $x_0$, and their bits are independent with probability $1/n$ each. A bit is 0 in $x_0$ and 1 in the final string only if some mask flips it, whether or not that iteration was accepted. So $T \le t$ implies that every position $j$ with $x_0(j) = 0$ has $M_s(j) = 1$ for some $s \le t$.

For one position, the probability that no mask of the first $t$ flips it is $(1 - 1/n)^t \ge (1 - 1/n)^{(n-1)\ln n} \ge e^{-\ln n} = 1/n$. So it is flipped at least once with probability at most $1 - 1/n$. The positions are independent, so if $x_0$ has $z$ zeros, they are all flipped with probability at most $(1 - 1/n)^z \le e^{-z/n}$.

The number $Z$ of zeros in $x_0$ has the [binomial distribution](/binomial-distribution/) $B(n, 1/2)$, which is symmetric about $n/2$, so $\Pr[Z \ge n/2] \ge 1/2$. On that event, $e^{-Z/n} \le e^{-1/2}$. Since $Z$ and the masks are independent,
$$\Pr[T > t] \ge \Pr[Z \ge n/2] \, (1 - e^{-1/2}) \ge \tfrac{1}{2}(1 - e^{-1/2}) \approx 0.197.$$
Finally, $\mathrm{E}[T] \ge t \Pr[T > t]$, by [Markov's inequality](/markov-inequality/) in the form $\mathrm{E}[T] \ge t \Pr[T \ge t]$. $\square$

Claims 2 and 3 give $\mathrm{E}[T] = \Theta(n \log n)$ for the $(1+1)$ EA on OneMax. The lower bound has the form of the [coupon collector problem](/coupon-collector-problem/): about $n/2$ positions must each be hit by a mutation, and each is hit with probability $1/n$ per iteration. Droste, Jansen and Wegener (2002) proved the same order for every linear function $f(x) = \sum_i w_i x_i$ with nonzero weights, where the upper bound needs a more careful potential function. $\blacksquare$
