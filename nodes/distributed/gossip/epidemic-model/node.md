---
tag: 6N6A1S
kind: model
slug: epidemic-model
name: SIR epidemic model
aliases:
- SIR model
- Kermack-McKendrick model
area: distributed/gossip
level: intro
summary: Nodes are susceptible, infective or removed, and infectives meet random nodes. Its equations predict how gossip grows and what fraction it misses, s = e^(-R0(1-s)).
prereqs: [euler-method, fixed-point-iteration, gossip-protocol]
see_also: [epidemic-threshold, push-gossip, rumor-mongering, gossip-fanout, giant-component, bimodal-multicast, random-phone-call-model, percolation]
sources:
  - paper: doi:10.1098/rspa.1927.0118
    title: William O. Kermack and Anderson G. McKendrick, A contribution to the mathematical theory of epidemics, Proceedings of the Royal Society of London, Series A 115(772), 700-721, 1927
    locator: the general model with infectivity and removal rates depending on the age of infection; the threshold density of susceptibles and the final size of the epidemic
  - paper: doi:10.1137/S0036144500371907
    title: Herbert W. Hethcote, The mathematics of infectious diseases, SIAM Review 42(4), 599-653, 2000
    locator: Section 2 (the SIR and SIS models, the basic reproduction number R0, the final size relation, the endemic equilibrium of SIS)
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1 (susceptible, infective and removed sites), Section 1.4 (the differential equations of rumor mongering and the residue s = e^{-(k+1)(1-s)})
  - paper: doi:10.1038/2041118a0
    title: Daryl J. Daley and David G. Kendall, Epidemics and rumours, Nature 204, 1118, 1964
    locator: the rumor model in which a spreader stops when it meets another spreader or a stifler
---

The SIR epidemic model describes how something spreads through a population whose members are susceptible (S), infective (I) or removed (R). Infectives meet other members at random and pass the infection to the susceptibles they meet, and they leave the infective class at some rate. Kermack and McKendrick (1927) gave its differential equations, its threshold and its final size; Demers et al. (1987) took its words and its equations for gossip, where "infective" means a node that is spreading an update. Push gossip is the SI model, rumor mongering is an SIR model, and the final size equation $s_\infty = e^{-R_0(1 - s_\infty)}$ gives the fraction of nodes that a gossip protocol misses.

## The machine

**Population.** There are $n$ members, called nodes. Each node is in one of three states:

- **susceptible**: it does not have the update;
- **infective**: it has the update and spreads it;
- **removed**: it has the update and no longer spreads it.

Write $s$, $i$ and $r$ for the fractions of nodes in each state, with $s + i + r = 1$.

**Contacts.** Mixing is homogeneous: every pair of nodes is equally likely to meet. Each infective makes contacts at rate $\beta$, each with a node chosen uniformly at random, and a contact with a susceptible infects it. This is "mass action": new infections occur at rate $\beta s i$ per node.

**Removal.** In SIR, each infective is removed at rate $\gamma$, so it stays infective for an exponential time with mean $1/\gamma$ and makes $\beta/\gamma$ contacts on average.

**Three models.**

| Model | Equations | Gossip meaning |
|---|---|---|
| SI | $\dot s = -\beta s i$, $\dot i = \beta s i$ | push forever: an informed node never stops |
| SIS | $\dot s = -\beta s i + \gamma i$, $\dot i = \beta s i - \gamma i$ | a node can forget, or a value can be overwritten |
| SIR | $\dot s = -\beta s i$, $\dot i = \beta s i - \gamma i$, $\dot r = \gamma i$ | the node stops spreading after a while: rumor mongering |

**Deterministic and stochastic forms.** The equations above are the deterministic form, the limit of the fractions as $n \to \infty$ over finite time intervals. The stochastic form is a continuous-time Markov chain on the counts $(S, I, R)$: an infection happens at rate $\beta S I / n$ and a removal at rate $\gamma I$. The discrete-time form, a chain binomial, lets each infective of one generation infect each susceptible with a fixed probability; [bimodal multicast](/bimodal-multicast/) analyses its gossip rounds this way.

**Notation.**

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $s$, $i$, $r$ | the fractions of susceptible, infective and removed nodes |
| $\beta$ | the contact rate of an infective |
| $\gamma$ | the removal rate |
| $R_0$ | $\beta/\gamma$, the mean number of nodes one infective infects in a fully susceptible population |
| $s_\infty$ | the fraction of nodes never infected, the residue |
| $f$ | the number of crashed nodes |

## What it counts

- **Growth.** How fast the infective fraction grows; this predicts the number of rounds or the time until most nodes have an update.
- **Final size.** The fraction $1 - s_\infty$ of nodes ever infected; in gossip, $s_\infty$ is the fraction that never gets the update, the *residue*.
- **Threshold.** Whether an infection that starts in one node reaches a constant fraction of the nodes, or dies out after a few contacts.
- **Traffic.** The number of contacts per node, $m$, which is the message cost of a gossip protocol.

## Relation to other models

**SI and push gossip.** In [push gossip](/push-gossip/) on the complete graph, every informed node contacts one random node per round and never stops; this is the SI model with $\beta = 1$ per round. In continuous time, the solution of $\dot i = i(1 - i)$ with $i(0) = 1/n$ is the logistic curve
$$i(t) = \frac{1}{1 + (n - 1)e^{-t}},$$
which takes time $\ln(n - 1)$ to reach $1/2$ and another $\ln(n - 1)$ to reach $1 - 1/n$, so asynchronous push takes about $2 \ln n$ units of time. In synchronous rounds, the fluid limit is the recurrence
$$i_{t+1} = 1 - (1 - i_t) e^{-i_t},$$
because a susceptible node is missed by each of the $i_t n$ pushes with probability $1 - 1/n$. It doubles $i$ while $i$ is small and divides $1 - i$ by about $e$ when $i$ is close to 1, which gives the $\log_2 n + \ln n$ rounds of [the push rumor spreading time](/push-rumor-spreading-time/).

**SIS.** If $\beta > \gamma$, the SIS model has the endemic equilibrium $i^* = 1 - \gamma/\beta$; if $\beta \le \gamma$, the infection dies out. On a graph, the threshold depends on the largest eigenvalue of the adjacency matrix; see [the epidemic threshold](/epidemic-threshold/).

**SIR and rumor mongering.** In [rumor mongering](/rumor-mongering/), an infective site that contacts a site that already knows the rumor loses interest with probability $1/k$. Demers et al. write this as
$$\dot s = -s i, \qquad \dot i = s i - \frac{1}{k}(1 - s) i.$$
The removal rate $(1 - s)/k$ grows as the rumor spreads, which is the form of the rumor model of Daley and Kendall (1964), not the constant rate $\gamma$ of SIR. Dividing the two equations gives $di/ds = -\frac{k+1}{k} + \frac{1}{ks}$, so $i(s) = \frac{k+1}{k}(1 - s) + \frac{1}{k}\ln s$ with $s = 1$ and $i = 0$ at the start. Setting $i = 0$ at the end gives the residue equation
$$s = e^{-(k+1)(1 - s)},$$
which is the SIR final size equation with $R_0 = k + 1$.

**Random graphs.** The set of nodes ever infected in the SIR model with a fixed infectious period is the set reached from the source in a random graph in which each node points to its contacts. The final size is the size of the [giant component](/giant-component/) of that graph, and the threshold $R_0 = 1$ is the threshold of [percolation](/percolation/) and of the [Erdős-Rényi giant component](/erdos-renyi-giant-component-theorem/). The same view gives the fanout threshold of [gossip fanout](/gossip-fanout/).

**The random phone call model.** The [random phone call model](/random-phone-call-model/) is a discrete, stochastic version of the homogeneous mixing above, with exactly one contact per node per round, in which the contacts of uninformed nodes also matter (pull).

## Known results in the model

**The threshold (Kermack and McKendrick 1927).** In SIR, $\dot i = (\beta s - \gamma) i$, so the infective fraction grows if and only if $s > 1/R_0$. If $R_0 \le 1$ and $s \le 1$, it never grows, and an infection that starts in a few nodes reaches only $o(n)$ of them. If $R_0 > 1$, it grows while $s > 1/R_0$.

**The final size.** Divide $\dot s = -\beta s i$ by $\dot r = \gamma i$ to get $ds/dr = -R_0 s$, so $s = s_0 e^{-R_0 (r - r_0)}$. Start with $s_0 \to 1$ and $r_0 = 0$, and wait until $i = 0$, so $r_\infty = 1 - s_\infty$:
$$s_\infty = e^{-R_0 (1 - s_\infty)}.$$
For $R_0 > 1$ this has exactly one root in $(0, 1)$, because $g(s) = e^{-R_0(1 - s)} - s$ is convex with $g(0) > 0$, $g(1) = 0$ and $g'(1) = R_0 - 1 > 0$. The proof is complete as stated; it uses only the two equations.

| $R_0$ | 1.5 | 2 | 3 | 5 |
|---|---|---|---|---|
| $s_\infty$ (the residue) | 0.417 | 0.203 | 0.060 | 0.007 |
| $1 - s_\infty$ (ever infected) | 0.583 | 0.797 | 0.940 | 0.993 |

The implementation of the rumor mongering page runs the stochastic SIR chain with $n = 2000$ and keeps the runs that take off: the mean residue is 0.4145, 0.2053 and 0.0602 for $R_0 = 1.5$, 2 and 3, against 0.4172, 0.2032 and 0.0595 from the equation.

**The peak.** The quantity $i + s - \frac{1}{R_0} \ln s$ is constant along solutions of SIR, so the largest infective fraction, reached at $s = 1/R_0$, is
$$i_{\max} = 1 - \frac{1 + \ln R_0}{R_0}$$
when the infection starts with $s_0 \approx 1$. For $R_0 = 2$ it is about 0.153, and for $R_0 = 3$ about 0.300.

**Traffic and residue.** In rumor mongering, Demers et al. observe that the residue $s$ and the traffic $m$, the number of messages per site, satisfy $s = e^{-m}$ for all the push variants they study. Since each message reaches a random site, a site is missed by all $mn$ messages with probability about $(1 - 1/n)^{mn} \approx e^{-m}$.

**The stochastic start.** In the stochastic SIR model with $R_0 > 1$ and one initial infective, the infection dies out early with probability about $1/R_0$, and otherwise it reaches about $(1 - s_\infty) n$ nodes. In gossip, a node that keeps spreading until it has made enough contacts, as in fixed fanout, never dies out early.

## References
