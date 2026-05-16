import os
import random
from pathlib import Path
from dataclasses import dataclass

import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

API_USERNAME = os.getenv("RA_USERNAME")
API_KEY = os.getenv("RA_API_KEY")

USERS = [
    "tmfc666"
]

OUTPUT_DIR = Path("users")
OUTPUT_DIR.mkdir(exist_ok=True)

FONT_PATH = "Pixellari.ttf"


@dataclass
class GamerProfile:
    username: str
    motto: str
    rich_presence: str
    total_points: int
    total_true_points: int
    total_mastered: int
    user_pic: str


def get_profile(username: str):
    url = (
        f"https://retroachievements.org/API/API_GetUserProfile.php"
        f"?u={API_USERNAME}&y={API_KEY}&z={username}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    return GamerProfile(
        username=data.get("User", username),
        motto=data.get("Motto", ""),
        rich_presence=data.get("RichPresenceMsg", "Offline"),
        total_points=data.get("TotalPoints", 0),
        total_true_points=data.get("TotalTruePoints", 0),
        total_mastered=data.get("TotalRanked", 0),
        user_pic=data.get("UserPic", "")
    )


def load_background():
    bg_dir = Path("backgrounds")
    choices = list(bg_dir.glob("background*.png"))

    if not choices:
        return Image.new("RGB", (800, 200), (20, 20, 20))

    selected = random.choice(choices)
    return Image.open(selected).convert("RGBA")


def generate_signature(profile: GamerProfile, output_path: Path):
    bg = load_background().resize((800, 200))

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 110))
    bg.alpha_composite(overlay)

    draw = ImageDraw.Draw(bg)

    title_font = ImageFont.truetype(FONT_PATH, 24)
    text_font = ImageFont.truetype(FONT_PATH, 16)

    draw.text((20, 20), profile.username, font=title_font, fill="white")
    draw.text((20, 60), f"Points: {profile.total_points}", font=text_font, fill="white")
    draw.text((20, 85), f"True Points: {profile.total_true_points}", font=text_font, fill="white")
    draw.text((20, 110), f"Mastered Games: {profile.total_mastered}", font=text_font, fill="white")
    draw.text((20, 145), profile.rich_presence[:60], font=text_font, fill="white")

    bg.convert("RGB").save(output_path, "PNG")


def main():
    for username in USERS:
        try:
            profile = get_profile(username)

            output = OUTPUT_DIR / f"{username}.png"

            generate_signature(profile, output)

            print(f"Generated: {output}")

        except Exception as e:
            print(f"Failed for {username}: {e}")


if __name__ == "__main__":
    main()
