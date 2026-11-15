---
title: The Rete network keeps exactly the partial matches and the conflict set
proves: [correctness]
status: full
---

Fix a set of rules with positive conditions and the network that Rete builds for them. A join node $j$ stands for a prefix $c_1, \ldots, c_i$ of the conditions of one or more rules; $i$ is the *depth* of $j$ (counted from 1 in this proof), and for $i > 1$ its parent is the node of $c_1, \ldots, c_{i-1}$. For a working memory $W$, a *match* of $j$ is a tuple $(w_1, \ldots, w_i)$ of elements of $W$ such that one binding $\theta$ of the variables makes $c_k\theta = w_k$ for all $k$. We use the procedures INSERT and DELETE of the page.

**Invariant.** For the current working memory $W$:

- (A) each alpha memory with pattern $\pi$ holds exactly the elements $w \in W$ that match $\pi$ alone;
- (B) the beta memory of each join node $j$ holds exactly one token for each match of $j$, and the token records the tuple and its binding;
- (C) the conflict set holds exactly the pairs $(\rho, t)$ where $t$ is a match of the last join node of the rule $\rho$.

The invariant holds for the empty memory, since all memories and the conflict set are empty. (C) follows from (B), because a token at a node with productions adds or removes its instantiations at the same moment as the token is made or removed. So we prove that INSERT and DELETE keep (A) and (B).

## Lemma 1 (a join step)

Let $t$ be a token for a match $(w_1, \ldots, w_{i-1})$ of the parent of $j$ with binding $\theta$, and let $w$ be an element. The test of lines L6 and L10 succeeds exactly when $(w_1, \ldots, w_{i-1}, w)$ is a match of $j$, and then it returns the binding of that match.

*Proof.* The test extends $\theta$ so that $c_i$ equals $w$. It fails exactly when a constant of $c_i$ differs from $w$, or a variable already bound in $\theta$, or bound earlier in $c_i$, gets two values. These are the conditions for a common binding of $c_1, \ldots, c_i$. $\square$

The alpha test of line L1 uses $c_i$ with its variables renamed by first occurrence. It accepts a superset of the elements that pass the join test with any parent binding, so taking the candidates of the join from the alpha memory loses no match.

## Lemma 2 (insert)

Let $w \notin W$ and $W' = W \cup \{w\}$. After INSERT$(w)$, invariant (B) holds for $W'$, and no token is made twice.

*Proof.* Lines L1 and L2 make (A) hold for $W'$ before any join runs. The matches of $j$ for $W'$ are the old matches, which keep their tokens, and the *new* matches, which contain $w$. Take a new match $u = (w_1, \ldots, w_i)$ of a node $j$, and let $p$ be the first position with $w_p = w$. Let $j_p$ be the ancestor of $j$ at depth $p$ (or $j$ itself when $p = i$), and $j_{p-1}$ its parent.

*$u$ gets a token.* The prefix $(w_1, \ldots, w_{p-1})$ does not contain $w$, so it was a match of $j_{p-1}$ before the insert and has an old token (for $p = 1$ the root token plays this part). The node $j_p$ reads an alpha memory that received $w$, so line L4 right-activates it. Line L3 sorts the nodes by depth, deepest first, and a token made by a join only goes down to deeper nodes. So when $j_p$ is right-activated, nothing has added a token to $j_{p-1}$ yet, and its memory holds exactly the old matches. By Lemma 1, the right activation makes a token for $(w_1, \ldots, w_p)$. Each new token at a node is passed at once to each child node (line L8), and the left activation of lines L9 to L11 joins it with the whole alpha memory of the child, which already holds $w$ and every other element of $W'$. By induction on $k = p, \ldots, i$, a token for $(w_1, \ldots, w_k)$ is made at depth $k$.

*$u$ gets only one token.* Each token is made either by a right activation, from an old parent token and the element $w$ in the last position, or by a left activation, from a new parent token and one element of the alpha memory. Consider the tokens for $(w_1, \ldots, w_k)$ for $k \ge p$. At depth $p$, a left activation would need a new token for $(w_1, \ldots, w_{p-1})$, which does not exist since that tuple does not contain $w$. So the only token at depth $p$ is the one that the single right activation of $j_p$ made with the old parent token. For $k > p$ the parent tuple $(w_1, \ldots, w_{k-1})$ contains $w$, so it is new. If $w_k = w$, the node $j_k$ was right-activated before $j_p$, at a time when the memory of $j_{k-1}$ held no new token, so the right activation made no token for $u$'s prefix. So a token for $(w_1, \ldots, w_k)$ comes only from the left activation by the unique new parent token, and that left activation meets $w_k$ once in the alpha memory. By induction, $u$ gets exactly one token.

*No other token is made.* By Lemma 1, every token that the joins make is a match for $W'$, and it contains $w$, since right activations put $w$ last and left activations start from a new parent token. $\square$

## Lemma 3 (delete)

Let $w \in W$ and $W' = W \setminus \{w\}$. After DELETE$(w)$, invariants (A) and (B) hold for $W'$.

*Proof.* Line L12 makes (A) hold. A token for $(w_1, \ldots, w_i)$ is the child of the token for $(w_1, \ldots, w_{i-1})$, and it records $w_i$. So the tokens whose tuple contains $w$ are exactly the tokens that record $w$ and their descendants, and lines L13 and L14 remove exactly these. The matches for $W'$ are the matches for $W$ that do not contain $w$, and each of them kept its one token. $\square$

## Theorem

After every sequence of inserts and deletes, the conflict set of the network equals the set of all instantiations of the rules in the current working memory, with no duplicates.

*Proof.* By induction on the length of the sequence, with Lemmas 2 and 3 for the step and (C) for the conflict set. An insert of an element that is in $W$ already, or a delete of an element that is not, changes nothing. $\blacksquare$

## Why the order of line L3 matters

Take the rule with the conditions $q(x, y)$ and $q(y, x)$, and insert $q(a, a)$. It enters both alpha memories. If the node of depth 1 runs first, it makes the token $(q(a, a))$, and the left activation of the node of depth 2 makes $(q(a, a), q(a, a))$. If the node of depth 2 is right-activated after that, it finds the new parent token and makes the same pair again. Deepest first, the node of depth 2 runs while its parent memory is still empty, and the pair is made once.
