# -*- coding: UTF8 -*-
import math

import pygame, sys
import autopy

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


class Controller:
    __axis = 0
    __just_up = dict()
    __just_down = dict()
    __buttons = dict()

    @classmethod
    def update(cls) -> None:
        cls.__just_up.clear()
        cls.__just_down.clear()

    @classmethod
    def set_axis(cls, value: float) -> None:
        cls.__axis = value

    @classmethod
    def set_button_down(cls, button: int) -> None:
        cls.__buttons[button] = True
        cls.__just_down[button] = True

    @classmethod
    def set_button_up(cls, button: int) -> None:
        cls.__buttons[button] = False
        cls.__just_up[button] = True

    @classmethod
    def is_button_down(cls, button: int) -> bool:
        return cls.__buttons.get(button, False)

    @classmethod
    def is_button_just_down(cls, button: int) -> bool:
        return cls.__just_down.get(button, False)

    @classmethod
    def is_button_just_up(cls, button: int) -> bool:
        return cls.__just_up.get(button, False)

    @classmethod
    def get_axis(cls) -> float:
        return cls.__axis


class Screen:
    width, height = autopy.screen.size()


class Mouse:
    x = Screen.width / 2
    y = Screen.height / 2
    autopy.mouse.move(x, y)

    __left_toggled = False
    __right_toggled = False

    @classmethod
    def __check_x(cls, x: float) -> float:
        if x < 0:
            x = 0
        elif x >= Screen.width:
            x = Screen.width - 1
        return x

    @classmethod
    def __check_y(cls, y: float) -> float:
        if y < 0:
            y = 0
        elif y >= Screen.height:
            y = Screen.height - 1
        return y

    @classmethod
    def set(cls, x: float, y: float) -> None:
        cls.x = cls.__check_x(x)
        cls.y = cls.__check_y(y)
        autopy.mouse.move(cls.x, cls.y)

    @classmethod
    def set_smooth(cls, x: float, y: float) -> None:
        cls.x = cls.__check_x(x)
        cls.y = cls.__check_y(y)
        autopy.mouse.smooth_move(cls.x, cls.y)

    @classmethod
    def move(cls, dx: float, dy: float) -> None:
        cls.set(cls.x + dx, cls.y + dy)

    @classmethod
    def move_smooth(cls, dx: float, dy: float) -> None:
        cls.set_smooth(cls.x + dx, cls.y + dy)

    @classmethod
    def press_left(cls) -> None:
        autopy.mouse.click(autopy.mouse.Button.LEFT)

    @classmethod
    def toggle_left(cls, toggle: bool) -> None:
        if toggle != cls.__left_toggled:
            cls.__left_toggled = toggle
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, toggle)

    @classmethod
    def press_right(cls) -> None:
        autopy.mouse.click(autopy.mouse.Button.RIGHT)

    @classmethod
    def toggle_right(cls, toggle: bool) -> None:
        if toggle != cls.__right_toggled:
            cls.__right_toggled = toggle
            autopy.mouse.toggle(autopy.mouse.Button.RIGHT, toggle)

    @classmethod
    def press_middle(cls) -> None:
        autopy.mouse.click(autopy.mouse.Button.MIDDLE)


class DriveMode:
    angle = 0

    @classmethod
    def set_mouse(cls):
        x = Screen.width / 2 + math.cos(DriveMode.angle) * 200
        y = Screen.height / 2 + math.sin(DriveMode.angle) * 200
        Mouse.set(x, y)

    @classmethod
    def set_mouse_smooth(cls):
        x = Screen.width / 2 + math.cos(DriveMode.angle) * 200
        y = Screen.height / 2 + math.sin(DriveMode.angle) * 200
        Mouse.set_smooth(x, y)


MOUSE_MODE = 0
DRIVE_MODE = 1
mode = MOUSE_MODE

while True:
    Controller.update()
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Button: {event.button}")
            Controller.set_button_down(event.button)
        if event.type == pygame.JOYBUTTONUP:
            Controller.set_button_up(event.button)
        if event.type == pygame.JOYAXISMOTION:
            print(event)
            Controller.set_axis(event.value)

    if mode == MOUSE_MODE:
        if Controller.is_button_just_down(2):
            mode = DRIVE_MODE
            Mouse.toggle_left(False)
            Mouse.toggle_right(False)
            DriveMode.set_mouse()
        if Controller.is_button_down(0):
            Mouse.move_smooth(-1, 0)
        if Controller.is_button_down(1):
            Mouse.move_smooth(1, 0)
        if Controller.is_button_down(8):
            Mouse.move_smooth(0, 1)
        if Controller.is_button_down(9):
            Mouse.move_smooth(0, -1)
        if Controller.is_button_just_down(4):
            Mouse.toggle_right(True)
        if Controller.is_button_just_up(4):
            Mouse.toggle_right(False)
        if Controller.is_button_just_down(5):
            Mouse.toggle_left(True)
        if Controller.is_button_just_up(5):
            Mouse.toggle_left(False)
    elif mode == DRIVE_MODE:
        if Controller.is_button_just_down(2):
            mode = MOUSE_MODE
        if Controller.get_axis() < -0.3:
            DriveMode.angle -= abs(Controller.get_axis() / 10)
            DriveMode.set_mouse_smooth()
        elif Controller.get_axis() > 0.3:
            DriveMode.angle += abs(Controller.get_axis() / 10)
            DriveMode.set_mouse_smooth()
        if Controller.is_button_down(3):
            Mouse.press_middle()

joystick.quit()
pygame.joystick.quit()
sys.exit()
