import logging

logging.basicConfig(filemode='logfiles/logfile.log', level=logging.DEBUG)


def main():
    a = 10
    b = 25

    logging.debug(f'a: {a} + b: {b}')
    logging.debug(f'= sum: {a+b}')

if __name__ == "__main__":
    main()