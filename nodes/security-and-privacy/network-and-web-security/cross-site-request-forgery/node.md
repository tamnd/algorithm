---
tag: V1QSDN
kind: concept
slug: cross-site-request-forgery
name: Cross-site request forgery
aliases:
- CSRF
- XSRF
area: security-and-privacy/network-and-web-security
level: intro
summary: "An attack in which another site makes the browser send a request with the user's cookies, so that it acts as the user."
history:
  year: 2008
  people: [Norm Hardy, Adam Barth, Collin Jackson, John C. Mitchell]
  note: "Hardy described the confused deputy in 1988. Barth, Jackson and Mitchell studied the defenses against cross-site request forgery in 2008, described login forgery, and proposed the Origin header."
prereqs: [same-origin-policy]
see_also: [cross-site-scripting, hmac, message-authentication-code, constant-time-programming, capability-list, content-security-policy]
sources:
  - paper: "Adam Barth, Collin Jackson and John C. Mitchell, Robust defenses for cross-site request forgery, ACM CCS 2008, pages 75 to 88"
    locator: "the threat models, login cross-site request forgery, the analysis of secret tokens, Referer checks and custom headers, and the proposal of the Origin header"
  - paper: "Norm Hardy, The confused deputy (or why capabilities might have been invented), ACM SIGOPS Operating Systems Review 22(4), 1988"
    locator: the compiler that used its own authority on a file named by its caller
  - url: "https://www.rfc-editor.org/rfc/rfc6454"
    title: "Adam Barth, The Web Origin Concept, RFC 6454, December 2011"
    locator: Section 7 (the Origin request header field)
  - url: "https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/"
    title: "IETF HTTP Working Group, Cookies, HTTP State Management Mechanism (draft-ietf-httpbis-rfc6265bis, an Internet-Draft, not yet an RFC)"
    locator: "the SameSite attribute, its Strict, Lax and None values, and the rules for same-site and cross-site requests"
  - url: "https://www.w3.org/TR/fetch-metadata/"
    title: "W3C, Fetch Metadata Request Headers"
    locator: "the Sec-Fetch-Site header and its values same-origin, same-site, cross-site and none"
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html"
    title: "OWASP, Cross-Site Request Forgery Prevention Cheat Sheet"
    locator: "the synchronizer token, the signed double-submit cookie, the check of the Origin header and the role of SameSite cookies"
---

Cross-site request forgery (CSRF) is a class of attack in which a page on one site makes the user's browser send a request to another site where the user is logged in. The browser attaches the user's cookies to that request, so the target site sees a request with valid credentials and acts on it as if the user had asked. The [same-origin policy](/same-origin-policy/) does not stop this, because it limits what a page can read, not where it can send requests. The flaw is a case of the confused deputy of Hardy (1988): the browser holds the user's authority and uses it for a request that someone else chose. The defenses make the server check that a state-changing request comes from its own pages: a secret token in each form, a check of the `Origin` header proposed by Barth, Jackson and Mitchell (2008), `SameSite` cookies that the browser does not send on cross-site requests, and the `Sec-Fetch-Site` header. This page describes the class and the defenses; it gives no attack pages or requests.

## In plain words

When you are logged in to a site, your browser keeps a cookie that proves it. The browser sends that cookie with every request to the site, no matter which page asked for the request.

So a page on another site can make your browser send a request to the site where you are logged in, for example a form that is sent without you seeing it. The site sees your cookie and does what the request says. The other page cannot read the answer, but it does not need to: the harm is the action itself. The fix is for the site to accept actions only with a proof that the request came from its own page, such as a secret value in the form that other sites cannot know.

## The idea

**Ambient authority.** A cookie, an HTTP authentication header or a client certificate is ambient: the browser adds it to each request to the site, without asking which page started the request. A server that decides "this request is from the user" only from such a credential cannot tell a request that the user made from one that another site caused. In Hardy's words, the browser is a deputy with two masters, and it uses the authority of one for the purpose of the other. A [capability](/capability-list/) that is passed with the request, instead of an ambient credential, avoids the confusion, and the token defense is a capability of this kind.

**What the attacker needs.** The user must be logged in to the target site in the same browser, the target action must be a request whose parameters the attacker can predict, and the server must decide only from ambient credentials. The attacker does not need to read any response.

**Login forgery.** Barth, Jackson and Mitchell described a variant in which the forged request logs the user in to the attacker's own account. The user then works in the attacker's account, and what the user enters, such as a search history or a card number, goes to an account that the attacker controls. A defense that protects only the requests of logged-in users misses this; the login form needs the same protection.

**The defenses.**

1. **Secret tokens.** The server puts a value $t$ in each form and in each state-changing request that its own pages make, and rejects a request whose token is missing or wrong. Other sites cannot read the pages of the target, so they cannot learn $t$. A stateless form is $t = \mathrm{HMAC}_k(\text{session id})$, an [HMAC](/hmac/) under a server key $k$, so the server can check $t$ by recomputing it. The token must be long enough not to be guessed, for example 128 bits, must be bound to the session, and should be compared in [constant time](/constant-time-programming/).
2. **The `Origin` header.** RFC 6454 defines a request header that names the origin that caused the request. The server rejects a state-changing request whose `Origin` is not one of its own. When the header is missing, the server must fall back to another check.
3. **`SameSite` cookies.** The cookie draft RFC 6265bis lets a site mark a cookie `SameSite=Strict`, which the browser sends only on requests that a page of the same site starts, or `SameSite=Lax`, which it also sends on top-level navigations with safe methods such as GET. Some browsers, such as Chrome since 2020, treat a cookie without the attribute as `Lax`. This blocks the cookie on most cross-site requests, but it depends on the browser, and "same site" is wider than "same origin".
4. **Fetch metadata.** The browser sends `Sec-Fetch-Site` with the value `same-origin`, `same-site`, `cross-site` or `none`. A server can reject state-changing requests marked `cross-site`.
5. **Safe methods.** GET and HEAD requests must not change state. All of the checks above are about the other methods, and a site that changes state on GET loses the protection of `SameSite=Lax`.

A [cross-site scripting](/cross-site-scripting/) flaw defeats all of these, because a script that runs in the target origin can read the token and send requests from the site's own pages.

## Examples

**The server's check.** The site is `https://app.example.com`, with a session cookie marked `SameSite=Lax` and a token in each of its forms. The table shows how each defense decides some abstract requests.

| request | started by | cookie sent? | `Origin` header | token | decision |
| --- | --- | --- | --- | --- | --- |
| POST from the site's own form | `https://app.example.com` | yes | `https://app.example.com` | valid | accept |
| POST from a page of another site | `https://www.example.org` | no (Lax) | `https://www.example.org` | missing | reject: no session, wrong origin, no token |
| the same, but the cookie is `SameSite=None` | `https://www.example.org` | yes | `https://www.example.org` | missing | reject: wrong origin and no token |
| POST from the site's form, `Origin` removed by a proxy | `https://app.example.com` | yes | none | valid | accept, on the token |
| GET of a link on another site | `https://www.example.org` | yes (top-level, Lax) | none | none | safe only if GET changes no state |

The third row shows why `SameSite` alone is not enough: a cookie marked `None`, an old browser or a request from a sibling host of the same site still carries the cookie. The token and the `Origin` check do not depend on the cookie attributes.

**Token numbers.** With a token of 128 random bits, a guess is right with probability $2^{-128}$. With an HMAC token, a forger who does not know $k$ has no better chance than the forgery bound of the [MAC](/message-authentication-code/). If the server used the session id itself as the token, an attacker who learned the session id, for example from a log, would also have the token; the HMAC keeps the two apart.

## Where it is used

- **Web frameworks.** Many frameworks include a token check for every form and every non-GET request by default, often in the signed double-submit form that keeps no state on the server.
- **Browsers.** `SameSite` cookies, the `Origin` header and fetch metadata exist largely to give servers a simple CSRF check. Where a browser treats cookies as `Lax` by default, sites that did nothing get some protection.
- **Interfaces of devices.** Admin pages of routers and other devices on a home network are reached through the browser and often use cookies or HTTP authentication. They need the same checks as any web site.
- **Security models.** The class is a standard example of the confused deputy problem, and of why ambient authority is hard to use safely.

## References
