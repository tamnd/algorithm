---
tag: 5V20J4
kind: problem
slug: anonymous-communication
name: Anonymous communication
aliases:
- sender anonymity
- traffic analysis resistance
area: cryptography/protocols
level: advanced
summary: Send messages over a network so that observers cannot tell who sent a message, who received it, or who talks to whom, even when they see every packet.
prereqs: [public-key-encryption, authenticated-encryption]
see_also: [mix-network, dining-cryptographers, secure-messaging, signal-protocol, private-information-retrieval, ring-signature, group-signature, random-permutation]
sources:
  - url: "https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf"
    title: Andreas Pfitzmann and Marit Hansen, A terminology for talking about privacy by data minimization, version 0.34, 2010
    locator: the definitions of anonymity, the anonymity set, unlinkability, undetectability and unobservability, and of sender, recipient and relationship anonymity
  - paper: "Roger Dingledine, Nick Mathewson and Paul Syverson, Tor: the second-generation onion router, USENIX Security Symposium 2004, pages 303 to 320"
    locator: the design of circuits built hop by hop, fixed-size cells, directory servers, and the threat model that excludes a global passive adversary and end-to-end timing correlation
  - paper: "Debajyoti Das, Sebastian Meiser, Esfandiar Mohammadi and Aniket Kate, Anonymity trilemma: strong anonymity, low bandwidth overhead, low latency, choose two, IEEE Symposium on Security and Privacy 2018"
    locator: the lower bound that relates latency, the fraction of cover traffic and strong anonymity against a global passive adversary
  - paper: doi:10.1145/358549.358563
    title: David Chaum, Untraceable electronic mail, return addresses, and digital pseudonyms, Communications of the ACM 24(2), 1981, pages 84 to 90
    locator: the mix, which hides the link between its inputs and outputs, and untraceable return addresses
  - paper: doi:10.1007/BF00206326
    title: David Chaum, The dining cryptographers problem, unconditional sender and recipient untraceability, Journal of Cryptology 1(1), 1988, pages 65 to 75
    locator: sender anonymity that holds against an adversary of any power
  - paper: "David M. Goldschlag, Michael G. Reed and Paul F. Syverson, Hiding routing information, Information Hiding 1996, LNCS 1174, pages 137 to 150"
    locator: onion routing with layered encryption, in which each router learns only its neighbors
  - paper: "Andrei Serjantov and George Danezis, Towards an information theoretic metric for anonymity, Privacy Enhancing Technologies 2002, LNCS 2482, pages 41 to 53"
    locator: the entropy of the attacker's distribution over possible senders as the effective size of the anonymity set
  - paper: doi:10.1145/2508859.2516651
    title: Aaron Johnson, Chris Wacek, Rob Jansen, Micah Sherr and Paul Syverson, Users get routed, traffic correlation on Tor by realistic adversaries, ACM CCS 2013, pages 337 to 348
    locator: the estimates of how soon a relay adversary or a network adversary sees both ends of a Tor circuit and correlates them
---

Anonymous communication is the problem of sending messages over a network so that an observer cannot tell who sent a message, who received it, or which pairs of people talk to each other. Encryption alone does not solve it: [secure messaging](/secure-messaging/) hides what is said, but the source and destination addresses, the times and the sizes of packets still show who talks to whom, which is often as sensitive as the content. A solution must hide this metadata from an adversary who watches part of the network or all of it, and who may run some of the servers. The two classic designs are Chaum's [mix network](/mix-network/) (1981) and Chaum's [dining cryptographers](/dining-cryptographers/) protocol (1988). The most used system is Tor, a low-latency onion routing network.

## In plain words

Suppose that you mail a letter to a clinic. Even if nobody opens it, the postman sees your address on the back and the clinic on the front. That alone tells a story.

To hide it, you can put the letter in three envelopes, one inside the other, addressed to three helpers in turn. Each helper opens one envelope and passes on what is inside. The first helper knows you but not the clinic, and the last knows the clinic but not you.

This works only if many people send letters through the same helpers at the same time. If a watcher sees you post a letter at 9:00 and a letter reach the clinic at 9:01, and nobody else was posting, the envelopes do not help. Anonymity needs a crowd, and it costs time or extra traffic.

## Definition

There are $n$ users who send messages through a network to receivers, and an adversary. The adversary may observe some links or all of them (a *global passive* adversary), may control some relays or receivers, and may delay, drop or inject messages. It sees the times, sizes and endpoints of what crosses the links it watches, but cannot break the encryption.

- **Anonymity set.** The set of users who could have done an action, from the adversary's view. A user is anonymous if the adversary cannot pick them out of this set.
- **Sender anonymity.** For a given message, the adversary cannot tell which user sent it, better than by guessing within the anonymity set.
- **Receiver anonymity.** For a given message, the adversary cannot tell which user received it.
- **Relationship anonymity (unlinkability of sender and receiver).** The adversary may know that Alice sends and that Bob receives, but cannot tell whether Alice sends to Bob.
- **Unobservability.** The adversary cannot even tell whether a user sends at all; it needs cover traffic.

A common game-based form: the adversary picks two scenarios that differ only in who sends to whom, the system runs one of them at random, and the adversary must guess which; the scheme is secure if its advantage is negligible. A weaker, measured form gives the adversary's probability distribution over the anonymity set and takes its entropy as the effective size of the set (Serjantov and Danezis, and Díaz et al., PET 2002).

## Variants

- **Low latency and high latency.** Web browsing and voice need answers within a second, so low-latency systems such as Tor forward each cell at once. Email and messaging can wait, so mixes may hold messages for minutes and reorder them in batches.
- **Local and global adversary.** Tor protects against an adversary who sees only part of the network. Mix networks and DC-nets aim to protect against one who sees every link.
- **One-shot and long-term.** A single message can hide in a crowd, but a user who talks to the same receiver often can be found by an *intersection* or *statistical disclosure* attack, which links the times when the user is active with the times when the receiver gets messages.
- **Information-theoretic and computational.** DC-nets give sender anonymity against an adversary of any power; mixes and onion routing rest on encryption.
- **Anonymous broadcast, anonymous reply and anonymous storage.** Sender anonymity for a public message, untraceable return addresses, and reading from a server without saying what is read, as in [private information retrieval](/private-information-retrieval/).

## Examples

**A toy onion circuit.** The Python code builds a network of relays with X25519 keys. A client builds a circuit through a guard, a middle relay and an exit, one hop at a time, and sends each cell inside three layers of authenticated encryption. Each relay removes one layer and sees only its two neighbors: the guard sees the client and the middle relay, the middle relay sees the guard and the exit, and the exit sees the middle relay and the destination. The plaintext appears only on the link from the exit to the destination, and the circuit identifier changes at each hop. A changed cell fails the authentication check at the first relay.

**A timing correlation attack.** In the same code, 16 clients each send 10 cells at random times through their own circuits over 8 relays, each to their own website. The attacker sees only the times on the links from clients to guards and from exits to websites, not the content. For each website it picks the client with the most cells that entered the network up to 0.15 s before a cell reached the website. When relays forward at once, the attack names the right client for all 16 websites, while chance is 1 in 16. When each relay holds each cell for a random time with a mean of one second, as a mix does, the same attack names the right client for 1 website in 16, the rate of a guess. Longer observation would still let a statistical attack recover part of the pattern.

The code is for study only. It is not constant time, has no link encryption and no padding, and its cells become shorter at each hop, which tells a relay where it is on the path. It derives hop keys with a one-way handshake, a simplification of Tor's ntor handshake. For real use, use Tor (or Arti, the Rust version of Tor). There are no official test vectors for such a toy network, so the tests check the X25519 copy against RFC 7748 and check the properties above.

**The anonymity set and its entropy.** Suppose that four users could have sent a message, and that the attacker's analysis gives them the probabilities $1/2$, $1/6$, $1/6$ and $1/6$. The entropy is $\frac12 \log_2 2 + 3 \cdot \frac16 \log_2 6 \approx 1.79$ bits, less than the $2$ bits of a uniform set of four. The effective set size is $2^{1.79} \approx 3.46$ users.

## Known algorithms

- **[Mix networks](/mix-network/) (Chaum 1981).** A mix collects a batch of encrypted messages, removes a layer of encryption or re-encrypts them, and sends them out in a random order. A cascade or a network of mixes hides the link if one mix is honest. Verifiable shuffles prove that a mix did not drop or change messages. Sphinx gives a compact packet format, and Loopix adds cover traffic and random delays.
- **[Dining cryptographers networks](/dining-cryptographers/) (Chaum 1988).** Users who share secret keys in pairs each broadcast the XOR of their keys, and the sender also XORs in the message. Everyone learns the message and no one learns the sender, even with unlimited computing power. The cost is a broadcast from every user for every message, and one user can jam the channel.
- **Onion routing and Tor.** Onion routing (Goldschlag, Reed and Syverson, 1996) sends each packet through a path of relays with one layer of encryption per relay. Tor (Dingledine, Mathewson and Syverson, USENIX Security 2004) builds circuits hop by hop with ephemeral keys for forward secrecy, uses fixed-size cells, and picks paths from a list of volunteer relays published by directory authorities. It forwards at once and adds no cover traffic, so it does not protect against an adversary who sees both ends of a circuit.
- **Crowds (Reiter and Rubin, 1998).** Each user forwards a request to a random member of the crowd or to the server, with a fixed probability, which hides the sender from the server and from some members.
- **Systems for messaging.** Vuvuzela, Pung, Riposte and others give metadata privacy for messages with differential privacy, private information retrieval or DC-net ideas, at the cost of latency.

## Bounds

- **The trilemma.** Das, Meiser, Mohammadi and Kate (IEEE S&P 2018) showed that against a global passive adversary a protocol cannot have strong anonymity, low latency and low bandwidth overhead at the same time. Roughly, when each message may wait at most $\ell$ rounds and only a fraction $\beta$ of users send in a round, strong anonymity is impossible when $2\ell\beta < 1$. So Tor, with low latency and no cover traffic, cannot resist a global adversary.
- **End-to-end correlation.** An adversary who sees the traffic entering and leaving a low-latency network can link the two ends from timing and volume alone, as in the example above. Johnson et al. (CCS 2013) estimated that a typical Tor user who runs for months is likely to have some circuits seen at both ends by an adversary that runs relays or a large autonomous system.
- **Cost of DC-nets.** For $n$ users, each message costs $n$ broadcasts, or $O(n^2)$ messages without a broadcast channel, because every user must send in every round to hide the sender.
- **Entropy.** The degree of anonymity is at most $\log_2$ of the size of the anonymity set, and is equal to it only when the attacker's distribution is uniform.
- **Long-term exposure.** If a user keeps talking to the same small set of receivers, intersection and disclosure attacks find them after a number of rounds that grows with the size of the anonymity set, whatever the mix design.

## Reductions

- Sender anonymity for a broadcast reduces to a DC-net, or to a verifiable shuffle of the messages of all users.
- Receiver anonymity reduces to broadcast: send every message to everyone, encrypted to the receiver, so only the receiver can read it. Private information retrieval cuts the cost of the download.
- Relationship anonymity reduces to a mix network or to onion routing, which hide the link between the incoming and outgoing messages.
- Anonymous replies reduce to Chaum's untraceable return addresses, in which the receiver of a message gets a sealed route back to the sender.
- Anonymity in a protocol also depends on the layers above: a message signed with an ordinary signature names its sender, so anonymous systems use [ring signatures](/ring-signature/), [group signatures](/group-signature/) or no signatures.

## Applications

Tor protects millions of daily users, including journalists, activists and people who want to avoid tracking, and it hosts onion services whose location is hidden. Mix networks are used for electronic voting, where a verifiable shuffle separates the voters from their ballots before the tally, and in some newer messaging and cryptocurrency privacy networks. DC-net ideas appear in anonymous group messaging systems such as Dissent. Messaging apps such as Signal limit metadata with sealed sender, which hides the sender from the server for each message but not the network addresses.

## References
