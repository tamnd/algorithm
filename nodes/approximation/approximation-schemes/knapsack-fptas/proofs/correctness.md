---
title: The knapsack FPTAS returns a feasible set of profit at least (1 − ε)·OPT
proves: [correctness, time.worst]
status: full
---

We use the names of the pseudocode. The input has $N$ items with positive integer profits $p_i$ and weights $w_i$, a capacity $W \ge 0$ and a number $0 < \varepsilon \le 1$. Line L1 keeps the set $I$ of the items with $w_i \le W$, and $n = |I|$. We number the kept items $1, \ldots, n$ in the order of $I$. For a set $T$ of kept items we write $p(T) = \sum_{j \in T} p_j$, $p'(T) = \sum_{j \in T} p'_j$ and $w(T) = \sum_{j \in T} w_j$.

**Step 0 (the removed items).** An item with $w_i > W$ is in no feasible set, because the weights are positive. So the feasible sets of the input are exactly the sets $T \subseteq I$ with $w(T) \le W$, and $\mathrm{OPT}$ is the same for the input and for $I$. If $n = 0$, the only feasible set is $\emptyset$, $\mathrm{OPT} = 0$, and line L2 returns $\emptyset$. From here on, $n \ge 1$.

**Lemma 1 (the table).** For $0 \le j \le n$ and $0 \le q \le Q$, the entry $A[j][q]$ is the least weight $w(T)$ over the sets $T \subseteq \{1, \ldots, j\}$ with $p'(T) = q$, and $\infty$ if there is no such set.

*Proof.* By induction on $j$. For $j = 0$, the only set is $\emptyset$, with $p'(\emptyset) = 0$ and $w(\emptyset) = 0$, which is line L6. Let $j \ge 1$ and assume the claim for $j - 1$. A set $T \subseteq \{1, \ldots, j\}$ with $p'(T) = q$ either does not hold $j$, and then it is a set for row $j - 1$ and column $q$, or it holds $j$, and then $T \setminus \{j\}$ is a set for row $j - 1$ and column $q - p'_j$, which needs $p'_j \le q$. Conversely each set of these two kinds gives such a $T$. So the least weight is the minimum of $A[j-1][q]$ and, when $p'_j \le q$, of $A[j-1][q - p'_j] + w_j$. Lines L9 and L10 compute exactly this minimum. $\square$

**Lemma 2 (the returned set).** Line L11 is well defined, and the set $S$ of line L12 has $w(S) \le W$ and $p'(S) = q^*$, where $q^* = \max \{p'(T) : T \subseteq \{1, \ldots, n\},\ w(T) \le W\}$.

*Proof.* Every set $T$ has $p'(T) \le Q$, so by Lemma 1 the value $\max\{q : A[n][q] \le W\}$ is the largest scaled profit of a set of weight at most $W$. It exists because $A[n][0] = 0 \le W$. So line L11 finds $q^*$. For the trace back we keep this invariant at the start of the loop body for index $j$: the current $q$ satisfies $A[j][q] < \infty$, and the items already put in $S$ are a set $R \subseteq \{j + 1, \ldots, n\}$ with $p'(R) = q^* - q$ and $w(R) = A[n][q^*] - A[j][q]$. It holds for $j = n$ with $R = \emptyset$. If $A[j][q] = A[j-1][q]$, the loop skips item $j$, and the invariant holds for $j - 1$ with the same $q$. Otherwise line L10 set $A[j][q] = A[j-1][q - p'_j] + w_j$, so $p'_j \le q$ and $A[j-1][q - p'_j] = A[j][q] - w_j < \infty$; the loop adds $j$ and sets $q \leftarrow q - p'_j$, and both equations stay true. After $j = 1$, the current $q$ has $A[0][q] < \infty$, so $q = 0$ and $A[0][0] = 0$. Hence $p'(S) = q^*$ and $w(S) = A[n][q^*] \le W$. $\square$

**Lemma 3 (rounding error).** Let $K = \varepsilon P / n$ as in line L4. For each item, $p_j - K < K p'_j \le p_j$.

*Proof.* Line L5 sets $p'_j = \lfloor p_j / K \rfloor$, and $x - 1 < \lfloor x \rfloor \le x$ for each real $x$. Multiply by $K > 0$. $\square$

**Theorem.** The set $S$ is feasible, and $p(S) \ge (1 - \varepsilon) \cdot \mathrm{OPT}$. More exactly, $\mathrm{OPT} - p(S) < nK = \varepsilon P$ when $\mathrm{OPT} > 0$.

*Proof.* Feasibility is Lemma 2. Let $O \subseteq I$ be an optimal set, so $p(O) = \mathrm{OPT}$ and $w(O) \le W$. Then

$$
p(S) \ge K \, p'(S) = K q^* \ge K \, p'(O) > p(O) - |O| K \ge \mathrm{OPT} - nK = \mathrm{OPT} - \varepsilon P.
$$

The first step is Lemma 3 summed over $S$. The second is Lemma 2. The third is Lemma 2 again, because $O$ is a candidate in the maximum that defines $q^*$. The fourth is Lemma 3 summed over $O$, and it is strict when $O \ne \emptyset$; $O$ is not empty because $n \ge 1$ and a single kept item is feasible. The fifth uses $|O| \le n$.

The item with the largest profit $P$ is kept, so the set that holds only this item is feasible, and $P \le \mathrm{OPT}$. So $p(S) > \mathrm{OPT} - \varepsilon P \ge (1 - \varepsilon)\,\mathrm{OPT}$. $\blacksquare$

**Running time.** Each kept item has $p_j \le P$, so $p'_j \le P / K = n / \varepsilon$, and $p'_j \le \lfloor n / \varepsilon \rfloor$ because $p'_j$ is an integer. Hence $Q \le n \lfloor n / \varepsilon \rfloor$. Lines L6 to L10 fill $(n + 1)(Q + 1)$ entries with $O(1)$ work each on the [word RAM](/word-ram/), line L11 reads $Q + 1$ entries and line L12 does $n$ steps. Lines L1 to L5 take $O(N)$ time. The total is $O(N + n^3 / \varepsilon)$, and the table takes $O(n^3 / \varepsilon)$ space. Each entry is a sum of at most $n$ input weights, so it fits in a constant number of words. $\blacksquare$
