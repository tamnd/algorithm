---
title: The table-filling algorithm marks exactly the distinguishable pairs and returns the minimal DFA
proves: [correctness, termination]
status: full
---

Let $M = (Q, \Sigma, \delta, q_0, F)$ be a complete DFA, $\delta : Q \times \Sigma \to Q$, and let $R$ be the set of states reachable from $q_0$. For $p, q \in R$, a string $z$ *distinguishes* $p$ and $q$ if exactly one of $\delta^*(p, z)$ and $\delta^*(q, z)$ is in $F$. The states are *equivalent*, $p \approx q$, if no string distinguishes them. Pairs are unordered pairs $\{p, q\}$ of distinct states of $R$.

**Lemma 1 (termination).** The loop of lines L6 to L9 stops, and each pair is pushed at most once.

*Proof.* A pair is pushed only at the moment it is marked, at line L4 or line L9, and a marked pair is never unmarked. Line L9 marks only unmarked pairs. So each pair is pushed at most once, and the loop makes at most $\binom{|R|}{2}$ passes. $\square$

**Lemma 2 (the waiting lists).** For pairs $\{p, q\}$ and $\{r, s\}$, $\{p, q\}$ is in the list $S[r, s]$ if and only if $\{\delta(p, a), \delta(q, a)\} = \{r, s\}$ for some $a \in \Sigma$.

*Proof.* Line L5 appends $\{p, q\}$ to $S[\delta(p, a), \delta(q, a)]$ for each $a$ with $\delta(p, a) \ne \delta(q, a)$, and nothing else appends to the lists. $\square$

**Lemma 3 (soundness).** Each marked pair is distinguishable.

*Proof.* By induction on the order in which pairs are marked. A pair marked at line L4 has exactly one state in $F$, so $\varepsilon$ distinguishes it. A pair $\{p, q\}$ marked at line L9 is in $S[r, s]$ for a pair $\{r, s\}$ that was marked earlier, since it was pushed when marked. By Lemma 2 there is $a$ with $\{\delta(p, a), \delta(q, a)\} = \{r, s\}$, and by induction some $z$ distinguishes $r$ and $s$. Then $az$ distinguishes $p$ and $q$. $\square$

**Lemma 4 (completeness).** Each distinguishable pair is marked when the loop stops.

*Proof.* By induction on the length of a shortest distinguishing string $z$ of the pair $\{p, q\}$. If $z = \varepsilon$, exactly one of $p, q$ is in $F$, and line L4 marks the pair. If $z = az'$, then $r = \delta(p, a)$ and $s = \delta(q, a)$ are distinguished by the shorter string $z'$, so $r \ne s$, and by induction $\{r, s\}$ is marked. Each marked pair is pushed once and, by the loop condition, popped before the loop stops. When $\{r, s\}$ is popped at line L7, line L8 reads the list $S[r, s]$, which contains $\{p, q\}$ by Lemma 2. So $\{p, q\}$ is marked then, if it was not marked before. $\square$

So, when the loop stops, an unordered pair of distinct reachable states is unmarked if and only if its states are equivalent.

**Lemma 5 (the classes).** $\approx$ is an equivalence relation on $R$. If $p \approx q$, then $\delta(p, a) \approx \delta(q, a)$ for each $a$, and $p \in F \Leftrightarrow q \in F$.

*Proof.* "Same membership in $F$ after $z$" is reflexive, symmetric and transitive for each fixed $z$, so $\approx$ is an equivalence relation. If $z$ distinguished $\delta(p, a)$ and $\delta(q, a)$, then $az$ would distinguish $p$ and $q$. With $z = \varepsilon$, $p$ and $q$ agree on $F$. $\square$

**Lemma 6 (the quotient).** Lines L10 to L12 make the DFA $M' = (R / {\approx}, \Sigma, \delta', [q_0], F')$ with $\delta'([p], a) = [\delta(p, a)]$ and $F' = \{[p] : p \in F \cap R\}$, and $L(M') = L(M)$.

*Proof.* Line L10 gives each state the least state of $R$, in the fixed order, that is unmarked with it, which by Lemmas 3 to 5 is the least element of its class. So two states get the same representative if and only if they are equivalent. By Lemma 5, $\delta'$ and $F'$ do not depend on the choice of $p$ in its class. By induction on $|w|$, $\delta'^*([q_0], w) = [\delta^*(q_0, w)]$, and by Lemma 5 again, $[\delta^*(q_0, w)] \in F'$ if and only if $\delta^*(q_0, w) \in F$. $\square$

**Theorem.** TABLE-FILLING$(M)$ stops and returns a DFA with the language of $M$ and with the least number of states among all complete DFAs for $L(M)$.

*Proof.* It stops by Lemma 1 and the finiteness of the other loops, and $L(M') = L(M)$ by Lemma 6. Each state of $M'$ is $[\delta^*(q_0, x)]$ for some $x$, since $R$ is the set of reachable states. Two different states $[\delta^*(q_0, x)]$ and $[\delta^*(q_0, y)]$ are distinguished by some $z$, and then exactly one of $xz$ and $yz$ is in $L(M)$, so $x \not\equiv_L y$ for the Myhill-Nerode relation of $L = L(M)$. So $L$ has at least $|R / {\approx}|$ classes, and by the Myhill-Nerode theorem each complete DFA for $L$ has at least that many states. $\blacksquare$

**Running time.** Let $n = |R|$ and $\sigma = |\Sigma|$. The search of line L1 costs $O(|Q| \sigma)$ in the worst case and $O(n \sigma)$ on the reachable part. Lines L2 to L5 touch each of the $\binom{n}{2}$ pairs $O(\sigma)$ times, and the lists hold at most $\sigma \binom{n}{2}$ entries in total. By Lemma 1 each list is read at most once in lines L6 to L9, so the loop costs $O(\sigma n^2)$. Lines L10 to L12 cost $O(n^2 + n\sigma)$. The total is $O(\sigma n^2)$ time and $O(\sigma n^2)$ space.
