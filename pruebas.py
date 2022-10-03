import re
import subprocess
import os

file = open("references.bib","r")
dataC = file.readlines()
file.close()


file = open("base_long_table_I.txt","r")
base_LTI = ['\\documentclass{article}\n', '\\usepackage{longtable}\n', '\\title{Contenido de .bib}\n', '\\begin{document}\n', '%\\begin{center}\n', '\\begin{longtable}{|p{0.33\\textwidth}|p{0.33\\textwidth}|p{0.33\\textwidth}|}\n', '\\caption{Contenido de .bib} \\label{tab:long} \\\\\n', '\\hline \\multicolumn{1}{|c|}{\\textbf{Referencia}} & \\multicolumn{1}{c|}{\\textbf{Titulo}} & \\multicolumn{1}{c|}{\\textbf{Autores}} \\\\ \\hline\n', '\\endfirsthead\n', '\\multicolumn{3}{c}%\n', '{{\\bfseries \\tablename\\ \\thetable{} -- continued from previous page}} \\\\\n', '\\hline \\multicolumn{1}{|c|}{\\textbf{First column}} & \\multicolumn{1}{c|}{\\textbf{Second column}} & \\multicolumn{1}{c|}{\\textbf{Third column}} \\\\ \\hline \n', '\\endhead\n', '\\hline \\multicolumn{3}{|r|}{{Continued on next page}} \\\\ \\hline\n', '\\endfoot\n', '\\hline \\hline\n', '\\endlastfoot\n']
#file.readlines()
file = open("base_long_table_F.txt","r")
base_LTF = ['\\end{longtable}\n', '\\end{document}\n']
#file.readlines()

def get_index(list_c):
    start1 = 0
    start2 = 0
    L_index=[]
    patronA = re.compile(r"@")
    list_c.append("@")
    for i in range(0,len(list_c)):
        if patronA.search(list_c[i]): 
            if(start1 < start2):
                start1 = i
            else:           
                start2=i
                L_index.append([start1,start2-1])
                start1 = start2
                start2 = 0
    return L_index
        

def set_grupe_ref(Index,list_c):
    or_data = []
    for i in range(1,len(Index)):
        or_data.append(list_c[Index[i][0]:Index[i][1]])
    return or_data


def get_ref(list_o):
    patronR = re.compile(r"w*({[A-za-z0-9.\-:]+),*")
    reference_list = []
    for i in range(0,len(list_o)):
        ref = patronR.search(list_o[i][0])
        if patronR.search(list_o[i][0]):
            reference_list.append(list_o[i][0][ref.start()+1:ref.end()-1])
 
    return reference_list

def clean_string(string_c):
    string_p=""
    if string_c.find("{")!=-1:
        string_p = string_c[string_c.find("{")+1:string_c.find("}")-1] 
        #print(string_p)
    
    if string_c.find('"')!=-1:
        string_p = string_c[string_c.find('"')+1:len(string_c)-1]
        #print(string_p)
    string_p = string_p.replace('"',"").replace(',',"").replace("\n","\\\\").replace("\t","").replace("{","").replace("}","").replace("&","\&").replace("\\","").replace("$","\$").replace("|","")

    return string_p

def get_author(list_o,op):
    if (op==1):
        patronA1 = re.compile(r"(AUTHOR)+([\s=]+)")
    else:
        patronA1 = re.compile(r"(TITLE)+([\s=]+)")
    patronA2 = re.compile(r'(= {)+|(= ")+')
    start =0
    end=0
    cont =0
    num_ref=0
    author=[]
    for i in range(0,len(list_o)):
        cont = 0
        num_ref=0
        for j in range(0,len(list_o[i])):
            if patronA1.search(list_o[i][j].upper()):
                num_ref = 1
                start = j
                for h in range(j+1,len(list_o[i])):
                    if (patronA2.search(list_o[i][h]) and cont ==0):
                        cont = 1
                        end = h
                if start == end-1:
                    author.append(clean_string(list_o[i][start]))
                else:
                    aut = ""
                    for g in range(start,end):
                        aut = aut + list_o[i][g]
                    author.append(clean_string(aut))
            
        if num_ref == 0:
            author.append("")
            num_ref=1
    return author



    
def insert_table(base_LTI,base_LTF,reference,author,title):
    for i in range(0,len(reference)):
        row = reference[i]+"&"+title[i]+"&"+author[i]+"\\\\"+"\n"+"\hline"+"\n" 
        base_LTI.append(row)
    base_LTI = base_LTI+base_LTF
    #print(base_LTI)
    return base_LTI   

def generate_tex(base_tex):
    try:
        fileTex = open("main.tex","a+")
        os.remove("main.tex")
    except FileNotFoundError:
        print("main.tex exist")    
    fileTex = open("main.tex","a+")
    fileTex.writelines(base_tex)
    fileTex.close()
    #try:
    #    file = open("main.pdf")
    #    file.close()
    #    os.remove("main.pdf")
    #    os.remove("main.aux")
    #    os.remove("main.log")
    #except FileNotFoundError:
    #    print("main.pdf exist")
    subprocess.run(["pdflatex","main.tex"])
    subprocess.run(["pdflatex","main.tex"])
    print("PDF generade")
    subprocess.run(["okular","main.pdf"])


Index = get_index(dataC)
dataO = set_grupe_ref(Index,dataC)
ref = get_ref(dataO)
aut =get_author(dataO,1)
title =get_author(dataO,0)

base_tex = insert_table(base_LTI,base_LTF,ref,aut,title)
generate_tex(base_tex)



#%One & abcdef ghjijklmn & 123.456778 \\