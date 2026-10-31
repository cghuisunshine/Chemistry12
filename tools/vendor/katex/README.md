KaTeX 0.16.22, MIT license (see LICENSE).
Browser distribution; woff2 fonts are in assets/chemistry12-math/fonts.
JavaScript and CSS are embedded by the practice builder for offline use.
Source: https://github.com/KaTeX/KaTeX/releases/tag/v0.16.22

The mhchem extension from the same release is embedded after KaTeX, before the solution formatter, for offline chemistry and unit notation.
Source: https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/mhchem.min.js
Original SHA-384 (base64): F2ptQFZqNJuqfGGl28mIXyQ5kXH48spn7rcoS0Y9psqIKAcZPLd1NzwFlm/bl1mH
The two CommonJS imports use ./katex.min.js instead of katex so Node tests share the vendored instance. The browser implementation is unchanged.
Copyright and license notices: mhchem-NOTICE.txt and mhchem-APACHE-LICENSE.txt.
