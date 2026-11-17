import pygame
from pathlib import Path

WIDTH, HEIGHT = 900, 600
GAME_TITLE = "The Morning After"
BACKGROUND = (24, 30, 42)
PANEL_COLOR = (39, 49, 65)
TEXT_COLOR = (235, 235, 240)
MUTED_COLOR = (185, 195, 205)
ACCENT_COLOR = (244, 197, 102)
FONT_FILE = None
TITLE_SIZE = 38
TEXT_SIZE = 22

pygame.init()

try:
    pygame.mixer.init()
except pygame.error:
    pass

def load_sound(filename):
    try:
        return pygame.mixer.Sound(str(Path(__file__).parent / filename))
    except (pygame.error, FileNotFoundError):
        return None

collect_sound = load_sound("sound.wav")
wake_sound = load_sound("head ringing-2.wav")
thateus_sound = load_sound("womp womp womp sound-2.wav")



class Treasure:
    def __init__(self, name, points, description):
        self.name = name
        self.points = points
        self.description = description
        self.found = False


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.neighbors = {}
        self.treasure = None

    def add_neighbor(self, direction, room):
        self.neighbors[direction] = room


class Game:
    def __init__(self):
        quad = Room(
            "Quad",
            "You are Jack, a Sewanee freshman. You wake up on the Quad, "
            "the open field in the center of campus. You blacked out the "
            "night before and are extremely hungover. Your phone, wallet, "
            "and keys are gone. You must find them.\n\n"
            "You wake to the sound of bells, expecting to find your dorm "
            "ceiling above you. Instead, you see a gray sky and branches "
            "moving in the wind. Your jacket is damp, your head aches, "
            "and grass clings to your sleeves.\n\n"
            "You sit up slowly. A few students cross the Quad carrying "
            "backpacks, and one gives you a concerned look as they walk "
            "to class. The last thing you remember is music coming from Ayres.\n\n"
            "Near the path, Thateus stops and looks down at you. He is a "
            "guy from your high school whom you never really trusted.\n\n"
            "'Looking for your stuff? I heard someone took it off campus,' "
            "he says. Before you can ask who, he points toward the road.\n\n"
            "Across the Quad, you spot Cole standing outside Ayres. You "
            "must decide whether to follow Thateus or retrace your steps."
        )

        ayres = Room(
            "Ayres",
            "The steps outside Ayres are scattered with wet leaves. "
            "Cole stands outside, leaning against the railing with a cup "
            "of coffee.\n\n"
            "'Jack, we were wondering where you went,' he says.\n\n"
            "You ask if someone stole your belongings. Cole shakes his head.\n\n"
            "'You kept taking things out of your pockets. You definitely "
            "dropped something right here when we came outside. Check "
            "beside the steps.'\n\n"
            "You remember standing in a crowded room with music playing, "
            "laughing with your friends, taking shots, and doing sidewalk "
            "slammers. Then comes a flash of cold air, someone laughing, "
            "and your hand fumbling with your key. You cannot remember "
            "what happened next.\n\n"
            "Cole notices you shivering and offers you some water.\n\n"
            "'Brad went toward All Saints with you. He might remember more.'\n\n"
            "A small piece of metal catches the light beneath a curled leaf."
        )

        all_saints = Room(
            "All Saints",
            "The chapel doors are closed, and the stone path is quiet.\n\n"
            "Brad sits near a bench but stands when he notices you.\n\n"
            "'You look better than you did last night,' he says.\n\n"
            "You tell him about your empty pockets. His expression softens.\n\n"
            "You remember sitting down and emptying your pockets. You "
            "remember falling over and throwing up. Your wallet slid off "
            "your knee, but you were distracted by feeling sick.\n\n"
            "Brad tells you he stayed with you until Cole came back with water.\n\n"
            "'We wanted to take you back to your dorm, but you said you "
            "needed food. We headed toward Clurg. Try looking under the "
            "bench first.'\n\n"
            "You crouch beside it. Something dark is wedged behind one "
            "of the legs."
        )

        clurg = Room(
            "Clurg",
            "The smell of toast makes you realize how hungry you actually are. "
            "Trays clatter, chairs scrape, and students talk over breakfast.\n\n"
            "TJ, an interesting fellow, waves you down from a table.\n\n"
            "'Please tell me you're here for this,' he says, holding up your phone.\n\n"
            "'I found it outside after you left. I tried to catch you, but "
            "you had already gone across the Quad.'\n\n"
            "The screen has a muddy streak across it, but it still turns on. "
            "Several missed calls from Cole and Brad appear on the lock screen.\n\n"
            "TJ slides a glass of water to you while you unlock it.\n\n"
            "'You were convinced somebody had your wallet. Check your photos.'\n\n"
            "You kept taking pictures so you could remember where you had "
            "been. For the first time that morning, you have a way to check "
            "your memories."
        )

        dupont = Room(
            "DuPont Library",
            "You climb the library steps and pause beneath the entrance "
            "canopy. The quiet inside feels strange after the noise of "
            "breakfast at Clurg.\n\n"
            "A student named Gigi looks up from a notebook near the windows.\n\n"
            "'Jack, did you find everything?' she asks.\n\n"
            "You stop. 'How do you know I lost something?'\n\n"
            "'I saw you outside last night. You were checking the benches "
            "and asking whether anyone had turned in a wallet.'\n\n"
            "You remember standing beneath this same canopy, trying to read "
            "a sign on the locked doors. You had hoped someone could help.\n\n"
            "Gigi closes her notebook. 'Cole came looking for you a few "
            "minutes later. I told him you had walked back to the Quad.'\n\n"
            "You mention Thateus and his story about a car off campus.\n\n"
            "Gigi frowns. 'He asked me about a missing bag, not a wallet.'\n\n"
            "The conversation ends, and you leave Gigi in the library."
        )

        benny = Room(
            "Benedict Hall",
            "The front steps of Benedict Hall are still wet from the "
            "morning fog. You can smell coffee through an open window "
            "upstairs. You reach for your dorm key out of habit and pull "
            "a crumpled napkin from your pocket.\n\n"
            "Michael is sitting by the entrance, staring at you as he ties "
            "his shoes. He looks up.\n\n"
            "'There you are. You were on the Quad last night patting every "
            "pocket you had. I asked what you lost, and you said your key.'\n\n"
            "You ask if he remembers where you came from. 'Ayres,' he says. "
            "'You told me you sat on the steps to fix your shoe.'\n\n"
            "You look down and notice one of your laces is still knotted "
            "twice. For a second, you remember the cold stone under your "
            "hands. The steps at Ayres seem like a good place to start."
        )

        assembly = Room(
            "The Assembly",
            "At the Assembly, the houses sit farther apart and the road "
            "goes quiet.\n\n"
            "Evy is on a front porch shaking leaves out of a doormat. When "
            "you ask if she saw you last night, she leans the mat against "
            "the railing.\n\n"
            "'I saw you sitting on the bench outside All Saints. I tried "
            "to help you when you went to sleep. After you got up, Brad "
            "went back and crouched down to look underneath. I couldn't "
            "see what he was looking for, but you should ask him.'\n\n"
            "Then Evy remembers something else. 'TJ told me this morning "
            "that he had your phone at Clurg. He said he was going to call "
            "you to tell you, and then he realized how stupid that sounded.'\n\n"
            "For the first time all morning, you laugh. Now you've got two "
            "places to check: the bench at All Saints and TJ's table at Clurg."
        )

        lake_cheston = Room(
            "Lake Cheston",
            "At Lake Cheston, a fishing bobber drifts past the reeds. You "
            "hear someone say, 'Oh, come on,' and find Sawyer behind a tree, "
            "pulling dirt and worms out of his clothes. He sees you looking.\n\n"
            "'JJ said the bank was dry. I took one step and slid right into "
            "the dirt where we dug up the bait.'\n\n"
            "You ask Sawyer if he knows Thateus. Sawyer stops brushing "
            "himself off.\n\n"
            "'Yeah. He asked me and JJ this morning if we'd seen your stuff. "
            "We hadn't. Then he asked us where he should tell you to look.'\n\n"
            "You tell Sawyer that Thateus sent you off campus. Sawyer "
            "snorts. 'He didn't even know what you lost until JJ told him.'\n\n"
            "As you turn to leave, Sawyer pulls out one last worm. 'If you "
            "see JJ, tell him I found his bait.'"
        )

        # Campus connections
        quad.add_neighbor("north", ayres)
        quad.add_neighbor("east", all_saints)
        quad.add_neighbor("south", clurg)
        quad.add_neighbor("west", benny)

        ayres.add_neighbor("south", quad)
        ayres.add_neighbor("north", assembly)

        all_saints.add_neighbor("west", quad)
        all_saints.add_neighbor("north", dupont)

        clurg.add_neighbor("north", quad)
        clurg.add_neighbor("south", lake_cheston)

        benny.add_neighbor("east", quad)
        assembly.add_neighbor("south", ayres)
        dupont.add_neighbor("south", all_saints)
        lake_cheston.add_neighbor("north", clurg)

        ayres.treasure = Treasure(
            "key", 10,
            "Your dorm key, lying beside the steps.\n\n"
            "You wipe the dirt off it and recognize the chipped blue key ring. "
            "You remember pulling it out to show Cole which room was yours. "
            "When someone opened the door behind you, you stepped aside and "
            "dropped it without noticing. You carefully put it in your pocket."
        )

        all_saints.treasure = Treasure(
            "wallet", 10,
            "Your wallet, tucked beneath the bench behind the wooden leg.\n\n"
            "You open it and find your student ID, cards, and cash still inside. "
            "A folded receipt falls out. You remember searching for your wallet "
            "and looking for something with your room number on it.\n\n"
            "Nobody took it. It slipped down while you were distracted. "
            "Brad smiles when you hold it up. 'That's two things accounted for.'"
        )

        clurg.treasure = Treasure(
            "phone", 10,
            "TJ returns your phone. You scroll through last night's photos.\n\n"
            "The first shows Cole at Ayres. The next is a blurry picture of "
            "the bench outside All Saints, with your wallet on your knee. "
            "Another shows Brad pointing toward the dining hall.\n\n"
            "The final picture shows the Quad, tilted sideways, with your "
            "friends approaching in the distance.\n\n"
            "The messages tell the rest: they searched for you after you "
            "walked off. Nobody robbed you. You left your belongings along "
            "the route, and your friends had been trying to help you find them."
        )

        self.current_room = quad
        self.score = 0
        self.game_over = False

        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(FONT_FILE, TITLE_SIZE)
        self.text_font = pygame.font.Font(FONT_FILE, TEXT_SIZE)
        self.small_font = pygame.font.Font(FONT_FILE, 17)
        self.history = []
        self.command_text = ""
        self.scroll = 0
        self.running = True

    def say(self, message):
        self.history.append(message)
        self.history.append("")
        self.scroll = 0

    def announce_room(self):
        self.say(self.current_room.name)
        self.say(self.current_room.description)

    def look(self):
        self.announce_room()
        if self.current_room.treasure is not None:
            if not self.current_room.treasure.found:
                self.say("You see something here: " + self.current_room.treasure.name)

    def go(self, direction):
        if direction in self.current_room.neighbors:
            self.current_room = self.current_room.neighbors[direction]
            self.announce_room()
        else:
            self.say("You cannot go that way.")

    def take(self, item):
        if self.current_room.treasure is not None:
            treasure = self.current_room.treasure
            if treasure.name == item and not treasure.found:
                treasure.found = True
                self.score += treasure.points
                if collect_sound is not None:
                    collect_sound.play()
                self.say("You found your " + item + "!")
                self.say(treasure.description)
            else:
                self.say("You cannot take that here.")
        else:
            self.say("There is nothing to take here.")

    def check_ending(self):
        if self.score >= 30 and not self.game_over:
            self.say(
                "With your key, wallet, and phone recovered, you sit down "
                "in Clurg and finally eat breakfast. The morning is less "
                "overwhelming now that you have found everything.\n\n"
                "You scroll through last night's photos and call Cole and "
                "Brad to thank them for their help.\n\n"
                "'Next time, let us get you home,' Brad says."
            )
            self.say(
                "You remember everything: the party at Ayres, sleeping "
                "outside All Saints, and dropping your belongings along the way."
            )
            self.say(
                "Cole and Brad were helping you. TJ saved your phone. "
                "Thateus had sent you in the wrong direction."
            )
            self.say(
                "You head back to your dorm, exhausted but relieved. "
                "Next time, you're keeping your pockets zipped."
            )
            self.say("THE END - Everything Found")
            self.game_over = True

    def thateus_ending(self):
        self.say(
            "You trust Thateus and walk off campus. He says somebody "
            "mentioned seeing your belongings near a parked car, but "
            "he cannot remember whose car it was.\n\n"
            "You pass the last campus buildings and search the roadside. "
            "Every dark shape turns out to be a leaf or a shadow.\n\n"
            "After an hour of searching, you find nothing. At the fork "
            "in the road, Thateus stops.\n\n"
            "'I think it was farther down,' Thateus says. 'I've got class. "
            "You'll probably find it.'\n\n"
            "You ask who told him, but he only shrugs before leaving. "
            "You keep searching until you realize you've been gone "
            "for over an hour."
        )
        self.say(
            "You return to the Quad, hungry, tired, and angry. Your friends "
            "have left. Thateus is gone too.\n\n"
            "Cole is no longer outside Ayres. The bench near All Saints "
            "is empty, and the breakfast crowd has gone.\n\n"
            "Without your phone, you cannot contact anyone who was there. "
            "You sit on the same patch of grass where you woke up."
        )
        self.say(
            "With your belongings still missing, you head back to your dorm. "
            "Last night remains a mystery.\n\n"
            "You wish you had asked Cole what he actually remembered "
            "before following a rumor off campus."
        )
        self.say("THE END - Wrong Direction")
        self.game_over = True

    def draw(self):
        self.screen.fill(BACKGROUND)
        title = self.title_font.render(GAME_TITLE, True, ACCENT_COLOR)
        self.screen.blit(title, (30, 18))

        room_text = self.small_font.render(
            "Location: " + self.current_room.name +
            "     Items found: " + str(self.score // 10) + "/3",
            True, MUTED_COLOR
        )
        self.screen.blit(room_text, (32, 72))

        pygame.draw.rect(self.screen, PANEL_COLOR, (25, 105, 850, 390), border_radius=12)
        pygame.draw.rect(self.screen, MUTED_COLOR, (25, 105, 850, 390), 1, border_radius=12)

        visible_lines = []
        for message in self.history:
            if message == "":
                visible_lines.append("")
            else:
                words = message.split()
                line = ""
                for word in words:
                    test_line = line + word + " "
                    if self.text_font.size(test_line)[0] < 800:
                        line = test_line
                    else:
                        visible_lines.append(line.rstrip())
                        line = word + " "
                if line:
                    visible_lines.append(line.rstrip())

        line_height = self.text_font.get_linesize()
        max_lines = 390 // line_height - 1
        start = max(0, len(visible_lines) - max_lines - self.scroll)
        shown_lines = visible_lines[start:start + max_lines]
        y = 120
        for line in shown_lines:
            color = ACCENT_COLOR if line.startswith("THE END") else TEXT_COLOR
            self.screen.blit(self.text_font.render(line, True, color), (42, y))
            y += line_height

        pygame.draw.rect(self.screen, PANEL_COLOR, (25, 510, 850, 55), border_radius=10)
        pygame.draw.rect(self.screen, ACCENT_COLOR, (25, 510, 850, 55), 2, border_radius=10)
        prompt = self.small_font.render("> " + self.command_text, True, TEXT_COLOR)
        self.screen.blit(prompt, (42, 526))

        hint = self.small_font.render(
            "Enter a command  |  look, go north, take key, help",
            True, MUTED_COLOR
        )
        self.screen.blit(hint, (30, 574))
        pygame.display.flip()

    def handle_command(self, command):
        command = command.lower().strip()
        if not command:
            return

        self.say("> " + command)

        if command == "look":
            self.look()
        elif command.startswith("go "):
            direction = command[3:]
            if direction in ["north", "south", "east", "west"]:
                self.go(direction)
            else:
                self.say("Choose north, south, east, or west.")
        elif command in ["take key", "take wallet", "take phone"]:
            self.take(command[5:])
        
        elif command == "talk to thateus":
            if thateus_sound is not None:
                thateus_sound.play()
            self.say("Thateus tells Jack to follow him.")

        elif command == "trust thateus":
            if thateus_sound is not None:
                thateus_sound.play()
            self.thateus_ending()

        elif command == "help":
            self.say(
                "Commands: look, go north, go south, go east, go west, "
                "take key, take wallet, take phone, trust thateus. "
                "You can explore Benedict Hall, the Assembly, DuPont Library, "
                "and Lake Cheston too."
            )
        else:
            self.say("I do not understand that command. Type help to see commands.")

        self.check_ending()

    def play(self):

        if wake_sound is not None:
            wake_sound.play()
        self.say("THE MORNING AFTER")
        self.say(
            "Find your belongings and piece together last night.\n\n"
            "A passing student, Thateus, says, 'Your stuff is off campus.'\n\n"
            "Then you spot Cole outside Ayres. Who should you trust?\n\n"
            "Thateus points off campus, but Cole is waiting outside Ayres. "
            "Whose advice will you follow?"
        )
        self.say("Try: look, go north, take key")
        self.announce_room()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.handle_command(self.command_text)
                        self.command_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.command_text = self.command_text[:-1]
                    elif event.key == pygame.K_UP:
                        self.scroll = min(self.scroll + 3, max(0, len(self.history)))
                    elif event.key == pygame.K_DOWN:
                        self.scroll = max(0, self.scroll - 3)
                    elif event.unicode and event.unicode.isprintable():
                        if len(self.command_text) < 90:
                            self.command_text += event.unicode
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll = max(0, min(self.scroll + event.y * 3, len(self.history)))

            self.draw()
            self.clock.tick(30)

        pygame.quit()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
