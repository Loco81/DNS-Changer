from Classes import *



def main(page: ft.Page):
    page.title = 'DNS Changer'
    page.window.width, page.window.height = 650, 450
    page.window.min_width, page.window.min_height  = 650, 450
    page.window.opacity = 0.95
    #page.window.frameless = True
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window.center()
    path_cb = ft.Checkbox('Add to windows path', width=180, tooltip='Enter "DNS" command in Run window', active_color=ft.colors.GREEN_800, on_change=path_func)
    path_cb.rtl = True
    if os.path.exists(drive_+'Windows\\DNS.exe'): path_cb.value = True
    else: path_cb.value = False
    if sys.argv[0].upper() == drive_+'Windows\\DNS.exe'.upper() : path_cb.disabled = True
    page.appbar = ft.AppBar(
                    title = ft.Text("DNS Changer"),
                    bgcolor = ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
                    center_title = True,
                    actions=[path_cb]
                )
    page.window.icon = meipass+"\\Icon.ico"
    set_btn = ft.ElevatedButton('Set DNS', color=ft.colors.GREEN)
    clear_btn = ft.ElevatedButton('Clear DNS', color=ft.colors.RED)
    secondary_tf = ft.TextField(label='Secondary')
    primary_tf = ft.TextField(label='Primary', on_submit=lambda _: secondary_tf.focus())

    col_l = ft.Column(
            [
                primary_tf,
                secondary_tf,
                ft.Row([set_btn, clear_btn], rtl=True, width=300)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
            height = 160
        )

    add_rem_line = ft.Row([])
    rg = ft.RadioGroup(content=ft.Column([]))
    fill_radio(page, rg.content.controls)
    rg.on_change = lambda _:change_radio(page, rg.value, primary_tf, secondary_tf)
  
    col_r = ft.Column(
            [
                rg,
                add_rem_line
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
            rtl = True,
            width=300,
            scroll=ft.ScrollMode.ALWAYS
        )
    add_rem_line.controls.append(ft.FloatingActionButton(icon=ft.icons.ADD, width=40, height=30, on_click=lambda _: add_dns(page, rg)))
    add_rem_line.controls.append(ft.FloatingActionButton(icon=ft.icons.REMOVE, width=40, height=30, on_click=lambda _: del_dns(page, rg)))

    row1 = ft.Row(
            [
                col_l,
                col_r
            ],
            expand=True
            #alignment = ft.MainAxisAlignment.CENTER,
            #width=page.window_width
        )
    
    info = get_info()
    info_txt = ft.Row([ft.Text('Current System DNS:   ', color=ft.colors.GREY_700), ft.Text(info[0]+'   '+info[1] , color=ft.colors.AMBER_600)], alignment=ft.MainAxisAlignment.CENTER)
    main_col = ft.Column([row1, ft.Divider(), info_txt, ft.Text(height=130),ft.Row([ft.Text('Powered by LoCo', color=ft.colors.GREY_700)], alignment=ft.MainAxisAlignment.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True)
    secondary_tf.on_submit = lambda _: set_dns(page, primary_tf, secondary_tf, info_txt.controls[1])
    set_btn.on_click = lambda _: set_dns(page, primary_tf, secondary_tf, info_txt.controls[1])
    clear_btn.on_click = lambda _: clear_dns(page, info_txt.controls[1])
    


    page.add(ft.Container(content=ft.WindowDragArea(main_col), expand=True))
    page.update()


ft.app(main)