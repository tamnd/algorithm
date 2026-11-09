---
title: Symbolic reachability computes the reachable states after d + 1 images
proves: [correctness]
status: full
---

We use the notation of the page. The state space is $S = \{0, 1\}^n$. We identify a Boolean function over $x$ with the set of states where it is true. A path is a sequence $s_0, s_1, \ldots, s_k$ with $T(s_{i-1}, s_i)$ for each $i$. The distance $\delta(s)$ of a state $s$ is the least $k$ such that a path $s_0, \ldots, s_k$ has $s_0 \in I$ and $s_k = s$, and $\delta(s) = \infty$ when there is no such path. So $\mathrm{Reach} = \{s : \delta(s) < \infty\}$. Let $D_i = \{s : \delta(s) = i\}$ and $d = \max \{\delta(s) : s \in \mathrm{Reach}\}$. As $S$ is finite and $I$ is not empty, $d$ is a finite number, and $d \le |S| - 1 = 2^n - 1$ because a shortest path visits no state twice. If $I$ is empty, the first image is empty, and the loop returns the empty set after one image; below we assume $I \ne \emptyset$.

**Lemma 1 (the relational product).** For BDDs $f$ and $g$ and a set $Q$ of variables, AND-EXISTS$(f, g, Q)$ returns the BDD of $\exists Q.\, f \wedge g$.

*Proof.* By induction on the sum of the sizes of $f$ and $g$. If one of them is false, the result is false, which is correct. If both are true, the result is true. If one is true, the result is the quantification of the other, which is correct by the same argument for a single BDD. Else let $v$ be the smaller of the top variables, and let $f_b = f|_{v=b}$ and $g_b = g|_{v=b}$ for $b \in \{0, 1\}$. These cofactors are the children when $v$ is the top variable, and $f$ itself when it is not. By the [Shannon expansion](/shannon-expansion/), $f \wedge g = (\neg v \wedge f_0 \wedge g_0) \vee (v \wedge f_1 \wedge g_1)$, and the four cofactors do not depend on $v$. Existential quantification commutes with itself and distributes over $\vee$. If $v \notin Q$, then
$$\exists Q.\, f \wedge g = (\neg v \wedge \exists Q.\, f_0 \wedge g_0) \vee (v \wedge \exists Q.\, f_1 \wedge g_1),$$
which is the node $(v, \mathrm{AE}(f_0, g_0), \mathrm{AE}(f_1, g_1))$. If $v \in Q$, then
$$\exists Q.\, f \wedge g = \exists (Q \setminus \{v\}).\, \exists v.\, f \wedge g = \exists (Q \setminus \{v\}).\, \big((f_0 \wedge g_0) \vee (f_1 \wedge g_1)\big) = \mathrm{AE}(f_0, g_0) \vee \mathrm{AE}(f_1, g_1),$$
where the last step uses $\exists Q.\, h = \exists (Q \setminus \{v\}).\, h$ for $h$ that does not depend on $v$. When $\mathrm{AE}(f_0, g_0)$ is true, the disjunction is true without the second call. The recursive calls are on smaller BDDs, so the induction hypothesis applies. A cached result is a result of the same call, so the cache does not change the value. ∎

**Lemma 2 (image and preimage).** With $Q = x$ (and the inputs, for a circuit), IMAGE$(F, T)$ is the BDD of $\mathrm{Post}(F) = \{t : \exists s \in F.\, T(s, t)\}$ over $x$. With $Q = x'$, AND-EXISTS$(T, F[x := x'], x')$ is the BDD of $\mathrm{Pre}(F) = \{s : \exists t \in F.\, T(s, t)\}$.

*Proof.* By Lemma 1, $P = \exists x.\, F(x) \wedge T(x, x')$, a function of $x'$ that is true at $t$ exactly when some $s \in F$ has $T(s, t)$. The renaming replaces $x'_j$ by $x_j$ in each node. With an order in which $x_j$ and $x'_j$ are adjacent and $P$ has no $x$ variable, the renamed diagram is still ordered and reduced, and it denotes the same set over $x$. For a circuit, $T$ also has the input variables $w$; quantifying them with $x$ gives $\exists x, w.\, F(x) \wedge \bigwedge_j (x'_j \leftrightarrow f_j(x, w))$, which is the set of states $f(s, w)$ with $s \in F$ and any input $w$. The proof for $\mathrm{Pre}$ is the same, with the roles of $x$ and $x'$ exchanged. ∎

**Lemma 3 (the loop invariant).** Let $R_i$ and $F_i$ be the values of $R$ and $F$ after $i$ iterations of the loop, with $R_0 = F_0 = I$. Then for each $i \ge 0$ that the loop reaches,
$$F_i = D_i \quad \text{and} \quad R_i = D_0 \cup D_1 \cup \ldots \cup D_i.$$

*Proof.* For $i = 0$: $D_0 = I$ by the definition of the distance, so $F_0 = R_0 = D_0$. Assume the claim for $i$. By Lemma 2, line L4 sets $N = \mathrm{Post}(D_i)$. We show $\mathrm{Post}(D_i) \setminus (D_0 \cup \ldots \cup D_i) = D_{i+1}$.

($\subseteq$) Let $t \in \mathrm{Post}(D_i)$ with $\delta(t) > i$. A path of length $i$ to some $s \in D_i$ and the edge $(s, t)$ give a path of length $i + 1$ to $t$, so $\delta(t) \le i + 1$, and therefore $\delta(t) = i + 1$.

($\supseteq$) Let $\delta(t) = i + 1$, with a shortest path $s_0, \ldots, s_{i+1} = t$. Then $\delta(s_i) \le i$. If $\delta(s_i) < i$, then $t$ has a path of length at most $i$, which contradicts $\delta(t) = i + 1$. So $s_i \in D_i$ and $t \in \mathrm{Post}(D_i)$, and $t$ is not in $D_0 \cup \ldots \cup D_i$.

So line L5 gives $F_{i+1} = D_{i+1}$, and line L6 gives $R_{i+1} = R_i \cup D_{i+1} = D_0 \cup \ldots \cup D_{i+1}$. ∎

**Theorem.** SYMBOLIC-REACH terminates after exactly $d + 1$ images and returns $\mathrm{Reach}$.

*Proof.* By Lemma 3, the test of line L7 after iteration $i$ checks whether $D_i$ is empty. For $1 \le i \le d$ the set $D_i$ is not empty: take a state $s$ with $\delta(s) = d$ and a shortest path to it; its state number $i$ has distance exactly $i$, since a shorter path to it would give a shorter path to $s$. And $D_{d+1}$ is empty by the choice of $d$. So the loop stops after iteration $d + 1$, which makes $d + 1$ images. It returns $R_{d+1} = D_0 \cup \ldots \cup D_{d+1} = \{s : \delta(s) \le d\} = \mathrm{Reach}$. ∎

**Remark (other frontiers).** If line L4 images any set $G_i$ with $F_i \subseteq G_i \subseteq R_i$, the proof of Lemma 3 still holds. Indeed $\mathrm{Post}(G_i) \supseteq \mathrm{Post}(D_i)$, and $\mathrm{Post}(G_i) \subseteq \mathrm{Post}(R_i) \subseteq D_0 \cup \ldots \cup D_{i+1}$ by the ($\subseteq$) argument applied to each $D_j$ with $j \le i$. After removing $R_i$, both give $D_{i+1}$. With $G_i = R_i$ we get the variant that images the full set.

**Remark (the fixed point).** The returned set is the least fixed point of $\tau(Z) = I \cup \mathrm{Post}(Z)$ on the lattice of subsets of $S$. It is a fixed point because $\mathrm{Post}(\mathrm{Reach}) \subseteq \mathrm{Reach}$. Any fixed point $Z$ contains $D_0 = I$, and by induction it contains each $D_{i+1} \subseteq \mathrm{Post}(D_i)$. So $\mathrm{Reach} \subseteq Z$, as the [Knaster-Tarski theorem](/knaster-tarski-theorem/) and Kleene iteration also give.
