---
title: The weave of a causal tree depends only on its atoms, puts local edits in place, and equals the RGA order
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ sites. Each runs the main block. A site makes an atom with id $(\ell, s)$, where $s$ is its site id and $\ell$ is one more than the largest time of every id it has seen. Atoms are delivered at every site, each one after its cause and, for the bounds on local edits, in causal order. Duplicates are dropped. Write $u \prec v$ when atom $u$ was at the source of $v$ when $v$ was made, closed under transitivity.

**Claim 1 (ids).** Ids are unique, and if $u \prec v$ then $\mathit{id}(u) < \mathit{id}(v)$ in lexicographic order. In particular every atom's cause has a smaller id.

*Proof.* Two atoms of one site have different times, since the clock grows. Atoms of different sites differ in the site. If $u$ was at the source of $v$, then the time of $v$ is larger than that of $u$. Transitivity follows. The cause of $v$ was at its source. $\square$

**The tree and the weave.** For a set $A$ of atoms closed under causes, let $T(A)$ be the tree with the root and the atoms of $A$, where the parent of an atom is its cause, and children are ordered by decreasing id. Let $W(A)$ be the pre-order of $T(A)$.

**Claim 2 (WEAVE computes the pre-order).** WEAVE returns $W(A)$ for the set $A$ of atoms that the site holds.

*Proof.* Lines L2 to L4 keep, for every atom, the list of its children in $A$ sorted by decreasing id. The stack loop of lines L6 to L8 is the iterative pre-order walk: it pops a node, outputs it, and pushes its children so that the first child is on top. By induction on the size of a subtree, popping a node $x$ outputs the whole subtree of $x$, in pre-order, before anything that was below $x$ on the stack. $\square$

**Theorem 1 (convergence).** Two sites that hold the same set of atoms return the same text.

*Proof.* By Claim 2 both weaves are $W(A)$ for the same $A$. READ then filters by kind and by the presence of a del child, which also depends on $A$ only. $\square$

**Theorem 2 (local intent).** A local INSERT$(i, x)$ makes $x$ the $i$-th visible element at its source, and a local DELETE$(i)$ hides exactly the $i$-th visible element.

*Proof.* Let $c$ be the cause, the visible element $i - 1$ or the root. The new atom $v$ has a larger id than every atom at the source, by the clock rule, so it is the first child of $c$. In pre-order, $v$ comes right after $c$, and $v$ has no children. The atoms before $c$ in the weave and their visibility do not change, so $v$ follows the $i - 1$ visible elements up to $c$. For a delete, the del atom only hides its cause; a del atom has no char children, since local inserts take visible chars as causes. $\square$

**Theorem 3 (the same order as RGA).** Let $A$ be the char atoms of a set closed under causes, and run RGA on the same inserts, with an atom's cause as its reference and its id as its timestamp, delivered in any causal order. The RGA list is the weave of $A$ restricted to chars.

*Proof.* By Claim 1, ids are unique and grow along the cause relation, which are the two properties that the RGA correctness proof uses for its timestamps. That proof shows that the RGA list is the pre-order of the tree with parent "reference" and children by decreasing timestamp, which is $T(A)$ with the same order of children. Del atoms are leaves of $T$ and do not change the relative order of the char atoms. $\square$

**Theorem 4 (one order for all sites).** If $A$ is the set of all atoms of a run, the weave at every site at every time is $W(A)$ restricted to the atoms it holds.

*Proof.* Whether $x$ comes before $y$ in pre-order depends only on the paths from the root to $x$ and $y$ and on the ids of the children where the paths split. A site holds a set closed under causes, so these paths are the same in its tree as in $T(A)$. $\square$

**Termination.** WEAVE pushes and pops each atom once. $\blacksquare$
