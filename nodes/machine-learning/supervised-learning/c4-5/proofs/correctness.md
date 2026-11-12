---
title: C4.5 conserves case weights, stops, computes U_CF exactly and prunes to a tree whose estimate it returns
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. A case is $(x, y, w)$ with weight $w > 0$; the weight of a set of cases is the sum of their weights. Let $m > 0$ be the minimum number of cases (2 by default). At a node with cases $S$ of weight $W$ that tests attribute $a$, let $W_o$ be the weight of the cases with known outcome $o$, $W_K = \sum_o W_o$, and $W_u = W - W_K$ the weight with $a$ unknown. Line L6 sets $p_o = W_o / W_K$. Line L7 sends a known case to its outcome with its full weight, and an unknown case to every outcome $o$ with weight $w p_o$.

**Claim 1 (weights are conserved).** The child for outcome $o$ receives weight $W_o W / W_K$, and these add up to $W$. For each case, the weights of its copies over all leaves add up to its weight $w$.

*Proof.* The child for $o$ gets the known cases of outcome $o$, of weight $W_o$, and a fraction $p_o$ of each unknown case, of total weight $p_o W_u$. So its weight is $W_o + W_o W_u / W_K = W_o W / W_K$, and $\sum_o W_o W / W_K = W$. For one case of weight $w$: a known case goes to one child with weight $w$; an unknown case goes to all children with weights $w p_o$, and $\sum_o p_o = 1$. By induction on the height of the subtree, the copies of a case of weight $w$ that enters a node have total weight $w$ over the leaves below it. $\square$

**Claim 2 (growth stops).** Every child of a node of weight $W$ has weight at most $W - m$. So a node at depth $t$ has weight at most $W_0 - t m$, where $W_0$ is the total weight, and the tree has depth at most $W_0 / m - 1$.

*Proof.* Line L2 accepts a test only if at least two outcomes have known weight at least $m$ (for a numeric test, both sides). So for each outcome $o$ some other outcome has known weight at least $m$, and $W_o \le W_K - m$. By Claim 1 the child weight is $W_o W / W_K \le (W_K - m) W / W_K = W - m W / W_K \le W - m$, because $W \ge W_K$. Line L1 makes a leaf when $W < 2m$, so an internal node has weight at least $2m$; by induction an internal node at depth $t$ has $W_0 - t m \ge 2m$, so $t \le W_0/m - 2$, and its children have depth at most $W_0/m - 1$. Each call does finite work, so growth stops. $\square$

Without unknown values, the same argument shows that each child has at most $W - m$ of the weight, and each case reaches exactly one leaf.

**Claim 3 (class probabilities).** For every input $x$, possibly with missing values, the class probabilities that the tree returns are nonnegative and add up to 1.

*Proof.* By induction on the height. A leaf returns its normalized class weights, or probability 1 for its label when it has no cases. An internal node either follows one branch, or, for an unknown or unseen value, returns $\sum_o p_o P_o$ where each $P_o$ is a probability vector by induction and $p_o \ge 0$ with $\sum_o p_o = 1$. A convex combination of probability vectors is a probability vector. $\square$

**Claim 4 (the upper limit).** For $0 < \mathrm{CF} < 1$ and $0 \le E < N$, there is exactly one $p \in (0, 1)$ with $P(\mathrm{Bin}(N, p) \le E) = \mathrm{CF}$, which is $U_{\mathrm{CF}}(E, N)$. For $E = 0$ it equals $1 - \mathrm{CF}^{1/N}$. The bisection returns it to within $2^{-100}$.

*Proof.* For integer $E$ and $N$, the standard identity $P(\mathrm{Bin}(N, p) \le E) = 1 - I_p(E + 1, N - E)$ holds, where $I_p(\alpha, \beta) = \frac{1}{B(\alpha, \beta)} \int_0^p t^{\alpha - 1} (1 - t)^{\beta - 1} \, dt$; we use the right side as the definition for fractional $E$ and $N$. For $\alpha, \beta > 0$, the map $p \mapsto I_p(\alpha, \beta)$ is continuous and strictly increasing from 0 at $p = 0$ to 1 at $p = 1$, since its integrand is positive on $(0, 1)$. So $f(p) = 1 - I_p(E + 1, N - E)$ falls strictly from 1 to 0, and $f(p) = \mathrm{CF}$ has exactly one root in $(0, 1)$. The bisection keeps $f(\mathit{lo}) > \mathrm{CF} \ge f(\mathit{hi})$, which holds at the start, so the root stays in $[\mathit{lo}, \mathit{hi}]$, whose length halves 100 times. For $E = 0$, $f(p) = 1 - I_p(1, N) = (1 - p)^N$, and $(1 - p)^N = \mathrm{CF}$ gives $p = 1 - \mathrm{CF}^{1/N}$. $\square$

For each leaf with cases of weight $N$, of which weight $E$ is not of the leaf's label, the predicted errors are $N \cdot U_{\mathrm{CF}}(E, N)$; the estimate $\mathrm{est}(T, S)$ of a tree on cases $S$ is the sum of the predicted errors of its leaves, where $S$ is sent down the tree as in line L7.

**Claim 5 (pruning).** PRUNE$(T, S)$ stops and returns a tree $T'$ and a number $r$ with $r = \mathrm{est}(T', S)$. Without subtree raising, $r \le \mathrm{est}(T, S) + 0.1\, i(T)$, where $i(T)$ is the number of internal nodes of $T$.

*Proof.* We use induction on the number of nodes of $T$. If $T$ is a leaf, line L11 returns $T$ and its predicted errors, which is $\mathrm{est}(T, S)$. Otherwise line L12 prunes each branch $T_o$ on its cases $S_o$ and gets $(T'_o, r_o)$ with $r_o = \mathrm{est}(T'_o, S_o)$ by induction, since $T_o$ has fewer nodes. Let $E_{\mathrm{tree}} = \sum_o r_o$; this is the estimate of the node with the new branches on $S$, since the node sends $S$ down as $S_o$. Then there are three cases.

- Line L14 returns a leaf with the label of the node and the value $E_{\mathrm{leaf}}$, which is the estimate of that leaf on $S$.
- Line L15 returns PRUNE(largest branch, $S$). The branch is a proper subtree, so it has fewer nodes, and by induction the call stops and its value is the estimate of the tree it returns.
- Line L16 returns the node with value $E_{\mathrm{tree}}$, its estimate.

So $T'$ and $r$ satisfy $r = \mathrm{est}(T', S)$ in each case, and the recursion stops because each call is on a smaller tree.

Without raising, line L15 is never taken and $E_{\mathrm{branch}} = \infty$. Line L14 returns $E_{\mathrm{leaf}} \le E_{\mathrm{tree}} + 0.1$, and line L16 returns $E_{\mathrm{tree}}$, so $r \le E_{\mathrm{tree}} + 0.1$. By induction $r_o \le \mathrm{est}(T_o, S_o) + 0.1\, i(T_o)$, so
$$r \le \sum_o \mathrm{est}(T_o, S_o) + 0.1 \sum_o i(T_o) + 0.1 = \mathrm{est}(T, S) + 0.1\, i(T). \quad\blacksquare$$
