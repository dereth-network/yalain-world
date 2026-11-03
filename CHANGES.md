# Changes

## v0.26.0

- Quests that other quests require have rows, so a quest asking for one can see it. New pack `required-quests/`.
- The explorers and obelisks send their seekers from stone to stone, and more people and gates that send whoever uses them
  have their destinations. New pack `person-trips/`; a step triggered by a use may name `to`.
- More people say their own lines as they give, remind of and take back their quests. New pack `quest-lines/`.
- The postings boards give one quest at a time, with a wait after each, from level 70. New pack `postings/`; a step's
  `requires` may ask that a quest be `free`.

## v0.25.0

- Many more of the quests creatures' deaths move can be taken from the people and postings boards who give them. New
  pack `kill-quest-givers/`.
- Those quests, and hunts whose last phase says to return, can be handed back. New pack `kill-quest-returns/`.

## v0.24.0

- Killing creatures moves the quests their deaths name, and a kill can give a quest. New pack `kill-quests/`; quests
  may name `fellows`.
- Portals that led to the wrong place now lead where they led in 2017, and more placed portals that led nowhere have
  their destinations. New pack `fix-portal-landings/`.
- The town hunts and some errands can be taken from the people who give them and handed back to them. New pack
  `fill-quest-givers/`.

## v0.23.0

- Many more people and objects take items handed to them and move their quests along, each quest from its start to
  its end. New pack `quest-hand-ins/`; a step's `requires` may name phase 0 (the quest not under way).
- Errands can be done again, and people with several hand them out one at a time. Quests may name `once` (the install's
  setup decides when left out); lines may have the role `too-soon`.
- Maps handed to the people who read them send players where the maps lead, and two quest mines are placed. New pack
  `maps-and-mines/`; a place's `named_by` may name maps, and lines may have the role `refuse-map`.
- Five storekeepers whose stores opened empty now sell their wares, and three stores list all their sales. New pack
  `store-listings/`; sales may follow the rule `store-sales-unseen`.
- The kingdom-against-kingdom, controlled and free-for-all areas are marked. New pack `conflict-areas/`; rows of the
  new kind `[[area]]`.
- Quest items, keys and mushrooms lie where they lay in 2017 and come back after they are taken. New
  pack `lying-items/`; a camp's spawns may be items.
- Chests the world put out in 2017 stand in their places. New pack `spawned-chests/`.
- Six placed portals that led nowhere take players where they took them in 2017. New pack `portal-trips/`.
- Portals say whether a player can recall and summon to them, and the cities' recalls have their places. New pack
  `portal-recall/`; objects may name `recall` and `summon`, and a place's `destination` is looked up by name.

## v0.21.0

- Items handed to people and shrines move their quests, the hero's gem among them. New pack `gives/`; steps may
  name `{ give, to }`.

## v0.20.0

- Kingdom stones, quest shrines, the Cauldron and the Hero Shrine move their quests. New pack `quest-uses/`;
  quests may name `min_level` and `fails_on_death`, and list subquests.

## v0.19.0

- Some placed orbs answer a use with their line. New pack `object-lines/`.

## v0.18.0

- Vault, cache and Dominion Center portals keep out who 2017 kept out. New pack `portal-gates/`;
  objects may name `requires`.
- Four more Shaper's hoards can be entered. New pack `hoard-entrances/`.

## v0.17.0

- Hoard keys open their hoards to the whole fellowship. New pack `hoard-keys/`; steps may name `fellows`.
- 70 quests run out at the time limits 2017 gave them. New pack `quest-durations/`.
- The Sentries walk their rounds. New pack `people-routes/`; people may name a route.

## v0.16.0

- The patrolling guards walk the routes they walked, and camps can set how their creatures move. New
  pack `patrol-routes/`, new `[[route]]` rows.

## v0.15.0

- Reward quests are done with the quests they reward, and the iron hoard has its mine quest. New pack
  `hidden-quests/`.

## v0.14.0

- Four creatures broadcast their idle emote to the landblocks around them. New pack `creature-emotes/`.

## v0.13.0

- The quests 2017 players held are all defined. New pack `quest-catalog/`.
- The iron hoard's veins stand where they stood. New pack `hoard-veins/`.

## v0.12.0

- Glyphs open their vaults, and each vault leads somewhere. New pack `glyph-vaults/`.

## v0.11.0

- Locked doors hold from their front and open to their keys. New pack `door-locks/`.
- Chests hold what the recorded chests held. New pack `chest-loot/`.

## v0.10.0

- Creatures hold weapons that no template names, and every turret spot is filled. New packs
  `creature-weapons/` and `fix-camps-turrets/`.

## v0.9.0

- Camps no longer make players' pets and summons. New pack `fix-camps-summons/`.

## v0.8.0

- Market-room, vault and dungeon doors play their scenes. New pack `market-doors/`.

## v0.7.0

- Butchering some creatures can find nothing.
- The Esper Warder's quest update comes before its recipes.

## v0.6.0

- Butchering corpses yields bone, hide, tallow, sinew or chitin, by creature. New pack
  `craft-butchery/`.
- A start-area quest gives each race its own three weapon recipes.

## v0.5.0

- The story's scenes and the shards that bestow them: 62 scenes, 24 shards, the 30 scenes a new
  character holds. New pack `story-scenes/`.

## v0.4.0

- New characters know their craft skills and starting recipes. New pack `start-crafting/`.
- The Arwic obelisks and the explorer bless the player; the Arwic mines give the sword's recipe and
  twenty iron; the miller renews the player's focus.

## v0.3.0

- The start halls' quick exits go somewhere: where each hall's shard leads. New pack `fix-start/`.

## v0.2.0

- What NPCs say and when: 5,510 lines in a new pack, `seed-2017-talk/`.
- The start area's quests have their steps: 162 steps of 18 quests.
- Quests say how long before they can be done again.
- Every key from v0.1.0 is kept.

## v0.1.0

- The first release: the whole world as the January 2017 recordings show it. 2,450 people and
  objects, 13,098 spawn camps, 321 portal destinations, 341 loot profiles, 17 storekeepers and 144
  store listings, 251 quests and the training hall quest's steps, every row with its provenance and
  confidence.
