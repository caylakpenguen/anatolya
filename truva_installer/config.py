		#Kurulum sonrasi ayarlari yapiliyor
		setup_1 = ('chroot %s /sbin/ldconfig' %mntdir)
		os.system(setup_1)
		
		setup_2 = ('chroot %s /usr/X11R6/bin/fc-cache -f' %mntdir)
		os.system(setup_2)
		
		shutil.copyfile("/truva_installer/files/rc.keymap","%s/etc/rc.d/rc.keymap" %mntdir)
			
		setup_3 = ('chmod 755 %s/etc/rc.d/rc.keymap' %mntdir)
		os.system(setup_3)
		
		shutil.copyfile("/truva_installer/files/rc.font","%s/etc/rc.d/rc.font" %mntdir)
				
		setup_4 = ('chmod 755 %s/etc/rc.d/rc.font' %mntdir)
		os.system(setup_4)
		
		setup_5 = ('chmod 755 %s/etc/rc.d/rc.postinstall' %mntdir)
		os.system(setup_5)
		
		setup_6 = ('chmod 755 %s/etc/rc.d/rc.messagebus' %mntdir)
		os.system(setup_6)
		
		setup_7 = ('chmod 755 %s/etc/rc.d/rc.hald' %mntdir)
		os.system(setup_7)
		
		shutil.copyfile("/truva_installer/files/fstab","%s/etc/fstab" %mntdir)
