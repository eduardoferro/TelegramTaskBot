from telegram.ext import Updater, CommandHandler

idconv = 0
conversaciones = {}

#Codigos de Salida
OK = 0
ERROR = 1
#Estados de Tareas
TODO = 0
DOING = 1
DONE = 2

members = ""

class task():
    def __init__(self,nombre):
        self.members= []
        self.nombre=nombre
        self.estado= TODO
        self.date=0
    def toString(self):
        return "["+ParseStateToStr(self.estado)+"] "+self.nombre+" "

class conversacion ():
    def __init__(self):
        self.tareas=[]    
    def addTask(self,nombre):
        self.tareas.append(task(nombre))
    def getStateTasks(self,state):
        i = 0 
        output="\n"
        for tarea in self.tareas :
            if tarea.estado==state:
                output += "("+str(i)+") "+tarea.toString()+"\n"
            i+=1
        return output
    def toString(self):
        i = 0 
        output="Tasks:\n"
        for tarea in self.tareas :
            output += "("+str(i)+") "+tarea.toString()+"\n"
            i+=1
        return output
    def removeTask(self,i):
        if i < len(self.tareas):
            del self.tareas[i]
            return OK
        else:
            return ERROR

def ParseState(cadena):
    if cadena=="TODO" or cadena=="Todo" or cadena=="todo":
        return TODO
    if cadena=="DOING" or cadena=="Doing" or cadena=="doing":
        return DOING
    if cadena=="DONE" or cadena=="Done" or cadena=="done":
        return DONE
    return TODO

def ParseStateToStr(estado):
    if estado == TODO:
        return "x" #"TODO"
    if estado == DOING:
        return "~" #DOING"
    if estado == DONE:
        return "√" #DONE"
    

def newProject(bot, update):
    global idconv
    global conversaciones
    # idconv += 1
    conversaciones[str(update.message.chat.id)]=(conversacion())
    update.message.reply_text(
        'HEY Creado proyecto, id:{}'.format( str(update.message.chat.id)  ))

def getTasks(bot,update):
    global conversaciones
    if str(update.message.chat.id) not in conversaciones:
        conversaciones[str(update.message.chat.id)]=(conversacion())
    # print(conversaciones[str(update.message.chat.id)].tareas[0].nombre )
    update.message.reply_text(
        'HEY Tareas, {}'.format(  conversaciones[str(update.message.chat.id)].toString()  ))
        # 'HEY Tareas, {}'.format( str(conversaciones[int(update.message.getText())])  ))

def getTodoTasks(bot,update):
    global conversaciones
    if str(update.message.chat.id) not in conversaciones:
        conversaciones[str(update.message.chat.id)]=(conversacion())
    update.message.reply_text(
        'HEY Tareas TODO, {}'.format(  conversaciones[str(update.message.chat.id)].getStateTasks(TODO)  ))

def getDoingTasks(bot,update):
    global conversaciones
    if str(update.message.chat.id) not in conversaciones:
        conversaciones[str(update.message.chat.id)]=(conversacion())
    update.message.reply_text(
        'HEY Tareas DOING, {}'.format(  conversaciones[str(update.message.chat.id)].getStateTasks(DOING)  ))

def getDoneTasks(bot,update):
    global conversaciones
    if str(update.message.chat.id) not in conversaciones:
        conversaciones[str(update.message.chat.id)]=(conversacion())
    update.message.reply_text(
        'HEY Tareas DONE, {}'.format(  conversaciones[str(update.message.chat.id)].getStateTasks(DONE)  ))


def SetTaskState(bot,update):
    global conversaciones
    if str(update.message.chat.id) not in conversaciones:
        conversaciones[str(update.message.chat.id)]=(conversacion())
    # print("id: "+str(int(update.message.text.replace("/setTaskState","").split(";")[0])))
    # print("estado: "+ParseStateToStr(ParseState(update.message.text.replace("/setTaskState","").split(";")[1])))
    conversaciones[str(update.message.chat.id)].tareas[
        int(update.message.text.replace("/setTaskState","").split(";")[0])
        ].estado=ParseState(update.message.text.replace("/setTaskState","").split(";")[1])
    update.message.reply_text(
        'HEY Tarea set , {}'.format(  conversaciones[str(update.message.chat.id)].tareas[ int(update.message.text.replace("/setTaskState","").split(";")[0])].toString() ))

def addTask(bot,update):
    global conversaciones
    if str(update.message.chat.id) not in conversaciones:
        conversaciones[str(update.message.chat.id)]=(conversacion())
    cadena = update.message.text.replace("/addTask"," ")
    if cadena == "":
        update.message.reply_text(
            'ERROR: tarea vacia {}'.format( "" ))
        return 
    conversaciones[str(update.message.chat.id)].addTask(cadena)
    # print(conversaciones[str(update.message.chat.id)].tareas[0].nombre)
    update.message.reply_text(
        'Añadida tarea:\n {}'.format( conversaciones[str(update.message.chat.id)].tareas[len(conversaciones[str(update.message.chat.id)].tareas)-1].toString()))
def removeTask(bot,update):
    global conversaciones
    if str(update.message.chat.id) not in conversaciones:
        conversaciones[str(update.message.chat.id)]=(conversacion())
    print(int(update.message.text.replace("/removeTask","")))
    if conversaciones[str(update.message.chat.id)].removeTask(int(update.message.text.replace("/removeTask","")))==OK:
         update.message.reply_text(
        'HEY  tarea, {}'.format("Eliminada correctamente"))
    else:
        update.message.reply_text(
        'ERROR:  {}'.format("Indice no valido"))
def start(bot,update):
    update.message.reply_text(
        'Instrucciones,\n {}'.format( 
           # "/newProject : \n    Crea un nuevo proyecto\n "+
            "/getTasks : \n    Muestra TODAS las tareas \n"+
            "/getTodoTask /getDoingTask /getDoneTask : \n    Muestra las tareas en esos estados \n"+
            "/setTaskState <id>;<Doing/Done/Todo> : \n    Cambia el estado de una tarea con el id \n"+
            "/addTask <Nombre> : \n    Añade una tarea al proyecto \n"+
            "/removeTask <id> : \n    Elimina una tarea del proyecto"))
# def set_members(bot, update):
#     global members 
#     update.message.reply_text(
#         'Miembros actuales:')
#     print (update.message.text)
    
#     members =  update.message.text.replace("/set_members"," ")

updater = Updater('KEY')


#updater.dispatcher.add_handler(CommandHandler('newProject', newProject))
updater.dispatcher.add_handler(CommandHandler('getTasks', getTasks))
updater.dispatcher.add_handler(CommandHandler('getTodoTasks', getTodoTasks))
updater.dispatcher.add_handler(CommandHandler('getDoingTasks', getDoingTasks))
updater.dispatcher.add_handler(CommandHandler('getDoneTasks', getDoneTasks))
updater.dispatcher.add_handler(CommandHandler('setTaskState', SetTaskState))
updater.dispatcher.add_handler(CommandHandler('addTask', addTask))
updater.dispatcher.add_handler(CommandHandler('removeTask', removeTask))
updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('set_members', set_members))

updater.start_polling()
updater.idle()


# test 
# /newProject
# /addTask aaa
# /addTask aaab
# /getTasks
# /removeTask 0
