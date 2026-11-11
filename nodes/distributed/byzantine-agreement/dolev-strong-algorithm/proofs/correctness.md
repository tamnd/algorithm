---
title: Dolev-Strong solves Byzantine broadcast with signatures for any t < n in t + 1 rounds
proves: [correctness, termination, time.worst]
status: full
---

**Claim.** In the synchronous model with $n$ processes on a complete network, unforgeable signatures, and a static adversary that controls at most $t < n$ processes, each run of DOLEV-STRONG has these properties. (Agreement) All correct processes output the same value. (Validity) If the sender is correct with input $b$, every correct process outputs $b$. (Termination) Every correct process outputs at the end of round $t + 1$. Also, the correct processes send at most $(n - 1) + 2(n - 1)(n - 2)$ messages.

**Setup.** A message $v{:}0{:}j_1{:}\cdots{:}j_{r-1}$ is *accepted* by $i$ in round $r$ if it passes lines L4 and L5. Then $i$ *extracts* $v$ (line L6). For a correct $i$, let $F_i$ be the set of the first $\min(2, |\text{EXTR}_i|)$ values that $i$ extracts, in order of extraction. By unforgeability, a valid signature of a correct process $k$ on a content exists only if $k$ made it. A correct process $k \ne 0$ signs only in line L8, so:

**Fact 1.** If a correct process $k \ne 0$ is a signer on a valid chain for $v$, then $k$ extracted $v$ in some round $r \le t$ with $v \in F_k$, and in round $r + 1$ it sent $v$ with $r + 1$ distinct signatures to every process not on the chain it accepted.

The sender, if correct, has $\text{EXTR}_0 = \{b\}$ from line L1 and signs only $b$.

**Lemma 2.** Let $i$ be correct and $v \in F_i$. Then every correct process $j$ has $v \in \text{EXTR}_j$ at the end of round $t + 1$.

*Proof.* If $i = 0$ is the correct sender, then $v = b$, and in round 1 every correct $j$ receives $b{:}0$, which has one valid signature, so $j$ extracts $b$ unless it already has it. Now let $i \ne 0$ and let $i$ extract $v$ in round $r$ from the chain $C = 0, j_1, \ldots, j_{r-1}$.

*Case $r \le t$.* Since $v \in F_i$, line L7 holds, and in round $r + 1 \le t + 1$, $i$ sends $v$ with the chain $C, i$ to every process not on $C$ and not $i$. The names on $C$ are distinct, and $i$ is not on $C$, since otherwise $i$ would have signed $v$ before and $v$ would already be in $\text{EXTR}_i$. So the new chain has $r + 1$ distinct names and valid signatures. Let $j$ be a correct process. If $j$ is on $C$, then $j = 0$ is the sender (and $v = b$ is its value) or $j$ signed $v$, and by Fact 1 $v \in \text{EXTR}_j$. If $j = i$, the claim holds. Otherwise $j$ receives the new chain in round $r + 1$ and accepts it or already has $v$.

*Case $r = t + 1$.* The chain $C$ has $t + 1$ distinct names. At most $t$ processes are faulty, so some name $k$ on $C$ is correct. If $k = 0$, the sender is correct and $v = b$, handled above. If $k \ne 0$, Fact 1 gives a round $r' \le t$ in which $k$ extracted $v$ with $v \in F_k$. The first case, applied to $k$ and $r'$, shows that every correct process has $v$ at the end of round $r' + 1 \le t + 1$. $\square$

**Agreement.** Let $i$ and $j$ be correct. We show that $i$ and $j$ output the same value.

- If $|\text{EXTR}_i| \ge 2$ and $|\text{EXTR}_j| \ge 2$, both output $\bot$.
- If $\text{EXTR}_i = \{v\}$, then $F_i = \{v\}$ and by Lemma 2, $v \in \text{EXTR}_j$. If $\text{EXTR}_j$ had a second value, $F_j$ would hold two distinct values, and by Lemma 2 both would be in $\text{EXTR}_i$, which has one value. So $\text{EXTR}_j = \{v\}$ and both output $v$.
- The case $\text{EXTR}_j = \{v\}$ is the same with $i$ and $j$ swapped.
- $\text{EXTR}_i$ is never empty at the end: if $\text{EXTR}_j \ne \emptyset$ for some correct $j$, Lemma 2 applied to the first value of $j$ puts it into $\text{EXTR}_i$. If all correct sets are empty, all correct processes output $\bot$.

So all correct processes output the same value. $\square$

**Validity.** Let the sender be correct with input $b$. It signs only $b$, so every accepted chain carries $b$, and $\text{EXTR}_j \subseteq \{b\}$ for every correct $j$. In round 1, every correct $j \ne 0$ receives $b{:}0$ and extracts $b$. So $\text{EXTR}_j = \{b\}$ and $j$ outputs $b$. The sender outputs $b$ by line L1. $\square$

**Termination.** The loop of line L2 has $t + 1$ rounds, each round ends in the synchronous model, and line L10 always outputs a value. $\square$

**Messages.** The correct sender sends $n - 1$ messages in round 1 and never relays, because every chain that it could accept contains the name 0 and carries its own value, which is already extracted. A correct process $i \ne 0$ sends messages only in line L9, at most once for each of the at most two values for which line L7 holds, and each time to at most $n - 2$ processes (not 0 and not $i$). With at most $n - 1$ correct non-senders, the total is at most $(n - 1) + 2(n - 1)(n - 2)$. $\blacksquare$

**Where the hypotheses are used.** Unforgeability is used in Fact 1 and in validity. The bound of $t$ faulty processes is used only in the case $r = t + 1$ of Lemma 2, together with the distinct names of line L4. The number $t + 1$ of rounds is used in the same place: with only $t$ rounds, a value extracted in round $t$ cannot be relayed, and the example on the page shows that agreement then fails.
