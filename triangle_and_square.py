from textx import metamodel_from_file

turtle_meta = metamodel_from_file("tx_turtle/turtle.tx")
scene = turtle_meta.model_from_file("triangle_and_square.turtle")

drawing_total = len(scene.draw_instructions)

import turtle
import argparse 

parser = argparse.ArgumentParser(description="Draw graphics specified from Trutle DSL")
parser.add_argument('graphic_num', metavar='N', type=int, help="Specify the number of graphics to draw (default: all)")
parser.add_argument('--no_color', '-nc',action="store_true", help="Specify if you want shapes to be in black and white")
args = parser.parse_args()

# print(scene)
import inspect

# print(inspect.getmembers(scene))
import objgraph

objgraph.show_refs([scene], filename='scene-graph.png')

def rad_to_deg(radian):
    return radian * 57.296

def draw_shape(shape):
    turtle.pencolor(shape.line_color.color if (shape.line_color is not None and args.no_color is False)  else 'black')
    turtle.fillcolor(shape.fill_color.color if (shape.fill_color is not None and args.no_color is False) else 'white')
    turtle.down()
    turtle.begin_fill()
    for l in shape.lines:
        draw_line(l)
    turtle.end_fill()

def draw_line(l):
    bearing = l.direction.bearing
    if bearing == 'N':
        turtle.setheading(90)
    elif bearing == 'NE':
        turtle.setheading(45)
    elif bearing == 'E':
        turtle.setheading(0)
    elif bearing == 'SE':
        turtle.setheading(-45)
    elif bearing == 'S':
        turtle.setheading(-90)
    elif bearing == 'SW':
        turtle.setheading(-135)
    elif bearing == 'W':
        turtle.setheading(-180)
    elif bearing == 'NW':
        turtle.setheading(-225)
    else:
        
        # here we will introduce a check for degree or radians
        if (l.direction.angle.radians):
            turtle.left(rad_to_deg(l.direction.angle.radians))
        else:
            turtle.left(l.direction.angle.degrees)
    turtle.forward(l.length)

# use if statements to specify a new variable shape_count which will be processed into draw
if (args.graphic_num < 0):
    raise Exception ("You cannot have a negative number of shapes (value given: {})".format(args.graphic_num))

elif (args.graphic_num > drawing_total):
    print("Cannot have value greater than total number of shapes ({})".format(drawing_total))
    shape_count = drawing_total
else:
    shape_count = args.graphic_num
    
for i in range(0, shape_count):
    d = scene.draw_instructions[i]
    turtle.up()
    turtle.goto(d.position.x if d.position is not None else 0,
                d.position.y if d.position is not None else 0)
    draw_shape(d.shape)

turtle.hideturtle()
turtle.done()
