---
title: Proof of the graph minor theorem, in part
proves: [statement]
status: sketch
---

The full proof of Robertson and Seymour fills the twenty-three papers Graph Minors I to XXIII, and it is not given here. This file proves in full three parts: the Ramsey lemma on well-quasi-orders, the equivalence of the theorem with the finite obstruction form, and the theorem for trees. It then outlines the general proof. So the file has the status of a sketch. The proofs of the first three parts follow Diestel, Sections 12.1 and 12.2, and Nash-Williams (1963).

Graphs are finite, and isomorphic graphs are identified. A **quasi-order** $\le$ on a set $X$ is reflexive and transitive. A sequence $x_1, x_2, \ldots$ in $X$ is **good** if $x_i \le x_j$ for some $i < j$, and **bad** otherwise. $X$ is **well-quasi-ordered** if every infinite sequence is good. An **antichain** is a set of pairwise incomparable elements. $\le$ is **well-founded** if there is no infinite sequence with $x_{i+1} \le x_i$ and not $x_i \le x_{i+1}$ for all $i$ (a strictly decreasing sequence).

## Part 1: the Ramsey lemma

**Lemma 1.** For a quasi-order $(X, \le)$ the following are equivalent.

(a) $X$ is well-quasi-ordered.

(b) Every infinite sequence in $X$ has an infinite subsequence $x_{i_1}, x_{i_2}, \ldots$ ($i_1 < i_2 < \cdots$) with $x_{i_k} \le x_{i_l}$ for all $k < l$.

(c) $\le$ is well-founded, and $X$ has no infinite antichain.

*Proof.* (b) implies (a): take $x_{i_1} \le x_{i_2}$.

(a) implies (b): let $x_1, x_2, \ldots$ be a sequence. Colour each pair $\{i, j\}$ with $i < j$ red if $x_i \le x_j$ and blue otherwise. By the infinite Ramsey theorem for pairs there is an infinite set $I$ of indices all of whose pairs have the same colour. If the colour is blue, the subsequence on $I$ is bad, which contradicts (a). So it is red, and the subsequence on $I$ is as in (b).

(a) implies (c): a strictly decreasing sequence is bad, since $x_i \le x_j$ with $i < j$ would give $x_i \le x_j \le x_{j-1} \le \cdots \le x_{i+1}$ by transitivity, and that contradicts $x_{i+1} \le x_i$ and not $x_i \le x_{i+1}$. An infinite antichain, listed as a sequence of distinct elements, is bad.

(c) implies (a): let $x_1, x_2, \ldots$ be a sequence. Colour the pair $\{i, j\}$, $i < j$, red if $x_i \le x_j$, green if $x_j \le x_i$ and not $x_i \le x_j$, and blue if the two are incomparable. Ramsey's theorem gives an infinite set $I$ with one colour. Blue gives an infinite antichain: the elements on $I$ are pairwise incomparable, so they are distinct. Green gives a strictly decreasing sequence. Both are excluded by (c), so the colour is red and the sequence is good. $\square$

## Part 2: the obstruction form

Write $H \preceq G$ if $H$ is a minor of $G$. This is a quasi-order (a model of a model is a model), and since isomorphic graphs are identified, $H \preceq G \preceq H$ gives $H = G$. If $H \preceq G$ and $H \ne G$, then $H$ has fewer vertices plus edges than $G$, because each deletion or contraction lowers this number. So there is no strictly decreasing sequence: $\preceq$ is well-founded.

For a class $\mathcal{C}$ closed under minors, let $\mathrm{Obs}(\mathcal{C})$ be the set of graphs $G \notin \mathcal{C}$ all of whose proper minors are in $\mathcal{C}$.

**Lemma 2.** (i) $G \in \mathcal{C}$ if and only if no graph of $\mathrm{Obs}(\mathcal{C})$ is a minor of $G$. (ii) $\mathrm{Obs}(\mathcal{C})$ is an antichain.

*Proof.* (i) If $G \in \mathcal{C}$, every minor of $G$ is in $\mathcal{C}$, and graphs of $\mathrm{Obs}(\mathcal{C})$ are not. If $G \notin \mathcal{C}$, take a minor $H$ of $G$ with $H \notin \mathcal{C}$ and the fewest vertices plus edges. Every proper minor of $H$ is a minor of $G$ with fewer vertices plus edges, so it is in $\mathcal{C}$. So $H \in \mathrm{Obs}(\mathcal{C})$ and $H \preceq G$.

(ii) If $H, H' \in \mathrm{Obs}(\mathcal{C})$ and $H \preceq H'$ with $H \ne H'$, then $H$ is a proper minor of $H'$, so $H \in \mathcal{C}$, a contradiction. $\square$

**Theorem 3.** The following are equivalent: (A) the finite graphs are well-quasi-ordered by $\preceq$; (B) every class closed under minors has a finite obstruction set.

*Proof.* (A) implies (B): by Lemma 2(ii) and Lemma 1, (a) implies (c), $\mathrm{Obs}(\mathcal{C})$ is a finite antichain.

(B) implies (A): suppose $A$ is an infinite antichain. Let $\mathcal{C}$ be the class of graphs that have no member of $A$ as a minor; it is closed under minors by transitivity. Each $H \in A$ is not in $\mathcal{C}$, and a proper minor $H'$ of $H$ is in $\mathcal{C}$: if some $H'' \in A$ had $H'' \preceq H' \preceq H$, then $H'' \preceq H$ with $H'' \ne H$ (the minor $H'$ is smaller than $H$), which contradicts that $A$ is an antichain. So $A \subseteq \mathrm{Obs}(\mathcal{C})$, and the obstruction set is infinite, against (B). So there is no infinite antichain, $\preceq$ is well-founded, and Lemma 1, (c) implies (a), gives (A). $\square$

## Part 3: trees

A **rooted tree** is a finite tree $T$ with a chosen vertex $r(T)$, the root. The **branches** of $T$ are the subtrees $T_c$, one for each neighbour $c$ of the root: $T_c$ is the component of $T - r(T)$ that contains $c$, rooted at $c$. Define a relation $\sqsubseteq$ on rooted trees by recursion on the size of $T'$: $T \sqsubseteq T'$ if

1. $T \sqsubseteq B$ for some branch $B$ of $T'$, or
2. there is an injective map $f$ from the branches of $T$ to the branches of $T'$ with $B \sqsubseteq f(B)$ for each branch $B$ of $T$.

A single vertex has no branches, so case 2 with the empty map gives that a single vertex is $\sqsubseteq$ every rooted tree.

**Lemma 4.** If $T \sqsubseteq T'$, then $T'$ has a model of $T$ (as graphs) in which the branch set of $r(T)$ contains $r(T')$. In particular $T \preceq T'$.

*Proof.* Induction on the size of $T'$. In case 1, by induction $B$ has a model of $T$ whose root branch set contains $r(B)$, a neighbour of $r(T')$. Add $r(T')$ to the root branch set. It stays connected, because $r(T')$ is joined to $r(B)$, and the sets stay disjoint, because $r(T') \notin B$. In case 2, by induction each $f(B)$ has a model of $B$ whose root branch set contains $r(f(B))$. Take all these models together, and give $r(T)$ the branch set $\{r(T')\}$. The branches $f(B)$ are pairwise disjoint and do not contain $r(T')$, so the branch sets are disjoint. Each edge of $T$ either lies in a branch $B$, and is realized in the model of $B$, or joins $r(T)$ to $r(B)$, and is realized by the edge from $r(T')$ to $r(f(B))$, which is in the branch set of $r(B)$. $\square$

**Lemma 5.** Let $X$ be a set with a relation $\le$ such that every infinite sequence in $X$ is good. Let $X^*$ be the set of finite sequences in $X$, and write $(a_1, \ldots, a_p) \le^* (b_1, \ldots, b_q)$ if there is an injective map $g: \{1, \ldots, p\} \to \{1, \ldots, q\}$ with $a_i \le b_{g(i)}$ for all $i$. Then every infinite sequence in $X^*$ is good.

The relation $\le$ need not be transitive here; the argument of Lemma 1, (a) implies (b), uses only the colouring of pairs, so it still gives, from any infinite sequence in $X$, an infinite subsequence with $x_{i_k} \le x_{i_l}$ for all $k < l$.

*Proof.* Suppose some infinite sequence in $X^*$ is bad. Choose a **minimal bad sequence** $A_1, A_2, \ldots$: for each $n$ in turn, let $A_n$ be a sequence of least length such that some bad sequence starts with $A_1, \ldots, A_n$. The sequence $A_1, A_2, \ldots$ is bad, since any pair $i < j$ lies in the prefix $A_1, \ldots, A_j$, which starts a bad sequence. No $A_n$ is empty, because the empty sequence is $\le^*$ every sequence, so an empty $A_n$ would make $A_n \le^* A_{n+1}$. Write $A_n = A_n' a_n$, with $a_n$ the last term and $A_n'$ the rest.

Apply the remark above to $a_1, a_2, \ldots$: there are $n_1 < n_2 < \cdots$ with $a_{n_k} \le a_{n_l}$ for all $k < l$. Consider the sequence

$$A_1, \ldots, A_{n_1 - 1}, A_{n_1}', A_{n_2}', A_{n_3}', \ldots$$

It starts with $A_1, \ldots, A_{n_1 - 1}$ followed by $A_{n_1}'$, which is shorter than $A_{n_1}$, so by the choice of $A_{n_1}$ it is good. Take a pair $x \le^* y$ in it with $x$ earlier. Both cannot be among $A_1, \ldots, A_{n_1 - 1}$, since the minimal sequence is bad. If $x = A_i$ with $i < n_1$ and $y = A_{n_k}'$, then $A_i \le^* A_{n_k}' \le^* A_{n_k}$ (extend by nothing), with $i < n_k$. If $x = A_{n_k}'$ and $y = A_{n_l}'$ with $k < l$, then the map for $A_{n_k}' \le^* A_{n_l}'$, extended by sending the last position of $A_{n_k}$ to the last position of $A_{n_l}$, shows $A_{n_k} \le^* A_{n_l}$, because $a_{n_k} \le a_{n_l}$, and the extended map is still injective. In each case the minimal sequence is good, a contradiction. $\square$

**Theorem 6 (Kruskal, in the form of Nash-Williams).** Every infinite sequence of rooted trees is good for $\sqsubseteq$.

*Proof.* Suppose not, and choose a minimal bad sequence $T_1, T_2, \ldots$ as in Lemma 5, now with $T_n$ of the fewest vertices. Let $\mathcal{B}$ be the set of all branches of all $T_n$.

*Claim: every infinite sequence in $\mathcal{B}$ is good.* Suppose $C_1, C_2, \ldots$ is a bad sequence in $\mathcal{B}$, and let $C_k$ be a branch of $T_{n(k)}$. A bad sequence has no repeated term, since $C \sqsubseteq C$ holds for every rooted tree (by induction: case 2 with the identity map on branches). Each $T_n$ has finitely many branches, so each value $n(k)$ occurs for finitely many $k$. So there are $k_1 < k_2 < \cdots$ such that $n(k_1)$ is the least value of $n(k)$ over all $k$ and $n(k_1) < n(k_2) < \cdots$; a subsequence of a bad sequence is bad, so we may write $C_{k_l}$ as the new sequence. Consider

$$T_1, \ldots, T_{n(k_1) - 1}, C_{k_1}, C_{k_2}, \ldots$$

$C_{k_1}$ is a branch of $T_{n(k_1)}$, so it has fewer vertices. By the choice of $T_{n(k_1)}$, this sequence is good. Two of the $T_i$ cannot form the pair, nor two of the $C_{k_l}$. So $T_i \sqsubseteq C_{k_l}$ for some $i < n(k_1) \le n(k_l)$. Since $C_{k_l}$ is a branch of $T_{n(k_l)}$, case 1 of the definition gives $T_i \sqsubseteq T_{n(k_l)}$ with $i < n(k_l)$. So $T_1, T_2, \ldots$ is good, a contradiction. This proves the claim.

Now list the branches of each $T_n$ as a finite sequence $S_n \in \mathcal{B}^*$. By the claim and Lemma 5, the sequence $S_1, S_2, \ldots$ is good: $S_i \le^* S_j$ for some $i < j$. The injective map that shows it is a map $f$ from the branches of $T_i$ to those of $T_j$ with $B \sqsubseteq f(B)$, so case 2 gives $T_i \sqsubseteq T_j$, a contradiction. $\square$

**Corollary 7 (the graph minor theorem for trees).** The finite trees are well-quasi-ordered by the minor relation.

*Proof.* Given trees $T_1, T_2, \ldots$, root each at any vertex. By Theorem 6, $T_i \sqsubseteq T_j$ for some $i < j$, and by Lemma 4, $T_i \preceq T_j$. $\square$

Small cases: a single vertex is a minor of every tree; a path is a minor of a tree exactly when the tree has a path at least as long; the stars $K_{1,1}, K_{1,2}, \ldots$ form a chain, and no star $K_{1,3}$ or larger is a minor of a path.

## Part 4: outline of the general proof

The rest follows Robertson and Seymour, and Diestel, Chapter 12, which proves the case of a planar first graph in full and states the rest.

1. **Bounded tree-width (Graph Minors IV).** The argument of Theorem 6 extends from trees to tree decompositions of bounded width, with each node labelled by its bag. Graphs of tree-width less than a fixed $k$ are well-quasi-ordered by minors.
2. **The grid theorem (Graph Minors V).** For every planar graph $H$ there is an $N$ such that every graph of tree-width at least $N$ has $H$ as a minor.
3. **A planar first graph.** Let $G_1, G_2, \ldots$ be bad. Then no $G_j$, $j > 1$, has $G_1$ as a minor. If $G_1$ is planar, step 2 bounds the tree-width of all $G_j$, $j > 1$, and step 1 makes the sequence $G_2, G_3, \ldots$ good, a contradiction.
4. **The structure theorem (Graph Minors XVI).** For every graph $H$, every graph without an $H$ minor is a tree-like clique-sum of graphs that, after deleting a bounded number of apex vertices, embed in a surface on which $H$ does not embed, up to a bounded number of vortices of bounded depth.
5. **Well-quasi-ordering of such pieces (Graph Minors XVIII to XX).** By induction on the surface and on the number of vortices, the pieces of step 4 are well-quasi-ordered, in a strengthened form that keeps track of how they are glued. Running the tree argument on the clique-sum decompositions then makes $G_2, G_3, \ldots$ good when $G_1$ is not planar.

Steps 1 to 5 together give the theorem, and Theorem 3 gives the finite obstruction sets. $\blacksquare$
