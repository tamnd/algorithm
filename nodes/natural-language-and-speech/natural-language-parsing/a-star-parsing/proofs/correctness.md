---
title: With a consistent outside estimate, A* parsing returns a Viterbi parse, and it stops
proves: [correctness, termination]
status: full
---

We use the pseudocode A-STAR-PARSE and RELAX of the page. The grammar $G = (N, \Sigma, R, S)$ is in Chomsky normal form, and each rule $r$ has a probability $q(r) > 0$; rules with $q = 0$ are dropped first. All scores are natural logs, combined in the Viterbi semiring (max, +). The input is $w = w_1 \cdots w_n$ with $n \ge 1$. An item $[X, i, j]$ with $0 \le i < j \le n$ stands for the fencepost span $(i, j)$, which covers the words $w_{i+1}, \ldots, w_j$. The goal is $[S, 0, n]$.

## Definitions

A derivation of an item $e = [X, i, j]$ is a parse tree with root $X$ and yield $w_{i+1} \cdots w_j$. Its score is the sum of $\log q$ over its rules. The inside score $\beta(e)$ is the largest score of a derivation of $e$, and $-\infty$ when there is none. The outside score $\alpha(e)$ is the largest score of a tree with root $S$ and yield $w$ in which the subtree of $e$ is cut out and its own rules are not counted, and $-\infty$ when there is none.

Since all scores are finite sums, a derivation of largest score has optimal parts: if a derivation of $e$ uses the rule $Z \to X\,Y$ at its root over the items $c_1$ and $c_2$ and has score $\beta(e)$, then its subtrees have the scores $\beta(c_1)$ and $\beta(c_2)$, or replacing a subtree by a better one would beat $\beta(e)$. We call a derivation optimal when every subtree in it has the inside score of its item. Every item with $\beta(e) > -\infty$ has an optimal derivation, by induction on the span length.

The estimate is a function $a$ from items to $\mathbb{R} \cup \{-\infty\}$. It is **consistent** when $a(\text{goal})$ is finite and, for every rule $Z \to X\,Y$ and every three items $e = [X, i, j]$, $f = [Y, j, k]$ and $g = [Z, i, k]$,

$$a(e) \ge \log q(Z \to X\,Y) + \beta(f) + a(g) \quad \text{and} \quad a(f) \ge \log q(Z \to X\,Y) + \beta(e) + a(g).$$

It is **admissible** when $a(e) \ge \alpha(e)$ for every item. Consistency with $a(\text{goal}) \ge 0$ implies admissibility: apply the two inequalities along the path from $e$ to the root of a tree that gives $\alpha(e)$.

The value $b(e)$ is the stored score of $e$, with $b(e) = -\infty$ before the first update. An item is finished when line L5 has marked it. A copy of $e$ in the agenda has the priority $b + a(e)$, where $b$ is the value of $b(e)$ when that copy was pushed.

## Lemma 1: stored scores are scores of derivations

At every moment, $b(e) \le \beta(e)$ for every item, and if $b(e) > -\infty$ then the back pointers of $e$ give a derivation of $e$ whose score, computed from the current values of $b$ at its children, is $b(e)$.

*Proof.* Line L1 sets $b([X, i, i + 1]) = \log q(X \to w_{i+1})$, the score of a one-rule derivation. Line L7 or L8 offers $\log q(Z \to X\,Y) + b(c_1) + b(c_2)$ for two items with stored scores, and by induction this is the score of the derivation that puts $Z \to X\,Y$ over derivations of $c_1$ and $c_2$. So every stored value is the score of a derivation, and it is at most $\beta(e)$. $\square$

## Lemma 2: a finished item has its inside score

When line L5 marks an item $e$ as finished, $b(e) = \beta(e)$.

*Proof.* Suppose not, and let $e$ be the first item finished with $b(e) < \beta(e)$. By Lemma 1 it is not more, and $\beta(e) > -\infty$. Every item finished before $e$ has its inside score, by the choice of $e$. Fix an optimal derivation $D$ of $e$.

Let $f$ be a lowest node of $D$ that is not finished at the moment $e$ is popped. Such a node exists, because $e$ itself is not finished yet. All children of $f$ in $D$ are finished, with their inside scores. If $f$ is a preterminal item $[X, i, i + 1]$, line L1 has set $b(f) = \log q(X \to w_{i+1}) = \beta(f)$, since $D$ is optimal. Otherwise, $f$ has the children $c_1$ and $c_2$ in $D$ with the rule $Z \to X\,Y$, and when the later of the two was finished, line L7 or L8 offered $\log q(Z \to X\,Y) + \beta(c_1) + \beta(c_2) = \beta(f)$ to $f$, which was not finished then. In both cases, line L10 has made $b(f) = \beta(f)$, the largest possible value by Lemma 1.

If $f = e$, then $b(e) = \beta(e)$, a contradiction. So $f$ is a proper descendant of $e$ in $D$. Walk up $D$ from $f$ to $e$. For a node $g$ of $D$ with a child $c$ and the other child $c'$, both in $D$, consistency gives

$$\beta(c) + a(c) \ge \beta(c) + \log q + \beta(c') + a(g) = \beta(g) + a(g),$$

where the last step is the optimality of $D$. Chaining these inequalities from $f$ to $e$ gives

$$\beta(f) + a(f) \ge \beta(e) + a(e) > b(e) + a(e).$$

The copy of $e$ just popped has the priority $b(e) + a(e)$, and $a(e) > -\infty$ because line L10 pushes no copy with $a = -\infty$. So the left side is above $-\infty$, which means $a(f) > -\infty$, and line L10 pushed a copy of $f$ with the priority $\beta(f) + a(f)$ when it set $b(f) = \beta(f)$. That copy is still in the agenda, because popping it would have finished $f$. The agenda pops a copy of largest priority, and this copy of $f$ has a strictly larger priority than the copy of $e$. This contradicts the choice of the copy of $e$ at line L3. $\square$

## Theorem

Let the estimate be consistent. If $w$ has a parse, A-STAR-PARSE returns $\beta(\text{goal})$, the largest log probability of a parse of $w$, and a parse tree with that score. If $w$ has no parse, it returns "no parse". In both cases it stops.

*Proof.* **Termination.** There are finitely many items. An item is finished at most once, because line L4 skips copies of finished items. Line L10 pushes a copy only when $b(e)$ strictly increases, and $b(e)$ only takes the scores of the combinations offered at lines L1, L7 and L8. Each finished item makes finitely many offers at lines L7 and L8, once, when it is finished. So the number of pushes is finite, and every iteration of line L2 pops one copy, so the loop ends.

**No parse.** If $w$ has no parse, $\beta(\text{goal}) = -\infty$, and by Lemma 1 $b(\text{goal})$ stays $-\infty$, so line L10 never pushes the goal. Line L6 never fires, and the loop ends at line L9.

**A parse exists.** Then $\beta(\text{goal}) > -\infty$. Fix an optimal derivation $D^*$ of the goal. All items of $D^*$ have $a > -\infty$: $a(\text{goal})$ is finite, and for a child $c$ of a node $g$ of $D^*$, consistency gives $a(c) \ge \log q + \beta(c') + a(g) > -\infty$. Suppose the loop ended without popping the goal. Let $f$ be a lowest unfinished node of $D^*$. As in the proof of Lemma 2, $b(f) = \beta(f)$ was set and a copy of $f$ was pushed, since $a(f) > -\infty$. That copy was never popped, because $f$ is not finished, so the agenda was not empty at the end. This is a contradiction, so the goal is popped, and at that moment line L6 returns $b(\text{goal}) = \beta(\text{goal})$ by Lemma 2.

**The tree.** The back pointers of a finished item point to finished items, because lines L7 and L8 combine $e$ only with finished items, and a finished item never changes its $b$ or its back pointer again (line L10 tests that $e$ is not finished). So the tree built from the back pointers of the goal is a derivation of the goal, and by Lemma 1 its score is $b(\text{goal}) = \beta(\text{goal})$. $\blacksquare$

## The estimates of the page are consistent

The null estimate $a = 0$ is consistent because $\log q + \beta(f) \le 0$ for probabilities.

For the SX estimate, let $\mathrm{in}(Y, k)$ be the largest inside score of $Y$ over $k$ words when every word may be any terminal. Then $\mathrm{in}(Y, k) \ge \beta([Y, j, j + k])$ for every sentence, since the actual words are one choice. The estimate $a([X, i, j]) = \mathrm{out}(X, i, n - j)$ satisfies, by its defining recurrence, $\mathrm{out}(X, l, r) \ge \mathrm{out}(Z, l, r - k) + \log q(Z \to X\,Y) + \mathrm{in}(Y, k)$ for every rule $Z \to X\,Y$ and every $k$ with $1 \le k \le r$, and the mirror inequality for $Z \to Y\,X$. With $e = [X, i, j]$, $f = [Y, j, j + k]$ and $g = [Z, i, j + k]$ this reads $a(e) \ge a(g) + \log q + \mathrm{in}(Y, k) \ge a(g) + \log q + \beta(f)$, which is the first consistency inequality. The second is the mirror case. Finally $a(\text{goal}) = \mathrm{out}(S, 0, 0) = 0$. So the SX estimate is consistent, and hence admissible.
