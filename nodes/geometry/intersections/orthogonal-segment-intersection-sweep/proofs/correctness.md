---
title: The orthogonal sweep reports each meeting horizontal-vertical pair exactly once
proves: [correctness, termination]
status: full
---

**Claim.** Let $H$ be a finite list of horizontal closed segments $h = \{(x, y(h)) : x_1(h) \le x \le x_2(h)\}$ and $V$ a finite list of vertical closed segments $v = \{(x(v), y) : y_1(v) \le y \le y_2(v)\}$, with $x_1 \le x_2$ and $y_1 \le y_2$ after the end points are put in order. ORTHOGONAL-SWEEP$(H, V)$ reports each pair $(h, v)$ with $h \cap v \ne \emptyset$ exactly once, and no other pair.

**Fact.** $h \cap v \ne \emptyset$ if and only if $x_1(h) \le x(v) \le x_2(h)$ and $y_1(v) \le y(h) \le y_2(v)$. The only candidate common point is $(x(v), y(h))$, and it lies on $h$ exactly when the first condition holds and on $v$ exactly when the second holds.

**Invariant.** Line L2 sorts the events by $x$, and at equal $x$ the inserts (kind 0) come before the queries (kind 1), which come before the deletes (kind 2). When the loop of line L4 reaches a query event of $v$, the set $T$ holds exactly the horizontal segments $h$ with $x_1(h) \le x(v) \le x_2(h)$, each once.

*Proof.* A segment $h$ is inserted by its event $(x_1(h), 0)$ and deleted by its event $(x_2(h), 2)$, and $(x_1(h), 0)$ comes before $(x_2(h), 2)$ because $x_1(h) \le x_2(h)$. At the query event $(x(v), 1)$, the insert of $h$ has been processed if and only if $(x_1(h), 0) < (x(v), 1)$, that is $x_1(h) \le x(v)$. The delete of $h$ has been processed if and only if $(x_2(h), 2) < (x(v), 1)$, that is $x_2(h) < x(v)$. So $h \in T$ exactly when $x_1(h) \le x(v) \le x_2(h)$. $\square$

**The range query.** The structure stores $T$ by position: the sorted list $ys$ of the distinct values $y(h)$, a bucket of the segments of $T$ at each position, a Fenwick tree over the flags "the bucket at position $i$ is not empty", and a doubly linked list through the positions with non-empty buckets.

*Structure invariant.* After each insert and delete, (a) the Fenwick tree holds the flags of the current buckets, and (b) the linked list, from its head, visits exactly the positions with non-empty buckets, in increasing order. Insert puts $h$ into the bucket at position $i$. If the bucket was empty, it sets flag $i$, finds the next used position $nx > i$ and the last used position $pv < i$ from prefix counts of the Fenwick tree (the $r$-th used position is found by the standard descent on the tree), and links $i$ between them; since no used position lies strictly between $pv$ and $i$ or between $i$ and $nx$, the list stays sorted and complete. Delete removes $h$ from its bucket, and if the bucket becomes empty it clears the flag and unlinks $i$, joining its two list neighbors. Both keep (a) and (b). The method `check_invariant` tests (a) and (b) directly.

*Query.* `first_at_least(a)` returns the $(c + 1)$-th used position, where $c$ is the number of used positions before $a$; this is the first used position $\ge a$, or none. Line L7 starts at the first used position whose value is $\ge y_1(v)$ and walks the linked list while the value is $\le y_2(v)$. By (b), it visits exactly the used positions with $y_1(v) \le ys[i] \le y_2(v)$, and line L8 reports every segment in their buckets, each once.

**Proof of the claim.** By the invariant and the query, the query of $v$ reports exactly the pairs $(h, v)$ with $x_1(h) \le x(v) \le x_2(h)$ and $y_1(v) \le y(h) \le y_2(v)$, which by the Fact are the meeting pairs with this $v$. Each $v$ has one query event, so each pair is reported once.

**Termination.** There are $2|H| + |V|$ events. Each update and each Fenwick operation takes $O(\log n)$ steps, and the walk of a query visits only used positions in range, each with at least one segment to report, plus one step to stop. $\blacksquare$
