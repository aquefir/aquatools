#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def getbp(fname):
	text = open(fname, 'r').readlines()
	return ''.join(text[4:10])

def mkincguard(proj, module, public):
	return 'INC_' + ('API__' if public else '_') + proj.upper() + \
		'_' + module.replace('/', '_').upper() + '_H'

def main(args):
	from os import getcwd
	from os.path import basename, join
	argc = len(args)
	if argc == 1:
		print('Usage:-\n\n    ./newmodule.py <module> [proj]\n')
		return 0
	module = args[1]
	proj = ''
	if argc == 3:
		proj = args[2]
	else:
		proj = basename(getcwd())
	public_h = join(getcwd(), 'include', proj, module + '.h')
	private_h = join(getcwd(), 'src', module + '.h')
	sourcefile = join(getcwd(), 'src', module + '.c')
	bp = getbp(join(getcwd(), 'BOILERPLATE'))
	incdef = mkincguard(proj, module, True)
	pubh_text = bp + '\n#ifndef ' + incdef + '\n#define ' + incdef + \
		'\n\n/* Nothing here yet... */\n\n#endif /* ' + incdef + ' */\n'
	incdef = mkincguard(proj, module, False)
	privh_text = bp + '\n#ifndef ' + incdef + '\n#define ' + incdef + \
		'\n\n#include <' + proj + '/' + module + '.h>\n\n#endif /* ' + incdef \
		+ ' */\n'
	srcf_text = bp + '\n#include "' + basename(module) + '.h"\n'
	with open(public_h, 'w') as f:
		f.write(pubh_text)
	with open(private_h, 'w') as f:
		f.write(privh_text)
	with open(sourcefile, 'w') as f:
		f.write(srcf_text)
	return 0

if __name__ == '__main__':
	from sys import argv, exit
	exit(main(argv))
