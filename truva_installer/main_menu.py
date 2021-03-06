#!/usr/bin/env python
# -*- coding: UTF8 -*-
# Based on:
# Main menu program for installing/upgrading Nonux on harddisk 
# Author: Marcel J. Zwiebel <http://www.nnlinux.com>
# Adapted to SLAMPP by Kemas Antonius <http://slampp.abangadek.com/>
# Düzenleyenler : Onur ÖZDEMİR - Atlantis
#                 Daron DEDEOĞLU - T-ReX
#                 http://www.truvalinux.org.tr 

import os
import gtk
from SimpleGladeApp import SimpleGladeApp

glade_dir = ""

class truvaInstall(SimpleGladeApp):
	def __init__(self, glade_path="truva_hd_installer_menu.glade", root="truva_install", domain=None):
		glade_path = os.path.join(glade_dir, glade_path)
		SimpleGladeApp.__init__(self, glade_path, root, domain)
		self._exedir = '/truva_installer'

	def on_install_clicked(self, widget, *args):
		msgtext  = "KURULUMA BAŞLAMADAN ÖNCE\n\n"
		msgtext += "Başarılı bir kurulum için ihtiyacınız olan\n"
		msgtext += "boş disk alanı miktarı en az 3 GB olmalıdır.\n"
		msgtext += "Eğer Truva'yı başka bir sistemle birlikte kullanmak\n"
		msgtext += "istiyorsanız (mesela Windows) mutlaka boş bir\n"
		msgtext += "disk bölümü oluşturmalısınız...\n"
		msgdialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msgtext )
		msgdialog.run()
		msgdialog.destroy()
		os.system( '%s/install.py &' % self._exedir )
		self.quit()

	def on_gparted_clicked(self, widget, *args):
		msgtext  = "DİSK BÖLÜMLEME\n\n"
		msgtext += "Disk bölümleme programı GParted sayesinde\n"
		msgtext += "diskinizi kolayca bölümleyebilirsiniz. Bu yazılım\n"
		msgtext += "sabit disk bölümleme tablonuzu ve dosya formatınızı\n"
		msgtext += "değiştirebileceğinden çok dikkatli bir şekilde\n"
		msgtext += "kullanmanız gerekiyor. Başlamadan önce mevcut \n"
		msgtext += "sisteminizin bir yedeğini almanızı tavsiye ederiz.\n"
		msgtext += "Dilerseniz başka bir bölümleme yazılımı da \n"
		msgtext += "kullanabilirsiniz ama GParted kadar kolay bir \n"
		msgtext += "bölümleyici bulmanız oldukça zor. Kurulum için \n"
		msgtext += "en az 3 GB boş alana sahip bir bölüme ihtiyacınız\n"
		msgtext += "var. Öncelikle kuruluma uygun bir bölüm oluşturmanızı\n"
		msgtext += "rica ederiz."
		msgdialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msgtext )
		msgdialog.run()
		msgdialog.destroy()
		os.system( 'gparted &' )
		
	def on_about_clicked(self, widget, *args):		
		self.textview1.show()

def main():
	truva_install = truvaInstall()

	truva_install.run()

if __name__ == "__main__":
	main()
