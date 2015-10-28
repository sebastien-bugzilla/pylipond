# -*- coding:Utf-8 -*-
#!/usr/bin/python
from gi.repository import Gtk
from datetime import datetime
import commands

class createScore(Gtk.Window):
	
	def __init__(self):
		
		# Généralités sur le nom de la fenêtre
		Gtk.Window.__init__(self, title="Création de partitions")
		self.set_border_width(10)
		self.set_size_request(800, 200)
		self.fixed = Gtk.Fixed()
		
		typePartition=["Partition Simple", "Partition à plusieurs mouvements", "Partition à plusieurs voix", "Partition pour piano", "Partition pour ensemble"]
		
		labelDossier = Gtk.Label("Dossier de travail :")
		labelFichier = Gtk.Label("Nom du fichier :")
		labelTypePartition = Gtk.Label("Type de partition :")
		labelNbreMvt = Gtk.Label("Nombre de mouvements :")
		labelNbreVoix = Gtk.Label("Nombre de voix :")
		labelNbreMesure = Gtk.Label("Nombre de mesures :")
		labelVoixSupInf = Gtk.Label("Nombre de Voix Sup / Inf :")
		entryDossier = Gtk.Entry()
		entryFichier = Gtk.Entry()
		entryNbreMesure = Gtk.Entry()
		
		
		spinNbreMvt = Gtk.SpinButton()
		spinNbreVoix = Gtk.SpinButton()
		spinVoixSup = Gtk.SpinButton()
		spinVoixInf = Gtk.SpinButton()
		limiteVoix = Gtk.Adjustment(1, 1, 20, 1, 10, 0) #on limite de 1 à 20 le nombre de voix
		limiteMvt = Gtk.Adjustment(1, 1, 20, 1, 10, 0)  #idem pour le nombre de mvt
		limiteVoixSup = Gtk.Adjustment(1, 1, 20, 1, 10, 0)
		limiteVoixInf = Gtk.Adjustment(1, 1, 20, 1, 10, 0)
		spinNbreMvt.set_adjustment(limiteMvt)
		spinNbreVoix.set_adjustment(limiteVoix)
		spinVoixSup.set_adjustment(limiteVoixSup)
		spinVoixInf.set_adjustment(limiteVoixInf)
		spinNbreVoix.set_value(1)
		spinNbreMvt.set_value(1)
		
		comboTypePartition = Gtk.ComboBoxText()
		comboTypePartition.set_entry_text_column(0)
		comboTypePartition.connect("changed", self.on_typepartition_changed, spinNbreMvt, spinNbreVoix, spinVoixSup, spinVoixInf)
		for i_part in typePartition:
			comboTypePartition.append_text(i_part)
		
		boutonOK = Gtk.Button("OK")
		boutonAnnuler = Gtk.Button("Annuler")
		boutonOK.connect("clicked", self.on_ok_clicked, entryDossier, entryFichier, comboTypePartition, spinNbreMvt, spinNbreVoix, entryNbreMesure, spinVoixSup, spinVoixInf)
		boutonAnnuler.connect("clicked", self.on_annuler_clicked)
		boutonOuvrirRep = Gtk.Button("Ouvrir")
		boutonOuvrirRep.connect("clicked", self.choix_rep, entryDossier)
		
		table = Gtk.Table(8, 7)
		# 1ere colonne
		table.attach(labelDossier, 0, 1, 0, 1)
		table.attach(labelFichier, 0, 1, 1, 2)
		table.attach(labelTypePartition, 0, 1, 2, 3)
		table.attach(labelNbreMvt, 0, 1, 5, 6)
		table.attach(labelNbreVoix, 0, 1, 3, 4)
		table.attach(labelVoixSupInf, 0, 1, 4, 5)
		table.attach(labelNbreMesure, 0, 1, 6, 7)
		table.attach(boutonOK, 0, 1, 7, 8)
		# 2eme colonne
		table.attach(boutonOuvrirRep, 1, 2, 0, 1)
		# 3eme colonne
		table.attach(entryDossier, 2, 4, 0, 1)
		table.attach(entryFichier, 2, 4, 1, 2)
		table.attach(comboTypePartition, 2, 4, 2, 3)
		table.attach(spinNbreVoix, 2, 4, 3, 4)
		table.attach(spinVoixSup, 2, 3, 4, 5)
		table.attach(spinVoixInf, 3, 4, 4, 5)
		table.attach(spinNbreMvt, 2, 4, 5, 6)
		table.attach(entryNbreMesure, 2, 4, 6, 7)
		table.attach(boutonAnnuler, 2, 3, 7, 8)
		
		self.add(table)
		
	#Gestion des dépendances entre les widgets
	def on_typepartition_changed(self, combo, spinNbreMvt, spinNbreVoix, spinVoixSup, spinVoixInf):
		choixTypePartition = combo.get_active_text()
		if choixTypePartition == "Partition Simple":
			spinNbreMvt.set_value(1)
			spinNbreVoix.set_value(1)
			spinNbreMvt.set_sensitive(False)
			spinNbreVoix.set_sensitive(False)
		elif choixTypePartition == "Partition à plusieurs mouvements":
			spinNbreVoix.set_value(1)
			spinNbreVoix.set_sensitive(False)
			spinNbreMvt.set_sensitive(True)
		elif choixTypePartition == "Partition à plusieurs voix":
			spinNbreMvt.set_value(1)
			spinNbreMvt.set_sensitive(False)
			spinNbreVoix.set_sensitive(True) 
		else:
			spinNbreVoix.set_sensitive(True)
			spinNbreMvt.set_sensitive(True)
		if choixTypePartition == "Partition pour piano":
			spinVoixSup.set_sensitive(True)
			spinVoixInf.set_sensitive(True)
		else:
			spinVoixSup.set_sensitive(False)
			spinVoixInf.set_sensitive(False)
	
	def choix_rep(self, widget, entryDossier):
		dialog = Gtk.FileChooserDialog("Please choose a folder", self,
			Gtk.FileChooserAction.SELECT_FOLDER,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			"Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800, 400)
		response = dialog.run()
		
		#repertoireChoisi.set_text(response)
		if response == Gtk.ResponseType.OK:
			entryDossier.set_text(dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")
		dialog.destroy()
	
	def on_ok_clicked(self, boutonOK, Dossier, Fichier, typePartition, nbreMvt, nbreVoix, mesure, nbreVoixSup, nbreVoixInf):
		# chaque entrée de l'utilisateur est déclaré en tant qu'attribut.
		self.path = Dossier.get_text()
		self.fichier = Fichier.get_text()
		self.typePartition = typePartition.get_active_text()
		self.nombreMouvement = int(nbreMvt.get_value())
		self.nombreVoix = int(nbreVoix.get_value())
		self.nombreMesure = mesure.get_text()
		self.nombreVoixSup = int(nbreVoixSup.get_value())
		self.nombreVoixInf = int(nbreVoixInf.get_value())
		Gtk.main_quit()
		
	def on_annuler_clicked(self, boutonAnnuler):
		# print("Annuler")
		Gtk.main_quit()
	
createScore = createScore()
createScore.connect("delete-event", Gtk.main_quit)
createScore.show_all()
Gtk.main()

nomVoix = ['VoixUne','VoixDeux', 'VoixTrois', 'VoixQuatre', 'VoixCinq', 'VoixSix', 'VoixSept', 'VoixHuit', 'VoixNeuf', 'VoixDix', 'VoixOnze', 'VoixDouze', 'VoixTreize', 'VoixQuatorze', 'VoixQuinze', 'VoixSeize', 'VoixDixSept', 'VoixDixHuit', 'VoixDixNeuf', 'VoixVingt']
nomMvt = ['MvtUn', 'MvtDeux', 'MvtTrois', 'MvtQuatre', 'MvtCinq', 'MvtSix', 'MvtSept', 'MvtHuit', 'MvtNeuf', 'MvtDix', 'MvtOnze', 'MvtDouze', 'MvtTreize', 'MvtQuatorze', 'MvtQuinze', 'MvtSeize', 'MvtDixSept', 'MvtDixHuit', 'MvtDixNeuf', 'MvtVingt']
Romain = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX']


def creationEnTete(adresse, fichier):
	"fonction qui créé une entête et la section paper d'un fichier lilypond"
	tabEnTete = []
	ligne = 0
	resEnTete = ""
	obFichier = open( adresse + "/" + fichier, "a")
	dateCourante = datetime.now().strftime('%A %d %B %Y, %H:%M:%S')
	tabEnTete.append("%Fichier : " + adresse + "/" + fichier)
	tabEnTete.append("%Généré le : " + dateCourante)
	tabEnTete.append("%#######################################################################")
	tabEnTete.append("%#             G E N E R A L I T E S   E T   E N T E T E               #")
	tabEnTete.append("%#######################################################################")
	tabEnTete.append("\paper {")
	tabEnTete.append("	ragged-last-bottom = ##t")
	tabEnTete.append("	ragged-bottom = ##t")
	tabEnTete.append("	bookTitleMarkup = \\markup {")
	tabEnTete.append("		\\override #'(baseline-skip . 3.5)")
	tabEnTete.append("		\\column {")
	tabEnTete.append("			\\fill-line { \\fromproperty #'header:dedication }")
	tabEnTete.append("			\\override #'(baseline-skip . 3.5)")
	tabEnTete.append("			\\column {")
	tabEnTete.append("				\\fill-line {")
	tabEnTete.append("					\\huge \\larger \\larger \\bold")
	tabEnTete.append("					\\fromproperty #'header:title")
	tabEnTete.append("				}")
	tabEnTete.append("				\\fill-line {")
	tabEnTete.append("					\\large %\\bold")
	tabEnTete.append("					\\fromproperty #'header:subtitle")
	tabEnTete.append("				}")
	tabEnTete.append("				\\fill-line {")
	tabEnTete.append("					\\smaller %\\bold")
	tabEnTete.append("					\\fromproperty #'header:subsubtitle")
	tabEnTete.append("				}")
	tabEnTete.append("				\\fill-line {")
	tabEnTete.append("					\\fromproperty #'header:poet")
	tabEnTete.append("					{ \\large \\bold \\fromproperty #'header:instrument }")
	tabEnTete.append("					\\fromproperty #'header:composer")
	tabEnTete.append("				}")
	tabEnTete.append("				\\fill-line {")
	tabEnTete.append("					\\fromproperty #'header:meter")
	tabEnTete.append("					\\fromproperty #'header:arranger")
	tabEnTete.append("				}")
	tabEnTete.append("			}")
	tabEnTete.append("		}")
	tabEnTete.append("	}")
	tabEnTete.append("}")
	tabEnTete.append("%-----------------------------------------------------------------------")
	tabEnTete.append("\\include \"/media/Documents/Partitions/lilypond/markup.ly\"")
	tabEnTete.append("%-----------------------------------------------------------------------")
	while ligne < len(tabEnTete):
		resEnTete = resEnTete + tabEnTete[ligne] + "\n"
		ligne = ligne + 1
	obFichier.write(resEnTete)
	obFichier.close()

def creationMusique(adresse, fichier, nomPart, mouvement, voix, nombreMesure, siWarning):
	tabMusique = []
	ligne = 0
	resMusique = ""
	obFichier = open(adresse + "/" + fichier, "a")
	dateCourante = datetime.now().strftime('%A %d %B %Y, %H:%M:%S')
	tabMusique.append("%Fichier : " + adresse + "/" + fichier)
	tabMusique.append("%Généré le : " + dateCourante)
	if siWarning == 1:
		tabMusique.append("%-----------------------------------------------------------------------")
		tabMusique.append("%         /!\ /!\ /!\   Fichier non compilable   /!\ /!\ /!\           -")
		tabMusique.append("%-----------------------------------------------------------------------")
	tabMusique.append("%#######################################################################")
	if mouvement != 0:
		if voix != 0:
			tabMusique.append("%#               M O U V E M E N T   " + str(mouvement) + "   -   V O I X   " + str(voix) + "               #")
		else:
			tabMusique.append("%#                     M O U V E M E N T     N° " + str(mouvement) + "                      #")
	else:
		tabMusique.append("%#                        V O I X     N° " + str(voix) +"                             #")
	tabMusique.append("%#######################################################################")
	tabMusique.append(nomPart + " = \\relative c {")
	tabMusique.append("	\\clef treble")
	tabMusique.append("	\\override TupletBracket #'bracket-visibility = ##f")
	i_mesure = 1
	while i_mesure < int(nombreMesure)-5:
		tabMusique.append("% mesures " + str(i_mesure) + " à " + str(i_mesure + 4))
		tabMusique.append("	")
		i_mesure = i_mesure + 5
	tabMusique.append("% mesures " + str(i_mesure) + " à " + str(nombreMesure))
	tabMusique.append("	")
	tabMusique.append("}")
	while ligne < len(tabMusique):
		resMusique = resMusique + tabMusique[ligne] + "\n"
		ligne = ligne + 1
	obFichier.write(resMusique)
	obFichier.close()

def creationZoneGlobale(adresse, fichier, nomZone):
	tabZoneGlobale = []
	ligne = 0
	resZoneGlobale = ""
	versionLilypond=commands.getoutput('lilypond -v | head -1 | cut -d" " -f3')
	tabZoneGlobale.append(nomZone + " = {")
	tabZoneGlobale.append("	\\version \"" + versionLilypond + "\"")
	tabZoneGlobale.append("	\\time 4/4")
	tabZoneGlobale.append("	\\key c \\major")
	tabZoneGlobale.append("	\\set Score.markFormatter = #format-mark-box-numbers")
	tabZoneGlobale.append("	\\compressFullBarRests")
	tabZoneGlobale.append("	\\tempo \"Indication Tempo\" 4 = ")
	tabZoneGlobale.append("	#(set-global-staff-size 19)")
	tabZoneGlobale.append("}")
	tabZoneGlobale.append("%-----------------------------------------------------------------------")
	while ligne < len(tabZoneGlobale):
		resZoneGlobale = resZoneGlobale + tabZoneGlobale[ligne] + "\n"
		ligne = ligne + 1
	obFichier = open(adresse + "/" + fichier, "a")
	obFichier.write(resZoneGlobale)
	obFichier.close()
	

def creationTitre(adresse, fichier):
	tabTitre = []
	ligne = 0
	resTitre = ""
	obFichier = open(adresse + "/" + fichier, "a")
	tabTitre.append("%#######################################################################")
	tabTitre.append("%#       C O N S T R U C T I O N   D E   L A   P A R T I T I O N       #")
	tabTitre.append("%#######################################################################")
	tabTitre.append("\\book {")
	tabTitre.append("	\\header {")
	tabTitre.append("		title = \\markup { \\fontsize #5 \\sans ")
	tabTitre.append("			\\center-column {")
	tabTitre.append("				\\vspace #10")
	tabTitre.append("				\"Compositeur\"")
	tabTitre.append("				\"Annee Naissance - deces\"")
	tabTitre.append("			}")
	tabTitre.append("		}")
	tabTitre.append("		subtitle = \\markup { ")
	tabTitre.append("			\\fontsize #5 \sans")
	tabTitre.append("			\\center-column {")
	tabTitre.append("				\\vspace #10")
	tabTitre.append("				\"Oeuvre\"")
	tabTitre.append("				\"Opus - reference\"")
	tabTitre.append("			}")
	tabTitre.append("		}")
	tabTitre.append("		subsubtitle = \\markup { \\fontsize #3 \\sans")
	tabTitre.append("			\\center-column {")
	tabTitre.append("				\\vspace #10")
	tabTitre.append("				\"Titre - Partie\"")
	tabTitre.append("			}")
	tabTitre.append("		}")
	tabTitre.append("	}")
	while ligne < len(tabTitre):
		resTitre = resTitre + tabTitre[ligne] + "\n"
		ligne = ligne + 1
	obFichier.write(resTitre)
	obFichier.close()

def creationPartitionType1(adresse, fichier):
	tabPartitionType1 = []
	ligne = 0
	resPartitionType1 = ""
	tabPartitionType1.append("	\\score {")
	tabPartitionType1.append("		\\new Staff << \global \VoixUne >>")
	tabPartitionType1.append("		\\header {")
	tabPartitionType1.append("			breakbefore = ##t")
	tabPartitionType1.append("		}")
	tabPartitionType1.append("		\\layout {")
	tabPartitionType1.append("			%system-count = #20")
	tabPartitionType1.append("		}")
	tabPartitionType1.append("	}")
	tabPartitionType1.append("}")
	while ligne < len(tabPartitionType1):
		resPartitionType1 = resPartitionType1 + tabPartitionType1[ligne] + "\n"
		ligne = ligne + 1
	obFichier = open(adresse + "/" + fichier, "a")
	obFichier.write(resPartitionType1)
	obFichier.close()

def creationPartitionType2(adresse, fichier, nombreMouvement):
	tabPartitionType2 = []
	ligne = 0
	resPartitionType2 = ""
	i_mvt = 0
	while i_mvt < nombreMouvement:
		tabPartitionType2.append("	\\score {")
		tabPartitionType2.append("		{")
		tabPartitionType2.append("			\\new Staff << \\global" + str(nomMvt[i_mvt]) + " \\" + str(nomMvt[i_mvt]) + " >>")
		tabPartitionType2.append("		}")
		tabPartitionType2.append("		\\header {")
		tabPartitionType2.append("			breakbefore = ##t")
		tabPartitionType2.append("			piece = \\markup {")
		tabPartitionType2.append("				\\fill-line {")
		tabPartitionType2.append("					\\fontsize #5")
		tabPartitionType2.append("					" + Romain[i_mvt])
		tabPartitionType2.append("				}")
		tabPartitionType2.append("			}")
		tabPartitionType2.append("		}")
		tabPartitionType2.append("		\\layout {")
		tabPartitionType2.append("			%system-count = #20")
		tabPartitionType2.append("		}")
		tabPartitionType2.append("	}")
		if i_mvt == nombreMouvement - 1:
			tabPartitionType2.append("}")
		i_mvt = i_mvt + 1
	while ligne < len(tabPartitionType2):
		resPartitionType2 = resPartitionType2 + tabPartitionType2[ligne] + "\n"
		ligne = ligne + 1
	obFichier = open(adresse + "/" + fichier, "a")
	obFichier.write(resPartitionType2)
	obFichier.close()

def creationPartitionType3(adresse, fichier, nomZoneGlobale, nombreVoix):
	tabPartitionType3 = []
	ligne = 0
	resPartitionType3 = ""
	i_voix = 0
	tabPartitionType3.append("	\\score {")
	tabPartitionType3.append("		\\new StaffGroup <<")
	while i_voix < nombreVoix:
		tabPartitionType3.append("			\\new Staff << \\" + str(nomZoneGlobale) + " \\" + str(nomVoix[i_voix]) + " >>")
		i_voix = i_voix + 1
	tabPartitionType3.append("		>>")
	tabPartitionType3.append("		\\header {")
	tabPartitionType3.append("			breakbefore = ##t")
	tabPartitionType3.append("		}")
	tabPartitionType3.append("		\\layout {")
	tabPartitionType3.append("			%system-count = #20")
	tabPartitionType3.append("		}")
	tabPartitionType3.append("	}")
	tabPartitionType3.append("}")
	while ligne < len(tabPartitionType3):
		resPartitionType3 = resPartitionType3 + tabPartitionType3[ligne] + "\n"
		ligne = ligne + 1
	obFichier = open(adresse + "/" + fichier, "a")
	obFichier.write(resPartitionType3)
	obFichier.close()

def creationPartitionType4(adresse, fichier, nombreVoixSup, nombreVoixInf, nbreMvt):
	tabPartitionType4 = []
	ligne = 0
	resPartitionType4 = ""
	
	i_mvt = 0
	while i_mvt < nbreMvt:
		debut = "\\global" + str(nomMvt[i_mvt]) + " << { "
		intermediaire = " } \\\\ { "
		fin = " } >>"
		nbreVoixTraite = 0
		
		tabPartitionType4.append("	\\score {")
		tabPartitionType4.append("		\\new PianoStaff <<")
	
		#gestion de la voix supérieure
		tabPartitionType4.append("			\\new Staff = \"up\" {")
		if nombreVoixSup == 1:
			VoixSup = "\\global" + str(nomMvt[i_mvt]) + " \\" + str(nomMvt[i_mvt]) + str(nomVoix[0])
			nbreVoixTraite = nbreVoixTraite + 1
		else:
			VoixSup = debut
			i_voix = 0
			while i_voix < int(nombreVoixSup) - 2:
				VoixSup = VoixSup + " \\" + str(nomMvt[i_mvt]) + str(nomVoix[i_voix]) + intermediaire 
				nbreVoixTraite = nbreVoixTraite + 1
				i_voix = i_voix + 1
			VoixSup = VoixSup + " \\" + str(nomMvt[i_mvt]) + str(nomVoix[nbreVoixTraite]) + fin
			nbreVoixTraite = nbreVoixTraite + 1
		tabPartitionType4.append("				" + VoixSup)
		tabPartitionType4.append("			}")
	
		#gestion de la voix inférieure
		tabPartitionType4.append("			\\new Staff = \"down\" {")
		if nombreVoixInf == 1:
			VoixInf="\\global" + str(nomMvt[i_mvt]) + " \\" + str(nomMvt[i_mvt]) + str(nomVoix[nbreVoixTraite])
			nbreVoixTraite = nbreVoixTraite + 1
		else:
			VoixInf = debut
			i_voix = 0
			while i_voix < int(nombreVoixInf) - 2:
				VoixInf = VoixInf + " \\" + str(nomMvt[i_mvt]) + str(nomVoix[nbreVoixTraite]) + intermediaire
				nbreVoixTraite = nbreVoixTraite + 1
				i_voix = i_voix + 1
			VoixInf = VoixInf + " \\" + str(nomMvt[i_mvt]) + str(nomVoix[nbreVoixTraite]) + fin
		tabPartitionType4.append("				" + VoixInf)
		tabPartitionType4.append("			}")
		if i_mvt == 0:
			tabPartitionType4.append("		>>")
			tabPartitionType4.append("		\\header {")
			tabPartitionType4.append("			breakbefore = ##t")
			tabPartitionType4.append("		}")
			tabPartitionType4.append("		\\layout {")
			tabPartitionType4.append("			%system-count = #20")
			tabPartitionType4.append("		}")
			tabPartitionType4.append("	}")
		else:
			tabPartitionType4.append("		>>")
			tabPartitionType4.append("		\\layout {")
			tabPartitionType4.append("			%system-count = #20")
			tabPartitionType4.append("		}")
			tabPartitionType4.append("	}")
		i_mvt = i_mvt + 1
	tabPartitionType4.append("}")
	while ligne < len(tabPartitionType4):
		resPartitionType4 = resPartitionType4 + tabPartitionType4[ligne] + "\n"
		ligne = ligne + 1
	obFichier = open(adresse + "/" + fichier, "a")
	obFichier.write(resPartitionType4)
	obFichier.close()

def creationConducteur(adresse, fichier, i_mvt, nbreMvt, nbreVoix):
	tabConducteur = []
	ligne = 0
	resConducteur = ""
	if i_mvt < 9:
		indexMvt = "0" + str(i_mvt + 1)
	else:
		indexMvt = str(i_mvt + 1)
	fileName = "00_" + fichier + "_Conducteur_Mvt" + str(i_mvt + 1) + ".ly"
	creationEnTete(adresse, fileName)
	creationZoneGlobale(adresse, fileName, "global")
	i_part = 0
	obFichier = open(adresse + "/" + fileName, "a")
	while i_part < nbreVoix:
		fileNamePart = indexMvt + "_" + fichier + "_Mvt" + str(i_mvt + 1) + "_Voix" + str(i_part + 1) + ".ly"
		obFichier.write("\\include \"" + fileNamePart + "\"\n")
		i_part = i_part + 1
	obFichier.write("%-----------------------------------------------------------------------\n")
	obFichier.close()
	creationTitre(adresse, fileName)
	tabConducteur.append("	\\score {")
	tabConducteur.append("		\\new StaffGroup <<")
	i_part = 0
	while i_part < nbreVoix:
		tabConducteur.append("			\\new Staff << \\global \\" + nomMvt[i_mvt] + nomVoix[i_part] + " >>")
		i_part = i_part + 1
	
	tabConducteur.append("		>>")
	tabConducteur.append("		\\header {")
	tabConducteur.append("			breakbefore = ##t")
	tabConducteur.append("		}")
	tabConducteur.append("		\\layout {")
	tabConducteur.append("			%system-count = #20")
	tabConducteur.append("		}")
	tabConducteur.append("	}")
	tabConducteur.append("}")
	while ligne < len(tabConducteur):
		resConducteur = resConducteur + tabConducteur[ligne] + "\n"
		ligne = ligne + 1
	obFichier = open(adresse + "/" + fileName, "a")
	obFichier.write(resConducteur)
	obFichier.close()

def creationVoix(adresse, fichier, nbreMvt, i_voix, nbreVoix):
	ligne = 0
	tabVoix = []
	resVoix = ""
	if i_voix < 9:
		indexVoix = "0" + str(i_voix + 1)
	else:
		indexVoix = str(i_voix + 1)
	fileName = "00_" + fichier + "_Voix" + str(i_voix + 1) + ".ly"
	creationEnTete(adresse, fileName)
	i_mouv = 0
	while i_mouv < nbreMvt:
		creationZoneGlobale(adresse, fileName, "global" + nomMvt[i_mouv])
		i_mouv = i_mouv + 1
	obFichier = open(adresse + "/" + fileName, "a")
	i_mouv = 0
	while i_mouv < nbreMvt:
		if i_mouv < 9:
			indexMvt = "0" + str(i_mouv + 1)
		else:
			indexMvt = str(i_mouv + 1)
		fileNamePart = 	indexMvt + "_" + fichier + "_Mvt" + str(i_mouv + 1) + "_Voix" + str(i_voix + 1) + ".ly"
		obFichier.write("\\include \"" + fileNamePart + "\"\n")
		i_mouv = i_mouv + 1
	obFichier.write("%-----------------------------------------------------------------------\n")
	obFichier.close()
	creationTitre(adresse, fileName)
	i_mouv = 0
	while i_mouv < nbreMvt:
		tabVoix.append("	\\score {")
		tabVoix.append("		{")
		tabVoix.append("			\\new Staff << \\global" + nomMvt[i_mouv] + " \\" + nomMvt[i_mouv] + nomVoix[i_voix] + " >>")
		tabVoix.append("		}")
		tabVoix.append("		\\header {")
		tabVoix.append("			breakbefore = ##t")
		tabVoix.append("			piece = \\markup {")
		tabVoix.append("				\\fill-line {")
		tabVoix.append("					\\fontsize #5")
		tabVoix.append("					" + Romain[i_mouv])
		tabVoix.append("				}")
		tabVoix.append("			}")
		tabVoix.append("		}")
		tabVoix.append("	}")
		i_mouv = i_mouv + 1
	tabVoix.append("}")
	ligne = 0
	while ligne < len(tabVoix):
		resVoix = resVoix + tabVoix[ligne] + "\n"
		ligne = ligne + 1
	obFichier = open(adresse + "/" + fileName, "a")
	obFichier.write(resVoix)
	obFichier.close()


if createScore.typePartition == "Partition Simple":
	creationEnTete(createScore.path, createScore.fichier)
	creationZoneGlobale(createScore.path, createScore.fichier, "global")
	creationMusique(createScore.path, createScore.fichier, "VoixUne", createScore.nombreMouvement - 1, createScore.nombreVoix, createScore.nombreMesure, 0)
	creationTitre(createScore.path, createScore.fichier)
	creationPartitionType1(createScore.path, createScore.fichier)
elif createScore.typePartition == "Partition à plusieurs mouvements":
	nombreMesureParMouvement = createScore.nombreMesure.split()
	creationEnTete(createScore.path, createScore.fichier)
	i_mvt = 0
	while i_mvt < createScore.nombreMouvement:
		creationZoneGlobale(createScore.path, createScore.fichier, "global" + nomMvt[i_mvt])
		i_mvt = i_mvt + 1
	i_mvt = 0
	while i_mvt < createScore.nombreMouvement:
		creationMusique(createScore.path, createScore.fichier, nomMvt[i_mvt], i_mvt + 1, 0, nombreMesureParMouvement[i_mvt], 0)
		i_mvt = i_mvt + 1
	creationTitre(createScore.path, createScore.fichier)
	creationPartitionType2(createScore.path, createScore.fichier, createScore.nombreMouvement)
elif createScore.typePartition == "Partition à plusieurs voix":
	creationEnTete(createScore.path, createScore.fichier)
	creationZoneGlobale(createScore.path, createScore.fichier, "global")
	i_voix = 0
	while i_voix < createScore.nombreVoix:
		creationMusique(createScore.path, createScore.fichier, nomVoix[i_voix], 0, i_voix + 1, createScore.nombreMesure, 0)
		i_voix = i_voix + 1
	creationTitre(createScore.path, createScore.fichier)
	creationPartitionType3(createScore.path, createScore.fichier, "global", createScore.nombreVoix)
elif createScore.typePartition == "Partition pour piano":
	nombreMesureParMouvement = createScore.nombreMesure.split()
	creationEnTete(createScore.path, createScore.fichier)
	i_mvt = 0
	while i_mvt < createScore.nombreMouvement:
		creationZoneGlobale(createScore.path, createScore.fichier, "global" + nomMvt[i_mvt])
		i_mvt = i_mvt + 1
	i_mvt = 0
	while i_mvt < createScore.nombreMouvement:
		i_voix = 0
		while i_voix < createScore.nombreVoix:
			creationMusique(createScore.path, createScore.fichier, nomMvt[i_mvt] + nomVoix[i_voix], i_mvt + 1, i_voix + 1, nombreMesureParMouvement[i_mvt], 0)
			i_voix = i_voix + 1
		i_mvt = i_mvt + 1
	creationTitre(createScore.path, createScore.fichier)
	creationPartitionType4(createScore.path, createScore.fichier, createScore.nombreVoixSup + 1, createScore.nombreVoixInf + 1, createScore.nombreMouvement)
elif createScore.typePartition == "Partition pour ensemble":
	nombreMesureParMouvement = createScore.nombreMesure.split()
	# création des voix séparées (fichiers non compilables)
	i_mvt = 0
	while i_mvt < createScore.nombreMouvement:
		i_voix = 0
		while i_voix < createScore.nombreVoix:
			if i_mvt < 9:
				indexMvt = "0" + str(i_mvt + 1)
			else:
				indexMvt = str(i_mvt + 1)
			fileName = indexMvt + "_" + createScore.fichier + "_Mvt" + str(i_mvt + 1) + "_Voix" + str(i_voix + 1) + ".ly"
			creationMusique(createScore.path, fileName, nomMvt[i_mvt] + nomVoix[i_voix], i_mvt + 1, i_voix + 1, nombreMesureParMouvement[i_mvt], 1)
			i_voix = i_voix + 1
		i_mvt = i_mvt + 1
	
	# création des fichiers conducteurs :
	i_mvt = 0
	while i_mvt < createScore.nombreMouvement:
		creationConducteur(createScore.path, createScore.fichier, i_mvt, createScore.nombreMouvement, createScore.nombreVoix)
		i_mvt = i_mvt + 1
	# creation des fichiers par voix : 
	i_voix = 0 
	while i_voix < createScore.nombreVoix:
		creationVoix(createScore.path, createScore.fichier, createScore.nombreMouvement, i_voix, createScore.nombreVoix)
		i_voix = i_voix + 1
