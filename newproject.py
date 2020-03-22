#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdin, stdout

def recv_yn(text):
	while True:
		stdout.write(text + ' [Y/N]: ')
		stdout.flush()
		resp = stdin.readline().lower()[:-1]
		stdout.flush()
		if resp == 'y':
			return True
		elif resp == 'n':
			return False
		else:
			stdout.write('Invalid response.\n')
			stdout.flush()

def recv_line(text):
	stdout.write(text + ' ')
	stdout.flush()
	return stdin.readline()[:-1]

def center74(text):
	textlen = len(text)
	if textlen % 2 == 1:
		return None
	space_ct = (74 - textlen) // 2
	return (' ' * space_ct) + text + (' ' * space_ct)

def decorate_sh(lines):
	return ('#' * 78) + '\n##' + lines[0] + '##\n##' + (' ' * 74) + '##\n##' \
		+ lines[1] + '##\n##' + lines[2] + '##\n' + ('#' * 78)

def decorate_c(lines):
	return '/' + ('*' * 76) + '\\\n *' + lines[0] + '*\n *' + (' ' * 74) + \
		'*\n *' + lines[1] + '*\n *' + lines[2] + '*\n\\' + ('*' * 76) + '/'

def writelocal(projdir, name, text):
	from os.path import join
	f = open(join(projdir, name), 'w')
	f.write(text)
	f.close()

def readfar(name):
	f = open(name, 'r')
	data = f.read()
	f.close()
	return data

def readlocal(name):
	from os.path import dirname, join, realpath
	f = open(join(dirname(realpath(__file__)), name), 'r')
	data = f.read()
	f.close()
	return data

def main(args):
	stdout.write('New Project Generator\n\nCopyright © 2020 Aquefir\n' +
		'Released under BSD-2-Clause.\n\n')
	projdir = ''
	if recv_yn('Is the project in the CWD?'):
		from os import getcwd
		projdir = getcwd()
	else:
		from os.path import expanduser
		projdir = expanduser(recv_line('Okay, where is the project root?'))
	mkfilesdir = ''
	if recv_yn('Can the Aquefir standard Makefiles be found in ' +
		'/usr/local/share?'):
		mkfilesdir = '/usr/local/share/aquefir/makefiles'
	else:
		mkfilesdir = recv_line('Okay, where can they be found?')
	codename = recv_line('What is the project’s codename?')
	fullname = recv_line('What is the project’s full name?')
	if len(fullname) % 2 == 1:
		fullname += ' '
	copyholder = recv_line('Who is the project’s copyright holder?')
	copydates = recv_line('What is the copyright timespan by the years?')
	if len(copydates) % 2 == 1:
		# copyholder len must be even
		if len(copyholder) % 2 == 1:
			copyholder += ' '
	else:
		# copyholder len must be odd
		if len(copyholder) % 2 == 0:
			copyholder += ' '
	licblurb = ''
	lic = 'custom'
	if recv_yn('Is this proprietary?'):
		licblurb = 'All rights reserved.'
		lic = 'prop'
	elif recv_yn('Is this BSD-2-Clause?'):
		licblurb = 'Released under BSD-2-Clause.'
		lic = 'bsd'
	elif recv_yn('Is this Affero GPLv3?'):
		licblurb = 'Released under GNU AGPLv3.'
		lic = 'agpl3'
	else:
		licblurb = recv_line('Please provide a short licence blurb:')
		if len(licblurb) % 2 == 1:
			licblurb += ' '
	lines = ['', '', '']
	lines[0] = center74(fullname)
	lines[1] = center74('Copyright © ' + copydates + ' ' + copyholder)
	lines[2] = center74(licblurb)
	stdout.write('\nOkay.\n')
	stdout.write('Here’s a preview of how the boilerplate will look:\n')
	stdout.flush()
	boiler_c = decorate_c(lines)
	boiler_sh = decorate_sh(lines)
	stdout.write('\nC style:\n\n' + boiler_c + '\n\nShell style:\n\n'
		+ boiler_sh + '\n\n')
	stdout.flush()
	if not recv_yn('Looks alright?'):
		return 0
	stdout.write('Alright.\n\nReady to write files. Please confirm each.\n')
	stdout.flush()
	if recv_yn('Write BOILERPLATE?'):
		writelocal(projdir,
			'BOILERPLATE',
			'This file contains the project’s copypastable boilerplate' +
			' comment headers.\n\nBoilerplate for C-like languages:\n\n' +
			boiler_c + '\n\nHash-based boilerplate (Python, POSIX shell' +
			', Makefile):\n\n' + boiler_sh + '\n')
	if lic != 'custom' and recv_yn('Write COPYING?'):
		text = ''
		if lic == 'bsd':
			text = readlocal('COPYING.bsd').replace('<year>',
				copydates).replace('<holder>', copyholder)
		elif lic == 'agpl3':
			text = readlocal('COPYING.agpl3')
		else:
			# proprietary
			text = fullname + '\n\nCopyright © ' + copydates + ' ' + copyholder \
				+ '\nAll rights reserved.\n'
		writelocal(projdir, 'COPYING', text)
	if recv_yn('Write .clang-format?'):
		writelocal(projdir, '.clang-format', readlocal('clang-format'))
	if recv_yn('Write .gitignore?'):
		writelocal(projdir, '.gitignore', readlocal('gitignore'))
	from os import mkdir, path
	if recv_yn('Create 3rdparty/ folder?'):
		mkdir(path.join(projdir, '3rdparty'))
		f = open(path.join(projdir, '3rdparty', 'README'), 'w')
		f.flush()
		f.close()
	if recv_yn('Create src/ folder?'):
		mkdir(path.join(projdir, 'src'))
	if recv_yn('Create include/ folders?'):
		mkdir(path.join(projdir, 'include'))
		mkdir(path.join(projdir, 'include', codename))
	if recv_yn('Create doc/ folders?'):
		mkdir(path.join(projdir, 'doc'))
		mkdir(path.join(projdir, 'doc', codename))
	if recv_yn('Create standard Makefiles?'):
		writelocal(projdir, 'base.mk', readfar(path.join(mkfilesdir,
			'base.mk')))
		writelocal(projdir, 'targets.mk', readfar(path.join(mkfilesdir,
			'targets.mk')))
		if recv_yn('Is this project for an executable?'):
			writelocal(projdir, 'Makefile', readfar(path.join(mkfilesdir,
				'Makefile.program')))
		elif recv_yn('Okay, is this project for a library?'):
			writelocal(projdir, 'Makefile', readfar(path.join(mkfilesdir,
				'Makefile.library')))
	if recv_yn('Create README stub?'):
		writelocal(projdir, 'README', '*****\n\n' + fullname + '\n\n' +
			'Copyright © ' + copydates + ' ' + copyholder + '\n' + licblurb +
			'\n\n*****\n')
	return 0

if __name__ == '__main__':
	from sys import argv, exit
	exit(main(argv))
