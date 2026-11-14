---
title: Steensgaard's analysis gives a solution of the subset constraints, so its sets contain Andersen's, in almost linear time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a set of $m$ statements in the four forms `p = &a`, `p = q`, `p = *q` and `*p = q` over $n$ variables, and each variable is also a location. The constraints of a statement are those of [Andersen's analysis](/andersen-analysis/), and $L$ is their least solution in the order $\subseteq$ on each set. The proof of the Andersen page shows that $L \subseteq P$ for every solution $P$.

The algorithm keeps a union-find forest over the variables and the fresh classes made in line L10. For a root $c$, $pt(c)$ is a class or none, and $pending(c)$ is a list of classes. At the end, $cls(v)$ is the root of $v$, $T(c)$ is the root of $pt(c)$ when $pt(c)$ is set, and

$$S(v) = \{a \text{ a variable} : cls(a) = T(cls(v))\},$$

or the empty set when $cls(v)$ has no target. All operations queued while a statement is read run in line L8 before the next statement, so no operation is left in the queue at the end. We write $x \sim y$ if $x$ and $y$ are in the same class at the end. Classes only merge, so two elements in one class at some moment are in one class at the end.

**Lemma 1 (a target, once set, stays).** If at some moment the root of the class of $x$ has the target $t$, then at the end $cls(x)$ has a target and $T(cls(x)) \sim t$.

*Proof.* A target is written only in line L19, which is called only for a root with no target, and in lines L17 and L18, when two roots merge. So a root with a target keeps it until its class merges with another. We use induction on the number of later merges of the class of $x$. With none, the root of $x$ at the end still has $t$. At the next merge, the class of $x$, with target $t$, merges with a class with target $t_2$ or with none. If the other class has none, line L17 gives the new root the target $t$. If it has $t_2$, line L18 gives the new root one of $t$ and $t_2$ and queues JOIN$(t, t_2)$, which runs before the end, so $t \sim t_2$. In both cases the new root has a target $t'$ with $t' \sim t$, and the induction hypothesis for the remaining merges gives $T(cls(x)) \sim t' \sim t$. $\square$

**Lemma 2 (a pending copy is not lost).** If ASSIGN$(x, y)$ runs, then at the end either $cls(y)$ has no target, or both $cls(x)$ and $cls(y)$ have targets and $T(cls(x)) = T(cls(y))$.

*Proof.* Let $x$ and $y$ be the roots when ASSIGN runs. If $x = y$, there is nothing to show. If $pt(y)$ is set and $pt(x)$ is not, line L13 sets the target of $x$ to $pt(y)$, and Lemma 1, used for $x$ and for $y$, gives $T(cls(x)) \sim pt(y) \sim T(cls(y))$. If both are set, line L14 queues JOIN$(pt(x), pt(y))$, and Lemma 1 again gives the claim. If $pt(y)$ is not set, line L12 puts $x$ on $pending(y)$. As long as the class of $y$ has no target, a merge with another class with no target keeps the entry on the joined list (line L16). The class of $y$ gets a target only in line L19 or line L17, and both queue ASSIGN$(d, c)$ for every $d$ on its list, with $c$ the root of the class of $y$. That ASSIGN runs with $pt(c)$ set, so it falls in one of the cases above. If the class of $y$ never gets a target, then $cls(y)$ has none at the end. $\square$

**Theorem 1 (the result is a solution).** $S$ meets every constraint of the program.

*Proof.* Take each statement form.

- `p = &a`. Line L3 sets the target of $p$ to the class of $a$, or line L4 queues JOIN$(pt(p), a)$. By Lemma 1, $T(cls(p)) \sim a$, so $a \in S(p)$.
- `p = q`. Line L5 runs ASSIGN$(p, q)$. If $cls(q)$ has no target, $S(q) = \emptyset$. Otherwise, by Lemma 2, $T(cls(p)) = T(cls(q))$ and $S(p) = S(q)$.
- `p = *q`. Line L6 gets $t = pt(q)$ from DEREF, so $T(cls(q)) \sim t$ by Lemma 1, and then runs ASSIGN$(p, t)$. Let $a \in S(q)$. Then $cls(a) = T(cls(q)) = cls(t)$. If this class has no target, $S(a) = \emptyset$. Otherwise Lemma 2 gives $T(cls(p)) = T(cls(t)) = T(cls(a))$, so $S(a) = S(p)$.
- `*p = q`. Line L7 gets $t = pt(p)$, with $T(cls(p)) \sim t$, and runs ASSIGN$(t, q)$. Let $a \in S(p)$, so $cls(a) = cls(t)$. If $cls(q)$ has no target, $S(q) = \emptyset$. Otherwise Lemma 2 gives $T(cls(a)) = T(cls(t)) = T(cls(q))$, so $S(q) = S(a)$. $\square$

**Corollary (containment).** $L(v) \subseteq S(v)$ for every variable $v$: Steensgaard's sets contain Andersen's. This is the least-solution property of $L$ applied to the solution $S$. In particular $S$ is sound for every run that executes the statements in any order, by the soundness argument of the Andersen page.

**Unification.** For any $u$ and $v$, $S(u)$ and $S(v)$ are equal or disjoint, since each is one whole class of variables or empty. So two pointers whose sets meet always have the same set. This is the loss of precision against Andersen.

**Theorem 2 (time).** With linked lists for the pending lists, and union by rank with path compression, the algorithm takes $O((n + m)\,\alpha(n + m))$ time and $O(n + m)$ space to compute the classes and their targets. Listing the sets $S(v)$ costs their total size more.

*Proof.* There are at most $n + m$ classes: one per variable, and at most one fresh class per load or store, made in line L10. Count the operations.

- Each statement runs one of lines L3 to L7: at most one SET-TARGET, one queued JOIN, one ASSIGN and two DEREF.
- An ASSIGN puts an entry on a pending list at most once, and an entry is taken off once, when its class gets a target, and then gives one ASSIGN that cannot add to a pending list again, because the class it reads now has a target. So there are at most $2m$ ASSIGN operations, and each queues at most one JOIN.
- A JOIN that merges two classes lowers the number of classes by one, so at most $n + m - 1$ JOINs merge. Each queues at most one more JOIN in line L18. A JOIN that finds both arguments in one class does nothing else.
- So the number of JOINs is at most $m$ from line L4, plus $2m$ from line L14, plus $n + m$ from line L18. The ASSIGNs queued by lines L17 and L20 number at most the pending entries, at most $m$.

Every operation does $O(1)$ finds and unions plus $O(1)$ other work, since joining two linked lists is $O(1)$. In total there are $O(n + m)$ operations on the union-find forest, which cost $O((n + m)\,\alpha(n + m))$ by the bound of Tarjan for union by rank with path compression. The space is one record per class and one per pending entry. $\square$

The implementation joins two pending lists by appending the shorter Python list to the longer one. An entry then moves only when its list at least doubles, so it moves $O(\log m)$ times, and this part costs $O(m \log m)$ in the worst case instead of $O(m)$.
