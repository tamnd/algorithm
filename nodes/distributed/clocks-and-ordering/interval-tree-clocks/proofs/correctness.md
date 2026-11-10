---
title: Interval tree clocks order stamps exactly as their causal histories
proves: [correctness]
status: full
---

We read trees as functions on the unit interval $[0, 1)$. An id $i$ denotes a set $\|i\|$: $\|0\| = \emptyset$, $\|1\| = [0,1)$, and $\|(l, r)\|$ is $\|l\|$ squeezed into $[0, \tfrac12)$ together with $\|r\|$ squeezed into $[\tfrac12, 1)$. An event tree $e$ denotes a function $\|e\|$: $\|n\|$ is the constant $n$, and $\|(n, l, r)\|$ is $n$ plus $\|l\|$ squeezed into the left half and $n$ plus $\|r\|$ squeezed into the right half. We write $e \le e'$ for $\|e\|(x) \le \|e'\|(x)$ at every $x$.

**Lemma 1 (normal form).** Lifting the root by $m$ adds $m$ to the function and sinking subtracts $m$. So $\mathrm{norm}$ does not change the function: $(n, m, m)$ and $n + m$ denote the same function, and moving $m = \min(\min l, \min r)$ from the children to the root does not change any sum along a path. A tree is normal when no node has two equal integer children and every inner node has a child with minimum $0$. Bottom-up normalization makes every node normal, and it leaves a normal tree as it is, so it is idempotent. The same holds for ids with $(0,0) \to 0$ and $(1,1) \to 1$.

*Proof.* By induction on the tree. The function is unchanged at each rewrite by the arithmetic above. After the rewrite at a node, its children are normal by induction and the node is normal by construction. A normal node matches no rewrite rule, since its children are not equal integers and $m = 0$. $\square$

**Lemma 2 (the four primitives).** For normal operands:

1. $\mathrm{leq}(e_1, e_2)$ is true if and only if $e_1 \le e_2$.
2. $\mathrm{join}(e_1, e_2)$ denotes the pointwise maximum.
3. $\mathrm{split}(i) = (i_1, i_2)$ gives disjoint sets with $\|i_1\| \cup \|i_2\| = \|i\|$, both nonempty when $i \ne 0$, and $\mathrm{sum}$ of two disjoint ids denotes their union.
4. For $i \ne 0$, the result $e'$ of EVENT satisfies $e' \ge e$, $e' \ne e$ as functions, and $\|e'\|(x) = \|e\|(x)$ for every $x \notin \|i\|$.

*Proof.* (1) In a normal tree the minimum of $\|(n, l, r)\|$ is $n$, because some child has minimum $0$. So an integer $n_1$ is below $(n_2, l_2, r_2)$ exactly when $n_1 \le n_2$, which is line L6. A tree $(n_1, l_1, r_1)$ is below an integer when its root and both lifted children are, which is line L7. Two trees compare half by half after the roots are pushed into the children, which is line L8. Induction on the sum of the depths finishes the proof.

(2) The rule takes the maximum of two integers, promotes an integer $n$ to $(n, 0, 0)$, which has the same function, and on two trees keeps the smaller root $n_1$ and pushes the difference $n_2 - n_1$ into the children of the other tree. Then the maximum on each half is $n_1$ plus the maximum of the children, which is the recursive call. Lemma 1 covers the final $\mathrm{norm}$.

(3) $\mathrm{split}(1)$ gives the two halves. For $(0, i)$ and $(i, 0)$ the split recurses into the one nonempty half. For $(i_1, i_2)$ with both halves nonempty, the left half goes to one side and the right half to the other. In each case the parts are disjoint, both nonempty and cover $\|i\|$. $\mathrm{sum}$ recurses half by half, and it never meets two $1$ leaves at the same place because the operands are disjoint.

(4) $\mathrm{fill}$ changes values only under leaves $1$ of the id: on a $0$ leaf it returns $e$, and in the other cases it recurses into the halves. Each change replaces a value by a maximum that contains it, so $\mathrm{fill}(i, e) \ge e$. If $\mathrm{fill}$ changed the function, line L4 returns a tree that is greater and different. Otherwise $\mathrm{grow}$ walks down only into halves where the id is not $0$. At a leaf $1$ over an integer $n$ it returns $n + 1$, and at an integer over a mixed id it expands $n$ to $(n, 0, 0)$ and continues. So it adds $1$ on a nonempty part of $\|i\|$ and nowhere else. $\square$

**The run.** A run starts with the seed stamp $(1, 0)$ and applies fork, event and join to live stamps. A message is a peek $(0, e)$ of the sender, taken after the sender's event, and the receiver joins it and then does an event. An anonymous stamp does no events. Each event creates a fresh name $u$. The causal history $H(s)$ of a stamp is: empty for the seed; the same for both results of a fork; the union for a join; $H \cup \{u\}$ after an event $u$. The history of a peek is the history of its sender. For an event $u$, let $T_u$ be the event tree just after $u$ and $H(u)$ the history just after $u$. A history is *closed*: if $v \in H(s)$ then $H(v) \subseteq H(s)$, because histories only grow along a stamp and are united by joins.

**Lemma 3 (ownership).** At each moment, the ids of the live non-anonymous stamps are pairwise disjoint and cover $[0,1)$. For a point $x$, call the stamp whose id covers $x$ the *owner* of $x$. If $u$ happens at a stamp whose id covers $x$, every later owner of $x$ has $u$ in its history.

*Proof.* The seed covers everything. A fork splits one id into a partition of it by Lemma 2(3), and a join replaces two ids by their union. Joining an anonymous stamp leaves the id unchanged. For the second claim: just after $u$ the owner has $u$. Ownership of $x$ passes only through a fork, where the new owner copies the history, or a join, where the new owner has the union. Histories never shrink. $\square$

**Lemma 4 (owner is maximal).** At each moment, for every point $x$, the tree of the owner of $x$ is at least $\|T\|(x)$ for every event tree $T$ that any stamp or message has carried so far.

*Proof.* By induction over the run. An event $u$ at the owner of $x$ only raises the owner's tree (Lemma 2(4)). An event at another stamp does not change values at $x$ (Lemma 2(4)), so it creates no new value at $x$. A fork copies trees. A join takes the pointwise maximum (Lemma 2(2)) of two trees that are each at most the owner's value at $x$, and if the join creates the new owner, its tree is at least both old trees. $\square$

**Lemma 5 (tree of a history).** At each moment, the tree of a stamp $s$ is the pointwise maximum of $0$ and of $T_v$ for $v \in H(s)$.

*Proof.* By induction. The seed has tree $0$ and an empty history. A fork copies both. A join takes the maximum of two maxima, which is the maximum over the union (Lemma 2(2)). An event $u$ replaces the tree $T$ by $T_u \ge T$ (Lemma 2(4)), and the maximum over $H \cup \{u\}$ is $\max(T, T_u) = T_u$. $\square$

**Lemma 6 (a fresh value).** Let $u$ be an event at a stamp with id $i$ and tree $T$ before the event. There is a point $x \in \|i\|$ with $\|T_u\|(x) > \|T\|(x)$. For each such $x$ and every event $v$ with $u \notin H(v)$, $\|T_v\|(x) < \|T_u\|(x)$.

*Proof.* The point exists by Lemma 2(4). Take $v$ with $u \notin H(v)$ and use induction on the time of $v$.

If $v$ happened before $u$, note that just before $u$ the stamp of $u$ owns $x$, because $x \in \|i\|$. So $\|T_v\|(x) \le \|T\|(x) < \|T_u\|(x)$ by Lemma 4.

If $v$ happened after $u$ at a stamp $s'$, then $s'$ does not own $x$: by Lemma 3 every later owner of $x$ has $u$ in its history, and the history of $s'$ is contained in $H(v)$. So by Lemma 2(4), $\|T_v\|(x)$ equals the value at $x$ of the tree of $s'$ before $v$. By Lemma 5 that is the maximum of $0$ and of $\|T_w\|(x)$ over $w \in H(s')$. Each such $w$ is earlier than $v$ and has $H(w) \subseteq H(v)$ by closure, so $u \notin H(w)$ and, by induction, $\|T_w\|(x) < \|T_u\|(x)$. Also $0 \le \|T\|(x) < \|T_u\|(x)$. $\square$

**Theorem.** For any two stamps $s_1$ and $s_2$ taken at any moments of a run, with trees $E_1$ and $E_2$, $\mathrm{leq}(E_1, E_2)$ holds if and only if $H(s_1) \subseteq H(s_2)$.

*Proof.* By Lemma 2(1), $\mathrm{leq}$ is the pointwise order. If $H(s_1) \subseteq H(s_2)$, then $E_1 \le E_2$ by Lemma 5, since a maximum over a subset is smaller. Conversely, let $u \in H(s_1) \setminus H(s_2)$ and take the point $x$ of Lemma 6. Then $\|E_1\|(x) \ge \|T_u\|(x)$ by Lemma 5. Every $v \in H(s_2)$ has $u \notin H(v)$, since otherwise closure would put $u$ in $H(s_2)$. So by Lemmas 5 and 6, $\|E_2\|(x) < \|T_u\|(x) \le \|E_1\|(x)$, and $\mathrm{leq}(E_1, E_2)$ is false. $\blacksquare$
