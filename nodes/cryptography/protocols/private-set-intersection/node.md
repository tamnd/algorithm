---
tag: P1QYT2
kind: problem
slug: private-set-intersection
name: Private set intersection
aliases:
- PSI
area: cryptography/protocols
level: advanced
summary: Two parties with sets X and Y compute X ∩ Y so that each learns only the intersection (and the set sizes). Solved by Diffie-Hellman blinding, by OPRFs from OT extension, or by circuits.
history:
  year: 1986
  people: [Catherine Meadows]
  note: Meadows gave a matching protocol based on Diffie-Hellman exponents in 1986; Huberman, Franklin and Hogg used it for set intersection in 1999. OT-based protocols since 2014 made PSI fast.
prereqs: [decisional-diffie-hellman, oblivious-transfer]
see_also: [secure-multiparty-computation, oblivious-transfer-extension, cuckoo-hashing, private-information-retrieval, bloom-filter, communication-complexity, homomorphic-encryption, yao-garbled-circuits]
sources:
  - paper: "Catherine Meadows, A more efficient cryptographic matchmaking protocol for use in the absence of a continuously available third party, IEEE Symposium on Security and Privacy 1986, pages 134 to 137"
    locator: the matching of items by commuting Diffie-Hellman exponents
  - paper: "Bernardo A. Huberman, Matt Franklin and Tad Hogg, Enhancing privacy and trust in electronic communities, ACM Conference on Electronic Commerce (EC) 1999, pages 78 to 86"
    locator: the commutative encryption protocol for set intersection
  - paper: "Michael J. Freedman, Kobbi Nissim and Benny Pinkas, Efficient private matching and set intersection, EUROCRYPT 2004, LNCS 3027, pages 1 to 19"
    locator: PSI by evaluating an encrypted polynomial whose roots are the client's items
  - paper: "Benny Pinkas, Thomas Schneider and Michael Zohner, Faster private set intersection based on OT extension, USENIX Security 2014, pages 797 to 812"
    locator: PSI from OT extension with hashing into bins, and the comparison of earlier protocols
  - paper: doi:10.1145/2976749.2978381
    title: "Vladimir Kolesnikov, Ranjit Kumaresan, Mike Rosulek and Ni Trieu, Efficient batched oblivious PRF with applications to private set intersection, CCS 2016, pages 818 to 829"
    locator: the batched OPRF from OT extension, and PSI with cuckoo hashing for the receiver and simple hashing for the sender
  - paper: "Yan Huang, David Evans and Jonathan Katz, Private set intersection, are garbled circuits better than custom protocols?, NDSS 2012"
    locator: PSI as a Boolean circuit evaluated with garbled circuits
  - paper: "Hao Chen, Kim Laine and Peter Rindal, Fast private set intersection from homomorphic encryption, CCS 2017, pages 1243 to 1255"
    locator: unbalanced PSI with communication sublinear in the larger set
  - paper: "Abhishek Bhowmick, Dan Boneh, Steve Myers, Kunal Talwar and Karl Tarbe, The Apple PSI system, technical summary, Apple, 2021"
    locator: the proposed PSI protocol for matching photos against a database of known images
---

In private set intersection (PSI), a client holds a set $X$ and a server holds a set $Y$. The client must learn $X \cap Y$, and nothing else about $Y$; the server must learn nothing about $X$ beyond its size. It is a special case of [secure multiparty computation](/secure-multiparty-computation/) that is used widely on its own: for contact discovery in messaging apps, for checking passwords against a list of leaked passwords, and for measuring how many people who saw an advertisement bought the product. The classic solution, from Meadows (1986) and Huberman, Franklin and Hogg (1999), blinds hashed items with Diffie-Hellman exponents. The fast modern solutions build an oblivious pseudorandom function from [OT extension](/oblivious-transfer-extension/) and use [cuckoo hashing](/cuckoo-hashing/), and handle sets of millions of items in seconds.

**Notation.** $X$ is the client's set with $|X| = n$, and $Y$ the server's set with $|Y| = m$. $\mathbb{G}$ is a group of prime order $q$ in which the [decisional Diffie-Hellman](/decisional-diffie-hellman/) problem is hard, and $H$ hashes items to $\mathbb{G}$. $\lambda$ is the security parameter.

## In plain words

Two companies want to know which customers they have in common, without showing each other their customer lists.

Sending hashes of the names does not work: if names are guessable, the other side hashes every possible name and checks. So each company locks every name with a secret key of its own, in a way where the order of the locks does not matter. The client locks its names and sends them; the server adds its lock and sends them back, and also sends its own names locked with its key. The client adds its lock to those.

Now every name carries both locks. Equal names give equal locked values, and different names give values that look random. The client compares the two lists and learns which of its names are shared, and nothing about the server's other names.

## Definition

**Functionality.** The ideal functionality $\mathcal{F}_{\mathrm{PSI}}$ receives $X \subseteq U$ from the client and $Y \subseteq U$ from the server, for a universe $U$ of items such as strings. It gives $X \cap Y$ to the client and $|X|$ to the server. The client also learns $|Y|$. The sizes are allowed leakage; to hide them, the parties pad their sets to agreed upper bounds.

**Security.** A protocol is a PSI protocol for [semi-honest](/semi-honest-model/) or [malicious](/malicious-adversary-model/) parties if it securely computes $\mathcal{F}_{\mathrm{PSI}}$ in that model. In the malicious model, a party may choose its input set freely, so the definition does not stop a client from putting many guesses in $X$; it only stops leakage beyond what $X \cap Y$ for the chosen $X$ reveals. The usual remedy is a bound on $|X|$ and a limit on repeated queries.

## Variants

- **Two-sided PSI.** Both parties learn $X \cap Y$.
- **PSI cardinality.** The client learns only $|X \cap Y|$. Used for ad conversion counts and for contact tracing statistics.
- **PSI with associated data, and PSI-sum.** Each server item carries a value, and the client learns the values of the matching items, or only their sum.
- **Circuit PSI.** The parties get secret shares of the intersection (or of a bit for each item), to be fed into a further secure computation, so that no one sees the intersection itself.
- **Unbalanced PSI.** $m \gg n$, for example a client with a phone book and a server with a billion users; the goal is communication sublinear in $m$.
- **Multiparty PSI.** Three or more parties intersect their sets.
- **Threshold PSI.** The output is revealed only when the intersection is large enough, or the items only when enough matches exist.

## Examples

**Diffie-Hellman PSI on a toy group.** The group is the subgroup of squares modulo the safe prime $p = 1019$, of order $q = 509$. $H(x)$ is SHA-256 of the item, reduced mod $p$ and squared. The client has $X = \{\text{alice}, \text{bob}, \text{carol}\}$ and key $a = 7$; the server has $Y = \{\text{bob}, \text{dave}\}$ and key $b = 11$.

| item | $H(\cdot)$ | client sends $H(x)^a$ | server returns $H(x)^{ab}$ | server sends $H(y)^b$ | client computes $H(y)^{ba}$ |
|---|---|---|---|---|---|
| alice | 1013 | 289 | 411 | | |
| bob | 803 | 516 | 23 | 149 | 23 |
| carol | 49 | 816 | 424 | | |
| dave | 953 | | | 500 | 861 |

The client's doubly blinded values are $\{411, 23, 424\}$ and the server's are $\{23, 861\}$. The common value 23 belongs to bob, so the client outputs $\{\text{bob}\}$. The value 500 for dave is $H(\text{dave})^{11}$: without $b$, the client cannot test a guess against it. The server sees $\{289, 516, 816\}$, three values that look random to it without $a$. All values are mod 1019; this group is far too small for any security.

**Why plain hashing fails.** If the server sends $\mathrm{SHA\text{-}256}(y)$ for each $y$, a client can hash every candidate in a small universe (all 10000 four-digit codes, or all phone numbers of a country) and learn all of $Y$. The test does this for 50 codes out of 10000.

**The code.** The page's Python file implements two semi-honest protocols. The first is the Diffie-Hellman PSI above, in a 64-bit safe-prime group for the correctness tests and the 1019 group for statistical tests: 20 random pairs of sets are checked against the plain intersection, the message count $2n + m$ is checked, and over 8000 runs the server's value for an item outside $X$ is checked to be uniform on the group, for two different server sets with the same intersection. The second is an OPRF-based PSI in the layout of KKRT: the client puts each item into one of 3 bins by cuckoo hashing with $1.5n$ bins, the server puts each item into all 3 of its bins, each bin has its own PRF key, and the client gets one OPRF value per bin. Its OPRF is the Diffie-Hellman OPRF $H(x)^{k}$ with blinding, not the OT-based OPRF of KKRT, so it shows the hashing structure but not the speed. There are no official test vectors for PSI. The code is for study only and is not constant time; for real data use a maintained library, such as the PSI protocols in libOTe or Microsoft's APSI for the unbalanced case.

## Known algorithms

| protocol | security | communication | computation | main idea |
|---|---|---|---|---|
| Naive hashing | none for small universes | $O(m)$ hashes | $O(n + m)$ hashes | send $H(y)$; broken by guessing |
| Diffie-Hellman PSI (Meadows 1986; Huberman, Franklin and Hogg 1999) | semi-honest, DDH in the random oracle model | $2n + m$ group elements | $O(n + m)$ exponentiations | commuting exponents $H(x)^{ab} = H(x)^{ba}$ |
| Freedman, Nissim and Pinkas (2004) | semi-honest (malicious versions exist) | $O(n + m)$ ciphertexts | $O(nm)$, or less with hashing | the server evaluates an encrypted polynomial with roots $X$ |
| Pinkas, Schneider and Zohner (2014) | semi-honest | $O((n + m)\lambda)$ bits, with larger constants | symmetric key | OT extension and hashing into bins |
| KKRT (Kolesnikov, Kumaresan, Rosulek and Trieu 2016) | semi-honest | about $3m$ short PRF values plus OT extension on a little more than $n$ bins | symmetric key | batched OPRF from OT extension, [cuckoo hashing](/cuckoo-hashing/) for the client |
| Circuit PSI (Huang, Evans and Katz 2012, and later) | semi-honest or malicious | larger | garbled circuits | a sort-compare-shuffle or hashing circuit, output in shares |
| Chen, Laine and Rindal (2017) | semi-honest | sublinear in $m$ | homomorphic encryption | unbalanced PSI with leveled [homomorphic encryption](/homomorphic-encryption/) |

**Diffie-Hellman PSI.** The client sends $H(x)^a$ for each $x \in X$ in random order. The server returns $H(x)^{ab}$ in the same order, and sends $H(y)^b$ for each $y \in Y$. The client raises those to $a$ and outputs the $x$ whose $H(x)^{ab}$ appears among the $H(y)^{ba}$. Its cost is small in communication and it is simple, so it is still used where the sets are small or bandwidth matters, as in Google's Password Checkup. Its security for semi-honest parties rests on DDH with $H$ as a random oracle.

**OPRF-based PSI.** An oblivious PRF lets the client learn $F_k(x)$ for its items while the server keeps $k$ and learns nothing. Then the server sends $\{F_k(y)\}$ and the client compares. KKRT build a batched OPRF for many keys from OT extension, at a cost close to one OT each. Cuckoo hashing puts each client item into one of a little more than $n$ bins, with at most one item per bin, so the client needs one OPRF per bin; the server puts each item into all 3 of its candidate bins and sends 3 values per item. Later work replaced the OT extension by vector OLE and the bins by oblivious key-value stores, and is faster still.

## Bounds

- **Communication.** Any PSI protocol solves set disjointness, whose randomized [communication complexity](/communication-complexity/) for sets of size $k$ is $\Theta(k)$ bits. So PSI needs $\Omega(\min(n, m))$ bits of communication even without privacy. Balanced protocols reach $O((n + m)\lambda)$.
- **Public-key operations.** The OT-based protocols need only $O(\lambda)$ public-key operations in total, for the base OTs; Diffie-Hellman PSI needs $\Theta(n + m)$ of them.
- **Unbalanced sets.** With homomorphic encryption, communication can be sublinear in $m$ (but at least linear in $n$), at the cost of heavy server computation.
- **Leakage of sizes.** Without padding, $|X|$ and $|Y|$ are revealed by the message counts.

## Reductions

- **From general MPC.** PSI is a function, so [Yao's garbled circuits](/yao-garbled-circuits/) or any general protocol computes it. Circuit PSI does this with a circuit of size $O((n + m) \log(n + m))$ or less with hashing.
- **From an OPRF.** Given an OPRF, PSI costs one OPRF evaluation per client item (or bin) and $m$ PRF values from the server. An OPRF in turn comes from [oblivious transfer](/oblivious-transfer/) (KKRT) or from DH blinding.
- **To keyword PIR.** Unbalanced PSI with a one-item client is close to keyword [private information retrieval](/private-information-retrieval/), and the protocols share techniques.

## Applications

Contact discovery, where a messaging app finds which of a user's contacts use it. Password breach alerting, as in Google's Password Checkup, where a client checks a hashed password against a set of leaked ones by Diffie-Hellman blinding. Ad conversion measurement, with PSI-sum over purchase records. Exposure notification and contact tracing research. Apple's 2021 proposal to detect known abuse images on devices used a threshold PSI protocol, and Apple dropped the plan after public criticism.

## References
