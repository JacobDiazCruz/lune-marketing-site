import sys, os, json
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

ROOT = '/Users/carlcruz/Documents/Lune map assets/Isometric assets/'
OUT = '/Users/carlcruz/Downloads/Landing page-html/assets/art/'
os.makedirs(OUT, exist_ok=True)

# (source, slug, name, group)  — order = display order
PIECES = [
  # Characters: people
  ('Humans/Scholar transparent.png', 'scholar', 'Scholar', 'people'),
  ('Humans/Noblewoman 2.png', 'noblewoman', 'Noblewoman', 'people'),
  ('Humans/Hooded traveler.png', 'hooded-traveler', 'Hooded Traveler', 'people'),
  ('Humans/Bounty hunter.png', 'bounty-hunter', 'Bounty Hunter', 'people'),
  ('Humans/Transparent .png', 'shieldmaiden', 'Shieldmaiden', 'people'),
  ('Humans/Knight7final.png', 'knight', 'Knight', 'people'),
  ('Humans/Monk.png', 'monk', 'Monk', 'people'),
  ('Humans/Teacher.png', 'teacher', 'Teacher', 'people'),
  ('Humans/Merchant Final Render.png', 'merchant', 'Merchant', 'people'),
  ('Humans/Character 13.png', 'armored-knight', 'Armored Knight', 'people'),
  ('Humans/Char3.png', 'villager', 'Villager', 'people'),
  # Characters: creatures
  ('Creatures/Dragon 2.png', 'dragon', 'Dragon', 'creatures'),
  ('Creatures/13518.png', 'stone-troll', 'Stone Troll', 'creatures'),
  ('Creatures/Creature 2.png', 'ghoul', 'Ghoul', 'creatures'),
  # World: medieval
  ('Medieval/Medieval 5.png', 'tower-house', 'Stone tower house', 'medieval'),
  ('Medieval/Medieval 6.png', 'tower-house-red', 'Tower house, red roof', 'medieval'),
  ('Houses/Medieval 1 Asset - Iso - Transparent.png', 'snowy-cottage', 'Snowy cottage', 'medieval'),
  ('Houses/House 13.png', 'thatched-cottage', 'Thatched cottage', 'medieval'),
  ('Houses/House10a.png', 'brick-cottage', 'Brick cottage', 'medieval'),
  ('Houses/House11.png', 'timber-townhouse', 'Timber townhouse', 'medieval'),
  ('Houses/House12s.png', 'stone-townhouse', 'Stone townhouse', 'medieval'),
  ('Houses/House14.png', 'timber-house', 'Timber house', 'medieval'),
  ('Houses/Market.png', 'market-stall', 'Market stall', 'medieval'),
  ('Houses/Market2.png', 'market-stall-2', 'Covered stall', 'medieval'),
  # World: empire
  ('Empire/Empire Building - Great Mausoleum.png', 'great-mausoleum', 'Great mausoleum', 'empire'),
  ('Empire/Empire Building - Temple Agora.png', 'temple-agora', 'Temple agora', 'empire'),
  ('Empire/Empire Building -  Agora _ Colonnade Market.png', 'colonnade-market', 'Colonnade market', 'empire'),
  ('Empire/Empire arena 1.png', 'arena', 'Arena', 'empire'),
  ('Empire/Ampitheatere - Iso Transparent.png', 'amphitheatre', 'Amphitheatre', 'empire'),
  ('Empire/Empire Lighthouse - ISO Transparent.png', 'lighthouse', 'Lighthouse', 'empire'),
  ('Empire/Empire Building -  001.png', 'domed-tower', 'Domed tower', 'empire'),
  ('Empire/Empire Uppe Class - ISO Transparent.png', 'upper-class-villa', 'Upper-class villa', 'empire'),
  ('Empire/Empire Middle Class - ISO Transparent.png', 'middle-class-house', 'Middle-class house', 'empire'),
  ('Empire/Empire Slums - ISO Transparent.png', 'slums', 'Slums', 'empire'),
  ('Empire/Empire Market  - ISO Transparent.png', 'empire-market', 'Market hall', 'empire'),
  ('Empire/Empire house 2.png', 'empire-house', 'Townhouse', 'empire'),
  # World: eastern
  ('Eastern/Eastern Castle - ISO Transparent.png', 'eastern-castle', 'Eastern castle', 'eastern'),
  ('Eastern/Eastern Style Asset - Iso - Transparent.png', 'eastern-hall', 'Eastern hall', 'eastern'),
  ('Eastern/Eastern House - ISO.png', 'eastern-house', 'Eastern house', 'eastern'),
  ('Eastern/Eastern cart - ISO.png', 'eastern-cart', 'Eastern cart', 'eastern'),
  # World: babylonian
  ('Babylonian/Babylonian Castle- ISO Transparent.png', 'babylonian-castle', 'Babylonian castle', 'babylonian'),
  ('Babylonian/Babylonian Temple - ISO.png', 'babylonian-temple', 'Babylonian temple', 'babylonian'),
  ('Babylonian/Babylonian Pyramid - ISO.png', 'babylonian-pyramid', 'Stepped pyramid', 'babylonian'),
  ('Babylonian/babylonian House.png', 'babylonian-house', 'Babylonian house', 'babylonian'),
  # World: elven
  ('Elves/ElfB1v1(New).png', 'elven-village', 'Elven village', 'elven'),
  ('Elves/ElfB2v1.png', 'elven-manor', 'Elven manor', 'elven'),
  ('Elves/ElfB1 - 02 (New).png', 'elven-hall', 'Elven hall', 'elven'),
  ('Elves/ElfB1 - 01.png', 'elven-spire', 'Elven spire', 'elven'),
  ('Elves/ElfB1 - 03.png', 'elven-gazebo', 'Elven gazebo', 'elven'),
  # World: castles & ruins
  ('Castle/castle Asset 2  HD with shadow.png', 'castle', 'Castle', 'castles'),
  ('Houses/Dark Citadel - Iso Transparent.png', 'dark-citadel', 'Dark citadel', 'castles'),
  ('Ruins/Ruined Church - ISO Transparent.png', 'ruined-church', 'Ruined church', 'castles'),
  ('Ruins/Ancient ruins - Iso - Transparent.png', 'ancient-ruins', 'Ancient ruins', 'castles'),
  ('Castle/castle Asset 2  HD_ Castle Wall With Shadow.png', 'castle-wall-ring', 'Castle wall', 'castles'),
  ('Walls/Castle wall Quarter view.png', 'castle-wall', 'Castle wall section', 'castles'),
  ('Walls/Wall_ quarter view.png', 'stone-wall', 'Stone wall section', 'castles'),
  # World: farm
  ('Farm/Farm Village (No Sky).png', 'farm-village', 'Farm village', 'farm'),
  ('Eastern/Windmill - ISO.png', 'windmill', 'Windmill', 'farm'),
  ('Farm/House 1 - v1.png', 'farmhouse', 'Farmhouse', 'farm'),
  ('Farm/House 2 - v1.png', 'farm-cottage', 'Farm cottage', 'farm'),
  ('Farm/House 3.png', 'barn', 'Barn', 'farm'),
  ('Farm/Field (3).png', 'fields', 'Crop fields', 'farm'),
  ('Farm/Well.png', 'well', 'Well', 'farm'),
  # World: nature
  ('Trees/Tree 10.png', 'oak', 'Oak', 'nature'),
  ('Trees/Green Tree PNG update 2.png', 'green-tree', 'Green tree', 'nature'),
  ('Trees/Orange tree 3 PNG.png', 'autumn-tree', 'Autumn tree', 'nature'),
  ('Trees/Red tree PNG.png', 'red-tree', 'Red tree', 'nature'),
  ('Trees/Snow pine Tree PNG.png', 'snow-pine', 'Snowy pine', 'nature'),
  ('Trees/Tree 11y.png', 'tall-pine', 'Tall pine', 'nature'),
  ('Trees/Dried Tree  PNG.png', 'dead-tree', 'Dead tree', 'nature'),
  ('Mountains/Snow Mountain.png', 'snow-range', 'Snowy range', 'nature'),
  ('Mountains/Snow mountain PNG.png', 'snow-peak', 'Snowy peak', 'nature'),
  ('Mountains/Rocky Mountain PNG.png', 'rocky-mountain', 'Rocky mountain', 'nature'),
  ('Mountains/Rocky Mountain PNG_Revision.png', 'dark-mountain', 'Dark mountain', 'nature'),
  ('Mountains/Green Mountain PNG.png', 'green-mountain', 'Green mountain', 'nature'),
  ('Mountains/Sand Mountain PNG.png', 'sand-mountain', 'Sand mountain', 'nature'),
  ('Mountains/volcano PNG (2).png', 'volcano', 'Volcano', 'nature'),
  ('Rock-Hill- Bush/Twin Hill.png', 'twin-hill', 'Twin hills', 'nature'),
  ('Rock-Hill- Bush/Hill.png', 'hill', 'Hill', 'nature'),
  ('Rock-Hill- Bush/Rock.png', 'rock', 'Rock', 'nature'),
  ('Rock-Hill- Bush/Bush  with Shadow.png', 'bush', 'Bush', 'nature'),
  ('Grass/Grass 4.png', 'grass', 'Tall grass', 'nature'),
  ('Terrains/Chasm.png', 'chasm', 'Chasm', 'nature'),
  # World: props
  ('Fountains/Fountain.png', 'fountain', 'Fountain', 'props'),
  ('Statues/Warrior - Iso - Transparent.png', 'warrior-statue', 'Warrior statue', 'props'),
  ('Animals/Carriage 1.png', 'carriage', 'Horse and carriage', 'props'),
  ('Cart, Esplosion and cave/Cart 2.png', 'hay-cart', 'Hay cart', 'props'),
  ('Camp/Tent.png', 'tent', 'Tent', 'props'),
  ('Camp/Bonfire.png', 'bonfire', 'Bonfire', 'props'),
  ('Cart, Esplosion and cave/Mine.png', 'mine', 'Mine entrance', 'props'),
  ('Bridges/Bridge  2 PNG Kheil.png', 'rope-bridge', 'Rope bridge', 'props'),
  ('Bridges/bridge 1 PNG Kheil with shadow.png', 'wooden-bridge', 'Wooden bridge', 'props'),
  ('Bridges/bridge 3 PNG Kheil with shadow.png', 'stone-bridge', 'Stone bridge', 'props'),
  ('Stairs/Stairs.png', 'stairs', 'Stairs', 'props'),
  ('Cart, Esplosion and cave/Explosion.png', 'explosion', 'Explosion', 'props'),
]

def cut_white(im, seeds):
    """Opaque white background → alpha: remove near-white regions touching the border or a seed point."""
    a = np.asarray(im.convert('RGB')).astype(np.int16)
    cand = a.min(axis=2) > 222
    h, w = cand.shape
    bg = np.zeros_like(cand)
    q = deque()
    starts = [(0, x) for x in range(w)] + [(h - 1, x) for x in range(w)] + [(y, 0) for y in range(h)] + [(y, w - 1) for y in range(h)] + seeds
    for y, x in starts:
        if cand[y, x] and not bg[y, x]:
            bg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and cand[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; q.append((ny, nx))
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert('RGBA'); out.putalpha(alpha)
    return out

def trim(im):
    bbox = im.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox()
    im = im.crop(bbox)
    pad = int(max(im.size) * 0.03)
    canvas = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    canvas.paste(im, (pad, pad))
    return canvas

def fit(im, box):
    im = im.copy(); im.thumbnail(box, Image.LANCZOS); return im

manifest = []
for src, slug, name, group in PIECES:
    im = Image.open(ROOT + src).convert('RGBA')
    if slug == 'stone-troll':
        im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
        im = cut_white(im, [(1572, 1757)])
    im = trim(im)
    is_char = group in ('people', 'creatures')
    thumb = fit(im, (600, 800) if is_char else (640, 640))
    full = fit(im, (1800, 1800))
    thumb.save(OUT + slug + '.webp', 'WEBP', quality=86, method=6)
    full.save(OUT + slug + '-full.webp', 'WEBP', quality=88, method=6)
    manifest.append({'id': slug, 'name': name, 'group': group, 'w': full.width, 'h': full.height})
    print(f'{slug:22} {group:10} full={full.size} thumb={thumb.size}')

json.dump(manifest, open(OUT + 'manifest.json', 'w'), indent=1)
print(len(manifest))
