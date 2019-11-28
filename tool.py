# CHECAR LOS SALTOS DE LINEA EN EL ARCHIVO DE INFO Y LOS SITES NO SE AGREGUEN DE MAS
# LIBRARIES
import os
import pprint
# VARIALBES GLOBALES
origin = 'C:\\Users\\Superman\\Documents\\ESCOM\\9no\\ASR'
sitesPath = origin + '\\named.conf.local'
httpIp = '192.168.1.1'
xmppIp = '192.168.1.2'
ftpIp = '192.168.1.3'
sites = []
# CLASES
class site:
    def __init__(self,siteName):
        self.name = siteName
        self.services = {}

    def addService(self, dns, ip):
        self.services[dns] = ip

# FUNCIONES
#Imprime cada sitio y sus servicios en ese momento
def printSites():
    print('Sitios existentes:')
    for site in sites:
        print(site.name)

    #for site in sites:
    #    print('Nombre sitio: ' , site.name, ' Servicios Asociados: ', site.services)
def printServices(site):
    print('Servicios existentes del sitio' , site.name)
    for dns, ip in site.services.items():
        print('Dominio=', dns, ' con ip=', ip)
# Devuelve un texto para un archivo base
def createDB(siteName):
    #filedbPath = open(dbpath, 'wt')
    db = '''$TTL \t\t\t 604800
@               IN          SOA     ''' + siteName + '''. root.''' + siteName + '''. (
                            2                       ; Serial
                            604800                  ; Refresh
                            86400                   ; Retry
                            2419200                 ; Expire
                            604800  )               ; Negative Cache TTL
;
@               IN          NS      ''' +siteName + '''.
'''
    return(db)

def createFileDB(newSite):
    try:
        db = createDB(newSite.name)
        # print(db)
        for dns,ip in newSite.services.items():
            db += dns + '\tIN          A       '+ip+'\n'
        print(db)
        dbPath = origin + '\\db.' + newSite.name
        dbFile = open(dbPath, 'wt')
        dbFile.write(db)
        dbFile.close()
        print('Archivo db creado exitosamente.')
    except:
        print('Error al crear archivo db.')
#Funcion para agregar servicios a un sitio
def addToSite(newSite, kind):
    dns = input('Ingrese un nombre de dominio para este servicio '+ kind + ':')
    ip = input('Ingrese la ip para asociar este dominio:')
    newSite.addService(dns,ip)
#Funcion para devolver un sitio existente, devuelve null si no lo encuentra
def getSite(siteName):
    for site in sites:
        if site.name == siteName:
            return site

    return None

# Funcion para eliminar un servicio de un sitio
def delService(site, serviceName):
    if serviceName in site.services:
        site.services.pop(serviceName)
        print('Servicio eliminado')
        return
    print('Servicio no encontrado en este sitio.')

#Funcion para eliminar un sitio
def delSite(siteName):
    site = getSite(siteName)
    if site != None:
        sites.remove(site)
    else:
        print('Sitio no existente')

# Funcion para obtener la información inicial del archivo auxiliar para los sitios
def getInfo():
    try:
        info = open(origin + '\\infoFile.txt')
        #Se lee cada linea del archivo auxiliar
        #file = open(origin + '\\infoFile.txt')
        for line in info:
            tuplas = line.split('&')
            newSite = site(tuplas[0])
            for i in range(1, len(tuplas)):
                services = tuplas[i].split('/')
                dns = services[0]
                ip = services[1]
                newSite.addService(dns, ip)
            sites.append(newSite)
    except:
        print('ocurrió un error al empezar el programa ')

# Funcion para escribir la información inicial del archivo auxiliar de los sitios
def setInfo():
    zone = ''
    aux = ''
    for site in sites:
        zone += '''zone \"''' + site.name + '''\" {
    type master;
    file \"''' + origin + '''\\db.''' + site.name + '''\";
};\n'''
        aux += site.name
        for dns, ip in site.services.items():
            aux += '&' + dns + '/' + ip

        aux += '\n'

    try:
        fileSites = open(sitesPath, 'wt')
        info = open(origin + '\\infoFile.txt', 'wt')
        fileSites.write(zone)
        info.write(aux)
        print(aux)
        fileSites.close()
        info.close()
        print('Sitio agregado correctamente.')
    except:
        print('Error al guardar la información')

    print(aux)
    print(zone)


def main():
    getInfo()
    printSites()

    print('Escoge un número de opción:')
    opc = -1
    #Menu principal para escoger acción a realizar
    while opc != 0:
        printSites()
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
            siteName = input('Agregando nuevo sitio. Ingrese el nombre del nuevo sitio:')
            newSite = site(siteName)

            print('¿Desea agregar servicio de HTTP al nuevo sitio?\n1)Si 2)No')
            httpBand = int(input())
            if httpBand == 1:
                addToSite(newSite, 'HTTP')
                print(newSite.services)

            print('¿Desea agregar servicio de XMPP?\n1)Si 2)No')
            xmppBand = int(input())
            if xmppBand == 1:
                addToSite(newSite, 'XMPP')
                print(newSite.services)

            print('¿Desea agregar servicio de FTP?\n1)Si 2)No')
            ftpBand = int(input())
            if ftpBand == 1:
                addToSite(newSite, 'FTP')
                print(newSite.services)
            # Agregar al arreglo de clases de los sitios
            sites.append(newSite)
            #Crea un archivo por cada servicio en este sitio
            createFileDB(newSite)

        if opc == 2:
            print('Modificar un sitio')
            printSites()
            siteName2 = input('Ingrese el nombre de algun sitio a modificar:')
            actualSite = getSite(siteName2)
            if actualSite != None:
                print('Seleccione una opción para realizar con este sitio:')
                print('1) Agregar un servicio.')
                print('2) Modificar servicio.')
                print('3) Eliminar servicio.')
                print('4) Cambiar nombre de sitio')
                print('0) Salir.')
                op2 = int(input())
                if op2 == 1:
                    print('Agregando un servicio.')
                    addToSite(actualSite, '')
                if op2 == 2:
                    print('Modificar un servicio')
                if op2 == 3:
                    printServices(actualSite)
                    serviceName = input('Ingrese el nombre del servicio a eliminar:')
                    delService(actualSite, serviceName)
                if op2 == 4:
                    newName = input('Ingrese el nuevo nombre de este sitio:')
                    actualSite.name = newName
            else:
                print('Sitio no encontrado')
        if opc == 3:
            siteName = input('Ingrese el nombre del sitio que desea eliminar: ')
            delSite(siteName)
            print('Sitio ', siteName, 'Eliminado')

        print('¿Deseas seguir?')
        print('1) Si, 0)Salir')
        opc = int(input())

    printSites()
    #setInfo()


if __name__=='__main__':
    main()
