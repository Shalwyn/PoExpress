import pygtk

def on_file(self, widget):
   dlg = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
      (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
   response = dlg.run()
   self.text.set_text(dlg.get_filename())
   dlg.destroy()