#!/usr/bin/env python
# -*- coding: UTF8 -*-
# Based on:
# Main menu program for installing/upgrading Nonux on harddisk 
# Author: Marcel J. Zwiebel <http://www.nnlinux.com>
# Adapted to SLAMPP by Kemas Antonius <http://truva.abangadek.com/>
# Düzenleyenler : Onur ÖZDEMİR - Atlantis
#                 Daron DEDEOĞLU - T-ReX
#                 http://www.truvalinux.org.tr 


import os
import gtk
import time
import gobject
import array
from SimpleGladeApp import SimpleGladeApp

glade_dir = ""
g_activepid = 0
g_exedir = '/truva_installer'
g_arrowcount = 0


def runbg( self, program, *args ):
	return os.spawnvp( os.P_NOWAIT, program, (program,) + args )


def execute_install( device ):
	global g_activepid
	global g_exedir
	exedir = g_exedir

	statfile = ( '%s/stat' % exedir )
	if os.access( statfile, os.F_OK ) == 1:
		os.remove( statfile )

	oscmd = ( 'echo "0" > %s/pid' % exedir ) 
	os.system( oscmd )
	
	oscmd = ( '%(exedir)s/install_run.py -g --device=%(device)s &' % vars() )
	os.system( oscmd )
	
	if os.access( statfile, os.F_OK ) == 0:
		time.sleep(1)
	if os.access( statfile, os.F_OK ) == 0:
		time.sleep(1)
	if os.access( statfile, os.F_OK ) == 0:
		time.sleep(1)
	if os.access( statfile, os.F_OK ) == 0:
		time.sleep(1)
	if os.access( statfile, os.F_OK ) == 0:
		time.sleep(1)

	if os.access( statfile, os.F_OK ) == 0:
		if ( pid_active() == False ):
			return False;
		else:	
			return True	
	else:
		return True	

		
def pid_read():
	global g_activepid
	global g_exedir
	exedir = g_exedir

	pidfile = ( '%s/pid' % exedir )
	if os.access( pidfile, os.F_OK ) == 1:
		oscmd = ( 'cat %s' % pidfile )
		pidnum = os.popen( oscmd )
		pid = pidnum.readline()
		pid = pid.strip()
		g_activepid = int(pid)
		

def pid_active():
	global g_activepid
	retval = False
	
	if ( g_activepid == 0 ):
		pid_read()

	if ( g_activepid != 0 ):
		pidlist = os.popen( 'ps -A | grep %s' % g_activepid )
		pidcheck = pidlist.readline()
		if ( pidcheck != '' ):
			retval = True
	return retval		
			

def check_status( pobj ):
	global g_exedir
	
	exedir = g_exedir
	
	if ( pid_active() == False ):
		pobj.busyprogress.hide()
	
	statfile = ( '%s/stat' % exedir )
	if os.access( statfile, os.F_OK ) == 1:
		oscmd = ( 'cat %s' % statfile )
		stattxt = os.popen( oscmd )
		statmsg = stattxt.read()
		pobj.text.set_text( statmsg ) 
		pobj.busyprogress.pulse()
	
	if ( pid_active() == True ):
		pobj.busyprogress.show()
		return True


class truvaLinuxInstall(SimpleGladeApp):
	def __init__(self, glade_path="truva_install.glade", root="truvalinux_install", domain=None):
		glade_path = os.path.join(glade_dir, glade_path)
		SimpleGladeApp.__init__(self, glade_path, root, domain)
		self._buttonfunc = 1
		self._mntdir = '/truva_installer/mount'
		self._partname = {}
		self._osname = {}
		
	def new(self):
		self.partcombo.hide()
		self.button_cancel.grab_focus()
	 
	def run_install(self):	
		self.button_start.hide()
		self.truvalinux_install.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

		partition = os.popen("fdisk -l | grep /dev/ | grep -iv Disk | grep -iv Swap | grep -iv Ext | cut -d ' ' -f1")
		filesystem = os.popen("fdisk -l | grep /dev/ | grep -iv Disk | grep -iv Swap | grep -iv Ext")

		partname = partition.readline()
		osname = filesystem.readline()

		self.list = gtk.ListStore(int, str)
		cbidx = 0

		mntdir = self._mntdir

		while partname:
			partname = partname.strip()
			mntcmd = 'mount %(partname)s %(mntdir)s' % vars()
			os.system( mntcmd )
			osname = osname.strip()

			# check for Windows primary partitions
			is_win_part = False			
			parttype = osname[52:54]
			parttype = parttype.strip()
			# windows partition types (no hidden ones)
			if ( parttype == '6' or parttype == '7' or parttype == 'b' or parttype == 'c' or parttype == 'e'):
				is_win_part = True
				# check if primary partition 
				primaries = os.popen( 'parted %s print | grep prima' % partname[:8] )		
				primname = primaries.readline()
				primname = primname.strip()
				if ( primname != '' ):
					is_win_part = False
					while primname:
						ppnr = primname[:2]
						if ( ppnr.strip() == partname[8] ):
							is_win_part = True
						primname = primaries.readline()

			osname = osname[-(len(osname)-56): ]
			if ( is_win_part == True ):
				osname += " (Windows)"

			sizecmd = ( 'df %s | grep /dev/ | cut -c21-30' % partname )
			psize = os.popen( sizecmd )
			partsize = psize.readline()
			partsize = partsize.strip()
			if ( (partsize == '') | (partsize=='0') ):
				partsize = int(0)
			else:
				part_gb = ( float(partsize) / (1024 * 1024) )

			if ( int(partsize) > 2000000 ):
				partshort = partname.replace( '/dev/', '' )
				cbtxt = '%(partshort)s - %(osname)s - %(#)1.1fGB'  % {'partshort':partshort, 'osname':osname, '#':part_gb}

				cbitem = self.list.append( (cbidx, cbtxt,) )
				self.list.set(cbitem)
				self._partname[cbidx] = partname
				self._osname[cbidx]= osname
				cbidx = cbidx + 1

			time.sleep(2)
			mntcmd = ( 'umount %s' % partname )
			os.system( mntcmd )
			time.sleep(1)	

			partname = partition.readline()
			osname = filesystem.readline()

		liststore = gtk.ListStore(gobject.TYPE_STRING)
		cell = gtk.CellRendererText()
		self.partcombo.pack_start(cell, True)
		self.partcombo.add_attribute(cell, 'text', 1)		
		
		self.partcombo.set_model(self.list)
		if cbidx > 0:
			self.partcombo.set_active(0)
			self.button_start.show()
			self.partcombo.show()
			self.partcombo.grab_focus()
			self.text.set_text('\nLütfen Truva Linux\'u kuracağınız disk bölümünü seçin...\n')
			self._buttonfunc = 2
		else:
			self.text.set_text('\n\nKurulumun yapılabilmesi için gerekli 3 GB\'lık disk bölümü bulunamadı.\nBu durumda kuruluma devam edilemez...\n')		

		self.truvalinux_install.window.set_cursor(None)
		
	def on_button_cancel_clicked(self, widget, *args):
		global g_activepid
		if ( pid_active() == True ):
			msgtext  = '\nKurulum süreci çalışmakta.\n'
			msgtext += 'Durdurmak istediğinizden emin misiniz?\n'
			msgdialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msgtext )
			response = msgdialog.run()
			msgdialog.destroy()
			if response == gtk.RESPONSE_YES:
				os.kill( g_activepid, 9 )
				self.truvalinux_install.destroy()
		else:		
			self.truvalinux_install.destroy()

	def on_button_start_pressed(self, widget, *args):
		if (self._buttonfunc == 1):
			self.text.set_text('\n\nLütfen bekleyin. Sistem, kurulum öncesi\ndisk bölümlerini inceliyor...\n')
			self.truvalinux_install.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

	def on_button_start_released(self, widget, *args):
		if (self._buttonfunc == 1):
			self.run_install()
		else:
			cbidx = self.partcombo.get_active()
			partname = self._partname[cbidx]
			osname = self._osname[cbidx]
			
			msgtext  = "\nTruva\'yı bu disk bölümüne kurmayı seçtiniz.\n\n"
			msgtext += partname
			msgtext += " - "
			msgtext += osname
			msgtext += "\n\nTüm veriler silinecek!\n"
			msgtext += "Bir sonraki adıma geçmek istediğinizden emin misiniz?\n"
					
			msgdialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msgtext )
			response = msgdialog.run()
			msgdialog.destroy()

			if response == gtk.RESPONSE_YES:
				msgtext  = "\nTruva Linux Kurulum Cd\'sinin takılı\n\n"
				msgtext += "olduğuna eminseniz Evet butonuna tıklayınız...\n"
						
				msgdialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msgtext )
				response = msgdialog.run()
				msgdialog.destroy()
				
				if response == gtk.RESPONSE_YES:
					self.text.set_text( '\n\nLütfen bekleyiniz...\n' )
					self.button_start.hide()
					self.button_cancel.grab_focus()
	
					self.partcombo.destroy()
					self.busyprogress.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
					self.busyprogress.set_pulse_step(0.1)
					self.busyprogress.show()
					self.timer = gobject.timeout_add (500, check_status, self)
	
					result = execute_install( partname )
					if ( result == False ):
						self.text.set_text("\nBir hata meydana geldi.\nKurulum başlatılamıyor.\nLütfen bir daha deneyin." )			
						self.button_start.show()


def main():

	truvalinux_install = truvaLinuxInstall()
	truvalinux_install.run()

if __name__ == "__main__":
	main()
