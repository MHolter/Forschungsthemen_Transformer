import logging
import os
import random
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path


def convertToXml():
    # Erste Stufe: Identifizierung der richtigen Dateien und Konvertierung von xes in xml
    root = os.getcwd() + '/data'
    for xes in Path(root).rglob('*.xes'):
        with open(xes, "r") as file:
            content = file.read()
            filename = str(os.path.basename(xes)).split(".")[0]

            if "http://iot.uni-trier.de/StreamDataAnnotationOnto#VGR_2_Crane_Jib_Property_Current_Position_X" in content:
                with open("./Data/Converted_Data/" + str(filename) + ".xml", "w") as output:
                    output.write(content)
                    output.close()


def extractFromXML():
    # Zweite Stufe: Extrahierung der Daten aus der xml und Konvertierung in ein csv-file
    root = os.getcwd() + '/Data/Converted_Data'
    for xml in Path(root).rglob('*.xml'):
        with open(xml, 'r') as f:
            data = f.read()
            filename = str(os.path.basename(xml)).split(".")[0]
            Base_Data = BeautifulSoup(data, "xml")

            Data_Y_Current = Base_Data.find_all('list', {
                'stream:observation': "http://iot.uni-trier.de/StreamDataAnnotationOnto#VGR_2_Crane_Jib_Property_Current_Position_Y"})
            Data_X_Current = Base_Data.find_all('list', {
                'stream:observation': "http://iot.uni-trier.de/StreamDataAnnotationOnto#VGR_2_Crane_Jib_Property_Current_Position_X"})
            Data_Z_Current = Base_Data.find_all('list', {
                'stream:observation': "http://iot.uni-trier.de/StreamDataAnnotationOnto#VGR_2_Crane_Jib_Property_Current_Position_Z"})

            Data_Y_Target = Base_Data.find_all('list', {
                'stream:observation': "http://iot.uni-trier.de/StreamDataAnnotationOnto#VGR_2_Crane_Jib_Property_Target_Position_Y"})
            Data_X_Target = Base_Data.find_all('list', {
                'stream:observation': "http://iot.uni-trier.de/StreamDataAnnotationOnto#VGR_2_Crane_Jib_Property_Target_Position_X"})
            Data_Z_Target = Base_Data.find_all('list', {
                'stream:observation': "http://iot.uni-trier.de/StreamDataAnnotationOnto#VGR_2_Crane_Jib_Property_Target_Position_Z"})

            date_y_current = []
            value_y_current = []
            for Set in Data_Y_Current:
                date = Set.find('date')
                test_date = date.get('stream:timestamp')
                date_y_current.append(test_date)
                sensor = Set.find('string')
                sensor_value = sensor.get('stream:value')
                value_y_current.append(sensor_value)

            date_x_current = []
            value_x_current = []
            for Set in Data_X_Current:
                date = Set.find('date')
                test_date = date.get('stream:timestamp')
                date_x_current.append(test_date)
                sensor = Set.find('string')
                sensor_value = sensor.get('stream:value')
                value_x_current.append(sensor_value)

            date_z_current = []
            value_z_current = []
            for Set in Data_Z_Current:
                date = Set.find('date')
                test_date = date.get('stream:timestamp')
                date_z_current.append(test_date)
                sensor = Set.find('string')
                sensor_value = sensor.get('stream:value')
                value_z_current.append(sensor_value)

            date_x_target = []
            value_x_target = []
            for Set in Data_X_Target:
                date = Set.find('date')
                test_date = date.get('stream:timestamp')
                date_x_target.append(test_date)
                sensor = Set.find('string')
                sensor_value = sensor.get('stream:value')
                value_x_target.append(sensor_value)

            date_y_target = []
            value_y_target = []
            for Set in Data_Y_Target:
                date = Set.find('date')
                test_date = date.get('stream:timestamp')
                date_y_target.append(test_date)
                sensor = Set.find('string')
                sensor_value = sensor.get('stream:value')
                value_y_target.append(sensor_value)

            date_z_target = []
            value_z_target = []
            for Set in Data_Z_Target:
                date = Set.find('date')
                test_date = date.get('stream:timestamp')
                date_z_target.append(test_date)
                sensor = Set.find('string')
                sensor_value = sensor.get('stream:value')
                value_z_target.append(sensor_value)

            main_frame = pd.DataFrame(list(
                zip(date_x_current, value_x_current, value_y_current, value_z_current, value_x_target, value_y_target,
                    value_z_target)), columns=['timestamp', 'VALUE_X_CURRENT', 'VALUE_Y_CURRENT',
                                               'VALUE_Z_CURRENT', 'VALUE_X_TARGET',
                                               'VALUE_Y_TARGET', 'VALUE_Z_TARGET'])

            main_frame.to_csv("./Data/csv/" + str(filename) + ".csv", sep=",")


def createOverview():
    # Dritte Stufe: Erstellung einer Übersichtsdatei basierend auf den erstellten Csv-Dateien
    Main_data = pd.DataFrame(columns=['id', 'name', 'timestamp (START)', 'timestamp (END)', 'data_length'])
    root = os.getcwd() + '/data/csv'
    source_id = 0
    for csv in Path(root).rglob('*.csv'):
        source_id += 1
        data = pd.read_csv(csv, index_col=0)
        f_stamp = data.iloc[0, 0]
        data_length = len(data)
        e_stamp = data.iloc[data_length - 1, 0]
        filename = str(os.path.basename(csv)).split(".")[0]
        data_row = [[source_id, filename, f_stamp, e_stamp, data_length]]
        new_row = pd.DataFrame(data_row, columns=['id', 'name', 'timestamp (START)', 'timestamp (END)', 'data_length'])

        Main_data = pd.concat([Main_data, new_row], axis=0)
    Main_data.to_excel(root + '/Main_Data.xlsx')


def identifyTasks():
    # Vierte Stufe: Extrahierung der IDs und der zugehörigen Tasks aus der MainProcess xes
    file_xes = os.getcwd() + '/Data/MainProcess.xes'
    file_xml = os.getcwd() + '/Data/Converted_Data/MainProcess.xml'
    with open(file_xes, "r") as MP:
        content = MP.read()

        with open("./Data/Converted_Data/MainProcess.xml", "w") as output:
            output.write(content)
            output.close()

    with open(file_xml, "r") as file:
        root = os.getcwd() + '/data/csv'
        dataframe = pd.read_excel(root + '/Main_Data.xlsx', index_col=0)
        subprocessID = dataframe['name'].to_list()
        data = file.read()
        XML_Data = BeautifulSoup(data, "xml")
        id_list = []
        task_list = []
        record_process_id = False
        record_task = False
        tree = ET.parse('./Data/Converted_Data/MainProcess.xml')
        for root_element in tree.iter():
            content = root_element.attrib.values()
            for element in content:

                if str(element) == 'SubProcessID':
                    record_process_id = True
                elif record_process_id:
                    id_list.append(str(element))
                    record_process_id = False
                elif str(element) == 'current_task':
                    record_task = True
                elif record_task:
                    task_list.append(str(element))
                    record_task = False

        list_of_tuples = list(zip(id_list, task_list))
        dataframe = pd.DataFrame(list_of_tuples, columns=['id', 'task'])
        dataframe.to_csv(root + '/extracted_tasks.csv', index=False)


def MatchOverviewWithTasks():
    # Fünfte Stufe: Kombinierung der extrahierten Tasks mit der erstellten Overview_Datei
    Overview = pd.read_excel(os.getcwd() + '/data/csv/Main_Data.xlsx', index_col=0)
    Tasks = pd.read_csv(os.getcwd() + '/data/csv/extracted_tasks.csv')

    result = pd.concat([Overview.set_index('name'), Tasks.set_index('id')], axis=1, join='inner').reset_index()
    result.to_excel(os.getcwd() + '/data/csv/Main_Data_with_Tasks.xlsx', index=False)


def CreateDataSetsPerTask():
    # Sechste Stufe: Erstellung der Datensätze basierend auf der ergänzten Overview-Datei
    overview = pd.read_excel(os.getcwd() + '/data/csv/Main_Data_with_Tasks.xlsx')
    task_set = set(overview['task'].to_list())
    task_nr = 1
    for task in task_set:
        task_dataframe = pd.DataFrame(columns=['timestamp', 'VALUE_X_CURRENT', 'VALUE_Y_CURRENT',
                                               'VALUE_Z_CURRENT', 'VALUE_X_TARGET',
                                               'VALUE_Y_TARGET', 'VALUE_Z_TARGET'])
        source_frame = overview[overview['task'] == task]
        source_list = source_frame['index'].to_list()
        for source in source_list:
            sensor_id = 0
            for row in range(0, len(overview), 1):
                if str(overview.iat[row, 0]) == str(source):
                    sensor_id = str(overview.iat[row, 1])
                    break
            source_dataframe = pd.read_csv(os.getcwd() + '/data/csv/' + str(source) + '.csv')
            source_dataframe['sensor_id'] = sensor_id
            task_dataframe = pd.concat([task_dataframe, source_dataframe], axis=0)

        task_dataframe.to_csv(os.getcwd() + '/data/csv/task_' + str(task_nr) + '.csv')
        task_nr += 1


def CreateTestAndTrainingsData():
    try:
        # Todo: Hier Parameter einstellen
        selected_task = 1  # Possible to choose between 1 - 5 (due to five different identified tasks)
        amount_training = 18
        amount_test = 2


        dataset = pd.read_csv(os.getcwd() + '/data/csv/task_' + str(selected_task) + '.csv', index_col=0)
        task_ids = set(dataset['sensor_id'].values)
        task_amount = len(task_ids)
        if amount_training > task_amount or amount_test > task_amount:
            raise "You have selected more datasets for test/training than are available."
        selected_train_ids = randomTaskSelector(amount_training, task_ids)
        selected_test_ids = randomTaskSelector(amount_test, task_ids)

        trainings_dataframe = generateTaskDataFrame(dataset, selected_train_ids)

        test_dataframe = generateTaskDataFrame(dataset, selected_test_ids)

        path = Path(__file__).parent.parent

        trainings_dataframe.to_csv(str(path) + '/transformer/source/task_train.csv')
        test_dataframe.to_csv(str(path) + '/transformer/source/task_test.csv')

    except Exception as e:
        logging.error("Failed to generate test and trainings data. Error-Log: " + str(e))


def randomTaskSelector(length, task_list):
    nr_list = []
    for i in range(0, length, 1):
        value_complete = False
        while not value_complete:
            random_value = random.randrange(0, 46)
            selected_task = list(task_list)[random_value]
            if selected_task not in nr_list:
                nr_list.append(selected_task)
                value_complete = True
    return nr_list


def generateTaskDataFrame(base_dataset, selected_ids):
    try:
        selected_dataframe = pd.DataFrame(columns=['timestamp', 'VALUE_X_CURRENT', 'VALUE_Y_CURRENT',
                                                   'VALUE_Z_CURRENT', 'VALUE_X_TARGET',
                                                   'VALUE_Y_TARGET', 'VALUE_Z_TARGET', 'Unnamed: 0', 'sensor_id'])
        for entry in selected_ids:
            dataframe = base_dataset.loc[base_dataset['sensor_id'] == entry]
            selected_dataframe = pd.concat([selected_dataframe, dataframe], axis=0)
        return selected_dataframe
    except Exception as e:
        logging.error("Failed to generate the required dataframe. Error-Log: " + str(e))


if __name__ == '__main__':
    CreateTestAndTrainingsData()
