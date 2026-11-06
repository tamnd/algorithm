---
title: CYK computes exactly the nonterminals that derive each substring
proves: [correctness]
status: full
---

We use the pseudocode of the page. The grammar $G = (V, \Sigma, P, S)$ is in Chomsky normal form: each production is $A \to BC$ with $B, C \in V$, or $A \to a$ with $a \in \Sigma$, or $S \to \varepsilon$ with $S$ on no right side. The input is $w = a_1 \cdots a_n$. For $1 \le i \le j \le n$ write $w_{i,j} = a_i \cdots a_j$ and $D[i, j] = \{A \in V : A \Rightarrow^* w_{i,j}\}$.

**Lemma 1 (one symbol).** $A \in D[i, i]$ if and only if $A \to a_i \in P$.

*Proof.* If $A \to a_i \in P$, then $A \Rightarrow a_i$. Conversely, let $A \Rightarrow^m a_i$ with $m \ge 1$ (the case $m = 0$ is impossible since $A \ne a_i$). The first step uses a production of $A$. It is not $A \to \varepsilon$: that is allowed only for $A = S$, and then the derivation ends at $\varepsilon \neq a_i$. It is not $A \to BC$: in Chomsky normal form no nonterminal other than $S$ derives $\varepsilon$, and $S$ is on no right side, so each of $B$ and $C$ derives only nonempty strings, and $BC$ derives only strings of length at least 2. So the first step is $A \to a$ for a terminal $a$, the derivation ends there, and $a = a_i$. $\square$

**Lemma 2 (longer substrings).** For $i < j$, $A \in D[i, j]$ if and only if there are $k$ with $i \le k < j$ and a production $A \to BC \in P$ with $B \in D[i, k]$ and $C \in D[k + 1, j]$.

*Proof.* If such $k$, $B$ and $C$ exist, then $A \Rightarrow BC \Rightarrow^* w_{i,k}\, C \Rightarrow^* w_{i,k}\, w_{k+1,j} = w_{i,j}$. Conversely, let $A \Rightarrow^* w_{i,j}$ with $j - i + 1 \ge 2$. As in Lemma 1, the first step is not $A \to \varepsilon$ and not $A \to a$, since those derive strings of length 0 and 1. So it is some $A \to BC$, and $BC \Rightarrow^* w_{i,j}$. By the splitting lemma (see the derivation page), $w_{i,j} = xy$ with $B \Rightarrow^* x$ and $C \Rightarrow^* y$. Both $x$ and $y$ are nonempty, because $B$ and $C$ are not $S$ (as $S$ is on no right side) and so derive no empty string. Let $k = i + |x| - 1$; then $i \le k < j$, $x = w_{i,k}$ and $y = w_{k+1,j}$. $\square$

**Claim.** When line L11 is reached, $T[i, j] = D[i, j]$ for all $1 \le i \le j \le n$, and CYK returns true if and only if $w \in L(G)$.

*Proof.* We show by induction on $\ell = j - i + 1$ that after the iteration of line L4 for length $\ell$ (or after line L3 for $\ell = 1$), every cell $T[i, j]$ with $j - i + 1 = \ell$ equals $D[i, j]$, and that no later line changes it.

*Base, $\ell = 1$.* Line L3 sets $T[i, i] = \{A : A \to a_i \in P\}$, which is $D[i, i]$ by Lemma 1. Later lines write only cells with $j > i$.

*Step, $\ell \ge 2$.* Assume the claim for all lengths less than $\ell$. Fix $i$ and $j = i + \ell - 1$. Line L6 sets $T[i, j] = \emptyset$, and only the iterations for this $(i, j)$ write to $T[i, j]$, since each later iteration has another pair $(i, j)$. Lines L7 to L10 add $A$ exactly when some $k$ with $i \le k \le j - 1$ and some $A \to BC$ have $B \in T[i, k]$ and $C \in T[k + 1, j]$. The cells $T[i, k]$ and $T[k + 1, j]$ have lengths $k - i + 1$ and $j - k$, both between 1 and $\ell - 1$, so by the induction hypothesis they equal $D[i, k]$ and $D[k + 1, j]$. By Lemma 2, the set of added nonterminals is exactly $D[i, j]$.

For $n \ge 1$ the claim gives $T[1, n] = D[1, n]$, and line L11 returns true if and only if $S \Rightarrow^* w$. For $n = 0$, line L1 returns true if and only if $S \to \varepsilon \in P$. In Chomsky normal form this is the only way to derive $\varepsilon$: a derivation that starts with $S \to a$ or $S \to BC$ yields a string of length at least 1, as shown in Lemma 1. $\square$

**The parse tree.** Line L10 sets $back[i, j, A] = (k, B, C)$ only when $A \to BC \in P$, $B \in T[i, k]$ and $C \in T[k + 1, j]$, and for $i = j$ the leaf comes from $A \to a_i \in P$. Define the tree of $(i, j, A)$ with $A \in T[i, j]$ as the leaf node $A$ over $a_i$ if $i = j$, and otherwise as the node $A$ with the trees of $(i, k, B)$ and $(k + 1, j, C)$ as children. By induction on $j - i$, this is well defined (both children satisfy $B \in T[i, k]$ and $C \in T[k + 1, j]$, with shorter spans), it uses only productions of $P$, and its leaves spell $w_{i,j}$. So the tree of $(1, n, S)$ is a parse tree of $w$. Each internal node with two children splits its span into two nonempty parts, so the tree has $n$ nodes of the form $A \to a$ and $n - 1$ binary nodes, and its construction takes $O(n)$ time.

**Termination.** All loops are bounded `for` loops over finite ranges and the finite set $P$, so CYK stops after $\binom{n+1}{3}$ runs of line L8. $\blacksquare$
