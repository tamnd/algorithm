---
title: The embedding theorem, and why the fixed point over canonical structures covers every reachable heap
proves: [correctness, termination, complexity]
status: full
---

**Setting.** Truth values are $0$, $\tfrac12$ and $1$. The *information order* is $a \sqsubseteq b$ if $a = b$ or $b = \tfrac12$. Kleene's connectives are $a \wedge b = \min(a, b)$, $a \vee b = \max(a, b)$ and $\neg a = 1 - a$.

A *structure* $S$ has a finite set of nodes $U^S$, a value $p^S(u)$ for each unary predicate $p$ and node $u$, a value $n^S(u, w)$ for each pair of nodes, and a flag $sm^S(u) \in \{0, \tfrac12\}$. The unary predicates are $x$ ("$x$ points here") and $r_x$ ("reachable from $x$ by zero or more $n$ steps") for each variable $x$, and $c$ ("on a cycle of $n$"). Equality is not stored. Its value is $eq^S(u, w) = 0$ for $u \ne w$, $1$ for $u = w$ with $sm^S(u) = 0$, and $\tfrac12$ for $u = w$ with $sm^S(u) = \tfrac12$. A *heap* is a structure with all values in $\{0, 1\}$ and $sm = 0$ everywhere, and whose predicates have their intended meaning: each variable holds at most one cell, each cell has at most one successor, and $r_x$ and $c$ are the reachability and the cycle sets of that graph.

Formulas are built from $p(v)$, $n(v, w)$, $v = w$, $\neg$, $\wedge$, $\vee$, $\exists v$, $\forall v$ and the constants $0, \tfrac12, 1$. $[\![\varphi]\!]^S(Z)$ is the value of $\varphi$ in $S$ under an assignment $Z$ of nodes to its free variables. The quantifiers are the maximum and the minimum over $U^S$.

**Embedding.** A map $f : U^S \to U^{S'}$ *embeds* $S$ into $S'$, written $S \sqsubseteq^f S'$, if:

1. $f$ is onto;
2. $p^S(u) \sqsubseteq p^{S'}(f(u))$ for every unary $p$, and $n^S(u, w) \sqsubseteq n^{S'}(f(u), f(w))$;
3. $eq^S(u, w) \sqsubseteq eq^{S'}(f(u), f(w))$. That is, if two distinct nodes or one summary node map to $u'$, then $sm^{S'}(u') = \tfrac12$.

Two embeddings compose into an embedding. The *concretization* $\gamma(S)$ is the set of heaps that embed into $S$, and $\gamma(\mathcal{X}) = \bigcup_{S \in \mathcal{X}} \gamma(S)$ for a set of structures $\mathcal{X}$.

## 1. The embedding theorem

**Lemma 1.** Kleene's connectives are monotone in $\sqsubseteq$: if $a \sqsubseteq a'$ and $b \sqsubseteq b'$, then $\neg a \sqsubseteq \neg a'$, $a \wedge b \sqsubseteq a' \wedge b'$ and $a \vee b \sqsubseteq a' \vee b'$. If $a_i \sqsubseteq b_i$ for $i$ in a finite set $I$, then $\max_I a_i \sqsubseteq \max_I b_i$ and $\min_I a_i \sqsubseteq \min_I b_i$.

*Proof.* For $\neg$: $1 - \tfrac12 = \tfrac12$. For $\wedge$, assume $a' \wedge b'$ is definite, since otherwise there is nothing to prove. If $a' \wedge b' = 0$, one of $a', b'$ is $0$, so the same one of $a, b$ is $0$, and $a \wedge b = 0$. If $a' \wedge b' = 1$, both are $1$, so $a = b = 1$. $\vee$ is the dual. The finite cases follow by induction on $|I|$. $\square$

**Theorem 1 (embedding theorem).** If $S \sqsubseteq^f S'$, then $[\![\varphi]\!]^S(Z) \sqsubseteq [\![\varphi]\!]^{S'}(f \circ Z)$ for every formula $\varphi$ and assignment $Z$.

*Proof.* By induction on $\varphi$. Constants have the same value on both sides. For $p(v)$, $n(v, w)$ and $v = w$ the claim is conditions 2 and 3. For $\neg$, $\wedge$ and $\vee$ it follows from the induction hypothesis and Lemma 1. For $\exists v.\, \psi$, the left side is $\max_{u \in U^S} [\![\psi]\!]^S(Z[v \mapsto u])$. By the induction hypothesis, each term is $\sqsubseteq [\![\psi]\!]^{S'}(f \circ Z[v \mapsto f(u)])$. By Lemma 1 the maximum of the left terms is $\sqsubseteq$ the maximum of the right terms over $u \in U^S$. Since $f$ is onto, that maximum runs over all of $U^{S'}$, which is the right side. $\forall$ is the same with the minimum. $\square$

So a formula that has a definite value on a structure has that value on every heap in its concretization. A value of $\tfrac12$ says nothing.

## 2. The three steps

**Lemma 2 (blur).** Let $g$ map each node of $S$ to its class of nodes with the same unary values. Then $S \sqsubseteq^g \mathrm{blur}(S)$, so $\gamma(S) \subseteq \gamma(\mathrm{blur}(S))$.

*Proof.* $g$ is onto. A class keeps the common unary values of its members, so condition 2 holds for unary predicates with equality. The value of $n$ between two classes is the join of the values between their members, and each member value is $\sqsubseteq$ the join. A class gets $sm = \tfrac12$ if it has two members or a summary member, which is condition 3. Every heap $H \sqsubseteq^f S$ then embeds into $\mathrm{blur}(S)$ by $g \circ f$. $\square$

Two nodes of $\mathrm{blur}(S)$ always differ on some unary value, and the code orders the nodes by those values. So the result does not depend on the names of the nodes of $S$, and a set of blurred structures can be stored as a set of keys.

**Lemma 3 (variables stay definite).** In every structure that the analysis builds, $x^S(u) \in \{0, 1\}$ for every variable $x$ and node $u$.

*Proof.* `from_heap` gives definite values. `null` and `new` write $0$ and $1$. `copy` copies a definite row. `load` copies the row $n(u, \cdot)$ of the node $u$ of $y$ after the focus step, which makes that row definite (Lemma 5). The other steps do not write variable predicates. Blur and coerce keep unary values or make them definite. $\square$

So "the node of $x$" is well defined, and $x$ is null in a heap of $\gamma(S)$ exactly when no node of $S$ has $x = 1$. The analysis reports a null dereference at a point exactly when the dereferenced variable has no node, and that is then true in every heap of $\gamma(S)$.

**Lemma 4 (coerce).** If $H \sqsubseteq^f S$, then $\mathrm{coerce}(S)$ is not `None`, and $H \sqsubseteq^f \mathrm{coerce}(S)$ with the same $f$.

*Proof.* Each rule changes a value only to the one that every heap with an embedding into $S$ must have, or it reports that no heap can embed. We check each rule against $H$ and $f$. Write $f^{-1}(u)$ for the cells of $H$ at node $u$. These sets are not empty, because $f$ is onto.

- Some node $u$ has $x(u) = 1$. Then every cell in $f^{-1}(u)$ has $x = 1$. Since $x$ holds at most one cell, $f^{-1}(u)$ is that one cell, so setting $sm(u) = 0$ keeps condition 3. Two such nodes would give two cells, which is not possible. The cell is reachable from $x$, so $r_x(u)$ cannot be $0$, and it may be set to $1$.
- No node has $x = 1$. By Lemma 3 every cell has $x = 0$, so $x$ is null and no cell is reachable from $x$. So $r_x = 0$ everywhere, and a value $1$ is a contradiction.
- $n(v, w) = 1$. Then every cell of $f^{-1}(v)$ has every cell of $f^{-1}(w)$ as successor. A cell has at most one successor, so $f^{-1}(w)$ is one cell, and $sm(w) = 0$ is correct. Every other node $w'$ holds no successor of these cells, so a value $\tfrac12$ of $n(v, w')$ may become $0$. Two nodes with $n(v, \cdot) = 1$ are a contradiction.
- $c(v) = 1$ and $c(w) = 0$. The successor of a cell on a cycle is on the same cycle, so no cell of $f^{-1}(v)$ points to a cell of $f^{-1}(w)$. So $n(v, w)$ may be set to $0$, and a value $1$ is a contradiction. The rule for $r_z(v) = 1$ and $r_z(w) = 0$ is the same: the successor of a cell reachable from $z$ is reachable from $z$.
- $c(w) = 0$, and either $w = v$ with $sm(v) = 0$, or $z(w) = 1$ and $r_z(v) = 1$ for a variable $z$. In the first case $f^{-1}(v)$ is one cell $e$, and an edge from $e$ to $e$ would put $e$ on a cycle. In the second case $f^{-1}(w)$ is the one cell $b$ of $z$, and every cell $e$ of $f^{-1}(v)$ is reachable from $b$. An edge from $e$ to $b$ would put $b$ on a cycle. Both contradict $c = 0$, so $n(v, w)$ may be set to $0$, and a value $1$ is a contradiction.

In each case $H$ keeps conditions 1 to 3 against the changed structure. The loop repeats the rules until nothing changes, and the claim holds after each round. $\square$

**Lemma 5 (focus).** Let $u$ be the node of a variable in $S$. Every heap $H \sqsubseteq^f S$ embeds into some structure returned by `focus_succ(S, u)`, and in each returned structure the row $n(u, \cdot)$ is definite.

*Proof.* By Lemma 4, $H$ embeds into $S_0 = \mathrm{coerce}(S)$. In $S_0$ the node $u$ is one cell $a$. Let $W$ be the set of nodes $w$ with $n(u, w) = \tfrac12$. If $W$ is empty, the row is definite and $S_0$ is returned. Otherwise there are three cases for the successor $d$ of $a$ in $H$.

- $d$ is null, or $f(d) \notin W$. Then $n^H(a, e) = 0$ for every cell $e$ with $f(e) \in W$. $H$ embeds by $f$ into the structure that sets $n(u, w) = 0$ for all $w \in W$.
- $f(d) = w \in W$ and $f^{-1}(w) = \{d\}$. $H$ embeds by $f$ into the structure with $n(u, w) = 1$ and $n(u, w') = 0$ for the other $w' \in W$.
- $f(d) = w \in W$ and $f^{-1}(w)$ has other cells. Then $sm(w) = \tfrac12$ by condition 3, and the split structure is built. It has a new node $k$ that copies all values of $w$, with $sm(k) = 0$, $n(u, k) = 1$, $n(u, w) = 0$ and the other $\tfrac12$ values of row $u$ set to $0$. The map $f'$ that sends $d$ to $k$, and every other cell as $f$ does, is an embedding: $f'$ is onto because $w$ keeps a cell; $d$ is the only cell at $k$; the copied values are $\sqsubseteq$-above those of $d$ as they were for $f$; and in row $u$ the only $1$ is the edge from $a$ to $d$.

Each result is coerced again, and $H$ survives that by Lemma 4. $\square$

## 3. The update of each statement

**Lemma 6.** Let $H \sqsubseteq^f S$, and let $H'$ be the heap after a statement. If the statement dereferences a variable that is null in $H$, the analysis reports the point. Otherwise $H'$ embeds into some structure in `post(S, st)`.

*Proof.* `assume` tests only whether variables are null or equal. By Lemma 3 the test has the same value in $S$ and in $H$, so $S$ is kept exactly when $H$ passes. For `null`, `copy` and `new` the new predicate values are the old values of other predicates, $0$ or $1$, in both $H$ and $S$. So the same $f$, sending the new cell to the new node for `new`, is still an embedding. For the other statements, the new value of each predicate in $H'$ is a formula over $H$, and the code computes the same formula over $S$, so Theorem 1 gives condition 2. Here $a$ is the cell of $x$ (for `load`, of $y$), and $u = f(a)$.

- `load` $x = y.n$, after focus on $u$ (Lemma 5). $x'(v) = n(a, v)$. For reachability, $r_x'(v) = (r_y(v) \wedge \neg y(v)) \vee (y(v) \wedge c(v))$. Proof in $H$: the cells reachable from the successor of $a$ are the cells reachable from $a$, without $a$ itself unless $a$ is on a cycle.
- `cut` $x.n = \mathrm{null}$. Let $A(v) = r_z(a) \wedge r_x(v) \wedge \neg x(v)$. In a functional graph the path from $z$ is unique. If $a$ is not on a cycle and $A(v) = 1$, then $v$ comes after $a$ on that path. It cannot come before $a$, because then $a$ and $v$ would be on a cycle. So $v$ loses reachability from $z$. If $A(v) = 0$, the path from $z$ to $v$ does not use the edge of $a$, and $r_z(v)$ stays. If $a$ is on a cycle and $A(v) = 1$, then $v$ is on that cycle, and whether it stays depends on where the path from $z$ enters the cycle. So the new value is $\min(r_z(v),\ \neg(A(v) \wedge \neg c(a)),\ \beta)$, where $\beta$ is a definite value when $A(v) \wedge c(a) = 1$, and $\beta = 1$ otherwise. The code uses $\neg(A(v) \wedge c(a) \wedge \tfrac12)$ in place of $\beta$. That is $\tfrac12$ in the first case and $1$ in the second, so it is $\sqsupseteq \beta$ in both, and Lemma 1 with Theorem 1 gives condition 2. For cycles, $c'(v) = c(v) \wedge \neg(c(a) \wedge r_x(v))$: cutting an edge of a cycle breaks exactly that cycle, which is the set reachable from $a$.
- `link` $x.n = y$, done as `cut` and then the new edge on the result, where $a$ has no successor. Then $r_z'(v) = r_z(v) \vee (r_z(a) \wedge r_y(v))$, and $n'(a, v) = y(v)$. A cycle forms exactly when $y$ reaches $a$, and then it consists of the cells on the path from $y$ to $a$, which are all the cells reachable from $y$. So $c'(v) = c(v) \vee (r_y(a) \wedge r_y(v))$.

In each case the result is coerced, and $H'$ survives that by Lemma 4. Dereferences: `load`, `cut` and `link` report the point exactly when the dereferenced variable has no node, which by Lemma 3 means that it is null in $H$. $\square$

## 4. Soundness of the analysis

Let $F$ be the concrete transfer on sets of states at the program points, from the given initial heaps. The reachable states are $R = \mathrm{lfp}\, F$, and $\bot$ assigns no states to any point. Let $F^\#$ be the abstract transfer on sets of canonical structures that `analyze` iterates: blur of coerce of the entry heaps at the start point, and blur of `post` along each edge.

**Theorem 2 (soundness).** $\mathrm{lfp}\, F \subseteq \gamma(\mathrm{lfp}\, F^\#)$. That is, every heap that the program reaches at point $p$ embeds into some structure in $A[p]$. Every null dereference that happens in a run is at a point that the analysis reports.

*Proof.* `analyze` stops only when its worklist is empty. Every key added to $A[q]$ is pushed once, and its successors are computed when it is popped. So at the end, $A$ is closed under $F^\#$, and it is the least closed family that contains the entry. Now take a run $(p_0, H_0), (p_1, H_1), \ldots$ and use induction on $i$. For $i = 0$, $H_0$ embeds into the blur of its own coerced structure, by Lemmas 2 and 4. For the step from $i$ to $i + 1$, let $H_i \sqsubseteq S$ with $S$ in $A[p_i]$. By Lemma 6, $H_{i+1}$ embeds into some $T$ in `post(S, st)`, or the dereference is reported. By Lemma 2, $H_{i+1}$ embeds into $\mathrm{blur}(T)$, which is in $A[p_{i+1}]$ because $A$ is closed. $\square$

By Theorem 1, a formula with value $1$ on every structure of $A[p]$ holds in every heap at $p$. This is how the page example reads off "acyclic" and "every cell is reachable from $y$".

## 5. Termination and cost

**Theorem 3.** `analyze` terminates.

*Proof.* Let $U = 2v + 1$ be the number of unary predicates for $v$ variables. A blurred structure has nodes with pairwise different unary values, so it has at most $N \le 2^v 3^{v + 1}$ nodes, since the variable predicates are definite (Lemma 3). Its values are drawn from finite sets. So there are finitely many canonical structures, at most doubly exponential in $v$. Each $A[p]$ only grows, and a key is pushed only when it is new. So the worklist empties. Inside one step, the loop of `coerce` ends because each round that changes something turns a $\tfrac12$ into a definite value, or a flag into $0$, and there are at most $N^2 + vN + N$ such values. `focus_succ` returns at most $2N + 1$ structures. $\square$

**Cost.** Let $N$ bound the nodes of a structure, $M$ bound the number of canonical structures at a point, $v$ be the number of variables, and $E$ be the number of edges of the program. One round of `coerce` costs $O(vN^2)$, and there are $O(N^2 + vN)$ rounds, so `coerce` costs $O(vN^4 + v^2 N^3)$. A transfer focuses into $O(N)$ structures and coerces each one. Blur costs $O(N^2 + vN \log N)$. Every structure at a point is popped once, and each of its out edges is processed once. So the total time is $O(E M (v N^5 + v^2 N^4))$, which is within $O(E M v^2 N^5)$. The sets $A[p]$ take $O(L M (N^2 + vN))$ space for $L$ points. Since $M$ can be doubly exponential in $v$, the bound is useful only because, in practice, the sets of structures that a program reaches are small. In the page example, at most 13 structures reach any point. This holds for input lists of any length, because all lists of three or more cells have the same canonical abstraction.
