---
title: The capped rows form a deterministic automaton for the words within distance k
proves: [correctness]
status: full
---

Indices are 0-based. Fix a word $W$ of length $m$ and $k \ge 0$, and let $K = k + 1$. For a string $x$ let $D_x[i] = \operatorname{ed}(W[0..i), x)$ for $0 \le i \le m$, in the Levenshtein model with unit costs, and let $R_x[i] = \min(D_x[i], K)$ be the capped row. For a row $R$ and a symbol $c$ let $\operatorname{step}(R, c)$ be the row $R'$ of lines L3 to L5: $R'[0] = \min(R[0] + 1, K)$ and $R'[i] = \min(R[i-1] + [W[i-1] \ne c],\ R[i] + 1,\ R'[i-1] + 1,\ K)$ for $1 \le i \le m$.

**Lemma 1 (the uncapped step).** For each string $x$ and symbol $c$, $D_{xc}[0] = D_x[0] + 1$ and, for $1 \le i \le m$,

$$D_{xc}[i] = \min\bigl(D_x[i-1] + [W[i-1] \ne c],\ D_x[i] + 1,\ D_{xc}[i-1] + 1\bigr).$$

*Proof.* $D_x[i]$ is the entry in row $i$ and column $|x|$ of the [Wagner-Fischer](/wagner-fischer-algorithm/) table of $W$ and $x$, and appending $c$ to $x$ adds one column. The first line is $\operatorname{ed}(\varepsilon, xc) = |x| + 1$, and the second is the Wagner-Fischer recurrence for the new column, whose correctness is proved on that page. $\square$

**Lemma 2 (capping commutes with the step).** For every string $x$ and symbol $c$, $\operatorname{step}(R_x, c) = R_{xc}$.

*Proof.* For integers $a \ge 0$ and $d \ge 0$, $\min(\min(a, K) + d, K) = \min(a + d, K)$: if $a \ge K$ both sides are $K$, and else they are equal. Also $\min(\min(a, K), \min(b, K)) = \min(a, b, K)$. Induction on $i$: $R'[0] = \min(\min(D_x[0], K) + 1, K) = \min(D_x[0] + 1, K) = R_{xc}[0]$ by Lemma 1. For $i \ge 1$, assume $R'[i-1] = \min(D_{xc}[i-1], K)$. Each of the three terms in line L5 has the form $\min(a, K) + d$ with $d \in \{0, 1\}$, where $a$ is the matching term of Lemma 1. Taking the minimum with $K$ and using the two identities gives $R'[i] = \min(D_{xc}[i], K) = R_{xc}[i]$. $\square$

**Theorem 1 (the automaton).** Let the states be the capped rows, the start state $R_\varepsilon$ with $R_\varepsilon[i] = \min(i, K)$, the transition $\operatorname{step}$, and the accepting states the rows with $R[m] \le k$. Then the state after reading $x$ is $R_x$, and the automaton accepts $x$ exactly when $\operatorname{ed}(W, x) \le k$.

*Proof.* $D_\varepsilon[i] = i$, so the start state is $R_\varepsilon$ (line L2). By Lemma 2 and induction on $|x|$, the state after $x$ is $R_x$. It is accepting exactly when $\min(\operatorname{ed}(W, x), K) \le k$, that is, when $\operatorname{ed}(W, x) \le k$ (line L7). Lines L6 and the memo table only give each distinct row one id, which does not change the function from inputs to rows. $\square$

**Lemma 3 (the dead state).** $\min_i R_x[i] \le k$ exactly when some string $y$ has $\operatorname{ed}(W, xy) \le k$.

*Proof.* Suppose $R_x[i] \le k$ for some $i$. Let $y = W[i..m)$. An alignment of $W[0..i)$ with $x$ of cost $D_x[i]$, followed by $m - i$ matches, aligns $W$ with $xy$, so $\operatorname{ed}(W, xy) \le D_x[i] \le k$. Conversely, suppose all entries of $R_x$ equal $K$. Then $\operatorname{step}$ gives $R'[0] = \min(K + 1, K) = K$, and by induction on $i$ each term of line L5 is at least $K$, so $R'[i] = K$. So the row of all $K$ maps to itself on every symbol, and it is not accepting. By Theorem 1, no extension $xy$ has $\operatorname{ed}(W, xy) \le k$. $\square$

So line L8 returns false exactly for the dead state, and the walk of lines L9 to L12 loses no answer when it drops a trie node whose state is dead: every word below that node extends the string of the node.

**Theorem 2 (the lookup).** `LOOKUP` reports each word $y$ of the dictionary with $\operatorname{ed}(W, y) \le k$ exactly once, and no other word.

*Proof.* The trie has one node for each prefix of a dictionary word, and a node is marked when its string is a word. Each entry $(u, R)$ pushed on the stack has $R = R_y$ for the string $y$ of node $u$: this holds for the root with $R_\varepsilon$, and line L12 pushes the child $v$ of $u$ by symbol $c$ with $\operatorname{step}(R_y, c) = R_{yc}$ by Lemma 2. Each node is pushed at most once, because it has one parent. Line L11 reports $y$ exactly when $u$ is marked and $R_y[m] \le k$, so every report is correct by Theorem 1 and no word is reported twice. For completeness, let $y$ be a word with $\operatorname{ed}(W, y) \le k$. For each prefix $y'$ of $y$, $y$ extends $y'$, so $R_{y'}$ is not dead by Lemma 3, and line L12 pushes the node of $y'$ when it pops its parent. By induction on the length of the prefix, the node of $y$ is pushed and popped, and line L11 reports $y$. $\square$

**Search mode.** In search mode line L3 sets $R'[0] = 0$. With $D_x[i] = C[i][|x|]$, the column of the [Sellers table](/sellers-algorithm/) of $W$ against the text $x$, Lemma 1 holds with $D_{xc}[0] = 0$ in place of $D_x[0] + 1$, by the Sellers recurrence, and the proof of Lemma 2 goes through unchanged for $i \ge 1$. So after reading $T[0..j)$ the state is the capped column $j$, and it is accepting exactly when $C[m][j] \le k$, which is the condition for the end position $j$ proved on the Sellers page.

**Theorem 3 (the number of states).** The automaton has at most $(m + k + 1)(k + 2)\,3^{2k} + 1$ reachable states.

*Proof.* Let $L = |x|$. Each alignment of $W[0..i)$ with $x$ needs at least $|i - L|$ insertions or deletions, so $D_x[i] \ge |i - L|$. If $L \ge m + K$, then every $i \le m$ has $|i - L| \ge K$, so $R_x$ is the dead row. Else $0 \le L \le m + k$. For $|i - L| > k$ the entry $R_x[i]$ is $K$, so $R_x$ is fixed by $L$ and the entries with $i$ in the window $\{L - k, \ldots, L + k\} \cap \{0, \ldots, m\}$, which has at most $2k + 1$ indices. Deleting $W[i-1]$ turns an alignment of $W[0..i)$ with $x$ into one of $W[0..i-1)$ with $x$ at one more unit of cost, and the reverse insertion works the same way, so $|D_x[i] - D_x[i-1]| \le 1$. Capping keeps this bound, since $a \mapsto \min(a, K)$ does not increase distances between integers. So the window is fixed by its first entry, one of the $k + 2$ values $0$ to $K$, and at most $2k$ differences in $\{-1, 0, 1\}$. This gives at most $(k + 2)\,3^{2k}$ rows for each of the $m + k + 1$ values of $L$, plus the dead row. $\blacksquare$
