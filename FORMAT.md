# The format

How the database's files are written: the world, its packs, the rows of each kind, their keys and
references, where each row came from, and what a row may and may not hold. `yalain world check`
holds a database to all of it.

## Files

```text
world.toml                         the world: key, game, era, packs in load order, overrides
world.lock                         ids given to authored symbols, kept across builds
<pack>/pack.toml                   name, version, game, authors, license, description
<pack>/server/landblocks/XXYY.toml [[object]], [[camp]] and [[clearing]] rows standing in landblock XXYY
<pack>/server/places.toml          [[place]]
<pack>/server/loot.toml            [[loot]]
<pack>/server/stores.toml          [[keeper]], [[sale]]
<pack>/server/quests/QQQQQQQQ.toml [[quest]], [[step]] of one quest
<pack>/server/gives/TTTTTTTT.toml  [[give]] of one template given to
<pack>/server/talk/TTTTTTTT.toml   [[talk]] of one template
<pack>/server/crafting.toml        [[craft]], [[tool]]
<pack>/server/mines.toml           [[mine]]
<pack>/server/maps.toml            [[map_region]]
<pack>/server/story.toml           [[scene]], [[shard]]
<pack>/server/butchery.toml        [[butchery]]
<pack>/server/weapons.toml         [[weapon]]
<pack>/server/death_spawns.toml    [[death_spawn]]
<pack>/server/death_treasures.toml [[death_treasure]]
<pack>/server/pets.toml            [[pet]], [[pet_limit]]
<pack>/server/pools.toml           [[treasure_pool]]
<pack>/server/effects.toml         [[effect_name]], [[effect_rule]]
<pack>/server/events.toml          [[event]]
<pack>/server/values.toml          [[treasure_value]]
<pack>/server/routes.toml          [[route]]
<pack>/server/areas.toml           [[area]]
<pack>/server/kingdoms.toml        [[points_bonus]]
<pack>/server/popups.toml          [[popup]]
<pack>/server/treasure.toml        [[treasure_rules]], [[treasure_sort]]
<pack>/server/treasure_words.toml  [[treasure_word]]
<pack>/server/treasure_looks.toml  [[treasure_look]]
<pack>/server/treasure_potions.toml [[treasure_potion]]
<pack>/server/treasure_families.toml [[treasure_family]]
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
| `object KEY@XXYY`, `camp KEY@XXYY`, `clearing KEY@XXYY` | the row's `key`, unique within its landblock in its pack |
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
| `death_treasure KEY` | the row's `key` |
| `treasure_pool NAME` | the pool's name |
| `pet 0xEFFECT` | the pet effect (or the contract's template) |
| `pet_limit 0xSKILL` | the summoning skill |
| `treasure_rules` | the world's one row |
| `treasure_sort SORT` | the sort: `weapon`, `armor`, `shield` or `jewelry` |
| `treasure_word SORT 0xWORD` | the sort and the word's string |
| `treasure_look 0xTEMPLATE` | the template |
| `treasure_potion KIND` | the kind's name |
| `treasure_family SORT ORDER` | the sort and the family's `order` |
| `treasure_value LEVEL` | the creatures' level |
| `mine 0xSKILL` | the mining craft skill |
| `map_region REGION` | the region's key |

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
| `treasure-pool-fit` | a pool's templates are those the corpses recorded in 2017 held, each drawn where the dropper's loot base lies in its window (the middle 90% of the bases it dropped at, from 8 drops; the bases seen widened by 3 below that); the kinds lowest in a pool reach down to level 0 and the highest, and those mostly dropped from 45 up, are open above; each weight is fit so that the windows and weights give back each template's recorded count at the recorded bases |
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
| `scale` | | how large it stands, in place of the scale its template gives; a compile keeps the template's, with a warning, when it isn't above 0 |
| `name`, `name_text` | | a name the server gives it (a portal named for where it leads); else the template's |
| `to` | | the place using it takes a player to; a person says its line for a use as it does |
| `landings` | | a lifestone's recall spots: `{ cell, at, heading, seen }` |
| `scene` | | a door's scene: the `[[scene]]` a player plays on the way to `to`, in place of portal space |
| `locked` | statics | a locked door: from its front a plain use is refused and only its key opens it (it locks again as it closes); from behind it opens |
| `lock` | | a locked door's key id: the id (a key's `Lock_KeyID`) a key must carry to open it; none known: no key does |
| `route`, `route_start`, `route_direction` | people | the `[[route]]` a person walks (`key`, or `pack:key`), the waypoint it sets out toward (from 0) and `forward` or `backward`, as a camp's creatures do |
| `recall`, `summon` | statics | a portal a player who used it may recall to (`recall = true`: a recall to the last portal used returns there) and summon a portal to (`summon = true`); left out, neither |
| `requires` | statics | the quest a player must hold to use it (a portal this placement keeps closed, over its template's): `{ quest = Q, done = true }` (completed), `{ quest = Q, underway = true }` (under way at any phase), `{ quest = Q, phase = N }` (under way at that phase) or `{ quest = Q, had = true }` (failed, completed or under way); a use or a walk-in it keeps out is refused at once |
| `min_level` | statics | the least level a player must be to use it, over its template's; its examination names it, and a use or a walk-in of a portal below it is refused at once |
| `hero` | statics | true: only a hero may use it; its examination says so, and anyone else's use or walk-in of a portal is refused at once |
| `kingdom` | statics | the kingdom a player must be of to use it, by the number a character's description names it: 1, 2 or 4; its examination names it, and anyone else's use or walk-in is refused at once |
| `event` | | the `[[event]]` (its `key`) it stands for: it is in the world only while the event is on, made for those who see it as the event starts and forgotten as it ends; while it is off a use of it, a walk into it or a give to it finds nothing |

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
| `name` | | the name its creatures are told by, examined by and their corpses named after, in place of their template's: `{ table, string }`, a string of the install (a creature of an ordinary kind that a quest names as one) |
| `event` | | the `[[event]]` (its `key`) it keeps its creatures for: none while the event is off, filled as it starts, and its creatures leave the world as it ends |

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
`duration` (s of the player's time in the world, 0 for none), `timed_phase` (the one phase the duration runs in, from when that phase comes, shown and able to fail the quest in that phase only; left out, every phase from its giving), `retry` (s, by the calendar, in the world or not), `cancel_wait` (s, by the calendar, from 0: the wait after its player cancels it before it is given again; left out, 300, except that a world whose rows name none has the server's own five hours for the quests 2017 gave them), `xp` (left out, as the quest's setup in the install says), `xp_share` (in place of an amount, the
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
or was cancelled is given again only once its wait is over (a cancelled one's its `cancel_wait`), as a done one is; a done quest with no wait (`retry`
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
player's fellows in the world as well, each told it alone; what the step takes and gives is the player's alone, and a fellow
needs only the phase and what the step requires), `races` (the races it is for, by number: 1 human, 2
Lugian, 4 Tumerok, 8 Drudge, 16 Empyrean; every race when left out), `effects_last` (true: the
quest's update is told before the effects and their text, not after them), `wants` (for a give, exactly how many of the item it wants: any other count is refused and handed
back, with the person's `refuse-give` line naming the quest and the `item` if it has one, else its plain refusal; left out, it runs for whatever is given and takes it all), `transforms` (a give's step that makes its player a hero: `{ seconds, fx, behavior, text, name }`, below).

| `trigger` | moves the quest when the player |
|---|---|
| `{ use = T }` | uses a person or an object of template T (or a held item of it) |
| `{ use = I, on = T }` | uses a held item of template I on an object of template T |
| `{ give = I, to = T }` | gives an item of template I to a person or an object of template T (drags it onto it) |
| `{ arrive = T }` | arrives through a portal of template T |
| `{ arrive = T, from = O }` | arrives through the one placed portal O (its `id`), of template T |
| `{ take = T }` | takes an item of template T |
| `{ kill = T }` | kills a creature of template T (the effects its template names at its death need no step: they move their quests whatever a step says, on any quest no step moved at that kill) |
| `{ kill = T, camp = K }` | kills a creature of template T that the one camp K made: its `key`, or `key@XXYY` where camps of several landblocks share the key; the camp must make T. A quest a step of T alone moved at that kill isn't moved again |
| `{ done = Q }` | completes quest Q |
| `{ given = Q }` | is given quest Q, shown or kept hidden, by whatever gives it |

`requires` lists other quests the step needs, each `{ quest = Q, phase = N }` (under way at that
phase; phase 0: not under way), `{ quest = Q, done = true }` or `{ quest = Q, free = true }` (free to
be given: not under way, and never had or its wait over); and `{ event = "key" }`, an `[[event]]` that
must be on for the step to run. `takes` lists templates of items taken from the player's
pack, which the player must hold (a hand-in); a give's step that takes the item given keeps it (the rest of a
stack stays), one that does not hands it back after its update, and a give no step takes is handed back with the
person's refusal of a give (its `refuse-give` line). The items a give's step gives come from the person, and one
that moves a quest when taken (`{ take = T }`) moves it after the step's update. A give's step that `transforms` its
player keeps the gift at once and plays the appearances `fx` and the `behavior` on the player, and runs `seconds` (from 0)
after the give's answer, if it still may (at once if the player leaves the world first): the player is then made a hero,
before its effects, and told `text` (`{ table, string }`), its name in the text's variable `name` (only with a text). A world
whose steps name no `transforms` has the server's own on a give's step putting on the hero's transformation (`0x6F001C6F`):
25.59 s, as 2017's; a world with any has its rows alone. `to` names a place the step takes the player to,
through portal space: an item's use on an object makes its update on arrival; a use of a person or
an object tells its update at once and takes the player after.

A step's or a give's `requires` may also name one kingdom, `{ kingdom = "order" }`: `neutral`, `shadow`,
`order` or `dominion`. It then runs only for players of that kingdom, a player in no kingdom counting as of
the neutral one, as at a faction shrine, and only when its other requirements are met too. A give it
refuses is refused as any other, the item handed back. Any other word, or a second kingdom, is a problem.

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

**`[[tool]]`**: what a gathering tool (a knife or a mining tool) yields when it was not made: `template` (the
tool's) and `yield` (a count). A made tool's yield is its own; a tool that was not made and that no row names yields
1, except a mining tool of a world with no `[[mine]]` rows, which yields what the server's own say.

**`[[mine]]`**: what the nodes of a mining craft skill do. One row per skill.

| field | | meaning |
|---|---|---|
| `skill` | required | the craft skill (its saved state); a node mined by it is the row's |
| `behavior` | required | the behavior a miner plays with none of the skill's tools in hand |
| `tools` | | the skill's own tools: one in the miner's hand plays its own use behavior, adds its yield (`[[tool]]`) to a summoned node's units, and wears |
| `answer`, `rich_answer` | required | string references: what a use answers, plain and when it finds twice the units |
| `delving` | | `{ effect, node }`: the name of the effect a stone's use conjures the skill's node by, and the node (a template the install gives a material when mined) |
| `lodestones` | | `{ from, template }`, levels rising from 0: the lodestone a find unearths, the last whose `from` the finder's level reaches |
| `find_chance` | | from 0 to 1: how often a use of the skill's node a map led to is a find in place of its material; 0 when left out |
| `finds` | | `{ template, share }`: the other items a find may be, each by its share of finds, above 0 and at most 1 in all; the rest are lodestones |

A world with no `[[mine]]` rows has the server's own, those of the five mining skills as 2017 had them; a world
with any has its rows alone.

```toml
# <pack>/server/mines.toml
[[mine]]
skill = 0x6F00069C
behavior = 0x4100014D
tools = [0x47000CC1, 0x47000CC2]
answer = { table = 0x25000CEC, string = 0x79C276DB }
rich_answer = { table = 0x25000CEC, string = 0x53EE7371 }
delving = { effect = "Eff_SummonMine_Copper_Hills", node = 0x47000C8C }
lodestones = [{ from = 0, template = 0x47000C16 }, { from = 30, template = 0x47000C14 }]
find_chance = 0.05
finds = [{ template = 0x4700052F, share = 0.25 }]
prov = { from = "authored", by = "you" }
```

**`[[map_region]]`**: the nodes a region's surveyor's maps lead to. `region` (a key: lowercase letters, digits and
hyphens) and `nodes`, at least one `{ effect, node }`: the name of an effect a map's use names, and the node it
conjures where the map leads (a template the install gives a material when mined). A map whose effects no row names
is no map. A world with no `[[map_region]]` rows has the server's own, Linvak's, Omishan's and Osteth's; a world with
any has its rows alone.

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

**`[[death_spawn]]`**: what a creature's death effect makes around its killer, or an item's use effect around its user, where the install names it by a name it doesn't resolve. `effect` (the death effect, as creatures' templates name it), `template` (what it makes), `count` (how many it tries to make; 1 when left out), `chance` (that each is made; 1 when left out) and `offset` (where each stands, in meters from the killer as the killer faces, `[x, y, z]`, on the ground), and `lasts` (how long each stands, in seconds). They stay until killed when it's left out; a kill's make no more than 24 of one effect's at once, and a use has no such limit.

**`[[death_treasure]]`**: a fixed item a creature leaves at its death, or a chest at an opening, at a chance of its own. `key`; `template` (every creature or chest of it) or `camp` (every creature the camp keeps: `key@XXYY`, or `pack:key@XXYY` in another pack), one of them; `item` (the item's template) and `chance` (above 0, at most 1). Each is rolled once as the corpse is made, after the rest of what the creature leaves, and a full corpse still holds it. Only a creature a camp keeps leaves one, so it comes no faster than the camp makes the creature again; a chest's comes only with an opening its key paid for, as a chest is filled anew at every opening. A corpse or chest holds an item once, and two rows giving the same creatures or chests one item are refused.

A `[[loot]]` row may draw its items from treasure pools instead of `items`: `draws` (`{ pool, weight, least, most }`, each draw one of them by weight among those whose window holds the level of the item; `least` and `most` may be left out), and `rare` (`{ pool, chance }`, rolled once a corpse). The level of the item is the creature's loot base, its loot quality in tens, else its level. Its `counts` and the template's bounds give how many items, its extras among them and its template's trophies beside them.

**`[[treasure_pool]]`**: a named pool treasure is drawn from. `name` (the install's name for it, `GP_...`); `pools` (`{ pool, weight, least, most }`) and `items` (`{ template, weight, least, most }`): a draw takes one of them by weight among those whose window holds the level of the item and goes on down until it reaches a template, giving nothing where none holds the level; `race` (`human`, `lugian`, `tumerok`, `drudge`, `empyrean`) and `own` (a share): a draw from its parent by a killer of its race takes this pool at that share outright, the rest drawn by weight. A pool may not lead back to itself, and a draw goes at most eight pools deep.

**`[[pet]]`**: what a pet effect makes, or what a contract hires, as the effect's description gives it and
the recordings show it fight. One row for each effect.

| field | | meaning |
|---|---|---|
| `effect` | required | the pet effect's saved state, or the contract's template, or for a pet only items make (one with `item_effects` and no pet effect of the install) the item's template |
| `template` | required | what it makes; a compile refuses a template the install lacks |
| `flags` | | the flags of its pet data as its owner is told them; 0 when left out |
| `count` | | how many the effect makes at once, at least 1; 1 when left out |
| `stays` | | true: it stays where it is made and never follows, taking on what comes within its reach |
| `health` | | its greatest health at levels, `{ level, health }`, levels going up: between two the line, beyond the first and last held; its template's when left out |
| `per_level_squared`, `variance`, `lands` | | what a hit of it takes: `per_level_squared` times its level squared (0.05 when left out), varied by `variance` either side (0.35), less the target's armor; `lands` is the share of its strikes that land, from 0 to 1 (0.8) |
| `swing` | | hits a swing on its one target, at least 1; 1 when left out |
| `area` | | its missile lands on every creature this many meters from where it falls; left out, on its target alone |
| `taunts` | | true: its strikes taunt, and the creature may turn on it; whether they harm is its skill's |
| `ends_on_strike` | | true: it ends as its first strike lands, what the strike carries landing first |
| `vigor_per_level` | | its greatest vigor for each level; the pets' own when left out |
| `vigor_per_second` | | it pays its attacks' vigor, which comes back this much a second; left out, its attacks cost it nothing |
| `outdoors_only` | | true: it can't be set down indoors, and a summoning there fails |
| `attacks` | | the attacks it uses, `{ skill, weight }`, each skill once and each weight at least 1: of those that reach its target it draws one by weight. Each skill must be one its template names, or a compile refuses the row. Left out: every attack its template names, all alike |
| `corpse_after` | | seconds after its death its corpse comes; 1.5 when left out |
| `no_corpse` | | true: it leaves no corpse |
| `tends` | | whom it tends: `{ whom = "owner" or "owners-pets", effect, every, below }`, the effect it puts on them at its own level, every `every` seconds, while their health is below the share `below` of the whole |
| `hire` | | a contract's terms, the row's `effect` being the contract's template: `{ class, seconds, level }`, the mercenary's class of pet, how many seconds it stays and its level. On a row with `item_effects` whose `effect` is no pet effect of the install, the terms the item's pet is made on, and the row is no contract |
| `item_effects` | | names of effects an item's use may name that no install holds, each making this pet as its own effect does |

**`[[pet_limit]]`**: how many pets a summoning skill allows its user. `skill` (the skill's id) and `limits`,
at least one `{ most, classes }`: a use is refused while its user has `most` pets of a class sharing a bit
with `classes`, a pet's class being its effect's. A skill no row names goes by each kind of pet's own limit
of its class; a pet an item's use makes keeps to the limits of a skill that makes the same pet; and no
player has more pets in all than the server allows.

**`[[treasure_value]]`**: what treasure a creature of a level leaves is worth. `level` (the creature's level) and `values` (whole numbers, at least one): each treasure item the creature leaves carries one of them as its own value, drawn evenly, so a value listed twice comes twice as often; selling it pays that. A level with no row draws from the nearest level that has one (the lower of two as near); a world with none has the server's own instead, a band of values for each ten levels up to 50. A rare and a trump of the tarot never carry one.

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

**`[[points_bonus]]`**: what an effect does to the kingdom points of the player it is put on (by a give or a
quest step), where the install's record of the effect gives no amount. `effect` (its saved state, one the install
holds), `add` (above 0) and `up_to` (kingdom points, a whole number the points can hold): the points rise by
`add`, never above `up_to`, and points already at or above it stay as they are. A give that gives nothing and
whose only effects are such bonuses, the player's points already at or above every one's `up_to`, is refused as a
give no row takes: the item is handed back. A player's points start at 500
and are kept with the character. After the rise, the kingdom skills the player's own kingdom's shrine grants
at those points are granted at once, as a use of the shrine grants them. One row per effect.

```toml
# <pack>/server/kingdoms.toml
[[points_bonus]]
effect = 0x6F00188E
add = 200
up_to = 1500
prov = { from = "authored", by = "you" }
```

**`[[popup]]`**: a tip a player is shown once, in a box of its own, the first time a moment comes for its
character. `on`, the moment: `first-entry` (the character's first entry into the world, as its session starts),
`level-up` (its first level gained, after the level's own line) or `glyph` (when a glyph first comes into its
hands, taken or given, before any quest the glyph moves); `effect`, the saved state of an effect of the install,
whose description is the tip (`yalain world check --dats <install>` holds it to the install and to having a
description). Each moment comes once per character, a tip or none: a tip added later is not shown for a moment a
character passed before it, and a character kept before tips were shown has passed them all. One row per moment.

```toml
# <pack>/server/popups.toml
[[popup]]
on = "level-up"
effect = 0x6F001925
prov = { from = "authored", by = "you" }
```

**`[[clearing]]`**: ground in a landblock kept free of what the land grows, written in
`server/landblocks/XXYY.toml`. `key` (unique in its landblock in its pack), `at` (`[x, y, z]`, x and y in
meters within the landblock, from 0 up to 160), and its shape, one of: `radius` (a circle) or `size`
(`[x, y]`, a rectangle along its own axes), each above 0 and at most 240 meters; `heading` turns a
rectangle, in degrees clockwise from north. The world builder builds it into the client's data; the
server has no use for it.

**`[[effect_name]]`**: the saved state an effect's name stands for, where the install names the effect
(an item's use, a wearer's or a death's effect) and the server can't resolve the name: `name` (the name, as
text) and `state` (the saved state, `0x6F...` or `0x70...`). A name the server already resolves (by its effect
enumeration's value and the install's one effect of that value, or by a package of the name) can't be given a
row: `yalain world check --dats <install>` says which state it resolves to.

**`[[effect_rule]]`**: what an effect of the install does where its own data says nothing. `effect` (its saved
state, one the install holds), and a `ward`, a `vitae_share` or both. `vitae_share`: the share of its player's vitae
the effect takes when it is put on, above 0 and at most 1, the effect's own appearance played on the player; a world
whose rules name none has the server's own (the tap `0x6F001C64`, a tenth), one with any its rows alone.
`ward`: `{ classes, effects, chance }`, what a player holding it keeps off:
effects of these classes and these effects (saved states the install holds), at least one of either, each kept off
by `chance`, above 0 and at most 1, at any spellcraft. Of a player's wards of one class only the top one draws. A
ward whose own data names what it keeps off needs no row; one whose data names nothing keeps off nothing without
one. One row per effect.

```toml
# <pack>/server/effects.toml
[[effect_rule]]
effect = 0x6F002672
ward = { classes = [48, 1119, 5013], chance = 0.15 }
prov = { from = "authored", by = "you" }

[[effect_rule]]
effect = 0x6F001C64
vitae_share = 0.1
prov = { from = "authored", by = "you" }
```

**`[[treasure_rules]]`**: what every treasure item draws by, whatever its sort. `above_base`: weights of an
item's own least level standing 0, 1, 2, ... above its dropper's base (numbers from 0, at least one above 0);
`most_level`: the highest least level an item's own may be (1 or more); `lore = { above, from, to }`: an item needs
lore to use only when its dropper's base is above `above`, read through the game's lore table at a level drawn
evenly from the base plus `from` to the base plus `to` (`from` at most `to`); `potion_tiers`: the least dropper
level of each of a treasure potion's five tiers, from 0 and rising; `potion_spellcraft = [least, most]`: a potion's
spellcraft, drawn evenly; `look = { glow_most, round_chance, round_from, round_tenths }`: a glow is drawn evenly up
to `glow_most`, and a color whose key's highest is `round_from` or more is, by `round_chance`, one of the first
`round_tenths` round tenths (0, 0.1, ...), else drawn in hundredths up to its key's highest (the first three from 0
to 1, `round_tenths` 1 or more). A world has one row, or none and the server's own.

**`[[treasure_sort]]`**: the numbers one sort of treasure item draws by. `sort` (`weapon`, `armor`, `shield` or
`jewelry`) and `counts`: bands of the item's own level, `[{ from, weights }]`, `from` the band's least level (the
first 0, then rising), `weights` how often an item of the band has 0, 1, 2, ... enchantments (from 0, at least one
above 0); weapons, armor and shields have six bands, as the words before their names are drawn by the same bands.
Beside them, each sort has its own fields and no others:

- weapons and shields: `damage_share = [least, most]`, their greatest damage as a share of a made weapon's at their
  level, drawn evenly; `vigor`, bands of the vigor they cost, `[{ from, least, most, every }]` (`from` the first 0
  and rising, `least` 1 or more and at most `most`), each drawn evenly from `least` to `most`; `every`, only on the
  last band, adds one to both for each that many levels above its `from`;
- shields: `span = [least, most]`, their span of damage when their template names none, drawn evenly;
- weapons, armor and shields: `delays = { from, weights }`, how often each delay between blows from `from` (0 or
  more) up is drawn;
- armor and shields: `rating_share`, their rating as a share of a made one's at their level, as points `[[level,
  share], ...]` (levels from 0 and rising, shares from 0 to 1) in proportion between them and held past the ends;
  `rating_spread`, how far either side of it each is drawn, evenly; `slot_chance`, how often one has an
  enchantment slot (robes always have three, weapons one).

Shares and chances are from 0 to 1, least at most most. A world gives all four sorts or none: a world with none
has the server's own, and one with some but not all is refused. A sort's families of enchantments and its words
are the server's own.

```toml
# <pack>/server/treasure.toml
[[treasure_sort]]
sort = "jewelry"
counts = [{ from = 0, weights = [9.0, 1.0] }, { from = 25, weights = [1.0, 1.0] }]
prov = { from = "authored", by = "you" }
```

**`[[treasure_word]]`**: a word before treasure items' names. `sort` (`weapon`, `armor` or `shield`); `order`, its
place in the order its sort's words are drawn in (each once in a sort); `word`, its string in the install's table of
these words (`0x2500035F`); `delays = [least, most]`, the delays between blows it goes with; `weights`, its weight in
each band of its sort's `counts`, one a band (the world's bands, or the server's own six), from 0 and at least one
above 0. Once its effects have changed an item's numbers, the item takes one of the words that go with its delay, by
their weights in its level's band, else one of its band's; with none weighted in the band, the plain word. A world
whose sorts' counts have other bands than the server's own six gives its own words. The check warns of a band no word
of a sort is weighted in.

```toml
# <pack>/server/treasure_words.toml
[[treasure_word]]
sort = "weapon"
order = 0
word = 0xEF4F89B9
delays = [7, 18]
weights = [0.0, 136.0, 149.0, 29.0, 0.0, 0.0]
prov = { from = "authored", by = "you" }
```

**`[[treasure_look]]`**: the look a template's treasure items draw. `template`; `table`, the appearance table it is
drawn in (a record of the install); `keys`, one to three `{ key, most }`, each key and the highest value it draws, from
0 to 1, drawn as `[[treasure_rules]]`'s `look` says. A template with no row draws no look of its own.

**`[[treasure_potion]]`**: a kind of treasure potion. `kind` (lowercase letters, digits and hyphens), `order` (its
place in the order the kinds are drawn in, each once) and `states`, its effect's saved state at each tier from the
lowest, one a tier of `[[treasure_rules]]`'s `potion_tiers` (the world's, or the server's own five). A treasure potion
draws its kind evenly and takes its dropper's tier.

**`[[treasure_family]]`**: a family of enchantments one sort of treasure item draws from. `sort` (`weapon`,
`armor`, `shield` or `jewelry`); `order`, its place in the order its sort's families are drawn in; `when` (`permanent`,
on the item itself; `equipped`, on whoever wields or wears it; `hit`, on what it hits); `weight`, how often it is
drawn against its sort's others (0 or more: a family of weight 0 comes only as another's pair); `by_level`, whether an
item's level takes the family's one tier it reaches last, else any tier it reaches, evenly; and `tiers`, at least one,
each `{ least, state, puts_on, chance, glow, pair, named }`: `least`, the least level of an item that reaches it (from 0, and
rising in a family by level); `state`, the enchantment (a saved state of the install, a tier of one family alone);
`puts_on`, what it puts on what the item hits, only in a family of `hit` (left out: nothing); `chance`, how often it
does, from 0 to 1; `glow`, the glow it gives weapons (0 for none), from 0 to 1; `pair`, an enchantment (a tier's
state in some family) that comes with it in the same draw; `named = false`, never the one an item is named for. An
item draws no family twice. A world that gives any families gives every sort's it means to: a sort with none draws no
enchantments. `yalain world check` warns of the server's own enchantments a world's families leave out: an item that
carries one keeps it, but it puts nothing on what the item hits and shows as the item's own.

```toml
# <pack>/server/treasure_families.toml
[[treasure_family]]
sort = "jewelry"
order = 0
when = "equipped"
weight = 1.0
by_level = false
tiers = [
    { least = 44, state = 0x6F000664, chance = 1.0, glow = 0.0 },
]
prov = { from = "authored", by = "you" }
```

A world with no rows of one of these kinds plays the server's own of that kind, those fit to the 2017 servers'
items, and its server says so at start. A kind's rows are taken whole, never mixed with the server's.

**`[[event]]`**: a named state of the world, on for its times. `key` (lowercase letters, digits and
hyphens); `game_event`, a value of the install's game events it stands for (optional; `yalain world check
--dats <install>` holds it to them); `when`, at least one window: `{ from, until }`, a dated one, each a UTC time
`YYYY-MM-DDTHH:MMZ` (seconds may follow), the end after the start and not included; or `{ days, from, until }`,
a weekly one, `days` from `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun` and the times of day `HH:MM`, UTC,
running into the next day when `until` is not after `from` (the same time: a whole day); `on_players`, effects
(saved states) every player in the world holds while it is on, each put on at spellcraft 1 and running out as
the event ends, and given to a player who comes into the world while it is on (one already holding a running
record of the effect isn't given a second). Times are UTC for every world, whoever plays it. What an event
gates names it: a camp's or an object's `event`, a step's `requires = [{ event = "key" }]`; each must name an
event of the world. A world with no events gates nothing.

```toml
# <pack>/server/events.toml
[[event]]
key = "harvest-fair"
when = [{ days = ["sat", "sun"], from = "18:00", until = "02:00" }]
on_players = [0x6F001C71]
prov = { from = "authored", by = "you" }
```

**`[[remove]]`**: `items` (or `item`), the items a pack takes away.

## What a row never holds

- the game's own text: names, descriptions, lines, journals (referenced by string id instead);
- bytes of the client's records, or values a compile reads from the install;
- names of players or characters, chat, or anything identifying a recording or the person who made
  it;
- anything from other projects' databases.
