---
title: Cheap Paxos chooses at most one command per slot
proves: [correctness]
status: full
---

The model is asynchronous, with crash failures, stable storage at main processors, and messages that can be lost, duplicated and reordered. The window is $\alpha = 1$: the configuration $C(s + 1)$ is $C(s)$ changed by the command chosen in slot $s$, and $C(0)$ is the initial configuration with $f + 1$ mains and $f$ auxiliaries. A command $v$ is *chosen in slot $s$ with ballot $b$* when every processor of some quorum of $C(s)$ has run line L11 with $(b, s, v)$.

**Lemma 1 (quorums of one configuration meet).** Let $C$ have mains $M$ and members $G \supseteq M$ with $|M| \ge \lceil |G|/2 \rceil$. Then any two quorums of $C$ meet.

*Proof.* Two majorities of $G$ meet, since together they have more than $|G|$ elements. A majority $Q$ of $G$ and the set $M$ meet, since $|Q| + |M| > |G|/2 + |G|/2 = |G|$, and both are subsets of $G$. The set $M$ meets itself because $|M| \ge 1$. $\square$

**Lemma 2 (the invariant holds in every configuration).** Every configuration that line L8 builds satisfies $|M| \ge \lceil |G|/2 \rceil$ and $|M| \ge 1$.

*Proof.* At the start $|M| = f + 1 = \lceil (2f + 1)/2 \rceil$. A "remove" command takes one main out of $M$, and then line L8 drops auxiliaries from $G$ while $2|M| < |G|$. Each drop lowers $|G|$ by one, so the loop ends with $2|M| \ge |G|$, which is $|M| \ge \lceil |G|/2 \rceil$ for integers. A leader never queues the removal of itself, and a command that would remove the last main leaves the configuration unchanged, so $M$ keeps at least one main. $\square$

**Lemma 3 (one value per ballot and slot).** For each ballot $b$ and slot $s$, at most one value appears in a message ACCEPT($b$, $s$, $v$).

*Proof.* Only the processor named in $b$ uses $b$. Line L1 gives it a fresh round each time. In one ballot it runs line L4 for slot $s$ once, and later resends of line L7 repeat the same message. $\square$

**Lemma 4 (promises cover all later slots).** If processor $a$ sends PROMISE($b$, ...) for a PREPARE($b$, $s_0$), then for each slot $s \ge s_0$ it never accepts a ballot below $b$ afterwards, and the report holds its vote with the largest ballot in $s$ so far, all of which have ballots below $b$, or the decision of $s$.

*Proof.* The variable promised never decreases (lines L10 and L11 only raise it) and survives crashes. Line L11 accepts only ballots $\ge$ promised. Votes in slot $s$ are overwritten only by votes with a ballot at least as large, so the stored vote is the largest. Line L10 reports all votes for slots $\ge s_0$. At an auxiliary, line L13 erases only slots below its forget bound, and line L10 refuses a PREPARE whose start slot is below that bound, so no erased vote is ever needed in a report. $\square$

**Lemma 5 (one configuration per slot).** If, for every slot $t < s$, at most one command is chosen in $t$, then all processors that compute $C(s)$ get the same configuration.

*Proof.* A processor computes $C(s)$ only from decisions of slots $t < s$ (line L8), each of which is the chosen command of $t$. By the assumption these are unique, and $C(s)$ is a function of them. $\square$

**Invariant P2c (per slot).** If ACCEPT($b$, $s$, $v$) is sent, there is a quorum $S$ of $C(s)$ such that either (a) no processor of $S$ ever accepts a ballot below $b$ in slot $s$, or (b) $v$ is the value of the largest ballot below $b$ that any processor of $S$ ever accepts in slot $s$, or (c) $v$ was reported as decided in slot $s$.

*Proof.* Let $S$ be the quorum of line L3 that sent PROMISE($b$, ...) for a PREPARE($b$, $s_0$) with $s_0 \le s$. By Lemma 4, every acceptance below $b$ in slot $s$ at a processor of $S$ happens before its promise and is reported. Line L4 takes a reported decision (case (c)), else the value of the largest reported ballot, which is the value of every acceptance in that ballot by Lemma 3 (case (b)), else any value (case (a)). $\square$

**Theorem (agreement).** For every slot $s$, at most one command is chosen in $s$.

*Proof.* Induction on $s$. Assume the claim for all slots below $s$. By Lemma 5 all processors use the same $C(s)$, and by Lemmas 1 and 2 any two quorums of $C(s)$ meet.

A decision for $s$ is stored only by line L6, after a quorum of $C(s)$ has accepted $(b_1, s, w)$, so every reported decision is a value chosen in $s$. Fix a finite prefix of the run in which some value is chosen in $s$, let $b_0$ be the smallest ballot with which a value is chosen in $s$, and let $v$ be that value.

We show by induction on the order in which the messages are sent: every ACCEPT($b$, $s$, $w$) with $b > b_0$ has $w = v$. Let $S$ be the quorum of P2c for this message.

- Case (c): $w$ is a reported decision, so $w$ is chosen in $s$ with some ballot $b_1 \ge b_0$. If $b_1 = b_0$, Lemma 3 gives $w = v$. If $b_1 > b_0$, the message ACCEPT($b_1$, $s$, $w$) was sent before the decision was reported, so before the current message, and the induction hypothesis gives $w = v$.
- Otherwise, let $Q$ be the quorum of $C(s)$ that chose $v$ with $b_0$. Some processor $a$ is in $S \cap Q$. It accepts $b_0 < b$ in slot $s$, which by Lemma 4 happens before its promise, so case (a) fails and case (b) holds: $w$ is the value of the largest ballot $c$ with $b_0 \le c < b$ accepted in slot $s$ by a processor of $S$ before its promise. If $c = b_0$, Lemma 3 gives $w = v$. If $c > b_0$, the message ACCEPT($c$, $s$, $w$) was sent before that acceptance, so before the current message, and the induction hypothesis gives $w = v$.

Now let $w$ be chosen in $s$ with ballot $b_1$. By the choice of $b_0$, $b_1 \ge b_0$. If $b_1 = b_0$, Lemma 3 gives $w = v$. If $b_1 > b_0$, the acceptances in $b_1$ follow ACCEPT($b_1$, $s$, $w$), and the claim above gives $w = v$. $\square$

**Theorem (decisions are chosen values).** Every decision that line L6 or line L12 stores for slot $s$ is the command chosen in $s$.

*Proof.* Line L6 decides $v$ only after ACCEPTED($b$, $s$) from a quorum of $C(s)$, and each processor sends it only after it accepts $(b, s, v)$ with the unique value of Lemma 3. So $v$ is chosen. Line L12 copies a decision of line L6. By the agreement theorem, all decisions for $s$ are equal. $\square$

**Theorem (forgetting is safe).** After line L9 has run for slot $k$, no chosen command of a slot below $k$ is lost when the auxiliaries of $C(k - 1)$ forget.

*Proof.* Line L9 sends FORGET only after it has sent all decisions below $k$ to the mains of $C(k)$, which keep them on stable storage. A later leader learns the decision of each slot below $k$ from any quorum of $C(k)$ or later configurations, since each such quorum holds a main of the current configuration, and every main has received the decisions. A stale leader that sends PREPARE for a slot below $k$ to an auxiliary that has forgotten it gets a refusal from line L10, so it cannot form a quorum that misses a vote. Mains never forget. So a quorum of the PREPARE either includes a main that reports the decision (case (c) of P2c), or the leader gets no quorum. $\blacksquare$

The window $\alpha = 1$ is what lets Lemma 5 use only earlier slots: the leader starts slot $s$ only after the decision of slot $s - 1$ (line L8). With a larger window $\alpha$, the same proof works with $C(s)$ a function of the slots up to $s - \alpha$.
