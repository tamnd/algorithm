---
title: The bitmap index answers range queries exactly, and WAH-OP combines compressed bitmaps correctly
proves: [correctness]
status: full
---

We use the notation of the page. The column has rows $0, \ldots, n-1$ and distinct values $v_0 < \cdots < v_{c-1}$. A bitmap is a set of rows; AND, OR and NOT (masked to $n$ rows) are intersection, union and complement in $\{0, \ldots, n-1\}$.

**Claim 1 (invariant).** After each `append`, $E^{j} = \{r : A(r) = v_j\}$ for all $j$, and $R^{j} = \{r : A(r) \le v_j\}$ for all $j < c - 1$.

*Proof.* Induction on $n$. For $n = 0$ the domain is empty and there are no bitmaps. Assume the claim for $n$ rows and append row $n$ with value $v$.

- If $v$ is new, it enters the domain first. For equality encoding its bitmap is empty, which is right since no row has value $v$. For range encoding, if $v$ is not the new largest value, its bitmap is a copy of $R$ of its predecessor $u$ (or empty if there is none). No row has a value strictly between $u$ and $v$, and no row has value $v$, so $\{r : A(r) \le v\} = \{r : A(r) \le u\}$. If $v$ is the new largest value, the old largest value $u$ now needs a stored bitmap, and $\{r : A(r) \le u\}$ is the set of all $n$ existing rows. All other bitmaps keep their values, since their defining sets do not depend on the new domain value.
- Then row $n$ is added. Equality: only $E$ of $v$ gets row $n$, and $A(n) = v$ is in exactly that set. Range: row $n$ goes into $R^{j}$ exactly when $v \le v_j$ and $j < c - 1$, which is the definition.

So the claim holds for $n + 1$ rows. $\square$

**Claim 2.** RANGE$(I, lo, hi)$ returns $\{r : lo \le A(r) \le hi\}$.

*Proof.* Let $a$ and $b$ be as in lines L1 and L2. A row value $A(r)$ is some $v_j$, and $lo \le v_j \le hi$ holds if and only if $a \le j \le b$, by the choice of $a$ as the least index with $v_j \ge lo$ and of $b$ as the largest with $v_j \le hi$ (the domain is sorted). If $a > b$, no $j$ qualifies, and line L3 returns the empty set, which is right.

Equality encoding: lines L5 to L8 return $\bigcup_{j=a}^{b} E^{j} = \{r : A(r) = v_j \text{ for some } a \le j \le b\}$ by Claim 1, which is the answer by the remark above.

Range encoding: by Claim 1, $U = R^{b} = \{r : A(r) \le v_b\}$; for $b = c - 1$ this is all rows, which is also $\{r : A(r) \le v_{c-1}\}$. Since every value is some $v_j$ and $v_j \le v_b \iff j \le b \iff v_j \le hi$, we get $U = \{r : A(r) \le hi\}$. If $a > 0$, $D = R^{a-1} = \{r : A(r) \le v_{a-1}\}$, and $v_j \le v_{a-1} \iff j < a \iff v_j < lo$, so $D = \{r : A(r) < lo\}$. If $a = 0$, no value is below $lo$ and $D = \emptyset = \{r : A(r) < lo\}$. Line L11 returns $U \setminus D = \{r : lo \le A(r) \le hi\}$, after the mask removes positions $\ge n$, which are in no set. $\square$

**Claim 3.** If the WAH words $X$ and $Y$ encode bitmaps $x$ and $y$ over the same $g$ groups, WAH-OP$(X, Y, \circ)$ returns words that encode $x \circ y$.

*Proof.* Expand each word into the groups it stands for: a literal is one group, and a fill with count $k$ is $k$ groups equal to 31 copies of its bit. Let the sequence of groups of $x$ be $x_0, \ldots, x_{g-1}$ and of $y$ be $y_0, \ldots, y_{g-1}$. The operation $\circ$ acts on each bit position alone, so the groups of $x \circ y$ are $x_i \circ y_i$.

Invariant at the test of line L13: for some $t$, the words of $Z$ encode exactly the groups $x_0 \circ y_0, \ldots, x_{t-1} \circ y_{t-1}$; the current word $x$ with its current count stands for the groups $x_t, \ldots$ up to the end of that word, and the same holds for $y$ with $y_t$; and the words after the current ones encode the rest.

*Initialization.* $t = 0$, $Z$ is empty, and the current words are the first ones.

*Maintenance.* If both current words are fills, the next $k = \min(\mathrm{count}(x), \mathrm{count}(y))$ groups of $x$ all equal the fill of $x$, and the same holds for $y$, so the groups $x_{t+i} \circ y_{t+i}$ for $0 \le i < k$ all equal 31 copies of $\mathrm{bit}(x) \circ \mathrm{bit}(y)$. Line L16 appends exactly these $k$ groups. Else one word is a literal, $k = 1$, and line L19 appends the one group $x_t \circ y_t$, where the group of a fill is 31 copies of its bit. In both cases APPEND-FILL and APPEND-LITERAL change only the encoding (a homogeneous literal becomes a fill of count 1, and equal fills merge, with a new word when the 30-bit count is full), not the sequence of groups. Lines L20 to L22 consume $k$ groups from each current word and move to the next word when a word is used up. So the invariant holds with $t + k$.

*Termination.* Each pass consumes $k \ge 1$ groups of each operand, so after at most $g$ passes, both operands are used up at the same time, because they have the same number of groups. Then $t = g$, and $Z$ encodes $x \circ y$. $\blacksquare$
