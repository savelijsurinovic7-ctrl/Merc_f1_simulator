import turtle
import math
import random
import time

# ================= НАСТРОЙКИ =================
screen = turtle.Screen()
screen.setup(1200, 700)
screen.bgcolor("black")
screen.title("SIMULATOR F! FOR MERC")
screen.tracer(0)

# ================= ПЕРЕМЕННЫЕ =================
speed = 0
laps = 0
crashes = 0
game_active = True
crossed_start = True          # ИСПРАВЛЕНО: стартуем уже после прохода стартовой линии

# ================= АСФАЛЬТ =================
asphalt = turtle.Turtle()
asphalt.penup()
asphalt.goto(-560, -200)
asphalt.pendown()
asphalt.color("#2a2a2a")
asphalt.begin_fill()
for _ in range(2):
    asphalt.forward(1120)
    asphalt.left(90)
    asphalt.forward(400)
    asphalt.left(90)
asphalt.end_fill()
asphalt.hideturtle()

# ================= СУПЕР-ИЗВИЛИСТАЯ ТРАССА =================
def get_track_bounds(x):
    wave1 = 70 * math.sin(x * 0.008)
    wave2 = 30 * math.sin(x * 0.025 + 2)
    wave3 = 15 * math.sin(x * 0.06 + 1)
    center_y = wave1 + wave2 + wave3
    
    # ШИРОКАЯ ДОРОГА (было 140, стало 200)
    width = 260 + 40 * math.sin(x * 0.012) + 20 * math.sin(x * 0.03)
    
    return center_y + width/2, center_y - width/2

track_top = turtle.Turtle()
track_top.penup()
track_top.color("white")
track_top.width(4)

track_bottom = turtle.Turtle()
track_bottom.penup()
track_bottom.color("white")
track_bottom.width(4)

for x in range(-550, 551, 8):
    top_y, bottom_y = get_track_bounds(x)
    track_top.goto(x, top_y)
    track_top.pendown()
    track_bottom.goto(x, bottom_y)
    track_bottom.pendown()

track_top.hideturtle()
track_bottom.hideturtle()

# ================= СТАРТОВАЯ ЛИНИЯ =================
start_line = turtle.Turtle()
start_line.penup()
start_line.goto(-530, -200)
start_line.pendown()
start_line.color("red")
start_line.width(5)
start_line.goto(-530, 200)
start_line.hideturtle()

# ================= БОРДЮРЫ =================
def draw_curb(x_start, x_end, y_offset, color1, color2):
    curb = turtle.Turtle()
    curb.penup()
    curb.width(8)
    x = x_start
    block = 0
    while x < x_end:
        if block % 2 == 0:
            curb.color(color1)
        else:
            curb.color(color2)
        curb.goto(x, y_offset)
        curb.pendown()
        curb.goto(x + 15, y_offset)
        curb.penup()
        x += 15
        block += 1
    curb.hideturtle()

draw_curb(-540, 540, 150, "red", "white")
draw_curb(-540, 540, -170, "red", "white")

# ================= МАШИНА =================
car = turtle.Turtle()
car.shape("triangle")
car.shapesize(1.2, 1.5)
car.color("#00D2BE")
car.penup()
car.goto(-500, 100)          # Старт сразу за стартовой линией
car.setheading(0)

# ================= ТЕКСТ =================
info = turtle.Turtle()
info.penup()
info.hideturtle()
info.color("white")
info.goto(-550, 250)

def update_info():
    info.clear()
    status = "ГОНКА" if game_active else "GAME OVER"
    info.write(
        f"СКОРОСТЬ: {int(abs(speed))} km/h\n"
        f"КРУГИ: {laps} / 13\n"
        f"ВРЕЗАНИЯ: {crashes} / 3\n"
        f"СТАТУС: {status}",
        font=("Courier", 16, "bold")
    )

# ================= ПРОВЕРКА ВЫЛЕТА =================
def is_on_track(x, y):
    top_y, bottom_y = get_track_bounds(x)
    return bottom_y - 15 <= y <= top_y + 15

# ================= УПРАВЛЕНИЕ =================
def accelerate():
    global speed
    if not game_active:
        return
    speed += 2
    if speed > 16:
        speed = 16

def brake():
    global speed
    if not game_active:
        return
    speed -= 2.5
    if speed < -6:
        speed = -6

def turn_left():
    if not game_active:
        return
    car.left(12)

def turn_right():
    if not game_active:
        return
    car.right(12)

# ================= ЛОГИКА КРУГОВ (ИСПРАВЛЕНА) =================
def check_lap():
    global laps, crossed_start, game_active
    x = car.xcor()
    if x > -500 and not crossed_start:
        crossed_start = True
    if x < -530 and crossed_start and game_active:
        laps += 1
        crossed_start = False
        update_info()
        if laps >= 13:
            game_active = False
            win = turtle.Turtle()
            win.penup()
            win.hideturtle()
            win.color("gold")
            win.goto(0, 0)
            win.write("🏆 GRAND PRIX WON! 🏆", font=("Courier", 24, "bold"), align="center")
            screen.update()

# ================= ДВИЖЕНИЕ =================
def move():
    global speed, crashes, game_active
    if not game_active:
        return

    old_x, old_y = car.xcor(), car.ycor()
    car.forward(speed)

    if not is_on_track(car.xcor(), car.ycor()):
        car.goto(old_x, old_y)
        car.color("red")
        speed = 0
        crashes += 1
        update_info()

        if crashes >= 3:
            game_active = False
            update_info()
            game_over = turtle.Turtle()
            game_over.penup()
            game_over.hideturtle()
            game_over.color("red")
            game_over.goto(0, -50)
            game_over.write("❌ 3 CRASHES — GAME OVER ❌", font=("Courier", 20, "bold"), align="center")
            screen.update()
            return

        screen.ontimer(lambda: car.color("#00D2BE"), 400)

    if car.xcor() > 550:
        car.goto(-550, car.ycor())
    if car.xcor() < -550:
        car.goto(550, car.ycor())

    check_lap()
    update_info()
    screen.update()
    screen.ontimer(move, 30)

# ================= ЗАПУСК =================
screen.listen()
screen.onkey(accelerate, "Up")
screen.onkey(brake, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")

update_info()
move()
screen.mainloop()