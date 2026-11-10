---
title: Two-phase commit is safe under any crashes and delays, and it blocks
proves: [correctness]
status: full
---

We use lines L1 to L14 of the page. The model is asynchronous with crash-recovery failures: a process can crash at any point and later recover, with its log on stable storage and nothing else. Messages can be delayed without bound, and a crash loses the messages that the process had not yet sent. Messages are not changed or invented. The coordinator sends PREPARE once (line L1). A *decision* of a process is the moment it applies COMMIT or ABORT, which happens only after it writes the decision to its log.

**Lemma 1 (one decision per process).** Each process decides at most once, and never decides a different value after a recovery.

*Proof.* A process decides only if it has not decided. A decision is written to the log before it takes effect, and line L13 reads it back after a crash. The only decision after a recovery without a decision in the log is ABORT (line L13), and then the process had not decided before. $\square$

**Lemma 2 (every commit comes from the coordinator).** If some process decides COMMIT, the coordinator decided COMMIT before.

*Proof.* Take the first COMMIT decision in the run. The coordinator decides COMMIT only in line L2. A participant decides COMMIT only in line L7, on a COMMIT message, or in line L13, from its own log, which holds an earlier COMMIT decision of its own (Lemma 1). A COMMIT message is sent by line L4, L10 or L13, and in each case its sender has decided COMMIT earlier. So the first COMMIT decision is made by the coordinator, in line L2. $\square$

**Lemma 3 (a commit excludes every abort).** If the coordinator decides COMMIT, then every participant voted yes, and no process ever decides ABORT.

*Proof.* Line L2 needs YES from every participant, and a participant sends YES only after it forces PREPARED to its log (line L5). So each participant voted yes and has PREPARED in its log from then on. Assume that some process decides ABORT, and take the first ABORT decision in the run.

- It is not the coordinator. The coordinator decided COMMIT, and by Lemma 1 it does not decide again.
- It is not a decision in line L7. That needs an ABORT message, and the sender of an ABORT message (lines L4, L10, L11, L13) has already decided ABORT, which is earlier than the first ABORT decision.
- It is not a participant in line L6 or L8. A participant that voted yes did not vote no, and line L8 applies only before the vote. After a crash, the log holds PREPARED, so line L14 makes it uncertain, not line L8.
- It is not a participant in line L11. That line applies only to a participant that has not voted yes.
- It is not a participant in line L13. With no decision in its log, a participant aborts there only if PREPARED is missing.

So no process decides ABORT. $\square$

**Theorem 1 (safety).** In every run:

- *Agreement.* No two processes decide differently.
- *Validity.* If some process decides COMMIT, every participant voted yes.

*Proof.* If some process decides COMMIT, the coordinator decided COMMIT (Lemma 2). Then every participant voted yes, and no process decides ABORT (Lemma 3). $\square$

These two properties need no bound on delays, on the number of crashes or on the clocks.

**Theorem 2 (non-triviality and termination).** If no process crashes, no timeout fires, and every participant votes yes, then every process decides COMMIT. If every process that crashes recovers and then stays up, and every message between live processes arrives, then every process decides.

*Proof.* In the first case, every PREPARE arrives, every participant sends YES, the coordinator gets YES from all and decides COMMIT (line L2), and line L4 tells every participant, which decides COMMIT in line L7.

In the second case, after its last recovery the coordinator decides: it has a decision in its log, or it decides ABORT in line L13, or it waits in line L1 and decides on the votes or on a timeout (lines L2 and L3). Line L4, or line L13 after a recovery, sends the decision to every participant. A participant that is up when it arrives decides in line L7. A participant that recovers later and is uncertain asks the coordinator by line L9, and the coordinator answers by line L10. $\square$

**Theorem 3 (blocking).** A participant that is uncertain cannot decide while the coordinator is down and every other participant that it can reach is uncertain, without risk of breaking agreement.

*Proof.* Let participant $p$ be uncertain: it voted yes and knows no decision. Consider two runs that $p$ cannot tell apart. In run $R_c$, every participant voted yes, the coordinator decided COMMIT and crashed before it sent any message. In run $R_a$, the coordinator timed out before the last YES arrived, decided ABORT (line L3) and crashed before it sent any message. In both runs, every participant is uncertain, the coordinator is silent, and every message that $p$ gets is the same: UNCERTAIN from the other participants. If $p$ decides COMMIT, it breaks agreement in $R_a$, where the coordinator recovers and keeps ABORT. If $p$ decides ABORT, it breaks agreement in $R_c$, where the coordinator recovers and keeps COMMIT. So $p$ must wait until the coordinator, or a participant that knows the decision, answers. $\square$

The proof of Theorem 3 is the reason for the [atomic commit](/atomic-commit/) result that no protocol is non-blocking in an asynchronous system with crashes. Two-phase commit keeps safety and gives up termination while a failure lasts.
