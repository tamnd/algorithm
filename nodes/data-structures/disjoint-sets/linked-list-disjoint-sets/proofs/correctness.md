---
title: Linked-list disjoint sets keep one list per set and answer each query correctly
proves: [correctness, termination]
status: full
---

We write $E$ for the set of elements made so far, and for each set object $S$ we write $L(S)$ for the sequence $S.head, S.head.next, \ldots$, followed until NIL. We prove that after each operation the invariant of the page holds:

> **(L)** For each set object $S$, the sequence $L(S)$ has exactly $S.size$ distinct elements, ends at $S.tail$ with $S.tail.next = \mathrm{NIL}$, and each of its elements $x$ has $x.set = S$. Each element of $E$ is in exactly one sequence $L(S)$.

Under (L), the sets of the structure are the sets of elements of the lists $L(S)$, they are disjoint and they cover $E$, and the representative of the set of $x$ is $x.set.head$.

**Initialization.** With no elements and no set objects, (L) holds trivially.

**MAKE-SET$(x)$**, for a new element $x$. Lines L1 and L2 make an object $S$ with $L(S) = (x)$, $S.size = 1$, $S.tail = x$, $x.next = \mathrm{NIL}$ and $x.set = S$. No other field changes, and $x$ was in no list before. So (L) holds, and the new set is $\{x\}$, as the [disjoint-set](/disjoint-set/) type requires.

**FIND$(x)$.** Line L3 changes nothing and returns $x.set.head$. By (L), $x$ is in $L(x.set)$, and two elements get the same answer exactly when they have the same set object, that is, when they are in one set. It stops after two reads.

**UNION$(x, y)$.** Assume (L). Line L4 sets $S = x.set$ and $T = y.set$, the objects of the sets of $x$ and $y$. If $S = T$, the two elements are in one set, line L5 returns, and nothing changes.

Let $S \ne T$. Line L6 may swap the names $S$ and $T$; the rest of the proof uses the names after the swap, and the claim to prove is symmetric in the two sets. Let $L(S) = (s_1, \ldots, s_a)$ and $L(T) = (t_1, \ldots, t_b)$, with $a = S.size$ and $b = T.size$. These $a + b$ elements are distinct, because each element is in only one list.

*Line L7.* The walk visits $s_1, \ldots, s_a$ and sets $s_i.set \leftarrow T$. It stops after $a$ steps, because $s_a.next = \mathrm{NIL}$ by (L), and it changes no `next` field, so the list it walks does not change during the walk.

*Line L8.* Before it, $t_b = T.tail$ and $t_b.next = \mathrm{NIL}$. It sets $t_b.next \leftarrow s_1$ and $T.tail \leftarrow s_a$. Now $L(T) = (t_1, \ldots, t_b, s_1, \ldots, s_a)$: from $t_1$ the old links lead to $t_b$, the new link leads to $s_1$, and the old links of $S$ lead to $s_a$, whose `next` is NIL.

*Line L9.* It sets $T.size \leftarrow a + b$ and removes $S$.

Now check (L). The list $L(T)$ has $a + b$ distinct elements, equal to $T.size$; it ends at $T.tail = s_a$ with $s_a.next = \mathrm{NIL}$; its first $b$ elements had $set = T$ and kept it, and the last $a$ got $set = T$ at line L7. The object $S$ no longer exists, and no element points to it. Every other object and its list is unchanged, because lines L7 to L9 change only fields of $s_1, \ldots, s_a$, $t_b$, $S$ and $T$. Each element is still in exactly one list: the elements of the old lists $L(S)$ and $L(T)$ are now in the new $L(T)$, and the other lists did not change. So (L) holds. The new set of $T$ is the union of the two old sets, and all other sets are as before, which is the effect that the disjoint-set type requires of UNION. The swap of line L6 changes only which of the two objects survives, so the sets are the same with or without it.

**Conclusion.** By induction on the number of operations, (L) holds after each operation, each operation stops, and FIND returns a representative that is shared by exactly the members of one set. $\blacksquare$
