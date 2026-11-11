---
title: Treedoc paths are ordered in infix order, new paths fall between their neighbours, and replicas converge
proves: [correctness, invariant, termination]
status: full
---

**Setting.** A path is a finite list of steps $(s, d)$ with side $s \in \{0, 1\}$ and disambiguator $d = (\mathit{clock}, \mathit{site})$. The root is the empty path. KEY$(x)$ maps each step $(s, d)$ to the pair $(2s, d)$ and appends the one-element tuple $(1)$. Keys are compared in lexicographic order, where tuples are compared element by element and a proper prefix is smaller. For a path $x$, a *left descendant* is a path $x + [(0, d)] + y$ and a *right descendant* is a path $x + [(1, d)] + y$. Sites have distinct ids, and a site increases its clock before each NEWPATH. Operations are delivered at every replica in a causal order, possibly more than once. Write $a < b$ for KEY$(a) <$ KEY$(b)$.

**Claim 1 (the key is the infix order).** For distinct paths $a$ and $b$, $a < b$ if and only if one of these holds: $b$ is a right descendant of $a$; $a$ is a left descendant of $b$; or at the first step $j$ where they differ, $(s_a, d_a) < (s_b, d_b)$ as tuples. So the key order puts the left subtree of a node before it and the right subtree after it, and orders the children of one node by side and then by disambiguator. It is a total order on paths.

*Proof.* If $a$ is a proper prefix of $b$, let $(s, d)$ be the step of $b$ at index $|a|$. The keys agree on the first $|a|$ entries, and then KEY$(a)$ has $(1)$ and KEY$(b)$ has $(2s, d)$. Since $(0, d) < (1) < (2, d)$ as tuples, $b < a$ when $s = 0$ and $b > a$ when $s = 1$. The case where $b$ is a proper prefix of $a$ is symmetric. Otherwise the paths differ first at a step $j$ below both lengths, the keys agree before $j$ and differ at $j$ with $(2s_a, d_a)$ against $(2s_b, d_b)$, which compare as $(s_a, d_a)$ against $(s_b, d_b)$. The map from paths to keys is one to one, since the steps can be read back from the key. So the key order is a total order on paths. $\square$

**Claim 2 (subtrees are intervals).** Let $r$ be a right descendant of $p$, and let $z$ be a path with $p < z < r$. Then $z$ is a right descendant of $p$.

*Proof.* By Claim 1, $p < z$ leaves three cases. If $z$ is a right descendant of $p$, we are done. If $p$ is a left descendant of $z$, then so is $r$, which extends $p$, and $r < z$, a contradiction. If $p$ and $z$ differ first at a step $j < |p|$ with $p$'s step smaller, then $r$ agrees with $p$ on its first $|p|$ steps, so it differs from $z$ first at step $j$ in the same way, and $r < z$, a contradiction. $\square$

**Claim 3 (prefix closure).** The set $S$ of paths at a replica contains every prefix of every path in it.

*Proof.* NEWPATH extends by one step a path $p$ or $q$ that is present at the source. That path was made by an insert that is causally before the new one, so causal delivery brings it to every replica first. BUILD adds a path only after the path one step shorter. $\square$

**Claim 4 (NEWPATH).** Let $p \in S$, let $q$ be the successor of $p$ in $S$ in key order, or none, and let $x =$ NEWPATH$(p, q)$ with a disambiguator not used in $S$. Then $p < x$, and $x < q$ when $q$ exists. So $x$ falls right after $p$ in $S \cup \{x\}$.

*Proof.* *Case 1: $p$ has no right child in $S$*, that is, no path $p + [(1, d)]$, and $x = p + [(1, \mathit{dis})]$. By Claim 1, $p < x$. Suppose $q$ exists. $q$ is not a right descendant of $p$, since by Claim 3 it would then have a right child of $p$ as a prefix in $S$. By Claim 1 and $p < q$, either $p$ is a left descendant of $q$, or $p$ and $q$ differ first at a step $j < |p|$ with $p$'s step smaller. In the first case $x$ is also a left descendant of $q$, so $x < q$. In the second case $x$ agrees with $p$ on its first $|p|$ steps, so it differs from $q$ first at step $j$ in the same way, and $x < q$.

*Case 2: $p$ has a right child $r$ in $S$*, and $x = q + [(0, \mathit{dis})]$. Since $p < r$, the successor $q$ exists and $p < q \le r$. By Claim 2, or because $q = r$, $q$ is a right descendant of $p$, and so is $x$, which extends $q$. So $p < x$, and by Claim 1, $x < q$. $\square$

**Claim 5 (unique paths).** Two different inserts make different paths.

*Proof.* The last step of a path made by NEWPATH holds the disambiguator $(\mathit{clock}, \mathit{site})$ of the insert. Site ids are distinct and a site never reuses a clock value. $\square$

**Theorem 1 (convergence).** Two replicas that have run the same set of operations, in any causal orders and with any duplicates, show the same list.

*Proof.* ADD of line L2 adds a path and its value if the path is absent, and DELETE of line L7 adds a path to the deleted set. Both are unions with one element, which commute and are idempotent. By Claim 5 a path belongs to one insert, so the value stored with it is the same everywhere. Hence the two replicas hold the same set of paths and the same deleted set. READ lists the paths not deleted in key order, which by Claim 1 is a total order. $\square$

**Theorem 2 (local intent and stable order).** A local INSERT$(i, v)$ makes $v$ the $i$-th visible element at its source, and a local DELETE$(i)$ hides exactly the $i$-th visible element. Between two flattens, the relative order of two elements never changes.

*Proof.* For an insert, $p$ is the path of visible element $i - 1$, or the root. The root is the smallest path, since every other path starts with a right step: NEWPATH from the root with no right child makes a right step, otherwise it extends a successor of the root, and BUILD starts with a right step. By Claim 4 the new path falls right after $p$ in the full order, so exactly $i - 1$ visible elements are before it. A delete marks one path. Paths do not change between flattens, and the order is the key order of Claim 1. $\square$

**Flatten.** Suppose all replicas hold the same state and no operation is in flight, and all run FLATTEN. Each computes the same list of visible values, by Theorem 1, and BUILD is a deterministic function of that list, so all replicas end in the same state. BUILD puts element $\mathit{mid}$ at $\mathit{prefix}$, the elements before it in its left subtree and those after it in its right subtree, so by Claim 1 the infix order is the list order and READ does not change. Without the precondition, an operation made before the flatten and received after it names paths of the old tree, and this proof says nothing about its effect.

**Termination.** NEWPATH, ADD and DELETE each do a bounded number of steps on paths of finite length. BUILD recurses on intervals of strictly smaller length. $\blacksquare$
