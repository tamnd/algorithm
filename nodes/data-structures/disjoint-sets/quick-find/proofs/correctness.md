---
title: Quick-find keeps one name per set and answers each query correctly
proves: [correctness, termination]
status: full
---

Let the elements be $0$ to $n - 1$. For a sequence of operations, let $\equiv$ be the equivalence closure of the pairs of the unions done so far, as in the [dynamic equivalence problem](/dynamic-equivalence-problem/). We prove that after each operation:

> **(Q)** For all $x, y$: $\mathrm{id}[x] = \mathrm{id}[y]$ if and only if $x \equiv y$. Each value $\mathrm{id}[x]$ is an element $r$ with $r \equiv x$ and $\mathrm{id}[r] = r$. The counter equals the number of classes of $\equiv$.

**Termination.** Each operation runs at most one loop of $n$ steps, so it stops.

**Initialization.** After lines L1 and L2, $\mathrm{id}[x] = x$ for each $x$, and no union has been done, so $\equiv$ is equality. Then $\mathrm{id}[x] = \mathrm{id}[y]$ if and only if $x = y$, each $x$ is its own name, and there are $n$ classes. So (Q) holds.

**Find and connected.** These change nothing, so (Q) still holds. By (Q), `connected(p, q)` returns true exactly when $p \equiv q$, and `find(p)` returns an element equivalent to $p$ that is the same for all members of the class of $p$.

**Union.** Assume (Q) before UNION$(p, q)$. Let $\equiv$ be the relation before and $\equiv'$ the relation after, the closure of $\equiv$ and the pair $(p, q)$. Let $a = \mathrm{id}[p]$ and $b = \mathrm{id}[q]$ be the values that line L4 saves, and let $A = \{x : \mathrm{id}[x] = a\}$ and $B = \{x : \mathrm{id}[x] = b\}$. By (Q), $A$ is the class of $p$ and $B$ is the class of $q$.

*Case $a = b$.* Then $p \equiv q$ by (Q), so $\equiv' = \equiv$. Line L5 returns with no change, and (Q) holds.

*Case $a \ne b$.* Then $A$ and $B$ are two different classes, and $\equiv'$ has the classes of $\equiv$ except that $A$ and $B$ are replaced by $A \cup B$. Indeed, $A \cup B$ is closed under $\equiv'$: an element $\equiv'$-related to a member of $A \cup B$ is linked to it by a chain of pairs of $\equiv$ and the pair $(p, q)$, and each such step stays inside $A \cup B$ or inside a class of $\equiv$ that meets $A \cup B$, which is $A$ or $B$. And all of $A \cup B$ is one class of $\equiv'$, since $p \equiv' q$. The other classes do not meet $A \cup B$, and they stay classes of $\equiv'$.

The loop of lines L6 and L7 compares each $\mathrm{id}[i]$ with the saved value $a$, which the loop does not change. *Loop invariant:* before the step with index $i$, each $j < i$ with an old value $a$ now has the value $b$, and every other entry has its old value. It holds for $i = 0$. The step with index $i$ writes $b$ to entry $i$ exactly when its value is $a$, and the value at $i$ is still the old one, because only earlier entries have changed. So the invariant holds for $i + 1$. At the end, $i = n$: the entries of $A$ have the value $b$, and all other entries are unchanged.

After the loop, the elements with value $b$ are $A \cup B$, and for each other old value $c \notin \{a, b\}$ the elements with value $c$ are the same class as before. So equal values mean one class of $\equiv'$, which is the first part of (Q). The name $b$ is in $B \subseteq A \cup B$, and $\mathrm{id}[b] = b$ was true before and is not changed, since $b \notin A$. The names of the other classes do not change. Two classes merge into one, so the number of classes falls by one, and line L8 lowers the counter by one. So (Q) holds after the union.

**Conclusion.** By induction on the number of operations, (Q) holds after each operation, so each `connected` and `find` answers as the [disjoint-set](/disjoint-set/) type requires, and the counter is the number of sets. $\blacksquare$
