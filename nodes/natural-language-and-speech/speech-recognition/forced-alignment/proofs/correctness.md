---
title: Forced alignment returns a best path of the transcript chain
proves: [correctness]
status: full
---

We use the notation of the page. The chain has the states $0, 1, \ldots, S-1$ and there are $T \ge S$ frames, numbered $0$ to $T-1$ as in the code. Write $e_t(j)$ for the log emission score of state $j$ at frame $t$, $a_j$ for the log self loop of state $j$ and $m_j$ for the log move $j \to j+1$. All logs are natural logs.

A *chain path to $(t, j)$* is a sequence $q_0, \ldots, q_t$ with $q_0 = 0$, $q_t = j$ and $q_u - q_{u-1} \in \{0, 1\}$ for $u = 1, \ldots, t$. Its score is

$$\mathrm{score}(q) = e_0(0) + \sum_{u=1}^{t} \big( w(q_{u-1}, q_u) + e_u(q_u) \big), \qquad w(i, i) = a_i, \quad w(i, i+1) = m_i.$$

A full path is a chain path to $(T-1, S-1)$. Its score is $\log P(O, Q \mid \lambda)$ of the chain HMM, up to the exit transition of the last state, which is the same constant for every full path. Let $V(t, j)$ be the largest score of a chain path to $(t, j)$, with $V(t, j) = -\infty$ if there is none.

**Lemma 1 (which cells matter).** A chain path to $(t, j)$ exists if and only if $0 \le j \le t$. It can be extended to a full path if and only if, in addition, $j \ge S - T + t$.

*Proof.* Each step raises the state by at most 1, so $q_t \le t$, and any $j \le \min(t, S-1)$ is reached by moving $j$ times and staying the rest. From $(t, j)$, the $T - 1 - t$ remaining steps raise the state by at most $T - 1 - t$, so $S - 1 \le j + T - 1 - t$ is needed, and it is enough. $\square$

Write $lo_t = \max(0, S - T + t)$ and $hi_t = \min(S-1, t)$, as in the code. Since $T \ge S$, $lo_t \le hi_t$ for every $t$.

**Lemma 2 (invariant).** After line L1 (for $t = 0$) and after the pass of line L2 for frame $t \ge 1$, $\delta[j] = V(t, j)$ for $lo_t \le j \le hi_t$, and $\delta[j] = -\infty$ for every other $j$. For $lo_t \le j \le hi_t$ and $t \ge 1$, the back pointer $\psi_t(j)$ is a state $i$ with $V(t, j) = V(t-1, i) + w(i, j) + e_t(j)$.

*Proof.* By induction on $t$. For $t = 0$, the only chain path is $q_0 = 0$, with score $e_0(0)$. Line L1 sets $\delta[0] = e_0(0)$ and the other entries to $-\infty$, and $lo_0 = hi_0 = 0$.

For $t \ge 1$, take $j$ with $lo_t \le j \le hi_t$. The last step of a chain path to $(t, j)$ comes from $(t-1, j)$ or from $(t-1, j-1)$. The score is additive along the path, so

$$V(t, j) = \max\big( V(t-1, j) + a_j,\ V(t-1, j-1) + m_{j-1} \big) + e_t(j),$$

with the second term absent for $j = 0$. We check that $\delta$ holds the correct values of these two predecessors. First, $j \ge lo_t \ge lo_{t-1}$ and, if $j \ge 1$, $j - 1 \ge lo_t - 1 \ge lo_{t-1}$ when $lo_{t-1} > 0$, and $j - 1 \ge 0 = lo_{t-1}$ otherwise. Second, $j - 1 \le hi_{t-1}$ because $j - 1 \le t - 1$ and $j - 1 \le S - 1$. Third, $j \le hi_{t-1}$ unless $j = t$; in that case Lemma 1 gives $V(t-1, j) = -\infty$, and the induction hypothesis gives $\delta[j] = -\infty$. So line L4 computes the two terms with the correct values, lines L5 and L6 take the larger one, add $e_t(j)$ and store the state that gives it. The entries outside $lo_t \ldots hi_t$ stay $-\infty$, because the new array starts at $-\infty$. $\square$

**Theorem.** If some full path has a finite score, FORCED-ALIGN returns a full path $Q$ with the largest score, and this score. Otherwise it raises an error at line L7.

*Proof.* At $t = T - 1$, $lo_{T-1} = hi_{T-1} = S - 1$, so by Lemma 2, $\delta[S-1] = V(T-1, S-1)$ at line L7. This is the largest score of a full path, and it is $-\infty$ exactly when every full path has probability 0. The loop of line L8 follows the back pointers from $(T-1, S-1)$. By Lemma 2, each pointer goes to a state $i$ with $V(t, j) = V(t-1, i) + w(i, j) + e_t(j)$, and $i \in \{j-1, j\}$ is a cell in the range of frame $t-1$. By induction from $t = T-1$ down to $t = 1$, the suffix $q_t, \ldots, q_{T-1}$ found so far has the property that the best chain path to $(t, q_t)$ followed by this suffix has the score $V(T-1, S-1)$. At $t = 0$ the only chain path is $q_0 = 0$, so the whole path has the score $V(T-1, S-1)$. $\square$

**Proposition (tie rule).** Among all full paths with the largest score, FORCED-ALIGN returns the one whose reversed sequence $(q_{T-1}, q_{T-2}, \ldots, q_0)$ is the largest in lexicographic order. So, scanned from the end, each state keeps as many frames as an optimal path allows.

*Proof.* Let $Q^*$ be that path and $Q$ the returned path. Both end in $S-1$. Assume that they agree on the frames $t, \ldots, T-1$, with $t \ge 1$, and let $j = q_t$. A full path with this suffix is optimal if and only if its prefix is a best chain path to $(t, j)$, because the score is additive. So $q^*_{t-1}$ is the largest state $i \in \{j-1, j\}$ with $V(t-1, i) + w(i, j) = V(t, j) - e_t(j)$. Line L5 picks the move only if the move is strictly better than the stay. So the pointer is $j$ whenever $j$ attains the maximum, and $j - 1$ only when $j$ does not. That is the same choice, so $q_{t-1} = q^*_{t-1}$. $\square$

**Remark (rounding).** In floating point, each addition is rounded, and rounding to nearest is monotone: $x \le y$ implies $\mathrm{fl}(x + c) \le \mathrm{fl}(y + c)$. The code adds the terms of a path in the same order as the left fold in the definition of the score. Lemma 2 and the theorem then hold word for word with the score replaced by its rounded left fold, so the code returns the exact maximum of the rounded path scores. The values are sums of logs, not products of probabilities, so they do not underflow: a path of $T$ frames whose terms are at least $-c$ has a score of at least $-cT$, which is far inside the range of a double.
