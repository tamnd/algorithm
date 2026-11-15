---
title: The hypertableau search for ALC with anywhere equality blocking terminates and is sound and complete
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, lines L1 to L11. The logic is ALC with a general TBox $T$ and no inverse roles. The input is a concept $C$, and the question is whether $C$ is satisfiable with respect to $T$. The proof follows the structure of Motik, Shearer and Horrocks (2009), restricted to this setting, with the rule order, the blocking condition and the backjumping of the implementation.

## DL-clauses

A DL-clause is a formula $\forall x \forall y_1 \dots \forall y_k\, (U_1 \wedge \dots \wedge U_m \to V_1 \vee \dots \vee V_n)$. Body atoms are $A(x)$, $r(x, y_i)$ and $A(y_i)$; every $y_i$ occurs in exactly one body atom $r_i(x, y_i)$. Head atoms are $A(x)$, $A(y_i)$ and $(\exists r.A)(x)$, with $A$ a concept name. With $n = 0$ the head is false.

Line L1 builds the clauses as follows. A concept $E$ in negation normal form gives the clauses of $\top \sqsubseteq E$: for $E = E_1 \sqcap E_2$ the clauses of both parts; otherwise one clause from the disjuncts of $E$. A disjunct $A$ gives the head atom $A(x)$; $\neg A$ gives the body atom $A(x)$; $\exists r.D$ gives the head atom $(\exists r.Q_D)(x)$; $\forall r.D$ gives a new variable $y$, the body atom $r(x, y)$, and either the body atom $A(y)$ when $D = \neg A$, or the head atom $Q_D(y)$; a conjunction $D$ gives the head atom $Q_D(x)$. Here $Q_D$ is $D$ itself when $D$ is a name, and otherwise a fresh name with the clauses of $\top \sqsubseteq \neg Q_D \sqcup D$ (for $D = D_1 \sqcap D_2$, those of $\neg Q_D \sqcup D_1$ and $\neg Q_D \sqcup D_2$). A disjunct $\top$ or $\forall r.\top$ drops the clause; $\bot$ and $\exists r.\bot$ are left out. The clauses are those of $\top \sqsubseteq \mathrm{nnf}(\neg D_1 \sqcup D_2)$ for each $D_1 \sqsubseteq D_2$ in $T$, and those of $Q_0 \sqsubseteq C$ for the root name $Q_0 = Q_{\mathrm{nnf}(C)}$. Call the set $\Gamma$.

**Lemma 1.** (a) In every model $I$ of $\Gamma$, $Q_D^I \subseteq D^I$ for every fresh name, $I$ is a model of $T$, and $Q_0^I \subseteq C^I$. (b) If $C$ is satisfiable with respect to $T$, then $\Gamma$ has a model with $Q_0^I \neq \emptyset$.

*Proof.* (a) By induction on the size of $D$. The clause made from $\neg Q_D \sqcup D$ reads $\top \sqsubseteq \neg Q_D \sqcup D'$, where $D'$ is $D$ with some subconcepts $D''$ replaced by $Q_{D''}$; by induction $Q_{D''}^I \subseteq D''^I$. In negation normal form every such $D''$ occurs positively, so $D'^I \subseteq D^I$, and $Q_D^I \subseteq D'^I \subseteq D^I$. The same argument applied to the clauses of the inclusions of $T$ and of $Q_0 \sqsubseteq C$ gives the rest. The translation of each disjunct is equivalent to it: for example $\forall y\,(r(x, y) \to Q(y))$ is $(\forall r.Q)(x)$, and $\forall y\,(r(x, y) \wedge A(y) \to \bot)$ is $(\forall r.\neg A)(x)$; several $\forall$-disjuncts use different variables, so the prenex form is still their disjunction.
(b) Take a model $I$ of $T$ with $C^I \ne \emptyset$, and set $Q_D^I = D^I$ for every fresh name. Each clause then states a valid inclusion or an inclusion of $T$. $\square$

## The rules and the dependency sets

A branch is a tree of nodes. Each node $x$ has a label $L(x)$, a set of names and existential atoms; each node other than the root $n_0$ was made at line L6 from an existential atom $(\exists r.A)(x)$ of its parent, and the edge carries the role $r$. Line L1 starts with $L(n_0) = \{Q_0\}$. A clause instance is a map $\sigma$ of $x$ to a node and of each $y_i$ to an $r_i$-child of $\sigma(x)$; it is applicable when every body atom is in the branch and no head atom is. Lines L3 to L5 apply instances with at most one head atom; line L6 applies the existential rule at a node that is not blocked; line L7 branches on an instance with two or more head atoms, one branch for each head atom.

Nodes are numbered in the order they are made. A node $w$ is *blocked* if its parent is blocked, or if some node $v < w$ that is not blocked has $L(v) = L(w)$ (anywhere blocking with equality); in the second case $w$ is directly blocked by the least such $v$. The status of $w$ depends only on nodes before $w$, so it is well defined.

Every atom and every edge carries a set of branch levels. The root atom has the empty set. An atom added at line L5 gets the union of the sets of the body atoms and edges of the instance; at line L7 the alternative at level $\ell$ gets that union plus $\{\ell\}$. A node made at line L6 and its edge get the set of the existential atom. An atom that is already present keeps its first set.

Read the node made from $(\exists r.A)(x)$ as the term $f_{r,A}(x)$ of a Skolem function, and let $\Sigma$ be the formulas $(\exists r.A)(x) \to r(x, f_{r,A}(x)) \wedge A(f_{r,A}(x))$. A model of $\Gamma$ extends to a model of $\Gamma \cup \Sigma$ by choosing witnesses, so $\Gamma \cup \{Q_0(n_0)\}$ and $\Gamma \cup \Sigma \cup \{Q_0(n_0)\}$ are satisfiable together.

**Lemma 2.** Let $H_D$ be the set of the atoms chosen at line L7 on the current branch at the levels in $D$. Every atom or edge with dependency set $D$ is a consequence of $\Gamma \cup \Sigma \cup \{Q_0(n_0)\} \cup H_D$. A call at level $\ell$ that returns a set $D$ (a clash) returns $D \subseteq \{0, \dots, \ell - 1\}$, and $\Gamma \cup \Sigma \cup \{Q_0(n_0)\} \cup H_D$ is unsatisfiable.

*Proof.* The first part is by induction on the order of the steps: a step at line L5 is an instance of a clause of $\Gamma$ whose body facts are consequences of the sets they carry, and the union of those sets is the set of the new atom; a step at line L6 is an instance of $\Sigma$; an alternative at line L7 is in $H_D$ itself.

For the second part, use induction on the depth of the recursion. A clash at line L4 is an instance with an empty head whose body facts carry sets with union $D$; all of them were made below the current level, so $D \subseteq \{0, \dots, \ell - 1\}$, and by the first part the set is unsatisfiable. At a branch point at level $\ell$ with alternatives $\alpha_1, \dots, \alpha_n$ and body set $B$, the call for $\alpha_i$ returns $D_i \subseteq \{0, \dots, \ell\}$ with $\Gamma \cup \Sigma \cup \{Q_0(n_0)\} \cup H_{D_i}$ unsatisfiable. If $\ell \notin D_i$, then $H_{D_i}$ uses only choices made above this branch point, and the call returns $D_i$ (backjumping). Otherwise every atom that carries $\ell$ was derived from $\alpha_i$, so its set contains the set $B \cup \{\ell\}$ of $\alpha_i$, and hence $B \subseteq D_i \setminus \{\ell\}$. Let $D = \bigcup_i (D_i \setminus \{\ell\})$. Then $\Gamma \cup \Sigma \cup \{Q_0(n_0)\} \cup H_D$ implies the body of the instance, so it implies $\alpha_1 \vee \dots \vee \alpha_n$, and with each $\alpha_i$ it is unsatisfiable. So it is unsatisfiable, and $D \subseteq \{0, \dots, \ell - 1\}$. $\square$

**Soundness.** If the search answers "unsatisfiable", the top call at level 0 returned a set $D \subseteq \emptyset$, so $\Gamma \cup \Sigma \cup \{Q_0(n_0)\}$ is unsatisfiable, so $\Gamma$ has no model with $Q_0^I \ne \emptyset$, and by Lemma 1(b) $C$ is unsatisfiable with respect to $T$.

## Termination

Let $N$ be the set of names of $\Gamma$ and $X$ the set of existential atoms in the heads of $\Gamma$, and let $K = |N| + |X|$. Labels are subsets of $N \cup X$, and they only grow along a branch; edges are never removed.

- **Out-degree.** Line L6 makes a child for $(\exists r.A)(x)$ only when $x$ has no $r$-child with $A$, and after that it always has one. So a node has at most $|X|$ children.
- **Depth.** Two nodes $v < w$ that are both not blocked never have the same label, because then $w$ would be directly blocked. When line L6 makes a child of a node $p_j$ at depth $j$, $p_j$ is not blocked, so none of its ancestors $p_0, \dots, p_{j - 1}$ is blocked either. These $j + 1$ nodes have pairwise different labels, so $j + 1 \le 2^K$, and every node has depth at most $2^K$.

So a branch has at most $|X|^{2^K + 1}$ nodes and at most $K$ atoms on each, every step of lines L5 and L6 adds an atom or a node, and every branch point creates at most $\max |{\rm head}|$ branches that are each longer by one atom. The search tree is finite, and the search stops.

## Completeness

**Lemma 3.** If line L10 is reached, the following interpretation $M$ is a model of $\Gamma$ with $n_0 \in Q_0^M$. The domain is the set of nodes that are not blocked. A name $A$ holds at $x$ when $A \in L(x)$. For each node $x$ of the domain and each child $w$ of $x$ with role $r$, $M$ has the edge $(x, t(w))$ in $r$, where $t(w) = w$ if $w$ is not blocked and $t(w)$ is the blocker of $w$ otherwise.

*Proof.* The root is never blocked, and $Q_0 \in L(n_0)$. A child $w$ of a node $x$ that is not blocked is either not blocked or directly blocked, so $t(w)$ is defined, it is in the domain, and $L(t(w)) = L(w)$.

Take a clause and a map $\sigma'$ of its variables into the domain that makes the body true in $M$. Then $\sigma'(y_i) = t(w_i)$ for some $r_i$-child $w_i$ of $x = \sigma'(x)$. Let $\sigma$ map $x$ to $x$ and $y_i$ to $w_i$. The body holds under $\sigma$ in the branch: the edges are there, the names at $x$ are the same, and the names at $w_i$ are those at $t(w_i)$. Lines L3 and L7 found no applicable instance, so some head atom holds under $\sigma$ in the branch. If it is $A(x)$, it holds in $M$. If it is $A(y_i)$, then $A \in L(w_i) = L(t(w_i))$. If it is $(\exists r.A)(x)$, then $x$ is not blocked and line L6 did not apply, so $x$ has an $r$-child $w$ with $A \in L(w)$, and $M$ has the edge $(x, t(w))$ with $A \in L(t(w))$. In every case the clause holds under $\sigma'$. $\square$

**Theorem.** The search returns "satisfiable" if and only if $C$ is satisfiable with respect to $T$, and then the interpretation of Lemma 3 is a model of $T$ in which the root is in $C$.

*Proof.* The search stops. If it answers "unsatisfiable", $C$ is unsatisfiable by the soundness argument. If it answers "satisfiable", Lemma 3 gives a model of $\Gamma$ with $n_0 \in Q_0^M$, and by Lemma 1(a) it is a model of $T$ with $n_0 \in C^M$. $\blacksquare$

## Subset blocking is not sound here

Blocking $w$ by an earlier node $v$ with $L(w) \subseteq L(v)$ is sound for the plain ALC tableau, where information only flows from a node to its children. A clause such as $r(x, y) \wedge A(y) \to A(x)$, from $\exists r.A \sqsubseteq A$, sends information from a child to its parent, and then the proof of Lemma 3 fails: the edge to $t(w)$ makes more body atoms true than the edge to $w$. Take $C = A \sqcap W \sqcap \exists r.W \sqcap \forall r.\neg A$ and $T = \{W \sqsubseteq \exists r.B,\ \exists r.B \sqsubseteq A\}$. The $r$-child made for $W$ has the label $\{W, \exists r.B\}$, a subset of the root label. Subset blocking stops there and answers "satisfiable". But that child needs a $B$-successor, so it is in $A$, which $\forall r.\neg A$ at the root forbids, and $C$ is unsatisfiable. Equality blocking does not block the child, and the search finds the clash.

## Running time

The number of names and existential atoms is $K = O(n)$ for an input of size $n$. One branch has at most $|X|^{2^K + 1} = 2^{2^{O(n)}}$ nodes, and the search tree has at most $(\max |{\rm head}|)$ choices at each of at most $2^{2^{O(n)}}$ branch points along a path, which bounds the time by $2^{2^{2^{O(n)}}}$. The space is one branch for each open branch point on the path, $2^{2^{O(n)}}$. These are coarse bounds for this simple search, not the complexity of the problem, which is EXPTIME-complete.
