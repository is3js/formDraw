#!pip install ipycanvas # 처음이면 설치할 것

# 코랩 노트북 폴더(Colab Notebooks)에 draw.py 및 images 폴더가 있을 것 있을 것

import os

import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display

from ipywidgets import Image
from ipywidgets import ColorPicker, IntSlider, link, AppLayout, HBox
from ipycanvas import MultiCanvas, hold_canvas
import platform 


##################=========================select======================
def f_부위_to_file_path_list( 부위 ):
    idx_ = folders.index(부위)
    folder_files = [ (부위, file, os.path.join(path, file)) for path, dir_, files in os.walk(f"./images/{부위}") for file in files ]
    return folder_files

##################################  widget
w_draw_label = widgets.Label('그림선택 : ')

# 폴더명 
if  platform.system()=='Windows':
    folders = list(set([ os.path.join(path, file).split("\\")[-2] for (path, dir_, files) in os.walk("./images") for file in files]))
else:
    folders = list(set([ os.path.join(path, file).split("/")[-2] for (path, dir_, files) in os.walk("./images") for file in files]))

w_draw_folder_select = widgets.Select(options=sorted(folders),
                                layout=Layout(width='250px'),
                                  description='폴더명'
                                )# 1. 딕셔너리 키값들을 select에 옵션으로 주어 select위젯 객체 만들기
v_folder = w_draw_folder_select.value# 2. select객체의 선택된 value를 받아, 2번재 select로 데려갈 준비를 한다. /  각종 부위 필요할 때 쓰인다.

# 파일명 dict
# file_dict [ 파일명 ] = 경로
file_dict = { file:path for folder, file, path in f_부위_to_file_path_list(v_folder)}

    
w_draw_file_select = widgets.Select(options=file_dict.keys(),
                                  description = '파일'
                                ) # 3. 선택된key로 받은 list값으로 새로운 select 위젯에 option으로 준다.

##################################  functions
def f_select_폴더_to_파일(폴더):
    global file_dict 
    file_dict = { file:path for folder, file, path in f_부위_to_file_path_list(폴더)}
    w_draw_file_select.options = file_dict.keys()
    



ui_draw_1 = widgets.interactive(f_select_폴더_to_파일, 폴더=w_draw_folder_select, layout=Layout(width='40%'))


percent = 1
width = f'{int(768*percent)}'
height = f'{int(918*percent)}'

canvas = MultiCanvas(3, width=width, height=height)

background_layer = canvas[0]
drawing_layer = canvas[1]
interaction_layer = canvas[2]

drawing = False
start = None

def on_mouse_down(x, y):
    global drawing
    global start

    if not drawing:
        start = (x, y)
    else:
        with hold_canvas(canvas):
            drawing_layer.stroke_line(start[0], start[1], x, y)
            interaction_layer.clear()
        start = None
    drawing = not drawing

def on_mouse_move(x, y):
    if not drawing:
        return
    with hold_canvas(canvas):
        interaction_layer.clear()
        interaction_layer.stroke_line(start[0], start[1], x, y)
        
interaction_layer.on_mouse_down(on_mouse_down)
interaction_layer.on_mouse_move(on_mouse_move)

drawing_layer.stroke_style = '#749cb8'
drawing_layer.line_width = 6
interaction_layer.stroke_style = '#749cb8'
interaction_layer.line_width = 6

picker = ColorPicker(description='Color:', value='#ff0000')
slider = IntSlider(description='Line width:', value=6, min=1, max=20)

link((picker, 'value'), (drawing_layer, 'stroke_style'))
link((picker, 'value'), (interaction_layer, 'stroke_style'))
link((slider, 'value'), (drawing_layer, 'line_width'))
link((slider, 'value'), (interaction_layer, 'line_width'))


def f_select_파일_to_canvas(파일):
    canvas.clear()
    
    file_path = file_dict[파일]
    global image
    image = Image.from_file(file_path)
    
    background_layer.draw_image(image, 0, 0, width, height)
        

ui_draw_2 = widgets.interactive(f_select_파일_to_canvas, 파일=w_draw_file_select, layout=Layout(width='40%')) 

ui_draw = widgets.VBox([widgets.HBox([ w_draw_label, ui_draw_1, ui_draw_2]),
                        widgets.HBox((picker, slider)),
                        canvas])

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

#=========================title======================
ui_title = widgets.HTML("<p/><center><h3>----------------------------------------</h3></center><p/><center><H2>JS's Drawing Note in CY</H2><center><p/><center><h3>----------------------------------------</h3></center><p/>")


def draw():
    canvas.clear()
    display(ui_title, ui_draw)