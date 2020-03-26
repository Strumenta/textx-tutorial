from os.path import dirname, join

from textx import language, metamodel_from_file

@language("Turtle", "*.turtle")
def turtle():
    "A language for drawing shapes using Turtle Graphics."
    return metamodel_from_file(join(dirname(__file__), "turtle.tx"))
