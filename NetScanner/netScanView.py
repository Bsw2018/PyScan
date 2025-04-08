# This is a class for having a view for the NetScanner class
# The NetScanner is the controller for the netScanView class
import tkinter as tk
from tkinter import ttk
from net_scan import NetScanner



class netScanView(tk.Tk):

    

    def __init__(self, scanner):
        super().__init__()          


        self.title("Network Scanner")
        self.scanner = scanner

        self.tab_control = ttk.Notebook(self)
        
        # Interface Tab
        self.interface_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.interface_tab, text='Interfaces Scan')

        self.interface_tree = ttk.Treeview(self.interface_tab)
        self.interface_tree["columns"] = ("Family", "Address", "Netmask", "Broadcast")

        self.interface_tree.heading("#0", text="Interface", anchor=tk.W)
        self.interface_tree.column("#0", width=120, anchor=tk.W)

        for col in self.interface_tree["columns"]:
            self.interface_tree.column(col, width=120, anchor=tk.W)
            self.interface_tree.heading(col, text=col, anchor=tk.W)

        self.populate_interface_tree()
        self.interface_tree.pack(fill=tk.BOTH, expand=True)

        # Port Scan Tab
        self.portscan_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.portscan_tab, text='Port Scans')

        self.portscan_tree = ttk.Treeview(self.portscan_tab)
        self.portscan_tree["columns"] = ("Open Ports",)

        self.portscan_tree.column("#0", width=150, anchor=tk.W)
        self.portscan_tree.heading("#0", text="Interface", anchor=tk.W)
        self.portscan_tree.column("Open Ports", width=300, anchor=tk.W)
        self.portscan_tree.heading("Open Ports", text="Open Ports", anchor=tk.W)

        self.populate_portscan_tree()
        self.portscan_tree.pack(fill=tk.BOTH, expand=True)

        self.tab_control.pack(expand=1, fill="both")

    def populate_interface_tree(self):
            interfaces = self.scanner.scan_interfaces()
            for interface, details in interfaces.items():
                parent = self.interface_tree.insert("", tk.END, text=interface, open=True)
                for addr in details:
                    self.interface_tree.insert(parent, tk.END, text="", values=(
                        addr.family, addr.address, addr.netmask, addr.broadcast
                        ))
        
    def populate_portscan_tree(self):
            interfaces = self.scanner.scan_interfaces()
            for interface, details in interfaces.items():
                    addresses = [addr.address for addr in details if '.' in addr.address]
                    ports_info = []
                    for addr in addresses:
                        open_ports = self.scanner.scan_ports(addr)
                        if open_ports:
                            ports_info.extend([f"{addr}:{port}" for port in open_ports])
                            ports_str = ', '.join(ports_info) if ports_info else 'No open ports found'
                            self.portscan_tree.insert("", tk.END, text=interface, values=(ports_str,))




def main():

    netscanner = NetScanner()


    netScanApp = netScanView(netscanner)
    netScanApp.mainloop()

if __name__ == "__main__":

    main()