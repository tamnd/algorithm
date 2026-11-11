---
title: Synchronous Byzantine broadcast and consensus with t faults need t + 1 rounds
proves: [statement]
status: full
---

The proof reduces the Byzantine bound to the crash bound. It uses the theorem of the crash round lower bound page, in the form with weak validity that step 3 justifies. That proof is not repeated here.

**Statement.** Let $1 \le t \le n - 2$. Let $A$ be a deterministic synchronous algorithm, in the oral or the signed messages model, that solves Byzantine broadcast, or binary consensus with weak or strong validity, for at most $t$ Byzantine faults. Then $A$ has a run with at most $t$ faulty processes, which all fail by crashing, in which some correct process has not decided at the end of round $t$.

**Definitions.** In a *crash run*, a faulty process follows $A$ until some round $r$, sends its round $r$ messages to a subset of the processes of the adversary's choice, and sends nothing after round $r$. A process is *correct* if it is not faulty. *Weak validity:* if no process is faulty and all inputs are $v$, every decision is $v$. *Strong validity:* if all correct processes have input $v$, every correct decision is $v$.

**Step 1 (crash runs are Byzantine runs).**

1. A Byzantine process may send any messages in any round. The behavior of a crashed process is one such behavior.
2. In the signed messages model, a crashed process signs only what $A$ tells it to sign. So it uses only its own key, and every signature it sends is one that $A$ makes. No forgery is needed.
3. So every crash run with at most $t$ crashed processes is a run of $A$ with at most $t$ Byzantine processes, and in it $A$ satisfies agreement, validity and termination. The crashed processes are the faulty ones, and the others are correct, in both readings.

**Step 2 (one problem is enough).**

1. If $A$ solves consensus with strong validity, it solves consensus with weak validity: when no process is faulty and all inputs are $v$, all correct processes have input $v$, so every decision is $v$.
2. If $A$ solves broadcast with sender $p_0$, define $A'$ for consensus: process $p_0$ runs $A$ as the sender with its own input as the value, all processes run $A$, and each decides the output of $A$. $A'$ uses the same rounds as $A$, and a process decides in $A'$ in the round in which it outputs in $A$.
3. $A'$ satisfies termination and agreement because $A$ does. If no process is faulty and all inputs are $v$, then $p_0$ is a correct sender with value $v$, so by the validity of broadcast every output is $v$. So $A'$ satisfies weak validity.
4. So in all three cases there is a deterministic algorithm $B$ for binary consensus with agreement, weak validity and termination, in which each process decides in the same round as in $A$.

**Step 3 (the crash bound with weak validity).**

1. Restrict $B$ to crash runs with at most $t$ crashes. By Step 1, $B$ satisfies agreement and termination in these runs, and weak validity in its failure-free runs.
2. The crash round lower bound page proves: if $1 \le f \le n - 2$ and an algorithm satisfies agreement, termination and unanimity validity (if all inputs are $v$, every decision is $v$) in every crash run with at most $f$ crashes, then it has a crash run with at most $f$ crashes in which a correct process is undecided after round $f$.
3. That proof uses validity in exactly one place: step 1 of its Lemma 1, which says that $I_0$ is 0-valent and $I_n$ is 1-valent, where $I_j$ gives input 1 to $p_1, \ldots, p_j$ and input 0 to the others. Step 2 of Lemma 1 uses this fact only under the assumption that no $I_j$ is bivalent.
4. Under that assumption $I_0$ is univalent, so every extension of $I_0$ has the same decision value, and one extension fixes it. Take the failure-free run from $I_0$. All inputs are 0, so weak validity gives the decision 0, and $I_0$ is 0-valent. In the same way $I_n$ is 1-valent. So Lemma 1 holds with weak validity.
5. Lemmas 2 and 3 of that proof and its final step use only agreement, termination and the indistinguishability of runs. So the whole proof holds with weak validity.
6. So, with $f = t$, the crash proof gives a crash run of $B$ with at most $t$ crashes in which some correct process is undecided after round $t$.

**Step 4 (back to $A$).** A process decides in $B$ in the same round as in $A$, by Step 2. By Step 1, the run from Step 3 is a run of $A$ with at most $t$ Byzantine faults, all of which are crashes. In it, some correct process has not decided at the end of round $t$. $\blacksquare$

**Remarks.**

- The proof uses determinism through the crash bound, which needs it. Randomized algorithms can beat $t + 1$ rounds in expectation.
- The proof gives the bound for every message format, since crash runs use only the messages of $A$. This is the sense of the remark of Dolev and Strong that the bound holds no matter what message types are allowed.
