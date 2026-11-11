---
title: SM(m) satisfies IC1 and IC2 with at most m traitors, for any n
proves: [correctness, termination, time.worst]
status: full
---

**Claim.** In the synchronous model with signed messages (assumptions A1 to A4), a complete network of $n$ generals and at most $m$ traitors, each run of SM(m) in the round form of the pseudocode satisfies IC1 and IC2, and each loyal lieutenant obeys an order at the end of round $m + 1$. There is no condition on $n$. (The problem is vacuous for $n < m + 2$.)

This is Theorem 2 of Lamport, Shostak and Pease (1982). Their proof is given for the form of the algorithm without rounds. The proof below follows it on the round form, and makes explicit the use of distinct signers in the last case.

**Setup.** A message $v{:}0{:}j_1{:}\cdots{:}j_k$ is *accepted* by lieutenant $i$ in round $r$ if it passes lines L5 and L6: $k = r - 1$, the names $0, j_1, \ldots, j_k$ are distinct and do not include $i$, and all signatures are valid. Then $i$ adds $v$ to $V_i$ if it is new (line L7). By A4 (a), a valid signature of a loyal general $g$ on a content exists only if $g$ made it. A loyal commander signs only its order $v$ (line L1). A loyal lieutenant $g$ signs a content only in line L9, and only for an order that it has just added to $V_g$ with a chain of $k < m$ lieutenant signatures.

**Fact 1.** If a loyal lieutenant $g$ appears as a signer on a valid chain for $v$, then $v \in V_g$. Moreover, $g$ added $v$ in round $l$ from a chain with $l - 1 < m$ lieutenant signatures, and in round $l + 1$ it sent $v$, with its signature added, to every lieutenant not on that chain.

*Proof.* By A4 (a), the signature of $g$ on the prefix of the chain up to $g$ was made by $g$, and only line L9 makes it. Lines L7 to L10 show the rest. Round $l + 1 \le m + 1$ exists because $l - 1 < m$. By A1, every message sent arrives. $\square$

**IC2.** Let the commander be loyal with order $v$. In round 1, each loyal lieutenant $i$ receives $v{:}0$ by A1. It has $k = 0$, a valid signature, and distinct names, so $i$ accepts it and $v \in V_i$. Every accepted message has a valid commander signature on its order, and by A4 (a) the loyal commander signed only $v$, so every order in $V_i$ is $v$. Hence $V_i = \{v\}$, and $i$ obeys choice($\{v\}$) $= v$. $\square$

**IC1.** If the commander is loyal, all loyal lieutenants obey $v$ by IC2. So assume the commander is a traitor. Then at most $m - 1$ lieutenants are traitors. Choice is a function of the set only, so it is enough to prove:

*For loyal lieutenants $i \ne j$: if $v \in V_i$ at the end, then $v \in V_j$ at the end.*

Let $i$ add $v$ in round $r$ from the accepted message $v{:}0{:}j_1{:}\cdots{:}j_k$ with $k = r - 1$.

- *Case A: $j$ is one of $j_1, \ldots, j_k$.* By Fact 1, $v \in V_j$.
- *Case B: $j$ is not a signer and $k < m$.* In line L10, $i$ queues $v{:}0{:}j_1{:}\cdots{:}j_k{:}i$ for every lieutenant other than $i, j_1, \ldots, j_k$, so also for $j$, and sends it in round $r + 1 \le m + 1$ (line L3). By A1 it arrives in round $r + 1$. It has $k + 1 = r$ lieutenant signatures, distinct names (since $i$ was not on the chain by line L5), $j$ is not among them, and all signatures are valid (the earlier ones were valid, and $i$ signed the new content). So $j$ accepts it, and $v \in V_j$ after round $r + 1$.
- *Case C: $j$ is not a signer and $k = m$.* The names $j_1, \ldots, j_m$ are $m$ distinct lieutenants by line L5. At most $m - 1$ lieutenants are traitors, so some $j_l$ is loyal. By Fact 1, $j_l$ added $v$ in round $l$ and in round $l + 1$ sent $v$ to every lieutenant not on its chain $0, j_1, \ldots, j_{l-1}$. The lieutenant $j$ is not on that chain, since it is not a signer of the longer chain, and $j \ne j_l$. So $j$ receives the message in round $l + 1$. It has $l$ distinct lieutenant names, none equal to $j$, and valid signatures, so $j$ accepts it and $v \in V_j$.

A chain with $k > m$ cannot be accepted, because it would arrive in round $k + 1 > m + 1$. So the three cases are complete, and $V_i = V_j$ for all loyal $i, j$. They obey the same order. $\square$

Case C is the only place where the bound of $m$ traitors is used, and it needs the $m$ signers to be distinct. Without the check of distinct names in line L5, a chain $v{:}0{:}g{:}g$ with one traitor $g$ could reach a loyal lieutenant in round $m + 1$ with no loyal signer, and the case would fail.

**Termination and rounds.** The loop of line L2 has $m + 1$ rounds, each round ends in the synchronous model, and line L11 then gives an order, since choice is defined on every finite set. Messages sent by traitors do not change the number of rounds. $\blacksquare$
