---
title: The demand-driven solver stops, and for every demanded variable it computes exactly the set of the exhaustive Andersen analysis
proves: [correctness, termination, complexity]
status: full
---

**Setting.** A program is a finite list $S$ of statements of the forms $v = \&a$, $v = y$, $v = {*}y$ and ${*}p = q$ over a finite set $V$ of variables. A variable is *taken* if it is the $a$ of some statement $v = \&a$. Andersen's analysis is the least map $A : V \to 2^V$ such that

1. $v = \&a$ gives $a \in A(v)$;
2. $v = y$ gives $A(y) \subseteq A(v)$;
3. $v = {*}y$ and $b \in A(y)$ give $A(b) \subseteq A(v)$;
4. ${*}p = q$ and $b \in A(p)$ give $A(q) \subseteq A(b)$.

The least map exists because the rules are monotone, and it is the set of facts $(v, a)$ that have a finite derivation by the rules. The *rank* of a fact is the height of its shortest derivation. Every fact $(v, a) \in A$ has $a$ taken, by induction on the rank.

The algorithm keeps a set $D$ of demanded variables (the keys of `pts`), a set $pts(v)$ for each $v \in D$, a set of edges $u \to v$ between demanded variables, a queue of variables that wait to start, and a worklist of variables whose sets have grown, with the new part in $delta(v)$. The line numbers refer to the pseudocode of the page.

**Lemma 1 (soundness).** At all times, $pts(v) \subseteq A(v)$ for every $v \in D$, and every edge $u \to v$ has $A(u) \subseteq A(v)$.

*Proof.* By induction over the steps. A set grows only at line L15, called from line L9 or along an edge. Line L9 adds $a$ for $v = \&a$, and $a \in A(v)$ by rule 1. Along an edge $u \to v$ the added elements come from $pts(u) \subseteq A(u) \subseteq A(v)$. Edges are created at four places. Line L10 adds $y \to v$ for $v = y$, and $A(y) \subseteq A(v)$ by rule 2. Lines L11 and L5 add $b \to v$ for $v = {*}y$ with $b \in pts(y) \subseteq A(y)$, and rule 3 gives $A(b) \subseteq A(v)$. Lines L12 and L6 add $q \to b$ for ${*}p = q$ with $b \in pts(p) \subseteq A(p)$, and rule 4 gives $A(q) \subseteq A(b)$. $\square$

**Lemma 2 (termination).** The run stops.

*Proof.* A variable enters $D$ at most once (line L14), so at most $|V| + |Q|$ variables start, where $Q$ is the set of queries. A variable joins the worklist only when its set grows, and a set is a subset of $V$ that never shrinks, so there are at most $|V|$ growths per variable. Each step of the main loop either starts a variable or removes one entry of the worklist. $\square$

**Lemma 3 (edges carry everything).** When the run stops, $pts(u) \subseteq pts(v)$ for every edge $u \to v$.

*Proof.* Let $a \in pts(u)$. If $a$ entered $pts(u)$ before the edge was created, line L13 added the whole of $pts(u)$ to $pts(v)$ at that moment. Otherwise $a$ entered $pts(u)$ later, together with $delta(u)$, and $u$ was put on the worklist. The worklist is empty at the end, so $u$ was removed afterwards, with $a$ in the removed $delta(u)$, and line L7 sent it along every edge of $u$, including $u \to v$. $\square$

**Lemma 4 (closure of the demanded part).** When the run stops, for every $v \in D$:

- (a) if $v = \&a$ is in $S$, then $a \in pts(v)$;
- (b) if $v = y$ is in $S$, then $y \in D$ and $y \to v$ is an edge;
- (c) if $v = {*}y$ is in $S$, then $y \in D$, and every $b \in pts(y)$ is in $D$ with an edge $b \to v$;
- (d) if $v$ is taken and ${*}p = q$ is in $S$, then $p \in D$, and if $v \in pts(p)$, then $q \in D$ with an edge $q \to v$.

*Proof.* The queue of waiting variables is empty at the end, so $v$ has started. (a) and (b) come from lines L9 and L10, and line L13 demands the source of each edge. For (c), line L11 demands $y$ and adds $b \to v$ for every $b$ that is in $pts(y)$ when $v$ starts. A $b$ that enters $pts(y)$ later is in $delta(y)$ when $y$ is removed from the worklist, and since $v \in D$ already, line L5 adds $b \to v$. For (d), line L12 demands $p$ and adds $q \to v$ if $v \in pts(p)$ when $v$ starts. If $v$ enters $pts(p)$ later, it is in $delta(p)$ when $p$ is removed, $v \in D$, and line L6 adds $q \to v$. $\square$

**Theorem 1 (exact answers).** When the run stops, $pts(v) = A(v)$ for every $v \in D$. In particular every query gets the answer of the exhaustive analysis.

*Proof.* $pts(v) \subseteq A(v)$ is Lemma 1. For the other direction, we show by induction on the rank $r$ that every fact $(v, a) \in A$ with $v \in D$ has $a \in pts(v)$. Take the last rule of a shortest derivation of $(v, a)$.

- Rule 1: $v = \&a$, and Lemma 4(a) gives $a \in pts(v)$.
- Rule 2: $v = y$ and $(y, a)$ has a smaller rank. By Lemma 4(b), $y \in D$ with an edge $y \to v$. By induction $a \in pts(y)$, and by Lemma 3 $a \in pts(v)$.
- Rule 3: $v = {*}y$, and $(y, b)$ and $(b, a)$ have smaller ranks. By Lemma 4(c), $y \in D$, so by induction $b \in pts(y)$. Then Lemma 4(c) gives $b \in D$ and an edge $b \to v$. By induction $a \in pts(b)$, and by Lemma 3 $a \in pts(v)$.
- Rule 4: ${*}p = q$, and $(p, v)$ and $(q, a)$ have smaller ranks. The fact $(p, v) \in A$ shows that $v$ is taken, so Lemma 4(d) gives $p \in D$. By induction $v \in pts(p)$. Then Lemma 4(d) gives $q \in D$ and an edge $q \to v$. By induction $a \in pts(q)$, and by Lemma 3 $a \in pts(v)$.

So $A(v) \subseteq pts(v)$. Queries are in $D$ from line L1. $\square$

**Theorem 2 (cost).** Let $m = |V| + |Q|$ and $s = |S|$. With hash sets and unit-cost set operations per element, the run takes $O(m^3 + m s)$ time and $O(m^2 + s)$ space. Only demanded variables cost anything beyond the $O(s)$ indexing.

*Proof.* Each demanded variable starts once. A start scans the statements into $v$ and, for a taken $v$, all stores, so all starts cost $O(m s)$. There are at most $m^2$ edges, and creating one copies a set of at most $m$ elements, so edge creation costs $O(m^3)$. Each of the at most $m$ elements of a set is in exactly one removed delta of that variable. When it is removed, it is sent along at most $m$ edges and checked against the loads and stores of the variable, so the delta work is $O(m \cdot (m^2 + s))$ in total. The sets, edges and indexes take $O(m^2 + s)$ space. $\blacksquare$
