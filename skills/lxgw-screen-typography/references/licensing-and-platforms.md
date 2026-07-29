# Licensing and platform reference

## Upstream sources

- LXGW Neo XiHei Screen and LXGW Neo ZhiSong Screen:
  <https://github.com/lxgw/LxgwNeoXiZhi-Screen>
- LXGW Bright:
  <https://github.com/lxgw/LxgwBright>

Use official releases when obtaining font files. Preserve the license and copyright files that accompany every source font.

## Compatibility boundary

The screen-reading project states that its fonts are derived from IPA fonts and distributed under IPA Font License 1.0. It also states that derivative fonts must inherit that license and that IPA Font License 1.0 and SIL OFL 1.1 are incompatible.

LXGW Bright is distributed under SIL Open Font License 1.1. Its project states that modified fonts must remain under OFL and cannot be distributed under another license.

Therefore, do not treat a TTF/OTF containing glyphs from both projects as safely redistributable. This is a conservative implementation rule, not legal advice.

## Safe implementation patterns

### HTML and CSS

Define multiple `@font-face` rules under one virtual family and use non-overlapping `unicode-range` values. The browser selects the correct source without modifying or merging the font files.

Keep Chinese general punctuation in the Chinese range. For English typographic punctuation outside ASCII, wrap the complete English run with `lang="en"` or `.latin`.

### Word-processing and presentation formats

Use separate East Asian and Latin font properties when the format exposes them. If the library does not support that distinction reliably, split mixed text into runs:

- Han characters and Chinese punctuation: the semantic Chinese font.
- Basic Latin, Latin extensions, and ASCII numbers: LXGW Bright.

### Design tools

Create character styles named:

- `Typography / Reading / ZH`
- `Typography / Interface / ZH`
- `Typography / Latin & Numbers`

Apply the Latin style to embedded English or numeric runs. Do not expect a text style to switch fonts by semantic context automatically.

### System font replacement

Prefer a platform configuration that maps font roles to separate files. One static TTF cannot know whether a Han character is being used in a reading surface or in interface chrome.
