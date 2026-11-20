---
tag: 5Q1GE1
kind: problem
slug: unsourced-random-access
name: Unsourced random access
aliases:
- URA
area: communications/multiple-access-and-spread-spectrum
level: research
summary: Many users send short messages with the same codebook, and the receiver must find the list of messages but not who sent them.
prereqs: [coded-slotted-aloha, medium-access-control]
see_also: [compressed-sensing, approximate-message-passing, orthogonal-matching-pursuit, additive-white-gaussian-noise-channel, energy-per-bit-to-noise-density-ratio, successive-interference-cancellation, massive-mimo, polar-code]
sources:
  - paper: doi:10.1109/ISIT.2017.8006984
    title: Yury Polyanskiy, A perspective on massive random-access, IEEE International Symposium on Information Theory (ISIT), Aachen, 2017
    locator: pp. 2523 to 2527, Definition 1 (the random-access code with one codebook and the per-user error), Theorem 1 (the random coding bound) and Section III with Fig. 1 (100 bits in 30000 real channel uses at a per-user error of 0.1)
  - paper: doi:10.1109/ISIT.2017.8006985
    title: Or Ordentlich and Yury Polyanskiy, Low complexity schemes for the random access Gaussian channel, IEEE International Symposium on Information Theory (ISIT), Aachen, 2017
    locator: pp. 2528 to 2532, the T-fold ALOHA scheme (random sub-blocks as in slotted ALOHA, with a code inside each sub-block that decodes up to T colliding users)
  - paper: doi:10.1109/TIT.2020.3012948
    title: Vamsi K. Amalladinne, Jean-Francois Chamberland and Krishna R. Narayanan, A coded compressed sensing scheme for unsourced multiple access, IEEE Transactions on Information Theory 66(10), 2020
    locator: pp. 6509 to 6533 (the message split into pieces with parity bits of a tree code, compressed sensing recovery in each sub-block and the stitching of the pieces)
---

Unsourced random access (URA) is the problem of decoding many short messages from a large population of devices that share one channel and one codebook. A small, changing set of $K_a$ users is active. Each active user sends a message of $k$ bits, about 100, in a frame of $n$ channel uses, using the same encoder as everyone else and without any coordination. The receiver must output the list of messages that were sent, but not who sent them. If the identity matters, the user puts it inside its message. Polyanskiy posed the problem in 2017 for machine-type traffic, where devices wake up rarely to send a few bits, and the cost of telling the network who is active is larger than the data. The error is counted per user, and the goal is the smallest energy per bit for a given $K_a$, $k$, $n$ and target error. This page is about the problem. [Coded slotted ALOHA](/coded-slotted-aloha/) is a scheme for the collision channel, in which each user also sends one packet without coordination; many URA schemes use it as their outer layer.

## In plain words

Picture thousands of sensors. At any moment, a few hundred of them have one short reading to send, and they all speak at once into the same radio channel. Giving each sensor its own codebook would mean the receiver first has to find out which of the thousands are speaking. Instead, all sensors use one shared book of codewords. The receiver hears the sum of the chosen codewords plus noise and must list which codewords are in the sum. It does not care which sensor sent which one, so the problem is about finding a set, not a set of names.

## Definition

**Channel.** Following Polyanskiy, the channel is real and Gaussian. With $K_a$ active users, the receiver gets

$$ Y = \sum_{i=1}^{K_a} c_{W_i} + Z, \qquad Z \sim \mathcal N(0, I_n), $$

where $W_i$ is the message of user $i$, uniform on $\{1, \ldots, M\}$ with $M = 2^k$, and independent across users. The codewords $c_1, \ldots, c_M \in \mathbb R^n$ form one codebook, common to all users, with the power constraint $\|c_j\|^2 \le nP$.

**Code.** An $(M, n, \varepsilon)$ random-access code (Definition 1 in Polyanskiy's paper) is an encoder, common to all users, and a decoder that maps $Y$ to a list $\hat L$ of $K_a$ messages. The decoder knows $K_a$ but not the active users. The error event of user $i$ is $E_i = \{W_i \notin \hat L\} \cup \{W_i = W_j \text{ for some } j \ne i\}$, so a message that another user also sent counts as an error. The per-user probability of error is

$$ P_e = \frac{1}{K_a} \sum_{i=1}^{K_a} \Pr[E_i], $$

and the code must have $P_e \le \varepsilon$. Each noise sample has variance 1, so the one-sided noise density is $N_0 = 2$ in these units. The energy per bit is $E_b = nP/k$, and the figure of merit is

$$ \frac{E_b}{N_0} = \frac{nP}{2k}. $$

**Benchmark.** Polyanskiy's comparison (Section III, Fig. 1) used $k = 100$ bits, $n = 30000$ real channel uses and $\varepsilon = 0.1$. Later papers mostly use the same $k$ and $n$ with $\varepsilon = 0.05$, and $K_a$ from about 25 to 300. For each $K_a$, a scheme is judged by the smallest $E_b/N_0$ at which it reaches the target.

## Variants

- **Fading and many antennas.** With Rayleigh fading and a large number of receive antennas, each user has an unknown channel vector, and the decoder can use the covariance of the received signal. This lets far more users be active in the same frame, as in [massive MIMO](/massive-mimo/).
- **Unknown number of users.** The decoder does not know $K_a$. Then false alarms, messages on the list that nobody sent, are counted as a second error measure.
- **Asynchronous users.** Users are not aligned to frame boundaries, or their carriers differ.
- **Sourced random access.** Each user has its own codebook, and the receiver must also say who is active. This is activity detection with multiuser decoding. It is a different problem, because the receiver must search a set of identities as large as the whole population.
- **Complex baseband.** With complex noise of density $N_0$ per complex symbol, $n$ complex uses equal $2n$ real ones, and the definitions change accordingly.

## Examples

- **Benchmark scale.** With $k = 100$ bits, the codebook has $2^{100} \approx 1.3 \times 10^{30}$ codewords. No decoder can test every codeword, so every practical scheme splits the message or the frame into smaller parts.
- **Same message from two users (closed form).** By the union bound over pairs, the probability that two of $K_a$ users pick the same message is at most $\binom{K_a}{2}/2^k$. For $K_a = 300$ and $k = 100$ this is $3.5 \times 10^{-26}$, so lists of distinct messages lose almost nothing.
- **Sum-rate estimate (heuristic).** If the receiver had to carry $K_a k$ bits through $n$ real uses with total power $K_a P$, it would need $K_a k \le \frac{n}{2}\log_2(1 + K_a P)$. This gives $E_b/N_0 \ge \frac{n}{2k} \cdot \frac{2^{2K_a k/n} - 1}{K_a}$. At the benchmark, it is $-0.55$ dB for $K_a = 100$ and $1.76$ dB for $K_a = 300$. The estimate ignores the target $\varepsilon$ and the finite length, so it is only a rough lower limit, not a theorem about these codes.
- **Slotted ALOHA baseline.** Split the frame into $V$ slots, and let each user send a single-user code in one random slot. A user is lost if another user picks its slot, which has probability $1 - (1 - 1/V)^{K_a - 1}$ (closed form). To keep this below $0.05$ with $K_a = 300$ needs $V \ge 5830$ slots, about 5 real uses each, which is far too short to carry 100 bits. So plain ALOHA cannot meet the benchmark at large $K_a$.

## Known algorithms

- **ALOHA with a strong single-user code.** Polyanskiy compared slotted ALOHA and treating interference as noise with his bound and found both far from it when $K_a$ is large. They remain the baseline.
- **T-fold ALOHA.** Ordentlich and Polyanskiy split the frame into sub-blocks. Each user picks one at random, as in slotted ALOHA, and inside a sub-block a code for the sum of up to $T$ codewords decodes all users when at most $T$ collide. This was the first low-complexity scheme with a clear gain over ALOHA.
- **Coded compressed sensing.** Amalladinne, Chamberland and Narayanan split the $k$ bits of each user into pieces and add parity bits of a tree code that link the pieces. Each piece is sent in its own sub-block, as a column of a small sensing matrix. A [compressed sensing](/compressed-sensing/) decoder, such as non-negative least squares or [orthogonal matching pursuit](/orthogonal-matching-pursuit/), finds the set of pieces in each sub-block, and a tree decoder joins pieces that satisfy the parity checks into whole messages.
- **Approximate message passing with an outer code.** Later schemes view the problem as a sparse regression code shared by all users and decode with [approximate message passing](/approximate-message-passing/), with the outer tree code inside the iterations.
- **Spreading with successive cancellation.** The first bits of a message pick a spreading sequence, and the rest are encoded with a [polar code](/polar-code/) or an LDPC code. The receiver detects the sequences, decodes the strongest users and removes them with [successive interference cancellation](/successive-interference-cancellation/).
- **Coded slotted ALOHA as the outer layer.** Each user sends several copies of its message in random slots, as in [coded slotted ALOHA](/coded-slotted-aloha/), and a $T$-user code works inside each slot. Decoded messages are cancelled from their other slots.

## Bounds

- **Achievability (theorem).** Theorem 1 of Polyanskiy is a random coding bound. The codewords are drawn independently and Gaussian, and the decoder chooses the $K_a$ codewords whose sum is closest to $Y$. The bound counts the events in which some of the decoded codewords are wrong, adds the probability that a codeword breaks the power limit, and adds the collision term above. It gives the smallest $E_b/N_0$ known to be possible for each $K_a$ at the benchmark. For small $K_a$, the required $E_b/N_0$ hardly grows with $K_a$, which means that well designed codes can almost cancel the interference among users.
- **Collision term (closed form).** Any scheme in which users with equal messages send equal signals loses at most $\binom{K_a}{2}/2^k$ to identical messages.
- **Converse (heuristic).** The sum-rate estimate in the examples is the simplest lower limit. Tighter converses add finite-length terms and the per-user error.

## Reductions

- **To support recovery in compressed sensing.** Put the $M$ codewords as the columns of an $n \times M$ matrix $A$. Then $Y = A x + Z$, where $x \in \{0, 1, 2, \ldots\}^M$ counts the users of each message and has at most $K_a$ nonzero entries. Finding the list is finding the support of $x$. With $M = 2^{100}$, the dimension is too large, which is why coded compressed sensing splits the message.
- **To the $T$-user multiple access channel.** If users choose random slots, each slot sees a random number of users. A code that decodes up to $T$ users per slot turns URA into a slotted ALOHA problem in which a slot fails only above $T$ users.
- **From sourced access.** A user can put its identity in its $k$ bits. So an unsourced code also solves the sourced problem, at the cost of the identity bits in each message, and the receiver never needs to search the full population.

## Applications

The target is massive machine-type communication: sensors, meters and trackers that send a few bytes at rare times, in very large numbers. The base station does not grant a slot for each packet, so the scheme is grant-free, and it must work with one shared transmitter design. The same problem appears in satellite return links for many terminals, where [coded slotted ALOHA](/coded-slotted-aloha/) is already used, and in any system where only the content of each message matters.

## References
