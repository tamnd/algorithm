---
tag: D7Z6QK
kind: algorithm
slug: kerberos
name: Kerberos
aliases:
- Kerberos protocol
- Kerberos V5
area: cryptography/protocols
level: advanced
summary: Network authentication with a key distribution center. A login gives a ticket-granting ticket, which buys service tickets; authenticators with timestamps prove freshness. RFC 4120.
solves: [entity-authentication, key-distribution-problem]
model: word-ram
complexity:
  vars: {s: the number of services that a client uses in one login, r: the number of authenticators that a server accepts within one skew window}
  time: {worst: O(s), average: O(s), best: O(s)}
  space: {extra: O(r)}
properties: {deterministic: false, randomized: true}
history:
  year: 1988
  people: [Jennifer G. Steiner, Clifford Neuman, Jeffrey I. Schiller]
  note: Built at MIT Project Athena after the Needham-Schroeder design, with timestamps in place of the nonce handshake; version 5 was published as RFC 1510 in 1993 and as RFC 4120 in 2005.
prereqs: [key-distribution-center, needham-schroeder-protocol, authenticated-encryption]
see_also: [needham-schroeder, denning-sacco-protocol, entity-authentication, challenge-response-authentication, clock-skew, pbkdf2, password-authenticated-key-exchange, otway-rees-protocol]
sources:
  - paper: "Jennifer G. Steiner, Clifford Neuman and Jeffrey I. Schiller, Kerberos: an authentication service for open network systems, Proceedings of the USENIX Winter Conference, 1988, pages 191 to 202"
    locator: the design of Kerberos version 4, tickets, authenticators, the ticket-granting service and the use at Project Athena
  - url: "https://www.rfc-editor.org/rfc/rfc4120"
    title: Clifford Neuman, Tom Yu, Sam Hartman and Ken Raeburn, RFC 4120, The Kerberos Network Authentication Service (V5), July 2005
    locator: Section 3.1 (AS exchange), Section 3.2 (client/server exchange, with the skew check and the replay cache in Section 3.2.3), Section 3.3 (TGS exchange), Section 5.2.7.2 (PA-ENC-TIMESTAMP), Section 7.5.1 (key usage numbers)
  - paper: doi:10.1145/381906.381946
    title: Steven M. Bellovin and Michael Merritt, Limitations of the Kerberos authentication system, Computer Communication Review 20(5), October 1990, pages 119 to 132; also USENIX Winter Conference 1991, pages 253 to 267
    locator: replay within the authenticator lifetime, attacks on the time service, offline password guessing on the AS reply, and the proposal of challenge-response in place of timestamps
  - paper: doi:10.1145/359657.359659
    title: Roger M. Needham and Michael D. Schroeder, Using encryption for authentication in large networks of computers, Communications of the ACM 21(12), 1978, pages 993 to 999
    locator: the authentication server protocol with conventional keys on which Kerberos is based
  - url: "https://www.rfc-editor.org/rfc/rfc3962"
    title: Ken Raeburn, RFC 3962, Advanced Encryption Standard (AES) Encryption for Kerberos 5, February 2005
    locator: the PBKDF2 string-to-key function with the salt made of realm and principal name, and the default iteration count 4096
  - url: "https://www.rfc-editor.org/rfc/rfc1510"
    title: John Kohl and Clifford Neuman, RFC 1510, The Kerberos Network Authentication Service (V5), September 1993
    locator: the first specification of version 5, made obsolete by RFC 4120
  - url: "https://www.rfc-editor.org/rfc/rfc6113"
    title: Sam Hartman and Larry Zhu, RFC 6113, A Generalized Framework for Kerberos Pre-Authentication, April 2011
    locator: FAST armoring, which protects pre-authentication data inside a tunnel against offline guessing
---

Kerberos is a network authentication protocol built around a [key distribution center](/key-distribution-center/) (KDC). A user logs in once with a password and gets a ticket-granting ticket (TGT). With the TGT, the user's machine asks the KDC for a ticket for each service it wants, and shows that ticket to the service with an authenticator, a fresh encrypted timestamp. The service then knows who the user is, the two share a session key, and the user never sends the password over the network. Kerberos follows the [Needham-Schroeder protocol](/needham-schroeder-protocol/) with symmetric keys, but replaces its nonce handshake with timestamps, as Denning and Sacco proposed. Version 5 is RFC 4120 (2005), and it is the default sign-on of Windows domains.

**Notation.** $C$ is the client principal, $S$ a service and $c$, $s$ their names. The KDC has an authentication server (AS) and a ticket-granting server (TGS), with the long-term key $K_{tgs}$. $K_c$ is the long-term key of $C$, made from its password, and $K_s$ the key of $S$. $\{m\}^u_K$ is the authenticated encryption of $m$ under $K$ with key usage number $u$ (RFC 4120 Section 7.5.1). $n_1, n_2$ are nonces, $t$ is the client's local time, $\delta$ the allowed clock skew, and $e$ an end time.

## In plain words

Think of a fair. At the entrance you show your ID once and get a day wristband. At each ride you show the wristband at a ticket booth and get a ride ticket, which only the ride's operator can read. At the ride you hand over the ticket together with a small note, sealed with a code that only you and the operator learned from the booth, which says "it is me, and it is now 10:31".

The operator opens the ticket, learns the code and your name, opens your note, and checks that the time is close to the real time and that this note was not used before. Your password stayed at the entrance; everything after it uses wristbands and tickets that run out at the end of the day.

## The problem

Many users must prove who they are to many network services, over a network that an attacker can read and change. Each service must learn the user's name and share a fresh key with the user. Users should type a password once per day, the password should never cross the network, and services should not store user passwords. This is [entity authentication](/entity-authentication/) together with the [key distribution problem](/key-distribution-problem/), solved with a trusted online server that shares one key with each principal.

## The algorithm

```pseudo id=main
AS exchange, once per login                                         ▷ RFC 4120 Section 3.1
L1  C → AS: c, krbtgt, n1, till, and the pre-authentication {t}^1_Kc
L2  AS: look up Kc; if pre-authentication is required, decrypt it and check |now − t| ≤ δ, else fail
L3  AS: pick K_c,tgs; TGT ← {K_c,tgs, c, authtime, e1}^2_Ktgs, with e1 ≤ now + the longest life
L4  AS → C: c, TGT, {K_c,tgs, n1, krbtgt, e1}^3_Kc
L5  C: Kc ← string-to-key(password, realm ∥ c); decrypt the reply; check n1 and the server name
TGS exchange, once per service                                      ▷ Section 3.3
L6  C → TGS: TGT, the authenticator {c, t, u}^7_K_c,tgs, s, n2, till
L7  TGS: open the TGT with Ktgs; check the end time and the authenticator (as in line L12)
L8  TGS: pick K_c,s; ticket ← {K_c,s, c, authtime, e2}^2_Ks, with e2 ≤ e1
L9  TGS → C: c, ticket, {K_c,s, n2, s, e2}^8_K_c,tgs
L10 C: decrypt with K_c,tgs; check n2 and s
Client/server exchange, once per connection                         ▷ Section 3.2
L11 C → S: ticket, the authenticator {c, t, u}^11_K_c,s
L12 S: open the ticket with Ks; check now ≤ e2 + δ; open the authenticator with K_c,s; check the name, |now − t| ≤ δ, and that (c, t, u) is not in the replay cache; add it
L13 S → C: {t, u}^12_K_c,s                                          ▷ only when mutual authentication is asked
L14 C: decrypt and check that the reply holds its own (t, u)
```

**The AS exchange.** The client asks for a TGT (line L1). With pre-authentication, the request carries the current time encrypted under the client's key, so the AS answers only someone who knows the password (line L2). The AS makes a session key for the client and the TGS, seals it in the TGT under the TGS key, and seals another copy for the client under $K_c$ (lines L3 and L4). The client turns the password into $K_c$ and opens its part; the nonce $n_1$ shows that the reply answers this request (line L5). The client can now forget the password and $K_c$.

**The TGS exchange.** For each service, the client sends the TGT with an authenticator sealed under $K_{c,tgs}$ (line L6). The TGS checks them as a service checks an AP-REQ (line L7), makes a session key $K_{c,s}$, and seals it in a service ticket under $K_s$ and in a reply under $K_{c,tgs}$ (lines L8 and L9). The ticket cannot outlive the TGT.

**The client/server exchange.** The client sends the ticket with a new authenticator (line L11). The service opens the ticket with its own key, so it needs no contact with the KDC. It then checks the authenticator: the name matches the ticket, the time is within $\delta$ of its own clock, and the same authenticator was not seen before (line L12). For mutual authentication, the service returns the authenticator's time sealed under $K_{c,s}$, which only the holder of the ticket key could make (lines L13 and L14).

**Why timestamps.** A ticket is a reusable credential: anyone who copies it can send it again. The authenticator proves that the sender holds the session key now. In the Needham-Schroeder protocol, the responder proves freshness with an extra nonce round trip, and the [Denning-Sacco](/denning-sacco-protocol/) attack shows that the responder still cannot tell an old key from a new one. Kerberos puts an expiry time in each ticket and a timestamp in each authenticator instead, so one message suffices, at the cost of synchronized clocks and a replay cache that holds each authenticator for $\delta$ seconds.

**About the code.** The Python code is a toy Kerberos for study only. It is not constant time and must not protect real data; use MIT Kerberos, Heimdal or Active Directory. Messages are dicts and JSON, not ASN.1. The encryption is a study AEAD (encrypt-then-MAC with an HMAC-SHA256 key stream), not a Kerberos enctype such as aes256-cts-hmac-sha384-192; the key usage number is bound into each ciphertext as RFC 3961 does with derived keys. The string-to-key function is PBKDF2-HMAC-SHA256 with the salt realm $\|$ name and 1000 iterations, after the PBKDF2 design of RFC 3962. Flags, renewal, cross-realm keys and subkeys are left out. RFC 4120 has no test vectors for the exchanges, and this toy encoding could not match them in any case.

## Example

A run of the code, with the realm EXAMPLE.ORG, $\delta = 300$ seconds, and all clocks at $T_0$ unless the row says otherwise.

| Step | Line | Message or check | Result |
|---|---|---|---|
| 1 | L1, L2 | AS-REQ for alice with $\{T_0\}^1_{K_c}$ | the AS decrypts the time; $0 \le 300$; passes |
| 2 | L3 to L5 | AS-REP with a TGT that ends at $T_0 + 3600$ | alice opens her part with $K_c$; $n_1$ matches |
| 3 | L6 to L10 | TGS-REQ for host/files, life 600 s | ticket with $e_2 = T_0 + 600$ |
| 4 | L11, L12 | AP-REQ at $T_0$ | accepted; the cache holds (alice, $T_0$, 2, host/files) |
| 5 | L12 | the same AP-REQ again at $T_0$ | KRB_AP_ERR_REPEAT |
| 6 | L12 | the same AP-REQ at $T_0 + 301$ | the cache entry is gone, but $301 > 300$: KRB_AP_ERR_SKEW |
| 7 | L12 | a new AP-REQ at $T_0 + 900$ | $900 \le 600 + 300$; accepted |
| 8 | L12 | a new AP-REQ at $T_0 + 901$ | KRB_AP_ERR_TKT_EXPIRED |
| 9 | L1, L2 | AS-REQ with alice's clock at $T_0 - 305$ | KRB_AP_ERR_SKEW at the AS |

Rows 5 and 6 show why the cache and the skew check work together: the cache only needs to remember entries for $\delta$ seconds, because older authenticators fail the time check.

**Offline guessing.** With pre-authentication off for alice, anyone may send line L1 without the encrypted time. The AS answers with line L4, whose last part is sealed under $K_c$. The attacker tries each word of a list as the password and checks the tag; in the tests, the weak password "sunshine" is found among eight words. This is the guess that Bellovin and Merritt describe and that is now called AS-REP roasting. With pre-authentication on, the AS refuses (KDC_ERR_PREAUTH_REQUIRED), and a wrong password gives KDC_ERR_PREAUTH_FAILED.

## Correctness

**Claim.** If all parties follow the protocol, messages arrive unchanged, the clocks differ by at most $\delta$, the run ends before the tickets expire, and no authenticator is sent twice, then every check in lines L2, L5, L7, L10, L12 and L14 passes, and the client and the service hold the same $K_{c,s}$. The reason is that each sealed part is opened with the key that sealed it: $K_c$ is known to the client and the AS, $K_{tgs}$ to the KDC, $K_s$ to the service and the KDC, and the session keys reach both of their holders inside sealed parts. Both copies of $K_{c,s}$ come from the single value chosen in line L8.

**Replay and expiry.** A replayed AP-REQ is rejected in line L12: within $\delta$ seconds of its time the replay cache still holds it, and after that the skew check fails. A ticket is rejected after its end time plus $\delta$, and no one without the service key can change the end time. The proof page gives the full argument.

**Security.** These claims are about honest runs and replays. Formal analyses of the secrecy of the session keys and of authentication include Bella and Paulson for Kerberos IV in Isabelle (1998) and Butler, Cervesato, Jaggard and Scedrov for Kerberos 5 (2006). All of them assume that the long-term keys are strong, which is false for password-derived keys, and that the clocks are honest.

## Complexity

A login costs the AS exchange: two messages, one string-to-key computation on the client and a few encryptions. Each new service costs the TGS exchange (two messages) once per ticket life, and each connection costs one AP-REQ and, with mutual authentication, one AP-REP. Each check is a constant number of AEAD operations, so a login that reaches $s$ services costs $O(s)$ messages and operations. A service keeps no per-client state except its replay cache, which holds the $r$ authenticators that arrived in the last $\delta$ seconds, so its extra space is $O(r)$. The string-to-key cost is set on purpose by the PBKDF2 iteration count (4096 by default in RFC 3962).

## Properties

- **Single sign-on.** The password is used once, in line L5, to get the TGT. The client may then delete $K_c$.
- **No password on the wire.** The password never crosses the network, but material sealed under a password-derived key does, so a weak password can be guessed offline.
- **Stateless services.** A service checks a ticket with its own key and needs no contact with the KDC, apart from the replay cache.
- **Synchronized clocks.** Security depends on the clocks: an attacker who can set a server's clock back can replay old authenticators.
- **Central trust.** The KDC knows every long-term key and can make any ticket. Anyone who steals $K_{tgs}$ can forge TGTs for any user.
- **No forward secrecy.** An attacker who records traffic and later learns $K_c$ or $K_s$ can open the recorded tickets and replies and learn the session keys. PKINIT with Diffie-Hellman changes this for the AS exchange.

## Variants and improvements

- **Kerberos version 4.** The version of 1988 used DES in a propagating CBC mode, had a fixed message format and no pre-authentication. Version 5 added the ASN.1 encoding, several encryption types, cross-realm trust, delegation of tickets, and pre-authentication.
- **Pre-authentication.** PA-ENC-TIMESTAMP (RFC 4120 Section 5.2.7.2) stops anyone from asking for an AS reply for another user. An eavesdropper on a real login can still guess the password offline against the encrypted timestamp. FAST (RFC 6113) puts the pre-authentication inside an armored tunnel, made with a key the machine already has, which stops this as well.
- **PKINIT.** RFC 4556 (2006) lets the client authenticate to the AS with a public key and a certificate, for example a smart card, with an optional Diffie-Hellman exchange that removes the password from the AS exchange.
- **Encryption types.** RFC 3961 defines the framework and RFC 3962 the AES types. DES was deprecated in Kerberos by RFC 6649 (2012), and 3DES and RC4-HMAC by RFC 8429 (2018); RFC 8009 (2016) adds AES with HMAC-SHA-2.
- **Cross-realm trust.** Two realms share a key; the TGS of the first realm issues a TGT for the second realm, sealed under that key.

## When to use it

Use Kerberos for single sign-on inside an organization that runs a directory, such as an Active Directory domain or a Unix site with a MIT Kerberos or Heimdal KDC. On the open Internet, with no shared administration, public-key protocols such as the [TLS handshake](/tls-handshake/) with certificates, or OAuth and OpenID Connect on top of TLS, fit better. Use a maintained implementation, strong service keys, AES enctypes, and FAST where it is available.

## Pitfalls

- **Weak passwords with pre-authentication off.** Without line L2, anyone can ask for line L4 and guess the password offline (AS-REP roasting). Require pre-authentication for every user.
- **Weak service keys.** Any user with a TGT can ask the TGS for a ticket to any service (lines L6 to L9). If the service key comes from a human-chosen password, the user can guess it offline against the ticket. This is called Kerberoasting, and was shown publicly by Tim Medin in 2014. Use long random keys for service accounts.
- **No replay cache.** Without the cache in line L12, an attacker who copies an AP-REQ can replay it to the same service within $\delta$ seconds. Some services keep no cache; mutual authentication with a subkey limits the damage.
- **Clock attacks.** If an attacker can set a server's clock, it can make old authenticators or tickets valid again. Secure the time service.
- **Checking the nonce and the name.** Lines L5 and L10 must check $n_1$, $n_2$ and the server name; otherwise an attacker can send an old reply, or a reply for another service.
- **The KDC keys.** A copy of $K_{tgs}$ lets an attacker make TGTs for any user (a golden ticket). Protect the KDC database and change $K_{tgs}$ after a breach, twice, because old tickets are still sealed under the previous key.
- **Old encryption types.** DES, RC4-HMAC and 3DES are deprecated and should be disabled.

## Implementations

## History

Kerberos was built at MIT's Project Athena from 1983 on, after the shared-key protocol of Needham and Schroeder (1978), with timestamps in place of the nonce handshake. Version 4 was described by Steiner, Neuman and Schiller at the USENIX Winter Conference of 1988. In 1990, Bellovin and Merritt published the limitations of the design: replay within the authenticator lifetime, dependence on secure clocks, and offline password guessing. Version 5 addressed several of them and was published as RFC 1510 in 1993 by Kohl and Neuman. Microsoft made Kerberos the default authentication of Windows 2000 domains. RFC 4120 replaced RFC 1510 in 2005, together with RFC 3961 and RFC 3962 for the encryption. PKINIT followed in 2006 and FAST in 2011.

## References
