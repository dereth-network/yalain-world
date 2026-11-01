# yalain-world

The world database for Yalain, a Dereth Network reimplementation of the Asheron's Call 2 game server. The intended target for the world database is currently the set of content present at the end of retail service, otherwise known as the era `eor`.

## Format

The world is built up from a collection of TOML-based rows, described in [FORMAT.md](FORMAT.md). Rows describe templates, cells, string tables and enum values, consistent with the game DAT files; short identifiers (generator profile names, quest names, destination keys) are beside raw numbers so a tool can read the rows without fully parsing DATs.

## Contents

`seed-2017/` was derived from community pcap archives generated in January 2017.

`seed-2017-talk/` is what NPCs say and when: the lines heard in those recordings, plus the other
lines in each NPC's string table, placed by what their names say they are for.

`fix-start/` sends the start halls' quick exits where each hall's shard leads; no recording shows a
trip through one.

`start-crafting/` is what a new character knows of crafting (every craft skill and the starting
recipes, as the 2017 servers gave every new character), and what the start area's quest steps put on
the player: the Arwic obelisks' blessings, the Arwic mines' recipe and iron, the miller's focus.

`story-scenes/` is the story's scenes as the January 2017 servers sent them (their pictures, voices
and subtitles by id), the shards that bestow them, and the scenes every new character holds.

`craft-butchery/` is what butchering a corpse yields (each butchery profile's materials and their
shares, as 2017's butcheries cut them) and a start-area quest's weapon recipes, three for each race.

Every row's `prov` says where it came from: `capture` (measured; with an `AC2-EVID-...` evidence handle naming the extraction, an opaque reference to the recording, the confidence and the sample counts), `derived` (computed by a rule listed in FORMAT.md), `dat` (a record rooted in the client DATs) or `authored` (written by a person).

## What's Missing

A lot. There is no known server data to reference, so most of the world is missing, and filling it in is where contributors can help. The client's DATs show how much there is to fill:

| | in the client DATs | in the database |
|---|---:|---:|
| landblocks with something built on them | 2,221 | 717 with people or objects |
| NPC templates | 912 | 418 placed |
| creature templates | 2,578 | 935 in a camp |
| generator profiles | 2,143 | names only, no contents |
| loot profiles | 880 | 341 |
| item magic effects | 720 | none |
| store templates | 1,008 | 12 with listings |
| storekeeper templates | 126 | 17 placed |
| quests | 2,323 | 252, 18 with their steps |
| lines in NPCs' string tables | 51,296 | 5,510, 1,033 of them heard in 2017 |

## Contributing

The seed packs, `seed-2017/` and `seed-2017-talk/`, are written by the project's builders from the
recordings and are never edited by hand. Changes go in authored packs that lie on top of them:

- **`fill-<area>/`** fills a hole: people in a town, camps in a valley, a quest's steps
  (`fill-millstone`, `fill-quest-kill-red-wasps`).
- **`fix-<topic>/`** corrects seed rows: it sets a row with the same key, and `world.toml` says it
  wins (`[[override]] pack = "fix-arwic-camps" over = "seed-2017"`).

A pack is listed in `world.toml`'s `packs`, after the seed packs. Write rows with `prov = { from =
"authored" }` (and `by`, `note` if you like). Never paste the game's own text into a row: reference
it by string id. New text a world needs belongs, by preference, in new string-table entries of that
world's data overlay, referenced by id; a `*_text` field holds it only when that is not possible.

Before sending a change, `yalain world check .` must report no problems. Contributions are accepted
under CC0-1.0.

## Releases

A release is a tag `vX.Y.Z` and one archive, `yalain-world-<tag>.zip`: `world.toml`, `world.lock`, the packs, this file, the license and a `manifest.json`, with its SHA-256 beside it. The archive is the same bytes for the same files, so `yalain world release . --tag vX.Y.Z` rebuilds any release exactly.
