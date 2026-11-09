---
title: The local algorithm returns true iff the start vertex is in the least solution, and the encoding is correct
proves: [correctness, complexity]
status: full
---

We use the pseudocode and the notation of the page. A dependency graph has vertices $V$ and hyperedges $(v, T)$ with $T \subseteq V$ finite. The function $F(A) = \{v : \text{some hyperedge } (v, T) \text{ has } T \subseteq A\}$ is monotone on subsets of $V$, and a set $A$ is *closed* when $F(A) \subseteq A$. By the Knaster-Tarski theorem the least fixed point $\mathit{Lfp}$ of $F$ is the intersection of all closed sets, so it is contained in every closed set, and it is itself closed: $F(\mathit{Lfp}) = \mathit{Lfp}$. We assume the graph that the search can reach from $v_0$ is finite, and that each vertex has finitely many hyperedges.

**Lemma 1 (soundness of the value 1).** At every time, each vertex with value $1$ is in $\mathit{Lfp}$.

*Proof.* By induction on the number of executions of line L8. Line L8 sets $\mathit{value}[v] = 1$ only when, by line L7, every target of some hyperedge $(v, T)$ has value $1$. By the induction hypothesis these targets are in $\mathit{Lfp}$, so $T \subseteq \mathit{Lfp}$, and $v \in F(\mathit{Lfp}) = \mathit{Lfp}$. Values never go from $1$ back to $0$. $\square$

So if the algorithm returns true at line L8, then $v_0 \in \mathit{Lfp}$.

**Lemma 2 (termination and cost).** The loop runs at most $\sum_{(v, T)} (|T| + 1)$ times, the sum over the hyperedges of the built vertices, and its total time is linear in the size of the built part of the graph.

*Proof.* A hyperedge $(v, T)$ is pushed by line L2 or L13 once, when $v$ is built, and by line L9 once for each time it is in $D[u]$ for a vertex $u$ that becomes true. It is added to some $D[u]$ only at line L12 or L14, at the end of a pop in which $u$ is the first target of $T$ with value $0$. After $u$ becomes true, the next pop of $(v, T)$ moves the pointer past $u$, and $u$ never becomes $0$ again, so $(v, T)$ is added to the list of each target at most once, and it is pushed at most $|T| + 1$ times. Line L6 only moves the pointer of $(v, T)$ forward, so its total work for $(v, T)$ is $O(|T| + 1)$. Each other line takes constant time per pop. $\square$

**Lemma 3 (the value 0 at the end).** Suppose line L15 is reached. Let $Z$ be the set of built vertices with value $0$. Then for each built vertex $v \in Z$ and each hyperedge $(v, T)$, some target of $T$ is in $Z$.

*Proof.* Fix $v \in Z$ and a hyperedge $(v, T)$. It was pushed when $v$ was built, so it was popped at least once; consider its last pop. At that time $\mathit{value}[v] = 0$, since values only grow and $v$ has value $0$ at the end. Line L8 did not run for $v$ at that pop, again because $v$ is in $Z$, so line L10 chose a target $u \in T$ with value $0$, and lines L12 or L14 put $(v, T)$ into $D[u]$ (building $u$ if needed, so $u$ is built). If $u$ later became $1$, line L9 would push $(v, T)$ again, and it would be popped again before the stack is empty, which contradicts the choice of the last pop. So $u$ has value $0$ at the end, and $u \in Z$. $\square$

**Lemma 4 (completeness).** If line L15 is reached, then $v_0 \notin \mathit{Lfp}$.

*Proof.* Let $A = V \setminus Z$. We show that $A$ is closed. Take a hyperedge $(v, T)$ with $T \subseteq A$. If $v \in Z$, then $v$ is built and by Lemma 3 some target of $T$ is in $Z$, so $T \not\subseteq A$, which is false. So $v \in A$. As $A$ is closed, $\mathit{Lfp} \subseteq A$. The vertex $v_0$ was built at line L1 and never became true (else line L8 would have returned), so $v_0 \in Z$ and $v_0 \notin \mathit{Lfp}$. $\square$

**Theorem 1.** LOCAL-LFP$(v_0)$ terminates and returns true iff $v_0 \in \mathit{Lfp}$.

*Proof.* Termination is Lemma 2. A return at line L8 implies $v_0 \in \mathit{Lfp}$ by Lemma 1, and a return at line L15 implies $v_0 \notin \mathit{Lfp}$ by Lemma 4. $\square$

**The encoding.** Let $\varphi$ be a closed formula in positive normal form in which each variable is bound once, and in which each subformula $\nu Y.\, \chi$ is treated as a *leaf*: the vertex $(s, \nu Y.\, \chi)$ has one hyperedge with no targets if $s \models \nu Y.\, \chi$, and none otherwise. All other fixed points are least, and $(s, X)$ points to the binder $\mu X.\, \psi$ of $X$, as in the table of the page. For a subformula $\psi$ of $\varphi$, the free variables of $\psi$ are bound by binders outside $\psi$. Define the meaning $m(\psi) \subseteq S$ by $m(\psi) = [\![\psi]\!]_{\rho}$, where the environment $\rho$ maps each variable $X$ to $m(\mu X.\, \psi_X)$, the meaning of its binder. This is well defined by induction on the nesting depth of binders, since the meaning of a binder depends only on the binders outside it. For a closed $\varphi$, $m(\varphi)$ is the usual set of states that satisfy $\varphi$. Let $\mathit{Lfp}$ be the least solution of the dependency graph, and write $\mathit{Lfp}_\psi = \{s : (s, \psi) \in \mathit{Lfp}\}$.

**Lemma 5.** For each subformula $\psi$ of $\varphi$, $\mathit{Lfp}_\psi = m(\psi)$.

*Proof.* ($\subseteq$) The set $T^* = \{(s, \psi) : s \in m(\psi)\}$ is closed. Take a hyperedge of $(s, \psi)$ whose targets are all in $T^*$, and check $s \in m(\psi)$ by the form of $\psi$. For $\mathsf{true}$, literals and $\nu$ leaves, a hyperedge exists only when $s \in m(\psi)$. For $\psi_1 \wedge \psi_2$, $s \in m(\psi_1) \cap m(\psi_2) = m(\psi)$; for $\psi_1 \vee \psi_2$ similarly. For $\Diamond\psi'$, some successor $t$ has $t \in m(\psi')$; for $\Box\psi'$, every successor has. For $\mu X.\, \psi'$, $s \in m(\psi') = [\![\psi']\!]_\rho$ with $\rho(X) = m(\mu X.\, \psi')$, and since $m(\mu X.\, \psi')$ is a fixed point of $A \mapsto [\![\psi']\!]_{\rho[X \mapsto A]}$, $s \in m(\mu X.\, \psi')$. For a variable $X$, the target is $(s, \mu X.\, \psi_X)$, and $m(X) = \rho(X) = m(\mu X.\, \psi_X)$. So $T^*$ is closed and $\mathit{Lfp} \subseteq T^*$.

($\supseteq$) Let $\rho_L$ be the environment that maps each variable $X$ to $\mathit{Lfp}_{\mu X. \psi_X}$. We show $[\![\psi]\!]_{\rho_L} \subseteq \mathit{Lfp}_\psi$ for each subformula $\psi$, by induction on $\psi$, using that $\mathit{Lfp}$ is a fixed point of $F$, so a vertex is in $\mathit{Lfp}$ iff one of its hyperedges has all its targets in $\mathit{Lfp}$.

- Literals, $\mathsf{true}$, $\mathsf{false}$ and $\nu$ leaves: their hyperedges have no targets, so $\mathit{Lfp}_\psi = m(\psi)$, and $m(\psi)$ does not depend on the environment.
- $X$: the only hyperedge of $(s, X)$ has the target $(s, \mu X.\, \psi_X)$, so $\mathit{Lfp}_X = \mathit{Lfp}_{\mu X. \psi_X} = \rho_L(X)$.
- $\wedge$, $\vee$, $\Diamond$, $\Box$: by the induction hypothesis, the semantics of the operator, and the fixed-point property. For example, if $s \in [\![\Diamond\psi']\!]_{\rho_L}$, some successor $t$ is in $[\![\psi']\!]_{\rho_L} \subseteq \mathit{Lfp}_{\psi'}$, so the hyperedge with target $(t, \psi')$ puts $(s, \Diamond\psi')$ in $\mathit{Lfp}$.
- $\mu X.\, \psi'$: as $X$ is bound only here, $\rho_L[X \mapsto \mathit{Lfp}_{\mu X. \psi'}] = \rho_L$. By the induction hypothesis and the single hyperedge of $(s, \mu X.\, \psi')$, $[\![\psi']\!]_{\rho_L[X \mapsto \mathit{Lfp}_{\mu X. \psi'}]} = [\![\psi']\!]_{\rho_L} \subseteq \mathit{Lfp}_{\psi'} = \mathit{Lfp}_{\mu X. \psi'}$. So $\mathit{Lfp}_{\mu X. \psi'}$ is a pre-fixed point of $A \mapsto [\![\psi']\!]_{\rho_L[X \mapsto A]}$, and by Knaster-Tarski the least fixed point $[\![\mu X.\, \psi']\!]_{\rho_L}$ is contained in it.

It remains to show $\rho = \rho_L$; then $m(\psi) = [\![\psi]\!]_{\rho_L} \subseteq \mathit{Lfp}_\psi$ for each subformula $\psi$. By the first part, $\rho_L(Y) = \mathit{Lfp}_{\mu Y. \psi_Y} \subseteq m(\mu Y.\, \psi_Y) = \rho(Y)$ for every variable $Y$. For the other inclusion, go through the binders from the outside in. Suppose $\rho$ and $\rho_L$ agree on the variables of all binders outside $\mu Y.\, \psi_Y$ (for an outermost binder there are none). The free variables of $\mu Y.\, \psi_Y$ are among these, so $\rho(Y) = m(\mu Y.\, \psi_Y) = [\![\mu Y.\, \psi_Y]\!]_{\rho} = [\![\mu Y.\, \psi_Y]\!]_{\rho_L} \subseteq \mathit{Lfp}_{\mu Y. \psi_Y} = \rho_L(Y)$ by the claim above. So $\rho(Y) = \rho_L(Y)$, and by induction $\rho = \rho_L$. $\square$

**Greatest fixed points.** For a closed $\nu Y.\, \chi$, the positive normal form $\overline{\nu Y.\, \chi}$ of its negation satisfies $m(\overline{\nu Y.\, \chi}) = S \setminus m(\nu Y.\, \chi)$, by the duality $\neg \nu Y.\, \chi(Y) \equiv \mu Y.\, \neg\chi(\neg Y)$ and De Morgan. Its outermost operator is $\mu$. If $\varphi$ is alternation-free, each $\nu$ subformula that a search for a $\mu$ formula reaches lies below least fixed points only, and its free variables could only be bound by those least fixed points, which alternation-freedom forbids; so it is closed, and it is a proper subformula of the formula being searched. By induction on the size of the formula, each such leaf is decided correctly by its own call, and Lemma 5 and Theorem 1 apply to every call.

**Cost.** By Lemma 2, one call takes time linear in the part of the dependency graph it builds. The full graph has at most $|S| \cdot |\varphi|$ vertices, and the total size of its hyperedges is $O((|S| + |R|) \cdot |\varphi|)$, because the hyperedges of $(s, \Diamond\psi)$ and $(s, \Box\psi)$ have $|R(s)|$ targets in total and every other vertex has at most two. So a call for a formula with only least fixed points takes $O((|S| + |R|) \cdot |\varphi|)$ time and space. $\blacksquare$
