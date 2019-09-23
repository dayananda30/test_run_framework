import logging as logger
import sys
import os

from publisher import publish_test
from postgre_models.db import DBSession
from functions import copy
from prettytable import PrettyTable

from os.path import dirname, abspath, join, exists
from argparse import ArgumentParser
from time import sleep

current_dir = dirname(abspath(__file__))

sys.path.append(current_dir)

def main(csv_files_path, local_download_path):

    logger.info("###############START#########################")

#    path_of_deployment_yaml = join(current_dir, 'config', 'deployment')
#    yaml_file_list = list_of_yaml_files(path_of_deployment_yaml)
    logger.info('Converted deployment CSV input to yaml format')

    logger.info("###############END###########################\n")
    sleep(2)

    while True:
        option = input ("""Please choose one option from following:
        1.      Test Run	
        2.      Show all Test results	
        3.      Get detailed log for the test run	
        4.      Initial Setup
        """)

        if int(option) == 1:
            print("##############################################")
            print("You have selected Test Run option \n")
            while True:
                sub_option = input("""Please provide test scripts path:

                Example: Following format input is expected
                        /home/test/test_scripts
                or Default path will be selected from software.
                """)

                if sub_option:
                    #User input
                    if os.path.isdir(sub_option):
                        src_path =sub_option
                    else:
                        print("Please check script path - {}".format(sub_option))
                        continue
                else:
                    #Use default path from software.
                    src_path = current_dir+"/test_scripts"
                    print(current_dir)
                db = DBSession()
                test_id = db.create_entry()
                db.session_close()
                dest_path = current_dir+"/mnt/test_run_"+str(test_id)
                copy(src_path, dest_path)
                publish_test(test_id)
                print("Test execution started and test id - ", test_id)

                break

        elif int(option) == 2:
            print("##############################################")
            print("You have selected Show all Test results option \n")
            db = DBSession()
            list_objs = db.get_all_records()
            db.session_close()

            x = PrettyTable()

            x.field_names = ["Test Id", "Environment", "Test", "Created at", "Started at", "Finished at", "Status"]
            for obj in list_objs:
                x.add_row([obj['id'], obj['environment'], obj['test'], obj['created_at'],
                          obj['started_at'], obj['finished_at'], obj['status']])
            print(x)
            break

        elif int(option) == 3:
            print("##############################################")
            print("You have selected Get detailed log for the test run option \n")
            sleep(1)

            while True:
                sub_option = input("""Please provide test run id:

                Example: 
                        12 
                """)
                if not sub_option.isdigit(): 
                    print("Please enter valid test run id.")
                    continue

                db = DBSession()
                obj = db.get_one_record(sub_option)
                db.session_close()
                
                if type(obj) == str:
                    print(obj)
                else:
                    print(obj['logs'])
                break
        elif int(option) == 4:
            options = 'abcd'
            print("##############################################")
            print("You have selected configuration update (YAML update) option \n")
            while True:
                yaml_update = input("""Choose one or more options separated by space for configuration update:
                  a.	Middleware
                  b.	TAMS
                  c.	Worker
                  d.	All above
                  e.    Bridgeburvner Certificate

                  Example: For Middleware and worker configuration update, pass the following input
                                a c
                  """)
                yaml_update = yaml_update.split()
                resume_flag = 1
                for item in yaml_update:
                    if item in options:
                        continue
                    else:
                        resume_flag = 0

                if resume_flag:
                    for item in yaml_update:
                        if item == 'a' or item == 'd':
                            logger.info("###############START#########################")

                            logger.info("Middleware configuration update is started \n")
                            logger.info("###############END###########################\n")

                        if item == 'b' or item == 'd':
                            logger.info("###############START#########################")
                            logger.info("TAMS configuration update is started \n")
                            logger.info("###############END###########################\n")

                    break
                else:
                    print('Sorry, that was incorrect input')
                    continue

        else:
            print('Sorry, that was incorrect input')
            continue
        resume_flag = 1

        logger.info("###############START#########################")
        logger.info("END OF TEST MODULES")

        logger.info("###############END###########################\n")

        break


if __name__ == '__main__':

    parser = ArgumentParser(description='Arguments for upgrading/config update/validation')
    parser.add_argument('-csv', '--csv_path',
                        default=join(current_dir, 'config', 'csv_files'),
                        action='store',
                        help='Deployment CSV file location')
    parser.add_argument('-b', '--bundles',
                        default=join(current_dir, 'config', 'bundles'),
                        action='store',
                        help='Location of the dir where all bundles need to download')

    args = parser.parse_args()
    main(args.csv_path, args.bundles)