import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import pyautogui
import os
import pyautogui
import json
from tkinter import messagebox
print("py")
def startYoutube(query):
    query = query.replace(' ', '+')
    os.system("start C:\\Users\\js314\\Desktop\\chrome https://www.youtube.com/results?search_query=" + query)
    # Move the mouse to the search bar
    pyautogui.sleep(2)
    pyautogui.moveTo(658, 420)
    # Click the search bar
    pyautogui.click()

def processFunction(name, args):
    print(f"Function name: {name}")
    print(f"Function arguments: {args}")
    args = json.loads(args)
    prompt = args.get("prompt")
    if name == "Play":
        startYoutube(prompt)
    else:
        print("Function not found")
scr = pyautogui.screenshot()
scr.save('scr.png')
import base64

def Tobase(path):
    with open(path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"

def center_window():
    # Update the root window to get the latest size
    root.update_idletasks()
    
    # Calculate the position to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = (screen_width - size[0]) // 2
    y = (screen_height - size[1]) // 2
    
    # Set the window's position
    root.geometry(f"+{x}+{y}")

root = tk.Tk()
root.title("GPT 4 omni")
root.geometry('980x60')
h=60
root.overrideredirect(True)

def increase_height(event):
    global h, inp
    lines = inp.get("1.0", "end").count('\n')
    root.geometry(f"980x{lines*20+60}")
    inp.config(height=lines)

def adjust_height(event):
    # Calculate the number of lines in the text widget after the key press event
    lines = inp.get("1.0", "end").count('\n')
    # Adjust the height of the text widget to match the number of lines (or minimum of 1)
    inp.config(height=max(2, lines))
    root.geometry(f"980x{lines*20+60}")

def on_backspace(event):
    # Get the current cursor position
    cursor_pos = inp.index(tk.INSERT)
    if cursor_pos == "1.0":
        # Prevent deletion if it's the first character
        return "break"
    # Allow the event to proceed, deletion occurs
    return

use = False
def OnImageClick():
    global use, imfimg, imfimg2
    if not use:
        use = True
    else:
        use = False
    root.update()

inp = tk.Text(root, width=5, height=2, font = ('Arial', 20))
inp.place(x=0, y=0, width=800)
inp.bind("<BackSpace>", on_backspace)
inp.bind("<Key>", adjust_height)

def get_text():
    raw_text = inp.get("1.0", "end-1c")
    return raw_text

from openai import OpenAI
client = OpenAI(api_key='sk-...')

answer = ""

def Respond():
    global answer
    txt = get_text()
    response=0
    print(f"use : {use}")
    if not use:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "Answer as short and concise as possible. Respond in Korean."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type":"text",
                            "text":txt
                        }
                    ]
                }
            ],
            temperature=1,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            tools=[
                {
                "type": "function",
                "function": {
                    "name": "Play",
                    "description": "Start a video or music that is most relevant with the prompt",
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                        "type": "string",
                        "description": "The prompt. Determines what video or music should be."
                        },
                        "type": {
                        "type": "string",
                        "enum": [
                            "music",
                            "video"
                        ]
                        }
                    },
                    "required": [
                        "prompt",
                        "type"
                    ]
                    }
                }
                }
            ]
        )
    else:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "Answer as short and concise as possible. Respond in Korean."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type":"image_url",
                            "image_url": {
                                "url":Tobase('scr.png')
                            }
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type":"text",
                            "text":txt
                        }
                    ]
                }
            ],
            temperature=1,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            tools=[
                    {
                    "type": "function",
                    "function": {
                        "name": "Play",
                        "description": "Start a video or music that is most relevant with the prompt",
                        "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                            "type": "string",
                            "description": "The prompt. Determines what video or music should be."
                            },
                            "type": {
                            "type": "string",
                            "enum": [
                                "music",
                                "video"
                            ]
                            }
                        },
                        "required": [
                            "prompt",
                            "type"
                        ]
                        }
                    }
                    }
                ]
        ) 
    print(response)
    print(dict(dict(dict(response)['choices'][0])['message'])['content'])
    answer = dict(dict(dict(response)['choices'][0])['message'])['content']
    functionName = None
    functionArgs = None
    if dict(dict(dict(dict(response)['choices'][0]))['message'])['tool_calls'] is not None:
        print(dict(dict(dict(dict(dict(response)['choices'][0]))['message'])['tool_calls'][0])['function'])
        functionName = dict(dict(dict(dict(dict(dict(response)['choices'][0]))['message'])['tool_calls'][0])['function'])['name']
        functionArgs = dict(dict(dict(dict(dict(dict(response)['choices'][0]))['message'])['tool_calls'][0])['function'])['arguments']
        print(f"Function name: {functionName}")
        print(f"Function arguments: {functionArgs}")
        processFunction(functionName, functionArgs)
        exit(0)
    print(f"Function name: {functionName}")
    print(f"Function arguments: {functionArgs}")
    root.destroy()


oimage = Image.open('search.png')
image = oimage.resize((50, 50))
img = ImageTk.PhotoImage(image)
oximage = Image.open('x.png')
ximage = oximage.resize((50, 50))
ximg = ImageTk.PhotoImage(ximage)
searchButton = tk.Button(root, image=img, bg = 'white', command=Respond)
searchButton.image = img
searchButton.place(x=860, y=0, width=60, height=60)
oimimg = Image.open('imgic.png')
iming = oimimg.resize((50, 50))
imfimg = ImageTk.PhotoImage(iming)
xButton = tk.Button(root, image = ximg, bg = 'white', command= lambda:exit(0))
xButton.image = ximg
xButton.place(x=920, y=0, width=60, height=60)
iButton = tk.Button(root, image = imfimg, bg = 'white', command=OnImageClick)
iButton.image = imfimg
iButton.place(x=800, y=0, width=60, height=60)

center_window()
root.mainloop()

Result = tk.Tk()
Result.title("AI answer")
size = 0
if len(answer)<15:
    size = 30
elif len(answer)<30:
    size = 20
else:
    size = 15
ResultText = tk.Label(text = answer.replace('. ','.\n'), font = ('Arial', size)).pack()
Okay = tk.Button(text="Got it", fg='green', command=lambda:exit(0), font=('Arial', 20)).pack()
# Update the root window to get the latest size
Result.update_idletasks()

# Calculate the position to center the window
screen_width = Result.winfo_screenwidth()
screen_height = Result.winfo_screenheight()
size = tuple(int(_) for _ in Result.geometry().split('+')[0].split('x'))
x = (screen_width - size[0]) // 2
y = (screen_height - size[1]) // 2

# Set the window's position
Result.geometry(f"+{x}+{y}")
Result.overrideredirect(True)
Result.mainloop()