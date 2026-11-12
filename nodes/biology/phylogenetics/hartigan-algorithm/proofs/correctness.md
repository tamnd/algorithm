---
title: Hartigan's algorithm gives the parsimony score and all optimal states
proves: [correctness]
status: full
---

Let $T$ be a rooted tree with leaf states $x$, and let $\Sigma$ be the set of states that occur at the leaves. For a node $w$, write $T_w$ for its subtree, and $[P]$ for 1 if $P$ holds and 0 if not. For $a \in \Sigma$, let $c_w(a)$ be the least number of changes on the edges of $T_w$ over the labelings of $T_w$ that agree with $x$ at the leaves and give $w$ the state $a$ ($\infty$ if there is none). Let $s_w = \min_a c_w(a)$ and

$$g_w(a) = \min_b \bigl(c_w(b) + [a \ne b]\bigr),$$

the least number of changes on $T_w$ and on the edge above $w$ when the parent of $w$ has state $a$. As for Fitch's algorithm, a node $v$ with children $w_1, \ldots, w_d$ has

$$c_v(a) = \sum_{j = 1}^{d} g_{w_j}(a), \tag{1}$$

because the subtrees of the children can be labeled independently once $v$ has a state.

States outside $\Sigma$ can be left out. If a labeling gives some internal nodes a state $z \notin \Sigma$, change all nodes in state $z$ to one fixed state of $\Sigma$, and do this for each such $z$ in turn. An edge between two nodes in state $z$ had no change and still has none, and every other edge at such a node had a change before. So the number of changes does not grow, and the least value over labelings with states in $\Sigma$ is the parsimony score.

**Lemma 1 (first pass).** For every node $w$: (a) $U_w = \{a : c_w(a) = s_w\}$; (b) $g_w(a) = s_w + [a \notin U_w]$; (c) if $w$ is internal, $L_w = \{a : c_w(a) = s_w + 1\}$; (d) the amount that line L7 adds over the internal nodes of $T_w$ is $s_w$.

*Proof.* By induction in postorder. At a leaf, $c_w(x(w)) = 0$ and $c_w(a) = \infty$ otherwise, so $s_w = 0$, $U_w = \{x(w)\}$ and $g_w(a) = [a \ne x(w)]$, which gives (a), (b) and (d).

Let $v$ be internal with children $w_1, \ldots, w_d$. By (1) and (b) for the children,

$$c_v(a) = \sum_j s_{w_j} + \sum_j [a \notin U_{w_j}] = \sum_j s_{w_j} + d - n_v(a).$$

This is least exactly when $n_v(a)$ is largest, that is $n_v(a) = M$. So $s_v = \sum_j s_{w_j} + d - M$, and

$$c_v(a) = s_v + M - n_v(a). \tag{2}$$

By (2), $c_v(a) = s_v$ if and only if $n_v(a) = M$, which is (a) by line L6, and $c_v(a) = s_v + 1$ if and only if $n_v(a) = M - 1$, which is (c). Line L7 adds $d - M$ at $v$, and with (d) for the children the total in $T_v$ is $\sum_j s_{w_j} + d - M = s_v$, which is (d). For (b): if $a \in U_v$, then $g_v(a) \le c_v(a) = s_v \le g_v(a)$. If $a \notin U_v$, then $c_v(a) \ge s_v + 1$, and $c_v(b) + 1 \ge s_v + 1$ for every $b$, with equality for $b \in U_v$. So $g_v(a) = s_v + 1$. $\square$

So the score of line L13 is $s_{\text{root}}$, the parsimony score.

**Lemma 2 (one node, given its parent).** For an internal node $w$ and a state $a$, let $\operatorname{opt}(w \mid a)$ be the set of states $b$ that reach the minimum in the definition of $g_w(a)$. Then

$$\operatorname{opt}(w \mid a) = \begin{cases} \{a\} & \text{if } a \in U_w, \\ \{a\} \cup U_w & \text{if } a \in L_w, \\ U_w & \text{otherwise.} \end{cases}$$

For a leaf $w$, $\operatorname{opt}(w \mid a) = \{x(w)\}$.

*Proof.* For a leaf, $c_w(b)$ is finite only for $b = x(w)$. Let $w$ be internal. The value for $b$ is $c_w(b) + [a \ne b]$. By Lemma 1, $c_w(b)$ is $s_w$ on $U_w$, $s_w + 1$ on $L_w$, and at least $s_w + 2$ elsewhere.

If $a \in U_w$: $b = a$ gives $s_w$, and every $b \ne a$ gives at least $s_w + 1$. If $a \in L_w$: $b = a$ gives $s_w + 1$, each $b \in U_w$ gives $s_w + 1$, and every other $b$ gives at least $s_w + 2$; the minimum is $s_w + 1$ by Lemma 1 (b). Otherwise $b = a$ gives at least $s_w + 2$, each $b \in U_w$ gives $s_w + 1$, and the other $b$ give at least $s_w + 2$. $\square$

**Lemma 3 (the whole tree).** Let $\operatorname{Opt}(v)$ be the set of states that $v$ has in at least one labeling of $T$ with $s_{\text{root}}$ changes. Then $\operatorname{Opt}(\text{root}) = U_{\text{root}}$, and for each child $w$ of a node $v$,

$$\operatorname{Opt}(w) = \bigcup_{a \in \operatorname{Opt}(v)} \operatorname{opt}(w \mid a).$$

*Proof.* The root: a labeling with root state $a$ has at least $c_{\text{root}}(a)$ changes, and some labeling has exactly that many. So the root states of optimal labelings are the states with $c_{\text{root}}(a) = s_{\text{root}}$, which is $U_{\text{root}}$ by Lemma 1 (a).

For a labeling $\lambda$ of $T$, split its changes into those on $T_w$ and on the edge $(v, w)$, which we call the $w$-part, and the others. The $w$-part is $\operatorname{cost}(\lambda|_{T_w}) + [\lambda(v) \ne \lambda(w)]$, and the others do not depend on $\lambda$ inside $T_w$.

($\supseteq$) Let $\lambda$ be optimal with $\lambda(v) = a$, and let $b \in \operatorname{opt}(w \mid a)$. Replace $\lambda$ on $T_w$ by a labeling of $T_w$ with $w$ in state $b$ and $c_w(b)$ changes. The new $w$-part is $c_w(b) + [a \ne b] = g_w(a)$, and the old one was at least $g_w(a)$. So the new labeling is also optimal, and it gives $w$ the state $b$.

($\subseteq$) Let $\lambda$ be optimal, $a = \lambda(v)$ and $b = \lambda(w)$. If its $w$-part were larger than $g_w(a)$, the replacement above would give a labeling with fewer changes. So the $w$-part is $g_w(a)$. It is at least $c_w(b) + [a \ne b] \ge g_w(a)$, so $c_w(b) + [a \ne b] = g_w(a)$ and $b \in \operatorname{opt}(w \mid a)$, with $a \in \operatorname{Opt}(v)$. $\square$

**Lemma 4 (lines L10 to L12).** For a child $w$ of $v$, lines L10 to L12 compute $\bigcup_{a \in F_v} \operatorname{opt}(w \mid a)$.

*Proof.* For a leaf $w$, every $\operatorname{opt}(w \mid a)$ is $\{x(w)\} = U_w$, which is line L10; $F_v$ is not empty, since $F_{\text{root}} = U_{\text{root}}$ is not empty and each step below keeps a non-empty set. For an internal $w$, by Lemma 2, a state $a \in F_v$ contributes $a$ itself if and only if $a \in U_w \cup L_w$, which gives the set $F_v \cap (U_w \cup L_w)$ of line L11. It contributes the set $U_w$ if and only if $a \notin U_w$. So $U_w$ is in the union if and only if some $a \in F_v$ is outside $U_w$, which is the test of line L12. No other state is contributed. $\square$

**Theorem.** Hartigan's algorithm returns the parsimony score of $T$, and $F_v = \operatorname{Opt}(v)$ for every node $v$.

*Proof.* The score is $s_{\text{root}}$ by Lemma 1 (d). For the sets, use induction in the preorder of line L9. Line L8 gives $F_{\text{root}} = U_{\text{root}} = \operatorname{Opt}(\text{root})$ by Lemma 3. If $F_v = \operatorname{Opt}(v)$, then Lemma 4 and Lemma 3 give $F_w = \bigcup_{a \in \operatorname{Opt}(v)} \operatorname{opt}(w \mid a) = \operatorname{Opt}(w)$ for each child $w$. $\blacksquare$

**Remark (binary trees).** With $d = 2$, $M = 2$ if and only if the two upper sets meet, and then $U_v$ is their intersection; otherwise $M = 1$ and $U_v$ is their union. Line L7 adds 0 or 1 in the two cases. So Lemma 1 is also a proof of Fitch's first pass.
