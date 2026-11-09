---
title: The knapsack table holds the optimal values, and the traceback returns an optimal set
proves: [correctness, termination]
status: full
---

Write $w(S) = \sum_{i \in S} w_i$ and $v(S) = \sum_{i \in S} v_i$. For $0 \le i \le n$ and $0 \le c \le W$, let $\mathcal{F}(i, c) = \{ S \subseteq \{1, \ldots, i\} : w(S) \le c \}$ and $\mathrm{OPT}(i, c) = \max \{ v(S) : S \in \mathcal{F}(i, c) \}$. The family is never empty, because $\emptyset \in \mathcal{F}(i, c)$, so the maximum exists.

**Lemma 1 (recurrence).** $\mathrm{OPT}(0, c) = 0$. For $i \ge 1$, $\mathrm{OPT}(i, c) = \mathrm{OPT}(i-1, c)$ if $w_i > c$, and $\mathrm{OPT}(i, c) = \max(\mathrm{OPT}(i-1, c), \mathrm{OPT}(i-1, c - w_i) + v_i)$ if $w_i \le c$.

*Proof.* $\mathcal{F}(0, c) = \{\emptyset\}$, so $\mathrm{OPT}(0, c) = 0$. Let $i \ge 1$. Split $\mathcal{F}(i, c)$ into the sets without item $i$ and the sets with it. The sets without item $i$ are exactly $\mathcal{F}(i-1, c)$, and their best value is $\mathrm{OPT}(i-1, c)$. If $w_i > c$, no feasible set contains item $i$, because its weight alone exceeds $c$ and all weights are non-negative. If $w_i \le c$, the map $S \mapsto S \setminus \{i\}$ is a bijection from the sets with item $i$ onto $\mathcal{F}(i-1, c - w_i)$, because $w(S) \le c$ if and only if $w(S \setminus \{i\}) \le c - w_i$. It lowers the value by exactly $v_i$. So the best value of a set with item $i$ is $\mathrm{OPT}(i-1, c - w_i) + v_i$. The maximum over the two parts is the claim. $\square$

**Lemma 2 (table).** After lines L1 to L6, $V[i][c] = \mathrm{OPT}(i, c)$ for all $0 \le i \le n$ and $0 \le c \le W$.

*Proof.* By induction on $i$. Line L1 sets $V[0][c] = 0 = \mathrm{OPT}(0, c)$. Let $i \ge 1$, and assume that row $i - 1$ is correct (the induction hypothesis). In the iteration for $(i, c)$, line L4 sets $V[i][c] = V[i-1][c]$. If $w_i > c$, line L5 does nothing, and the value is $\mathrm{OPT}(i-1, c) = \mathrm{OPT}(i, c)$ by Lemma 1. If $w_i \le c$, then $c - w_i \in [0, c]$ is a valid index, and lines L5 and L6 replace the value by $V[i-1][c - w_i] + v_i$ exactly when this is larger. So $V[i][c] = \max(\mathrm{OPT}(i-1, c), \mathrm{OPT}(i-1, c-w_i) + v_i) = \mathrm{OPT}(i, c)$ by the hypothesis and Lemma 1. Row $i$ reads only row $i - 1$, which no later step changes. $\square$

**Lemma 3 (traceback).** Before the iteration of line L8 for index $i$ (and after the loop, with $i = 0$), the set $S$ and the capacity $c$ satisfy:

> **(T)** $S \subseteq \{i+1, \ldots, n\}$, $c \ge 0$, $w(S) + c \le W$, and $v(S) + \mathrm{OPT}(i, c) = \mathrm{OPT}(n, W)$.

*Proof.* Before the first iteration, $i = n$, $S = \emptyset$ and $c = W$, so (T) holds. Assume (T) before the iteration for $i \ge 1$.

*Case $V[i][c] = V[i-1][c]$.* By Lemma 2, $\mathrm{OPT}(i, c) = \mathrm{OPT}(i-1, c)$. Nothing changes, and (T) holds for $i - 1$.

*Case $V[i][c] \ne V[i-1][c]$.* By Lemma 1, $\mathrm{OPT}(i, c) \ne \mathrm{OPT}(i-1, c)$ is possible only when $w_i \le c$ and $\mathrm{OPT}(i, c) = \mathrm{OPT}(i-1, c - w_i) + v_i$. Line L10 adds $i$ to $S$ and sets $c' = c - w_i \ge 0$. Then $S \cup \{i\} \subseteq \{i, \ldots, n\}$, $w(S \cup \{i\}) + c' = w(S) + c \le W$, and $v(S \cup \{i\}) + \mathrm{OPT}(i-1, c') = v(S) + \mathrm{OPT}(i, c) = \mathrm{OPT}(n, W)$. So (T) holds for $i - 1$. $\square$

**Theorem.** KNAPSACK-DP terminates and returns $V[n][W] = \mathrm{OPT}(n, W)$ and a set $S$ with $w(S) \le W$ and $v(S) = \mathrm{OPT}(n, W)$.

*Proof.* Every loop runs over a finite range that the body does not change, so the algorithm terminates after $(W+1) + n(W+1) + n$ iterations. The first value is correct by Lemma 2. After the loop of line L8, (T) holds with $i = 0$. Since $\mathrm{OPT}(0, c) = 0$, it gives $v(S) = \mathrm{OPT}(n, W)$, and $w(S) \le W - c \le W$. So $S$ is feasible and optimal. $\blacksquare$

**The one-row form.** In the version with one array and $c$ from $W$ down to $w_i$, the pass for item $i$ writes the positions in decreasing order. At the step for $c$, it reads $V[c - w_i]$. If $w_i > 0$, the position $c - w_i$ is smaller than $c$ and is written only later in the pass. If $w_i = 0$, the read comes before the write of the same step. In both cases the value read is still that of row $i - 1$. The same induction applies. With $c$ from low to high, position $c - w_i$ is already updated, and the recurrence becomes that of the unbounded problem.
