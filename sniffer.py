from scapy.sendrecv import sniff
from scapy.utils import wrpcap
from scapy import route
from matplotlib import pyplot
import dpkt
import socket
import datetime

pkt = sniff(count=100)
wrpcap("demo.pcap", pkt)
xticks = []
dic = {}

def printPcap(pcap):
    try:
        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)  # 获得以太包，即数据链路层包
            print("mac layer:" + eth.__class__.__name__)  # 以太包的既是数据链路层包
            print("ip layer:" + eth.data.__class__.__name__)  # 数据链路层包的数据既是网络层包
            print("tcp layer:" + eth.data.data.__class__.__name__)  # 网络层包的数据既是传输层包
            if eth.data.data.__class__.__name__ in dic:
                dic[eth.data.data.__class__.__name__] = dic.get(eth.data.data.__class__.__name__) + 1
            else:
                xticks.append(eth.data.data.__class__.__name__)
                dic[eth.data.data.__class__.__name__] = 1
            print("http layer:" + eth.data.data.data.__class__.__name__)  # 传输层包的数据既是应用层包
            print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))  # 打印出包的抓取时间
            if not isinstance(eth.data, dpkt.ip.IP):
                print('Non IP Packet type not supported %s' % eth.data.__class__.__name__)
                continue
            mac = eth
            ip = eth.data
            tcp = eth.data.data
            print('MAC:' + str(mac.src) + '->' + str(mac.dst))
            # print(mac.src)
            # print(mac.dst)
            # print(tcp.sport)
            # print(tcp.dport)
            do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
            print('IP: %s -> %s (len=%d ttl=%d DF=%d MF=%d offset=%d)' % (
                socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments,
                fragment_offset))
            print('PORT:' + str(tcp.sport) + '->' + str(tcp.dport))

    except:
        pass


def main():
    f = open('demo.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)
    r = route.Route()
    print(r)
    pyplot.bar(range(len(xticks)), [dic.get(xtick, 0) for xtick in xticks], align='center')
    pyplot.xticks(range(len(xticks)), xticks)
    pyplot.xlabel("Types of Protocol")
    pyplot.ylabel("Frequency")
    pyplot.title("Numbers of current Protocol")
    pyplot.show()

if __name__ == '__main__':
    main()
