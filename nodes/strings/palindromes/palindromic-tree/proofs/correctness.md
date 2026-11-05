---
title: Correctness of the palindromic tree
proves: [correctness]
status: full
---

We prove that after each call of ADD the structure satisfies the invariant below, for the text $t = t[0..i]$ read so far. Indices are 0-based, $t[a..b]$ includes both ends, and $\mathrm{pal}(v)$ is the palindrome of node $v$. For the two roots, $\mathrm{pal}$ is a string of length $-1$ (a formal object with $c\,\mathrm{pal}(0)\,c = c$) and the empty string.

**Invariant.**

1. The nodes other than the roots are in one-to-one correspondence with the distinct nonempty palindromes that occur in $t$, and $\mathrm{len}[v] = |\mathrm{pal}(v)|$.
2. For each node $v \ge 2$, $\mathrm{link}[v]$ is the node of the longest proper palindromic suffix of $\mathrm{pal}(v)$, the empty root if there is none; $\mathrm{link}[1] = 0$ and $\mathrm{link}[0] = 0$.
3. $\mathrm{to}[v][c] = w$ if and only if $\mathrm{pal}(w) = c\,\mathrm{pal}(v)\,c$ and this palindrome occurs in $t$.
4. $\mathrm{last}$ is the node of the longest palindromic suffix of $t$, and the empty root when $t$ is empty.

At the start, $t$ is empty, there are only the two roots, and the invariant holds.

**Lemma 1 (the chain).** If the invariant holds for $t[0..i-1]$, the nodes $\mathrm{last}, \mathrm{link}[\mathrm{last}], \mathrm{link}^2[\mathrm{last}], \ldots$ are all the palindromic suffixes of $t[0..i-1]$, the empty one included, in strictly decreasing length, followed by the imaginary root.

*Proof.* Let $p$ be a palindromic suffix of $t[0..i-1]$ and $q$ a palindromic suffix of $t[0..i-1]$ shorter than $p$. Then $q$ is a suffix of $p$. So the palindromic suffixes of $t[0..i-1]$ in decreasing length are: the longest one, $\mathrm{pal}(\mathrm{last})$ by part 4, then the longest proper palindromic suffix of it, and so on, which by part 2 are the nodes of the chain. The chain reaches the empty root, whose link is the imaginary root. $\square$

**Lemma 2 (the new longest suffix).** Let $c = t[i]$. The longest palindromic suffix of $t[0..i]$ is $c\,\mathrm{pal}(v)\,c$ for the first node $v$ on the chain of Lemma 1 that fits at $i$ for $c$, that is, with $j = i - \mathrm{len}[v] - 1 \ge 0$ and $t[j] = c$.

*Proof.* A palindromic suffix of $t[0..i]$ of length at least 2 has the form $c\,q\,c$, where $q$ is a palindromic suffix of $t[0..i-1]$, possibly empty, preceded by $c$; and the suffix $c$ of length 1 is $c\,\mathrm{pal}(0)\,c$. Conversely, each node of the chain that fits gives such a suffix. The imaginary root always fits, since $j = i$. Longer $q$ give longer suffixes, and the chain is in decreasing length, so the first node that fits gives the longest one. $\square$

**Lemma 3 (at most one new palindrome).** Each distinct palindrome of $t[0..i]$ that does not occur in $t[0..i-1]$ ends at $i$, and only the longest palindromic suffix $P$ of $t[0..i]$ can be one.

*Proof.* A new occurrence must end at $i$, so it is a palindromic suffix of $t[0..i]$. Let $q$ be a palindromic suffix shorter than $P$. Then $q$ is a suffix of $P$, and since $P$ and $q$ are palindromes, $q = q^R$ is also a prefix of $P$. That occurrence ends at position $i - |P| + |q| < i$, so $q$ occurs in $t[0..i-1]$. $\square$

**Lemma 4 (the suffix link of a new node).** If $P = c\,\mathrm{pal}(v)\,c$ is new and $|P| \ge 2$, the longest proper palindromic suffix of $P$ is $c\,\mathrm{pal}(u)\,c$ for the first node $u$ after $v$ on the chain of Lemma 1 that fits at $i$ for $c$, and it has a node.

*Proof.* The proper palindromic suffixes of $P$ are the palindromic suffixes of $t[0..i]$ shorter than $P$. By the proof of Lemma 2, they are $c\,\mathrm{pal}(u)\,c$ for the nodes $u$ after $v$ on the chain that fit, and the first one gives the longest. The node $u = 0$ fits, so $u$ exists, and the result has length 1 when $u = 0$. By Lemma 3 this palindrome occurs in $t[0..i-1]$, so by parts 1 and 3 for $t[0..i-1]$, the node $\mathrm{to}[u][c]$ exists and is its node. If $|P| = 1$, then $P$ has no nonempty proper palindromic suffix and its link is the empty root, which line L5 sets. $\square$

**Theorem.** If the invariant holds for $t[0..i-1]$, it holds for $t[0..i]$ after ADD$(t[i])$, and ADD returns true exactly when $t[0..i]$ has a palindrome that $t[0..i-1]$ does not have.

*Proof.* Line L2 walks the chain of Lemma 1 and stops at the first node $v$ that fits, which exists because the imaginary root fits. By Lemma 2, $P = c\,\mathrm{pal}(v)\,c$ is the longest palindromic suffix of $t[0..i]$. By part 3, $\mathrm{to}[v][c]$ exists if and only if $P$ occurs in $t[0..i-1]$. If it does, line L3 sets $\mathrm{last}$ to its node, which gives part 4; by Lemma 3 no palindrome is new, so parts 1 to 3 still hold, and the result false is correct. Otherwise $P$ is the only new palindrome, by Lemma 3. Line L4 makes one node $w$ for it with $\mathrm{len}[w] = \mathrm{len}[v] + 2 = |P|$, which keeps part 1. Lines L5 to L8 set $\mathrm{link}[w]$ as in Lemma 4, since the walk of line L7 starts at $\mathrm{link}[v]$, the node after $v$ on the chain; this gives part 2 for $w$, and the links of the other nodes do not change. Line L9 adds the one edge $v \to w$ by $c$, the only new pair for part 3, since $P$ is the only new palindrome and $P = c\,\mathrm{pal}(v)\,c$ for exactly one node $v$ and symbol $c$. Finally $\mathrm{last} = w$ gives part 4, and the result true is correct. Each walk follows links that strictly decrease the length, from at most $i$ down to $-1$, so ADD stops. By induction on $i$, the invariant holds after every call. $\blacksquare$
