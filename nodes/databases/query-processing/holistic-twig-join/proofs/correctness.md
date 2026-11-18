---
title: TwigStack outputs every match exactly once, and for ancestor-descendant twigs every path solution is part of a match
proves: [correctness, termination, optimality]
status: full
---

We use the line numbers of the pseudocode. The document is a tree of elements with region codes $(\mathit{start}, \mathit{end}, \mathit{level})$ from one depth-first walk, so all start and end values are distinct and the intervals $[\mathit{start}, \mathit{end}]$ of two elements are either nested, when one element is an ancestor of the other, or disjoint. A *match* $m$ of the twig $Q$ maps each query node $q$ to an element $m(q)$ with the tag of $q$, so that for each edge from $p$ to $q$ the element $m(q)$ is a descendant of $m(p)$ (axis //) or a child of $m(p)$ (axis /). For a query node $q$, $Q_q$ is the subtree of $Q$ rooted at $q$.

For a query node $q$, $h(q)$ is the head of the stream $T_q$, $L(q)$ is its start and $R(q)$ its end, with $L(q) = R(q) = \infty$ when $T_q$ is exhausted. The node $q$ is *ended* when the streams of all leaves of $Q_q$ are exhausted. An element is *taken* from $T_q$ when the head moves past it: by a push (line L5), a skip (line L7) or a drop (line L12). For a match $m$, the element $m(q)$ is *waiting* while it is not yet taken from $T_q$; then $L(q) \le m(q).\mathit{start}$, because the stream is sorted by start.

**Invariant J.** For every match $m$ and every query node $q$:

- (J1) if $m(q)$ is taken, it was pushed, and if $q$ is not the root, $m(\mathit{parent}(q))$ was pushed before it;
- (J2) if $m(q)$ is taken and $m(l)$ is waiting for some leaf $l$ strictly below $q$, then $m(q)$ is in the stack $S_q$;
- (J3) if $q$ is not the root and $m(q)$ is in $S_q$, the pointer of its entry is at least the position of $m(\mathit{parent}(q))$ in $S_{\mathit{parent}(q)}$.

An entry keeps its position while it is in a stack, because stacks change only at the top. By J1, if $m(q)$ is waiting, then $m(y)$ is waiting for every $y$ in $Q_q$: the waiting nodes of a match are closed downward. In particular, no node of an ended subtree $Q_c$ has a waiting element in any match, since a waiting $m(y)$ would give a waiting leaf below $y$ whose stream is exhausted.

**Lemma 1 (getNext).** Suppose J holds when $\mathrm{getNext}(q)$ is called on a node $q$ that is not ended, and let $x$ be the node it returns. Then:

- (a) no drop at line L12 during the call takes an element $m(y)$ of a match $m$;
- (b) $L(x) < \infty$, and $x$ is a node of $Q_q$ that is not ended;
- (c) let $P = Q_q$ if $x = q$ and $P = Q_{\mathit{parent}(x)}$ otherwise; for every match $m$ and every $y$ in $P$ with $m(y)$ waiting, $L(x) \le m(y).\mathit{start}$;
- (d) if every edge of $Q_q$ has axis //, the heads $h(y)$ for $y$ in $Q_x$ form a match of $Q_x$.

*Proof.* By induction on the height of $q$. If $q$ is a leaf, then $x = q$ (line L9) and there is no drop. $T_q$ is not exhausted, since $q$ is not ended, and for $y = q$ a waiting $m(q)$ has $L(q) \le m(q).\mathit{start}$. Property (d) holds with one node.

Let $q$ be internal. At least one child is not ended, since $q$ is not ended. Line L10 calls getNext on each live child $c$ in turn. Drops in these calls take no match element by the induction hypothesis, so J still holds, and the waiting elements stay waiting. If a call returns $n \ne c$, then $\mathrm{getNext}(q)$ returns $n$, and (a) to (d) follow from the hypothesis for $c$, because $\mathit{parent}(n)$ is in $Q_c$.

Otherwise every live child $c$ returned $c$, so $L(c) < \infty$ and $L(c) \le m(y).\mathit{start}$ for each waiting $m(y)$ with $y$ in $Q_c$. Later calls on other children change only heads of other subtrees, so these facts still hold. Line L11 chooses the live child $n_{\min}$ with the smallest $L$ and sets $\mathit{far}$ to the largest $L(c)$ over all children, with $\infty$ for an ended child.

(a) Suppose line L12 drops $h(q)$, so $R(q) < \mathit{far}$, and $h(q) = m(q)$ for a match $m$, so that $m(q)$ is waiting. If some child $c$ is ended, then $m(l)$ is taken for a leaf $l$ of $Q_c$, and by J1 so is $m(q)$, which is false. If no child is ended, let $c$ be a child with $L(c) = \mathit{far}$. Then $m(c)$ is waiting, and $L(c) \le m(c).\mathit{start} < m(q).\mathit{end} = R(q) < \mathit{far} = L(c)$, which is false. After a drop, J still holds, so the same argument applies to the next head.

(b) Line L13 returns $q$ only when $L(q) < L(n_{\min}) < \infty$, and otherwise it returns $n_{\min}$, which is live with $L(n_{\min}) < \infty$.

(c) Let $m$ be a match and $y$ a node with $m(y)$ waiting. There is no such $y$ in an ended subtree. If $x = q$: for $y = q$, $L(q) \le m(q).\mathit{start}$, because by (a) the drops did not pass $m(q)$; for $y$ in $Q_c$ with $c$ live, $L(q) < L(n_{\min}) \le L(c) \le m(y).\mathit{start}$. If $x = n_{\min}$, then $\mathit{parent}(x) = q$ and $P = Q_q$: for $y = q$, $L(n_{\min}) \le L(q) \le m(q).\mathit{start}$, and for $y$ in $Q_c$, $L(n_{\min}) \le L(c) \le m(y).\mathit{start}$.

(d) If $x = n_{\min}$, use the hypothesis for $n_{\min}$. If $x = q$, no child is ended, because then $\mathit{far} = \infty$, line L12 exhausts $T_q$, and $q$ is not returned. For each child $c$, $L(q) < L(c)$, and $R(q) \ge \mathit{far} \ge L(c)$, with $R(q) \ne L(c)$ because codes are distinct. So $h(c)$ starts inside the interval of $h(q)$, and since the intervals are nested or disjoint, $h(c)$ is a descendant of $h(q)$. With the matches of each $Q_c$ formed by the heads, from the hypothesis, the heads form a match of $Q_q$. $\square$

**Theorem 1 (completeness).** J holds during the whole run, and for every match $m$ and every leaf $l$, the path solution of $m$ on the path from the root to $l$ is output.

*Proof.* At the start nothing is taken, so J holds. Consider one iteration, with $x = \mathrm{getNext}(\mathit{root})$ at line L2, $s = L(x) < \infty$ by Lemma 1(b), and $p = \mathit{parent}(x)$ when $x$ is not the root. Let $P$ be as in Lemma 1(c), so $P = Q_p$, or all of $Q$ when $x$ is the root.

*Line L3.* cleanStack pops from $S_p$ only entries with end below $s$. Suppose it pops $m(p)$ while $m(l)$ is waiting for a leaf $l$ below $p$. Since $l$ is in $P$, Lemma 1(c) gives $s \le m(l).\mathit{start} < m(p).\mathit{end} < s$, which is false. So J2 holds after line L3.

*Lines L4 and L5.* Suppose $h(x) = m(x)$ for a match $m$. If $x$ is not the root, then $m(p)$ is taken: otherwise it is waiting, and Lemma 1(c) gives $s \le m(p).\mathit{start} < m(x).\mathit{start} = s$. So $m(p)$ was pushed by J1, and since $m(x)$ and all leaves below $x$ are waiting, $m(p)$ is in $S_p$ by J2. So $S_p$ is not empty and $m(x)$ is pushed, not skipped. The cleanStack of $S_x$ in line L5 keeps every $m'(x)$ that has a waiting leaf below it, by the argument of line L3, since that leaf is in $P$. The new entry points to the top of $S_p$, at least the position of $m(p)$, which gives J3. So J1, J2 and J3 hold after line L5.

*Line L7.* By the above, a skipped head is not $m(x)$ for any match $m$, so J1 holds. Drops keep J by Lemma 1(a).

*Line L6.* Let $x$ be a leaf with $h(x) = m(x)$. Before the push, $m(x)$ is waiting, so by J1 and J2 every $m(q)$ on the path from the root to $x$, except $m(x)$, is in its stack. By J3 the pointer of each entry on this path is at least the position of the element of the parent. The output step visits every entry of the parent stack at a position up to the pointer, keeps those that satisfy the edge, and continues from the pointer of each. So it visits $m(p)$, then the element of the parent of $p$, and so on up to the root, and it outputs the path solution of $m$.

The loop ends when the root is ended, that is, when all leaf streams are exhausted. Then every $m(l)$ is taken, so by J1 it was pushed, and its path solution was output at line L6. $\square$

**Theorem 2 (correctness and termination).** TwigStack ends, and it outputs every match of $Q$ exactly once and nothing else.

*Proof.* Each iteration takes an element from a stream that is not exhausted (line L5 or L7), by Lemma 1(b), and each drop takes one, so the run ends after at most $\sum_q |T_q|$ iterations. Each output path solution takes its elements from the streams of the path, so the tags are right, and line L6 checks every edge of the path, so it is an embedding of the path. A stack holds distinct elements, and each leaf element is pushed once, so each path solution is output once. Line L8 joins the path solutions on the shared query nodes. The result is the set of maps whose restriction to every root-to-leaf path is an output path solution. Every edge of $Q$ lies on some root-to-leaf path, so each such map is a match, and by Theorem 1 every match is in the result, once. $\blacksquare$

**Theorem 3 (no useless path solutions).** If every edge of $Q$ has axis //, every path solution that TwigStack outputs is the restriction of a match to its path. So for each leaf the number of path solutions is at most the number of matches.

*Proof.* Let $(e_0, \dots, e_t)$ be an output path solution on the path $q_0, \dots, q_t$ from the root to the leaf $q_t$. Each $e_i$ was pushed at a time when getNext returned $q_i$ and $e_i = h(q_i)$. By Lemma 1(d), at that time the heads of $Q_{q_i}$ formed a match $\mu_i$ of $Q_{q_i}$ with $\mu_i(q_i) = e_i$. Define $m(q_i) = e_i$, and for each child $c$ of $q_i$ that is not $q_{i+1}$, let $m$ agree with $\mu_i$ on $Q_c$. Each node of $Q$ is on the path or in exactly one such $Q_c$. The edges of the path hold because line L6 checked them; an edge from $q_i$ to $c$ holds because $\mu_i(c)$ is a descendant of $\mu_i(q_i) = e_i$; and the edges inside $Q_c$ hold because $\mu_i$ is a match. So $m$ is a match whose restriction to the path is the path solution. Distinct path solutions of one leaf are restrictions of distinct matches. $\blacksquare$

With an edge of axis /, Lemma 1(d) fails: the heads are nested, but not necessarily parent and child. In the document $a(b(c))$ and the twig with root $a$, a child $b$ on an edge //, and a child $c$ on an edge /, TwigStack pushes $a$ because $c$ lies inside it, outputs the path solution $(a, b)$, and finds no match, because $c$ is not a child of $a$.
