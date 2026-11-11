---
title: OM(m) satisfies IC1 and IC2 when n > 3m and at most m generals are traitors
proves: [correctness, termination, time.worst]
status: full
---

**Claim.** In the synchronous model with oral messages (assumptions A1, A2 and A3), a complete network of $n$ generals and at most $m$ traitors, if $n > 3m$, then each run of OM(m) satisfies IC1 (all loyal lieutenants obey the same order) and IC2 (if the commander is loyal, every loyal lieutenant obeys its order). Each run ends after $m + 1$ rounds.

This is Theorem 1 of Lamport, Shostak and Pease (1982), with their Lemma 1. The proof follows theirs and fills in the steps.

**Setup.** We reason on the recursive form of the pseudocode. An instance $\text{OM}(m, c, v, G)$ has the commander $c$ and the lieutenants $G$, so it has $|G| + 1$ generals. A traitor may do anything in place of its code. By A1 and A2, a message from a loyal general arrives unchanged, and the receiver knows its sender, so a traitor cannot pose as a loyal general. By A3, a missing message is detected and replaced by RETREAT (line L2), so a traitor that stays silent acts as a traitor that sends RETREAT. The majority function returns $w$ if more than half of its arguments equal $w$.

Say that an instance *satisfies IC2* if, when its commander is loyal with value $v$, every loyal lieutenant of the instance obeys $v$ in it. Say that it *satisfies IC1* if all loyal lieutenants of the instance obey the same value in it.

**Lemma 1.** For all $m \ge 0$ and $k \ge 0$: an instance of OM(m) with more than $2k + m$ generals and at most $k$ traitors satisfies IC2.

*Proof.* By induction on $m$. Assume the commander $c$ is loyal and has value $v$.

*Base, $m = 0$.* By line L1 and A1, each loyal lieutenant $i$ receives $v$ from $c$, so $v_i = v$ in line L2, and $i$ obeys $v$ in line L3.

*Step, $m > 0$.* Assume the lemma for $m - 1$ and all $k$. Let the instance have $N > 2k + m$ generals, so $|G| = N - 1$ lieutenants, at most $k$ of them traitors. By line L1 and A1, each loyal lieutenant $j$ has $v_j = v$ after line L2. In line L4, $j$ is the loyal commander of $\text{OM}(m - 1, j, v, G \setminus \{j\})$. That instance has $N - 1 > 2k + (m - 1)$ generals and at most $k$ traitors. By the induction hypothesis, every loyal general $i \in G \setminus \{j\}$ obeys $v$ in it, so $w_j = v$ at $i$ in line L6.

Fix a loyal lieutenant $i$. In line L8 it takes the majority of $N - 1$ entries $w_j$, one for each $j \in G$. For $j = i$ the entry is $w_i = v_i = v$ by line L7. For each other loyal $j$ the entry is $v$, as shown. So at least $N - 1 - k$ entries equal $v$. Since $N > 2k + m \ge 2k + 1$, we have $N - 1 > 2k$, so $N - 1 - k > (N - 1)/2$. The entries equal to $v$ are a strict majority, and $i$ obeys $v$. $\square$

**Theorem 1.** For all $m \ge 0$: an instance of OM(m) with more than $3m$ generals and at most $m$ traitors satisfies IC1 and IC2.

*Proof.* By induction on $m$.

*Base, $m = 0$.* There are no traitors. By Lemma 1 with $k = 0$, every lieutenant obeys the commander's value, so IC1 and IC2 hold.

*Step, $m > 0$.* Assume the theorem for $m - 1$. Let the instance have $N > 3m$ generals and at most $m$ traitors.

*Case 1: the commander is loyal.* Take $k = m$ in Lemma 1. Then $N > 3m = 2k + m$, so IC2 holds. IC1 follows from IC2, because every loyal lieutenant obeys the same value $v$.

*Case 2: the commander is a traitor.* IC2 holds because its hypothesis is false. For IC1, at most $m - 1$ of the lieutenants are traitors. For each $j \in G$, the instance $I_j = \text{OM}(m - 1, j, v_j, G \setminus \{j\})$ of line L4 has $N - 1$ generals and at most $m - 1$ traitors. Since $N \ge 3m + 1$, we have $N - 1 \ge 3m > 3(m - 1)$. By the induction hypothesis, each $I_j$ satisfies IC1 and IC2.

Fix $j \in G$. We show that all loyal lieutenants $i \in G$ hold the same entry $w_j$ in line L8.

- If $j$ is loyal, then $j$ itself holds $w_j = v_j$ by line L7. Every other loyal $i$ holds $w_j = v_j$ by IC2 of $I_j$, whose commander $j$ is loyal with value $v_j$.
- If $j$ is a traitor, then $j$ is not a loyal lieutenant, and every loyal $i \ne j$ holds the same $w_j$ by IC1 of $I_j$.

So every loyal lieutenant applies the majority function to the same list of $N - 1$ entries, and all of them obey the same value. This is IC1. $\square$

The top instance has $n$ generals, so Theorem 1 with $N = n$ gives the claim.

**Termination and rounds.** Let $R(m)$ be the number of rounds of an instance of OM(m). $R(0) = 1$, because line L1 is one round and line L3 needs no message. For $m > 0$, line L1 takes one round, and the instances of line L4 run at the same time, so $R(m) = 1 + R(m - 1)$. Thus $R(m) = m + 1$. In the round form, round $r$ carries the messages on paths of length $r$, and a lieutenant drops a path of length more than $m + 1$, so the run ends after round $m + 1$ whatever the traitors do. The evaluation of lines L6 to L8 is a finite computation over the stored paths, so each loyal lieutenant obeys a value. $\blacksquare$

**Why the bound is tight.** The proof of Case 2 uses $N - 1 > 3(m - 1)$, and the proof of Case 1 uses $N > 3m$. For $N = 3m$, the scenario argument of Fischer, Lynch and Merritt (see the [Byzantine resilience bound](/byzantine-resilience-bound/)) shows that every algorithm, so also OM(m), fails in some run.
