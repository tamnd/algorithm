---
title: The reaching-definitions iteration and the block scan build exactly the def-use chains
proves: [correctness, termination]
status: full
---

**Setting.** A program has blocks with instructions and one terminator each, and an entry block. A *point* is $(b, i)$ for $0 \le i \le n_b$, where $n_b$ is the number of instructions of $b$: for $i < n_b$ it is instruction $i$ of $b$, and $(b, n_b)$ is the terminator. The point graph has the edges $(b, i) \to (b, i + 1)$ for $i < n_b$ and $(b, n_b) \to (c, 0)$ for every successor $c$ of $b$. Add a start point $\sigma$ with the single edge $\sigma \to (\mathit{entry}, 0)$. A *definition site* is a point that defines a name $x$, written $d = (b, i, x)$; a parameter $x$ is the site $(\mathit{entry}, -1, x)$, placed at $\sigma$. The point *after* $d$ is $(b, i + 1)$, or $(\mathit{entry}, 0)$ for a parameter. A phi instruction at a point defines its name there, like any other instruction.

**Definition.** A path $\pi$ of points is *clear for $x$* if no point of $\pi$ except possibly its last one defines $x$. The definition $d$ of $x$ *reaches* a point $q$ if some path clear for $x$ goes from the point after $d$ to $q$, with $q$ itself allowed to define $x$. It *reaches the end* of a block $p$ if it reaches $(p, n_p)$; the terminator defines nothing. The chains are the pairs $(d, u)$ for a use $u$ of $x$ such that:

- $u = (b, i, x)$ where point $(b, i)$ is not a phi and reads $x$, and $d$ reaches $(b, i)$; or
- $u = (b, i, x)$ where point $(b, i)$ is a phi whose operand for the predecessor $p$ is $x$, and $d$ reaches the end of $p$.

The function returns $du[d]$, the uses $u$ with $(d, u)$ a chain, and $ud[u]$, the definitions $d$ with $(d, u)$ a chain. So $du$ and $ud$ are the same relation read in two directions, and it is enough to show that the set of pairs is right.

**Block summaries.** For a block $b$, $GEN[b]$ holds, for each name defined in $b$, the site of its last definition in $b$, and $KILL[b]$ is the set of names defined in $b$. $P$ is the set of parameter sites. Let $RIN[b]$ be the set of definitions that reach $(b, 0)$ and $ROUT[b]$ the set that reach the end of $b$. Write $name(d)$ for the name that $d$ defines.

**Lemma 1 (the equations).** $RIN$ and $ROUT$ satisfy

$$IN[b] = [b = \mathit{entry}]\,P \;\cup \bigcup_{p \in pred(b)} OUT[p], \qquad OUT[b] = GEN[b] \cup \{d \in IN[b] : name(d) \notin KILL[b]\},$$

and every other solution $(IN, OUT)$ has $RIN[b] \subseteq IN[b]$ and $ROUT[b] \subseteq OUT[b]$ for all $b$. So they are the least solution.

*Proof.* *They are a solution.* The points with an edge into $(b, 0)$ are the ends of the predecessors of $b$, and $\sigma$ if $b$ is the entry. A path clear for $x$ from the point after $d$ to $(b, 0)$ either has length 0, which happens only for a parameter and $b = \mathit{entry}$, or its last but one point is the end of a predecessor $p$, and the part up to it is a path clear for $x$ that ends at a point defining nothing. This gives $RIN[b] = [b = \mathit{entry}]\,P \cup \bigcup_p ROUT[p]$, and the converse direction is the same argument read backwards. For $ROUT[b]$, a path clear for $x$ to $(b, n_b)$ from the point after $d$ either starts inside $b$, after $d = (b, i, x)$, and then no later point of $b$ defines $x$, so $d \in GEN[b]$; or it passes through $(b, 0)$, its part up to $(b, 0)$ shows $d \in RIN[b]$, and then the whole block is passed without a definition of $x$, so $x \notin KILL[b]$. Conversely each such $d$ gives such a path. (A path that starts inside $b$ and later passes $(b, 0)$ falls under the second case; the first case uses its last visit to $b$.)

*They are the least solution.* Let $(IN, OUT)$ be a solution. We show by induction on the number of points of the path that if a path clear for $x$ goes from the point after $d$ to $(b, 0)$ then $d \in IN[b]$, and if it goes to $(b, n_b)$ then $d \in OUT[b]$. For $(b, 0)$: the path has length 0 and $d \in P \subseteq IN[\mathit{entry}]$, or its part up to the end of a predecessor $p$ is shorter, so $d \in OUT[p] \subseteq IN[b]$. For $(b, n_b)$: look at the last time the path is at $(b, 0)$. If there is none, the path lies in $b$ after $d$, and $d \in GEN[b] \subseteq OUT[b]$. Otherwise the part up to that point is shorter, so $d \in IN[b]$, and the rest crosses $b$ without a definition of $x$, so $name(d) \notin KILL[b]$ and $d \in OUT[b]$. $\square$

**Lemma 2 (the iteration).** Lines L2 to L7 stop, and when they stop, $IN = RIN$ and $OUT = ROUT$. The number of passes is at most $B \cdot D + 1$, where $B$ is the number of blocks and $D$ the number of definition sites.

*Proof.* Let $F$ be the map that takes the $OUT$ sets to new $IN$ and $OUT$ sets by the equations. It is monotone: larger $OUT$ sets give larger $IN$ sets and then larger $OUT$ sets. Two invariants hold at all times.

(i) $OUT[b] \subseteq ROUT[b]$ for all $b$. At the start $OUT[b] = GEN[b]$, and $GEN[b] \subseteq ROUT[b]$, because the last definition of $x$ in $b$ reaches the end of $b$ along the rest of $b$. An update computes $IN[b]$ and $OUT[b]$ from sets that lie below $(RIN, ROUT)$, and $(RIN, ROUT)$ is a fixed point of the equations, so by monotonicity the new sets lie below it too.

(ii) The $OUT$ sets never shrink. The first value of $OUT[b]$ is $GEN[b]$, and every later value is $GEN[b] \cup \ldots \supseteq GEN[b]$. After that, each new value of $OUT[b]$ is computed from $OUT$ sets that are at least as large as at the previous update of $b$, so by monotonicity it is at least the previous value.

A pass that sets $changed$ adds at least one site to some $OUT$ set, and by (i) the sets are bounded by the finite $ROUT$ sets, which have at most $B \cdot D$ elements in total. So at most $B \cdot D$ passes change something, and the loop stops after at most one more pass. In the last pass no $OUT$ set changed, so each $IN[b]$ was computed from the final $OUT$ sets, and each final $OUT[b]$ equals the right side of its equation. So the final sets are a solution, by (i) they lie below the least solution, and by Lemma 1 they are the least solution. $\square$

**Lemma 3 (the block scan).** In lines L8 to L12, just before point $(b, i)$ is handled, $live[x]$ is the set of definitions of $x$ that reach $(b, i)$, for every name $x$.

*Proof.* By induction on $i$. For $i = 0$, line L9 sets $live$ from $IN[b] = RIN[b]$ by Lemma 2. For $i + 1 \le n_b$: the only edge into $(b, i + 1)$ comes from $(b, i)$. A path clear for $x$ to $(b, i + 1)$ is either the path of length 0 from the point after $d = (b, i, x)$, or a path clear for $x$ to $(b, i)$ followed by one step, and then $(b, i)$ must not define $x$, because it is not the last point. So if point $(b, i)$ defines $x$, the set for $x$ at $(b, i + 1)$ is $\{(b, i, x)\}$, and otherwise it is the set at $(b, i)$. Line L12 makes exactly this change, and does it after the uses of point $(b, i)$ have been read. $\square$

**Theorem.** `chains` returns exactly the chains of the definition.

*Proof.* For a use at a point that is not a phi, including a terminator, line L11 links it to $live[x]$, which by Lemma 3 is the set of definitions that reach the point. For a phi operand $x$ from the predecessor $p$, the code links the use to the definitions of $x$ in $OUT[p] = ROUT[p]$, the definitions that reach the end of $p$. These are the two cases of the definition. Each pair is added to both $du$ and $ud$. $\square$

**Cost.** Let $E$ be the number of edges of the control flow graph, $I$ the number of instructions and $C$ the number of chains. With bit vectors of $D$ bits, one pass costs $O((B + E)\, D / w)$ word operations on a machine with $w$-bit words, and by Lemma 2 there are at most $B D + 1$ passes. The scan costs $O(I + C)$ set operations plus the cost of reading the $IN$ sets. The bound on the passes is crude. Kam and Ullman showed that for problems of this kind, round-robin iteration in reverse postorder needs at most $k + 2$ passes, where $k$ is the loop connectedness of the graph; that result is cited, not proved here.

**What is proved and what is measured.** Lemmas 1 to 3 and the theorem are proved here, for the chains of the definition above. They say nothing about stores through pointers: a store `*p = a` writes a variable without naming it, so a program that takes the address of a name can read a value that no chain explains. The tests compare the result with a graph search from each definition over the point graph, with the union over all paths of acyclic programs, and with random walks on programs with loops. The pass counts in the tests are measurements.
