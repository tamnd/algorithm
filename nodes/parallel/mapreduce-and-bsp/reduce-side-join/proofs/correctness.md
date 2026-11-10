---
title: The reduce-side join outputs exactly the join, with multiplicities
proves: [correctness]
status: full
---

The relations are bags: $R$ is a finite multiset of tuples $(a, b)$ and $S$ a finite multiset of tuples $(b, c)$. The join is the multiset $R \bowtie S$ in which the tuple $(a, b, c)$ has multiplicity $m_R(a, b) \cdot m_S(b, c)$, where $m_R$ and $m_S$ count the copies in $R$ and $S$. The line numbers refer to the `pseudo id=main` block of the page. The partitioner $h$ is any function of the key alone, the same in every map task.

## Lemma 1. The reduce call for $b$ sees exactly the tuples of $R$ and $S$ with join value $b$

*Proof.* Lines L1 and L2 emit one pair for each tuple, with the join value as the key and the tagged rest of the tuple as the value. Line L3 sends a pair with key $b$ to reducer $h(b) \bmod k$, which depends only on $b$, so all pairs with key $b$ go to the same reducer. The reducer groups its pairs by key (line L4), so the group of $b$ holds every pair with key $b$ and no other pair. The tag of a value records which relation it came from. So, at line L5, $X$ is the multiset $\{a : (a, b) \in R\}$ with $a$ repeated $m_R(a, b)$ times, and at line L6, $Y$ is the multiset $\{c : (b, c) \in S\}$ with $c$ repeated $m_S(b, c)$ times. $\square$

## Lemma 2. The reduce call for $b$ outputs exactly the join tuples with join value $b$

*Proof.* Line L7 outputs $(x, b, y)$ for each element $x$ of $X$ and each element $y$ of $Y$, counting copies. So the tuple $(a, b, c)$ is output $m_R(a, b) \cdot m_S(b, c)$ times by this call, by Lemma 1. A tuple with join value $b' \neq b$ is never output by this call, because every output of line L7 has middle component $b$. $\square$

## Theorem. The union of the reducer outputs is $R \bowtie S$

*Proof.* Each key $b$ that occurs in $R$ or $S$ forms exactly one group at exactly one reducer, by Lemma 1, so it gets exactly one reduce call. A key that occurs in only one relation gives an empty $X$ or an empty $Y$, and the call outputs nothing, which is right because no join tuple has that join value. By Lemma 2, the calls for different keys output disjoint sets of tuples (they differ in the middle component), and the call for $b$ outputs each join tuple with join value $b$ with the right multiplicity. Adding over all keys $b$ gives every tuple $(a, b, c)$ exactly $m_R(a, b) \cdot m_S(b, c)$ times. $\blacksquare$

## The variant with a secondary sort

When the tag is part of the key and the sort puts the tag of $R$ before the tag of $S$, while the partitioner and the grouping use only $b$, the group of $b$ is the same multiset as before, in an order where all values from $R$ come first. The reducer then appends each $R$ value to $X$, and for each $S$ value $c$ outputs $(x, b, c)$ for every $x \in X$. When the first $S$ value arrives, $X$ already holds all $R$ values of the group, so each $S$ value is paired with all of them. The multiset of outputs is the same as in Lemma 2, and the theorem holds unchanged.

## Termination and cost

Each map call emits one pair and each reduce call does $|X| + |Y| + |X| \cdot |Y|$ steps, so the job ends. The shuffle carries $|R| + |S|$ pairs. The reducer that owns $b$ receives $|R_b| + |S_b|$ pairs for $b$, where $R_b$ and $S_b$ are the tuples with join value $b$, and outputs $|R_b| \cdot |S_b|$ tuples for it.
