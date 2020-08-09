import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Servicio:
    def __init__(self, id, descripcion, precio):
        self.id = id
        self.descripcion = descripcion
        self.precio = precio

contadorServicio = 1
listaServicios = []

def esNumero(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False
 
class Realizar_Factura_Frame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

class Buscar_Factura_Frame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

class Eliminar_Factura_Frame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

class PDF_Factura_Frame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

class FacturaFrame(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
         
        self.notebook = ttk.Notebook(self)
        self.Realizar_Factura_Frame = Realizar_Factura_Frame(self.notebook)
        self.notebook.add(
            self.Realizar_Factura_Frame, text="Realizar Factura", padding=10)
          
        self.buscar_factura_frame = Buscar_Factura_Frame(self.notebook)
        self.notebook.add(
            self.buscar_factura_frame, text="Buscar Factura", padding=10)
          
        self.Eliminar_Factura_Frame = Eliminar_Factura_Frame(self.notebook)
        self.notebook.add(
            self.Eliminar_Factura_Frame, text="Eliminar Factura", padding=10)
          
        self.PDF_Factura_Frame = PDF_Factura_Frame(self.notebook)
        self.notebook.add(
            self.PDF_Factura_Frame, text="Generar Factura PDF", padding=10)
        
        self.notebook.pack(fill='both',padx=1, pady=1)

class GenerarReportFrame(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.label = ttk.Label(self)
        self.label["text"] = ("Visitanos en recursospython.com y "
                              "foro.recursospython.com.")
        self.label.pack(fill='both')
        
        self.web_button = ttk.Button(self, text="Visitar web")
        self.web_button.pack(fill='both',pady=10)
        
        self.forum_button = ttk.Button(self, text="Visitar foro")
        self.forum_button.pack(fill='both')


class Agregar_Servicio_Frame(ttk.Frame): 
    
    def agregarServicio(self): 
        global esNumero
        global listaServicios
        global contadorServicio

        if bool(self.txt_descripcion.get().strip()):  
            if esNumero(self.txt_precio.get()):  
                listaServicios.append(Servicio(contadorServicio, self.txt_descripcion.get(), self.txt_precio.get())) 
                contadorServicio += 1
                self.txt_descripcion.delete(0, 'end')
                self.txt_precio.delete(0, 'end')

                messagebox.showinfo(title=None, message="Servicio agregado satisfactoriamente")
            else:
                messagebox.showinfo(title=None, message="El campo Precio es un numero")
        else:
            messagebox.showinfo(title=None, message="El campo Descripcion es obligatorio")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.lbl_descripcion = ttk.Label(self, text="Descripcion") 
        self.lbl_descripcion.grid(column=0, row=0) 
        self.txt_descripcion = ttk.Entry(self,width=10) 
        self.txt_descripcion.grid(column=1, row=0)

        self.lbl_precio = ttk.Label(self, text="Precio") 
        self.lbl_precio.grid(column=0, row=1) 
        self.txt_precio = ttk.Entry(self,width=10) 
        self.txt_precio.grid(column=1, row=1) 

        self.btn_insertar_servicio = ttk.Button(self, text = "Insertar", command = self.agregarServicio) 
        self.btn_insertar_servicio.grid(column=1, row=2) 


class Actualizar_Servicio_Frame(ttk.Frame):
    def refrescarCmb(self):
        global listaServicios

        lista_ID = []
        for servicio in listaServicios:
            lista_ID.append(servicio.id)

        self.cmb_id['values'] = lista_ID

    def modified (self, event):
        global listaServicios 
         
        for servicio in listaServicios:
            if servicio.id == (int)(self.cmb_id.get()):  
                self.txt_descripcion_upd.delete(0, 'end')
                self.txt_descripcion_upd.insert(0,servicio.descripcion)
                self.txt_precio_upd.delete(0, 'end')
                self.txt_precio_upd.insert(0,servicio.precio)

    def modificarServicio(self): 
        global esNumero
        global listaServicios
        global contadorServicio
        
        if bool(self.txt_descripcion_upd.get().strip()):  
            if esNumero(self.txt_precio_upd.get()):   
                for servicio in listaServicios: 
                    if servicio.id == (int)(self.cmb_id.get()):   
                        servicio.descripcion = self.txt_descripcion_upd.get() 
                        servicio.precio = self.txt_precio_upd.get()   
                        messagebox.showinfo(title=None, message="Servicio modificado satisfactoriamente") 
            else:
                messagebox.showinfo(title=None, message="El campo Precio es un numero")
        else:
            messagebox.showinfo(title=None, message="El campo Descripcion es obligatorio")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        global listaServicios

        lista_ID = []
        for servicio in listaServicios:
            lista_ID.append(servicio.id)
        self.lbl_id = ttk.Label(self, text="Id") 
        self.lbl_id.grid(column=0, row=0) 
        self.cmb_id = ttk.Combobox(self, value=lista_ID, postcommand = self.refrescarCmb)     
        self.cmb_id.grid(column=1, row=0)
        #self.cmb_id.bind("<FocusIn>", self.refrescarCmb)
        self.cmb_id.bind('<<ComboboxSelected>>', self.modified)    
        
        self.lbl_descripcion_upd = ttk.Label(self, text="Descripcion") 
        self.lbl_descripcion_upd.grid(column=0, row=1) 
        self.txt_descripcion_upd = ttk.Entry(self,width=10) 
        self.txt_descripcion_upd.grid(column=1, row=1)

        self.lbl_precio_upd = ttk.Label(self, text="Precio") 
        self.lbl_precio_upd.grid(column=0, row=2) 
        self.txt_precio_upd = ttk.Entry(self,width=10) 
        self.txt_precio_upd.grid(column=1, row=2) 

        self.btn_actualizar_servicio = ttk.Button(self, text = "Actualizar", command = self.modificarServicio) 
        self.btn_actualizar_servicio.grid(column=1, row=3) 

class ServicioFrame(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
         
        self.notebook = ttk.Notebook(self)
        self.Agregar_Servicio_Frame = Agregar_Servicio_Frame(self.notebook)
        self.notebook.add(
            self.Agregar_Servicio_Frame, text="Agregar Servicio", padding=10)
          
        self.Actualizar_Servicio_Frame = Actualizar_Servicio_Frame(self.notebook)
        self.notebook.add(
            self.Actualizar_Servicio_Frame, text="Actualizar Servicio", padding=10) 
        
        self.notebook.pack(fill='both', padx=1, pady=1)

class Application(ttk.Frame): 
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Panel de pestañas en Tcl/Tk")
        
        self.notebook = ttk.Notebook(self)
        
        self.factura_Frame = FacturaFrame(self.notebook)
        self.notebook.add(
            self.factura_Frame, text="Factura", padding=0)
        
        self.generar_Reporte_Frame = GenerarReportFrame(self.notebook)
        self.notebook.add(
            self.generar_Reporte_Frame, text="Generar Informe", padding=0)
        
        self.ServicioFrame = ServicioFrame(self.notebook)
        self.notebook.add(
            self.ServicioFrame, text="Servicios", padding=0)
        
        self.notebook.pack(fill='both',padx=1, pady=1, anchor = "s")
        self.pack(fill='both')

listaServicios.append(Servicio(90, "Desc1", 456)) 
listaServicios.append(Servicio(91, "Desc2", 456)) 
listaServicios.append(Servicio(92, "Desc3", 456)) 
listaServicios.append(Servicio(93, "Desc4", 456)) 
main_window = tk.Tk()
app = Application(main_window)
app.mainloop()