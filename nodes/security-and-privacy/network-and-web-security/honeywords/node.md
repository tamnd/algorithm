---
tag: JHVSNH
kind: technique
slug: honeywords
name: Honeywords
aliases:
- honeyword scheme
area: security-and-privacy/network-and-web-security
level: advanced
summary: "Stores each password hash among decoy hashes, so that a thief who cracks the file and logs in with a decoy sets off an alarm."
history:
  year: 2013
  people: [Ari Juels, Ronald L. Rivest, Ding Wang, Haibo Cheng, Ping Wang, Jeff Yan, Xinyi Huang]
  note: "Juels and Rivest proposed honeywords and the honeychecker in 2013. Wang, Cheng, Wang, Yan and Huang showed in 2018, on 104 million real passwords, that the generators of the original paper are far from flat."
prereqs: [password-hashing]
see_also: [markov-password-model, pcfg-password-model, base-rate-fallacy-intrusion-detection, message-authentication-code, misuse-detection, intrusion-detection-problem, min-entropy]
sources:
  - paper: "Ari Juels and Ronald L. Rivest, Honeywords, making password-cracking detectable, ACM CCS 2013, pages 145 to 160"
    locator: "the sweetword list and the honeychecker, flatness, the generators (chaffing by tweaking, chaffing with a password model, take-a-tail and hybrids), the choice k = 20, and the discussion of denial of service"
  - paper: "Ding Wang, Haibo Cheng, Ping Wang, Jeff Yan and Xinyi Huang, A security analysis of honeywords, NDSS 2018, doi:10.14722/ndss.2018.23142"
    locator: "the attacks that tell the real password from the honeywords, measured on 104 million real passwords, and the finding that the four main generators of Juels and Rivest are not flat"
---

Honeywords are decoy passwords stored next to the real one, so that the theft of a password file can be detected. For each user $u$ the server keeps a list of $k$ sweetwords, as salted slow [password hashes](/password-hashing/): one is the real password and the other $k - 1$ are honeywords made by a generator. The index $c(u)$ of the real one is kept apart, in a small separate server called the honeychecker. A thief who steals the file and cracks all $k$ hashes still does not know which one is real. If the thief logs in with a honeyword, the honeychecker sees a wrong index and raises an alarm: the file has leaked. Juels and Rivest (2013) proposed the scheme with $k = 20$. Its security depends on the generator: the honeywords must look as likely to be the real password as the real one does. The scheme does not make cracking harder; it makes the use of a cracked file detectable. Wang et al. (2018) showed, on 104 million real passwords, that the simple generators of the original paper are easy to tell apart from real passwords, so a generator needs a good model of human passwords.

## In plain words

A site keeps scrambled copies of passwords. If a thief steals that file, the thief can try to unscramble it offline, and the site may never learn about it.

With honeywords, the site stores many fake passwords for each user next to the real one, all scrambled the same way. Only a second, separate machine knows which one is real. A thief who unscrambles the file sees, say, twenty passwords for each user and must guess which one works. When someone logs in with one of the fakes, the second machine knows at once that the file was stolen. For this to work, the fakes must look just like passwords that real people choose.

## When it applies

- The site stores password hashes and wants to detect a leak of the hash file, which an offline attack does not reveal.
- The site can run a honeychecker: a small, separately administered system that stores only the index $c(u)$ for each user and answers one question. It must not share the failure modes of the login server, or a thief gets both.
- The site has a generator whose honeywords are plausible for its users, for example from a [password model](/markov-password-model/) trained on a similar population.
- The site has a policy for alarms: what to do when a honeyword is used, and how to tell a real leak from a user who mistypes.

It does not help when the attacker gets the plaintext passwords elsewhere, for example by phishing or from another site where the user reused the password: such a thief knows the real one.

## The template

```pseudo id=main
REGISTER(u, p)
L1  h_1, ..., h_{k-1} ← GEN(p, k - 1)            ▷ honeywords, all different from p
L2  c ← a uniform random index in 1..k
L3  W_u ← the list of p and the h_i, with p at position c
L4  store salted slow hashes of W_u on the login server; send (u, c) to the honeychecker

LOGIN(u, q)
L5  j ← the index with H(salt_u, q) = stored hash j of u, or none
L6  if j = none then reject                       ▷ an ordinary wrong password
L7  send (u, j) to the honeychecker
L8  if j = c(u) then accept
L9  else raise an alarm, and follow the alarm policy for u
```

Lines L1 to L4 run when the user sets a password. The login server never stores $c(u)$, and the honeychecker never sees a password or a hash. The channel between the two should be authenticated, for example with a [MAC](/message-authentication-code/), so that a thief on the login server cannot fake the honeychecker's answers.

**Flatness.** A generator is $\varepsilon$-flat if no attacker who sees the sweetword list of a user can pick the real password with probability more than $\varepsilon$. The best possible value is $1/k$, called perfectly flat. Against a perfectly flat generator, an attacker who cracked the file and tries one sweetword for one user is caught with probability $1 - 1/k$, which is $0.95$ for $k = 20$. To avoid all alarms over $m$ users with one try each, the attacker must be lucky $m$ times, with probability $(1/k)^m$. In practice the success of the best attacker against a generator is measured on real password lists, and it is a [min-entropy](/min-entropy/) style quantity of the list given the generator.

## Classic examples

- **Chaffing by tweaking.** GEN changes the last $t$ characters of the real password within their character class, for example the digits of `blue42` to `blue17`, `blue93` and `blue08`. It is simple but not flat: a real password such as `march1985` stands out from tweaks such as `march1932` that no person chose, as Wang et al. showed.
- **Chaffing with a password model.** GEN draws honeywords from a model of human passwords, such as a [Markov model](/markov-password-model/) or a [PCFG model](/pcfg-password-model/) trained on a large list. The honeywords are then as likely as real passwords under the model, but they are unrelated to the user, so personal data about the user can still point to the real one.
- **Take-a-tail.** The system chooses a random tail, for example three digits, and asks the user to append it to the chosen password. The honeywords use other random tails. The tail is truly random, so this generator is flat with respect to the tail, at the cost of a harder password for the user.
- **Hybrid generators.** Juels and Rivest also combine a model-based base word with tweaked tails, to get both plausible structure and many variants.
- **Detection as a signal.** A honeyword alarm is a near-certain signal of a leak, because a user who mistypes is unlikely to type one of the other sweetwords. This makes it a detector with a low false alarm rate, which matters because of the [base rate fallacy](/base-rate-fallacy-intrusion-detection/) of most [intrusion detectors](/intrusion-detection-problem/).

## Variations

- **Alarm policies.** On an alarm, the system can block the account, let the login proceed into a monitored session, ask for a second factor, or only log the event and reset all passwords. The choice trades detection against denial of service.
- **Honeyword sharing.** To save space, the sweetwords of one user can be real passwords of other users, so that the system stores each hash once and each user keeps only a list of indices. Juels and Rivest describe a scheme of this kind.
- **Honeychecker in hardware or another trust domain.** The index $c(u)$ can live in a hardware module or another trust domain, as long as a thief of the login server cannot read it.
- **Typo tolerance.** A generator must avoid honeywords that are a likely typo of the real password, or users who mistype set off false alarms.

## Pitfalls

- **A non-flat generator in line L1.** If GEN tweaks only digits, or draws from a model that does not fit the users, the real password stands out. Wang et al. (2018) found that the four main generators of Juels and Rivest give an attacker a success rate far above $1/k$. Line L1 needs a generator tested against such attacks on realistic data.
- **Storing the index on the login server.** If line L4 stores $c$ next to the hashes, a thief of the file reads it and the scheme gives nothing. The index must go only to the honeychecker.
- **A predictable position in line L2.** If $c$ is not uniform, for example always the first or the last, the position gives the real password away. Line L2 must choose $c$ uniformly at random.
- **Denial of service.** An attacker who knows a user's real password, for example from another site, may guess the honeywords of a tweaking generator and log in with them to set off alarms. An alarm policy that locks accounts on each alarm makes this an attack on availability.
- **Fast hashes.** Honeywords add detection, not resistance to cracking. The sweetwords still need a slow, salted [password hash](/password-hashing/).

## Exercises

1. With $k = 20$ and a perfectly flat generator, an attacker logs in with one cracked sweetword for each of 3 users. What is the probability that no alarm is raised? *Answer:* $(1/20)^3 = 1/8000$.
2. A generator tweaks the last two digits of a password. For the real password `blue42`, how many distinct honeywords can it make, and is $k = 20$ possible? *Answer:* $10^2 - 1 = 99$ other two-digit tails, so 19 honeywords are possible.
3. Why must the honeychecker not see the password that the user typed? *Answer:* so that a thief who controls the honeychecker learns nothing about passwords; it only learns which index is real, which does not reveal the password without the hash file.
4. A site uses honeyword sharing, where the sweetwords of a user are real passwords of other users. Users A and B have the same real password, and the password of B is also a sweetword of A at another index. What goes wrong at line L5? *Answer:* two stored entries of A match the typed password, so "the index" of line L5 is not unique, and the check can raise a false alarm for an honest login. The list of A must not hold the same password twice.

## References
