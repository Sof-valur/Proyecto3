import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkintertable import Tables
import webbrowser
import pdfkit
import json
import os
import datetime

### The purpose of this class is to create objects with the information that a service requires ###
class Servicio:
    def __init__(self, id, descripcion, precio):
        self.id = id
        self.descripcion = descripcion
        self.precio = precio

### The purpose of this class is to create objects with the information that invoice requires ###
class Factura:
    def __init__(self, customerName, customerEmail, invoiceNumber, sentDate, dueDate, notes, items, subtotal):
        self.customerName = customerName 
        self.customerEmail = customerEmail 
        self.invoiceNumber = invoiceNumber 
        self.sentDate = sentDate 
        self.dueDate = dueDate 
        self.notes = notes 
        self.items = items 
        self.subtotal = subtotal 
        self.tax = subtotal * 0.13
        self.total = self.subtotal + self.tax 
         
### The purpose of this function is to retrieve the consecutive of the invoice ###
def consecutivoFactura():
    file1 = open('consecutivoFactura.txt', 'r+')
    consecutivo = file1.read(100000000)
    consecutivo = int(consecutivo) + 1
    lines = []

    with open("consecutivoFactura.txt", "r") as infile:
        lines = infile.readlines()

    with open("consecutivoFactura.txt", "w") as outfile:
        for pos, line in enumerate(lines): 
            outfile.write(str(consecutivo)) 

    file1.close()
    return consecutivo

### The purpose of this class is to create objects with the properties that an item requires ###
class Item:
    def __init__(self, id, item, quantity, price, amount):
        self.id = id 
        self.item = item 
        self.quantity = quantity 
        self.price = price 
        self.amount = amount 

### Global variables ###
contadorServicio = 1
listaServicios = []
contadorFactura = 1
listaFactura = []

### This function receives a value and determines if that value is a number ### 
def esNumero(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

###  This is the frame in the main page where you can create an invoice ###
class Realizar_Factura_Frame(ttk.Frame):
 
    def cell(self, event, e = None):
        '''Identify cell from mouse position'''
        row, col = self.tv_factura.identify_row(e.y), self.tv_factura.identify_column(e.x)
        pos = self.tv_factura.bbox(row, col)       # Calculate positon of entry
        return row, col, pos

    def single(self, event=None):
        '''Single click to select row and column'''
        global row, col, pos
        row, col, pos = self.cell(self, event)
        print('Select', row, col)

    def ok(self, event=None):
        '''Validate entry as at loses focus'''
        try:             
            self.tv_factura.set(*item, self.typed.get())    # Set tree cell text
            self.entry.place_forget()            # Remove entry without deleting it
        except :
            print('Display Row Cannot be set . . .')

    def double(self, event=None, e = None):
        '''Double click to edit cell'''
        global row, col, pos, item
        row, col, pos = self.cell(event, event)
        print('Edit', row, col)
        item = row, col                 # Remember which item you are editing
        self.typed.set(self.tv_factura.set(row, col))   # Set entry text
        x, y, w, h = pos                # Place entry on tree
        self.entry.place(x=x, y=y, width=w, height=h, anchor='nw')
        self.entry.focus_set() 

    def deleterow(self, event):
        '''Delete selected row'''
        print('delete', len(self.tv_factura.selection()))
        if len(self.tv_factura.selection()) != 0:
            row = self.tv_factura.selection()[0]
        try:
            print('deleterow', row)
            self.tv_factura.delete(row)
        except:
            print('no row selected') 

    def refrescarCmb(self):
        global listaServicios

        lista_ID = []
        for servicio in listaServicios:
            lista_ID.append(servicio.descripcion)

        self.cmb_Item['values'] = lista_ID

    def modified (self, event):
        global listaServicios 
         
        for servicio in listaServicios:
            if servicio.descripcion == (str)(self.cmb_Item.get()): 
                cantidad = 0
                if esNumero(self.txt_quantity.get()):
                    cantidad = int(self.txt_quantity.get())
                self.txt_precio.config(state=NORMAL)
                self.txt_amount.config(state=NORMAL)
                self.txt_precio.delete(0, 'end') 
                self.txt_amount.delete(0, 'end') 
                self.txt_precio.insert(0,servicio.precio) 
                self.txt_amount.insert(0,servicio.precio * cantidad)  
                self.txt_precio.config(state=DISABLED)
                self.txt_amount.config(state=DISABLED)
    
    def agregarItem(self): 
        global listaServicios  
        global contadorFactura  

        cont = 0
        for child in self.tv_factura.get_children():
            print(self.tv_factura.identify_row(cont))
            print(self.tv_factura.item(child)["values"])
            cont += 1
        if esNumero(self.txt_quantity.get()): 
            for servicio in listaServicios:
                if servicio.descripcion == (str)(self.cmb_Item.get()):  
                    cantidad = int(self.txt_quantity.get())
                    self.txt_precio.config(state=NORMAL)
                    self.txt_amount.config(state=NORMAL) 
                    self.txt_precio.delete(0, 'end') 
                    self.txt_amount.delete(0, 'end') 

                    self.txt_precio.insert(0,servicio.precio) 
                    self.txt_amount.insert(0,servicio.precio * cantidad)  
                    self.txt_precio.config(state=DISABLED)
                    self.txt_amount.config(state=DISABLED)
                    self.tv_factura.insert("", tk.END, text="" + str(contadorFactura), values=(self.cmb_Item.get(), self.txt_quantity.get(), self.txt_precio.get(), self.txt_amount.get()))
                    contadorFactura += 1
        else:
            messagebox.showinfo(title=None, message="El campo Cantidad tiene que ser numero.") 
    
    def agregarFactura(self): 
        global listaServicios  
        global contadorFactura  
        global consecutivoFactura
        continuar = True
        try:
            x = datetime.datetime.strptime(self.txt_Sentdate.get(), "%d/%m/%Y")
        except Exception as e:
            messagebox.showinfo(title=None, message="El campo Sent Date tiene que tener formato dd/mm/YYYY") 
            continuar = False
            pass        
        try:
            x1 = datetime.datetime.strptime(self.txt_Duedate.get(), "%d/%m/%Y")
        except Exception as e:
            messagebox.showinfo(title=None, message="El campo Due Date tiene que tener formato dd/mm/YYYY") 
            continuar = False
            pass
        
        if continuar:
            if abs((x - x1).days) > 3 or abs((x - x1).days) < 0: 
                messagebox.showinfo(title=None, message="La fecha de vencimiento debe de ser maximo 3 dias despues de la fecha de creacion. Actualmente: " + str(abs((x - x1).days))) 
                continuar = False

        if len(self.txt_CustomerName.get().strip()) == 0:
            messagebox.showinfo(title=None, message="Campo Customer Name es obligatorio") 
            continuar = False

        if len(self.txt_CustomerEmail.get().strip()) == 0:
            messagebox.showinfo(title=None, message="Campo Customer Email es obligatorio") 
            continuar = False

        if len(self.tv_factura.get_children()) == 0:
            messagebox.showinfo(title=None, message="Agregue al menos un servicio") 
            continuar = False
        if continuar:   
            consecutivo = consecutivoFactura()
            listaItems = []
            total = 0;
            cont = 1
            for child in self.tv_factura.get_children(): 
                print(self.tv_factura.item(child)["values"])
                items = self.tv_factura.item(child)["values"]
                listaItems.append(Item(cont,items[0],items[1],items[2],items[3])) 
                total += int(items[3]) 
                cont += 1

            factura = Factura(self.txt_CustomerName.get(),
                    self.txt_CustomerEmail.get(),
                    consecutivo,
                    self.txt_Sentdate.get(),
                    self.txt_Duedate.get(),
                    self.txt_Notes.get(),
                    listaItems,
                    total) 

        
            f = open('factura.html','wb')

            message = """
        
            <!DOCTYPE html>

            <html lang='en' xmlns='http://www.w3.org/1999/xhtml'>
            <head>
                <meta charset='utf-8' />
                <title></title>
            </head>
            <body>
                <h1>Empresa 3C</h1>
                <table>
                    <tr>
                        <td>Invoice</td>
                        <td style='float: right'>""" + str(factura.invoiceNumber) + """</td> 
                    </tr>
                    <tr>
                        <td>""" + factura.customerName + """</td>
                        <td style='float: right'>Sent: """ + factura.sentDate  + """</td>
                    </tr>
                    <tr>
                        <td>""" + factura.customerEmail   + """</td>
                        <td style='float: right'>Due: """ + factura.dueDate    + """</td>
                    </tr>
                </table>

                <hr />
                <H4>""" + factura.notes     + """</H4>
                <hr /> 

                <table border='1'>
                    <thead>
                        <tr>
                            <td>Item</td>
                            <td>Quantity</td>
                            <td>Price</td>
                            <td>Amount</td>
                        </tr>
                    </thead>
                    <tbody>"""

            for item in factura.items:
                message +=  """<tr>
                            <td>""" + str(item.item) + """</td>
                            <td>""" + str(item.quantity) + """</td>
                            <td>""" + str(item.price) + """</td>
                            <td>""" + str(item.amount) + """</td>
                        </tr>""" 
            message += """
                    </tbody>
                    <tfoot>
                        <tr>
                            <td></td>
                            <td></td>
                            <td>Subtotal</td>
                            <td>""" + str(factura.subtotal) + """</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td></td>
                            <td>Tax</td>
                            <td>""" + str(factura.tax) + """</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td></td>
                            <td>Total</td>
                            <td>""" + str(factura.total) + """</td>
                        </tr>
                    </tfoot>
                </table>
            </body>
            </html>  
            """

            f.write(message.encode(encoding='UTF-8'))
            f.close()
        
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            try:
                pdfkit.from_url('factura.html', 'facturas/factura' + str(factura.invoiceNumber) + '.pdf', configuration=config)
            except Exception as e:  
                messagebox.showinfo(title=None, message="Error al generarPDF, por favor cierre el archivo si lo tiene abierto. \n" + str(e)) 
            webbrowser.open('file://C:/Users/ExtremeTech/source/repos/Proyecto3/facturas/factura' + str(factura.invoiceNumber) + '.pdf')
         
            data = {} 
            with open('facturas.json') as json_file:
                data = json.load(json_file)
        
            itemList = []

            for item in factura.items :
                itemList.append([str(item.id), str(item.item), str(item.quantity), str(item.price), str(item.amount) ])

            data['facturas'].append({
                'customerName': factura.customerName,
                'customerEmail': factura.customerEmail ,
                'invoiceNumber': factura.invoiceNumber ,
                'sentDate': factura.sentDate ,
                'dueDate': factura.dueDate ,
                'notes': factura.notes ,
                'items': itemList  ,
                'subtotal': factura.subtotal ,
                'tax': factura.tax ,
                'total': factura.total
            })

            with open('facturas.json', 'w') as outfile:
                json.dump(data, outfile) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        global listaServicios

        lista_ID = []
        for servicio in listaServicios:
            lista_ID.append(servicio.descripcion)
        
        self.lbl_CustomerName = ttk.Label(self, text="Customer Information") 
        self.lbl_CustomerName.pack(side=tk.TOP, expand=True) 

        self.pnl_CustomerInfo = ttk.Frame(self)
        self.pnl_CustomerInfo.pack(side=tk.TOP, expand=True,fill=tk.X,)  

        self.lbl_CustomerName = ttk.Label(self.pnl_CustomerInfo, text="Customer Name") 
        self.lbl_CustomerName.grid(column=0, row=1, sticky=N+S+E+W)
        self.txt_CustomerName = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_CustomerName.grid(column=1, row=1, sticky=N+S+E+W)

        self.lbl_CustomerEmail = ttk.Label(self.pnl_CustomerInfo, text="Customer Email") 
        self.lbl_CustomerEmail.grid(column=0, row=2, sticky=N+S+E+W)
        self.txt_CustomerEmail = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_CustomerEmail.grid(column=1, row=2, sticky=N+S+E+W)

        #self.lbl_InvoiceN = ttk.Label(self.pnl_CustomerInfo, text="Invoice Number") 
        #self.lbl_InvoiceN.grid(column=8, row=1, sticky=N+S+E+W, padx=100)
        #self.txt_InvoiceN = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        #self.txt_InvoiceN.grid(column=9, row=1, sticky=N+S+E+W) 
        
        self.lbl_Sentdate = ttk.Label(self.pnl_CustomerInfo, text="Sent Date") 
        self.lbl_Sentdate.grid(column=8, row=1, sticky=N+S+E+W, padx=100)
        self.txt_Sentdate = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_Sentdate.grid(column=9, row=1, sticky=N+S+E+W)
        
        self.lbl_Duedate = ttk.Label(self.pnl_CustomerInfo, text="Due Date") 
        self.lbl_Duedate.grid(column=8, row=2, sticky=N+S+E+W, padx=100)
        self.txt_Duedate = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_Duedate.grid(column=9, row=2, sticky=N+S+E+W)

        
        self.lbl_Notes = ttk.Label(self, text="Notes") 
        self.lbl_Notes.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.txt_Notes = ttk.Entry(self)
        self.txt_Notes.pack(side = TOP, fill = X)

        
        self.lbl_AgregarItem = ttk.Label(self, text="Agregar Item") 
        self.lbl_AgregarItem.pack(side=tk.TOP, expand=True) 

        self.sptr_1 = ttk.Separator(self, orient=HORIZONTAL)
        self.sptr_1.pack(side = TOP, fill = X, padx=5)

        self.lbl_descripcion = ttk.Label(self, text="Item") 
        self.lbl_descripcion.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.cmb_Item = ttk.Combobox(self, value=lista_ID, postcommand = self.refrescarCmb)     
        self.cmb_Item.pack(side=tk.TOP, fill=tk.X, padx=5)
        #self.cmb_id.bind("<FocusIn>", self.refrescarCmb)
        self.cmb_Item.bind('<<ComboboxSelected>>', self.modified)    

        self.lbl_Quantity = ttk.Label(self, text="Quantity") 
        self.lbl_Quantity.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.txt_quantity = ttk.Entry(self,width=10) 
        self.txt_quantity.pack(side=tk.TOP, fill=tk.X, padx=5)

        self.lbl_precio = ttk.Label(self, text="Price")
        self.lbl_precio.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.txt_precio = ttk.Entry(self,width=10, state='disabled')  
        self.txt_precio.pack(side=tk.TOP, fill=tk.X, padx=5)

        self.lbl_amount = ttk.Label(self, text="Amount") 
        self.lbl_amount.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.txt_amount = ttk.Entry(self,width=10, state='disabled') 
        self.txt_amount.pack(side=tk.TOP, fill=tk.X, padx=5)

        self.btn_agregar = ttk.Button(self, text="Agregar",command = self.agregarItem)
        self.btn_agregar.pack(side = TOP, fill = X)

        self.tv_factura = ttk.Treeview(self, columns=("item","Quantity", "Price", "Amount"))
        self.tv_factura.heading("#0", text="#")
        self.tv_factura.column("#0", minwidth=0, width=50, stretch=NO)
        self.tv_factura.heading("item", text="item")
        self.tv_factura.heading("Quantity", text="Quantity")
        self.tv_factura.heading("Price", text="Price")
        self.tv_factura.heading("Amount", text="Amount")

        self.tv_factura.bind('<1>', self.single)
        self.tv_factura.bind('<Double-Button-1>', self.double)
        self.tv_factura.bind("<Delete>", self.deleterow)

        self.btn_crearFactura = ttk.Button(self, text="Crear Factura",command = self.agregarFactura)
        self.btn_crearFactura.pack(side = BOTTOM, fill = X)
        self.tv_factura.pack( side = BOTTOM )

        self.typed = tk.StringVar()
        self.entry = ttk.Entry( self.tv_factura, textvariable=self.typed)
        self.entry.bind('<FocusOut>', self.ok) 

class Buscar_Factura_Frame(ttk.Frame): 
 

    def cell(self, event, e = None):
        '''Identify cell from mouse position'''
        row, col = self.tv_factura.identify_row(e.y), self.tv_factura.identify_column(e.x)
        pos = self.tv_factura.bbox(row, col)       # Calculate positon of entry
        return row, col, pos

    def single(self, event=None):
        '''Single click to select row and column'''
        global row, col, pos
        row, col, pos = self.cell(self, event)
        print('Select', row, col) 

    def getFacturas(self, e=None):
        data = {}  
        with open('facturas.json') as json_file:
            data = json.load(json_file) 

        list = []
        for x in data["facturas"]:
            print(x)
            print('Name: ' + str(x['customerName']))
            print('Website: ' + str(x['invoiceNumber']))
            print('From: ' + str(x['total']))
            print('')  
            list.append([x['customerName'],
                x['invoiceNumber'],
                x['total'],
                x['dueDate']])
        return list

    def get_numeroFactura(self,factura):
        return factura[1];

    def refrescarTV(self): 

        continuar = True

        try:
            fechaInicio = datetime.datetime.strptime(self.txt_FechaInicio.get(), "%d/%m/%Y")
        except Exception as e:
            messagebox.showinfo(title=None, message="El campo FechaInicio tiene que tener formato dd/mm/YYYY") 
            continuar = False
            pass        
        try:
            fechaFinal = datetime.datetime.strptime(self.txt_FechaFinal.get(), "%d/%m/%Y")
        except Exception as e:
            messagebox.showinfo(title=None, message="El campo Due Date tiene que tener formato dd/mm/YYYY") 
            continuar = False
            pass 
        
        if fechaFinal < fechaInicio: 
            messagebox.showinfo(title=None, message="La fecha final no debe de ser menor a la fecha inicial") 
            continuar = False

        if continuar: 
            for x in self.tv_factura.get_children():
                self.tv_factura.delete(x)

            listaFacturas = self.getFacturas() 
            numeroCont = 1
            listaFacturas.sort(key=self.get_numeroFactura)
            for x in listaFacturas:
                if fechaInicio <= datetime.datetime.strptime(x[3], "%d/%m/%Y") <= fechaFinal: 
                    self.tv_factura.insert("", tk.END, text="" + str(numeroCont), values=(x[0], x[1], x[2], x[3]))
                    numeroCont += 1

    def getAll(self): 
        for x in self.tv_factura.get_children():
            self.tv_factura.delete(x)

        listaFacturas = self.getFacturas() 
        numeroCont = 1
        listaFacturas.sort(key=self.get_numeroFactura)
        for x in listaFacturas: 
            self.tv_factura.insert("", tk.END, text="" + str(numeroCont), values=(x[0], x[1], x[2], x[3]))
            numeroCont += 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        global listaServicios

        listaFacturas = self.getFacturas() 
        
        self.pnl_CustomerInfo = ttk.Frame(self)
        self.pnl_CustomerInfo.pack(fill=X, expand=0)

        self.lbl_FechaInicio = ttk.Label(self.pnl_CustomerInfo, text="Fecha Inicio") 
        self.lbl_FechaInicio.grid(column=0, row=1, sticky=N+S+E+W)
        self.txt_FechaInicio = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_FechaInicio.grid(column=1, row=1, sticky=N+S+E+W)

        self.lbl_FechaFinal = ttk.Label(self.pnl_CustomerInfo, text="Fecha Final") 
        self.lbl_FechaFinal.grid(column=0, row=2, sticky=N+S+E+W)
        self.txt_FechaFinal = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_FechaFinal.grid(column=1, row=2, sticky=N+S+E+W)

        self.btn_Refresh = ttk.Button(self, text = "Refrescar", command=self.refrescarTV) 
        self.btn_Refresh.pack(fill=X, expand=0)

        self.sptr_1 = ttk.Separator(self, orient=HORIZONTAL)
        self.sptr_1.pack(side = TOP, fill = X, padx=5)   

        self.tv_factura = ttk.Treeview(self, columns=("NombredelCliente","Numerodeconsecutivo", "MontoaPagar", "FechaVencimiento"))
        self.tv_factura.heading("#0", text="#")
        self.tv_factura.column("#0", minwidth=0, width=50, stretch=NO)
        self.tv_factura.heading("NombredelCliente", text="Nombre del Cliente")
        self.tv_factura.heading("Numerodeconsecutivo", text="Numero de consecutivo")
        self.tv_factura.heading("MontoaPagar", text="Monto a Pagar") 
        self.tv_factura.heading("FechaVencimiento", text="Fecha Vencimiento") 

        self.tv_factura.bind('<1>', self.single)  
        self.tv_factura.pack(fill=X, expand=0)

        self.getAll()

class Eliminar_Factura_Frame(ttk.Frame):
    def refrescarCmb(self):
        global listaServicios

        lista_ID = []
        for servicio in listaServicios:
            lista_ID.append(servicio.descripcion)

        self.cmb_Item['values'] = lista_ID

    def modified (self, event):
        global listaServicios 
         
        for servicio in listaServicios:
            if servicio.descripcion == (str)(self.cmb_Item.get()): 
                cantidad = 0
                if esNumero(self.txt_quantity.get()):
                    cantidad = int(self.txt_quantity.get())
                self.txt_precio.config(state=NORMAL)
                self.txt_amount.config(state=NORMAL)
                self.txt_precio.delete(0, 'end') 
                self.txt_amount.delete(0, 'end') 
                self.txt_precio.insert(0,servicio.precio) 
                self.txt_amount.insert(0,servicio.precio * cantidad)  
                self.txt_precio.config(state=DISABLED)
                self.txt_amount.config(state=DISABLED) 

    def cell(self, event, e = None):
        '''Identify cell from mouse position'''
        row, col = self.tv_factura.identify_row(e.y), self.tv_factura.identify_column(e.x)
        pos = self.tv_factura.bbox(row, col)       # Calculate positon of entry
        return row, col, pos

    def single(self, event=None):
        '''Single click to select row and column'''
        global row, col, pos
        row, col, pos = self.cell(self, event)
        print('Select', row, col)

    def ok(self, event=None):
        '''Validate entry as at loses focus'''
        try:             
            self.tv_factura.set(*item, self.typed.get())    # Set tree cell text
            self.entry.place_forget()            # Remove entry without deleting it
        except :
            print('Display Row Cannot be set . . .') 

    def deleterow(self, event):
        '''Delete selected row'''
        deletedRow = 0
        print('delete', len(self.tv_factura.selection()))
        if len(self.tv_factura.selection()) != 0:
            row = self.tv_factura.selection()[0]
        try:
            print('deleterow', row)
            print(self.tv_factura.item(row, "values"))
            deletedRow = self.tv_factura.item(row, "values")
            self.tv_factura.delete(row)
        except:
            print('no row selected')  

        data = {} 
        with open('facturas.json') as json_file:
            data = json.load(json_file)
        newList = []   
        for x in data["facturas"] :
            s1 = str(x['invoiceNumber'])
            s2 = deletedRow[1]
            if s1 != s2: 
                newList.append(x)
        try:
            os.remove("facturas/factura" + deletedRow[1] + ".pdf")
        except Exception as e:
            messagebox.showinfo(title=None, message="No se pudo borrar el PDF porque esta abierto por otro programa, no tiene permisos o no existe.")

        data["facturas"] = newList
                 
        with open('facturas.json', 'w') as outfile:
            json.dump(data, outfile) 

    def getFacturas(self, e=None):
        data = {}  
        with open('facturas.json') as json_file:
            data = json.load(json_file) 

        list = []
        for x in data["facturas"]:
            print(x)
            print('Name: ' + str(x['customerName']))
            print('Website: ' + str(x['invoiceNumber']))
            print('From: ' + str(x['total']))
            print('')  
            list.append([x['customerName'],
                x['invoiceNumber'],
                x['total']])
        return list

    def get_numeroFactura(self,factura):
        return factura[1];

    def refrescarTV(self): 
        for x in self.tv_factura.get_children():
            self.tv_factura.delete(x)

        listaFacturas = self.getFacturas() 
        numeroCont = 1
        listaFacturas.sort(key=self.get_numeroFactura)
        for x in listaFacturas:
            self.tv_factura.insert("", tk.END, text="" + str(numeroCont), values=(x[0], x[1], x[2]))
            numeroCont += 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        global listaServicios

        listaFacturas = self.getFacturas() 

        self.btn_Refresh = ttk.Button(self, text = "Refrescar", command=self.refrescarTV) 
        self.btn_Refresh.pack(fill=X, expand=0)

        self.sptr_1 = ttk.Separator(self, orient=HORIZONTAL)
        self.sptr_1.pack(side = TOP, fill = X, padx=5)   

        self.tv_factura = ttk.Treeview(self, columns=("NombredelCliente","Numerodeconsecutivo", "MontoaPagar"))
        self.tv_factura.heading("#0", text="#")
        self.tv_factura.column("#0", minwidth=0, width=50, stretch=NO)
        self.tv_factura.heading("NombredelCliente", text="Nombre del Cliente")
        self.tv_factura.heading("Numerodeconsecutivo", text="Numero de consecutivo")
        self.tv_factura.heading("MontoaPagar", text="Monto a Pagar") 

        self.tv_factura.bind('<1>', self.single) 
        self.tv_factura.bind("<Delete>", self.deleterow) 
        self.tv_factura.pack(fill=X, expand=0)

        self.refrescarTV()

class PDF_Factura_Frame(ttk.Frame):
    def refrescarCmb(self):
        global listaServicios

        lista_ID = []
        for servicio in listaServicios:
            lista_ID.append(servicio.descripcion)

        self.cmb_Item['values'] = lista_ID

    def modified (self, event):
        global listaServicios 
         
        for servicio in listaServicios:
            if servicio.descripcion == (str)(self.cmb_Item.get()): 
                cantidad = 0
                if esNumero(self.txt_quantity.get()):
                    cantidad = int(self.txt_quantity.get())
                self.txt_precio.config(state=NORMAL)
                self.txt_amount.config(state=NORMAL)
                self.txt_precio.delete(0, 'end') 
                self.txt_amount.delete(0, 'end') 
                self.txt_precio.insert(0,servicio.precio) 
                self.txt_amount.insert(0,servicio.precio * cantidad)  
                self.txt_precio.config(state=DISABLED)
                self.txt_amount.config(state=DISABLED) 

    def cell(self, event, e = None):
        '''Identify cell from mouse position'''
        row, col = self.tv_factura.identify_row(e.y), self.tv_factura.identify_column(e.x)
        pos = self.tv_factura.bbox(row, col)       # Calculate positon of entry
        return row, col, pos

    def single(self, event=None):
        '''Single click to select row and column'''
        global row, col, pos
        row, col, pos = self.cell(self, event)
        print('Select', row, col)

    def ok(self, event=None):
        '''Validate entry as at loses focus'''
        try:             
            self.tv_factura.set(*item, self.typed.get())    # Set tree cell text
            self.entry.place_forget()            # Remove entry without deleting it
        except :
            print('Display Row Cannot be set . . .') 

    def deleterow(self, event):
        '''Delete selected row'''
        deletedRow = 0
        print('delete', len(self.tv_factura.selection()))
        if len(self.tv_factura.selection()) != 0:
            row = self.tv_factura.selection()[0]
        try:
            print('deleterow', row)
            print(self.tv_factura.item(row, "values"))
            deletedRow = self.tv_factura.item(row, "values")
            self.tv_factura.delete(row)
        except:
            print('no row selected')  

        data = {} 
        with open('facturas.json') as json_file:
            data = json.load(json_file)
        newList = []   
        for x in data["facturas"] :
            s1 = str(x['invoiceNumber'])
            s2 = deletedRow[1]
            if s1 != s2: 
                newList.append(x)
        try:
            os.remove("facturas/factura" + deletedRow[1] + ".pdf")
        except Exception as e:
            messagebox.showinfo(title=None, message="No se pudo borrar el PDF porque esta abierto por otro programa, no tiene permisos o no existe.")

        data["facturas"] = newList
                 
        with open('facturas.json', 'w') as outfile:
            json.dump(data, outfile) 

    def getFacturas(self, e=None):
        data = {}  
        with open('facturas.json') as json_file:
            data = json.load(json_file) 

        list = []
        for x in data["facturas"]:
            print(x)
            print('Name: ' + str(x['customerName']))
            print('Website: ' + str(x['invoiceNumber']))
            print('From: ' + str(x['total']))
            print('')  
            list.append([x['customerName'],
                x['invoiceNumber'],
                x['total']])
        return list

    def double(self, event=None, e = None):
        '''Double click to edit cell'''
        global row, col, pos, item
        row = self.tv_factura.selection()[0]
        print('Edit', row, col) 
        selectedRow = self.tv_factura.item(row, "values")
        webbrowser.open('file://C:/Users/ExtremeTech/source/repos/Proyecto3/facturas/factura' + selectedRow[1] + '.pdf')

    def get_numeroFactura(self,factura):
        return factura[1];

    def refrescarTV(self): 
        for x in self.tv_factura.get_children():
            self.tv_factura.delete(x)

        listaFacturas = self.getFacturas() 
        numeroCont = 1
        listaFacturas.sort(key=self.get_numeroFactura)
        for x in listaFacturas:
            self.tv_factura.insert("", tk.END, text="" + str(numeroCont), values=(x[0], x[1]))
            numeroCont += 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        global listaServicios

        listaFacturas = self.getFacturas() 

        self.btn_Refresh = ttk.Button(self, text = "Refrescar", command=self.refrescarTV) 
        self.btn_Refresh.pack(fill=X, expand=0)

        self.sptr_1 = ttk.Separator(self, orient=HORIZONTAL)
        self.sptr_1.pack(side = TOP, fill = X, padx=5)   

        self.tv_factura = ttk.Treeview(self, columns=("NombredelCliente","Numerodeconsecutivo" ))
        self.tv_factura.heading("#0", text="#")
        self.tv_factura.column("#0", minwidth=0, width=50, stretch=NO)
        self.tv_factura.heading("NombredelCliente", text="Nombre del Cliente")
        self.tv_factura.heading("Numerodeconsecutivo", text="Numero de consecutivo") 

        self.tv_factura.bind('<1>', self.single)  
        self.tv_factura.bind('<Double-Button-1>', self.double)
        self.tv_factura.pack(fill=X, expand=0)

        self.refrescarTV()

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

    def cell(self, event, e = None):
        '''Identify cell from mouse position'''
        row, col = self.tv_factura.identify_row(e.y), self.tv_factura.identify_column(e.x)
        pos = self.tv_factura.bbox(row, col)       # Calculate positon of entry
        return row, col, pos

    def single(self, event=None):
        '''Single click to select row and column'''
        global row, col, pos
        row, col, pos = self.cell(self, event)
        print('Select', row, col) 

    def getFacturas(self, e=None):
        data = {}  
        with open('facturas.json') as json_file:
            data = json.load(json_file) 

        list = []
        for x in data["facturas"]: 
            list.append([
                x['tax'],
                x['total'],
                x['dueDate']])
        return list

    def get_numeroFactura(self,factura):
        return factura[1];

    def refrescarTV(self): 

        continuar = True

        try:
            fechaInicio = datetime.datetime.strptime(self.txt_FechaInicio.get(), "%d/%m/%Y")
        except Exception as e:
            messagebox.showinfo(title=None, message="El campo FechaInicio tiene que tener formato dd/mm/YYYY") 
            continuar = False
            pass        
        try:
            fechaFinal = datetime.datetime.strptime(self.txt_FechaFinal.get(), "%d/%m/%Y")
        except Exception as e:
            messagebox.showinfo(title=None, message="El campo Due Date tiene que tener formato dd/mm/YYYY") 
            continuar = False
            pass 
        
        if fechaFinal < fechaInicio: 
            messagebox.showinfo(title=None, message="La fecha final no debe de ser menor a la fecha inicial") 
            continuar = False

        if continuar: 
            for x in self.tv_factura.get_children():
                self.tv_factura.delete(x)
            totalImpuestos = 0
            totalMonto = 0
            listaFacturas = self.getFacturas() 
            numeroCont = 1
            listaFacturas.sort(key=self.get_numeroFactura)
            for x in listaFacturas:
                if fechaInicio <= datetime.datetime.strptime(x[2], "%d/%m/%Y") <= fechaFinal: 
                    totalImpuestos += x[0];
                    totalMonto += x[1];
            self.tv_factura.insert("", tk.END, text="" + str(numeroCont), values=(totalImpuestos, totalMonto))
            numeroCont += 1

    def getAll(self): 
        for x in self.tv_factura.get_children():
            self.tv_factura.delete(x)

        totalImpuestos = 0
        totalMonto = 0
        listaFacturas = self.getFacturas() 
        numeroCont = 1
        listaFacturas.sort(key=self.get_numeroFactura)
        for x in listaFacturas: 
            totalImpuestos += x[0];
            totalMonto += x[1];
        self.tv_factura.insert("", tk.END, text="" + str(numeroCont), values=(totalMonto,totalImpuestos))
        numeroCont += 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        global listaServicios

        listaFacturas = self.getFacturas() 
        
        self.pnl_CustomerInfo = ttk.Frame(self)
        self.pnl_CustomerInfo.pack(fill=X, expand=0)

        self.lbl_FechaInicio = ttk.Label(self.pnl_CustomerInfo, text="Fecha Inicio") 
        self.lbl_FechaInicio.grid(column=0, row=1, sticky=N+S+E+W)
        self.txt_FechaInicio = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_FechaInicio.grid(column=1, row=1, sticky=N+S+E+W)

        self.lbl_FechaFinal = ttk.Label(self.pnl_CustomerInfo, text="Fecha Final") 
        self.lbl_FechaFinal.grid(column=0, row=2, sticky=N+S+E+W)
        self.txt_FechaFinal = ttk.Entry(self.pnl_CustomerInfo,width=10) 
        self.txt_FechaFinal.grid(column=1, row=2, sticky=N+S+E+W)

        self.btn_Refresh = ttk.Button(self, text = "Refrescar", command=self.refrescarTV) 
        self.btn_Refresh.pack(fill=X, expand=0)

        self.sptr_1 = ttk.Separator(self, orient=HORIZONTAL)
        self.sptr_1.pack(side = TOP, fill = X, padx=5)   

        self.tv_factura = ttk.Treeview(self, columns=("MontoTotal","MontoTotalImpuestos"))
        self.tv_factura.heading("#0", text="#")
        self.tv_factura.column("#0", minwidth=0, width=50, stretch=NO)
        self.tv_factura.heading("MontoTotal", text="Monto Total")
        self.tv_factura.heading("MontoTotalImpuestos", text="Monto Total Impuestos") 

        self.tv_factura.bind('<1>', self.single)  
        self.tv_factura.pack(fill=X, expand=0)

        self.getAll()


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
        main_window.title("3C: Company System With Face Recognition")
        
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

listaServicios.append(Servicio(90, "Cortar zacate", 456)) 
listaServicios.append(Servicio(91, "Podar arbustos", 456)) 
listaServicios.append(Servicio(92, "Podar arboles", 456)) 
listaServicios.append(Servicio(93, "Combo 1", 456)) 
main_window = tk.Tk()
app = Application(main_window)
app.mainloop()