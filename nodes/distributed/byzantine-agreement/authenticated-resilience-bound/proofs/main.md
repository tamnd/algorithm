---
title: With signatures, broadcast works for any t < n, and strong consensus works if and only if n > 2t
proves: [statement]
status: full
---

The proof has four parts: broadcast for any $t < n$, weak validity for any $t < n$, strong validity for $n > 2t$, and the impossibility of strong validity for $n \le 2t$. The first part uses the correctness proof of the Dolev-Strong algorithm. The other parts are complete here.

**Statement.** In the synchronous model with $n$ processes, a complete network of reliable links, unforgeable signatures and at most $t$ Byzantine processes:

1. for $0 \le t < n$, Byzantine broadcast and interactive consistency are solvable in $t + 1$ rounds;
2. for $0 \le t < n$, consensus with agreement, weak validity and termination is solvable;
3. for $t \ge 1$ and $n \ge 2$, consensus with agreement, strong validity and termination is solvable if and only if $n > 2t$, and the "only if" part holds for every algorithm in every timing model, with or without signatures.

**Definitions.**

- *Broadcast:* a designated sender $s$ has an input. Every correct process outputs a value (termination). All correct processes output the same value (agreement). If $s$ is correct, that value is its input (validity).
- *Interactive consistency:* every process $p$ has an input $x_p$. Every correct process outputs a vector of $n$ entries (termination). All correct processes output the same vector (agreement). For each correct $q$, entry $q$ of that vector is $x_q$ (validity).
- *Consensus:* every process has an input. Every correct process decides (termination), and all correct processes decide the same value (agreement). *Weak validity:* if no process is faulty and all inputs are $v$, the decision is $v$. *Strong validity:* if all correct processes have input $v$, the decision of every correct process is $v$.

**Part 1 (broadcast and interactive consistency).**

1. The Dolev-Strong algorithm solves broadcast for every $t < n$ in $t + 1$ rounds. Its correctness proof is on the Dolev-Strong page. It uses only that a correct process signs a value it relays, and that no process can produce the signature of a correct process on anything the correct process did not sign. It does not use any bound on $t$ other than $t < n$.
2. For interactive consistency, run $n$ instances of Dolev-Strong in parallel, one with each process $q$ as the sender and $x_q$ as its input. Every signature names the instance it belongs to, so a signature from one instance is not valid in another one. Each instance is then a run of Dolev-Strong with at most $t$ faults.
3. Process $p$ outputs the vector whose entry $q$ is the output of $p$ in instance $q$. By the agreement of each instance, all correct processes have the same entry $q$ for each $q$, so the same vector. By the validity of instance $q$ for a correct $q$, entry $q$ is $x_q$. All instances end after $t + 1$ rounds. $\square$

**Part 2 (weak validity).**

1. Run broadcast with sender $p_0$ and input $x_{p_0}$, and let each correct process decide its output.
2. Termination and agreement are those of broadcast.
3. If no process is faulty and all inputs are $v$, then $p_0$ is correct with input $v$. By the validity of broadcast every process outputs $v$, so it decides $v$. $\square$

**Part 3, "if" (strong validity for $n > 2t$).**

1. Run interactive consistency (Part 1). Each correct process decides the value that occurs in more than $n/2$ entries of its vector, if there is one, and a fixed default value $d$ otherwise.
2. Termination: interactive consistency ends after $t + 1$ rounds.
3. Agreement: all correct processes have the same vector, and the rule in step 1 is a function of the vector.
4. Strong validity: let all correct processes have input $v$. At least $n - t$ processes are correct, and by the validity of interactive consistency their entries are $v$. Since $n > 2t$, $n - t > n/2$. So $v$ occurs in more than $n/2$ entries, and no other value can. Every correct process decides $v$. $\square$

**Part 3, "only if" (no strong validity for $n \le 2t$).**

1. Let $t \ge 1$ and $2 \le n \le 2t$, and assume an algorithm $P$ solves consensus with strong validity for at most $t$ faults. If $P$ is randomized, fix the coins of each process. A failure for one outcome of the coins is a failure of $P$.
2. Split the processes into two nonempty sets $A$ and $B$ with $|A| = \lceil n/2 \rceil \le t$ and $|B| = \lfloor n/2 \rfloor \le t$. Both are nonempty since $n \ge 2$, and $\lceil n/2 \rceil \le t$ since $n \le 2t$.
3. Let $\rho$ be the run in which each process of $A$ has input 0, each process of $B$ has input 1, and every process follows $P$, with the same timing as any fixed run of the model. Each process signs only with its own key.
4. A faulty process may do anything, so it may follow $P$. So $\rho$ is also a run in which exactly the processes of $B$ are faulty. There are $|B| \le t$ of them. In this run the correct processes are those of $A$, and they all have input 0. By termination and strong validity, each process of $A$ decides 0. The decision of a process depends only on what it sees, and it sees the same thing whichever processes are called faulty. So in $\rho$ each process of $A$ decides 0.
5. In the same way, $\rho$ is a run in which exactly the processes of $A$ are faulty, and each process of $B$ decides 1.
6. $\rho$ is also a run in which no process is faulty. By agreement, all processes decide the same value. But by steps 4 and 5 the processes of $A$ decide 0 and those of $B$ decide 1. This is a contradiction. $\blacksquare$

**Remarks.**

- Step 4 of the last part uses no property of messages or timing. So the bound $n > 2t$ holds with any authentication and in every timing model. Signatures cannot help because no process in $\rho$ does anything that a correct process would not do.
- The argument needs a faulty process that behaves exactly like a correct one and is still counted as faulty. With crash failures this is not possible, because a process that never crashes is correct. That is why crash consensus is solvable for any $t < n$.
