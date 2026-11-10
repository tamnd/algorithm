---
title: The invitation algorithm keeps groups consistent, and merges cost 3(k − 1) messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** In every run, with any message delays, lost messages, partitions, crashes and recoveries:

1. If two processes are in the normal state with the same group number, they have the same coordinator.
2. If $p$ is normal in group $g$ with coordinator $c \ne p$, and $c$ is normal in group $g$, then $p \in \mathit{members}_c$.
3. No process stays in the election or reorganizing state for longer than its timer.
4. A merge by a coordinator of groups with $k$ processes in total, in which no message is lost and no process fails, sends exactly $3(k - 1)$ INVITE, ACCEPT and READY messages.

**Uniqueness of group numbers.** Only process $i$ makes group numbers of the form $(\cdot, i)$ (lines L1 and L4), and each time with a larger counter; the counter is kept over crashes. So each group number $g = (x, i)$ names one process, write $\mathrm{owner}(g) = i$, and is made only once.

**Lemma 1.** At all times, every process $p$ has $\mathit{coord}_p = \mathrm{owner}(\mathit{gid}_p)$.

*Proof.* Lines L1 and L4 set $\mathit{gid}_p = (\cdot, p)$ and $\mathit{coord}_p = p$ (line L4 keeps $\mathit{coord}_p = p$, since only a coordinator merges). Line L9 does not change $\mathit{gid}$ and sets $\mathit{coord}_p = p$, and $\mathit{gid}_p$ was set by line L4 of the same process. Line L7 sets $\mathit{gid}_p = g$ and $\mathit{coord}_p = \mathrm{owner}(g)$; in the code this is $c = g$'s second component, whether the invitation came from the owner or was passed on by line L6. No other line changes either variable. $\square$

**Part 1** follows: two processes with the same group number $g$ both have coordinator $\mathrm{owner}(g)$.

**Lemma 2.** A process $c$ changes $\mathit{members}_c$ only in lines L1, L7 and L9, and in each case it also changes $\mathit{gid}_c$ or its state. While $c$ stays normal in group $g$ after line L9, $\mathit{members}_c$ is fixed.

*Proof.* By inspection. Line L9 sets the list once and the state to normal; leaving group $g$ needs line L1, L4 or L7, each of which sets a new group number. $\square$

**Part 2.** Process $p \ne \mathrm{owner}(g)$ becomes normal in group $g$ only by line L10, on READY$(g)$. Only $c = \mathrm{owner}(g)$ sends READY$(g)$, once, in line L9, to the processes in $\mathit{members}_c$ at that moment. Since $g$ is made once, $c$ is normal in $g$ only from that line L9 on, until it leaves $g$, and by Lemma 2 its list does not change in that time. So $p \in \mathit{members}_c$ whenever $c$ is normal in $g$. If $p$ received READY before $c$ is normal in $g$: impossible, because $c$ sends READY in line L9 at the moment it becomes normal in $g$.

**Part 3.** Lines L4 and L7 start a timer, and lines L9 and L12 end the state when it runs out. The timer is local, so this holds without any bound on message delays.

**Part 4.** Let $c$ merge, with its own members $M$ and the found coordinators $F$, whose groups $G_f$ are disjoint from $M$ and from each other, and $k = |M| + \sum_{f \in F} |G_f|$. Suppose all these processes are normal when the invitations arrive, no message is lost, and all ACCEPT messages arrive before the timer of $c$ ends. Process $c$ sends INVITE to $(M \setminus \{c\}) \cup F$. Each $f \in F$ is a coordinator and passes the invitation on to $G_f \setminus \{f\}$ by line L6. Each member of $G_f$ gets that invitation while normal, and gets no other one, because after line L7 it is reorganizing and ignores more invitations. So each of the $k - 1$ processes other than $c$ gets one INVITE: $k - 1$ messages. Each sends one ACCEPT: $k - 1$ messages. Then $\mathit{accepted}_c$ has $k$ elements and line L9 sends $k - 1$ READY messages. In total $3(k - 1)$.

**Progress (sketch).** Assume that after some time the partitions, the live processes and the crash state stop changing, every message within a part arrives within $\delta$, and the timers are long enough for these delays. Then no member is wrongly removed by line L12, so groups only merge. In each period every coordinator of a part finds all other normal coordinators of the part. The merge wait in line L3 differs by at least one period plus $\delta$ per step of priority, so the coordinator $c^*$ with the highest priority among them merges first, and its invitations reach the others before their own merge times; they join and drop their planned merges. So after each such period the number of groups in the part goes down to one, unless a merge of $c^*$ meets a coordinator that is itself in the election state. This can only happen when a lower coordinator started its merge first, which the waits make impossible after the first period in which all coordinators have found each other. The seeded tests check this behaviour, including runs with crashes and partitions that end. This part is a sketch; Garcia-Molina's paper does not claim that one group always forms. $\blacksquare$
