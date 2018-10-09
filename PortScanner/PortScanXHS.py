import PortScanner as ps
import xlrd


def main():
    IpOpenPortsFile = open("/Users/zr/Desktop/IpOpenPorts.csv", "w+")
    ip_excel = xlrd.open_workbook("/Users/zr/Desktop/waiwangip.xlsx")
    ip = set()
    for sheet in ip_excel.sheets():
        nrows = sheet.nrows
        for i in range(0, nrows):
            ip.add(sheet.row_values(i)[0])
            print sheet.row_values(i)[0]

    # Initialize a Scanner object that will scan top 1000 commonly used ports.
    scanner = ps.PortScanner(target_ports=1000)
    message = ''
    scanner.set_thread_limit(1500)
    scanner.set_delay(15)

    for one in ip:
        openPorts = scanner.scan(one, message)
        IpOpenPortsFile.write(one+","+('.'.join(list(map(str, openPorts))))+"\n")


if __name__ == "__main__":
    main()
