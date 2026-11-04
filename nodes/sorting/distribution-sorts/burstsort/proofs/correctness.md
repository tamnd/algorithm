---
title: Burstsort sorts strings in lexicographic order
proves: [correctness, termination]
status: full
---

Let $c(s, d) = s[d] + 1$ for $d < |s|$ and $c(s, d) = 0$ otherwise. Give each node of the trie a *label*: the root has the empty label, and the child in slot $r \ge 1$ of a node with label $p$ at depth $d = |p|$ has the label $p$ followed by the character $r - 1$. (Slot 0 never holds a node, because line L6 never bursts it.)

**Invariant (I).** At each moment, every string $s$ that has been inserted is in exactly one bucket. If that bucket is in slot $r$ of a node with label $p$ at depth $d$, then $s$ has $p$ as a prefix and $c(s, d) = r$.

*Proof.* Insertion (lines L3 to L5): the walk of line L4 moves from a node with label $p$ at depth $d$ to the child in slot $c(s, d)$ only if that slot holds a node, and that slot is not 0, so $s$ has the child label as a prefix. The walk stops at a node with label $p$ such that $s$ has prefix $p$ and slot $c(s, d)$ does not hold a node; line L5 puts $s$ in that slot. Burst: BURST$(v, r, d + 1)$ is called only with $r \ge 1$. The strings of that bucket have prefix $p$ and character $r - 1$ at index $d$, so they have the label of the new node $u$ as a prefix, and each one goes to slot $c(s, d + 1)$ of $u$. Other buckets do not change. $\square$

**Termination.** Each string is inserted once. The walk of line L4 goes down one level per step, and a node at depth $d$ has a label of length $d$ that is a prefix of the string, so the walk takes at most $|s|$ steps. A burst moves the strings of one bucket one level down; a string in a bucket at depth $d$ in a slot $r \ge 1$ has length more than $d$, so a string can move down at most $|s|$ times in total. So the number of moves is finite, each burst moves at least one string, and the insertion phase ends. The traversal visits a finite trie, so the whole algorithm ends.

**Order of the buckets.** Let $s$ be in a bucket $B$ and $t$ in a bucket $B' \ne B$, and let the traversal of line L8 visit $B$ before $B'$. We show $s < t$. Let $v$ be the deepest node that is on the path from the root to both buckets, with label $p$ at depth $d$. Both strings have the prefix $p$ by (I). The buckets are reached from $v$ through different slots $r < r'$, because the traversal visits the slots of $v$ in increasing order and visits everything under slot $r$ before slot $r'$. Each string has $c(\cdot, d)$ equal to the slot it was reached through, by (I) when the bucket is in a slot of $v$, and by the label of the child otherwise. So $c(s, d) = r < r' = c(t, d)$, and since $s$ and $t$ agree on their first $d$ characters, $s < t$ (Fact 1 of [MSD radix sort](/msd-radix-sort/)).

**Inside a bucket.** If $B$ is in slot 0 of a node with label $p$, all its strings equal $p$ by (I). If $B$ is in slot $r \ge 1$ of a node at depth $d$, all its strings agree on the first $d + 1$ characters. For such strings, the lexicographic order is the order of the suffixes from index $d + 1$, so line L9 puts $B$ in order.

**Result.** Line L10 writes the buckets in the order of the traversal, each one sorted. By the two paragraphs above, the output is in lexicographic order, and by (I) every input string is written exactly once. $\blacksquare$
