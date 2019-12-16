from socket import socket, AF_INET, SOCK_DGRAM


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    source_ip = '0.0.0.0'
    source_port = 12345
    s.bind((source_ip, source_port))
    client=[];
    strclient = ""
    #dictionary of buffet info for each clients
    BufferInfoDic = {}
    while True:
        data, sender_info = s.recvfrom(2048)
        if data.decode()[0] == '1':
            sinfo=(data.decode()[1:].strip(),sender_info);
            #send to user all clients names
            if strclient:
                s.sendto(strclient.strip().encode(), sender_info)
            else:
                s.sendto("".encode(), sender_info)
            #add name with ip and port to list
            client.append(sinfo);
            #add to string the name of the person that joined the group
            strclient += data.decode()[2:]
            strclient += ", "
            #call func join
            join(s, data, sender_info, client, BufferInfoDic)
        #send all messages stock in dictionary
        if data.decode()[0] == '5':
            if sender_info in BufferInfoDic:
                refresh(s, sender_info, BufferInfoDic)
            else:
                s.sendto("".encode(), sender_info)
        #send to dictionary message to all user without sending to the sender
        if data.decode()[0] == '2':
            sendMessage(s, data, sender_info, client, BufferInfoDic)
        # change the name in list and string and send nessage to all of the users
        if data.decode()[0] == '3':
            i=0
            namehlpr = ""
            #access to list name and change it
            senderinfo = ""
            for name, info in client:

                if info == sender_info:
                    namehlpr = name
                    #change also content in string strclient
                    strclient = strclient.replace(name.strip() + ",", data.decode()[2:].strip() + ",")
                    strclient = strclient.lstrip()
                    break
                i += 1
            client[i] = (data.decode()[1:], sender_info);
            changeName(s, data, sender_info, client, BufferInfoDic, namehlpr)
        #delete account
        if data.decode()[0] == '4':
            namehlper = ""
            for name , info in client:
                if info == sender_info:
                    namehlper = name
            left(s, data, sender_info, client, BufferInfoDic, namehlper)
            sinfo = (namehlper, sender_info);
            client.remove(sinfo)
            strclient = strclient.replace(namehlper.strip() + ", ", " ")
            strclient = strclient.lstrip()

#join the group
def join(s, data, sender_info, client, bufferinfodic):
    for x,y in client:
        if y != sender_info:

            #if sender info key exist in dictionary
            if y in bufferinfodic:
                bufferinfodic[y] = bufferinfodic[y] + ";" + data.decode()[2:] + " has joined"
            else:
                bufferinfodic[y] = data.decode()[2:] + " has joined"

#refresh the message in the dic for specified user
def refresh(s, sender_info, bufferinfodic):
    s.sendto(bufferinfodic[sender_info].encode(), sender_info)
    bufferinfodic.pop(sender_info)

#send message to every one
def sendMessage(s, data, sender_info, client, bufferinfodic):
    senderName = ""
    #access name of sender message
    for name , info in client:
        if info == sender_info:
            senderName = name
    for x,y in client:
        if y != sender_info:
            #if sender info key exist in dictionary
            if y in bufferinfodic:
                bufferinfodic[y] = bufferinfodic[y] + ";" + senderName.strip() + ': ' + data.decode()[2:]
            else:
                bufferinfodic[y] = senderName.strip() + ': ' + data.decode()[2:]

#change name
def changeName(s, data, sender_info, client, bufferinfodic, name):
    for x,y in client:
        if y != sender_info:
            #if sender info key exist in dictionary
            if y in bufferinfodic:
                bufferinfodic[y] = bufferinfodic[y] + ";" + name.strip() + " ‫‪changed‬‬ ‫‪his‬‬ ‫‪name‬‬ ‫‪to " + data.decode()[2:]
            else:
                bufferinfodic[y] = name.strip() + " ‫‪changed‬‬ ‫‪his‬‬ ‫‪name‬‬ ‫‪to " + data.decode()[2:]

#left the group
def left(s, data, sender_info, client, bufferinfodic, name):
    for x,y in client:
        if y != sender_info:
            #if sender info key exist in dictionary
            if y in bufferinfodic:
                bufferinfodic[y] = bufferinfodic[y] + ";" + name.strip() + " ‫‪has‬‬ ‫‪left‬‬ ‫‪the‬‬ ‫‪group‬‬"
            else:
                bufferinfodic[y] = name.strip() + " ‫‪has‬‬ ‫‪left‬‬ ‫‪the‬‬ ‫‪group‬‬"


main()




