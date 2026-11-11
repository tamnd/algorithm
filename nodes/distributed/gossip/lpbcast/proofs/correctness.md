---
title: lpbcast keeps bounded views without self entries, delivers each notification once, and infects at rate 1 - (1 - F/n)^i under uniform views
proves: [correctness]
status: full
---

**Setting.** Processes run lines L1 to L9. A message is handled from start to end before the next one. The eventIds buffer is large enough that no id of a notification still in circulation is trimmed.

**Claim.**

1. *Bounded views.* At all times, view($p$) holds at most $l$ processes and does not hold $p$.
2. *At most once.* A process delivers each notification at most once.
3. *No return of a leaver.* While $u$ is in unSubs($p$), the process $p$ does not add $u$ to view($p$).
4. *Infection rate.* Suppose that in a round $i$ processes forward a notification $e$, each to $F$ distinct members of its view, and that the views are independent uniform samples of $l$ other processes. Then a given process that has not delivered $e$ receives it in that round with probability $1 - (1 - F/(n - 1))^i$, which does not depend on $l$.

**Proof of 1.** By induction over the steps. A view changes only in lines L3, L4 and L5, and at a join, where the new process starts with one contact. Line L3 only removes. Line L4 adds only processes $s \ne p$. Line L5 runs at the end of each handled message and removes members until at most $l$ remain. So after every handled message the view has at most $l$ members, none equal to $p$. $\square$

**Proof of 2.** A delivery happens in line L7 or line L9, and in both places only for a notification whose id is not in eventIds($p$); the delivery adds the id at once. Ids are not removed (setting), so a second delivery of the same notification finds its id and is skipped. $\square$

**Proof of 3.** Line L4 is the only line that adds to a view after a join, and it skips every $s \in$ unSubs($p$). $\square$

**Proof of 4.** Fix an uninfected process $x$ and one forwarding process $y \ne x$. The view of $y$ is a uniform $l$-subset of the $n - 1$ other processes, so it holds $x$ with probability $l/(n - 1)$. Given that it holds $x$, the $F$ targets are a uniform $F$-subset of the view, which holds $x$ with probability $F/l$. So $y$ sends to $x$ with probability $(l/(n - 1)) (F/l) = F/(n - 1)$, and $l$ cancels. The views of different forwarding processes are independent, and so are their choices of targets, so $x$ is missed by all $i$ of them with probability $(1 - F/(n - 1))^i$. $\square$

**What is not proved.** The views produced by lines L3 to L6 are not exactly independent uniform samples; a gossip carries its sender and its recent subscriptions, so views of neighbours are correlated. Claim 4 is the model behind the analysis in the paper; the page measures how far the protocol is from it.
