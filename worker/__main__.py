import logging
from worker.hh_parser import run_parser

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('parser is running')

    run_parser(delay=3600)


if __name__ == '__main__':
    main()
