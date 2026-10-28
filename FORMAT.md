# The format

How the database's files are written: the world, its packs, the rows of each kind, their keys and
references, where each row came from, and what a row may and may not hold. `yalain world check`
holds a database to all of it.

## Files

```text
world.toml                         the world: key, game, era, packs in load order, overrides
world.lock                         ids given to authored symbols, kept across builds
<pack>/pack.toml                   name, version, game, authors, license, description
<pack>/server/landblocks/XXYY.toml [[object]] and [[camp]] rows standing in landblock XXYY
<pack>/server/places.toml          [[place]]
<pack>/server/loot.toml            [[loot]]
<pack>/server/stores.toml          [[keeper]], [[sale]]
<pack>/server/quests/QQQQQQQQ.toml [[quest]], [[step]] of one quest
```

Any file under `server/` may also hold `[[remove]]` rows. One file per landblock and per quest
keeps changes small: two people filling different towns never touch the same file.

```toml
# world.toml
format_version = 1
key = "yalain-world"
game = "ac2"
era = "eor"
packs = ["seed-2017", "fill-arwic"]   # load order

[[override]]                          # where two packs set one item, this pack wins
pack = "fill-arwic"
over = "seed-2017"
# items = ["camp c-4586@77B8"]        # only these items (all of them when left out)
```

```toml
# <pack>/pack.toml
format_version = 1
name = "fill-arwic"                   # lowercase letters, digits and hyphens
version = "0.1.0"
game = "ac2"
authors = ["you"]
license = "CC0-1.0"
description = "People of Arwic's market."
```

## Values

- **Data ids** are integers, written in hexadecimal: `template = 0x470031E6`. They name records of
  the install: templates `0x47...`, cells (`0xXXYYCCCC`, landblock and cell), saved states `0x6F...`,
  string tables `0x25...`, pictures `0x41...`.
- **Enum values** are integers whose enumeration is fixed by the field: `profile` is always a
  generator profile.
- **Identifiers** of the install may be written as text beside their number (`profile_name =
  "GP_CampBeetleEdge"`, `id_name = "QuestRescueHold"`, a place's `destination =
  "dng_btd_ironlinvak"`): letters, digits, `_`, `:`, `.`, `-`, at most 80. A compile checks that
  each is the install's own for its number.
- **String references** point at the install's text: `{ table = 0x25002AFC, string = 0x2824938C }`.
- **New prose** a pack writes goes in a field ending in `_text` (`name_text`, `greeting_text`,
  `tell_text`), at most 200 characters, beside the string reference it stands in for. A compile
  uses the reference when there is one. Prefer new string-table entries in the world's own data
  overlay, referenced by id; `_text` is for when there is no overlay. The game's own text is never
  copied into a `_text` field.
- **Places**: `cell` (the full cell id), `at = [x, y, z]` in meters within the cell's landblock
  (outdoors the landblock is 160 m on a side), and either `rotation = [w, x, y, z]` (scalar first)
  or `heading` (degrees). Outdoors `cell` may be left out: it follows from `at` (cells of 20 m,
  numbered from 1 along y within each x).

## Keys and references

Every row sets one **item**, named by its key:

| item | key |
|---|---|
| `object KEY@XXYY`, `camp KEY@XXYY` | the row's `key`, unique within its landblock in its pack |
| `place KEY` | the row's `key` |
| `loot 0xVALUE` | the profile's value |
| `keeper 0xTEMPLATE` | the storekeeper template |
| `sale 0xSTORE ORDINAL` | the store template and the listing's ordinal |
| `quest 0xID` | the quest's id |
| `step 0xQUEST KEY` | the quest and the step's `key` |

Keys are lowercase letters, digits and hyphens. The seed's keys are made from numbers: `s-5c` (the
static object whose id ends in `5C`), `n-31e6` (a person of template `0x470031E6`), `c-12402` (camp
12402), `p-77b80003` (a place in cell `0x77B80003`), `s1` (a step). A row refers to another by key:
an object's `to` names a place, a camp's `parent` a camp; `pack:key` reaches another pack's row,
`key@XXYY` another landblock's.

Packs merge in load order. A pack that sets an item an earlier pack set wins only where an
`[[override]]` says so; otherwise the build stops naming both rows. `[[remove]] items = ["camp
c-4586@77B8"]` takes an item away.

## Provenance

Every row has `prov`; a field whose source differs from its row's says so in `prov.fields`.

| `from` | means | required | optional |
|---|---|---|---|
| `capture` | measured from recordings of the live servers | `evidence` (an `AC2-EVID-...` handle), `ref` (opaque), `confidence` (`high`, `medium`, `low`) | `sample`: `sessions`, `creatures`, `corpses`, `views`, `trips` |
| `dat` | a record of the install | `record` | |
| `derived` | computed by a listed rule | `rule` | `record` |
| `authored` | written by a person | | `by`, `note` |

```toml
[[camp]]
key = "c-4586"
cell = 0x77B80040
at = [144.8, 144.7, 133.0]
radius = 5.0
population = 2
regen = 192.0
spawns = [{ template = 0x47002224, weight = 2 }]
prov = { from = "capture", evidence = "AC2-EVID-WDB-CAMPS-2017", ref = "camp 4586", confidence = "low", sample = { creatures = 2, sessions = 1 }, fields = { regen = { from = "derived", rule = "camp-regen-median" }, radius = { from = "authored" } } }
```

### Rules

| rule | value |
|---|---|
| `camp-regen-generator` | a camp's regeneration is the regeneration period of the generator template whose profile matches the camp's species |
| `camp-regen-median` | a camp with no matching generator regenerates 192 s after a death, the median respawn measured |
| `camp-regen-hall` | the training hall's camps regenerate after the respawn measured at the spot |
| `camp-profile-species` | a camp's generator profile is the one camp profile whose name matches the species of the creatures it made |
| `keeper-store` | a storekeeper opens the store its template names |
| `store-sales` | a sale's product, price and currency are the store template's own listing at that ordinal; its name is the product's |
| `quest-definition` | a quest's name, description, icon and journal entries are its definition's |
| `quest-setup-static` | a quest's duration, retry wait and experience are the constant values its setup sets |

## Record kinds

A field marked † is read from the install when left out.

**`[[object]]`**: a person or an object of the world.

| field | | meaning |
|---|---|---|
| `key` | required | unique in its landblock |
| `kind` | required | `npc` (a person the server numbers) or `static` (an object with an id of its own) |
| `id` | statics | the world id (the live servers' own, for the seed's) |
| `template` | required | what it is |
| `cell`, `at`, `rotation` / `heading` | `at` required | where it stands |
| `name`, `name_text` | | a name the server gives it (a portal named for where it leads); else the template's |
| `to` | | the place using it takes a player to |
| `landings` | | a lifestone's recall spots: `{ cell, at, heading, seen }` |

**`[[camp]]`**: a spawn camp.

| field | | meaning |
|---|---|---|
| `key` | required | |
| `cell`, `at` | `at` required | the center |
| `radius` | | outdoors, how far from the center a creature appears (m) |
| `spots` | | indoors, the points creatures appear at: `{ cell, at }` |
| `population` | required | how many it keeps alive |
| `regen` | required | seconds from a death to its replacement |
| `spawns` | | what it makes: `{ template, weight }` |
| `profile`, `profile_name` | | the generator profile it stands for |
| `parent` | | a master camp |

**`[[place]]`**: a destination. `key`, `cell`, `at`, `rotation` / `heading`, `named_by` (templates
whose destination names it), `destination` (that name, as text).

**`[[loot]]`**: what a dead creature leaves. `profile` and `profile_name` (its death-loot profile),
`counts` (the chance of 0, 1, 2, ... items), `items` (`{ template, weight }`, what a draw picks
from), `extras` (`{ template, chance }`, items with a chance of their own). A creature's trophies
are its template's and are not rows.

**`[[keeper]]`**: a storekeeper. `template`, `store`† (the store template it opens), `greeting` /
`greeting_text`.

**`[[sale]]`**: what a store's listing shows that the store template lacks. `store`, `ordinal`,
`stack`, `icon` (`{ layer, picture, color }`), `product`†, `cost`†, `currency`†, `name`† /
`name_text`.

**`[[quest]]`**: a quest's server values. `id` and `id_name`, `state`† (its definition), `challenge`,
`duration` (s, 0 for none), `retry` (s), `xp`, `cancellable`. Its name, description, icon and journal
are the definition's.

**`[[step]]`**: what moves a quest on. `key`, `quest`, `needs` (the phase it must be at; 0 for not
under way), `trigger` (`{ use = T }`, `{ take = T }` or `{ kill = T }`), `tell` / `tell_text` (what
the person says), `update` (`bestow`, `advance`, `complete`), `phase` (for `advance`), `xp`, `gives`
(templates).

**`[[remove]]`**: `items`, the items a pack takes away.

## What a row never holds

- the game's own text: names, descriptions, lines, journals (referenced by string id instead);
- bytes of the client's records, or values a compile reads from the install;
- names of players or characters, chat, or anything identifying a recording or the person who made
  it;
- anything from other projects' databases.
