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
<pack>/server/talk/TTTTTTTT.toml   [[talk]] of one template
<pack>/server/crafting.toml        [[craft]]
<pack>/server/story.toml           [[scene]], [[shard]]
<pack>/server/butchery.toml        [[butchery]]
<pack>/server/weapons.toml         [[weapon]]
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
  `tell_text`, `line_text`), at most 200 characters, beside the string reference it stands in for.
  A compile uses the reference when there is one; a line, a step's line or a greeting with only
  `_text` is said as that text, which the client shows as it is (the same in every language, with
  nothing filled in). Prefer new string-table entries in the world's own data overlay, referenced
  by id; `_text` is for when there is no overlay. The game's own text is never copied into a
  `_text` field.
- **Token names**: a line's `line_name` is the name of the string token its string id is (such as
  `ID_Begin2`); every token is computed from its name, so a check holds the name to the id, and a
  tool can show what a line is for without the install.
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
| `talk KEY` | the row's `key` |
| `craft 0xID` | the craft skill or recipe |
| `scene 0xID` | the scene's id |
| `shard 0xOBJECT` | the shard's world id |
| `butchery 0xPROFILE` | the butchery profile |
| `weapon NAME` | the weapon's name, as creatures' templates write it |

Numbers in an item are hexadecimal after `0x`, else decimal; `keeper 0x470033D0` and
`keeper 0x470033d0` are one item. Keys are lowercase letters, digits and hyphens. The seed's keys are
made from numbers: `s-5c` (the static object whose id ends in `5C`), `n-31e6` (a person of template
`0x470031E6`), `c-12402` (camp 12402), `p-77b80003` (a place in cell `0x77B80003`), `s1` (a step),
`t-335b-1cf7eb76` (a line of template `0x4700335B`, string `0x1CF7EB76`); a second row that would
take a key already used gets `-2`, `-3`, ... The seed keeps each row's key from release to release,
and never gives a key that a row has had to another row. A row refers to another by key: an
object's `to` and a step's `to` name a place, a camp's `parent` a camp, a line's `object` a person;
`pack:key` reaches another pack's row, `key@XXYY` another landblock's.

Packs merge in load order. Two packs that set an item alike agree. A pack that sets an item an
earlier pack set differently wins only where an `[[override]]` says so (its `items` naming the
item, or `landblock XXYY` for everything in a landblock, or nothing for everything both set);
otherwise the build stops naming both rows. `[[remove]] items = ["camp c-4586@77B8"]` (or
`item = "camp c-4586@77B8"`) takes an item away.

## Provenance

Every row has `prov`; a field whose source differs from its row's says so in `prov.fields`.

| `from` | means | required | optional |
|---|---|---|---|
| `capture` | measured from recordings of the live servers | `evidence` (an `AC2-EVID-...` handle), `ref` (opaque), `confidence` (`high`, `medium`, `low`) | `sample`: `sessions`, `creatures`, `corpses`, `views`, `trips`, `lines` |
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
| `quest-death-effect` | killing a creature whose template's death effect moves a quest on advances that quest a phase, as the recordings show for others of that effect |
| `talk-token-role` | a line's role is the one its token's name gives (`ID_Begin2` offers a quest, `ID_Underway1` reminds, `ID_TooLow` refuses), said at that role's moment the way recorded lines of the name or role were; a derived line's `confidence` is how often recorded lines of its role agreed |
| `talk-quest-number` | a person's quest line numbered k goes with the quest a recorded line of the same person numbered k went with |
| `talk-quest-name` | a person's quest line numbered k goes with the quest named after the person's own table and k |

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
| `scene` | | a door's scene: the `[[scene]]` a player plays on the way to `to`, in place of portal space |

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
under way), `trigger`, `tell` / `tell_text` (what the person says), `update` (`bestow`, `advance`,
`complete`), `phase` (for `advance`), `xp`, `gives` (templates), `counts` (how many of each item
given, in order; 1 when left out), `requires`, `takes`, `to`, `effects` (the effects it puts on the
player, by their saved states: a blessing, a recipe learned or forgotten), `text` (a text shown
after the effects, `{ table, string }`), `races` (the races it is for, by number: 1 human, 2
Lugian, 4 Tumerok, 8 Drudge, 16 Empyrean; every race when left out), `effects_last` (true: the
quest's update is told before the effects and their text, not after them).

| `trigger` | moves the quest when the player |
|---|---|
| `{ use = T }` | uses a person or an object of template T (or a held item of it) |
| `{ use = I, on = T }` | uses a held item of template I on an object of template T |
| `{ arrive = T }` | arrives through a portal of template T |
| `{ take = T }` | takes an item of template T |
| `{ kill = T }` | kills a creature of template T |

`requires` lists other quests the step needs, each `{ quest = Q, phase = N }` (under way at that
phase) or `{ quest = Q, done = true }`. `takes` lists templates of items taken from the player's
pack, which the player must hold (a hand-in). `to` names a place the step takes the player to,
through portal space; its update is made on arrival.

**`[[talk]]`**: a line a person (or a creature) says, and when. One row per line; a person says the
lines of its rows whose moment and quest match, picking at random among several.

| field | | meaning |
|---|---|---|
| `key` | required | unique in its pack |
| `who` | required | the template that says it |
| `object` | | one placed person only (`key@XXYY`) |
| `line`, `line_text` | one of them | the line: a string reference, in the person's own string table, or new prose |
| `line_name` | | the token name of `line`'s string id |
| `role` | | what it does: `offer`, `remind`, `advance`, `accept`, `complete`, `fail`, `refuse-use`, `refuse-give`, `use`, `near`, `idle`, `combat`, `death`, `teleport` |
| `how` | | `tell` (to the player, naming the speaker; the default), `say` (aloud, to everyone near), `emote` (text naming the speaker) |
| `when` | required | the moment: `use`, `give`, `attack`, `death`, `near`, `idle` |
| `quest`, `update`, `phase` | | the quest update the line comes with (`bestow`, `advance` and its phase, `complete`, `fail`) |
| `item` | | the item given, for a line said when one is |
| `order` | | its place in a speech of several lines (0 first) |

**`[[craft]]`**: a craft skill (`skill`, its saved state) or a recipe (`recipe`) every new character
starts with, at level 1 for a craft skill. One of the two.

**`[[scene]]`**: a scene of the story, as a client plays it.

| field | | |
|---|---|---|
| `id` | required | the scene's id (an enumeration's value, such as `0x40000021`) |
| `act`, `number` | `act` required | its act and its place in the act |
| `name` | required | its name, a string reference |
| `hidden`, `playable` | | a scene no story page lists (default false); one a player may replay (default true) |
| `keyframes` | | its steps in order: `{ seconds, picture, music, voice, subtitle, tracks }`; `picture`, `music` and `voice` data ids, `subtitle` a string reference, `tracks` which of them the step defines (picture 0x1, music 0x2, voice 0x4, subtitle 0x10) |
| `at_start` | | its place among the scenes every new character holds from its first entry |

**`[[shard]]`**: `object`, a story shard's world id, and `scene`, the scene using it bestows (the
shard's destination is its `[[object]]` row's `to`).

**`[[butchery]]`**: what butchering a corpse yields, by its creature's butchery profile: `profile`
(the profile's saved state), `items` (the materials' templates) and `weights` (each one's share, in
order), and `empty` (the share of butcheries that find nothing, against the weights; none when left
out). One material is cut per butchery.

**`[[weapon]]`**: a weapon creatures wield, where the name their templates give it (an identifier
of the install, such as `ClubBurunBrowerk`) is no template of the install's own. `name`, `template`
(the template it is made of), `two_share` (of the creatures whose template asks two of it, the share
given two, the rest one; every one is given two when left out) and `stance` (the stance it is fought
with, where its template sets none).

**`[[remove]]`**: `items` (or `item`), the items a pack takes away.

## What a row never holds

- the game's own text: names, descriptions, lines, journals (referenced by string id instead);
- bytes of the client's records, or values a compile reads from the install;
- names of players or characters, chat, or anything identifying a recording or the person who made
  it;
- anything from other projects' databases.
