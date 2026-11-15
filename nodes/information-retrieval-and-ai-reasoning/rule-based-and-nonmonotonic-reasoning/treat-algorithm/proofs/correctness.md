---
title: TREAT keeps the conflict set exact, with each instantiation made once
proves: [correctness]
status: full
---

Fix a set of rules with positive conditions. For a working memory $W$, an *instantiation* of a rule $\rho = c_1, \ldots, c_m$ is a tuple $(w_1, \ldots, w_m)$ of elements of $W$ with one binding $\theta$ such that $c_k\theta = w_k$ for every $k$. We use the procedures INSERT and DELETE of the page.

**Invariant.** For the current working memory $W$:

- (A) each alpha memory with pattern $\pi$ holds exactly the elements of $W$ that match $\pi$ alone;
- (C) the conflict set holds exactly the pairs $(\rho, u)$ where $u$ is an instantiation of $\rho$ in $W$, each once.

Both hold for the empty memory.

## Lemma 1 (the seeded join)

Let (A) hold for $W' = W \cup \{w\}$. For a rule $\rho$ and a position $i$, line L5 enumerates, each exactly once, the instantiations $(w_1, \ldots, w_m)$ of $\rho$ in $W'$ with $w_i = w$ and $w_j \ne w$ for all $j < i$.

*Proof.* The join binds the positions $j \ne i$ one at a time and tries each element of the alpha memory of $c_j$, extending the binding with the test of $c_j$; this is a depth-first enumeration of all tuples of candidates, so each tuple is reached at most once. An element that matches $c_j$ under some binding also passes the alpha test of $c_j$, since the alpha pattern is $c_j$ with its variables renamed by first occurrence. So by (A) every element of $W'$ that can stand at position $j$ is in the alpha memory. The test of each step succeeds exactly when the chosen elements so far have a common binding. So the leaves are exactly the instantiations with $w$ at position $i$, minus those that the rule $w_j \ne w$ for $j < i$ excludes. $\square$

## Lemma 2 (insert)

Let $w \notin W$. After INSERT$(w)$ the invariant holds for $W' = W \cup \{w\}$.

*Proof.* Lines L1 and L2 make (A) hold. The instantiations in $W'$ are the old ones, which are still in the conflict set, and the new ones, which contain $w$. Take a new instantiation $u = (w_1, \ldots, w_m)$ of $\rho$ and let $p$ be the first position with $w_p = w$. The element $w$ matches $c_p$, so the alpha memory of $c_p$ received $w$, and line L4 runs the join with $i = p$. By Lemma 1 this join yields $u$ once. A join with $i \ne p$ does not yield $u$: if $w_i \ne w$, then $u$ does not have $w$ at position $i$; if $w_i = w$, then $i > p$, and $w_p = w$ breaks the rule for the positions before $i$. No join yields a tuple that is not an instantiation, or one without $w$. So each new instantiation is added once, and nothing else is added. $\square$

## Lemma 3 (delete)

Let $w \in W$. After DELETE$(w)$ the invariant holds for $W' = W \setminus \{w\}$.

*Proof.* Line L7 makes (A) hold. The instantiations in $W'$ are the instantiations in $W$ that do not contain $w$. Lines L8 and L9 remove exactly the others. $\square$

## Theorem

After every sequence of inserts and deletes, the conflict set equals the set of all instantiations of the rules in the current working memory, and no instantiation was added twice.

*Proof.* By induction on the length of the sequence, with Lemmas 2 and 3. An insert of an element of $W$ or a delete of an element not in $W$ changes nothing. $\blacksquare$

## Remark

The rule "$w_j \ne w$ for $j < i$" is what makes each instantiation appear once when $w$ matches two conditions of the same rule. Without it, the rule $q(x, y), q(y, x)$ and the insert of $q(a, a)$ would add the pair $(q(a, a), q(a, a))$ twice, once for each seed position.
