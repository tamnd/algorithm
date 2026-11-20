---
title: Correctness and properties of the single transferable vote
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$ be the candidates and $k \ge 1$ the number of seats. The input is a list of ballots, each a sequence of distinct candidates, best first, possibly truncated. Empty ballots are dropped, and $V$ is the number of the other ballots. The quota is $q = \lfloor V/(k + 1) \rfloor + 1$ (Droop) or $q = V/k$ (Hare). In both cases $(k + 1) q > V$. Every claim below holds for both quotas.

The direct rule keeps a set $C$ of continuing candidates, a list $W$ of winners and a weight $w_i$ for each ballot, with $w_i = 1$ at the start. Ballot $i$ counts for the first entry of $r_i$ that is in $C$, if there is one; otherwise it is exhausted. Let $t(a)$ be the sum of the weights of the ballots that count for $a$. One round of the direct rule is:

1. If $|C| \le k - |W|$, append all of $C$ to $W$ by decreasing $t$ and then by index, and stop.
2. Else let $e$ be the candidate of $C$ with the largest $t$, the smallest index among ties. If $t(e) \ge q$ and $t(e) > 0$, multiply the weight of each ballot that counts for $e$ by $f = (t(e) - q)/t(e)$, remove $e$ from $C$ and append it to $W$.
3. Else remove from $C$ the candidate with the smallest $t$, the largest index among ties.

The rule stops when $|W| = k$ or $C$ is empty. The test file has an implementation of this direct rule, which recounts all ballots in every round.

**Claim 1 (invariant).** At the start of each pass of line L4, the set $C$, the list $W$ and the weights of the method are those of the direct rule after the same number of rounds. For every $a \in C$, $pile[a]$ is the set of ballots that count for $a$, and the tally of $a$ is the sum of their weights. For each ballot $i$ on $pile[a]$, $r_i[ptr[i]] = a$, and every entry of $r_i$ before position $ptr[i]$ is outside $C$.

*Proof.* By induction on the number of rounds. At the start, $C = A$, every weight is 1, and line L3 puts every ballot on the pile of its first entry, with the pointer at that entry. Assume the claim before a round. Then the tallies are the values $t(a)$ of the direct rule, so line L5 makes the same test as step 1, and line L7 picks the same $e$ as step 2. In the fill case both rules append the same list and stop.

In the elect case, line L8 removes $e$ and appends it to $W$, as in step 2. The ballots that count for $e$ are those of $pile[e]$. Line L10 multiplies their weights by $f$, as in step 2, and moves each one. A move advances the pointer past every entry that is not in $C$, so the ballot goes to the pile of its first entry in the new $C$, or it is exhausted. A ballot that counted for some $a \ne e$ still counts for $a$, because its earlier entries were outside the old $C$ and so are outside the new one; the method does not touch it. If $f = 0$, the ballots of $pile[e]$ have weight 0 in the direct rule from now on, and the method drops them; in both rules they add 0 to every later tally. The tally of each pile grows by the weights of the ballots that join it, so the tallies stay correct.

The eliminate case is the same with $f = 1$: line L11 picks the same candidate $x$ as step 3, line L12 removes it, and line L13 moves the ballots of $pile[x]$ with their weights unchanged.

**Claim 2 (termination and output).** The method stops after at most $m$ rounds and returns $\min(k, m)$ distinct candidates.

*Proof.* Each round that does not stop removes one candidate from $C$, so there are at most $m$ rounds. A candidate enters $W$ only when it leaves $C$, so the winners are distinct. Let $s = k - |W|$ be the number of empty seats. If $m \le k$, step 1 applies in the first round and $W$ gets all $m$ candidates. If $m > k$, then $|C| - s$ starts at $m - k > 0$. An election lowers $|C|$ and $s$ by 1 each, so it keeps $|C| - s$. An elimination lowers $|C| - s$ by 1. So the count either fills all seats in step 2, or it reaches $|C| - s = 0$ and step 1 elects exactly the $s$ candidates that are left. In both cases $|W| = k$.

**Claim 3 (conservation of votes).** At the start of each round,
$$\sum_{a \in C} t(a) + q \cdot |W| + X = V,$$
where $X$ is the total weight of the exhausted ballots. So each candidate elected in step 2 keeps exactly $q$ votes.

*Proof.* At the start the tallies sum to $V$, $W$ is empty and $X = 0$. An elimination moves each ballot of the eliminated candidate, with its weight, to another pile or to the exhausted ballots, so the sum does not change. An election of $e$ removes $t(e)$ from the tallies; the ballots of $pile[e]$ go on with the total weight $f \cdot t(e) = t(e) - q$, to other piles or to $X$, and $|W|$ grows by 1, which adds $q$. So the sum does not change.

**Claim 4 (proportionality for solid coalitions).** Let $S \subseteq A$ and $j \ge 1$ with $j \le \min(k, |S|)$. Suppose at least $j q$ ballots rank all members of $S$ above every other candidate (in any order among themselves, and with any continuation, or none, after $S$). Then the rule elects at least $j$ members of $S$.

*Proof.* Let $B$ be the set of these ballots, so $|B| \ge j q$, and let $e_S$ be the number of members of $S$ in $W$. We show that the following holds at the start of every round in which $e_S < j$:

(a) every ballot of $B$ counts for a member of $S \cap C$;

(b) $\sum_{a \in S \cap C} t(a) \ge (j - e_S) \, q$;

(c) $|S \cap C| \ge j - e_S$.

Note first that (a) follows from (c): each ballot of $B$ lists all of $S$ before any other candidate, so if $S \cap C$ is not empty, its first continuing entry is in $S \cap C$. At the start, $S \cap C = S$, so the sum in (b) is at least $|B| \ge j q$, and (c) is $|S| \ge j$. Assume (a), (b) and (c) at the start of a round of step 2 or step 3, and that $e_S < j$ still holds after it. First (c): an election of a member of $S$ lowers both sides of (c) by 1, and an election outside $S$ changes neither. An elimination happens only when every continuing candidate has $t < q$. Then, by (b), the members of $S \cap C$ have tallies that sum to at least $(j - e_S) q$, each below $q$, so there are at least $j - e_S + 1$ of them, and at least $j - e_S$ are left after one is removed. So (c) holds after the round, and (a) with it. Now (b): by (a), before and after the round, no ballot of $B$ is exhausted and none lies on the pile of a candidate outside $S$. So the weight of $B$, which is $|B|$ at the start of the count, is split between the piles of $S \cap C$ and the votes kept by the elected members of $S$. Each of them keeps $q$ votes in total by Claim 3, so at most $q$ from $B$, and (b) holds after the round.

Now suppose that $e_S < j$ when the count stops. If it stops in step 1, all of $C$ is elected, and by (c) this adds at least $j - e_S$ members of $S$, so $e_S \ge j$ after all. If it stops in step 2 with $|W| = k$, then $k - e_S$ winners are outside $S$, each elected in step 2, and by (a) none of the $q$ votes that each keeps comes from $B$. So the ballots outside $B$ have a total weight of at least $(k - e_S) q$:
$$V - |B| \ge (k - e_S) \, q, \qquad\text{so}\qquad V \ge (k - e_S + j) \, q \ge (k + 1) \, q > V.$$
This is a contradiction. The count cannot stop with $C$ empty while $e_S < j$, by (c). So at least $j$ members of $S$ are elected.

**Claim 5 (one seat).** With $k = 1$ and the Droop quota, the rule elects the winner of [instant-runoff voting](/instant-runoff-voting/) with the same elimination tie rule.

*Proof.* With $k = 1$, $q = \lfloor V/2 \rfloor + 1$, which is more than $V/2$. Step 1 applies only when one candidate is left, and step 2 elects $e$ only when $t(e) > V/2$, which is at least half of the ballots that are not exhausted. While nobody has $t \ge q$, steps 3 of both rules remove the same candidate. If step 2 elects $e$ with $t(e) > V/2 \ge T/2$, where $T$ is the number of ballots that are not exhausted, then by Claim 3 of the instant-runoff page, eliminating to the end also elects $e$, and so does the instant-runoff rule, which stops at the first majority of the ballots that still count.
