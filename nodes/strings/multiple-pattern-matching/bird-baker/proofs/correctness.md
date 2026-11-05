---
title: Bird-Baker outputs exactly the occurrences of the patterns
proves: [correctness, termination]
status: full
---

**Claim.** For every rectangular text $T$ with $n_1$ rows and $n_2$ columns and every list of rectangular patterns $P_0, \ldots, P_{k-1}$, BIRD-BAKER stops and outputs each triple $(r, c, j)$ such that $P_j$ occurs with its top-left corner at $(r, c)$ exactly once, and no other triple.

**Notation.** For a set $W$ of words, its trie has a node for each prefix of a word of $W$; $\mathrm{spell}(v)$ is the prefix of node $v$, and $|v|$ is its length. The failure link $\mathrm{fail}(v)$ of a node $v \ne$ root is the node of the longest proper suffix of $\mathrm{spell}(v)$ that is a node. The step from $v$ by a symbol $a$ follows failure links from $v$ until a node with a child by $a$ is found, and goes to that child, or to the root if no such node exists. The output list of $v$ is the list of indices of the words equal to $\mathrm{spell}(v)$, followed by the output list of $\mathrm{fail}(v)$.

**Lemma 1 (Aho-Corasick).** Let $s$ be a sequence and $v$ the state after the steps for $s[0], s[1], \ldots$, from the root. Then $\mathrm{spell}(v)$ is the longest suffix of $s$ that is a prefix of a word of $W$, and the output list of $v$ holds each index $i$ with $W_i$ a suffix of $s$ exactly once.

*Proof.* First, the nodes on the failure chain $v, \mathrm{fail}(v), \mathrm{fail}(\mathrm{fail}(v)), \ldots$ spell exactly the suffixes of $\mathrm{spell}(v)$ that are nodes, in decreasing length: each link goes to the longest shorter one, so none is skipped. Now use induction on $|s|$; for $s$ empty the state is the root. Let $v$ satisfy the claim for $s$, and read $a$. A suffix of $sa$ that is a node and is not empty has the form $y a$, where $y$ is a suffix of $s$ and a node, so $|y| \le |v|$ and $y$ is a suffix of $\mathrm{spell}(v)$, so $y$ is on the failure chain of $v$. The step walks this chain in decreasing length and stops at the first $y$ with a child by $a$, which gives the longest $ya$; if there is none, the answer is the empty suffix, the root. For the output, a word $W_i$ that is a suffix of $s$ is a node and a suffix of $s$, so it is a suffix of $\mathrm{spell}(v)$ and is spelled by exactly one node of the failure chain of $v$. The output list of $v$ is the concatenation of the lists of the words equal to the strings of these distinct nodes, so it holds $i$ exactly once. Conversely each index on it is of a word that is a suffix of $\mathrm{spell}(v)$, hence of $s$. $\square$

Fix the width $w$ of one pass, and let $P_j$ for $j \in J$ be the nonempty patterns of width $w$. Let $X$ be the set of their rows, all of length $w$, with distinct names, and ⊥ a symbol that is not a name.

**Lemma 2 (row names).** After line L7 for row $r$, for each $c$ with $w - 1 \le c < n_2$, $L[c]$ is the name of $T[r][c - w + 1 \ldots c]$ if this string is in $X$, and ⊥ otherwise.

*Proof.* By Lemma 1 for $W = X$, the state after $T[r][0 \ldots c]$ spells the longest suffix $y$ of $T[r][0 \ldots c]$ that is a prefix of a row in $X$, and $|y| \le w$. If $x = T[r][c - w + 1 \ldots c]$ is in $X$, then $x$ is such a suffix of length $w$, so $y = x$, the state has depth $w$, and line L7 writes the name of $x$. If the state has depth $w$, then $y$ is a prefix of length $w$ of a row of length $w$, so $y$ is in $X$, and $y = T[r][c - w + 1 \ldots c]$ because $|y| = w$. So line L7 writes a name exactly when $x \in X$, and then the name of $x$. $\square$

**Lemma 3 (reduction).** For $j \in J$ and $0 \le r_0 \le n_1 - m_j$, $0 \le c_0 \le n_2 - w$, the pattern $P_j$ occurs at $(r_0, c_0)$ if and only if, with $c = c_0 + w - 1$, the names $L[c]$ written for the rows $r_0, \ldots, r_0 + m_j - 1$ spell $R_j$.

*Proof.* $P_j$ occurs at $(r_0, c_0)$ if and only if $T[r_0 + i][c_0 \ldots c] = P_j[i]$ for each $i < m_j$. Since $P_j[i] \in X$, Lemma 2 shows that this holds if and only if the name written at $(r_0 + i, c)$ is the name of $P_j[i]$: if the strings are equal, that name is written; if the name of $P_j[i]$ is written, the text string is the row with that name, which is $P_j[i]$ because different rows have different names. $\square$

**Lemma 4 (columns).** In the pass for width $w$, line L10 at row $r$ and column $c$ outputs $(r - m_j + 1, c - w + 1, j)$ exactly for the $j \in J$ such that $R_j$ is a suffix of the column string $S = L_0[c] \cdots L_r[c]$, where $L_t[c]$ is the name written at $(t, c)$, and each such $j$ once.

*Proof.* Line L5 starts $q[c]$ at the root, and line L9 feeds it $L_0[c], L_1[c], \ldots$ in order, one symbol per row, since column $c \ge w - 1$ is visited at every row. A ⊥ is in no $R_j$, so the step sends the state to the root, which is right by Lemma 1 because no nonempty suffix of a sequence ending in ⊥ is a prefix of some $R_j$. Apply Lemma 1 with $W = (R_j)_{j \in J}$. $\square$

**Theorem.** The claim holds.

*Proof.* Termination: every loop runs over a finite range, and each step of an automaton follows finitely many failure links because each one lowers the depth. Line L1 outputs, for each pattern with no rows or with empty rows, exactly the triples of its occurrences given in the problem statement, once each, and such patterns take part in no pass. Take a nonempty pattern $P_j$ of width $w$ and a corner $(r_0, c_0)$. A triple $(r_0, c_0, j)$ can be output only in the pass for width $w$, at row $r = r_0 + m_j - 1$ and column $c = c_0 + w - 1$, since line L10 determines $r_0$ and $c_0$ from $r$, $c$ and $j$. At that row and column, by Lemma 4 it is output once if $R_j$ is a suffix of $L_0[c] \cdots L_r[c]$, that is, if the rows $r_0, \ldots, r$ of column $c$ spell $R_j$ (which needs $r_0 \ge 0$), and not otherwise. By Lemma 3 this happens exactly when $P_j$ occurs at $(r_0, c_0)$. A corner with $c_0 > n_2 - w$ or $r_0 > n_1 - m_j$ never arises, since $c \le n_2 - 1$ and $r \le n_1 - 1$. So every occurrence is output once and nothing else is output. $\blacksquare$
