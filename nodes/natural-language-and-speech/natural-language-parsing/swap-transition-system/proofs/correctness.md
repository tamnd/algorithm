---
title: The swap system is sound and complete for all dependency trees, and every run ends after 2n + 2k transitions with k at most n(n - 1)/2
proves: [correctness, termination]
status: full
---

The words are $1, \ldots, n$ and 0 is the root. A configuration is $(\sigma, \beta, A)$ with stack $\sigma$, buffer $\beta$ (a list of words) and arc set $A$; $s_0$ is the stack top and $s_1$ the word below it. Words are compared by their positions in the sentence.

**Lemma 1 (invariant).** In every configuration of a run:

- (a) 0 is at the bottom of the stack and nowhere else, and no arc enters 0;
- (b) every word is in exactly one of three places: on the stack, in the buffer, or removed; a word is removed exactly when it has a head in $A$, and it then has exactly one;
- (c) no removed word is ever again on the stack or in the buffer;
- (d) $A$ has no cycle.

*Proof.* At the start, $\sigma = [0]$, $\beta = [1, \ldots, n]$ and $A = \emptyset$. SHIFT and SWAP move one word between the buffer and the stack, add no arc, and never move 0: SWAP needs $s_1 > 0$. LEFT-ARC adds $s_0 \to s_1$ with $s_1 \ne 0$ and removes $s_1$; RIGHT-ARC adds $s_1 \to s_0$ and removes $s_0$; in both cases the dependent was on the stack, so by (b) it had no head, and it now has one. No arc into 0 is added, since LEFT-ARC needs $s_1 \ne 0$ and $s_0 \ne 0$ because 0 is at the bottom. Removed words are not on the stack or in the buffer, and no transition brings a word back from the removed ones, which gives (c). For (d): a new arc $h \to d$ closes a cycle only if $A$ already has a path of arcs from $d$ to $h$. Such a path ends with an arc into $h$, so $h$ would have a head. But $h$ stays on the stack, so by (b) it has no head, and no cycle closes. $\square$

**Lemma 2 (no pair is swapped twice).** For words $u < v$, there is at most one SWAP with $s_1 = u$ and $s_0 = v$, and there is never a SWAP with $s_1 = v$ and $s_0 = u$.

*Proof.* The second part is the condition $s_1 < s_0$. For the first, define the relative order of $u$ and $v$ while both are on the stack or in the buffer, reading the stack from bottom to top and then the buffer from front to back. SHIFT keeps this sequence as it is (the front of the buffer becomes the new top of the stack), and LEFT-ARC and RIGHT-ARC only delete words from it. SWAP exchanges $s_1$ and $s_0$, two neighbours in this sequence, and changes no other relative order. At the start, $u$ comes before $v$. The only transition that changes their order is a SWAP with $s_1 = u$, $s_0 = v$, which puts $v$ before $u$; after that, the only one that could change it back is a SWAP with $s_1 = v$, $s_0 = u$, which is never legal. $\square$

**Theorem 3 (soundness and termination).** Every run ends after exactly $2n + 2k$ transitions, where $k \le n(n - 1)/2$ is its number of swaps, in a terminal configuration whose arcs form a dependency tree rooted at 0.

*Proof.* *Termination.* By Lemma 2 there are at most $n(n - 1)/2$ swaps. Let $\Phi = 2|\beta| + |\sigma|$. SHIFT lowers $\Phi$ by 1, LEFT-ARC and RIGHT-ARC lower it by 1, and SWAP raises it by 1. $\Phi$ is $2n + 1$ at the start and at least 1, so a run with $k$ swaps has at most $2n + k$ transitions of the other kinds, and is finite.

*No dead end.* If the configuration is not terminal, the buffer is not empty and SHIFT is legal, or the buffer is empty and the stack has at least two words, and RIGHT-ARC is legal.

*Count.* At the end, $\Phi = 1$, so the number of SHIFT, LEFT-ARC and RIGHT-ARC transitions is $2n + k$. Each of the $n$ words is removed once, by an arc, so there are $n$ arcs and $n + k$ shifts. The total is $2n + 2k$.

*Tree.* In the terminal configuration, $\sigma = [0]$ and $\beta$ is empty, so by (b) every word is removed and has exactly one head. By (a) 0 has none, and by (d) there is no cycle. So following heads from any word ends at 0, and $A$ is a dependency tree. $\square$

**The projective order.** For a dependency tree $G$, define the order $\pi_G$ by an inorder traversal: at a word $v$ with left dependents $l_1 < \cdots < l_a$ and right dependents $r_1 < \cdots < r_m$, visit the subtrees of $l_1, \ldots, l_a$, then $v$, then the subtrees of $r_1, \ldots, r_m$; start at 0. In $\pi_G$, each subtree is a block of consecutive words, so $G$ is projective when the words are put in the order $\pi_G$. Write $\mathrm{pos}(w)$ for the rank of $w$ in $\pi_G$.

**Theorem 4 (completeness).** For every dependency tree $G$ there is a run that ends with $A = G$.

*Proof.* Let $w_0 = 0, w_1, \ldots, w_n$ be the words in the order $\pi_G$. By the completeness of arc-standard parsing, applied to the sentence $w_1 \cdots w_n$ in which $G$ is projective, there is an arc-standard sequence $T$ that builds $G$; in it, the $j$-th SHIFT pushes $w_j$, and every arc is made between the two top stack words. We change $T$ into a run of the swap system that keeps two properties before each SHIFT of $T$: (P1) the stack and the arc set are the same as in the arc-standard run; (P2) the buffer is the list of words not yet pushed, in sentence order.

Both hold at the start. LEFT-ARC and RIGHT-ARC of $T$ are copied unchanged: they are legal in the swap system under the same conditions, and they do not touch the buffer. A SHIFT of $T$ that pushes $w_j$ is replaced as follows. By (P2), the buffer is in sentence order and holds $w_j$; let $u_1 < \cdots < u_p$ be the words in front of $w_j$, all smaller than $w_j$. Do SHIFT $p + 1$ times, which pushes $u_1, \ldots, u_p, w_j$, and then SWAP $p$ times. The first SWAP has $s_1 = u_p < w_j = s_0$ and $u_p > 0$, so it is legal, and it puts $u_p$ at the front of the buffer. The next has $s_1 = u_{p - 1} < w_j$ and puts $u_{p - 1}$ in front of $u_p$, and so on. After the $p$ swaps, $w_j$ is on top of the old stack and the buffer is $u_1, \ldots, u_p$ followed by the rest, in sentence order. So (P1) and (P2) hold again, and the arc-standard run and the new run end together, with $A = G$. $\square$

The run of Theorem 4 uses, for each $w_j$, as many swaps as there are words still unpushed that come before $w_j$ in the sentence but after it in $\pi_G$; in total, the number of pairs whose order in the sentence is the opposite of their order in $\pi_G$. The oracle of the main page can do better, because it may make an arc and remove a word before that word has to be moved. The tests check, for every tree with $n \le 5$, that the oracle builds the tree in $2n + 2k$ transitions with $k$ at most the number of such pairs, and they compare $k$ with the least number of swaps, found by search, for every tree with $n \le 4$ and 150 sampled trees with $n = 5$. They also build all complete sequences for $n \le 4$ and find that the trees they produce are exactly all $(n + 1)^{n - 1}$ dependency trees, which checks Theorems 3 and 4.
