# State of HTTP2 and HTTP3 and content-prioritization

... as far as I can tell, as of July 13 2025.

There are two prioritization standards:
* RFC 7540 HTTP/2
    * Original HTTP2 spec.
    * Defines the original HTTP2 tree-based prioritization, coded in the Stream Dependency field of `HEADERS` (type=0x1) frames.
    * Later updates are possible with `PRIORITY` (type=0x2) frames.
    * Later deprecated by RFC 9113 HTTP/2.
* RFC 9218 Extensible Prioritization Scheme for HTTP (from herein, "EPS")
    * Only scheme defined for HTTP3, technically optional.
    * Backported into HTTP2
    * Based on a `priority:` header (regular HTTP header) and `PRIORITY_UPDATE` (type=0x10 in HTTP2, type=0xF0700 or 0xF0701 in HTTP3) frames.

# Servers

## Apache httpd

Supports HTTP2. Does not support HTTP3.

Supports RFC 7540 prioritization (the deprecated one). Includes code to support `PRIORITY` frames.

I cannot find references to RFC 9218 in the code, but I may have missed it.

Apache uses nghttp2, which *does* support RFC 9218, but may require some settings not used by Apache: https://web.archive.org/web/20250612122442/https://nghttp2.org/documentation/programmers-guide.html#stream-priorities

## nginx

Not tested. Supports HTTP3.

According to [HTTP/3’s Extensible Prioritization Scheme in the Wild](https://documentserver.uhasselt.be/bitstream/1942/43545/2/ANRW24_h3_eps_in_the_wild_authorversion_20240626.pdf), it has no support for EPS at all as of April 2024.

## Caddy.

Not tested. Supports HTTP3.

According to [HTTP/3’s Extensible Prioritization Scheme in the Wild](https://documentserver.uhasselt.be/bitstream/1942/43545/2/ANRW24_h3_eps_in_the_wild_authorversion_20240626.pdf), it has no support for EPS at all as of April 2024.

Relevant issue: https://github.com/quic-go/quic-go/issues/3470 http3: RFC 9218 - Extensible Priority Scheme

## lighttpd1.4

Not tested. Supports HTTP2. Does not support HTTP3.

There is code to parse the `priority` header (EPS).

```
  * [core] HTTP/2 PRIORITY_UPDATE frame (experimental)
  * [core] send HTTP/2 SETTINGS_NO_RFC7540_PRIORITIES
```

# Browsers

## Chrome

Sends both the Priority header and a dummy tree.

## Firefox

[Firefox was the only browser that used to send a non-flat prioritization tree.](https://www.youtube.com/watch?v=nH4iRpFnf1c&t=1194s)

Later, Firefox disabled the old scheme:

* May 21 2024, [Bugzilla: Implement Extensible Prioritization Scheme for HTTP/2](https://bugzilla.mozilla.org/show_bug.cgi?id=1865040) [(Changeset)](https://hg-edge.mozilla.org/integration/autoland/pushloghtml?fromchange=750a9d68013bf86f5d1e16ddc95cce396fffd4a2&tochange=deedf27980767ec044741273bc0c9ad212bc4e1d)
    * In addition to enabling EPS, it disables the old tree-based mechanism.
    * `network.http.http2.enabled.deps` controls whether the old mechanism is still used, and it defaults to false.
* Jul 24 2024, it had to be re-enabled [due to some websites not working](https://bugzilla.mozilla.org/show_bug.cgi?id=1909666): [Bug 1909666 - Re-enable network.http.http2.enabled.deps and not send SETTINGS_NO_RFC7540_PRIORITIES, r=#necko](https://phabricator.services.mozilla.com/D217584)
* Sep 13 2024, it was disabled again, after ostensibly more testing: [Bug 1915134 - Flip network.http.http2.enabled.deps to false r=acreskey](https://phabricator.services.mozilla.com/D220390)

As of Jul 13 204, it is still disabled by default.