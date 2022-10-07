import re
import string
import subprocess
import os
from tracemalloc import start

class getGeneral():
    def __init__(self,list_c) -> None:#Constructor de la clase get
        self.list_c = list_c
    """
    Este metodo genera una lista de pares ordenados de numeros enteros, donde cada par representa el inicio y el fin
    de cada referencia. Para encontrar el inicio de la referencia detecta el primer arroba, posteriormente
    al detectar el segundo se puede establecer donde empieza y donde termina una referencia. Ya que la ultima
    referencia no tiene un arroba al final que nos ayude detectar el fin de esta, se agrega este ultimo arroba
    al final de la lista_c.
    Entradas:
    Ninguna entrada
    
    Salida:
    Una lista de pares ordenados que representa el inicio y el fin de cada referencia
    """
    def get_index(self):
        start1 = 0
        start2 = 0
        L_index = [] #r"(@+.*+({.*})+)"
        patronA = re.compile(r"(@+[\w\_\-\:\.\,\*]+{)")#Expresion regular para obtener el el arroba
        self.list_c.append("@a{")
        for i in range(0,len(self.list_c)):
            if patronA.search(self.list_c[i]): 
                if(start1 < start2):
                    start1 = i
                else:           
                    start2=i
                    L_index.append([start1,start2-1])
                    start1 = start2
                    start2 = 0
        if len(L_index) <= 1:
            os.system("clear")
            print("ERROR: Formato invalido.\n\tEl archivo .bib seleccionado no cumple con el formato adecuado. Seleccione otro archivo .bib")
            input("Presione enter...")
            exit()
        return L_index

class set():
    def __init__(self,Index,list_c) -> None:#Constructor de la clase set
        self.Index = Index
        self.list_c = list_c
    """
    Tomando los indeices producidos por el metodo get_idex de la clase getGeneral, se agrupan las lineas que
    correspondan a cada referencia.
    Entradas:
        Ninguna
    Salidas:
        Lista donde cada item corresponde a una lista con todas las lineas de cada referencia 
    """
    def set_grupe_ref(self):
        or_data = []
        for i in range(1,len(self.Index)):
            or_data.append(self.list_c[self.Index[i][0]:self.Index[i][1]])
        return or_data
    """
    Metodo encargado de determinar el visor PDF que usa el usuario. Se pide que ingrese una de las opciones
    por defecto, o que se ingrese el nombre del mismo.
    Entradas:
        Ninguna
    Salida
        Un string con el nombre del visor pdf
    """
    def set_reader(self):
        pdfr ="-1"
        while(pdfr == "-1"):
            os.system("clear")
            print("Lectores PDF")
            print("1.- Evince\n2.- Okular\n3.- Atril\n4.- Xpdf\n5.- Otro")
            pdfr = input("Seleccione su lector pdf: ")
            if pdfr == "1":
                pdfr = "evince"
            elif(pdfr == "2"):
                pdfr = "okular"
            elif(pdfr == "3"):
                pdfr = "atril"
            elif(pdfr == "4"):
                pdfr = "xpdf"
            elif(pdfr == "5"):
                os.system("clear")
                print("Lectores PDF")
                pdfr = input("Ingrese el nombre de su lector pdf: ").lower()
            else:
                os.system("clear")
                print("ERROR: Opcion incorrecta\n\tIngrese una opcion de la lista")
                input("\nPresione enter...")
                pdfr = "-1"
        os.system("clear")
        return pdfr

        
        
class getTabla():
    def __init__(self,list_o) -> None:#Constructor de la funcion set
        self.list_o=list_o
        self.reference_list = []
        #self.author_list = []
        self.title_list = []

    """
    Metodo encargado de obtener la clave de cada referencia.
    Entradas:
        Ninguna
    Salidas:
        Una lista de strings que contienen las claves de cara referencia
    """
    def get_ref(self):
        patronR = re.compile(r"w*({[A-za-z0-9.\-:]+),*")#Expresion regular para encontrar la referencia 
        for i in range(0,len(self.list_o)):
            ref = patronR.search(self.list_o[i][0])
            if patronR.search(self.list_o[i][0]):
                self.reference_list.append(self.list_o[i][0][ref.start()+1:ref.end()-1])
        return self.reference_list

    """
    Metodo encargado de limpiar un string de caracteres basura, como llaves, secuencias de escape, etc.
    Entradas:
        string_c: String a limpiar
        op: Numero entero que especifica si se trata de un autor(1) o un titulo(2).
    Salidas:
        String libre de caracteres no deseados. 
    """
    def clean_string(self,string_c,op):
            string_p=string_c
            if op == 1:
                patronA = re.compile(r'(AUTHOR)*(=)+')
            if op ==2:
                patronA = re.compile(r'(TITLE)*(=)+')

            if patronA.search(string_c.upper()):
                authorE = patronA.search(string_c.upper())
                string_p =string_c[authorE.end()+1:len(string_c)]
                
            string_p = string_p.replace('"',"").replace("\n","\\\\").replace("\t","").replace("{","").replace("}","").replace("&","\&").replace("\\","").replace("$","\$").replace("|","")
        
            if len(string_p) > 0:
                if string_p[(len(string_p)-1)] == ",":
                    string_p = string_p[0:len(string_p)-1]
            return string_p
    """
    Obtiene el autor o el titulo dependiendo de la opcion(op) pasada como parametro donde 1 es para autores
    y 2 es para titulos.
    Entradas:
        op: Opcion que especifica que atributo se va a obtener
    """
    def get_atributs(self,op):
        if (op==1):
            patronA1 = re.compile(r"(AUTHOR)+([\s=]+)")
        else:
            patronA1 = re.compile(r"(TITLE)+([\s=]+)")
            patronA1 = None
            patronA1 = re.compile(r"(TITLE)+([\s=]+)")
        patronA2 = re.compile(r'(= {)|(= ")')
        start =0
        end=0
        cont =0
        num_ref=0
        author_list = []
        for i in range(0,len(self.list_o)):
            cont = 0
            num_ref=0
            for j in range(0,len(self.list_o[i])):
                if (i == (len(self.list_o))-1) and j == (len(self.list_o[i])-1):
                    self.list_o[i].append("= {")
                if patronA1.search(self.list_o[i][j].upper()):
                    num_ref = 1
                    start = j
                    for h in range(j+1,len(self.list_o[i])):
                        if (patronA2.search(self.list_o[i][h]) and cont ==0):
                            cont = 1
                            end = h
                        elif h == len(self.list_o[i])-1 and cont == 0:
                            cont = 1
                            end = h
                    if start == end-1:
                        author_list.append(self.clean_string((self.list_o[i][start]),op))
                    else:
                        aut = ""
                        for g in range(start,end):
                            aut = aut + self.list_o[i][g]
                        author_list.append(self.clean_string(aut,op))             
            if num_ref == 0:
                author_list.append("")
                num_ref=1
        return author_list

class crearPdf(): 
    def __init__(self,base_LTI, base_LTF, reference,title,author) -> None:
        self.reference = reference
        self.title = title
        self.author=author
        self.base_LTI = base_LTI
        self.base_LTF = base_LTF
    
    """
    Metodo que inserta los valores leidos en el cuerpo de la tabla siguiente el formato de un long-table.
    Entradas:
        Ninguna
    Salidas:
        Una lista donde cada item es una linea del documento .tex final        

    """
    def insert_table(self):
        for i in range(0,len(self.reference)):
            row = self.reference[i]+"&"+self.title[i]+"&"+self.author[i]+"\\\\"+"\n"+"\hline"+"\n" 
            self.base_LTI.append(row)
        self.base_LTI +=self.base_LTF
        return self.base_LTI

    """
    Metodo que escribe el .tex final, compila el archivo con el compilador de latex pdflatex y abre el 
    documento pdf final. Antes de escribir el archivo tex elimina el anterior. Es capaz de detectar si el
    visor pdf esta instalado y si se cuenta con el compilador pdflatex
    Entradas:
        pdfr: La opcion de visor pdf seleccionada por el usuario

    Salida:
        Genera el .tex
        Genera el pdf producto de compilar el .tex anterior
    """
    def generate_tex(self, generate_tex, pdfr):
        try:
            fileTex = open("main.tex","a+")
            os.remove("main.tex")
        except FileNotFoundError:
            print("main.tex exist")    
        fileTex = open("main.tex","a+")
        fileTex.writelines(self.base_LTI)
        fileTex.close()
        try:
            subprocess.run(["pdflatex","main.tex"])
        except:
            os.system("clear")
            print("ERROR: Medios no encontrados\n\tEl compilador de Latex no esta instalado")
            input("\nPresione enter...")
            exit()
        subprocess.run(["pdflatex","main.tex"])
        print("PDF generade")
        try:
            subprocess.run([pdfr,"main.pdf"])
        except:
            os.system("clear")
            print("ERROR: Medios no encontrados\n\tEl lector de pdf que ha ingresado no se encontro")
            input("\nPresione enter...")
            exit()

class ClasePrincipal():
    """
    Baner con las indicaciones para usar el programa.
    Sin entradas ni salidas
    """
    def instrucciones(self):#Metodo de instrucciones para el usuario
        os.system("clear")
        print("\t\t!!!!ADVERTENCIA!!!!")
        print("-------------------------------------------------------")
        print("El código solo funcionara mientras que el archivo .bib a \ningresar este en la misma carpeta que el archivo PYTHON")
        print("-------------------------------------------------------")

    def main(self)->None:#Funcion  principal donde se leen los datos y se llaman a las demas clases
        
        Fname = False
        while(Fname ==False):
            os.system("clear")
            self.instrucciones()
            print("Ingrese el nombre del archivo .bib que desea examinar: ")
            name_file = input()#Lee el archivo .bib
            if (name_file[((len(name_file))-4):((len(name_file)))]) == ".bib":
                try:
                    file = open(name_file,'r')
                    Fname = True
                except FileNotFoundError:
                    os.system("clear")
                    print("ERROR: Archivo no encontrado.\n\t Verifique que el archivo .bib se encuentre en el mismo directorio que el .py ")
                    input("\nPresione enter...")
                    Fname = False
            else:
                os.system("clear")
                print("ERROR: Extencion invalida\n\t La extencion del archivo debe ser .bib")
                input("\nPresione enter...")
                Fname = False
                
        dataC = file.readlines()
        file.close()

        #Los objetos base_LTI y LTF contienen el formato de archivo para generar el latex
        base_LTI = ['\\documentclass{article}\n', '\\usepackage{longtable}\n', '\\title{Contenido de .bib}\n', '\\begin{document}\n', '%\\begin{center}\n', '\\begin{longtable}{|p{0.33\\textwidth}|p{0.33\\textwidth}|p{0.33\\textwidth}|}\n', '\\caption{Contenido de .bib} \\label{tab:long} \\\\\n', '\\hline \\multicolumn{1}{|c|}{\\textbf{Referencia}} & \\multicolumn{1}{c|}{\\textbf{Titulo}} & \\multicolumn{1}{c|}{\\textbf{Autores}} \\\\ \\hline\n', '\\endfirsthead\n', '\\multicolumn{3}{c}%\n', '{{\\bfseries \\tablename\\ \\thetable{} -- continued from previous page}} \\\\\n', '\\hline \\multicolumn{1}{|c|}{\\textbf{First column}} & \\multicolumn{1}{c|}{\\textbf{Second column}} & \\multicolumn{1}{c|}{\\textbf{Third column}} \\\\ \\hline \n', '\\endhead\n', '\\hline \\multicolumn{3}{|r|}{{Continued on next page}} \\\\ \\hline\n', '\\endfoot\n', '\\hline \\hline\n', '\\endlastfoot\n']
        base_LTF = ['\\end{longtable}\n', '\\end{document}\n']
        Index = getGeneral(dataC)
        dataO = set(Index.get_index(),dataC)
        pdf_reader = set.set_reader(self)
        ref = getTabla(dataO.set_grupe_ref())
        base_tex = crearPdf(base_LTI,base_LTF,ref.get_ref(),ref.get_atributs(op=2),ref.get_atributs(op=1))
        base_tex.insert_table()
        base_tex.generate_tex(self,pdfr=pdf_reader)

object = ClasePrincipal()
object.main()