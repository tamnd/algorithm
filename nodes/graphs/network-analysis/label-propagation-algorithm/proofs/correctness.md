---
title: Label propagation stops after at most m + 1 rounds with a stable labelling
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be an undirected simple graph with $n$ vertices and $m$ edges, and let $N(v)$ be the set of neighbours of $v$. For a labelling $\ell$, a vertex $v$ and a label $x$, let $c_\ell(v, x) = |\{w \in N(v) : \ell(w) = x\}|$. A labelling is *stable* when $c_\ell(v, \ell(v)) = \max_x c_\ell(v, x)$ for every $v$ with $N(v) \ne \emptyset$.

Let $\Phi(\ell) = |\{\{u, w\} \in E : \ell(u) = \ell(w)\}|$, the number of agreeing edges. Clearly $0 \le \Phi(\ell) \le m$.

**Lemma 1 (each change raises the potential).** If line L7 changes the label of $v$ from $a$ to $b$, then $\Phi$ grows by $c_\ell(v, b) - c_\ell(v, a) \ge 1$, where $\ell$ is the labelling just before the change.

*Proof.* Only the edges at $v$ can change status. Before the change, the edge $\{v, w\}$ agrees exactly when $\ell(w) = a$, which holds for $c_\ell(v, a)$ edges; after it, exactly when $\ell(w) = b$, which holds for $c_\ell(v, b)$ edges, since the labels of the neighbours do not change and $v \notin N(v)$. Line L6 ran just before with the counts of line L5, which are $c_\ell(v, \cdot)$, and found $c_\ell(v, a) < \max_x c_\ell(v, x)$; line L7 chose $b$ with $c_\ell(v, b) = \max_x c_\ell(v, x)$. Both counts are integers, so the difference is at least 1. $\square$

**Lemma 2 (termination).** The loop of lines L2 to L9 runs at most $m + 1$ times.

*Proof.* At the start, every label is distinct, so $\Phi = 0$. By Lemma 1 and $\Phi \le m$, line L7 changes a label at most $m$ times in the whole run. A round that sets $changed$ to true makes at least one change, so at most $m$ rounds do so. The first round that makes no change ends the loop at line L9, and it is at most round $m + 1$. $\square$

**Lemma 3 (stability at exit).** When the loop ends, the labelling is stable.

*Proof.* The loop ends after a round in which line L8 never ran, so no label changed during that round, and every vertex $v$ was visited once with the final labelling $\ell$. For each $v$ with a neighbour, the test of line L6 failed, so $c_\ell(v, \ell(v)) \ge \max_x c_\ell(v, x)$, where the maximum is over the labels of the neighbours and is at least 1. Then $c_\ell(v, \ell(v)) \ge 1$, so $\ell(v)$ is one of those labels, and the reverse inequality holds too. So $c_\ell(v, \ell(v)) = \max_x c_\ell(v, x)$. $\square$

**Lemma 4 (communities stay inside components).** At all times, every label $x$ that some vertex holds is a vertex of the same connected component as that vertex.

*Proof.* At the start, $\ell(v) = v$. Line L7 gives $v$ a label held by a neighbour of $v$, which by induction lies in the component of that neighbour, the component of $v$. $\square$

**Theorem.** LABEL-PROPAGATION($G$) stops after at most $m + 1$ rounds, for every random order and every random choice, and returns the classes of a stable labelling; each class lies inside one connected component of $G$.

*Proof.* Lemma 2 gives termination, Lemma 3 stability, and Lemma 4 that two vertices with equal labels lie in the same component as that label, hence in one component. $\square$

∎
