#!/bin/bash
download() {
  local name="$1"
  local url="$2"
  echo "Downloading: $name"
  curl -sL "$url" -o "$name" && echo "  OK: $name ($(wc -c < "$name") bytes)" || echo "  FAIL: $name"
}

download "逆龙道.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E3%80%8A%E9%80%86%E9%BE%99%E9%81%93%E3%80%8B%E4%BD%9C%E8%80%85%EF%BC%9A%E8%A1%80%E7%BA%A2-c132e762a2656af86050233ada96697a.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331150090&Signature=jBHx3NwSOry/sWxCvte0DJovudI=" &
download "太阳王之证.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/48289c84-2022-447e-8d37-1873cf131355.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331151841&Signature=utkCIEgnaenOmEPKte1GwLlsHPw=" &
download "偷天.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E3%80%8A%E5%81%B7%E5%A4%A9%E3%80%8B%E4%BD%9C%E8%80%85%EF%BC%9A%E8%A1%80%E7%BA%A2-b9b460cc4adced1cd1cc2a364100f968.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331150951&Signature=1Pv2xCV7PBQChfKr/PxrpT7s+KM=" &
download "邪龙道.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E3%80%8A%E9%82%AA%E9%BE%99%E9%81%93%E3%80%8B%E4%BD%9C%E8%80%85%EF%BC%9A%E8%A1%80%E7%BA%A2-4aaa9408bc5e4513d1717ab41af94391.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331150672&Signature=wK4m6nj0vmV5PNVi3uKtf8nK1oQ=" &
wait
download "光明纪元.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/41467eac-c9ef-47f4-b415-dbcfe6ef826c.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331152280&Signature=EWG3qCCQstoPFidj37HN9Ri52Es=" &
download "开天录.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E3%80%8A%E5%BC%80%E5%A4%A9%E5%BD%95%E3%80%8B%E4%BD%9C%E8%80%85%EF%BC%9A%E8%A1%80%E7%BA%A2-aff9259e8ca2bf11416f3fc15bf929b8.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331151322&Signature=p28LpsdYEBZ07yC6cQEn1rtrUKg=" &
download "暗影神座.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E6%9A%97%E5%BD%B1%E7%A5%9E%E5%BA%A7-54bcf8ce4fb520fdd545eb761daf2106.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331156237&Signature=e+/fMHd2Sch7FpCmcPt4O418JCg=" &
download "暴风法神.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E6%9A%B4%E9%A3%8E%E6%B3%95%E7%A5%9E-a48c4932bd00671d5dbe8cfc4418e87d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331156828&Signature=eLNbcPVEo0UJkZ20kw9jZllx1I0=" &
wait
download "不死武皇.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E4%B8%8D%E6%AD%BB%E6%AD%A6%E7%9A%87-01d77ab6de57caa6528b2a6875baedbe.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331156938&Signature=DXSUi7mThKD3XpOKab+qVzLOmPI=" &
download "沧元图.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E6%B2%A7%E5%85%83%E5%9B%BE-6dc79535419807743836d5e992130a65.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331157101&Signature=GArlplfOMMuLJGvgaQC30MwzFaQ=" &
download "超凡黎明.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E8%B6%85%E5%87%A1%E9%BB%8E%E6%98%8E-a277d3e11a42a2ef4c452b429580eaa8.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331156999&Signature=Br8zVWD0IinbLxWmxEJCFHNo0ds=" &
download "传奇族长.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E4%BC%A0%E5%A5%87%E6%97%8F%E9%95%BF-5ea9b7da144405f39a80008352fc7092.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331157484&Signature=ZNXBOc9n3us2bg9z3dFFBeXF1Ng=" &
wait
download "寸芒.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E5%AF%B8%E8%8A%92-d4486dca7397e962f15787971f574f3d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331157026&Signature=UkkVMCgW43xydZE6L3L4uvycT4A=" &
download "大奉打更人.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E5%A4%A7%E5%A5%89%E6%89%93%E6%9B%B4%E4%BA%BA-537cfaecc5e08af5753c1471ae4df875.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331157114&Signature=qa2z72+2pmwNnjiE7buG+2tq/A4=" &
download "大荒蛮神.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E5%A4%A7%E8%8D%92%E8%9B%AE%E7%A5%9E-fac6c110904e3acd49e1e9c99064d29f.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331157491&Signature=uoN7ypdQqEffG1xET8Vqvm9yrYw=" &
download "大周皇族.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E5%A4%A7%E5%91%A8%E7%9A%87%E6%97%8F-84d58a907ab408c88ab8f694b917fd88.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331157492&Signature=MUkvz/HaePIWarwIlIGYkQmtyOw=" &
download "大主宰.txt" "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/%E5%A4%A7%E4%B8%BB%E5%AE%B0-ed1cd8f85415fc8521e24ba45d8bf570.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808331157485&Signature=lGboOM2mPLNITvu7l+g+KOgNuWQ=" &
wait
echo "=== ALL DONE ==="
ls -lh *.txt | wc -l
ls -lh *.txt
