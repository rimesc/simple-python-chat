"""
Support for emoticons/emoji.

Functions:
* replace(message) - replace known emoticons with the equivalent emoji
"""

# Unicode codes for some common emoji.  You can add more from
# https://www.unicode.org/emoji/charts/full-emoji-list.html (you
# need to use the code from the second column, but with the U+
# replaced by 0x).
SMILE = chr(0x1F642)
LAUGH = chr(0x1F600)
FROWN = chr(0x2639)
CRY = chr(0x1F622)
SURPRISE = chr(0x1F62E)
TONGUE = chr(0x1F61B)
WINK = chr(0x1F609)
ANGRY = chr(0x1F620)
SKEPTICAL = chr(0x1F914)
COOL = chr(0x1F60E)

# Some common emoticons and the corresponding emoji.  You can invent
# your own, or get some ideas from https://en.wikipedia.org/wiki/List_of_emoticons.
REPLACEMENTS = {
  ':-)': SMILE,
  ':-D': LAUGH,
  ':-(': FROWN,
  ':\'-(': CRY,
  ':-O': SURPRISE,
  ';-)': WINK,
  ':-P': TONGUE,
  '>:[': ANGRY,
  ':-/': SKEPTICAL,
  'B-)': COOL,
}

def replace(message):
  "Replace known emoticons with the equivalent emoji."
  for (emoticon, emoji) in REPLACEMENTS.items():
    message = message.replace(emoticon, emoji)
  return message