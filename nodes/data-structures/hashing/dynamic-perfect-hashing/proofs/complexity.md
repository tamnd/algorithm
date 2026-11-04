---
title: Dynamic perfect hashing has O(1) worst-case search, O(1) expected amortized updates and O(n) space
proves: [time.amortized, space.extra]
status: full
---

The model is the word RAM with $p < 2^w$, so a hash value costs $O(1)$ time. The structure starts with REHASH-ALL$(\emptyset)$, and the sequence of operations is fixed before the random choices (an oblivious adversary). We use the invariants (D1) to (D5), Fact (U), Lemma 1 and the corollary $M \le 2|S| + 1$ of [the correctness proof](correctness.md). The sum $\sum_i 2L_i^2$ of line L8 is kept in a counter, set by line L23 and changed at line L7, so line L8 takes $O(1)$ time. The constants 64 and 512 are those of this page, not of the paper of Dietzfelbinger and others; the structure of the proof (rebuild a bucket after a collision, double a full bucket, start a new phase after a fixed number of updates or when the space is too large) follows that paper.

A **phase** is the time from one call of REHASH-ALL to the next. In a phase, $h$ and $M$ are fixed. As in the correctness proof, an update is **effective** when it changes $S$. Whether an update is effective depends only on $S$, so the sequence of sets $S$ is fixed by the sequence of operations and does not depend on the random choices.

**Claim 1 (search).** DPH-SEARCH takes $O(1)$ time in the worst case. So does each operation that is not effective.

*Proof.* Lines L14 and L15 compute two hash values and compare one key. Lines L1 and L10 call it once. $\square$

**Claim 2 (space).** In each state the structure uses $O(|S| + 1)$ words.

*Proof.* The first level stores $M$ entries of $O(1)$ words each ($S_j$ is not stored apart from $T_j$; the Python version keeps it as a set of size $|S_j|$, which adds $O(|S|)$). The second level has $\sum_j 2L_j^2 \le 512M$ slots by (D4). By the corollary, $M \le 2|S| + 1$. $\square$

**Lemma 3 (one rebuild of a bucket).** Given any history, REBUILD-BUCKET$(j)$ takes $O(|S_j| + 1)$ expected time, plus $O(L_j^2)$ if line L16 allocates a new array.

*Proof.* By Lemma 1 of the correctness proof, each trial succeeds with probability more than $3/4$, whatever happened before, because its draws are fresh. So the expected number of trials is less than $4/3$. A trial computes $|S_j|$ hash values and tests that they are distinct. The test takes $O(|S_j|)$ time with the table itself: write a mark in each slot, stop at a slot that is already marked, then clear the marked slots. Line L16 clears $|S_j|$ slots, or allocates $2L_j^2$ slots. Line L19 takes $O(|S_j| + 1)$. $\square$

**Lemma 4 (a collision is unlikely).** Consider an effective insert of $x$ that reaches line L5 with $c_j \le L_j$ for $j = h(x)$. The probability that the slot $T_j[h_j(x)]$ is in use, given the history up to this point, is at most $2/(3L_j)$.

*Proof.* Look at the last rebuild of bucket $j$ before this insert, and let $H$ be the history up to its start. Given $H$, the function $h$ of the phase and the sequence of effective updates are fixed. Let $A_0$ be $S_j$ at that rebuild, and let $B$ be $A_0$ together with the keys that the effective updates insert into bucket $j$ from then up to and including $x$. So $B$ is fixed given $H$, and $|B| \le c_j \le L_j$, since $c_j$ was set to $|A_0|$ by the rebuild and raised by one at each of these inserts.

The rebuild draws functions $g$ from the family with $s = 2L_j^2$ slots until $g$ is one-to-one on $A_0$, so the accepted $h_j$ is a raw draw $g$ conditioned on the event $G$ that $g$ is one-to-one on $A_0$. Let $E$ be the event that bucket $j$ is not rebuilt between the rebuild and this insert. A rebuild in between could come from line L9 or from REHASH-ALL. The rebuilds of cases 3 and 4 of the correctness proof, and REHASH-ALL at lines L3 and L12, depend only on counters, which are fixed given $H$; REHASH-ALL at line L8 depends only on the limits of the other buckets, because $L_j$ changes only at a rebuild of bucket $j$, and these limits depend on draws for the other buckets, which are independent of $g$. So, given $H$, $E$ is the intersection of an event $E_j$ that depends only on $g$ (that $g \in G$ and that no insert into bucket $j$ before $x$ found its slot in use) and an event independent of $g$, which cancels out of the conditional probability.

Let $I$ be the event that $g$ is one-to-one on $B$. Then $I \subseteq E_j$: if $g$ is one-to-one on $B$, it is one-to-one on $A_0$, and each key placed before $x$ found a free slot, since the slots in use hold other keys of $B$. By Lemma 1 of the correctness proof applied to $B$, $\Pr[I] > 3/4$. Let $D$ be the event that $g(x) = g(y)$ for some $y \in B \setminus \{x\}$. The slot of $x$ is in use only if it holds a key of $B \setminus \{x\}$, so the event of the claim implies $D$. By (U), $\Pr[D] \le (|B| - 1)/s < L_j / (2L_j^2)$. So

$$\Pr[\text{slot in use} \mid H, E] \le \frac{\Pr[D \cap E_j]}{\Pr[E_j]} \le \frac{\Pr[D]}{\Pr[I]} < \frac{1/(2L_j)}{3/4} = \frac{2}{3L_j}. \qquad \square$$

**Lemma 5 (rebuilds without doubling).** The rebuilds of line L9 in cases 2 and 3 of the correctness proof take $O(1)$ expected amortized time for each effective update.

*Proof.* *Case 2* (a collision with $c_j \le L_j$). By Lemma 3 the rebuild costs $O(|S_j| + 1) = O(L_j)$ expected time; no array is allocated, since $L_j$ did not change. By Lemma 4 it happens with probability at most $2/(3L_j)$. So its expected cost, for each insert, is $O(1)$.

*Case 3* ($c_j > L_j$ and $|S_j| \le L_j/2$). The cost is $O(|S_j| + 1) = O(L_j)$ expected time. Since the last rebuild of bucket $j$, let $c_0 = |S_j|$ at that rebuild, and let $i \ge 1$ and $d$ be the numbers of effective inserts and deletes in bucket $j$. Then $c_j = c_0 + i \ge L_j + 1$ and $|S_j| = c_0 + i - d \le L_j/2$. If $i < L_j/2$, then $c_0 > L_j/2$ and $d = c_0 + i - |S_j| > L_j/2$. In both cases $i + d \ge L_j/2$, so the cost is $O(i + d)$. Charge it to these $i + d$ updates. Each update is charged at most once, to the first rebuild of its bucket after it, since a rebuild resets the count. $\square$

**Lemma 6 (doubling).** Fix a phase, and let $k_j$ be the number of distinct keys that are in $S_j$ at some time during the phase. Then at each time of the phase, $L_j \le 4\max(k_j, 1)$. The arrays allocated in the phase, including those of the REHASH-ALL that starts it, have at most $\frac{4}{3} \cdot 512M$ slots in total, and the rebuilds of case 4 take $O(M)$ expected time in total.

*Proof.* REHASH-ALL sets $L_j = 2\max(|S_j|, 1) \le 2\max(k_j, 1)$. Line L7 doubles $L_j$ to $2L_j$ only when $|S_j| > L_j/2$, so $k_j \ge |S_j| > L_j/2$ and the new limit $2L_j < 4k_j$. A bucket allocates an array at the start of the phase and after each doubling that passes line L8, of sizes $2L^2, 2(2L)^2, 2(4L)^2, \ldots$, which grow by a factor of 4. Their sum is less than $\frac{4}{3}$ times the last one. The last ones are the current sizes, whose sum is at most $512M$ by (D4); a doubling that fails line L8 allocates nothing in this phase. So the total is at most $\frac{4}{3} \cdot 512M$ slots, and allocating them takes $O(M)$ time. A rebuild of case 4 costs, by Lemma 3, $O(|S_j| + 1) = O(L_j)$ expected time plus its allocation of $2L_j^2 \ge L_j$ slots, so these rebuilds take $O(M)$ expected time in total. $\square$

**Lemma 7 (REHASH-ALL).** REHASH-ALL$(S')$ takes $O(M)$ expected time, where $M = \max(|S'|, 1)$, given any history.

*Proof.* By the proof of Lemma 2 of the correctness proof, a trial of lines L21 and L22 succeeds with probability more than $5/8$, so the expected number of trials is less than $8/5$, and each takes $O(|S'| + M) = O(M)$ time. Line L23 then calls REBUILD-BUCKET for $M$ buckets. By Lemma 3, this takes $O(\sum_j (|S_j| + 1)) = O(M)$ expected time plus the allocation of $\sum_j 2L_j^2 \le 64M$ slots. $\square$

**Lemma 8 (line L8 rarely ends a phase).** Let $F$ be the history up to the start of a phase, before its first-level function is drawn. Then the probability, given $F$, that the phase ends at line L8 is less than $0.64$.

*Proof.* Given $F$, the set $S'$ at the start, with $n_0 = |S'| \le M$ keys, and the sequence of effective updates after it, are fixed. Let $K$ be $S'$ together with the keys inserted by the next $\lceil M/2 \rceil$ effective updates. Then $|K| \le n_0 + \lceil M/2 \rceil \le 2M$. The phase reaches line L4 for at most $\lceil M/2 \rceil$ effective updates, because the next one makes $u > \lceil M/2 \rceil$ and ends the phase at line L3 or L12. So each key that is ever in a bucket during the phase is in $K$. Let $k^*_j = |\{x \in K : h(x) = j\}|$, so $k_j \le k^*_j$. By Lemma 6, at each time of the phase,

$$\sum_j 2L_j^2 \le 32 \sum_j \max(k^*_j, 1)^2 \le 32 \Big( \sum_j (k^*_j)^2 + M \Big).$$

So line L8 can end the phase only if $\sum_j (k^*_j)^2 > 15M$. For a raw draw $g$ of the first-level function, the identity $\sum_j (k^*_j)^2 = |K| + 2C$, with $C$ the number of colliding pairs of $K$, and (U) give $E[\sum_j (k^*_j)^2] \le |K| + |K|(|K| - 1)/M \le 2M + 2(2M - 1) < 6M$, so by Markov's inequality $\Pr[\sum_j (k^*_j)^2 > 15M] < 6/15 = 0.4$. The function $h$ of the phase is a raw draw conditioned on the acceptance test of line L22, which passes with probability more than $5/8$ (Lemma 7). So the probability is less than $0.4/(5/8) = 0.64$. $\square$

**Theorem (time).** A sequence of $N$ operations, from the empty structure, takes $O(N + 1)$ expected time in total. So each operation takes $O(1)$ expected amortized time.

*Proof.* Each operation does $O(1)$ work outside the rebuilds (Claim 1, the counter of line L8). The rebuilds of cases 2 and 3 cost $O(N)$ expected in total (Lemma 5). The rest of the cost is in the phases: each phase $i$, with $M_i$ buckets, costs $O(M_i)$ expected time given its history $F_i$, for its REHASH-ALL (Lemma 7) and its doublings (Lemma 6). So the expected total is $O(N + 1 + E[\sum_i M_i])$. There are at most $N + 1$ phases, since each phase after the first starts during an effective update.

Let $Q_i$ be the indicator that phase $i$ exists and ends at line L8. $M_i$ is fixed by $F_i$, so by Lemma 8, $E[M_i Q_i] \le 0.64\, E[M_i]$, which gives $E[M_i] \le E[M_i (1 - Q_i)] / 0.36$. A phase with $Q_i = 0$ either ends at line L3 or L12, and then it contains $\lceil M_i/2 \rceil + 1 \ge M_i / 2$ effective updates of its own, or it is the last phase, and then $M_i \le 2|S| + 1 \le 2N + 1$. The phases are disjoint, so

$$E\Big[\sum_i M_i\Big] \le \frac{1}{0.36} E\Big[\sum_i M_i (1 - Q_i)\Big] \le \frac{1}{0.36} \big( 2N + 2N + 1 \big) = O(N + 1). \qquad \square$$

The paper of Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert and Tarjan (SIAM Journal on Computing 23(4), 1994, pages 738 to 761) proves the same three bounds for its own version of the scheme; the constants and the accounting above are not taken from it.
