"""Friendly GATUZ dashboard with per-farm reporting shortcuts."""

import tkinter as tk
from datetime import date

import app as existing_app
import database as db

BG = "#061b15"
BG2 = "#0b2119"
PANEL = "#123b2d"
PANEL_ALT = "#184635"
PANEL_DEEP = "#0b221b"
PANEL_TOP = "#1a4e3b"
SHADOW = "#020d0a"
GREEN = "#2e6b45"
GOLD = "#d6b45c"
TEXT = "#f3f2e9"
MUTED = "#a9b9ae"
HIGHLIGHT = "#2c5443"

EGG_TOTAL = "COALESCE(jumbo,0)+COALESCE(xl,0)+COALESCE(large,0)+COALESCE(medium,0)+COALESCE(small,0)+COALESCE(peewee,0)"
GRADE_FIELDS = (("Peewee", "peewee"), ("Small", "small"), ("Medium", "medium"), ("Large", "large"), ("XL", "xl"), ("Jumbo", "jumbo"))


class FriendlyGatuzApp(existing_app.GatuzApp):
    """Keep the existing screens and replace only the dashboard renderer."""

    def _dash_card(self, parent, title, value, note="", accent=TEXT):
        shell = tk.Frame(parent, bg=SHADOW)
        shell.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        card = tk.Frame(shell, bg=PANEL, padx=16, pady=14, highlightthickness=1,
                        highlightbackground=HIGHLIGHT, bd=0, relief="raised")
        card.pack(fill="both", expand=True, padx=2, pady=2)
        tk.Label(card, text=title, bg=PANEL, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(card, text=value, bg=PANEL, fg=accent, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(6, 0))
        if note:
            tk.Label(card, text=note, bg=PANEL, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=(2, 0))
        return shell

    def _dash_panel(self, parent, title, subtitle=""):
        shell = tk.Frame(parent, bg=SHADOW)
        shell.pack(fill="both", expand=True, padx=4, pady=4)
        panel = tk.Frame(shell, bg=PANEL, padx=14, pady=12, highlightthickness=1,
                         highlightbackground=HIGHLIGHT, bd=0, relief="raised")
        panel.pack(fill="both", expand=True, padx=2, pady=2)
        tk.Label(panel, text=title, bg=PANEL, fg=GOLD, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(panel, text=subtitle, bg=PANEL, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=(3, 4))
        return panel

    def _dash_chart(self, parent, labels, values, ylabel, kind="line", color=GOLD):
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            fig = Figure(figsize=(4.8, 2.0), dpi=85)
            ax = fig.add_subplot(111)
            if labels:
                if kind == "bar":
                    ax.bar(labels, values, color=color, width=0.62)
                else:
                    ax.plot(labels, values, marker="o", linewidth=2, color=color)
            else:
                ax.text(0.5, 0.5, "Wala pang datos. Magdagdag ng records para makita ang trend.",
                        ha="center", va="center", color=MUTED, wrap=True, transform=ax.transAxes, fontsize=8)
                ax.set_xticks([])
                ax.set_yticks([])
            ax.set_facecolor(PANEL)
            fig.patch.set_facecolor(PANEL)
            ax.tick_params(colors=MUTED, labelsize=7, labelrotation=25)
            for spine in ax.spines.values():
                spine.set_color("#345542")
            ax.set_ylabel(ylabel, color=MUTED, fontsize=8)
            ax.grid(axis="y", color="#264533", linewidth=0.5, alpha=0.65)
            fig.tight_layout(pad=1.2)
            chart = FigureCanvasTkAgg(fig, master=parent)
            chart.draw()
            chart.get_tk_widget().pack(fill="both", expand=True, pady=(4, 0))
            return chart
        except Exception:
            tk.Label(parent, text="Hindi maipakita ang graph. I-install muli ang dependencies gamit ang START_GATUZ.bat.",
                     bg=PANEL, fg=MUTED, wraplength=360, justify="left").pack(anchor="w", pady=12)
            return None

    def dashboard(self):
        self.current_page = self.dashboard
        self.page("Farm Dashboard", "Pangkalahatang tanaw ng farm. Piliin ang farm sa itaas o sa mga card sa ibaba.")
        body = self.body()
        farm_id = self.selected_farm()
        active_farms = db.farm_rows()
        selected_name = self.farm_filter.get()

        farm_section = tk.Frame(body, bg=BG)
        farm_section.pack(fill="x", pady=(0, 7))
        tk.Label(farm_section, text="FARM MANAGEMENT", bg=BG, fg=GOLD,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=4)
        tk.Label(farm_section, text="Pumili ng farm o pindutin ang Gumawa ng Report para sa farm na iyon.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", padx=4, pady=(1, 3))
        farm_cards = tk.Frame(farm_section, bg=BG)
        farm_cards.pack(fill="x")
        shown_farms = active_farms[:4]
        for col, farm in enumerate(shown_farms):
            is_selected = selected_name == farm["name"]
            shell = tk.Frame(farm_cards, bg=SHADOW)
            shell.grid(row=0, column=col, sticky="nsew", padx=4, pady=4)
            farm_cards.grid_columnconfigure(col, weight=1)
            tile = tk.Frame(shell, bg=PANEL_TOP if is_selected else PANEL_DEEP, padx=10, pady=9,
                            highlightthickness=1, highlightbackground=GOLD if is_selected else HIGHLIGHT,
                            bd=0, relief="raised")
            tile.pack(fill="both", expand=True, padx=2, pady=2)
            tk.Button(tile, text=farm["name"],
                      command=lambda name=farm["name"]: self._choose_dashboard_farm(name),
                      bg=tile.cget("bg"), fg=TEXT, activebackground=GREEN, activeforeground="white",
                      anchor="w", justify="left", wraplength=150, relief="flat",
                      font=("Segoe UI", 9, "bold"), cursor="hand2").pack(fill="x")
            location = farm["location"] or "Lokasyon hindi pa nailalagay"
            tk.Label(tile, text=location, bg=tile.cget("bg"), fg=MUTED,
                     font=("Segoe UI", 8)).pack(anchor="w", pady=(3, 6))
            tk.Button(tile, text="▤  Gumawa ng Report",
                      command=lambda name=farm["name"]: self._open_farm_report(name),
                      bg=GREEN, fg="white", activebackground=GOLD, activeforeground="#101010",
                      relief="flat", font=("Segoe UI", 8, "bold"), cursor="hand2",
                      padx=7, pady=5).pack(fill="x", pady=(1, 0))

        add_col = len(shown_farms)
        farm_cards.grid_columnconfigure(add_col, weight=1)
        add_shell = tk.Frame(farm_cards, bg=SHADOW)
        add_shell.grid(row=0, column=add_col, sticky="nsew", padx=4, pady=4)
        add_tile = tk.Frame(add_shell, bg=BG2, padx=8, pady=8, highlightthickness=1,
                            highlightbackground="#8a793c", bd=0, relief="raised")
        add_tile.pack(fill="both", expand=True, padx=2, pady=2)
        tk.Button(add_tile, text="＋  Magdagdag ng Farm", command=self.farms_page,
                  bg=BG2, fg=GOLD, activebackground=GREEN, activeforeground="white",
                  relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2").pack(expand=True, fill="both")
        if len(active_farms) > len(shown_farms):
            tk.Label(farm_section, text=f"Ipinapakita ang unang {len(shown_farms)} sa {len(active_farms)} farms. Gamitin ang Farm view filter para sa iba.",
                     bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", padx=4)

        stats = db.farm_stats(farm_id)
        where = " WHERE farm_id=?" if farm_id is not None else ""
        args = (farm_id,) if farm_id is not None else ()
        with db.connect() as conn:
            birds_row = conn.execute("SELECT COALESCE(SUM(bird_count),0) AS n FROM flocks WHERE status='Active'" + where, args).fetchone()
            total_sales_row = conn.execute("SELECT COALESCE(SUM(total),0) AS n FROM sales" + where, args).fetchone()
        birds = int(birds_row["n"] or 0)
        eggs = int(stats["eggs"] or 0)
        sales_total = float(total_sales_row["n"] or 0)
        kpi_row = tk.Frame(body, bg=BG)
        kpi_row.pack(fill="x", pady=(2, 5))
        self._dash_card(kpi_row, "Aktibong Manok", f"{birds:,}", "Batay sa aktibong flock records")
        self._dash_card(kpi_row, "Nakolektang Itlog", f"{eggs:,}", "Kabuuang naitalang production")
        self._dash_card(kpi_row, "Kabuuang Benta", f"₱{sales_total:,.2f}", "Batay sa sales records")
        self._dash_card(kpi_row, "Hindi Pa Bayad", f"₱{float(stats['balance']):,.2f}", "Natitirang balance", GOLD)

        prod_where = " WHERE day >= date('now','-30 days')" + (" AND farm_id=?" if farm_id is not None else "")
        prod_args = (farm_id,) if farm_id is not None else ()
        with db.connect() as conn:
            daily = conn.execute(
                f"SELECT day, SUM({EGG_TOTAL}) AS eggs FROM production{prod_where} GROUP BY day ORDER BY day DESC LIMIT 8",
                prod_args).fetchall()
            today_row = conn.execute(
                f"SELECT COALESCE(SUM({EGG_TOTAL}),0) AS eggs FROM production WHERE day=?" + (" AND farm_id=?" if farm_id is not None else ""),
                (date.today().isoformat(), farm_id) if farm_id is not None else (date.today().isoformat(),)).fetchone()
            month_row = conn.execute(
                f"SELECT COALESCE(SUM({EGG_TOTAL}),0) AS eggs, COUNT(DISTINCT day) AS days FROM production WHERE substr(day,1,7)=substr(date('now'),1,7)" + (" AND farm_id=?" if farm_id is not None else ""),
                args).fetchone()
            grades = conn.execute(
                "SELECT " + ",".join(f"COALESCE(SUM({field}),0) AS {field}" for _, field in GRADE_FIELDS) + " FROM production" + where,
                args).fetchone()
        daily = list(reversed(daily))

        mid = tk.Frame(body, bg=BG)
        mid.pack(fill="both", expand=True, pady=4)
        prod_panel = self._dash_panel(mid, "Poultry Extension — Egg Production",
                                      "Aktuwal na egg count sa pinakahuling 30 araw; hindi ito age-based percentage.")
        prod_panel.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        self._dash_chart(prod_panel, [r["day"][5:] for r in daily],
                         [int(r["eggs"] or 0) for r in daily], "Itlog", "line", GOLD)

        summary_panel = self._dash_panel(mid, "Egg Production Summary", "Batay sa kasalukuyang talaan")
        summary_panel.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        summary_lines = (
            ("Produksyon ngayong araw", f"{int(today_row['eggs'] or 0):,} itlog"),
            ("Average ngayong buwan", f"{(int(month_row['eggs'] or 0) / max(int(month_row['days'] or 0), 1)):,.0f} itlog/araw"),
            ("Average egg weight", "Hindi pa itinatala"),
            ("Age-based hen-day rate", "Kailangan ng flock history"),
        )
        for label, value in summary_lines:
            line = tk.Frame(summary_panel, bg=PANEL)
            line.pack(fill="x", pady=8)
            tk.Label(line, text=label, bg=PANEL, fg=MUTED, font=("Segoe UI", 8)).pack(side="left", anchor="w")
            tk.Label(line, text=value, bg=PANEL, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(side="right", anchor="e")

        bottom = tk.Frame(body, bg=BG)
        bottom.pack(fill="both", expand=True, pady=4)
        grade_panel = self._dash_panel(bottom, "Egg Size Classification", "Kabuuang bilang ayon sa egg grade na naitala")
        grade_panel.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        grade_row = tk.Frame(grade_panel, bg=PANEL)
        grade_row.pack(fill="x", expand=True, pady=(12, 3))
        for label, field in GRADE_FIELDS:
            value = int(grades[field] or 0)
            cell = tk.Frame(grade_row, bg=PANEL_ALT, padx=5, pady=9)
            cell.pack(side="left", fill="both", expand=True, padx=2)
            tk.Label(cell, text=f"{value:,}", bg=PANEL_ALT, fg=GOLD, font=("Segoe UI", 10, "bold")).pack()
            tk.Label(cell, text=label, bg=PANEL_ALT, fg=MUTED, font=("Segoe UI", 7)).pack(pady=(3, 0))

        grades_panel = self._dash_panel(bottom, "Production Mix", "Bahagi ng bawat grade sa lahat ng nakolektang itlog")
        grades_panel.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        total_grade = sum(int(grades[field] or 0) for _, field in GRADE_FIELDS)
        for label, field in GRADE_FIELDS:
            count = int(grades[field] or 0)
            pct = (count / total_grade * 100) if total_grade else 0
            row = tk.Frame(grades_panel, bg=PANEL)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, bg=PANEL, fg=MUTED, font=("Segoe UI", 8), width=8, anchor="w").pack(side="left")
            bar = tk.Canvas(row, height=9, bg=PANEL_ALT, highlightthickness=0)
            bar.pack(side="left", fill="x", expand=True, padx=5)
            bar.update_idletasks()
            bar.create_rectangle(0, 0, max(1, bar.winfo_width() * pct / 100), 9, fill=GOLD, outline="")
            tk.Label(row, text=f"{pct:.0f}%", bg=PANEL, fg=TEXT, font=("Segoe UI", 8), width=5).pack(side="right")

        lower = tk.Frame(body, bg=BG)
        lower.pack(fill="both", expand=True, pady=4)
        sales_panel = self._dash_panel(lower, "Sales & Receipts", "Benta kada buwan — huling 6 na buwang may records")
        sales_panel.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        with db.connect() as conn:
            sales_by_month = conn.execute(
                "SELECT substr(day,1,7) AS month, SUM(total) AS amount FROM sales WHERE day IS NOT NULL" +
                (" AND farm_id=?" if farm_id is not None else "") +
                " GROUP BY substr(day,1,7) ORDER BY month DESC LIMIT 6",
                args).fetchall()
        sales_by_month = list(reversed(sales_by_month))
        self._dash_chart(sales_panel, [r["month"] for r in sales_by_month],
                         [float(r["amount"] or 0) for r in sales_by_month], "PHP", "bar", GOLD)

        activity_panel = self._dash_panel(lower, "Recent Activities", "Pinakahuling naitalang galaw")
        activity_panel.pack(side="left", fill="both", expand=True, padx=3, pady=3)
        activities = db.recent_activity(farm_id, limit=5)
        if activities:
            for day, description, _farm_id in activities:
                tk.Label(activity_panel, text=f"•  {day}  {description}", bg=PANEL, fg=TEXT, anchor="w",
                         justify="left", wraplength=360, font=("Segoe UI", 8)).pack(fill="x", pady=5)
        else:
            tk.Label(activity_panel, text="Wala pang aktibidad. Magsimula sa pagdagdag ng farm, flock, o egg collection.",
                     bg=PANEL, fg=MUTED, wraplength=350, justify="left", font=("Segoe UI", 8)).pack(anchor="w", pady=12)

    def _choose_dashboard_farm(self, name):
        self.farm_filter.set(name)
        self.dashboard()

    def _open_farm_report(self, name):
        """Open report export options with the selected farm pre-filtered."""
        self.farm_filter.set(name)
        self.reports_page()


if __name__ == "__main__":
    root = tk.Tk()
    FriendlyGatuzApp(root)
    root.mainloop()
