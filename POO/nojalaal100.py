import re
import subprocess
import os

class getGeneral():
    def __init__(self,list_c) -> None:
        self.list_c = list_c

    def get_index(self):
        start1 = 0
        start2 = 0
        L_index = []
        patronA = re.compile(r"@")
        self.list_c.append("@")
        for i in range(0,len(self.list_c)):
            if patronA.search(self.list_c[i]): 
                if(start1 < start2):
                    start1 = i
                else:           
                    start2=i
                    L_index.append([start1,start2-1])
                    start1 = start2
                    start2 = 0
        return L_index

class set():
    def __init__(self,Index,list_c) -> None:
        self.Index = Index
        self.list_c = list_c

    def set_grupe_ref(self):
        or_data = []
        for i in range(1,len(self.Index)):
            or_data.append(self.list_c[self.Index[i][0]:self.Index[i][1]])
        return or_data

class getTabla():
    def __init__(self,list_o) -> None:
        self.list_o=list_o
        self.reference_list = []
        self.author_list = []
        self.title_list = []

    def get_ref(self):
        patronR = re.compile(r"w*({[A-za-z0-9.\-:]+),*")
        for i in range(0,len(self.list_o)):
            ref = patronR.search(self.list_o[i][0])
            if patronR.search(self.list_o[i][0]):
                self.reference_list.append(self.list_o[i][0][ref.start()+1:ref.end()-1])
        return self.reference_list

    def get_Title(self):
        def clean_string(string_c):
            string_p=""
            if string_c.find("{")!=-1:
                string_p = string_c[string_c.find("{")+1:string_c.find("}")-1] 
            if string_c.find('"')!=-1:
                string_p = string_c[string_c.find('"')+1:len(string_c)-1]
            string_p = string_p.replace('"',"").replace(',',"").replace("\n","\\\\").replace("\t","").replace("{","").replace("}","").replace("&","\&").replace("\\","").replace("$","\$").replace("|","")
            return string_p

        patronA1 = re.compile(r"(TITLE)+([\s=]+)")
        patronA2 = re.compile(r'(= {)+|(= ")+')
        start =0
        end=0
        cont =0
        num_ref=0
        for i in range(0,len(self.list_o)):
            cont = 0
            num_ref=0
            for j in range(0,len(self.list_o[i])):
                if patronA1.search(self.list_o[i][j].upper()):
                    num_ref = 1
                    start = j
                    for h in range(j+1,len(self.list_o[i])):
                        if (patronA2.search(self.list_o[i][h]) and cont ==0):
                            cont = 1
                            end = h
                    if start == end-1:
                        self.title_list.append(clean_string(self.list_o[i][start]))
                    else:
                        tit = ""
                        for g in range(start,end):
                            tit = tit + self.list_o[i][g]
                        self.title_list.append(clean_string(tit))
                
            if num_ref == 0:
                self.title_list.append("")
                num_ref=1
        return self.title_list

    def get_author(self):
        def clean_string(string_c):
            string_p=""
            if string_c.find("{")!=-1:
                string_p = string_c[string_c.find("{")+1:string_c.find("}")-1] 
            if string_c.find('"')!=-1:
                string_p = string_c[string_c.find('"')+1:len(string_c)-1]
            string_p = string_p.replace('"',"").replace(',',"").replace("\n","\\\\").replace("\t","").replace("{","").replace("}","").replace("&","\&").replace("\\","").replace("$","\$").replace("|","")
            return string_p
        patronA1 = re.compile(r"(AUTHOR)+([\s=]+)")
        patronA2 = re.compile(r'(= {)+|(= ")+')
        start =0
        end=0
        cont =0
        num_ref=0
        for i in range(0,len(self.list_o)):
            cont = 0
            num_ref=0
            for j in range(0,len(self.list_o[i])):
                if patronA1.search(self.list_o[i][j].upper()):
                    num_ref = 1
                    start = j
                    for h in range(j+1,len(self.list_o[i])):
                        if (patronA2.search(self.list_o[i][h]) and cont ==0):
                            cont = 1
                            end = h
                    if start == end-1:
                        self.author_list.append(clean_string(self.list_o[i][start]))
                    else:
                        aut = ""
                        for g in range(start,end):
                            aut = aut + self.list_o[i][g]
                        self.author_list.append(clean_string(aut))
                
            if num_ref == 0:
                self.author_list.append("")
                num_ref=1
        return self.author_list

class crearPdf(): 
    def __init__(self,base_LTI, base_LTF, reference,title,author) -> None:
        self.reference = reference
        self.title = title
        self.author=author
        self.base_LTI = base_LTI
        self.base_LTF = base_LTF
        
    def insert_table(self):
        for i in range(0,len(self.reference)):
            row = self.reference[i]+"&"+self.title[i]+"&"+self.author[i]+"\\\\"+"\n"+"\hline"+"\n" 
            self.base_LTI.append(row)
        self.base_LTI +=self.base_LTF
        return self.base_LTI

    def generate_tex(self):
        try:
            fileTex = open("main.tex","a+")
            os.remove("main.tex")
        except FileNotFoundError:
            print("main.tex exist")    
        fileTex = open("main.tex","a+")
        fileTex.writelines(self.base_LTI)
        fileTex.close()
        subprocess.run(["pdflatex","main.tex"])
        subprocess.run(["pdflatex","main.tex"])
        print("PDF generade")
        subprocess.run(["evince","main.pdf"])

class ClasePrincipal():
    def main(self)->None:
        file = open("references.bib","r")
        dataC = file.readlines()
        file.close()
        base_LTI = ['\\documentclass{article}\n', '\\usepackage{longtable}\n', '\\title{Contenido de .bib}\n', '\\begin{document}\n', '%\\begin{center}\n', '\\begin{longtable}{|p{0.33\\textwidth}|p{0.33\\textwidth}|p{0.33\\textwidth}|}\n', '\\caption{Contenido de .bib} \\label{tab:long} \\\\\n', '\\hline \\multicolumn{1}{|c|}{\\textbf{Referencia}} & \\multicolumn{1}{c|}{\\textbf{Titulo}} & \\multicolumn{1}{c|}{\\textbf{Autores}} \\\\ \\hline\n', '\\endfirsthead\n', '\\multicolumn{3}{c}%\n', '{{\\bfseries \\tablename\\ \\thetable{} -- continued from previous page}} \\\\\n', '\\hline \\multicolumn{1}{|c|}{\\textbf{First column}} & \\multicolumn{1}{c|}{\\textbf{Second column}} & \\multicolumn{1}{c|}{\\textbf{Third column}} \\\\ \\hline \n', '\\endhead\n', '\\hline \\multicolumn{3}{|r|}{{Continued on next page}} \\\\ \\hline\n', '\\endfoot\n', '\\hline \\hline\n', '\\endlastfoot\n']
        base_LTF = ['\\end{longtable}\n', '\\end{document}\n']
        Index = getGeneral(dataC)
        dataO = set(Index.get_index(),dataC)
        ref = getTabla(dataO.set_grupe_ref())
        base_tex = crearPdf(base_LTI,base_LTF,ref.get_ref(),ref.get_Title(),ref.get_author())
        base_tex.insert_table()
        base_tex.generate_tex()

object = ClasePrincipal()
object.main()