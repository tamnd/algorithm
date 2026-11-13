---
title: QUIESCE returns a fail-soft bound of the quiescence value, and the exact value inside the window
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode QUIESCE of the page. Values are negamax values: EVALUATE$(n)$ is the static score for the side to move at $n$, and the score of a child is for the side to move there. Let $C(n)$ be the set of positions reached from $n$ by one capture. We assume that each chain of captures is finite. This holds in chess and in every game in which a capture removes a piece, because the number of pieces goes down at each capture.

The *capture height* $h(n)$ is 0 if $C(n)$ is empty and $1 + \max_{c \in C(n)} h(c)$ otherwise. It is finite, because the capture tree of $n$ is finite: it has finite branching and no infinite path (König's lemma).

**Definition.** The quiescence value of $n$ is
$$ Q(n) = \max\Bigl(\text{EVALUATE}(n),\ \max_{c \in C(n)} \bigl(-Q(c)\bigr)\Bigr), $$
with the inner maximum taken as $-\infty$ when $C(n)$ is empty. This is the negamax value of the *capture-or-stop game*, in which the side to move either makes a capture or stops, and a stop scores EVALUATE$(n)$.

We say that $r$ is a *fail-soft answer* for $Q(n)$ with the window $(\alpha, \beta)$, $\alpha < \beta$, when
$$ Q(n) \le r \le \alpha \ \text{ if } Q(n) \le \alpha, \qquad r = Q(n) \ \text{ if } \alpha < Q(n) < \beta, \qquad \beta \le r \le Q(n) \ \text{ if } Q(n) \ge \beta. $$

**Lemma 1 (the loop invariant).** In a call QUIESCE$(n, \alpha_0, \beta)$, after line L3 and after each turn of lines L5 to L8, the variable $m$ is the maximum of EVALUATE$(n)$ and of the exact values $-Q(c)$ or the bounds returned for the captures seen so far, and $\alpha = \max(\alpha_0, m)$.

*Proof.* Line L3 sets $m$ to the stand-pat score and raises $\alpha$ to it. Lines L6 and L8 keep both statements true when one more child is seen. $\square$

**Theorem 1 (termination and correctness).** For every $n$ and $\alpha < \beta$, the call QUIESCE$(n, \alpha, \beta)$ stops and returns a fail-soft answer for $Q(n)$.

*Proof.* By induction on $h(n)$. The calls go to captures only, and $h(c) < h(n)$ for each $c \in C(n)$, so the recursion stops.

Let $s = $ EVALUATE$(n)$. If $s \ge \beta$, line L2 returns $s$. Then $Q(n) \ge s \ge \beta$, so $\beta \le s \le Q(n)$, which is a fail-soft answer.

Otherwise $s < \beta$. Let the captures be $c_1, \ldots, c_k$ in the order of line L4, and let $\alpha_i$ and $m_i$ be the values of $\alpha$ and $m$ before the call on $c_i$. By Lemma 1, $\alpha_i = \max(\alpha, m_i)$ and $\alpha_i < \beta$, because the loop has not returned. The call on $c_i$ uses the window $(-\beta, -\alpha_i)$, and by the induction hypothesis it returns a fail-soft answer $r_i$ for $Q(c_i)$. So $t_i = -r_i$ satisfies
$$ t_i = -Q(c_i) \ \text{ if } \alpha_i < -Q(c_i) < \beta, \qquad -Q(c_i) \le t_i \le \alpha_i \ \text{ if } -Q(c_i) \le \alpha_i, \qquad \beta \le t_i \le -Q(c_i) \ \text{ if } -Q(c_i) \ge \beta. $$
The three cases give three facts. If $t_i \ge \beta$, then the third case holds and $t_i \le -Q(c_i)$. If $\alpha_i < t_i < \beta$, then the first case holds and $t_i = -Q(c_i)$. If $t_i \le \alpha_i$, then the second case holds and $-Q(c_i) \le t_i$.

*Case of a cutoff at line L7 after $c_j$.* Then $m = t_j \ge \beta$, because $m_j \le \alpha_j < \beta$. So $t_j \le -Q(c_j) \le Q(n)$, and the returned value $m$ lies in $[\beta, Q(n)]$.

*Case of no cutoff.* Line L9 returns $m = \max(s, t_1, \ldots, t_k) < \beta$, so no $t_i$ is at least $\beta$. By the second and third facts, $-Q(c_i) \le t_i$ for every $i$, so
$$ Q(n) = \max\bigl(s, -Q(c_1), \ldots, -Q(c_k)\bigr) \le \max(s, t_1, \ldots, t_k) = m. $$
If $m \le \alpha$, this is the first fail-soft condition. If $\alpha < m$, take the first term that reaches the final value of $m$. If it is $s$, it is a term of $Q(n)$. If it is $t_j$, then $t_j > m_j$ and $t_j > \alpha$, so $t_j > \alpha_j = \max(\alpha, m_j)$, and the second fact gives $t_j = -Q(c_j)$, again a term of $Q(n)$. So $Q(n) \ge m$, and $Q(n) = m$ with $\alpha < m < \beta$.

In all cases the answer is fail-soft. With the full window $(-\infty, +\infty)$, the middle case always holds, and QUIESCE returns $Q(n)$ exactly. $\square$

**Corollary 2 (quiescence equals the full search of the capture-or-stop game).** QUIESCE$(n, -\infty, +\infty)$ equals the [negamax](/negamax/) value of the game tree in which each node $n$ has the children $C(n)$ and one more leaf child, "stop", with the value EVALUATE$(n)$ for the side to move at $n$.

*Proof.* The negamax value of that tree satisfies the defining equation of $Q$, and the equation has one solution on a finite tree, by induction on $h(n)$. $\square$

**Theorem 3 (the depth-limited search).** Let SEARCH$(n, d, \alpha, \beta)$ be the fail-soft [alpha-beta](/alpha-beta-pruning/) search of the page, which returns EVALUATE$(n)$ at a node with no moves and calls QUIESCE at depth 0. Then it returns a fail-soft answer for the value $S_d(n)$ defined by $S_d(n) = $ EVALUATE$(n)$ at a terminal node, $S_0(n) = Q(n)$, and $S_d(n) = \max_c (-S_{d-1}(c))$ over all moves otherwise.

*Proof.* The search is the fail-soft alpha-beta procedure on the tree cut at depth $d$, with the value $Q$ at the frontier. Theorem 1 says that the frontier calls return fail-soft answers, and the proof of alpha-beta uses only this property of the values below the cut. $\square$

**Theorem 4 (cost).** QUIESCE$(n, \alpha, \beta)$ makes at most one call per node of the capture tree of $n$, and the number of calls active at the same time is at most $h(n) + 1$.

*Proof.* Each call calls QUIESCE only on the captures of its node, once each, so by induction no node of the capture tree is visited twice in one call tree. The active calls form one path of captures from $n$. $\blacksquare$
