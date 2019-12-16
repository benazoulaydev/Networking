from socket import socket, AF_INET, SOCK_DGRAM

def main():
    s = socket(AF_INET, SOCK_DGRAM)
    dest_ip = '127.0.0.1'
    dest_port = 12345
    msg = input()

     #if message not equal to "" print it
    strhelper = msg[0]
    i = 0
    #infinite loop for user
    while 1:
        #if create account
        if strhelper == "1":
            #if not legal form
            if len(msg) <= 2 or msg[1] != " " :
                print("‫‪Illegal‬‬ ‫‪request‬‬")
                msg = input()
                strhelper = msg[0]
            else :
                #print list client when click on 1 only once
                if i == 0:
                    i = 1
                    #send to server the message
                    s.sendto(msg.encode(), (dest_ip, dest_port))
                    #receive the data from server
                    data, sender_info = s.recvfrom(2048)
                    #if data not empty print it
                    if data.decode():
                        print(data.decode()[:-1])
                msgGroup = input()
                #if message not equal to "" illegal
                if len(msgGroup) > 1 and msgGroup[1] != " ":
                    print("‫‪Illegal‬‬ ‫‪request‬‬")
                    continue
                #refresh messages
                elif msgGroup[0] == "5":
                    s.sendto(msgGroup.encode(), (dest_ip, dest_port))
                    data, sender_info = s.recvfrom(2048)
                    if data.decode():
                        for x in data.decode().split(";"):
                            print(x)
                #send a message
                elif msgGroup[0] == "2":
                    if not len(msgGroup) > 1:
                        print("‫‪Illegal‬‬ ‫‪request‬‬")
                    else :
                        s.sendto(msgGroup.encode(), (dest_ip, dest_port))
                    continue
                # change name
                elif msgGroup[0] == "3":
                    if not len(msgGroup) > 1:
                        print("‫‪Illegal‬‬ ‫‪request‬‬")
                    else :
                        s.sendto(msgGroup.encode(), (dest_ip, dest_port))
                    continue
                elif msgGroup[0] == "4":
                    s.sendto(msgGroup.encode(), (dest_ip, dest_port))
                    main()
                # if 1 is resend after login
                elif msgGroup[0] == "1":
                    print("‫‪Illegal‬‬ ‫‪request‬‬")
                    continue
        else :
            print("‫‪Illegal‬‬ ‫‪request‬‬")
            msg = input()
            strhelper = msg[0]
            #reset i to 0
            i = 0
    s.close()

main()











