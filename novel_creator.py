from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()
    font_size = font.getsize(text)

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return text_lines

class SceneData:
    def __init__(self, id):
        self.id = id
        self.background = None
        self.character = None
        self.text = None

    def createNovelScene(self):
        new_background = self.background.copy()
        new_background.paste(self.character, (self.background.width // 2 - self.character.width // 2, self.background.height - self.character.height), self.character.convert('RGBA'))
        print(f"User {self.id} made a scene")

        dialogue_image = Image.open("res/dialogue.png")
        new_background.paste(dialogue_image, (self.background.width // 2 - dialogue_image.width // 2, self.background.height - dialogue_image.height), dialogue_image)


        draw = ImageDraw.Draw(new_background)
        font = ImageFont.truetype("sans-serif.ttf", 50)
        text_to_print = wrap_text(self.text, dialogue_image.width - 100, font)

        y = self.background.height * 3 / 4
        for line in text_to_print:
            draw.text((self.background.width // 2 * 1.5 / 4, y), line, fill=(255,255,255), font=font)
            #w, h = draw.textsize(line)
            y = y + 50

        new_background.save(f"img{self.id}.png")
        return open(f"img{self.id}.png", "rb")
