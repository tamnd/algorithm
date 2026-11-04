---
title: The matroid greedy algorithm returns a maximum-weight basis
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a matroid $M = (E, \mathcal{I})$ with $|E| = n$, given by the test $indep$, and a weight function $w : E \to \mathbb{R}$. Let $e_1, \ldots, e_n$ be the order of line L1, so $w(e_1) \ge \cdots \ge w(e_n)$. Let $A_0 = \emptyset$ and let $A_i$ be the value of $A$ after iteration $i$ of the loop of line L3. The algorithm returns $A_n$.

**Claim.** The algorithm stops after $n$ oracle calls, and $A_n$ is a basis of $M$ with $w(A_n) \ge w(B)$ for every basis $B$. Moreover, for every independent set $X$ with elements $x_1, \ldots, x_s$ sorted so that $w(x_1) \ge \cdots \ge w(x_s)$, and for the elements $g_1, \ldots, g_r$ of $A_n$ in the order in which they were added, $s \le r$ and $w(g_k) \ge w(x_k)$ for $k = 1, \ldots, s$.

**Step 1: termination.** The sort of line L1 stops, and the loop of line L3 runs $n$ times with one oracle call each.

**Step 2: $A_i$ is independent.** $A_0 = \emptyset \in \mathcal{I}$ by (I1). If $A_{i-1}$ is independent, then $A_i$ is either $A_{i-1}$ or $A_{i-1} \cup \{e_i\}$, and line L5 runs only when line L4 found $A_{i-1} \cup \{e_i\} \in \mathcal{I}$.

**Step 3: $A_n$ is a basis.** Let $x \in E \setminus A_n$. Then $x = e_i$ for some $i$ with $A_{i-1} \cup \{e_i\} \notin \mathcal{I}$. Since $A_{i-1} \cup \{e_i\} \subseteq A_n \cup \{e_i\}$, the hereditary property (I2) gives $A_n \cup \{x\} \notin \mathcal{I}$. So no element can be added to $A_n$, and $A_n$ is a maximal independent set, a basis. Write $r = |A_n|$.

**Step 4: $s \le r$.** Let $X$ be independent. If $|X| > r$, then (I3) applied to $A_n$ and $X$ gives $x \in X \setminus A_n$ with $A_n \cup \{x\} \in \mathcal{I}$, against Step 3. So $s = |X| \le r$.

**Step 5: $w(g_k) \ge w(x_k)$.** The elements $g_1, \ldots, g_r$ were added in the order of line L1, so $w(g_1) \ge \cdots \ge w(g_r)$. Suppose that $w(g_k) < w(x_k)$ for some $k \le s$, and take the least such $k$. Let $P = \{g_1, \ldots, g_{k-1}\}$ and $Q = \{x_1, \ldots, x_k\}$. Both are independent by (I2), and $|P| = k - 1 < k = |Q|$, so by (I3) there is $x_j \in Q \setminus P$ with $P \cup \{x_j\} \in \mathcal{I}$. Since $j \le k$, $w(x_j) \ge w(x_k) > w(g_k)$. Let $x_j = e_t$. Because $w(e_t) > w(g_k)$, line L1 puts $e_t$ before $g_k$. At the start of iteration $t$, the set $A_{t-1}$ contains only elements added before $g_k$, so $A_{t-1} \subseteq P$, and $A_{t-1} \cup \{e_t\} \subseteq P \cup \{x_j\}$ is independent by (I2). So line L4 accepted $e_t$, and $e_t \in A_n$ was added before $g_k$, which means $e_t \in P$. This contradicts $x_j \notin P$. So $w(g_k) \ge w(x_k)$ for all $k \le s$.

**Step 6: optimality.** Let $B$ be any basis. All bases have the same size, so $|B| = r$, and by Step 5 with $X = B$ and $s = r$,
$$ w(B) = \sum_{k=1}^{r} w(x_k) \le \sum_{k=1}^{r} w(g_k) = w(A_n). $$
The argument does not use the sign of the weights. If all weights are nonnegative, Step 5 also gives $w(X) \le \sum_{k \le s} w(g_k) \le w(A_n)$ for every independent set $X$, so $A_n$ is a maximum-weight independent set. $\blacksquare$
