import codecs
def writeChars(theFile,text):
	f = codecs.open(theFile,"w+", "utf-8")
	s = ""
	ite = 0
	while ite < len(text):
		if text[ite] == "`":
			specChar = text[ite+1:ite+4]
			if specChar == "ent":
				temp = u"\u000a"#line feed
				s = s + temp
			if specChar == "bac":
				temp = u"\u007f"#delete
				s = s + temp
			if specChar == "esc":
				temp = u"\u001b"#escape
				s = s + temp
			ite = ite + 3
		else:
			s = s + text[ite]
		ite += 1
	f.write(s)
	f.close




writeChars("test7.txt","abcd|bacef|entghi" )
