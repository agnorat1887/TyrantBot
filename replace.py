ans = ""
with open("Server Info/Infiltrator raw.txt", 'r') as f:
    for x in f:
        for i in x:
            if i != " ":
                ans += "█"
            elif i == " ":
                ans += " "
        ans += "\n"
with open("Server Info/Infiltrator.txt", 'wb') as n:
    n.write(ans.encode('utf-8'))