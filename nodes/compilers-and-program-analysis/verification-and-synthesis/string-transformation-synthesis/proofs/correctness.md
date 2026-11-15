---
title: The product DAG holds exactly the consistent programs, and the search returns a cheapest one
proves: [correctness]
status: full
---

**Setting.** A program is a list of atoms $f_1, \ldots, f_n$ with $n \ge 1$. An atom is ConstStr$(c)$ with a non-empty string $c$, or SubStr$(p_1, p_2)$ with two position expressions. On an input $\sigma$, a position expression denotes an index in $0, \ldots, |\sigma|$ or is undefined. SubStr$(p_1, p_2)$ gives $\sigma[a .. b)$ when $p_1$ denotes $a$, $p_2$ denotes $b$ and $a < b$, and is undefined otherwise. A program gives the concatenation of its atoms, and it is undefined if one atom is undefined. $P_\sigma(t)$ is the set of all position expressions of the language that denote $t$ on $\sigma$. Line numbers refer to the pseudocode on the page.

A *rectangle* $(A, B)$ with sets of position expressions $A$ and $B$ stands for the atoms SubStr$(p_1, p_2)$ with $p_1 \in A$ and $p_2 \in B$. A label $W$ is a set of constants together with a list of rectangles, and it stands for the union of these atoms.

## Lemma 1: one example

**Claim.** For an example $(\sigma, o)$ and $0 \le i < j \le |o|$, the label $W(i, j)$ built by lines L8 to L12 holds exactly the atoms that give $o[i .. j)$ on $\sigma$. Its rectangles have pairwise disjoint first sets.

**Proof.** ConstStr$(c)$ gives $c$, and line L9 puts in the one constant $o[i .. j)$. SubStr$(p_1, p_2)$ gives $o[i .. j)$ exactly when $p_1$ denotes some $a$, $p_2$ denotes $b = a + (j - i)$, and $\sigma[a .. b) = o[i .. j)$. Line L10 tries every $a$ with this property, and line L11 adds the rectangle $(P_\sigma(a), P_\sigma(a + j - i))$, which holds exactly the atoms with these two positions. A position expression denotes one index on $\sigma$, so the sets $P_\sigma(a)$ for different $a$ are disjoint. $\square$

**Claim.** A program $f_1, \ldots, f_n$ gives $o$ on $\sigma$ if and only if there are indices $0 = t_0 < t_1 < \cdots < t_n = |o|$ with $f_r \in W(t_{r-1}, t_r)$ for each $r$. The indices are unique.

**Proof.** If the program gives $o$, each atom gives a non-empty string, so the atoms cut $o$ into $n$ non-empty pieces. Let $t_r$ be the length of the output of $f_1, \ldots, f_r$. Then $f_r$ gives $o[t_{r-1} .. t_r)$, and $f_r \in W(t_{r-1}, t_r)$ by the first claim. The $t_r$ are fixed by the lengths of the outputs, so they are unique. In the other direction, each $f_r$ gives $o[t_{r-1} .. t_r)$, and the concatenation is $o$. $\square$

## Lemma 2: the intersection of labels

**Claim.** For labels $W$ and $W'$, the label $W \cap W'$ of line L5 holds exactly the atoms in both. If the rectangles of each label have pairwise disjoint first sets, so do the rectangles of the result.

**Proof.** A constant is in both when it is in both sets of constants. An atom SubStr$(p_1, p_2)$ is in both when some rectangle $(A, B)$ of $W$ and some $(A', B')$ of $W'$ hold it, that is, when $p_1 \in A \cap A'$ and $p_2 \in B \cap B'$. The result has the rectangle $(A \cap A', B \cap B')$ for each such pair with non-empty parts, so it holds exactly these atoms. Two rectangles of the result come from different pairs; they differ in the rectangle of $W$ or in that of $W'$, so their first sets are subsets of two disjoint sets. $\square$

## Lemma 3: the product DAG

Let the examples be $(\sigma_1, o_1), \ldots, (\sigma_k, o_k)$ with non-empty outputs. A state is a tuple $u = (u_1, \ldots, u_k)$ with $0 \le u_j \le |o_j|$. Lines L3 to L6 have an edge from $u$ to $w$, with the label $W_1(u_1, w_1) \cap \cdots \cap W_k(u_k, w_k)$, when $u_j < w_j$ for all $j$ and the label is not empty.

**Claim.** A program is consistent with all examples if and only if it is the list of atoms along a path from $(0, \ldots, 0)$ to $(|o_1|, \ldots, |o_k|)$, with one atom taken from the label of each edge. Each consistent program comes from exactly one path.

**Proof.** Let the program $f_1, \ldots, f_n$ be consistent. Lemma 1 gives, for each example $j$, unique indices $t^j_0 < \cdots < t^j_n$. The states $u^r = (t^1_r, \ldots, t^k_r)$ form a path: each component grows from $u^{r-1}$ to $u^r$, and $f_r$ is in each $W_j(t^j_{r-1}, t^j_r)$, so by Lemma 2 it is in the label, which is therefore not empty. Each state on the path is reachable from the start, so the loop of line L3 visits it. The path is unique because the indices are. In the other direction, a path with atoms from its labels gives, for each $j$, indices as in Lemma 1, so the program gives $o_j$ on $\sigma_j$. $\square$

## Theorem

SYNTHESIZE returns a consistent program of least cost, and "none" exactly when no program of the language is consistent with the examples. The count of the programs with at most $A$ atoms, computed over the product DAG, is exact.

**Proof.** The cost of a program is the sum of the cost tuples of its atoms, compared in lexicographic order. This order is total, and $x \le y$ implies $x + z \le y + z$. The cost of an atom SubStr$(p_1, p_2)$ is a fixed part plus the costs of $p_1$ and $p_2$, so the cheapest atom of a rectangle takes the cheapest member of each set, and the cheapest atom of a label is the cheapest over its constants and rectangles.

Along each edge every component of the state grows, so the sum of the components grows, and the order by this sum is a topological order. Line L6 relaxes the edges in this order. By induction over the order, when a state $w$ is handled, its value is the least cost of a path from the start to $w$ with the cheapest atom on each edge: each path into $w$ ends with an edge from a state with a smaller sum, which was final at that time, and the order on costs is compatible with addition. By Lemma 3 the programs of the paths to the goal are exactly the consistent programs, so line L7 returns a cheapest one, or "none" when the goal is not reachable.

For the count: by Lemma 3 each consistent program is one path together with one atom for each edge, and different choices give different programs. The number of atoms in a label is the number of constants plus $|A| \cdot |B|$ for each rectangle $(A, B)$, because the rectangles are disjoint by Lemmas 1 and 2. A sum over paths with at most $A$ edges of the product of these numbers is the count. $\square$
