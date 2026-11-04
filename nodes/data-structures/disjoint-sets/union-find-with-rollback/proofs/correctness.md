---
title: Union-find with rollback restores the earlier forest on each undo
proves: [correctness, termination]
status: full
---

For a node $x$ of a forest, $T(x)$ is the set of nodes whose path to the root passes through $x$, including $x$. The sets of the structure are the sets $T(r)$ of the roots $r$. We prove that after each operation the invariants (S) and (H) of the page hold:

> **(S)** The parent pointers form a forest, $r.size = |T(r)|$ for each root $r$, and $2|T(x)| \le |T(x.p)|$ for each non-root $x$.
>
> **(H)** Let the stack be $H = (h_1, \ldots, h_k)$. There are forests $F_0, \ldots, F_k$, with $F_0$ the forest of all elements as roots and $F_k$ the current forest, such that for each $i$: if $h_i = \mathrm{NONE}$ then $F_i = F_{i-1}$, and if $h_i = (a, b)$ then $a$ and $b$ are roots of $F_{i-1}$ with $a.size \le b.size$, and $F_i$ is $F_{i-1}$ with $a.p \leftarrow b$ and $b.size \leftarrow b.size + a.size$. Each $F_i$ satisfies (S).

Here MAKE-SET adds a root to all of $F_0, \ldots, F_k$, as if the element had been made at the start; this keeps every statement, because the new element is a root in each of them and appears in no record.

**Depth bound.** Under (S), if $x$ has depth $d$, then the sizes along its path at least double at each step, so $n \ge |T(\mathrm{root})| \ge 2^d |T(x)| \ge 2^d$ and $d \le \lfloor \lg n \rfloor$. So each FIND stops after at most $\lfloor \lg n \rfloor$ steps.

**MAKE-SET.** It adds a root $x$ with size 1 and $T(x) = \{x\}$, so (S) holds, and (H) holds as explained above.

**FIND$(x)$.** Lines L2 and L3 write nothing, and by (S) they return the root of the tree of $x$ after at most $\lfloor \lg n \rfloor$ steps. So `connected` is right, and (S) and (H) still hold.

**UNION$(x, y)$.** Line L4 replaces $x$ and $y$ by their roots. If they are equal, line L5 pushes NONE and changes nothing, so (H) holds with $F_{k+1} = F_k$, and (S) holds. Otherwise, after line L6, $x$ and $y$ are different roots with $x.size \le y.size$. Line L7 pushes $(x, y)$ and line L8 sets $x.p = y$ and adds the size, which is exactly the change that (H) describes for $F_{k+1}$. We check (S) for the new forest. The parent pointers form a forest, because $x$ was a root of another tree, so no cycle is made. The new root $y$ has $|T(y)| = $ old $|T(y)| + |T(x)| = y.size + x.size$, which line L8 stores. The new edge satisfies $2|T(x)| = 2\,x.size \le x.size + y.size = |T(y)|$. For other non-roots $z$, $T(z)$ does not change, and $T(z.p)$ grows or stays the same, so the inequality still holds. The sets $T(x)$ and $T(y)$ merge into one set, which is the effect that the [disjoint-set](/disjoint-set/) type requires.

**UNDO.** Let $k \ge 1$ and pop $h_k$. If it is NONE, then $F_{k-1} = F_k$ is the current forest, and (H) holds for the shorter stack with the same forests $F_0, \ldots, F_{k-1}$. If it is $(a, b)$, then by (H) the current forest $F_k$ is $F_{k-1}$ with $a.p$ changed from $a$ to $b$ and $b.size$ increased by $a.size$. The value $a.size$ in $F_k$ equals its value in $F_{k-1}$: sizes change only at the root that receives a link, and $a$ is not a root in $F_k$. So line L13, which subtracts $a.size$ from $b.size$ and sets $a.p \leftarrow a$, turns $F_k$ into $F_{k-1}$ exactly. Then the current forest is $F_{k-1}$, and (H) holds for the stack $h_1, \ldots, h_{k-1}$ with the forests $F_0, \ldots, F_{k-1}$. By (H), $F_{k-1}$ satisfies (S). The sets are those of $F_{k-1}$, the state before the undone union, which is the effect that undo must have.

**SNAPSHOT and ROLLBACK.** A snapshot returns $t = |H|$. Later operations push and pop, and as long as at least $t$ records remain, the first $t$ records and the forests $F_0, \ldots, F_t$ are the ones of the time of the snapshot, because a push or pop changes only the top of $H$. So ROLLBACK$(t)$, which undoes until $|H| = t$, ends in the forest $F_t$ of the snapshot, by the UNDO case applied $|H| - t$ times.

**Conclusion.** By induction on the operations, (S) and (H) hold after each operation. So every find stops and returns the right root, each union merges the right sets, and each undo restores the forest and the sets as they were before the undone union. $\blacksquare$
