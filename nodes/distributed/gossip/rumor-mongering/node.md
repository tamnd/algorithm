---
tag: 97KQKR
kind: algorithm
slug: rumor-mongering
name: Rumor mongering
aliases:
- complex epidemics
- feedback rumor mongering
area: distributed/gossip
level: advanced
summary: A site pushes a hot update to random sites and stops after k contacts that were not needed. A residue s of sites misses it, with s close to e^(-m) for m messages per site.
model: random-phone-call-model
complexity:
  vars: {n: the number of sites, k: the counter or coin parameter, s: the residue}
  messages: {total: Θ(n log(1/s))}
  time: {rounds: Θ(log n)}
  space: {extra: O(1)}
properties: {deterministic: false, recursive: false}
history:
  year: 1987
  people: [Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart, Doug Terry]
  note: Demers et al. took the rumor model of epidemiology, added the counter, coin, blind and pull variants, and used it with anti-entropy as a backup in the Xerox Clearinghouse.
prereqs: [push-gossip, epidemic-model, anti-entropy, random-phone-call-model]
see_also: [death-certificates, pull-gossip, push-pull-gossip, epidemic-threshold, gossip-fanout, rumor-spreading-message-lower-bound, bimodal-multicast, eventual-consistency]
sources:
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1.4 (the rumor equations, the residue, traffic and delay, the variants, Tables 1 to 3), Section 1.5 (backup with anti-entropy)
  - paper: doi:10.2307/3213787
    title: Aidan Sudbury, The proportion of the population never hearing a rumour, Journal of Applied Probability 22(2), 443-446, 1985
    locator: the main theorem, the fraction that never hears the rumor in the model of Maki and Thompson tends to about 0.203
  - paper: doi:10.1093/imamat/1.1.42
    title: Daryl J. Daley and David G. Kendall, Stochastic rumours, Journal of the Institute of Mathematics and its Applications 1(1), 42-55, 1965
    locator: the rumor model with spreaders, ignorants and stiflers
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: the median counter algorithm, push-pull with O(log n) rounds and O(n log log n) transmissions
---

Rumor mongering is the "complex epidemic" of Demers et al. (1987): a site that receives a new update treats it as a hot rumor and pushes it to random sites, and it stops after the rumor has been found to be already known a number of times. Unlike [push gossip](/push-gossip/) with no stopping rule, the spreading ends by itself and the traffic stays at a few messages per site. The price is a residue: a small fraction $s$ of the sites never hears the update, and for every push variant $s$ is close to $e^{-m}$, where $m$ is the number of messages sent per site. A slow [anti-entropy](/anti-entropy/) process runs as a backup and repairs the residue.

## In plain words

Somebody tells you a piece of news. While the news is fresh, you phone friends at random and tell them. When a friend says "I knew that already", you get a little bored. After a few such calls you stop calling. Everyone who learns the news does the same.

At first nearly every call reaches somebody new, so the news spreads fast. Later most calls reach people who already know it, so people get bored and stop. The spreading dies out on its own, after few calls per person.

Some people are never called before everyone stops. If people put up with more boring calls before they stop, fewer people miss the news, but more calls are made. To catch the few who missed it, sites also compare their whole databases now and then.

## The problem

Each site holds a replica of a database. An update enters at one site and must reach all $n$ sites with few messages and a short delay. The model is the [random phone call model](/random-phone-call-model/) on the complete graph, in synchronous cycles: in a cycle, each site with a hot update calls one site chosen uniformly at random among the others. Demers et al. measure three things:

- **Residue** $s$: the fraction of sites that are still susceptible when no site is infective.
- **Traffic** $m$: the number of update messages sent, divided by $n$.
- **Delay**: $t_{\text{ave}}$, the mean over the sites that receive the update of the cycle in which it arrives, and $t_{\text{last}}$, the cycle in which the last of them receives it.

With respect to one update, a site is susceptible (it does not know the update), infective (it knows the update and spreads it) or removed (it knows the update and has stopped spreading it).

| Symbol | Meaning |
|---|---|
| $n$ | the number of sites |
| $k$ | the counter limit or the coin parameter |
| $s, i, r$ | the fractions of susceptible, infective and removed sites, $s + i + r = 1$ |
| $m$ | the traffic, update messages per site (in this page $m$ is not a number of edges) |
| $t_{\text{ave}}, t_{\text{last}}$ | the mean and the last arrival cycle |
| $f$ | the number of sites that crash |
| $D$, $\Delta$ | the diameter and the maximum degree; on the complete graph $D = 1$ and $\Delta = n - 1$ |

## The algorithm

```pseudo id=main
RUMOR MONGERING at site p, once per cycle, for one update u
L1  if u is hot (infective) at p then
L2      q ← a site chosen uniformly at random, other than p
L3      send UPDATE(u) to q; q replies "needed" if it did not know u at the start of the cycle
ON UPDATE(u) received at site q
L4  if q did not know u then q stores u, and u is hot at q from the next cycle on
AFTER THE REPLY at site p
L5  if feedback is on and the reply is "needed" then
L6      count ← 0, and nothing else happens in this cycle
L7  if counter is on then count ← count + 1, and if count ≥ k then u stops being hot at p
L8  else with probability 1/k, u stops being hot at p
```

There are four combinations. With **feedback**, only a contact that was not needed makes $p$ lose interest; in the **blind** form, line L5 is never true, so every contact counts and the receiver does not have to reply. With a **counter**, $p$ stops after $k$ such contacts (line L7); with a **coin**, $p$ stops with probability $1/k$ at each such contact (line L8). Blind with a counter keeps the update hot for exactly $k$ cycles.

**The counter reset (line L6).** Section 1.4 of Demers et al. says only that a site with a counter loses interest "after $k$ unnecessary contacts". The footnote of their Table 3, for pull, says that the counter is reset when a contact was needed. Line L6 applies the same reset to push. The reset is a choice made on this page, but it is the reading that reproduces Table 1 (see the Example). Without it, the residue is larger for every $k \ge 2$.

## Example

**One run.** With seed 7, $n = 1000$, feedback and a counter with $k = 1$ (the reset has no effect when $k = 1$), the implementation gives the following counts at the end of each cycle.

| Cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Susceptible | 998 | 996 | 992 | 984 | 969 | 941 | 890 | 801 | 670 |
| Infective | 2 | 4 | 8 | 16 | 30 | 56 | 103 | 179 | 282 |
| Removed | 0 | 0 | 0 | 0 | 1 | 3 | 7 | 20 | 48 |

| Cycle | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|
| Susceptible | 504 | 354 | 264 | 216 | 189 | 176 | 174 | 174 |
| Infective | 354 | 326 | 205 | 101 | 56 | 26 | 5 | 0 |
| Removed | 142 | 320 | 531 | 683 | 755 | 798 | 821 | 826 |

The rumor doubles while few sites know it, as in push gossip. After cycle 10 most contacts reach sites that know the update, and the infective count falls. The run ends after 17 cycles with residue $0.174$, traffic $m = 1.754$, $t_{\text{ave}} = 9.88$ and $t_{\text{last}} = 16$. Note that $e^{-1.754} = 0.173$.

**The simulator against Table 1.** Table 1 of Demers et al. is for push, feedback and a counter on 1000 sites. The table below gives it next to the means of 30 seeded runs of the implementation, with and without the reset of line L6. No run died out early.

| $k$ | Table 1: $s$ | $m$ | $t_{\text{ave}}$ | $t_{\text{last}}$ | With reset: $s$ | $m$ | $t_{\text{ave}}$ | $t_{\text{last}}$ | No reset: $s$ | $m$ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.18 | 1.7 | 11.0 | 16.8 | 0.173 | 1.75 | 9.79 | 16.67 | 0.173 | 1.75 |
| 2 | 0.037 | 3.3 | 12.1 | 16.9 | 0.035 | 3.30 | 9.97 | 17.13 | 0.048 | 3.03 |
| 3 | 0.011 | 4.5 | 12.5 | 17.4 | 0.010 | 4.54 | 10.03 | 17.70 | 0.016 | 4.15 |
| 4 | 0.0036 | 5.6 | 12.7 | 17.5 | 0.0035 | 5.63 | 10.05 | 17.13 | 0.0050 | 5.20 |
| 5 | 0.0012 | 6.7 | 12.8 | 17.7 | 0.0011 | 6.68 | 10.04 | 17.73 | 0.0016 | 6.22 |

With the reset, the residue, the traffic and $t_{\text{last}}$ agree with Table 1. The mean delay $t_{\text{ave}}$ of the simulator is 1 to 3 cycles smaller than in Table 1, and it does not grow with $k$ as much. The paper does not say how it counts cycles or over which sites it takes the mean, so this page does not explain the difference. In the simulator, a site that receives the update in cycle $t$ has arrival time $t$, the source has arrival time 0, and the mean is over the sites that receive the update.

**Blind and coin.** Table 2 of Demers et al. gives, for $k = 1$ to 5, the residues 0.96, 0.20, 0.060, 0.021 and 0.008 with traffic 0.04, 1.6, 2.8, 3.9 and 4.9. The simulator gives the residues 0.955, 0.2065 and 0.0598 for $k = 1$, 2 and 3. With $k = 1$ in the blind coin form, each infective site makes exactly one contact and stops, so the update moves along a single chain of sites until the chain reaches a site that knows it. As in the birthday problem, the chain has about $\sqrt{\pi n / 2} \approx 40$ sites for $n = 1000$, which is the traffic 0.04 of Table 2.

**Pull.** Table 3 of Demers et al. is for pull with feedback and a counter (reset as above). At $k = 2$ the residue is $5.8 \times 10^{-4}$ with $m = 4.5$, and at $k = 3$ it is $4.0 \times 10^{-6}$ with $m = 6.1$, far below $e^{-m}$.

## Correctness

**Safety and termination.** A site stores only the update that it receives (line L4), and the set of sites that know it only grows. With probability 1, no site is infective after a finite number of cycles; the proof is in the proof file.

**Incomplete delivery is possible.** For every fixed $k$ and every $n \ge 3$, the rumor stops before all sites know it with positive probability. For example, with feedback and a counter, suppose the source calls site $q$ in cycle 1, and in each of the next $k$ cycles the source and $q$ call each other. Both reach count $k$ and stop, and $n - 2$ sites never hear the update. This is why Demers et al. back up rumor mongering with anti-entropy.

**The residue equation (feedback and coin).** Let each infective site make contacts at rate 1, and let $n \to \infty$. Demers et al. model the fractions with the rate equations
$$\frac{ds}{dt} = -s i, \qquad \frac{di}{dt} = s i - \frac{1}{k}(1 - s) i.$$
The first term is the rate of contacts from infective to susceptible sites. The second is the rate of contacts that were not needed, $(1 - s) i$, times the chance $1/k$ of losing interest. Divide the second equation by the first:
$$\frac{di}{ds} = -\frac{k + 1}{k} + \frac{1}{k s}, \qquad i(s) = \frac{k + 1}{k}(1 - s) + \frac{1}{k} \ln s,$$
with the constant chosen so that $i(1) = 0$, which is the limit of one infective site among $n$. The spreading ends at the root $s$ in $(0, 1)$ of $i(s) = 0$:
$$s = e^{-(k + 1)(1 - s)}.$$
For $k = 1$, 2, 3, 4 and 5 the root is 0.2032, 0.0595, 0.0198, 0.0070 and 0.0025. Demers et al. state the first two as about 20% and 6%. For $k = 1$ the feedback and coin rule is the rumor model of Maki and Thompson, and Sudbury (1985) proved that the fraction that never hears the rumor tends to about 0.203 in that model.

**Residue against traffic.** In the same rate equations, traffic per site grows at rate $dm/dt = i$, since each infective site sends one message per unit of time. The first equation gives $d(\ln s)/dt = -i$. So at the end
$$\ln s = -m, \qquad s = e^{-m},$$
and $m = (k + 1)(1 - s)$. For the blind coin form, the second equation is $di/dt = s i - i/k$, and the same steps give $s = e^{-k(1 - s)}$ and again $s = e^{-m}$. This is the final size equation of the SIR [epidemic model](/epidemic-model/) with $R_0 = k$, so blind and coin with parameter $k$ has the residue of feedback and coin with $k - 1$: 0.2032 at $k = 2$ and 0.0595 at $k = 3$, as in Table 2.

Demers et al. give a heuristic for the counter forms too: the $nm$ messages go to random sites, and a site misses all of them with probability $(1 - 1/n)^{nm} \approx e^{-m}$. They note that this needs the spread of the per-site traffic to vanish as $n \to \infty$, which they observed in simulations but did not prove. The relation is an observation, not a theorem, for the counter forms.

## Complexity

- **Messages.** Exactly one message per infective site per cycle, so the total is the sum of the infective counts over the cycles. For a residue $s$, push needs about $n \ln(1/s)$ messages. To miss no site with high probability, $s$ must be about $1/n$, so $k = \Theta(\log n)$ and $\Theta(n \log n)$ messages, the same order as [push gossip](/push-gossip/). This agrees with the lower bound of Karp et al. for push on [the message lower bound page](/rumor-spreading-message-lower-bound/).
- **Cycles.** $t_{\text{last}}$ is about 17 for $n = 1000$ and every $k$ from 1 to 5, in Table 1 and in the simulator. This page does not prove a bound on the number of cycles; $\Theta(\log n)$ for a fixed $k$ is what the simulations show.
- **Space.** One state (susceptible, infective or removed) and one counter per update per site, and a list of the hot updates.

## Properties

- **Self-stopping.** No clock or age bound is needed; the feedback or the counter ends the spreading.
- **Cheap when the update is old news.** A hot rumor that is already known at almost all sites dies after a few cycles, which makes rumor mongering a good way to redistribute an update found missing during anti-entropy (Demers et al., Section 1.5).
- **Not reliable alone.** The residue is positive, and the whole epidemic can die early. Anti-entropy must back it up.
- **Feedback needs a reply.** The blind forms need no reply from the receiver.

## Variants and improvements

- **Pull.** Sites ask a random site for its hot updates. Pull does much better than $s = e^{-m}$ (Table 3). It suits a database with many updates; when there are no updates, pull still sends requests.
- **Minimization.** Push and pull together, and when both sites already know the update, only the site with the smaller counter adds one (both if the counters are equal). Demers et al. report the smallest residue of all their variants.
- **Connection limit.** If a site accepts at most one connection per cycle, push gets better and pull gets worse. Demers et al. estimate $s = e^{-\lambda m}$ with $\lambda = 1/(1 - e^{-1}) \approx 1.58$ for push with limit 1, and $\lambda = -\ln \delta$ for pull when a connection fails with probability $\delta$.
- **Hunting.** A site whose connection is refused tries other sites. With limit 1 and no bound on the hunt, the contacts form a permutation, and push and pull become the same.
- **Peel back with rumor feedback.** Updates are kept in a list in local activity order; useful updates move to the front. Demers et al. describe this as a mix of rumor mongering and anti-entropy with no failure probability.
- **Median counter.** Karp et al. (2000) give a push-pull rule with counters that informs all sites in $O(\log n)$ rounds with $O(n \log \log n)$ messages, with high probability; see [push-pull gossip](/push-pull-gossip/).
- **Deletions.** A deleted item must spread as a [death certificate](/death-certificates/), or anti-entropy brings the old value back.

## When to use it

Use rumor mongering for the first, fast spread of each update in a replicated store when a few messages per site per update are the budget and a slow anti-entropy process repairs what it misses. Use pull or push-pull when there are many updates at the same time. Use [push gossip](/push-gossip/) with an age bound or a [probabilistic broadcast](/probabilistic-broadcast/) protocol when each message must reach all sites with high probability and no backup exists.

## Pitfalls

- **No backup.** Wrong: take the residue $e^{-m}$ as the probability that one site misses the update and then drop anti-entropy. Right: the residue is a fraction of sites, and the whole epidemic can also die early, so a backup is needed.
- **Judging "needed" at the wrong time.** Wrong: compare simulations that decide "needed" at the moment of contact with ones that decide it at the start of the cycle. Right: fix one rule. With the start-of-cycle rule, two contacts to the same susceptible site in one cycle both count as needed. This is why the lock-step simulator gives 0.178 for feedback and coin with $k = 1$, while the rate equations give 0.203.
- **Counter semantics.** Wrong: assume that "after $k$ unnecessary contacts" fixes the algorithm. Right: say whether a needed contact resets the counter; at $k = 2$ the residue is 0.035 with the reset and 0.048 without it.
- **Choosing $k$ for one $n$.** Wrong: keep $k$ fixed as the system grows. Right: the number of sites that miss the update is about $n e^{-m}$, so $k$ must grow like $\ln n$ to keep it below 1.

## Implementations

The Python code is a seeded lock-step simulator of push rumor mongering on the complete graph. Each site has one of three states and a counter, and the message type is UPDATE. In each cycle, every site that is infective at the start of the cycle calls one random other site, and the receiver says whether it was susceptible at the start of the cycle. The flags select feedback or blind, counter or coin, and the reset. New infectives start to push in the next cycle. The function returns the residue, the traffic, $t_{\text{ave}}$, $t_{\text{last}}$ and the number of cycles. Other functions run the one-contact-at-a-time chain whose rate equations are above, solve the residue equation by bisection, and run the stochastic SIR model. The same file has the death certificate store used on [the death certificates page](/death-certificates/).

## History

Rumor models come from applied probability: Daley and Kendall (1965) studied the spread of a rumor in which spreaders stop when they meet people who know it. In the later model of Maki and Thompson only the caller stops, and Sudbury (1985) proved the 0.203 limit for that model. Demers, Greene, Hauser, Irish, Larson, Shenker, Sturgis, Swinehart and Terry (1987) at Xerox PARC used the model to spread updates in the Clearinghouse name service. They introduced the blind, counter, pull, minimization, connection limit and hunting variants, found the relation $s = e^{-m}$, and used anti-entropy as a backup. Karp, Schindelhauer, Shenker and Vöcking (2000) gave a counter rule for push-pull with $O(n \log \log n)$ messages.

## References
