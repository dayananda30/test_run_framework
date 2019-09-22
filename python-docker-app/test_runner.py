import logging as logger
import sys

from publisher import publish_test
from postgre_models.db import DBSession
from functions import copy

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
        2.	Configuration update
        3.	Validation/Health Check
        4.      Initial Setup
        """)

        if int(option) == 1:
            print("##############################################")
            print("You have selected Upgrade option \n")
            options = 'abcde'
            while True:
                initial_setup_options = input("""Please provide test scripts path:

                Example: Following format input is expected
                        /home/test/test_scripts
                or Default path will be selected from software.
                """)
                initial_setup_options = initial_setup_options.split()

                if initial_setup_options:
                    #User input
                    print(initial_setup_options)
                    logger.info("#############################################\n")
                    logger.info("###############END###########################\n")
                else:
                    #Use default path from software.
                    src_path = current_dir+"/test_scripts"
                    print(current_dir)
                db = DBSession()
                test_id = db.create_entry()

                dest_path = current_dir+"/mnt/test_run_"+str(test_id)
                copy(src_path, dest_path)
                publish_test(test_id)
                print("Test execution started and test id - ", test_id)

                break
        elif int(option) == 4:
            print("##############################################")
            print("You have selected Initial Configuration option \n")
            logger.info("###############START#########################")

            logger.info("###############END###########################\n")
            sleep(2)

            options = 'ab'
            while True:
                initial_setup_options = input("""Choose one or more options separated by space for Initial configuration:
                a.	Salt CherryPy
                b.	Bridgeburner client

                Example: For Salt CherryPy and Bridgeburner client configuration, pass the following input
                        a b
                """)
                initial_setup_options = initial_setup_options.split()
                resume_flag = 1
                for item in initial_setup_options:
                    if item in options:
                        continue
                    else:
                        resume_flag = 0
                if resume_flag:
                    for item in initial_setup_options:
                        if item == 'a':
                            logger.info("###############START#########################")
                            logger.info('Salt CherryPy is installed and configured')
                            logger.info("###############END###########################\n")
                        if item == 'b':
                            logger.info("###############START#########################")
                            logger.info("###############END###########################\n")

                    break
        elif int(option) == 2:
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

        elif int(option) == 3:
            logger.info("###############START#########################")

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
