---
title: The arc-eager system is sound and complete for projective trees, and every run ends after at most 2n transitions
proves: [correctness, termination]
status: full
---

The words are $1, \ldots, n$ and 0 is the root. A configuration is $(\sigma, \beta, A)$ with stack top $s$ and buffer front $b$; the buffer is always $[b, \ldots, n]$, since only SHIFT and RIGHT-ARC change it and both take the front. "Before time $t$" refers to the configurations of one run in order.

**Lemma 1 (invariant).** In every configuration of a run:

- (a) the stack is increasing in position from bottom to top, and its bottom is 0;
- (b) every word that has been popped from the stack has a head in $A$, and no word in the buffer has a head;
- (c) each word has at most one head, and no arc enters 0;
- (d) every head in $A$ of a stack word is a stack word below it;
- (e) $A$ has no cycle.

*Proof.* At the start all hold. (a): SHIFT and RIGHT-ARC push $b$, which is larger than every shifted word; pops keep the order; 0 is never popped, since LEFT-ARC and REDUCE need $s \ne 0$ (REDUCE needs a head, and 0 never has one by (c)). (b): LEFT-ARC pops $s$ after giving it a head, REDUCE pops only a word with a head, and the only arc into a buffer word is the one RIGHT-ARC adds when it moves the word to the stack. (c): LEFT-ARC needs $s$ without a head and $s \ne 0$; RIGHT-ARC gives a head to $b$, which has none by (b). (d): RIGHT-ARC gives $b$ the head $s$, directly below $b$ after the push; a stack word is never popped while words are above it, so the head stays below it on the stack. (e): LEFT-ARC adds $b \to s$; a cycle through the new arc would need a path of heads from $b$ up to $s$, but $b$ has no head. RIGHT-ARC adds $s \to b$; a cycle would need $b$ to be an ancestor of $s$, but by (d) all ancestors of $s$ are on the stack, and $b$ is not. $\square$

**Lemma 2 (no arc passes over a stack word).** If $p < v < q$, $v$ is on the stack in some configuration, and $A$ contains an arc between $p$ and $q$ in that configuration or later, then $v$ was not on the stack when the arc was added.

*Proof.* An arc is always added between the stack top and the buffer front, and the top is the smaller of the two, since the buffer holds only words larger than every shifted word. So when the arc was added, $p$ was the top and $q$ the front. Then $v < q$ had been shifted. If $v$ were on the stack at that time, (a) would give $v < p$, since $p$ is the top; but $p < v$. $\square$

**Theorem 3 (soundness and termination).** Every run ends after at most $2n$ transitions, and the arcs, with line L9, form a projective tree rooted at 0.

*Proof.* *No dead end and count.* While the buffer is not empty, SHIFT is legal. SHIFT and RIGHT-ARC remove one word from the buffer, so there are exactly $n$ of them. LEFT-ARC and REDUCE pop a word that was pushed by one of these, and each word is popped at most once, so there are at most $n$ of them. So the run ends, after at most $2n$ transitions, when the buffer is empty.

*Tree.* At the end, by (b) every word that is not on the stack has a head; line L9 gives a head 0 to every stack word without a head. With (c) every word has exactly one head and 0 has none. The arcs of line L9 cannot close a cycle, since they point from 0, which has no head; with (e) the whole set has no cycle. So following heads from any word ends at 0, and the arcs form a tree.

*Projective.* By the crossing form of projectivity, it is enough to show that no two arcs cross, with the root arcs included. Take two arcs, $(p, q)$ added before $(x, y)$, with $p < q$ and $x < y$, both added by LEFT-ARC or RIGHT-ARC. When $(x, y)$ was added, $x$ was the top and $y$ the front. If they crossed, one endpoint of $(p, q)$ would lie strictly between $x$ and $y$ and the other outside. The endpoint $q$ was the front at an earlier time, so $q \le y$. If $p < x < q < y$: when $(p, q)$ was added, $x < q$ had been shifted, and $x$ is on the stack later, at the time of $(x, y)$, so it was on the stack then too, since a popped word is never pushed again. That contradicts Lemma 2 for $v = x$. If $x < p < y < q$: impossible, since $q \le y$. The arcs of line L9 join 0 to a word $v$ that is on the stack at the end; an arc $(x, y)$ crosses $(0, v)$ only if $x < v < y$ with $x > 0$, which Lemma 2 forbids, and two arcs from 0 cannot cross. $\square$

**Theorem 4 (completeness).** For every projective tree $G$ with heads $h^\ast$, the static oracle produces a legal run whose final arcs, before line L9, are exactly $G$.

*Proof.* We show that the oracle run keeps two properties: (i) $A \subseteq G$; (ii) every arc of $G$ whose two endpoints are both smaller than $b$ is in $A$.

*Legality and (i).* The oracle is called only while the buffer is not empty, so SHIFT and RIGHT-ARC are legal. It chooses LEFT-ARC only when $h^\ast(s) = b$; then $s \ne 0$, and $s$ has no head. Indeed, by (i) a head of $s$ in $A$ would be $h^\ast(s) = b$; but an arc from a larger word to a smaller one is added only by LEFT-ARC, which pops the dependent, and $s$ is still on the stack. REDUCE is chosen only when $s$ has a head. Every arc added is a gold arc, so (i) holds.

*(ii).* LEFT-ARC and REDUCE do not move $b$ and only add arcs, so (ii) is kept. Consider a buffer move of $b$, by SHIFT or RIGHT-ARC. The new gold arcs with both endpoints below $b + 1$ are the arcs between $b$ and smaller words: the arc from a gold head $h = h^\ast(b) < b$, and the arcs to the gold dependents $d < b$ of $b$.

First, the dependents. Suppose $h^\ast(d) = b$ with $d < b$ and the arc not in $A$. Then $d$ has no head by (i), so by (b) it is on the stack. If $d = s$, the oracle would choose LEFT-ARC, not a buffer move. So $d < s < b$ by (a). The gold arc $b \to d$ passes over $s$, so $b$ dominates $s$ in $G$. The gold head $g = h^\ast(s)$ is not $b$, or the oracle would choose LEFT-ARC. It is not larger than $b$: the arc $g \to s$ would pass over $b$, so $g$ would dominate $b$, while $b$ dominates $s$ and hence its parent $g$. So $g < b$, and by (ii) the arc $g \to s$ is in $A$; $s$ has a head. A gold dependent $e \ge b$ of $s$ is impossible: $e = b$ would make $s$ the parent of $b$ and $b$ an ancestor of $s$; $e > b$ would make the arc $s \to e$ pass over $b$, so $s$ would dominate $b$, which dominates $s$. So the conditions of REDUCE hold, and the oracle, which tries REDUCE before SHIFT, would choose REDUCE. Its choice of RIGHT-ARC is also excluded, since RIGHT-ARC needs $h^\ast(b) = s$, while $b$ dominates $s$. This contradicts the buffer move.

Next, the head. Suppose $h = h^\ast(b) < b$ and the oracle moves $b$ without adding $h \to b$, so it chooses SHIFT and $h \ne s$. If $h$ had been popped, then by LEFT-ARC with a head $b' \le b$, or by REDUCE. REDUCE was impossible, since $b$, a gold dependent of $h$, was in the buffer. A LEFT-ARC gave $h$ the gold head $b'$: $b' = b$ would make $b$ and $h$ each other's parents, and $b' < b$ would make the gold arc $h \to b$ pass over $b'$, so $h$ would dominate its own parent. So $h$ is on the stack, and $h < s < b$. The gold arc $h \to b$ passes over $s$, so $h$ dominates $s$. The gold head $g = h^\ast(s)$ is not $b$ (the oracle would choose LEFT-ARC) and not larger than $b$ (the arc $g \to s$ would pass over $b$, so $g$ would dominate $b$ and its parent $h$, while $h$ dominates $s$ and its parent $g$; this forces $g = h < b$, a contradiction). So $g < b$ and by (ii) $s$ has a head. A gold dependent $e \ge b$ of $s$ is impossible: $e = b$ contradicts $h^\ast(b) = h \ne s$, and $e > b$ makes $s$ dominate $b$ and its parent $h$, while $h$ dominates $s$. So the oracle would choose REDUCE, a contradiction.

*End.* When the buffer is empty, $b = n + 1$, and (ii) says that every arc of $G$ is in $A$. With (i), $A = G$ before line L9, and line L9 adds nothing. $\square$

The tests check Theorems 3 and 4 by brute force: for $n \le 5$ they build all complete sequences and compare the trees with the projective trees found by a search over all head lists, and they check that the static oracle rebuilds every projective tree and fails on every other tree.
