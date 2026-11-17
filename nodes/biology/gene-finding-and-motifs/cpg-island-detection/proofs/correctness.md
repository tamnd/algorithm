---
title: The Viterbi decoder and the window scan find the CpG islands they define
proves: [correctness]
status: full
---

Let $x = x_1 \cdots x_n$ be a sequence over $\{A, C, G, T\}$ with $n \ge 1$. The model has the states $Q = \{+, -\}$, the start probabilities $\pi_k$, the transition probabilities $a_{jk}$, the first-base emissions $e_k(b)$ and the conditional emissions $e_k(b \mid p)$. For a state path $q = q_1 \cdots q_n$,

$$\ln P(x, q) = \ln \pi_{q_1} + \ln e_{q_1}(x_1) + \sum_{i=2}^{n} \big(\ln a_{q_{i-1} q_i} + \ln e_{q_i}(x_i \mid x_{i-1})\big),$$

with $\ln 0 = -\infty$. The island calls of the HMM are the maximal runs of $+$ in a path $q^*$ that maximizes $\ln P(x, q)$.

## The Viterbi decoder

For $1 \le i \le n$ and $k \in Q$, let $v_i(k)$ be the largest value of $\ln P(x_1 \cdots x_i, q_1 \cdots q_i)$ over the paths of length $i$ with $q_i = k$, where the prefix probability is the same sum stopped at $i$.

**Lemma 1.** After line L1, $V[k] = v_1(k)$. After the pass of lines L3 to L6 for position $i$, $V[k] = v_i(k)$, and $\mathit{ptr}[i][k]$ is a state $j$ with $v_{i-1}(j) + \ln a_{jk} = \max_{j'} (v_{i-1}(j') + \ln a_{j'k})$.

*Proof.* For $i = 1$ the only path of length 1 that ends in $k$ is $k$ itself, and line L1 sets $V[k] = \ln \pi_k + \ln e_k(x_1)$. Assume the claim for $i - 1$. A path of length $i$ that ends in $k$ is a path of length $i - 1$ that ends in some $j$, followed by $k$, and its value is the value of the shorter path plus $\ln a_{jk} + \ln e_k(x_i \mid x_{i-1})$. The added term depends only on $j$ and $k$, so the best path that ends in $k$ extends a best path that ends in its state $j$, and

$$v_i(k) = \max_{j} \big(v_{i-1}(j) + \ln a_{jk}\big) + \ln e_k(x_i \mid x_{i-1}).$$

Line L4 picks a $j$ that reaches this maximum, with $V[j] = v_{i-1}(j)$ by the induction hypothesis, and line L5 computes the right side. Line L6 replaces $V$ only after both states are done, so line L5 always reads the values of position $i - 1$. $\square$

**Lemma 2.** The path $q$ built by lines L7 and L8 satisfies $\ln P(x, q) = \max_k v_n(k) = \max_{q'} \ln P(x, q')$.

*Proof.* Line L7 picks $q_n$ with $v_n(q_n) = \max_k v_n(k)$, and every path ends in some state, so this is the largest value of $\ln P(x, q')$. Line L8 sets $q_{i-1} = \mathit{ptr}[i][q_i]$. We show by induction on $i$, from $n$ down to 1, that the path $q_1 \cdots q_i$ obtained by following the pointers from $q_i$ has prefix value $v_i(q_i)$. For $i = 1$ this is Lemma 1. For $i > 1$, the pointer $j = q_{i-1}$ satisfies $v_i(q_i) = v_{i-1}(j) + \ln a_{j q_i} + \ln e_{q_i}(x_i \mid x_{i-1})$ by Lemma 1, and by the induction hypothesis the prefix up to $i - 1$ has value $v_{i-1}(j)$, so the prefix up to $i$ has value $v_i(q_i)$. At $i = n$ this is the claim. $\square$

Line L9 reads off the maximal runs of $+$ of this path, so the HMM calls are the islands of a most probable path. When several paths tie, the decoder returns the one given by its tie rule (the state listed first wins); any of them is a correct answer.

## The window rule

For a window $x[i, i + w)$ (0-based, half-open), let $C_i$ and $G_i$ be its numbers of C and G, and $D_i$ its number of positions $j$ with $i \le j < i + w - 1$, $x_j = C$ and $x_{j+1} = G$. The window is marked when $(C_i + G_i)/w > g$ and $D_i \, w / (C_i G_i) > r$, with the ratio taken as 0 if $C_i G_i = 0$.

**Lemma 3.** At line L11 for window $i$, the counters hold $C_i$, $G_i$ and $D_i$.

*Proof.* For $i = 0$ they are counted directly. Going from window $i - 1$ to window $i$ removes the base $x_{i-1}$ and adds the base $x_{i + w - 1}$, so $C$ and $G$ change by the indicator of the added base minus that of the removed one. The CG pairs of window $i - 1$ start at $j = i - 1, \ldots, i + w - 3$, and those of window $i$ at $j = i, \ldots, i + w - 2$. So the pair at $j = i - 1$ leaves and the pair at $j = i + w - 2$ enters, and the code subtracts and adds exactly these two indicators. $\square$

**Lemma 4.** The intervals returned are exactly the maximal intervals of the union of the marked windows, where two marked windows that overlap or touch are joined.

*Proof.* The marked windows are visited in increasing order of start. The last interval of the output is the union of a group of marked windows, and it ends at $e$, the largest end in the group, which is the end of the last window added because all windows have the same length. A new marked window $[i, i + w)$ with $i \le e$ overlaps or touches it, so the union is $[\text{start}, i + w)$, which the code stores. If $i > e$, no later window starts before $i$, so no later window can touch the old interval, and the old interval is maximal. $\square$

## Running time

Lines L2 to L6 run $n - 1$ times, each with $|Q|^2 = 4$ additions and comparisons, and lines L7 and L8 take $n$ steps, so the decoder takes $\Theta(n |Q|^2) = \Theta(n)$ time and $\Theta(n)$ space for the pointers. The window scan spends $\Theta(w)$ time on the first window and $O(1)$ on each of the other $n - w$ windows, so $\Theta(n)$ time in total and $O(1)$ extra space besides the output.
