#coding=utf-8
from __future__ import unicode_literals, print_function, division
from visual import window, exit, cylinder
from visual.graph import display, vector
import wx

import config

config.w = window(title = 'Модель динамики газа в поршне',
            style = wx.CAPTION | wx.CLOSE_BOX)
config.w.win.ShowFullScreen(True)

width, height = config.w.win.GetSize()
config.w.width = width
config.w.height = height

# To fully redraw window use:
# w.win.DestroyChildren()
# p = w.panel = wx.Panel(w.win, size = w.win.GetSize())

def MenuInterface():
    """Create main menu interface"""
    
    def ModelButton(evt):
        """Go to simulation window"""
        config.menu_switch = 1

    def AuthorsButton(evt):
        """Go to authors window"""
        config.menu_switch = 2

    def TheoryButton(evt):
        """Go to theory window"""
        config.menu_switch = 3

    def ExitButton(evt):
        """Exit program complerely"""
        exit()
    
    # Clear old widgets and scale font
    config.w.win.DestroyChildren()
    p = config.w.panel = wx.Panel(config.w.win, size = config.w.win.GetSize())
    p.SetFont(config.w.win.GetFont().Scaled(3))
    width, height = config.w.win.GetSize()

    config.menu_button_size = (width * 0.182, height * 0.074)
    offset = 10
    # Create new widgets and bind them
    model_button = wx.Button(p, label = 'Модель', size = config.menu_button_size)
    theory_button = wx.Button(p, label ='Теория', size = config.menu_button_size)
    authors_button = wx.Button(p, label = 'Авторы', size = config.menu_button_size)
    exit_button = wx.Button(p, label = 'Выход', size = config.menu_button_size)

    cmc_bmp = wx.Bitmap('cmc.bmp')
    cmc = wx.StaticBitmap(p, -1, cmc_bmp)
    cmc.SetPosition((offset, offset))

    phys_bmp = wx.Bitmap('phys.bmp')
    phys = wx.StaticBitmap(p, -1, phys_bmp)
    phys.SetPosition((width - phys_bmp.GetWidth() - offset, offset))

    year = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL, label='2019')

    main_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL,
                label = 'МГУ им. М.В. Ломоносова\n Компьютерные демонстрации по курсу лекций\n Статистическая физика')
    main_title.Wrap(width - phys_bmp.GetWidth() - cmc_bmp.GetWidth())         

    p.SetFont(p.GetFont().MakeBold())

    sub_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL,
                label = 'Разогрев газа в результате периодического движения поршня')
    sub_title.Wrap(width - phys_bmp.GetWidth() - cmc_bmp.GetWidth())

    model_button.Bind(wx.EVT_BUTTON, ModelButton)
    theory_button.Bind(wx.EVT_BUTTON, TheoryButton)
    authors_button.Bind(wx.EVT_BUTTON, AuthorsButton)
    exit_button.Bind(wx.EVT_BUTTON, ExitButton)

    # Add all widgets to sizer to properly place them in a window
    padding = height + config.w.dheight - main_title.GetSize()[1] - sub_title.GetSize()[1] -\
                4 * config.menu_button_size[1] - year.GetSize()[1] - 5 * offset

    control_box = wx.BoxSizer(wx.VERTICAL)

    #interface layout
    control_box.Add((-1, offset))

    control_box.Add(main_title, flag = wx.ALIGN_CENTER)
    control_box.Add(sub_title, flag = wx.ALIGN_CENTER)

    control_box.Add((-1, padding / 2)) # add some padding

    control_box.Add(model_button, flag = wx.ALIGN_CENTER)
    control_box.Add(theory_button, flag = wx.ALIGN_CENTER)
    control_box.Add(authors_button, flag = wx.ALIGN_CENTER)
    control_box.Add(exit_button, flag = wx.ALIGN_CENTER)

    control_box.Add((-1, padding / 2))

    control_box.Add(year, flag = wx.ALIGN_CENTER)

    p.SetSizer(control_box)
    p.Layout()

def AuthorsInterface():
    pass

def TheoryInterface():
    pass

def ModelInterface():
    """Create interface for model showcase"""

    # Declare functions to bind with widgets later
    def SetMode(evt):
        config.piston_mode = piston_mode_choice.GetSelection()

    def SetAmp(evt):
        """Set default amplitude of a piston"""
        #todo
        config.ampl = amp_slider.GetValue()

    def SetPeriod(evt):
        """Set default period of a piston"""
        config.period = 10*per_slider.GetValue()
        
    def SetNum(evt):
        """Set default number of atoms"""
        config.Natoms = number_spinctrl.GetValue()

    def SetMass(evt):
        """Set default mass of an atom"""
        config.mass = mass_slider.GetValue() * 1e-3 / 6e23

    def SetAtomRadius(evt):
        """Set default radius of an atom"""
        config.Ratom = ratom_slider.GetValue() / 100

    def SetTemp(evt):
        """Set default temperature"""
        config.T = temp_slider.GetValue()

    def PressStart(evt):
        """Start and stop the simulation"""
        if config.start == 0:
            config.start = 1
        elif config.pause == 0:
            config.pause = 1
        else:
            config.pause = 0

    def ClearButton(evt):
        """Clear screen to completely restart simulation"""
        config.pause = 0
        config.start = 0

    def BackToMenu(evt):
        """Switch back to the main menu"""
        config.pause = 0
        config.start = 0
        config.menu_switch = 0
    
    def ExitButton(evt):
        """Exit program completely"""
        exit()

    # Clear old widgets and scale font
    config.w.win.DestroyChildren()
    p = config.w.panel = wx.Panel(config.w.win, size = config.w.win.GetSize())
    p.SetFont(config.w.win.GetFont().Scaled(2))
    width, height = config.w.win.GetSize()

    config.button_size = (width * 0.14, height * 0.046)
    config.slider_size = (width * 0.14, height * 0.046)

    # Create new widgets and bind them
    piston_mode_text = wx.StaticText(p, label = 'Движение поршня:')
    per_text = wx.StaticText(p, label = 'Период:')
    amp_text = wx.StaticText(p, label = 'Амплитуда:')
    number_text = wx.StaticText(p, label = 'Число атомов:')
    mass_text = wx.StaticText(p, label = 'Масса атома:')
    ratom_text = wx.StaticText(p, label = 'Размер атома:')
    temp_text = wx.StaticText(p, label = 'Температура:')

    piston_mode_choice = wx.Choice(p, choices = ['Нет', 'sin', 'равномерно', 'быстро вниз', 'быстро вверх'], size = config.button_size)
    piston_mode_choice.SetSelection(0)

    number_spinctrl = wx.SpinCtrl(p, size = config.button_size,
                min = 1, max = 100, initial = 10)
    
    per_slider = wx.Slider(p, size = config.slider_size,
                minValue = 3, maxValue = 20, value = 10)
    amp_slider = wx.Slider(p, size = config.slider_size,
                minValue = 5, maxValue = 20, value = 10)
    mass_slider = wx.Slider(p, size = config.slider_size,
                minValue = 1, maxValue = 20, value = 4)
    ratom_slider = wx.Slider(p, size = config.slider_size,
                minValue = 1, maxValue = 10, value = 6)
    temp_slider = wx.Slider(p, size = config.slider_size,
                minValue = 100, maxValue = 1000, value = 300)
    
    start_button = wx.Button(p, label = 'Старт / Пауза', size = config.button_size)
    back_button = wx.Button(p, label = 'Меню', size = config.button_size)
    exit_button = wx.Button(p, label = 'Выход', size = config.button_size)
    clear_button = wx.Button(p, label = 'Сброс', size = config.button_size)

    piston_mode_choice.Bind(wx.EVT_CHOICE, SetMode)
    per_slider.Bind(wx.EVT_SCROLL, SetPeriod)
    amp_slider.Bind(wx.EVT_SCROLL, SetAmp)
    number_spinctrl.Bind(wx.EVT_SPINCTRL, SetNum)
    mass_slider.Bind(wx.EVT_SCROLL, SetMass)
    ratom_slider.Bind(wx.EVT_SCROLL, SetAtomRadius)
    temp_slider.Bind(wx.EVT_SCROLL, SetTemp)
    start_button.Bind(wx.EVT_BUTTON, PressStart)
    clear_button.Bind(wx.EVT_BUTTON, ClearButton)
    exit_button.Bind(wx.EVT_BUTTON, ExitButton)
    back_button.Bind(wx.EVT_BUTTON, BackToMenu)

    # Add all widgets to sizer to properly place them in a window
    h_offset = (width / 3 - 100 - config.button_size[0]) / 2
    v_offset = config.w.dheight
    control_box = wx.BoxSizer(wx.VERTICAL)

    control_box.Add((-1, v_offset))
    control_box.Add(piston_mode_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(piston_mode_choice, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(per_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(per_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(amp_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(amp_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    
    control_box.Add(number_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(number_spinctrl, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(mass_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(mass_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(ratom_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(ratom_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(temp_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(temp_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(start_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(clear_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)


    pad = height - 7 * temp_text.GetSize()[1] -\
        5 * temp_slider.GetSize()[1] - number_spinctrl.GetSize()[1] -\
        piston_mode_choice.GetSize()[1] - 4 * start_button.GetSize()[1] - 2 * v_offset
    
    control_box.Add((-1, pad))

    control_box.Add(back_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(exit_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    p.SetSizer(control_box)
    p.Layout()

if __name__ == "__main__":
    import model
    from visual import sleep
    ModelInterface()
    while True:
        if config.start:
            model.Simulation()
        sleep(0.1)
