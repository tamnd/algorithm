---
title: WTO builds a weak topological ordering, and the recursive strategy stops at a post-fixed point
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode on the main page. A vertex is *done* when its DFN is $+\infty$. For a list $L$ of elements and a vertex $u$ in it, $\omega_L(u)$ is the set of heads of the components of $L$ (at any depth) that contain $u$. For the full WTO this is $\omega(u)$. If $(h, C)$ is an element of $L$ and $u$ is in $C$, then

$$ \omega_L(u) = \{h\} \cup \omega_C(u), \qquad \omega_L(h) = \{h\}. \tag{1} $$

The vertices of one element are next to each other in the flattened order, with the head first.

## Part 1. The searches

A *search* $\Sigma(W, s_1, \ldots, s_q)$ is a run of VISIT$(s_i, P)$ for $i = 1, \ldots, q$ in turn, on one list $P$, where the call for $s_i$ is skipped if $\mathit{DFN}[s_i] \ne 0$ at that time. WTO is the search $\Sigma(V, r)$. COMPONENT$(h)$ is the search $\Sigma(S \setminus \{h\}, \mathit{succ}(h))$ for the set $S$ named in Lemma 2. We say that a search starts in a *clean state* when

- (C1) every vertex of $W$ has DFN 0,
- (C2) every edge from a vertex of $W$ goes to a vertex of $W$ or to a done vertex,
- (C3) every DFN already on the stack is smaller than every number that the search will give.

(C3) holds always, because $\mathit{num}$ only grows. Let $R$ be the set of vertices of $W$ that the start vertices reach by paths inside $W$.

**Lemma 1 (Tarjan).** In a search from a clean state, VISIT behaves as Tarjan's algorithm on the graph $G[W]$, with the edges to done vertices left out. In particular, as shown on the [Tarjan page](/tarjan-scc/):

- (T1) VISIT$(v)$ returns $\mathit{DFN}[v]$ if and only if $v$ is the first vertex of its strongly connected component (SCC) of $G[R]$ that the search reaches;
- (T2) at that time the vertices on the stack from $v$ upward are exactly the SCC of $v$;
- (T3) if an edge of $G[R]$ goes from the SCC $A$ to another SCC $B$, then the root of $B$ reaches line L10 before the root of $A$;
- (T4) VISIT$(v)$ returns the least of $\mathit{DFN}[v]$ and the numbers $\mathit{DFN}[b]$ of the vertices $b$ on the stack that an edge $a \to b$ of the search tree below $v$ reaches.

*Proof.* Line L8 uses the returned value of a tree child and the DFN of any other successor. A successor $w$ that is on the stack has a finite DFN, which is Tarjan's rule. A done successor gives $+\infty$, which never passes the test of line L9, so the edge has no effect. This is Tarjan's rule for a vertex of a finished component. An edge out of $W$ goes to a done vertex by (C2). Tarjan's algorithm uses the numbers only to compare them, so (C3) makes the numbers that are already on the stack harmless; the search never reaches those vertices anyway, by (C2). The only other difference is lines L13 and L14, and Lemma 2 shows that when line L14 ends, the vertices popped at line L13 are done and the stack is as Tarjan's algorithm leaves it. So the state that the rest of the search sees is the state of Tarjan's algorithm. $\square$

**Lemma 2.** Let a search $\Sigma(W, \ldots)$ start in a clean state. When it ends:

- (a) every vertex of $R$ is done, every other vertex has its old DFN, and the stack is as at the start;
- (b) the elements of $P$ correspond one to one to the SCCs of $G[R]$, in an order such that every edge of $G[R]$ goes from an element to the same element or to a later one;
- (c) the element of an SCC $S$ is the vertex $v$ if $S = \{v\}$ and $v \to v$ is not an edge; otherwise it is a component $(h, C)$, where $h$ is the first vertex of $S$ that the search reaches, and $C$ is the result of the search $\Sigma(S \setminus \{h\}, \mathit{succ}(h))$, which starts in a clean state.

*Proof.* By strong induction on $|W|$. Assume the claim for all smaller sets.

*The loop flag.* Let $v$ be a root, so VISIT$(v)$ reaches line L10 with $\mathit{head} = \mathit{DFN}[v]$. The variable $\mathit{head}$ only goes down, so no successor gave a value below $\mathit{DFN}[v]$, and $\mathit{loop}$ is true if and only if some successor gave exactly $\mathit{DFN}[v]$. Let $S$ be the SCC of $v$. If $v \to v$ is an edge, line L8 gives $\mathit{DFN}[v]$ for it. If $|S| \ge 2$, some edge $u \to v$ has $u \in S$ and $u \ne v$. All of $S$ lies in the search tree below $v$, so $u$ lies below some tree child $w$ of $v$, and $v$ is on the stack when the edge $u \to v$ is examined. By (T4) VISIT$(w)$ returns at most $\mathit{DFN}[v]$, so it returns exactly $\mathit{DFN}[v]$. In the other direction, if a successor $w$ gives $\mathit{DFN}[v]$, then either $w = v$, or by (T4) the tree below $w$ has an edge to $v$, so $v$ is on a cycle. So $\mathit{loop}$ is true if and only if $S$ is not a single vertex without a self-loop.

*The elements.* By (T1) line L10 holds once per SCC, at its first vertex $h$. By (T2) the vertices above $h$ on the stack are $S \setminus \{h\}$. If $\mathit{loop}$ is false, $S = \{h\}$, line L11 makes $h$ done, and line L15 adds the vertex $h$. If $\mathit{loop}$ is true, line L11 makes $h$ done, and line L13 pops $S \setminus \{h\}$ and sets their DFN to 0. So the search $\Sigma(S \setminus \{h\}, \mathit{succ}(h))$ of line L14 starts with (C1). For (C2), let $a \to b$ be an edge with $a \in S \setminus \{h\}$. If $b \in S$, then $b = h$, which is done, or $b \in S \setminus \{h\}$. If $b \notin S$, then $b$ is not on the stack: a vertex on the stack below $h$ reaches $h$ (Tarjan's stack invariant), so it would be in $S$. And $b$ has a nonzero DFN, because the search tree below $h$ has examined the edge $a \to b$. So $b$ is done. Thus the inner search starts in a clean state, and $|S \setminus \{h\}| < |S| \le |W|$, so the claim holds for it.

Every vertex of $S \setminus \{h\}$ is reached by the inner search. Take $u \in S \setminus \{h\}$ and a shortest path from $h$ to $u$ in $G[S]$. It visits $h$ only at its start, so its second vertex is in $\mathit{succ}(h)$ and the rest of the path stays in $S \setminus \{h\}$. So by (a) for the inner search, all of $S \setminus \{h\}$ is done when line L14 ends, and the stack is back to its state after line L13, which is Tarjan's state after it pops $S$. This is what Lemma 1 needs.

*The order.* Each element goes to the front of $P$ when its root reaches line L14 or L15. By (T3), if an edge goes from SCC $A$ to SCC $B \ne A$, the element of $B$ is added first, so it ends up after the element of $A$. This is (b).

*Part (a).* Every vertex of $R$ is in some SCC, so it is either a root made done at line L11 or a vertex of some $S \setminus \{h\}$ made done by the inner search. VISIT pushes and pops each vertex once per search, so the stack is restored. The search changes no DFN outside $R$, because by (C2) it only reaches vertices of $W$ or done vertices. $\square$

**Theorem 1.** WTO$(G, r)$ returns a weak topological ordering of the set $V_r$ of vertices reachable from $r$.

*Proof.* WTO is the search $\Sigma(V, r)$, which starts in a clean state, and its set $R$ is $V_r$. We show by strong induction on $|W|$ that the list $P$ of any search from a clean state has two properties.

*It is a hierarchical ordering of $R$.* By (b) and (c), the elements cover the SCCs of $G[R]$, which partition $R$. A vertex element holds one vertex. A component element of $S$ holds $h$ and, by induction, each vertex of $S \setminus \{h\}$ once.

*Every edge $u \to v$ with $u, v \in R$ satisfies the WTO condition with $\omega_P$.* Let $e_u$ and $e_v$ be the elements of $P$ that contain $u$ and $v$.

1. $e_u \ne e_v$. By (b) $e_u$ comes before $e_v$, so $u \prec v$. The heads in $\omega_P(u)$ lie in $e_u$, and $v$ does not, so $v \notin \omega_P(u)$. The edge is forward.
2. $e_u = e_v$ is a vertex. Then $u = v$ and $u \to u$ is a self-loop, which (c) rules out. This case does not occur.
3. $e_u = e_v = (h, C)$ and $v = h$. The head comes first in its element, so $h \preceq u$, and $h \in \omega_P(u)$ by (1). The edge is backward. This includes the self-loop $h \to h$.
4. $e_u = e_v = (h, C)$, $u = h$ and $v \ne h$. Then $v$ is in $C$, so $h \prec v$, and $\omega_P(h) = \{h\}$ does not hold $v$. The edge is forward.
5. $e_u = e_v = (h, C)$ and $u, v \ne h$. Both are in $C$, the edge lies in $G[S \setminus \{h\}]$, and the inner search reaches both. By induction the edge satisfies the condition in $C$. The order of $P$ restricted to $C$ is the order of $C$, and by (1) $\omega_P(u) = \{h\} \cup \omega_C(u)$ with $v \ne h$. So a forward edge of $C$ ($u \prec v$, $v \notin \omega_C(u)$) is forward in $P$, and a backward edge of $C$ ($v \preceq u$, $v \in \omega_C(u)$) is backward in $P$.

For the top level, every edge out of a vertex of $V_r$ ends in $V_r$, so every such edge is covered. $\square$

**Theorem 2.** Every cycle of $G$ through a vertex of $V_r$ contains a head of the WTO.

*Proof.* All the vertices of the cycle are in $V_r$. Let $u$ be the last of them in the order, and let $v$ be the vertex after $u$ on the cycle. Then $v \preceq u$, so the edge $u \to v$ is not forward, and by Theorem 1 it is backward: $v \in \omega(u)$. So $v$ is a head. $\square$

So removing the heads leaves a graph without cycles. This is the first half of Bourdoncle's result: the heads are an admissible set of widening points.

## Part 2. The recursive strategy

Assume that every $F_v$ is monotone and reads only $x[u]$ for the predecessors $u$ of $v$. Assume that $\nabla$ is a widening: $a \sqsubseteq a \nabla b$ and $b \sqsubseteq a \nabla b$, and for every increasing chain $y_0 \sqsubseteq y_1 \sqsubseteq \cdots$ the sequence $z_0 = y_0$, $z_{j+1} = z_j \nabla y_{j+1}$ is constant from some index on. All values start at $\bot$. A vertex outside $V_r$ is never assigned, so its value stays $\bot$.

**Lemma 3 (values only grow).** No assignment of ITERATE makes a value smaller: after each assignment the new value is $\sqsupseteq$ the old one.

*Proof.* By induction on the number of assignments. At lines L24 and L29, $x[h] \sqsubseteq x[h] \nabla t$. At line L22, the old value of $x[v]$ is $\bot$ or $F_v(x')$ for the state $x'$ of the last assignment to $v$. By induction $x' \sqsubseteq x$ at every vertex, so by monotonicity $F_v(x') \sqsubseteq F_v(x)$. $\square$

**Lemma 4 (finitely many changes at a head).** Over any run, the value of a head $h$ changes only finitely many times.

*Proof.* Only lines L24 and L29 for the component of $h$ assign $x[h]$. Let $t_1, t_2, \ldots$ be the values of $F_h(x)$ used by these assignments, in time order. By Lemma 3 the states grow, so $t_1 \sqsubseteq t_2 \sqsubseteq \cdots$ by monotonicity. The values of $x[h]$ are $z_0 = \bot$ and $z_j = z_{j-1} \nabla t_j$, the widened sequence of the chain $\bot \sqsubseteq t_1 \sqsubseteq t_2 \sqsubseteq \cdots$. If the chain is infinite, the sequence is constant from some index on. Either way it changes finitely often. $\square$

**Theorem 3 (termination).** ITERATE$(P)$ stops for every WTO $P$.

*Proof.* By induction on the depth of nesting of $P$. If $P$ has no component, it makes one assignment per element. Otherwise take a component $(h, C)$ of $P$. By induction every call ITERATE$(C)$ stops. Consider one run of the loop of lines L25 to L29. Each round that does not leave the loop has $t \not\sqsubseteq x[h]$ at line L28. Then line L29 gives $x[h] \nabla t \sqsupseteq t$, which differs from the old $x[h]$, so the value of $h$ changes. If the loop never ended, $h$ would change infinitely often, against Lemma 4. So each element of $P$ is processed in finite time, and $P$ has finitely many elements. $\square$

**Lemma 5 (who comes after whom).** Let $u \to v$ be an edge with $u, v \in V_r$.

- (i) If $v$ is not a head, then every assignment to $u$ is followed later by an evaluation of $F_v$ at line L22.
- (ii) If $v$ is the head of the component $c$ and $u$ is not in $c$, then every assignment to $u$ is followed later by a test of line L28 for $c$.

*Proof.* In both cases the edge is forward by Theorem 1. For (i), $v \notin \omega(u)$ because $v$ is not a head, and $v \preceq u$ would need $v \in \omega(u)$. For (ii), a backward edge to $v$ needs $v \in \omega(u)$, which means $u$ is in $c$. So $u \prec v$ and $v \notin \omega(u)$.

Let $L$ be the body of the innermost component that contains both $u$ and $v$, or the whole WTO if there is none. Write $g$ for its head, if it has one.

If $u = g$, then $v$ is in the body $L$. Every assignment to $g$ is at line L24 or L29, and both are followed by a call ITERATE$(L)$, which processes the element of $L$ that contains $v$.

Otherwise $u$ and $v$ are in $L$, in elements $e_u$ and $e_v$ of $L$. These differ: a component element holding both would contradict the choice of $L$, and a vertex element holding both would mean $u = v$ with a self-loop, so $v$ would be a head with $u$ in its component. Since $u \prec v$, $e_u$ comes before $e_v$. Every assignment to $u$ happens while ITERATE processes $e_u$ in some pass over $L$, and that pass then processes $e_v$, by Theorem 3 to its end.

It remains to see what processing $e_v$ does. A component is processed by at least one pass over its body, and each pass processes every element of the body. So processing $e_v$ reaches line L22 for $v$ in case (i), since $v$ is not a head and so is a vertex element at some depth. In case (ii), $c$ is $e_v$ or lies inside $e_v$, and every processing of $c$ ends with a test of line L28 that passes, by Theorem 3. $\square$

**Theorem 4 (post-fixed point).** When ITERATE ends, the final values $x$ satisfy $F_v(x) \sqsubseteq x[v]$ for every $v \in V_r$.

*Proof.* Let $v$ be a vertex that is not a head, and let $T$ be the time of its last evaluation at line L22, with state $x_T$. By Lemma 5 (i), no predecessor of $v$ in $V_r$ is assigned after $T$, and predecessors outside $V_r$ never change. $F_v$ reads only the predecessors, so $F_v(x) = F_v(x_T) = x[v]$.

Let $v = h$ be the head of the component $c$, and let $T$ be the time of the last test of line L28 for $c$. That test passed, since the run ended: $F_h(x_T) \sqsubseteq x_T[h]$. After $T$, $c$ is never processed again, since each processing ends with such a test. Every assignment to a vertex of $c$ happens while $c$ is processed, so no vertex of $c$, $h$ included, changes after $T$. A predecessor $u$ of $h$ outside $c$ is not assigned after $T$ by Lemma 5 (ii). Hence $F_h(x) = F_h(x_T) \sqsubseteq x_T[h] = x[h]$. $\square$

Theorems 2, 3 and 4 together are Bourdoncle's result: widening only at the heads of a WTO, with the recursive strategy, gives an iteration that stops, and that ends at an element $x$ with $F(x) \sqsubseteq x$, which the Cousots call a post-fixed point and the [Knaster-Tarski page](/knaster-tarski-theorem/) calls a pre-fixed point. When each $F_v$ is a sound abstraction of the concrete step, such an element over-approximates the [collecting semantics](/collecting-semantics/), by the local condition proved on the [abstract domain](/abstract-domain/) page. $\blacksquare$
