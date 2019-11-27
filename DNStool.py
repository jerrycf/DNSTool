#///LIBRARIES

#///VARIABLES GLOBALES
#Sustituir origin por el path de /etc/bind para ubuntu
origin = 'C:\\Users\\Superman\\Documents\\ESCOM\\9no\\ASR'
sitesPath = origin + '\\named.conf.local'

#///FUNCTIONS
# Funcion para agregar un nuevo sitio.
def addSite(siteName):
    try:
        fileSites = open(sitesPath, 'at')
        #Arreglar la forma de agregar un sitio en esta parte.
        zone = '''zone \"''' + siteName + '''.net\" {
    type master;
    file \"ruta del archivo\";
};\n\n'''
        print(zone)
        fileSites.write(zone)
        print('Sitio agregado correctamente.')
        fileSites.close()
    except:
        print('Ah ocurrido un error, intentelo más tarde.')
#Funcion que devuelve la base de un archivo db.xxxx basado en un siteName
def createDB(siteName):
    #filedbPath = open(dbpath, 'wt')
    db = '''$TTL \t 604800
@               IN          SOA     ''' + siteName + '''.net. root.''' + siteName + '''.net. (
                                2                   ; Serial
                                604800              ; Refresh
                                86400               ; Retry
                                2419200             ; Expire
                                604800  )           ; Negative Cache TTL
;
@               IN          NS      ''' +siteName + '''.net.
'''
    return(db)

#Funciones para agregar servicios al nuevo sitio
def addToSite(siteName):
    print('Agregando servicio HTTP a ', siteName)
    dbPath = origin + '\\db.' + siteName
    db = createDB(siteName)
    dns = input('Ingrese un nombre de dominio para este servicio:')
    ip = input('Ingrese la ip para asociar este dominio:')
    # Checar si se necesita validación para ambos valores obtenidos
    db += dns + '   IN          A       '+ip
    print(db)
    #Crear archivo con el dbPath y escribirle el contenido de db
    dbFile = open(dbPath, 'wt')
    dbFile.write(db)
    dbFile.close()

def addXMPP(siteName):
    print('Agregando servicio XMPP a ', siteName)
    dbPath = origin + '\\db.' + siteName

def addFTP(siteName):
    print('Agregando servicio FTP a ', siteName)
    dbPath = origin + '\\db.' + siteName


##########  MAIN()  ##########
print('Escoge un número de opción:')
opc = -1
#Menu principal para escoger acción a realizar
while opc != 0:
    print('1) Agregar un sitio.')
    print('2) Modificar sitio.')
    print('3) Eliminar sitio.')
    print('0) Salir.')
    opc = int(input())
    #Validacion para opciones inválidas
    while opc<0 or opc>3:
        print('Opción no válida, ingrese una opción válida o 0 para salir')
        opc = int(input())
        if opc == 0:
            exit(-2)
    #Se escogió AGREGAR UN NUEVO SITIO
    if opc == 1:
        print('Agregando nuevo sitio. Ingrese el nombre del nuevo sitio:')
        siteName = input()
        addSite(siteName)
        print('¿Desea agregar servicio de HTTP?\n1)Si 2)No')
        httpBand = int(input())
        print('¿Desea agregar servicio de XMPP?\n1)Si 2)No')
        xmppBand = int(input())
        print('¿Desea agregar servicio de FTP?\n1)Si 2)No')
        ftpBand = int(input())
        #Se escogió agregar un servidor de HTTP
        if httpBand == 1:
            addHTTP(siteName)
        #Se escogió agregar un servidor de XMPP
        if xmppBand == 1:
            addToSite(siteName)
        #Se escogió agregar un servidor de FTP
        if ftpBand == 1:
            addToSite(siteName)

    print('¿Deseas seguir?')
    print('1) Si, 0)Salir')
    opc = int(input())
