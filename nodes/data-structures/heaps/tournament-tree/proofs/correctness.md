---
title: The winner tree and the loser tree give the winner after each update
proves: [correctness]
status: full
---

The slots are $0, \dots, k - 1$. Slot $a$ *beats* slot $b$ if $key[a] < key[b]$, or $key[a] = key[b]$ and $a < b$, with $+\infty$ larger than every real key. This is a strict total order on slots, so every nonempty set $S$ of slots has a unique winner $\mathrm{win}(S)$, which beats every other slot of $S$. For a node $j$ of the tree, let $S(j)$ be the set of slots whose leaves are below $j$ or at $j$, and let $w(j) = \mathrm{win}(S(j))$. For an internal node $j$, $S(j) = S(2j) \cup S(2j + 1)$, a disjoint union, so
$$w(j) = \text{the one of } w(2j), w(2j+1) \text{ that beats the other}. \tag{1}$$

**Lemma 1 (winner tree).** If $t[k + i] = i$ for each slot and $t[j]$ is the winner of $t[2j]$ and $t[2j + 1]$ for each internal $j$, then $t[j] = w(j)$ for every node.

*Proof.* By induction on the height of $j$. At a leaf $k + i$, $S = \{i\}$ and $t = i$. At an internal node, $t[2j] = w(2j)$ and $t[2j + 1] = w(2j + 1)$ by induction, and (1) gives $t[j] = w(j)$. $\square$

**BUILD.** Line L1 sets the leaves. Line L2 visits $j = k - 1, \dots, 1$ in decreasing order, and both children $2j, 2j + 1$ are larger than $j$, so they are set before $j$. Line L3 then sets $t[j]$ as Lemma 1 needs. So after BUILD, $t[1] = w(1)$ is the overall winner.

**UPDATE in the winner tree.** A change of $key[i]$ changes $w(j)$ only for the nodes $j$ with $i \in S(j)$, which are the ancestors of leaf $k + i$. Lines L4 to L7 visit these ancestors from the bottom up. When node $j$ is visited, its child on the path was visited before, and its other child is not an ancestor of the leaf, so both children satisfy the condition of Lemma 1. Line L6 then makes $j$ satisfy it. Nodes off the path are unchanged and still satisfy it. By Lemma 1, after the loop $t[1]$ is the winner of the new keys.

**Lemma 2 (loser tree, the path of the winner).** Let the loser tree satisfy (L): $l[j]$ is the loser of $w(2j)$ and $w(2j + 1)$ for each internal $j$, and $l[0] = w(1)$. Let $i = l[0]$. Then for each internal ancestor $j$ of leaf $k + i$, with $c$ its child on the path and $c'$ the other child, $w(c) = i$ and $l[j] = w(c')$.

*Proof.* Slot $i$ is in $S(c)$ and beats every slot of $S(1) \supseteq S(c)$, so $w(c) = i$. At node $j$, the two players are $w(c) = i$ and $w(c')$, and $i$ wins, so the loser $l[j]$ is $w(c')$. $\square$

**LOSER-UPDATE.** Let $i = l[0]$, and let the key of $i$ change; all other keys stay. Let $j_1, j_2, \dots, j_d = 1$ be the internal ancestors of leaf $k + i$ from the bottom, and write $c_r$ for the child of $j_r$ on the path and $c'_r$ for the other child. After the change, write $w'$ for the new winners. Since $S(c'_r)$ does not contain $i$, $w'(c'_r) = w(c'_r) = l[j_r]$ by Lemma 2.

We show by induction on $r$ the claim: when the loop reaches $j_r$, the variable $w$ holds $w'(c_r)$, and each $l[j_s]$ for $s < r$ holds the new loser at $j_s$. At $r = 1$, $c_1$ is the leaf of $i$ and $w = i = w'(c_1)$. At step $r$, the two players at $j_r$ are $w'(c_r) = w$ and $w'(c'_r) = l[j_r]$. Line L11 keeps the loser in $l[j_r]$ and puts the winner in $w$, which by (1) is $w'(j_r) = w'(c_{r+1})$. This proves the claim for $r + 1$.

After the loop, every node on the path holds its new loser, $w = w'(1)$, and line L13 stores it in $l[0]$. Nodes off the path have no slot $i$ below them, so their players and losers are unchanged. So (L) holds for the new keys, and $l[0]$ is the new winner. Each visited node costs one comparison, so the update costs $d = \lfloor \lg(k + i) \rfloor$ comparisons.

**Merge.** In the $k$-way merge, slot $r$ holds the smallest key not yet output from run $r$, or $+\infty$. The winner is the smallest of these, which is a smallest key not yet output of all runs, because each run is sorted. So each output is the next key in sorted order, the output stops when all slots hold $+\infty$, and every key is output once. $\blacksquare$
