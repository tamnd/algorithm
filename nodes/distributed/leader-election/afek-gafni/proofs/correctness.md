---
title: The synchronous capture algorithm elects the largest initiator with at most 4n⌈log₂ n⌉ + n − 1 messages in 4⌈log₂ n⌉ + 1 rounds
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run AFEK-GAFNI on a synchronous complete network of $n \ge 2$ processes with distinct identifiers, where a nonempty set of initiators start in phase 0. Let $m$ be the initiator with the largest identifier and $L = \lceil \log_2 n \rceil$. Then (a) $m$ is alive at the end of every phase, and it is elected at the end of phase $L - 1$; (b) no other process is elected; (c) at the end of each phase $i$ with $2^{i+1} \le n$, at most $n / 2^{i+1}$ candidates are alive; (d) the run sends at most $4nL$ messages before the announcement and $n - 1$ announcements, and it takes exactly $4L + 1$ rounds. For $n = 1$ the only process is elected at once if it starts.

This proof covers the simplified synchronous form on the page.

**Facts.** (F1) A process that is not alive never becomes alive again. (F2) In phase $i$, a candidate that has been alive since phase 0 has tried $2^0 + \cdots + 2^{i-1} = 2^i - 1$ links before the phase, and tries $\min(2^i, n - 2^i)$ links in it. (F3) Each request gets exactly one answer in round 4: ACC to the chosen request of a process if it was accepted, and REJ to every other request. (F4) The owner of a process changes only in round 4 of a phase, at most once per phase, to the chosen candidate.

**Lemma 1 (an alive candidate keeps what it owns).** Let $c$ be alive at the end of phase $i$. Then at the end of phase $i$, $\mathrm{owner}(c) = c$, and $\mathrm{owner}(y) = c$ for every process $y$ whose request from $c$ got ACC in phases $0, \ldots, i$.

*Proof.* By F1, $c$ was alive throughout phases $0, \ldots, i$. The owner of $c$'s own process changes only if, in round 2 at $c$, a request is accepted while $\mathrm{owner}(c) = c$. Since $c$ is alive, this needs $u > \mathrm{id}(c)$ and sets $\mathit{alive}_c \leftarrow \mathit{false}$ (L2), a contradiction. Now let $y$ have accepted $c$ in phase $j \le i$, so $\mathrm{owner}(y) = c$ after phase $j$. A later change in a phase $j' \le i$ needs, by L3 and L5, a YES from the owner $c$ in round 3. Since $c$ is alive, the YES needs $u > \mathrm{id}(c)$ and sets $\mathit{alive}_c \leftarrow \mathit{false}$ (L4), a contradiction. $\square$

**Lemma 2 (domains are disjoint).** For a candidate $c$ alive at the end of phase $i$, let $D_c$ be $c$ together with the processes that accepted $c$ in phases $0, \ldots, i$. Then $|D_c| = \min(n, 2^{i+1})$, and $D_c \cap D_d = \emptyset$ for any other candidate $d$ alive at the end of phase $i$.

*Proof.* By L6, all requests of $c$ got ACC, and by F2 it sent $2^{i+1} - 1$ requests, or $n - 1$ if that is smaller, on distinct links. So $|D_c| = \min(n, 2^{i+1})$. By Lemma 1, every $y \in D_c$ has owner $c$ at the end of phase $i$, and every $y \in D_d$ has owner $d$. So a common element would give $c = d$. $\square$

**Part (c).** If $2^{i+1} \le n$, the alive candidates at the end of phase $i$ have disjoint sets of $2^{i+1}$ processes each, so there are at most $n / 2^{i+1}$ of them.

**Part (a).** Induction on the phase. Assume $m$ is alive at the start of phase $i$. Every request in the phase comes from a live candidate, and every live candidate is an initiator, so $\mathrm{id}(m)$ is the largest request at every process that $m$ asks, and it is chosen in round 2. If the process owns itself, it accepts: either it is not alive, or it is alive with a smaller identifier than $m$. If not, its owner $o \ne m$ (F4 and Lemma 1, since $m$ never asks a process twice and never asks itself) answers YES in round 3: either it is dead, or it is alive with a smaller identifier. So all requests of $m$ get ACC (F3). The other ways to die are L2 at $m$'s own process and L4 at $m$, and both need a request with $u > \mathrm{id}(m)$, which no candidate has. So $m$ is alive at the end of phase $i$. By F2, after phase $i$ it has tried $2^{i+1} - 1$ links, or all of them, and this reaches $n - 1$ first at $i = L - 1$, since $2^{L} \ge n > 2^{L-1}$. Then L7 elects it.

**Part (b).** Suppose a candidate $c \ne m$ is elected. Then $c$ is alive and all $n - 1$ of its requests got ACC, including the one to $m$'s process. By part (a), $m$ is alive in that phase, and by Lemma 1, applied to $m$ at the end of the previous phase, or because no one has asked yet, $m$ owns itself. So round 2 at $m$ decides locally, and since $m$ is alive and $\mathrm{id}(c) < \mathrm{id}(m)$, it does not accept $c$, a contradiction.

**Termination.** By parts (a) and (b), the run ends after phase $L - 1$ with $m$ elected, plus one round for the announcements.

**Part (d), messages.** In phase 0 there are at most $n$ requests, one per initiator. In phase $i \ge 1$, the live candidates are those alive at the end of phase $i - 1$, at most $n / 2^i$ by part (c) since $2^i \le 2^{L-1} < n$, and each sends at most $2^i$ requests, so at most $n$ in all. Each request causes at most one query (only the chosen request of a process that does not own itself is forwarded, so there is at most one query per process, hence at most one per request), at most one answer to a query, and exactly one ACC or REJ (F3). So each phase sends at most $4n$ messages, and the $L$ phases at most $4nL$. The announcement adds $n - 1$.

**Part (d), rounds.** Each phase has 4 rounds, there are exactly $L$ phases by parts (a) and (b), and the announcement takes one more round: $4L + 1$. $\blacksquare$
