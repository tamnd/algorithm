---
title: Ben-Or's algorithm is safe always and terminates with probability 1
proves: [correctness, termination]
status: full
---

**Claim.** In the asynchronous model with $n$ processes, reliable links and at most $f$ crash failures, $n > 2f$, each run of BEN-OR has these properties. (Agreement) No two processes decide different values, also when one of them crashes later. (Validity) If all inputs are $v$, every decision is $v$, and each correct process decides in round 1. (Progress) Each correct process completes every round. (Termination) Against an adversary whose schedule does not depend on the coin values, each correct process decides with probability 1, and the expected number of rounds is at most $2^n + 1$.

The safety part holds in every run, whatever the schedule and the coins. The termination part is proved here for an adversary that does not see the coins. Aguilera and Toueg (2012) prove termination with probability 1 also for an adversary that sees all states and coins; their proof is longer and is not repeated here.

**Setup.** In round $r$, process $p$ sends a report $(R, r, x)$ at line L3 and a proposal $(P, r, w)$ at line L5 or L6, where $w \in \{0, 1, ?\}$. Each process sends at most one report and one proposal per round, with the same content to every receiver. A crash can cut a broadcast, so some processes may get the message and others not, but no two processes get different contents for the same message. Lines L4 and L7 use the first $n - f$ messages of the kind and round, from $n - f$ different senders. A process *completes round $r$* when it runs line L11 in round $r$. The *start value* of $p$ for round $r$ is the value of $x$ that it reports at line L3 in round $r$.

**Lemma A (one proposal value).** In each round $r$, all proposals other than $?$ carry the same value.

*Proof.* A process proposes $v$ only if more than $n/2$ of the reports it uses carry $v$ (line L5). These reports come from different senders, so more than $n/2$ processes have start value $v$ for round $r$. If one process proposed 0 and another proposed 1, more than $n/2$ processes would have start value 0 and more than $n/2$ would have start value 1. Each process has one start value, so this needs more than $n$ processes. $\square$

**Lemma B (a decision fixes the next round).** If some process decides $v$ in round $r$, then every process that completes round $r$ sets $x = v$ at line L9 of round $r$.

*Proof.* The decider used $n - f$ proposals of round $r$ and found at least $f + 1$ of them equal to $v$ (line L8). So at least $f + 1$ different processes sent $(P, r, v)$. Let $q$ complete round $r$. It used proposals from $n - f$ different senders, so at most $f$ processes are missing from its set. At least one of the $f + 1$ senders of $(P, r, v)$ is in its set, so $q$ got at least one proposal $v$. By Lemma A, every proposal other than $?$ that $q$ got is $v$. So $q$ runs line L9 with the value $v$, and does not reach line L10. $\square$

**Lemma C (a common start value decides).** If every process that reports in round $r$ has start value $v$, then every proposal of round $r$ is $v$, every process that completes round $r$ ends it with $x = v$, and every process that completes round $r$ with no earlier decision decides $v$ in round $r$.

*Proof.* Let $q$ propose in round $r$. All the $n - f$ reports that $q$ uses carry $v$. Since $n > 2f$, $n - f > n/2$, so $q$ proposes $v$ at line L5. So every proposal of round $r$ is $v$. Now let $q$ complete round $r$. The $n - f$ proposals that $q$ uses are all $v$, and $n - f \ge f + 1$ because $n \ge 2f + 1$. So line L8 makes $q$ decide $v$ if it has not decided before, and line L9 sets $x = v$. $\square$

**Agreement.** Let $r$ be the first round in which some process decides, and let it decide $v$.

1. Every decision made in round $r$ is $v$. A decision $v'$ at line L8 needs $f + 1$ proposals $v'$, and by Lemma A every proposal other than $?$ in round $r$ is $v$. So $v' = v$.
2. By Lemma B, every process that completes round $r$ has $x = v$ at its end. So every process that reports in round $r + 1$ has start value $v$.
3. By Lemma C, every process that completes round $r + 1$ ends it with $x = v$, and every proposal of round $r + 1$ is $v$, so every decision made in round $r + 1$ is $v$.
4. By induction on $r' \ge r + 1$, using Lemma C in each round, every process that reports in round $r'$ has start value $v$, every proposal of round $r'$ is $v$, and every decision made in round $r'$ is $v$.

So every decision is $v$. This covers a process that decides and then crashes, so the agreement is uniform.

**Validity.** If all inputs are $v$, every process that reports in round 1 has start value $v$. By Lemma C, every process that completes round 1 decides $v$ in round 1. By the agreement argument with $r = 1$, every decision is $v$.

**Progress.** By induction on $r$, every correct process completes round $r$. Assume every correct process completed round $r - 1$, or let $r = 1$. Then every correct process sends its report of round $r$ to all, and since it never crashes, the whole broadcast goes out. At least $n - f$ processes are correct, and links are reliable, so every correct process gets at least $n - f$ reports of round $r$ and passes line L4. In the same way every correct process sends its proposal of round $r$, and every correct process gets $n - f$ of them and passes line L7. It then runs lines L8 to L11 with no further wait. A process that has decided keeps running the loop, so the others always find $n - f$ senders.

**Termination with probability 1.** Assume an adversary whose choices do not depend on the coin values: it chooses which message to deliver next and when processes crash by looking only at the senders, receivers, kinds and round numbers of messages.

1. *The schedule does not depend on the coins.* The control flow of a process depends only on how many messages of each kind and round it has, not on their contents: lines L4 and L7 count, and every other line runs without a wait. So, for a fixed adversary, inputs and crash plan, the order of deliveries, the crash points and the sets of $n - f$ messages that each process uses at lines L4 and L7 are the same for every outcome of the coins.
2. *Coins of round $r$ are fresh.* Let $c_p(r)$ be the coin that $p$ would flip at line L10 in round $r$. The coins $c_p(r)$ for all $p$ and $r$ are independent and uniform on $\{0, 1\}$. By step 1, the start values for round $r$, the proposals of round $r$ and the set $F_r$ of processes that run line L10 in round $r$ are functions of the inputs and of the coins $c_q(r')$ with $r' < r$. They do not depend on the coins of round $r$.
3. *A good round.* By Lemma A, at most one value $w_r$ appears in proposals of round $r$. Let $t_r = w_r$ if it exists, and $t_r = 0$ otherwise. Every process that completes round $r$ and is not in $F_r$ sets $x = w_r$ at line L9. So if $c_p(r) = t_r$ for every $p \in F_r$, every process that completes round $r$ ends it with $x = t_r$. Given the coins of earlier rounds, $t_r$ and $F_r$ are fixed, and $|F_r| \le n$, so this event has probability at least $2^{-n}$.
4. *A good round ends the run.* If round $r$ is good, every process that reports in round $r + 1$ has start value $t_r$, and by Lemma C every process that completes round $r + 1$ decides. By Progress, every correct process completes round $r + 1$, so every correct process has decided by the end of round $r + 1$.
5. *Counting rounds.* By step 3, for each $r$, the probability that round $r$ is good is at least $2^{-n}$ given any outcome of the earlier rounds. So the probability that none of the rounds $1, \ldots, k$ is good is at most $(1 - 2^{-n})^k$, which tends to 0. With probability 1 some round is good, and every correct process decides one round later. The first good round $G$ has $\Pr[G > k] \le (1 - 2^{-n})^k$, so $\mathbb{E}[G] = \sum_{k \ge 0} \Pr[G > k] \le 2^n$, and the expected number of rounds until all correct processes have decided is at most $2^n + 1$. $\blacksquare$
