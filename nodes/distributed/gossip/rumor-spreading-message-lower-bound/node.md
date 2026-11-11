---
tag: XGC5CN
kind: theorem
slug: rumor-spreading-message-lower-bound
name: Rumor spreading message lower bound
aliases:
- Karp et al. lower bound
area: distributed/gossip
level: research
summary: In the random phone call model, an address-oblivious algorithm needs Ω(n log log n) rumor transmissions to inform all n nodes; with push only it needs Θ(n log n).
prereqs: [random-phone-call-model, push-pull-gossip, chernoff-bound, coupon-collector-problem, linearity-of-expectation]
see_also: [rumor-spreading-problem, push-pull-gossip, push-gossip, pull-gossip, push-rumor-spreading-time, message-complexity, lower-bound, coupon-collector-problem]
sources:
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Section 1.2 (the model, transmissions, distributed and address-oblivious algorithms), Section 1.3 (the algorithm with n - 1 transmissions), Theorem 2.1, Theorem 3.1, Theorem 4.1 and its proof (sparse and dense phases), Theorem 5.1
  - paper: doi:10.1137/0147013
    title: Boris Pittel, On spreading a rumor, SIAM Journal on Applied Mathematics 47(1), 213-223, 1987
    locator: the number of rounds of push on the complete graph, log2 n + ln n + O(1)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Section 2.4 (the coupon collector problem), Section 3.3 (Chebyshev's inequality)
---

The rumor spreading message lower bound of Karp, Schindelhauer, Shenker and Vöcking (2000) says that in the [random phone call model](/random-phone-call-model/), every address-oblivious algorithm that informs all $n$ nodes needs $\Omega(n \log \log n)$ transmissions of the rumor in expectation, however many rounds it uses. An algorithm is address-oblivious if a node decides whether to send the rumor along a call without knowing who is at the other end. [Push-pull](/push-pull-gossip/) with a good stopping rule reaches this bound, while every push-only algorithm needs $\Theta(n \log n)$ transmissions. A second result shows that no algorithm, address-oblivious or not, can use $O(\log n)$ rounds and $O(n)$ transmissions together.

## Statement

**Model.** There are $n$ players, the nodes. Time runs in synchronous rounds. In each round, every player calls one partner chosen uniformly at random, independently of all other choices, and the rumor can go along each call in both directions: from the caller to the called player (*push*) or back (*pull*). Information received in a round can be sent on only in a later round. One rumor starts at one player. The cost is the number of *transmissions*: one for each call along which the rumor is sent, whatever the size of the message. Calls that carry no rumor cost nothing. There are no failures.

**Distributed and address-oblivious.** An algorithm is *distributed* if the decision of a player to send the rumor along a call in round $t$ depends only on its state. The state may depend on its own address, on $n$, on random bits, on everything it has received, and, for the lower bounds, on the global round number and the birth time of the rumor. It is *address-oblivious* if, in addition, the state in round $t$ does not depend on the addresses of the partners in round $t$, only on their number; it can depend on the addresses of partners of earlier rounds. All the rumor spreading algorithms of Demers et al. (1987), and push, pull, push-pull and the median counter, are address-oblivious.

| Symbol | Meaning |
|---|---|
| $n$ | the number of players |
| $f$ | the fraction of players that may stay uninformed (on other pages $f$ is a number of crashed nodes) |
| $X$ | the number of rumor transmissions |
| $U_i$ | the number of players still uninformed at the end of phase $i$ |
| $m$, $D$, $\Delta$ | on the complete graph, $n(n-1)/2$, 1 and $n - 1$ |

**Theorem 1 (Karp et al. 2000, Theorem 4.1).** "Any address-oblivious algorithm guaranteeing that all but a fraction $f$ of the players receive the rumor with constant probability needs to perform $\Omega(n \ln \ln \frac{1}{f})$ transmissions in expectation." The bound holds for every number of rounds.

**Corollary.** An address-oblivious algorithm that informs all $n$ players with constant probability needs $\Omega(n \log \log n)$ transmissions in expectation. (Take $f = \ln^2 n / n$; then $\ln \ln (1/f) = \ln \ln n - o(1)$.)

**Theorem 2 (push only).** An address-oblivious algorithm that sends the rumor only by push, and informs all $n$ players with probability at least $p > 0$, needs at least $\frac{p}{2}(n - 1)\left(H_{n-1} - \pi/\sqrt{3p}\right)$ transmissions in expectation, where $H_{n-1} = \ln n + O(1)$ is the harmonic number. So push needs $\Omega(n \log n)$ transmissions, and push with a stopping age of $O(\log n)$ rounds uses $O(n \log n)$, so the bound for push is $\Theta(n \log n)$.

**Theorem 3 (Karp et al. 2000, Theorem 5.1).** "Any distributed rumor spreading algorithm guaranteeing that all but a fraction $o(1)$ of the players receive the rumor within $O(\ln n)$ rounds with constant probability needs to perform $\omega(n)$ transmissions in expectation."

## In plain words

A node that has the news and is on the phone with somebody does not know whether that person already knows. If it cannot use the name of the person to decide, every message it sends goes to a random person in effect. With push alone, the news must reach the last few people by chance, and to hit every one of them by chance you need about $n \ln n$ messages, as when you collect every card of a set. With pull added, the people who do not know call out, and the number of people who do not know falls much faster, but even then each burst of about $n$ messages can only square the fraction of people who do not know. Squaring a fraction until it is below $1/n$ takes about $\log \log n$ steps, so about $n \log \log n$ messages.

## Proof

**Proof of Theorem 2 (complete).** Call a player *hit* when some push has been sent to it. A player that is not the source can become informed only by a push, so if all players are informed, then every one of the $n - 1$ other players has been hit.

Order all pushes by round, and within a round in any fixed way. Consider a push from player $u$. Because the algorithm is address-oblivious, the decision of $u$ to push in this round does not depend on the address of its partner, and the partner is uniform on the other $n - 1$ players and independent of the past and of the other calls. So, given everything before it, the target of the push is uniform on $V \setminus \{u\}$. If $j$ players other than the source are not yet hit, none of them is informed, so $u$ is not one of them, and the push hits a new one with probability exactly $j/(n - 1)$.

Extend the sequence of pushes with extra uniform pushes after the algorithm stops, and let $C$ be the number of pushes until all $n - 1$ players other than the source are hit. By the remark above, $C$ is the sum of independent geometric variables with success probabilities $j/(n-1)$ for $j = n - 1, \ldots, 1$: this is the [coupon collector problem](/coupon-collector-problem/) with $n - 1$ coupons. So
$$\mathbb{E}[C] = (n - 1) H_{n-1}, \qquad \mathrm{Var}[C] \le \sum_{j=1}^{n-1} \left(\frac{n-1}{j}\right)^2 \le \frac{\pi^2}{6}(n - 1)^2.$$
Let $a = (n - 1)(H_{n-1} - \lambda)$. By Chebyshev's inequality, $\Pr[C < a] \le \pi^2/(6\lambda^2)$, which is $p/2$ for $\lambda = \pi/\sqrt{3p}$.

If the run informs all players, then $X \ge C$. So
$$\mathbb{E}[X] \ge a \Pr[X \ge a] \ge a \left(\Pr[\text{all informed}] - \Pr[C < a]\right) \ge a \left(p - \frac{p}{2}\right) = \frac{p}{2}(n - 1)\left(H_{n-1} - \frac{\pi}{\sqrt{3p}}\right).$$
For the upper bound: by [the push rumor spreading time](/push-rumor-spreading-time/), push that stops when the rumor is $C' \ln n$ rounds old, for a large constant $C'$, informs all players with high probability, and at most $n$ pushes are sent per round, so $X \le C' n \ln n$. $\blacksquare$

**Proof of Theorem 1 (sketch, following Karp et al.; this is not a complete proof).** The constants below are chosen for this page and differ from those of the paper. Assume $n \ge 4$.

1. *Phases.* Cut the run into consecutive phases. A *dense* phase is a single round with more than $n/2$ transmissions. A *sparse* phase is a maximal run of rounds with at most $n/2$ transmissions in total: it ends just before the round that would make the total exceed $n/2$. So two consecutive phases always contain more than $n/2$ transmissions together, and the first $i$ phases contain at least $(i - 1)n/4$ transmissions.
2. *One uninformed player in one phase.* Let $k$ be a player that is uninformed at the start of phase $i$, and let $u = U_{i-1} \ge 2$.
   - In a sparse phase, at most $n/2$ messages are sent, and since each one is sent without knowing the receiver, each reaches $k$ with probability at most $1/(n - 1)$. So $k$ receives the rumor with probability at most $\frac{n}{2(n-1)} \le \frac{2}{3}$, and it stays uninformed with probability at least $\frac{1}{3} \ge \frac{u}{8n}$.
   - In a dense phase, $k$ stays uninformed if it calls an uninformed player, with probability $\frac{u - 1}{n - 1} \ge \frac{u}{2n}$, and nobody calls $k$, with probability $(1 - \frac{1}{n-1})^{n-1} \ge \frac14$. The two events are independent, so the probability is at least $\frac{u}{8n}$.
3. *Expectation.* By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[U_i \mid U_{i-1} = u] \ge u^2/(8n)$.
4. *Concentration (cited).* Karp et al. note that the indicators "player $k$ stays uninformed" in one phase are negatively dependent, so a Chernoff bound applies; while $\mathbb{E}[U_i] \ge \ln^2 n$, this gives $U_i \ge \mathbb{E}[U_i]/2$ with probability $1 - n^{-\omega(1)}$. This step is cited, not proved here.
5. *Double exponential decay.* Let $w_i = U_i/n$. Steps 3 and 4 give $w_i \ge w_{i-1}^2/16$. With $y_i = w_i/16$, this is $y_i \ge y_{i-1}^2$, and $y_0 = (n-1)/(16n) \ge 1/32$, so $w_i \ge 32^{-2^i}$. To reach $w_i \le f$ the algorithm needs $2^i \ge \ln(1/f)/\ln 32$, that is, at least $\log_2 \ln (1/f) - 1.8$ phases.
6. *Count.* By step 1, these phases contain $\Omega(n \log \log (1/f))$ transmissions, with high probability, whenever the algorithm reaches the fraction $f$. Since that happens with constant probability, the expectation is $\Omega(n \log \log (1/f))$.

The idea is that one round can at most square the uninformed fraction, as pull does, and that a round in which fewer than about $n$ messages are sent cannot do even that much.

**Proof of Theorem 3 (cited).** Karp et al. compare the run with a simpler random process in which a small random sample of players acts independently for $O(\log \log n)$ rounds (their Lemmas 5.2 to 5.4, whose proofs the conference paper leaves out). They show that $O(n)$ transmissions in such a stretch of rounds lower the number of uninformed players only by a constant factor, and they iterate. This is cited, not proved here.

## Consequences

- **Push-pull is optimal among address-oblivious algorithms.** Push-pull with a stopping age of $\log_3 n + O(\log \log n)$ rounds uses $O(n \log \log n)$ transmissions (Karp et al., Theorem 2.1), and the median counter algorithm does the same without knowing $n$ exactly (Theorem 3.1). By Theorem 1, no address-oblivious algorithm does better by more than a constant factor.
- **Pull is the source of the saving.** Theorem 2 shows that the gap between $n \log n$ and $n \log \log n$ comes from pull: a push-only algorithm cannot avoid the coupon collector end.
- **Gossip is not message-optimal.** A deterministic broadcast on a known tree uses $n - 1$ messages. By Theorem 3, random phone calls cannot match this in $O(\log n)$ rounds, even if players use the addresses of their partners and attach any amount of information to the rumor.

## Tightness

- **Theorem 1 is tight** for $f = 1/n$ up to the constant: push-pull uses $O(n \log \log n)$ transmissions.
- **Theorem 2 is tight**, by the upper bound in its proof. In a simulation of push on the complete graph run until all players are informed, the number of transmissions per player is 6.94, 8.04 and 9.18 for $n = 256$, 1024 and 4096, which grows like $\ln n$ (5.55, 6.93, 8.32), while push-pull with the median counter stays near 9.7 for the same sizes.
- **Address-obliviousness is needed in Theorems 1 and 2.** If the source may use the addresses of its partners, it can wait until each other player has been its partner once and send the rumor to each player exactly then. This uses $n - 1$ transmissions, but $\Theta(n \log n)$ rounds (Karp et al., Section 1.3), because the source has only about two partners per round.
- **A round bound is needed in Theorem 3,** by the same example.

## History

Demers et al. (1987) observed in simulations that the fraction of sites that miss an update falls exponentially with the number of messages for all push variants, and that pull seems to do better. Karp, Schindelhauer, Shenker and Vöcking (2000) proved the $O(n \log \log n)$ upper bound for push-pull and the matching lower bound of Theorem 1, together with Theorem 3, which separates random phone call algorithms from deterministic broadcast. Their paper also states the $\Theta(n \ln n)$ cost of push; the time of push on the complete graph had been found by Frieze and Grimmett (1985) and Pittel (1987).

## References
