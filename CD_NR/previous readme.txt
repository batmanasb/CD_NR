At this point, I've just about finished the terrian physics and objects. I've decided to make all interactions
collision based, meaning all interactions such as damaging, standing on, and land staying in place/falling are
on how many and what type of object's hitboxes they collide with.
 
The "Land" blocks come in 4 modes: 
*"joint" is the most basic, it require no structual support to stay in place. (0 collisions) These will be used
 for holding most building and etc in place.
*"stone" is needs to be touching one other block in order to stay in place. (1 collision) Stones will be the
 building blocks of most structures.
*"bridge" is a little more complex as it requires two other blocks to stay up. (2 collisions) Bridges will be
 used for adding interesting effects to building, such as bridges, stairs, and etc that create a chain reaction
 when one piece breaks.
*"unstable" is just blocks requiring 3 collisions, at this point it is just a place holder. I'll add new collison
 types as i see a use for them.
 
Most of my time recently has been spent on optimizing collision checks, I've managed to make the frame rate stay
at a playable 30 (30 is the max) around all parts of the level, with up to 140 "Land" objects on screen, or 5 rows
of blocks of "stone" or "bridge". The "joint" blocks affect performance minimally, allowing a full screen of them.
(around 10 rows or 280 objects on screen). As I hinted about above, I've designed the game so that only the blocks
in the player's sight range are drawn, and one block more in both dirrections for collision checks. That way I can
add over a thousand objects to the map, while keeping the performance playable.

Another two features I've finished are side scrolling and scaling. After hitting the surface size limits, I've
decided on a set size for the levels at 200 blocks wide. Scrolling is locked to the right of player's location,
so that the player can see where s/he's going. Everything is the level nearly accurately scales accross all
three different resolutions.

The player's movement has been fine tuned to make navigating the blocks more fun. The player will bounce off blocks
that he runs into, and can fall or jump nearly realistically. Since everything is collision based, standing on the
ground is based on the player's feet's collision with the ground. To make sure s/he doesn't fall too far into a
block, the player move's up out of blocks if his chest is also colliding with the block. (the player is a
combination of 3 objects and 4 hitboxes, top[area around head], head, chest, and feet) This feature created a fun
little bug I like to call "edge bouncing." If you just at the edge of a block, you bounce up a little higher than
a normal jump. i decided I like this "feature" so I've fine tuned it too.

The last feature I've developed is a place holder for weapons. The mouse curser is a box that damages blocks. It
does more damage based on how long the collisions last.



To be developed(currently planned features):
-weapons:
	-weapons will range from melee to ranged, and from swords to rifles to homing missles
-AI:
	-normal enemies about your size
	-weird enemies ranging in sizes
	-normal bosses
	-final boss
	-your wife (check the pitch doc)
-levels
	-somewhat randomly generated, but preplaned types, such as bridge, cave, flat, etc.
	-game should reset and load a new level every time
-art/animations
	-currently the game is using placeholder textures, the final product use a variety of textures.
	-barely and animations are implemented yet, and those are just placeholders
-the ending
	-will contain gameplay feature that differ from the rest of the other levels
-sound
	-lots of things will make sounds



Controls(user):
-A:
	move left
-D:
	move right
-P:
	saves a screenshot to the screenshots folder
-space:
	jump if on the ground
-mouse:
	damage blocks the mouse curser colides with 

Controls(developer):
-left:
	tilt screen left
-right:
	tilt screen right
-H:
	display all hitboxes accross the entire map

Launch the game by running "run.py"