from Libraries import *



meipass = sys._MEIPASS
#meipass = "C:\\Users\\LoCo\\Desktop\\DNS Changer\\"
drive_ = os.environ['USERPROFILE'][0]+":\\"
_data_ = drive_+'Windows\\'
#_data_ = ''
inf = []

if not os.path.exists(_data_+'DNS_LIST.dll'):
    file = open(_data_+'DNS_LIST.dll', 'w')
    file.write('403<dns>10.202.10.202<dns>10.202.10.102\nShekan<dns>178.22.122.100<dns>185.51.200.2\n')
    inf.append('403<dns>10.202.10.202<dns>10.202.10.102')
    inf.append('Shekan<dns>178.22.122.100<dns>185.51.200.2')
    file.close()
else:
    file = open(_data_+'DNS_LIST.dll', 'r')
    inf = file.readlines()
    file.close()
    for i in range(len(inf)): inf[i] = inf[i].strip('\n') 


def get_info():
    servers = []
    cmd = subprocess.getstatusoutput('ipconfig /all')[1].split('\n')
    for i in range(len(cmd)):
        if 'DNS Servers' in cmd[i]:
            servers.append(cmd[i].split(':')[1].strip('\n').strip(' '))
            if '                    ' in cmd[i+1]: servers.append(cmd[i+1].strip('\n').strip(' '))
            else: servers.append('')
    if len(servers)==0: 
        servers.append('')
        servers.append('')
    return servers

def del_dns(page, rg):
    for i in range(len(rg.content.controls)):
        try:
            if rg.content.controls[i].value == rg.value:
                for j in range(len(inf)):
                    try:
                        if inf[j].split('<dns>')[0] == rg.value:
                            inf.pop(j)
                    except: pass
                        
                rg.content.controls.pop(i)
        except : pass
    file = open(_data_+'DNS_LIST.dll', 'w')
    for i in inf:
        file.write(i+'\n')
    file.close()
    page.update()
    
def add_dns(page, rg):
    def dns_adder(popup):
        file = open(_data_+'DNS_LIST.dll', 'a')
        file.write(f'{name_tf.value}<dns>{primary_tf.value}<dns>{secondary_tf.value}\n')
        file.close()
        inf.append(f'{name_tf.value}<dns>{primary_tf.value}<dns>{secondary_tf.value}')
        rg.content.controls.append(ft.Radio(name_tf.value, value=name_tf.value))
        page.update()
        page.close(popup)
        
    secondary_tf = ft.TextField(label='Secondary')
    primary_tf = ft.TextField(label='Primary', on_submit=lambda _:secondary_tf.focus())
    name_tf = ft.TextField(label='Name', on_submit=lambda _:primary_tf.focus())

    add_popup = ft.AlertDialog(title=ft.Text('Add DNS Server', text_align=ft.TextAlign.CENTER), content=name_tf, actions=[primary_tf, secondary_tf])
    add_popup.actions.append(ft.TextButton('Ok', width=70, height=40, on_click=lambda _: dns_adder(add_popup)))
    secondary_tf.on_submit = lambda _: dns_adder(add_popup)

    page.open(add_popup)
    name_tf.focus()
    page.update()
    
def set_dns(page, primary_tf, secondary_tf, current_tf):    
    if primary_tf.value!='' or secondary_tf.value!='':
        subprocess.getstatusoutput(f'wmic nicconfig where (IPEnabled=TRUE) call SetDNSServerSearchOrder ("{primary_tf.value}", "{secondary_tf.value}")')

    info = get_info()
    
    if current_tf.value == info[0] + '   ' + info[1]:
        page.bgcolor = ft.colors.RED_700
        page.update()
        sleep(0.2)
        page.bgcolor = None
    else:
        page.bgcolor = ft.colors.GREEN_600
        page.update()
        sleep(0.2)
        page.bgcolor = None
        
    current_tf.value = info[0] + '   ' + info[1]
    page.update()
        
def clear_dns(page, current_tf):
    subprocess.getstatusoutput(f'wmic nicconfig where (IPEnabled=TRUE) call SetDNSServerSearchOrder ()')
    subprocess.getstatusoutput('ipconfig /flushdns')
    
    info = get_info()

    if current_tf.value == info[0] + '   ' + info[1]:
        page.bgcolor = ft.colors.RED_700
        page.update()
        sleep(0.2)
        page.bgcolor = None
    else:
        page.bgcolor = ft.colors.GREEN_600
        page.update()
        sleep(0.2)
        page.bgcolor = None
        
    current_tf.value = info[0] + '   ' + info[1]
    page.update()
    
def change_radio(page, radio, primary_tf, secondary_tf):
    for i in inf:
        if i.split('<dns>')[0] == radio:
            primary_tf.value = i.split('<dns>')[1]
            secondary_tf.value = i.split('<dns>')[2]
    page.update()
    
def fill_radio(page, rg):
    for i in inf:
        rg.append(ft.Radio(i.split('<dns>')[0], value=i.split('<dns>')[0]))
    page.update()
    
def path_func(e):
    if e.data=='true':
        try:
            shutil.copy(sys.argv[0], _data_)
            os.rename(_data_+sys.argv[0].split('\\')[-1], _data_+'DNS.exe')
        except: pass
    else:
        try: os.remove(_data_+'DNS.exe')
        except: pass