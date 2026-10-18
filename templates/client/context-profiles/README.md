# Context profiles (optional)

A context profile is a JSON file that describes how the brand sounds and looks. Put one or more here, for example `acme-brand.json` or `acme-anna.json` (one per author or tone). `/research` copies the chosen profile into each new article project, so later edits never change an article that has already started.

No profile is fine: the stages then use `facts.md` alone.

The stages read these fields when they exist (any extra fields are ignored):

```json
{
  "identity": { "name": "", "tagline": "", "values": [] },
  "positioning": { "unique_value_proposition": "", "differentiators": [] },
  "ideal_customer_profiles": [{ "persona_name": "", "pain_points": [], "desired_outcomes": [] }],
  "voice_and_tone": { "personality_traits": [], "tone_descriptors": [], "speaks_like": "", "never_sounds_like": "" },
  "content_guidelines": { "dos": [], "donts": [], "copy_mechanics": {} },
  "visual_identity": { "color_palette": {}, "typography": {}, "imagery": {} },
  "offer_context": { "products_services": [{ "name": "", "description": "" }] }
}
```

`visual_identity` drives the feature image prompt. Prices or rate cards in a profile are never put into an article; `facts.md` decides what may be claimed.
