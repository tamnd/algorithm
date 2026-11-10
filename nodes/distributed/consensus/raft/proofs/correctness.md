---
title: Raft keeps election safety, log matching, leader completeness and state machine safety
proves: [correctness]
status: full
---

We use the pseudocode of the page, lines L1 to L31. The model is asynchronous with crash-recovery failures. Messages can be lost, duplicated and reordered, but not corrupted. A server writes current_term, voted_for and its log to stable storage before it sends a message, so a crash loses only the other variables. We prove four safety properties. None of them needs a timing assumption, and none needs a bound on the number of crashes. Liveness is not claimed here.

We write $\mathit{log}_s[i]$ for the entry at index $i$ of server $s$. An entry is a pair $(t, c)$ of a term and a command. Index 0 holds a sentinel of term 0 on every server.

**Lemma 1 (terms grow).** The value current_term of a server never decreases. A message of kind RequestVote or AppendEntries with term $t$ is sent by a server whose current_term is $t$ at that moment.

*Proof.* Line L1 adds 1. Line L31 runs only when the new term is larger (lines L4, L9, L15, L24). No other line writes current_term, and the value is on stable storage. Each message carries the current_term of its sender at the time of sending. $\square$

**Lemma 2 (election safety).** For each term $T$, at most one server becomes leader in term $T$.

*Proof.* Inside one term a server sets voted_for at most once to a value other than nil. When a server enters term $T$ by line L1, it sets voted_for to itself. When it enters term $T$ by line L31, it sets voted_for to nil, and then line L6 grants a vote only if voted_for is nil or the same candidate, and line L7 records it. The value is on stable storage, so a restart does not reset it. A grant is sent only when the voter's term equals the request's term $T$ (line L6), and the reply carries $T$. Line L10 counts a grant only if its term is $T$, and it counts each sender once, because votes is a set. So a leader of term $T$ (line L11) has grants of term $T$ from a majority of the $n$ servers. Two leaders of term $T$ need two majorities, and two majorities share a server, which then granted its one vote of term $T$ to two candidates. That is not possible. A server also cannot lead term $T$ twice: after a restart its votes set is empty, and it can become a candidate only through line L1, which moves it to a higher term. $\square$

**Lemma 3 (a leader only appends).** While a server is leader of term $T$, its log changes only by line L12, which appends at the end.

*Proof.* Lines L20 and L21 run only in ON-APPEND-ENTRIES. A message there with a term below $T$ stops at line L16. A message with a term above $T$ first makes the server a follower by line L15. A message with term exactly $T$ is an AppendEntries of term $T$, and by Lemma 1 only a leader of term $T$ sends it. The leader does not send to itself, and by Lemma 2 no other server leads term $T$. $\square$

**Lemma 4 (one entry for each index and term).** For each pair $(i, T)$, at most one entry of term $T$ is ever created at index $i$, and each entry of term $T$ in any log is a copy of it.

*Proof.* Entries are created only by line L12, with the term of the leader. Only one server leads term $T$ (Lemma 2), and it leads it only once. During its leadership its log only grows (Lemma 3), so it creates its entries of term $T$ at distinct indexes. Lines L20 and L21 only copy entries that a message carries, and a message only carries entries that some log holds. $\square$

**Lemma 5 (log matching).** Let $\mathcal H$ be the set of all sequences that occur in the run: the log of each server at each moment, and for each AppendEntries message $m$ the sequence $L_m$, which is the log of its sender at the time of sending, cut after index $\mathit{prev}+|\mathit{entries}|$. For any $X, Y \in \mathcal H$ and any index $i$: if $X[i]$ and $Y[i]$ have the same term, then $X[0 \ldots i] = Y[0 \ldots i]$.

*Proof.* By induction on the steps of the run. At the start every log is the sentinel alone, and the claim holds. Assume it holds for all sequences of $\mathcal H$ before a step. We look at each step that adds a sequence.

1. Line L12 appends $(T, c)$ at index $i$ to a log $A$. By Lemma 4 no sequence of $\mathcal H$ holds an entry of term $T$ at index $i$. So a pair of the new log with another sequence agrees in term only at indexes below $i$, where the new log equals $A$, and the claim follows from the claim for $A$.
2. Line L14 adds $L_m$, a prefix of a log in $\mathcal H$. If $X$ is a prefix of $A$, then a common term of $X$ and $Y$ at index $i$ is also a common term of $A$ and $Y$, so $Y[0 \ldots i] = A[0 \ldots i] = X[0 \ldots i]$.
3. A follower with log $F$ handles an AppendEntries $m$ and passes the test of line L18, so $F[p]$ and $L_m[p]$ have the same term, where $p$ is prevIndex. By the hypothesis, $F[0 \ldots p] = L_m[0 \ldots p]$. Let $q = p + |\mathit{entries}|$. If line L20 finds no conflict, then each $F[i]$ with $p < i \le \min(q, |F|-1)$ has the term of $L_m[i]$. If $F$ is at least as long as $q + 1$, the hypothesis at index $q$ gives $F[0 \ldots q] = L_m$, and the log does not change. If $F$ is shorter, line L21 appends the rest, and the new log is $L_m$. If line L20 finds a first conflict at index $i > p$, then $F[0 \ldots i-1] = L_m[0 \ldots i-1]$ by the hypothesis at index $i-1$, the suffix is deleted, line L21 appends the rest, and the new log is again $L_m$. In each case the new log is already in $\mathcal H$ or is $F$ itself.

Crashes, restarts, losses and duplicates add no new sequence. $\square$

**Lemma 6 (terms in a log).** In each log, the terms do not decrease along the indexes, and each term is at most the current_term of the server.

*Proof.* Line L12 appends an entry with the current term, and by induction the earlier entries have terms at most that. Lines L20 and L21 make the log equal to $L_m$ or leave it as it is (proof of Lemma 5). The sequence $L_m$ has the property, and its terms are at most $m.\mathit{term}$, which is the current_term of the receiver after line L15. Terms only grow (Lemma 1). $\square$

We say that the leader of term $T$ **commits** index $N$ when line L29 sets commit_index to $N$. Then $\mathit{log}[N]$ has term $T$, by the test of line L29. We say that the entry $x$ at an index $i \le N$ of the leader's log is committed in term $T$.

**Lemma 7 (a commit has a majority).** If the leader of term $T$ commits index $N$, then a majority of servers stored the leader's entry $e = \mathit{log}[N]$ at a moment when their current_term was $T$.

*Proof.* The leader counts $j$ when match_index$[j] \ge N$. For $j$ other than the leader, line L26 set this from a success reply of term $T$ (line L25) to an AppendEntries $m$ of term $T$, with $q = p + |\mathit{entries}| \ge N$. When $j$ sent the success reply, its term was $T$, and by step 3 of Lemma 5 its log began with $L_m$. The sequence $L_m$ is a prefix of the leader's log at the time of sending, and the leader's log only grows (Lemma 3), so $L_m[N] = e$. The leader itself counts with its own last index, and it holds $e$ in term $T$. $\square$

**Theorem 1 (leader completeness).** If an entry $x$ at index $i$ is committed in term $T$, then the log of the leader of each term $U > T$ holds $x$ at index $i$ when it becomes leader, and during all of its leadership.

*Proof.* By Lemma 3 it is enough to show the claim at the moment of election. Let the leader of $T$ commit index $N \ge i$, with $e = \mathit{log}[N]$ of term $T$. If a later leader holds $e$ at $N$, then by Lemma 5 it also holds the leader's entry $x$ at $i$. So we prove the claim for $e$ and $N$.

Assume that the claim fails, and let $U$ be the smallest term above $T$ whose leader $\ell$ does not hold $e$ at $N$ when it is elected. By Lemma 7 a majority stored $e$ in term $T$. The leader $\ell$ got grants of term $U$ from a majority. The two majorities share a server $v$, the voter.

*Step 1: $v$ stored $e$ before it voted for $\ell$.* It stored $e$ when its term was $T$, and it voted when its term was $U > T$. Terms grow (Lemma 1).

*Step 2: $v$ still held $e$ at $N$ when it voted.* Between the two moments, the term of $v$ was between $T$ and $U$, so line L16 rejected every AppendEntries of a term below $T$. Take a message $m$ of a term $t$ with $T \le t < U$ that $v$ handled. Its sender is the leader of $t$. If $t = T$, that leader holds $e$ at $N$ since it created $e$. If $t > T$, it holds $e$ at $N$ by the choice of $U$. In both cases it held $e$ at $N$ when it sent $m$ (Lemma 3), so $L_m$ agrees with that log. Line L20 deletes from index $i'$ only if $L_m[i']$ and $\mathit{log}_v[i']$ have different terms. If $i' \le N$, then Lemma 5 for $\mathit{log}_v$ and the sender's log at index $N$ gives equal prefixes up to $N$, so $L_m[i'] = \mathit{log}_v[i']$ and there is no conflict. So $e$ stays.

*Step 3: the vote gives a contradiction.* Line L5 held when $v$ granted. Let $t_v$ be the last term of $v$, and $t_\ell$ the last term of $\ell$. By Lemma 6, $t_v \ge T$, because $v$ holds $e$ of term $T$.

- Case $t_\ell = t_v$ and $\mathit{lastIndex}_\ell \ge \mathit{lastIndex}_v$. Let $\Lambda$ be the log of the leader of term $t_v$ at the end of its leadership. By Lemma 4 both last entries are entries of $\Lambda$. Lemma 5 for $\mathit{log}_\ell$ and $\Lambda$ at $\mathit{lastIndex}_\ell$ gives $\mathit{log}_\ell[\mathit{lastIndex}_v] = \Lambda[\mathit{lastIndex}_v] = \mathit{log}_v[\mathit{lastIndex}_v]$. Then Lemma 5 for $\mathit{log}_\ell$ and $\mathit{log}_v$ gives equal prefixes up to $\mathit{lastIndex}_v \ge N$, so $\ell$ holds $e$ at $N$.
- Case $t_\ell > t_v \ge T$. When $\ell$ asks for votes in term $U$, its entries have terms below $U$: entries of term $U$ are made only by the leader of $U$ after its election, and by Lemma 6 no entry has a term above $U$. So $T < t_\ell < U$. By the choice of $U$, the leader of $t_\ell$ held $e$ at $N$ when it was elected. It made its entries of term $t_\ell$ after that, at indexes above its length at election, so above $N$. Let $\Lambda'$ be its log at the end of its leadership. Then the last entry of $\ell$ is an entry of $\Lambda'$ at an index above $N$, and Lemma 5 gives $\mathit{log}_\ell[N] = \Lambda'[N] = e$.

In both cases $\ell$ holds $e$ at $N$, which contradicts the choice of $U$. $\blacksquare$

**Why line L29 needs the term test.** Step 3 uses $t_v \ge T$, where $T$ is the term of the commit. That holds because the committed entry $e$ has term $T$. If a leader of term $T$ commits an entry of an older term $t < T$ by counting replicas, a voter's last term can be $t$, and a candidate whose last term is between $t$ and $T$ wins. This is the run of Figure 8 on the page.

**Theorem 2 (state machine safety).** If a server applies the entry $x$ at index $i$, then no server ever applies another entry at index $i$.

*Proof.* We first show this invariant (C): for each server $s$ and each $i \le \mathit{commit\_index}_s$, the entry $\mathit{log}_s[i]$ is committed in some term $T_0 \le \mathit{current\_term}_s$.

- After a start or a restart, commit_index is 0, and (C) holds.
- Line L29 in term $T$ commits all indexes up to $N$ in term $T$, the current term.
- Line L22 sets commit_index to at most $\min(\mathit{leaderCommit}, q)$. Up to $q$ the follower's log equals $L_m$, a prefix of the sender's log at the time of sending, and leaderCommit was the sender's commit_index then. By (C) for the sender, each entry up to leaderCommit is committed in a term at most the sender's term, which is $m.\mathit{term}$, the follower's current term.
- A deletion at line L20 at an index $i' \le \mathit{commit\_index}_s$ would change a committed entry. Let $x = \mathit{log}_s[i']$ be committed in $T_0 \le \mathit{current\_term}_s \le t$, where $t$ is the term of the message. The sender is the leader of $t$, and it holds $x$ at $i'$: by Theorem 1 if $t > T_0$, and because the leader of $T_0$ only appends if $t = T_0$. So $L_m[i'] = x$, and there is no conflict. Hence deletions never touch indexes up to commit_index, and (C) is kept.

A server applies index $i$ only when $i \le$ commit_index (line L30). So if two servers apply $x$ and $y$ at index $i$, then $x$ is committed in a term $T_0$ and $y$ in a term $T_1$, say $T_0 \le T_1$. If $T_0 < T_1$, the leader of $T_1$ holds $x$ at $i$ by Theorem 1, and $y$ is its entry at $i$, so $x = y$. If $T_0 = T_1$, both are entries of the one leader of that term at index $i$, and that log only grows, so $x = y$. $\blacksquare$

**Theorem 3 (the replicas agree).** Every server applies the same sequence of commands, in the same order. A server that has applied $k$ commands has applied the first $k$ commands of the sequence of any other server.

*Proof.* Line L30 applies the indexes 1, 2, 3 and so on, in order and without gaps. By Theorem 2 the entry at each index is the same on every server that applies it. $\blacksquare$
