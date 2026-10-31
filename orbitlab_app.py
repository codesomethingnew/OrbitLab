"""OrbitLab — a free, very basic introduction to Python and astronomy."""

from pathlib import Path
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
BG = "#F4F7FB"
WHITE = "#FFFFFF"
NAVY = "#12233F"
BLUE = "#2463EB"
MUTED = "#465770"
BORDER = "#DFE7F1"
FONT = "Segoe UI"

SEQUENCE = [
    f"Data/demo_sequence/ah-demo-{n}.fits"
    for n in range(1, 5)
]

# Data files that are not included with OrbitLab.
# simulate_motion.py is not listed because it makes its own pictures.
DATA_NEEDED = {
    "view_fits.py": ["Data/horsehead/HorseHead.fits"],
    "explore_sequence.py": SEQUENCE,
    "find_candidate_changes.py": SEQUENCE,
    "compare_two_images.py": SEQUENCE[:2],
    "filter_noise.py": SEQUENCE[:2],
}

ACTIVITIES = {
    "Explore": [
        (
            "View an astronomical image",
            "Open an astronomical image (a FITS file) of the Horsehead Nebula, "
            "a dark cloud of dust and gas in space. "
            "You will see a grey-scale picture. Brighter areas mean more light. "
            "This activity needs an image file that is not included.",
            "view_fits.py",
        ),
        (
            "Explore an image sequence",
            "See four pictures of the same patch of sky, taken one after another. "
            "The window also prints what each file says about itself. "
            "This is a demonstration sequence. It needs files that are not included.",
            "explore_sequence.py",
        ),
    ],
    "Detect": [
        (
            "Find candidate changes",
            "Red circles mark spots that look brighter than in the first picture. "
            "These are only candidates. They could be noise or errors, "
            "and they are not confirmed asteroids. "
            "This activity needs the demonstration sequence files.",
            "find_candidate_changes.py",
        ),
    ],
    "Experiment": [
        (
            "Compare two images",
            "Subtract one picture from another. Red and blue in the "
            "third picture show where the brightness went up or down. "
            "This activity needs the demonstration sequence files.",
            "compare_two_images.py",
        ),
        (
            "Filter image noise",
            "Hide small random speckles (noise) so only the stronger changes "
            "stay visible. White spots show the changes that remain. "
            "This activity needs the demonstration sequence files.",
            "filter_noise.py",
        ),
        (
            "Simulate movement",
            "Make three pictures of an artificial star field with one dot "
            "that moves a little each time. This is a simulation. "
            "It works without any extra files.",
            "simulate_motion.py",
        ),
    ],
}

LESSONS = [
    (
        "1. What to install",
        """This lesson helps you set up OrbitLab on Windows.
Go slowly. Do one step at a time.

Python is the language we will learn.
Visual Studio Code (VS Code) is a free program for writing and running code.

PART 1. INSTALL PYTHON

OrbitLab was tested with Python 3.14 on Windows. A newer version of
Python may be offered first on the Python website. To match the tested
version, use the Python 3.14 page below.

The Python website changes from time to time. Button names may look
different from the ones here. That is normal.

1. Open your web browser.
2. Go to this page (Python 3.14.10):
   https://www.python.org/downloads/release/python-31410/
3. Scroll down to the list called Files.
4. Find the row called "Windows installer (64-bit)". It is marked
   "Recommended". Click it to download the file.
   Most Windows computers need this one. Do not choose the 32-bit or
   ARM64 files unless you know your computer needs them.
5. Open the file you downloaded.
6. On the first screen of the installer, tick the box about adding
   Python to PATH. It may say "Add python.exe to PATH". PATH is the
   list of places where Windows looks for programs. This box lets you
   type python in a terminal.
7. Follow the instructions on the screen. Keep the other default
   choices.
8. When the installer says it has finished, close it.
9. Close VS Code and any terminal windows that are open.

To check, open a new terminal (see Part 5) and type this:

    python --version

If you see Python 3.14 and some numbers, such as Python 3.14.10,
Python is ready. If you see a different version, OrbitLab may still
work, but it has not been tested (see the README).

PART 2. INSTALL VISUAL STUDIO CODE

1. Go to code.visualstudio.com
2. Click Download for Windows.
3. Open the file you downloaded.
4. Click Next and accept the licence. Keep the default choices.
5. Click Install, then Finish.

PART 3. ADD THE PYTHON EXTENSION

An extension adds a new skill to VS Code.

1. Open VS Code.
2. On the left, click the Extensions icon. It looks like four squares.
3. Type Python in the search box.
4. Find the one made by Microsoft.
5. Click Install.

PART 4. OPEN THE ORBITLAB FOLDER

1. In VS Code, click File, then Open Folder.
2. Find the OrbitLab folder. It contains orbitlab_app.py.
3. Click it once, then click Select Folder.
4. If VS Code asks "Do you trust the authors?", click Yes if you got
   the folder from a source you trust.

PART 5. OPEN THE TERMINAL

The terminal is a window where you type commands.

1. In VS Code, click Terminal at the top.
2. Click New Terminal.
3. A panel opens at the bottom. Type each command there.
4. Press Enter after each command.

PART 6. CREATE A VIRTUAL ENVIRONMENT

A virtual environment is a private box of tools for one project.
It keeps this project separate from your other projects.

1. Create it. This is done only once:

    python -m venv .venv

2. Switch it on. This is called activating:

    .\\.venv\\Scripts\\Activate.ps1

3. Look at the start of the line. You should see (.venv). That means
   it is working.

If Windows says scripts are blocked, type this, press Enter, and then
repeat step 2:

    Set-ExecutionPolicy -Scope Process RemoteSigned

This only changes the setting for this one terminal window. It goes
back to normal when you close the window. It does not change your
computer permanently.

If it still does not work, you can skip activation. Then use the long
commands below instead of the short ones in Parts 7 and 8. Type each
one exactly as shown.

To install the libraries (instead of Part 7, step 1):

    .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

To check the libraries (instead of Part 7, step 3):

    .\\.venv\\Scripts\\python.exe -c "import numpy, matplotlib, cv2, astropy; print('Ready!')"

To start OrbitLab (instead of Part 8, step 1):

    .\\.venv\\Scripts\\python.exe orbitlab_app.py

PART 7. INSTALL THE LIBRARIES

A library is a box of ready-made code that other people wrote for us.
The tool pip installs libraries. The file requirements.txt lists the
libraries OrbitLab needs.

1. Type this and press Enter:

    python -m pip install -r requirements.txt

2. Wait. It may take a few minutes.
3. To check, type this:

    python -c "import numpy, matplotlib, cv2, astropy; print('Ready!')"

4. If you see Ready!, everything is installed.

PART 8. START ORBITLAB

1. Type this and press Enter:

    python orbitlab_app.py

2. The OrbitLab window opens. Well done!
3. Next time, open the folder and the terminal, activate the
   environment (Part 6, step 2), and start OrbitLab.

IF SOMETHING GOES WRONG

"python is not recognized" or "Python was not found":
1. Python may not be installed, or Windows may not know where it is.
2. Run the Python installer again. Choose the option to repair or
   modify, and tick the PATH choice if you see one.
3. Close VS Code, open it again, and open a New Terminal.
4. Type python --version to check.

"No module named numpy" (or cv2, matplotlib, astropy):
1. A library is missing, or the environment is not switched on.
2. Check that you see (.venv) at the start of the line.
3. If not, repeat Part 6, step 2.
4. Then repeat Part 7, step 1.

"No module named tkinter":
Tkinter is the library OrbitLab uses to draw its window, buttons and
menus. It normally comes with Python.
1. Test it. Type this and press Enter:

    python -m tkinter

2. If it works, a small window opens. It shows the Tcl/Tk version
   number and two buttons. Close that window. Tkinter is fine.
3. If you see "No module named tkinter" instead, run the Python
   installer again and choose Modify. Make sure the item about
   tcl/tk is ticked, then finish. Keep all other choices as they are.
4. Open a New Terminal and test again.

Git and a GitHub account are optional. You only need them if you want
to save versions of your work or share it online (see Lesson 9).

Try it: In your own words, why is a separate box of tools for each
project useful?""",
    ),
    (
        "2. Python basics",
        """Python is a programming language. A program is a list of instructions
that a computer follows, one line at a time.

To try an example:

1. In VS Code, click File, then New File, and choose Python File.
2. Type or copy the example into the file.
3. Click File, then Save. Give it a name that ends in .py, such as test.py.
4. Click the Run button (a small triangle at the top right).

The result appears in the terminal at the bottom.

The word print tells Python to show something on the screen.

VARIABLES

A variable is a named box that holds a value:

    telescope = "My telescope"
    observations = 4

    print(telescope)
    print(observations)

This prints:

    My telescope
    4

DATA TYPES

A string stores text. Text goes inside quotation marks:

    name = "OrbitLab"

An integer stores a whole number:

    images = 4

A float stores a decimal number:

    brightness = 12.5

A Boolean stores True or False:

    detected = False

Try it: Change the values, then use print to show them.""",
    ),
    (
        "3. Conditions and loops",
        """INDENTATION

In Python, the spaces at the start of a line matter. Lines that belong
together are pushed in by four spaces. In the examples below, the pushed-in
lines are the ones that belong to the line above them.

CONDITIONS: if AND else

An if statement asks a question. If the answer is yes (True), Python runs
the pushed-in lines under if. If the answer is no, Python runs the lines under
else.

    brightness = 42

    if brightness > 30:
        print("Bright pixel")
    else:
        print("Dim pixel")

This prints:

    Bright pixel

Why? Because 42 is bigger than 30, so the question "brightness > 30" is
True. If you change brightness to 10, it prints Dim pixel instead.

LOOPS: for AND range()

A loop repeats instructions. The function range(1, 5) gives the numbers
1, 2, 3 and 4. It starts at the first number and stops BEFORE the last one.

    for number in range(1, 5):
        print("Observation", number)

This prints:

    Observation 1
    Observation 2
    Observation 3
    Observation 4

Why? The loop runs once for each number. Each time, number holds the next
value, and print shows it.

WHILE LOOPS

A while loop keeps repeating as long as its question is True.

    count = 1

    while count <= 3:
        print(count)
        count += 1

This prints:

    1
    2
    3

Why? The line count += 1 means "add 1 to count". The first time, count
is 1, so Python prints 1 and then adds 1, making count 2. This repeats.
When count becomes 4, the question "count <= 3" is False, so the loop stops.
If you forget count += 1, the loop never stops. Press Ctrl+C to stop it.

Try it: Change range(1, 5) to range(1, 7) to print six observations.""",
    ),
    (
        "4. Functions and errors",
        """FUNCTIONS

A function groups reusable instructions:

    def difference(a, b):
        return abs(a - b)

    print(difference(15, 9))

Functions help organize larger programs. The word abs means "absolute value":
it turns a negative number into a positive one, so the difference is never below zero.

ERRORS

Common Python errors include:

- SyntaxError: Invalid Python syntax.
- IndentationError: Incorrect indentation.
- NameError: A variable or function name is unknown.
- ModuleNotFoundError: A required library cannot be found.
- FileNotFoundError: A file does not exist at the given path.

Read the error message carefully. It usually identifies where the problem occurred.

Try it: Add the line print(difference(100, 72)) to the end of the example and run it.
You should see 28.""",
    ),
    (
        "5. Libraries and imports",
        """WHAT IS A LIBRARY?

A library contains reusable code.

Python has built-in libraries (they come with Python) and third-party
libraries (other people made them, and you install them).

NUMPY — Numerical computing

    import numpy as np

    pixels = np.array([10, 20, 30])
    print(pixels.mean())

OPENCV — Computer vision

    import cv2

    print(cv2.__version__)

MATPLOTLIB — Charts and images

    import matplotlib.pyplot as plt

    plt.plot([1, 2, 3], [2, 4, 6])
    plt.show()

ASTROPY — Astronomy

    from astropy.io import fits

Astropy can read scientific FITS telescope files.

TKINTER — Desktop interfaces

    import tkinter as tk

Tkinter is used to build OrbitLab's interface.

Try it: Change the NumPy pixel values and calculate their mean.""",
    ),
    (
        "6. Images and computer vision",
        """WHAT IS A DIGITAL IMAGE?

A grayscale image is a grid of tiny squares called pixels.

Each pixel has a number that says how bright it is.

ARRAYS

An array is a way to organize values. It can be a single row of numbers,
like [10, 20, 30]. It can also be a grid of rows and columns. A grayscale
image is stored as a grid like this, with one number for every pixel.

COMPUTER VISION

Computer vision uses software to analyze images.

IMAGE SUBTRACTION

Two images can be compared by subtracting the pixel numbers of one from
the other. NumPy (a library you will meet in Lesson 5) can do this for a
whole array at once.

    import numpy as np

    first = np.array([10, 20, 30])
    second = np.array([10, 35, 28])

    change = np.abs(second - first)

    print(change)

This prints:

    [ 0 15  2]

Why? The three differences are 10-10=0, 35-20=15 and 28-30=-2. The
function np.abs removes the minus sign, so -2 becomes 2.

THE BRIGHT-AND-DARK PATTERN

When you subtract without removing minus signs, the result can be positive
or negative. If a bright spot moves between two pictures, the difference
picture shows a bright spot where it is now, and a dark spot where it was
before. Seeing this pair is a clue that something changed. It is not proof.

Large differences may indicate movement, brightness changes, noise, or alignment problems.

NOISE FILTERING

Filtering means ignoring small changes that are probably just "noise" (random
speckles), so that stronger changes are easier to see.

Try it: Open OrbitLab's Experiment section and compare two pictures
(this needs the image files described in the README).""",
    ),
    (
        "7. Astronomy and FITS",
        """ASTRONOMY

Astronomy studies objects and phenomena beyond Earth.

Astronomers observe stars, galaxies, nebulae, planets, and other objects.

- A star is a huge ball of hot gas that makes its own light.
- A galaxy is a very large group of stars, gas and dust.
- A nebula is a cloud of gas and dust in space.
- An asteroid is a small, rocky object that travels around the Sun.

TELESCOPES

Telescopes collect light. Light is one kind of electromagnetic radiation.
Radio waves are another kind. There are many kinds, and different
telescopes are built to observe different kinds. For example, an optical
telescope observes visible light, and a radio telescope observes radio
waves. No single telescope can detect every kind.

Scientific observations are measurements, not necessarily natural-color photographs.

FITS FILES

FITS means Flexible Image Transport System.

FITS files can store:

- Telescope image data.
- Observation timestamps.
- Exposure information.
- Scientific metadata.

OrbitLab uses Astropy to read FITS files.

The image files are not included with OrbitLab. See the README to learn
what you need and where to put it. Until you add them, the Explore, Detect
and Experiment activities show a message instead of a picture.

Try it: Open Explore and view the Horsehead Nebula image.""",
    ),
    (
        "8. What does detection mean?",
        """DETECTION IS NOT CONFIRMATION

OrbitLab highlights candidate brightness changes between images.

A candidate is only a possibility. It is NOT a confirmed asteroid.

(An asteroid is a small, rocky object that travels around the Sun.)

A bright region might result from:

- A changing astronomical source.
- Image noise.
- Telescope or camera artifacts.
- Misalignment (the telescope pointed a tiny bit differently each time).
- An object that actually moved.

Reliable moving-object identification requires further checks.

For example, astronomers may align images and verify that an object's position changes consistently across observations.

OrbitLab is a learning demonstration. It is not professional software,
and it cannot find or confirm real asteroids. The image sequence used in
the Detect activity is for demonstration only.

Try it: Open Detect and look at the red circles.

Question: Why might a stationary star appear different in two images?""",
    ),
    (
        "9. Git and GitHub",
        """GIT

Git tracks changes to project files.

It helps developers save versions and collaborate.

A repository (or "repo") is a project folder that Git is tracking.

GITHUB

GitHub is a website that stores repositories online.

A repository can contain code, documentation, and examples.

COMMON COMMANDS

Type these in the terminal, inside your project folder.

Before your first commit, tell Git who you are. Use your own name and
email. They are stored in your commits:

    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"

Initialize a repository:

    git init

Stage changes:

    git add .

Save a version:

    git commit -m "Initial project"

IMPORTANT

Before publishing a project, exclude:

- Virtual environments.
- Passwords and private information.
- Temporary files.
- Third-party datasets without redistribution permission.

Try it: In your own words, explain the difference between Git and GitHub.""",
    ),
    (
        "10. Build your own experiment",
        """YOUR FIRST PYTHON EXPERIMENT

Create a new Python file, as you did in Lesson 2.

Add:

    import numpy as np

    first = np.array([10, 20, 30])
    second = np.array([10, 35, 28])

    change = np.abs(second - first)

    print("Differences:", change)
    print("Largest change:", change.max())

Run the program. It prints:

    Differences: [ 0 15  2]
    Largest change: 15

WHAT DID YOU LEARN?

- Importing a library.
- Creating arrays.
- Subtracting values.
- Printing results.
- Finding a maximum value.

THINK ABOUT IT

Which value changed the most, and what does that tell you about the two
sets of measurements?

Hint: look at the printed differences. The second value changed the most
(from 20 to 35, a change of 15). The first value did not change at all.
So the two sets of measurements are the same at the start, and they differ
most at the second position. A big difference is a clue to look closer.
It does not explain by itself why the values differ.

NEXT CHALLENGE

Open OrbitLab's simulate_motion.py in VS Code. It is the simplest script.

Find:

1. The libraries it imports.
2. Its variables.
3. Its loop (the line that starts with for).
4. The line that saves each picture.

You do not need to understand every line. Just look for the parts you
learned about.""",
    ),
]


class ScrollablePage(tk.Frame):
    """A scrollable Tkinter page."""

    def __init__(self, parent):
        super().__init__(parent, bg=BG)

        self.canvas = tk.Canvas(
            self,
            bg=BG,
            highlightthickness=0,
            bd=0,
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(self.canvas, bg=BG)

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw",
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region,
        )

        self.canvas.bind(
            "<Configure>",
            self.update_width,
        )

        self.canvas.bind(
            "<MouseWheel>",
            self.mousewheel,
        )

        self.content.bind(
            "<MouseWheel>",
            self.mousewheel,
        )

        self.canvas.bind_all("<MouseWheel>", self.mousewheel)

    def destroy(self):
        self.canvas.unbind_all("<MouseWheel>")
        super().destroy()

    def update_scroll_region(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def update_width(self, event):
        self.canvas.itemconfigure(
            self.window_id,
            width=event.width,
        )

    def mousewheel(self, event):
        self.canvas.yview_scroll(
            int(-event.delta / 120),
            "units",
        )


class OrbitLab(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("OrbitLab — Explore · Experiment · Learn")
        self.geometry("1100x760")
        self.minsize(900, 600)
        self.configure(bg=BG)

        self.nav_buttons = {}
        self.images = {}

        self.sidebar = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )

        # No fixed width: the sidebar sizes itself to its text, so nothing is
        # clipped on screens that use display scaling (125%, 150%, ...).
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar,
            text="◉  ORBITLAB",
            font=(FONT, 15, "bold"),
            fg=NAVY,
            bg=WHITE,
        ).pack(
            anchor="w",
            padx=20,
            pady=(26, 6),
        )

        tk.Label(
            self.sidebar,
            text="Explore · Experiment · Learn",
            font=(FONT, 10),
            fg=MUTED,
            bg=WHITE,
            justify="left",
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 24),
        )

        for page in [
            "Home",
            "Explore",
            "Detect",
            "Experiment",
            "Learn",
        ]:
            button = tk.Button(
                self.sidebar,
                text=page,
                anchor="w",
                font=(FONT, 12),
                relief="flat",
                bd=0,
                bg=WHITE,
                fg=NAVY,
                activebackground="#EAF1FF",
                padx=20,
                pady=9,
                cursor="hand2",
                command=lambda p=page: self.show_page(p),
            )

            button.pack(
                fill="x",
                padx=10,
                pady=2,
            )

            self.nav_buttons[page] = button

        tk.Label(
            self.sidebar,
            text="FREE  •  EDUCATIONAL\nFOR BEGINNERS",
            justify="left",
            font=(FONT, 9),
            fg=MUTED,
            bg=WHITE,
        ).pack(
            side="bottom",
            anchor="w",
            padx=20,
            pady=20,
        )

        self.main = tk.Frame(self, bg=BG)
        self.main.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.show_page("Home")

    def clear(self):
        for child in self.main.winfo_children():
            child.destroy()

    def show_page(self, page):
        self.clear()

        for name, button in self.nav_buttons.items():
            button.configure(
                bg="#EAF1FF" if name == page else WHITE,
                fg=BLUE if name == page else NAVY,
            )

        if page == "Home":
            self.home()
        elif page == "Learn":
            self.learn()
        else:
            self.activities(page)

    def auto_wrap(self, label, container, margin):
        """Re-wrap a label whenever its container is resized."""
        def rewrap(event):
            if label.winfo_exists():
                label.configure(wraplength=max(200, event.width - margin))

        container.bind("<Configure>", rewrap, add="+")

    def illustration(self, parent, filename, bg):
        """Return a label with a decorative picture, or None if it is missing."""
        try:
            if filename not in self.images:
                self.images[filename] = tk.PhotoImage(file=str(ASSETS / filename))
        except tk.TclError:
            return None
        return tk.Label(parent, image=self.images[filename], bg=bg, bd=0)

    def heading(self, parent, title, subtitle):
        tk.Label(
            parent,
            text=title,
            font=(FONT, 23, "bold"),
            bg=BG,
            fg=NAVY,
        ).pack(
            anchor="w",
            padx=30,
            pady=(24, 4),
        )

        sub = tk.Label(
            parent,
            text=subtitle,
            font=(FONT, 12),
            bg=BG,
            fg=MUTED,
            wraplength=500,
            justify="left",
        )
        sub.pack(
            anchor="w",
            padx=30,
            pady=(0, 16),
        )
        self.auto_wrap(sub, parent, 70)

    def action_button(self, parent, label, command):
        return tk.Button(
            parent,
            text=label,
            command=command,
            bg=BLUE,
            fg=WHITE,
            activebackground="#164BC1",
            activeforeground=WHITE,
            font=(FONT, 11, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
        )

    def card(self, parent, title, description, command):
        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )

        frame.pack(
            fill="x",
            pady=6,
        )

        tk.Label(
            frame,
            text=title,
            font=(FONT, 14, "bold"),
            fg=NAVY,
            bg=WHITE,
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 4),
        )

        desc = tk.Label(
            frame,
            text=description,
            font=(FONT, 12),
            fg=MUTED,
            bg=WHITE,
            wraplength=500,
            justify="left",
        )
        desc.pack(
            anchor="w",
            padx=18,
            pady=(0, 10),
        )
        self.auto_wrap(desc, frame, 46)

        self.action_button(
            frame,
            "Open activity  →",
            command,
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 14),
        )

    def home(self):
        page = ScrollablePage(self.main)
        page.pack(fill="both", expand=True)

        content = page.content

        hero = tk.Frame(content, bg=NAVY)

        hero.pack(
            fill="x",
            padx=30,
            pady=(28, 18),
        )

        # Decorative picture on the right. It is placed (not packed) so it never
        # pushes text around, and it is hidden if the banner becomes too narrow.
        art = self.illustration(hero, "solar_system.png", NAVY)
        art_width = 0
        if art is not None:
            art_width = self.images["solar_system.png"].width() + 18

        tk.Label(
            hero,
            text="YOUR SPACE TO DISCOVER",
            font=(FONT, 10, "bold"),
            fg="#9DC5FF",
            bg=NAVY,
        ).pack(
            anchor="w",
            padx=24,
            pady=(20, 8),
        )

        hero_title = tk.Label(
            hero,
            text="Explore the universe.\nLearn how code works.",
            font=(FONT, 22, "bold"),
            fg=WHITE,
            bg=NAVY,
            justify="left",
        )
        hero_title.pack(
            anchor="w",
            padx=24,
        )

        hero_text = tk.Label(
            hero,
            text=(
                "A free educational desktop application for anyone curious "
                "about Python programming and astronomy. It introduces a "
                "selection of fundamental concepts through simple "
                "explanations, beginner-friendly lessons, and basic "
                "demonstrations. No previous experience is required. "
                "OrbitLab is a very basic first step, not a complete course."
            ),
            font=(FONT, 12),
            fg="#D9E5F7",
            bg=NAVY,
            wraplength=500,
            justify="left",
        )
        hero_text.pack(
            anchor="w",
            padx=24,
            pady=(8, 16),
        )

        title_font = tkfont.Font(font=hero_title.cget("font"))
        title_need = title_font.measure("Learn how code works.") + 10

        def fit_hero(event):
            if not hero_text.winfo_exists():
                return
            room = event.width - 52
            show_art = art is not None and room - art_width >= title_need
            if art is not None:
                if show_art:
                    art.place(relx=1.0, x=-18, rely=0.5, anchor="e")
                else:
                    art.place_forget()
            wrap = max(150, room - (art_width if show_art else 0))
            hero_title.configure(wraplength=wrap)
            hero_text.configure(wraplength=wrap)

        hero.bind("<Configure>", fit_hero, add="+")

        self.action_button(
            hero,
            "Start learning  →",
            lambda: self.show_page("Learn"),
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 20),
        )

        tk.Label(
            content,
            text="Choose your path",
            font=(FONT, 15, "bold"),
            fg=NAVY,
            bg=BG,
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 6),
        )

        holder = tk.Frame(content, bg=BG)

        holder.pack(
            fill="x",
            padx=30,
            pady=(0, 24),
        )

        items = [
            ("Explore", "See astronomical images."),
            ("Detect", "Investigate candidate image changes."),
            ("Experiment", "Discover image processing techniques."),
            ("Learn", "Start with Python and development tools."),
        ]

        holder.columnconfigure(0, weight=1)
        holder.columnconfigure(1, weight=1)

        for index, (name, description) in enumerate(items):
            frame = tk.Frame(
                holder,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
            )

            frame.grid(
                row=index // 2,
                column=index % 2,
                sticky="nsew",
                padx=6,
                pady=6,
            )

            tk.Label(
                frame,
                text=name,
                font=(FONT, 14, "bold"),
                fg=NAVY,
                bg=WHITE,
            ).pack(
                anchor="w",
                padx=18,
                pady=(16, 4),
            )

            home_desc = tk.Label(
                frame,
                text=description,
                font=(FONT, 12),
                fg=MUTED,
                bg=WHITE,
                wraplength=220,
                justify="left",
            )
            home_desc.pack(
                anchor="w",
                padx=18,
                pady=(0, 10),
            )
            self.auto_wrap(home_desc, frame, 46)

            self.action_button(
                frame,
                "Open  →",
                lambda p=name: self.show_page(p),
            ).pack(
                anchor="w",
                padx=18,
                pady=(0, 16),
            )

    def activities(self, page_name):
        subtitles = {
            "Explore": (
                "View astronomical images and "
                "learn how telescope image files work."
            ),
            "Detect": (
                "Investigate changes in telescope images. "
                "Candidate detections are not confirmed objects."
            ),
            "Experiment": (
                "See image comparison, noise filtering, "
                "and simulated motion in action."
            ),
        }

        page = ScrollablePage(self.main)
        page.pack(fill="both", expand=True)

        header = page.content
        if page_name == "Explore":
            # Picture on the right; the title and text wrap beside it.
            top = tk.Frame(page.content, bg=BG)
            top.pack(fill="x")
            art = self.illustration(top, "telescope.png", BG)
            if art is not None:
                art.pack(side="right", padx=(0, 30), pady=(16, 0), anchor="n")
            header = tk.Frame(top, bg=BG)
            header.pack(side="left", fill="x", expand=True)

        self.heading(
            header,
            page_name,
            subtitles[page_name],
        )

        holder = tk.Frame(page.content, bg=BG)

        holder.pack(
            fill="x",
            padx=30,
            pady=(0, 24),
        )

        for title, description, script in ACTIVITIES[page_name]:
            self.card(
                holder,
                title,
                description,
                lambda s=script: self.launch(s),
            )

    def launch(self, script):
        path = ROOT / script

        if not path.is_file():
            messagebox.showerror(
                "Activity not found",
                f"Could not find {script} in:\n{ROOT}",
            )
            return

        missing = [
            name for name in DATA_NEEDED.get(script, [])
            if not (ROOT / name).is_file()
        ]

        if missing:
            messagebox.showinfo(
                "Telescope data needed",
                "This activity needs a file that is not included with "
                "OrbitLab:\n\n"
                + "\n".join(missing)
                + "\n\nPlease read the 'Telescope data' section of "
                "README.md to see where to get it and where to put it.",
            )
            return

        try:
            process = subprocess.Popen(
                [sys.executable, str(path)],
                cwd=str(ROOT),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except OSError as exc:
            messagebox.showerror(
                "Could not start activity",
                str(exc),
            )
            return

        # Collect stderr in a thread so failures can be reported
        # without freezing the interface.
        def watch():
            error_text = process.communicate()[1]
            if process.returncode != 0:
                lines = (error_text or "").strip().splitlines()
                detail = "\n".join(lines[-6:]) or "No details available."
                self.after(
                    0,
                    lambda: messagebox.showerror(
                        "Activity failed",
                        f"{script} stopped with an error:\n\n{detail}",
                    ),
                )

        threading.Thread(target=watch, daemon=True).start()

    def learn(self):
        self.heading(
            self.main,
            "Learning Center",
            (
                "Start from zero: tools, Python fundamentals, "
                "libraries, astronomy, and hands-on coding."
            ),
        )

        body = tk.Frame(self.main, bg=BG)

        body.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 24),
        )

        lesson_list = tk.Listbox(
            body,
            width=29,
            font=(FONT, 12),
            bg=WHITE,
            fg=NAVY,
            selectbackground=BLUE,
            selectforeground=WHITE,
            highlightthickness=1,
            highlightbackground=BORDER,
            relief="flat",
            activestyle="none",
            exportselection=False,
        )

        lesson_list.pack(
            side="left",
            fill="y",
            padx=(0, 16),
        )

        for title, _ in LESSONS:
            lesson_list.insert("end", title)

        detail = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )

        detail.pack(
            side="left",
            fill="both",
            expand=True,
        )

        title_label = tk.Label(
            detail,
            text="",
            font=(FONT, 18, "bold"),
            fg=NAVY,
            anchor="w",
            justify="left",
            wraplength=400,
        )

        title_label.pack(
            fill="x",
            padx=20,
            pady=(14, 10),
        )
        self.auto_wrap(title_label, detail, 40)

        text_frame = tk.Frame(detail, bg=WHITE)

        text_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 18),
        )

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        content = tk.Text(
            text_frame,
            wrap="word",
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 13),
            relief="flat",
            padx=2,
            pady=2,
            spacing1=4,
            spacing2=4,
            spacing3=8,
            yscrollcommand=scrollbar.set,
        )

        content.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.configure(
            command=content.yview
        )

        content.tag_configure(
            "code",
            font=("Consolas", 12),
            background="#EEF3FA",
            lmargin1=12,
            lmargin2=12,
        )

        def select_lesson(event=None):
            selection = lesson_list.curselection()

            if not selection:
                return

            title, explanation = LESSONS[selection[0]]

            title_label.configure(text=title)

            content.configure(state="normal")
            content.delete("1.0", "end")
            content.insert("1.0", explanation)

            # Show indented code examples in a fixed-width font.
            for number, line in enumerate(explanation.split("\n"), start=1):
                if line.startswith("    "):
                    content.tag_add("code", f"{number}.0", f"{number}.end")

            content.configure(state="disabled")

        lesson_list.bind(
            "<<ListboxSelect>>",
            select_lesson,
        )

        lesson_list.selection_set(0)
        select_lesson()


if __name__ == "__main__":
    OrbitLab().mainloop()