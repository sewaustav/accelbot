from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
buttons = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = "/OK"), KeyboardButton(text = "/OK")],
], resize_keyboard = True)

ok = KeyboardButton("/OK")
button = ReplyKeyboardMarkup(resize_keyboard=True).add(ok)

foot = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Left"), KeyboardButton(text="Right")], ], resize_keyboard=True)

contract = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")], ], resize_keyboard=True)

contact = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="ВСЁ"), KeyboardButton(text="Начать заново")], ], resize_keyboard=True)

finish = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Завершить"), KeyboardButton(text="Начать заново")], ], resize_keyboard=True)


lw = KeyboardButton("LW")
st = KeyboardButton("ST")
rw = KeyboardButton("RW")
ss = KeyboardButton("SS")
cam = KeyboardButton("CAM")
cm = KeyboardButton("CM")
cdm = KeyboardButton("CDM")
lb = KeyboardButton("LB")
lcb = KeyboardButton("LCB")
rcb = KeyboardButton("RCB")
rb = KeyboardButton("RB")
gk = KeyboardButton("GK")

position = ReplyKeyboardMarkup(resize_keyboard=True).row(lw, st, rw).row(cam, cdm, cm).row(lb, lcb, rcb, rb).add(gk)
