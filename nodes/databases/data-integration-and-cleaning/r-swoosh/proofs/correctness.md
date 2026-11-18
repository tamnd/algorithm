---
title: Under the ICAR properties R-Swoosh returns the maximal records of the merge closure, with at most (n-1)^2 match calls
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page. $I$ is the input, a finite set of $n$ records. We write $r \approx s$ for $\mathit{match}(r, s) = \text{true}$ and $\langle r, s \rangle$ for $\mathit{merge}(r, s)$, which is defined when $r \approx s$. The *merge closure* $\bar I$ is the smallest set of records that contains $I$ and contains $\langle r, s \rangle$ for all $r, s$ in it with $r \approx s$. The record $r$ is *dominated* by $s$, written $r \le s$, if $r \approx s$ and $\langle r, s \rangle = s$.

The ICAR properties are:

- **Idempotence.** $r \approx r$ and $\langle r, r \rangle = r$ for every record $r$.
- **Commutativity.** $r \approx s$ if and only if $s \approx r$, and then $\langle r, s \rangle = \langle s, r \rangle$.
- **Associativity.** $\langle r, \langle s, t \rangle \rangle = \langle \langle r, s \rangle, t \rangle$ whenever both sides are defined.
- **Representativity.** If $u = \langle r, s \rangle$ and $r \approx t$, then $u \approx t$.

Termination and the bound on the calls hold for any functions $\mathit{match}$ and $\mathit{merge}$ that always return. The correctness part uses ICAR.

## Termination and the number of calls

Let $a = |R|$ and $b = |R'|$. A step is one run of lines L3 to L8. In a *no-match* step line L7 runs, the step makes $b$ calls, and $(a, b)$ becomes $(a - 1, b + 1)$. In a *merge* step line L8 runs, the step makes at most $b$ calls, and $(a, b)$ becomes $(a, b - 1)$, because $r$ leaves $R$, the merged record enters $R$, and the buddy leaves $R'$.

So $a + b$ falls by one in each merge step and stays the same in each no-match step. It starts at $n$ and is never negative, so there are at most $n$ merge steps. The value $a$ never grows, and each no-match step lowers it by one, so there are at most $n$ no-match steps. The loop stops after at most $2n$ steps, and it stops only when $a = 0$, so there are exactly $n$ no-match steps. If the output has $j$ records, then $a + b$ fell from $n$ to $j$, so there are exactly $n - j$ merge steps and $2n - j$ steps.

**Lemma 1.** The number of calls is at most $(n - 1)^2 - (j - 1)(j - 2)/2$ for $n \ge 1$.

*Proof.* The calls are at most the sum of $b$ before each step. The sequence of steps is a word of $n$ no-match steps (N) and $n - j$ merge steps (M). The last step is N, because only N makes $a = 0$. A merge step needs $b \ge 1$ before it, and every step needs $a \ge 1$, which holds for any order of the first $2n - j - 1$ steps because they hold only $n - 1$ no-match steps. Exchanging an adjacent pair MN among these steps for NM changes the two values of $b$ before these steps from $(h, h - 1)$ to $(h, h + 1)$, so the sum grows by 2. Hence the sum is largest for the word $N^{n-1} M^{n-j} N$. Its values of $b$ are $0, 1, \ldots, n - 2$, then $n - 1, n - 2, \ldots, j$, then $j - 1$. The sum is
$$\frac{(n-1)(n-2)}{2} + \frac{n(n-1)}{2} - \frac{j(j-1)}{2} + (j - 1) = (n - 1)^2 - \frac{(j-1)(j-2)}{2}. \qquad \square$$

For $j = 1$ the bound is $(n - 1)^2$, and the tests reach it for each $n \le 9$ with a match rule that makes each merged record match only the last record of $R'$. For $j = n$ there are no merge steps, and the count is exactly $0 + 1 + \cdots + (n - 1) = n(n-1)/2$.

## Correctness under ICAR

**Lemma 2 ($\le$ is a partial order).** *Reflexive:* $r \approx r$ and $\langle r, r \rangle = r$ by idempotence. *Antisymmetric:* if $r \le s$ and $s \le r$, then $s = \langle r, s \rangle = \langle s, r \rangle = r$ by commutativity. *Transitive:* let $r \le s \le t$. From $s \approx r$ and $t = \langle s, t \rangle$, representativity gives $t \approx r$, so $\langle r, t \rangle$ is defined. Also $\langle \langle r, s \rangle, t \rangle = \langle s, t \rangle$ is defined, and associativity gives $\langle r, t \rangle = \langle r, \langle s, t \rangle \rangle = \langle \langle r, s \rangle, t \rangle = \langle s, t \rangle = t$. $\square$

**Lemma 3 (a merge dominates its parts).** If $r \approx s$ and $m = \langle r, s \rangle$, then $r \le m$ and $s \le m$.

*Proof.* From $r \approx r$ and $m = \langle r, s \rangle$, representativity gives $m \approx r$. Both $\langle r, m \rangle$ and $\langle \langle r, r \rangle, s \rangle = \langle r, s \rangle$ are defined, so associativity gives $\langle r, m \rangle = \langle \langle r, r \rangle, s \rangle = \langle r, s \rangle = m$. So $r \le m$. By commutativity $m = \langle s, r \rangle$, and the same argument gives $s \le m$. $\square$

Let $O$ be the list $R'$ at line L9.

**Lemma 4 (invariants).** At the start of each step: (a) every record in $R \cup R'$ is in $\bar I$; (b) no two records at different positions of $R'$ match; (c) every record of $I$ is dominated by some record in $R \cup R'$.

*Proof.* All three hold at the start, with $R = I$ and $R' = \emptyset$, using reflexivity for (c). (a) A step adds only $r$, which is already there, or $\langle r, s \rangle$ with $r, s \in \bar I$ and $r \approx s$, which is in $\bar I$ by its definition. (b) Line L7 adds $r$ to $R'$ only after lines L5 and L6 found that $r$ matches no record of $R'$, and line L8 only removes a record from $R'$. (c) A no-match step moves $r$ from $R$ to $R'$. A merge step removes $r$ and its buddy $s$ and adds $m = \langle r, s \rangle$, and $r \le m$, $s \le m$ by Lemma 3. A record of $I$ that $r$ or $s$ dominated is now dominated by $m$, by transitivity (Lemma 2). $\square$

**Theorem.** Under ICAR, $O$ is exactly the set of maximal records of $\bar I$ under $\le$, with each record once.

*Proof.* At the end $R = \emptyset$, so by Lemma 4, $O \subseteq \bar I$, no two records of $O$ match, and every record of $I$ is dominated by a record of $O$. Two equal records match by idempotence, so the records of $O$ are distinct.

Let $D = \{ y : y \le o \text{ for some } o \in O \}$. We show that $D$ is closed under merges. Let $y_1 \le o_1$ and $y_2 \le o_2$ with $o_1, o_2 \in O$ and $y_1 \approx y_2$. From $y_1 \approx y_2$ and $o_1 = \langle y_1, o_1 \rangle$, representativity gives $o_1 \approx y_2$. From $y_2 \approx o_1$ and $o_2 = \langle y_2, o_2 \rangle$, it gives $o_2 \approx o_1$. No two different records of $O$ match, so $o_1 = o_2 = o$. Let $u = \langle y_1, y_2 \rangle$. From $y_1 \approx o$, representativity gives $u \approx o$. Both $\langle u, o \rangle$ and $\langle y_1, \langle y_2, o \rangle \rangle = \langle y_1, o \rangle$ are defined, and associativity gives $\langle u, o \rangle = \langle y_1, \langle y_2, o \rangle \rangle = \langle y_1, o \rangle = o$. So $u \le o$ and $u \in D$.

$D$ contains $I$ and is closed under merges, so $\bar I \subseteq D$: every record of $\bar I$ is dominated by a record of $O$.

Now let $o \in O$ and $o \le y$ with $y \in \bar I$. Then $y \le o'$ for some $o' \in O$, so $o \le o'$ by transitivity. If $o \ne o'$, they would match, which (b) forbids. So $o = o'$, and $o \le y \le o$ gives $y = o$ by antisymmetry. So every record of $O$ is maximal in $\bar I$. Conversely, let $x$ be maximal in $\bar I$. Then $x \le o$ for some $o \in O \subseteq \bar I$, and maximality gives $x = o \in O$. $\blacksquare$

**Remarks.** The result does not depend on the order in which line L3 takes records from $R$ or on the order of the scan in line L5, because the set of maximal records of $\bar I$ does not. The number of calls does depend on these orders. Without representativity the theorem can fail: R-Swoosh drops $r$ and its buddy after a merge, and a later record that matches $r$ but not the merged record is then never merged with the information of $r$.
