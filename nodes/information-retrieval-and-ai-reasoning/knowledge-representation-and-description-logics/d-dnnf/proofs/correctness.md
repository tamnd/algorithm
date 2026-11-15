---
title: The CNF to decision-DNNF compiler and the linear-time d-DNNF queries are correct
proves: [correctness]
status: full
---

We use the pseudocode of the page, lines L1 to L24. For a node $u$, $f_u$ is its function and $\mathrm{vars}(u)$ is the set of variables at the leaves below $u$. For a set of variables $Y \supseteq \mathrm{vars}(u)$, $\#_Y(u)$ is the number of assignments to $Y$ that satisfy $f_u$. For a clause set $\Delta$, $\mathrm{vars}(\Delta)$ is the set of variables in its clauses, and $\Delta|l$ is defined on the page.

**Lemma 0 (constructors).** AND$(c_1, \ldots, c_k)$ returns a node whose function is $f_{c_1} \wedge \cdots \wedge f_{c_k}$ and whose variables are a subset of $\bigcup_i \mathrm{vars}(c_i)$; if the $c_i$ have pairwise disjoint variables and are decomposable, so is the result. OR is the same with $\vee$; if the $c_i$ are pairwise contradictory and deterministic, so is the result.

*Proof.* The constructor either returns $\mathit{false}$ (for AND, when a child is $\mathit{false}$; the conjunction is then false), or removes $\mathit{true}$ children (which does not change a conjunction), or returns the only remaining child, or makes a gate over the remaining children. Removing children keeps disjointness of variables and pairwise contradiction among the rest. The duals hold for OR. Hash-consing returns a node with the same key, hence the same function. $\square$

## The compiler

**Lemma 1 (equivalence).** COMPILE$(\Delta)$ returns a node $r$ with $f_r \equiv \Delta$ and $\mathrm{vars}(r) \subseteq \mathrm{vars}(\Delta)$.

*Proof.* By induction on $|\mathrm{vars}(\Delta)|$, and for equal values on the order of the calls (a cached result was computed earlier for the same $\Delta$, so line L3 is covered by the hypothesis for that earlier call). Line L1: the empty conjunction is $\mathit{true}$. Line L2: a clause set with the empty clause is unsatisfiable. Line L5: if $\{l\} \in \Delta$, every model of $\Delta$ sets $l$ true, and under $l = 1$ the clauses with $l$ are satisfied and $\neg l$ is false in the rest, so $\Delta \equiv l \wedge \Delta|l$. The set $\Delta|l$ does not mention the variable of $l$, so it has fewer variables, and the hypothesis and Lemma 0 give the claim. Line L7: $\Delta$ is the conjunction of its groups. Each group is non-empty and the groups have pairwise disjoint, non-empty variable sets, so with $k \ge 2$ each group has fewer variables than $\Delta$. Line L10: the Shannon expansion $\Delta \equiv (x \wedge \Delta|x) \vee (\neg x \wedge \Delta|\neg x)$, where $\Delta|x$ and $\Delta|\neg x$ do not mention $x$. $\square$

**Lemma 2 (decision-DNNF).** Every node that COMPILE creates is decomposable, and every or-node is a decision node, hence deterministic.

*Proof.* By the same induction. At line L5, the literal $l$ and the node for $\Delta|l$ have disjoint variables, by Lemma 1. At line L7, the node for $\Delta_i$ has variables in $\mathrm{vars}(\Delta_i)$, and these sets are pairwise disjoint. At line L10, each and-node joins $x$ or $\neg x$ with a node whose variables avoid $x$. The or-node has the children $x \wedge \alpha$ and $\neg x \wedge \beta$, which no assignment satisfies together. By Lemma 0 the folding of constants keeps both properties. $\square$

**Lemma 3 (termination).** Without the cache, the recursion tree of COMPILE$(\Delta)$ has at most $2^{|\mathrm{vars}(\Delta)|}$ leaves.

*Proof.* Let $L(n)$ be the largest number of leaves for $n$ variables. A call that stops at lines L1 to L3 is one leaf, and $1 \le 2^n$. Line L5 makes one call with at most $n - 1$ variables. Line L7 makes calls on $n_1, \ldots, n_k \ge 1$ variables with $\sum n_i \le n$ and $k \ge 2$, and $\sum 2^{n_i} \le 2^{\sum n_i}$ because $2^a + 2^b \le 2^{a+b}$ for $a, b \ge 1$. Line L10 makes two calls with at most $n - 1$ variables, and $2 \cdot 2^{n-1} = 2^n$. Each call has fewer variables than its caller, so the depth is at most $n$ and the recursion stops. The cache returns early at line L3 and only removes subtrees. $\square$

## The queries

**Lemma 4 (CO).** If $N$ is decomposable, CO$(N)$ returns true if and only if $f_N$ is satisfiable.

*Proof.* We show $c[u] = 1$ if and only if $f_u$ is satisfiable, for each $u$ in the order of line L12. Leaves (line L13): a literal and $\mathit{true}$ are satisfiable, $\mathit{false}$ is not. An or-node (line L15) is satisfiable if and only if some child is. An and-node $u$ (line L14) with an unsatisfiable child is unsatisfiable. If every child $c_i$ has a model $\mu_i$ over $\mathrm{vars}(c_i)$, the sets $\mathrm{vars}(c_i)$ are pairwise disjoint, so the union of the $\mu_i$ is a well-defined assignment, and it satisfies every child, hence $f_u$. $\square$

**Lemma 5 (CONDITION).** For a set $\gamma$ of literals with no complementary pair, CONDITION$(N, \gamma)$ returns a node $N'$ with $f_{N'} = f_N|\gamma$ (the function with the variables of $\gamma$ fixed so that $\gamma$ is true). If $N$ is decomposable or deterministic, so is $N'$, and $\mathrm{vars}(N') \subseteq \mathrm{vars}(N) \setminus \mathrm{vars}(\gamma)$.

*Proof.* By induction in the order of line L17. A literal $l \in \gamma$ becomes $\mathit{true} = l|\gamma$, a literal with $\neg l \in \gamma$ becomes $\mathit{false}$, and any other literal is kept. Restriction commutes with $\wedge$ and $\vee$, and Lemma 0 gives the function of the rebuilt gate. Variables only disappear, so disjointness is kept. If $f_{c_i} \wedge f_{c_j} \equiv \mathit{false}$, then $(f_{c_i}|\gamma) \wedge (f_{c_j}|\gamma) = (f_{c_i} \wedge f_{c_j})|\gamma \equiv \mathit{false}$, so determinism is kept. $\square$

**Lemma 6 (CE).** If $N$ is decomposable, CE$(N, \delta)$ returns true if and only if $f_N \models \delta$.

*Proof.* If $\delta$ contains $l$ and $\neg l$, it is valid and line L18 is right. Otherwise $\neg\delta$ is the consistent term $\gamma = \{\neg l : l \in \delta\}$. $f_N \models \delta$ if and only if $f_N \wedge \gamma$ is unsatisfiable. A model of $f_N \wedge \gamma$ restricts to a model of $f_N|\gamma$, and a model of $f_N|\gamma$ extends by $\gamma$ to a model of $f_N \wedge \gamma$, since $f_N|\gamma$ does not mention $\mathrm{vars}(\gamma)$. So line L19 is right by Lemmas 4 and 5. $\square$

**Lemma 7 (SMOOTH).** SMOOTH$(N, X)$ returns a node $N''$ with $f_{N''} \equiv f_N$, $\mathrm{vars}(N'') = X$, which is smooth, and which is decomposable (deterministic) when $N$ is.

*Proof.* By induction in the order of line L20, the rebuilt node $u'$ of $u$ has $f_{u'} \equiv f_u$ and $\mathrm{vars}(u') = \mathrm{vars}(u)$. For an and-node this follows from the children by Lemma 0. For an or-node $u$, line L21 replaces the rebuilt child $v'$ by $v' \wedge \bigwedge_{y} (y \vee \neg y)$ over $y \in \mathrm{vars}(u) \setminus \mathrm{vars}(v)$. Each factor is valid, so the function is $f_v$, and the variables become exactly $\mathrm{vars}(u)$, so all children of $u'$ have the same variables (smooth). The new and-node is decomposable: $v'$ has the variables $\mathrm{vars}(v)$, the factors mention distinct variables outside it, and each factor $y \vee \neg y$ is an or-node of two literals on one variable, which is smooth and deterministic. The functions of the children of $u'$ are those of $u$, so pairwise contradiction is kept. Line L22 is the same step at the root with $X$ in place of $\mathrm{vars}(u)$. $\square$

**Lemma 8 (CT).** If $N$ is a smooth d-DNNF, the value $t[u]$ of line L23 is $\#_{\mathrm{vars}(u)}(u)$ for each node $u$. So CT$(\mathrm{SMOOTH}(N, X))$ is the number of models of $f_N$ over $X$.

*Proof.* By induction in the order of line L23. A literal has one model over its variable; $\mathit{true}$ has one model over $\emptyset$ and $\mathit{false}$ none. For an and-node $u$ with children $c_1, \ldots, c_k$ and pairwise disjoint $V_i = \mathrm{vars}(c_i)$, the map $\mu \mapsto (\mu|_{V_1}, \ldots, \mu|_{V_k})$ is a bijection from the assignments to $\mathrm{vars}(u) = \bigcup V_i$ onto tuples of assignments to the $V_i$, and $\mu$ satisfies $f_u$ if and only if each $\mu|_{V_i}$ satisfies $f_{c_i}$. So $\#(u) = \prod_i \#(c_i)$. For an or-node $u$, smoothness gives $\mathrm{vars}(c_i) = \mathrm{vars}(u)$ for all $i$, so all counts are over the same set. The model sets of the children are pairwise disjoint by determinism, and their union is the model set of $f_u$, so $\#(u) = \sum_i \#(c_i)$. The second sentence follows from Lemma 7, which gives $\mathrm{vars}(\mathrm{SMOOTH}(N, X)) = X$ and keeps the function and the two properties. $\square$

**Cost.** Each query visits each node below the root once and does work proportional to its number of children, plus one expected $O(1)$ hash lookup in CONDITION and SMOOTH, so CO, CONDITION and CE take $O(s)$ expected time for $s$ edges. SMOOTH adds at most $|X|$ factors of size $O(1)$ for each edge out of an or-node and at the root, so its output has $O(s n)$ edges with $n = |X|$. $\square$
