import argparse
from datetime import date, timedelta

from ccollab2eeplatform import utils
from ccollab2eeplatform.ccollab import review
from ccollab2eeplatform.ccollab import defect
from ccollab2eeplatform.log import logger
from ccollab2eeplatform.manager import RecordManager


def main():
    """The main routine."""
    parser = argparse.ArgumentParser(
        description='Extract data from Code Collaborator to EagleEye Platform')

    parser.add_argument('--task-id',
                        help="the task id for this job in EagleEye-Platform")
    parser.add_argument('--start-date',
                        help="review creation start date in yyyy-MM-dd")
    parser.add_argument('--end-date',
                        help="review creation end date in yyyy-MM-dd")

    args = parser.parse_args()

    # Process EagleEye Platform task
    if args.task_id is None:
        logger.warn('Cannot update task state to EagleEye Platform, '
                    'because no task id provided on command line.')

    # End date defaults to today
    if args.end_date is None:
        review_end_date = date.today().isoformat()
    else:
        try:
            review_end_date = utils.to_isoformat(args.end_date)
        except Exception as e:
            logger.error('Error occurred parsing end date. Details: %s' % e)
            return 1

    # Start date defaults to one year before end date
    if args.start_date is None:
        try:
            delta = timedelta(days=365)
            parts = [int(part) for part in review_end_date.split('-')]
            start = date(parts[0], parts[1], parts[2]) - delta
            review_start_date = start.isoformat()
        except Exception as e:
            logger.error('Error occurred setting start date. Details: %s' % e)
            return 1
    else:
        try:
            review_start_date = utils.to_isoformat(args.start_date)
        except Exception as e:
            logger.error('Error occurred parsing start date. Details: %s' % e)
            return 1

    logger.info('Set review creation start date: "%s"' % review_start_date)
    logger.info('Set review creation end date: "%s"' % review_end_date)

    # Download review data
    review_records = review.fetch_review_records(review_start_date,
                                                 review_end_date)
    if len(review_records) == 0:
        logger.warn('No review records.')

    # Download defect data
    defect_records = defect.fetch_defect_records(review_start_date,
                                                 review_end_date)
    if len(defect_records) == 0:
        logger.warn('No defect records.')

    record_manager = RecordManager(review_records=review_records,
                                   defect_records=defect_records)

    # Start to process all the charts.
    record_manager.process(review_start_date, review_end_date)

    logger.info('Completed.')
    return 0
