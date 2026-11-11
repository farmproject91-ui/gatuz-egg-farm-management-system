import os, sys, sqlite3, tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import date, datetime
import database as db

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    CTK = True
except Exception:
    ctk = None
    CTK = False

BG="#101b17"; PANEL="#182820"; PANEL2="#20372b"; GREEN="#2e6b45"; GOLD="#d6b45c"; TEXT="#f3f2e9"; MUTED="#b6c3b9"; RED="#a8433e"

class GatuzApp:
    def __init__(self, root):
        self.root=root
        self.root.title("GATUZ EGG FARM MANAGEMENT SYSTEM")
        self.root.geometry("1320x820")
        self.root.minsize(1050,680)
        self.root.configure(bg=BG)
        self.user=None
        self.farm_id=None
        self.farm_filter=tk.StringVar(value="All Farms")
        self._style()
        db.init_db()
        self._automatic_backup()
        self.login_screen()

    def _style(self):
        s=ttk.Style()
        try: s.theme_use("clam")
        except: pass
        s.configure("Treeview",background=PANEL,foreground=TEXT,fieldbackground=PANEL,rowheight=28,borderwidth=0)
        s.configure("Treeview.Heading",background=GREEN,foreground="white",font=("Segoe UI",10,"bold"))
        s.map("Treeview",background=[("selected",GREEN)],foreground=[("selected","white")])
        s.configure("TCombobox",fieldbackground=PANEL,background=PANEL,foreground=TEXT)

    def _automatic_backup(self):
        marker=os.path.join(db.BACKUP_DIR,"last_auto_backup.txt")
        today=date.today().isoformat()
        try:
            last=open(marker).read().strip() if os.path.exists(marker) else ""
            if last != today:
                db.backup_db(os.path.join(db.BACKUP_DIR,"auto_"+today+".db"))
                open(marker,"w").write(today)
        except Exception: pass

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def label(self,parent,text,size=11,bold=False,color=TEXT):
        return tk.Label(parent,text=text,bg=parent.cget("bg") if "bg" in parent.keys() else BG,fg=color,font=("Segoe UI",size,"bold" if bold else "normal"))

    def btn(self,parent,text,command,color=GREEN):
        return tk.Button(parent,text=text,command=command,bg=color,fg="white",activebackground=GOLD,activeforeground="#101010",relief="flat",font=("Segoe UI",10,"bold"),padx=12,pady=8,cursor="hand2")

    def login_screen(self):
        self.clear()
        frame=tk.Frame(self.root,bg=PANEL,padx=42,pady=38)
        frame.place(relx=.5,rely=.5,anchor="center")
        tk.Label(frame,text="GATUZ",bg=PANEL,fg=GOLD,font=("Segoe UI",30,"bold")).pack()
        tk.Label(frame,text="EGG FARM MANAGEMENT SYSTEM",bg=PANEL,fg=TEXT,font=("Segoe UI",13,"bold")).pack(pady=(0,24))
        tk.Label(frame,text="Username",bg=PANEL,fg=MUTED).pack(anchor="w")
        u=tk.Entry(frame,font=("Segoe UI",12),width=32); u.pack(pady=(4,12),ipady=6); u.insert(0,"admin")
        tk.Label(frame,text="Password",bg=PANEL,fg=MUTED).pack(anchor="w")
        p=tk.Entry(frame,font=("Segoe UI",12),width=32,show="•"); p.pack(pady=(4,18),ipady=6); p.insert(0,"admin123")
        def login():
            with db.connect() as c: row=c.execute("SELECT * FROM users WHERE username=? AND active=1",(u.get().strip(),)).fetchone()
            if row and db.verify_password(p.get(),row["password"]):
                self.user=dict(row); self.main_screen()
            else: messagebox.showerror("Login failed","Incorrect username or password.")
        self.btn(frame,"SIGN IN",login).pack(fill="x")
        tk.Label(frame,text="First login: admin / admin123 — change password after signing in.",bg=PANEL,fg=MUTED,font=("Segoe UI",9)).pack(pady=(16,0))
        p.bind("<Return>",lambda e:login())

    def main_screen(self):
        self.clear()
        self.shell=tk.Frame(self.root,bg=BG); self.shell.pack(fill="both",expand=True)
        side=tk.Frame(self.shell,bg="#0c1511",width=220); side.pack(side="left",fill="y"); side.pack_propagate(False)
        tk.Label(side,text="GATUZ",bg="#0c1511",fg=GOLD,font=("Segoe UI",25,"bold")).pack(pady=(24,0))
        tk.Label(side,text="EGG FARM SYSTEM",bg="#0c1511",fg=MUTED,font=("Segoe UI",9,"bold")).pack(pady=(0,22))
        nav=[("Dashboard",self.dashboard),("Farms",self.farms_page),("Chicken Records",self.chickens_page),("Egg Production",self.production_page),("Inventory",self.inventory_page),("Customers",self.customers_page),("Sales",self.sales_page),("Expenses",self.expenses_page),("Reports",self.reports_page),("Backup / Restore",self.backup_page)]
        if self.user["role"]=="admin": nav.append(("Users",self.users_page))
        for name,fn in nav:
            tk.Button(side,text="  "+name,command=fn,anchor="w",bg="#0c1511",fg=TEXT,activebackground=GREEN,activeforeground="white",relief="flat",font=("Segoe UI",10),padx=14,pady=10).pack(fill="x",padx=8,pady=1)
        tk.Frame(side,bg="#344b3d",height=1).pack(fill="x",pady=14)
        tk.Label(side,text=f"Signed in: {self.user['username']}\nRole: {self.user['role']}",bg="#0c1511",fg=MUTED,font=("Segoe UI",9)).pack(pady=5)
        self.btn(side,"Log out",self.login_screen,RED).pack(fill="x",padx=12,pady=12)
        self.content=tk.Frame(self.shell,bg=BG); self.content.pack(side="left",fill="both",expand=True)
        self.dashboard()

    def page(self,title,subtitle=""):
        for w in self.content.winfo_children(): w.destroy()
        head=tk.Frame(self.content,bg=BG); head.pack(fill="x",padx=25,pady=(20,10))
        tk.Label(head,text=title,bg=BG,fg=TEXT,font=("Segoe UI",22,"bold")).pack(anchor="w")
        if subtitle: tk.Label(head,text=subtitle,bg=BG,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",pady=(3,0))
        bar=tk.Frame(self.content,bg=BG); bar.pack(fill="x",padx=25,pady=6)
        tk.Label(bar,text="Farm view:",bg=BG,fg=MUTED).pack(side="left")
        farms=["All Farms"]+[r["name"] for r in db.farm_rows()]
        self.farm_filter.set(self.farm_filter.get() if self.farm_filter.get() in farms else "All Farms")
        combo=ttk.Combobox(bar,textvariable=self.farm_filter,values=farms,state="readonly",width=24)
        combo.pack(side="left",padx=8)
        combo.bind("<<ComboboxSelected>>",lambda e:self._refresh_current())
        return head

    def _refresh_current(self):
        # Re-open the currently selected page by dispatching its renderer.
        if hasattr(self,"current_page"): self.current_page()

    def selected_farm(self):
        val=self.farm_filter.get()
        if val=="All Farms": return None
        with db.connect() as c:
            r=c.execute("SELECT id FROM farms WHERE name=? AND archived=0",(val,)).fetchone()
            return r["id"] if r else None

    def body(self):
        f=tk.Frame(self.content,bg=BG); f.pack(fill="both",expand=True,padx=25,pady=10); return f

    def dashboard(self):
        self.current_page=self.dashboard
        self.page("Farm overview","Combined performance across farms, or select an individual farm.")
        b=self.body(); st=db.farm_stats(self.selected_farm())
        cards=[("Eggs collected",f"{st['eggs']:,.0f}"),("Sales value",f"₱{st['sales']:,.2f}"),("Paid",f"₱{st['paid']:,.2f}"),("Outstanding",f"₱{st['balance']:,.2f}"),("Expenses",f"₱{st['expenses']:,.2f}"),("Net profit",f"₱{st['profit']:,.2f}")]
        row=tk.Frame(b,bg=BG); row.pack(fill="x")
        for title,value in cards:
            p=tk.Frame(row,bg=PANEL,padx=15,pady=16); p.pack(side="left",fill="both",expand=True,padx=5)
            tk.Label(p,text=title,bg=PANEL,fg=MUTED,font=("Segoe UI",9)).pack(anchor="w")
            tk.Label(p,text=value,bg=PANEL,fg=GOLD if title=="Net profit" else TEXT,font=("Segoe UI",17,"bold")).pack(anchor="w",pady=(5,0))
        lower=tk.Frame(b,bg=BG); lower.pack(fill="both",expand=True,pady=18)
        left=tk.Frame(lower,bg=PANEL,padx=15,pady=12); left.pack(side="left",fill="both",expand=True,padx=5)
        tk.Label(left,text="PRODUCTION SNAPSHOT",bg=PANEL,fg=GOLD,font=("Segoe UI",11,"bold")).pack(anchor="w")
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            fig=Figure(figsize=(5.2,3.0),dpi=90); ax=fig.add_subplot(111)
            with db.connect() as c:
                if self.selected_farm() is None:
                    rows=c.execute("SELECT day,SUM(jumbo+xl+large+medium+small+peewee) n FROM production GROUP BY day ORDER BY day DESC LIMIT 10").fetchall()
                else:
                    rows=c.execute("SELECT day,(jumbo+xl+large+medium+small+peewee) n FROM production WHERE farm_id=? ORDER BY day DESC LIMIT 10",(self.selected_farm(),)).fetchall()
            rows=list(reversed(rows)); ax.plot([r["day"] for r in rows],[r["n"] for r in rows],marker="o",color="#d6b45c")
            ax.set_facecolor("#182820"); fig.patch.set_facecolor("#182820"); ax.tick_params(colors="white",labelrotation=25); ax.spines[:].set_color("#718578"); ax.set_ylabel("Eggs",color="white")
            fig.tight_layout(); canvas=FigureCanvasTkAgg(fig,master=left); canvas.draw(); canvas.get_tk_widget().pack(fill="both",expand=True)
        except Exception as e:
            tk.Label(left,text="Chart unavailable. Install matplotlib to enable charts.",bg=PANEL,fg=MUTED).pack(pady=30)
        center=tk.Frame(lower,bg=PANEL,padx=15,pady=12); center.pack(side="left",fill="both",expand=True,padx=5)
        tk.Label(center,text="SALES SNAPSHOT",bg=PANEL,fg=GOLD,font=("Segoe UI",11,"bold")).pack(anchor="w")
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            fig2=Figure(figsize=(4.3,3.0),dpi=90); ax2=fig2.add_subplot(111)
            with db.connect() as c:
                if self.selected_farm() is None:
                    sr=c.execute("SELECT day,SUM(total) n FROM sales GROUP BY day ORDER BY day DESC LIMIT 10").fetchall()
                else:
                    sr=c.execute("SELECT day,SUM(total) n FROM sales WHERE farm_id=? GROUP BY day ORDER BY day DESC LIMIT 10",(self.selected_farm(),)).fetchall()
            sr=list(reversed(sr)); ax2.bar([r["day"] for r in sr],[r["n"] for r in sr],color="#d6b45c")
            ax2.set_facecolor("#182820"); fig2.patch.set_facecolor("#182820"); ax2.tick_params(colors="white",labelrotation=25); ax2.spines[:].set_color("#718578"); ax2.set_ylabel("PHP",color="white")
            fig2.tight_layout(); cv2=FigureCanvasTkAgg(fig2,master=center); cv2.draw(); cv2.get_tk_widget().pack(fill="both",expand=True)
        except Exception:
            tk.Label(center,text="Sales chart unavailable.",bg=PANEL,fg=MUTED).pack(pady=30)
        right=tk.Frame(lower,bg=PANEL,padx=15,pady=12); right.pack(side="left",fill="both",expand=True,padx=5)
        tk.Label(right,text="RECENT ACTIVITY",bg=PANEL,fg=GOLD,font=("Segoe UI",11,"bold")).pack(anchor="w")
        for day,desc,fid in db.recent_activity(self.selected_farm()):
            tk.Label(right,text=f"• {day}  {desc}",bg=PANEL,fg=TEXT,anchor="w",wraplength=390,justify="left").pack(fill="x",pady=5)

    def table_page(self,title,subtitle,columns,rows,actions=()):
        self.page(title,subtitle); b=self.body()
        tools=tk.Frame(b,bg=BG); tools.pack(fill="x",pady=(0,8))
        for label,fn in actions: self.btn(tools,label,fn).pack(side="left",padx=(0,7))
        tree=ttk.Treeview(b,columns=columns,show="headings")
        for col in columns: tree.heading(col,text=col.replace("_"," ").title()); tree.column(col,width=125,anchor="w")
        for r in rows: tree.insert("", "end",values=[r[k] if k in r.keys() else "" for k in columns])
        tree.pack(fill="both",expand=True)
        self.active_tree=tree
        return tree

    def form(self,title,fields,callback):
        win=tk.Toplevel(self.root); win.title(title); win.configure(bg=PANEL); win.transient(self.root); win.grab_set()
        entries={}
        for i,(key,label,default) in enumerate(fields):
            tk.Label(win,text=label,bg=PANEL,fg=TEXT).grid(row=i,column=0,sticky="w",padx=14,pady=7)
            e=tk.Entry(win,width=34); e.grid(row=i,column=1,padx=14,pady=7,ipady=4); e.insert(0,str(default))
            entries[key]=e
        def save():
            vals={k:v.get().strip() for k,v in entries.items()}
            try: callback(vals); win.destroy()
            except Exception as e: messagebox.showerror("Cannot save",str(e),parent=win)
        self.btn(win,"Save",save).grid(row=len(fields),column=0,columnspan=2,pady=14,sticky="ew",padx=14)

    def farms_page(self):
        self.current_page=self.farms_page
        with db.connect() as c: rows=c.execute("SELECT * FROM farms ORDER BY archived,name").fetchall()
        def add():
            self.form("Add farm",[("name","Farm name",""),("location","Location",""),("notes","Notes","")],lambda v:self._farm_save(None,v))
        def edit():
            r=self._selected_row()
            if not r:return
            self.form("Edit farm",[("name","Farm name",r[1]),("location","Location",r[2]),("notes","Notes",r[3])],lambda v:self._farm_save(r[0],v))
        def archive():
            r=self._selected_row()
            if r and messagebox.askyesno("Archive farm","Archive this farm? It will be hidden from normal farm selectors."):
                with db.connect() as c:c.execute("UPDATE farms SET archived=1 WHERE id=?",(r[0],))
                self.farms_page()
        def restore():
            r=self._selected_row()
            if r:
                with db.connect() as c:c.execute("UPDATE farms SET archived=0 WHERE id=?",(r[0],))
                self.farms_page()
        def delete():
            r=self._selected_row()
            if r and messagebox.askyesno("Permanent delete","Permanently delete this farm and its records? This cannot be undone."):
                with db.connect() as c:c.execute("DELETE FROM farms WHERE id=?",(r[0],))
                self.farms_page()
        tree=self.table_page("Farm management","Archived farms are retained and can be restored.",("id","name","location","notes","archived"),rows,[("Add Farm",add),("Edit Selected",edit),("Archive",archive),("Restore",restore),("Delete",delete)])
        self.farm_tree=tree
    def _selected_row(self):
        if not hasattr(self,"active_tree"): return None
        sel=self.active_tree.selection()
        return self.active_tree.item(sel[0],"values") if sel else None
    def _farm_save(self,fid,v):
        with db.connect() as c:
            if fid:c.execute("UPDATE farms SET name=?,location=?,notes=? WHERE id=?",(v["name"],v["location"],v["notes"],fid))
            else:c.execute("INSERT INTO farms(name,location,notes) VALUES(?,?,?)",(v["name"],v["location"],v["notes"]))
        self.farms_page()

    def chickens_page(self):
        self.current_page=self.chickens_page
        fid=self.selected_farm()
        with db.connect() as c:
            q="SELECT x.id,f.name farm,x.batch_name,x.breed,x.bird_count,x.date_added,x.status,x.notes FROM flocks x JOIN farms f ON f.id=x.farm_id"
            rows=c.execute(q+(" WHERE x.farm_id=?" if fid else "")+" ORDER BY x.date_added DESC",(fid,) if fid else ()).fetchall()
        def add():
            self.form("Add chicken batch",[("batch_name","Batch / flock name",""),("breed","Breed",""),("bird_count","Number of chickens","0"),("date_added","Date added (YYYY-MM-DD)",date.today().isoformat()),("status","Status (Active/Sold/Deceased)","Active"),("notes","Notes","")],self._flock_save)
        self.table_page("Chicken records","Track flock batches by farm. Active birds are counted on the dashboard.",("id","farm","batch_name","breed","bird_count","date_added","status","notes"),rows,[("Add Chicken Batch",add),("Delete Selected",lambda:self._delete_selected("flocks",self.chickens_page))])
    def _flock_save(self,v):
        fid=self.selected_farm()
        if fid is None:
            farms=db.farm_rows()
            if len(farms)==1:fid=farms[0]["id"]
            else:raise ValueError("Select one farm before adding a chicken batch.")
        count=int(v["bird_count"])
        if count<0:raise ValueError("Chicken count cannot be negative.")
        if v["status"] not in ("Active","Sold","Deceased"):raise ValueError("Status must be Active, Sold, or Deceased.")
        with db.connect() as c:c.execute("INSERT INTO flocks(farm_id,batch_name,breed,bird_count,date_added,status,notes) VALUES(?,?,?,?,?,?,?)",(fid,v["batch_name"],v["breed"],count,v["date_added"],v["status"],v["notes"]))
        self.chickens_page()

    def production_page(self):
        self.current_page=self.production_page
        fid=self.selected_farm()
        with db.connect() as c:
            q="SELECT p.id,f.name farm,p.day,p.jumbo,p.xl,p.large,p.medium,p.small,p.peewee,p.cracked,p.damaged,(p.jumbo+p.xl+p.large+p.medium+p.small+p.peewee) total FROM production p JOIN farms f ON f.id=p.farm_id"
            rows=c.execute(q+(" WHERE p.farm_id=?" if fid else "")+" ORDER BY p.day DESC",(fid,) if fid else ()).fetchall()
        def add():
            farms=db.farm_rows()
            if not farms: messagebox.showwarning("Farm required","Create a farm first.");return
            self.form("Daily egg collection",[("day","Date (YYYY-MM-DD)",date.today().isoformat()),("jumbo","Jumbo","0"),("xl","XL","0"),("large","Large","0"),("medium","Medium","0"),("small","Small","0"),("peewee","Peewee","0"),("cracked","Cracked","0"),("damaged","Damaged","0"),("notes","Notes","")],lambda v:self._production_save(v))
        self.table_page("Egg production","Enter daily collection by grade. Counts must be whole non-negative numbers.",("id","farm","day","jumbo","xl","large","medium","small","peewee","cracked","damaged","total"),rows,[("Add Collection",add),("Delete Selected",lambda:self._delete_selected("production",self.production_page))])
    def _production_save(self,v):
        fid=self.selected_farm()
        if fid is None:
            farms=db.farm_rows()
            if len(farms)==1:fid=farms[0]["id"]
            else: raise ValueError("Select one farm in the Farm view selector before adding a record.")
        nums=[int(v[k] or 0) for k in ["jumbo","xl","large","medium","small","peewee","cracked","damaged"]]
        if any(n<0 for n in nums):raise ValueError("Counts cannot be negative.")
        with db.connect() as c:c.execute("INSERT INTO production(farm_id,day,jumbo,xl,large,medium,small,peewee,cracked,damaged,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(fid,v["day"],*nums,v["notes"]))
        self.production_page()

    def _delete_selected(self,table,refresh):
        r=self._selected_row()
        if r and messagebox.askyesno("Confirm delete","Delete selected record?"):
            with db.connect() as c:c.execute(f"DELETE FROM {table} WHERE id=?",(r[0],))
            refresh()

    def inventory_page(self):
        self.current_page=self.inventory_page; fid=self.selected_farm()
        with db.connect() as c:
            q="SELECT i.id,f.name farm,i.name,i.category,i.unit,i.quantity,i.reorder_level FROM inventory i JOIN farms f ON f.id=i.farm_id"
            rows=c.execute(q+(" WHERE i.farm_id=?" if fid else "")+" ORDER BY i.name",(fid,) if fid else ()).fetchall()
        def add():
            self.form("Add inventory item",[("name","Item name",""),("category","Category (Feeds/Medicines/Vitamins/Supplies)","Feeds"),("unit","Unit (kg, sack, pcs)","kg"),("quantity","Opening stock","0"),("reorder_level","Low-stock threshold","0")],self._inventory_save)
        def move(kind):
            r=self._selected_row()
            if not r: messagebox.showinfo("Select item","Select an inventory item first.");return
            qty=simpledialog.askfloat(kind,f"Quantity to {kind.lower()}:",minvalue=0.01)
            if qty is None:return
            try:
                with db.connect() as c:
                    cur=c.execute("SELECT quantity,farm_id FROM inventory WHERE id=?",(r[0],)).fetchone()
                    new=cur["quantity"]+qty if kind=="Stock In" else cur["quantity"]-qty
                    if new<0:raise ValueError("Not enough stock.")
                    c.execute("UPDATE inventory SET quantity=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",(new,r[0]))
                    c.execute("INSERT INTO stock_moves(farm_id,item_id,move_type,quantity) VALUES(?,?,?,?)",(cur["farm_id"],r[0],kind,qty))
                self.inventory_page()
            except Exception as e:messagebox.showerror("Stock movement",str(e))
        self.table_page("Inventory","Stock movements update on-hand quantity and are logged.",("id","farm","name","category","unit","quantity","reorder_level"),rows,[("Add Item",add),("Stock In",lambda:move("Stock In")),("Stock Out",lambda:move("Stock Out")),("Delete Item",lambda:self._delete_selected("inventory",self.inventory_page))])
        for item in self.active_tree.get_children():
            vals=self.active_tree.item(item,"values")
            try:
                if float(vals[5])<=float(vals[6]): self.active_tree.item(item,tags=("low",))
            except:pass
        self.active_tree.tag_configure("low",foreground="#ff9c83")
    def _inventory_save(self,v):
        fid=self.selected_farm()
        if fid is None:
            farms=db.farm_rows()
            if len(farms)==1:fid=farms[0]["id"]
            else:raise ValueError("Select one farm before adding an item.")
        with db.connect() as c:c.execute("INSERT INTO inventory(farm_id,name,category,unit,quantity,reorder_level) VALUES(?,?,?,?,?,?)",(fid,v["name"],v["category"],v["unit"],float(v["quantity"]),float(v["reorder_level"])))
        self.inventory_page()

    def customers_page(self):
        self.current_page=self.customers_page; fid=self.selected_farm()
        with db.connect() as c:
            q="SELECT c.id,f.name farm,c.name,c.phone,c.address FROM customers c JOIN farms f ON f.id=c.farm_id"
            rows=c.execute(q+(" WHERE c.farm_id=?" if fid else "")+" ORDER BY c.name",(fid,) if fid else ()).fetchall()
        def add():
            self.form("Add customer",[("name","Customer name",""),("phone","Phone",""),("address","Address","")],self._customer_save)
        self.table_page("Customers","Customer records are farm-specific.",("id","farm","name","phone","address"),rows,[("Add Customer",add),("Delete Selected",lambda:self._delete_selected("customers",self.customers_page))])
    def _customer_save(self,v):
        fid=self.selected_farm()
        if fid is None:
            farms=db.farm_rows()
            if len(farms)==1:fid=farms[0]["id"]
            else:raise ValueError("Select one farm before adding a customer.")
        with db.connect() as c:c.execute("INSERT INTO customers(farm_id,name,phone,address) VALUES(?,?,?,?)",(fid,v["name"],v["phone"],v["address"]))
        self.customers_page()

    def sales_page(self):
        self.current_page=self.sales_page; fid=self.selected_farm()
        with db.connect() as c:
            q="SELECT s.id,f.name farm,s.day,COALESCE(c.name,'Walk-in') customer,s.grade,s.quantity,s.unit_price,s.total,s.paid,(s.total-s.paid) balance FROM sales s JOIN farms f ON f.id=s.farm_id LEFT JOIN customers c ON c.id=s.customer_id"
            rows=c.execute(q+(" WHERE s.farm_id=?" if fid else "")+" ORDER BY s.day DESC",(fid,) if fid else ()).fetchall()
        def add():
            with db.connect() as c:
                customers=c.execute("SELECT id,name FROM customers"+(" WHERE farm_id=?" if fid else "")+" ORDER BY name",(fid,) if fid else ()).fetchall()
            opts=[""]+[f"{r['id']}|{r['name']}" for r in customers]
            self.form("Record egg sale",[("day","Date",date.today().isoformat()),("customer","Customer ID (blank = walk-in)",""),("grade","Egg grade","Large"),("quantity","Quantity","0"),("unit_price","Price per egg/tray unit","0"),("paid","Amount paid","0"),("notes","Notes","")],lambda v:self._sale_save(v))
        self.table_page("Egg sales","Outstanding balance is calculated as total less amount paid.",("id","farm","day","customer","grade","quantity","unit_price","total","paid","balance"),rows,[("Record Sale",add),("Delete Selected",lambda:self._delete_selected("sales",self.sales_page)),("Receipt",self.receipt)])
    def _sale_save(self,v):
        fid=self.selected_farm()
        if fid is None:
            farms=db.farm_rows()
            if len(farms)==1:fid=farms[0]["id"]
            else:raise ValueError("Select one farm before recording a sale.")
        qty=float(v["quantity"]); price=float(v["unit_price"]); paid=float(v["paid"]); total=qty*price
        if qty<=0 or price<0 or paid<0 or paid>total:raise ValueError("Check quantity, price, and payment. Payment cannot exceed total.")
        cid=int(v["customer"]) if v["customer"].strip().isdigit() else None
        with db.connect() as c:c.execute("INSERT INTO sales(farm_id,customer_id,day,grade,quantity,unit_price,total,paid,notes) VALUES(?,?,?,?,?,?,?,?,?)",(fid,cid,v["day"],v["grade"],qty,price,total,paid,v["notes"]))
        self.sales_page()
    def receipt(self):
        r=self._selected_row()
        if not r:return
        msg=f"GATUZ EGG FARM\\nSale ID: {r[0]}\\nDate: {r[2]}\\nCustomer: {r[3]}\\nGrade: {r[4]}\\nQty: {r[5]}\\nTotal: PHP {float(r[7]):,.2f}\\nPaid: PHP {float(r[8]):,.2f}\\nBalance: PHP {float(r[9]):,.2f}"
        win=tk.Toplevel(self.root); win.title("Receipt"); t=tk.Text(win,width=42,height=16);t.pack(padx=12,pady=12);t.insert("1.0",msg);t.configure(state="disabled")
        self.btn(win,"Print (open system print dialog)",lambda:messagebox.showinfo("Receipt","Copy this receipt into a document and print it.")).pack(pady=8)

    def expenses_page(self):
        self.current_page=self.expenses_page; fid=self.selected_farm()
        with db.connect() as c:
            q="SELECT e.id,f.name farm,e.day,e.category,e.description,e.amount FROM expenses e JOIN farms f ON f.id=e.farm_id"
            rows=c.execute(q+(" WHERE e.farm_id=?" if fid else "")+" ORDER BY e.day DESC",(fid,) if fid else ()).fetchall()
        def add():
            self.form("Add expense",[("day","Date",date.today().isoformat()),("category","Category","Feed"),("description","Description",""),("amount","Amount (PHP)","0"),("notes","Notes","")],self._expense_save)
        self.table_page("Expenses","Record feed, labor, medicine, utilities, and other operating costs.",("id","farm","day","category","description","amount"),rows,[("Add Expense",add),("Delete Selected",lambda:self._delete_selected("expenses",self.expenses_page))])
    def _expense_save(self,v):
        fid=self.selected_farm()
        if fid is None:
            farms=db.farm_rows()
            if len(farms)==1:fid=farms[0]["id"]
            else:raise ValueError("Select one farm before adding an expense.")
        amount=float(v["amount"])
        if amount<0:raise ValueError("Amount cannot be negative.")
        with db.connect() as c:c.execute("INSERT INTO expenses(farm_id,day,category,description,amount,notes) VALUES(?,?,?,?,?,?)",(fid,v["day"],v["category"],v["description"],amount,v["notes"]))
        self.expenses_page()

    def reports_page(self):
        self.current_page=self.reports_page; self.page("Reports & analytics","Export operational and financial data to Excel or PDF.")
        b=self.body()
        tk.Label(b,text="Export scope follows the selected farm filter. Select All Farms for consolidated reports.",bg=BG,fg=MUTED).pack(anchor="w",pady=8)
        self.btn(b,"Export Excel workbook",lambda:self.export_report("xlsx")).pack(anchor="w",pady=7)
        self.btn(b,"Export PDF summary",lambda:self.export_report("pdf")).pack(anchor="w",pady=7)
        st=db.farm_stats(self.selected_farm())
        for k,v in st.items(): tk.Label(b,text=f"{k.title()}: {v:,.2f}",bg=BG,fg=TEXT,font=("Segoe UI",11)).pack(anchor="w",pady=2)
    def export_report(self,kind):
        path=filedialog.asksaveasfilename(defaultextension="."+kind,filetypes=[(kind.upper(), "*."+kind)])
        if not path:return
        fid=self.selected_farm()
        try:
            if kind=="xlsx":
                from openpyxl import Workbook
                from openpyxl.styles import Font,PatternFill
                wb=Workbook(); ws=wb.active;ws.title="Summary"
                st=db.farm_stats(fid);ws.append(["GATUZ EGG FARM — SUMMARY"]);ws.append(["Metric","Value"])
                for k,v in st.items():ws.append([k.title(),v])
                with db.connect() as c:
                    for table in ["production","inventory","sales","expenses","customers"]:
                        sh=wb.create_sheet(table.title())
                        q=f"SELECT * FROM {table}"+(" WHERE farm_id=?" if fid else "")
                        cur=c.execute(q,(fid,) if fid else ())
                        sh.append([x[0] for x in cur.description])
                        for row in cur.fetchall():sh.append(list(row))
                for sh in wb:
                    sh.freeze_panes="A2"
                    for cell in sh[1]:
                        cell.font=Font(bold=True,color="FFFFFF");cell.fill=PatternFill("solid",fgColor="24583A")
                    for col in sh.columns:
                        letter=col[0].column_letter
                        sh.column_dimensions[letter].width=min(28,max(12,max(len(str(x.value or "")) for x in col)+2))
                wb.save(path)
            else:
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
                from reportlab.lib import colors
                from reportlab.lib.styles import getSampleStyleSheet
                st=db.farm_stats(fid); styles=getSampleStyleSheet(); story=[Paragraph("GATUZ EGG FARM MANAGEMENT SYSTEM",styles["Title"]),Paragraph("Management Summary",styles["Heading2"]),Spacer(1,12)]
                data=[["Metric","Value"]]+[[k.title(),f"{v:,.2f}"] for k,v in st.items()]
                t=Table(data,colWidths=[220,180]);t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#24583A")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.5,colors.grey),("PADDING",(0,0),(-1,-1),8)]));story.append(t);SimpleDocTemplate(path,pagesize=A4).build(story)
            messagebox.showinfo("Export complete",f"Report saved to:\\n{path}")
        except Exception as e:messagebox.showerror("Export failed",str(e))

    def backup_page(self):
        self.current_page=self.backup_page; self.page("Backup & restore","Protect your records. Close the application before copying the whole folder.")
        b=self.body()
        self.btn(b,"Create manual backup",self.manual_backup).pack(anchor="w",pady=7)
        self.btn(b,"Restore from backup file",self.restore_backup,RED).pack(anchor="w",pady=7)
        tk.Label(b,text="Automatic daily backup runs at first launch each day. Backup files are stored in the backups folder.",bg=BG,fg=MUTED,wraplength=700,justify="left").pack(anchor="w",pady=14)
    def manual_backup(self):
        path=filedialog.asksaveasfilename(defaultextension=".db",initialfile="gatuz_manual_backup.db",filetypes=[("SQLite database","*.db")])
        if path:
            try:db.backup_db(path);messagebox.showinfo("Backup created",path)
            except Exception as e:messagebox.showerror("Backup failed",str(e))
    def restore_backup(self):
        path=filedialog.askopenfilename(filetypes=[("SQLite database","*.db")])
        if not path:return
        if not messagebox.askyesno("Restore database","This replaces current data. A safety backup will be created first. Continue?"):return
        try:
            db.backup_db()
            test=sqlite3.connect(path);test.execute("PRAGMA integrity_check");test.close()
            shutil_copy(path,db.DB_PATH)
            messagebox.showinfo("Restored","Database restored. The application will restart.");self.main_screen()
        except Exception as e:messagebox.showerror("Restore failed",str(e))
    def users_page(self):
        self.current_page=self.users_page
        with db.connect() as c:rows=c.execute("SELECT id,username,role,active,created_at FROM users ORDER BY username").fetchall()
        def add():
            self.form("Create user",[("username","Username",""),("password","Temporary password",""),("role","Role (admin/staff)","staff")],self._user_save)
        def reset():
            r=self._selected_row()
            if not r:return
            pwd=simpledialog.askstring("Reset password","Enter new password:",show="•")
            if pwd:
                with db.connect() as c:c.execute("UPDATE users SET password=? WHERE id=?",(db.hash_password(pwd),r[0]))
                messagebox.showinfo("Updated","Password changed.")
        def toggle():
            r=self._selected_row()
            if r and int(r[0])!=self.user["id"]:
                with db.connect() as c:c.execute("UPDATE users SET active=1-active WHERE id=?",(r[0],))
                self.users_page()
        self.table_page("User management","Admin-only. Staff users can manage farm records but cannot manage accounts.",("id","username","role","active","created_at"),rows,[("Add User",add),("Reset Password",reset),("Enable / Disable",toggle),("Change My Password",self.change_my_password)])
    def _user_save(self,v):
        if v["role"] not in ("admin","staff"):raise ValueError("Role must be admin or staff.")
        if len(v["password"])<6:raise ValueError("Password must be at least 6 characters.")
        with db.connect() as c:c.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",(v["username"],db.hash_password(v["password"]),v["role"]))
        self.users_page()
    def change_my_password(self):
        p=simpledialog.askstring("Change password","Enter a new password (at least 6 characters):",show="•")
        if p:
            if len(p)<6:messagebox.showerror("Invalid","Password must be at least 6 characters.");return
            with db.connect() as c:c.execute("UPDATE users SET password=? WHERE id=?",(db.hash_password(p),self.user["id"]))
            messagebox.showinfo("Updated","Your password has been changed.")

def shutil_copy(src,dst):
    import shutil
    shutil.copy2(src,dst)

if __name__=="__main__":
    root=tk.Tk()
    app=GatuzApp(root)
    root.mainloop()
