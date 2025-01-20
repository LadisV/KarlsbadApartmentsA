from PIL import Image
import os

input_folder = "media/room_images"  # Složka s obrázky
max_width = 1920  # Maximální šířka obrázků
quality = 70  # Kvalita obrázků (v procentech)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Změna velikosti obrázku (zachování poměru stran)
        img.thumbnail((max_width, img.height * max_width // img.width))

        # Přepsání původního obrázku optimalizovanou verzí
        img.save(img_path, optimize=True, quality=quality)

        print(f"Optimalizován: {filename}")

print("Optimalizace dokončena!")
