#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pkginfo
import codecs
import j2py

import os.path

from translatepackages import rename_pkg
import java_front
from config import config,logger


DEBUG = True
save_intermediates = DEBUG


def package2py(basedir,pkg=None,outbase=None,recursive=True):
    """
    translates all java src in pkg to python,
    writes py src into outbase/pkg
    """

    if outbase is None:
        outbase = os.path.join(basedir,"..","py")

    logger.debug(pkg)
    #figure out output dir
    outpkg = rename_pkg(pkg)

    pkgdir = os.path.join(basedir,pkg.replace(".",os.path.sep))
    if outpkg is None:
        outdir = outbase
    else:
        outdir = os.path.join(outbase,outpkg.replace(".",os.path.sep))

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    logger.info("starting java2py")
    logger.info("  pkgdir: %s",pkgdir)
    logger.info("  outdir: %s",outdir)

    pi = pkginfo.PackageInfo.load(basedir,pkg)

    #make __init__.py
    of = open(os.path.join(outdir,"__init__.py"),"w")
    of.write('''#-*- coding:utf-8 -*-\n"""%s"""\n''' % pi.doc)

    of.write('\n#public classes:\n')
    for c in pi.public_classes():
        of.write('from %s import %s\n' % (c.name,c.name) )

    of.write('\n#public interfaces:\n')
    for i in pi.public_interfaces():
        of.write('from %s import %s\n' % (i.name,i.name) )

    of.close()

    for n in os.listdir(pkgdir):
        if recursive and os.path.isdir(os.path.join(pkgdir,n)) \
           and not n.startswith('.') \
           and (True or os.path.exists(os.path.join(pkgdir,n,'package.html'))):
            package2py(basedir,pkg+"."+n,outbase,True)
        elif n.endswith(".java"):
            print "translating",n

            ast = java_front.parse_java(os.path.join(pkgdir,n))

            if save_intermediates:
                f = codecs.open(os.path.join(outdir,n+".aterm"),"w","utf8")
                f.write(java_front.pp_aterm(ast))
                f.close()

            j2py.run(ast)

            #todo: add package imports

            if save_intermediates:
                f = codecs.open(os.path.join(outdir,n+".j2py.aterm"),"w","utf8")
                s = java_front.pp_aterm(ast)
                f.write(s)
                f.close()

            py_ast = java_front.java2py(ast)

            if save_intermediates:
                f = codecs.open(os.path.join(outdir,n+".box"),"w","utf8")
                s = java_front.pp_aterm(py_ast)
                f.write(s)
                f.close()

            py = java_front.abox2text(py_ast)

            py = py.split("\n")


            #skip
            skip = config['skip']

            def keep(l):
                ls = l.strip()
                if ls in skip: return False
                for s in skip:
                    if ls.startswith(s): return False
                return True

            res = [ l for l in filter(keep,py) ]

            py = "\n".join(res)

            pyfn = n.replace('.java','.py')
            f = codecs.open(os.path.join(outdir,pyfn),'w','utf8')
            f.write(py)
            f.close()

if __name__ == '__main__':
    #hardcoded args while developing ...
    basedir = '/home/toka/dv2/google-web-toolkit/user/src/'
    pkg = 'com.google.gwt.user.client'

    basedir = '/home/toka/dv/gwt1.7-dnd/DragDrop/src/'
    pkg = 'com.allen_sauer.gwt.dnd'

    basedir = '/home/toka/dv2/gwt-facebook/GwittIt/src'
    pkg = 'com.gwittit'

    package2py(basedir,pkg)
