# Generated by Django 3.1.2 on 2020-10-07 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(None, 'Bitte Wert auswählen'), ('C10', 'Herstellung von Nahrungs- und Futtermitteln (C.10)'), ('C11', 'Getränkeherstellung (C.11)'), ('C12', 'Tabakverarbeitung (C.12)'), ('C13', 'Herstellung von Textilien (C.13)'), ('C14', 'Herstellung von Bekleidung (C.14)'), ('C15', 'Herstellung von Leder, Lederwaren und Schuhen (C.15)'), ('C16', 'Herstellung von Holz-, Flecht-, Korb- und Korkwaren (ohne Möbel) (C.16)'), ('C17', 'Herstellung von Papier, Pappe und Waren daraus (C.17)'), ('C18', 'Herstellung von Druckerzeugnissen; Vervielfältigung von bespielten Ton-, Bild und Datenträgern (C.18)'), ('C19', 'Kokerei und Mineralölverarbeitung (C.19)'), ('C20', 'Herstellung von chemischen Erzeugnissen (C.20)'), ('C21', 'Herstellung von pharmazeutischen Erzeugnissen (C.21)'), ('C22', 'Herstellung von Gummi- und Kunststoffwaren (C.22)'), ('C23', 'Herstellung von Glas und Glaswaren, Keramik, Verarbeitung von Steinen und Erden (C.23)'), ('C24', 'Metallerzeugung und –bearbeitung (C.24)'), ('C25', 'Herstellung von Metallerzeugnissen (C.25)'), ('C26', 'Herstellung von Datenverarbeitungsgeräten, elektronischen und optischen Erzeugnissen (C.26)'), ('C27', 'Herstellung von elektrischen Ausrüstungen (C.27)'), ('C28', 'Maschinenbau (C.28)'), ('C29', 'Herstellung von Kraftwagen und Kraftwagenteilen (C.29)'), ('C30', 'Sonstiger Fahrzeugbau (C.30)'), ('C31', 'Herstellung von Möbeln (C.31)'), ('C32', 'Herstellung von sonstigen Waren (C.32)')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Bezeichnung der Komponente', max_length=200, verbose_name='Name')),
                ('trl', models.IntegerField(choices=[(None, 'Bitte Wert auswählen'), (1, 'TRL 1 - Grundprinzipien beobachtet'), (2, 'TRL 2 - Technologiekonzept formuliert'), (3, 'TRL 3 - Experimenteller Nachweis des Konzepts'), (4, 'TRL 4 - Technologie im Labor überprüft'), (5, 'TRL 5 - Technologie in relevanter Umgebung überprüft'), (6, 'TRL 6 - Technologie in relevanter Umgebung getestet'), (7, 'TRL 7 - Test eines System-Prototyps im realen Einsatz'), (8, 'TRL 8 - System ist komplett und qualifiziert'), (9, 'TRL 9 - System funktioniert in operationeller Umgebung')], help_text='Status der Komponente in Bezug auf Ihre Einsetzbarkeit durch die Angabe eines Technischen Reifegrades (Technology Readiness Level).', verbose_name='TRL')),
                ('description', models.TextField(help_text='Kurze Beschreibung der Komponente', verbose_name='Kurzbeschreibung')),
            ],
        ),
        migrations.CreateModel(
            name='DataAnalysisProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(None, 'Bitte Wert auswählen'), ('DA', 'Datenerfassung'), ('DC', 'Data-Cleaning/Pre-processing'), ('DI', 'Datenintegration'), ('MS', 'Modellauswahl'), ('MT', 'Modellbildung & Training'), ('MA', 'Modellanalyse/erklärung'), ('MU', 'Modellanwendung'), ('VI', 'Visualisierung'), ('PC', 'KI-basierte Prozesssteuerung')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Use',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kpi', models.CharField(help_text='Key Performance Indikator, der durch die Komponente optimiert werden soll;es sollte auf jeden Fall eine Kategorie ausgesucht werden (Wert); dies Auswahl kann über KPI-Verfeinerung noch verfeinert werden;', max_length=1000, verbose_name='KPI')),
                ('scenarios', models.TextField(help_text='Beschreibung von Szenarien, in denen die Komponente bereits erfolgreich eingesetzt wurde', verbose_name='Szenarien / Use cases')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalogue.component')),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ai_method', models.CharField(help_text='Angabe der verwendeten KI-Methode (z.B. Deep Learning)', max_length=1000, verbose_name='KI-Methode')),
                ('realtime_processing', models.IntegerField(choices=[(None, 'Bitte Wert auswählen'), (0, 'Keine Echtzeit'), (1, 'Weiche Echtzeit'), (2, 'Harte Echtzeit'), (3, 'Feste Echtzeit')], help_text='Klassifizierung der Komponente in Bezug auf ihre Echtzeitfähigkeit', verbose_name='Echtzeitverarbeitung')),
                ('data_formats', models.CharField(help_text='Datenformate, die von der KI-Komponente verarbeitet werden können und Datenformat der Ergebnisse', max_length=1000, verbose_name='Datenformate')),
                ('licenses', models.CharField(help_text='Welche Lizenzen bringt die Komponente mit, insbesondere Open Source Lizenzen', max_length=1000, verbose_name='Lizenzen')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalogue.component')),
                ('data_analysis_process', models.ManyToManyField(help_text='Unterstützte Phasen des Datenanalyse-Prozesses (z.B. Data Cleaning)', to='catalogue.DataAnalysisProcess', verbose_name='Datenanalyse-Prozess')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(None, 'Bitte Wert auswählen'), ('PMCM', 'Predictive Maintenance/Condition Monitoring'), ('QCM', 'Qualitätskontrolle und –management'), ('OPP', 'Optimierte Prozessplanung'), ('OPC', 'Optimierte Prozesssteuerung'), ('RAS', 'Robotik & autonome Systeme'), ('IST', 'Intelligente Sensorik'), ('KM', 'Wissensmanagement'), ('FPA', 'Vorhersagen und Predictive Analytics'), ('ORS', 'Optimiertes Ressourcenmanagement'), ('IA', 'Intelligente Automatisierung'), ('IAS', 'Intelligente Assistenzsysteme'), ('DA', 'Datenanalyse'), ('DM', 'Data Management'), ('VAR', 'Virtuelle und erweiterte Realität'), ('OTHER', 'Sonstiges?')], max_length=5, unique=True)),
                ('component', models.ForeignKey(help_text='Art der Aufgabe, der die beschriebene KI-Komponente zugeordnet werden kann (z.B. Predictive Maintenance, Qualitätsprüfung)', on_delete=django.db.models.deletion.CASCADE, to='catalogue.component', verbose_name='Task')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.CharField(help_text='Entwickler und/oder Hersteller der Komponente', max_length=1000, verbose_name='Hersteller')),
                ('contact', models.TextField(help_text='Möglichkeit zum Hersteller Kontakt aufzunehmen', verbose_name='Kontakt')),
                ('additional_info', models.TextField(help_text='Zusatzinformation zur Komponente', verbose_name='Zusatzinformationen')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalogue.component')),
            ],
        ),
        migrations.CreateModel(
            name='Requirements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocols', models.CharField(help_text='Schnittstellen und/oder Protokolle, die von der Kompomente unterstützt werden', max_length=1000, verbose_name='Protokolle/Schnittstellen')),
                ('it_environment', models.CharField(help_text='Anforderungen an die IT-Umgebung (inkl. IT Hardware) und an weitere Software/Bibliotheken, die für den Betrieb der Komponente notwendig sind', max_length=1000, verbose_name='IT Umgebung/Software')),
                ('hardware_requirements', models.CharField(help_text='Spezielle Hardware, welche für den Betrieb der Komponente notwendig ist (z.B. Kamera, Roboter)', max_length=1000, verbose_name='Spezielle Hardware')),
                ('devices', models.CharField(help_text='Maschinen und IoT Devices, mit denen die Komponente kompatibel ist', max_length=1000, verbose_name='Maschinen/Steuerungen')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalogue.component')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporate_division', models.CharField(choices=[(None, 'Bitte Wert auswählen'), ('CS', 'Kundendienst / Inbetriebnahme'), ('DD', 'Konstruktion / Entwicklung'), ('PA', 'Produktion / Montage'), ('MA', 'Instandhaltung'), ('LO', 'Logistik / Supply Chain Management'), ('MC', 'Marketing / Kommunikation'), ('MM', 'Materialwirtschaft / Einkauf'), ('AC', 'Rechnungswesen / Controlling'), ('CG', 'Management / Unternehmensführung'), ('SP', 'Sales / Preisgestaltung')], help_text='Bereich des produzierenden Unternehmens, für den die Komponenten entwickelt wurde', max_length=2, verbose_name='Unternehmensbereich')),
                ('hierarchy_level', models.CharField(choices=[(None, 'Bitte Wert auswählen'), ('IP', 'Intelligentes Produkt (product)'), ('FD', 'Feldebene/Sensoren/Aktoren (field device)'), ('CD', 'Regelung & Steuerung (control device)'), ('ST', 'Station/Maschine oder Maschinengruppe (station)'), ('WC', 'Technische Anlage (work center)'), ('EP', 'Unternehmen (enterprise)'), ('CW', 'Vernetze Welt (Connected World)')], help_text='Automatisierebene, für die die KI-Komponente gedacht ist', max_length=2, verbose_name='Hierarchie-Ebene')),
                ('process', models.CharField(choices=[(None, 'Bitte Wert auswählen'), ('PD', 'Produktionsentwicklung'), ('PA', 'Fertigungs- und Montagevorbereitung'), ('PP', 'Produktionsplanung und –steuerung'), ('PM', 'Teilefertigung'), ('PMPP', 'Teilefertigung - Produktionsprozess (Prozesskette)'), ('PMSP', 'Teilefertigung - Einzelfertigungsprozess'), ('AS', 'Montage, (VDI 2860)'), ('QA', 'Qualitätssicherung'), ('MFL', 'Materialfluss, Logistik'), ('CP', 'Änderungsprozesse'), ('PRODM', 'Produktionsinstandhaltung')], help_text='Prozess der durch die KI-Komponente unterstützt wird', max_length=5, verbose_name='Prozess')),
                ('product', models.TextField(help_text='Hergestelltes Produkt', verbose_name='Produkt')),
                ('branch_applicable', models.ManyToManyField(help_text='Branche, in denen die Komponenten anwendbar ist', related_name='branch_applicable_for', to='catalogue.Branch', verbose_name='Branche (anwendbar)')),
                ('branch_proven', models.ManyToManyField(help_text='Branche(n) für die die Komponente bereits erfolgreich erprobt wurde; belegte Anwendung', related_name='branch_proven_for', to='catalogue.Branch', verbose_name='Branche (erprobt)')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalogue.component')),
            ],
        ),
    ]
