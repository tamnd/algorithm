---
title: Bottom-up reduced-error pruning returns the smallest pruned tree with the fewest errors on the pruning set
proves: [correctness, termination, complexity]
status: full
---

Let $T$ be a finite decision tree. Each node $t$ has a label $\ell(t)$, and an internal node has a test with one child for some of the outcomes; a case whose outcome has no child stops at $t$ and gets $\ell(t)$. A *pruning* $T'$ of $T$ is a subtree with the same root in which each node keeps either all its children or none; it classifies a case by following its path until a leaf of $T'$ or a stop. Let $V$ be the pruning set of $m$ labeled cases. For a node $t$:

- $\mathrm{wrong}(t)$ is the number of cases of $V$ that reach $t$ in $T$ and whose class is not $\ell(t)$;
- $\mathrm{stop}(t)$ is the number of those cases that also stop at $t$.

Whether a case reaches $t$ depends only on the tests above $t$, so these counts are the same in every pruning that contains $t$. Line L1 computes them.

**Lemma 1 (errors of a pruning).** The errors of $T'$ on $V$ are $\sum_{u \text{ leaf of } T'} \mathrm{wrong}(u) + \sum_{s \text{ internal in } T'} \mathrm{stop}(s)$.

*Proof.* Each case of $V$ ends its path in $T'$ at exactly one node: a leaf $u$ of $T'$, or an internal node $s$ of $T'$ at which it stops. It is an error exactly when its class differs from the label of that node, and it is then counted once, in $\mathrm{wrong}(u)$ or in $\mathrm{stop}(s)$. $\square$

For a node $t$, the cases that reach $t$ end in the branch at $t$, so Lemma 1 also gives the errors of a pruning $B$ of the branch $T_t$ on the cases that reach $t$; write $e(B)$ for them. Let $E^*(t) = \min_B e(B)$ over the prunings $B$ of $T_t$. A pruning of $T_t$ is either $\{t\}$, with $e = \mathrm{wrong}(t)$, or $t$ with a pruning of each child branch, with $e = \mathrm{stop}(t) + \sum_u e(B_u)$. Hence
$$E^*(t) = \min\Big(\mathrm{wrong}(t),\ \mathrm{stop}(t) + \sum_{u \text{ child of } t} E^*(u)\Big),$$
and $E^*(t) = \mathrm{wrong}(t)$ at a leaf. PRUNE (lines L3 to L6) evaluates this recursion in postorder and makes $t$ a leaf when the first term is at most the second. Let $T^*_t$ be the pruning of $T_t$ that it leaves, and $T^* = T^*_{\text{root}}$.

**Theorem 1 (smallest most accurate pruning).** $T^*$ has the fewest errors on $V$ among all prunings of $T$, and it is contained in every pruning with that many errors. So it is the unique smallest such pruning.

*Proof.* By induction on the height of $t$ we show that $e(T^*_t) = E^*(t)$ and that $T^*_t \subseteq B$ for every pruning $B$ of $T_t$ with $e(B) = E^*(t)$. At a leaf both trees are $\{t\}$. Let $t$ be internal and $S = \mathrm{stop}(t) + \sum_u E^*(u)$. If $\mathrm{wrong}(t) \le S$, then $T^*_t = \{t\}$, $e(\{t\}) = \mathrm{wrong}(t) = E^*(t)$, and $\{t\}$ is contained in every pruning of $T_t$. If $\mathrm{wrong}(t) > S$, then $E^*(t) = S$, and a pruning $B$ with $e(B) = S$ is not $\{t\}$; so $B$ keeps the children of $t$, and $e(B) = \mathrm{stop}(t) + \sum_u e(B_u)$ with each $e(B_u) \ge E^*(u)$. The sum equals $S$ only if $e(B_u) = E^*(u)$ for each child, and then $T^*_u \subseteq B_u$ by induction. So $T^*_t$, which is $t$ with all $T^*_u$, has $e = S$ and lies in $B$. $\square$

This is the theorem of Esposito, Malerba and Semeraro (1997) for reduced-error pruning. The recursion is the one of cost-complexity pruning with $\alpha = 0$, where the leaf risk is replaced by the errors on $V$.

**Theorem 2 (Quinlan's iterative rule gives the same tree).** Call an internal node $s$ of the current tree $C$ *qualifying* when $\mathrm{wrong}(s) \le e(C_s)$, where $C_s$ is the branch of $C$ at $s$. Quinlan's rule repeatedly makes a leaf of a qualifying node that has no qualifying internal node below it. It stops after fewer than $|T|$ steps, with $C = T^*$, whatever the order of the choices.

*Proof.* Each step turns one internal node into a leaf, so there are fewer than $|T|$ steps.

*Claim.* Let $B$ be a pruning of $T_u$ that contains $T^*_u$ and in which no internal node qualifies. Then $B = T^*_u$. Otherwise take a node $s$ that is internal in $B$ but not in $T^*_u$, as high as possible; then $s$ is a leaf of $T^*_u$, so PRUNE made it a leaf and $\mathrm{wrong}(s) \le E^*(s) \le e(B_s)$. So $s$ qualifies in $B$, which is false.

*Invariant: $T^* \subseteq C$.* It holds at the start. Suppose the rule is about to cut a node $t$ that is internal in $T^*$. No internal node of $C$ below $t$ qualifies, and $C_u \supseteq T^*_u$ for each child $u$, so the claim gives $C_u = T^*_u$ and $e(C_t) = \mathrm{stop}(t) + \sum_u E^*(u)$ by Theorem 1. As PRUNE kept $t$, $\mathrm{wrong}(t)$ is larger than this, so $t$ does not qualify. Hence the rule never cuts an internal node of $T^*$.

*End.* When the rule stops, no internal node of $C$ qualifies and $T^* \subseteq C$, so the claim at the root gives $C = T^*$. $\blacksquare$

**The greedy variant is not optimal.** Mitchell's statement prunes, at each step, the node whose removal most increases the accuracy on $V$, while some removal does not decrease it. Take a node $t$ labeled $+$ with 8 positive and 3 negative cases and three children: $u_1$ and $u_2$, each labeled $+$ with 4 positive and 1 negative case, and a leaf $w$ labeled $-$ with 1 negative case. Each $u_i$ has two leaves: one labeled $-$ with 2 positive cases, and one labeled $+$ with 2 positive cases and 1 negative case. The unpruned tree makes $3 + 3 + 0 = 6$ errors. Cutting $t$ saves 3 errors, and cutting a $u_i$ saves 2, so the greedy step cuts $t$ and ends with 3 errors. PRUNE cuts $u_1$ and $u_2$, keeps $t$, and makes 2 errors. The tests check this tree.

**Complexity.** Line L1 walks each case of $V$ down one path of at most $h + 1$ nodes, where $h$ is the depth of $T$, and so costs $O(m h)$, with a dictionary lookup per node. PRUNE visits each node once and does work proportional to its number of children, so it costs $O(|T|)$. The total is $O(m h + |T|)$ time and $O(|T|)$ extra space besides the recursion stack of depth $h$.
