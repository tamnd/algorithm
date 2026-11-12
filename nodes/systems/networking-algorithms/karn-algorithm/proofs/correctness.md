---
title: Karn's algorithm takes only exact samples and recovers from a longer path
proves: [correctness]
status: full
---

**Model.** The sender sends segments one after another and may resend a segment after a timeout. Each copy that is not lost is answered by an ACK that arrives a round-trip time after that copy was sent, but the ACK does not say which copy it answers. The sender acts on the first ACK for a segment. The estimator is the one of [Jacobson's RTO estimation](/jacobson-rto-estimation/): a sample updates SRTT, RTTVAR and RTO, and a timeout doubles the RTO up to the upper bound $U$. The lower bound is $L > 0$.

**Claim 1 (only exact samples).** Every sample that line L6 takes is the round-trip time of a copy that was really sent.

*Proof.* Line L6 runs only if the segment $s$ was sent once (line L5). Then there is exactly one copy, so the first ACK answers it, and $now - sent[s]$ is the round-trip time of that copy. $\square$

**Claim 2 (each naive rule fails on some trace).** If the sender measures from the first copy, a lost first copy makes the sample too large by at least the RTO. If it measures from the last copy, an ACK for an earlier, slow copy makes the sample too small.

*Proof.* First copy: let the first copy be lost, and let the second copy be sent at $t_0 + \mathrm{RTO}$ and answered after the true round trip $D$. The sample is $\mathrm{RTO} + D$. The next RTO is then larger than this sample, so the error grows with each such loss. In the tests, with $D = 0.5$ s and the first copies of six segments in a row lost, the samples are $1.5625$, $2.6172$, $4.4785, \ldots$, and the RTO is still above 18 s ten segments later.

Last copy: let the true round trip jump to $D = 3.5$ s while $\mathrm{RTO} = 1$. The first copy is sent at $t_0$, a copy at $t_0 + 1$ and a copy at $t_0 + 3$. The ACK of the first copy comes at $t_0 + 3.5$, and the sample is $0.5$. The estimate stays at $0.5$, the RTO stays 1, and each later segment is sent three times. $\square$

**Claim 3 (the backed-off RTO is needed).** If the sender used line L5 but set the RTO back to the value from SRTT and RTTVAR for each new segment, a jump of the round-trip time to a value $D > \mathrm{RTO}$ would stop all sampling.

*Proof.* Each new segment starts with the same RTO $< D$, so its timer expires before any ACK, and it is resent. So each segment is retransmitted, line L5 rejects every sample, and SRTT, RTTVAR and the RTO never change. $\square$

**Claim 4 (recovery).** Assume that from some time on the round-trip time is a constant $D < U$ and no packet is lost. Then within a bounded number of timeouts a segment is sent once, its sample is $D$, and from then on the estimate converges to $D$.

*Proof.* Line L3 doubles the RTO at each timeout, and no sample is taken from a retransmitted segment, so no step lowers the RTO until a segment is sent once. After at most $\lceil \log_2 (D/L) \rceil + 1$ timeouts, $\mathrm{RTO} \ge 2^j L > D$. The next segment is sent once, its ACK comes after $D$, before its timer expires, and line L6 takes the sample $D$ (Claim 1). Let $S$ be the SRTT before this sample. If $D > S$, line L5 gives $4\,\mathrm{RTTVAR} \ge D - S$ and line L6 gives $\mathrm{SRTT} = S + (D - S)/8$, so the new RTO is at least $S + \frac98 (D - S) > D$. If $D \le S$, the new SRTT is at least $D$, so the new RTO is at least $D$. So after the first sample of $D$, the RTO is never below $D$, every later segment is sent once, and each of them gives the sample $D$. SRTT is then a weighted mean in which the weight of the old values falls by the factor $\frac78$ per sample, so it converges to $D$. $\blacksquare$
