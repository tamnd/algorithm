---
title: Bitonic sort sorts each input
proves: [correctness]
status: full
---

The calls of BITONIC-SORT and HALF-CLEANERS make the same comparators on each input, so they form a comparator network. Each comparator only exchanges two items, so the output is a permutation of the input. By the [zero-one principle](/zero-one-principle/) it is enough to show that the output is sorted for each input in $\{0, 1\}^n$. In this proof all sequences are of zeros and ones, and positions are counted from 0.

**Bitonic 0-1 sequences.** Call $x \in \{0, 1\}^m$ *bitonic* when the set of positions $t$ with $x_t = 1$ is empty or one cyclic interval $\{a, a + 1, \ldots, a + \ell - 1\}$ of $\mathbb{Z}_m$, with the positions read modulo $m$. The complement of a cyclic interval is empty or a cyclic interval, so $x$ is bitonic exactly when its zeros fill one cyclic interval or none. Each sorted sequence $0^{z} 1^{m - z}$ is bitonic, and so is a sequence of one value only, which we call *clean*. The reverse of a bitonic sequence is bitonic. These are the 0-1 images of the [bitonic sequences](/bitonic-sequence/) of the usual definition.

**Lemma 1 (half-cleaner).** Let $x \in \{0, 1\}^{2h}$ be bitonic, and apply the comparators $[t : t + h]$ for $t = 0, \ldots, h - 1$ (line L10, with $lo = 0$). Let $u$ be the first half and $v$ the second half of the result. Then $u$ and $v$ are bitonic, $u$ or $v$ is clean, and $u_s \le v_t$ for all $s, t$.

*Proof.* The comparators have disjoint wires, so $u_t = \min(x_t, x_{t+h})$ and $v_t = \max(x_t, x_{t+h})$. Let $\ell$ be the number of ones of $x$.

Case $\ell \le h$. The ones fill a cyclic interval $I$ of length $\ell \le h$. The positions $t$ and $t + h$ have cyclic distance $h$ in both directions, so an interval that holds both has at least $h + 1$ positions. So no $t$ has $x_t = x_{t+h} = 1$, and $u$ is all zeros. Next, $v_t = 1$ if and only if $t \in I$ or $t + h \in I$, that is, if and only if $t \equiv i \pmod h$ for some $i \in I$. The map $i \mapsto i \bmod h$ sends the $\ell \le h$ consecutive positions of $I$ to $\ell$ consecutive positions of $\mathbb{Z}_h$, so the ones of $v$ fill one cyclic interval. So $v$ is bitonic, $u$ is clean, and $u_s = 0 \le v_t$.

Case $\ell \ge h$. Then $x$ has $2h - \ell \le h$ zeros, and they fill a cyclic interval. The argument above with zeros and ones exchanged shows that no $t$ has $x_t = x_{t+h} = 0$, so $v$ is all ones, and the zeros of $u$ fill one cyclic interval. So $u$ is bitonic, $v$ is clean, and $u_s \le 1 = v_t$. $\square$

**Lemma 2.** For each power of 2 $m$ and each $lo$, HALF-CLEANERS$(A, lo, m)$ sorts $A[lo \ldots lo + m - 1]$ if this part is a bitonic 0-1 sequence, and it changes no other entry of $A$.

*Proof.* By induction on $m$. If $m = 1$, line L8 returns and one item is sorted. Let $m = 2h \ge 2$. Line L10 is the half-cleaner of Lemma 1 on the part. After it, both halves are bitonic and each item of the first half is at most each item of the second half. By the induction hypothesis, lines L11 and L12 sort each half and touch nothing else. A sorted first half whose items are all at most the items of a sorted second half gives a sorted part. $\square$

**Lemma 3 (the flip).** Let $A[lo \ldots lo + m - 1]$ with $m = 2h$ be two sorted 0-1 halves. Then after line L5, both halves are bitonic and each item of the first half is at most each item of the second half.

*Proof.* Take $lo = 0$. Let $p = A[0 \ldots h-1] = 0^{a} 1^{h-a}$ and $q = A[h \ldots m-1] = 0^{b} 1^{h-b}$, and let $q^R$ be $q$ in reverse order. The sequence $y = p \, q^R = 0^{a} 1^{2h - a - b} 0^{b}$ is bitonic, because its ones are consecutive. Line L5 compares $A_t$ with $A_{m-1-t}$, and $A_{m-1-t} = q_{h-1-t} = (q^R)_t = y_{t+h}$. So the first half after line L5 is the first half $u$ of the half-cleaner applied to $y$, and the second half after line L5 is the second half $v$ of that half-cleaner, in reverse order. By Lemma 1, $u$ and $v$ are bitonic and $u_s \le v_t$ for all $s, t$. The reverse of $v$ is bitonic and holds the same items as $v$. $\square$

**Theorem.** For each power of 2 $m$ and each $lo$, BITONIC-SORT$(A, lo, m)$ sorts $A[lo \ldots lo + m - 1]$ for each 0-1 content of this part, and it changes no other entry of $A$. So, by the zero-one principle, BITONIC-SORT$(A, 0, n)$ sorts each array $A$ of $n$ items from a totally ordered set.

*Proof.* By induction on $m$. If $m = 1$, line L1 returns. Let $m = 2h \ge 2$. By the induction hypothesis, lines L3 and L4 sort the two halves and change nothing else. By Lemma 3, after line L5 both halves are bitonic and each item of the first half is at most each item of the second half. By Lemma 2, lines L6 and L7 sort each half, and the part is then sorted. Each line touches only positions in $[lo, lo + m)$. $\blacksquare$
