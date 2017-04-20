"""Records statistics module."""

from ccollab2eeplatform import utils


class RecordsStatistics:
    """Review records statistics class.

    Args:
        records: A list of record.
    """

    def __init__(self, records):
        self._records = records

    @property
    def count(self):
        """Records count."""
        return len(self._records)

    @property
    def total_defect(self):
        """Defects count."""
        return sum(record.defect_count for record in self._records)

    @property
    def total_comment(self):
        """Total comments."""
        return sum(record.comment_count for record in self._records)

    @property
    def total_loc(self):
        """Total LOC."""
        return sum(record.loc for record in self._records)

    @property
    def total_loc_changed(self):
        """Total LOC changed."""
        return sum(record.loc_changed for record in self._records)

    @property
    def comment_density_uploaded(self):
        """Code comment density(uploaded).
        
        Formula:
        CommentDensity(uploaded) = (total_comment * 1000) / total_loc
        """
        try:
            return (self.total_comment * 1000) / self.total_loc
        except ZeroDivisionError:
            return 0

    @property
    def comment_density_changed(self):
        """Code comment density(changed).
        
        Formula:
        CommentDensity(changed) = (total_comment * 1000) / total_loc_changed
        """
        try:
            return (self.total_comment * 1000) / self.total_loc_changed
        except ZeroDivisionError:
            return 0

    @property
    def defect_density_uploaded(self):
        """Defect density(uploaded).
        
        Formula:
        DefectDensity(uploaded) = (total_defect * 1000) / total_loc
        """
        try:
            return (self.total_defect * 1000) / self.total_loc
        except ZeroDivisionError:
            return 0

    @property
    def defect_density_changed(self):
        """Defect density(changed).
        
        Formula:
        DefectDensity(changed) = (total_defect * 1000) / total_loc_changed
        """
        try:
            return (self.total_defect * 1000) / self.total_loc_changed
        except ZeroDivisionError:
            return 0

    @property
    def total_person_time_in_second(self):
        """Total person time in second."""
        return sum(
            record.total_person_time_in_second for record in self._records
        )

    @property
    def total_person_time_in_hour(self):
        """Total person time in hour."""
        return self.total_person_time_in_second / (60 * 60)

    @property
    def inspection_rate(self):
        """Inspection rate.
        
        Formula:
        InspectionRate = (LOCC) / (TotalPersonTimeInHour * 1000)
        """
        try:
            return (self.total_loc_changed
                   / (self.total_person_time_in_hour * 1000))
        except ZeroDivisionError:
            return 0
