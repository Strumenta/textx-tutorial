from textx import metamodel_from_file

turtle_meta = metamodel_from_file("tx_turtle/turtle.tx")
scene = turtle_meta.model_from_file("triangle_and_square.turtle")
max_turtle_speed = 10
default_speed = max_turtle_speed * (50 / 100)

drawing_total = len(scene.draw_instructions)

import turtle
import argparse 

# CLI commands for processing Turtle DSL
parser = argparse.ArgumentParser(description="Draw graphics specified from Trutle DSL")
parser.add_argument('graphic_num', nargs='?', const=drawing_total,default=drawing_total, type=int, help="Specify the number of graphics to draw (default: all)")
parser.add_argument('--no_color', '-nc',action="store_true", help="Specify if you want shapes to be in black and white")
args = parser.parse_args()

# print(scene)
import inspect

# print(inspect.getmembers(scene))
import objgraph

objgraph.show_refs([scene], filename='scene-graph.png')

def rad_to_deg(radian):
    return radian * 57.296

def draw_circle(draw_instruct):
    shape = draw_instruct.shape
    turtle.pencolor(shape.line_color.color if (shape.line_color is not None and args.no_color is False)  else 'black')
    turtle.fillcolor(shape.fill_color.color if (shape.fill_color is not None and args.no_color is False) else 'white')
    turtle.down()
    turtle.begin_fill()
    
    if (draw_instruct.scale):
        draw_radius = round((shape.radius.radius) * draw_instruct.scale.a)
    else:
        draw_radius = shape.radius.radius
    turtle.circle(draw_radius)
    turtle.end_fill()
    
def draw_shape(draw_instruct):
    shape = draw_instruct.shape
    turtle.pencolor(shape.line_color.color if (shape.line_color is not None and args.no_color is False)  else 'black')
    turtle.fillcolor(shape.fill_color.color if (shape.fill_color is not None and args.no_color is False) else 'white')
    turtle.down()
    turtle.begin_fill()
    for l in shape.lines:
        draw_line(l, draw_instruct)
    turtle.end_fill()

def draw_line(l, draw_instruct):
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
            
    # At this point, add the rotation angle and scaling factor if it exists in the shape
    if (draw_instruct.rotation):
        if (draw_instruct.rotation.b.radians):
            turtle.left(rad_to_deg(draw_instruct.rotation.b.radians))
        else:
            turtle.left(draw_instruct.rotation.b.degrees)

    if (draw_instruct.scale):
        draw_length = round(l.length * draw_instruct.scale.a)
    else:
        draw_length = l.length
    turtle.forward(draw_length)

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
    # set turtle speed to default speed when moving between shapes
    turtle.speed(default_speed)
    turtle.goto(d.position.x if d.position is not None else 0,
                d.position.y if d.position is not None else 0)
    
    # Specify the turtle speed here if applicable (if no value given, default scaling value to 0.5)
    if (d.shape.speed is not None):
        turtle_speed = max_turtle_speed * (d.shape.speed.speedMultiplier / 100)
    else:
        turtle_speed = default_speed # 50% of max speed
    turtle.speed(turtle_speed)
    
    # check which instructions to follow > check if shape type is either a circle or a polygon
    
    if (d.shape.type.type in ['circle', 'Circle']):
        try:
            draw_circle(d)
        except Exception as e:
            print("Error: {}. Skipping...".format(e))
            continue
            
    elif (d.shape.type.type in ['polygon', 'Polygon']):
        try:
            draw_shape(d)
        except Exception as e:
            print("Error: {}. Skipping...".format(e))
            continue

turtle.hideturtle()
turtle.done()
