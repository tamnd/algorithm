---
title: The sweep computes a maximum-weight colinear chain
proves: [correctness]
status: full
---

Let $F$ be a set of $n$ fragments with $x_1(f) \le x_2(f)$, $y_1(f) \le y_2(f)$ and $w(f) > 0$, and let $g \prec f$ mean $x_2(g) < x_1(f)$ and $y_2(g) < y_1(f)$.

**Lemma 1 (recurrence).** Let $\mathit{opt}(f)$ be the largest weight of a chain whose last fragment is $f$. Then $\mathit{opt}(f) = w(f) + \max(\{0\} \cup \{\mathit{opt}(g) : g \prec f\})$.

*Proof.* The chain $(f)$ alone has weight $w(f)$. If $g \prec f$ and $C$ is a chain that ends at $g$, then $C$ followed by $f$ is a chain, because its last pair satisfies $g \prec f$. So $\mathit{opt}(f)$ is at least the right side. Conversely, a chain that ends at $f$ is either $(f)$ or a chain $C$ that ends at some $g$ with $g \prec f$, followed by $f$, and then its weight is at most $\mathit{opt}(g) + w(f)$. $\square$

The relation $\prec$ is a strict partial order: it is irreflexive, since $x_2(f) < x_1(f)$ is false, and transitive, since $g \prec f \prec h$ gives $x_2(g) < x_1(f) \le x_2(f) < x_1(h)$, and the same for $y$. So the recurrence is well founded.

**Lemma 2 (event order).** After the sort of line L2, for fragments $f$ and $g$, the end event of $g$ comes before the start event of $f$ if and only if $x_2(g) < x_1(f)$. The start event of each fragment comes before its end event.

*Proof.* The events are sorted by coordinate, and at equal coordinate every start comes before every end. If $x_2(g) < x_1(f)$, the end of $g$ has the smaller coordinate and comes first. If $x_2(g) > x_1(f)$, it comes later. If $x_2(g) = x_1(f)$, the start of $f$ comes first. For one fragment, $x_1(f) \le x_2(f)$ and the same rule put the start first. $\square$

**Lemma 3 (tree).** The tree $T$ over the sorted list of the values $y_2$ supports RAISE$(y, v)$, which replaces the value $u$ at slot $y$ by $\max(u, v)$, and MAX-BELOW$(y)$, which returns the maximum of the slots for values less than $y$, or $(0, \text{NIL})$ when no slot qualifies or all are at their start value. Each operation takes $O(\log n)$ time.

*Proof.* MAX-BELOW finds by binary search the number $c$ of values below $y$ and asks the Fenwick tree for the maximum of the first $c$ slots. The Fenwick tree for prefix maxima is correct for updates that only raise slots, since each node stores the maximum of a fixed block of slots and a raise of one slot can only raise the maxima of the blocks that hold it, which are the nodes that RAISE visits. A prefix of length $c$ is the disjoint union of the blocks that the query visits. $\square$

Pairs are compared first by score. Two fragments with the same $y_2$ share a slot; the slot keeps the larger pair, which is the correct value for any query that includes the slot.

**Theorem.** COLINEAR-CHAIN returns the weight of a maximum-weight chain and a chain of that weight.

*Proof.* We show by induction over the events this invariant: before each event, (a) $\mathit{score}[g] = \mathit{opt}(g)$ for each $g$ whose start event is processed, and (b) $T$ holds, as the maximum over each slot, the pairs $(\mathit{score}[g], g)$ of exactly the fragments $g$ whose end event is processed. Before the first event no event is processed and $T$ holds only start values, so the invariant holds.

At an end event of $g$, its start event is already processed by Lemma 2, so $\mathit{score}[g] = \mathit{opt}(g)$ by (a), and line L8 adds its pair to $T$. Both parts stay true.

At a start event of $f$, by Lemma 2 the fragments in $T$ are exactly the $g$ with $x_2(g) < x_1(f)$, and by (a) their scores are final. Line L6 returns the largest pair among those with $y_2(g) < y_1(f)$ by Lemma 3, that is, among the $g \prec f$, or $(0, \text{NIL})$ when there is none. Line L7 sets $\mathit{score}[f] = w(f) + \max(\{0\} \cup \{\mathit{opt}(g) : g \prec f\})$, which is $\mathit{opt}(f)$ by Lemma 1. The pointer $\mathit{pred}[f]$ is a fragment $g \prec f$ with $\mathit{opt}(g) = \mathit{opt}(f) - w(f)$, or NIL when $\mathit{opt}(f) = w(f)$.

After the last event, every score is final. Every chain ends at some fragment, so the largest weight of a chain is $\max_f \mathit{opt}(f)$, which line L9 finds. Following the pointers from $f^*$ gives fragments $f^* \succ \mathit{pred}[f^*] \succ \cdots$, each step losing exactly the weight of the later fragment, until a fragment with no predecessor. The list reversed is a chain, and its weight is $\mathit{opt}(f^*)$ by a telescoping sum. $\square$

**Lower bound.** For distinct numbers $a_1, \ldots, a_n$, let $f_i = [i, i] \times [a_i, a_i]$ with weight 1. Then $f_i \prec f_j$ if and only if $i < j$ and $a_i < a_j$, so the chains are the increasing subsequences and the best weight is the length of a longest increasing subsequence. The fragments are built in $O(n)$ time without comparisons between the $a_i$, so a chaining algorithm in the comparison model with $o(n \log n)$ comparisons would contradict Fredman's lower bound of $n \log_2 n - n \log_2 \log_2 n + O(n)$ comparisons for that length.
