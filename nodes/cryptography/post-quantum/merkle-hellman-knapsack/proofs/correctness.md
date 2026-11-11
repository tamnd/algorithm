---
title: CJLOSS returns only solutions, and finds the target whenever it is the shortest vector
proves: [correctness]
status: full
---

Let $a_1, \ldots, a_n$ be positive integers, $s$ an integer, and $L$ the lattice spanned by the rows $b_1, \ldots, b_{n+1}$ of lines L2 and L3, with $N = \lfloor \sqrt{n} \rfloor + 1$ from line L1. Write $v = (v_1, \ldots, v_n, v_{n+1})$.

**Lemma 1 (the rows are a basis).** If $2 s \ne \sum_i a_i$, the rows $b_1, \ldots, b_{n+1}$ are linearly independent. If $2 s = \sum_i a_i$, then $2 b_{n+1} = \sum_i b_i$.

*Proof.* Suppose $\sum_i y_i b_i + y_{n+1} b_{n+1} = 0$ with real $y$. The first $n$ entries give $2 y_i + y_{n+1} = 0$, so $y_i = -y_{n+1}/2$ for all $i$. The last entry gives $N(\sum_i y_i a_i + y_{n+1} s) = N y_{n+1} (s - \frac{1}{2} \sum_i a_i) = 0$. If $2s \ne \sum_i a_i$, then $y_{n+1} = 0$ and so all $y_i = 0$. The second claim is a direct check: $\sum_i b_i = (2, \ldots, 2, N \sum_i a_i) = (2, \ldots, 2, 2 N s) = 2 b_{n+1}$. $\square$

So we assume $2s \ne \sum_i a_i$. In the excluded case, every solution $x$ has its complement as a second solution, and the local LLL stops with an error on the dependent rows; a caller can then drop $b_{n+1}$ and search for $\pm(2x - 1)$ in the lattice of $b_1, \ldots, b_n$ shifted by one vector. The code does not handle this case, which a random instance hits with negligible probability.

**Lemma 2 (the target).** If $x \in \{0, 1\}^n$ and $\sum_i x_i a_i = s$, then $t = \sum_i x_i b_i - b_{n+1} = (2x_1 - 1, \ldots, 2x_n - 1, 0)$ lies in $L$ and $\|t\| = \sqrt{n}$.

*Proof.* Entry $i \le n$ of $\sum_j x_j b_j$ is $2 x_i$, and entry $n+1$ is $N \sum_j x_j a_j = N s$. Subtracting $b_{n+1} = (1, \ldots, 1, N s)$ gives $(2 x_i - 1)_i$ and $0$. Each $2x_i - 1$ is $\pm 1$, so $\|t\|^2 = n$. $\square$

**Lemma 3 (long vectors).** Every $v \in L$ with $v_{n+1} \ne 0$ has $\|v\| > \sqrt{n}$.

*Proof.* $v_{n+1}$ is $N$ times an integer, so $|v_{n+1}| \ge N = \lfloor \sqrt{n} \rfloor + 1 > \sqrt{n}$. $\square$

**Lemma 4 (what the scan accepts).** Let $v \in L$ with $v_{n+1} = 0$ and $v_i \in \{-1, 1\}$ for $i \le n$, and write $v = \sum_i y_i b_i + y_{n+1} b_{n+1}$ with integers $y$. Then $y_{n+1}$ is odd. If $y_{n+1} = -1$, then $x = ((v_i + 1)/2)_i$ solves $\sum x_i a_i = s$. If $y_{n+1} = 1$, the same holds for $-v$.

*Proof.* Entry $i \le n$ is $v_i = 2 y_i + y_{n+1}$, which is odd only if $y_{n+1}$ is odd. If $y_{n+1} = -1$, then $y_i = (v_i + 1)/2 \in \{0, 1\}$, so $x = y$. Entry $n+1$ is $N(\sum_i y_i a_i - s) = 0$, so $\sum_i x_i a_i = s$. If $y_{n+1} = 1$, then $-v$ has coefficients $-y$ with $-y_{n+1} = -1$, and the first case applies. $\square$

**Theorem 1 (soundness).** If CJLOSS returns $x$, then $x \in \{0, 1\}^n$ and $\sum_i x_i a_i = s$.

*Proof.* Line L7 is reached only when every $v_i \in \{-1, 1\}$, so every $x_i = (v_i + 1)/2 \in \{0, 1\}$. Line L8 returns $x$ only if $\sum_i x_i a_i = s$. $\square$

**Theorem 2 (completeness given the target).** If a solution $x$ exists and the reduced basis of line L4 contains $t$ or $-t$ as a row, CJLOSS returns a solution. In particular this holds when $\pm t$ are the only vectors of $L$ of length at most $\sqrt{n}$, and line L4 returns a basis whose first row is a shortest vector.

*Proof.* LLL returns a basis of the same lattice. If the row is $t$, line L5 tries $v = t$ first; $t_{n+1} = 0$ and every $t_i = \pm 1$ by Lemma 2, so line L6 accepts, line L7 gives $(t_i + 1)/2 = x_i$, and line L8 returns $x$. If the row is $-t$, line L5 also tries $-(-t) = t$, with the same result; it may first try $-t$ itself, which gives the complement $\bar{x}$, and line L8 rejects it unless $\bar{x}$ is also a solution, in which case returning it is correct. For the second claim: by Lemma 2 the shortest vector has length at most $\sqrt{n}$, so if $\pm t$ are the only vectors of that length or less, the first row is $\pm t$. $\blacksquare$

**When the target is the shortest vector (CJLOSS, 1992).** Let $a_1, \ldots, a_n$ be chosen uniformly at random from $\{1, \ldots, A\}$ with $A = 2^{c n}$, and let $s = \sum x_i a_i$ for a fixed $x$. If $c > 1.0628$, that is, $d = n / \log_2 A < 1/1.0628 \approx 0.9408$, then the probability that $L$ has a vector of length at most $\sqrt{n}$ other than $\pm t$ (and the vectors from the complement) tends to 0 as $n \to \infty$. The idea of the proof: a bad vector $v$ with $v_{n+1} = 0$ gives integers $y$ with $\sum_i y_i a_i = y_{n+1} s$ and $(2y_i + y_{n+1})_i$ short. For a fixed such $y$ not proportional to the target, this one linear relation holds with probability at most $1/A$ over the random $a$. The number of candidate vectors $y$ is bounded with the estimate of Mazo and Odlyzko for integer points in balls, and is at most $2^{c_0 n + o(n)}$ with $c_0 = 1.0628\ldots$ for this lattice. A union bound gives probability at most $2^{c_0 n + o(n)} / A \to 0$ when $c > c_0$. The same argument for the Lagarias-Odlyzko lattice gives the larger constant $1.5472\ldots$, that is, density $0.6463$. These constants are the content of the CJLOSS and Lagarias-Odlyzko papers and are not reproved here.
