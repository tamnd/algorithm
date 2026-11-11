---
title: Byzantine broadcast and consensus need n >= 3t + 1 without signatures
proves: [statement]
status: full
---

This is the scenario (hexagon) proof of Fischer, Lynch and Merritt (1986) for three processes, with the reduction of Lamport, Shostak and Pease (1982) from $n$ processes to three.

**Statement.** Consider the synchronous model with oral messages on a complete network of $n$ processes, with at most $t$ Byzantine processes and a static adversary.

1. If $3 \le n \le 3t$, no algorithm solves Byzantine broadcast.
2. If $t \ge 1$ and $2 \le n \le 3t$, no algorithm solves binary consensus with agreement, strong validity and termination.

Here an algorithm *solves* a problem if every run with at most $t$ faulty processes satisfies its conditions. For a randomized algorithm, this means every run for every outcome of the coins.

**Setup.**

1. In round $r$ each process sends a message on each of its links, then receives the messages sent to it in round $r$. The receiver knows the link, so it knows the sender. A faulty process may send any message on any of its links.
2. The *view* of a process after round $r$ is its input, its coin values and the list of messages it received in rounds $1$ to $r$, each with its sender. The messages that a correct process sends in round $r + 1$, and its decision if it decides after round $r$, are functions of its view after round $r$.
3. *Indistinguishability.* If a correct process has the same view after each round in two runs, it sends the same messages and decides the same value in both.
4. For a randomized algorithm, fix one coin string $c_X$ for each process $X$. Every run below gives process $X$, and every copy of $X$, the coin string $c_X$. A contradiction for one choice of coins shows that the algorithm fails in some run.

**Lemma 1 (the hexagon).** Let $P$ be an algorithm for three processes $A$, $B$, $C$. Place six copies on a ring in the order $A_0, B_0, C_0, A_1, B_1, C_1$, with $C_1$ next to $A_0$. Each copy $X_i$ runs the code of $X$ with input $i$. Each copy has one ring neighbor that is a copy of each other process, and it uses the link to that neighbor as its link to that process. For example, $A_0$ uses $B_0$ as $B$ and $C_1$ as $C$. Run the six copies in lockstep rounds. Call this system $S$. Then for any two adjacent copies $X_i$ and $Y_j$ there is a run $\rho$ of $P$ in which $X$ and $Y$ are correct with inputs $i$ and $j$, the third process $Z$ is faulty, and $X$ and $Y$ have the views of $X_i$ and $Y_j$ in $S$ after every round.

*Proof.* $S$ is well defined, because each copy sends and receives on exactly two links, as a process of $P$ does. Let $Z_k$ be the other neighbor of $X_i$, and let $Z_l$ be the other neighbor of $Y_j$. In $\rho$, the faulty $Z$ sends to $X$ in each round $r$ the message that $Z_k$ sends to $X_i$ in round $r$ of $S$, and to $Y$ the message that $Z_l$ sends to $Y_j$. This is allowed, by step 1 of the setup. Show by induction on $r$ that $X$ and $Y$ have the views of $X_i$ and $Y_j$ after round $r$. For $r = 0$ the views are the inputs and coins, which are the same. Assume the claim after round $r - 1$. By step 3 of the setup, $X$ sends to $Y$ in round $r$ what $X_i$ sends to $Y_j$, and $Y$ sends to $X$ what $Y_j$ sends to $X_i$. $Z$ sends to each what its other neighbor sends in $S$. So both receive in round $r$ the same messages as their copies, and the claim holds after round $r$. $\square$

**Lemma 2 (three processes, consensus).** No algorithm solves consensus for $n = 3$ and $t = 1$.

1. Assume $P$ does. Build $S$ as in Lemma 1.
2. $B_0$ and $C_0$ are adjacent. Take the run $\rho_\alpha$ of Lemma 1 for them: $B$ and $C$ are correct with input 0, and $A$ is faulty. By termination and strong validity, $B$ and $C$ decide 0. By Lemma 1 and step 3 of the setup, $C_0$ decides 0 in $S$.
3. $A_1$ and $B_1$ are adjacent. In the run $\rho_\beta$ for them, $A$ and $B$ are correct with input 1. They decide 1, so $A_1$ decides 1 in $S$.
4. $C_0$ and $A_1$ are adjacent. In the run $\rho_\gamma$ for them, $C$ and $A$ are correct with inputs 0 and 1, and $B$ is faulty. By Lemma 1, $C$ decides what $C_0$ decides, which is 0 by step 2, and $A$ decides what $A_1$ decides, which is 1 by step 3. This breaks agreement in $\rho_\gamma$. So $P$ does not solve consensus. $\square$

**Lemma 3 (three processes, broadcast).** No algorithm solves Byzantine broadcast for $n = 3$ and $t = 1$.

1. Assume $P$ does, with sender $A$. Only the sender has an input, so only $A_0$ and $A_1$ have inputs in $S$: $A_0$ has 0 and $A_1$ has 1.
2. In the run of Lemma 1 for the adjacent $A_0$ and $B_0$, the sender $A$ is correct with input 0, and $C$ is faulty. By validity $B$ outputs 0, so $B_0$ outputs 0.
3. In the run for the adjacent $B_0$ and $C_0$, $B$ and $C$ are correct and the sender $A$ is faulty. By agreement $C$ outputs what $B$ outputs. So $C_0$ outputs what $B_0$ outputs, which is 0 by step 2.
4. In the run for the adjacent $C_0$ and $A_1$, the sender $A$ is correct with input 1, and $B$ is faulty. By validity $C$ outputs 1. But $C$ outputs what $C_0$ outputs, which is 0 by step 3. This is a contradiction. $\square$

**Lemma 4 (from $n$ processes to three).** Let $3 \le n \le 3t$. If an algorithm $Q$ solves broadcast (or consensus) for $n$ processes with $t$ faults, then an algorithm $P$ solves the same problem for 3 processes with 1 fault.

1. Split the processes $1, \ldots, n$ of $Q$ into three groups $G_A$, $G_B$, $G_C$, each of size $\lfloor n/3 \rfloor$ or $\lceil n/3 \rceil$. Each group is nonempty since $n \ge 3$, and has at most $\lceil n/3 \rceil \le t$ members since $n \le 3t$. For broadcast, put the sender of $Q$ in $G_A$.
2. In $P$, process $X$ simulates all members of $G_X$. In round $r$ it computes the round $r$ messages of each simulated member. It delivers a message between two members of $G_X$ itself. It sends all messages from members of $G_X$ to members of $G_Y$ as one message on the link from $X$ to $Y$, with each part labelled by its sender and receiver.
3. When $X$ receives a bundle on the link from $Y$, it uses only parts whose sender is in $G_Y$ and whose receiver is in $G_X$, and it reads a missing or malformed part as a fixed default message. So a faulty $Y$ can only send messages in the name of members of $G_Y$.
4. Inputs. For broadcast, the simulated sender gets the input of $A$. For consensus, each member of $G_X$ gets the input of $X$.
5. A correct $X$ outputs the output of the first member of $G_X$.
6. Fix a run of $P$ in which at most one process, say $Y$, is faulty. The simulated steps form a run of $Q$: the members of the groups of the correct processes follow $Q$ exactly, and the members of $G_Y$ send the messages that the parts of $Y$'s bundles give. This run of $Q$ has at most $|G_Y| \le t$ faulty processes, so $Q$ satisfies agreement, validity and termination in it.
7. Agreement of $P$: two correct processes of $P$ output the outputs of two correct members of $Q$, which are equal.
8. Validity of $P$ for broadcast: if $A$ is correct with input $v$, then the simulated sender is correct with input $v$, so every correct member outputs $v$. For consensus: if all correct processes of $P$ have input $v$, then all correct members have input $v$ by step 4, so every correct member decides $v$ by strong validity.
9. Termination of $P$: every correct member decides in the run of $Q$, and so does every correct process of $P$. $\square$

**Lemma 5 (two processes, consensus).** No algorithm solves consensus for $n = 2$ and $t = 1$.

1. Assume $P$ does. Let $\rho$ be the run in which $A$ has input 0, $B$ has input 1, and both follow $P$.
2. View $\rho$ as a run in which $B$ is faulty and sends exactly what the code of $P$ tells it to send. That is one allowed behavior of a faulty process. In this view the only correct process is $A$, and all correct processes have input 0. By termination and strong validity, $A$ decides 0.
3. In the same way, view $\rho$ as a run with $A$ faulty. Then $B$ decides 1.
4. In $\rho$ both processes are correct and they decide 0 and 1. This breaks agreement. $\square$

**Proof of the statement.** Part 1: if $3 \le n \le 3t$, an algorithm for broadcast would give one for $n = 3$ and $t = 1$ by Lemma 4, which Lemma 3 rules out. Part 2: for $n = 2$ use Lemma 5. For $3 \le n \le 3t$, an algorithm for consensus would give one for $n = 3$ and $t = 1$ by Lemma 4, which Lemma 2 rules out. $\blacksquare$

**Remarks.**

- The proof does not use the number of rounds or the size of messages. So it holds for any number of rounds and any message size.
- The faulty process in each run of Lemma 1 sends to each correct neighbor messages that a correct process would send in some other system. Signatures stop this for broadcast. In $S$, $C_0$ can relay to $B_0$ the value 1 with the signature of $A_1$. In the run of Lemma 3, step 2, the sender $A$ is correct with input 0, so the faulty $C$ cannot produce that signature. See the authenticated resilience bound.
