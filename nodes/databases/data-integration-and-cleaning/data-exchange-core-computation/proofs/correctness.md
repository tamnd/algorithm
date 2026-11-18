---
title: The block method returns the core of the universal solutions for source-to-target tgds
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The mapping is a finite set $\Sigma$ of source-to-target tgds $\forall x\, (\varphi(x) \to \exists y\, \psi(x, y))$, with no target dependencies. An instance is a finite set of facts. A value is a constant or a labeled null. A homomorphism $h : K \to L$ maps values to values, is the identity on constants, and maps each fact of $K$ to a fact of $L$. An instance $C$ is a *core* if there is no homomorphism from $C$ to a proper subset of $C$. A *core of* $K$ is a subset $C \subseteq K$ that is a core and has a homomorphism $K \to C$. A target instance $K$ is a *solution* for a source instance $I$ if $(I, K)$ satisfies $\Sigma$, and it is *universal* if it has a homomorphism into each solution.

Let $w$ be the largest number of existential variables in one tgd and let $a$ be the largest number of atoms in one head.

**Lemma 1 (the chase).** Lines L8 to L11 return a universal solution $J$.

*Proof.* A *trigger* is a tgd with an assignment $m$ of its body variables that maps the body into $I$. For each trigger, line L10 adds the head with fresh nulls for the existential variables. So each trigger has a witness in $J$, and $J$ is a solution. Let $K$ be any solution. For each trigger, $K$ has values $b$ for the existential variables such that $\psi(m(x), b)$ holds in $K$. Map the fresh nulls of that trigger to $b$. The nulls of different triggers are different, so this defines one map $h$, and $h$ is the identity on constants. Each fact of $J$ comes from one trigger and $h$ maps it to a fact of $K$. So $h : J \to K$. $\square$

**Lemma 2 (small blocks).** Each fact of $J$ holds nulls of one trigger only. So each block of $J$ has at most $w$ nulls, and at most $a$ facts of $J$ hold a null of a given block.

*Proof.* A fact added at line L10 holds constants of $I$ and nulls made for its own trigger. Two nulls are in one block only if a chain of facts joins them, and each fact of the chain stays within one trigger. The facts that hold a null of the block all come from the head of that trigger. $\square$

**Lemma 3 (groups).** Let $K$ be an instance, and split its nulls into groups $G_1, \ldots, G_k$ such that each fact holds nulls of at most one group. Let $F_i$ be the set of facts that hold a null of $G_i$. Call a map $h$ from $G_i$ to the values of $K$ a *witness* for $i$ if $h(F_i) \subseteq K$ and $h(F_i) \neq F_i$, where $h$ is the identity on all other values. Then $K$ is a core if and only if no group has a witness.

*Proof.* Assume $h$ is a witness for $i$. Let $g$ be $h$ on $G_i$ and the identity elsewhere. A fact outside $F_i$ holds no null of $G_i$, so $g$ fixes it, and $g(K) = (K \setminus F_i) \cup h(F_i) \subseteq K$. Since $|h(F_i)| \le |F_i|$ and $h(F_i) \neq F_i$, some fact $f \in F_i$ is not in $h(F_i)$. It is also not in $K \setminus F_i$, so $f \notin g(K)$. So $g$ maps $K$ to a proper subset of $K$, and $K$ is not a core.

Now assume $K$ is not a core: some homomorphism $r$ maps $K$ into a proper subset of $K$. Each fact of $K$ is ground or is in exactly one $F_i$, and $r$ fixes the ground facts. If $r(F_i) = F_i$ for each $i$, then $r(K) = K$, which is false. So $r(F_i) \neq F_i$ for some $i$. The facts of $F_i$ hold only constants and nulls of $G_i$, so the restriction of $r$ to $G_i$ maps $F_i$ to $r(F_i) \subseteq K$, and it is a witness for $i$. $\square$

**Lemma 4 (one step).** Let $J_t$ be the instance before an execution of line L5, with a witness $h$ for the current group with facts $F$. Then $J_{t+1} = J_t \setminus (F \setminus h(F)) = g(J_t)$ for the map $g$ of Lemma 3, and $J_{t+1}$ is a proper subset of $J_t$.

*Proof.* By the first part of the proof of Lemma 3, $g(J_t) = (J_t \setminus F) \cup h(F)$. Since $h(F) \subseteq J_t$, this is $J_t \setminus (F \setminus h(F))$. The set $F \setminus h(F)$ is not empty, as shown there. $\square$

**Invariant.** Let $B_1, \ldots, B_k$ be the blocks of $J$ in the order of line L2. At each time, let the group $G_i$ be the set of nulls of $B_i$ that still occur, and let $F_i$ be the facts that hold one of them. Every fact of the current instance is a fact of $J$, so it holds nulls of at most one group, and Lemma 3 applies to the groups. Line L3 sets the variable $F$ to $F_i$ when block $i$ starts, and lines L5 and L6 keep $F = F_i$, because line L5 removes only facts of $F_i$. For the same reason, the work on block $j$ does not change $F_i$ for $i \neq j$.

**Theorem.** The procedure stops and returns an instance $C$ such that $C \subseteq J$, there is a homomorphism $J \to C$, $C$ is a core, and $C$ is a universal solution.

*Proof.* *Termination.* Each pass through line L5 removes at least one fact by Lemma 4, so there are at most $|J|$ passes in total. Each witness search of line L4 is over a finite set of maps.

*Subset and homomorphism.* By Lemma 4, the instance only shrinks, and each step is the image of the instance before it under a homomorphism. The composition of these maps is a homomorphism $G : J \to C$ with $G(J) = C$.

*Core.* Fix $i$. When the loop of block $i$ ends, there is no witness for $i$ in the instance $J'$ of that time. After that, $F_i$ does not change, by the invariant, and the instance only shrinks, so $C \subseteq J'$. A witness for $i$ in $C$ maps $F_i$ into $C \subseteq J'$, so it would be a witness in $J'$. So no group has a witness in $C$, and $C$ is a core by Lemma 3.

*Universal solution.* Let a trigger with assignment $m$ hold in $I$. By Lemma 1, $J$ has the facts $\psi(m(x), y_0)$ for the fresh nulls $y_0$. Then $C = G(J)$ has the facts $\psi(m(x), G(y_0))$, because $G$ fixes the constants $m(x)$. So $C$ is a solution. For a solution $K$, Lemma 1 gives $J \to K$, and $C \subseteq J$, so the inclusion followed by that map is a homomorphism $C \to K$. $\blacksquare$

**Corollary (one core for all universal solutions).** Let $C_1$ and $C_2$ be cores, with homomorphisms $f : C_1 \to C_2$ and $g : C_2 \to C_1$. Then $C_1$ and $C_2$ are isomorphic. So all universal solutions have isomorphic cores, the core $C$ above is the core of each of them, and no universal solution has fewer facts than $C$.

*Proof.* The map $g \circ f$ sends $C_1$ into $C_1$. Since $C_1$ is a core, its image is all of $C_1$. So $g \circ f$ is onto the facts of $C_1$, hence onto its values, and as these are finite it is a bijection on them. So $f$ is one to one on values, and $|C_1| = |f(C_1)| \le |C_2|$. In the same way $|C_2| \le |C_1|$, so $f(C_1) = C_2$. The inverse of $f$ on values maps each fact $f(c)$ back to $c$, so it is a homomorphism, and $f$ is an isomorphism.

Two universal solutions $U_1$ and $U_2$ have homomorphisms each way, so their cores, which are subsets with homomorphisms from them, have homomorphisms each way and are isomorphic. If $U$ is a universal solution and $C'$ is a core of $U$, then $C' \subseteq U$ and $C'$ is isomorphic to $C$, so $|C| = |C'| \le |U|$. $\square$

**Running time.** Fix $\Sigma$, so $w$, $a$ and the arities are constants. Let $m = |J|$, so the number of values of $J$ is $O(m)$. Line L4 runs at most $m$ times with success and at most once per block without, so at most $2m$ times. One search backtracks over the at most $a$ facts of $F$. Each node of the search tree is a partial map of the nulls of $F$, and different nodes at one depth give different partial maps, so there are at most $(a + 1) \cdot O(m)^w$ nodes. Each node scans the facts of one relation, $O(m)$ work, and building the index takes $O(m \log m)$. So one search takes $O(m^{w+1})$ time, and the whole run takes $O(m^{w+2})$ time. For a fixed $\Sigma$, $m$ is polynomial in $|I|$, so this is polynomial time in data complexity.
