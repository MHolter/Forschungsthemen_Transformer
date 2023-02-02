<h2>Repository für die Studienarbeit "Machine Learning Model zur Statusprognose am Beispiel einer Smart Factory"</h2>
<br>
Autor/Entwickler: Moritz Holter

<hr>
Datenquelle: https://figshare.com/articles/dataset/Dataset_An_IoT-Enriched_Event_Log_for_Process_Mining_in_Smart_Factories/20130794<br>
Code-Source: https://github.com/nklingen/Transformer-Time-Series-Forecasting<br>
Article: https://medium.com/mlearning-ai/transformer-implementation-for-time-series-forecasting-a9db2db5c820<br>
<hr>
Die ursprünglichen Datensätze wurden zur Beschränkung der Größe aus dem Repository entfernt.<br>
Es ist dennoch möglich alles zu testen, da die konsolidierten Testdatensätze im Directory "data_converter/data/csv" abgelegt sind.
<hr>
<h2> Durchführung einer Simulation </h2>
Für die Durchführung einer Simulation müssen drei Schritte unternommen werden:<br>
1. Auswahl der Daten:<br>
 - Öffnen der Datei "data_converter.py"<br>
 - Einstellen der Parameter: selected_task, amount_training, amount_test <br>
    Wichtig: Die ausgewählte Aufgabe muss über ausreichend Datensätze verfügen! <br>
 - Ausführen der Funktion "CreateTestAndTrainingsData"<br>
 (Wollen Sie selbst Daten konvertieren folgen Sie dem Prozess innerhalb der Datei)<br>
<br>
2. Vorbereitung der Daten: <br>
 - Öffnen der Datei: "transformer/data_processor.py"<br>
 - Ausführen der Funktion "SelectData"<br>
<br>
3. Start des Transformers: <br>
 - Öffnen der Datei: "transformer/transformer_main.py"<br>
 - Ausführen der Main-Funktion
 - In diesem Zuge können auch die Parameter angepasst werden
