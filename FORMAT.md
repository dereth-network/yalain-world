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
<pack>/server/gives/TTTTTTTT.toml  [[give]] of one template given to
<pack>/server/talk/TTTTTTTT.toml   [[talk]] of one template
<pack>/server/crafting.toml        [[craft]]
<pack>/server/story.toml           [[scene]], [[shard]]
<pack>/server/butchery.toml        [[butchery]]
<pack>/server/weapons.toml         [[weapon]]
<pack>/server/death_spawns.toml    [[death_spawn]]
<pack>/server/routes.toml          [[route]]
<pack>/server/areas.toml           [[area]]
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
  "GP_AnExampleCamp"`, `id_name = "QuestAnExample"`, a place's `destination =
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
| `area XXYY` | the area's landblock |

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
| `capture` | measured from recordings of the live servers | `evidence` (an `AC2-EVID-...` handle), `ref` (opaque), `confidence` (`high`, `medium`, `low`) | `sample`: `sessions`, `creatures`, `corpses`, `views`, `trips`, `lines`, `visits` |
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
| `store-sales-unseen` | a sale no recording listed is the store template's own listing at that ordinal (as `store-sales`), its stack the most its product stacks to (1 when the product names none) and its icon the layers its product's look gives (none when the look gives none), as every recorded sale was |
| `quest-definition` | a quest's name, description, icon and journal entries are its definition's |
| `quest-setup-static` | a quest's duration, retry wait, experience, challenge and whether it is shown are the constant values its setup sets |
| `quest-death-effect` | a quest a creature's death effect moves on holds its definition's text alone, as no setup says more of it; the death effect itself is read from the creature's template when the creature dies |
| `quest-kill-fellows` | a kill's move on a quest with no setup and no recording to say otherwise stays the killer's: nothing says it reaches fellows, and the setup decides that quest by quest, so its row leaves `fellows` out; a row or a later study may opt one in |
| `talk-token-role` | a line's role is the one its token's name gives (`ID_Begin2` offers a quest, `ID_Underway1` reminds, `ID_TooLow` refuses), said at that role's moment the way recorded lines of the name or role were; a derived line's `confidence` is how often recorded lines of its role agreed |
| `talk-quest-number` | a person's quest line numbered k goes with the quest a recorded line of the same person numbered k went with |
| `hoard-key-table` | a hoard's key used on the stockpile its interaction table names gives its user and fellowship the quest the key's use needs able to be given, which the stockpile's use needs under way, as the recordings show for one hoard |
| `hoard-key-text` | a hoard's entry quest lasts the ten minutes, and its mine quest the five, that its key's own text gives, as the recordings measured for one hoard |
| `hoard-teleport-place` | a hoard's stockpile leads to the place its mine quest's teleport sends a player out from, where the recordings show players of one hoard arriving |
| `talk-quest-name` | a person's quest line numbered k goes with the quest named after the person's own table and k |
| `map-marked-place` | a surveyor's map leads where the recordings show maps marking the same area (the same search rectangle) leading, whatever their material |
| `item-spot-regen` | an item a camp keeps lying whose return no recording timed comes back as the timed spots of its template did, else 20 s after its taking, as every timed quest item lying alone did |

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
| `to` | | the place using it takes a player to; a person says its line for a use as it does |
| `landings` | | a lifestone's recall spots: `{ cell, at, heading, seen }` |
| `scene` | | a door's scene: the `[[scene]]` a player plays on the way to `to`, in place of portal space |
| `locked` | statics | a locked door: from its front a plain use is refused and only its key opens it (it locks again as it closes); from behind it opens |
| `lock` | | a locked door's key id: the id (a key's `Lock_KeyID`) a key must carry to open it; none known: no key does |
| `route`, `route_start`, `route_direction` | people | the `[[route]]` a person walks (`key`, or `pack:key`), the waypoint it sets out toward (from 0) and `forward` or `backward`, as a camp's creatures do |
| `recall`, `summon` | statics | a portal a player who used it may recall to (`recall = true`: a recall to the last portal used returns there) and summon a portal to (`summon = true`); left out, neither |
| `requires` | statics | the quest a player must hold to use it (a portal this placement keeps closed, over its template's): `{ quest = Q, done = true }` (completed), `{ quest = Q, underway = true }` (under way at any phase) or `{ quest = Q, phase = N }` (under way at that phase); a use or a walk-in it keeps out is refused at once |

**`[[camp]]`**: a spawn camp.

| field | | meaning |
|---|---|---|
| `key` | required | |
| `cell`, `at` | `at` required | the center |
| `radius` | | outdoors, how far from the center a creature appears (m) |
| `spots` | | indoors, the points creatures appear at: `{ cell, at }` |
| `population` | required | how many it keeps alive |
| `regen` | required | seconds from a death to its replacement |
| `spawns` | | what it makes: `{ template, weight }`; an item's template (one with a value, no creature) it keeps lying at its place, a new one `regen` seconds after the last is taken |
| `profile`, `profile_name` | | the generator profile it stands for |
| `parent` | | a master camp |
| `movement` | | how its creatures may move, over their template's: `stationary` (never moves nor fights), `turn-only` (turns where it stands), `constrained-to-home` (kept near home: the default), `constrained-to-master` (follows a master), `free-range` (no distance from home ends a fight) |
| `wanders`, `wander_range`, `wander_chance` | | over their template's: whether they wander at rest (default true), how far from home (m, default 25), the chance a wander sets out when one falls due (default 0.1) |
| `homesick`, `perception` | | over their template's: the distance from home they keep to (m, default 40; under 5 they never wander), how near a player must come to be noticed (m, default 20) |
| `uses_doors` | | over their template's: whether they open doors (default true) |
| `route` | | the `[[route]]` its creatures walk at rest (`key`, or `pack:key`), in place of wandering, indoors too |
| `route_start`, `route_direction` | | the waypoint they set off toward (from 0; default 0) and which way they go on: `forward` (default) or `backward` |

**`[[place]]`**: a destination. `key`, `cell`, `at`, `rotation` / `heading`, `named_by` (templates
whose destination names it: a portal's, or a surveyor's map's, whose holder a person who sends players by
maps sends here; a template is named by one place at most), `destination` (that name, as text: the name an
effect that sends a player to a named place, a city's recall, looks it up by; one place to a name), `row`
and `holds` (a room of a row of like rooms, and the cell its creature stands in: a step that leads to any
room of a row sends a player to one of them, free of players and with its creature standing if it can).

**`[[loot]]`**: what a dead creature leaves. `profile` and `profile_name` (its death-loot profile),
`counts` (the chance of 0, 1, 2, ... items), `items` (`{ template, weight }`, what a draw picks
from), `extras` (`{ template, chance }`, items with a chance of their own). A creature's trophies
are its template's and are not rows. A chest's row may name `level` and `value` (`[low, high]`): what it
draws is then treasure of that level, each piece worth a draw from that band; its extras aren't.

**`[[keeper]]`**: a storekeeper. `template`, `store`† (the store template it opens), `greeting` /
`greeting_text`.

**`[[sale]]`**: what a store's listing shows that the store template lacks. `store`, `ordinal`,
`stack`, `icon` (`{ layer, picture, color }`), `product`†, `cost`†, `currency`†, `name`† /
`name_text`. Who a sale is for (a race, a least level, quests at a status) and whether its store
hides from a player the sales the player may not have (else shows them restricted) are the
install's.

**`[[quest]]`**: a quest's server values. `id` and `id_name`, `state`† (its definition), `challenge`,
`duration` (s of the player's time in the world, 0 for none), `timed_phase` (the one phase the duration runs in, from when that phase comes, shown and able to fail the quest in that phase only; left out, every phase from its giving), `retry` (s, by the calendar, in the world or not), `xp` (left out, as the quest's setup in the install says), `xp_share` (in place of an amount, the
share of what the player's level takes to reach the next that its completion pays, whole; left out, as the setup says), `xp_share_level` (the level
at and above which that share pays no more), `xp_least`, `xp_most` (the least and the most that share pays), `xp_whole` (true: an amount is paid whole, whatever the quest's challenge against the player's level; left out, as the setup says), `cancellable`, `visible`† (false: the quest is kept for
its player but never shown, in no journal and no update; left out, a quest is shown when its
definition has a description), `min_level` (the least level a player is given it at; a person whose
step would give it says its refusal of the quest, a `refuse-use` line naming it, to a player under
it), `fails_on_death` (true: it fails when its player dies), `once` (true: given only once, done never given again; false: given again;
left out, as the quest's setup in the install says), `fellows` (true: a kill's move on it reaches the killer's fellows; false: only the killer; left out, as the quest's setup in the install says, and only the killer for a quest with no setup). Its name, description, icon, journal
and the effects each of its updates puts on the player are the definition's. A phase the definition
says is done by other quests (subquests) gives them with it, kept hidden: steps move them, each
move told as the quest's own record with its phase kept, and the quest moves on to its next phase
once all of them (or one, where the definition says one is enough) are done; from its last phase it
is done, the person who took the last of them saying its `complete` line. A quest that failed
or was cancelled is given again only once its wait is over, as a done one is; a done quest with no wait (`retry`
0 or left out) is given again at once, unless it is done once (its setup in the install says it may be done one
time, or the row says `once`). A person who gives several quests gives one of them at a
use, picked at random, none while one is under way, and, when none of them has a wait, none for two hours of the player's
time in the world after the last it gave (it says its `too-soon` line).

**`[[step]]`**: what moves a quest on. `key`, `quest`, `needs` (the phase it must be at; 0 for not
under way), `trigger`, `tell` / `tell_text` (what the person says), `update` (`bestow`, `advance`,
`complete`, `fail`: a step that fails its quest needs it under way; `none`: it moves no quest, and only says, gives and sends), `phase` (for `advance`), `xp`, `xp_share` (a share of what the player's level takes to reach the next, whole), `least_level`, `most_level` (the levels it runs for),  `gives` (templates), `counts` (how many of each item
given, in order; 1 when left out), `requires`, `takes`, `to`, `effects` (the effects it puts on the
player, by their saved states: a blessing, a recipe learned or forgotten), `text` (a text shown
after the effects, `{ table, string }`), `fellows` (true: the update is made for each of the
player's fellows in the world as well, each told it alone), `races` (the races it is for, by number: 1 human, 2
Lugian, 4 Tumerok, 8 Drudge, 16 Empyrean; every race when left out), `effects_last` (true: the
quest's update is told before the effects and their text, not after them), `wants` (for a give, exactly how many of the item it wants: any other count is refused and handed
back, with the person's `refuse-give` line naming the quest and the `item` if it has one, else its plain refusal; left out, it runs for whatever is given and takes it all).

| `trigger` | moves the quest when the player |
|---|---|
| `{ use = T }` | uses a person or an object of template T (or a held item of it) |
| `{ use = I, on = T }` | uses a held item of template I on an object of template T |
| `{ give = I, to = T }` | gives an item of template I to a person or an object of template T (drags it onto it) |
| `{ arrive = T }` | arrives through a portal of template T |
| `{ take = T }` | takes an item of template T |
| `{ kill = T }` | kills a creature of template T (the effects its template names at its death need no step: they move their quests whatever a step says, on any quest no step moved at that kill) |
| `{ done = Q }` | completes quest Q |
| `{ given = Q }` | is given quest Q, shown or kept hidden, by whatever gives it |

`requires` lists other quests the step needs, each `{ quest = Q, phase = N }` (under way at that
phase; phase 0: not under way), `{ quest = Q, done = true }` or `{ quest = Q, free = true }` (free to
be given: not under way, and never had or its wait over). `takes` lists templates of items taken from the player's
pack, which the player must hold (a hand-in); a give's step that takes the item given keeps it (the rest of a
stack stays), one that does not hands it back after its update, and a give no step takes is handed back with the
person's refusal of a give (its `refuse-give` line). The items a give's step gives come from the person, and one
that moves a quest when taken (`{ take = T }`) moves it after the step's update. A give's step whose effects include the
transformation into a hero (`0x6F001C6F`) runs when the transformation is through, 25.59 s after the give. `to` names a place the step takes the player to,
through portal space: an item's use on an object makes its update on arrival; a use of a person or
an object tells its update at once and takes the player after.

**`[[give]]`**: what a person or an object does with an item given it that moves no quest (a toll is a
quest, even one kept hidden, and is a step). `key`, `to` (the template given to), `item` (the template
given; left out, any item), `wants` (exactly how many of it: any other count is refused, the stack handed
back, with the person's `refuse-give` line naming the item if it has one, else its plain refusal; left out,
whatever is given is taken whole), `gives`, `counts` (what it gives in its place, from the person), `effects`,
`text` (what it puts on the player, cast by the person, and a text after them), `fx` (what the person or the
object plays as it takes the item), `requires` (as a step's; not met, the item is refused). A step the give
runs comes first, and a row for the item comes before one for any item. The person says its `accept` lines at a
give naming the item and no quest, in their `order`, else one of those naming no item.

**`[[talk]]`**: a line a person (or a creature) says, and when. One row per line; a person says the
lines of its rows whose moment and quest match, picking at random among several.

| field | | meaning |
|---|---|---|
| `key` | required | unique in its pack |
| `who` | required | the template that says it |
| `object` | | one placed person only (`key@XXYY`) |
| `line`, `line_text` | one of them | the line: a string reference, in the person's own string table, or new prose |
| `line_name` | | the token name of `line`'s string id |
| `role` | | what it does: `offer`, `remind`, `advance`, `accept`, `complete`, `fail`, `refuse-use`, `refuse-give`, `too-soon`, `use`, `near`, `idle`, `combat`, `death`, `teleport` (said as a person sends a map's holder where it leads), `refuse-map` (said of a map it does not send anyone with) |
| `how` | | `tell` (to the player, naming the speaker; the default), `say` (aloud, to everyone near), `emote` (text naming the speaker), `broadcast` (read by every player in the speaker's landblock and the eight around it, indoors its own landblock, whether their clients know the speaker or not) |
| `when` | required | the moment: `use`, `give`, `attack`, `death`, `near`, `idle` |
| `quest`, `update`, `phase` | | the quest update the line comes with (`bestow`, `advance` and its phase, `complete`, `fail`) |

A `remind` line names its `quest` and no `update`: it is said at a plain use with that quest under way, at the `phase` it names if it names one.
| `item` | | the item given, for a line said when one is: at a give it is said of that item and no other, before the person's plain refusal |
| `order` | | its place in a speech of several lines (0 first) |

A person with a `teleport` line said at a give sends the holder of a surveyor's map given it to the place that names
the map's template (`[[place]]` `named_by`), handing the map back: a map of its own land (the land its template's table
names), or one its `teleport` lines name as their `item`. Any other map, or one no place names, is handed back with its
`refuse-map` line.

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

**`[[weapon]]`**: the weapon a creature wields, where the name its templates give it (an identifier
of the install) is no template of the install's own. `name`, `template`
(the template it is made of), `two_share` (of the creatures whose template asks two of it, the share
given two, the rest one; every one is given two when left out) and `stance` (the stance it is fought
with, where its template sets none).

**`[[death_spawn]]`**: what a creature's death effect makes around its killer, or an item's use effect around its user, where the install names it by a name it doesn't resolve. `effect` (the death effect, as creatures' templates name it), `template` (what it makes), `count` (how many it tries to make; 1 when left out), `chance` (that each is made; 1 when left out) and `offset` (where each stands, in meters from the killer as the killer faces, `[x, y, z]`, on the ground). They stay until killed, no more than 24 of one effect's at once.

**`[[route]]`**: places creatures (and people that name it) walk at rest in turn. `key`; `waypoints` (`{ cell, at, rest }`, `rest`
the seconds a creature stands there, else the route's); `shape`, `back-and-forth` (turn back at either
end, the default) or `loop` (on from the last to the first); `gait`, `walk` (the default) or `run`;
`speed` (meters a second for a creature of scale 1, when not the gait's own pace); `rest` (seconds, for
waypoints that set none; 0 when left out). Several camps may share one route, each with its own start.
A creature that gives up a fight goes back to its route's nearest waypoint and carries on from there.

**`[[area]]`**: the kind of player conflict a landblock allows. `landblock` (`0xXXYY`, outdoors or a
dungeon's), `conflict`: `peace` (no player may fight another), `controlled` (players of different
kingdoms may fight, neutral players stay out of it), `kingdom-vs-kingdom` (players of different kingdoms
may fight) or `free-for-all` (any player may fight any other). A landblock no row names is a peace
area. Players are told the kind of where they are as they enter, walk or arrive; who may fight whom
there is the client's own rule.

**`[[remove]]`**: `items` (or `item`), the items a pack takes away.

## What a row never holds

- the game's own text: names, descriptions, lines, journals (referenced by string id instead);
- bytes of the client's records, or values a compile reads from the install;
- names of players or characters, chat, or anything identifying a recording or the person who made
  it;
- anything from other projects' databases.
