---
name: wa-cta-standard
description: Build contact CTA HTML blocks for articles in WordPress Classic Editor. Use for one or two blocks per article (an optional earlier CTA and the closing CTA) in three site-branded visual variants, with the phone, email, or address the user chose for this run and no default contact.
---

# Contact CTA Visual Standard

Use pure inline-style HTML without `wp:html` block comments. The output is for the WordPress Classic Editor Text tab.

Use only the channels, contact details, and button labels the user chose in the `/convert` contact question for this run: phone (WhatsApp chat or call), email, address, or all of them. There is no default contact. Never hardcode or reuse contact details, credentials, or brand values.

## Channels

- One chosen link channel (phone or email): one button, as in the variants below.
- Two link channels: two buttons side by side, with `display: inline-block; margin: 4px;` on each. The first chosen channel uses the variant's filled button; the second uses an outline button: `background: transparent; color: {accent}; border: 2px solid {accent};` with the same padding and font (on Variant 2, use `color: #ffffff; border-color: #ffffff;`).
- Address: a text line below the buttons, 14px, in the variant's body color, starting with the label the user chose (for example "Alamat:"). Link it only to a maps URL the user gave.
- Address only: the address line replaces the button.

## Color system

Derive every value from the target website or user-provided brand guide:

| Slot | Used for |
|---|---|
| `{accent}` | Eyebrow, border accent, button background |
| `{secondary-accent}` | Variant 2 eyebrow |
| `{dark-bg}` | Variant 2 background and light-variant headings |
| `{light-bg}` | Variant 1 and 3 background |
| `{body-text}` | Variant 1 and 3 body copy |
| `{muted-text}` | Variant 2 body copy |
| `{border}` | Variant 3 border |
| `{footer-text}` | Optional footer copy |

Resolve every token to an actual hex value before delivering HTML. Maintain readable text and button contrast. If a slot is unavailable, reuse the closest observed brand color or ask the user; never invent a brand color.

## Variant 1 — Light with border accent

Use after a mechanism or process explanation.

- Container: `background: {light-bg}; border-left: 4px solid {accent}; border-radius: 6px; padding: 24px 28px; margin: 32px 0;`
- Eyebrow: 13px uppercase, `color: {accent}`, weight 600
- Headline: 18px, weight 700, `color: {dark-bg}`
- Body: 14px, `color: {body-text}`
- Button: `background: {accent}; color: #fff; padding: 12px 24px; border-radius: 4px;` 14px, weight 600

## Variant 2 — Dark

Use after a problem, risk, or decision section resolves.

- Container: `background: {dark-bg}; border-radius: 6px; padding: 28px 32px; margin: 32px 0;`
- Eyebrow: 13px uppercase, `color: {secondary-accent}`, weight 600
- Headline: 20px, weight 700, `color: #ffffff`
- Body: 14px, `color: {muted-text}`
- Button: `background: {accent}; color: #fff; padding: 12px 24px; border-radius: 4px;` 14px, weight 600

## Variant 3 — Light, bordered, centered

Use at the natural close of the article.

- Container: `background: {light-bg}; border: 1px solid {border}; border-radius: 6px; padding: 28px 32px; margin: 32px 0; text-align: center;`
- Eyebrow: 13px uppercase, `color: {accent}`, weight 600
- Headline: 20px, weight 700, `color: {dark-bg}`
- Body: 14px, `color: {body-text}; max-width: 480px; margin: auto;`
- Button: `background: {accent}; color: #fff; padding: 14px 32px; border-radius: 4px;` 15px, weight 600
- Footer: optional 12px copy, `color: {footer-text}`; include credentials only when supplied and verified

## Rules

- Use one or two CTA blocks per article: the closing CTA (Variant 3) always, plus an earlier CTA (Variant 1 or 2) only when the outline's CTA count is 2.
- Reference the preceding section instead of using generic CTA filler.
- Escape or encode every confirmed link correctly in the HTML (`&` as `&amp;`, the WhatsApp message and email subject URL-encoded).
- Every phone number, email, and address in the block comes from this run's contact question, never from memory, the website, or an earlier article.
- Deliver plaintext HTML with an implementation note.
- Never fabricate contact details, credentials, colors, products, or claims.
