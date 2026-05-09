#!/bin/bash
d(){ echo "DL: $1"; curl -sL "$2" -o "$1" && echo "  OK $(wc -c < "$1")" || echo "  FAIL"; }
d "点道为止.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E7%82%B9%E9%81%93%E4%B8%BA%E6%AD%A2-26cfc8b082eab92ff2eaa33a3089d221.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331616472&Signature=FhpKsexlwUNKGPrewkz5xiRs/Zg=" &
d "斗破苍穹.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E6%96%97%E7%A0%B4%E8%8B%8D%E7%A9%B9-595825254357facb3855305ade680c95.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331616830&Signature=E37V8b4I/CEx6h9i7eTuSL65Ddo=" &
d "法师传奇.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E6%B3%95%E5%B8%88%E4%BC%A0%E5%A5%87-2903844bc812ce10adb646756f38863d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331615104&Signature=TxU2QhHHrh5cirW/P8fFurnW0HU=" &
d "飞剑问道.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E9%A3%9E%E5%89%91%E9%97%AE%E9%81%93-1660c97e19a1024204846957690a3ef5.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331614866&Signature=oOtiYyI4L2TK0N0n+FrOmS3ZLPg=" &
wait
d "飞升之后.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E9%A3%9E%E5%8D%87%E4%B9%8B%E5%90%8E-76bc405403b7ce0e4e08fd2a494b4d8d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331617228&Signature=Dpu/QyQWpLvI1pyGDxCbcyxEqBs=" &
d "佛本是道.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E4%BD%9B%E6%9C%AC%E6%98%AF%E9%81%93-59ae58d83b3b55842af5ab59f9052720.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331614905&Signature=nmoF9tBnDVJGqm5YS+Hmp7m8DVM=" &
d "苟在妖武.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E8%8B%9F%E5%9C%A8%E5%A6%96%E6%AD%A6%E4%B9%B1%E4%B8%96%E4%BF%AE%E4%BB%99%20(1)-943e0827855c9b6c747dd6ff7c7f0137.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331617005&Signature=6qp9fAH0GmmvImjhtj+VnM0ZqX4=" &
d "蛊惑魔王.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E8%9B%8A%E6%83%91%E9%AD%94%E7%8E%8B-af4c2e9e4c584e68049176b387ff4cb9.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331615425&Signature=woFnJxaeeEzgrhMJCMecWW0HWkI=" &
wait
d "诡秘如风常伴吾身.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E8%AF%A1%E7%A7%98%E5%A6%82%E9%A3%8E%EF%BC%8C%E5%B8%B8%E4%BC%B4%E5%90%BE%E8%BA%AB-c8a56c07fa72118824ae64bfa9e7e8ae.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331614918&Signature=rJSBoylQ6dKdyA0kZwZNmgvvcwM=" &
d "诡秘之主.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E8%AF%A1%E7%A7%98%E4%B9%8B%E4%B8%BB-2fc2e5714cb44436ba3c50bc3b48ea9b.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331617470&Signature=QX3H77vOgoHyqcLJLRs956BApfQ=" &
d "哈利波特之学霸传奇.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E5%93%88%E5%88%A9%E6%B3%A2%E7%89%B9%E4%B9%8B%E5%AD%A6%E9%9C%B8%E4%BC%A0%E5%A5%87-5df73ea9bec9e2efeafb2c77bf5226d4.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331615138&Signature=wz1Bs8uNfLz/Q7PGMRQ20jffc/A=" &
d "汉阙.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E6%B1%89%E9%98%99-d2505221f2e4e6dc3135e531c4922302.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331616580&Signature=NTcngwBGyKbxbqgSrW+Dqul6lJY=" &
wait
d "黄龙真人异界游.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E9%BB%84%E9%BE%99%E7%9C%9F%E4%BA%BA%E5%BC%82%E7%95%8C%E6%B8%B8-7289fc82de32dbb507037f35c845d2e3.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331615706&Signature=a8EWL4tP6j9hr2K2CGGmrCAOfU4=" &
d "极道天魔.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E6%9E%81%E9%81%93%E5%A4%A9%E9%AD%94-72858e10e8386ea765a261a7b31ea229.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331615953&Signature=Ow1ySlBAD4q0Cg3zMv/oSgrRgXg=" &
d "剑来.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E5%89%91%E6%9D%A5-2759f5373218d52ef58f5d6e22372dfc.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331618498&Signature=kH3vWqvbnUUNg3JBx684u600hJg=" &
d "九鼎记.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E4%B9%9D%E9%BC%8E%E8%AE%B0-13a2050f776dd98a8ae312aac25932b2.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331615757&Signature=r47DWZdQIW/KLWScnhCROW4Bdj4=" &
d "黎明之剑.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E9%BB%8E%E6%98%8E%E4%B9%8B%E5%89%91-2a1c818327378538a01c16dea09f2a29.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331617824&Signature=1simvFiRFoC1iI+0vhcqth8DDPs=" &
wait
echo "=== DONE ==="
ls *.txt | wc -l
