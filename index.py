from whatsapp import WhatsApp

wpp = WhatsApp()
grupo = 'grupo teste'
wpp.mention_all_group(grupo)
wpp.send_message(grupo, 'teste tavin')
wpp.exit()