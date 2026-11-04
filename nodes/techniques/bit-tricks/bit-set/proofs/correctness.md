---
title: Each bit vector operation keeps the invariant and returns the right result
proves: [correctness]
status: full
---

**Setting.** Fix the word size $w \ge 1$ and the universe size $n \ge 0$. Let $m = \lceil n / w \rceil$. For $0 \le i < n$ write $q(i) = \lfloor i / w \rfloor$ and $r(i) = i \bmod w$, so $i = q(i) w + r(i)$ with $0 \le q(i) < m$ and $0 \le r(i) < w$. The map $i \mapsto (q(i), r(i))$ is one-to-one. A position $(j, t)$ with $0 \le j < m$, $0 \le t < w$ is a *padding position* when $jw + t \ge n$; then $j = m - 1$, because $(m - 1) w < n$ by the choice of $m$, so for $j \le m - 2$ every position satisfies $jw + t \le (m - 1) w - 1 < n$. Write $B[j]_t$ for bit $t$ of word $B[j]$.

**Invariant** for an array $B$ and a set $S \subseteq \{0, \dots, n - 1\}$:

- (I1) for every $0 \le i < n$: $i \in S \iff B[q(i)]_{r(i)} = 1$;
- (I2) $B[j]_t = 0$ for every padding position $(j, t)$.

Every position of the array is either the position $(q(i), r(i))$ of exactly one $i < n$ or a padding position, because the positions $(j, t)$ with $jw + t < n$ are exactly the images of $0, \dots, n - 1$. Hence (I1) and (I2) together say: $B[j]_t = 1$ exactly when $jw + t \in S$.

**Lemma (one-bit masks).** For $0 \le t < w$ and a $w$-bit word $x$: $(x \vee 2^t)_s = 1$ for $s = t$ and $= x_s$ otherwise; $(x \wedge \neg 2^t)_s = 0$ for $s = t$ and $= x_s$ otherwise; $((x \gg t) \wedge 1) = x_t$.

*Proof.* The word $2^t$ has its only 1-bit at position $t$, and $\neg 2^t$ has its only 0-bit there. OR with 0 and AND with 1 leave a bit unchanged; OR with 1 gives 1 and AND with 0 gives 0. The right shift by $t$ moves bit $t$ to bit 0, and AND with 1 keeps only bit 0. $\square$

**NEW.** Line L1 makes all $m$ words 0. For $S = \emptyset$, (I1) says that every bit of a universe element is 0, and (I2) says the same of the padding: both hold.

**INSERT$(B, i)$ with $0 \le i < n$.** Assume (I1) and (I2) for $S$. Line L2 replaces $B[q(i)]$ by $B[q(i)] \vee 2^{r(i)}$. By the lemma only position $(q(i), r(i))$ changes, and it becomes 1. That position belongs to $i$ and is not a padding position, so (I2) still holds. For $k \ne i$ the bit of $k$ is unchanged and $k \in S \cup \{i\} \iff k \in S$, so (I1) holds for $k$; for $k = i$ the bit is 1 and $i \in S \cup \{i\}$. So the invariant holds for $S \cup \{i\}$.

**DELETE$(B, i)$ with $0 \le i < n$.** The same argument with line L3 and the second part of the lemma: only the bit of $i$ changes, it becomes 0, and the invariant holds for $S \setminus \{i\}$.

**CONTAINS$(B, i)$ with $0 \le i < n$.** By the lemma line L4 returns true exactly when $B[q(i)]_{r(i)} = 1$, which by (I1) is $i \in S$. Nothing is written.

**COUNT.** *Loop invariant:* before the test of line C2 with index $j$, $c = \sum_{j' < j} \nu(B[j'])$, where $\nu$ is the number of 1-bits. It holds for $j = 0$ with $c = 0$ by line C1, and line C3 keeps it. At exit $j = m$ and $c$ is the number of 1-bits in the array. By (I1) and (I2) the 1-bits are exactly the positions of the members of $S$, one per member, so $c = \lvert S \rvert$.

**NEXT$(B, i)$ with $i \ge 0$.** Let $g$ be the least member of $S$ with $g \ge i$, or NIL if there is none. If $q = \lfloor i / w \rfloor \ge m$ (line N2), then $i \ge mw \ge n$ and no member is $\ge i$, so NIL is right. Otherwise line N3 sets $x$ to $B[q]$ with the bits at positions $< i \bmod w$ cleared, because $(1 \ll (i \bmod w)) - 1$ has 1-bits exactly at those positions. *Loop invariant* for lines N4 to N7: $x$ is the word whose 1-bits are exactly the positions $t$ of word $j$ with $jw + t \ge i$ and $jw + t \in S$, and no member of $S$ lies in $[i, jw)$. Initially $j = q$ and this holds by line N3 and by (I1) and (I2), and $[i, qw)$ is empty since $qw \le i$. If $x = 0$, word $j$ has no member $\ge i$, so no member lies in $[i, (j + 1) w)$; lines N5 to N7 move to $j + 1$ and load the whole word, which is right because every position of word $j + 1$ is $\ge (j + 1) w > i$. If $j + 1 = m$, then no member lies in $[i, mw) \supseteq [i, n)$ and NIL is right. When the loop ends with $x \ne 0$, the lowest 1-bit of $x$ is at position $\mathrm{CTZ}(x)$, and $j w + \mathrm{CTZ}(x)$ is the least member $\ge i$ by the invariant. The loop stops because $j$ increases and is bounded by $m$.

**COMPLEMENT.** After lines K1 and K2, every bit of the array is inverted. So for $0 \le i < n$ the bit of $i$ is 1 exactly when $i \notin S$, which is (I1) for $\{0, \dots, n - 1\} \setminus S$, and every padding bit is 1. If $n \bmod w = 0$ there are no padding positions, because then $mw = n$. Otherwise the padding positions are the bits $t \ge n \bmod w$ of $B[m - 1]$, since $(m - 1) w + t \ge n \iff t \ge n - (m - 1) w = n \bmod w$. Line K3 ANDs $B[m - 1]$ with $2^{n \bmod w} - 1$, which clears exactly these bits and keeps the others, so (I2) holds and (I1) is not affected.

**UNION$(A, B)$.** Both arrays satisfy the invariant over the same $n$, for sets $S$ and $T$. Lines K4 and K5 set each bit of $A$ to the OR of the bits at the same position. For $0 \le i < n$ the new bit is 1 exactly when $i \in S$ or $i \in T$, which is (I1) for $S \cup T$. A padding bit is the OR of two zeros by (I2), so it stays 0. Intersection and difference are the same argument with AND, and with AND of the complement; a padding bit of $A$ is 0 and stays 0.

**Conclusion.** NEW establishes the invariant, each operation that writes keeps it for the new set, and each operation that reads returns the value the abstract type asks for, given the invariant. By induction on the number of operations, every sequence of operations from NEW returns correct answers. $\blacksquare$
