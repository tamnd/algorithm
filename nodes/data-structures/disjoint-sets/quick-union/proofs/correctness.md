---
title: Quick-union keeps a forest whose trees are the sets
proves: [correctness, termination]
status: full
---

Let the elements be $0$ to $n - 1$, and let $\equiv$ be the equivalence closure of the pairs of the unions done so far, as in the [dynamic equivalence problem](/dynamic-equivalence-problem/). Call $r$ a *root* when $\mathrm{parent}[r] = r$. We prove that after each operation:

> **(U1)** For each $x$, the sequence $x, \mathrm{parent}[x], \mathrm{parent}[\mathrm{parent}[x]], \ldots$ reaches a root within $n - 1$ steps. Write $\mathrm{root}(x)$ for that root.
>
> **(U2)** For all $x, y$: $\mathrm{root}(x) = \mathrm{root}(y)$ if and only if $x \equiv y$.
>
> **(U3)** The counter equals the number of roots.

**Initialization.** After lines L1 and L2, every element is a root, so (U1) holds with 0 steps and $\mathrm{root}(x) = x$. No union has been done, so $\equiv$ is equality, and (U2) holds. There are $n$ roots and the counter is $n$.

**Find.** Assume (U1). FIND$(p)$ follows the same sequence as in (U1): the loop of lines L3 and L4 replaces $p$ by its parent while $p$ is not a root. By (U1) it reaches a root after at most $n - 1$ steps, so it stops, and line L5 returns $\mathrm{root}(p)$. It writes nothing, so (U1) to (U3) still hold. By (U2), `connected(p, q)` returns true exactly when $p \equiv q$.

**Union.** Assume (U1) to (U3) before UNION$(p, q)$. Line L6 sets $i = \mathrm{root}(p)$ and $j = \mathrm{root}(q)$, by the find case.

*Case $i = j$.* By (U2), $p \equiv q$, so the new relation $\equiv'$ equals $\equiv$. Line L7 returns, nothing changes, and the invariants hold.

*Case $i \ne j$.* Line L8 sets $\mathrm{parent}[i] = j$, the only change to the array. Let $T_i = \{x : \mathrm{root}(x) = i\}$ and $T_j = \{x : \mathrm{root}(x) = j\}$ before the union.

(U1). Take any $x$. If $x \notin T_i$, the path from $x$ to its root does not pass through $i$, since a path that reaches $i$ ends at $i$, a root. So none of its parents changed, and the path is the same as before. If $x \in T_i$, the old path from $x$ ends at $i$ with no repeated node; its nodes are distinct, because a repeated node would make a cycle that never reaches a root. Now it continues from $i$ to $j$ and then along the old path from $j$ to $j$, which is empty because $j$ is a root. So the new path from $x$ is the old path followed by one edge to $j$, and $j$ is still a root. The nodes of this path are distinct: the old path lies in $T_i$, and $j \in T_j$, which does not meet $T_i$. A path of distinct nodes has at most $n - 1$ edges. So (U1) holds, with $\mathrm{root}'(x) = j$ for $x \in T_i \cup T_j$ and $\mathrm{root}'(x) = \mathrm{root}(x)$ otherwise.

(U2). By (U2) before the union, $T_i$ is the class of $p$ and $T_j$ the class of $q$ under $\equiv$. The relation $\equiv'$ adds the pair $(p, q)$, and its classes are those of $\equiv$ with $T_i$ and $T_j$ replaced by $T_i \cup T_j$: this set is one class because $p \equiv' q$, and no chain of pairs leaves it, since each pair of $\equiv$ stays inside one old class and the new pair joins $T_i$ and $T_j$. The new roots are $j$ on $T_i \cup T_j$ and the old roots elsewhere, so equal roots mean one class of $\equiv'$.

(U3). The element $i$ is no longer a root and no other element changes, so the number of roots falls by one, and line L9 lowers the counter by one.

**Conclusion.** By induction on the number of operations, (U1) to (U3) hold after each operation. Each find stops and returns a representative that is the same for exactly the elements of one class, which is what the [disjoint-set](/disjoint-set/) type requires. $\blacksquare$
