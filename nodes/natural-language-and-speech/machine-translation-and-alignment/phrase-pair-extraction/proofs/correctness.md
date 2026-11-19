---
title: Phrase pair extraction returns exactly the consistent phrase pairs up to the length limit
proves: [correctness]
status: full
---

Let $A \subseteq \{1, \ldots, m\} \times \{1, \ldots, l\}$ be the links $(j, i)$, with $j$ a source position and $i$ a target position. Spans are fencepost: the span $(s, t)$ covers the positions $s + 1, \ldots, t$. A phrase pair $((s, t), (u, v))$ is *consistent* if (a) some link $(j, i) \in A$ has $s < j \le t$ and $u < i \le v$, and (b) no link has exactly one of $s < j \le t$ and $u < i \le v$. Let $L$ be the length limit. Let $P^*$ be the set of consistent pairs with $t - s \le L$ and $v - u \le L$, and let $P$ be the set that EXTRACT returns. A target position $i$ is *aligned* if some link has target $i$.

For a source span $(s, t)$ let $T(s, t) = \{i : (j, i) \in A, s < j \le t\}$, the set that line L4 collects. When it is not empty, let $u_0 = \min T(s, t) - 1$ and $v_0 = \max T(s, t)$, the values of line L6.

**Lemma 1 (the tight target span).** A pair $((s, t), (u, v))$ is consistent if and only if $T(s, t) \ne \emptyset$, $u \le u_0$, $v \ge v_0$, every link $(j, i)$ with $u_0 < i \le v_0$ has $s < j \le t$, and every target position in $u + 1, \ldots, u_0$ and in $v_0 + 1, \ldots, v$ is unaligned.

*Proof.* Suppose the pair is consistent. By (a), some link starts inside $(s, t)$, so $T(s, t) \ne \emptyset$. Every $i \in T(s, t)$ comes from a link with its source inside, so by (b) its target is inside: $u < i \le v$. So $u < \min T = u_0 + 1$, that is $u \le u_0$, and $v \ge \max T = v_0$. A link with $u_0 < i \le v_0$ has its target inside $(u, v)$, so by (b) its source is inside $(s, t)$. A target position $i$ in $u + 1, \ldots, u_0$ is inside $(u, v)$ but not in $T(s, t)$. If it had a link $(j, i)$, then by (b) $s < j \le t$, so $i \in T(s, t)$, a contradiction. The same holds for $v_0 + 1, \ldots, v$.

Conversely, suppose the conditions hold. A link with source in $(s, t)$ has its target in $T(s, t) \subseteq (u_0, v_0] \subseteq (u, v]$, and there is at least one such link, so (a) holds. A link with target in $(u, v]$ has its target in $(u_0, v_0]$, because the positions outside it are unaligned, so its source is in $(s, t)$. So no link has exactly one end inside, and (b) holds. $\square$

**Lemma 2 (lines L8 to L16).** Let $(s, t)$ pass the tests of lines L5 and L7. Then the loops of lines L8 to L16 visit exactly the pairs $(u_2, v_2)$ with $u_2 \le u_0$, $v_2 \ge v_0$, $u_2 \ge 0$, $v_2 \le l$, and all target positions in $u_2 + 1, \ldots, u_0$ and in $v_0 + 1, \ldots, v_2$ unaligned. Line L12 adds those of them with $v_2 - u_2 \le L$.

*Proof.* The outer loop starts at $u_2 = u_0$ and, at line L15, lowers $u_2$ by one. Line L16 stops it when $u_2 < 0$ or when the newly added position $u_2 + 1$ is aligned. So the outer loop runs for $u_2 = u_0, u_0 - 1, \ldots$ down to the last value such that $u_2 \ge 0$ and all positions $u_2 + 1, \ldots, u_0$ are unaligned. These are exactly the allowed values of $u_2$, because the condition "all of $u_2 + 1, \ldots, u_0$ unaligned" stays false once it fails. The inner loop does the same for $v_2$ from $v_0$ upward with lines L13 and L14, and it does not depend on $u_2$. Line L12 tests the length. $\square$

**Theorem.** $P = P^*$.

*Proof.* Line L2 and L3 go over every source span with $1 \le t - s \le L$. Take one. If $T(s, t) = \emptyset$, no pair with this source span is consistent by (a), and line L5 skips it. Otherwise the test of line L7 is the third condition of Lemma 1 for this source span, which does not depend on $u$ or $v$. If it fails, no pair with this source span is consistent, and the span is skipped. If it holds, Lemma 2 says that line L12 adds exactly the target spans $(u_2, v_2)$ that meet the other conditions of Lemma 1 and have $v_2 - u_2 \le L$. By Lemma 1 these are exactly the consistent pairs with this source span and both sides at most $L$ words. Each pair is added to a set, so none is counted twice. $\square$

**Termination and cost.** There are at most $m L$ source spans. For each, lines L4 and L7 read the $|A|$ links once, and the loops of lines L8 to L16 run at most $(u_0 + 1)(l - v_0 + 1) \le (l + 1)^2$ times but add only pairs with $v_2 - u_2 \le L$. With $l'$ the length of the longest run of unaligned target words, the inner work is $O((l' + 1)^2)$ for each source span, and the total time is $O(m L (|A| + (l' + 1)^2))$.
