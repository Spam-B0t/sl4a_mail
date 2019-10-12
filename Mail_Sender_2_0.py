import smtplib, os, shelve, androidhelper
#from mfuncs import *
droid = androidhelper.Android()
#FuncBegin-------------------------------------------------------
def toSend(receivers, message, set_arr):
    sender = set_arr[0]

    try:
        server = smtplib.SMTP_SSL(set_arr[1], int(set_arr[2]))
        server.login(set_arr[3], set_arr[4])
        server.sendmail(sender, receivers, message)
        print("Successfully sent email")
        server.quit()

    except smtplib.SMTPException:
        print("ERROR")
    
    

def Menu_list(a, title):
    droid.dialogCreateAlert(title)
    droid.dialogSetItems(a)
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    try:
        return response['item']
    except KeyError:
        return Menu_list(a, title)
 
    
def usr_input(a, a_data, inp):  
    if a[inp] == 'mailbox password':
        enter = droid.dialogGetPassword('Type in '+ a[inp]).result
    else:   
        enter = droid.dialogGetInput(a[inp]+': '+a_data[inp]).result
    if enter!='' and type(enter)==type(""):
        a_data[inp]=enter
        result = droid.makeToast(a[inp]+' was updated!')
        return result.error is None  
#FuncEnd---------------------------------------------------------   
#Var
menu=['sender settings', 'receivers', 'message', 'save', 'load', 'SEND', 'Exit']
sender_settings=['sender mailbox', 'server', 'port', 'mailbox login', 'mailbox password', 'return to menu']
sender_settings_values=[' ', ' ', ' ', ' ', ' ']
receivers=[]
message=''

#main menu
menuz=True
while menuz:
    res=Menu_list(menu, 'Main Menu')
#-----------------------------
    if menu[res]=='sender settings':
        setn=True
        while setn:            
            res_2=Menu_list(sender_settings, 'Sender Settings') 
            if res_2!=len(sender_settings)-1:
                usr_input(sender_settings, sender_settings_values, res_2)
            else:
                setn=False
#----------------------------
    if menu[res]=='receivers':
        s=droid.dialogGetInput('Enter a path to a file containing receivers or just list them divided by space').result
        if os.path.isdir(s):
            receivers=open(s).split()
        else:
            receivers=s.split()
#-------------------------
    if menu[res]=='message':
        s=droid.dialogGetInput('Enter a path to a message or just type it in').result
        if os.path.isdir(s):
            message=open(s)
        else:
            message=s
#-------------------------
    if menu[res]=='save':
        #DataFile=shelve.open('./MSettings')
        try:
            DataFile=shelve.open('storage/emulated/0/Mail-Sender/MSettings')
        except IOError:
            DataFile = shelve.open(droid.dialogGetInput('Couldnt find setup file, enter a path').result)
        for i in range(len(sender_settings_values)):
            DataFile[sender_settings[i]]=sender_settings_values[i]
        droid.makeToast('SETTINGS SAVED!!!')
        DataFile.close()
#-------------------------
    if menu[res]=='load':
        try:
            DataFile=shelve.open('storage/emulated/0/Mail-Sender/MSettings')
        except IOError:
            DataFile = droid.dialogGetInput('Couldnt find setup file, enter a path').result
        for i in range(len(sender_settings_values)):
            sender_settings_values[i]=DataFile[sender_settings[i]]
        droid.makeToast('SETTINGS LOADED!!!')
        DataFile.close()
#------------------------- 
    if menu[res]=='SEND':
        toSend(receivers, message, sender_settings_values)
#-------------------------
    if menu[res]=='Exit':
        menuz=False