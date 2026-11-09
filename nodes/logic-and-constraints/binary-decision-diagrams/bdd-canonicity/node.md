---
tag: XF4MMQ
kind: theorem
slug: bdd-canonicity
name: Canonicity of reduced ordered BDDs
aliases:
- Bryant canonical form
- uniqueness of the ROBDD
- ROBDD canonicity theorem
area: logic-and-constraints/binary-decision-diagrams
level: core
summary: For a fixed order each boolean function has exactly one ROBDD, so equivalence is a pointer comparison.
prereqs: [reduced-ordered-bdd, bdd-reduction-rules, shannon-expansion, cofactor]
see_also: [reduced-ordered-bdd, bdd-reduction-rules, boolean-equivalence-checking, complemented-edges, variable-ordering, minimal-dfa-uniqueness, hash-consing, free-binary-decision-diagram]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 2, Definitions 1 to 5, Lemmas 1 and 2, and Theorem 1 (a unique reduced function graph for each function, and any other function graph for it has more vertices), proved by induction on the size of the dependency set
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the nodes of the BDD as the beads of the truth table)
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 3, OBDDs (the reduced OBDD is unique up to isomorphism and has minimal size for its order)
  - paper: doi:10.1109/DAC.1990.114826
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 40 to 45
    locator: the unique table, which gives a strong canonical form, so that equal functions have the same pointer
---

The canonicity theorem says that, for a fixed variable order, each [Boolean function](/boolean-function/) has exactly one [reduced ordered BDD](/reduced-ordered-bdd/), up to isomorphism, and that every other [ordered BDD](/ordered-binary-decision-diagram/) of the function with that order has more nodes. Bryant proved it in 1986 as Theorem 1 of the paper that made BDDs a standard tool. With a unique table, which applies the [reduction rules](/bdd-reduction-rules/) to each node as it is made, the theorem makes [equivalence checking](/boolean-equivalence-checking/) of two functions in one store a comparison of two pointers.

## Statement

Fix an order $\pi = (\pi_1, \ldots, \pi_n)$ of the variables $x_1, \ldots, x_n$. All diagrams below are ordered by $\pi$, and every node is reachable from the root. For $f \in B_n$ and $1 \le k \le n + 1$, let

$$\mathcal{S}_k(f) = \{\, f|_{x_{\pi_1}=a_1, \ldots, x_{\pi_{k-1}}=a_{k-1}} : a \in \{0,1\}^{k-1} \,\}$$

be the set of [cofactors](/cofactor/) of $f$ by the first $k - 1$ variables of the order, and let $\mathcal{N}_k(f) \subseteq \mathcal{S}_k(f)$ be the ones that depend on $x_{\pi_k}$. Let $\mathcal{N}_{n+1}(f) = \mathcal{S}_{n+1}(f)$, the set of constants that $f$ takes.

**Theorem.** Let $f \in B_n$.

1. (Existence) $f$ has a reduced ordered BDD.
2. (Structure) In each reduced ordered BDD $R$ of $f$, the map $u \mapsto f_u$ is a bijection from the nodes of level $k$ onto $\mathcal{N}_k(f)$, for each $k$. An inner node $u$ with $f_u = g$ has $\mathrm{var}(u) = x_{\pi_k}$, $f_{\mathrm{lo}(u)} = g|_{x_{\pi_k}=0}$ and $f_{\mathrm{hi}(u)} = g|_{x_{\pi_k}=1}$.
3. (Uniqueness) Any two reduced ordered BDDs of $f$ are isomorphic: there is a bijection between their nodes that keeps the variables, the labels of the terminals, and the lo and hi edges.
4. (Minimality) Every ordered BDD of $f$ has at least $|\mathcal{N}_k(f)|$ nodes on level $k$, for each $k$. So it has at least $|R| = \sum_k |\mathcal{N}_k(f)|$ nodes, with equality only if it is reduced.

**Corollary.** In a store where every node is made by MK, so that the whole store is one reduced ordered diagram with many roots, two nodes $u$ and $v$ have $f_u = f_v$ if and only if $u = v$.

## In plain words

Fix the order in which a flow chart asks about the inputs. Then there is exactly one smallest chart for each yes or no task, and every other chart for the task with this order is larger. The smallest chart is the one where no question is wasted and no part is drawn twice. Each box of it stands for one way the task can look after some first inputs are known, as long as the next input still matters. Two people who each build the smallest chart for the same task get the same drawing. So a program that only ever keeps smallest charts can test two tasks for sameness by checking if they are the same chart.

## Proof

Write $\mathrm{lev}(u)$ for the level of a node: $\mathrm{lev}(u) = k$ if $u$ tests $x_{\pi_k}$, and $\mathrm{lev}(u) = n + 1$ for a terminal. In an ordered BDD, all nodes below a node $u$ have a larger level than $u$, so $f_{\mathrm{lo}(u)}$ and $f_{\mathrm{hi}(u)}$ do not depend on $\mathrm{var}(u)$. By part 5 of the [Shannon expansion](/shannon-expansion/), they are the cofactors of $f_u$ by $\mathrm{var}(u) = 0$ and $\mathrm{var}(u) = 1$.

**Lemma A (every needed function has a node).** Let $D$ be an ordered BDD of $f$ with root $r$, let $1 \le k \le n + 1$, and let $g \in \mathcal{N}_k(f)$. Then $D$ has a node $w$ on level $k$ with $f_w = g$.

*Proof.* Let $g = f|_a$ for $a \in \{0,1\}^{k-1}$. Start at $r$, and while the current node $u$ has $\mathrm{lev}(u) < k$, go to $\mathrm{hi}(u)$ if $u$ tests $x_{\pi_j}$ with $a_j = 1$, and to $\mathrm{lo}(u)$ otherwise. The level grows at each step, so the walk stops at a node $w$ with $\mathrm{lev}(w) \ge k$. Each step goes from $f_u$ to its cofactor by one of the variables $x_{\pi_1}, \ldots, x_{\pi_{k-1}}$, set as in $a$. A variable of this prefix that the walk skips does not occur below the node where it was skipped, so fixing it does not change the function. So $f_w = f|_a = g$. If $k \le n$, $g$ depends on $x_{\pi_k}$. A node of level more than $k$ has no node on level $k$ below it, so its function does not depend on $x_{\pi_k}$. So $\mathrm{lev}(w) = k$. If $k = n + 1$, $w$ is a terminal with the label $g$. $\square$

**Lemma B (in a reduced diagram, distinct nodes have distinct functions).** Let $R$ be a reduced ordered BDD. If $u \ne v$ are nodes of $R$, then $f_u \ne f_v$. Also, the function of each inner node $u$ depends on $\mathrm{var}(u)$.

*Proof.* By induction on $m = \min(\mathrm{lev}(u), \mathrm{lev}(v))$, downward from $n + 1$. For $m = n + 1$, both are terminals. They are distinct, so by the merging rule they have different labels, and their functions are the two different constants.

Let $m \le n$, and assume the claim for all pairs with a larger minimum level. First, an inner node $w$ on level $m$ depends on $x_{\pi_m}$: its children are distinct (elimination rule) and have levels larger than $m$, so by the induction hypothesis $f_{\mathrm{lo}(w)} \ne f_{\mathrm{hi}(w)}$. These are the two cofactors of $f_w$ by $x_{\pi_m}$, so $f_w$ depends on $x_{\pi_m}$.

Now let $\mathrm{lev}(u) = m$ and suppose $f_u = f_v$. Then $f_v$ depends on $x_{\pi_m}$. If $\mathrm{lev}(v) > m$, no node below $v$ tests $x_{\pi_m}$, which is impossible. So $\mathrm{lev}(v) = m$, and $u$ and $v$ test the same variable. Their children are the cofactors of the same function, so $f_{\mathrm{lo}(u)} = f_{\mathrm{lo}(v)}$ and $f_{\mathrm{hi}(u)} = f_{\mathrm{hi}(v)}$. These children have levels larger than $m$, so by the induction hypothesis $\mathrm{lo}(u) = \mathrm{lo}(v)$ and $\mathrm{hi}(u) = \mathrm{hi}(v)$. Then the merging rule applies to $u$ and $v$, which contradicts that $R$ is reduced. So $f_u \ne f_v$. $\square$

**Part 1.** Take any ordered BDD of $f$, for example its decision tree, and apply the reduction rules until none applies. This stops, and the result is ordered and still has $f$ at the root, as the page on the [reduction rules](/bdd-reduction-rules/) shows. Nodes that are no longer reachable are dropped.

**Part 2.** Let $u$ be a node of $R$ on level $k$. It is reachable from the root $r$ by a path. Along the path each step goes to a cofactor by a variable of the prefix $\pi_1, \ldots, \pi_{k-1}$, and a skipped variable does not occur below the point where it is skipped. So $f_u = f|_a$ for an assignment $a$ that agrees with the tests of the path and is arbitrary on the skipped variables, and $f_u \in \mathcal{S}_k(f)$. By Lemma B, $f_u$ depends on $x_{\pi_k}$ if $k \le n$, so $f_u \in \mathcal{N}_k(f)$. The map is onto by Lemma A and one-to-one by Lemma B. The statement about the children is the cofactor property at the start of the proof.

**Part 3.** Let $R$ and $R'$ be reduced ordered BDDs of $f$. Map a node $u$ of $R$ on level $k$ to the node $u'$ of $R'$ on level $k$ with $f_{u'} = f_u$. By part 2 for both diagrams, this is a bijection on each level, so on all nodes. It keeps variables, since both nodes are on level $k$, and labels, since terminals with the same function have the same label. It keeps edges: $f_{\mathrm{lo}(u)}$ is the cofactor $f_u|_{x_{\pi_k}=0} = f_{u'}|_{x_{\pi_k}=0} = f_{\mathrm{lo}(u')}$, so the map sends $\mathrm{lo}(u)$ to $\mathrm{lo}(u')$, and the same holds for hi.

**Part 4.** Let $D$ be any ordered BDD of $f$. By Lemma A, $D$ has a node on level $k$ for each $g \in \mathcal{N}_k(f)$, and these nodes are distinct because their functions are distinct. So $D$ has at least $|\mathcal{N}_k(f)|$ nodes on level $k$, and at least $|R|$ nodes in all. Suppose $|D| = |R|$. Then each level of $D$ has exactly the nodes of Lemma A. If some inner node $u$ of $D$ had $\mathrm{lo}(u) = \mathrm{hi}(u)$, then $f_u$ would not depend on $\mathrm{var}(u)$, so $f_u$ would not be in $\mathcal{N}_k(f)$, and $u$ would be an extra node. If two distinct nodes had the same triple, they would have the same function, and one of them would be an extra node. So $D$ is reduced.

**Corollary.** The MK operation applies the elimination rule and then the merging rule, through the unique table, to each node it makes. So no node of the store has equal children and no two nodes have the same triple, and the store, seen from any root, is a reduced ordered diagram. Lemma B, applied to the whole store, gives $f_u = f_v \Rightarrow u = v$. $\blacksquare$

## Consequences

- **Equivalence in constant time.** In a BDD package, $f = g$ is the test $u = v$ on the two roots. So is the tautology test $f = 1$ and the satisfiability test $f \ne 0$. Implication $f \to g$ is the test $f \wedge \neg g = 0$, which costs one [APPLY](/bdd-apply/).
- **Size is a property of the function.** The size $B_\pi(f) = \sum_k |\mathcal{N}_k(f)|$ depends only on $f$ and $\pi$. Lower bounds on BDD size, such as the [multiplier lower bound](/multiplier-bdd-lower-bound/), are proved by counting the cofactors in $\mathcal{N}_k(f)$, which is what part 4 allows.
- **Counting levels from the truth table.** With $\pi$ the natural order and the table convention of these pages, the table of a cofactor in $\mathcal{S}_k(f)$ is a block of $2^{n-k+1}$ entries. It depends on $x_k$ exactly when its two halves differ. Knuth calls such a block a bead, and part 2 says that the nodes on level $k$ are the distinct beads of that length.
- **Results of operations need no extra reduction.** Any procedure that makes nodes only through MK, such as [ITE](/ite-operator/), APPLY or [quantification](/bdd-quantification/), returns the canonical diagram of its result.
- **[Complemented edges](/complemented-edges/)** keep canonicity only with an extra rule on where the negation bits may sit. That page proves the variant.

## Tightness

**The order must be fixed.** For a different order, the reduced diagram can be very different. The function $x_1 x_2 \vee x_3 x_4 \vee x_5 x_6$ has 8 nodes with the order $x_1, \ldots, x_6$ and 16 nodes with the order $x_1, x_3, x_5, x_2, x_4, x_6$; in general the sizes are $2k + 2$ and $2^{k+1}$ for $k$ pairs. Minimality is per order, and finding the order with the smallest diagram is a hard problem; see [variable ordering](/variable-ordering/).

**The diagram must be ordered.** For [free BDDs](/free-binary-decision-diagram/) the theorem fails. The diagrams $x_1 \to x_2$ and $x_2 \to x_1$ (test one variable, then the other on the high edge) are both reduced free BDDs of $x_1 \wedge x_2$, with 4 nodes each, and they are not isomorphic. A free BDD of $f$ may also mix orders on different paths, so there is no single set $\mathcal{N}_k(f)$ to count.

**Both rules are needed for minimality, but not for uniqueness.** The diagram with only the merging rule and no skipped levels, the quasi-reduced diagram, is also unique for $f$ and $\pi$, by the same proof with $\mathcal{S}_k(f)$ in place of $\mathcal{N}_k(f)$. It is larger whenever some cofactor does not depend on its next variable. Without the merging rule there is no uniqueness: the decision tree with shared terminals and a tree with some subtrees shared are different ordered diagrams of the same function.

**Pointer equality needs one store.** The theorem gives isomorphism. Two separate stores, or one store with nodes made outside MK, can hold two copies of the same function at different addresses.

## History

Bryant (1986) defined function graphs with an increasing index along each path, the reduced form (Definition 5), and isomorphism, and proved Theorem 1: for each Boolean function there is a unique reduced function graph up to isomorphism, and every other function graph for it has more vertices. His proof is by induction on the number of variables that the function depends on. The level-by-level proof on this page is in the style of Wegener (2000) and of Knuth (2011), who describes the nodes as the beads of the truth table. The idea is the same as the uniqueness of the [minimal deterministic automaton](/minimal-dfa-uniqueness/), in which states are the classes of an equivalence of suffixes. Brace, Rudell and Bryant (1990) built the theorem into their package as a strong canonical form: the unique table keeps the store reduced at every moment, so equal functions are equal pointers.

## References
