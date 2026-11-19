---
title: The biaffine decoder returns a tree of maximum total arc score, which also maximizes the total head log probability, and the head loss has the gradient p minus the gold indicator
proves: [correctness, termination]
status: full
---

The words are $1, \ldots, n$ and 0 is the root. $S$ is an $(n + 1) \times (n + 1)$ matrix of real arc scores; $S[h][d]$ is the score of the arc $h \to d$, for $h \ne d$ and $d \ge 1$. A head list $(\mathrm{head}(1), \ldots, \mathrm{head}(n))$ with $\mathrm{head}(d) \ne d$ has the score $\sigma(\mathrm{head}) = \sum_{d = 1}^n S[\mathrm{head}(d)][d]$. It is a tree when following heads from every word reaches 0.

**Lemma 1 (the best heads).** Let $\mathrm{head}^\circ(d)$ be a head $h \ne d$ with the largest $S[h][d]$. Then $\sigma(\mathrm{head}^\circ) \ge \sigma(\mathrm{head})$ for every head list, so if $\mathrm{head}^\circ$ is a tree, it is a tree of maximum score.

*Proof.* The score is a sum of $n$ terms, the $d$-th of which depends only on $\mathrm{head}(d)$, and $\mathrm{head}^\circ(d)$ maximizes each term on its own. Every tree is a head list, so the bound holds over trees too. $\square$

**Lemma 2 (the repair).** If $\mathrm{head}^\circ$ is not a tree, Chu-Liu-Edmonds on the complete graph with weights $S[h][d]$ ($h \ne d$, $d \ge 1$) returns a spanning arborescence rooted at 0 of maximum weight, that is, a tree of maximum score.

*Proof.* A head list is a tree exactly when its arcs form a spanning arborescence rooted at 0: each word has one head, 0 has none, and every word reaches 0. Chu-Liu-Edmonds returns a maximum-weight spanning arborescence; this is proved on the [MST parsing](/mst-dependency-parsing/) page. The complete graph has one, for instance all words attached to 0. $\square$

**Theorem 3 (the decoder).** The decoder stops and returns a tree of maximum score among all $(n + 1)^{n - 1}$ trees.

*Proof.* Line L3 takes $n$ maxima over finite sets. The tree test of line L4 follows at most $n$ heads from each word. If the test succeeds, Lemma 1 gives optimality; otherwise Lemma 2 does, and Chu-Liu-Edmonds stops, because each contraction removes at least one node and the recursion ends on a graph with no cycle among its best entering arcs. $\square$

**Lemma 4 (scores and log probabilities).** Let $\log p(h \mid d) = S[h][d] - \log Z_d$ with $Z_d = \sum_{h' \ne d} e^{S[h'][d]}$. Then for every tree $T$, $\sum_d \log p(\mathrm{head}_T(d) \mid d) = \sigma(T) - \sum_d \log Z_d$, so a tree maximizes the total log probability exactly when it maximizes the total score.

*Proof.* Sum the definition over $d$. The second term, $\sum_d \log Z_d$, does not depend on $T$. $\square$

**Lemma 5 (the head prior).** $s(h, d) = a_h^\top U e_d + a_h^\top u$. The term $a_h^\top u$ adds the same number to every entry of row $h$. It does not change which dependent a fixed head scores highest, but it changes the softmax over heads in each column.

*Proof.* The term depends on $h$ only. $\square$

**Lemma 6 (the gradient).** Let $\ell = -\sum_{d = 1}^n \log p(h^\ast(d) \mid d)$ for gold heads $h^\ast$, and $q_d(h) = p(h \mid d) - [h = h^\ast(d)]$ for $h \ne d$. Then

$$\frac{\partial \ell}{\partial S[h][d]} = q_d(h), \qquad \frac{\partial \ell}{\partial U} = \sum_{d} \sum_{h \ne d} q_d(h)\, a_h e_d^\top, \qquad \frac{\partial \ell}{\partial u} = \sum_{d} \sum_{h \ne d} q_d(h)\, a_h.$$

*Proof.* The term of word $d$ is $-S[h^\ast(d)][d] + \log \sum_{h \ne d} e^{S[h][d]}$, and only it depends on the column $d$. Its derivative in $S[h][d]$ is $p(h \mid d) - [h = h^\ast(d)]$. Since $S[h][d] = \sum_{i, j} a_{h, i} U_{ij} e_{d, j} + \sum_i a_{h, i} u_i$, the derivatives of $S[h][d]$ in $U_{ij}$ and $u_i$ are $a_{h, i} e_{d, j}$ and $a_{h, i}$, and the chain rule gives the result. $\square$

The tests check Theorem 3 against a search over all trees for $n \le 5$, with cases in which the best heads form a cycle; Lemma 4 for $n \le 4$; Lemma 5 on random views; and Lemma 6 against central finite differences.
