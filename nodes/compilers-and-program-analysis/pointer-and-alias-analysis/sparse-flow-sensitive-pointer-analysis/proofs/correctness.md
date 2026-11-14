---
title: The sparse analysis computes exactly the sets of the dense flow-sensitive analysis on its def-use pairs, and both are inside Andersen's result
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a control flow graph whose nodes $N$ are the nodes reachable from the entry $0$. Each node $n$ holds one statement $x = \&a$, $x = y$, $x = {*}y$ or ${*}x = y$. $\mathit{Names}$ is the set of all names, and a name that matches `h<digits>` is a *heap name*. $A$ is Andersen's least solution of the four inclusion rules for all statements (the [Andersen page](/andersen-analysis/)). A *state* $S$ maps every name to a set of names. $L_A$ is the set of states with $S(w) \subseteq A(w)$ for every $w$. Ordered by pointwise inclusion, $L_A$ is a finite complete lattice.

**The dense analysis.** For a node $n$ and a state $S$, $F_n(S)$ is $S$ with these changes:

1. $x = \&a$: $x \mapsto \{a\}$;
2. $x = y$: $x \mapsto S(y)$;
3. $x = {*}y$: $x \mapsto \bigcup_{b \in S(y)} S(b)$;
4. ${*}x = y$, with $X = S(x)$: if $X = \emptyset$, every $b \in A(x)$ maps to $\emptyset$; if $X = \{b\}$ and $b$ is not a heap name, $b \mapsto S(y)$; otherwise every $b \in X$ maps to $S(b) \cup S(y)$.

The dense equations are $IN_0 \supseteq \bot$, $IN_n = \bigcup_{p \in pred(n)} OUT_p$ and $OUT_n = F_n(IN_n)$, where $\bot$ maps every name to $\emptyset$. The dense result $D$ is their least solution in $L_A$.

**DEF, USE and def-use edges.** $DEF(n)$ is $\{x\}$ for the first three forms and $A(x)$ for a store. $USE(n)$ is $\emptyset$, $\{y\}$, $\{y\} \cup A(y)$ and $\{x, y\} \cup A(x)$ for the four forms. A node $d$ *reaches* $u$ for $w$ if there is a path $d = m_0 \to m_1 \to \cdots \to m_k = u$ with $k \ge 1$ and $w \notin DEF(m_i)$ for $0 < i < k$. The edge $d \xrightarrow{w} u$ exists when $w \in DEF(d)$, $w \in USE(u)$ and $d$ reaches $u$ for $w$. The search of lines L3 and L4 finds exactly these: it starts at the successors of $d$, records a visited $u$ when $w \in USE(u)$, and goes on past $u$ only when $w \notin DEF(u)$.

**The sparse analysis.** Its unknowns are $out(d, v)$ for $d \in N$ and $v \in DEF(d)$. For a node $u$ and $w \in USE(u)$, $in_u(w) = \bigcup \{ out(d, w) : d \xrightarrow{w} u \}$. The sparse equations are $out(d, v) = F_d(in_d)(v)$, where $in_d$ is extended to a state by $\emptyset$ outside $USE(d)$. The sparse result $P$ is their least solution with every $out(d, v) \subseteq A(v)$.

**Lemma 1 (closure and monotonicity).** Each $F_n$ maps $L_A$ into $L_A$ and is monotone on $L_A$.

*Proof.* Let $S \in L_A$. Rule 1 gives $\{a\} \subseteq A(x)$. Rule 2 gives $S(y) \subseteq A(y) \subseteq A(x)$. In rule 3, $b \in S(y) \subseteq A(y)$, so $S(b) \subseteq A(b) \subseteq A(x)$ by Andersen's load rule. In rule 4, $X \subseteq A(x)$, so every written $b$ is in $A(x)$, and $S(y) \subseteq A(y) \subseteq A(b)$ by Andersen's store rule. So $F_n(S) \in L_A$.

For monotonicity, only rule 4 needs care. Let $S \subseteq S'$ in $L_A$, with $X = S(x) \subseteq X' = S'(x)$, and fix a name $b$. If $b \notin A(x)$, then $b \notin X'$ and $b$ is unchanged in both. Let $b \in A(x)$. The value of $b$ is $\emptyset$ if $X = \emptyset$, $S(y)$ if $X = \{b\}$ with $b$ not a heap name, $S(b) \cup S(y)$ if $b \in X$ otherwise, and $S(b)$ if $b \notin X \neq \emptyset$. Going from $X$ to the larger $X'$ moves only from the empty case to any case, from the second case to the third, or from the fourth case to the third, and each of these moves gives a superset. With $S \subseteq S'$ the sets $S(y)$ and $S(b)$ only grow. $\square$

**Lemma 2 (locality).** For $S \in L_A$, $F_n(S)(w) = S(w)$ for $w \notin DEF(n)$, and $F_n(S)(v)$ for $v \in DEF(n)$ depends only on $S$ restricted to $USE(n)$.

*Proof.* The first three rules change only $x$. They read $y$, and rule 3 also reads $b \in S(y) \subseteq A(y)$. Rule 4 changes only names in $X \subseteq A(x)$ or in $A(x)$, and it reads $x$, $y$ and $b \in A(x)$. All of these are in $USE(n)$. $\square$

**Lemma 3 (both results exist and are computed).** $D$ and $P$ exist. The round-robin iteration of the dense equations from $\bot$ reaches $D$, and the worklist of lines L5 to L10 stops with $P$.

*Proof.* By Lemma 1 the dense equations define a monotone map on the finite lattice $L_A^{N} \times L_A^{N}$, so its least fixed point exists and is the limit of the iteration from the bottom (Kleene). The sparse map is monotone by Lemma 1 and keeps every $out(d, v) \subseteq A(v)$, so the same holds for it. The worklist starts with every node, so each equation is evaluated at least once. A value only changes to a larger set, by induction with monotonicity, so there are finitely many changes, and each change puts every user of that value on the worklist. When the worklist is empty, each node was last evaluated after its last input changed, so every equation holds. Every value it computes is inside every solution, by induction over the steps, so the result is the least one. $\square$

**Lemma 4 (paths carry values).** If $d$ reaches $u$ for $w$ and $w \in DEF(d)$, then $OUT_d(w) \subseteq IN_u(w)$ in $D$.

*Proof.* Along the path $d = m_0 \to \cdots \to m_k = u$, $OUT_{m_{i}}(w) \subseteq IN_{m_{i+1}}(w)$ by the join, and $OUT_{m_i}(w) = IN_{m_i}(w)$ for $0 < i < k$ by Lemma 2, since $w \notin DEF(m_i)$. $\square$

**Theorem 1 (sparse equals dense).** For every $d \in N$ and $v \in DEF(d)$, $P(d, v) = OUT_d(v)$ in $D$. For every $u \in N$ and $w \in USE(u)$, $in_u(w)$ computed from $P$ equals $IN_u(w)$ in $D$.

*Proof.* *Sparse inside dense.* Let $R(d, v) = OUT_d(v)$ from $D$. Then for $w \in USE(d)$, $in^R_d(w) = \bigcup_{e \xrightarrow{w} d} OUT_e(w) \subseteq IN_d(w)$ by Lemma 4. By Lemmas 1 and 2, $F_d(in^R_d)(v) \subseteq F_d(IN_d)(v) = OUT_d(v) = R(d, v)$. So $R$ satisfies every sparse equation with $\subseteq$, and since the least fixed point of a monotone map is below every such point (Knaster and Tarski), $P \subseteq R$.

*Dense inside sparse.* Build the state $E$ from $P$: $IN^E_u(w)$ is the union of $P(d, w)$ over all $d$ that reach $u$ for $w$ with $w \in DEF(d)$, and $OUT^E_n(w)$ is $P(n, w)$ for $w \in DEF(n)$ and $IN^E_n(w)$ otherwise. All its sets are inside $A$. Check the dense equations with $\supseteq$. For the join at $u$, take a predecessor $p$. If $w \in DEF(p)$, then $p$ reaches $u$ for $w$ by the path $p \to u$, so $OUT^E_p(w) \subseteq IN^E_u(w)$. If not, $OUT^E_p(w) = IN^E_p(w)$, and every $d$ that reaches $p$ for $w$ also reaches $u$ for $w$, through $p$. For the transfer at $n$ and $w \notin DEF(n)$, $F_n(IN^E_n)(w) = IN^E_n(w) = OUT^E_n(w)$ by Lemma 2. For $v \in DEF(n)$, $IN^E_n$ agrees with $in^P_n$ on $USE(n)$, because the edges into $n$ are exactly the reaching definitions of the names in $USE(n)$. So by Lemma 2, $F_n(IN^E_n)(v) = F_n(in^P_n)(v) = P(n, v) = OUT^E_n(v)$. So $E$ satisfies the dense equations with $\supseteq$, and $D \subseteq E$.

Now for $v \in DEF(d)$: $OUT_d(v) \subseteq OUT^E_d(v) = P(d, v) \subseteq R(d, v) = OUT_d(v)$. For $w \in USE(u)$: $IN_u(w) \subseteq IN^E_u(w) = in^P_u(w)$, and $in^P_u(w) = \bigcup OUT_e(w) \subseteq IN_u(w)$ by the first part and Lemma 4. $\square$

**Theorem 2 (inside Andersen, and sound).** Every set of $D$, and so every set of $P$, is inside Andersen's set for the same name. For every run that starts at the entry with no values and follows the graph, the state before each node is covered by $IN$: if location $\ell$ holds a pointer to $\ell'$, then the name of $\ell'$ is in $IN_n(\text{name of } \ell)$.

*Proof.* The first part is $D \in L_A$. For soundness, use induction on the length of the run. At the entry nothing holds a value. For one step through node $n$, the cases of rules 1 to 3 follow the concrete step. For a store ${*}x = y$ that runs, $x$ holds a location whose name $b$ is in $X = IN_n(x)$, so $X \neq \emptyset$. If $X = \{b\}$ and $b$ is not a heap name, then $b$ is the only location with that name, the store overwrites it, and the new value is covered by $IN_n(y)$. Otherwise the written location keeps a value covered by $IN_n(b) \cup IN_n(y)$. Other locations do not change. The empty case never runs, so its value does not matter for soundness. A heap name stands for every object created at its allocation statement, so it only gets weak updates. $\square$

**Theorem 3 (cost).** Let $n$ be the number of nodes and edges of the graph and $m$ the number of names. Building the def-use edges takes $O(n^2 m)$ time after Andersen's analysis, there are at most $n^2 m$ of them, and the worklist runs in $O(n^3 m^4)$ time. The space is $O(n^2 m + n m^2)$.

*Proof.* There are at most $n m$ pairs $(d, v)$, and each search visits each node and edge once, so the edges cost $O(n^2 m)$ and number at most $n \cdot n \cdot m$. Each $out(d, v)$ is a subset of $A(v)$ and only grows, so it changes at most $m$ times, and each change queues at most $n$ users. So there are at most $n + n^2 m^2$ visits. A visit computes at most $m$ values, and each reads at most $m$ inputs, each a union over at most $n$ sources of sets of size at most $m$, so it costs $O(n m^2)$. The product is $O(n^3 m^4)$. The space holds the edges and at most $n m$ sets of size at most $m$. $\blacksquare$
