"""
Program Name: Mad Libs Game
Author: Exonymos (https://github.com/exonymos)
Description: A friendly, colorful console-based Mad Libs Game.
"""

import random
import re
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track

# Initialize the console for rich text output.
console = Console()

# Color themes for the game.
THEMES = {
    "default": {
        "title": "bold magenta",
        "menu": "bold cyan",
        "input": "green",
        "error": "red",
        "info": "yellow",
        "story": "bold white",
    },
    "dark": {
        "title": "bold bright_blue",
        "menu": "bold bright_magenta",
        "input": "bright_green",
        "error": "bright_red",
        "info": "bright_yellow",
        "story": "bold bright_white",
    },
    "light": {
        "title": "bold blue",
        "menu": "bold black",
        "input": "dark_green",
        "error": "red",
        "info": "gold1",
        "story": "bold black",
    },
}


def clear_screen():
    console.clear()


class Story:
    """A story template with placeholders for dynamic words."""

    def __init__(self, title, template):
        self.title = title
        self.template = template
        # Combine placeholders from both title and content.
        combined_text = title + " " + template
        self.placeholders = list(dict.fromkeys(re.findall(r"\{(.*?)\}", combined_text)))

    def fill(self, words):
        """Fill in the story template and title with the provided words."""
        try:
            filled_title = self.title.format(**words)
        except KeyError as e:
            console.print(f"[red]Error in title: Missing input for '{e.args[0]}'[/red]")
            filled_title = self.title
        try:
            filled_story = self.template.format(**words)
        except KeyError as e:
            console.print(f"[red]Error in story: Missing input for '{e.args[0]}'[/red]")
            filled_story = self.template
        return filled_title, filled_story


class MadLibsGame:
    """Main class for Mad Libs Game."""

    def __init__(self):
        self.theme = THEMES["default"]
        self.stories = self.load_stories()
        self.history = []  # Keep the last 10 completed stories

    def load_stories(self):
        """Story templates with placeholders."""
        return [
            Story(
                "A Day at the {place}",
                "Today I went to the {place} and saw a {adjective} {noun} {verb} near the pond.",
                # Example 1: Today I went to the park and saw a happy dog run near the pond.
            ),
            Story(
                "My Crazy Adventure",
                "Yesterday, I decided to {verb} to the {noun} in a {adjective} manner, which surprised everyone at the {place}.",
                # Example 2: Yesterday, I decided to swim to the mountain in a funny manner, which surprised everyone at the beach.
            ),
            Story(
                "The Mystery of the {noun}",
                "In a {adjective} town, a {noun} was known to {verb} mysteriously at the {place}.",
                # Example 3: In a bright town, a tree was known to dance mysteriously at the park.
            ),
            Story(
                "The Quest for the {adjective} {noun}",
                "I embarked on a journey to the {place} to {verb} the legendary {adjective} {noun}.",
                # Example 4: I embarked on a journey to the forest to explore the legendary bright mountain.
            ),
            Story(
                "Unexpected Encounter",
                "While strolling through the {place}, I unexpectedly saw a {adjective} {noun} {verb} swiftly.",
                # Example 5: While strolling through the village, I unexpectedly saw a happy cat jump swiftly.
            ),
            Story(
                "The Secret of the {adjective} {noun}",
                "Deep in the heart of the {place}, I discovered a {adjective} {noun} that could {verb} like no other.",
                # Example 6: Deep in the heart of the forest, I discovered a mysterious river that could swim like no other.
            ),
            Story(
                "A {adjective} Day",
                "It was a {adjective} day when I found a {noun} {verb} at the {place}.",
                # Example 7: It was a happy day when I found a car run at the park.
            ),
            Story(
                "The {adjective} {noun}",
                "Once upon a time, there was a {adjective} {noun} that could {verb} like no other.",
                # Example 8: Once upon a time, there was a funny dog that could jump like no other.
            ),
            Story(
                "The {adjective} {noun} of {place}",
                "In the land of {place}, there was a {adjective} {noun} that could {verb} like no other.",
                # Example 9: In the land of mountains, there was a bright tree that could dance like no other.
            ),
            Story(
                "The {adjective} {noun} {verb}",
                "The {adjective} {noun} {verb} at the {place} was a sight to behold.",
                # Example 10: The happy dog run at the park was a sight to behold.
            ),
            Story(
                "The {adjective} Adventure at the {place}",
                "One {adjective} day, a group of {noun}s decided to {verb} at the {place}, leading to an unforgettable adventure.",
                # Example: One sunny day, a group of friends decided to explore at the beach, leading to an unforgettable adventure.
            ),
        ]

    def welcome_animation(self):
        """Welcome animation"""
        clear_screen()
        console.print(
            Panel(
                "Welcome to Mad Libs Game!",
                title="Mad Libs",
                style=self.theme["title"],
            )
        )
        for _ in track(range(10), description="Loading...", style=self.theme["info"]):
            time.sleep(0.1)

    def show_main_menu(self):
        """Display the main menu and handle user selection."""
        while True:
            clear_screen()
            console.print(Panel("MAD LIBS GAME", style=self.theme["title"]))
            console.print(f"[{self.theme['menu']}]1.[/] Start Game")
            console.print(f"[{self.theme['menu']}]2.[/] Instructions")
            console.print(f"[{self.theme['menu']}]3.[/] About")
            console.print(f"[{self.theme['menu']}]4.[/] Change Theme")
            console.print(f"[{self.theme['menu']}]5.[/] Exit")
            choice = Prompt.ask(f"[{self.theme['input']}]Enter your choice (1-5)[/]")
            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.show_instructions()
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                self.change_theme()
            elif choice == "5":
                self.exit_game()
            else:
                console.print(
                    f"[{self.theme['error']}]Invalid choice. Please select 1-5.[/]"
                )
                time.sleep(1)

    def show_instructions(self):
        """Display the game instructions."""
        clear_screen()
        instructions = (
            "How to Play:\n"
            "- Choose 'Start Game' to create a new Mad Libs story.\n"
            "- When prompted, enter words to fill in the placeholders.\n\n"
            "Available Commands (at any prompt):\n"
            "  'random'  : Auto-fill all remaining blanks with random words\n"
            "  'history' : Show the last 10 stories you created\n"
            "  'restart' : Return to the main menu immediately\n\n"
            "Example:\n"
            "  Template: 'I saw a {adjective} {noun} {verb} at the {place}.'\n"
            "  Inputs : happy, dog, run, park\n"
            "  Story  : 'I saw a happy dog run at the park.'\n"
            "  (If the title is 'The Mystery of {noun}', it becomes, for example, 'The Mystery of dog')"
        )
        console.print(
            Panel(instructions, title="Instructions", style=self.theme["info"])
        )
        Prompt.ask("Press Enter to return to the main menu")

    def show_about(self):
        """Display information about the game."""
        clear_screen()
        about_text = (
            "Mad Libs Game is a fun console game that creates hilarious stories from your input.\n"
            "Story titles can include dynamic words (e.g. 'The Mystery of {noun}').\n\n"
            "Author: Exonymos (https://github.com/exonymos)\n"
            "Enjoy and let your creativity shine!"
        )
        console.print(Panel(about_text, title="About", style=self.theme["info"]))
        Prompt.ask("Press Enter to return to the main menu")

    def change_theme(self):
        """Change the color theme for the game."""
        clear_screen()
        console.print(Panel("Available Themes", style=self.theme["title"]))
        for key in THEMES.keys():
            console.print(f"- {key}")
        new_theme = (
            Prompt.ask(f"[{self.theme['input']}]Enter theme name[/]").strip().lower()
        )
        if new_theme in THEMES:
            self.theme = THEMES[new_theme]
            console.print(
                f"[{self.theme['info']}]Theme changed to '{new_theme}' successfully.[/]"
            )
        else:
            console.print(
                f"[{self.theme['error']}]Theme '{new_theme}' not found. Using current theme.[/]"
            )
        time.sleep(1)

    def exit_game(self):
        """Exit the game after showing a goodbye message."""
        clear_screen()
        console.print(
            Panel(
                "Thank you for playing Mad Libs Game!\nGoodbye!",
                title="Goodbye",
                style=self.theme["info"],
            )
        )
        sys.exit(0)

    def start_game(self):
        """Handle the flow for creating a new story."""
        while True:
            clear_screen()
            # Select a random story template.
            story = random.choice(self.stories)
            console.print(Panel("Let's create a new story!", style=self.theme["title"]))
            console.print("At each prompt, enter a word or use commands:")
            console.print(
                f"[{self.theme['info']}] random  : Auto-fill all remaining blanks"
            )
            console.print(f"[{self.theme['info']}] history : Show the last 10 stories")
            console.print(f"[{self.theme['info']}] restart : Return to the main menu\n")

            words = {}
            # Loop through all placeholders from both title and content.
            for placeholder in story.placeholders:
                while True:
                    user_input = (
                        Prompt.ask(f"Enter a {placeholder}", default="").strip().lower()
                    )
                    if user_input == "restart":
                        return
                    elif user_input == "history":
                        self.show_history()
                        continue
                    elif user_input == "random":
                        # Fill all missing placeholders with random words.
                        for ph in story.placeholders:
                            if ph not in words:
                                words[ph] = self.get_random_word(ph)
                        break
                    elif not user_input:
                        console.print(
                            f"[{self.theme['error']}]Input cannot be empty. Please try again.[/]"
                        )
                        continue
                    else:
                        words[placeholder] = user_input
                        break
                # If random was used, break out of the loop.
                if "random" in words.values():
                    break

            # Fill both title and content.
            filled_title, filled_story = story.fill(words)
            # Store the complete story.
            combined_story = f"{filled_story}\n\n— {filled_title}"
            self.history.append(combined_story)
            if len(self.history) > 10:
                self.history.pop(0)

            clear_screen()
            console.print(
                Panel(combined_story, title="Your Story", style=self.theme["story"])
            )
            next_action = (
                Prompt.ask(
                    "Press Enter to play again or type 'restart' to return to the main menu",
                    default="",
                )
                .strip()
                .lower()
            )
            if next_action == "restart":
                return

    def show_history(self):
        """Display the last 10 completed stories."""
        clear_screen()
        if not self.history:
            console.print(f"[{self.theme['error']}]No stories in history yet.[/]")
        else:
            history_text = "\n" + "-" * 40 + "\n"
            history_text = history_text.join(self.history)
            console.print(
                Panel(history_text, title="Story History", style=self.theme["info"])
            )
        Prompt.ask("Press Enter to continue")

    def get_random_word(self, word_type):
        """Return a random word based on the given type."""
        random_words = {
            "noun": ["dog", "cat", "car", "tree", "mountain", "river"],
            "verb": ["run", "jump", "swim", "dance", "fly", "explore"],
            "adjective": [
                "happy",
                "sad",
                "funny",
                "bright",
                "mysterious",
                "enchanting",
            ],
            "adverb": ["quickly", "silently", "gracefully", "happily"],
            "place": ["park", "beach", "mall", "forest", "museum", "village"],
        }
        return random.choice(random_words.get(word_type, ["amazing"]))


def main():
    game = MadLibsGame()
    game.welcome_animation()
    game.show_main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Game interrupted. Goodbye![/red]")
